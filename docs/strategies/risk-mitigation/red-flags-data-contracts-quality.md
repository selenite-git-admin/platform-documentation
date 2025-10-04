# Data Contracts and Data Quality Red Flags

## Purpose
Identify risks related to data contracts and data quality during BareCount Data Action Platform engagements. Strong data contracts and reliable quality are essential for delivering governed KPIs. Weaknesses here can undermine trust in the platform.

## Context
BareCount relies on well-defined schemas, validated Golden Data Points, and consistent source system data. Customers often underestimate the importance of data quality and contracts, leading to delays and credibility issues. These red flags must be addressed early to prevent KPI failures or disputes over accuracy.

## Common Red Flags

### Weak or Missing Data Contracts
- No agreed schema between customer systems and BareCount
- Frequent schema changes without notification
- Multiple versions of the same field with inconsistent definitions
- Stakeholders unable to agree on KPI calculation rules

### Poor Data Quality
- High percentage of missing or null values in core fields
- Duplicates in transaction data such as invoices or orders
- Inconsistent identifiers across ERP, CRM, and HR systems
- Manual corrections in spreadsheets instead of source system fixes

### Lack of Ownership
- No assigned owner for data quality in finance, sales, or operations
- IT team disclaims responsibility, pointing to business teams
- Business teams defer issues back to IT without resolution

### Resistance to Validation
- Customer refuses to reconcile KPIs with system of record
- Pushback on variance checks, claiming “close enough”
- Unwillingness to fix upstream data issues in ERP or CRM

## Mitigation Actions
- Establish schema registry and contracts during onboarding
- Run automated validation checks during first ingestion
- Assign data owners for each domain with clear accountability
- Escalate unresolved data issues to executive sponsor
- Educate stakeholders that BareCount enforces governance and cannot bypass quality

## Example
During a POV, a finance customer provides invoice data with duplicate records. BareCount’s validation flags the duplicates and reconciliation fails. Instead of bypassing, the onboarding team escalates to the CFO sponsor, who directs the ERP team to fix source system processes. KPI validation succeeds after corrections.

## Notes
Data contracts and quality issues must be logged in the risk tracker. Red flags here are non-negotiable. BareCount’s value is derived from governed KPIs, which require clean and reliable data at the source.
