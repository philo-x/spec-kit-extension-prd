# Changelog

All notable changes to the `spec-kit-prd` extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-09-19

### Added
- **Extension Manifest (`extension.yml`)**: Spec Kit Extension Schema 1.0 compliant manifest with `prd` extension ID.
- **Commands**:
  - `speckit.prd.generate` (alias: `speckit.prd.gen`): Compile `spec.md` into `specs/<feature>/product/prd.md` using semantic requirement analysis.
  - `speckit.prd.review`: 8-Dimension consistency and fidelity audit tool against canonical `spec.md`.
- **Templates**:
  - `templates/prd-template.md`: 13-section enterprise & SaaS PRD template featuring Three-Tier Separation (Functional Capabilities, Business Rules, Acceptance Criteria).
- **Progressive Disclosure References**:
  - `references/prd-principles.md`: Single Source of Truth philosophy, unidirectional compiler model, zero HOW leakage.
  - `references/requirement-classification.md`: Semantic classification taxonomy and decision tree.
  - `references/business-rules.md`: Business rule modeling, UI decoupling, and standard phrasing.
  - `references/acceptance-criteria.md`: Gherkin (Given-When-Then) criteria and coverage matrices.
  - `references/quality-checklist.md`: 8-Dimension Quality Gate protocol and Anthropic doc-coauthoring Reader Test.
- **Documentation**:
  - `docs/architecture.md`: Visual architecture and intermediate product semantic model.
  - `docs/user-guide.md`: Installation, configuration, commands, and best practices.
- **Examples**:
  - Complete real-world enterprise work report example (`examples/work-report/`): `spec.md`, compiled `prd.md`, and `review-report.md`.
- **Validation**:
  - `scripts/validate_extension.py`: Automated manifest and asset validation script.
