
# Tenancy Module - Data Models
## File: sample-records.md

Audience: Developers, QA, and data validation teams  
Status: Draft v0.1  
Purpose: Provides representative sample data for tenancy database tables used in integration testing and migration validation.

---

## 1. tenants

| tenant_id | organization_id | profile | state | region | quotas | policies | billing | created_at |
|------------|----------------|----------|--------|---------|---------|----------|----------|-------------|
| t_5001 | org_acme | mt-standard | Active | ap-south-1 | {"storageGiB":200,"concurrentJobs":10} | {"dataResidency":"in-region-only"} | {"plan":"starter"} | 2025-10-08T14:32:00Z |
| t_5002 | org_beta | st-dedicated | Draft | us-east-1 | {"storageGiB":500,"concurrentJobs":20} | {"dataResidency":"cross-region-ok"} | {"plan":"enterprise"} | 2025-10-08T15:05:00Z |

---

## 2. environments

| env_id | tenant_id | name | region | isolation_level | quotas | retention_days |
|--------|------------|------|--------|-----------------|---------|----------------|
| env_01 | t_5001 | dev | ap-south-1 | shared | {"storageGiB":50} | 30 |
| env_02 | t_5001 | prod | ap-south-1 | strict | {"storageGiB":150} | 90 |
| env_03 | t_5002 | prod | us-east-1 | dedicated | {"storageGiB":500} | 365 |

---

## 3. tenant_audit

| audit_id | tenant_id | event_type | actor | correlation_id | occurred_at |
|-----------|------------|-------------|--------|----------------|--------------|
| a_1001 | t_5001 | TENANCY_CREATED | system | req_777 | 2025-10-08T14:32:00Z |
| a_1002 | t_5001 | TENANCY_ACTIVATED | controller | req_778 | 2025-10-08T14:40:00Z |
| a_1003 | t_5002 | TENANCY_CREATED | system | req_801 | 2025-10-08T15:05:00Z |

---

## 4. tenant_jobs

| job_id | tenant_id | action | state | progress | created_at |
|--------|------------|--------|--------|-----------|-------------|
| job_7001 | t_5001 | activate | completed | 1.0 | 2025-10-08T14:33:00Z |
| job_7002 | t_5002 | create | running | 0.6 | 2025-10-08T15:06:00Z |

---

## 5. tenant_webhooks

| webhook_id | tenant_id | url | events | retry_policy |
|-------------|------------|-----|--------|---------------|
| wh_01 | t_5001 | https://ops.example.com/hooks/tenancy | ["TENANCY_ACTIVATED"] | {"maxRetries":5,"backoffSeconds":30} |
| wh_02 | t_5002 | https://audit.example.com/hooks/tenancy | ["TENANCY_SUSPENDED"] | {"maxRetries":8,"backoffSeconds":60} |

---

Summary  
These records illustrate the shape and semantics of tenancy data across core entities. They are used for integration testing, schema verification, and synthetic data generation for analytics validation.
