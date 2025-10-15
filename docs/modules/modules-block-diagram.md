# Architecture Map

This page complements the Modules Framework with visual maps of how families interact across Core, Control, and Data planes. The diagrams are text based so they can live in version control and evolve with the platform.

## System Block Diagram

```mermaid
flowchart LR
    %% Planes
    subgraph CorePlane[Core Plane]
        Core[Core]
    end

    subgraph ControlPlane[Control Plane]
        Sub[Platform Subscription]
        Ctl[Platform Control]
        Ops[Platform Operations]
    end

    subgraph DataPlane[Data Plane]
        Acq[Data Acquisition]
        Store[Data Store]
        DQ[Data Quality]
        Intel[Data Intelligence]
        Act[Data Activation]
    end

    %% Edges
    Core --> Sub
    Sub --> Ctl
    Ctl --> Ops
    Ops --> Acq
    Acq --> Store
    Store --> DQ
    DQ --> Intel
    Intel --> Act

    %% Cross cutting read paths
    Core -. uses .-> Ops
    Acq -. reads policies .-> Ctl
    Store -. schemas .-> Ctl
    DQ -. evidence .-> Ctl
    Intel -. evidence .-> Ctl
    Act -. evidence .-> Ctl
```

## Runtime Sequence

```mermaid
sequenceDiagram
    autonumber
    participant User as User or System
    participant Core as Core
    participant Sub as Platform Subscription
    participant Ctl as Platform Control
    participant Ops as Platform Operations
    participant Acq as Data Acquisition
    participant Store as Data Store
    participant DQ as Data Quality
    participant Intel as Data Intelligence
    participant Act as Data Activation
    participant Led as Evidence Ledger

    User->>Core: Authenticate
    Core->>Sub: Resolve tenant and entitlements
    Sub->>Ctl: Load contracts, schemas, policies
    Ops->>Acq: Dispatch scheduled or triggered job
    Acq->>Store: Write Bronze and Silver
    Store->>DQ: Request validation and SLA checks
    DQ->>Store: Certify dataset for consumption
    Intel->>Store: Read certified Gold and GDP
    Intel->>Act: Publish insights and predictive indicators
    Act->>User: Deliver outputs and workflow actions
    Act->>Led: Record delivery evidence
    DQ->>Led: Record validation evidence
    Store->>Led: Record merge evidence
```

## Producer Consumer Matrix

| Producer | Consumer | What moves |
|----------|----------|------------|
| Platform Subscription | Platform Control | Tenant and entitlement context |
| Platform Control | Platform Operations | Policies, schemas, contract metadata |
| Platform Operations | Data Acquisition | Schedules and execution context |
| Data Acquisition | Data Store | Landed and conformed data with lineage |
| Data Store | Data Quality | Datasets and dataset metadata |
| Data Quality | Data Intelligence | Certified datasets and quality status |
| Data Intelligence | Data Activation | Insights, anomalies, forecasts |
| All families | Evidence Ledger | Evidence records with operation ids and hashes |

## Reading the Map

The block diagram shows the three planes and the main dependency direction. Cross cutting edges represent registry reads and evidence writes. The sequence diagram shows a typical job path from authentication to delivery with evidence recorded at each step. Together these views provide a consistent reference for onboarding and design reviews.
