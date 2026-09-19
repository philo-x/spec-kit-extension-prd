# 验收标准编写与对齐规范 (Acceptance Criteria Guidelines)

验收标准 (Acceptance Criteria, AC) 是连接产品经理业务诉求、工程师编码实现与测试人员质检验收的“铁律契约”。

在 `spec-kit-prd` 编译管道中，验收标准采用行业标准的 **Gherkin 行为驱动语法 (Given-When-Then)**，确保每一条产品需求都可以被无歧义、可自动化地验证。

---

## 一、Gherkin 语法三要素标准

```gherkin
Given [前置条件 / 业务上下文 / 初始状态]
When  [用户触发动作 / 外部系统事件 / 定时触发器]
Then  [可观测的业务结果 / 状态跃迁 / 提示与通知]
And   [补充并列条件或结果]
But   [排除的边界或反向状态]
```

### 1. Given: 明确上下文
- 必须包含业务判定所需的必要前置条件（如：用户角色、当前账期、历史已有工时数、当前数据状态）。
- ❌ 模糊："Given 系统正常运行"
- ✅ 具体："Given 员工 A 在 2026-09-19 已有 20.0 小时已确认报工记录"

### 2. When: 单一操作意图
- 聚焦单一关键动作，避免将一长串业务流程压缩在一个 When 中。
- ❌ 复杂："When 员工登录并浏览项目列表，随后点击填报按钮输入5小时并提交"
- ✅ 明确："When 员工 A 尝试在 2026-09-19 再次提交 5.0 小时工时申请"

### 3. Then: 可客观判定的结果
- 必须指明：
  1. 操作是否被允许或阻断；
  2. 系统的具体业务提示信息；
  3. 业务对象的状态变更（若有）。
- ❌ 模糊："Then 系统报错"
- ✅ 具体："Then 系统拒绝保存，并提示'单日累计工时已达20小时，本次填报5小时超出单日24小时上限'，且报工记录总数保持不变"

---

## 二、从 `spec.md` 到 PRD 验收标准的映射与升维

Spec Kit 的 `spec.md` 中通常以如下形式存在用户故事场景：
```markdown
#### Acceptance Scenarios
1. **Successful submission**: Given today is September 19, When I submit 8 working hours, Then the record is saved.
2. **Exceeding limit**: Given 20 hours already logged today, When I submit 5 hours, Then the system rejects the submission with a limit warning.
```

在 PRD 编译时，须升级为标准的 `AC-xx` 结构，并显式建立与功能 (`FR-xx`) 及业务规则 (`BR-xx`) 的交叉引用：

```markdown
### AC-01: 正常日工时成功申报 (Happy Path)
```gherkin
Given 员工处于已登录状态且具备工时填报权限
  And 2026-09-19 当天该员工尚无任何报工记录
 When 员工填报 2026-09-19 的工时为 8.0 小时并点击提交
 Then 系统成功持久化该条工时记录
  And 工时单状态更新为 "已提交" (Submitted)
  And 系统提示 "工时提交成功"
```
- **关联功能**: `FR-01` (工时填报)
- **关联业务规则**: `BR-01` (工时上限约束), `BR-03` (步长约束)
- **溯源引用**: `spec.md#User Story 1 / Scenario 1`

### AC-02: 单日累计工时超限阻断 (Rule Violation)
```gherkin
Given 员工在 2026-09-19 当天已累计申报并确认了 20.0 小时有效工时
 When 员工尝试继续提交同日 5.0 小时工时
 Then 系统阻断提交操作
  And 弹出业务拦截提示: "单日累计工时不可超过24小时"
  And 数据库中未产生新的工时记录
```
- **关联功能**: `FR-01` (工时填报)
- **关联业务规则**: `BR-01` (单日工时上限)
- **溯源引用**: `spec.md#User Story 1 / Scenario 2`
```

---

## 三、验收标准覆盖度检查矩阵 (Completeness Dimensions)

为确保 PRD 具备极高的一致性与严密性，每个核心功能模块必须在以下四个维度完成验收标准核查：

| 验证维度 | 验证关注点 | 典型用例目标 |
|:---|:---|:---|
| **1. 正向主流程 (Happy Path)** | 标准输入、合规状态下的成功执行 | 验证核心业务价值能否端到端顺利达成 |
| **2. 逆向业务规则校验 (Negative/Rule Failure)** | 触犯业务规则或边界阈值 | 验证系统能准确识别违规、合理阻断并友好提示 |
| **3. 极限与临界值测试 (Boundary Values)** | 0 值、最小值、最大上限值、临界时间点 | 验证如恰好等于 24.0 小时、第 N 天 23:59:59 时的系统表现 |
| **4. 权限与状态隔离 (Security & State Transitions)** | 非法角色越权操作、在非法前置状态下操作 | 验证数据隔离、未授权拦截及防重复提交 |

---

## 四、质量自查清单 (AC Quality Gates)

- [ ] **无技术术语泄漏**: 不包含 `HTTP 200`、`SELECT * FROM`、`Redis Key` 等实现名词。
- [ ] **原子性验证**: 每个 AC 聚焦一个独立的行为场景，可单独执行。
- [ ] **双向可追溯**: 标注了其支持的 `FR-xx` 和检验的 `BR-xx`。
- [ ] **无悬空规则**: `spec.md` 中声明的每一条业务规则，在第 10 节中均有对应的 AC 场景进行校验。
