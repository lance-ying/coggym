# Generation report guide

Keep the report beside `spec.py`, outside the compiled output tree so recompiling
cannot overwrite it. This is generation provenance, not a corpus paper-check report.
Use concise tables for repeated source mappings; retain previous human decisions
when revising an existing report.

## Identity and provenance

Record study/experiment IDs, exact paper experiment mapping and its confidence,
paper title, MEML checkout path/commit plus relevant uncommitted changes, compiler
version/validator pin from the card, seed, enumeration settings and their authority,
and agent/model/effort when known (otherwise “not recorded”).

For each paper/materials/code source record its URL or local path, revision or hash
where available, consulted pages/sections, and outcome: fetched, unavailable,
manual-requested, or not-design-relevant. Cite short exact quotes with locators
for extracted design claims; inference has no fabricated quotation. Distinguish
original author materials from previous CogGym reconstructions and user decisions.

## Design and content mapping

Summarize arms, factors, pool size, per-participant trials, queries/DVs, practice/
controls, ordering, and dependencies. Do not conflate these counts.

| Source item/claim and locator | Asset/trial/query/module ID or spec location | Transformation, if any | Evidence/decision status |
| --- | --- | --- | --- |

Include exact scale anchors and option semantics where relevant. Document all
content adaptations, missing assets, and user-supplied replacements. Do not copy
raw participant data or private correspondence into the report unnecessarily.

## Source check (D1–D10)

Use the current repository protocol's dimensions and statuses. Record confirmations
as well as mismatches, paper-silent fields, uncomparable features and not-applicable
dimensions. Each check ties source evidence to a concrete spec/input/output location.
Keep DRAFT expectations and unresolved interpretations distinguishable from settled
requirements. Include paper/instructions/flow contradictions even when compilation
passes. No source coverage means not assessed, not confirmed.

## Verification

| Check | Exact command or evidence | Result and limitations |
| --- | --- | --- |

Cover input validation, strict compile, media resolution/copying, the source-derived
assertions in `verify_design.py`, two-build byte reproducibility, lint, and rendering
where available. State the relative compiled output location. Record skipped and
failed checks explicitly. Do not claim semantic equivalence without an original
comparison and evidence; for a genuinely new experiment it is not applicable.

## Human review and decisions

Separate **pending questions** from **maintainer-supplied decisions**. Each pending
question should identify the conflicting/missing evidence, affected design, and
whether it blocks a faithful runnable artifact. Each actual decision records who
supplied it, when, rationale, and affected files; do not attribute agent defaults to
the maintainer. Record human review as pending unless it actually occurred.

Conclude with one artifact status: incomplete/blocked, compiled-awaiting-review,
or human-reviewed (name/date/scope). Pair it with separate source-check and
technical-check summaries; no single label should hide missing coverage.
