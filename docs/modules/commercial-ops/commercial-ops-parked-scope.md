# Wishlist / Parked Scope

## Overview

This document captures the deferred or future scope items for the Commercial-Ops module. These represent advanced capabilities planned for Phase 2 and beyond. Each item expands on the baseline architecture built in Phase 1 and aligns with AWS-native design patterns. The document serves as a parking zone for backlog items that require further design validation, dependency readiness, or cost modeling.

---

## Deferred Scope Items

| Category | Description | Dependencies | Target Phase |
|-----------|-------------|---------------|---------------|
| Automated invoicing | Trigger invoice generation via scheduled Lambda or CloudWatch event, eliminating manual API calls. | Stable cost allocation, recon reliability | Phase 2 |
| Payment gateway integration | Integrate Stripe or Razorpay for direct card or UPI payments. Keep current manual transfer path as fallback. | PCI compliance, webhook verification | Phase 2 |
| Auto reconciliation | Reconcile incoming payment webhooks with invoice and CUR data automatically. | Payment gateway integration | Phase 2 |
| Dynamic pricing engine | Allow operators to model custom pricing curves based on usage projections. | Historical usage data, cost API | Phase 3 |
| Multi-currency support | Convert tenant totals to preferred display currency with AWS FX rates or external feed. | Data layer currency normalization | Phase 3 |
| Forecasting | Predict usage or cost trends using time-series analysis (Glue ML or Amazon Forecast). | Daily snapshots, 90-day data history | Phase 3 |
| Tiered SKU catalog | Support reusable SKU definitions for add-ons and top-ups beyond simple metric caps. | Plan service and SKU registry | Phase 2 |
| Ledger integration | Sync invoices and payments with QuickBooks or Zoho Books via secure API. | Stable invoice schema | Phase 2 |
| Self-service plan management | Allow tenants to upgrade or downgrade plans directly in UI with proration. | Plan versioning and API safeguards | Phase 2 |
| Automated seat allocation | Link seat consumption to identity provider (OIDC user count). | Tenant identity linkage | Phase 3 |
| Audit and export automation | Export audit logs and evidence monthly to S3 or external archive. | Evidence versioning | Phase 2 |
| Cost anomaly detection | Implement ML-based outlier detection on metric variance. | CUR freshness, historical training data | Phase 3 |
| Alert policy versioning UI | Editable alert policies with version diff view. | Observability policy store | Phase 2 |
| Synthetic tenant testing | Create synthetic tenants for billing regression validation. | Automation pipeline | Phase 2 |

---

## Future Enhancements

### 1. Fine-Grained AWS Cost Integration

- Implement per-service allocation curves (e.g., EC2 vs NAT Gateway vs S3) with stored weight maps.
- Add Glue job partition auto-discovery for new CUR months.
- Include proactive validation on CUR size anomalies and missing partitions.
- Integrate cost and usage forecast APIs for projected monthly billing accuracy within ±3%.

### 2. Invoicing Automation

- Daily Lambda job checks `fact_cost_allocated` for completed periods and triggers invoice generation automatically.
- Introduce approval workflow for operator billing before final issuance.
- Auto-distribute invoice PDFs via email using SES templates and tenant billing contacts.
- Introduce pre-invoice “draft” status for manual validation before issue.

### 3. Payment Automation and Reconciliation

- Webhook listener for payment success/failure events.
- Map external provider reference (e.g., UTR, txn_id) to `payment_txn.provider_ref`.
- Auto-update invoice status to `paid` when full payment confirmed.
- Generate daily reconciliation summary and flag variances >0.5%.

### 4. AI and Anomaly Detection

- Apply statistical baselines to detect sudden deviations in egress_gb, storage_gb_peak, or runner_hours.
- Integrate AWS Lookout for Metrics or use in-house LSTM-based forecast comparison.
- Auto-create alerts when anomalies exceed 2σ deviation.
- Store anomaly results in dedicated `anomaly_events` table linked to evidence SQL.

### 5. Multi-Currency Support

- Currency exchange feed from AWS Billing FX API or third-party provider.
- Store exchange rates in `fx_rate_master` (date, currency_pair, rate).
- Render UI with tenant-preferred currency while retaining USD ledger base.
- Add audit trail for rate usage per invoice.

### 6. Dynamic Pricing and Quoting

- Extend plan schema to include tiered rate slabs, e.g., first 100 GB → $0.10, next 400 GB → $0.07.
- Add simulation endpoint `/api/v1/pricing/estimate` for “what-if” projections.
- UI to show projected monthly cost if usage increases by 10–50%.

### 7. Operator Automation and CI/CD

- Infrastructure-as-code deployment for plan registry and allocation rules.
- GitOps-style approval for production plan or metric schema updates.
- Lambda-driven validation before applying tag policy or allocation changes.
- Canary verification before promoting new rules to production.

### 8. Reporting and Export Services

- CSV and PDF exports for all billing tables.
- Scheduled reports to S3 with signed URL expiry policies.
- Support direct push to external BI systems (QuickSight, Power BI).

### 9. Data Lineage and Provenance

- Add lineage tracking to every transformation and cost allocation job.
- Capture input CUR partition digest, rule version, and evidence query ID.
- Generate monthly provenance manifest for audit export.

### 10. Observability Deepening

- Link alert events to AWS Health Dashboard where applicable.
- Enable cross-account CloudWatch dashboards for multi-region cost visibility.
- Add service quotas to monitoring (e.g., Lambda concurrency, Glue limits).
- Track budget forecast accuracy as a new metric for FinOps maturity.

---

## Integration Hooks (Phase 2/3 Targets)

| Integration | Purpose | Notes |
|-------------|----------|-------|
| DataJetty Admin Plane | Cross-link tenant provisioning and plan binding | Uses shared tenant_id registry |
| CFO Pack | Cost variance feeds and billing audit signals | Integration through KPI API |
| AWS Marketplace | Optional listing for subscription-based tenants | Requires new account model |
| External Payment Gateways | Direct checkout or auto reconciliation | Stripe, Razorpay, or internal bank API |
| Accounting Systems | Ledger synchronization | QuickBooks Online, Zoho Books |
| Analytics Layer | Cost and revenue dashboards | Aggregates data from `fact_cost_allocated` and `invoice_header` |
| Synthetic Data Service | Test data generation for usage and billing | Depends on seeded metrics and templates |

---

## Technical Prerequisites

- Complete CUR ingestion automation and partition validation.
- Finalize Aurora schema migration and versioning model.
- Enable Glue or Lambda orchestration for plan cost computation.
- Extend Observability to capture operator automation metrics.
- Review tagging schema for tenant_id and plan_code consistency.

---

## Roadmap Summary

| Phase | Focus | Key Deliverables |
|-------|--------|------------------|
| Phase 2 | Automation and Integration | Auto invoicing, payments, reconciliation, plan CI/CD, external integrations |
| Phase 3 | Intelligence and Prediction | Dynamic pricing, multi-currency, forecasting, anomaly detection |
| Phase 4 | Ecosystem and Marketplace | Marketplace listing, cross-platform analytics, advanced reporting |

---

## Notes

- All Phase 2–4 features will maintain backward compatibility with existing Phase 1 API and schema.
- Incremental migration is preferred over schema refactoring.
- All new components must comply with the same IAM, tagging, and audit standards defined in `security.md`.
- Deferred scope will be revisited quarterly after core Commercial-Ops modules reach production maturity.
