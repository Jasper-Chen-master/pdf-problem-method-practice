# PDF Problem Method Practice

> 把分散在题集 PDF 里的真实题目，整理成一个可以按“解题方法”检索的本地练习库。无需先配置 Python，支持直接使用 Agent 自带的 PDF 和视觉能力开始。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/Jasper-Chen-master/pdf-problem-method-practice/actions/workflows/ci.yml/badge.svg)](https://github.com/Jasper-Chen-master/pdf-problem-method-practice/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 这个项目解决什么问题？

传统题库通常按章节、文件名或考试时间组织。但真正复习时，你往往想练的是：

- 所有使用换元法的积分题；
- 所有使用能量守恒的物理题；
- 所有需要半反应法配平的化学题；
- 所有使用二分查找或动态规划的编程题。

这个项目让 AI Agent 从题集 PDF 中提取真实题目，并根据提供的解答判断题目实际使用了哪些方法。最终得到的 `problem_bank/` 是一个本地、可持续更新、可按方法检索的练习库。

它不是一个凭空出题器：题库中没有的题不会被编造来凑数量。

## 项目特点

| 特点 | 说明 |
| --- | --- |
| Agent 原生优先 | 能直接打开 PDF 的 Agent 可以立即开始，不要求用户先配置 Python。 |
| 多模态补足版面 | 扫描页、公式、图表、双栏、手写内容或文字层损坏时，使用模型的页面视觉能力复核。 |
| Python 可选增强 | Python 可提升批量抽取的一致性、可复现性和结构校验能力，但没有 Python 也不阻塞使用。 |
| 按解法组织 | 以“这道题是怎么解的”为核心，而不是只按章节或主题归类。 |
| 解答证据优先 | 有参考解答时，从可见的解题步骤确认方法；题目只提到某个定理，不代表实际使用了它。 |
| 支持方法组合 | 每道题可以关联主方法、次要方法和策略标签，支持检索组合方法。 |
| 来源可追溯 | 记录源 PDF、题号和页码，分类有疑问时可以回到原文核对。 |
| 只返回真实题目 | 练习时只从已经索引的题目中选择，默认隐藏解答，不虚构练习题。 |
| 本地优先 | PDF、抽取文本和生成题库默认保存在本机，并通过 `.gitignore` 排除在版本库之外。 |

## 开始使用

### 1. 安装技能

最稳妥的方式是把仓库安装到你使用的 Agent 的 skills 目录。以 Codex 为例：

#### Windows PowerShell

```powershell
git clone https://github.com/Jasper-Chen-master/pdf-problem-method-practice.git `
  "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
```

#### macOS / Linux

```bash
git clone https://github.com/Jasper-Chen-master/pdf-problem-method-practice.git \
  ~/.codex/skills/pdf-problem-method-practice
```

其他 Agent 的常见安装位置：

| Agent | 技能目录 |
| --- | --- |
| Codex | `~/.codex/skills/pdf-problem-method-practice/` |
| Claude Code | `~/.claude/skills/pdf-problem-method-practice/` |
| OpenCode | `~/.config/opencode/skill/pdf-problem-method-practice/` |
| Cursor | 项目内的 `.cursor/skills/` |

如果你的 Agent 支持直接读取当前项目里的 `SKILL.md`，也可以不做全局安装，直接在仓库目录中使用它。

### 2. 不需要 Python 也能开始

Python 不是使用前置条件。把题目 PDF 放进你的学习项目，然后直接对支持 PDF 或视觉理解的 Agent 发送：

```text
使用 $pdf-problem-method-practice 整理这个项目里的题目 PDF，
优先使用你自带的 PDF 和视觉能力解析页面；按实际解题方法建立或更新本地题库。
```

Agent 会先使用可检索的文本内容处理清晰页面，再对扫描页、公式、图表、双栏、手写内容或文字顺序异常的页面进行视觉复核。没有 Python 时，仍然可以完成题目提取、分类、建索引和练习检索。

### 3. 可选安装 Python 以提升稳定性

Python 工具不是必须的，但在大批量 PDF、重复构建或需要确定性校验时很有价值。它可以提升：

- 按页批量抽取的一致性；
- 源文件 SHA-256 和中间记录的可复现性；
- 题库结构、标签引用和索引的自动校验；
- Agent 对大量纯文本页面的处理效率。

安装可选工具：

```bash
python -m pip install -e .
```

开发和测试环境：

```bash
python -m pip install -e ".[dev]"
```

### 4. 准备题目 PDF

在你的学习项目中建立一个目录，例如：

```text
my-study-project/
├── problems/
│   ├── homework-01.pdf
│   └── final-review.pdf
└── ...
```

源 PDF 可以放在任意项目目录中；仓库默认忽略所有 `*.pdf` 和 `problem_bank/`，避免把课程资料、答案或个人学习数据提交到 Git。

### 5. 按方法练习

题库建立后，可以直接用自然语言检索：

```text
给我 5 道使用格林公式的题，不要显示答案。
给我需要替换曲面的 Stokes 定理题。
给我同时使用换元法和对称性的题。
这个项目目前有哪些方法可以练习？
```

Agent 会从 `problem_bank/indexes/` 中查找题目，并返回题目原文、来源文件和页码。没有匹配记录时，它会说明没有足够的已索引题目，而不是自行生成题目。

## 推荐的解析策略

1. 清晰的文本页优先使用 Agent 的原生文本读取能力；
2. 扫描页、公式、图表、双栏、手写内容和文字层损坏页使用原生视觉能力；
3. 重要公式、负号、上下标、单位、题号和表格单元格必须回看原页；
4. 记录 `agent_native_text` 或 `agent_native_visual` 等解析来源；
5. 不确定的题目边界或答案配对进入 `unresolved.jsonl`，不要靠常识补全。

视觉解析可以免去 Python 配置，但可能带来 OCR 误读、公式符号错误、上下文成本、非确定输出以及隐私风险。对于大批量和高复现要求的项目，再安装 Python 工具做辅助抽取和校验。

## 可选的本地工具

### 抽取 PDF 页面文本

输入可以是一个 PDF 文件，也可以是包含多个 PDF 的目录：

```bash
python scripts/extract_pdf_text.py ./problems \
  --output ./problem_bank/extraction
```

输出包括：

- `source_pages.jsonl`：每页一条记录，包含源文件、SHA-256、页码和文本；
- `extraction_errors.jsonl`：无法读取的 PDF 及错误信息。

这个脚本不是使用本 skill 的前置条件；它主要用于批量、可复现的文本预处理，不负责识别题目边界或替代 Agent 的视觉审核。

### 校验题库

```bash
python scripts/validate_bank.py --bank ./problem_bank
```

校验器会检查题目 ID 是否重复、标签引用是否存在、页码范围是否合理、方法索引是否指向真实题目，以及已分类题目是否有通过审核的分类记录。没有 Python 时，Agent 应按相同规则进行手动检查并说明未运行本地校验器。

## 题库目录结构

```text
problem_bank/
├── extraction/
│   ├── source_pages.jsonl
│   └── extraction_errors.jsonl
├── questions.jsonl
├── method_tags.json
├── strategy_tags.json
├── aliases.json
├── classification_runs.jsonl
└── indexes/
    ├── methods.json
    └── strategies.json
```

核心记录保存在 `questions.jsonl`。一条记录通常包含题目文本、解答文本、来源页码、方法标签、分类证据，以及可选的 `extraction` 解析来源和视觉复核记录。

完整字段定义见 [references/schemas.md](references/schemas.md)，视觉解析规范见 [references/agent-native-pdf.md](references/agent-native-pdf.md)，分类规则见 [references/classification-guide.md](references/classification-guide.md)。

## 质量边界与隐私

- 源 PDF 按只读输入处理，不修改原文件。
- 没有提供解答时可以保守分类，但必须标记为 provisional，并说明尚未经过解答验证。
- 视觉模型可能读错公式、符号、表格或页面顺序；重要细节必须回看原页，不确定时标记 unresolved。
- 如果 Agent 使用托管模型的视觉能力，PDF 内容可能会发送给对应服务；处理课程资料、个人资料或受版权保护内容前，应确认服务设置和再分发权限。
- 题库可能包含完整题目和解答文本，除非拥有再分发权限，不要把它们提交到公开仓库或发送到外部服务。
- Python 本地工具可以减少中间数据处理的不确定性，但不能替代 Agent 对版面和解题证据的判断。

## 开发

安装开发依赖并运行测试：

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

修改数据结构或校验器时，请同步更新 `references/schemas.md` 并添加针对性的测试。贡献时不要提交课程 PDF、答案文件或真实学生数据，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目文件速览

| 路径 | 作用 |
| --- | --- |
| `SKILL.md` | Agent 使用的核心技能说明和工作规则 |
| `agents/openai.yaml` | Codex 的可选显示名称、默认提示词和自动调用配置 |
| `scripts/extract_pdf_text.py` | 可选的 PDF 按页抽取工具 |
| `scripts/validate_bank.py` | 可选的题库一致性校验工具 |
| `references/agent-native-pdf.md` | Agent 原生 PDF 和多模态解析规范 |
| `references/` | 数据结构、分类指南和复核清单 |
| `tests/` | Python 工具测试 |
| `.github/workflows/ci.yml` | GitHub Actions 测试流程 |

## 许可证

[MIT License](LICENSE)
