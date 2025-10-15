# Security and Compliance

## Purpose
Connectors interact directly with enterprise systems and often handle sensitive data and credentials.  
If connectors are not secured correctly, they can create risks such as data leakage, unauthorized access, or compliance violations.  
This section defines the security and compliance requirements that every connector must follow. It ensures that all connectors operate within the same controlled and auditable framework.

## Scope
This document applies to all connectors regardless of vendor or method.  
It covers requirements for credential handling, encryption, least privilege, data sensitivity tagging, and compliance controls.  
It also defines how connectors must interact with the platform’s security services such as secrets management, key management, and audit logging.

## Credential Management
Connectors must never store credentials in code or configuration files.  
All secrets must be retrieved at runtime from the platform’s secure secrets store, such as AWS Secrets Manager or HashiCorp Vault.  

Examples:
- SAP OData connectors must fetch OAuth client credentials from the secrets store.  
- JDBC connectors must fetch database usernames and passwords from the secrets store.  
- Salesforce REST connectors must fetch refresh tokens from the secrets store.  

Credentials must always be encrypted at rest and in transit. Connectors must handle credential rotation gracefully and must fail fast if credentials are invalid.

## Encryption
All network communication must use TLS 1.2 or higher.  
Data written to the Bronze layer must be encrypted at rest using the platform’s key management system.  
Any temporary files created during connector execution must also be encrypted and deleted immediately after use.  

Examples:
- A file connector that downloads CSVs from SFTP must store them in an encrypted temp directory before moving them into Bronze.  
- A bulk API connector that processes compressed data files must ensure those files are encrypted until they are deleted.

## Least Privilege
Connectors must request the minimum permissions required to function.  
IAM roles or service accounts assigned to connectors must be scoped only to the necessary APIs, databases, or buckets.  

Examples:
- A Salesforce connector should only request read access to objects that are required by the tenant.  
- An S3 file connector should only have access to the specified bucket and prefix.  

Requests for wildcard or administrative permissions must be rejected in security reviews.

## Data Sensitivity
Connectors must classify streams that contain sensitive data. This classification is declared in the manifest and enforced by governance modules.  

Examples of tags:
- **pii**: personally identifiable information such as names, addresses, or phone numbers.  
- **pci**: payment card information.  
- **phi**: protected health information.  

The compliance section of the manifest must declare which categories a connector can handle. Streams that contain sensitive data must also emit lineage metadata so governance tools can enforce masking and access policies.

## Auditability
All connector activity must be auditable.  
Logs must record connector identity, tenant, run id, and source system.  
Access to secrets must be logged by the secrets management service.  
Any security or compliance errors must be surfaced to the orchestrator and recorded in the compliance registry.  

Examples:
- A failed attempt to authenticate to SAP must be logged with run id, but without revealing credentials.  
- If a Salesforce connector attempts to extract a field tagged as PCI without permission, an audit record must be created.  

## Compliance Standards
Connectors must align with the platform’s compliance requirements such as ISO 27001, SOC 2, or GDPR.  
This includes:
- Data minimization: only extract required fields.  
- Right to erasure: support retraction of records if required by policy.  
- Residency enforcement: ensure data does not leave approved regions.  

Examples:
- A connector configured with `data_residency: in-region-only` must reject requests to write data outside the tenant’s region.  
- A GDPR deletion request must propagate through to the connector if the source supports record-level deletion.

## Principles
- Credentials must always be managed by the platform’s secure services.  
- Encryption in transit and at rest is mandatory.  
- Connectors must operate under least privilege.  
- Sensitive data must be tagged and governed.  
- All connector actions must be auditable.  
- Compliance requirements such as ISO, SOC, and GDPR must be enforced consistently.  

## Relationships
- Security modules provide secrets management, key management, and audit logging.  
- Governance modules enforce policies based on sensitivity tags and residency constraints.  
- Runtime modules surface audit logs and errors to operators.  

## Exclusions
This document does not define tenant-specific credential provisioning workflows. Those are covered in implementation documentation.  
It also does not describe compliance certifications in detail. The scope here is connector-level controls that support overall platform compliance.
