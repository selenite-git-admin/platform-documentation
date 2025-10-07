# Schema Registry — CLI Reference
> Context: Developer Tools • Owner: Platform Engineering • Last updated: 2025-10-07

## Purpose
The **Schema Registry CLI (schemactl)** provides command‑line access to registry functions — validation, publishing, diffing, and drift monitoring — enabling automation in CI/CD and developer workflows.

---

## Installation
Install via pip (internal package registry):
```bash
pip install schemactl
```
Configuration:
```bash
schemactl configure --profile default --endpoint https://api.datajetty.com/v1/schema/
```

---

## Authentication
| Mode | Description |
|---|---|
| **IAM Role** | Default in CI/CD or AWS EC2/ECS. |
| **AWS Profile** | Uses `~/.aws/credentials`. |
| **JWT Token** | Via `--token` flag for Cognito users. |

Example:
```bash
schemactl list --token eyJhbGciOiJIUzI1NiIsInR5cCI...
```

---

## Commands

### List Schemas
```bash
schemactl list --domain finance --status published
```
Lists schemas filtered by domain and status.

---

### Fetch Schema
```bash
schemactl get finance.gdp.invoice:v1.2
```

---

### Validate Schema
```bash
schemactl validate finance.gdp.invoice:v1.2
```
Runs Envelope & Payload validation locally or via API.

---

### Publish Schema
```bash
schemactl publish finance.gdp.invoice:v1.2
```
Triggers Governance validation and publish workflow.

---

### Diff Versions
```bash
schemactl diff finance.gdp.invoice:v1.1 finance.gdp.invoice:v1.2
```
Displays side-by-side schema changes.

---

### Check Drift
```bash
schemactl drift finance.gdp.invoice:v1.2
```
Fetches drift events and quarantine summary.

---

### Metrics
```bash
schemactl metrics finance.gdp.invoice:v1.2
```
Displays success rate, latency, and drift counts.

---

## Environment Variables
| Variable | Description |
|---|---|
| `SCHEMACTL_PROFILE` | AWS profile name |
| `SCHEMACTL_ENDPOINT` | Registry API endpoint |
| `SCHEMACTL_LOG_LEVEL` | `INFO` or `DEBUG` |

---

## Example CI/CD Integration
**GitHub Actions Example**
```yaml
- name: Validate Schema
  run: schemactl validate finance.gdp.invoice:v1.2

- name: Publish Schema
  if: success()
  run: schemactl publish finance.gdp.invoice:v1.2
```

---

## Logging & Troubleshooting
Logs stored at `~/.schemactl/logs/`.  
Use verbose mode for debugging:
```bash
schemactl validate finance.gdp.invoice:v1.2 --verbose
```

| Error | Description | Action |
|---|---|---|
| `SCHEMA-401` | Unauthorized | Reauthenticate or refresh token |
| `SCHEMA-404` | Not found | Verify FQID |
| `SCHEMA-409` | Conflict | Use diff command |
| `SCHEMA-500` | Internal error | Retry or contact support |

---

## References
- CLI Spec: `/tools/schemactl/README.md`  
- API Mapping: `/api/v1/schema_registry_openapi.yaml`  
- Governance Workflow: `/events/schema_registry_events.json`

---
