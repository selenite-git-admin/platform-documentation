# Schema Registry Dependencies

## Module Dependencies

- Host Policy Engine – enforces approval workflows  
- Trust Ledger – stores evidence of approvals, deprecations, rollbacks  
- Access Module – enforces who can propose, approve, and read  
- Runtime Module – emits lifecycle events, schedules validation jobs  
- Storage Module – enforces schema at rest  
- Compute Module – validates schema during job execution  
- Consumption Module – publishes schema metadata alongside APIs

## Deployment Dependencies

- Database: PostgreSQL for registry metadata  
- Artifact store: S3 or equivalent for schema definitions  
- Messaging: Kafka or SNS for lifecycle events  
- Cache: Redis for high-volume schema reads
