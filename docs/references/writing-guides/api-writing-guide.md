# API Writing Guide

## Scope
Use this guide to write and maintain API documentation for the BareCount platform. It defines structure, style, and conventions for REST-style APIs.

## Style and tone
- AWS-style narrative with select Simplified Technical English
- Present tense, active voice
- No em dashes
- No horizontal rules
- Do not use bold in the middle of sentences
- Do not bold hyperlinks
- Keep sentences short and testable

## Principles
- APIs are contracts. Document exact behavior and constraints
- Do not speculate or add behavior that is not implemented
- Prefer consistency over cleverness
- Every operation must be safe to retry unless documented otherwise

## Document structure for each API page
1. Scope
2. Conventions
3. Related documents
4. Roles
5. At a glance table
6. Endpoints (one section per operation)
7. Error model
8. Idempotency
9. Rate limits
10. Examples

## Conventions
- Base path documented at the top of the page
- Content type is `application/json` unless stated otherwise
- Resource identifiers use `uuid` unless stated otherwise
- Time uses UTC ISO 8601 with timezone suffix
- Decimal values documented with scale and rounding rules
- Idempotency uses `Idempotency-Key` header on unsafe operations
- Pagination uses `page` and `page_size` unless streaming is used
- Filtering via `?field=value` and explicit operators if needed (e.g. `status=in:active,archived`)

## Resource naming and paths
- Use nouns for resources and plural collection names
- Use lower kebab-case for paths
- Keep paths short and stable
- Nest under a versioned base path, for example `/service-name/v1`
- Do not expose internal database IDs or table names in paths

## Methods and semantics
- GET reads resources
- POST creates or triggers evaluations
- PUT replaces a full resource
- PATCH partially updates a resource
- DELETE removes or disables a resource (stateful delete is preferred over hard delete)

## Status codes
- 200 for successful reads and evaluation responses
- 201 for creations with a response body
- 202 for accepted long-running operations with `Location` for polling
- 204 for success with no body
- 400 invalid request
- 401 unauthorized
- 403 forbidden
- 404 not found
- 409 conflict
- 422 unprocessable entity when validation fails but the request is syntactically valid
- 429 rate limited
- 5xx for server errors

## Error model
Use a common shape for errors.
```json
{
  "code": "invalid_request",
  "message": "scope_type must be one of tenant, schema, workflow",
  "details": { "field": "scope_type" },
  "correlation_id": "df2f4e85a5d64e7bb7a1b1a5a2f4c6d8"
}
```
- `code` is a stable machine-readable value
- `message` is clear and human readable
- `details` is optional structured context
- `correlation_id` is required for tracing

## Idempotency
- Require `Idempotency-Key` for POST requests that create or change state
- Return the same response for retries with the same key within the window
- Document the retention window for idempotency keys
- Idempotency keys must be unique per caller and resource type

## Concurrency control
- Use `ETag` and `If-Match` for conditional updates where appropriate
- Describe expected conflict behavior and retry guidance

## Pagination
- Use `page` and `page_size`
- Return `page`, `page_size`, and `total` in the response
- Enforce maximum `page_size` and document it
- Prefer cursor pagination for large or frequently changing collections

## Filtering and sorting
- Document allowed filter fields and operators
- Document default sort order and supported fields

## Security
- Authentication and authorization are documented at the service family level
- Do not duplicate identity details in API pages
- Document required scopes or roles for each operation if applicable
- Never include secrets in examples

## Headers
- Required: `Authorization`, `Content-Type`, `Idempotency-Key` where relevant
- Recommended: `Accept`, `Correlation-Id`
- Return `Retry-After` for `429` and `503`

## Long-running operations
- Return `202 Accepted` with a `Location` header for polling
- Provide a `GET` status endpoint and document terminal states

## Webhooks and callbacks
- Document event types, payload shape, and retry policy
- Require signature verification details and timestamp tolerance

## Observability
- State the log event names and fields
- List key metrics and units
- Provide example correlation flow between request, evaluation, and decision log

## Example section layout for an operation
Use the following order for each operation block.

### Operation name
`METHOD /service/v1/path`

Request
```json
{ "example": "request" }
```

Response 200
```json
{ "example": "response" }
```

Failure 400
```json
{
  "code": "invalid_request",
  "message": "example"
}
```

Notes
- Required fields listed explicitly
- Validation rules and limits
- Side effects and emitted events, if any

## At a glance table
Place a two-column table under “Endpoints”. Make operation names clickable using Markdown anchors that match the `### Operation name` headings.

Example
```markdown
| Operation | Method and Path |
| --- | --- |
| [Create policy](#create-policy) | `POST /policy-registry/v1/policies` |
| [Evaluate](#evaluate) | `POST /policy-registry/v1/evaluate` |
```

## Examples
Include realistic `curl` examples. Show required headers, including `Authorization` and `Idempotency-Key` for POST.

## OpenAPI
- Keep OpenAPI specs in `docs/assets/api/<service>-api.yaml` if used
- The Markdown page remains the primary reference
- If a spec is present, link it at the top of the API page

## Review checklist
- Scope and Conventions are present
- At a glance table exists and links to each operation
- Every operation has request and response examples
- Error model is documented once and referenced
- Idempotency and rate limit rules are stated
- Pagination, filtering, and sorting are defined for list endpoints
- Security notes are consistent with Access Modules
- Links to related module pages are correct
