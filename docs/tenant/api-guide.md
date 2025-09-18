# Tenant App – API Guide

## Purpose
The API guide documents how the Tenant App UI interacts with platform services through the back‑for‑frontend (BFF).  
It is primarily for internal developers maintaining the Tenant App.  
External developers should use platform APIs directly (Schema Service, KPI Service, Activation Plane, PHS).

## Authentication
- **Method**: OAuth2/OIDC flows with JWT tokens.  
- **Scopes**: Prefix `tenant.*` to mirror UI permissions.  
- **Examples**:  
  - `tenant.exec.*` – executive actions.  
  - `tenant.admin.*` – administrative configuration.  
  - `tenant.data.read` – read access to curated datasets.  

## Common Patterns
- **Idempotent Writes**  
  - Use `X‑Idempotency‑Key` header for POST/PUT requests.  
- **Pagination**  
  - Cursor‑based pagination with `next_token`.  
- **Conditional Requests**  
  - `If‑None‑Match` headers supported for cache validation.  
- **Error Model**  
  - All errors return JSON with:  
    ```json
    {
      "code": "string",
      "message": "string",
      "details": [ ... ],
      "correlation_id": "uuid"
    }
    ```

## Example Endpoints
- `POST /sources` – create a source and return validation checklist.  
- `POST /activations/{id}/run` – trigger an activation run.  
- `GET /reports/{id}/download` – return signed URL for report export.  

## Notes
- All requests require tenant scoping in headers or tokens.  
- BFF calls platform services and reshapes responses for the UI.  
- Use platform API references for field‑level details.  
