---
doc_id: ctrl_instrument_calibration
doc_type: controls
equipment: [induced_draft_fan, primary_fan, secondary_fan, economizer, steam_outlet, steam_drum]
tags: [TE_8332A, PTCA_8322A, PTCA_8324, PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, AIR_8301A, AIR_8301B, FT_8301, FT_8302, TE_8319A, TE_8319B, YFJ3_ZD1, YFJ3_ZD2, YFJ3_AI, TV_8329ZC, YJJWSLL, ZZQBCHLL, SXLTCYZ, SXLTCYY, ZCLCCY, YCLCCY]
title: Instrument Calibration Schedule and Tolerance Limits
revision: 3.0
date: 2022-01-01
---

# Instrument Calibration Schedule and Tolerance Limits

**Document No.:** ZJP-CTRL-005  
**Revision:** 3.0 | **Date:** 2022-01-01  
**Owner:** C&I Department

---

## 1. Purpose

This document specifies the calibration interval, method, and acceptance tolerance for every instrument in the Unit 1 boiler historian dataset. All calibration records are maintained in the plant maintenance management system (CMMS).

---

## 2. Calibration Schedule — All Tags

### 2.1 Temperature Instruments

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| TE_8332A | Type K thermocouple | 6 months | ± 2.0°C | NIST-traceable reference bath; pull thermocouple and test in workshop |
| TE_8313B | Type K thermocouple | 6 months | ± 3.0°C | Same as TE_8332A |
| TE_8319A | Type K thermocouple | 6 months | ± 3.0°C | Same |
| TE_8319B | Type K thermocouple | 6 months | ± 3.0°C | Same |
| TE_8303 | Type K thermocouple | 6 months | ± 2.5°C | Same |
| TE_8304 | Type K thermocouple | 6 months | ± 2.5°C | Same |

**Note:** TE_8332A is the primary KPI — any out-of-tolerance reading must be corrected immediately. Do not allow TE_8332A to remain uncalibrated for more than 7 days (contact instrument supervisor for emergency calibration).

### 2.2 Pressure Instruments

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| PTCA_8322A | DP transmitter (gauge) | 6 months | ± 5 kPa | Portable calibrator with certified dead-weight reference |
| PTCA_8324 | DP transmitter (gauge) | 6 months | ± 5 kPa | Same |
| PT_8313A–F (all 6) | DP transmitter (low range, gauge) | 6 months | ± 5 Pa | Inclined manometer or micro-manometer reference |
| SXLTCYZ | DP transmitter | 6 months | ± 20 Pa | Portable micro-manometer |
| SXLTCYY | DP transmitter | 6 months | ± 20 Pa | Portable micro-manometer |
| ZCLCCY | DP transmitter | 6 months | ± 20 Pa | Portable micro-manometer |
| YCLCCY | DP transmitter | 6 months | ± 20 Pa | Portable micro-manometer |

### 2.3 Flow Instruments

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| FT_8301 | Pitot tube + DP transmitter | Annual | ± 5% of reading | Zero check + span check; compare against portable traverse at known load |
| FT_8302 | Pitot tube + DP transmitter | Annual | ± 5% of reading | Same |
| FT_8306A | DP transmitter (orifice plate) | Annual | ± 3% of reading | Zero/span check with calibrator |
| FT_8306B | DP transmitter (orifice plate) | Annual | ± 3% of reading | Same |
| YJJWSLL | Vortex flowmeter | 6 months | ± 2% of reading | Zero check; comparison vs. feedwater mass balance |
| ZZQBCHLL | Orifice + DP + compensation | 6 months | ± 2% of reading | DP zero/span; verify compensation calc in DCS using known TE_8332A and PTCA_8324 |

### 2.4 Oxygen Analyzers

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| AIR_8301A | Zirconia in-situ O2 analyzer | Monthly | ± 0.2% O2 | Zero: N2 reference gas; Span: 6.0% O2 certified reference gas |
| AIR_8301B | Zirconia in-situ O2 analyzer | Monthly | ± 0.2% O2 | Same |

O2 analyzers are safety-critical — monthly calibration is mandatory. Do not extend interval without written approval from C&I Engineer and Safety Officer.

### 2.5 Vibration Instruments

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| YFJ3_ZD1 | Velocity vibration transducer | Annual | ± 0.5 mm/s at 25 mm/s reference | Compare against calibrated reference shaker table during outage |
| YFJ3_ZD2 | Velocity vibration transducer | Annual | ± 0.5 mm/s at 25 mm/s reference | Same |

Between annual calibrations: cross-check against portable analyzer at same measurement point during operator rounds. If difference > 1.0 mm/s: arrange calibration at next available outage.

### 2.6 Motor Current and Valve Position

| Tag | Type | Interval | Tolerance | Method |
|-----|------|----------|-----------|--------|
| YFJ3_AI | 4–20 mA current transmitter on MCC | Annual | ± 2 A | Compare DCS reading against calibrated clamp ammeter |
| TV_8329ZC | Positioner feedback (4–20 mA) | 6 months | ± 2% position | Stroke test full travel; verify position feedback at 0%, 50%, 100% |

---

## 3. Calibration Overdue Actions

If any instrument exceeds its calibration interval:
1. Enter corrective action in CMMS within 24 hours of overdue date
2. For safety-critical instruments (TE_8332A, PT_8313A–F, AIR_8301A/B): immediately inform C&I Engineer and Shift Supervisor — maximum 7-day grace period
3. For non-critical instruments: calibrate within 30 days of due date

---

## 4. Calibration Record Retention

All calibration certificates retained for minimum 7 years (Chinese regulatory requirement for pressure vessel instrumentation).

---

## 5. Calibration Equipment

| Equipment | Model | Cal Due |
|-----------|-------|---------|
| Pressure calibrator | Beamex MC6-T | Per Beamex schedule (annual) |
| Temperature reference bath | Fluke 7341 | Annual NIST trace |
| O2 reference gas cylinders | 6.0% O2/N2 (3 on site) | 2-year gas stability certification |
| Clamp ammeter | Fluke 376 FC | Annual |
| Micro-manometer | Testo 510i | Annual |
