# PRD 质量核对与审阅规程 (Quality Checklist & Review Protocol)

本规程定义了 `spec-kit-prd` 体系中用于自检（生成阶段）和专项审阅（`/speckit.prd.review` 阶段）的 **8 维质量门禁模型 (The 8-Dimension Quality Gates)** 以及基于 Anthropic `doc-coauthoring` 的**读者测试准则 (The Reader Test)**。

---

## 一、8 维核心审阅门禁 (The 8 Quality Gates)

| 维度编号 | 检查维度 | 判定准则 | 严重级别 | 违规表现 |
|:---|:---|:---|:---|:---|
| **GATE-01** | **完整性 (Completeness)** | `spec.md` 中的所有用户故事、`FR-xxx` 条目与验收场景均已完整映射至 PRD。 | 阻断 (FAIL) | 遗漏了 `FR-003` 或遗漏了某个角色。 |
| **GATE-02** | **保真度与零幻觉 (Fidelity & No Hallucination)** | PRD 严禁凭空发明未在 `spec.md` 中提及的新功能、附加模块或未经证实的业务逻辑。 | 阻断 (FAIL) | `spec.md` 未提及通知，PRD 自行增加了“短信与邮件通知模块”。 |
| **GATE-03** | **无实现细节泄漏 (No HOW Leakage)** | PRD 仅描述 WHAT 和 WHY，严禁出现底层架构、数据库表字段、内部 API 路由、HTTP 状态码及技术选型。 | 阻断 (FAIL) | 出现 "POST /api/v1/work-hours" 或 "新增 t_report 表"。 |
| **GATE-04** | **三层语义分离 (Semantic Separation)** | 功能需求 (Section 5)、业务规则 (Section 6) 与验收标准 (Section 10) 严格解耦。 | 警告 (WARN) | 将“单日不能超过24小时”写在功能描述中，未提取为独立 BR。 |
| **GATE-05** | **待确认项严格透传 (Open Questions Preservation)** | `spec.md` 中所有带有 `[NEEDS CLARIFICATION]` 标记的事项必须原样上浮至第 12 节，严禁模型擅自给出答案。 | 阻断 (FAIL) | 模型替业务方断定“N天取7天”，而不是在待确认项中保留问题。 |
| **GATE-06** | **范围与目标一致性 (Scope Alignment)** | PRD 的 Goals / Non-Goals 及本期/非本期范围与 `spec.md` 的范围界定严格一致。 | 阻断 (FAIL) | 缩小了本期应做范围，或将 Non-Goal 误写为 In-Scope。 |
| **GATE-07** | **验收标准保真度 (Acceptance Criteria Fidelity)** | 验收标准准确反映 `spec.md` 的验证意图，采用规范的 Gherkin (Given-When-Then) 语法，且未擅自篡改业务预期。 | 警告 (WARN) | Gherkin 缺失 Given 前置条件，或预期结果与规范矛盾。 |
| **GATE-08** | **溯源矩阵完整度 (Traceability Integrity)** | 第 13 节追溯矩阵 100% 覆盖所有 PRD 条目，双向引用可考。 | 警告 (WARN) | 某些 `FR-xx` 在追溯表中缺少出处，或出处指向不存在的行。 |

---

## 二、读者测试与可读性审查 (The Reader Test)

来源于 Anthropic `doc-coauthoring` 的 Reader Test 思想：**优秀的文档不仅要求内容正确，更要求受众能够在极短时间内精准获取信息。**

在生成 PRD 后，必须通过以下角色测试：

### 1. 业务与产品经理测试 (PM / Stakeholder Test)
- **3 分钟通读感**: 阅读第 1 节（背景与问题）到第 4 节（范围界定），能否立即清楚“本次版本为什么要做、解决谁的什么痛点、交付什么边界”？
- **业务决策友好性**: 第 12 节（待确认事项）是否列明了所有需要产品经理或业务负责人排版敲定的待定点？

### 2. 研发架构师测试 (Developer Test)
- **无过度设计束缚**: 文档是否未限制具体的编程语言、库、类结构和数据存储，给工程师留下了充足的架构设计自由？
- **业务规则清晰度**: 第 6 节业务规则是否足以让工程师理解所有数据校验、计算边界与业务守恒约束？

### 3. 测试与质量工程师测试 (QA Test)
- **直接派生测试用例**: 第 10 节验收标准是否具备直接作为自动化测试脚本（Cucumber / Behave）或手工测试用例的严密性？
- **正反与边界覆盖**: 是否兼顾了正常场景与非法超限拦截场景？

---

## 三、审阅报告输出规范 (Review Report Output)

当执行 `/speckit.prd.review` 时，审阅结果应输出为以下标准格式（可打印于终端或保存至 `review-report.md`）：

```markdown
# PRD 一致性与保真度审阅报告 (PRD Review Report)

- **审阅对象**: `specs/{feature}/product/prd.md`
- **事实源对照**: `specs/{feature}/spec.md`
- **审阅结论**: ✅ **通过 (APPROVED)** / ⚠️ **附条件通过 (WARNINGS)** / ❌ **拒绝 (REJECTED)**

## 1. 八维门禁检测总览

| 检查维度 | 状态 | 发现问题数 | 摘要简评 |
|:---|:---:|:---:|:---|
| 1. 完整性 (Completeness) | PASS | 0 | spec.md 所有 3 条需求与 2 个场景均已覆盖 |
| 2. 保真度 (No Hallucination) | PASS | 0 | 未发现任何无根据捏造的功能 |
| 3. 无实现泄漏 (No HOW Leakage) | PASS | 0 | 未检测到底层数据库或接口细节 |
| 4. 三层分离 (Semantic Separation) | PASS | 0 | 功能需求、业务规则与验收标准边界清晰 |
| 5. 待确认项透传 (Preserve Clarification) | PASS | 0 | 1 条 [NEEDS CLARIFICATION] 完整透传 |
| 6. 范围对齐 (Scope Alignment) | PASS | 0 | 目标与非目标完全契合 |
| 7. 验收标准保真 (AC Fidelity) | PASS | 0 | Gherkin 格式规范且准确 |
| 8. 溯源完整性 (Traceability) | PASS | 0 | 矩阵完全闭环 |

## 2. 详细问题与改进建议 (Findings & Recommendations)
*(若有问题，按条目详细指出定位行号、违规性质与修改建议；若全绿，输出精简评价)*

## 3. 总体结论与后续动作
- **下一步推荐**: 直接提交产品与技术评审，或执行 `/speckit.plan` 推进技术架构设计。
```
