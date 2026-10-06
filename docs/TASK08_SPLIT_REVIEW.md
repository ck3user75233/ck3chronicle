# Task 08 split — advisor review

2026-10-02. Advisory change account and recommendations, not implementation
instructions. The owner's Downloads versions of `TASK08A_PROMPT.md` and
`TASK08B_PROMPT.md` were the editing baseline; those original files are untouched.

## Changes made within the requested scope

- [08A.1](TASK08A_1_PROMPT.md) receives structured diagnostic/template filters,
  exact identity, query/results, rollups, Run chronology, recent windows,
  recurrence/notability and the syntax-selector interface.
- [08A.2](TASK08A_2_PROMPT.md) receives recorded-playset lookup, source-reference
  extraction, member/root/path/content search, candidates, excerpts, and the
  integration of source-dependent filters with 08A.1's query engine. This makes
  the dependency one-way: 08A.1, then 08A.2, then 08B.
- [08B](TASK08B_PROMPT.md) receives both split prompts/handoffs and starts only
  after both deliveries and query/source integration are complete. It also exposes
  explicit source roots and distinguishes unavailable optional context from an
  inability to evaluate a required source filter.
- Final search guidance treats high-performance disk search as an initial
  requirement, with ripgrep as the default bulk content-search engine invoked
  from Python. It requires a reused in-memory path inventory, batched searches,
  early scope filters, bounded streaming, explicit ripgrep coverage settings
  and representative large-playset timings without an arbitrary threshold.
  Standard-library helpers and wcmatch support path/filter operations. Dependency,
  license and Windows installation/distribution requirements belong in the
  implementation handoff. No packages or tools were installed.
- 08A.1 explicitly filters by one or more stored matched-template references,
  combined with OR. The operation is called searching diagnostic records;
  template filtering does not search model files or repeat classification.
- The old combined 08A filename now points to its replacements. Current planning
  pointers identify the split; historical wording is not silently restored over
  the owner's updated policies.

Chronology retains the original source-log modification timestamp ordering.
Duplicate-ingestion handling belongs to the pipeline. Source
search now follows the owner's explicit clarification: no mandatory playset
restriction, file-level content conditions, explicit source-filter evaluation
errors and the specified ripgrep wrapper behavior. No new link-resolution policy
or per-file observation timestamps were added. Syntax/severity presentation
remains with 08B; no new severity rules were added.

## Template clarification resolved

The earlier recommendation to define another searchable template display is
withdrawn. Records already retain their matched template reference. Filtering
by selected templates uses those references directly with OR; optional template
text conditions use stored literals/slots. No new template representation or
model-file lookup is required. Searching diagnostic records includes their
recorded content and bound values. This clarification is reflected in 08A.1.

## Recommendations for owner review — NOT applied

1. **Retire the missing-syntax-handoff conditional.** Both supplied prompts retain
   wording for a handoff that might be unavailable, while the research is now
   delivered and 08B links it. Recommend replacing that conditional with direct
   receipt of the verified selectors. Preserve the research's package scope and
   evidence limits; severity presentation still belongs to 08B.

This remaining recommendation has not been inserted into the executable prompts.
It does not authorize additional implementation or impose new acceptance gates.

## Verification of this document change

Compared the supplied drafts with the repository copies, partitioned their
sections, and checked the new references and preservation of policy text.
Reviewed official Python, wcmatch and ripgrep documentation for library guidance.
No runtime tests, production reads/ingestion, service changes, installs, commits
or pushes were performed.
