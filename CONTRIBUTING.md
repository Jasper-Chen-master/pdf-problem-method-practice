# 贡献指南

保持贡献的通用性：不要添加课程 PDF、专有答案或真实学生数据。测试优先使用合成夹具。

## 文档与代码规范

- 仓库内所有文档（`SKILL.md`、`README.md`、`references/`、`CONTRIBUTING.md`）与脚本的提示信息统一使用中文；面向 Agent 的标签 id、枚举值（如 `classified`、`active`）和代码标识符保持英文。
- 修改数据结构或校验器时，同步更新 `references/schemas.md` 并补充针对性测试——两侧必须保持一致。

## 提交前

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

全量测试通过后再开 PR。
