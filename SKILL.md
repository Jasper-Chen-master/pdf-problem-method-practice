---
name: pdf-problem-method-practice
description: 把题集 PDF 整理成本地练习题库，按参考解答中实际使用的解题方法分类真实题目。适用于任意学科，Agent 优先：有原生 PDF 与多模态能力即可直接开始；可选 Python 工具提升批量抽取一致性与结构校验。
metadata:
  short-description: 从 PDF 构建以解答为依据、任意学科通用的练习题库。
---

# PDF 题目方法练习库

把学习项目里的题集 PDF 转化为一个持久的练习题库，按每道题参考解答中**实际使用**的解题方法组织。这个技能与学科无关：分类依据是"这道题是怎么解的"——某个技巧、定理、流程或思路，无论是数学、化学、语言、历史、编程还是其他学科。

默认工作流是 Agent 优先。如果 Agent 能打开 PDF 并理解页面图像，用户无需安装 Python 即可开始。可选的 Python 工具用于提升批量抽取、可复现性和确定性校验；它们不是前置条件。

## Agent 兼容性

本技能使用大多数 Agent 技能系统都能识别的标准 `SKILL.md` frontmatter：

| Agent | 技能目录 |
|---|---|
| Codex CLI / 桌面版 | `~/.codex/skills/pdf-problem-method-practice/` |
| Claude Code | `~/.claude/skills/pdf-problem-method-practice/` 或项目内 `.claude/skills/` |
| OpenCode | `~/.config/opencode/skill/pdf-problem-method-practice/` 或项目内 `.opencode/skill/` |
| Cursor | 项目内 `.cursor/skills/` |
| 任何读取 `AGENTS.md` 的 Agent | 把整个文件夹复制进仓库并在 `AGENTS.md` 中引用 |

可选的 `agents/openai.yaml` 是 Codex 专用清单。`scripts/` 下的脚本是可选的纯 Python 工具，不构成使用本技能的最低要求。

## 运行模式

根据当前 Agent 和环境的能力，选择最高可用的模式：

1. **Agent 原生模式（默认）。** 直接打开 PDF，文本层可靠时优先使用文本；对版面、图像、公式、表格、扫描件或手写内容承载信息的页面使用原生视觉理解，把生成的记录直接写入 `problem_bank/`。
2. **混合模式。** 由 Agent 负责理解与判断，同时可选运行 `scripts/extract_pdf_text.py` 做快速按页文本抽取，用 `scripts/validate_bank.py` 做确定性结构校验。
3. **工具模式。** 当 Agent 无法打开 PDF、语料过大无法直接检视、需要可复现的文本抽取、或用户明确要求命令行工作流时，使用 Python 脚本。

处理前先声明使用的模式。如果原生 PDF 或图像理解不可用，退回到可选的工具模式，或请用户提供抽取后的文本。不要声称纯文本抽取能保留原始版面。

## 边界

- 源 PDF 按只读输入处理。
- 生成的数据存放在项目内的 `problem_bank/`，绝不写进本技能目录。
- 练习请求只返回已索引的题目，不为凑数量编造新题。
- 除非用户明确要求，隐藏解答文本。
- 有参考解答时从解答中分类。没有解答时，把结果标记为 provisional 并记录这一局限。
- 把视觉转写当作可能有误的证据，而不是事实。为视觉复核过的记录保留源页面和抽取来源。
- 抽取与解释分离。不要凭常识悄悄修复读不清的公式、符号、下标、表格单元格或图形。
- 用小批次页面做视觉复核，批准前对照原页复查高影响细节。
- 未经许可，不要把完整版权材料放进公开仓库或外部服务。

## 构建或更新题库

1. 找到用户指定的 PDF，确定可用的运行模式。Agent 原生模式下不要求任何 Python 配置步骤。
2. 逐页检视 PDF。干净的页面优先用原生文本；文本为空、稀疏、乱序、扫描、多栏、公式、表格、图形、手写或阅读顺序可疑的页面使用视觉理解。
3. 从原始页面版面判断题目与解答的边界。单独提供的答案键只在题号与上下文都对得上时才配对，否则记入 `unresolved.jsonl`。
4. 为每道可靠的题目建立记录，字段定义见 [references/schemas.md](references/schemas.md)。保留源路径、页码范围、抽取模式和视觉复核状态。
5. 复用语义相符的 active 方法标签；只有出现可复用的独立解法时才新建标签。方法标签与学科无关，例如 `method_uv_substitution`、`method_redox_balancing`、`method_topic_sentence`、`method_binary_search`。
6. 只有在次要方法被实质使用时才记录；处理边界情况、检查定向、利用对称性之类的战术放策略标签。
7. 基于可见的解题步骤写简短证据摘要。不存放隐藏的推理痕迹。视觉细节不确定时记录不确定性，不要猜。
8. 淘汰不再使用的题目时把 `active` 设为 `false` 并从所有索引中移除，不要物理删除记录。
9. 重建方法与策略索引。可选 Python 工具可用时运行 `scripts/validate_bank.py --bank problem_bank`；否则由 Agent 手动执行相同检查（见 schemas.md 末尾的校验清单），并说明未运行本地校验器。

视觉复核的判定规则和风险控制见 [references/agent-native-pdf.md](references/agent-native-pdf.md)。记录的完整字段结构见 [references/schemas.md](references/schemas.md)。分类决策见 [references/classification-guide.md](references/classification-guide.md)。抽取或分类含糊时参考 [references/review-checklist.md](references/review-checklist.md)。

## 原生 PDF 与多模态复核

Agent 的原生多模态能力可以解析和检视 PDF 页面，尤其是纯文本抽取会丢失信息的页面。可用时优先使用，但要保留源页面核对和不确定性追踪。

以下情况使用视觉复核：扫描件、公式、符号、图形、表格、手写、多栏、图注、空间分组，或文本为空、稀疏、乱码、乱序的页面。干净的纯文本页面用原生文本抽取通常更省、更快、更可复现、也更易检索。

主要风险是转写错误、幻觉补全、负号与下标误读、上下文与延迟成本、输出不确定，以及托管模型接收课程材料带来的隐私或版权暴露。缓解方式：只复核必要页面、保留页码引用、保留不确定性、重要细节对照原页，并且绝不在没有证据的情况下把模型重建的内容当作参考解答。

## 练习检索

用 `aliases.json` 和 active 方法标签解析用户请求的方法，从 `indexes/methods.json` 加载相关题目 id，再从 `questions.jsonl` 加载记录。`active=false` 的下架题目不参与检索。

呈现题面、来源文件和页码范围。记录是 provisional、视觉转写或没有参考解答时，如实说明。请求的方法没有已索引的题目时直说，并主动提供相近的现有方法；不编造题目。

## 可选本地工具

Python 是可选的。安装后：

- `scripts/extract_pdf_text.py`：按页抽取文本到 `source_pages.jsonl`，按 (源文件, SHA-256) 增量跳过未变化的 PDF，`--force` 可强制全量重抽；
- `scripts/validate_bank.py`：对题库做确定性结构校验，并给出中文错误清单。

这些工具能提升大批量场景的一致性与准确性，但缺少 Python 绝不能阻塞 Agent 原生 PDF 解析。
