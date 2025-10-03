# Connectors Writing Guide

> Reference standard for documenting connector modules across all providers, versions, and connection methods.

---

## Purpose

This guide standardizes how **Connector modules** are documented. It ensures consistency across vendors, versions, and connection methods, and makes seams with **Compute.Ingestion** explicit and auditable. It also captures legal/licensing constraints that affect connector implementation.

---

## 1. Terminology

| Term             | Definition                                                                                   |
|------------------|----------------------------------------------------------------------------------------------|
| **Data Origin**  | Highest-level classification: <br> - **Enterprise**: tenant-owned systems (ERP, CRM, HRMS, ITMS, MES, DBs, files). <br> - **Public**: open/subscription feeds (Weather.com, SEC EDGAR, IMF). <br> - **Partner**: semi-external sources (industry exchanges, distributor portals). |
| **Data Source**  | Domain/category of system. Examples: ERP, CRM, HRMS, ITMS, MES, Analytics, File Store, Public Feed. |
| **Provider**     | Vendor/platform supplying the data source. Examples: SAP, Salesforce, ServiceNow, NOAA, SEC EDGAR. |
| **Version**      | Product release within the provider. Examples: SAP ECC, SAP S/4HANA, Salesforce Classic vs Lightning, EDGAR API v2. |
| **Connection Method** | Technical interface/adapter. Examples: SAP RFC, SAP OData, Salesforce Bulk API, NOAA JSON API, EDGAR FTP dump. |

---

## 2. Connector Documentation Structure

```
/docs/modules/connectors/{provider}/
  index.md
  api.md
  data-model.md
  security.md
  observability.md
  runbook.md
  ui.md
  methods/
    {method}/
      index.md
      api.md
      data-model.md
      security.md
      observability.md
      runbook.md
      ui.md
```

- **Provider-level docs** describe the overall role, supported versions, connection methods, common state/security/observability, and legal constraints.  
- **Method-level docs** cover specific connection techniques (API, SDK, file dump, webhook, manual export).  
- **Common docs** define the **manifest contract**, seam with Compute.Ingestion, deployment profiles, and error taxonomy.

---

## 3. Mandatory Sections

### Provider-level (`index.md`)
- **Overview Table**: Data Origin, Source, Provider, Versions, Connection Methods.
- **Role in Platform**: why this provider matters.
- **Responsibilities**: handshake, auth, extraction, manifest.
- **Boundaries**: what it never does (no normalization/KPI/publish).
- **Capability Matrix**: versions × methods (coverage, CDC, throughput, infra reqs, licensing).
- **Legal & Licensing Constraints**:
  - SDK redistribution allowed? Y/N.
  - Required customer action (e.g., “Customer must upload SAP RFC SDK from their licensed account”).
  - API usage limits or fair-use clauses.
  - Export-control / jurisdiction notes.

### Method-level (`methods/{method}/index.md`)
- **Scope**: what the method is and when to use it.
- **Supported Entities**: modules/tables/feeds it can pull.
- **Extraction Model**: full vs CDC, pagination, ordering, time semantics.
- **Output**: file formats, partitioning, manifest integration.
- **Limits & Quirks**: vendor constraints, SDK bugs, API throttles.
- **Dependencies**: SDK, CLI, drivers, webhooks, partner services.
- **Deployment Guidance**: cloud pull, on-prem agent, air-gapped courier.

### `api.md`
- Surfaces: handshake, sync start, status, webhook callbacks.
- Request/response examples, idempotency, error mapping.
- Note if the provider ships an SDK/CLI instead of open HTTP APIs.

### `data-model.md`
- Persistent state: registry, credentials, cursor state, schema digests, rate policies.
- Method-specific state: webhook subscription tokens, SDK config files, dumps.

### `security.md`
- Secrets handling (via Trust).
- SDK license handling: ensure tenant supplies binaries if redistribution not allowed.
- Auth models, scopes, IP allowlists, encryption.
- Audit trails.

### `observability.md`
- Metrics: rows, bytes, lag, errors, throttles.
- Events: handshake success/failure, sync start/complete, schema drift.
- Logs: structured with run_id, connector_id, tenant, entity.

### `runbook.md`
- Standard ops: rotate creds, handle API rate limits, resume replays, recover from vendor outages.
- SDK/CLI-specific ops: installation, upgrade, patching.
- Manual fallback (file upload if automated pull fails).

### `ui.md`
- Admin screens: onboarding form, credential entry, profile selection.
- Preflight: connectivity, scope validation, sample record probe.
- SDK upload UI (if redistribution not allowed).

---

## 4. Seam With Compute.Ingestion

- Connectors **must emit** `manifest.json` + payloads into the landing path.  
- **Manifest Contract**: schema version, run_id, cursor, checksums, idempotency key.  
- Compute validates manifest, checksums, idempotency → ingests.  
- Connectors stop at the raw seam. Compute owns normalization/KPI.  

---

## 5. Cross-Vendor Consistency

All connectors must document:
- **Deployment Profiles**: Cloud Pull, On-Prem Agent, Air-Gapped Courier.
- **Error Taxonomy Mapping**: vendor error → platform error class.
- **Schema Drift Policy**: allow+tag / auto-extend / block.
- **Idempotency Key Recipe**.
- **Landing Path Convention**.

---

## 6. Writing Style

- Neutral, technical tone (STE compliant).
- Use **Role → Responsibilities → Boundaries** framing in index docs.
- Use **Scope → Conventions** in APIs and Data Model docs.
- Capture **legal/licensing constraints** explicitly.  
- Highlight **cross-cutting concerns**: multi-tenant, calendars, lineage, SDK obligations.

---

## 7. Examples of Legal/SDK Handling

- **SAP RFC SDK**: redistribution not allowed → customer must upload SDK to platform → connector consumes it.  
- **Oracle drivers**: may require explicit customer license → document the process in `security.md` and `runbook.md`.  
- **Public APIs (EDGAR, Weather)**: usually open, but include rate limits and TOS obligations.  
- **Webhooks**: document subscription flow, renewal policies, and signature validation.

---

> Every connector doc must capture **technical interface + legal/licensing boundaries** so that ops and compliance teams can run it safely.

---

_Last updated: 2025-10-03 09:21_
