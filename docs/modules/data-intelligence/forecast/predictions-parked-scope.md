# Predictions Module – Parked Scope

**Audience:** Data science leads, platform engineers, and product owners  
**Status:** Working draft  
**Purpose:** Identify deferred and future-scope areas for the Predictions module within the Tenancy platform. This document defines what is intentionally excluded from the current delivery phase and records dependencies for future activation.

## Context

The Predictions module follows the Anomaly Detection layer and is designed to provide forward-looking insights based on historical trends and behavioral data. While foundational telemetry and data pipelines are available, predictive model deployment, feature generation, and UI integration are deferred until future releases.

## Scope Classification

Items are classified as:
- **Parked for future delivery** – planned but not part of current sprint or release.  
- **Explicitly not covered** – requires a different architecture or external dependency.  
- **In scope elsewhere** – covered by existing modules such as Data Layer, Observability, or Policy.

## Parked for Future Delivery

### Predictive Models and Algorithms
- Forecasting models for revenue, churn, usage, and collection risk per tenant.
- Raw Material Cost Forecasting based on procurement, supplier, and market index data.
- Predictive variance analysis between forecasted and actual landed cost.
- Integration with Anomaly Detection layer for cost deviation alerts.
- Commodity-level trend dashboards and sourcing risk projection.

- Probabilistic forecasts using Prophet, ARIMA, and ensemble models.
- Feature store and embedding registry integration for model input standardization.
- Model explainability and confidence scoring surfaces.
- Per-tenant adaptive model selection and retraining schedules.

### Data and Model Pipeline
- Automated feature extraction from Golden Data Points and KPI packs.
- Model deployment pipeline integrated with AWS SageMaker or Glue ML jobs.
- CI/CD for model versioning and automated rollback based on validation metrics.
- Scheduled inference jobs with SLA monitoring.

### Integration with Tenancy Layer
- Prediction endpoints for consumption via Tenancy APIs.
- Forecast overlays in dashboards and anomaly timelines.
- UI components for confidence intervals and next-interval projections.

### UI and Experience
- Customer Portal predictive views for “forecasted usage” and “predicted risk.”
- Admin Portal model monitoring and performance dashboards.
- Feedback loops for manual override and labeling mispredictions.

### Governance and Audit
- Policy layer validation for automated actions triggered by predictions.
- Prediction audit trail with model version, confidence, and decision outcome.
- Drift detection, retraining triggers, and bias monitoring.

## Explicitly Not Covered

- Offline model training on customer premises or hybrid compute clusters.  
- Real-time predictive control loops for auto-scaling or quota throttling.  
- Generative AI–driven narrative insights or natural language explanations (separate AI Activation module).  
- External marketplace integrations for third-party predictive models.

## Dependencies

- Data layer enrichment (Silver and Gold) completion for consistent feature pipelines.  
- Schema and feature registry design for GDP-level features.  
- Model store and metadata catalog service for reproducibility.  
- Policy engine extension to interpret predictive obligations.  
- Resource quota extensions for model inference workloads.

## Review and Change Management

- Reviewed every release cycle after Anomaly Detection stability review.  
- Requires formal RFC and design approval before entering active scope.  
- Initial experiments tracked under the “Predictive Intelligence” stream in DataJetty backlog.

## Summary

The Predictions module will enable forecasting and forward-looking insights across tenants once foundational telemetry stabilizes. Current delivery defers predictive modeling, UI integration, and automated decision feedback loops. The module depends on mature feature pipelines, policy integration, and dedicated ML deployment infrastructure before activation.