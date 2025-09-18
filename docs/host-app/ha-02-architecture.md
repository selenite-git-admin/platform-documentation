# Host App — Core Architecture

## Purpose
Outlines the architectural components of the Host App and how it interacts with other platform services.  
This provides a shared view of system design, dependencies, and boundaries.

---

## Core Components
- **UI Layer** — browser-based governance console for contract lifecycle, tenant management, RBAC, and reference data.  
- **API Gateway** — exposes control-plane APIs to the UI and external clients.  
- **Metadata Store** — relational database for **governance metadata** (approvals, audit, tenants, refdata, RBAC) and **linkages to platform contract versions**.  
- **Audit Trail** — append-only evidence log of every governance action.  
- **Read-only Observability** — dashboards showing metrics without control capabilities.

---

## Data Flow
1. User interacts with Host App UI.  
2. UI sends control requests via API Gateway.  
3. Host App writes governance metadata and invokes Schema/PHS APIs.  
4. Schema Services and PHS persist and enforce contracts.  
5. Audit Trail records approvals and actions.  
6. Observability metrics surfaced for governance review.

---

## Design Tenets
- **Separation of Concerns** — governance vs. operations.  
- **Immutability** — governance evidence never altered.  
- **Integration** — contract enforcement handled by Schema/PHS, not Host App.  
- **Traceability** — governance actions linked to platform contract versions.

---

## Why This Matters
The architecture ensures Host App provides governance and oversight without assuming operational responsibilities.  
Contracts remain authoritative in Schema/PHS, while Host App centralizes visibility and control for governance users.
