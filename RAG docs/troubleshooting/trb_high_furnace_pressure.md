---
doc_id: trb_high_furnace_pressure
doc_type: troubleshooting
equipment: [furnace_chamber, induced_draft_fan]
tags: [PT_8313A, PT_8313B, PT_8313C, PT_8313D, PT_8313E, PT_8313F, YFJ3_AI, YFJ3_ZD1, YFJ3_ZD2, FT_8301, FT_8302, AIR_8301A, AIR_8301B]
title: Troubleshooting Guide — High Furnace Pressure (Trending Positive)
revision: 2.0
date: 2022-01-20
---

# Troubleshooting Guide: High Furnace Pressure

**Document No.:** ZJP-TRB-003  
**Symptom:** PT_8313A–F trending toward 0 Pa or positive; alarm at +100 Pa; trip at +200 Pa (2-of-6)  
**Revision:** 2.0 | **Date:** 2022-01-20

> **WARNING:** A furnace positive pressure (puff) can result in hot gas and ash ejection from access ports and expansion joints. If pressure rises above +200 Pa and IDF is confirmed running at full speed, initiate emergency shutdown immediately and evacuate the boiler area.

---

## 1. Immediate Actions

When PT_8313A–F average reads > −30 Pa (rising toward zero):
1. **Check IDF speed** — is VFD commanding maximum speed? If IDF speed is not already at maximum, manually override to 100%
2. **Check IDF running feedback** — if IDF has tripped, BPS will automatically shut the boiler; confirm sequence
3. **Check for sudden air flow increase** — did FT_8301 or FT_8302 spike? A large air flow surge can briefly overwhelm draft capacity
4. If pressure rising despite IDF at maximum: reduce primary fan and secondary fan to minimum flow immediately

---

## 2. Probable Causes

### 2.1 IDF Speed Limitation or VFD Fault (Most Common)

**Symptoms:** PT_8313A–F rising; YFJ3_AI not at maximum; IDF speed feedback lower than commanded.

**Diagnosis:**
- VFD commanded speed vs. actual speed feedback — are they matched?
- YFJ3_AI: if current is lower than expected at the commanded speed, the VFD may be limiting due to overcurrent protection or thermal limit

**Action:**
1. Check VFD alarm display (local panel)
2. If VFD fault: attempt VFD reset from DCS — if trip repeats, DO NOT reset again; reduce load to allow IDF to cope
3. If VFD cannot sustain full speed: reduce firing rate to a level IDF can handle; notify electrical team

### 2.2 Sudden Large Increase in Air Flow (Over-Drafting)

**Symptoms:** FT_8301 or FT_8302 spiked suddenly; PT_8313A–F went positive transiently then recovered.

**Cause:** Damper positioner fault causing sudden full-open; combustion_air_control_loop integrator windup.

**Action:**
1. Switch both fan dampers to manual and set to previous position
2. Allow PT_8313A–F to stabilize
3. Gradually return air flow to setpoint manually
4. Investigate control loop — check for integrator windup, positioner mechanical fault

### 2.3 Backpass Blockage Restricting Draft

**Symptoms:** PT_8313A–F rising gradually over hours; YFJ3_AI rising (IDF working harder); TE_8319A/B rising.

**Cause:** Ash bridging in backpass hopper, or major ash deposit dislodging from economizer/air preheater and blocking a duct.

**Action:**
1. Check and clear backpass hoppers (external — do not open while pressurized)
2. Initiate sootblowing if available
3. Reduce load to reduce gas flow until blockage is cleared
4. If pressure rises uncontrollably: reduce to minimum load; prepare for shutdown

### 2.4 Pressure Transmitter Fault

**Symptoms:** Only 1 or 2 of the 6 transmitters (PT_8313A–F) show elevated reading; others remain normal.

**The 2-of-6 voting logic protects against single-sensor trips.** However, a sustained anomalous reading from a single sensor should be investigated.

**Action:**
1. If only 1 sensor is high: flag as suspect; isolate from DCS; issue work order for transmitter check
2. Monitor remaining 5 sensors for true furnace pressure
3. Verify impulse lines are clear (blow-through) — impulse lines can plug with ash

### 2.5 IDF Inlet or Outlet Damper Stuck

**Symptoms:** IDF running at high current (YFJ3_AI elevated) but low flow — possible blockage or damper mechanical failure.

**Action:**
1. Check IDF inlet damper position indication — confirm it is fully open
2. Check outlet duct for unusual restriction
3. If damper is stuck partially closed: reduce firing, issue emergency work order

---

## 3. Sensor Validity Check

To verify PT_8313A–F readings are accurate:
- Compare left-side sensors (PT_8313A, C, E) against right-side (PT_8313B, D, F) — they should agree within ±30 Pa under normal balanced combustion
- A single sensor > 100 Pa higher than the average of the other 5 is likely a faulty transmitter, not a real furnace event

---

## 4. Trip Reset After Automatic ESD

After furnace pressure trip (automatic via BPS):
1. Do NOT attempt restart for minimum 30 minutes
2. Identify and correct the root cause — confirm in writing before reset
3. Perform 5-minute purge of furnace before any re-ignition
4. Restart per ZJP-SOP-002 (hot restart) if bed still warm, or ZJP-SOP-001 if cooled

---

## 5. Escalation

Furnace pressure rising despite full IDF speed and minimum air flows: this is a potential catastrophic failure scenario. Initiate manual ESD (ZJP-SOP-004), evacuate boiler area, and call all personnel clear before investigating.
