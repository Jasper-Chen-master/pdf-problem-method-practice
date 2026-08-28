"""validate_bank.validate 的全路径测试。"""

from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_bank import validate


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
        encoding="utf-8",
    )


def default_question() -> dict:
    return {
        "question_id": "q_001",
        "question_text": "求 x。",
        "solution_text": "x = 1。",
        "status": "classified",
        "active": True,
        "provisional": False,
        "primary_method_id": "method_example",
        "secondary_method_ids": [],
        "strategy_ids": [],
        "page_start": 1,
        "page_end": 1,
    }


def write_default_bank(bank: Path) -> None:
    """写一套结构一致的最小题库，各测试在此基础上做针对性破坏。"""
    write_jsonl(bank / "questions.jsonl", [default_question()])
    write_json(bank / "method_tags.json", {"tags": [{"id": "method_example", "status": "active"}]})
    write_json(bank / "strategy_tags.json", {"tags": []})
    write_json(bank / "aliases.json", {"aliases": {"例子": "method_example"}})
    write_json(bank / "indexes" / "methods.json", {"methods": {"method_example": ["q_001"]}})
    write_json(bank / "indexes" / "strategies.json", {"strategies": {}})
    write_jsonl(
        bank / "classification_runs.jsonl",
        [{"question_id": "q_001", "review_result": {"approved": True}}],
    )


def load_questions(bank: Path) -> list[dict]:
    return [
        json.loads(line)
        for line in (bank / "questions.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def save_questions(bank: Path, questions: list[dict]) -> None:
    write_jsonl(bank / "questions.jsonl", questions)


def test_validate_accepts_consistent_bank(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    assert validate(bank) == []


def test_missing_required_file_reports_path(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    bank.mkdir()
    errors = validate(bank)
    assert errors and "缺少必需文件" in errors[0]


def test_duplicate_question_id(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    save_questions(bank, [default_question(), default_question()])
    assert any("重复的 question_id" in e for e in validate(bank))


def test_missing_question_text(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["question_text"] = ""
    save_questions(bank, questions)
    assert any("缺少 question_text" in e for e in validate(bank))


def test_invalid_question_status(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["status"] = "classifed"  # 拼写错误应被抓住，而不是当未分类放过
    save_questions(bank, questions)
    errors = validate(bank)
    assert any("status" in e and "pending" in e and "classified" in e for e in errors)


def test_solutionless_question_must_be_provisional(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["solution_text"] = ""
    questions[0]["provisional"] = False
    save_questions(bank, questions)
    assert any("provisional=true" in e for e in validate(bank))


def test_invalid_page_range(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["page_start"], questions[0]["page_end"] = 4, 2
    save_questions(bank, questions)
    assert any("题目页码范围无效" in e for e in validate(bank))


def test_invalid_solution_page_range(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["solution_page_start"], questions[0]["solution_page_end"] = 12, 11
    save_questions(bank, questions)
    assert any("解答页码范围无效" in e for e in validate(bank))


def test_missing_primary_method(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["primary_method_id"] = "method_gone"
    save_questions(bank, questions)
    assert any("主方法" in e for e in validate(bank))


def test_missing_secondary_method_and_strategy(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["secondary_method_ids"] = ["method_gone"]
    questions[0]["strategy_ids"] = ["strategy_gone"]
    save_questions(bank, questions)
    errors = validate(bank)
    assert any("次要方法 method_gone" in e for e in errors)
    assert any("策略 strategy_gone" in e for e in errors)


def test_duplicate_tag_ids(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(
        bank / "method_tags.json",
        {"tags": [{"id": "method_example", "status": "active"}, {"id": "method_example", "status": "retired"}]},
    )
    assert any("重复的标签 id" in e for e in validate(bank))


def test_invalid_tag_status(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "method_tags.json", {"tags": [{"id": "method_example", "status": "enabled"}]})
    errors = validate(bank)
    assert any("method_tags.json" in e and "必须是" in e for e in errors)


def test_retired_tag_cannot_be_referenced(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "method_tags.json", {"tags": [{"id": "method_example", "status": "retired"}]})
    assert any("不存在或未激活的主方法" in e for e in validate(bank))


def test_method_strategy_id_collision(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "strategy_tags.json", {"tags": [{"id": "method_example", "status": "active"}]})
    assert any("冲突" in e for e in validate(bank))


def test_alias_pointing_to_missing_tag(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "aliases.json", {"aliases": {"悬空": "method_gone", "  ": "method_example"}})
    errors = validate(bank)
    assert any("别名 '悬空'" in e for e in errors)
    assert any("别名 '  '" in e for e in errors)


def test_unapproved_classification(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_jsonl(bank / "classification_runs.jsonl", [])
    assert any("没有审核通过的分类记录" in e for e in validate(bank))


def test_approved_run_requires_classified_status(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["status"] = "pending"
    save_questions(bank, questions)
    assert any("status 应设为 classified" in e for e in validate(bank))


def test_run_referencing_unknown_question(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_jsonl(
        bank / "classification_runs.jsonl",
        [
            {"question_id": "q_001", "review_result": {"approved": True}},
            {"question_id": "q_ghost", "review_result": {"approved": True}},
        ],
    )
    assert any("审核记录引用了不存在的题目" in e for e in validate(bank))


def test_stale_index_detected_via_reverse_coverage(tmp_path: Path) -> None:
    """题目引用了方法但索引还没收录 —— 必须报错而不是静默通过。"""
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "indexes" / "methods.json", {"methods": {}})
    assert any("未出现在 indexes/methods.json" in e for e in validate(bank))


def test_missing_strategy_index_entry(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "strategy_tags.json", {"tags": [{"id": "strategy_symmetry", "status": "active"}]})
    questions = load_questions(bank)
    questions[0]["strategy_ids"] = ["strategy_symmetry"]
    save_questions(bank, questions)
    assert any("未出现在 indexes/strategies.json" in e for e in validate(bank))


def test_retired_question_must_leave_index(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["active"] = False
    save_questions(bank, questions)
    assert any("已下架" in e for e in validate(bank))


def test_retired_question_without_index_is_accepted(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    questions = load_questions(bank)
    questions[0]["active"] = False
    save_questions(bank, questions)
    write_json(bank / "indexes" / "methods.json", {"methods": {}})
    assert validate(bank) == []


def test_index_referencing_unknown_question(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "indexes" / "methods.json", {"methods": {"method_example": ["q_001", "q_ghost"]}})
    assert any("引用了不存在的题目 q_ghost" in e for e in validate(bank))


def test_index_referencing_unknown_tag(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "indexes" / "methods.json", {"methods": {"method_ghost": ["q_001"]}})
    assert any("缺失或未激活的标签 method_ghost" in e for e in validate(bank))


def test_duplicate_ids_in_index(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_json(bank / "indexes" / "methods.json", {"methods": {"method_example": ["q_001", "q_001"]}})
    assert any("重复的题目 id" in e for e in validate(bank))


def test_jsonl_error_reports_line_number(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    (bank / "questions.jsonl").write_text(
        json.dumps(default_question(), ensure_ascii=False) + "\n{broken\n",
        encoding="utf-8",
    )
    assert any("questions.jsonl 第 2 行" in e for e in validate(bank))


def test_unresolved_record_reference(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_jsonl(bank / "unresolved.jsonl", [{"question_id": "q_ghost", "reason": "边界不清"}])
    assert any("unresolved.jsonl 引用了不存在的题目" in e for e in validate(bank))


def test_unresolved_record_without_question_id(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_jsonl(bank / "unresolved.jsonl", [{"reason": "缺 id"}])
    assert any("缺少 question_id" in e for e in validate(bank))


def test_unresolved_file_is_optional(tmp_path: Path) -> None:
    bank = tmp_path / "problem_bank"
    write_default_bank(bank)
    write_jsonl(bank / "unresolved.jsonl", [])
    assert validate(bank) == []
