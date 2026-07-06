---
doc_id: trb_low_steam_flow
doc_type: troubleshooting
equipment: [steam_outlet, steam_drum, low_temp_superheater, high_temp_superheater]
tags: [ZZQBCHLL, PTCA_8322A, PTCA_8324, TE_8332A]
title: Troubleshooting Guide — Low Steam Flow (ZZQBCHLL Below Expected)
revision: 1.4
date: 2022-01-20
---

# Troubleshooting Guide: Low Steam Flow

**Document No.:** ZJP-TRB-006  
**Symptom:** ZZQBCHLL below expected for current firing rate, or suddenly dropping  
**Revision:** 1.4 | **Date:** 2022-01-20

---

## 1. Immediate Assessment

ZZQBCHLL is a compensated mass flow — it uses TE_8332A and PTCA_8324 to correct the raw orifice differential pressure reading for actual steam density. A low reading could be:
1. **True low flow** — less steam being produced or less being consumed
2. **Instrument error** — orifice DP transmitter, TE_8332A, or PTCA_8324 fault affecting the compensation

First, cross-check:
- Is PTCA_8322A (drum pressure) stable? (Falling drum pressure with low steam flow = production problem)
- Is TE_8332A within normal range? (Abnormal TE_8332A affects ZZQBCHLL compensation formula)
- Is the main steam isolation valve fully open? (Partially closed valve restricts flow)

---

## 2. Probable Causes

### 2.1 Reduced Process Demand (Expected Cause)
Process has reduced steam consumption — this is normal and not a fault. Confirm by checking if process area requested load reduction.

### 2.2 Instrument Fault (ZZQBCHLL Reading Low)

**Diagnosis:**
- All other parameters normal
- Drum pressure (PTCA_8322A) stable and normal
- Boiler appears to be making full steam (firing rate, bed temperature normal)

**Action:**
1. Check ZZQBCHLL DP transmitter — zero drift is common (annual calibration required)
2. Check impulse lines — condensate pot may have drained (causes DP reading high, flow reading low)
3. Compare with mass balance: if feedwater flow in ≈ steam flow out (within 3%), ZZQBCHLL is the instrument fault

### 2.3 Main Steam Isolation Valve Not Fully Open

**Action:** Go to valve, confirm fully open position (handwheel, limit switch). A partially closed valve causes ZZQBCHLL to read low with normal drum conditions.

### 2.4 Steam Leak in Main Steam Line

**Symptoms:** ZZQBCHLL lower than expected AND drum pressure slowly dropping despite normal firing. Feedwater flow (from deaerator) increasing to compensate.

**Action:**
1. Walk main steam line from boiler to process — listen and look for steam leaks (noise, visible plume, surface staining)
2. If leak suspected: reduce load and notify supervisor; small leaks may be repaired online; large leaks require immediate shutdown

### 2.5 Reduced Boiler Steam Production

**Symptoms:** Firing rate normal but drum pressure slowly declining and ZZQBCHLL genuinely low. May indicate feedwater flow restriction (feedwater pump performance degraded) or tube failure on water side.

**Action:**
1. Check feedwater pump discharge pressure and flow
2. Confirm economizer inlet flow is normal
3. If drum pressure is dropping with normal firing: possible waterside tube leak — this is an emergency (shut down immediately)

---

## 3. Normal Operating Context

At full load (130 t/h boiler output):
- ZZQBCHLL: 125–135 t/h
- PTCA_8324: 9.4–10.0 MPa
- TE_8332A: 530–545°C

At 75% load:
- ZZQBCHLL: 90–100 t/h

At 50% load:
- ZZQBCHLL: 62–68 t/h

If ZZQBCHLL is more than 10% below the expected value for the current firing rate, treat as abnormal and investigate.

---

## 4. Escalation

ZZQBCHLL < 50 t/h with drum pressure declining and no intentional load reduction: this is a potential emergency. Notify supervisor immediately and prepare for emergency shutdown.
