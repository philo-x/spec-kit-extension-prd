---
description: "Review PRD fidelity, completeness, and consistency against spec.md"
---

# Review PRD Fidelity and Consistency

Conduct an exhaustive consistency and fidelity audit of a generated Product Requirements Document (`prd.md`) against its canonical source of truth (`spec.md`).

## User Input

```text
$ARGUMENTS
```

The user input may specify a feature directory (e.g., `specs/001-work-report`), direct paths to `spec.md` and `prd.md`, or be empty (defaulting to active feature).

---

## Review Scope & Objectives

The review command ensures that the PRD compiler faithfully preserved the intent of the specification without introducing hallucinations, omitting requirements, or leaking technical implementation details.

It enforces the **8 Quality Gates** and the **Reader Test** defined in [`references/quality-checklist.md`](../references/quality-checklist.md):

1. **Completeness (完整性)**: Zero requirement or scenario dropped.
2. **Fidelity & No Hallucination (保真度与零幻觉)**: Zero invented features or scopes.
3. **No HOW Leakage (无实现细节泄漏)**: Zero database schemas, internal APIs, or tech stacks.
4. **Three-Tier Semantic Separation (三层语义分离)**: Features ≠ Business Rules ≠ Acceptance Criteria.
5. **Open Questions Preservation (待确认事项严格透传)**: All `[NEEDS CLARIFICATION]` preserved verbatim, never answered.
6. **Scope Alignment (范围一致性)**: In-Scope and Out-of-Scope match `spec.md`.
7. **Acceptance Criteria Fidelity (验收标准保真度)**: Gherkin ACs accurately reflect spec scenarios.
8. **Traceability Matrix Integrity (溯源完整性)**: 100% bidirectional traceability.

---

## Execution Steps

### Step 1: Locate and Ingest Documents

1. Identify the target feature directory:
   - If `$ARGUMENTS` provides a path or slug, resolve `FEATURE_DIR = specs/<slug>`.
   - If empty, auto-detect the active feature directory under `specs/`.
2. Locate documents:
   - Source: `<FEATURE_DIR>/spec.md`
   - Target: `<FEATURE_DIR>/product/prd.md`
3. Verify both files exist and are readable. If `prd.md` is missing, advise running `/speckit.prd.generate` first.

### Step 2: Extract Requirement Artifacts

Parse both documents into structured comparison lists:
- From `spec.md`:
  - Context & Background
  - Goals and Non-Goals
  - User Stories & Acceptance Scenarios
  - Requirements list (`FR-xxx`, business constraints, edge cases)
  - All `[NEEDS CLARIFICATION: ...]` items
- From `prd.md`:
  - Background & Problems (Section 1)
  - Goals, Non-Goals, Metrics (Section 2)
  - Personas & Scenarios (Section 3)
  - Scope boundaries (Section 4)
  - Functional Requirements (`FR-xx`, Section 5)
  - Business Rules (`BR-xx`, Section 6)
  - Data, Field, Permission & State Rules (Sections 7 & 8)
  - Edge Cases (`EX-xx`, Section 9)
  - Acceptance Criteria (`AC-xx`, Section 10)
  - Open Questions (`OQ-xx`, Section 12)
  - Traceability Matrix (Section 13)

### Step 3: Run the 8-Dimension Audit

Evaluate each gate systematically:

#### Gate 1: Completeness
- Verify that every `FR-xxx`, User Story, and Scenario in `spec.md` has a corresponding item in `prd.md`.
- Flag any missing or dropped requirement.

#### Gate 2: Fidelity & Zero Hallucination
- Check whether `prd.md` introduced any features, capabilities, or scopes not mentioned or implied by `spec.md`.
- Flag any unauthorized scope additions.

#### Gate 3: No HOW Leakage
- Scan `prd.md` for technical keywords (e.g. `SQL`, `table`, `column`, `POST /api`, `Redis`, `Spring`, `React`, `foreign key`, `HTTP 400`, `indexedDB`, etc.).
- Flag any instance where technical implementation replaces or pollutes business requirement descriptions.

#### Gate 4: Three-Tier Separation
- Verify that Section 5 only contains functional user capabilities (WHAT/WHY).
- Verify that invariants, time limits, and calculation formulas are isolated in Section 6 (`BR-xx`).
- Verify that Section 10 contains behavior-driven Given-When-Then criteria (`AC-xx`).
- Flag any business rule wrongly embedded into feature paragraphs.

#### Gate 5: Open Questions Preservation
- Match every `[NEEDS CLARIFICATION: ...]` in `spec.md` against Section 12 of `prd.md`.
- Verify the wording is preserved verbatim.
- **Fail immediately** if the model attempted to answer or fabricate an unconfirmed business decision.

#### Gate 6: Scope Alignment
- Verify that `In Scope` and `Out of Scope` in Section 4 precisely mirror `Goals` and `Non-Goals` from `spec.md`.

#### Gate 7: Acceptance Criteria Fidelity
- Check that all Given-When-Then clauses in Section 10 are logically consistent with `spec.md` acceptance scenarios.
- Verify that expected outcomes match specification expectations.

#### Gate 8: Traceability Matrix Integrity
- Verify that Section 13 contains a valid, unbroken mapping between every PRD item (`FR-xx`, `BR-xx`, `AC-xx`, `OQ-xx`) and its origin in `spec.md`.

### Step 4: Perform Reader Test (Clarity & Readability)

Evaluate user empathy and stakeholder experience:
- Is the narrative clear and actionable for non-technical stakeholders?
- Can QA immediately adopt the Gherkin scenarios for test plans?
- Are tables and lists formatted cleanly without visual clutter?

### Step 5: Generate Review Report

Format the findings according to the report specification in [`references/quality-checklist.md`](../references/quality-checklist.md):

1. **Executive Summary Table** showing Status (`PASS` / `WARN` / `FAIL`), issue counts, and summary notes for all 8 gates.
2. **Detailed Findings**:
   - Location (Section / Line)
   - Violation type and severity
   - Concrete, actionable recommendation to fix the gap.
3. **Final Verdict**:
   - **APPROVED**: All 8 gates passed. Ready for stakeholder sign-off and engineering planning (`/speckit.plan`).
   - **WARNINGS**: Minor formatting or non-critical issues (e.g., phrasing tweaks). Can proceed with caution.
   - **REJECTED**: Critical failures (hallucination, missing requirements, HOW leakage, or answered clarifications). Must be re-generated.

### Step 6: Output & Persist

1. Print the executive summary and findings to the user.
2. If configured (or if `--save` is requested), write the full report to `<FEATURE_DIR>/product/review-report.md`.
