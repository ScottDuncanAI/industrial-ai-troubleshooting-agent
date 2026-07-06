---
doc_id: safe_loto_primary_fan
doc_type: safety
equipment: [primary_fan]
tags: [FT_8301]
title: LOTO Procedure — Primary Fan (YFJ1)
revision: 1.3
date: 2021-08-01
---

# Lockout/Tagout Procedure: Primary Fan (YFJ1)

**Document No.:** ZJP-SAFE-002  
**Equipment:** Unit 1 Primary Fan (YFJ1)  
**Revision:** 1.3 | **Date:** 2021-08-01

---

## 1. Energy Sources

| Energy Source | Location | Isolation Device |
|--------------|----------|-----------------|
| Fan motor power (6 kV) | 6 kV switchgear Panel 3, Breaker B-01 | Circuit breaker — open and lock |
| Instrument air (outlet damper) | Damper actuator isolation valve | Quarter-turn valve — close and lock |
| Process air pressure (pressurized duct) | Outlet damper | Damper closed and mechanically blocked |
| Hot air (from preheater — if still warm) | Inlet isolation valve | Confirm temperature < 60°C before opening any ductwork |

---

## 2. Pre-Isolation

- [ ] Confirm primary fan stopped on DCS (motor status = STOPPED)
- [ ] Confirm FT_8301 = 0 m³/h
- [ ] Boiler must be shut down or primary fan isolated from furnace before LOTO — do not LOTO while furnace is live
- [ ] Notify shift supervisor

---

## 3. Isolation Sequence

1. HV electrician opens 6 kV breaker B-01 and locks — confirm OPEN, tag "DO NOT ENERGIZE"
2. Close instrument air to outlet damper actuator — lock with padlock
3. Close outlet damper manually — install mechanical block (wedge in damper frame or scaffold pipe)
4. Verify FT_8301 reads 0 m³/h after isolation (no air flow)
5. Sign isolation register

---

## 4. Verification

- [ ] Attempt DCS start — motor must not start
- [ ] FT_8301 = 0 m³/h confirmed
- [ ] All locks in place: minimum 2 locks

---

## 5. Restoration

1. Remove all mechanical blocks and personal padlocks
2. HV electrician closes 6 kV breaker
3. Remove danger tags; sign isolation register
4. Notify control room — fan available for restart
5. Rotation check before committing to full load

---

## 6. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.3 | 2021-08-01 | Added note on hot air temperature check before ductwork opening |
