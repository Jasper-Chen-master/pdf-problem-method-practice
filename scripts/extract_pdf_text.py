"""按页抽取 PDF 文本到 JSONL 记录（可选工具）。

输入可以是单个 PDF 文件，也可以是包含多个 PDF 的目录。输出：

- source_pages.jsonl：每页一条记录（源文件、SHA-256、页码、文本、抽取方式）；
- extraction_errors.jsonl：无法读取的 PDF 及错误信息。

重复运行时按 (源文件, SHA-256) 增量跳过未变化的 PDF，只重抽新增或改动的
文件；使用 --force 可忽略增量缓存、强制全量重抽。
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pdfplumber

EXTRACTION_MODE = "python_pdfplumber"


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


def load_existing_pages(path: Path) -> dict[tuple[str, str], list[dict]]:
    """读取旧的 source_pages.jsonl，返回 (source_file, source_sha256) -> 页记录列表。

    无法解析或缺少关键字的旧行会被直接丢弃，由本次运行重新抽取补齐。
    """
    if not path.exists():
        return {}
    pages: dict[tuple[str, str], list[dict]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            record = json.loads(line)
            key = (record["source_file"], record["source_sha256"])
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
        pages.setdefault(key, []).append(record)
    return pages


def main() -> None:
    parser = argparse.ArgumentParser(description="从 PDF 按页抽取文本，输出 JSONL 记录。")
    parser.add_argument("input", type=Path, help="PDF 文件或包含 PDF 的目录。")
    parser.add_argument("--output", type=Path, required=True, help="source_pages.jsonl 的输出目录。")
    parser.add_argument("--force", action="store_true", help="忽略增量缓存，强制重新抽取全部 PDF。")
    args = parser.parse_args()

    input_path = args.input.resolve()
    output_dir = args.output.resolve()
    pdfs = discover_pdfs(input_path)
    if not pdfs:
        raise SystemExit(f"在 {input_path} 下没有找到 PDF 文件")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "source_pages.jsonl"
    errors_path = output_dir / "extraction_errors.jsonl"

    existing = {} if args.force else load_existing_pages(output_path)

    page_count = 0
    reused_pages = 0
    skipped_pdfs = 0
    errors: list[dict[str, str]] = []

    # 每次运行都整体重写 source_pages.jsonl：复用的旧记录 + 本次新抽取的记录。
    # 已删除或已变化的 PDF 的旧页记录因此自然被清理。
    with output_path.open("w", encoding="utf-8", newline="\n") as output:
        for pdf_path in pdfs:
            relative_path = pdf_path.name if input_path.is_file() else pdf_path.relative_to(input_path).as_posix()
            try:
                digest = file_hash(pdf_path)
                key = (relative_path, digest)
                if key in existing:
                    for record in existing[key]:
                        output.write(json.dumps(record, ensure_ascii=False) + "\n")
                        page_count += 1
                        reused_pages += 1
                    skipped_pdfs += 1
                    continue
                with pdfplumber.open(pdf_path) as pdf:
                    for page_number, page in enumerate(pdf.pages, start=1):
                        record = {
                            "source_file": relative_path,
                            "source_sha256": digest,
                            "page_number": page_number,
                            "text": page.extract_text(x_tolerance=1, y_tolerance=3) or "",
                            "extraction_mode": EXTRACTION_MODE,
                        }
                        output.write(json.dumps(record, ensure_ascii=False) + "\n")
                        page_count += 1
            except Exception as exc:  # 单个 PDF 失败不影响其余文件。
                errors.append({"source_file": relative_path, "error": str(exc)})

    with errors_path.open("w", encoding="utf-8", newline="\n") as output:
        for record in errors:
            output.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(
        json.dumps(
            {
                "pdfs": len(pdfs),
                "pages": page_count,
                "reused_pages": reused_pages,
                "skipped_pdfs": skipped_pdfs,
                "errors": len(errors),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
