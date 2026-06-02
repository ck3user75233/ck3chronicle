# Agent Prompt 05: Normalization and Categorization

Implement normalization and categorization helpers.

Normalization should mask:

- line numbers
- near-line references
- memory addresses
- obvious runtime IDs
- volatile internal IDs
- generated argument hashes where appropriate

Do not blindly mask every standalone number.

Categories:

- Syntax / Structural
- Scope Mismatch
- Missing Reference
- Script Execution
- Localization
- Database Conflict
- Asset / Graphics
- GUI / Interface
- Mod Descriptor / Metadata
- Crash Evidence
- Engine / System
- Unclassified

Severity values:

- Fatal
- High
- Medium
- Low
- Noise
- Unknown

Confidence values:

- High
- Medium
- Low

Acceptance criteria:

- Fixtures prove repeated line-number variants cluster together.
- Distinct event/object IDs are not accidentally collapsed unless explicitly intended.
- Every issue has category, severity, and confidence.
- Tests cover all initial categories.
- Localization and asset noise can be classified separately from script execution errors.
