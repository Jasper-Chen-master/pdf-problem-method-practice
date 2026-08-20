---
name: pdf-problem-method-practice
description: Build and maintain a local practice bank from problem-set PDFs, classifying real questions by the methods evidenced in their supplied solutions. Works for any subject and is agent-first: use native PDF and multimodal capabilities when available; optional Python utilities improve batch consistency and validation.
metadata:
  short-description: Build a solution-grounded practice bank from PDFs, any subject.
---

# PDF Problem Method Practice

Turn a project's problem-set PDFs into a persistent practice bank organized by the method actually used in each supplied solution. The skill is subject-agnostic: it classifies by how a problem is solved - a technique, theorem, procedure, or approach - whether the subject is calculus, chemistry, language, history, coding, or anything else.

The default workflow is agent-first. If the agent can open PDFs and understand page images, users can start immediately without installing Python. Optional Python utilities improve batch extraction, reproducibility, and deterministic validation; they are not prerequisites.

## Agent Compatibility

This skill uses the standard `SKILL.md` frontmatter understood by most agent skill systems:

| Agent | Skills location |
|---|---|
| Codex CLI / desktop | `~/.codex/skills/pdf-problem-method-practice/` |
| Claude Code | `~/.claude/skills/pdf-problem-method-practice/` or `.claude/skills/` in the project |
| OpenCode | `~/.config/opencode/skill/pdf-problem-method-practice/` or `.opencode/skill/` in the project |
| Cursor | `.cursor/skills/` in the project |
| Any agent reading `AGENTS.md` | copy the folder into the repo and reference it from `AGENTS.md` |

The optional `agents/openai.yaml` file is a Codex-specific manifest. The scripts under `scripts/` are optional plain-Python utilities and do not define the minimum installation needed to use the skill.

## Operating Modes

Choose the highest-capability mode available in the current agent and environment:

1. **Agent-native mode (default).** Open the PDF directly, use its text layer when it is reliable, and use native visual understanding for pages whose layout, images, formulas, tables, scans, or handwriting carry meaning. Write the resulting records directly to `problem_bank/`.
2. **Hybrid mode.** Let the agent triage and interpret the document, while optionally running `scripts/extract_pdf_text.py` for fast page-level text extraction and `scripts/validate_bank.py` for deterministic checks.
3. **Utility mode.** Use the Python scripts when the agent cannot open the PDF, the corpus is too large for direct inspection, reproducible text extraction is required, or the user explicitly requests a command-line workflow.

Before processing, state which mode is being used. If native PDF or image understanding is unavailable, fall back to the optional utility mode or ask the user to provide extracted text. Do not pretend that plain text extraction preserves the original layout.

## Boundaries

- Treat source PDFs as read-only inputs.
- Store generated data under `problem_bank/` in the project, never beside this skill.
- Return only indexed questions for practice requests. Do not create new exercises to satisfy a requested count.
- Keep solution text hidden unless the user explicitly asks for it.
- Classify from the supplied solution when present. If no solution is supplied, label the result as provisional and record that limitation.
- Treat visual transcription as evidence with possible errors, not as ground truth. Preserve the source page and extraction provenance for visually reviewed records.
- Separate extraction from interpretation. Do not silently repair an unreadable formula, sign, subscript, table cell, or diagram from general knowledge.
- Use small page batches for visual review and recheck high-impact details against the original page before approval.
- Do not put full copyrighted source material into a public repository or external service without permission.

## Build Or Update A Bank

1. Find the user-designated PDFs and determine which operating mode is available. Do not require a Python setup step in agent-native mode.
2. Inspect the PDF page by page. Prefer native text for clean pages. Use visual understanding for empty or sparse text, scans, multi-column layouts, formulas, tables, diagrams, handwriting, captions, or suspicious reading order.
3. Detect question and solution boundaries from the original page layout. Pair separately supplied answer keys only when numbering and context agree; otherwise record the pairing as unresolved.
4. Create a record for each reliable question using [references/schemas.md](references/schemas.md). Preserve source path, page range, extraction mode, and visual-review status.
5. Reuse an active canonical method tag when it accurately describes the actual solution. Create a new tag only for a distinct, reusable solution method. Method tags are subject-neutral, such as `method_uv_substitution`, `method_redox_balancing`, `method_topic_sentence`, or `method_binary_search`.
6. Record secondary methods only when they are materially used. Put tactics such as handling edge cases, checking orientation, or applying symmetry in strategy tags.
7. Write a short evidence summary based on visible solution steps. Never store hidden reasoning traces. If a visual detail is uncertain, record the uncertainty instead of guessing.
8. Rebuild the method and strategy indexes. Run `scripts/validate_bank.py --bank problem_bank` when the optional Python utility is available; otherwise perform the same structural checks from the agent and report that no local validator was run.

For the visual-review decision rules and risk controls, read [references/agent-native-pdf.md](references/agent-native-pdf.md). For the detailed record shape, read [references/schemas.md](references/schemas.md). For classification decisions, read [references/classification-guide.md](references/classification-guide.md). For ambiguous extraction or classification, read [references/review-checklist.md](references/review-checklist.md).

## Native PDF And Multimodal Review

The agent's native multimodal capability can parse and inspect PDF pages, especially when the page image contains information that plain text extraction loses. Use it as the primary path when available, but keep source-page checks and uncertainty tracking.

Use visual review for scans, equations, symbols, diagrams, tables, handwriting, columns, captions, spatial grouping, or any page where text is empty, sparse, garbled, or in the wrong order. For clean text-only pages, native text extraction is usually cheaper, faster, easier to reproduce, and easier to search.

The main risks are OCR or transcription mistakes, hallucinated missing structure, misread signs and subscripts, context-window and latency costs, non-deterministic outputs, and privacy or copyright exposure when a hosted model receives course material. Mitigate them by reviewing only necessary pages, keeping page citations, preserving uncertainty, comparing important details against the original page, and never treating a model-generated reconstruction as a supplied solution without evidence.

## Retrieve Practice

Resolve the user's requested method against `aliases.json` and active method tags, load the relevant IDs from `indexes/methods.json`, then load those question records from `questions.jsonl`.

Present the question statement with its source file and page range. Mention when a record is provisional, visually transcribed, or has no supplied solution. If the requested method has no indexed records, say so and offer nearby existing methods; do not fabricate problems.

## Optional Local Utilities

Python is optional. When installed, `scripts/extract_pdf_text.py` provides fast page-level text extraction and `scripts/validate_bank.py` provides deterministic structural checks. These utilities can improve consistency and accuracy for large batches, but the absence of Python must never block agent-native PDF parsing.
