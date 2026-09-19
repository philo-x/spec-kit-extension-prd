# Spec Kit PRD Extension: 用户使用与实战指南

本指南面向产品经理、研发团队及敏捷教练，详细说明如何安装、配置以及在日常敏捷规范开发生命周期中使用 `spec-kit-prd` 扩展。

---

## 一、快速上手 (Quick Start)

### 1. 安装扩展 (Installation)

在已初始化 Spec Kit 的工程目录下，使用 `--dev` 参数进行本地安装：

```bash
# 从本地路径安装 prd 扩展
specify extension add --dev /path/to/spec-kit-extension-prd

# 验证安装是否成功
specify extension list
```

如果成功安装，`specify extension list` 输出将包含 `prd`，且当前集成的 AI 助手（如 Claude Code, Gemini CLI, Cursor）会自动加载以下命令：
- `/speckit.prd.generate` (别名: `/speckit.prd.gen`)
- `/speckit.prd.review`

---

## 二、扩展配置 (Configuration)

扩展默认开箱即用，无需额外配置即可工作。若需要针对团队规范自定义语言或输出规则：

### 1. 生成项目配置文件

```bash
# 拷贝配置模板
cp .specify/extensions/prd/prd-config.template.yml .specify/extensions/prd/prd-config.yml
```

### 2. 配置选项解析

```yaml
general:
  # 目标 PRD 文档语言: "zh-CN" (默认中文), "en" (英文), "auto" (跟随 spec.md)
  language: "zh-CN"

output:
  # PRD 输出文件路径模板，支持 {feature} 变量
  path: "specs/{feature}/product/prd.md"
  # 审阅报告输出路径模板
  review_report_path: "specs/{feature}/product/review-report.md"
  # 覆盖已有文件前是否自动确认
  overwrite: true

policy:
  # 严格三层分离：功能需求 ≠ 业务规则 ≠ 验收标准
  strict_separation: true
  # 严禁实现细节泄漏 (禁止代码库、SQL、数据库表名、HTTP 状态码等)
  no_how_leakage: true
  # 待澄清事项原样透传 (严禁 AI 自作主张解答 [NEEDS CLARIFICATION])
  preserve_unresolved: true
  # 自动生成双向追溯矩阵表格
  traceability_matrix: true
  # 条件节开关 ("auto" | "always" | "never")
  conditional_sections:
    data_and_fields: "auto"        # 数据与字段规则
    permissions_and_state: "auto"  # 权限与状态流转规则

review:
  # 质量门禁级别: "standard" (阻止 FAIL) 或 "strict" (警告即阻止)
  quality_gate: "standard"
  # 是否持久化保存 review-report.md 报告文件
  save_report: true
```

---

## 三、命令使用详解 (Commands)

### 1. `/speckit.prd.generate` (别名 `/speckit.prd.gen`)

从当前活跃特性（或指定特性）的工程规范 `spec.md` 编译生成企业级 PRD。

#### 常见调用形式：
- `/speckit.prd.generate`  
  *自动识别当前工作分支关联的活跃特性，读取 `specs/<feature>/spec.md` 并生成 PRD。*
- `/speckit.prd.generate 001-work-report`  
  *指定生成特性目录为 `specs/001-work-report` 的 PRD。*
- `/speckit.prd.generate specs/payroll/spec.md`  
  *显式指定源文件路径。*

#### 输出结果：
- 目标文件：`specs/<feature>/product/prd.md`
- 并在对话框中输出编译成果度量：
  ```text
  ✅ 成功编译 PRD: specs/001-work-report/product/prd.md
  📊 包含度量:
     - 🎯 核心目标: 2 项, 非目标: 2 项
     - 🧩 功能需求模块: 1 个 (包含 2 项核心能力)
     - 📜 独立业务规则: 2 条 (单日上限约束、历史时效冻结)
     - 🧪 行为验收标准: 2 个 (Gherkin AC)
     - ❓ 待确认事项: 1 项 ([NEEDS CLARIFICATION] 完整保留)
  ```

---

### 2. `/speckit.prd.review`

对已生成的 `prd.md` 开展针对 `spec.md` 的可追溯性与保真度审计。

#### 常见调用形式：
- `/speckit.prd.review`
- `/speckit.prd.review 001-work-report`

#### 审阅检查要点：
1. **完整性**: `spec.md` 是否有被遗漏的需求或场景？
2. **零幻觉**: PRD 是否凭空加入了未经立项的功能？
3. **无实现泄漏**: 是否存在 SQL、数据库表结构或接口实现细节？
4. **三层解耦**: 业务规则是否独立于界面表述？
5. **待确认事项**: `[NEEDS CLARIFICATION]` 是否被 AI 擅自填补？
6. **全链路溯源**: Section 13 追溯矩阵是否 100% 覆盖闭环？

---

## 四、推荐的最佳实操流 (Best Practices)

```text
       Step 1: 编写需求与技术规格
               /speckit.specify
                      │
                      ▼
               specs/<feature>/spec.md
                      │
       Step 2: 编译为业务与产品视图
               /speckit.prd.generate
                      │
                      ▼
               specs/<feature>/product/prd.md
                      │
       Step 3: 自动质量审阅与人工确认
               /speckit.prd.review
                      │
                      ├───────────────────────┐
                      ▼                       ▼
                [存在疑问/遗漏]          [核验通过 APPROVED]
                      │                       │
               在 spec.md 中修订        推进技术设计
               (不直接在PRD中改)        /speckit.plan
                      │                       │
               重新 generate            研发拆解 tasks
```

### 关键经验法则：
- **永远不要为了方便直接修改 `prd.md`**：PRD 是事实源的投影像。如果发现规则有变，修改 `spec.md` 后重新执行 `/speckit.prd.generate`。这保证了代码测试、技术方案与产品文档永远基于同一套基准。
- **让非技术业务方直接审阅 `prd.md`**：业务方无需理解 Spec Kit 的工程细节，他们只需阅读 PRD 的前 6 节和第 12 节，即可在 5 分钟内完成业务对齐。
- **充分利用验收标准对齐测试**：第 10 节验收标准基于 Given-When-Then 编写，测试工程师可直接复制到测试管理工具中作为自动化测试套件。
