---
doc_id: trb_low_steam_temperature
doc_type: troubleshooting
equipment: [steam_outlet, high_temp_superheater, primary_desuperheater, low_temp_superheater, furnace_lower_hearth, furnace_chamber]
tags: [TE_8332A, TV_8329ZC, YJJWSLL, ZZQBCHLL, AIR_8301A, AIR_8301B, TE_8313B, FT_8301, FT_8302, SXLTCYZ, SXLTCYY]
title: Troubleshooting Guide — Low Steam Temperature (TE_8332A < 530°C)
revision: 2.1
date: 2022-01-20
---

# Troubleshooting Guide: Low Steam Temperature

**Document No.:** ZJP-TRB-002  
**Symptom:** TE_8332A below 530°C (normal minimum) or on a sustained declining trend  
**Revision:** 2.1 | **Date:** 2022-01-20

---

## 1. Immediate Actions

If TE_8332A < 528°C (low alarm):
1. Confirm reading is valid (not a thermocouple fault)
2. Check TV_8329ZC — if position > 40% and YJJWSLL > 3 t/h with TE_8332A dropping: desuperheater is overcooling → close TV_8329ZC to 10% manually
3. If YJJWSLL already near zero and TE_8332A still falling: root cause is combustion side, not desuperheater
4. Check TE_8313B — is combustion intensity adequate?
5. Notify shift supervisor if TE_8332A < 525°C and not recovering within 10 minutes

---

## 2. Diagnostic Decision Tree

**Step 1:** Is TV_8329ZC open and YJJWSLL high?
- YES → Desuperheater overcooling (go to Section 3.1)
- NO → Go to Step 2

**Step 2:** Is firing rate (coal feed) lower than expected for current load?
- YES → Insufficient firing (go to Section 3.2)
- NO → Go to Step 3

**Step 3:** Is TE_8313B lower than normal (< 820°C)?
- YES → Combustion problem (go to Section 3.3)
- NO → Go to Step 4

**Step 4:** Is ZZQBCHLL higher than expected for firing rate?
- YES → Excess steam demand / load change (go to Section 3.4)
- NO → Consider instrumentation fault or fouling (Section 3.5/3.6)

---

## 3. Probable Causes

### 3.1 Desuperheater Overcooling (TV_8329ZC Stuck Open)

**Symptoms:** YJJWSLL high (> 8 t/h), TV_8329ZC at high position despite low TE_8332A, control loop output is reducing but valve not responding.

**Action:**
1. Switch steam_temp_control_loop to manual
2. Manually close TV_8329ZC to < 5%
3. If YJJWSLL remains > 3 t/h with valve commanded closed: valve is stuck open — issue work order for ZJP-MNT-012
4. Confirm TE_8332A recovery within 5–10 minutes of spray water reduction

### 3.2 Insufficient Firing Rate

**Symptoms:** Coal feed known to be low (feeder issue, bunker running out), TE_8313B dropping, TE_8332A following.

**Action:**
1. Check coal bunker level — if low, notify supervisor for coal delivery
2. Check coal feeder speed — if not responding to DCS command, inspect feeder mechanically
3. Increase coal feed rate — response on TE_8332A will lag 10–20 minutes due to bed thermal mass

### 3.3 Combustion Quality Degradation (Low Bed Temperature)

**Symptoms:** TE_8313B declining, SXLTCYZ or SXLTCYY dropping (bed inventory loss), possibly AIR_8301A/B rising (excess air).

This is the most complex root cause. Possible sub-causes:
- **Bed inventory loss:** SXLTCYZ/Y < 1,000 Pa → bed material depleted → less heat generated per unit coal
  - Action: reduce air flow slightly (increase bed fluidizing velocity can worsen inventory); check cyclone solid return legs for blockage
- **Wet coal:** high moisture coal absorbs heat for evaporation → reduced flame temperature
  - Action: if coal quality known to have changed, adjust coal feed +10–15%
- **Low-volatility coal:** less volatile matter → ignition difficulty in upper furnace
  - Action: increase secondary air (FT_8302) to improve upper zone burnout

### 3.4 Load Increase Without Firing Increase

**Symptoms:** ZZQBCHLL increasing (process opened steam demand), firing rate held constant → steam temperature drops as heat is distributed over more mass flow.

**Action:**
1. Confirm this is intentional (process demand) or an anomaly (steam leak?)
2. If intentional: increase coal feed and air per ZJP-SOP-005 (load change procedure)
3. If unexplained ZZQBCHLL increase: inspect main steam header for possible leak

### 3.5 Fouled Superheater Tubes

**Symptoms:** Gradual decline over weeks; YJJWSLL at zero; all combustion parameters normal; TE_8319A/B also slightly elevated.

If ash has fouled the outside of HTSH tubes, heat transfer is reduced and TE_8332A falls.

**Action:**
1. Initiate sootblowing if available in superheater zone
2. Confirm TE_8319A/B — if rising alongside TE_8332A decline, indicates backpass fouling
3. Plan cleaning at next outage

### 3.6 Instrumentation Fault (TE_8332A Reading Low)

**Symptoms:** All combustion parameters normal; steam quality looks correct; process reports no change; TE_8332A alone showing low reading.

**Action:**
1. Check thermocouple: open circuit typically reads very low (near 0) or at cold junction temperature
2. Compare with process model expectation: at known load and firing rate, what should TE_8332A be?
3. If suspected fault: issue work order for thermocouple replacement at next opportunity; notify engineer

---

## 4. Long-Term Low Steam Temperature (Structural)

If TE_8332A consistently reads 525–530°C over multiple shifts with no acute cause:
- Calculate heat balance: is coal CV lower than design?
- Review O2 readings — if AIR_8301A/B consistently > 6%, excess air is high, reducing flame temperature
- Review LTSH performance: if LTSH exit temperature has decreased, HTSH receives cooler steam
- Consider engineering review of combustion tuning

---

## 5. Escalation

TE_8332A < 520°C sustained for > 30 minutes with no identified cause: notify plant engineer for heat balance investigation.
