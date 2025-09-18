# Platform Runtime Foundations — Secrets & Key Management

## Purpose
The Secrets & Key Management service provides a **centralized and consistent mechanism** to secure credentials, API tokens, and encryption keys across the platform.  
It ensures that both Control and Data plane services operate with scoped, rotated, and auditable secrets, protecting tenants from data breaches and compliance violations.

---

## Responsibilities
- **Key lifecycle management** — create, rotate, revoke, and retire encryption keys via integrated KMS (Key Management Service).  
- **Secrets storage** — securely store API keys, database credentials, and tokens with strict access controls.  
- **Scoped tokens** — issue least-privilege, time-bound tokens for Control and Data plane services.  
- **Encryption enforcement** — apply encryption in transit (TLS) and at rest using KMS-backed keys.  
- **Audit & attestation** — log key usage, rotation events, and access attempts for compliance.  

---

## Non-Goals
- Not a general-purpose password vault for tenant applications.  
- Does not manage tenant-facing RBAC (covered in Security & RBAC).  
- Not responsible for data classification or residency (covered in Residency & Compliance).  

---

## Flows
1. **Provision** — Host App or onboarding workflows request scoped credentials for new tenants or services.  
2. **Issue** — Secrets & KMS issues time-bound tokens or encryption keys.  
3. **Use** — Data Plane services consume tokens to access databases, queues, or storage.  
4. **Rotate** — secrets are automatically rotated on defined schedules, with zero-downtime rollover.  
5. **Audit** — all requests, issuances, and revocations logged for compliance evidence.  

---

## Interfaces
- **Orchestration & Scheduling** — consumes scoped tokens to run jobs securely.  
- **Tenant App** — uses tenant-specific credentials for data isolation.  
- **Host App** — manages governance-level access policies and rotations.  
- **Audit & Evidence** — ingests logs for proof of secret management compliance.  

---

## Why This Matters
Weak, hardcoded, or unrotated credentials are a leading cause of breaches.  
By enforcing centralized secrets and KMS integration:
- **Engineers** avoid handling raw credentials directly.  
- **Executives** demonstrate regulatory compliance with strong cryptographic controls.  
- **Auditors** can verify that all access is protected, rotated, and logged.  

The Secrets & Key Management service ensures the platform is **secure, controlled, and compliant by default**.
