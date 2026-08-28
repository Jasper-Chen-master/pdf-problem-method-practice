"""extract_pdf_text 纯函数的测试（不依赖真实 PDF 与 pdfplumber）。"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.extract_pdf_text import discover_pdfs, load_existing_pages


def test_discover_pdfs_in_directory_is_sorted_and_recursive(tmp_path: Path) -> None:
    (tmp_path / "b.pdf").write_bytes(b"%PDF-")
    (tmp_path / "a.pdf").write_bytes(b"%PDF-")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "c.pdf").write_bytes(b"%PDF-")
    (tmp_path / "notes.txt").write_text("not a pdf", encoding="utf-8")

    assert discover_pdfs(tmp_path) == [tmp_path / "a.pdf", tmp_path / "b.pdf", sub / "c.pdf"]


def test_discover_pdfs_single_file(tmp_path: Path) -> None:
    pdf = tmp_path / "only.pdf"
    pdf.write_bytes(b"%PDF-")
    assert discover_pdfs(pdf) == [pdf]

    txt = tmp_path / "only.txt"
    txt.write_text("nope", encoding="utf-8")
    assert discover_pdfs(txt) == []


def test_discover_pdfs_empty_directory(tmp_path: Path) -> None:
    assert discover_pdfs(tmp_path) == []


def test_load_existing_pages_groups_by_file_and_hash(tmp_path: Path) -> None:
    path = tmp_path / "source_pages.jsonl"
    rows = [
        {"source_file": "a.pdf", "source_sha256": "h1", "page_number": 1, "text": "第一页"},
        {"source_file": "a.pdf", "source_sha256": "h1", "page_number": 2, "text": "第二页"},
        {"source_file": "a.pdf", "source_sha256": "h2", "page_number": 1, "text": "旧版本"},
    ]
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    pages = load_existing_pages(path)
    assert set(pages) == {("a.pdf", "h1"), ("a.pdf", "h2")}
    assert [r["page_number"] for r in pages[("a.pdf", "h1")]] == [1, 2]


def test_load_existing_pages_drops_broken_lines(tmp_path: Path) -> None:
    path = tmp_path / "source_pages.jsonl"
    good = json.dumps(
        {"source_file": "a.pdf", "source_sha256": "h1", "page_number": 1, "text": "ok"},
        ensure_ascii=False,
    )
    path.write_text(good + "\n{broken json\n\n" + "not json at all\n", encoding="utf-8")

    pages = load_existing_pages(path)
    assert list(pages) == [("a.pdf", "h1")]


def test_load_existing_pages_missing_file(tmp_path: Path) -> None:
    assert load_existing_pages(tmp_path / "nope.jsonl") == {}
