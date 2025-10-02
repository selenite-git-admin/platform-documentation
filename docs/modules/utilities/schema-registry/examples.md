# Schema Examples

## Extraction Schema

```json
{
  "$id": "extract.sap.invoice:v1",
  "title": "SAP Invoice Extraction",
  "type": "object",
  "properties": {
    "invoice_id": { "type": "string" },
    "company_code": { "type": "string" },
    "amount": { "type": "number" },
    "currency": { "type": "string" },
    "posting_date": { "type": "string", "format": "date" }
  },
  "required": ["invoice_id", "company_code", "amount", "currency", "posting_date"]
}
```

## Raw Schema

```json
{
  "$id": "raw.invoice.header:v2",
  "title": "Raw Invoice Header",
  "type": "object",
  "properties": {
    "invoice_id": { "type": "string" },
    "vendor_id": { "type": "string" },
    "gross_amount": { "type": "number" },
    "tax_amount": { "type": "number" },
    "currency": { "type": "string" },
    "created_at": { "type": "string", "format": "date-time" }
  },
  "required": ["invoice_id", "vendor_id", "gross_amount", "currency", "created_at"]
}
```

## GDP Schema

```json
{
  "$id": "gdp.sales.order:v3",
  "title": "Sales Order",
  "type": "object",
  "properties": {
    "order_id": { "type": "string" },
    "tenant_id": { "type": "string" },
    "customer_id": { "type": "string" },
    "order_date": { "type": "string", "format": "date-time" },
    "currency_code": { "type": "string", "pattern": "^[A-Z]{3}$" },
    "net_amount": { "type": "number" },
    "tax_amount": { "type": "number" },
    "total_amount": { "type": "number" },
    "discount_amount": { "type": ["number", "null"] }
  },
  "required": ["order_id", "tenant_id", "order_date", "currency_code", "net_amount", "total_amount"]
}
```

## KPI Schema

```json
{
  "$id": "kpi.cfo.gross_margin:v2",
  "title": "Gross Margin",
  "type": "object",
  "properties": {
    "period_key": { "type": "string" },
    "tenant_id": { "type": "string" },
    "revenue": { "type": "number" },
    "cogs": { "type": "number" },
    "gross_margin_pct": { "type": "number" }
  },
  "required": ["period_key", "tenant_id", "revenue", "cogs", "gross_margin_pct"]
}
```

## Activation Schema

```json
{
  "$id": "activation.crm.campaign_trigger:v1",
  "title": "CRM Campaign Trigger",
  "type": "object",
  "properties": {
    "campaign_id": { "type": "string" },
    "tenant_id": { "type": "string" },
    "customer_id": { "type": "string" },
    "trigger_date": { "type": "string", "format": "date-time" },
    "kpi_reference": { "type": "string" }
  },
  "required": ["campaign_id", "tenant_id", "customer_id", "trigger_date", "kpi_reference"]
}
```
