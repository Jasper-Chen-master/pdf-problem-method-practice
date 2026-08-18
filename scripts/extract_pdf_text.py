from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pdfplumber


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_pdfs(input_path: Path) -> list[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".pdf" else []
    return sorted(path for path in input_path.rglob("*.pdf") if path.is_file())


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract page text from PDFs into JSONL records.")
    parser.add_argument("input", type=Path, help="A PDF file or directory containing PDFs.")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for source_pages.jsonl.")
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_dir = args.output.resolve()
    pdfs = discover_pdfs(input_path)
    if not pdfs:
        raise SystemExit(f"No PDF files found under {input_path}")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "source_pages.jsonl"
    errors_path = output_dir / "extraction_errors.jsonl"
    page_count = 0
    errors: list[dict[str, str]] = []

    with output_path.open("w", encoding="utf-8", newline="\n") as output:
        for pdf_path in pdfs:
            relative_path = pdf_path.name if input_path.is_file() else pdf_path.relative_to(input_path).as_posix()
            try:
                digest = file_hash(pdf_path)
                with pdfplumber.open(pdf_path) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        record = {
                            "source_file": relative_path,
                            "source_sha256": digest,
                            "page_number": page_number,
                            "text": page.extract_text(x_tolerance=1, y_tolerance=3) or "",
                        }
                        output.write(json.dumps(record, ensure_ascii=False) + "\n")
                        page_count += 1
            except Exception as exc:  # Keep other PDFs available for review.
                errors.append({"source_file": relative_path, "error": str(exc)})

    with errors_path.open("w", encoding="utf-8", newline="\n") as output:
        for record in errors:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(json.dumps({"pdfs": len(pdfs), "pages": page_count, "errors": len(errors)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

