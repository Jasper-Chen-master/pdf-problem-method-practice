# 数据结构

使用 UTF-8 JSON。每个 JSONL 文件每行恰好一个 JSON 对象。所有生成文件都存放在目标项目的 `problem_bank/` 目录下。结构定义与学科无关，并与 `scripts/validate_bank.py` 的校验规则保持同步——修改任何一侧时，同步更新文档并补充测试。

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
  "evidence_summary": "参考解答替换了曲面并应用斯托克斯定理。",
  "extraction": {
    "mode": "agent_native_visual",
    "pages_reviewed": [3, 4],
    "signals": ["formula", "diagram"],
    "verified_against_source": true,
    "notes": "文本层丢失了曲面标注，已对照页面图像复核。"
  }
}
```

字段语义：

- `solution_text` 仅在 `provisional=true` 时允许为空。
- `question_id` 必须唯一，且对"源路径 + 题号"保持稳定。
- `status` 只允许 `pending`（尚未完成分类审核）或 `classified`（分类已审核通过）。拼写错误的枚举值会被校验器拒绝。
- `active` 表示题目是否仍应参与检索，默认 `true`。淘汰题目时设为 `false`（保留记录、不物理删除）；`active=false` 的题目不得出现在任何索引中。
- `primary_method_id`、`secondary_method_ids`、`strategy_ids` 必须指向下方标签文件中 `status=active` 的标签。

可选的 `extraction` 对象记录抽取来源，不是模型推理。`mode` 允许的值：`agent_native_text`、`agent_native_visual`、`python_pdfplumber`、`hybrid`。当 Agent 阅读了页面图像或执行了原生视觉 OCR 时使用 `agent_native_visual`。重要细节尚未复核时，`verified_against_source` 设为 `false` 或省略。

## 可选的 `extraction/source_pages.jsonl`

按页抽取文件存在时，每条记录可以包含确定性或 Agent 报告的来源信息：

```json
{
  "schema_version": 1,
  "source_file": "problems/homework01.pdf",
  "source_sha256": "...",
  "page_number": 3,
  "text": "...",
  "extraction_mode": "python_pdfplumber",
  "visual_review_recommended": false,
  "visual_review_reasons": []
}
```

`extraction_mode` 使用与 `extraction.mode` 相同的枚举值。Agent 原生工作流可以直接写题目记录，不必创建这个中间文件。

## 可选的 `unresolved.jsonl`

存放无法可靠完成抽取或配对的记录：题目边界不清、答案键无法配对、视觉细节存疑等。它的作用是把"没把握"显式留痕，而不是伪装成确定结果或凭常识补全。文件可选，存在时校验器会检查引用有效性。

```json
{
  "schema_version": 1,
  "question_id": "q_ab12cd34",
  "reason": "answer_key_mismatch",
  "detail": "答案键第 7 题与正文第 7 题的学科语境不一致，暂不配对。",
  "source_file": "problems/final-review.pdf",
  "page_start": 11,
  "page_end": 12,
  "created_at": "2026-08-28T00:00:00Z"
}
```

字段语义：

- `question_id` 必填，指向 `questions.jsonl` 中已存在的题目（例如边界暂时存疑的那道题）。
- `reason` 建议使用简短英文标识，如 `boundary_unclear`、`answer_key_mismatch`、`visual_detail_unclear`。
- `detail`、`source_file`、页码与 `created_at` 均可选，但写上来源页码更利于回溯。

同一题目解决后，删除对应未决记录并正常更新题目即可。

## 标签文件

`method_tags.json` 与 `strategy_tags.json` 结构相同：

```json
{
  "schema_version": 1,
  "tags": [
    {
      "id": "method_stokes_theorem",
      "canonical_name": "Stokes 定理",
      "normalized_name": "stokes 定理",
      "description": "把边界上的环量与曲面积分联系起来。",
      "aliases": ["Stokes"],
      "usage_count": 5,
      "status": "active"
    }
  ]
}
```

- `id` 在同一文件内必须唯一，且方法与策略标签的 id 不得互相冲突。
- `status` 只允许 `active` 或 `retired`。淘汰标签用 `retired` 保留历史，`retired` 标签不能被新题目引用。

## 索引与别名

`indexes/methods.json` 与 `indexes/strategies.json` 把 active 标签 id 映射到题目 id 列表：

```json
{"schema_version": 1, "methods": {"method_stokes_theorem": ["q_ab12cd34"]}}
```

`aliases.json` 把规范化后的用户说法映射到 active 方法或策略标签：

```json
{"schema_version": 1, "aliases": {"stokes": "method_stokes_theorem"}}
```

索引必须在每次题目或标签变动后重建。校验器会做双向检查：索引引用的题目必须存在，题目使用的每个 active 标签也必须出现在对应索引里。

## 审核历史

`classification_runs.jsonl` 记录可见的分类元数据，不存放隐藏推理：

```json
{
  "schema_version": 1,
  "question_id": "q_ab12cd34",
  "timestamp": "2026-01-01T00:00:00Z",
  "review_result": {"approved": true},
  "final_method_ids": ["method_stokes_theorem"],
  "final_strategy_ids": [],
  "summary": "解答显式使用了 Stokes 定理。"
}
```

每条记录的 `question_id` 必须指向已存在的题目。题目 `status=classified` 的前提是存在审核通过的记录；反之，存在审核通过记录的题目应把 `status` 设为 `classified`。

## 校验器检查清单

无 Python 环境时，Agent 应手动执行与 `scripts/validate_bank.py` 相同的检查，并说明未运行本地校验器：

1. 必需文件齐全（questions、两个标签文件、aliases、两个索引、classification_runs）。
2. 每道题有非空且唯一的 `question_id`、非空 `question_text`、合法的 `status` 枚举。
3. 无解答文本的题目必须 `provisional=true`。
4. 页码范围不倒置（题目与解答分别检查）。
5. 题目引用的主方法、次要方法、策略都存在且 active；方法与策略 id 不冲突；标签 id 不重复、`status` 枚举合法。
6. 索引与题库双向一致：索引不引用缺失题目或缺失标签；active 题目的每个标签都进了索引；`active=false` 的题目不在任何索引中。
7. 每个别名非空且指向 active 标签。
8. 审核记录不引用不存在的题目；`classified` 与审核通过记录互相匹配。
9. `unresolved.jsonl`（若存在）的每条记录都有指向已存在题目的 `question_id`。
