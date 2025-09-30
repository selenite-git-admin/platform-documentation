# Scheduling and SLO

## Purpose
Define schedules and service level objectives for metrics delivery.

## Scheduling
Use time based schedules for most metrics.
Use event based triggers for metrics that depend on events.
Coordinate with Pipeline jobs and dependencies.

## SLOs
Track freshness and completeness.
Define breach policies and escalation steps.
Publish current SLO status in admin views.

## Alerts
Create alerts for missed schedules and SLO breaches.
Route alerts to owners with clear runbooks.

## Legacy content
The following sections are imported from legacy v1 scheduler and SLA docs.

### Scheduler
# Kpi Scheduler
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Scheduler Framework

## Purpose
The KPI Scheduler Framework defines how KPI computations are scheduled, triggered, and governed in Cxofacts.  
It complements the KPI Call Framework by ensuring each KPI is refreshed according to its business criticality and data freshness SLA.

This ensures:
- CFOs and executives always see KPIs within expected freshness windows.  
- Developers have a standard orchestration pattern for scheduling KPI calls.  
- The platform enforces transparency via lineage, logs, and retry rules.  

## Core Concepts

- Frequency Classes
  - Real-Time / Streaming – KPIs derived from event streams (e.g., cash balance, transactions).  
  - Daily Batch – KPIs recalculated once per day (e.g., DSO, AR/AP turnover).  
  - Weekly Roll-Up – Summaries and trend KPIs (e.g., Opex by function).  
  - Period Close – KPIs aligned with month/quarter/year-end closes (e.g., compliance ratios, audit packs).  

- Triggers
  - Time-Based (cron-like scheduling).  
  - Event-Based (file arrival, ERP posting, anomaly trigger).  
  - Hybrid (time + dependency).  

- Dependencies
  - KPI jobs wait for upstream GDP tables or KPI groups to finish.  
  - Example: DSO depends on Receivables + Sales GDP tables.  

- Retry & Alerts
  - Failed KPI jobs retried automatically (configurable n times).  
  - SLA breaches alert ops + business owners.  

- Contracts
  - Each KPI definition declares a freshness SLA (e.g., max 24h lag).  
  - Scheduler enforces SLA compliance and logs deviations.  

## Scheduler Schema (YAML Example)
```yaml

    kpi_id: CFO-LQ-04
    contract_version: 1.0.0
    schedule:
      frequency: daily
      time: "02:00"
      timezone: "UTC"
    trigger:
      type: time
      cron: "0 2 * * *"
    dependencies:
      - GDP_CashBalance
      - GDP_BankStatements
    retry_policy:
      max_retries: 3
      backoff: exponential
    sla:
      freshness: "24h"
    alerting:
      channels: ["email:cfo-office@company.com","slack:#kpi-alerts"]
      severity: high
```

## Governance & Dev Notes
- Lineage Tracking – each scheduled run logs input GDP tables, version, and SQL hash.  
- Auditability – SLA and retry compliance auditable by ops and business.  
- Isolation – tenant-aware scheduling; no cross-tenant data leaks.  
- Scalability – lightweight KPIs may run inline; heavy KPIs scheduled via orchestration engine (e.g., Airflow).  
- Observability – metrics: run count, success/failure rate, avg duration, SLA violations.  

## Examples

### A) Cash Balance (CFO-LQ-04)
- Frequency: Real-time (streaming from bank feeds).  
- Trigger: Event-based (transaction arrival).  
- SLA: < 1h lag.  

### B) DSO (CFO-EF-02)
- Frequency: Daily batch.  
- Trigger: Time-based (ERP sync + EOD).  
- Dependencies: Receivables + Sales GDP tables.  
- SLA: < 24h lag.  

### C) Compliance Ratio (CFO-CM-01)
- Frequency: Monthly (aligned with financial close).  
- Trigger: Event-based (ERP close posting).  
- SLA: < 3 days post-close.  

## Why It Matters
- Trust – KPIs aligned with CFO expectations of freshness.  
- Consistency – one scheduling standard across all packs.  
- Governance – SLA-driven, logged, auditable.  
- Resilience – retries, alerts, and lineage protect from silent failures.  
- Scalability – supports real-time to quarter-close cycles uniformly.

## Diagrams

None

## Tables

None



## Glossary

None

### SLA
# Kpi Sla
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI SLA Framework

## Purpose
The KPI SLA Framework defines how Service Level Agreements are declared, enforced, and monitored for each KPI.  
It ensures CFOs, executives, and operations teams can trust KPI timeliness and reliability, with clear expectations and escalation when SLAs are breached.

## SLA Dimensions

- Freshness – KPI must be computed within X time of source data availability.  
- Latency – KPI query/call must return results within Y seconds.  
- Availability – KPI must be delivered at scheduled time (e.g., daily 9 AM IST).  
- Consistency – KPI must reflect consistent rules across variants/tenants (e.g., all entities close by T+1).  

## SLA Metadata (DDL Sketch)

```sql
CREATE TABLE kpi_sla (
  kpi_id             TEXT NOT NULL,
  contract_version   TEXT NOT NULL,
  sla_type           TEXT CHECK (sla_type IN ('freshness','latency','availability','consistency')) NOT NULL,
  target_value       INT NOT NULL,                 -- seconds/minutes/hours depending on type
  grace_window       INT DEFAULT 0,                -- additional allowed slack in seconds
  criticality        TEXT CHECK (criticality IN ('low','medium','high','critical')) NOT NULL,
  escalation_policy  TEXT,                         -- reference to escalation config
  created_at         TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (kpi_id, contract_version, sla_type)
);
```

- Every KPI version must declare SLA rows.  
- Multiple SLA types may be attached to a single KPI.  
- Escalation policies stored separately (can point to playbooks, alert configs).  

## Workflow for SLA Tracking

```
Scheduler triggers KPI run →
  SLA definition fetched from kpi_sla →
  Run metadata logged (start_time, end_time, status) →
  Compare actual vs SLA target →
    - If within SLA → mark pass.  
    - If beyond SLA but within grace_window → warn.  
    - If beyond grace_window → breach → escalate.  
Logs → Monitoring views → Alerts/Reports.
```

## Example: Liquidity Ratio (CFO-LQ-07)

- Freshness SLA: must be available within 2 hours after source data load.  
- Availability SLA: must be delivered daily by 09:00 IST.  
- Latency SLA: KPI Call must return within 3 seconds at P95.  
- Criticality: High.  
- Escalation: Slack warning at T+2h, Opsgenie page if > T+3h.  

## Integration with Other Frameworks

- KPI Scheduler Framework → Enforces SLA at job runtime.  
- KPI Logging Framework → Records SLA checks for every run.  
- KPI Monitoring Framework → Provides SLA compliance dashboards (pass %, breach count).  
- KPI Error Handling Framework → SLA breaches treated as error category with retry/escalation.  
- KPI Alerts & Reports Framework → Alerts and reports are triggered on SLA breaches.  
- KPI Versioning Framework → SLA definitions are version-bound (different clients/variants may have different SLA commitments).  

## Why It Matters

- Executive trust – CFOs see KPIs when expected, not “eventually”.  
- Operational accountability – SLA breaches are transparent and traceable.  
- Comparability – Standard SLA types ensure consistency across KPIs, tenants, and domains.  
- Scalability – SLA metadata + monitoring views allow automated compliance reporting across hundreds of KPIs.  

## Diagrams

None

## Tables

None



## Glossary

None
