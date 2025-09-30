# Schema Services — GDP Framework

## Purpose
The GDP Framework (Golden Data Points) defines the canonical layer of the BareCount Data Platform.  
It provides standardized, business-relevant entities that abstract raw source data into consistent forms, enabling reliable KPI computation and cross-system comparability.

## Scope
- Canonicalize raw attributes (currency, units, dates, org structures).  
- Provide reusable entities for KPI contracts and analytics.  
- Serve as the bridge between Raw contracts and KPI contracts.  
- Ensure lineage, auditability, and compliance across schema versions.

## Design Principles
- **Canonicalization**: unify formats (currencies, units, periods, org hierarchies).  
- **Abstraction**: expose only the attributes needed for KPI computation.  
- **Auditability**: version every GDP contract, retain immutable history.  
- **Tenant-neutral**: design applicable across industries and ERPs.  
- **Declarative**: GDP definitions are declared once, reused across tenants.

## Database Representation
GDP entities are represented as relational tables in **Aurora PostgreSQL**.  
Each row is scoped by:
- `tenant_id`  
- `contract_id`  
- `version`  

**Table design patterns:**
- **Primary keys**: composite `(tenant_id, contract_id, version, entity_id)`.  
- **Foreign keys**: enforce hierarchy integrity (e.g., cost center → department).  
- **Metadata columns**: `valid_from`, `valid_to`, `lineage_ref`, `audit_ref`.  

**Example GDP Entities (DDL snippets):**

```sql
-- Calendar (simplified)
CREATE TABLE gdp_calendar (
    tenant_id    UUID NOT NULL,
    contract_id  UUID NOT NULL,
    version      INT  NOT NULL,
    date_key     DATE NOT NULL,
    fiscal_year  INT  NOT NULL,
    fiscal_period INT NOT NULL,
    week_number  INT,
    holiday_flag BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (tenant_id, contract_id, version, date_key)
);

-- Currency
CREATE TABLE gdp_currency (
    tenant_id    UUID NOT NULL,
    contract_id  UUID NOT NULL,
    version      INT  NOT NULL,
    currency_code CHAR(3) NOT NULL,
    fx_rate      DECIMAL(18,6) NOT NULL,
    valid_from   DATE NOT NULL,
    valid_to     DATE NOT NULL,
    PRIMARY KEY (tenant_id, contract_id, version, currency_code, valid_from)
);

-- Organization
CREATE TABLE gdp_org (
    tenant_id    UUID NOT NULL,
    contract_id  UUID NOT NULL,
    version      INT  NOT NULL,
    org_unit_id  VARCHAR(64) NOT NULL,
    parent_id    VARCHAR(64),
    org_type     VARCHAR(32) NOT NULL,
    name         TEXT NOT NULL,
    PRIMARY KEY (tenant_id, contract_id, version, org_unit_id),
    FOREIGN KEY (tenant_id, contract_id, version, parent_id)
        REFERENCES gdp_org (tenant_id, contract_id, version, org_unit_id)
);
```

## Version Binding
- Each GDP schema is tied to a **contract version**.  
- Versions follow **Major–Minor–Update** rules.  
- Superseded contracts remain queryable until their grace TTL expires.  
- Lineage references link GDP records back to Raw source attributes.  

## System Design Notes
- **Calendars**: fiscal years, periods, and holidays declared once at org level.  
- **Currency**: FX tables seeded centrally, applied consistently across GDP.  
- **Org hierarchy**: top-down representation ensures ratios and allocations are consistent.  
- **Headcount**: counts stored, not personal identifiers — designed for ratios and compliance.  
- **Flexibility**: GDP contracts can be extended by industry, but must preserve canonical core.

## End State
The GDP Framework ensures that KPIs are built on a **consistent, auditable foundation**.  
Every tenant operates with the same canonical definitions, while still allowing mapping flexibility to accommodate different industries and source systems.
