# Host App — SLAs & Error Model

## Purpose
This document defines the service-level objectives (SLOs) for the Host App and the error classification model used across UI and API interactions.  
The goal is to make expectations transparent for governance users and to ensure that errors are consistently explained, auditable, and actionable.

---

## Service-Level Objectives (SLOs)
SLOs are measurable targets that indicate how the Host App is expected to perform under normal conditions. They are not guarantees, but they guide both design choices and operational monitoring.

The Host App aims to provide:
- **UI Availability** — the user interface is accessible ≥ 99.9% of the time on a monthly basis.  
- **Publish Latency** — contract publishes complete within the target threshold, excluding human approval steps.  
- **Audit Exports** — evidence exports complete within an agreed timeframe, even under load.  
- **Telemetry Freshness** — health dashboards are updated within near-real-time windows to reflect the state of pipelines and tenants.  

These objectives are meant to reassure governance teams that the platform is reliable enough to support compliance, approvals, and oversight without unexpected gaps.

---

## Error Model
The error model standardizes how failures are communicated. This prevents confusion and ensures that errors can be traced back to their cause during audits.

Errors fall into three categories:
- **User Errors** — caused by invalid input, missing approvals, or RBAC denials. These indicate that the request was well-formed but disallowed.  
- **System Errors** — caused by service unavailability, internal timeouts, or storage issues. These typically require operator intervention or retry logic.  
- **Policy Errors** — caused by violations of compliance rules, such as residency restrictions or quota overruns. These are neither user mistakes nor system faults, but intentional safeguards.  

Every error is logged with a code, severity level, and recommended remediation path. Errors visible in the UI are designed to be human-readable, while errors returned via API also include structured machine-readable fields.

---

## Design Tenets
- **Clarity:** users must immediately understand the type of error and possible next steps.  
- **Consistency:** error categories remain stable across UI and API to avoid confusion.  
- **Auditability:** all errors are recorded in the evidence model, ensuring traceability in compliance audits.  
- **Separation:** technical failures (system) are clearly distinct from business-policy denials (policy).  

---

## Why This Matters
Without clear SLOs, governance users would not know what levels of availability and responsiveness they can depend on.  
Without a structured error model, operational noise would be indistinguishable from policy enforcement, weakening compliance.  
Together, these guarantees and models allow governance, audit, and compliance teams to operate with confidence in the Host App.

---

## Cross-References
- [Host App — Observability (Read-only Health)](ha-02e-observability.md)  
- [Audit & Evidence](ha-03b-audit.md)  
- [Platform Services — SLOs](../phs/slo.md)  
