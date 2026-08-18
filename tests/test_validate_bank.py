import json
from pathlib import Path

from scripts.validate_bank import validate


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")


def test_validate_accepts_consistent_bank(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    question_id = "q_example"
    method_id = "method_example"
    write_jsonl(
        bank / "questions.jsonl",
        [{"question_id": question_id, "question_text": "Solve x.", "solution_text": "x = 1.", "status": "classified", "primary_method_id": method_id, "secondary_method_ids": [], "strategy_ids": [], "page_start": 1, "page_end": 1, "provisional": False}],
    )
    write_json(bank / "method_tags.json", {"tags": [{"id": method_id, "status": "active"}]})
    write_json(bank / "strategy_tags.json", {"tags": []})
    write_json(bank / "aliases.json", {"aliases": {"example": method_id}})
    write_json(bank / "indexes" / "methods.json", {"methods": {method_id: [question_id]}})
    write_json(bank / "indexes" / "strategies.json", {"strategies": {}})
    write_jsonl(bank / "classification_runs.jsonl", [{"question_id": question_id, "review_result": {"approved": True}}])

    assert validate(bank) == []

