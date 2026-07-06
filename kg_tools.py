"""
Knowledge graph tool implementations for the boiler MCP server.

Wraps the KnowledgeGraph class from knowledge_graph.py with lazy loading,
error handling, and the response shaping the MCP server needs.

The MCP server (historian_mcp_server.py) imports and calls these directly;
this module has no knowledge of MCP types or the server protocol.
"""

import os
from collections import defaultdict

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
_KG_JSON    = os.path.join(PROJECT_DIR, "boiler_kg.json")

_KG_INSTANCE = None


def _get_kg():
    global _KG_INSTANCE
    if _KG_INSTANCE is not None:
        return _KG_INSTANCE
    try:
        import knowledge_graph as _kg_mod
        _KG_INSTANCE = _kg_mod.load_graph(_KG_JSON)
        return _KG_INSTANCE
    except Exception as e:
        raise RuntimeError(
            f"Knowledge graph unavailable: {e}. "
            "Run build_knowledge_graph.py then restart the MCP server."
        )


# ---------------------------------------------------------------------------
# Tool implementations
# ---------------------------------------------------------------------------

def tool_kg_trace_stream(stream_name: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}
    return kg.trace_stream(stream_name)


def tool_kg_query_equipment(query: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}

    matches = kg.find_equipment(query)
    if not matches:
        return {
            "error": (
                f"No equipment found matching '{query}'. "
                "Try terms like 'furnace', 'economizer', 'induced draft fan', "
                "'cyclone', 'steam drum', 'desuperheater'."
            )
        }

    results = []
    for m in matches:
        node_id = m.get("node_id")
        if not node_id:
            results.append(m)
            continue

        upstream      = kg.get_upstream_equipment(node_id)[:5]
        downstream_sg = kg._get_flow_subgraph()
        downstream    = []
        for _, v, _ in downstream_sg.out_edges(node_id, data=True):
            node_attrs = kg.G.nodes.get(v, {})
            if node_attrs.get("node_type") in ("Equipment", "Boundary"):
                downstream.append({"node_id": v, "name": node_attrs.get("name", v)})

        results.append({
            **m,
            "process_streams": kg.get_stream_at_equipment(node_id),
            "upstream_equipment": [
                {
                    "node_id":      u["node_id"],
                    "name":         u.get("name", u["node_id"]),
                    "hop_distance": u.get("hop_distance"),
                }
                for u in upstream
            ],
            "downstream_equipment": downstream[:5],
        })

    return {"query": query, "matches": results}


def tool_kg_get_upstream_sensors(node_id: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}

    sensors = kg.get_upstream_sensors(node_id)
    if not sensors:
        return {
            "node_id":         node_id,
            "message":         f"No upstream sensors found for '{node_id}'. Verify the tag name or equipment name.",
            "upstream_sensors": [],
        }

    by_hop: dict = defaultdict(list)
    for s in sensors:
        by_hop[s.get("hop_distance", "?")].append(s)

    return {
        "node_id":                node_id,
        "total_upstream_sensors": len(sensors),
        "grouped_by_hop": {
            str(k): v
            for k, v in sorted(by_hop.items(), key=lambda x: (isinstance(x[0], str), x[0]))
        },
        "flat_list": sensors,
    }


def tool_kg_find_process_path(from_node: str, to_node: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}
    return kg.find_process_path(from_node, to_node)


def tool_kg_get_related_sensors(tag_name: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}
    return kg.get_related_sensors(tag_name)


def tool_kg_get_system_sensors(system_name: str) -> dict:
    try:
        kg = _get_kg()
    except RuntimeError as e:
        return {"error": str(e)}
    return kg.get_system_sensors(system_name)
