# KPI Services — Roles and Permissions

## Purpose
This document defines the roles and access controls for KPI Services.  
It specifies who can create, update, approve, or consume KPI definitions and results.  
Permissions are enforced consistently through APIs and the control plane.

---

## Roles

### Author
- Create new KPI definitions.  
- Draft formulas referencing GDP entities.  
- Propose thresholds and validation rules.  
- Cannot approve or publish a KPI into production.

### Approver
- Review and approve KPI definitions authored by others.  
- Validate alignment with business requirements and compliance rules.  
- Authorize deployment of new KPI versions.  
- Cannot bypass version control.

### Consumer
- Access KPI results through APIs, reports, or downstream applications.  
- Cannot modify KPI definitions or thresholds.  
- Limited to read-only operations within their scope.

### Administrator
- Manage role assignments and access control policies.  
- Configure system-level settings (e.g., computation schedules, retention policies).  
- Override in exceptional cases, with full audit logging.

---

## Permissions Matrix

| Capability             | Author | Approver | Consumer | Administrator |
|------------------------|:------:|:--------:|:--------:|:-------------:|
| Create KPI definition  |   ✔    |          |          |       ✔       |
| Update KPI definition  |   ✔    |          |          |       ✔       |
| Approve KPI definition |        |    ✔     |          |       ✔       |
| Deprecate KPI version  |        |    ✔     |          |       ✔       |
| Execute computation    |        |          |    ✔     |       ✔       |
| Access KPI results     |        |    ✔     |    ✔     |       ✔       |
| Manage access controls |        |          |          |       ✔       |
| Configure schedules    |        |          |          |       ✔       |

---

## Notes
- Every KPI must have at least one Author and one Approver; these roles cannot be fulfilled by the same user.  
- All access events (create, update, approve, execute) are logged for audit.  
- Role mappings integrate with the organization’s identity provider.  

---

KPI Services enforce **role-based access control (RBAC)** to maintain separation of duties and ensure compliance across KPI lifecycle operations.
