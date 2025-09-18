# KPI Services — Validation & Thresholds

## Purpose
Validation ensures KPI computations are correct, reliable, and compliant.  
It applies rules before and after KPI calculations to detect errors, enforce thresholds, and provide audit evidence.  
Validation is mandatory for all KPI contracts.

---

## Dependency on GDP
All validation logic operates on GDP inputs and KPI outputs.  
- **Pre-validation** applies checks on GDP entities before KPI formulas run.  
- **Post-validation** applies checks on KPI results before publishing.  
Raw contracts are never directly validated by KPI Services.

---

## Pre-Validation
- **Schema Checks**: confirm GDP entities required by the KPI are present and up to date.  
- **Reference Data Checks**: validate currencies, fiscal calendars, and organizational structures.  
- **Freshness Checks**: verify data timeliness against defined SLOs.  
- **Conformance Checks**: ensure GDP attributes match expected formats and units.  

---

## Post-Validation
- **Reasonableness Tests**: confirm results fall within expected ranges.  
- **Cross-KPI Consistency**: compare results across related KPIs (e.g., Revenue vs Gross Margin).  
- **Threshold Enforcement**: trigger alerts if KPI values breach defined limits.  
- **Escalation Rules**: route validation failures to designated stakeholders or systems.  

---

## Validation Outcomes
- **Pass**: KPI result is published to downstream consumers.  
- **Warn**: KPI is published but flagged with annotations.  
- **Fail**: KPI result is withheld; error code and metadata logged for audit.  

---

## Evidence and Audit
- Every validation run is assigned a unique execution ID.  
- Results (pass, warn, fail) are logged with timestamp, KPI version, and GDP lineage.  
- Audit evidence is immutable and exportable for compliance.  

---

## Architectural Reference
Validation follows the **ADR-0003 Three-Contract Model**:  
- Pre-validation: Raw → GDP canonicalization (enforced in Schema Services).  
- Post-validation: GDP → KPI evaluation (enforced in KPI Services).  

---

## Example
*KPI: Attrition Rate*  
- **Inputs (GDP):** Headcount, Terminations  
- **Formula:** Terminations / Headcount  
- **Pre-validation:** check Headcount data freshness and reference calendar.  
- **Post-validation:** threshold alert if Attrition Rate > 15%.  
