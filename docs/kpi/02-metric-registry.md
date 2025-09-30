# Metric Registry

## Purpose
Store versioned metric definitions that all tools use.
Resolve definitions by date, tenant, and release channel.

## Record shape
- metric_id
- version (SemVer)
- name and description
- grain and dimensionality
- formula and inputs
- units and currency policy
- owners and approvers
- active_from and active_to
- release_channel: dev | test | prod
- tags and search keywords

## Operations
- create, propose, approve, release, deprecate
- link to metrics schema contracts and pipeline runs
- emit evidence for approvals and releases

## Registry APIs
- list metrics with filters
- get a metric by id and date
- diff two versions
- resolve inputs and lineage for a metric
