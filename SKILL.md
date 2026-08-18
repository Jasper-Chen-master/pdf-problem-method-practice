---
name: pdf-problem-method-practice
description: Build and maintain a local practice bank from problem-set PDFs, classifying real questions by methods evidenced in supplied solutions. Use for PDF problem extraction, method-based study retrieval, or rebuilding a local problem bank; do not use to invent exercises.
metadata:
  short-description: Build a solution-grounded practice bank from PDFs.
---

# PDF Problem Method Practice

Turn a project's problem-set PDFs into a persistent practice bank organized by the method actually used in each supplied solution.

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
4. Reuse an active canonical method tag when it accurately describes the actual solution. Create a new tag only for a distinct, reusable solution method.
5. Record secondary methods only when they are materially used. Put tactics such as orientation handling, symmetry, or closing a surface in strategy tags.
6. Write a short evidence summary based on the visible solution steps. Never store hidden reasoning traces.
7. Rebuild the method and strategy indexes, then run `scripts/validate_bank.py --bank problem_bank`.

For the detailed record shape, read [references/schemas.md](references/schemas.md). For classification decisions, read [references/classification-guide.md](references/classification-guide.md). For ambiguous extraction or classification, read [references/review-checklist.md](references/review-checklist.md).

## Retrieve Practice

Resolve the user's requested method against `aliases.json` and active method tags, load the relevant IDs from `indexes/methods.json`, then load those question records from `questions.jsonl`.

Present the question statement with its source file and page range. Mention when a record is provisional or has no supplied solution. If the requested method has no indexed records, say so and offer nearby existing methods; do not fabricate problems.

