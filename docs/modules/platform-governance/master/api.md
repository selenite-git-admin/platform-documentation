# API

## Scope
Read heavy APIs for Platform Catalog with guarded admin writes. Endpoints return cache friendly responses with ETags. Calendars include an endpoint to resolve effective events for a tenant overlay.

## Conventions
- Base path is `/platform-catalog/v1`
- Requests and responses use `application/json`
- Authentication and authorization are handled by Access Modules
- Idempotency uses the `Idempotency-Key` header on POST and PUT
- Pagination uses `page` and `page_size`
- Time uses UTC ISO 8601


## Endpoints

### At a glance
| Operation | Method and Path |
| --- | --- |
| [List regions](#list-regions) | `GET /platform-catalog/v1/regions` |
| [List residency policies](#list-residency-policies) | `GET /platform-catalog/v1/data-residency-policies` |
| [List product plans](#list-product-plans) | `GET /platform-catalog/v1/product-plans` |
| [List namespace prefixes](#list-namespace-prefixes) | `GET /platform-catalog/v1/namespace-prefixes` |
| [List tag taxonomy](#list-tag-taxonomy) | `GET /platform-catalog/v1/tag-taxonomy` |
| [List compliance profiles](#list-compliance-profiles) | `GET /platform-catalog/v1/compliance-profiles` |

Calendars moved to Calendar Service. See [Calendar Service API](../calendar-service/api.md).
## Error model
```json
{"code":"invalid_request","message":"unknown region code","correlation_id":"..."}
```

## Idempotency and caching
- Use `Idempotency-Key` for POST and PUT
- Return `ETag` on reads and accept `If-None-Match`

## Rate limits
- Apply per caller on write endpoints. Reads can be higher but still bounded


Features and limits moved to Access: [Subscription Enforcement API](../../platform-subscription/subscription-enforcement/api.md)
