---
name: generate-meml
description: Generate a source-grounded Meta-EML (MEML) experiment from a research paper and original materials using cog-gym-meml; author the input libraries and Python design, compile EML, and prepare evidence and human-review checks. Use for new MEML experiment creation, not merely lifting existing EML or running model evaluations.
---

# Generate MEML

Turn a source experiment into a reviewable MEML specification and compiled EML.
Keep three claims separate: **schema-valid**, **checked against sources**, and
**human-approved**. Compilation alone establishes only the first.

## Locate the checkout and scope

- Use the user's selected `cog-gym-meml` checkout. If none is supplied, look in
  the current workspace and sibling repositories. Verify any candidate rather
  than assuming it exists or is current. If no checkout is available, ask the
  user to provide or clone [kasmith/cog-gym-meml](https://github.com/kasmith/cog-gym-meml).
  Read its local agent instructions and record HEAD and working-tree status. Do
  not pull or switch branches implicitly.
- Read `docs/workbook/10-from-paper-to-spec.md`, `docs/input-formats.md`, and
  `docs/workbook/01-a-minimal-experiment.md` in that checkout. These are the
  maintained authoring references; do not reproduce the compiler's schemas here.
  If the checkout is missing, ask for its location or access; do not invent an API.
- Resolve the paper, original materials, target paper experiment(s), and output
  location from the request. Map paper experiment labels explicitly to intended
  `Study/exp` identifiers; `exp1` in a corpus need not be the paper's Experiment 1.
  Ask only when the choice cannot be established from evidence and context.
- Default new artifacts to `meml-generated/<Study>__<exp>/` inside the current
  writable workspace, outside the corpus and existing golden/lift directories.
  Confirm the resolved destination does not overlap source material. Preserve
  existing user edits: read before patching, do not replace an existing directory,
  and compile only into a separate derived-output subdirectory.
- Existing EML migration is a different workflow. If that is the actual request,
  read `docs/migration.md` and the repository's `check-study` skill instead.
  Existing EML may be a useful cross-reference, but is not authoritative evidence
  that the paper's experiment has been reconstructed faithfully.

Generating a spec does not authorize modifying datasets, paper text, model results,
compiler behavior, goldens, or reviewer rulings. Do not commit, publish, stage PRs,
contact authors, or run model experiments unless separately requested.

## 1. Establish source evidence before choosing a design

Read the target experiment's methods and relevant supplements. Follow the paper's
materials/code links and any source pointers in an existing study README, even if
the referenced files are absent locally. Original experiment scripts and Qualtrics
QSF exports can settle details omitted from the paper. Verify paper title/authors
and experiment identity rather than trusting a filename. Inspect rendered figures
when layout, colors, spatial relationships, or figure-carried text affect the task.

Create `generation-report.md` using [the report guide](references/generation-report.md).
Record source locations/versions, local hashes where applicable, short exact evidence
quotes with locators, and source-to-input mappings. Clearly mark inferences and
unavailable evidence; never invent quotes, stimuli, data, or original wording.

Before implementation, establish:

- Between-participant arms versus within-participant factors, and their crossing.
- Total stimulus pool, trials per participant, questions per trial, and practice/
  control counts separately. A dependent variable is not necessarily a trial.
- Blocks, assignment, ordering, counterbalancing, subsets, and cross-trial dependencies.
- Exact instructions, cover story, stimuli, response types, option order, native
  ranges, anchors, units, default values, and optional responses such as “I don't know.”
- Practice, quizzes, attention checks, feedback, and presentation requirements.

When sources conflict or a missing detail changes the design, retain both readings
and ask for a human decision. Continue independent work, but do not compile a guessed
choice into an apparently complete reconstruction. If essential materials remain
unavailable after checking accessible sources, hand off a blocked/incomplete draft
with precise missing inputs. A paper's silence is not permission to add a quiz,
randomization, a response scale, or new task instructions.

## 2. Author the four inputs, then the design

Use `inputs/assets_manifest.json`, `inputs/query_library.json`,
`inputs/instruction_library.json`, and `inputs/citation.json`, following the current
input contracts. Keep bibliographic information consistent across a study's experiments.

- Preserve source text and media. If source files need mechanical transformation,
  include a deterministic `make_inputs.py` and record the original-to-generated
  mapping. Document reconstruction or adaptation explicitly; never pass invented
  assets off as originals. Missing media are blockers, not invitations to substitute.
- Annotate stimuli with source-supported factor levels. Keep stable asset/trial IDs
  and query tags; tags are downstream human-data join keys. Record mappings rather
  than assuming row position or filename numbering identifies a stimulus.
- Preserve native response semantics. Do not normalize sliders, collapse distinct
  constructs, convert ratings to accuracy, or create normative answer keys from a
  human majority response. Retain genuine source answer keys and documented roles.
  Read the current API/decisions for role and answer rules: older input-format prose
  may predate changes allowing answer keys without a role.
- Retain source practice and controls in the experiment, with supported roles.
  Scoring eligibility belongs to a separate evaluation layer. Do not apply a model
  evaluation's 100-trial cap to the reconstructed source design.

Build `spec.py` with a module-level `Experiment` named `exp`; the CLI loads that
object. Use paths relative to `__file__`, register the libraries with `exp.use`,
and use the current public API. Do not hand-author derived `responseType`,
`stimuli_count`, or sequence IDs. Avoid import-time writes or network calls.

Read `docs/api.md` and the relevant workbook chapter(s) for the actual design:
2–3 for stimuli/factors and manipulation locus; 4 for between/within assignment;
5–6 for ordering/subsets; 7 for multipart trials; 8 for instructions/practice;
9 for constraints; 11 for matched variants. Treat examples as API demonstrations,
not evidence about this paper.

Prefer a declarative plan that expresses the source's design. Do not pool
between-participant arms, shuffle dependent phases independently, or force an
adaptive experiment into independent trials. Before proposing an unsupported
feature or workaround, consult `docs/deferred.md` and `docs/decisions.md`.
`ExplicitSequences` requires a documented source/maintainer-licensed ordering;
it is not a way to conceal unknown design semantics. Do not weaken validation or
implement compiler features just to make a reconstruction compile.

Record the seed as a reproducibility setting, not a paper fact. Follow established
maintainer choices for enumeration and read `docs/choosing-n-sequences.md` for
randomized designs. A library default may support a clearly provisional draft,
but is not human approval. Do not choose unlicensed statistical settings silently
or report enumerated randomization itself as a design defect.

## 3. Compile and verify

Use a Python environment with this checkout's MEML dependencies and Python version
from `pyproject.toml`. Prefer its existing `.venv/bin/python` if usable; otherwise
locate a suitable environment. Do not assume the local checkout has a venv or
modify a shared environment without authority. The CLI executes Python in the spec:
inspect externally supplied specs before running them.

From the verified repository root, with `meml_python` set to that interpreter and
`generation_dir` set to the resolved absolute artifact directory:

```bash
PYTHONPATH=src "$meml_python" -m meml.cli validate-inputs "$generation_dir"/inputs/*.json
PYTHONPATH=src "$meml_python" -m meml.cli compile "$generation_dir/spec.py" --out "$generation_dir/compiled" --validate strict
```

The output is `compiled/<Study>/<exp>/`, not directly `compiled/`. A complete
deliverable includes resolved/copied media: do not use `--no-assets` as a passing
asset check. An explicitly limited no-assets diagnostic must remain labeled partial.

Read the emitted `card.md`, `config.json`, `trial.jsonl`, and `instruction.jsonl`.
Create a small experiment-specific `verify_design.py` with source-derived assertions:
condition membership, per-sequence trial counts, block boundaries, subset constraints,
ID/tag uniqueness, reachable trials, instruction/practice placement, response ranges,
and required media references. Check all emitted sequences, not only the first.
Account for practice references before declaring a trial unreachable. Do not derive
expected counts solely from the same spec code being tested.

Compile twice into fresh temporary output roots with the same inputs and seed;
compare the emitted relative file inventories and bytes (for example, `diff -r`).
Keep this separate from science checks: deterministic wrong output still passes.
Run the new assertions and lint authored Python using the repository's tooling
when available. If shared code is changed under a separate authorized request,
run its regression tests too. Record commands, results, warnings and unavailable
checks; a failed or skipped check is never “passed.”

Where a renderer is available, inspect representative trials from every distinct
condition/response format, plus instructions and practice. Record what was actually
rendered; a readable card is not proof of the participant-facing presentation.

## 4. Source check and human handoff

Read `docs/paper-check/protocol.md` and `docs/paper-check/expectations.md` fully.
Apply their D1–D10 comparison dimensions, source-evidence rules, confirmation and
coverage reporting to the generated artifact. Compare paper ↔ instructions ↔ compiled
flow. Keep proposed dispositions provisional and human rulings unfilled until supplied.
This is a **generation self-check**, not an independent audit or a completed human check.

The current repository `check-meml` skill accepts only goldens and verified staged
lifts. Do not invoke it with an invented `root=generated`, manufacture `golden.json`
or waivers, or claim corpus equivalence for a new experiment. If that skill later
supports new generation, inspect its actual contract before using that mode.
Until then, keep this self-check in `generation-report.md` and hand the sources,
specification, assertions, and compiled card to the human reviewer.

Deliver links to the spec, compiled experiment/card, and report. State the evidence
coverage, technical checks actually passed, unresolved design decisions, and human
review status. Offer a rendered experiment for author review when available; do not
send it externally without authorization. Stop at this reviewable artifact unless
the user has requested an additional action.
