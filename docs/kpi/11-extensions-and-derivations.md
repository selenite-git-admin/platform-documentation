# Extensions and Derivations

## Purpose
Standardize common derived metrics.
Provide clear patterns for time based comparisons.

## Patterns
- Week over Week
- Month over Month
- Quarter over Quarter
- Year over Year
- Rolling windows

## Validation
Declare tests for derived metrics.
Declare windows and alignment to calendars.

## Legacy content
The following section is imported from legacy extensions.

# Kpi Extension
[![Version: 1.0](https://img.shields.io/badge/Version-1.0-374151?style=flat-square&labelColor=111827&color=374151)](#)
[![Status: Draft](https://img.shields.io/badge/Status-Draft-f59e0b?style=flat-square&labelColor=111827&color=f59e0b)](#)
[![Last Updated: 2025-08-23](https://img.shields.io/badge/Last%20Updated-2025--08--23-neutral?style=flat-square&labelColor=111827&color=neutral)](#)

**Author:** Anant Kulkarni  
**Owner:** KPI Platform Team  
**Contributors:** -  

## Document Information
- Purpose: Describe this component of the KPI System.  
- Scope: Covers key concepts, structures, and interactions. Excludes implementation-specific code and deployment runbooks.  
- Target Readers: Solution architects, developers, and reviewers.  
- Dependencies: <List related docs>  
- References: <List references>  

# KPI Extensions Framework

## Introduction
Cxofacts defines every KPI not only by its purpose and outcome, but also by the ways it can be extended for deeper analysis.  
These extensions describe how a KPI can be sliced, compared, or contextualized across time, entities, benchmarks, scenarios, or analytical dimensions.  

By standardizing extensions, Cxofacts ensures that KPIs are consistent, reusable, and business-aware - avoiding random, ad-hoc cuts in reporting.

## Extension Categories

### Time Extensions (When)
How a KPI evolves across time horizons.  
- Month over Month (MoM)  
- Quarter over Quarter (QoQ)  
- Year over Year (YoY)  
- Trendline / Rolling Average  
- Seasonality / Cyclicality  

### Entity / Structural Extensions (Where / Who)
How a KPI applies across organizational structures.  
- Unit / Subsidiary / Entity  
- Business Function / Department  
- Geography / Location (single vs multi-location, regional)  
- Entity Type (Proprietorship, LLP, Pvt Ltd, Public Ltd)  

### Benchmark Extensions (Against What)
How a KPI compares against expectations or peers.  
- Budget vs Actual  
- Forecast vs Actual  
- Industry / Peer Benchmark  
- Internal Benchmark (best-performing unit, top vs bottom quartile)  

### Scenario Extensions (What If)
Forward-looking variations and modeling.  
- Best Case / Worst Case  
- Scenario Modeling (e.g., cost increase, revenue drop, funding delay)  
- Sensitivity Analysis (impact of variable changes on KPI outcome)  

### Analytical Extensions (How Deep)
Derived insights and advanced cuts.  
- Ratio / Per Unit Analysis (e.g., per employee, per product, per store)  
- Segment Analysis (customer cohorts, product categories, channels)  
- Currency / Consolidation Views (multi-currency, consolidated vs standalone)  
- Anomaly Highlight (rule-based or AI-driven outliers)  

## Handling Evolving Structures (SCD Relevance)

### Why It Matters
KPI extensions often depend on dimensions that change over time - such as business units, cost centers, customers, or geographies.  
If these changes are not modeled correctly, KPI comparisons (MoM, YoY, unit-wise) can produce misleading results.

Example:  
- A business unit is split into two mid-year.  
- Without historical tracking, prior months' results may incorrectly roll into the new units.  
- With proper versioning, CFOs can view reports either *as originally reported* or *restated under the new structure*.

### Slowly Changing Dimensions (SCD)
To address this, Cxofacts data contracts apply Slowly Changing Dimension (SCD) techniques:
- Type 1 – Overwrite old values when only current view matters (e.g., Customer contact info).  
- Type 2 – Maintain full history with effective start/end dates for audit and trend reporting (e.g., Business Unit hierarchy, Entity Type).  
- Type 3 – Store limited prior values (e.g., previous vs current classification).

### Application in KPI Extensions
- Time Extensions (MoM, YoY, Trendlines) → rely on Type 2 to ensure past numbers reflect original structures.  
- Entity/Structural Extensions (Unit-wise, Geography-wise) → need SCD handling for reorganizations, mergers, or new locations.  
- Benchmark Extensions → may require restating past periods in line with current structures (optional).  
- Scenario Extensions → can project KPI performance under both current and hypothetical structures.  
- Analytical Extensions → ensure per-unit or segment analysis respects dimension history.

### Development Guidance
- Always define whether a KPI uses current structure or historical structure.  
- Store effective start and end dates for key dimensions (entity, cost center, geography, customer).  
- KPI contracts must reference the correct version of the dimension at reporting time.  
- For multi-location or group entities, enable toggling between “as reported” vs “restated” views.

## Usage in Cxofacts
- Each KPI may support multiple extensions, chosen based on relevance.  
- Extensions are cataloged alongside the KPI in the CFO Pack documentation.  
- During implementation, CFO Packs can be configured to activate extensions that match enterprise context (Business-Aware KPI principle).  

## Example
**KPI: Cash Balance**  
- Time Extensions: MoM, Trendline  
- Entity Extensions: Unit-wise, Currency cut  
- Benchmark Extensions: Budget vs Actual  
- Scenario Extensions: None  
- Analytical Extensions: Anomaly highlight  

This means Cash Balance is not just reported as a number, but also interpreted in terms of trend, unit-level breakdown, budget alignment, and anomalies.

## Benefits
- Provides a governed, reusable framework for KPI drill-downs.  
- Ensures consistency across CFO Packs (all Liquidity KPIs follow the same extension logic).  
- Enables Cxofacts UI/Reports to implement structured filters and drill paths.  
- Enhances the business-aware positioning by linking KPI usage to enterprise context.

## Diagrams

None

## Tables

None



## Glossary

None
