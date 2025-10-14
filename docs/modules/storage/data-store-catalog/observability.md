# Data Store Catalog (Catalog) Observability

**Family:** Data Store  **Tier:** Core  **Owner:** Platform Foundation  **Status:** Review

## Purpose
Observability ensures that Catalog’s dataset registry remains consistent, responsive, and reliable. Metrics and logs provide visibility into API usage, latency, errors, and data synchronization. Alerts are defined to detect anomalies before consumers experience degraded discovery or read failures.

## Observability Objectives
- Detect missing or inconsistent dataset records within one hour.
- Maintain p99 read latency below 100 ms.
- Detect drift between Catalog and DRR or underlying Postgres stores.
- Track access usage patterns by tenant and API scope.
- Maintain audit coverage for every write operation.

## Metrics
| Metric | Description | Type | Target |
|--------|--------------|------|--------|
| `catalog.api.latency_p99` | P99 latency of API reads | Gauge | < 100 ms |
| `catalog.api.errors_5xx` | API internal error count | Counter | 0 sustained |
| `catalog.api.errors_4xx` | Client error count | Counter | Monitored |
| `catalog.api.rps` | Requests per second per region | Gauge | Scales linearly |
| `catalog.dataset.count` | Total registered datasets | Gauge | Audited daily |
| `catalog.dataset.orphan_count` | Datasets with missing location | Gauge | 0 |
| `catalog.migration.count` | Successful migrations | Counter | Monitored |
| `catalog.audit.write_count` | Number of audit writes | Counter | ≥ 1 per write |
| `catalog.replication.lag_sec` | Read replica lag | Gauge | < 10 s |
| `catalog.api.cache_hit_ratio` | Cache efficiency for GETs | Gauge | > 0.85 |
| `catalog.freshness.drift_sec` | Drift between Catalog and DRR states | Gauge | < 300 s |

Metrics are emitted to CloudWatch or Prometheus and exported to Grafana dashboards.

## Dashboards
### API Performance
- Latency, error rate, and cache hit ratio visualized per endpoint.
- Top datasets by request volume.
- Regional comparison of p95 and p99 latency.

### Data Consistency
- Catalog–DRR drift heatmap by dataset layer.
- Missing or outdated location entries.
- Schema version mismatches detected via checksum diffs.

### Audit and Security
- Number of write operations per actor and module.
- Unauthorized access attempts (403 events).
- Evidence Ledger correlation completeness.

## Logs
Structured JSON logs are emitted to a centralized collector.

| Field | Description |
|--------|-------------|
| `timestamp` | ISO timestamp |
| `level` | info, warning, error |
| `event` | event name (`api_request`, `migration_applied`, `schema_diff_detected`) |
| `dataset_id` | Affected dataset |
| `actor` | Service or user id |
| `correlation_id` | Request correlation |
| `latency_ms` | Duration for request |
| `error_code` | If applicable |
| `region` | Region identifier |

### Example Log Entry
```json
{
  "timestamp": "2025-10-12T07:42:13Z",
  "level": "info",
  "event": "api_request",
  "dataset_id": "kpi.cash_conversion_cycle_v2",
  "actor": "kpi-service",
  "latency_ms": 64,
  "status": 200,
  "region": "ap-south-1"
}
```

## Alerts
| Condition | Threshold | Action |
|------------|------------|--------|
| p99 latency > 150 ms for 5 minutes | Alert | Notify DevOps via PagerDuty |
| error_5xx > 1% for 5 minutes | Alert | Trigger health check restart |
| orphan_count > 0 | Alert | Open incident ticket |
| drift_sec > 300 | Warning | Sync validation job runs |
| replication lag > 30 s | Alert | Notify DB team |
| unauthorized access > 10 in 10 min | Alert | Lock offending token |

## Synthetic Probes
Every 15 minutes a probe validates that:
1. Public API responds to `GET /storage/v1/catalog/datasets?limit=1` within SLA.
2. Sample dataset descriptor is consistent with DB record.
3. Audit entry appears within one minute of simulated write.

Results are logged to `catalog_probe_results` table for tracking.

## Audit Reconciliation
Nightly job compares:
- API read output vs Postgres state.
- Catalog audit trail vs Evidence Ledger records.

Drift entries are summarized and emailed to platform maintainers.

## Tracing
All APIs emit OpenTelemetry traces.
- Each request tagged with `dataset_id`, `tenant_id`, and `scope`.
- Spans include downstream Postgres query duration.
- Aggregated in Tempo for distributed request visualization.

## Metrics Aggregation
Metrics collected from:
- API services (Flask/FastAPI level)
- PostgreSQL (pg_stat_statements, replication lag, connection count)
- Infrastructure (ECS task CPU, memory, autoscaling events)

All metrics are prefixed with `catalog.*` for easy filtering.

## SLO Evaluation
| SLO | Target | Current Measurement |
|------|---------|---------------------|
| Read API availability | 99.99% | Measured daily |
| p99 latency | < 100 ms | Per-region metric |
| Schema drift detection | < 1 hour | Reconciliation job |
| Audit coverage | 100% of writes | Evidence Ledger match |
| Alert MTTA | < 5 min | PagerDuty logs |

## Ownership
| Function | Responsibility |
|-----------|----------------|
| Platform Foundation | Define metrics, maintain Grafana dashboards |
| DevOps | Maintain alert routing and PagerDuty integration |
| SRE | Execute reconciliation jobs and review drift reports |

## Summary
Observability for Catalog ensures fast, reliable discovery and consistent metadata across PostgreSQL stores. Metrics and alerts focus on performance, drift, and audit completeness to maintain operational trust.