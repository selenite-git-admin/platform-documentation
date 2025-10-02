# User Interface

## Scope
This page defines the user interface surfaces for Policy Registry.
It lists the required screens, where they belong, and their API dependencies.

## Placement
- Platform Admin App: administration and operations views
- Tenant App: tenant-facing decisions and approvals

## Screens at a glance
| Screen                                                            | App                | Purpose                                 |
|-------------------------------------------------------------------|--------------------|-----------------------------------------|
| [Policies](#policies)                                             | Platform Admin App | List, search, and create policies       |
| [Policy detail and versions](#policy-detail-and-versions)         | Platform Admin App | Inspect policy metadata and versions    |
| [Create or edit policy](#create-or-edit-policy)                   | Platform Admin App | Author policy and publish a new version |
| [Bindings](#bindings)                                             | Platform Admin App | List and create bindings for scopes     |
| [Binding detail](#binding-detail)                                 | Platform Admin App | Inspect binding and related evaluations |
| [Evaluations](#evaluations)                                       | Platform Admin App | Browse decisions and filter by result   |
| [Evaluation detail and evidence](#evaluation-detail-and-evidence) | Platform Admin App | Inspect a decision and its evidence     |
| [Audit log](#audit-log)                                           | Platform Admin App | View administrative changes             |
| [Tenant decisions](#tenant-decisions)                             | Tenant App         | View decisions impacting the tenant     |
| [Request approval](#request-approval)                             | Tenant App         | Submit approval when required           |
| [Tenant bindings](#tenant-bindings)                               | Tenant App         | View active bindings for tenant scope   |

## Policies
Purpose
List and search policies. Create a new policy.

Primary actions
- Create policy
- Search and filter

Data elements
- name, category, status, created_at

API
- [List policies](api.md#list-policies)
- [Create policy](api.md#create-policy)

Wireframe

<a href="#fig-policy-list" class="image-link">
  <img src="/assets/diagrams/policy-registry/policy-list.svg" alt="Policy list screen">
</a>

<div id="fig-policy-list" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/policy-registry/policy-list.svg" alt="Policy list screen">
</div>

_Figure 1: Policy list_{.figure-caption}

## Policy details and versions
Purpose
Inspect a policy, its versions, and current flag.

Primary actions
- Create version
- Set current version

Data elements
- policy_id, name, status, versions

API
- [Get policy](api.md#get-policy)
- [List policy versions](api.md#list-policy-versions)
- [Create a policy version](api.md#create-policy-version)
- [Set current version](api.md#set-current-version)

## Create or edit policy
Purpose
Author a new policy or update metadata.

Primary actions
- Save draft
- Publish active

API
- [Create policy](api.md#create-policy)

## Bindings
Purpose
List and create bindings for scopes.

Primary actions
- Create binding
- Filter by scope_type and scope_ref

Data elements
- policy_id, version_id, scope_type, scope_ref, status, created_at

API
- [List bindings](api.md#list-bindings)
- [Create binding](api.md#create-binding)

## Binding detail
Purpose
Inspect a binding and related evaluations.

Primary actions
- Disable binding

Data elements
- binding_id, policy_id, version_id, scope_type, scope_ref, status

API
- [List bindings](api.md#list-bindings)

Wireframe

<a href="#fig-binding-detail" class="image-link">
  <img src="/assets/diagrams/policy-registry/binding-detail.svg" alt="Binding detail screen">
</a>

<div id="fig-binding-detail" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/policy-registry/binding-detail.svg" alt="Binding detail screen">
</div>

_Figure 2: Binding detail_{.figure-caption}

## Evaluations
Purpose
Browse decisions and filter by result.

Primary actions
- Filter by decision and subject_type
- Open evaluation detail

Data elements
- eval_id, binding_id, subject_type, subject_ref, decision, evaluated_at

API
- [Get evaluation](api.md#get-evaluation)

## Evaluation detail and evidence
Purpose
Inspect a single decision with its evidence.

Primary actions
- Export evidence

API
- [Get evaluation](api.md#get-evaluation)

## Audit log
Purpose
View administrative changes.

Data elements
- actor, action, target, at

## Tenant decisions
Purpose
Allow a tenant user to view decisions that affect the tenant scope.

Primary actions
- Filter by decision
- Export evidence

API
- [Get evaluation](api.md#get-evaluation)

## Request approval
Purpose
Allow a tenant approver to respond to required approvals.
This screen hosts the workflow control that records the approval.

Note
Approval mechanics live in workflow execution. This screen surfaces the request.

## Tenant bindings
Purpose
Show bindings that apply to the tenant scope.

API
- [List bindings](api.md#list-bindings)

## Telemetry
Log events
- ui.policy.search
- ui.policy.create
- ui.binding.create
- ui.evaluation.view

Metrics
- policy_list_load_time_ms
- evaluation_detail_load_time_ms

## Access
- Platform Admin App screens require administrator or operator roles
- Tenant App screens require tenant membership

## Accessibility
- Form controls must be keyboard operable
- Provide labels and aria attributes for screen readers
- Use sufficient color contrast
