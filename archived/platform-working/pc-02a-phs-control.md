# Platform Orchestration — PHS Control APIs

## Purpose
The PHS Control APIs are the **orchestration layer** of the Control Plane.  
They translate approved contracts into executable plans and manage how those plans are rolled out to the Data Plane.  
This ensures that only validated, governed intent reaches execution.

## Responsibilities
- **Compilation** — convert approved schema versions into executable materialization plans.  
- **Rollout** — deploy plans into tenant environments with traceability and status reporting.  
- **Version management** — support dual-run, compare, and rollback of deployments.  
- **Feedback loop** — expose status and metrics back to the Host App for governance visibility.

## Non-Goals
- Do not store or define contracts — Schema Services is the source of truth.  
- Do not execute tenant data workloads — that is the role of the Data Plane.  
- Do not provide a governance UI — Host App handles human workflows.

## Why This Matters
Without orchestration, governance decisions stop at paper.  
PHS Control APIs make intent actionable, auditable, and reversible, bridging governance with execution in a safe and transparent way.
