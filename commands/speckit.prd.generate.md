---
description: "Generate a product-manager-friendly PRD from the active feature spec.md using semantic requirement analysis"
---

# Compile PRD from Feature Specification

Compile an engineering-focused feature specification (`spec.md`) into a high-quality, stakeholder-friendly Product Requirements Document (`prd.md`) using semantic requirement analysis and the intermediate product model.

## User Input

```text
$ARGUMENTS
```

The user input may specify a feature directory name, a direct path to `spec.md`, or be empty (defaulting to the current active feature).

---

## Core Philosophy & Compilation Rules

Before proceeding, internalize and enforce the core principles defined in [`references/prd-principles.md`](../references/prd-principles.md):

1. **`spec.md` is the Canonical Single Source of Truth**:
   - The PRD is a derived, read-only projection (`spec.md -> prd.md`).
   - **Strictly unidirectional**: Never modify `spec.md` from the PRD.
2. **WHAT and WHY Only — Zero HOW Leakage**:
   - Describe user goals, business outcomes, business rules, and constraints.
   - Strictly strip out technical implementation details (internal table schemas, SQL statements, HTTP endpoints, backend framework classes, technical libraries).
3. **Semantic Requirement Compilation (Not Shallow Summarization)**:
   - Apply the classification heuristics in [`references/requirement-classification.md`](../references/requirement-classification.md).
   - Enforce the **Three-Tier Separation**:
     - **Functional Capabilities** (Section 5)
     - **Business Rules** (Section 6, detailed in [`references/business-rules.md`](../references/business-rules.md))
     - **Acceptance Criteria** (Section 10, detailed in [`references/acceptance-criteria.md`](../references/acceptance-criteria.md))
4. **Zero Hallucination & Verbatim Clarification Pass-Through**:
   - Do not invent business features not grounded in `spec.md`.
   - Any `[NEEDS CLARIFICATION: ...]` in `spec.md` **MUST** be surfaced verbatim in Section 12. Never attempt to guess or answer it.
5. **Bidirectional Traceability**:
   - Every generated item must trace back to its origin in `spec.md` via Section 13.

---

## Execution Pipeline

### Phase 1: Context & Feature Resolution

1. **Resolve Feature Path**:
   - If `$ARGUMENTS` contains a path (e.g. `specs/001-work-report/spec.md`), use it.
   - If `$ARGUMENTS` contains a feature slug (e.g. `001-work-report`), look for `specs/001-work-report/spec.md`.
   - If empty, detect the active feature under `specs/` (e.g., sort by modification time or inspect current git branch name).
   - Set `FEATURE_DIR = specs/<feature-slug>` and `SPEC_FILE = <FEATURE_DIR>/spec.md`.
2. **Read Inputs**:
   - Read `SPEC_FILE`. If missing, notify the user that a valid `spec.md` is required (suggest running `/speckit.specify` first).
   - Read configuration from `.specify/extensions/prd/prd-config.yml` if present (or use default configuration).
   - Ensure target output directory `<FEATURE_DIR>/product/` exists.

### Phase 2: Requirement Analysis & Semantic Classification

Inspect all statements, requirements, and user stories in `SPEC_FILE` and classify each item using [`references/requirement-classification.md`](../references/requirement-classification.md):

- **Capabilities & User Goals** -> Map to **Section 5: 功能需求 (Functional Requirements)**
- **Invariants, Upper/Lower Limits, Calculation Formulas, Expirations** -> Map to **Section 6: 业务规则 (Business Rules)**
- **Field Validations, Format Constraints, Enums** -> Map to **Section 7: 数据与字段规则 (Data & Field Rules)**
- **Role Permissions, Data Isolation, State Machines** -> Map to **Section 8: 权限与状态规则 (Permission & State Rules)**
- **Edge Conditions, Failures, Race Conditions** -> Map to **Section 9: 异常与边界场景 (Edge Cases)**
- **Acceptance Scenarios, Test Conditions** -> Transform into Gherkin format in **Section 10: 验收标准 (Acceptance Criteria)**
- **Unresolved Markers `[NEEDS CLARIFICATION]`** -> Map to **Section 12: 待确认事项 (Open Questions)**

### Phase 3: Intermediate Product Requirement Model Construction

Construct an internal product semantic model before rendering:

```yaml
product:
  metadata:
    feature_name: string
    source_spec: "spec.md"
    date: YYYY-MM-DD
  problem_and_context:
    background: string
    current_problems: string
    why_now: string
  objectives:
    goals: [string]
    non_goals: [string]
    success_metrics: [{id, name, baseline, target, method}]
  users_and_scenarios:
    personas: [{id, name, role, pain_point}]
    scenarios: [{title, precondition, journey, outcome}]
  scope:
    in_scope: [string]
    out_of_scope: [string]
  features:
    - id: "FR-01"
      module: string
      name: string
      user_goal: string
      description: string
      capabilities: [string]
      priority: "P0" | "P1" | "P2"
      source_ref: "spec.md#FR-xxx"
  business_rules:
    - id: "BR-01"
      name: string
      definition: string
      scope: string
      violation_behavior: string
      source_ref: string
  data_and_fields:
    fields: [{entity, field, description, required, format, default, source_ref}]
  permissions_and_state:
    permission_matrix: [...]
    state_transitions: [...]
  edge_cases:
    - id: "EX-01"
      condition: string
      handling: string
      source_ref: string
  acceptance_criteria:
    - id: "AC-01"
      name: string
      gherkin: "Given ... When ... Then ..."
      linked_fr: ["FR-01"]
      linked_br: ["BR-01"]
      source_ref: string
  risks_and_dependencies:
    dependencies: [string]
    risks: [{risk, mitigation}]
    constraints: [string]
  open_questions:
    - id: "OQ-01"
      verbatim_question: string
      impact: string
      status: "Pending"
      source_ref: string
```

### Phase 4: Render PRD Document

1. Load the official PRD template from [`templates/prd-template.md`](../templates/prd-template.md).
2. Populate each template section with the structured data from the Intermediate Product Model.
3. Apply conditional section rules:
   - **Section 7 (数据与字段规则)**: Only render if `spec.md` defines specific fields, formats, or calculations.
   - **Section 8 (权限与状态规则)**: Only render if `spec.md` specifies role-based controls or lifecycle transitions.
4. Populate **Section 13 (需求追溯矩阵 / Requirement Traceability Matrix)**, mapping every generated item (`FR-xx`, `BR-xx`, `AC-xx`, `OQ-xx`) back to the originating line or requirement ID in `spec.md`.

### Phase 5: Self-Fidelity QA & Reader Test

Before writing the file, audit the draft against [`references/quality-checklist.md`](../references/quality-checklist.md):

- [ ] **Completeness**: Are any requirements from `spec.md` omitted?
- [ ] **No Hallucinations**: Are all features strictly backed by `spec.md`?
- [ ] **No HOW Leakage**: Are technical implementation details stripped out?
- [ ] **Three-Tier Separation**: Are functional capabilities, business rules, and acceptance criteria in distinct sections?
- [ ] **Unresolved Items Preserved**: Did any `[NEEDS CLARIFICATION]` get answered by mistake? (Must remain unanswered).
- [ ] **Reader Test**: Is the document clear, concise, and easy for PMs and stakeholders to review?

### Phase 6: Write Output & Report

1. Write the compiled markdown to `<FEATURE_DIR>/product/prd.md`.
2. Report the result to the user with a concise summary:
   - File path: `specs/<feature-slug>/product/prd.md`
   - Compiled statistics:
     - 🎯 Goals & Non-Goals
     - 🧩 Functional Capabilities (`FR-xx`)
     - 📜 Business Rules (`BR-xx`)
     - 🧪 Acceptance Criteria (`AC-xx`)
     - ❓ Open Questions (`[NEEDS CLARIFICATION]`)
   - Next recommended action: Review with `/speckit.prd.review` or proceed to engineering plan with `/speckit.plan`.
