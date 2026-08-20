# PDF Problem Method Practice

> 把分散在题集 PDF 里的真实题目，整理成一个可以按“解题方法”检索的本地练习库。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![CI](https://github.com/Jasper-Chen-master/pdf-problem-method-practice/actions/workflows/ci.yml/badge.svg)](https://github.com/Jasper-Chen-master/pdf-problem-method-practice/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 这个项目解决什么问题？

传统题库通常按章节、文件名或考试时间组织。但真正复习时，你往往想练的是：

- 所有使用换元法的积分题；
- 所有使用能量守恒的物理题；
- 所有需要半反应法配平的化学题；
- 所有使用二分查找或动态规划的编程题。

这个项目让 AI Agent 从题集 PDF 中提取真实题目，并根据提供的解答判断题目实际使用了哪些方法。最终得到的 \`problem_bank/\` 是一个本地、可持续更新、可按方法检索的练习库。

它不是一个凭空出题器：题库中没有的题不会被编造来凑数量。

## 项目特点

| 特点 | 说明 |
| --- | --- |
| 按解法组织 | 以“这道题是怎么解的”为核心，而不是只按章节或主题归类。 |
| 解答证据优先 | 有参考解答时，从可见的解题步骤确认方法；题目只提到某个定理，不代表实际使用了它。 |
| 支持方法组合 | 每道题可以关联主方法、次要方法和策略标签，支持检索组合方法。 |
| 来源可追溯 | 记录源 PDF、题号和页码，分类有疑问时可以回到原文核对。 |
| 诚实处理不确定性 | 没有解答或边界不清时，记录为 provisional / unresolved，而不是伪装成确定结果。 |
| 只返回真实题目 | 练习时只从已经索引的题目中选择，默认隐藏解答，不虚构练习题。 |
| 本地优先 | PDF、抽取文本和生成题库默认保存在本机，并通过 \`.gitignore\` 排除在版本库之外。 |
| 与 Agent 解耦 | \`SKILL.md\` 使用通用技能格式，可用于 Codex、Claude Code、OpenCode、Cursor 等支持项目技能的 Agent。 |

## 开始使用

### 1. 安装技能

最稳妥的方式是把仓库安装到你使用的 Agent 的 skills 目录。以 Codex 为例：

#### Windows PowerShell

\`\`\`powershell
git clone https://github.com/Jasper-Chen-master/pdf-problem-method-practice.git \`
  "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
\`\`\`

#### macOS / Linux

\`\`\`bash
git clone https://github.com/Jasper-Chen-master/pdf-problem-method-practice.git \
  ~/.codex/skills/pdf-problem-method-practice
\`\`\`

其他 Agent 的常见安装位置：

| Agent | 技能目录 |
| --- | --- |
| Codex | \`~/.codex/skills/pdf-problem-method-practice/\` |
| Claude Code | \`~/.claude/skills/pdf-problem-method-practice/\` |
| OpenCode | \`~/.config/opencode/skill/pdf-problem-method-practice/\` |
| Cursor | 项目内的 \`.cursor/skills/\` |

如果你的 Agent 支持直接读取当前项目里的 \`SKILL.md\`，也可以不做全局安装，直接在仓库目录中使用它。

### 2. 安装 Python 工具

Python 工具用于 PDF 文本抽取和题库校验，要求 Python 3.10 或更高版本。

只使用 PDF 抽取和校验功能：

\`\`\`bash
python -m pip install -e .
\`\`\`

本地开发或运行测试：

\`\`\`bash
python -m pip install -e ".[dev]"
\`\`\`

### 3. 准备题目 PDF

在你的学习项目中建立一个目录，例如：

\`\`\`text
my-study-project/
├── problems/
│   ├── homework-01.pdf
│   └── final-review.pdf
└── ...
\`\`\`

源 PDF 可以放在任意项目目录中；仓库默认忽略所有 \`*.pdf\` 和 \`problem_bank/\`，避免把课程资料、答案或个人学习数据提交到 Git。

> 当前抽取工具基于 \`pdfplumber\`，适合已有文本层的 PDF。扫描版 PDF 需要先用 OCR 生成可搜索文本；本项目暂不内置 OCR。

### 4. 让 Agent 建立题库

在包含 \`problems/\` 的项目中，对 Agent 发送：

\`\`\`text
使用 $pdf-problem-method-practice 整理这个项目里的题目 PDF，
按实际解题方法建立或更新本地题库，并在完成后运行校验。
\`\`\`

Agent 的工作流程是：

1. 按页抽取 PDF 文本；
2. 识别题目、解答和题号边界；
3. 配对独立的答案文件（只有题号和上下文都匹配时才配对）；
4. 依据解答步骤选择主方法、次要方法和策略标签；
5. 记录来源页码、证据摘要和不确定性；
6. 重建方法索引和别名索引；
7. 运行题库校验。

### 5. 按方法练习

题库建立后，可以直接用自然语言检索：

\`\`\`text
给我 5 道使用格林公式的题，不要显示答案。
给我需要替换曲面的 Stokes 定理题。
给我同时使用换元法和对称性的题。
这个项目目前有哪些方法可以练习？
\`\`\`

Agent 会从 \`problem_bank/indexes/\` 中查找题目，并返回题目原文、来源文件和页码。没有匹配记录时，它会说明没有足够的已索引题目，而不是自行生成题目。

## 也可以手动运行工具

### 抽取 PDF 页面文本

输入可以是一个 PDF 文件，也可以是包含多个 PDF 的目录：

\`\`\`bash
python scripts/extract_pdf_text.py ./problems \
  --output ./problem_bank/extraction
\`\`\`

输出包括：

- \`source_pages.jsonl\`：每页一条记录，包含源文件、SHA-256、页码和文本；
- \`extraction_errors.jsonl\`：无法读取的 PDF 及错误信息。

抽取脚本只负责“按页读取文本”，不会自动判断题目边界，也不会替代 Agent 的分类审核。

### 校验题库

\`\`\`bash
python scripts/validate_bank.py --bank ./problem_bank
\`\`\`

校验器会检查题目 ID 是否重复、标签引用是否存在、页码范围是否合理、方法索引是否指向真实题目，以及已分类题目是否有通过审核的分类记录。

## 题库目录结构

\`\`\`text
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
\`\`\`

核心记录保存在 \`questions.jsonl\`。一条记录通常包含：

- 题目文本和解答文本；
- 源文件、题号和题目/解答页码；
- 主方法、次要方法和策略标签；
- 分类置信度和可见证据摘要；
- \`provisional\` 标记，用于没有解答或尚未验证的记录。

完整字段定义见 [references/schemas.md](references/schemas.md)，分类规则见 [references/classification-guide.md](references/classification-guide.md)。

## 质量边界与隐私

- 源 PDF 按只读输入处理，不修改原文件。
- 没有提供解答时可以保守分类，但必须标记为 provisional，并说明尚未经过解答验证。
- 题目边界、答案配对或分类不清时，应保留在 \`unresolved.jsonl\` 供人工复核，不能强行归类。
- 题库可能包含完整题目和解答文本，通常属于课程资料或受版权保护内容；除非拥有再分发权限，不要把它们提交到公开仓库或发送到外部服务。
- 本仓库只提供抽取、组织和校验能力；分类质量仍取决于 PDF 文本质量、答案是否完整以及 Agent 的审核。

## 开发

安装开发依赖并运行测试：

\`\`\`bash
python -m pip install -e ".[dev]"
python -m pytest
\`\`\`

修改数据结构或校验器时，请同步更新 \`references/schemas.md\` 并添加针对性的测试。贡献时不要提交课程 PDF、答案文件或真实学生数据，详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 项目文件速览

| 路径 | 作用 |
| --- | --- |
| \`SKILL.md\` | Agent 使用的核心技能说明和工作规则 |
| \`agents/openai.yaml\` | Codex 的可选显示名称、默认提示词和自动调用配置 |
| \`scripts/extract_pdf_text.py\` | PDF 按页抽取为 JSONL |
| \`scripts/validate_bank.py\` | 校验生成题库的一致性 |
| \`references/\` | 数据结构、分类指南和复核清单 |
| \`tests/\` | Python 工具测试 |
| \`.github/workflows/ci.yml\` | GitHub Actions 测试流程 |

## 许可证

[MIT License](LICENSE)
