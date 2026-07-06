---
doc_id: trb_steam_drum_level
doc_type: troubleshooting
equipment: [steam_drum, economizer]
tags: [PTCA_8322A]
title: Troubleshooting Guide — Steam Drum Level Abnormal
revision: 1.7
date: 2022-01-20
---

# Troubleshooting Guide: Steam Drum Level Abnormal

**Document No.:** ZJP-TRB-012  
**Symptom:** Steam drum level rising above +80 mm (high) or falling below −80 mm (low) from centerline  
**Note:** PTCA_8322A measures drum pressure, not level. Level is monitored by separate transmitters and gauge glass.  
**Revision:** 1.7 | **Date:** 2022-01-20

---

## 1. Drum Level Limits

| Level | Alarm | BPS Action |
|-------|-------|-----------|
| +150 mm | High-High | Boiler trip (carryover to superheater — severe damage risk) |
| +80 mm | High | Alarm — operator action required |
| −50 to +50 mm | Normal | No action |
| −80 mm | Low | Alarm — operator action required |
| −150 mm | Low-Low | Boiler trip (tube dry-out — severe damage risk) |

---

## 2. High Drum Level

### 2.1 Immediate Action
If drum level > +100 mm and rising:
1. Reduce feedwater flow — partially close feedwater control valve (manual override)
2. Crack open manual bottom blowdown valve briefly to remove water quickly (caution: hot water discharge — PPE required)
3. Monitor level — should stabilize within 5 minutes

### 2.2 Causes
| Cause | Indicators | Action |
|-------|-----------|--------|
| Feedwater flow too high | FCV position too high, flow rate exceeds evaporation | Reduce FCV |
| Steam demand suddenly reduced | ZZQBCHLL drops while FW continues | Auto-controller should respond — check controller |
| Level transmitter fault (reading high) | Gauge glass shows different level | Trust gauge glass; calibrate transmitter |
| "Swell" during load increase | Rapid load increase causes pressure drop → temporary swell | Normal — wait for swell to subside |

### 2.3 Drum Swell Explanation
During a rapid load increase, drum pressure briefly drops as steam demand exceeds supply. The lower pressure causes water to flash and the drum water level to temporarily rise ("swell") — this is a normal transient and is NOT a true level increase. Level will return to normal within 3–5 minutes. Do not over-correct with excess blowdown during swell.

---

## 3. Low Drum Level

### 3.1 Immediate Action
If drum level < −100 mm and falling:
1. Increase feedwater flow immediately — fully open FCV in manual
2. If FCV is already fully open and level still falling: emergency feedwater pump start (if installed) or switch to standby pump
3. Notify supervisor — if level cannot be recovered, boiler must be tripped before −150 mm

### 3.2 Causes
| Cause | Indicators | Action |
|-------|-----------|--------|
| Feedwater pump failure | Low pump discharge pressure, pump trip alarm | Start standby pump; investigate main pump |
| Feedwater control valve stuck closed | FCV at 0% despite open command | Force open manual isolation bypass; repair valve |
| Steam leak in main steam line | ZZQBCHLL elevated, drum pressure declining | Locate and isolate leak |
| Drum level transmitter fault | Gauge glass shows different level | Trust gauge glass; calibrate transmitter |
| "Shrink" during load reduction | Pressure rises briefly → water contracts → apparent level drop | Normal transient — wait |

---

## 4. Level Instrument Reliability

**Critical rule:** Always cross-check drum level transmitter reading against the visual gauge glass. The gauge glass is direct — it cannot drift or be fooled by impulse line issues.

If transmitter and gauge glass disagree by > 50 mm, trust the gauge glass and issue a work order to recalibrate the transmitter.

---

## 5. PTCA_8322A Relationship

PTCA_8322A (drum pressure) is NOT drum level but is closely related:
- **Normal drum pressure with low level:** feedwater deficit, possible steam leak
- **High drum pressure with normal level:** steam demand has dropped, firing should be reduced
- **Low drum pressure with high level:** likely swell from load reduction, or steam demand surge

---

## 6. Escalation

If drum level cannot be stabilized by operator action:
- Level > +150 mm: BPS trips boiler automatically — confirm trip, stop feedwater
- Level < −150 mm: BPS trips boiler automatically — do not re-fire until tube inspection confirms no damage (ZJP-MNT-011)
