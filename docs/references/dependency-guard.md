# Dependency Guard

## Objective
Prevent cyclic dependencies across module families and between individual modules.

## Layering
The platform follows a topologically ordered set of families. Dependencies must only point forward in this order.

1. Access Modules
2. Security Modules
3. Host Modules
4. Data Utilities Modules
5. Data Storage Modules
6. Runtime Modules
7. Compute Modules
8. Consumption Modules
9. Action Modules
10. Trust Modules

## Rules
- A family can depend only on families that come before it in the order.
- A module can depend only on modules within its family or earlier families.
- Cycles at any level are forbidden.
- Exceptions are not allowed in code. If you need an exception, change the order and update docs.

## Enforcement
- Maintain a `deps.yaml` with family order and allowed family edges.
- Optionally maintain a `modules.deps.yaml` for fine grained module edges.
- Run `validate_deps.py` in CI to fail any pull request that introduces a cycle or a forbidden edge.

## Files
- `tools/dependency_guard/deps.yaml` controls family order and allowed family edges.
- `tools/dependency_guard/modules.deps.yaml` lists module level edges. Optional. Start empty.
- `tools/dependency_guard/validate_deps.py` performs the checks.

## Workflow
1. Edit `deps.yaml` only through documentation changes.
2. When adding a module, update `modules.deps.yaml` with its edges.
3. Run `python tools/dependency_guard/validate_deps.py`.
4. Fix violations before merging.
