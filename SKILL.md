---
name: pdf-problem-method-practice
description: Build and maintain a local practice bank from problem-set PDFs, classifying real questions by the methods evidenced in their supplied solutions. Works for any subject — math, physics, chemistry, English grammar, history, coding, and more. Use for PDF problem extraction, method-based study retrieval, or rebuilding a local problem bank; do not use to invent exercises.
metadata:
  short-description: Build a solution-grounded practice bank from PDFs, any subject.
---

# PDF Problem Method Practice

Turn a project's problem-set PDFs into a persistent practice bank organized by the method actually used in each supplied solution. The skill is subject-agnostic: it classifies by *how* a problem is solved (a technique, theorem, procedure, or approach), whether the subject is calculus, organic chemistry, English grammar, or anything else.

## Agent Compatibility

This skill uses the standard `SKILL.md` frontmatter (`name` + `description`) understood by most agent skills systems. Install it into whichever agent you use:

| Agent | Skills location |
|---|---|
| Codex CLI / desktop | `~/.codex/skills/pdf-problem-method-practice/` |
| Claude Code | `~/.claude/skills/pdf-problem-method-practice/` or `.claude/skills/` in the project |
| OpenCode | `~/.config/opencode/skill/pdf-problem-method-practice/` or `.opencode/skill/` in the project |
| Cursor | `.cursor/skills/pdf-problem-method-practice/` in the project |
| Any agent reading `AGENTS.md` | copy the folder into the repo and reference it from `AGENTS.md` |

The optional `agents/openai.yaml` file is a Codex-specific agent manifest; other agents ignore it. The scripts under `scripts/` are plain Python and run on any platform.

## Boundaries

- Treat source PDFs as read-only inputs.
- Store generated data under `problem_bank/` in the project, never beside this skill.
- Return only indexed questions for practice requests. Do not create new exercises to satisfy a requested count.
- Keep solution text hidden unless the user explicitly asks for it.
- Classify from the supplied solution when present. If no solution is supplied, label the result as provisional and record that limitation.
- Do not put full copyrighted source material into a public repository or external service without permission.

## Build Or Update A Bank

1. Find the user-designated PDFs. For a new project, use `scripts/extract_pdf_text.py` to create page-level extraction records under `problem_bank/extraction/`.
2. Detect question and solution boundaries from the source layout. Pair separately supplied answer keys only when numbering and context agree; otherwise record the pairing as unresolved.
3. Create a record for each reliable question using [references/schemas.md](references/schemas.md). Preserve source path and page range.
4. Reuse an active canonical method tag when it accurately describes the actual solution. Create a new tag only for a distinct, reusable solution method. Method tags are subject-neutral: e.g. `method_uv_substitution` (math), `method_redox_balancing` (chemistry), `method_topic_sentence` (writing), `method_binary_search` (coding).
5. Record secondary methods only when they are materially used. Put tactics such as handling edge cases, checking orientation, or applying symmetry in strategy tags.
6. Write a short evidence summary based on the visible solution steps. Never store hidden reasoning traces.
7. Rebuild the method and strategy indexes, then run `scripts/validate_bank.py --bank problem_bank`.

For the detailed record shape, read [references/schemas.md](references/schemas.md). For classification decisions, read [references/classification-guide.md](references/classification-guide.md). For ambiguous extraction or classification, read [references/review-checklist.md](references/review-checklist.md).

## Retrieve Practice

Resolve the user's requested method against `aliases.json` and active method tags, load the relevant IDs from `indexes/methods.json`, then load those question records from `questions.jsonl`.

Present the question statement with its source file and page range. Mention when a record is provisional or has no supplied solution. If the requested method has no indexed records, say so and offer nearby existing methods; do not fabricate problems.

