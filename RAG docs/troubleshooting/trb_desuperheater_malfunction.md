---
doc_id: trb_desuperheater_malfunction
doc_type: troubleshooting
equipment: [primary_desuperheater]
tags: [TV_8329ZC, YJJWSLL, TE_8332A]
title: Troubleshooting Guide — Desuperheater Spray Fault
revision: 1.6
date: 2022-01-20
---

# Troubleshooting Guide: Desuperheater Spray Fault

**Document No.:** ZJP-TRB-011  
**Symptom:** TV_8329ZC position and YJJWSLL disagree, or TE_8332A not responding to desuperheater adjustments  
**Revision:** 1.6 | **Date:** 2022-01-20

---

## 1. Overview

The desuperheater is a valve (TV_8329ZC) controlling a spray nozzle (YJJWSLL measures actual flow). Faults can occur in three places:
1. The valve (TV_8329ZC) — stuck, positioner fault, instrument air failure
2. The nozzle — blocked, eroded
3. The upstream water supply — isolation valve closed, low pressure

---

## 2. Valve Open but No Flow (YJJWSLL = 0 with TV_8329ZC > 20%)

**Probable causes:**
- Upstream isolation valve inadvertently closed
- Nozzle completely blocked
- Water supply pressure too low (feedwater pump fault)

**Diagnosis:**
1. Check upstream isolation valve — confirm open at valve body (not just DCS indication)
2. Check water supply pressure at desuperheater inlet: should be > 12 MPa (higher than steam pressure to overcome pressure drop)
3. If water pressure is correct and valve is confirmed open: nozzle is blocked → ZJP-MNT-012

---

## 3. Valve Closed but Flow Reported (YJJWSLL > 0 with TV_8329ZC = 0%)

**Probable causes:**
- TV_8329ZC valve internal seat leak (valve not seating fully)
- YJJWSLL instrument zero drift

**Diagnosis:**
- If YJJWSLL reads < 0.5 t/h with valve closed: likely instrument zero drift — recalibrate
- If YJJWSLL reads > 1.0 t/h with valve confirmed closed: valve is leaking through — TE_8332A may trend low over time

**Action:**
1. If TE_8332A is normal and YJJWSLL < 0.5 t/h: recalibrate YJJWSLL, schedule valve inspection at next outage
2. If valve is continuously leaking significant flow and TE_8332A is persistently low: arrange valve maintenance during planned outage (ZJP-MNT-012)

---

## 4. Erratic TV_8329ZC Response (Hunting/Oscillation)

**Symptoms:** TV_8329ZC position oscillating rapidly, causing YJJWSLL to fluctuate, causing TE_8332A to oscillate.

**Probable causes:**
- steam_temp_control_loop tuning mismatch (integral time too short, proportional gain too high)
- Instrument air supply pressure unstable
- Valve positioner feedback error

**Actions:**
1. Switch steam_temp_control_loop to manual — does oscillation stop? Yes → control tuning issue
2. Check instrument air pressure at valve: should be stable at 0.5–0.7 MPa
3. If air pressure is fluctuating: investigate instrument air header, compressor, or moisture separator
4. Control loop re-tuning: increase integral time from 180s to 240s as a first step

---

## 5. TE_8332A Not Responding to TV_8329ZC Changes

**Expected response time:** TE_8332A should respond to a TV_8329ZC change within 5–8 minutes (steam transit time from desuperheater to outlet).

If TE_8332A does not respond after 10 minutes:
1. Confirm YJJWSLL is actually changing (valve movement is real, not just a position signal)
2. If YJJWSLL is responding but TE_8332A is not: investigate if steam is bypassing the measurement (possible TE_8332A thermowell damage, loose thermocouple contact)
3. If both YJJWSLL and TV_8329ZC are functioning: the heat input to HTSH must be overwhelming the desuperheater capacity → reduce firing rate

---

## 6. Related Documents
- ZJP-DS-010: Desuperheater Datasheet (design specs and normal ranges)
- ZJP-MNT-012: Desuperheater Nozzle Inspection
- ZJP-CTRL-001: Steam Temperature Control Loop Description
- ZJP-TRB-001: High Steam Temperature Guide
- ZJP-TRB-002: Low Steam Temperature Guide
