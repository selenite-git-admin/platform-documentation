# Ingestion and Landing

## Purpose
Ingestion and landing pipelines are the controlled entry point for data into the BareCount Data Action Platform. Their role is to capture data from connectors, validate it against contracts, and land it in the Raw Stage with full lineage and reproducibility. This stage ensures that variability from source systems is contained and never leaks uncontrolled downstream.

## Context
Many enterprise ingestion processes accept whatever source systems emit and only detect issues later. This leads to drift, failed jobs, and loss of trust. BareCount addresses this with a contract first model. Each incoming stream must declare an extractor schema from the connector. The extractor schema is validated against the Data Contract Registry before data is landed. Violations generate governance events rather than silent failures. The connector remains stateless, and pipeline state is maintained centrally in the platform.

## Key Capabilities

### Extractor Schema
- Defined by the connector for each stream.  
- Describes expected fields, types, and relationships as emitted from the source.  
- Provides the baseline for validation before landing.

### Contract Validation
- Extractor schema is compared against the registered data contract in the Governance module.  
- If aligned, records land in the Raw Stage with metadata.  
- If drift is detected, records still land, but the run is flagged with a contract violation event.  
- Governance teams must act to accept or reject the drift before downstream processing continues.

### Stateless Connectors and Central State
- Connectors do not track their own progress.  
- Incremental cursors, watermarks, and checkpoints are managed by the platform.  
- This design allows connectors to be redeployed or scaled without losing continuity.

### Landing Zone
- Data is landed in the Raw Stage, partitioned by load date and run ID.  
- Metadata includes schema hash, contract version, source ID, and system build information.  
- No transformations are applied other than minimal coercions for storage compatibility.

### Quarantine
- Records that cannot be parsed according to the extractor schema are routed to a quarantine area.  
- Quarantine records carry run metadata, payload samples, and error descriptions.  
- This ensures downstream layers remain unaffected while issues are investigated.

### Security and Compliance
- Credentials, tokens, and network profiles are never embedded in pipeline code.  
- They are retrieved at runtime from the secrets manager.  
- Data is encrypted in transit and at rest.  
- Access is logged for audit in the Evidence Ledger.

## Operating Model
- Connector developers define extractor schemas as part of connector publishing.  
- Tenant administrators onboard streams by binding extractor schemas to approved data contracts.  
- Each run produces metadata: contract version, schema hash, record counts, lineage, and run status.  
- Violations create events routed to governance teams, who decide whether to update contracts or block progression.  
- Failed or partial runs are retried with exponential backoff and logged in observability dashboards.

## Example
An SAP OData connector extracts `GLAccounts` with fields `AccountID, Description, LastUpdated`.  
- If these match the registered contract, records land in the Raw Stage partitioned by load date.  
- If SAP introduces a new field `AccountType`, ingestion still lands the data but flags drift. Governance reviews and either amends the contract or rejects the change.

## Notes
Ingestion and landing should remain lightweight. Their role is capture, validation, and lineage stamping. Transformation, business logic, and KPI derivation belong to later pipeline stages. Keeping ingestion disciplined ensures trust, reproducibility, and clean handoff to downstream teams.
