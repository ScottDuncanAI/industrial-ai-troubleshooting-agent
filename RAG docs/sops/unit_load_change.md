---
doc_id: unit_load_change
doc_type: sop
equipment: [primary_fan, secondary_fan, induced_draft_fan, furnace_lower_hearth, furnace_chamber, steam_outlet, primary_desuperheater]
tags: [FT_8301, FT_8302, TE_8332A, PTCA_8324, ZZQBCHLL, AIR_8301A, AIR_8301B, TV_8329ZC, YJJWSLL, PT_8313A]
title: Unit Load Change / Ramping Procedure
revision: 1.8
date: 2021-06-10
---

# Unit Load Change / Ramping Procedure

**Document No.:** ZJP-SOP-005  
**Revision:** 1.8  
**Effective Date:** 2021-06-10  
**Approved By:** Plant Engineering Manager  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler, operating range 40–100% load

---

## 1. Scope

This procedure governs intentional load changes (increases or decreases) during normal operation. The CFB boiler has inherently slower response than pulverized coal or gas-fired boilers due to the thermal mass of the bed. Maximum ramp rates are defined to protect pressure parts and avoid combustion instability.

**Operating Range:** 52–130 t/h steam flow (40–100% MCR)  
**Minimum Stable Load:** 52 t/h (40% MCR) — below this, bed stability degrades

---

## 2. Maximum Ramp Rates

| Direction | Max Ramp Rate | Notes |
|-----------|--------------|-------|
| Load increase | 5 t/h per minute (ZZQBCHLL) | Coal feed + air must increase together |
| Load decrease | 4 t/h per minute (ZZQBCHLL) | Air reduction must lag coal reduction |
| Emergency load reduction | 15 t/h per minute | May cause temperature excursion — monitor TE_8332A |

---

## 3. Load Increase Procedure

### 3.1 Pre-Increase Checks
- Confirm feedwater supply capable of supporting increased flow (deaerator level adequate)
- Confirm coal bunker level > 30%
- Confirm IDF has sufficient headroom (current speed < 85% maximum)
- Notify process area of impending load increase

### 3.2 Increase Sequence
1. If in automatic mode: enter new load setpoint in DCS load controller — ramp rate will be enforced automatically
2. If in manual: increase coal feed rate at ≤ 5 t/h per minute
3. **Lead air:** increase FT_8301 (primary air) 10–15% ahead of coal increase to prevent oxygen dip
4. Increase FT_8302 (secondary air) proportionally — typically 60:40 primary-to-secondary split at mid-load, shifting to 55:45 at high load
5. Monitor AIR_8301A and AIR_8301B — must not drop below 3.0% during ramp (indicates under-aeration)
6. IDF speed will automatically increase to maintain furnace pressure (PT_8313A target −120 Pa)
7. TE_8332A will initially dip during load increase — expect 5–10°C drop, recovering within 10 minutes
8. TV_8329ZC desuperheater may open more as steam temperature rises with load — verify YJJWSLL increases appropriately

### 3.3 Stabilization Check (at each 20 t/h increment)
- [ ] AIR_8301A and AIR_8301B: 3.5–5.5%
- [ ] PT_8313A: −100 to −150 Pa
- [ ] TE_8332A: 530–545°C (may lag by 5–10 minutes)
- [ ] PTCA_8324: 9.4–10.0 MPa

---

## 4. Load Decrease Procedure

### 4.1 Pre-Decrease Coordination
- Notify process area — confirm they can accept reduced steam supply or have alternate source
- If reducing to minimum load (< 60 t/h): notify supervisor

### 4.2 Decrease Sequence
1. Reduce coal feed at ≤ 4 t/h per minute
2. **Lag air:** hold FT_8301 and FT_8302 at current values for 60–90 seconds, then reduce proportionally
   - This prevents O2 dip during transition
3. As load drops, TE_8332A will tend to rise — TV_8329ZC will respond automatically if in auto
4. If approaching minimum load (ZZQBCHLL < 60 t/h): increase excess air target to 5.5–7% to improve bed stability
5. Monitor SXLTCYZ and SXLTCYY — bed ΔP should remain > 1.0 kPa

### 4.3 Minimum Load Operation (40–60% MCR)
- At minimum load, combustion is less stable — increased operator vigilance required
- AIR_8301A and AIR_8301B targets: 5.0–7.0% (higher excess air for stability)
- If ZZQBCHLL drops below 52 t/h, the boiler must be shut down — minimum stable load has been reached
- Do not hold at minimum load for more than 4 hours without supervisor approval

---

## 5. Coordinator Actions During Ramp

| Parameter | Increase Load | Decrease Load |
|-----------|--------------|---------------|
| Coal feed | Increase first | Decrease first |
| Primary air (FT_8301) | Increase 10% ahead | Decrease 60 sec after coal |
| Secondary air (FT_8302) | Proportional to primary | Proportional to primary |
| IDF (draft) | Auto adjusts | Auto adjusts |
| Desuperheater (TV_8329ZC) | Will open more | Will close |
| Feedwater flow | Will increase | Will decrease |

---

## 6. References
- ZJP-CTRL-001: Steam Temperature Control Loop Description
- ZJP-CTRL-002: Furnace Draft Control Loop Description
- ZJP-CTRL-003: Combustion Air / O2 Trim Control Loop Description
- ZJP-SOP-004: Emergency Shutdown Procedure
