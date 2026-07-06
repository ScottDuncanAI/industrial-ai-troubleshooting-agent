---
doc_id: env_stack_emissions
doc_type: safety
equipment: [chimney, economizer, primary_air_preheater, secondary_air_preheater]
tags: [AIR_8301A, AIR_8301B, TE_8319A, TE_8319B]
title: Stack Emissions Limits and Monitoring
revision: 2.0
date: 2022-01-01
---

# Stack Emissions Limits and Monitoring

**Document No.:** ZJP-ENV-001  
**Revision:** 2.0 | **Date:** 2022-01-01  
**Regulatory Basis:** GB 13271-2014 (Boiler Air Pollutant Emission Standards), MEE Emission Permit

---

## 1. Applicable Emission Limits

Unit 1 is classified as a **coal-fired industrial boiler > 65 t/h steam capacity** under GB 13271-2014 and the subsequent Zhejiang provincial standards, which are more stringent:

| Pollutant | GB 13271-2014 Limit | Zhejiang Provincial Limit | Unit 1 Design Target |
|-----------|--------------------|--------------------------|--------------------|
| SO₂ | 200 mg/m³ | 100 mg/m³ | < 80 mg/m³ |
| NOₓ | 200 mg/m³ | 150 mg/m³ | < 120 mg/m³ |
| Particulate Matter (PM) | 30 mg/m³ | 20 mg/m³ | < 15 mg/m³ |
| CO | 80 mg/m³ | 80 mg/m³ | < 50 mg/m³ |

All concentrations expressed at standard dry reference conditions: 6% O2, 273 K, 101.3 kPa.

---

## 2. Continuous Emissions Monitoring System (CEMS)

CEMS is installed at the stack and measures the following continuously:

| Channel | Method | Range | Reporting Interval |
|---------|--------|-------|--------------------|
| SO₂ | UV-DOAS or extractive NDIR | 0–500 mg/m³ | 1 min averages |
| NOₓ | Chemiluminescence | 0–500 mg/m³ | 1 min averages |
| PM (particulate) | Laser backscatter (opacity) | 0–200 mg/m³ | 1 min averages |
| CO₂ | NDIR | 0–20% | 1 min averages |
| O2 | Electrochemical / paramagnetic | 0–25% | 1 min averages |
| Stack gas velocity | Pitot + temperature | 0–20 m/s | 1 min averages |
| Stack gas temperature | Type K thermocouple | 0–250°C | Continuous |

CEMS data is transmitted in real-time to the provincial environmental authority via the National Pollution Source Monitoring Data platform.

---

## 3. CEMS Calibration and QA

| Activity | Frequency | Method |
|----------|-----------|--------|
| Automatic zero/span check | Daily (automated at 01:00) | Internal certified reference gas |
| Manual calibration verification | Quarterly | NIST-traceable reference gas |
| Relative Accuracy Test Audit (RATA) | Annually | Third-party stack test |
| System availability requirement | > 90% of operating hours | |

CEMS data validity:
- > 90% valid data required for each compliance period
- Invalid or missing data periods filled per prescribed substitution method (conservative maximum for the emission window)

---

## 4. Emission Control Equipment

| Pollutant | Control Technology | Status |
|-----------|-------------------|--------|
| Particulate matter | Baghouse fabric filter (BFFS-1) | Online — pulse-jet cleaned |
| SO₂ | Limestone injection in CFB bed (in-situ desulfurization) | Ca/S ratio 2.5–3.0 |
| NOₓ | Air staging (primary/secondary air split) + SNCR (urea injection) | SNCR operational |
| CO | Combustion optimization (O2 trim control) | Maintained by combustion_air_control_loop |

---

## 5. Relationship to Process Sensors

The flue gas O2 sensors in the historian (AIR_8301A and AIR_8301B) are the combustion control instruments — not the CEMS O2 channel. However, they inform each other:

- If combustion_air_control_loop is maintaining AIR_8301A/B at 3.5–5.5% O2, CO emissions will typically be within limits
- If AIR_8301A/B drops below 2.5%, CO production increases sharply → CO CEMS alarm likely
- Economizer outlet temperature (TE_8319A/B) affects the energy available for desulfurization and the acid dew point at the baghouse inlet

---

## 6. Exceedance Response

If any CEMS channel exceeds its limit:
1. Within 1 hour: notify shift supervisor and environmental officer
2. Within 4 hours: determine root cause (fuel quality, equipment malfunction, control system fault)
3. Within 24 hours: implement corrective action
4. Report to provincial environmental authority within 2 hours if exceedance is > 2× the limit
5. If exceedance cannot be corrected within 24 hours: may be required to reduce load or shut down pending repair

---

## 7. Reporting

- **Monthly:** CEMS data report submitted to provincial authority via online platform
- **Annual:** Annual emission inventory submitted to MEE (Ministry of Ecology and Environment)
- **Quarterly:** CEMS QA audit results filed

---

## 8. Revision History

| Rev | Date | Change |
|-----|------|--------|
| 1.0 | 2019-03-01 | Initial issue |
| 2.0 | 2022-01-01 | Updated to Zhejiang 2022 provincial standards (SO₂ limit reduced from 200 to 100 mg/m³) |
