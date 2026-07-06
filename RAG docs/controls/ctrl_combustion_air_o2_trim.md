---
doc_id: ctrl_combustion_air_o2_trim
doc_type: controls
equipment: [primary_fan, secondary_fan, furnace_chamber, economizer]
tags: [AIR_8301A, AIR_8301B, FT_8301, FT_8302]
title: Combustion Air / O2 Trim Control Loop — Description and Tuning
revision: 1.6
date: 2021-10-01
---

# Combustion Air / O2 Trim Control Loop

**Document No.:** ZJP-CTRL-003  
**Loop Name:** combustion_air_control_loop  
**Revision:** 1.6 | **Date:** 2021-10-01

---

## 1. Loop Purpose

The combustion air / O2 trim loop optimizes combustion efficiency by maintaining the flue gas oxygen content at the target setpoint. It does this by adjusting the speeds (damper positions) of the primary fan and secondary fan to supply exactly the right amount of air for complete combustion with minimum excess. Low excess air improves efficiency; too-low excess air creates CO and safety hazards.

**Controlled Variable (PV):** Average of AIR_8301A and AIR_8301B (flue gas O2, %)  
**Setpoint (SP):** 4.0% O2 (adjustable 3.0–6.0%)  
**Manipulated Variables (MV):**
- FT_8301 — primary fan flow (via outlet damper)
- FT_8302 — secondary fan flow (via outlet damper)

---

## 2. Control Architecture

This loop uses a **ratio / bias structure** rather than simple PID on total air:

1. **Load feedforward:** Total air demand is calculated from coal feed rate setpoint (mass-flow-based air-to-fuel ratio = 8.5:1 by mass)
2. **O2 trim:** The measured O2 (AIR_8301A/B average) trims the total air demand setpoint up or down to correct the air-fuel ratio in real-time
3. **Split:** Total air is split into primary (60%) and secondary (40%) at base load, with the ratio adjustable per ZJP-SOP-005

**This architecture means:** Even if O2 analyzer is offline, the boiler can still run in feedforward-only mode using the mass-flow air-to-fuel ratio as the air demand basis. However, O2 trim must be re-enabled as soon as the analyzer is repaired.

---

## 3. PID Parameters (O2 Trim Outer Loop)

| Parameter | Value |
|-----------|-------|
| Proportional band | 1.0% O2 |
| Integral time (Ti) | 300 seconds (slow — O2 response to air changes takes 3–5 minutes) |
| Derivative time (Td) | 0 (not used) |
| Output limits | −15% to +15% trim on total air setpoint |
| Anti-windup | Enabled |

**The slow Ti (300 s) is deliberate.** O2 in a CFB furnace takes 3–5 minutes to stabilize after an air change, due to the large thermal mass of the bed. Faster integral action causes oscillation.

---

## 4. Air-Fuel Ratio Reference

| Coal CV Range | Air-to-Coal Ratio (theoretical) | Excess Air @ 4% O2 |
|---------------|--------------------------------|---------------------|
| 23–26 MJ/kg | 8.0–8.5 kg air / kg coal | ~20% |
| 26–29 MJ/kg | 8.5–9.0 kg air / kg coal | ~20% |
| 29–32 MJ/kg | 9.0–9.5 kg air / kg coal | ~20% |

When coal quality changes (different supplier, moisture content), the feedforward air-to-fuel ratio may need adjustment. Confirm by observing whether O2 trim output is persistently at +/−limit — this indicates the feedforward is mismatched with actual coal CV.

---

## 5. Primary-to-Secondary Air Split

The PA:SA split affects combustion staging and NOₓ formation:

| Load | PA (FT_8301) | SA (FT_8302) | PA:SA Ratio |
|------|-------------|-------------|-------------|
| 100% | 55% | 45% | 55:45 |
| 75% | 60% | 40% | 60:40 |
| 50% | 62% | 38% | 62:38 |
| 40% min | 65% | 35% | 65:35 |

Increasing secondary air share improves upper-furnace burnout and reduces CO. However, reducing primary air below minimum fluidization velocity (FT_8301 < 65,000 m³/h) destabilizes the bed — do not do this.

---

## 6. O2 Analyzer Management

AIR_8301A and AIR_8301B are redundant sensors at the economizer inlet. The control loop uses their average. Operating rules:

| Condition | Action |
|-----------|--------|
| AIR_8301A − AIR_8301B > 1.5% | Alert — investigate; do not average diverged analyzers |
| One analyzer confirmed faulty | Remove from average — run on single analyzer with manual backup monitoring |
| Both analyzers offline | Switch to feedforward-only air control; increase frequency of local CO spot checks |
| After recalibration | Allow 15 minutes for analyzer to stabilize before re-enabling O2 trim |

Analyzer calibration:
- Zero gas: nitrogen (O2 = 0%)
- Span gas: 6.0% O2 in nitrogen (certified reference)
- Calibration interval: monthly minimum; after any maintenance on probe or sample conditioning

---

## 7. Safety Interlocks

| Condition | Action |
|-----------|--------|
| AIR_8301A or AIR_8301B < 1.5% | BPS trip (low-low O2) |
| Both O2 analyzers failed | Loop forces to maximum air demand — conservative (over-aeration) |
| Primary fan trip | Loop automatically reduces coal demand to match available air |

---

## 8. Related Documents
- ZJP-DS-001: Primary Fan Datasheet (FT_8301 specs)
- ZJP-DS-003: Secondary Fan Datasheet (FT_8302 specs)
- ZJP-DS-007: Economizer Datasheet (AIR_8301A/B location)
- ZJP-TRB-007: High Flue Gas O2 Troubleshooting
- ZJP-TRB-008: Low Flue Gas O2 Troubleshooting
- ZJP-CTRL-004: Alarm Setpoint Register
