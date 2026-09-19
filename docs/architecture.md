# Spec Kit PRD Extension: 系统架构与编译模型设计

本文档深入阐释 `spec-kit-prd` 扩展的架构原理、编译流水线、中间语义模型设计以及与 Spec-Driven Development (SDD) 生命周期的集成机制。

---

## 一、架构全景与设计哲学

### 1. 唯一事实源与单向编译模型 (Single Source of Truth & Unidirectional Compiler)

```text
       ┌─────────────────────────────────────────────────────────────┐
       │                 用户需求 / 业务痛点                         │
       └──────────────────────────────┬──────────────────────────────┘
                                      │
                                      ▼ /speckit.specify
       ┌─────────────────────────────────────────────────────────────┐
       │                   specs/<feature>/spec.md                   │
       │           ★ 规范驱动开发唯一事实源 (Canonical Source)        │
       └──────────────┬──────────────────────────────┬───────────────┘
                      │                              │
                      │ [编译投影: 只读]             │ [工程实现拆解]
                      ▼ /speckit.prd.generate        ▼ /speckit.plan
       ┌──────────────────────────────┐ ┌─────────────────────────────┐
       │ specs/<feature>/product/     │ │ specs/<feature>/plan.md     │
       │ prd.md                       │ │ (技术方案与架构设计)         │
       │ (产品经理/业务方利益相关者视图)│ └──────────────┬──────────────┘
       └──────────────┬───────────────┘                │
                      │                                ▼ /speckit.tasks
                      ▼ /speckit.prd.review            tasks.md
       ┌──────────────────────────────┐                │
       │ 一致性与保真度审计报告       │                ▼ /speckit.implement
       │ (8 维门禁 / 零幻觉 / 溯源)    │              代码与自动化测试
       └──────────────────────────────┘
```

#### 关键架构约束：
1. **严格单向性 (Unidirectional Projection)**:
   - 流向为 `spec.md ──> prd.md`。
   - **严禁逆向流动 (`prd.md ──X──> spec.md`)**。避免出现两个可编辑文档同时维护业务事实导致的“双事实源漂移 (Dual Document Drift)”。
2. **职责边界清晰 (Separation of Concerns)**:
   - `spec.md`: 面向规范驱动体系的统一事实源，记录 WHAT & WHY 以及可执行规范。
   - `prd.md`: 面向业务与产品利益相关者（PM、运营、业务方）的可读视图，强调业务价值、使用场景与规则解耦。
   - `plan.md`: 面向开发工程团队的技术架构方案，定义技术栈、接口契约与数据模型（HOW）。

---

## 二、PRD 编译流水线 (The Compilation Pipeline)

`spec-kit-prd` 将 PRD 生成视作一种**“语义编译”**过程，而非简单的“文本润色”或“内容摘要”。整个管道分为 6 个确定性阶段：

```text
┌───────────┐    ┌────────────────────┐    ┌───────────────────────┐
│  Phase 1  │───>│      Phase 2       │───>│        Phase 3        │
│ 特征解析  │    │  需求语义分类分析  │    │ 中间语义模型 (IR) 构建│
│ Feature   │    │ Semantic Classifier│    │ Intermediate Model    │
└───────────┘    └────────────────────┘    └───────────────────────┘
                                                       │
                                                       ▼
┌───────────┐    ┌────────────────────┐    ┌───────────────────────┐
│  Phase 6  │<───│      Phase 5       │<───│        Phase 4        │
│ 文档持久化│    │ 质量自检与读者测试 │    │ PRD 结构化渲染        │
│ Emit File │    │ Self QA/Reader Test│    │ Template Rendering    │
└───────────┘    └────────────────────┘    └───────────────────────┘
```

### 各阶段详解：

1. **Phase 1: 特征解析 (Feature Ingestion)**
   - 自动推断或从参数接收当前活跃特性（Feature Slug），加载 `specs/<feature>/spec.md`。
   - 读取配置规则 `.specify/extensions/prd/prd-config.yml`。

2. **Phase 2: 需求语义分类分析 (Semantic Requirement Analysis)**
   - 依据 [`references/requirement-classification.md`](../references/requirement-classification.md) 的决策树，对 `spec.md` 中的每个文本段落和需求编号进行语义识别。
   - 识别出：用户意图、业务规则、数据规则、权限规则、状态跃迁、边界用例、验收用例以及待确认项。

3. **Phase 3: 中间语义模型构建 (Intermediate Semantic Model Construction)**
   - 在内存中将提炼出的要素组装为结构化的业务逻辑中间表示 (IR)。
   - 模型解耦了输入格式与输出模板，未来若需要输出 Confluence 格式、飞书文档或精简版 PRD，仅需更换渲染器即可。

4. **Phase 4: PRD 结构化渲染 (PRD Rendering)**
   - 根据 [`templates/prd-template.md`](../templates/prd-template.md) 进行填充。
   - 实行**三层明确分离**：功能需求 (Section 5) ≠ 业务规则 (Section 6) ≠ 验收标准 (Section 10)。
   - 条件节动态控制：仅在 spec 具备相应内容时才渲染字段规则与状态规则。
   - 严格保留 `[NEEDS CLARIFICATION]` 标记至第 12 节，严禁 AI 擅自臆测。
   - 生成完整的双向需求追溯矩阵（Section 13）。

5. **Phase 5: 质量自检与读者测试 (Self-QA & The Reader Test)**
   - 依据 [`references/quality-checklist.md`](../references/quality-checklist.md) 的 8 维门禁自查。
   - 执行 Anthropic `doc-coauthoring` 读者测试，确保文字干练、层次鲜明、受众友好。

6. **Phase 6: 输出与统计 (File Emission & Statistics)**
   - 将最终 PRD 写入 `specs/<feature>/product/prd.md`。
   - 汇总核心指标（模块数、规则数、AC数、待确认项数）并在终端提供反馈。

---

## 三、中间语义模型架构 (Intermediate Product Model Schema)

中间语义模型是整个编译器的心脏，其逻辑数据结构定义如下：

```yaml
# Product Requirement Intermediate Model (PRD-IR)
product_model:
  meta:
    feature_slug: string
    feature_name: string
    canonical_spec_path: string
    compiled_at: ISO8601_Timestamp
    version: string

  context:
    background: string               # 行业/业务背景
    problem_statement: string        # 当前核心痛点
    why_now: string                  # 解决时机与紧迫性

  objectives:
    goals:                           # 明确目标清单 (G-xx)
      - id: string
        description: string
    non_goals:                       # 排除范围 (NG-xx)
      - id: string
        description: string
    success_metrics:                 # 衡量指标 (SM-xx)
      - id: string
        name: string
        baseline: string
        target: string
        measurement_method: string

  users_and_scenarios:
    personas:                        # 目标用户画像
      - id: string
        name: string
        responsibilities: string
        core_pain_point: string
    scenarios:                       # 典型业务使用场景 (JTBD)
      - id: string
        title: string
        preconditions: string
        journey: [string]
        expected_outcome: string

  scope_boundary:
    in_scope: [string]               # 本期交付范围
    out_of_scope: [string]           # 延期/未来范围

  functional_requirements:           # 功能需求 (WHAT/WHY)
    - id: string                     # FR-01
      module_name: string
      user_goal: string
      description: string
      core_capabilities: [string]
      priority: "P0" | "P1" | "P2"
      source_spec_refs: [string]     # 对应 spec.md 中的行或条目编号

  business_rules:                    # 业务规则 (独立解耦的业务不变量)
    - id: string                     # BR-01
      name: string
      archetype: "constraint" | "calculation" | "temporal" | "eligibility"
      definition: string
      scope: string
      violation_behavior: string
      source_spec_refs: [string]

  data_and_fields:                   # 数据与字段规则 (按需)
    entities:
      - entity_name: string
        fields:
          - name: string
            description: string
            required: boolean
            validation_rule: string
            default_value: string
            source_ref: string

  permissions_and_state:             # 权限与状态机 (按需)
    permission_matrix:
      roles: [string]
      operations:
        - action: string
          rules_per_role: map<string, string>
    state_machine:
      states: [string]
      transitions:
        - from_state: string
          to_state: string
          trigger: string
          guard_condition: string

  edge_cases:                        # 异常与边界场景
    - id: string
      condition: string
      handling_strategy: string
      source_ref: string

  acceptance_criteria:               # 验收标准 (Gherkin 规范)
    - id: string                     # AC-01
      title: string
      scenario_type: "happy_path" | "rule_violation" | "boundary" | "security"
      given: string
      when: string
      then: string
      linked_fr: [string]
      linked_br: [string]
      source_spec_refs: [string]

  dependencies_and_risks:
    dependencies: [string]
    risks:
      - risk: string
        mitigation: string
    constraints: [string]

  open_questions:                    # 待确认事项 ([NEEDS CLARIFICATION] 必须透传)
    - id: string                     # OQ-01
      verbatim_question: string
      impact_area: string
      candidate_options: [string]
      status: "Pending"
      source_spec_refs: [string]
```

---

## 四、双命令生命周期交互 (Generate & Review)

`spec-kit-prd` 遵循极简原则，第一阶段聚焦于两个高内聚的核心命令：

```text
                      spec.md (编辑完成)
                             │
                             ▼
                  /speckit.prd.generate
                             │
                             ▼ 生成
                      product/prd.md
                             │
                             ▼
                   /speckit.prd.review
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
      [发现不一致/遗漏/幻觉]               [审计通过 APPROVED]
            │                                 │
            ▼                                 ▼
       修订 spec.md                      推进工程架构设计
       (或 /speckit.clarify)             (/speckit.plan)
            │
            ▼
   重新执行 /speckit.prd.generate
```

- **/speckit.prd.generate**:
  - 执行 Phase 1 到 Phase 6。
  - 完成从工程规约到产品 PRD 的高质量编译。
- **/speckit.prd.review**:
  - 执行全面的可追溯性与一致性审计。
  - 运用 8 维质量门禁进行双向验证，确保无虚构需求、无实现细节泄漏、待确认事项原样透传。
