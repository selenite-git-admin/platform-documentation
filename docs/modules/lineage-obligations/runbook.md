# Runbook

## Scope
Operational procedures for Lineage Obligations.

## Quick reference
| Symptom | First checks | Safe mitigations | Validation |
| --- | --- | --- | --- |
| Missing edges in graph | event gaps or normalize errors | re-run batch ingest for the time window | edge count increases |
| False fail on obligation | scope or params mismatch | adjust obligation or tags, re-evaluate | status becomes pass |
| Slow graph queries | large depth or hot path | cap depth, add indexes, materialize summaries | latency improves |
| Ingest backlog | producers slowed or erroring | scale intake workers, pause low priority producers | backlog drains |

## Procedures

### 1. Re-ingest a window
1. Identify event source and time window
2. Request batch export from source
3. Post to batch ingest
4. Validate edge counts

### 2. Investigate a failed obligation
1. Read obligation and evaluation details
2. Inspect target assets and upstream lineage
3. Confirm tags and contract references
4. Re-evaluate after fixes

### 3. Tune graph traversal
1. Profile query execution
2. Add or adjust indexes
3. Consider caching fan out summaries

## Routine tasks
- Review new obligations and their pass rates
- Monitor ingest volumes
- Audit changes to obligations

## References
- [API](api.md)
- [Data Model](data-model.md)
- [Observability](observability.md)
- [Security](security.md)
