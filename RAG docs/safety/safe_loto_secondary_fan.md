---
doc_id: safe_loto_secondary_fan
doc_type: safety
equipment: [secondary_fan]
tags: [FT_8302]
title: LOTO Procedure — Secondary Fan (YFJ2)
revision: 1.3
date: 2021-08-01
---

# Lockout/Tagout Procedure: Secondary Fan (YFJ2)

**Document No.:** ZJP-SAFE-003  
**Equipment:** Unit 1 Secondary Fan (YFJ2)  
**Revision:** 1.3 | **Date:** 2021-08-01

---

## 1. Energy Sources

| Energy Source | Location | Isolation Device |
|--------------|----------|-----------------|
| Fan motor power (6 kV) | 6 kV switchgear Panel 3, Breaker B-02 | Circuit breaker — open and lock |
| Instrument air (outlet damper) | Damper actuator isolation valve | Quarter-turn valve — close and lock |
| Process air pressure (pressurized duct) | Outlet damper | Damper closed and blocked |
| Hot air (from secondary preheater) | Check temperature < 60°C before opening ductwork | — |

---

## 2. Pre-Isolation

- [ ] Secondary fan stopped on DCS
- [ ] FT_8302 = 0 m³/h
- [ ] Boiler shut down or SA fan isolated from furnace
- [ ] Notify shift supervisor

---

## 3. Isolation Sequence

1. HV electrician opens 6 kV breaker B-02 and locks — tag "DO NOT ENERGIZE"
2. Close instrument air to outlet damper — lock
3. Close outlet damper — install mechanical block
4. Sign isolation register

---

## 4. Verification

- [ ] DCS start attempt fails
- [ ] FT_8302 = 0 m³/h
- [ ] Minimum 2 locks in place

---

## 5. Restoration

Identical to ZJP-SAFE-002 (Primary Fan LOTO restoration).

> Note: Primary and secondary fan LOTO procedures are almost identical — both fans are the same voltage class and similar design. Always verify you are working on the correct breaker by checking nameplate on MCC and switchgear before applying lock.

---

## 6. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 1.3 | 2021-08-01 | Aligned with ZJP-SAFE-002 format update |
