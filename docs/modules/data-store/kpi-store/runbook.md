# KPI Store – Runbook

## Quick Reference
| Symptom | Checks | Mitigation | Validation |
|---|---|---|---|
| Ingest backlog | Queue depth, worker health | Scale consumers; increase partitions | Backlog drains |
| Query timeouts | Hot partitions, skew | Repartition or add indexes | P99 ↓ |
| Storage pressure | Utilization %, growth rate | Expand tier; purge per policy | Utilization stable |

## Procedures
### Hot partition skew
1. Identify skewed keys
2. Repartition or add index
3. Warm caches

### SLA breach
1. Scale query nodes
2. Optimize pre-aggregations
3. Review dashboards

## Safety Notes
- Do not bypass retention policies; use approved purge jobs.
