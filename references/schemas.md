# Data Schemas

Use UTF-8 JSON. Each JSONL file contains exactly one JSON object per line. All generated files live under the target project's `problem_bank/` directory. The schemas are subject-agnostic.

## `questions.jsonl`

```json
{
  "schema_version": 1,
  "question_id": "q_ab12cd34",
  "source_file": "problems/homework01.pdf",
  "question_number": "5",
  "page_start": 3,
  "page_end": 4,
  "solution_page_start": 11,
  "solution_page_end": 12,
  "question_text": "...",
  "solution_text": "...",
  "content_hash": "...",
  "status": "classified",
  "active": true,
  "provisional": false,
  "primary_method_id": "method_stokes_theorem",
  "secondary_method_ids": [],
  "strategy_ids": ["strategy_replace_surface"],
  "classification_confidence": 0.93,
  "evidence_summary": "The supplied solution replaces the surface and applies Stokes' theorem.",
  "extraction": {
    "mode": "agent_native_visual",
    "pages_reviewed": [3, 4],
    "signals": ["formula", "diagram"],
    "verified_against_source": true,
    "notes": "The text layer lost the surface labels; the page image was checked."
  }
}
```

`solution_text` may be empty only when `provisional` is true. `question_id` must be unique and stable for the source path plus question number. `primary_method_id`, `secondary_method_ids`, and `strategy_ids` reference tags from the tag files below.

The optional `extraction` object records provenance, not model reasoning. Allowed `mode` values are `agent_native_text`, `agent_native_visual`, `python_pdfplumber`, and `hybrid`. Use `agent_native_visual` when the agent read the page image or performed native visual OCR. Set `verified_against_source` to false or omit it when an important detail remains unchecked.

## Optional `extraction/source_pages.jsonl`

When a page-level extraction file is created, each record may include deterministic or agent-reported provenance:

```json
{
  "schema_version": 1,
  "source_file": "problems/homework01.pdf",
  "source_sha256": "...",
  "page_number": 3,
  "text": "...",
  "extraction_mode": "agent_native_text",
  "visual_review_recommended": false,
  "visual_review_reasons": []
}
```

Agent-native workflows may write question records directly without creating this intermediate file.

## Tag Files

`method_tags.json` and `strategy_tags.json` use the same shape:

```json
{
  "schema_version": 1,
  "tags": [
    {
      "id": "method_stokes_theorem",
      "canonical_name": "Stokes' Theorem",
      "normalized_name": "stokes theorem",
      "description": "Relates circulation around a boundary to a surface integral of curl.",
      "aliases": ["Stokes"],
      "usage_count": 5,
      "status": "active"
    }
  ]
}
```

## Indexes And Aliases

`indexes/methods.json` and `indexes/strategies.json` map active tag IDs to question IDs:

```json
{"schema_version": 1, "methods": {"method_stokes_theorem": ["q_ab12cd34"]}}
```

`aliases.json` maps normalized user phrases to active method or strategy tags:

```json
{"schema_version": 1, "aliases": {"stokes": "method_stokes_theorem"}}
```

## Review History

`classification_runs.jsonl` records visible classification metadata, not hidden reasoning:

```json
{
  "schema_version": 1,
  "question_id": "q_ab12cd34",
  "timestamp": "2026-01-01T00:00:00Z",
  "review_result": {"approved": true},
  "final_method_ids": ["method_stokes_theorem"],
  "final_strategy_ids": [],
  "summary": "Solution explicitly uses Stokes' theorem."
}
```
