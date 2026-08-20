# Agent-Native PDF Processing

This skill is designed to work without a Python environment. When the current agent can open PDFs and inspect page images, use that capability first. Python is an optional enhancement for larger or more reproducible workflows.

## Recommended decision

| Situation | Default action |
|---|---|
| The agent can read the PDF and the text layer is clean | Use native PDF text understanding and cite page numbers. |
| The page is scanned, image-heavy, formula-heavy, tabular, multi-column, handwritten, or visually arranged | Use native visual understanding on the specific page or a small page batch. |
| The text layer is empty, sparse, garbled, or in the wrong order | Use visual review, then compare the result with the page image. |
| The corpus is very large or needs repeatable batch extraction | Optionally run the Python extractor, then use the agent for layout-sensitive pages and classification. |
| The agent cannot open the PDF | Ask for extracted text or use the optional Python utility if the user can provide an environment. |

## Agent-native workflow

1. Confirm that the agent can access the PDF and identify the relevant file names.
2. Start with page-level text or native document retrieval when available.
3. Triage pages that need visual review. Do not send an entire large corpus through visual reasoning if only a few pages are difficult.
4. Inspect difficult pages in small batches. Preserve page numbers and source file names in every note.
5. Transcribe only the information needed for the question or solution record. Do not silently fill gaps from domain knowledge.
6. Recheck equations, minus signs, exponents, subscripts, units, table cells, diagram labels, and question numbers against the original page.
7. Mark the record as visually reviewed and record the reason. If an important detail remains unclear, write an unresolved record instead of guessing.
8. Classify the method from the supplied solution evidence, not from the visual appearance or a keyword in the prompt.
9. Build indexes and validate them. Use the Python validator when available; otherwise perform the checks described in `scripts/validate_bank.py` manually.

## Prompt template for a visual page review

Use a constrained request such as:

```text
Inspect only pages 3-4 of problems/homework01.pdf.
Use the original page image as the source of truth. Return:
1. the visible question number and exact page range;
2. the question text needed for the practice record;
3. the visible solution text or a concise transcription of its steps;
4. any formula, sign, subscript, table, diagram, or reading-order uncertainty;
5. whether the page needs human review.

Do not infer missing text from general knowledge and do not classify the method until the extraction is checked.
```

## Risks and controls

| Risk | Control |
|---|---|
| OCR or visual transcription error | Recheck important symbols and source pages; keep a visual-review note. |
| Hallucinated missing text or reconstructed diagrams | Preserve gaps as unresolved; never complete them from domain knowledge. |
| Wrong question/solution boundary | Use page layout and numbering; inspect adjacent pages before pairing. |
| Math or science notation error | Verify signs, exponents, subscripts, units, orientation, and labels against the image. |
| Context-window or latency cost | Process small page batches and use text retrieval for clean pages. |
| Non-deterministic output | Preserve source page citations, confidence, and review status; rerun only when needed. |
| Privacy or copyright exposure | Tell the user when a hosted model may receive PDF content; avoid public or external storage without permission. |
| False confidence from a clean-looking transcription | Keep extraction provenance separate from classification confidence. |

## Provenance

For each question, record an optional `extraction` object:

- `mode`: `agent_native_text`, `agent_native_visual`, `python_pdfplumber`, or `hybrid`;
- `pages_reviewed`: source pages inspected visually;
- `signals`: why visual review was used, such as `scan`, `sparse_text`, `formula`, `table`, or `diagram`;
- `verified_against_source`: whether important details were checked against the original page;
- `notes`: a short, visible note about limitations.

Do not store hidden chain-of-thought or private model traces.
