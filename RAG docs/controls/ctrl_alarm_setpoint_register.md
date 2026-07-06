---
doc_id: ctrl_alarm_setpoint_register
doc_type: controls
equipment: [induced_draft_fan, primary_fan, secondary_fan, furnace_chamber, furnace_lower_hearth, cyclone_separator_left, cyclone_separator_right, economizer, steam_drum, primary_desuperheater, high_temp_superheater, steam_outlet]
tags: [TE_8332A, PTCA_8322A, PTCA_8324, PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, AIR_8301A, AIR_8301B, FT_8301, FT_8302, FT_8306A, FT_8306B, TE_8303, TE_8304, TE_8313B, TE_8319A, TE_8319B, TV_8329ZC, YJJWSLL, ZZQBCHLL, YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2, SXLTCYZ, SXLTCYY, ZCLCCY, YCLCCY]
title: Alarm and Trip Setpoint Register — All 30 Tags
revision: 4.2
date: 2022-03-01
---

# Alarm and Trip Setpoint Register

**Document No.:** ZJP-CTRL-004  
**Revision:** 4.2 | **Date:** 2022-03-01  
**Applicability:** Unit 1 — All Instrumentation  
**Owner:** Control and Instrumentation Engineer

> This register is the single authoritative source for all alarm and trip setpoints. Any changes to setpoints must be updated here, in the DCS, and in the relevant equipment datasheet. Changes require sign-off from the Control Engineer and Plant Manager.

---

## 1. Steam Side

| Tag | Description | Units | LoLo (Trip) | Lo (Alarm) | Normal | Hi (Alarm) | HiHi (Alarm) | HiHiHi (Trip) |
|-----|-------------|-------|-------------|-----------|--------|-----------|--------------|----------------|
| TE_8332A | Steam outlet temperature | °C | — | 528 | 530–545 | 548 | 558 | 565 |
| PTCA_8324 | Outlet steam pressure | kPa | 8,400 | 8,800 | 9,400–10,000 | 10,200 | 10,500 | — |
| PTCA_8322A | Steam drum pressure | kPa | — | 8,800 | 9,400–10,000 | 10,200 | 10,500 | 10,800 |
| ZZQBCHLL | Main steam flow (compensated) | t/h | — | 100 | 120–135 | 145 | — | — |
| TV_8329ZC | Desuperheater valve position | % | — | — | 20–60 | 85 (sustained) | — | — |
| YJJWSLL | Desuperheating water flow | t/h | — | — | 2–8 | 10 | 12 | — |

---

## 2. Combustion and Furnace

| Tag | Description | Units | LoLo (Trip) | Lo (Alarm) | Normal | Hi (Alarm) | HiHi (Trip) |
|-----|-------------|-------|-------------|-----------|--------|-----------|-------------|
| PT_8313A | Upper furnace pressure A | Pa | — | — | −80 to −160 | +100 | +200* |
| PT_8313B | Upper furnace pressure B | Pa | — | — | −80 to −160 | +100 | +200* |
| PT_8313C | Upper furnace pressure C | Pa | — | — | −90 to −170 | +100 | +200* |
| PT_8313D | Upper furnace pressure D | Pa | — | — | −90 to −170 | +100 | +200* |
| PT_8313E | Upper furnace pressure E | Pa | — | — | −100 to −180 | +100 | +200* |
| PT_8313F | Upper furnace pressure F | Pa | — | — | −100 to −180 | +100 | +200* |
| TE_8313B | Upper furnace temperature | °C | — | 750 | 850–950 | 980 | 1,020 |
| SXLTCYZ | Hearth ΔP left | Pa | — | 800 | 1,500–3,000 | 4,000 | — |
| SXLTCYY | Hearth ΔP right | Pa | — | 800 | 1,500–3,000 | 4,000 | — |

*PT_8313 trip requires 2-of-6 sensors to exceed +200 Pa simultaneously.

---

## 3. Flue Gas and O2

| Tag | Description | Units | LoLo (Trip) | Lo (Alarm) | Normal | Hi (Alarm) | HiHi |
|-----|-------------|-------|-------------|-----------|--------|-----------|------|
| AIR_8301A | Flue gas O2 left | % | 1.5 | 2.0 | 3.5–5.5 | 7.0 | — |
| AIR_8301B | Flue gas O2 right | % | 1.5 | 2.0 | 3.5–5.5 | 7.0 | — |
| TE_8319A | Economizer flue gas outlet left | °C | — | 110 | 135–160 | 185 | 210 |
| TE_8319B | Economizer flue gas outlet right | °C | — | 110 | 135–160 | 185 | 210 |
| ZCLCCY | Cyclone ΔP left | Pa | — | 300 | 600–1,200 | 1,800 | — |
| YCLCCY | Cyclone ΔP right | Pa | — | 300 | 600–1,200 | 1,800 | — |

---

## 4. Air Flows

| Tag | Description | Units | LoLo (Trip) | Lo (Alarm) | Normal | Hi (Alarm) |
|-----|-------------|-------|-------------|-----------|--------|-----------|
| FT_8301 | Primary fan outlet flow | m³/h | 50,000 | 70,000 | 90,000–135,000 | — |
| FT_8302 | Secondary fan outlet flow | m³/h | 25,000 | 40,000 | 55,000–80,000 | — |
| FT_8306A | Return air chamber flow left | m³/h | — | 5,000 | 8,000–15,000 | 20,000 |
| FT_8306B | Return air chamber flow right | m³/h | — | 5,000 | 8,000–15,000 | 20,000 |

---

## 5. Air Preheater Temperatures

| Tag | Description | Units | Lo (Alarm) | Normal | Hi (Alarm) |
|-----|-------------|-------|-----------|--------|-----------|
| TE_8303 | Primary air preheater outlet air temp | °C | 150 | 180–220 | 240 |
| TE_8304 | Secondary air preheater outlet air temp | °C | 145 | 175–215 | 230 |

---

## 6. IDF (Induced Draft Fan)

| Tag | Description | Units | Alert | Alarm | Trip |
|-----|-------------|-------|-------|-------|------|
| YFJ3_ZD1 | IDF bearing vibration A | mm/s | 3.5 | 4.5 | 11.0 |
| YFJ3_ZD2 | IDF bearing vibration B | mm/s | 3.5 | 4.5 | 11.0 |
| YFJ3_AI | IDF motor current | A | — | 280 | 310 |

---

## 7. Setpoint Change Log (Most Recent)

| Date | Tag | Old Value | New Value | Reason | Authorized By |
|------|-----|-----------|-----------|--------|---------------|
| 2022-03-01 | TE_8332A HiHiHi | 560°C | 565°C | OEM review recommended 565°C as conservative trip | Plant Mgr |
| 2021-06-15 | YFJ3_ZD1/ZD2 Trip | 7.1 mm/s | 11.0 mm/s | ISO 10816-3 review — original setpoint overly conservative | C&I Engineer |
| 2020-08-10 | AIR_8301A/B LoLo | 1.0% | 1.5% | O2 analyzer response time study showed 1.0% was too late for safe CO prevention | Safety Officer |

---

## 8. Notes

- All alarms are implemented in the DCS (Yokogawa CENTUM VP)
- BPS (Boiler Protection System) trips are hardwired in addition to DCS — hardwired trips cannot be bypassed from DCS
- Alarm rationalization was last performed: 2021-10-01 per IEC 62682 methodology
- Next alarm rationalization review due: 2024-10-01
