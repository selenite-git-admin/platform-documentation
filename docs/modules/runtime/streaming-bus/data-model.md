# Streaming Bus – Data Model

## Scope
Logical entities and relationships.

## Entities
### Topic
Logical stream.

| Field | Type | Req | Notes |
|------|------|-----|------|
| name | string | ✓ | PK |
| partitions | integer | ✓ |  |
| retention_h | integer | ✓ |  |

### ConsumerGroup
Consumer coordination.

| Field | Type | Req | Notes |
|------|------|-----|------|
| group | string | ✓ | PK |
| topic | string | ✓ | FK→Topic |
| lag | integer |  |  |

## Relationships
- Topic 1→* ConsumerGroup

## Retention
- Logs: 30d · Metrics: 90d · Job history: 180d+
