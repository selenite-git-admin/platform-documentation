# User Interface Writing Guide

## Scope
Define how to document screens and flows for a module.

## Structure
1. Scope
2. Placement
3. Screens at a glance
4. Screen details
5. Accessibility and localization
6. Error, loading, and empty states
7. Dependencies

## Placement
State which app hosts the screen: Platform Admin App or Tenant App. Mention roles that can access it.

## Screens at a glance
Provide a two column table of screen and purpose. Link each screen name to its section anchor.

## Screen details
For each screen include
- Purpose
- Primary actions
- Roles and permissions
- State model and validation rules
- API dependencies with links to operations
- Navigation entry points and exit points
- Notes on responsiveness if relevant

## Accessibility and localization
- Keyboard navigation and focus order
- Labels, aria attributes, and color contrast
- Timezone and locale rules for numbers and dates

## Error, loading, and empty states
- Show messages and recovery actions
- Use consistent patterns for skeletons and spinners
- Provide examples for common failures

## Dependencies
List API calls, feature flags, and upstream configuration needed for the screen to work.
