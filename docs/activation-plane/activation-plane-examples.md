# Activation Plane — Examples

These examples illustrate how the Activation Plane enables tenants to move directly from KPI insight to governed, auditable action.

---

## Finance — Accounts Receivable

**Scenario:**  
KPI: *AR overdue > 90 days increased by 15% this quarter.*  

**Activation:**  
- Event-driven flow detects threshold breach.  
- Activation Plane creates a collections task in Salesforce.  
- Slack notification sent to #finance-alerts channel.  
- Audit log captures KPI reference, user, correlation ID.

**Outcome:**  
- Collections team notified instantly.  
- Task recorded in CRM.  
- Compliance can trace back every action to KPI evidence.

---

## Operations — Manufacturing Efficiency

**Scenario:**  
KPI: *OEE dropped below 70% in Plant B.*  

**Activation:**  
- Event-driven flow triggers when KPI breach detected.  
- Activation Plane logs a maintenance work-order in MES.  
- Tenant App shows activation panel to review and approve escalation.  

**Outcome:**  
- Plant manager alerted proactively.  
- Maintenance team has a system-of-record task.  
- Reduced downtime through early intervention.

---

## Compliance — Regulatory Reporting

**Scenario:**  
KPI: *Quarterly compliance evidence bundle due in 5 days.*  

**Activation:**  
- Scheduled flow runs monthly.  
- Activation Plane exports PDF bundle to SharePoint / regulator portal.  
- Audit evidence hash stored in tamper-proof log.  

**Outcome:**  
- No missed deadlines.  
- Regulator-ready package always aligned with KPI outputs.  
- Full traceability for auditors.

---

## Liquidity Forecasting — AI Activation

**Scenario:**  
CFO requests liquidity forecast based on current receivables, payables, and cash.  

**Activation:**  
- Manual flow triggered via Tenant App panel.  
- Activation Plane calls AI Activation API `/api/v1/ai/liquidity_forecast:predict`.  
- Results returned with confidence score and explanations.  
- Optional reverse-connector writes forecast summary into ERP planning module.

**Outcome:**  
- CFO gets actionable forecast instantly.  
- Decision logged, reproducible, and compliant.  

---

## Why These Examples Matter

The Activation Plane ensures that every action — whether financial, operational, or regulatory — is:  
- **Contextual:** Tied directly to a KPI insight.  
- **Governed:** Policy-checked, quota-enforced, and role-controlled.  
- **Auditable:** Logged with correlation IDs and evidence hashes.  
- **Actionable:** Reaches the real system-of-record where work happens.
