# {Feature Name} 产品需求文档 (PRD)

> **文档元数据**
> - **来源规范 (Source of Truth)**: [`spec.md`](../spec.md)
> - **生成状态**: 衍生自规范 (Derived Product View) - **禁止反向修改事实源**
> - **生成时间**: {YYYY-MM-DD}
> - **版本**: v{Version} (对应 spec.md)

---

## 1. 背景与问题

### 1.1 背景
<!-- 业务背景、行业现状、产品当前所处阶段及历史沿革 -->
{Background description derived from spec.md context}

### 1.2 当前问题
<!-- 痛点描述：当前阻碍业务或用户达成目标的核心矛盾与障碍 -->
{Pain points and current problems identified in spec.md}

### 1.3 为什么现在需要解决
<!-- 业务紧迫性、战略时机、延期后果或价值放大点 -->
{Strategic urgency and rationale for addressing this feature now}

---

## 2. 目标与成功标准

### 2.1 Goals
<!-- 本次迭代明确要达成的业务与产品目标（定量/定性） -->
- **G-01**: {Goal 1 description}
- **G-02**: {Goal 2 description}

### 2.2 Non-Goals
<!-- 本次迭代明确不作为目标的内容，防止范围蔓延 -->
- **NG-01**: {Non-goal 1 description}
- **NG-02**: {Non-goal 2 description}

### 2.3 Success Metrics
<!-- 衡量成功的关键产品/业务指标与衡量方式 -->
| 指标编号 | 指标名称 | 当前基线 | 目标值 | 衡量维度 / 统计方式 |
|:---|:---|:---|:---|:---|
| **SM-01** | {Metric Name} | {Baseline} | {Target} | {Measurement method} |

---

## 3. 用户与使用场景

### 3.1 用户角色 (User Personas)
<!-- 核心利益相关者、最终使用者、运营/管理员角色定义 -->
| 角色编号 | 角色名称 | 角色定位与职责 | 核心痛点与诉求 |
|:---|:---|:---|:---|
| **ROLE-01** | {Role Name} | {Role definition} | {Core pain point} |

### 3.2 核心用户场景 (Core Scenarios)
<!-- 典型用户旅程与日常高频使用故事 (Jobs To Be Done) -->
- **场景 1: {Scenario Title}**
  - **前置条件**: {Preconditions}
  - **主干流程**: {Main journey steps}
  - **预期价值**: {Expected user outcome}

---

## 4. 需求范围

### 4.1 本期范围 (In Scope)
<!-- 本次功能交付确定的功能清单与边界 -->
- {In-scope item 1}
- {In-scope item 2}

### 4.2 非本期范围 (Out of Scope)
<!-- 明确未来规划或延期交付的功能特性 -->
- {Out-of-scope item 1}
- {Out-of-scope item 2}

---

## 5. 功能需求 (Functional Requirements)

<!-- 
三层分离原则 1：功能需求仅描述 WHAT/WHY，描述用户可用能力。
禁止将校验算法、时间期限、状态限制直接堆砌在功能描述中（提取到第6节业务规则）。
-->

### 5.1 {功能模块名称}

#### 5.1.1 模块说明与用户目标
- **对应用户故事**: {As a ... I want to ... So that ...}
- **用户目标**: {User goal}
- **功能概述**: {Feature overview}

#### 5.1.2 核心能力列表
| 功能编号 | 能力名称 | 用户价值与行为描述 | 优先级 | 溯源引用 |
|:---|:---|:---|:---|:---|
| **FR-01** | {Capability Name} | {WHAT user can do and WHY} | P0 / P1 / P2 | `spec.md#FR-xxx` |

---

## 6. 业务规则 (Business Rules)

<!-- 
三层分离原则 2：业务规则独立成章。
业务规则定义业务不变量（Invariant）、约束限制、计算公式、资格准入，独立于具体界面。
-->

### BR-01: {业务规则简述}
- **规则定义**: {Detailed business rule constraint, invariant, or limit}
- **适用场景**: {When and where this rule applies}
- **违规处理**: {Business feedback when rule is violated}
- **溯源引用**: `spec.md#FR-xxx` / `User Story x`

### BR-02: {业务规则简述}
- **规则定义**: {Detailed business rule constraint}
- **适用场景**: {When and where this rule applies}
- **违规处理**: {Business feedback when rule is violated}
- **溯源引用**: `spec.md#FR-xxx`

---

## 7. 数据与字段规则

<!-- 条件生成节：仅当 spec.md 存在具体数据实体、字段约束或计算口径时渲染 -->

### 7.1 核心数据对象与字段
| 实体/模块 | 字段名称 | 业务含义 | 必填 | 格式/取值范围 | 默认值 | 溯源引用 |
|:---|:---|:---|:---|:---|:---|:---|
| {Entity} | {Field} | {Description} | 是/否 | {Validation rule} | {Default} | `spec.md#FR-xxx` |

---

## 8. 权限与状态规则

<!-- 条件生成节：仅当 spec.md 存在权限控制矩阵或生命周期状态机时渲染 -->

### 8.1 角色权限矩阵
| 功能模块 / 操作 | {Role 1} | {Role 2} | {Role 3} | 补充约束 |
|:---|:---|:---|:---|:---|
| {Operation A} | 允许 (无限制) | 仅本人数据 | 禁止 | {Note} |

### 8.2 业务状态流转
<!-- 状态迁移规则：初始状态 -> 触发动作/条件 -> 目标状态 -->
- **状态迁移表**:
  | 起始状态 | 触发动作 (Trigger) | 约束前置条件 (Condition) | 目标状态 |
  |:---|:---|:---|:---|
  | {Initial} | {Action} | {Condition (BR-xx)} | {Target} |

---

## 9. 异常与边界场景

<!-- 极端用例、网络/并发/配额/并发冲突等业务级异常处理 -->
| 场景编号 | 异常/边界条件 | 业务表现与用户提示 | 降级/恢复机制 | 溯源引用 |
|:---|:---|:---|:---|:---|
| **EX-01** | {Edge condition} | {User feedback / error behavior} | {Recovery action} | `spec.md#Edge Cases` |

---

## 10. 验收标准 (Acceptance Criteria)

<!-- 
三层分离原则 3：验收标准采用 Gherkin 标准行为驱动语言 (Given-When-Then)。
每个验收标准必须能够被独立验证。
-->

### AC-01: {验收场景名称}
```gherkin
Given {初始业务状态与前置条件}
When  {用户执行的操作或系统触发的事件}
Then  {预期的业务结果、状态变更及用户提示}
```
- **关联功能**: FR-01
- **关联业务规则**: BR-01
- **溯源引用**: `spec.md#Scenario x`

### AC-02: {验收场景名称}
```gherkin
Given {初始业务状态与前置条件}
When  {用户执行的操作或系统触发的事件}
Then  {预期的业务结果、状态变更及用户提示}
```
- **关联功能**: FR-02
- **关联业务规则**: BR-02
- **溯源引用**: `spec.md#Scenario y`

---

## 11. 风险、依赖与约束

### 11.1 业务与技术依赖
- **DEP-01**: {Dependency description and impact}

### 11.2 潜在风险与应对预案
- **RSK-01**: {Risk description} -> **应对预案**: {Mitigation strategy}

### 11.3 业务与法律合规约束
- **CON-01**: {Constraint description}

---

## 12. 待确认事项 (Open Questions)

<!-- 
严格保真原则：必须原样透传 spec.md 中的所有 [NEEDS CLARIFICATION] 标记。
严禁 AI 自行假设或虚构业务答案！
-->
| 事项编号 | 待确认问题与背景 | 影响范围 | 建议方案 / 决策人 | 状态 | 溯源来源 |
|:---|:---|:---|:---|:---|:---|
| **OQ-01** | `[NEEDS CLARIFICATION: {Verbatim question from spec.md}]` | {Impact} | {Suggested options if any} | 待确认 (Pending) | `spec.md#Line` |

---

## 13. 需求追溯矩阵 (Requirement Traceability Matrix)

<!-- 确保 PRD 中的每一项关键需求均可追溯至规范，且规范中的需求未被遗漏 -->
| PRD 编号 | 类型 | PRD 需求简述 | `spec.md` 溯源编号 | 完整性核验 |
|:---|:---|:---|:---|:---|
| **FR-01** | 功能需求 | {Summary} | `FR-001` | [x] 完全覆盖 |
| **BR-01** | 业务规则 | {Summary} | `FR-002` / `Scenario 2` | [x] 完全覆盖 |
| **BR-02** | 业务规则 | {Summary} | `FR-003` | [x] 完全覆盖 |
| **AC-01** | 验收标准 | {Summary} | `Scenario 1` | [x] 完全覆盖 |
| **OQ-01** | 待确认项 | {Summary} | `[NEEDS CLARIFICATION]` | [x] 完整透传 |
