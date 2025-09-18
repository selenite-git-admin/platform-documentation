# KPI Services — Traceability

## Purpose
Traceability ensures every KPI can be linked back to its originating business requirement, design decision, and validation result.  
This provides auditability, reduces risk of misinterpretation, and supports compliance obligations.

---

## Scope
- Maintain alignment between **business requirements**, **GDP inputs**, **KPI definitions**, and **validation results**.  
- Provide evidence that every KPI in production has been reviewed and approved.  
- Enable audit teams to trace any KPI value back to its definition and data lineage.

---

## Traceability Dimensions

1. **Requirements → Design**
   - Each business requirement must map to one or more KPI definitions.  
   - Mappings are stored in metadata and versioned.  
   - Example: *Requirement: Track operating margin* → *Design: KPI formula referencing GDP Revenue and GDP Operating Expense*.

2. **Design → Validation**
   - Each KPI definition must include validation and threshold rules.  
   - Validation results are logged and stored alongside KPI versions.  
   - Example: *KPI: Gross Margin %* → *Validation: threshold alert if < 20%*.

3. **Design → Enforcement**
   - KPI computations reference only GDP entities.  
   - Enforcement services ensure mappings cannot include Raw contracts.  
   - Example: *KPI Contract v2.1* → *GDP Finance entities (Revenue, COGS)*.

4. **Validation → Evidence**
   - Validation outcomes are stored with timestamps and execution IDs.  
   - Audit evidence is exportable for compliance checks.  
   - Example: *Run ID 2025-09-15* → *KPI: Attrition Rate* → *Validation passed*.

---

## Traceability Matrix (Illustrative)

| Requirement            | GDP Inputs                | KPI Definition                  | Validation Rule                  |
|------------------------|---------------------------|---------------------------------|----------------------------------|
| Operating Margin       | Revenue, Operating Costs  | (Revenue – OpEx) / Revenue      | Alert if < 10%                   |
| Revenue Growth %       | Revenue, Calendar Periods | (Revenue_t – Revenue_t-1)/t-1   | Alert if variance > ±5%          |
| Headcount Utilization  | Headcount, Project Hours  | Hours Billed / Available Hours  | Alert if utilization < 70%       |

---

## Architectural Reference
Traceability is enforced by **ADR-0003: Adopt Three-Contract Model (Raw, GDP, KPI)**.  
This ensures:
- Business requirements are implemented only through GDP-based KPI definitions.  
- KPI results are always traceable to GDP inputs, never Raw schemas.  
- Validation outcomes provide end-to-end evidence across all three contracts.

---

## Governance Notes
- All mappings are stored in the control plane and versioned.  
- KPI contracts without complete traceability cannot be published.  
- Traceability reports are part of audit deliverables.  

---

KPI Traceability enforces a **closed loop**:  
**Requirement → GDP Inputs → KPI Definition → Validation → Evidence.**
