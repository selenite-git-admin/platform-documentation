# Schema Registry Interfaces

## APIs

The registry exposes programmatic interfaces to submit, validate, approve, and discover schemas.

- `POST /schemas/propose` – submit draft schema  
- `POST /schemas/validate` – validate payload against schema  
- `POST /schemas/approve` – approve schema version  
- `GET /schemas/{id}` – fetch schema definition  
- `GET /schemas/search?tag=...` – discover schemas by metadata  
- `POST /schemas/deprecate` – mark schema deprecated  
- `POST /schemas/rollback` – restore previous published version  

All APIs require authentication. Approvals require authorization roles.

## CLI

A command line interface wraps the APIs for developers.

```bash
barecount schemas propose ./gdp.sales.order.json
barecount schemas validate ./payload.json --schema gdp.sales.order:v3
barecount schemas search --tag=kpi
barecount schemas approve gdp.sales.order:v3
```

## UI

Schemas are also accessible in the BareCount Admin App for discovery, approval, and deprecation workflows.
