# Authentication

## Role in the Platform
Authenticate human and machine identities (tenant, admin, service).

## Responsibilities
- Handle OAuth2/OIDC
- Issue and validate JWT tokens
- Support API Keys/service principals
- MFA/conditional access

## Inputs
- IdP assertions
- Client metadata
- Tenant policy

## Outputs
- Tokens
- Sessions
- Auth events

## Lifecycle
IdP redirect → callback → token issuance → rotation/expiry → revoke
