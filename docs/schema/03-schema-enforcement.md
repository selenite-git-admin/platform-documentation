# Schema Enforcement

## Purpose
Ensure that data and contracts conform to expectations.
Prevent bad data from moving forward.
Produce evidence that supports audits.

## Enforcement Gates
Run checks at these gates:
- extraction
- raw
- gdp
- kpi
- outbound

## Validation Types
- Meta conformance for headers and payloads
- Naming and allowed values
- DDL compatibility
- Data quality rules from the rule catalog
- Mapping coverage for GDP and KPI
- Referential integrity checks
- Row level security checks when required

## Rule Catalog
Rules have an id, a description, a severity, and a check specification.
The Data Quality engine executes rules and returns counts and a verdict.
See pipeline: `../pipeline/07-data-quality-and-validation.md`

## Build Time
Validate contracts on commit.
Generate DDL drafts and mapping plans.
Block promotion on red severity.

## Deploy Time
Validate target stores and permissions.
Apply migrations with safety checks.
Record a deployment evidence event.

## Run Time
Validate inputs and outputs for each stage.
Run the rule catalog for that stage.
Record a validation report with counts and verdict.
Store evidence and link lineage.

## Evidence Records
Each gate creates an evidence record with run identifiers.
The record includes rule outcomes, counts, and links to logs and reports.
