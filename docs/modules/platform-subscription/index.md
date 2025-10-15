# Platform Subscription

The Platform Subscription family defines how tenants, subscriptions, and entitlements are managed across the DataJetty platform.  
It establishes identity and commercial context for every request, ensuring that access, usage, and feature availability align with contractual terms and tenant configurations.

Subscription services form the logical starting point for all platform operations.  
Every API call, data pipeline, and analytic job runs within the boundaries defined here — a tenant, a plan, and an entitlement set.  
The family integrates with authentication and authorization from Core, while its state and policies are referenced by Platform Control and Platform Operations at runtime.

### Functional Coverage

- Manages tenant onboarding, configuration, and identity linkage.  
- Defines subscription plans, pricing tiers, and active entitlements.  
- Applies runtime enforcement for feature gating and quota validation.  
- Tracks subscription lifecycle events, renewals, and expirations.  
- Propagates tenant and entitlement metadata to downstream families for context-aware operations.  
- Serves as the single source of truth for all tenant and plan relationships within the platform.

### Modules

[Tenancy](tenancy/index.md)  
Handles tenant creation, configuration, access credentials, and lifecycle state across all environments.

[Subscription](subscription/index.md)  
Defines commercial plans, plan tiers, usage counters, and billing synchronization logic.

[Subscription Enforcement](subscription-enforcement/index.md)  
Applies entitlement checks and feature gating rules for APIs, pipelines, and jobs before execution.
