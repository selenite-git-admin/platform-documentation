# API (CLI)

All commands are idempotent with `--request-id`.

```bash
# Validate local schema file against additive rules
bc schema validate --kind gdp --file schema.json --ruleset additive

# Diff local schema against latest in registry
bc schema diff gdp:order --file schema.json

# Create a new version
bc schema push gdp:order --file schema.json --compatibility additive --request-id req_01J...

# Propose deprecation
bc schema deprecate gdp:order --field legacy_code --window 180 --note "replace with product_code"

# Search subjects
bc schema search "owner:finance tag:core gdp:*"
```
