"""
knowledge_graph.py
==================
Runtime module for the Boiler Knowledge Graph.

Load once at MCP server startup:
    from knowledge_graph import load_graph
    KG = load_graph("boiler_kg.json")

Then query:
    KG.trace_stream("Steam")
    KG.get_upstream_sensors("TE_8332A")
    KG.find_process_path("primary fan", "steam outlet")
"""

import json, os, re
from typing import Any
import networkx as nx


class BoilerKnowledgeGraph:
    """Encapsulates the boiler process-flow graph and all query operations."""

    def __init__(self, G: nx.MultiDiGraph, stream_paths: dict, stream_descriptions: dict):
        self.G = G
        self.stream_paths        = stream_paths         # {"Steam": [...], ...}
        self.stream_descriptions = stream_descriptions  # {"Steam": "...", ...}

        # Build reverse lookup: tag_name -> equipment node_id
        self._sensor_to_equip: dict[str, str] = {}
        for u, v, attrs in G.edges(data=True):
            if attrs.get("edge_type") == "PART_OF":
                if G.nodes[u].get("node_type") == "Sensor":
                    self._sensor_to_equip[u] = v

        # Cache the unfiltered FLOW subgraph (graph is static after load)
        self._flow_subgraph_cache = self._build_flow_subgraph()

    # ── Internal helpers ────────────────────────────────────────────────────

    def _normalize(self, text: str) -> str:
        t = text.lower().strip()
        for w in [" the ", " of ", " in ", " at ", " a ", " an ", " and ", " or "]:
            t = t.replace(w, " ")
        return t.strip()

    def _fuzzy_find(self, query: str, node_types: list[str]) -> list[str]:
        """Return node_ids matching query string, filtered by node_type."""
        q = self._normalize(query)
        exact, partial = [], []
        for node_id, attrs in self.G.nodes(data=True):
            if attrs.get("node_type") not in node_types:
                continue
            name   = self._normalize(attrs.get("name", ""))
            nid    = node_id.lower().replace("_", " ")
            aliases = [self._normalize(a) for a in attrs.get("aliases", [])]
            if q == name or q == nid or q in aliases:
                exact.append(node_id)
            elif q in name or q in nid or any(q in a for a in aliases) or any(a in q for a in aliases):
                partial.append(node_id)
        return exact if exact else partial

    def _node_info(self, node_id: str) -> dict:
        """Return a clean serializable dict for a node."""
        attrs = dict(self.G.nodes[node_id])
        return attrs

    def _sensor_info(self, tag: str) -> dict:
        """Return concise sensor dict for tool output."""
        a = self.G.nodes.get(tag, {})
        return {
            "tag_name":    tag,
            "description": a.get("description", ""),
            "units":       a.get("units", ""),
            "sensor_type": a.get("sensor_type", ""),
            "normal_min":  a.get("normal_min"),
            "normal_max":  a.get("normal_max"),
            "is_primary_kpi": a.get("is_primary_kpi", False),
        }

    def _equip_info(self, node_id: str) -> dict:
        """Return concise equipment dict for tool output."""
        a = self.G.nodes.get(node_id, {})
        sensors = self.get_equipment_sensors(node_id)
        return {
            "node_id":         node_id,
            "name":            a.get("name", node_id),
            "equipment_class": a.get("equipment_class", ""),
            "side":            a.get("side"),
            "criticality":     a.get("criticality", ""),
            "process_streams": a.get("process_streams", []),
            "description":     a.get("description", ""),
            "sensors":         sensors,
        }

    def _build_flow_subgraph(self, stream: str = None) -> nx.MultiDiGraph:
        """Build a subgraph containing only FLOW edges (optionally filtered by stream)."""
        edges = [
            (u, v, k) for u, v, k, d in self.G.edges(keys=True, data=True)
            if d.get("edge_type") == "FLOW" and (stream is None or d.get("stream") == stream)
        ]
        sg = nx.MultiDiGraph()
        sg.add_nodes_from(self.G.nodes(data=True))
        sg.add_edges_from(edges)
        return sg

    def _get_flow_subgraph(self, stream: str = None) -> nx.MultiDiGraph:
        """Return the FLOW subgraph, using the cached version when no stream filter is applied."""
        if stream is None:
            return self._flow_subgraph_cache
        return self._build_flow_subgraph(stream)

    # ── Equipment & sensor lookup ──────────────────────────────────────────

    def find_equipment(self, query: str) -> list[dict]:
        """Find equipment nodes matching a natural-language query."""
        matches = self._fuzzy_find(
            query,
            ["Equipment", "Boundary", "System", "ControlLoop"]
        )
        return [self._equip_info(m) if self.G.nodes[m].get("node_type") == "Equipment"
                else self._node_info(m)
                for m in matches]

    def get_equipment_sensors(self, equipment_id: str) -> list[dict]:
        """Return all sensors attached to an equipment node."""
        return [
            self._sensor_info(u)
            for u, v, attrs in self.G.in_edges(equipment_id, data=True)
            if attrs.get("edge_type") == "PART_OF"
            and self.G.nodes[u].get("node_type") == "Sensor"
        ]

    def get_sensor_equipment(self, tag_name: str) -> dict | None:
        """Return the equipment node that a sensor belongs to."""
        equip_id = self._sensor_to_equip.get(tag_name)
        if equip_id:
            return self._equip_info(equip_id)
        return None

    # ── Stream traversal ───────────────────────────────────────────────────

    def trace_stream(self, stream_name: str) -> dict:
        """
        Return the ordered process path for a named stream, with sensors at each stop.
        stream_name: e.g. "Steam", "FlueGas", "PrimaryAir"
        """
        # Fuzzy match stream name
        matched = None
        q = stream_name.lower().replace(" ", "").replace("_", "")
        for s in self.stream_paths:
            if q in s.lower().replace(" ", "") or s.lower().replace(" ", "") in q:
                matched = s
                break
        if matched is None:
            available = list(self.stream_paths.keys())
            return {"error": f"Unknown stream '{stream_name}'. Available: {available}"}

        path_def  = self.stream_paths[matched]
        desc      = self.stream_descriptions.get(matched, "")
        steps = []
        step_num = 1
        for entry in path_def:
            if isinstance(entry, list):
                # Parallel branches
                for node_id in entry:
                    node_attrs = self.G.nodes.get(node_id, {})
                    sensors = (self.get_equipment_sensors(node_id)
                               if node_attrs.get("node_type") == "Equipment" else [])
                    steps.append({
                        "step": step_num,
                        "parallel_branch": True,
                        "node_id":   node_id,
                        "name":      node_attrs.get("name", node_id),
                        "node_type": node_attrs.get("node_type", ""),
                        "sensors":   sensors,
                    })
                step_num += 1
            else:
                node_attrs = self.G.nodes.get(entry, {})
                sensors = (self.get_equipment_sensors(entry)
                           if node_attrs.get("node_type") in ("Equipment", "Boundary") else [])
                steps.append({
                    "step":     step_num,
                    "parallel_branch": False,
                    "node_id":  entry,
                    "name":     node_attrs.get("name", entry),
                    "node_type":node_attrs.get("node_type", ""),
                    "sensors":  sensors,
                })
                step_num += 1

        return {
            "stream":      matched,
            "description": desc,
            "step_count":  step_num - 1,
            "path":        steps,
        }

    def get_stream_at_equipment(self, equipment_id: str) -> list[str]:
        """Return which process streams pass through an equipment node."""
        return self.G.nodes.get(equipment_id, {}).get("process_streams", [])

    # ── Upstream / downstream traversal ───────────────────────────────────

    def get_upstream_equipment(self, node_id: str, stream: str = None, max_hops: int = 15) -> list[dict]:
        """Return upstream equipment ordered by distance (closest first)."""
        sg = self._get_flow_subgraph(stream)
        if node_id not in sg:
            # Try fuzzy match
            matches = self._fuzzy_find(node_id, ["Equipment", "Sensor"])
            if not matches:
                return []
            node_id = matches[0]
            if node_id not in sg:
                # Use sensor's equipment
                equip = self._sensor_to_equip.get(node_id)
                node_id = equip if equip else node_id

        # BFS on reversed graph
        rev = sg.reverse()
        visited, result = set(), []
        queue = [(node_id, 0)]
        while queue:
            current, depth = queue.pop(0)
            if current in visited or depth > max_hops:
                continue
            visited.add(current)
            if current != node_id and self.G.nodes[current].get("node_type") in ("Equipment", "Boundary"):
                info = self._equip_info(current) if self.G.nodes[current].get("node_type") == "Equipment" else self._node_info(current)
                info["hop_distance"] = depth
                result.append(info)
            for neighbor in rev.successors(current):
                if neighbor not in visited:
                    queue.append((neighbor, depth + 1))
        return result

    def get_upstream_sensors(self, node_id: str) -> list[dict]:
        """
        Return all sensors on upstream equipment, ordered by hop distance.
        node_id may be a tag name or equipment node_id.
        """
        # Resolve to equipment if sensor
        start = node_id
        if self.G.nodes.get(node_id, {}).get("node_type") == "Sensor":
            start = self._sensor_to_equip.get(node_id, node_id)

        upstream_equip = self.get_upstream_equipment(start)
        results = []
        seen = set()
        for equip in upstream_equip:
            equip_id  = equip["node_id"]
            hop       = equip.get("hop_distance", "?")
            streams   = self.G.nodes.get(equip_id, {}).get("process_streams", [])
            for sensor in self.get_equipment_sensors(equip_id):
                tag = sensor["tag_name"]
                if tag not in seen:
                    seen.add(tag)
                    results.append({**sensor, "equipment": equip_id,
                                    "equipment_name": equip.get("name", equip_id),
                                    "hop_distance": hop, "streams": streams})
        return results

    # ── Path finding ───────────────────────────────────────────────────────

    def find_process_path(self, from_query: str, to_query: str) -> dict:
        """Find the physical process path between two equipment nodes (FLOW edges only)."""
        from_matches = self._fuzzy_find(from_query, ["Equipment","Boundary","System"])
        to_matches   = self._fuzzy_find(to_query,   ["Equipment","Boundary","System","Sensor"])

        if not from_matches:
            return {"error": f"Could not find node matching '{from_query}'"}
        if not to_matches:
            return {"error": f"Could not find node matching '{to_query}'"}

        from_id = from_matches[0]
        to_id   = to_matches[0]

        # Resolve sensor to equipment
        if self.G.nodes[to_id].get("node_type") == "Sensor":
            to_id = self._sensor_to_equip.get(to_id, to_id)

        # Search FLOW-only subgraph to return the physical process path
        flow_sg = self._get_flow_subgraph()

        try:
            path = nx.shortest_path(flow_sg, from_id, to_id)
        except nx.NetworkXNoPath:
            # Try reversed (upstream direction)
            try:
                path = nx.shortest_path(flow_sg, to_id, from_id)
                path = list(reversed(path))
            except nx.NetworkXNoPath:
                return {"error": f"No physical process path found between '{from_id}' and '{to_id}'. "
                                 f"Try tracing streams with kg_trace_stream instead."}
        except nx.NodeNotFound as e:
            return {"error": str(e)}

        steps = []
        for i, node_id in enumerate(path):
            attrs    = self.G.nodes[node_id]
            sensors  = self.get_equipment_sensors(node_id) if attrs.get("node_type") == "Equipment" else []
            edge_info = {}
            if i < len(path) - 1:
                next_id = path[i + 1]
                for u, v, k, d in self.G.edges(node_id, keys=True, data=True):
                    if v == next_id and d.get("edge_type") == "FLOW":
                        edge_info = {"edge_type": d.get("edge_type",""), "stream": d.get("stream",""), "description": d.get("description","")}
                        break
            steps.append({
                "step":      i + 1,
                "node_id":   node_id,
                "name":      attrs.get("name", node_id),
                "node_type": attrs.get("node_type", ""),
                "sensors":   sensors,
                "edge_to_next": edge_info if i < len(path) - 1 else None,
            })

        result = {
            "from": from_id,
            "to":   to_id,
            "hop_count": len(path) - 1,
            "path": steps,
        }
        if len(from_matches) > 1:
            result["also_matched_from"] = [self.G.nodes[m].get("name", m) for m in from_matches[1:]]
        if len(to_matches) > 1:
            result["also_matched_to"] = [self.G.nodes[m].get("name", m) for m in to_matches[1:]]
        return result

    # ── Sensor relationships ───────────────────────────────────────────────

    def get_related_sensors(self, tag_name: str) -> dict:
        """Return sensors related to tag_name: co-located, symmetric pair, same system."""
        equip_id = self._sensor_to_equip.get(tag_name)
        if not equip_id:
            # Try fuzzy match as sensor tag
            matches = self._fuzzy_find(tag_name, ["Sensor"])
            if matches:
                tag_name = matches[0]
                equip_id = self._sensor_to_equip.get(tag_name)
        if not equip_id:
            return {"error": f"No equipment found for sensor '{tag_name}'"}

        # Co-located sensors (same equipment, different tag)
        co_located = [s for s in self.get_equipment_sensors(equip_id) if s["tag_name"] != tag_name]

        # Symmetric pair
        sym_partner = None
        for u, v, d in self.G.out_edges(tag_name, data=True):
            if d.get("edge_type") == "SYMMETRIC_PAIR":
                sym_partner = self._sensor_info(v) if self.G.nodes[v].get("node_type") == "Sensor" else {"node_id": v}
                break

        # Symmetric equipment partner's sensors
        equip_sym_sensors = []
        for u, v, d in self.G.out_edges(equip_id, data=True):
            if d.get("edge_type") == "SYMMETRIC_PAIR":
                equip_sym_sensors = self.get_equipment_sensors(v)
                break

        # Same system sensors
        system_id = None
        for u, v, d in self.G.out_edges(equip_id, data=True):
            if d.get("edge_type") == "PART_OF" and self.G.nodes[v].get("node_type") == "System":
                system_id = v
                break
        same_system_sensors = []
        if system_id:
            # All equipment in same system
            for u, v, d in self.G.in_edges(system_id, data=True):
                if d.get("edge_type") == "PART_OF" and u != equip_id:
                    same_system_sensors.extend(self.get_equipment_sensors(u))

        # Control loop membership
        control_loop = self.get_control_loop_for_sensor(tag_name)

        return {
            "sensor": self._sensor_info(tag_name),
            "equipment": self._equip_info(equip_id),
            "co_located_sensors": co_located,
            "symmetric_pair_sensor": sym_partner,
            "symmetric_pair_equipment_sensors": equip_sym_sensors,
            "same_system_sensors": same_system_sensors,
            "control_loop": control_loop,
        }

    # ── System queries ─────────────────────────────────────────────────────

    def get_system_sensors(self, system_query: str) -> dict:
        """Return all sensors grouped by equipment within a system."""
        matches = self._fuzzy_find(system_query, ["System"])
        if not matches:
            available = [d.get("name", n) for n, d in self.G.nodes(data=True) if d.get("node_type") == "System"]
            return {"error": f"No system found matching '{system_query}'. Available: {available}"}

        system_id   = matches[0]
        system_name = self.G.nodes[system_id].get("name", system_id)
        equip_groups = []
        for u, v, d in self.G.in_edges(system_id, data=True):
            if d.get("edge_type") == "PART_OF" and self.G.nodes[u].get("node_type") == "Equipment":
                sensors = self.get_equipment_sensors(u)
                equip_groups.append({
                    "equipment_id":    u,
                    "equipment_name":  self.G.nodes[u].get("name", u),
                    "equipment_class": self.G.nodes[u].get("equipment_class", ""),
                    "criticality":     self.G.nodes[u].get("criticality", ""),
                    "sensors":         sensors,
                })
        # Sort by criticality
        order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
        equip_groups.sort(key=lambda e: order.get(e["criticality"], 9))

        result = {
            "system_id":   system_id,
            "system_name": system_name,
            "description": self.G.nodes[system_id].get("description", ""),
            "equipment_count": len(equip_groups),
            "total_sensors": sum(len(e["sensors"]) for e in equip_groups),
            "equipment": equip_groups,
        }
        if len(matches) > 1:
            result["also_matched"] = [self.G.nodes[m].get("name", m) for m in matches[1:]]
        return result

    # ── Control loop queries ───────────────────────────────────────────────

    def get_control_loop_for_sensor(self, tag_name: str) -> dict | None:
        """Return control loop info if this sensor is a feedback or actuator in any loop."""
        result = {"feedback_in": [], "actuator_in": []}
        for u, v, d in self.G.out_edges(tag_name, data=True):
            etype = d.get("edge_type")
            if etype == "FEEDBACK_TO" and self.G.nodes[v].get("node_type") == "ControlLoop":
                result["feedback_in"].append(self._node_info(v))
            elif etype == "ACTUATED_BY":
                pass  # ACTUATED_BY goes loop→sensor, not sensor→loop
        for u, v, d in self.G.in_edges(tag_name, data=True):
            if d.get("edge_type") == "ACTUATED_BY" and self.G.nodes[u].get("node_type") == "ControlLoop":
                result["actuator_in"].append(self._node_info(u))
        if result["feedback_in"] or result["actuator_in"]:
            return result
        return None

    def get_kpi_influencers(self) -> list[dict]:
        """Return all sensors with AFFECTS_KPI edges toward steam_outlet, sorted by hop distance."""
        sensors = []
        seen = set()
        for u, v, d in self.G.in_edges("steam_outlet", data=True):
            if d.get("edge_type") == "AFFECTS_KPI" and self.G.nodes[u].get("node_type") == "Sensor":
                if u not in seen:
                    seen.add(u)
                    info = self._sensor_info(u)
                    equip_id = self._sensor_to_equip.get(u)
                    info["equipment"] = equip_id
                    sensors.append(info)
        return sensors

    def list_streams(self) -> list[dict]:
        """Return all available streams with descriptions."""
        return [
            {"stream": s, "description": self.stream_descriptions.get(s, "")}
            for s in self.stream_paths
        ]


# ===========================================================================
# Factory function
# ===========================================================================

def load_graph(json_path: str) -> BoilerKnowledgeGraph:
    """Load a BoilerKnowledgeGraph from a boiler_kg.json file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(
            f"Knowledge graph not found at {json_path}. "
            "Run build_knowledge_graph.py first."
        )
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.node_link_graph(data, directed=True, multigraph=True, edges="links")

    stream_paths        = data.get("stream_paths", {})
    stream_descriptions = data.get("stream_descriptions", {})
    if not stream_paths:
        raise RuntimeError(
            "boiler_kg.json is missing 'stream_paths'. "
            "Run build_knowledge_graph.py to regenerate it."
        )

    return BoilerKnowledgeGraph(G, stream_paths, stream_descriptions)
