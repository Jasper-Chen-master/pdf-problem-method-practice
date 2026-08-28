"""题库一致性校验工具（可选）。

检查 questions.jsonl、方法/策略标签、别名、索引和分类审核记录之间的
引用一致性。校验规则与 references/schemas.md 保持同步；修改任何一侧时
请同步更新文档并补充测试。
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

QUESTION_STATUSES = {"pending", "classified"}
TAG_STATUSES = {"active", "retired"}


def load_json(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"缺少必需文件：{path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"{path} 不是有效的 JSON：{exc.msg}") from exc


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise ValueError(f"缺少必需文件：{path}")
    records: list[dict] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path} 第 {line_number} 行不是有效的 JSON：{exc.msg}") from exc
    return records


def active_tag_ids(data: dict) -> set[str]:
    return {tag.get("id") for tag in data.get("tags", []) if tag.get("status") == "active"}


def check_tags(data: dict, label: str, errors: list[str]) -> None:
    seen: set[str] = set()
    for tag in data.get("tags", []):
        tag_id = tag.get("id")
        if not tag_id:
            errors.append(f"{label} 中存在缺少 id 的标签。")
            continue
        if tag_id in seen:
            errors.append(f"{label} 中存在重复的标签 id：{tag_id}。")
        seen.add(tag_id)
        if tag.get("status") not in TAG_STATUSES:
            errors.append(
                f"{label} 中标签 {tag_id} 的 status 为 {tag.get('status')!r}，"
                f"必须是 {' 或 '.join(sorted(TAG_STATUSES))}。"
            )


def check_index(
    index: dict,
    key: str,
    known_tags: set[str],
    question_id_set: set[str],
    label: str,
    errors: list[str],
) -> dict[str, set[str]]:
    """检查索引的前向引用，返回 标签id -> 题目id集合 的映射。"""
    tag_map: dict[str, set[str]] = {}
    for tag_id, ids in index.get(key, {}).items():
        if tag_id not in known_tags:
            errors.append(f"{label} 引用了缺失或未激活的标签 {tag_id}。")
        if len(ids) != len(set(ids)):
            errors.append(f"{label} 中标签 {tag_id} 存在重复的题目 id。")
        for qid in ids:
            if qid not in question_id_set:
                errors.append(f"{label} 中标签 {tag_id} 引用了不存在的题目 {qid}。")
        tag_map[tag_id] = set(ids)
    return tag_map


def validate(bank: Path) -> list[str]:
    errors: list[str] = []
    unresolved_path = bank / "unresolved.jsonl"
    try:
        questions = load_jsonl(bank / "questions.jsonl")
        methods = load_json(bank / "method_tags.json")
        strategies = load_json(bank / "strategy_tags.json")
        aliases = load_json(bank / "aliases.json")
        method_index = load_json(bank / "indexes" / "methods.json")
        strategy_index = load_json(bank / "indexes" / "strategies.json")
        runs = load_jsonl(bank / "classification_runs.jsonl")
        unresolved = load_jsonl(unresolved_path) if unresolved_path.exists() else []
    except (OSError, ValueError) as exc:
        return [str(exc)]

    # ---- 题目记录 ----
    question_ids = [item.get("question_id") for item in questions]
    question_id_set = set(question_ids)
    if None in question_id_set or "" in question_id_set:
        errors.append("每道题目必须有非空的 question_id。")
    if len(question_ids) != len(question_id_set):
        errors.append("发现重复的 question_id。")

    for question in questions:
        qid = question.get("question_id", "<缺失>")
        if question.get("status") not in QUESTION_STATUSES:
            errors.append(
                f"{qid} 的 status 为 {question.get('status')!r}，"
                f"必须是 {' 或 '.join(sorted(QUESTION_STATUSES))}。"
            )
        if not question.get("question_text"):
            errors.append(f"{qid} 缺少 question_text。")
        if not question.get("solution_text") and not question.get("provisional"):
            errors.append(f"{qid} 没有解答文本，必须标记 provisional=true。")
        if question.get("page_start") and question.get("page_end") and question["page_start"] > question["page_end"]:
            errors.append(f"{qid} 的题目页码范围无效。")
        if (
            question.get("solution_page_start")
            and question.get("solution_page_end")
            and question["solution_page_start"] > question["solution_page_end"]
        ):
            errors.append(f"{qid} 的解答页码范围无效。")

    # ---- 标签 ----
    check_tags(methods, "method_tags.json", errors)
    check_tags(strategies, "strategy_tags.json", errors)
    method_ids = active_tag_ids(methods)
    strategy_ids = active_tag_ids(strategies)
    overlap = method_ids & strategy_ids
    if overlap:
        errors.append(f"方法与策略标签 id 冲突：{', '.join(sorted(overlap))}。")

    # ---- 题目对标签的引用 ----
    for question in questions:
        qid = question.get("question_id", "<缺失>")
        if question.get("primary_method_id") not in method_ids:
            errors.append(f"{qid} 引用了不存在或未激活的主方法。")
        for method_id in question.get("secondary_method_ids", []):
            if method_id not in method_ids:
                errors.append(f"{qid} 引用了不存在或未激活的次要方法 {method_id}。")
        for strategy_id in question.get("strategy_ids", []):
            if strategy_id not in strategy_ids:
                errors.append(f"{qid} 引用了不存在或未激活的策略 {strategy_id}。")

    # ---- 索引：前向引用 ----
    method_map = check_index(method_index, "methods", method_ids, question_id_set, "indexes/methods.json", errors)
    strategy_map = check_index(
        strategy_index, "strategies", strategy_ids, question_id_set, "indexes/strategies.json", errors
    )

    # ---- 索引：反向覆盖 ----
    # active 题目的每个标签都必须出现在对应索引中（防止改完题库忘记重建索引）；
    # active=false 的下架题目不得出现在任何索引中。
    all_indexed_qids: set[str] = set()
    for ids in method_map.values():
        all_indexed_qids.update(ids)
    for ids in strategy_map.values():
        all_indexed_qids.update(ids)

    for question in questions:
        qid = question.get("question_id")
        if not qid:
            continue
        if question.get("active") is False:
            if qid in all_indexed_qids:
                errors.append(f"{qid} 已下架（active=false），但仍出现在索引中。")
            continue
        for tag_id in {question.get("primary_method_id"), *question.get("secondary_method_ids", [])}:
            if tag_id in method_ids and qid not in method_map.get(tag_id, set()):
                errors.append(f"{qid} 未出现在 indexes/methods.json 的 {tag_id} 列表中，请重建索引。")
        for strategy_id in question.get("strategy_ids", []):
            if strategy_id in strategy_ids and qid not in strategy_map.get(strategy_id, set()):
                errors.append(f"{qid} 未出现在 indexes/strategies.json 的 {strategy_id} 列表中，请重建索引。")

    # ---- 别名 ----
    known_tags = method_ids | strategy_ids
    for alias, target in aliases.get("aliases", {}).items():
        if not alias.strip() or target not in known_tags:
            errors.append(f"别名 {alias!r} 指向缺失或无效的标签。")

    # ---- 审核记录 ----
    approved: set[str] = set()
    for run in runs:
        run_qid = run.get("question_id")
        if run_qid not in question_id_set:
            errors.append(f"审核记录引用了不存在的题目 {run_qid!r}。")
            continue
        if run.get("review_result", {}).get("approved"):
            approved.add(run_qid)

    for question in questions:
        qid = question.get("question_id", "<缺失>")
        status = question.get("status")
        if status == "classified" and qid not in approved:
            errors.append(f"{qid} 标记为 classified，但没有审核通过的分类记录。")
        if qid in approved and status != "classified":
            errors.append(f"{qid} 已有审核通过的分类记录，status 应设为 classified。")

    # ---- 未决记录（可选文件） ----
    for record in unresolved:
        record_id = record.get("question_id")
        if not record_id:
            errors.append("unresolved.jsonl 中存在缺少 question_id 的记录。")
        elif record_id not in question_id_set:
            errors.append(f"unresolved.jsonl 引用了不存在的题目 {record_id!r}。")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="校验 PDF 题目方法练习库的结构一致性。")
    parser.add_argument("--bank", type=Path, default=Path("problem_bank"), help="题库目录。")
    args = parser.parse_args()
    errors = validate(args.bank)
    if errors:
        print("校验未通过：")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("校验通过。")


if __name__ == "__main__":
    main()
