# Schema Lifecycle

## States

1. Proposed – draft submitted with metadata and JSON definition  
2. Approved – policy checks pass, impact report generated  
3. Published – schema becomes current and enforceable  
4. Deprecated – cutoff announced, migration guidance provided  
5. Retired – closed to writes, retained for audit only  

## Policies

- Deprecation windows: Extraction/Raw (90 days), GDP/KPI (120 days), Activation (180 days)  
- Retention: retired schemas must be stored for at least 7 years  
- Rollback: permitted within deprecation window only  

## Evidence

Every lifecycle transition is logged in the Trust ledger with approver, timestamp, and justification.

## Example Event Sequence

- `schema.proposed`  
- `schema.approved`  
- `schema.published`  
- `schema.deprecated`  
- `schema.retired`  
- `schema.rolledback`
