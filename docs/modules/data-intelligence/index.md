# Data Intelligence

The Data Intelligence family transforms curated datasets into analytical, predictive, and anomaly-driven insights.  
It represents the intelligence layer of the DataJetty platform — converting validated data into forward-looking, decision-ready metrics and signals for executive use cases.

These modules operate over high-quality, GDP-aligned data from the Data Store and are orchestrated under the governance of Platform Control.  
They apply statistical and machine learning techniques to detect anomalies, generate forecasts, and produce predictive indicators that power dashboards, alerts, and automated actions in downstream systems.

---

## Purpose

Data Intelligence delivers analytical depth and predictive awareness across the enterprise dataset landscape.  
It empowers CFO, COO, and CGO intelligence packs with automated insights, anomaly identification, and trend projections.  
This layer enables continuous business monitoring and proactive response rather than retrospective reporting.

---

## Principles

- **DataJetty-native:** Operates exclusively on curated GDP and KPI layers managed by Data Store.  
- **Metadata-driven intelligence:** All models, parameters, and thresholds are registered and versioned in control registries.  
- **Explainable outcomes:** Predictions and anomalies are traceable to their source data and evidence trails.  
- **Continuous adaptation:** Models update based on fresh data while preserving historical baselines.  
- **Governed execution:** All analytics and inference jobs run through validated runtime environments and audited policies.  
- **Cross-pack integration:** Insights integrate directly with Activation workflows for automated business actions.

---

## Logical Flow

```
Data Store → Data Quality → Data Intelligence → Data Activation
```

The Data Intelligence family consumes validated, structured data, applies detection and prediction logic, and exposes results to activation and visualization layers.

---

## Integration with Governance

| System | Role |
|---------|------|
| **Schema Registry** | Validates data structures used for model training and inference. |
| **Policy Registry** | Defines retention, refresh frequency, and alert thresholds for analytical jobs. |
| **Evidence Ledger** | Records model execution, anomalies detected, and forecast outcomes. |
| **Runtime** | Executes anomaly detection and forecast pipelines in scheduled or streaming modes. |
| **Data Store** | Supplies Gold and GDP datasets as model inputs. |

---

## Modules

[Anomaly Detection](anomaly-detection/index.md)  
Identifies outliers and unusual behavior across operational and financial metrics, using configurable thresholds and statistical methods.

[Forecast](forecast/index.md)  
Generates trend projections and predictive metrics using historical data, seasonality, and contextual business variables.

[Predictive Streams](predictive-streams/index.md)  
Produces continuous, near real-time inference outputs that drive alerts, KPI early warnings, and adaptive business signals.

---

## Summary

The Data Intelligence family brings proactive awareness to the platform — transforming validated data into actionable foresight.  
Anomaly Detection flags risks, Forecast projects outcomes, and Predictive Streams maintain a living intelligence layer across business domains.  
Together, they turn historical reporting into continuous decision support.
