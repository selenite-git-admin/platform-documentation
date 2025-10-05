# Taxonomy — BareCount™ Platform

> Canonical terminology and relationships for the BareCount™ Data Action Platform.  
> Use this as the single source of truth for naming, scope, and interactions.

---

## 1) Purpose & Scope

- **Purpose:** Freeze the platform’s conceptual map so all docs, UX, APIs, and diagrams use the same language.
- **Scope:** Architecture layers, core artifacts, execution surfaces, lifecycles, and cross-cutting services.

---

## 2) Canonical Map (Layers & Surfaces)

```mermaid
graph TD
  subgraph SoR["Systems of Record (ERP/CRM/HRMS/MES)"]
    S1[ERP]
    S2[CRM]
    S3[MES]
    S4[HRMS]
  end

  subgraph CP["Control Plane"]
    CP1["Contract Authoring & Registry"]
    CP2["Governance / Approvals / RBAC"]
    CP3["Observability & SLOs"]
    CP4["Plan Compiler to Plan Artifact"]
  end

  subgraph DP["Data Plane"]
    DP0["Ingest & Source Adapters"]
    DP1["Bronze (Raw/Landing)"]
    DP2["Silver (Standardized/Reconciled)"]
    DP3["Gold (Curated/Business-Ready)"]
    DP4["KPI System (Publish + Evidence)"]
  end

  subgraph DAL["Data Action Layer"]
    A1["Action Runtime: Triggers, Idempotency, Compensation"]
    A2["Reverse Connectors: ERP/CRM write-back"]
    A3["Evidence Emitter"]
  end

  subgraph Apps["Applications: Surfaces"]
    HA["Host App: Admin/Governance"]
    TA["Tenant App: KPI + Data Action Console"]
  end

  %% Flows
  S1 --> DP0
  S2 --> DP0
  S3 --> DP0
  S4 --> DP0

  CP1 --> CP4
  CP2 --> CP4
  CP4 --> DP1
  DP1 --> DP2
  DP2 --> DP3
  DP3 --> DP4

  DP4 --> DAL
  DAL --> A2
  DAL --> A3

  HA --- CP
  TA --- DP4
  TA --- DAL
```


## 3) Core Artifacts & Relationships

```mermaid
graph LR
  C[Contract]:::art -->|compiled into| PA[Plan Artifact]:::art
  PA -->|materializes| DS[(Datasets)]:::obj
  DS -->|builds| GDP[Golden Data Points]:::obj
  GDP -->|feeds| KPI[KPI]:::art
  KPI -->|drives| DA[Data Action]:::art
  C -->|binds| ORG[Origin]
  C -->|binds| LOG[Logic]
  C -->|binds| VAL[Validation]
  C -->|binds| DEL[Delivery]
  KPI -->|emits| EVD[Evidence]:::obj
  DA -->|emits| EVD

  classDef art fill:#eef7ff,stroke:#2b6cb0,stroke-width:1px,color:#1a365d;
  classDef obj fill:#f6ffed,stroke:#2f855a,stroke-width:1px,color:#22543d;
```

## 4) Lifecycle State Machines

### 4.1 Contract Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Proposed: author submits
  Proposed --> Approved: governance gate
  Approved --> Active: compiled & applied
  Active --> Deprecated: superseded
  Deprecated --> Archived: retired
  Active --> RolledBack: policy/evidence breach
  RolledBack --> Active: remediated
```

### 4.2 Plan Artifact Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Approved
  Approved --> DualRun: old + new compare
  DualRun --> Active: success criteria met
  DualRun --> Rollback: drift/exceedance
  Active --> Rollback
  Rollback --> Approved: fix & retry
```

### 4.3 KPI Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Draft
  Draft --> Validated: pre-checks pass
  Validated --> Approved
  Approved --> Published
  Published --> Quarantined: DQC/Policy fail
  Quarantined --> Published: remediated
  Published --> Deprecated
  Deprecated --> Archived
```

### 4.4 Data Action Lifecycle
```mermaid
stateDiagram-v2
  [*] --> Defined
  Defined --> Enabled
  Enabled --> Executing: trigger fires
  Executing --> Succeeded: evidence emitted
  Executing --> Failed: retry/compensation
  Failed --> Enabled: manual resume
  Enabled --> Disabled: policy/owner action
```

---

## 5) Trigger & Enforcement Model

```mermaid
flowchart TD
  subgraph Triggers
    T1["Event Trigger"]:::t
    T2["Schedule Trigger"]:::t
    T3["Manual Trigger"]:::t
  end

  T1 --> G["Gate Checks"]
  T2 --> G
  T3 --> G

  G --> P["Policy & RBAC Enforcement"]
  P --> R["Runtime: Idempotent Execution"]

  R --> C1["Compensation?"]
  R --> E["Evidence Emit"]

  C1 --> E

  classDef t fill:#fff5f5,stroke:#c53030,color:#742a2a;
```

## 6) Cross-Cutting Services (Where They Bite)

| Concern            | Control Plane                            | Data Plane                                   | Data Action Layer                             |
|--------------------|-------------------------------------------|----------------------------------------------|-----------------------------------------------|
| Identity & RBAC    | Authoring, approvals, registry access     | Build/read KPIs, evidence visibility         | Action ownership, trigger permissions         |
| Secrets & KMS      | Contract secrets refs, key policies       | Source creds, encryption at rest/in transit   | Connector creds, key usage audit              |
| Telemetry          | Policy eval metrics, governance latency   | Pipeline latency, freshness, success rates    | Action latency, retry counts, success ratio   |
| Lineage            | Contract lineage refs                     | Node/edge graph, impact analysis             | KPI→Action link & reverse connectors          |
| DQC                | Policy definitions (fail/soft-fail)       | Pre/post checks, reconcile, anomaly          | Preconditions for actions                     |
| Alerts             | Governance breaches                        | Freshness/drift/validation violations        | Action failures, compensation invoked         |
| Cost/Quota         | Plan budgets, approval thresholds         | Compute/storage quotas per tenant/artifact    | Action rate limits and budgets                |
| BCDR               | Registry backup, approval recovery        | Dataset/KPI backup & restore, RPO/RTO tiers  | Action replay safety, dedupe/idempotency      |
| Compliance/Evidence| Approval trails, policy proofs            | Validation evidence, lineage, data access    | Action proofs, external system receipts       |

---

## 7) Residency & Hybrid Patterns

```mermaid
graph LR
  subgraph On-Prem
    OP1["SoR: ERP/CRM/MES/HRMS"]
    OP2["Local Staging/Agent"]
  end
  subgraph Cloud_BareCount["Cloud: BareCount"]
    C1["Control Plane"]
    C2["Data Plane"]
    C3["Data Action Layer"]
    C4["Evidence Store"]
  end

  OP1 -- "secure tunnel" --> OP2
  OP2 -- "masked/aggregated feed" --> C2
  C2 --> C3
  C3 -- "reverse connector" --> OP1
  C3 --> C4
  C2 --> C4
  C1 --> C2
```

## 8) RACI (High-Level Responsibilities)

| Area                | Host App (Admin) | Control Plane | Data Plane | Data Action Layer | Tenant App |
|---------------------|------------------|---------------|-----------:|------------------:|-----------:|
| Author Contracts    | R                | A             | C          | C                 | I          |
| Approvals/Governance| R/A              | A             | C          | C                 | I          |
| Compile Plan        | C                | R/A           | C          | I                 | I          |
| Build KPIs          | I                | C             | R/A        | I                 | I          |
| Run Actions         | I                | C             | I          | R/A               | C          |
| Evidence & Audits   | C                | R/A           | R          | R                 | C          |
| SLOs & Alerts       | C                | R/A           | R          | R                 | C          |

(A = Accountable, R = Responsible, C = Consulted, I = Informed)

---

## 9) Naming & Versioning Conventions

- **Contracts:** `MC.<domain>.<metric>.<major>` → `MC.FIN.AR.DSO.v1`
- **Plan Artifacts:** `PA.<domain>.<group>.<major>` → `PA.FIN.AR.v1`
- **Datasets:** `bronze|silver|gold.<domain>.<entity>`
- **KPIs:** `kpi.<domain>.<name>`
- **Data Actions:** `da.<domain>.<name>`
- **States:** `draft → proposed → approved → dual-run → active → deprecated → archived`
- **IDs:** include `tenant_id`, `plan_id`, `contract_id`, `version`, and `trace_id` in logs/evidence.

---

## 10) Quick Compliance Hooks

- **Evidence Pack** per KPI/period: contract hash, plan version, lineage snapshot, validation results, action receipts.
- **Dual-Run** required when **logic** or **origin** changes; 1:1 diff threshold must pass before promotion.
- **Soft-fail policy** only for non-financial, non-regulatory KPIs; **hard-fail** elsewhere.

---

**This taxonomy is canonical.**  
If a term or relationship isn’t here, propose an ADR before using it anywhere else.
