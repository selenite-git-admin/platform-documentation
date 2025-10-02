# Schema Registry Storage

## Data Model

The registry stores:

- Metadata table – schema id, version, owner, classification, residency, timestamps  
- Definitions table – full JSON schema documents  
- History table – lifecycle events, approver, justification  
- Tags table – searchable attributes for discovery

## Residency

Every schema must declare residency rules.  
Residency is enforced at storage level: schemas for EU customers must reside in EU regions.  
Trust records residency approvals.

## Backup and Retention

- Daily backups retained for 90 days  
- Weekly backups retained for 1 year  
- Retired schemas retained for minimum of 7 years
