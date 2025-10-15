# Authorization – API

### Authorize
**Method**: `POST`  
**Path**: `/authz/evaluate`  
**Purpose**: Return decision for subject on resource

**Request**
```json
{
  "subject": "user:abc",
  "action": "read",
  "resource": "kpi:revenue_mtd"
}
```

**Response**
```json
{
  "decision": "permit",
  "policy_id": "pol-123"
}
```

