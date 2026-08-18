# PDF Problem Method Practice

[English](#english) | [中文](#中文)

## English

`pdf-problem-method-practice` is a Codex skill for turning problem-set PDFs into a local, solution-grounded practice bank. Its central idea is simple: organize problems by **the method actually used to solve them**, rather than only by chapter, file, or broad topic.

### Why It Helps

- **Practice one method until it sticks.** Retrieve a concentrated set of real problems that all use a target technique, such as Green's theorem, Lagrange multipliers, or Gram-Schmidt. This is more effective than mixed, chapter-order drilling when you are trying to internalize a single procedure.
- **Classify from evidence, not keywords.** When a solution is available, the primary method is based on the visible solution steps. A theorem merely named in the prompt is not enough.
- **Search method combinations.** Each question can have a primary method, material secondary methods, and separate strategy tags. This supports queries such as “Green's theorem with a singularity/hole,” “Stokes' theorem where the surface is replaced,” or “coordinate change plus symmetry.”
- **Keep tactical details searchable.** Orientation handling, symmetry, boundary comparison, replacing a surface, and closing a surface with a cap are stored as strategies rather than conflated with the main method.
- **Stay tied to the source.** Every record keeps its source PDF and page range, so ambiguous extraction or classification can be checked against the original document.
- **Preserve a local study memory.** Re-running the workflow updates a structured local bank with canonical tags, aliases, indexes, review records, and unresolved items.
- **Protect the learning flow.** Practice retrieval returns only real indexed questions and hides solutions by default. It never invents filler exercises to meet a requested count.

### Install

Clone this repository, then copy or link the `pdf-problem-method-practice` folder into your Codex skills directory.

```powershell
git clone https://github.com/YOUR-ACCOUNT/pdf-problem-method-practice.git
Copy-Item -Recurse .\pdf-problem-method-practice "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
```

Install the optional PDF extractor dependency when you want to extract text locally:

```powershell
python -m pip install -e .
```

### Use

Put PDFs in the project you want to study, then ask Codex:

```text
Use $pdf-problem-method-practice to organize the problem PDFs in this project.
```

Example retrieval requests:

```text
Give me five Green's theorem problems without solutions.
Give me Stokes' theorem problems that replace the original surface.
Which methods are currently available in this project?
```

For a first extraction pass, run:

```powershell
python scripts/extract_pdf_text.py .\problems --output .\problem_bank\extraction
```

After Codex creates or updates the bank, validate it:

```powershell
python scripts/validate_bank.py --bank .\problem_bank
```

### Data And Privacy

The bank is intentionally local. Its JSONL records can contain full question and solution text, so `problem_bank/` is ignored by Git by default. Do not commit course handouts, answer keys, extracted question text, or generated study data unless you have permission to redistribute them.

### Development

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

### License

MIT. See [LICENSE](LICENSE).

## 中文

`pdf-problem-method-practice` 是一个面向 Codex 的技能：它把题集 PDF 整理成本地、可持续维护的练习题库。它不只按章节或文件名归类，而是按**题目答案中实际使用的解题方法**分类。

### 核心优势

- **集中练熟一种方法。** 你可以一次调出一批真正使用同一方法的题，例如格林公式、拉格朗日乘子法或 Gram-Schmidt 正交化。这样更适合把一个完整解题流程练到熟练，而不是按章节混做。
- **依据答案步骤分类，而不是关键词匹配。** 有参考答案时，主方法必须能从可见的解题步骤中得到支持；题干仅提到某个定理并不足以成为标签依据。
- **支持方法联合搜索。** 每题可记录主方法、实质性的次要方法和独立策略标签，因此可检索“含奇点/孔洞的格林公式”“替换曲面的 Stokes 定理”“坐标变换加对称性”等组合。
- **策略也能单独检索。** 曲线或曲面的定向、对称性化简、边界候选比较、补面、替换曲面等会作为策略保存，不会和主方法混为一谈。
- **可回溯到原题。** 每条记录保留原 PDF 路径和页码范围；遇到抽取或分类有疑问时，可以直接回到原文件核对。
- **本地长期记忆。** 题库会保存规范标签、别名、索引、分类复核记录和未解决项；后续更新 PDF 时可以继续维护，而不是每次从零开始。
- **保持练习闭环。** 检索时只返回已经索引的真实题目，默认不显示答案，也不会为了凑题数虚构练习题。

### 安装

克隆仓库后，将 `pdf-problem-method-practice` 文件夹复制或链接到 Codex 的 skills 目录：

```powershell
git clone https://github.com/YOUR-ACCOUNT/pdf-problem-method-practice.git
Copy-Item -Recurse .\pdf-problem-method-practice "$env:USERPROFILE\.codex\skills\pdf-problem-method-practice"
```

若需要在本地抽取 PDF 文本，安装依赖：

```powershell
python -m pip install -e .
```

### 使用方式

把题目 PDF 放进要学习的项目后，对 Codex 说：

```text
使用 $pdf-problem-method-practice 整理这个项目里的题目 PDF，按实际解题方法建立本地题库。
```

例如：

```text
给我五道格林公式题，不要显示答案。
给我需要替换曲面的 Stokes 定理题。
当前项目里有哪些可练习的方法？
```

第一次抽取 PDF 文本时可运行：

```powershell
python scripts/extract_pdf_text.py .\problems --output .\problem_bank\extraction
```

题库创建或更新后，运行：

```powershell
python scripts/validate_bank.py --bank .\problem_bank
```

### 数据与隐私

题库设计为只在本地保存。其 JSONL 文件可能包含完整题目与解答文本，因此默认被 Git 忽略。除非你拥有再分发权限，不要提交课程讲义、答案、抽取后的题目文本或生成的题库数据。

### 开发

```powershell
python -m pip install -e ".[dev]"
python -m pytest
```

### 许可证

MIT，见 [LICENSE](LICENSE)。
