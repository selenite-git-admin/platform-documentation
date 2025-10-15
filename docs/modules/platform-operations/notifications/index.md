# Notifications

**Family:** Core Platform  
**Tier:** Foundation  
**Owner:** Platform Foundation  
**Status:** Draft

## Purpose
Provide a uniform way to inform users and systems about important events. This module standardizes channels, payloads, retry behavior, and governance so product teams can trigger notifications without building channel-specific logic.

## Design Principles
- One contract for all channels
- Zero engineering at the edges: product teams call a simple API
- Durable delivery with clear at-least-once semantics
- Tenant-safe templates and redaction policies
- Observable outcomes with correlation to Evidence Ledger

## Scope
Included:
- Human channels: email, Slack (or equivalent), in-app banner and toast
- System channels: webhooks
- Templates, variables, localization, and throttling
- Delivery receipts and complaint feedback

Excluded:
- Marketing campaigns
- Real-time chat

## Architecture Overview
```
Producers → Notification API → Queue → Worker → Channel Adapters → Providers
                                       ↘ Evidence Ledger
                                       ↘ Observability/DRR
```

- Producers send a channel-agnostic request with a template id and variables
- The API enqueues a job and returns a correlation id
- Workers render the template, route to channel adapters, and call providers
- Delivery attempts and outcomes are written to Evidence Ledger
- Aggregates power dashboards and SLO checks

## Channel Contracts
### Email
- RFC-compliant sender, subject, and body (HTML and text)
- Provider integration supports SPF/DKIM/DMARC
- Bounce and complaint hooks update suppression lists

### Slack
- Bot token or webhook per tenant
- Rich attachments allowed but must be under size thresholds
- Channel address stored in tenant configuration

### In-app
- Banners and toasts with severity, scope, and expiry
- Client polls or receives push to render pending notifications

### Webhook
- Signed POST with canonical envelope
- Idempotency key replay window 24 hours
- Retries with exponential backoff and dead-letter after max attempts

## Request Model
```json
{
  "template_id": "password-reset",
  "channel": ["email","inapp"],
  "to": [{"type":"user","id":"uuid"}],
  "variables": {"name":"Riya","reset_url":"..."},
  "priority": "normal",
  "idempotency_key": "c9f7..."
}
```

### Required fields
- `template_id`: selects content and policy
- `channel`: list of channels to fan out
- `to`: user or system destination
- `variables`: template variables

### Optional fields
- `priority`: normal or high
- `schedule_at`: optional future time within 7 days
- `idempotency_key`: client-supplied replay guard

## Delivery Semantics
- At-least-once per channel
- Idempotent downstream calls using `Idempotency-Key` and provider message ids
- Retries: exponential with jitter, channel-specific caps
- Dead-letter queue for exhausted retries with operator workflows

## Templates
- Stored in PostgreSQL with versioning and localization
- Variables are validated against a schema
- Preview endpoint for authors
- No dynamic code in templates; only variable substitution and a small safe helper set

## Governance
- Sensitive variables are redacted in logs
- Access classes restrict who can trigger specific templates
- Tenants can opt out of channels per template
- Rate limits per tenant and globally

## Data Model (summary)
- `notification_request` (immutable)
- `notification_attempt` (per channel try)
- `template` and `template_version`
- `destination` settings per tenant

DBML sketch:
```dbml
Table template {
  id text [pk]
  name text
  description text
  created_at timestamptz
}

Table template_version {
  id uuid [pk]
  template_id text [ref: > template.id]
  locale text
  subject text
  body_html text
  body_text text
  variables_schema jsonb
  created_at timestamptz
  is_active boolean
}

Table notification_request {
  id uuid [pk]
  template_id text
  variables jsonb
  channels jsonb
  to jsonb
  priority text
  idempotency_key text
  correlation_id uuid
  created_at timestamptz
}

Table notification_attempt {
  id uuid [pk]
  request_id uuid [ref: > notification_request.id]
  channel text
  status text
  provider_id text
  status_code text
  error_code text
  retry_count int
  last_attempt_at timestamptz
}
```

## API Outline
- `POST /notifications` create request, returns `correlation_id`
- `POST /notifications/preview` previews a template with variables
- `GET /notifications/{id}` returns request status and channel outcomes
- `POST /webhooks/notification` provider callbacks for bounces and complaints

All errors use the platform error envelope.

## Observability and SLOs
- `delivery.success_rate` per channel ≥ 99 percent
- `delivery.latency.p95` within channel threshold (email < 30s, webhook < 10s)
- Dashboards by template, tenant, and channel
- Alerts on bounce spikes and webhook failures

## Security
- Sign all webhooks and verify signatures
- No PII in logs; email body never logged
- Secrets in channel adapters live in the Secrets module
- Access control on template usage and preview endpoints

## Runbook Highlights
- Spike in bounces: check domain settings, DKIM, recent template changes
- Webhook failures: validate destination certs and idempotency handling
- Slack failures: rotate tokens, verify scopes, rate limit retries
- In-app backlog: verify queue and client poll cadence

## Examples
### Password reset
Channels: email and in-app banner  
Variables: `name`, `reset_url`  
Policy: high priority, rate limit 1 per user per hour

### KPI alert
Channels: Slack and webhook  
Variables: `kpi_name`, `delta`, `threshold`, `dashboard_url`  
Policy: normal priority, tenant opt-out enabled

## Summary
Notifications give product teams a safe, reliable, and uniform way to reach users and systems. With templates, channel adapters, and strong governance, this module delivers messages consistently without each team rebuilding the same plumbing.