# Runbook

## 1) Breaking change attempted
- **Symptom:** 400 `breaking_change_blocked`
- **Action:** Send diff; suggest additive path or branch subject (`*.v2`). Create migration plan.

## 2) Downstream failures after rename
- **Symptom:** Delivery errors; dashboards fail.
- **Checks:** alias map present? Delivery cache invalidated?
- **Fix:** publish alias; extend alias window; notify consumers; replay materializations if needed.

## 3) Webhook DLQ > 0
- **Action:** Pause events to failing tenant endpoints; replay after fix with `events/replay`.

## 4) Backfill window exceeded
- **Action:** Use Migration Service to plan staged backfill with quotas and checkpoints.
