# Tenant App – Troubleshooting

## SSO Failures
- Check IdP metadata validity and certificate expiry.
- Verify clock synchronization between IdP and Tenant App.
- Confirm redirect URIs are correctly configured.

## Onboarding Validation Fails
- Retry validation with verbose logging enabled.
- Review schema drift warnings from Schema Service.
- Check source system quotas and API rate limits.

## Activation Run Stuck
- Inspect activation queue depth in the Activation Plane.
- Retry run with the same idempotency key.
- Confirm approvals have been granted.

## Reports Not Visible
- Verify user role includes report access permissions.
- Confirm dataset freshness within contract window.
- Review applied row‑level and column‑masking rules.
