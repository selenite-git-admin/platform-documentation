# Health Security

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Active

## Purpose
Secure the Health module endpoints and processing paths for liveness, readiness, startup, metrics, and data freshness. This document assumes API Gateway and Lambda, with IAM based authentication, VPC endpoints, and least privilege.

## Threat model
- Unauthorized access to `/readyz`, `/startupz`, `/dataz`, or `/metrics`
- Information disclosure through verbose health payloads
- Replay or spoofing of fleet rollup requests
- Abuse and resource exhaustion by frequent probing
- Cross environment leakage between staging and production
- Configuration drift that exposes private health routes to the internet

## Principles
- Default deny on sensitive endpoints
- Stable and minimal responses without hostnames, stack traces, or credentials
- Separation of public liveness from authenticated readiness and data endpoints
- Defense in depth with IAM, resource policies, VPC endpoints, and rate limits
- Short retention for logs while preserving evidence for audit

## Authentication and authorization
- `/healthz` can be public if required by external monitors
- `/readyz`, `/startupz`, `/dataz` and `/fleet/*` require authentication when accessed outside the VPC
- `/metrics` is private and scraped only by the platform collector

Recommended controls
- JWT or OAuth2 on API Gateway for external callers
- Lambda authorizer for token verification when needed
- IAM auth for internal callers using SigV4
- Resource policies on API Gateway that limit source VPC or CIDR ranges

### API Gateway resource policy example
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowHealthzPublic",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:ap-south-1:123456789012:abc123/prod/GET/healthz"
    },
    {
      "Sid": "DenyReadyzFromInternet",
      "Effect": "Deny",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:ap-south-1:123456789012:abc123/prod/GET/readyz",
      "Condition": {
        "NotIpAddress": { "aws:SourceIp": ["10.0.0.0/8","192.168.0.0/16"] }
      }
    }
  ]
}
```

## Network and transport
- Enforce HTTPS only
- Enable HSTS on public stages
- For private access, put `/readyz`, `/startupz`, `/dataz`, and `/metrics` behind a private API in a VPC with interface endpoints for SQS, Secrets Manager, RDS, and CloudWatch
- Disable TLS weak ciphers and protocols through API Gateway stage settings

## Request headers
- Require and echo `X-Correlation-Id` where provided
- `Cache-Control: public, max-age=10` for `/healthz`
- `Cache-Control: no-store` for `/readyz`, `/startupz`, `/dataz`, and fleet endpoints
- Do not reflect request headers that might leak details

## Payload hygiene
- Health responses include only `status`, timing, and short hints
- Never include hostnames, IPs, usernames, schema names, connection strings, or stack traces
- Dataset names in `/dataz` use public identifiers only and never include tenant ids
- Errors use the platform envelope with short messages only

## Abuse protections
- Soft rate limits per caller for `/readyz`, `/startupz`, and `/dataz`
- Fleet aggregator limited to a low RPS per caller
- WAF on the public stage when `/healthz` is exposed
- Alarms on unusual request volume to health routes

## IAM for Lambda
Execution role should include only the following minimal permissions
- Read from Secrets Manager by key alias
- Read config and feature flags
- RDS or PostgreSQL connectivity via IAM DB authentication if used
- SQS send or receive as needed for synthetic checks

Example IAM policy snippet
```json
{
  "Version": "2012-10-17",
  "Statement": [
    { "Effect": "Allow", "Action": ["secretsmanager:GetSecretValue"], "Resource": "arn:aws:secretsmanager:ap-south-1:123456789012:secret:platform/*" },
    { "Effect": "Allow", "Action": ["sqs:GetQueueAttributes","sqs:SendMessage"], "Resource": "arn:aws:sqs:ap-south-1:123456789012:health-*"},
    { "Effect": "Allow", "Action": ["logs:CreateLogGroup","logs:CreateLogStream","logs:PutLogEvents"], "Resource": "*" }
  ]
}
```

## VPC and endpoint controls
- Use VPC endpoints for Secrets Manager, SQS, and CloudWatch Logs so checks do not traverse the internet
- Security groups restrict egress to necessary endpoints only
- NACLs enforce subnet level boundaries between environments

## Metrics security
- `/metrics` is not publicly routable
- Scraper identity is an IAM role with permission to read only through private networking
- Expose only service level counters and histograms, never include labels that contain secrets or internal hostnames

## Aggregation security
- The fleet aggregator reads service states through private networking or from the Health data store
- Aggregator responses avoid enumerating internal hosts
- Responses may include partial results and never embed per service failure details beyond `ok`, `degraded`, or `fail`

## Logging and trace hygiene
- Logs are structured and contain only safe keys such as `status`, `latency_ms`, `service_name`, and `check_name`
- Correlation ids flow into traces for deeper diagnostics
- Error logs do not include stack traces by default; traces carry detailed spans under access control

## Data model and privacy
- Health tables store platform scoped data only
- No tenant identifiers are stored or returned
- Evidence references are optional and do not embed payloads

## Configuration defaults
| Setting | Default | Purpose |
|---|---|---|
| `HEALTH_READYZ_RPS_LIMIT` | 10 | Prevent abuse |
| `HEALTH_FLEET_RPS_LIMIT` | 2 | Protect aggregator |
| `HEALTH_HINT_MAX_BYTES` | 128 | Keep hints short and safe |
| `HEALTH_CACHE_TTL_HEALTHZ_SEC` | 10 | Public liveness caching |
| `HEALTH_REQUIRE_AUTH_READYZ` | true | Guard readiness |
| `HEALTH_REQUIRE_AUTH_DATAZ` | true | Guard data freshness |
| `HEALTH_LOG_RETENTION_DAYS` | 30 | Control cost and exposure |

## Testing checklist
- Calls to `/readyz` and `/dataz` from the internet are rejected
- `/metrics` not reachable from public subnets
- Rate limits trip on synthetic flood and recover cleanly
- Payloads return only allowed fields under failure
- Correlation ids propagate to logs and traces
- API Gateway resource policy denies unexpected CIDRs

## Incident response hooks
- When health payloads appear to reveal sensitive details, roll the stage immediately and revert to safe build
- For excessive probing or DDoS on `/healthz`, enable WAF block rules and raise rate limits selectively for trusted monitors
- If unauthenticated access to `/readyz` or `/dataz` is detected, rotate keys, disable public stage, and audit recent calls

## Change management
- Changes to health schemas or headers require a review by Platform Foundation and Security
- Any expansion of payload fields must demonstrate zero risk of information disclosure

## Summary
The Health module balances visibility with restraint. Restrict sensitive routes, keep responses minimal, apply network and IAM boundaries, and enforce rate limits. With these controls in place, health signals remain useful to operators without exposing internals or creating attack surface.