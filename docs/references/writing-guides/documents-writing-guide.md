# Documentation Writing Guide

This guide defines the global rules for writing documentation in the BareCount Data Action Platform project.  
It applies to all content: module docs, architecture, user stories, references, and contributor material.

---

## 1. Tone and Style

- Write in AWS-style narrative: direct, factual, explanatory.  
- Use present tense. Use active voice unless the actor is unknown.  
- Do not sell. Do not speculate. Avoid marketing phrases or consultant jargon.  
- Keep sentences short (20 words or fewer). Split long ideas into multiple sentences.  
- One fact or instruction per sentence.  

---

## 2. Language Rules

- Use controlled verbs: configure, provision, validate, publish, record, enforce, authorize, authenticate, schedule, route, monitor, retry, rollback, export.  
- Define terms once in the Glossary or on first use. Use consistently across docs.  
- Prefer indicative mood for concepts, imperative for procedures.  
- Avoid ambiguous terms: robust, scalable, seamless, best-in-class, typical, often, usually.  
- Remove adjectives that cannot be measured. If you cannot quantify it, omit it.  
- Cross-reference precisely with Markdown links. Do not use vague references like “the system” or “elsewhere.”  

---

## 3. Formatting

### Markdown Guidelines
- Do not use em dashes.  
- Do not use horizontal rules.  
- Do not use bold in the middle of sentences.  
- Bold may be used at the start of a line for labels or list items.  
- Do not bold hyperlinks. Links must remain plain `[text](path.md)`.  
- Use `-` for bullets. Each bullet is one action or fact.  
- Use `#`, `##`, `###` for headings only as needed.  
- Wrap code, identifiers, and technical terms in backticks.  

### Image Embedding Guidelines
Use this pattern for all images across the documentation. It provides a clickable thumbnail that opens a modal with the full-size image.

**Rules**
- Always embed images with the modal pattern below.
- Do not use Markdown image syntax.
- Use absolute paths from site root: `/assets/diagrams/...`
- Give every image a unique `id` and meaningful `alt` text.
- Store files under `docs/assets/diagrams/<area>/<name>.svg`.
- Add an italic caption line with the `.figure-caption` class.
- Ensure the theme or custom CSS styles `.image-link`, `.image-modal`, `.close-btn`, and `.figure-caption`.

**Template**
```html
<a href="#fig-unique-id" class="image-link">
  <img src="/assets/diagrams/<area>/<name>.svg" alt="<Alt text>">
</a>

<div id="fig-unique-id" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/<area>/<name>.svg" alt="<Alt text>">
</div>

_Figure N: <Caption text>_{.figure-caption}
```

**Example**
```html
<a href="#fig-policy-registry-erd" class="image-link">
  <img src="/assets/diagrams/policy-registry/policy-registry-erd.svg" alt="Policy Registry ERD">
</a>

<div id="fig-policy-registry-erd" class="image-modal">
  <a href="#" class="close-btn">&times;</a>
  <img src="/assets/diagrams/policy-registry/policy-registry-erd.svg" alt="Policy Registry ERD">
</div>

_Figure 1: Policy Registry ERD_{.figure-caption}
```

**Notes**
- Keep `alt` short and descriptive.
- Increment figure numbers per page.
- Reuse the same path for thumbnail and enlarged image.
---

## 4. Content Focus

- Anchor every statement in what the platform does and how it works.  
- Tie explanations to modules, workflows, or user stories from the uploaded docs.  
- Do not make modules sound dependent on stories. Modules are primary; stories illustrate usage.  
- Replace abstract ideas with concrete mechanics.  
- State inputs, outputs, responsibilities, and constraints wherever possible.  

---

## 5. Document Types

Each document type should follow a consistent skeleton.

### Module Family Index
- Role in the Platform  
- Modules (list with hyperlinks + description)  
- Position in the Platform  

### Submodule Page
- Role in the Platform  
- Responsibilities  
- Inputs  
- Outputs  
- Interfaces  
- Operational Behavior  
- Constraints  
- Related User Stories  

### User Story
- Context  
- Trigger  
- Steps  
- Expected Result  
- Related Modules  

### Architecture Doc
- Purpose  
- Logical view  
- Data flow  
- Governance and constraints  
- ADR links  

---

## 6. Do’s and Don’ts

**Do**  
- Describe mechanics and actions.  
- State interfaces, inputs, and outputs.  
- Clarify scope boundaries and module responsibilities.  

**Don’t**  
- Write generic claims like “This is critical for governance.”  
- Use vague words like “robust,” “seamless,” or “often.”  
- Flip causality between modules and stories.  
- Add filler such as “Enterprises value data” or “governance failures are costly.”  

---

## 7. Consistency

- Page titles must match MkDocs nav text exactly.  
- Link paths must mirror the nav tree. Example: `[Policy Registry](policy-registry/index.md)`.  
- Index pages introduce, subpages explain in detail. No duplication.  
- Always align terms with Glossary and Taxonomy.  

---

## 8. Evidence and Source Discipline

- Anchor claims to uploaded documentation. If it is not in the repo, do not assert it.  
- Link to specific user stories where relevant.  
- Never create modules, features, or behaviors that are not present in the documentation baseline.  
