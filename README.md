# 📚 PDF Problem Method Practice

> **把堆积如山的题集 PDF，变成一本按「解题方法」检索的个人题库。**
> 适用任何学科、任何 AI 编程助手（Agent）——数学、物理、化学、英语、历史、编程……通吃。

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent-agnostic](https://img.shields.io/badge/Works%20with-Codex%20%E2%80%A2%20Claude%20Code%20%E2%80%A2%20OpenCode%20%E2%80%A2%20Cursor-8A2BE2)](SKILL.md)

[English](#english) | [中文](#中文)

---

## 中文

### 🎯 这是给谁用的？

**给正在备考的学生。**

你手里是不是有一堆这样的东西：老师发的作业 PDF、往年真题、练习册扫描件、期末复习讲义……它们按章节、按日期、按文件散落各处。考前你想集中练某一类题，比如「所有要用**换元法**的积分题」——但你在十几份 PDF 里翻了一个小时，也凑不齐 5 道。

这个 Skill 帮你解决这件事：**让 AI 帮你把每一道真题按「解题方法」分类整理，存成一个本地题库**。以后你说一句「给我 5 道格林公式的题」，AI 直接从题库里调出来给你练，不用再翻 PDF。

### ✨ 核心优势

| | 优势 | 说明 |
|---|---|---|
| 🧠 | **按方法分类，不按章节** | 不是按「第 3 章」归类，而是按「这道题到底用了什么方法解题」归类。复习时直接按方法集中训练 |
| 🔍 | **依据解答分类，不靠猜** | 有参考答案时，AI 会从解题步骤里找证据确认方法；题干里提到某个定理 ≠ 真的用了它。没答案的题会标记为「待验证」，不会糊弄你 |
| 🧩 | **支持方法组合搜索** | 一题可以记多个方法：主方法 + 次要方法 + 策略标签。能搜「含奇点的格林公式」「需要补面的 Stokes 定理」「换元 + 对称性」这种组合题 |
| 📖 | **可回溯到原题** | 每道题都记录来自哪个 PDF、第几页。分类有疑问？直接翻回原题核对 |
| 🔒 | **只练真题目** | 练习模式只返回题库里真实存在的题，默认不显示答案，也**绝不虚构题目**凑数 |
| 🗂️ | **长期本地记忆** | 题库会持续更新维护——今天加了新 PDF，明天再问 AI，它知道之前已经整理过哪些题 |
| 🏠 | **数据完全本地** | 你的讲义、答案、题目文本都保存在自己电脑上，默认不进 Git，不传外部服务 |

### 📐 支持哪些学科？

**任何学科都可以。** 关键不在于学科，而在于「这道题是用什么方法解的」：

| 学科 | 方法示例 |
|---|---|
| 数学 | 换元积分法、拉格朗日乘子法、格林公式、施密特正交化 |
| 物理 | 受力分析 + 牛顿第二定律、能量守恒、基尔霍夫定律 |
| 化学 | 氧化还原半反应配平、平衡常数 ICE 表 |
| 英语/语文 | 找主题句、主谓一致检查、同义替换 |
| 历史/文科 | 对比-对照结构、史料来源分析（谁-何时-为何） |
| 编程 | 二分查找、动态规划 + 记忆化、递归 + 基线条件 |

### 🤖 支持哪些 AI 助手？

Skill 使用通用的 `SKILL.md` 格式，**主流 AI 编程助手都能用**：

| 助手 | 安装位置 |
|---|---|
| **Codex**（CLI / 桌面版） | `~/.codex/skills/pdf-problem-method-practice/` |
| **Claude Code** | `~/.claude/skills/` 或项目里的 `.claude/skills/` |
| **OpenCode** | `~/.config/opencode/skill/` 或项目里的 `.opencode/skill/` |
| **Cursor** | 项目里的 `.cursor/skills/` |
| 任意读取 `AGENTS.md` 的助手 | 把文件夹放进仓库，在 `AGENTS.md` 里引用 |

### 🚀 快速开始

**第 1 步：安装**

克隆仓库，把 `pdf-problem-method-practice` 文件夹放进你所用助手的 skills 目录（见上表）。以 Codex 为例：

```powershell
git clone https://github.com/YOUR-ACCOUNT/pdf-problem-method-practice.git
Copy-Item -Recurse .\pdf-problem-method-practice "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
```

可选：本地抽取 PDF 文本需要安装依赖：

```powershell
python -m pip install -e .
```

**第 2 步：整理你的题集**

把题目 PDF 放进你想学习的项目文件夹，然后对你的 AI 助手说：

```text
使用 $pdf-problem-method-practice 整理这个项目里的题目 PDF，按实际解题方法建立本地题库。
```

AI 会抽取 PDF → 识别题目和答案边界 → 按方法分类 → 生成题库（`problem_bank/` 文件夹）。

**第 3 步：按方法复习**

```text
给我 5 道格林公式的题，不要显示答案。
给我需要替换曲面的 Stokes 定理题。
这个项目里目前有哪些可以练的方法？
```

第一次抽取 PDF 文本，也可以手动运行：

```powershell
python scripts/extract_pdf_text.py .\problems --output .\problem_bank\extraction
```

题库建好或更新后，验证数据完整性：

```powershell
python scripts/validate_bank.py --bank .\problem_bank
```

### 🏠 数据与隐私

题库设计为**只在本地保存**。它的 JSONL 记录可能包含完整题目与解答文本，因此 `problem_bank/` 默认被 Git 忽略。除非你拥有再分发权限，**不要**提交课程讲义、答案、抽取后的题目文本或生成的题库数据。

### 🛠️ 开发

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

### 📄 许可证

MIT，见 [LICENSE](LICENSE)。

---

## English

### 🎯 Who Is This For?

**Students preparing for exams.**

You have piles of problem PDFs — homework sets, past papers, scanned workbooks, review handouts. They're scattered by chapter, by date, by file. Before an exam you want to drill one specific method ("every integral solvable by **u-substitution**"), but after an hour of flipping through PDFs you still can't gather 5 of them.

This skill fixes that: **an AI agent organizes every real problem by the method used to solve it**, into a local practice bank. Next time you say "give me 5 Green's theorem problems," the agent pulls them straight from the bank — no more PDF archaeology.

### ✨ Key Benefits

| | Benefit | Details |
|---|---|---|
| 🧠 | **Organized by method, not chapter** | Classified by *how* each problem is actually solved, so you can drill one technique at a time |
| 🔍 | **Classified from evidence** | When a solution exists, the method is verified against its visible steps; a theorem merely named in the prompt isn't enough. Solution-less questions are marked provisional |
| 🧩 | **Method combinations searchable** | Primary + secondary methods + strategy tags per question: "Green's theorem with a singularity," "Stokes with surface replacement," "substitution plus symmetry" |
| 📖 | **Traceable to source** | Every record keeps its source PDF and page range for verification |
| 🔒 | **Real questions only** | Practice mode returns only indexed questions, hides solutions by default, and never fabricates exercises |
| 🗂️ | **Persistent local memory** | The bank updates incrementally — add new PDFs anytime, the agent remembers what's already indexed |
| 🏠 | **Fully local data** | Your handouts, answers, and extracted text stay on your machine, git-ignored by default |

### 📐 Any Subject

**Any discipline works.** What matters is *how* a problem is solved, not which subject:

| Subject | Example methods |
|---|---|
| Math | Integration by parts, Lagrange multipliers, Green's theorem, Gram-Schmidt |
| Physics | Free-body diagram + Newton's 2nd law, energy conservation, Kirchhoff's laws |
| Chemistry | Redox half-reaction balancing, ICE tables |
| English / languages | Topic-sentence scanning, subject-verb agreement, synonym paraphrasing |
| History / humanities | Compare-contrast structure, sourcing analysis (who-when-why) |
| Coding | Binary search, DP with memoization, recursion with base case |

### 🤖 Which Agents?

The skill uses the standard `SKILL.md` format understood by **all major AI coding agents**:

| Agent | Skills location |
|---|---|
| **Codex** (CLI / desktop) | `~/.codex/skills/pdf-problem-method-practice/` |
| **Claude Code** | `~/.claude/skills/` or `.claude/skills/` in the project |
| **OpenCode** | `~/.config/opencode/skill/` or `.opencode/skill/` in the project |
| **Cursor** | `.cursor/skills/` in the project |
| Any `AGENTS.md`-reading agent | copy the folder into the repo and reference it from `AGENTS.md` |

### 🚀 Quick Start

**Step 1 — Install.** Clone this repo and copy the folder into your agent's skills directory (table above). For Codex:

```powershell
git clone https://github.com/YOUR-ACCOUNT/pdf-problem-method-practice.git
Copy-Item -Recurse .\pdf-problem-method-practice "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
```

Optional local PDF extraction:

```powershell
python -m pip install -e .
```

**Step 2 — Build your bank.** Put the problem PDFs in a project folder, then ask your agent:

```text
Use $pdf-problem-method-practice to organize this project's problem-set PDFs into a local practice bank.
```

The agent extracts pages, detects question/solution boundaries, classifies by method, and writes the bank to `problem_bank/`.

**Step 3 — Practice by method:**

```text
Give me five Green's theorem problems without solutions.
Give me Stokes' theorem problems that replace the original surface.
Which methods are currently available in this project?
```

Manual first-pass extraction:

```powershell
python scripts/extract_pdf_text.py .\problems --output .\problem_bank\extraction
```

Validate the bank after builds/updates:

```powershell
python scripts/validate_bank.py --bank .\problem_bank
```

### 🏠 Data & Privacy

The bank is intentionally local. Its JSONL records can contain full question and solution text, so `problem_bank/` is git-ignored by default. Do **not** commit course handouts, answer keys, extracted text, or generated study data unless you have permission to redistribute them.

### 🛠️ Development

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

### 📄 License

MIT. See [LICENSE](LICENSE).
