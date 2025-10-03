# UI

## Scope
Screen definitions for Data Contract Registry. This page lists required screens, where they belong, their data elements, and API dependencies for the artifact-only model with four layers: extraction, raw, gold, activation.

## Placement
- Platform Admin App: authoring and operations
- Tenant App: read-only discovery for tenant users when you choose to expose it

## Screens at a glance
| Screen | App | Purpose |
| --- | --- | --- |
| [Datasets](#datasets) | Platform Admin App | List and search datasets |
| [Dataset detail](#dataset-detail) | Platform Admin App | View layers and schema timelines |
| [Ingest schema](#ingest-schema) | Platform Admin App | Post a new schema for a layer |
| [Diff versions](#diff-versions) | Platform Admin App | Compare two versions and view classification |
| [Subscriptions](#subscriptions) | Platform Admin App | Manage consumer subscriptions |
| [Tenant discovery](#tenant-discovery) | Tenant App | Browse current schemas for allowed datasets |

## Datasets
Purpose
List and search datasets by namespace, name, owner, and status.

Primary actions
- Create dataset
- Open dataset detail

Data elements
- namespace, name, owner, status, created_at

API
- [List datasets](api.md#list-datasets)
- [Create dataset](api.md#create-dataset)

Wireframe

<a href="#fig-dcr-datasets" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/datasets.svg" alt="Datasets list">
</a>

<div id="fig-dcr-datasets" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/datasets.svg" alt="Datasets list">
</div>

_Figure 1: Datasets list_{.figure-caption}

## Dataset detail
Purpose
Inspect a dataset across layers with timelines. Show current version, history, and quick links for actions.

Layout
- Header with namespace, name, owner, status
- Tabs per layer: extraction, raw, gold, activation
- Each tab shows: Current version, version timeline, actions (Ingest, Diff)

Primary actions
- Ingest schema to the selected layer
- Open diff between two versions
- Create subscription for this dataset and layer

Data elements
- layer, current_version, compatibility, created_at, created_by

API
- [List schema versions](api.md#list-schema-versions)
- [Get schema version](api.md#get-schema-version)

Wireframe

<a href="#fig-dcr-dataset-detail" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/dataset-detail.svg" alt="Dataset detail with layers and timeline">
</a>

<div id="fig-dcr-dataset-detail" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/dataset-detail.svg" alt="Dataset detail with layers and timeline">
</div>

_Figure 2: Dataset detail_{.figure-caption}

## Ingest schema
Purpose
Post a new schema artifact for a dataset and layer. Prefer additive changes. Use `set_current_if_compatible` to promote on ingest.

Primary actions
- Upload or paste schema JSON
- Submit ingest

Data elements
- schema_json or schema_registry_id
- set_current_if_compatible

API
- [Ingest schema for a layer](api.md#ingest-schema-for-a-layer)

## Diff versions
Purpose
Compare two versions for a dataset and layer and view compatibility classification.

Primary actions
- Select from and to versions
- View JSON patch and classification

Data elements
- from_version, to_version, changes[], classification

API
- [Diff versions](api.md#diff-versions)

Wireframe

<a href="#fig-dcr-diff" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/diff-view.svg" alt="Schema diff view">
</a>

<div id="fig-dcr-diff" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/diff-view.svg" alt="Schema diff view">
</div>

_Figure 3: Diff view_{.figure-caption}

## Subscriptions
Purpose
Manage consumer subscriptions for dataset layers. Subscriptions attach to a dataset and a layer.

Primary actions
- Create subscription
- Filter by dataset, layer, consumer

Data elements
- consumer, layer, required_compatibility, min_version, created_at

API
- [Create subscription](api.md#create-subscription)
- [List subscriptions](api.md#list-subscriptions)

Wireframe

<a href="#fig-dcr-subscriptions" class="image-link">
  <img src="/assets/diagrams/data-contract-registry/subscriptions.svg" alt="Subscriptions list and detail">
</a>

<div id="fig-dcr-subscriptions" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/data-contract-registry/subscriptions.svg" alt="Subscriptions list and detail">
</div>

_Figure 4: Subscriptions_{.figure-caption}

## Tenant discovery
Purpose
Read-only view for tenant users to browse current schemas for datasets they are allowed to see.

Primary actions
- Browse by namespace and layer
- Copy schema JSON or schema ID

API
- [List datasets](api.md#list-datasets)
- [Get schema version](api.md#get-schema-version)

## Telemetry
Log events
- ui.dcr.dataset.create
- ui.dcr.schema.ingest
- ui.dcr.version.diff.view
- ui.dcr.subscription.create

Metrics
- dcr_ui_datasets_load_time_ms
- dcr_ui_diff_compute_time_ms

## Access
- Platform Admin App requires platform roles for write actions
- Tenant App is read-only unless a role grants write on subscriptions for tenant-scoped datasets

## Accessibility
- All actions are keyboard accessible
- Provide labels and aria attributes
- Use sufficient color contrast
