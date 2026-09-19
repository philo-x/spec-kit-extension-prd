# Spec Kit PRD Extension (`spec-kit-prd`)

[![Spec Kit Compatible](https://img.shields.io/badge/Spec%20Kit-Extension%20v1.0-blue.svg)](https://github.com/github/spec-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **核心设计定位**：  
> `spec.md = 唯一事实源 (Single Source of Truth)` ； `PRD Extension = 产品视图编译器 (PRD Compiler)`。  
> 不创建第二套需求事实，严禁反向修改 `spec.md`，只把 Spec Kit 的工程规约转换为契合产品经理与业务方阅读习惯的高质量 PRD。

---

## 📖 目录

1. [设计哲学与为什么要做](#一设计哲学与为什么要做)
2. [与现有 PRD 工具的核心差异](#二与现有-prd-工具的核心差异)
3. [核心工作流与生命周期](#三核心工作流与生命周期)
4. [核心命令 (Commands)](#四核心命令-commands)
5. [企业级 PRD 模板设计 (13节)](#五企业级-prd-模板设计)
6. [智能语义编译与三层分离](#六智能语义编译与三层分离)
7. [中间语义模型 (Intermediate Model)](#七中间语义模型)
8. [安装与配置指南](#八安装与配置指南)
9. [目录结构与渐进式披露](#九目录结构与渐进式披露)
10. [实战案例](#十实战案例)

---

## 一、设计哲学与为什么要做

在传统的规范驱动开发 (Spec-Driven Development, SDD) 实践中，通常面临两大痛点：
1. **工程师与产品经理的语境割裂**：`spec.md` 往往高度工程化、结构规约化，虽然便于开发团队做架构规划 (`/speckit.plan`) 和任务分解 (`/speckit.tasks`)，但业务方、产品总监与运营团队阅读门槛较高。
2. **“双文档漂移”的梦魇**：很多团队尝试单独写一份 PRD，再写一份 `spec.md`，导致需求一变更，两套事实源立即失步，互相冲突。

`spec-kit-prd` 扩展为解决上述矛盾而生：

```text
                           用户诉求 / 业务需求
                                    │
                                    ▼ /speckit.specify
                         ┌─────────────────────┐
                         │       spec.md       │ ◄── 唯一事实源 (Canonical Source)
                         └─────────────────────┘
                             │             │
                (只读编译投影)│             │ (工程架构拆解)
                             ▼             ▼
                ┌─────────────────┐   ┌─────────────────┐
                │ product/prd.md  │   │     plan.md     │
                │ (Stakeholder)   │   │ (Architecture)  │
                └─────────────────┘   └─────────────────┘
```

- **单向流动 (Unidirectional Projection)**: `spec.md ──> prd.md`。
- **严禁逆向流动 (`prd.md ──X──> spec.md`)**: 发现业务缺陷或需求不全时，**必须修改 `spec.md`**（或通过 `/speckit.clarify` 澄清），然后重新运行 `/speckit.prd.generate`。
- **WHAT / WHY Only，零 HOW 泄漏**: PRD 严禁包含具体数据库表名、SQL、内部 API 路由、技术框架选型等工程实现细节，保持纯粹的业务视角。

---

## 二、与现有 PRD 工具的核心差异

市场上现有的 PRD 技能多为散落的 Prompt 拼盘，而 `spec-kit-prd` 是一套**提炼共识并去除冲突的“PRD 编译流水线”**：

| 维度 | 普通 PRD Prompt / 生成技能 | 现有 Product Spec Extension | `spec-kit-prd` (本扩展) |
|:---|:---|:---|:---|
| **事实源定位** | 独立生成，可能脱离实际代码与规范 | 试图涵盖 PRFAQ、Lean PRD 等多种形式 | **严格以 `spec.md` 为唯一事实源，纯粹编译器定位** |
| **反向同步** | 随意修改，易产生双事实源冲突 | 部分工作流存在逆向同步隐患 | **坚决禁止反向修改事实源，杜绝双文档漂移** |
| **需求处理方式** | 简单总结、重写文本或摘要 | 模版填充 | **需求语义升维：功能能力 ≠ 业务规则 ≠ 验收标准** |
| **实现细节过滤** | 经常把技术实现/SQL/接口混入文档 | 包含技术设计章节 (HOW) | **严格过滤 HOW，只保留 WHAT 与 WHY** |
| **待确认问题处理** | AI 经常自作主张臆造业务答案 | 未作强制约束 | **`[NEEDS CLARIFICATION]` 原样透传，严禁 AI 擅自代答** |
| **可追溯性** | 无系统溯源 | 章节级简单对应 | **条目级双向追溯矩阵 (Traceability Matrix)** |
| **一致性审查** | 生成即结束，无内置校验 | 基础检查 | **提供专有 `/speckit.prd.review` 进行 8 维门禁硬审** |

---

## 三、核心工作流与生命周期

```text
用户需求
   │
   ▼
/speckit.specify ───> spec.md (唯一事实源)
                         │
                         ├──────────────────────────────┐
                         ▼                              ▼
               /speckit.prd.generate               /speckit.plan
                         │                              │
                         ▼                              ▼
                  product/prd.md                     plan.md
                         │                              │
                         ▼                              ▼
                /speckit.prd.review              /speckit.tasks
                         │                              │
                         ▼                              ▼
                  评审通过 / 修订推进              代码实现与测试
```

---

## 四、核心命令 (Commands)

### 1. `/speckit.prd.generate` (别名: `/speckit.prd.gen`)

- **输入**: `specs/<feature>/spec.md`
- **输出**: `specs/<feature>/product/prd.md`
- **执行过程**:
  1. 解析活跃特性规范文件；
  2. 执行需求语义分析与分类；
  3. 构建中间语义模型；
  4. 渲染为 13 节企业级 PRD；
  5. 执行 8 维质量门禁自查与读者测试 (Reader Test)；
  6. 持久化输出并反馈统计。

### 2. `/speckit.prd.review`

- **输入**: `spec.md` 与 `prd.md`
- **输出**: 终端审查报告或 `specs/<feature>/product/review-report.md`
- **8 维核心审查门禁**:
  1. **完整性 (Completeness)**: 是否有遗漏的 `FR-xxx` 或验收场景？
  2. **保真度与零幻觉 (Fidelity)**: 是否凭空增加了未经立项的功能？
  3. **无实现细节泄漏 (No HOW Leakage)**: 是否混入了数据库、接口或框架？
  4. **三层语义分离 (Semantic Separation)**: 功能需求、业务规则与验收标准是否清晰解耦？
  5. **待确认项严格透传 (Preserve Clarification)**: `[NEEDS CLARIFICATION]` 是否被原样保留，而非被 AI 擅自解答？
  6. **范围对齐 (Scope Alignment)**: In-Scope / Out-of-Scope 是否一致？
  7. **验收标准保真 (AC Fidelity)**: Gherkin 格式是否规范，逻辑是否忠实于原场景？
  8. **追溯矩阵完整度 (Traceability Integrity)**: 第 13 节是否 100% 覆盖闭环？

---

## 五、企业级 PRD 模板设计

结合 SaaS 与复杂企业业务系统特点，模板内置 13 个标准化章节：

```markdown
# [Feature Name] PRD
> Generated from: `spec.md`
> Source of Truth: `spec.md`
> Generated: YYYY-MM-DD

## 1. 背景与问题
### 1.1 背景
### 1.2 当前问题
### 1.3 为什么现在需要解决

## 2. 目标与成功标准
### 2.1 Goals
### 2.2 Non-Goals
### 2.3 Success Metrics

## 3. 用户与使用场景
### 3.1 用户角色 (Personas)
### 3.2 核心用户场景 (Jobs To Be Done)

## 4. 需求范围
### 4.1 本期范围 (In Scope)
### 4.2 非本期范围 (Out of Scope)

## 5. 功能需求
### 5.1 [功能模块]
#### 用户目标
#### 功能说明
#### 核心能力 (FR-01, FR-02...)
#### 优先级 (P0 / P1 / P2)

## 6. 业务规则 (BR-01, BR-02...)
<!-- 核心隔离层：独立定义业务不变量、数值上限、计算公式、时效冻结 -->

## 7. 数据与字段规则 (按需条件生成)
<!-- 核心字段定义、格式校验、必填性 -->

## 8. 权限与状态规则 (按需条件生成)
<!-- 角色权限矩阵、生命周期状态迁移机 -->

## 9. 异常与边界场景 (EX-01, EX-02...)

## 10. 验收标准 (AC-01, AC-02...)
<!-- 标准 Gherkin 行为驱动语法：Given-When-Then -->

## 11. 风险、依赖与约束

## 12. 待确认事项
<!-- 原样透传 [NEEDS CLARIFICATION: ...]，严禁自行假设 -->

## 13. 需求追溯矩阵 (Requirement Traceability Matrix)
| PRD 编号 | 类型 | PRD 条目简述 | spec.md 来源位置 | 完整性状态 |
```

---

## 六、智能语义编译与三层分离

区别于普通的大模型总结，`spec-kit-prd` 具备针对需求文本的**语义分类与升维识别**能力：

```text
spec.md 输入                                 语义识别与升维                        PRD 归属
─────────────────────────────────────────────────────────────────────────────────────────────
FR-001: Users MUST view their own reports. ──> 用户端到端能力 (Capability) ──────> 第 5 节 功能需求 (FR-02)
FR-002: Users MUST NOT report > 24 hours. ───> 业务硬性不变量 (Invariant) ────────> 第 6 节 业务规则 (BR-01)
FR-003: Reports older than N days locked. ───> 时效约束 (Temporal Rule) ──────────> 第 6 节 业务规则 (BR-02)
Scenario: Given ... When ... Then ...      ──> 行为验证 (Verification) ───────────> 第 10 节 验收标准 (AC-01)
FR-007: [NEEDS CLARIFICATION: N is 7 or 30] ─> 未决分歧 (Pending Decision) ───────> 第 12 节 待确认事项 (OQ-01)
```

### 三层分离铁律：
1. **功能需求 (Functional Capability)**：解决“用户能调用什么能力”。
2. **业务规则 (Business Rules)**：解决“底层业务的不变量与约束”，独立于具体 UI 交互与实现。
3. **验收标准 (Acceptance Criteria)**：解决“在特定前置条件下，操作产生的客观确定性结果”，支持直接派生自动化测试。

---

## 七、中间语义模型

编译器在 Prompt 层先将规约解析为结构化的中间语义模型 (Intermediate Representation)，再行渲染，保证了架构的解耦与稳定性：

```yaml
product:
  problem: { background, current_problems, why_now }
  goals: []
  non_goals: []
  users: []
  scenarios: []
  features:
    - id: "FR-01"
      name: string
      user_value: string
      description: string
      priority: "P0"
      source_refs: []
  business_rules:
    - id: "BR-01"
      rule: string
      violation_behavior: string
      source_refs: []
  permissions: []
  state_rules: []
  data_rules: []
  edge_cases: []
  acceptance_criteria:
    - id: "AC-01"
      given: string
      when: string
      then: string
      source_refs: []
  success_metrics: []
  open_questions: []
  dependencies: []
```

---

## 八、安装与配置指南 (Installation & Configuration)

### Installation

Install the v0.1.0 release archive from a Spec Kit project:

```bash
specify extension add prd --from https://github.com/philo-x/spec-kit-extension-prd/archive/refs/tags/v0.1.0.zip
```

For local development:

```bash
specify extension add --dev /path/to/spec-kit-extension-prd
```

Verify the extension, its registered commands, and template:

```bash
specify extension list
specify extension info prd
```

Remove the extension with:

```bash
specify extension remove prd
```

### Configuration

The extension works out-of-the-box with sensible defaults. To customize:

Copy the configuration template to your project:
```bash
cp .specify/extensions/prd/prd-config.template.yml .specify/extensions/prd/prd-config.yml
```

Key configuration options in `prd-config.yml`:
- `general.language`: Output language (`zh-CN`, `en`, `auto`)
- `output.path`: Output file template (default: `specs/{feature}/product/prd.md`)
- `policy.strict_separation`: Enforce Functional Requirements ≠ Business Rules ≠ Acceptance Criteria (`true`)
- `policy.no_how_leakage`: Forbid implementation leaks such as SQL, schemas, or frameworks (`true`)
- `policy.preserve_unresolved`: Pass through `[NEEDS CLARIFICATION]` verbatim (`true`)
- `policy.traceability_matrix`: Generate Section 13 Traceability Matrix (`true`)

---

## 九、目录结构与渐进式披露

遵循 Spec Kit 与 Agent Skills 的**渐进式披露 (Progressive Disclosure)** 设计模式，核心命令提示词保持轻盈干练，规则细节模块化按需加载：

```text
spec-kit-extension-prd/
├── extension.yml                      # 扩展元数据清册 (Spec Kit v1.0 规范)
├── config-template.yml                # 扩展配置文件模板
├── README.md                          # 完整说明文档
├── LICENSE                            # MIT 开源协议
├── CHANGELOG.md                       # 版本发布日志
├── commands/
│   ├── speckit.prd.generate.md        # /speckit.prd.generate 命令
│   └── speckit.prd.review.md          # /speckit.prd.review 命令
├── templates/
│   └── prd-template.md                # 13 节企业级标准 PRD 模板
├── references/                        # 深度规则指南 (渐进式披露)
│   ├── prd-principles.md              # 编译器定位与核心原则
│   ├── requirement-classification.md  # 语义分类模型与决策树
│   ├── business-rules.md              # 业务规则建模与去 UI 化指南
│   ├── acceptance-criteria.md         # Gherkin 验收标准编写规范
│   └── quality-checklist.md           # 8 维质量门禁与 Reader Test 规程
├── docs/                              # 系统级详细文档
│   ├── architecture.md                # 架构设计与编译流水线说明
│   └── user-guide.md                  # 用户实操指南与最佳实践
├── examples/                          # 真实企业级案例 (工时报工系统)
│   └── work-report/
│       ├── spec.md                    # 原始特征规约事实源
│       └── product/
│           ├── prd.md                 # 编译生成的标准 PRD
│           └── review-report.md       # 一致性审阅报告
└── scripts/
    └── validate_extension.py          # 扩展自动化校验脚本
```

---

## 十、实战案例

本仓库内置了一个完整的企业级报工系统示例，位于 `examples/work-report/`：
- [`spec.md`](examples/work-report/spec.md): 输入的工程规范，包含用户故事、FR-001 ~ FR-007 及 `[NEEDS CLARIFICATION]`。
- [`product/prd.md`](examples/work-report/product/prd.md): 由编译器转换生成的 13 节高质量 PRD，体现了三层分离、Gherkin 验收用例与追溯矩阵。
- [`product/review-report.md`](examples/work-report/product/review-report.md): 运行 `/speckit.prd.review` 的输出范例，全绿通过 8 维门禁。

---

## 📄 License

本项目采用 [MIT License](LICENSE) 开源协议。
