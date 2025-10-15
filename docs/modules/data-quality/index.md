# Data Quality Modules
The Data Quality Modules safeguard the reliability and trustworthiness of all datasets within the platform.
They ensure that data meets defined standards for freshness, completeness, accuracy, 
and consistency before it is consumed by analytics, activation, or intelligence modules.
Data Quality operates as both a validation engine and a continuous observability layer, 
integrating deeply with Platform Control and Data Store.

<div class="info-box">

Data Quality maintains the assurance that every dataset in the platform is correct, timely, 
and compliant with its declared contract. 
It serves as the monitoring and validation plane between data movement and data consumption, 
continuously evaluating both schema and business-level quality metrics.  

</div>

- Quality enforcement in DataJetty is fully metadata-driven.  
- Validation rules, thresholds, and SLAs are declared and versioned within control registries.  
- Each dataset undergoes automated checks during ingestion and transformation, 
  with results persisted and auditable through the Evidence Ledger.

## Modules

[Data Observability](data-observability/index.md) collects and publishes quality and health signals. 
It exposes standard metrics and snapshots that other modules consume.

[DQC](dqc/dqc-overview.md) evaluates rule packs and computes a quality score and verdict that promotion gates use. 
Waivers are tracked and auditable.

## Principles

- **Metadata-based checks:** All validation rules are defined as control metadata, not hard-coded scripts.  
- **Automated enforcement:** Quality gates run automatically during ingestion, transformation, and publishing.  
- **Observability-first:** Data freshness, drift, and completeness are continuously tracked.  
- **Evidence-backed:** Every validation result is recorded and auditable through Platform Control’s Evidence Ledger.  
- **Fail-safe pipelines:** Downstream consumers only access datasets that meet validation thresholds.  
- **Continuous improvement:** Metrics and anomalies feed back into governance and pipeline tuning.

## Logical Flow

```
Data Acquisition → Data Store → Data Quality → Data Activation → Data Intelligence
```
Quality validation sits between ingestion and consumption, measuring compliance against defined contracts and 
schemas while updating observability metrics in near real time

## Integration with Governance

| System              | Role                                                                                |
|---------------------|-------------------------------------------------------------------------------------|
| **Policy Registry** | Hosts quality rule definitions and SLA thresholds.                                  |
| **Schema Registry** | Provides expected field-level definitions and constraints.                          |
| **Evidence Ledger** | Stores validation outcomes and audit trails.                                        |
| **Runtime**         | Executes DQC and observability checks as part of ingestion and transformation jobs. |
| **Data Store**      | Supplies datasets and metadata lineage for validation scope.                        |

## Summary

The Data Quality family forms the verification layer of DataJetty’s data lifecycle.  
It ensures that every dataset published by the platform is accurate, compliant, and traceable, with automated enforcement backed by immutable audit evidence.  
Observability provides visibility; DQC ensures discipline; together they build trust in every downstream insight.
