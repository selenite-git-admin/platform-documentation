# Tenant App – Onboarding Sources

## Purpose
Onboarding connects tenant systems (ERP, CRM, HRMS, file stores) into the platform.  
It establishes validated contracts and ensures data can be ingested reliably and securely.

## Workflow
1. **Select Source Type**
   - ERP, CRM, HRMS, file, or API endpoint.
2. **Authenticate**
   - Provide credentials or tokens with minimum required scope.
   - Validate authentication against the source system.
3. **Define Scope**
   - Choose entities, objects, or datasets to include.
   - Limit scope to reduce noise and risk.
4. **Validate Schema**
   - Introspect fields and match against contract requirements.
   - Identify drift, missing fields, or incompatible datatypes.
5. **Run Sample Ingest**
   - Fetch sample rows or objects.
   - Check row counts, null ratios, and enumerations.
6. **Confirm Contract**
   - Store schema contract in Schema Service.
   - Generate validation checklist for ongoing monitoring.

## Validation Checklist
- **Blocking checks**
  - Authentication successful with minimal scope.
  - Connectivity verified (latency, pagination, rate limits).
  - Schema alignment with contract.
  - Sample ingest succeeded with expected volume and datatypes.
- **Advisory checks**
  - Data freshness and lag hints.
  - Volume profiling and threshold warnings.
  - Rate limit advisories.

## Roles Involved
- **Admins**
  - Initiate and complete onboarding wizard.
- **Stewards**
  - Approve schema contracts and review validations.
- **Executives/Business Teams**
  - Consume onboarded data in curated reports once validated.

## Notes
- Failed validations can be retried step by step.
- All steps are logged with correlation IDs for audit.
- Contracts must be re‑approved if schema drift occurs after onboarding.
