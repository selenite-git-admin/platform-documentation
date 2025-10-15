# Action Catalog – Data Model

## Scope
Logical entities and relationships.

## Entities
### Template
Versioned template with schema and content.

| Field | Type | Req | Notes |
|------|------|-----|------|
| template_id | string | ✓ | PK |
| name | string | ✓ |  |
| kind | string | ✓ | notification,ticket,webhook,automation |
| status | string | ✓ | draft,published,deprecated |

### TemplateVersion
Published or draft version payload.

| Field | Type | Req | Notes |
|------|------|-----|------|
| template_id | string | ✓ | PK1 |
| version | integer | ✓ | PK2 |
| body | string | ✓ | content |
| schema_id | string |  | FK→Schema |
| signature | string |  | evidence ref |

## Relationships
- Template 1→* TemplateVersion

## Retention
- Logs: 30d · Metrics: 90d · Action history: 90d+
