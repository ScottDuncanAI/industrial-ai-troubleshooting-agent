---
doc_id: emergency_shutdown_procedure
doc_type: sop
equipment: [induced_draft_fan, primary_fan, secondary_fan, furnace_lower_hearth, furnace_chamber, steam_drum, steam_outlet]
tags: [PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, TE_8332A, PTCA_8322A, PTCA_8324, ZZQBCHLL, YFJ3_ZD1, YFJ3_ZD2, YFJ3_AI, AIR_8301A, AIR_8301B]
title: Emergency Shutdown Procedure (ESD)
revision: 4.0
date: 2022-03-01
---

# Emergency Shutdown Procedure (ESD)

**Document No.:** ZJP-SOP-004  
**Revision:** 4.0  
**Effective Date:** 2022-03-01  
**Approved By:** Plant Engineering Manager / Safety Manager  
**Applicability:** Unit 1 — 130 t/h CFB Coal-Fired Boiler

> **WARNING:** This procedure is initiated when normal operation cannot be safely maintained. Time is critical. Follow steps in sequence without deviation. Do not attempt to save the fire or recover the unit during an ESD.

---

## 1. Automatic Trip Conditions

The boiler protection system (BPS) will initiate an automatic trip and execute steps 2.1 through 2.4 automatically on any of the following:

| Trip Condition | Sensor / Signal | Trip Setpoint |
|----------------|----------------|---------------|
| Steam drum high pressure | PTCA_8322A | > 10.8 MPa |
| Steam drum low-low level | Drum level transmitter | < −200 mm |
| Furnace positive pressure (puff) | PT_8313A–F (any 2 of 6) | > +200 Pa |
| IDF trip / loss of draft | IDF motor running feedback | Lost |
| Steam outlet temperature high-high | TE_8332A | > 565°C |
| Flue gas O2 low-low | AIR_8301A or AIR_8301B | < 1.5% |
| IDF bearing vibration high-high | YFJ3_ZD1 or YFJ3_ZD2 | > 11 mm/s |
| Loss of all flame | Flame scanner input | All scanners dark |
| Manual ESD pushbutton | Operator action | — |

---

## 2. Automatic ESD Sequence (Executed by BPS)

### 2.1 Immediate (< 1 second)
- Trip all coal feeders — close coal feed gates
- Close coal bunker isolation valves
- De-energize ignition burner igniters and close fuel valves

### 2.2 Within 5 Seconds
- Open furnace emergency vent damper (if installed)
- Switch IDF to maximum speed (or maintain last speed if IDF was the trip cause)
- Close main steam isolation valve
- Close feedwater control valve (hold drum level with separate emergency feedwater if available)

### 2.3 Within 30 Seconds
- Reduce primary fan and secondary fan to minimum purge speed (30%)
- Initiate 5-minute post-trip purge sequence
- Alarm: "BOILER TRIP — INVESTIGATE CAUSE BEFORE RESTART"

### 2.4 After Purge Complete
- Stop primary fan and secondary fan
- IDF remains running at minimum speed to maintain cooling draft
- System holds in safe state pending operator investigation

---

## 3. Operator Actions After BPS Initiates Trip

### 3.1 Immediate (Within 2 Minutes)
1. Confirm coal feeders stopped — verify by sight glass or feeder current zero
2. Identify trip cause from BPS first-out annunciator on DCS
3. Confirm main steam isolation valve closed — verify ZZQBCHLL trending to zero
4. Notify plant supervisor and safety officer of boiler trip
5. Account for all personnel in boiler area — confirm no one is at risk

### 3.2 Draft Assessment (Minutes 2–5)
- If IDF is still running: confirm furnace pressure negative on PT_8313A–F
- If IDF has tripped: furnace may go to positive pressure — evacuate boiler area immediately if pressure exceeds +500 Pa and does not recover within 60 seconds
- Notify fire brigade if coal dust deflagration is suspected

### 3.3 Post-Purge Operator Actions
1. After 5-minute purge confirmed complete, reduce IDF to 15% speed (cooling mode)
2. Monitor PTCA_8322A — drum pressure should remain stable or slowly decay
3. Do NOT attempt restart without completing the following:
   - Written investigation of trip cause
   - Supervisor sign-off on restart authorization
   - Any defective equipment repaired or taken out of service

---

## 4. Specific Emergency Scenarios

### 4.1 Furnace Positive Pressure (Furnace Puff/Explosion)
1. Evacuate boiler area immediately
2. Initiate ESD manually if BPS has not already tripped
3. Do NOT open any furnace access doors until furnace pressure is confirmed negative AND bed temperature < 300°C
4. After event, inspect furnace refractory, expansion joints, and ductwork for damage before any restart

### 4.2 IDF Trip — Loss of Induced Draft
1. BPS will automatically trip boiler
2. Furnace will briefly go positive — this is expected and transient if coal has been cut
3. If furnace pressure rises above +500 Pa and does not return negative within 2 minutes: evacuate
4. Do not restart IDF without inspection — see ZJP-MNT-003 (IDF Bearing Inspection)

### 4.3 Steam Drum Low-Low Level
1. Open emergency feedwater valve immediately (manual override if control valve failed)
2. If level cannot be recovered: maintain ESD, do not fire the boiler with no water
3. Investigate feedwater pump trip or feedwater supply failure before restart

### 4.4 High-High Steam Temperature (TE_8332A > 565°C)
1. Confirm desuperheater valve TV_8329ZC is open — open manually if necessary
2. Reduce coal feed — if BPS has not tripped automatically, manually reduce firing
3. If TE_8332A does not respond within 5 minutes: execute manual ESD
4. Inspect superheater tubes for signs of overheating before restart (see ZJP-MNT-010)

---

## 5. Post-ESD Documentation Requirements

Within 4 hours of every ESD event, the shift supervisor must complete:
- [ ] Trip report form (Form ZJP-F-001) — trip time, first-out cause, sequence of events
- [ ] Operator actions log review
- [ ] Preliminary root cause assessment
- [ ] Equipment damage assessment
- [ ] Notification to plant management and engineering

Restart authorization requires sign-off from:
- Shift Supervisor
- Boiler Engineer or Engineering Manager
- Safety Officer (if personnel safety was at risk)

---

## 6. References
- ZJP-SOP-001: Cold Start Procedure (for restart after ESD)
- ZJP-SOP-007: Pre-Startup Safety Inspection Checklist
- ZJP-SAFE-006: Emergency Response Plan
- ZJP-MNT-003: IDF Bearing Inspection Procedure
- Form ZJP-F-001: Boiler Trip Report
