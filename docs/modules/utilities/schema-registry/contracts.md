# Schema Registry Contracts

## Purpose

Contracts define the shape, metadata, and governance requirements for schemas.  
They ensure that every schema published in the BareCount Data Action Platform is explicit, versioned, and auditable.

## Structure

Each schema contract must contain:

- Schema identifier (`$id`)  
- Title and description  
- Version number  
- Properties and constraints  
- Required fields  
- Metadata: owner, approver, classification, PII tags, residency, retention  

## Rules

- Identifiers must be unique per tenant and schema family  
- Versions must increment semantically (v1, v2, v3)  
- Required fields cannot be removed in backward compatible upgrades  
- Classification and residency metadata cannot be omitted  
- Contracts must be validated before schema publication  

## Enforcement

Contracts are enforced by the Host policy engine and evidenced in the Trust ledger.  
Any schema without a valid contract is rejected.

## Example Contract Metadata

```json
{
  "id": "gdp.sales.order:v3",
  "owner": "finance-team@company.com",
  "approver": "data-governance@company.com",
  "classification": "confidential",
  "pii_tags": ["customer_id"],
  "residency": "in-country",
  "retention_days": 3650
}
```

