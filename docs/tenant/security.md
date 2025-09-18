# Tenant App – Security

## Identity and Access Management
- **Authentication**
  - Primary: OIDC or SAML through the tenant’s IdP.
  - Supports Just‑in‑Time (JIT) user provisioning where enabled.
  - Local accounts are disabled by default; enable only for break‑glass.
  - Session length and MFA are enforced by the IdP.
- **Authorization**
  - Role‑based access control (RBAC) with fine‑grained permissions.
  - Attribute‑based controls (ABAC) for resource ownership where applicable.
  - Least‑privilege defaults; access is explicitly granted.
- **SCIM Provisioning**
  - Optional SCIM for automated user and group lifecycle.
  - Deprovisioning removes active sessions and tokens.
- **Sessions**
  - Browser sessions use HttpOnly, Secure cookies or short‑lived bearer tokens.
  - Silent refresh for short‑TTL tokens.
  - CSRF protection on state‑changing requests.

## Secrets and Keys
- **Storage**
  - No secrets in source code or config files.
  - Secrets stored in a managed vault with per‑tenant namespaces.
- **Rotation**
  - Automated rotation policies with dual control.
  - Rotation SLAs defined per secret class (credentials, keys, tokens).
- **Access**
  - Access to secrets is logged and scoped to service role identities.

## Data Protection
- **Data in Transit**
  - TLS 1.2+ for all endpoints.
  - mTLS used for private service‑to‑service calls where supported.
- **Data at Rest**
  - Encryption using cloud KMS keys; per‑tenant logical isolation at the platform layer.
- **Caching**
  - UI/BFF caches are tenant‑keyed; sensitive items are never cached in the browser.

## Application Security Controls
- **Input Validation**
  - Strict schema validation at the BFF boundary.
  - Allow‑list based parsing for file uploads and content types.
- **Output Encoding**
  - Standard HTML/JS escaping to prevent XSS.
- **Rate Limiting**
  - Request quotas per identity and per tenant at the edge and BFF.
- **Error Handling**
  - No sensitive data in error messages; correlation IDs included for support.
- **Dependencies**
  - SBOM generation; automated vulnerability scanning (SCA).
  - Pinning with approved update windows and emergency patch channel.

## Operational Security
- **Change Management**
  - Blue/green deployments with mandatory reviews and automated checks.
  - Feature flags for gradual rollout.
- **Monitoring and Alerting**
  - Structured logs, traces, and metrics with tenant and correlation IDs.
  - Security alerts for auth failures, anomalous access, and secrets access.
- **Incident Response**
  - Runbooks for auth outages, data exposure suspicion, and compromised credentials.
  - Evidence capture: logs, traces, configuration snapshots, timeline.
- **Access Reviews**
  - Periodic reviews for privileged roles (Admin, Steward, Operator).
  - Break‑glass account usage requires post‑use review and justification.

## Integrations and Third Parties
- **IdPs**
  - Tested against major IdPs supporting OIDC/SAML and SCIM.
  - IdP‑side policies (passwordless, risk‑based MFA) are recommended.
- **Outbound Services**
  - Egress allow‑list for email, storage, or CRM destinations.
  - Webhook signing and verification for event consumers.
- **Network**
  - Private links/VPC peering preferred; fallback to public endpoints with TLS and IP allow‑lists.

## Compliance and Evidence
- **Audit Logging**
  - Administrative actions, permission changes, and sensitive operations are logged.
  - Logs are immutable and time‑synchronized.
- **Data Residency**
  - Honors platform‑level residency controls; UI/BFF store no customer data at rest beyond transient caches.
- **Privacy**
  - PII minimization in telemetry; diagnostics scrubbed of sensitive content.
- **Evidence Packs**
  - Exportable artifacts for compliance audits (configuration, policies, and logs).

## Non‑Goals
- Cross‑tenant governance, platform SLO/SLA definitions, and global compliance attestations are owned by the Host App and platform services.
