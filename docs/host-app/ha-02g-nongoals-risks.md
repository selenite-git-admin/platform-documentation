# Host App — Non-goals & Risks

## Purpose
Clarifies what the Host App does not provide and the risks it must mitigate.  
This prevents scope creep and helps users understand operational limits.

## Non-goals
The Host App does not:  
- Manage infrastructure or scaling.  
- Execute or retry pipelines.  
- Edit tenant raw data.  
- Perform deep operational monitoring.  

These remain under PHS or tenant systems.

## Risks
- Scope creep — governance users expecting operational features.  
- RBAC misconfiguration — over-permissive roles.  
- Audit gaps — incomplete evidence chains.  
- Residency conflicts — inconsistent enforcement across environments.  

## Mitigations
- Clear separation of duties.  
- Role reviews and least-privilege defaults.  
- Immutable logging and evidence exports.  
- Residency validated at contract level.  

## Why This Matters
Governance tools that grow unchecked create confusion and compliance risk.  
By stating non-goals and risks upfront, the Host App sets transparent expectations for both auditors and operators.
