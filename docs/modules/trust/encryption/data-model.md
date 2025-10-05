# Encryption – Data Model

## Scope
Logical entities and relationships.

## Entities
### KeyAlias
Logical alias that points to an active key version.

| Field | Type | Req | Notes |
|------|------|-----|------|
| alias | string | ✓ | PK |
| active_kid | string | ✓ | FK→KeyVersion.kid |
| rotation_policy | string |  | e.g., 90d |

### KeyVersion
Specific key material reference managed by KMS/HSM.

| Field | Type | Req | Notes |
|------|------|-----|------|
| kid | string | ✓ | PK |
| provider | string | ✓ | aws-kms, gcp-kms, hsm |
| created_at | datetime | ✓ |  |
| state | string | ✓ | active, retired |

## Relationships
- KeyAlias 1→1 KeyVersion (active)

## Retention
- Logs: 30d · Metrics: 90d · Evidence (ledger): 90d+
