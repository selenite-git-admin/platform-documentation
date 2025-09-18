# KPI Services — Overview

## What is KPI Services
KPI Services provide a consistent way to define, compute, and validate **Key Performance Indicators (KPIs)** across an organization.  
The service abstracts standardized business data (Golden Data Points, or GDP) into metrics that can be reused across teams and applications.  
It ensures that KPI definitions remain traceable, governed, and technically repeatable.

## Why use KPI Services
Organizations often face fragmented KPI definitions across functions, systems, and reports.  
This leads to inconsistencies, duplicated effort, and lack of confidence in results.  
KPI Services address these problems by:
- Offering a central contract for KPI definitions  
- Enforcing validation and threshold rules  
- Providing governance through requirements, roles, and traceability  
- Standardizing lifecycle operations such as creation, update, and monitoring  

## Dependency on GDP
KPI Services operate **exclusively on GDP contracts**.  
They do not read directly from Raw contracts.  
GDP provides canonical entities such as Calendar, Currency, and Org Hierarchy, ensuring all KPI calculations are consistent, auditable, and system-agnostic.  
See [Schema Services — GDP Framework](../schema/gdp-framework.md) for details.

## Scope of the Service
KPI Services include:
- Definition of KPIs and their metadata  
- Standard frameworks for KPI computation (using GDP inputs)  
- Validation and threshold enforcement  
- Role-based access and governance  
- Canonical data model for storing and exchanging KPI results  

## Out of Scope
KPI Services do not provide:
- Source-system dashboards or visualization tools  
- Business process automation outside of KPI lifecycle  
- Non-metric data reporting (e.g., operational logs, transactions)  

## Relationship to Other Services
KPI Services are designed to work with other platform components:
- **Schema Services:** GDP contracts are mandatory inputs for KPI computation  
- **Platform Services (PHS):** supply infrastructure, storage, and observability  
- **APIs:** provide access patterns for integration with external applications  
- **Governance:** supported by decisions, glossary, and compliance artifacts  

## Next Steps
The following sections describe each aspect of KPI Services in detail:

- [KPI Framework](kpi-02-framework.md)  
  Contract boundaries, runtime model, and integration with GDP.

- [Requirements](kpi-03-requirements.md)  
  Functional and non-functional requirements, assumptions, and constraints.

- [Roles & Permissions](kpi-04-roles-permissions.md)  
  Defines who can author, approve, or consume KPIs.

- [Traceability](kpi-05-traceability.md)  
  Maps requirements → design → validation → evidence.

- [Validation & Thresholds](kpi-06-validation.md)  
  Pre- and post-validation logic, threshold enforcement, and evidence logging.

- [Data Model](kpi-07-data-model.md)  
  Canonical entities, schema, lineage, and governance rules.

