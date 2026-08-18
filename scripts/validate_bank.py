from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.exists():
        raise ValueError(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise ValueError(f"Missing required file: {path}")
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate(bank: Path) -> list[str]:
    errors: list[str] = []
    try:
        questions = load_jsonl(bank / "questions.jsonl")
        methods = load_json(bank / "method_tags.json")
        strategies = load_json(bank / "strategy_tags.json")
        aliases = load_json(bank / "aliases.json")
        method_index = load_json(bank / "indexes" / "methods.json")
        strategy_index = load_json(bank / "indexes" / "strategies.json")
        runs = load_jsonl(bank / "classification_runs.jsonl")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return [str(exc)]

    question_ids = [item.get("question_id") for item in questions]
    question_id_set = set(question_ids)
    if None in question_id_set or "" in question_id_set:
        errors.append("Every question must have a non-empty question_id.")
    if len(question_ids) != len(question_id_set):
        errors.append("Duplicate question_id values found.")

    method_ids = {tag.get("id") for tag in methods.get("tags", []) if tag.get("status") == "active"}
    strategy_ids = {tag.get("id") for tag in strategies.get("tags", []) if tag.get("status") == "active"}
    if None in method_ids or None in strategy_ids:
        errors.append("Every active tag must have an id.")

    for question in questions:
        qid = question.get("question_id", "<missing>")
        if not question.get("question_text"):
            errors.append(f"{qid} has empty question_text.")
        if question.get("primary_method_id") not in method_ids:
            errors.append(f"{qid} references a missing primary method.")
        for method_id in question.get("secondary_method_ids", []):
            if method_id not in method_ids:
                errors.append(f"{qid} references a missing secondary method {method_id}.")
        for strategy_id in question.get("strategy_ids", []):
            if strategy_id not in strategy_ids:
                errors.append(f"{qid} references a missing strategy {strategy_id}.")
        if question.get("page_start") and question.get("page_end") and question["page_start"] > question["page_end"]:
            errors.append(f"{qid} has an invalid question page range.")
        if question.get("solution_page_start") and question.get("solution_page_end") and question["solution_page_start"] > question["solution_page_end"]:
            errors.append(f"{qid} has an invalid solution page range.")
        if not question.get("solution_text") and not question.get("provisional"):
            errors.append(f"{qid} has no solution_text but is not marked provisional.")

    def check_index(index: dict, key: str, known_tags: set[str]) -> None:
        for tag_id, ids in index.get(key, {}).items():
            if tag_id not in known_tags:
                errors.append(f"{key} index references missing tag {tag_id}.")
            if len(ids) != len(set(ids)):
                errors.append(f"{key} index has duplicate question IDs for {tag_id}.")
            for qid in ids:
                if qid not in question_id_set:
                    errors.append(f"{key} index references missing question {qid}.")

    check_index(method_index, "methods", method_ids)
    check_index(strategy_index, "strategies", strategy_ids)

    known_tags = method_ids | strategy_ids
    for alias, target in aliases.get("aliases", {}).items():
        if not alias.strip() or target not in known_tags:
            errors.append(f"Alias {alias!r} points to a missing or invalid tag.")

    approved = {run.get("question_id") for run in runs if run.get("review_result", {}).get("approved")}
    for question in questions:
        if question.get("status") == "classified" and question.get("question_id") not in approved:
            errors.append(f"{question.get('question_id', '<missing>')} is classified but has no approved review run.")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a PDF problem-method practice bank.")
    parser.add_argument("--bank", type=Path, default=Path("problem_bank"), help="Path to the generated bank.")
    args = parser.parse_args()
    errors = validate(args.bank)
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("Validation passed.")


if __name__ == "__main__":
    main()

