# Security Writing Guide

## Scope
Define security expectations, access control, classification, and audit for a module.

## Structure
1. Scope
2. Ownership boundaries
3. Data classification and retention
4. Data protection
5. Access control
6. Auditability
7. Incident response hooks
8. References

## Ownership boundaries
List what the module stores or processes and what it does not.

## Data classification and retention
Define data classes present in the module and retention periods. Avoid PII unless necessary and documented.

## Data protection
State transport and at-rest encryption rules. Link to KMS usage and key rotation policies if applicable.

## Access control
List roles and allowed actions. Note required scopes. Capture principles like least privilege and rate limiting.

## Auditability
List write events and fields recorded. Include correlation id usage.

## Incident response hooks
Describe how to correlate incidents and where to find logs and traces. Link to runbook.
