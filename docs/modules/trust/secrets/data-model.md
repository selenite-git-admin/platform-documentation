# Secrets – Data Model

## Scope
Logical entities and relationships.

## Entities
### Secret
Logical secret addressable by path.

| Field | Type | Req | Notes |
|------|------|-----|------|
| path | string | ✓ | PK |
| created_at | datetime | ✓ |  |
| owner | string |  |  |

### SecretVersion
Encrypted value and metadata.

| Field | Type | Req | Notes |
|------|------|-----|------|
| path | string | ✓ | PK1 |
| version | integer | ✓ | PK2 |
| ciphertext_b64 | string | ✓ |  |
| key_ref | string | ✓ | FK→Encryption.KeyVersion |
| metadata | object |  | rotation, owner |

### Lease
Short‑lived credentials or tokens.

| Field | Type | Req | Notes |
|------|------|-----|------|
| lease_id | string | ✓ | PK |
| role | string | ✓ |  |
| tenant_id | string | ✓ |  |
| expires_at | datetime | ✓ |  |

## Relationships
- Lease belongs to Tenant

## Retention
- Logs: 30d · Metrics: 90d · Evidence (ledger): 90d+
