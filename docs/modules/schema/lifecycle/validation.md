# Lifecycle: Validation & Enforcement

## Pipeline
1. **Canonicalize** JSON Schema (draft 2020‑12).
2. **Ruleset** check (additive/backward).
3. **Alias map** verification (rename safety).
4. **PII** annotations surfaced to Governance.
5. **Impact analysis**: compute downstream consumers.
6. **Receipt** + **notifications** (Catalog, Delivery).

## Pseudo-code (validator)
```python
def validate_proposal(subject, schema, mode="additive"):
    canon = canonicalize(schema)
    current = registry.latest(subject)
    diff = compare(current.schema, canon)
    if not rules_compliant(diff, mode):
        raise PolicyError("breaking_change_blocked", details=diff.summary())
    ensure_alias_safety(diff)
    pii_check(canon)
    return {"ok": True, "diff": diff}
```

## Evidence Receipt (example)
```json
{
  "evidence_id": "ev_01J6X0...",
  "subject": "gdp:order",
  "version": 24,
  "action": "create_version",
  "diff": { "added": ["amount"], "aliased": [{"from":"id","to":"order_id"}] },
  "actor": "svc.schema-registry",
  "adr": "adr://schema/0007-field-aliasing",
  "created_at": "2025-10-05T08:55:00Z"
}
```

## Impact Notification (event)
```json
{
  "event":"schema.create_version",
  "subject":"gdp:order",
  "version":24,
  "consumers":[ "delivery:endpoint:kpi-orders", "dashboard:cfo" ],
  "produced_at":"2025-10-05T08:55:02Z"
}
```
