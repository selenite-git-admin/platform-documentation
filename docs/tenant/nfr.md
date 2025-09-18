# Tenant App – NFRs

## Availability
- UI availability target: 99.9% monthly.
- BFF availability target: 99.9% monthly.

## Recovery
- Recovery Time Objective (RTO): 30 minutes for stateless components.
- Recovery Point Objective (RPO): 15 minutes for transient caches and sessions.

## Performance
- P95 UI page load: < 1.5 seconds.
- P95 read API: < 500 ms.
- P95 write API: < 1.5 seconds.

## Scalability
- Must support 10x tenant growth without re‑architecture.
- Stateless tiers scale linearly with load.

## Security
- All changes auditable with correlation IDs.
- Secrets rotated at least every 90 days.
- No hard‑coded secrets in code or config.

## Compliance
- Evidence exports available for audit.
- Configurable data residency by tenant.
