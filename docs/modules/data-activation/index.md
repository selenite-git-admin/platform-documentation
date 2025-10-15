# Data Activation

The Data Activation family transforms insights into business actions.  
It delivers verified datasets, KPIs, and analytical outcomes from DataJetty into downstream applications, APIs, and workflows.  
Activation represents the point where governed data becomes operational, closing the loop between insight generation and business execution.

This family bridges the intelligence and operational layers of the platform.  
It packages curated outputs into consumable formats, manages controlled delivery to external systems, and orchestrates automated actions based on insights, forecasts, and thresholds defined upstream.  
It’s where analytics move from dashboards to decisions.

---

## Purpose

Data Activation ensures that business users and systems receive trustworthy, contextualized data in the form they need — reports, APIs, notifications, or automated triggers.  
It delivers the last mile of the platform’s data lifecycle, converting analytics into measurable business outcomes.

---

## Principles

- **Governed output:** Every delivery is backed by contract metadata and lineage proofs from Platform Control.  
- **Traceable actions:** All outbound data and triggered workflows carry unique evidence and job context.  
- **Format-agnostic delivery:** Supports APIs, reports, and connectors for system-to-system communication.  
- **Automation-first:** Allows creation of rule-based or predictive workflows that act on data signals.  
- **Security-aligned:** Inherits access, entitlement, and policy layers from Core and Subscription families.  
- **Observable delivery:** Tracks completion, latency, and target acknowledgments for every delivery event.

---

## Logical Flow

```
Data Store → Data Intelligence → Data Activation → External Systems / Business Users
```

Data Activation is the distribution and action layer — it consumes curated data and predictions to produce operational, reportable, or automated outcomes.

---

## Integration with Governance

| System | Role |
|---------|------|
| **Policy Registry** | Defines delivery restrictions, destinations, and security classifications. |
| **Evidence Ledger** | Records every delivery, trigger, and workflow execution as immutable proof. |
| **Subscription Enforcement** | Validates tenant and entitlement rules before delivery. |
| **Runtime** | Executes activation pipelines, notifications, and workflow triggers. |
| **Core Security** | Provides authentication, encryption, and signing for outbound payloads. |

---

## Modules

[Delivery](delivery/index.md)  
Manages distribution of datasets, KPIs, and reports to external systems, APIs, or visualization tools with guaranteed delivery and audit trails.

[Action](action/index.md)  
Implements rule-based and predictive workflows that translate analytical insights into automated business actions or alerts.

---

## Summary

The Data Activation family operationalizes intelligence.  
It ensures that every metric, anomaly, and forecast transitions from passive information to tangible impact — routed, executed, and verified through a governed, auditable process.  
Delivery provides reach; Action provides responsiveness; together, they close the data-to-decision loop.
