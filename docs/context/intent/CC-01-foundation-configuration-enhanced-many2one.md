# CC-01 Foundation / Configuration / Enhanced Many2one

> **Status: v1.0.0 FROZEN — IMPLEMENTATION AUTHORIZED FOR CC-01 ONLY**
>
> 本文档记录已冻结的 CC-01 Coding Contract。用户已授权仅实施 CC-01；完成实现、自动化验证和交接报告后必须停止，不得进入 CC-02。

## 1. Contract Metadata

| 项目 | 内容 |
|---|---|
| Contract ID | CC-01 |
| Contract Name | Foundation / Configuration / Enhanced Many2one |
| 版本 | v1.0.0 Frozen |
| 状态 | Frozen / Implementation Authorized for CC-01 only |
| Odoo | 18.0 Community Edition |
| 正式模块 | `mymodules/wd_advanced_m2o_record_panel/` |
| 正式最小依赖 | `web` |
| 上游 SRS | v1.0.0 Frozen |
| 上游 TDD | v1.0.1 Frozen（配置权限勘误） |
| 上游 Implementation Plan | v1.0.0 Frozen；其余规划不变，配置 read 以 TDD v1.0.1 勘误为准 |
| 当前 branch | `main` |
| 当前 HEAD | `b7f30ef` |
| `origin/main` | `b7f30ef` |
| 起草日期 | 2026-09-18 |

冻结前基线：working tree clean；正式模块目录已存在但没有正式模块文件；CC-01 不得把 SPIKE-02 改造成正式模块。

## 2. Authorization Status

当前实施授权：

- 创建和修改本 Contract 允许的 CC-01 正式模块文件；
- 安装/升级正式模块并运行 CC-01 自动化验证；
- 创建 IHR、ATR 和 HVR Checklist；
- 完成后停止，不创建或进入 CC-02/CC-03/CC-04；
- 不修改 SRS、TDD、Implementation Plan、TVR 或 Spike；
- 不 Commit、Push 或删除文件。

Contract 流程必须保持：

```text
CC-01 Draft
    ↓
User Review
    ↓
Corrections
    ↓
CC-01 Frozen
    ↓
Explicit Implementation Authorization
    ↓
Coding
```

## 3. Authoritative Baselines

1. `docs/context/principle/AGENT_OPERATION_PRINCIPLES.md`
2. `docs/context/designing/SRS-many2one-related-record-view-enhancement.md` — v1.0.0 Frozen
3. `docs/context/designing/TDD-many2one-related-record-view-enhancement.md` — v1.0.0 Frozen
4. `docs/context/designing/Implementation-Plan-many2one-related-record-view-enhancement.md` — v1.0.0 Frozen
5. `docs/context/verification/TVR-01-many2one-form-preview-feasibility.md` — v0.2.0 Verification Complete
6. `docs/requirement/需求分析报告RAR.md`
7. `docs/context/cognition/PROJECT_COGNITION.md`
8. Odoo 18 Community 官方源码中 Many2one field registry、Many2one component、field props 和相关打开入口。
9. `mymodules/wd_spike_02_form_preview/` — 仅历史技术证据，不是正式实现基础。

权威优先级：

```text
Agent Principles
    > Frozen SRS
    > Frozen TDD
    > Frozen Implementation Plan
    > TVR Verified Facts / Constraints
    > Official Odoo 18 Source Facts
    > Spike Reference
```

发现上游冲突时，必须标记 `CONTRACT BLOCKER` 并停止受影响部分；不得修改上游 Frozen 文档自行解决。

## 4. Contract Goal

CC-01 只建立以下最小基础闭环：

```text
Production Module Skeleton
        +
Preview Configuration
        +
Configuration Security
        +
Explicit Enhanced Many2one
        +
open_mode Contract
        +
Native Many2one Compatibility
```

CC-01 完成后，正式模块应可独立安装和验证，但只允许具备原生打开 fallback。CC-01 不产生 Tab 或 Preview 能力。

## 5. Entry Criteria

进入 CC-01 编码前必须满足：

1. SRS v1.0.0、TDD v1.0.0、Implementation Plan v1.0.0 均保持 Frozen。
2. 本 Draft 已经用户评审并明确批准冻结。
3. 用户另行明确授权实施 CC-01。
4. 正式模块身份为 `mymodules/wd_advanced_m2o_record_panel/`，最小依赖为 `web`。
5. working tree、branch 和远程基线已记录。
6. 当前不存在影响 CC-01 的 `CONTRACT BLOCKER` 或 `DESIGN CHANGE REQUIRED`。

## 6. In Scope

1. 正式模块 skeleton、manifest、module init 和 frontend assets registration。
2. Preview Configuration model 和 Configuration Line model。
3. target model 唯一性。
4. field belongs-to-model validation。
5. duplicate field prevention。
6. sequence ordering。
7. configuration validity constraints。
8. configuration administrator security and management views。
9. `advanced_many2one` field widget registration。
10. `open_mode` contract parsing and capability resolution。
11. 最大程度复用 Odoo 原生 Many2one。
12. 原生 select、search、create、clear、display、readonly、required、disabled 等兼容性。
13. CC-01 所需 Python、JavaScript、Browser、HVR 验证设计和证据记录。

## 7. Out of Scope

本 Contract 明确禁止实现：

- Tab Navigation Builder；
- browser `_blank`；
- Preview Pane；
- FormView Host；
- FormController Preview integration；
- page-scoped Preview State；
- Source Identity runtime；
- Server Preview Loader；
- Safe Preview DTO；
- readonly Preview renderer；
- formatter pipeline；
- Full Record navigation；
- responsive Preview layout；
- stale RPC implementation；
- Preview business record reading；
- HTTP Controller；
- editable Preview；
- multiple Pane；
- multiple Profile；
- generic Split View；
- `stock` dependency；
- Odoo 官方源码修改。

特别约束：

```text
open_mode=tab
    只能被识别为 capability；
open_mode=extend
    只能被识别为 capability；
CC-01 两者都必须 native fallback；
```

## 8. Frozen Technical Contracts

### 8.1 Module Identity

正式模块路径：

```text
mymodules/wd_advanced_m2o_record_panel/
```

`__manifest__.py` 只能声明实现 CC-01 所需的最小官方依赖 `web`。不得因为测试场景或示例模型声明 `stock` 或其他无关业务模块。

### 8.2 Configuration Model

正式模型 technical name：

```text
wd.preview.configuration
```

至少包含：

| 字段语义 | Contract |
|---|---|
| `target_model_id` | 必填，关联 `ir.model`，表示唯一配置所属的 target model |
| `active` | 必填 Boolean；表示该唯一配置是否启用，不参与绕过唯一性 |
| `line_ids` | One2many，关联 `wd.preview.configuration.line`，按 sequence 排序 |
| display/name | 使用稳定、可读的配置身份；不得引入 user/profile/scenario 语义 |

Frozen 行为：

- 一个 target model 只能存在一个 configuration entity；
- inactive configuration 仍占据该 target model 的唯一 configuration identity；
- 不支持 default configuration、user-specific configuration、profile 或 scenario；
- 不需要 chatter/activity；
- 不需要 custom HTML、CSS 或 arbitrary formatter expression；
- 删除 configuration 不得删除业务记录；
- 未经本 Contract 授权，不创建数据迁移或业务数据修复逻辑。

### 8.3 Configuration Uniqueness

唯一性必须是硬约束：

```text
target_model_id → one configuration entity
```

优先使用数据库唯一约束表达 `target_model_id` 唯一性。预期行为：

- 创建第二套同 target model configuration 被拒绝；
- 修改 configuration 使其与另一套冲突被拒绝；
- `active=False` 不改变上述结果；
- Odoo ORM 将约束失败转换为标准可诊断的 validation error；
- 不捕获后静默成功，不返回 success-shaped fallback。

如果目标 Odoo 18 字段/约束机制不能完整表达关系一致性，才增加最小 Python constraint，并在实现记录中说明 SQL 不足的具体原因。不得无理由堆叠重复约束。

### 8.4 Configuration Line

正式模型 technical name：

```text
wd.preview.configuration.line
```

至少包含：

| 字段语义 | Contract |
|---|---|
| `configuration_id` | 必填 Many2one，指向 `wd.preview.configuration` |
| `field_id` | 必填 Many2one，指向 `ir.model.fields` |
| `sequence` | 必填或有稳定默认值，决定 deterministic ordering |

约束：

1. `field_id` 必须属于 parent configuration 的 target model。
2. 同一 configuration 不得重复同一 `field_id`。
3. invalid、missing 或跨模型 field 不得静默保留。
4. configuration 存在 lines 时修改 `target_model_id` 必须直接抛出 ValidationError；用户必须先移除 lines，再修改 target model，再重新选择 fields；不得自动清空 lines。
5. line ordering 固定为 `_order = "sequence, id"`。
6. 不允许 custom label、custom CSS、custom formatter expression、field profile 或 arbitrary template。

### 8.5 Configuration Security

配置模型对普通内部用户开放 read；配置管理员拥有完整维护权限。

必须建立专用配置管理员 group，至少具备：

| 操作 | 配置管理员 | 普通内部用户 |
|---|---:|---:|
| read configuration | allow | allow |
| create | allow | deny |
| write | allow | deny |
| unlink | allow | deny |
| read configuration lines | allow | allow |
| create/write/unlink lines | allow | deny |

管理菜单和 action 只对配置管理员可见。普通业务用户：

- 可以通过标准 ORM read 读取 configuration/configuration line 的允许元数据；
- 不得 create/write/unlink 配置；
- CC-01 不新增普通用户的 `ir.model.fields` 访问权限；
- 不因为 CC-01 而获得任何业务模型、记录或字段权限。

CC-01 不实现未来 CC-03 的 Server Preview Loader；CC-03 可使用普通用户已有的 configuration read ACL，再以当前用户权限读取业务记录。

### 8.6 Enhanced Many2one Registry

正式 widget technical name：

```text
advanced_many2one
```

只在 XML 显式使用时生效：

```xml
<field name="partner_id"
       widget="advanced_many2one"
       options="{'open_mode': 'extend'}"/>
```

默认：

```xml
<field name="partner_id"/>
```

必须继续使用 Odoo 默认 `many2one` registry entry。CC-01 不得替换、覆盖、全局 patch 或改变默认 registry。

### 8.7 Native Many2one Reuse

实现必须复用 Odoo 18 原生 Many2one component/class、props、field services 和已有交互路径。只允许增加最小的：

- registry entry for `advanced_many2one`；
- options resolution；
- capability resolution；
- CC-01 native fallback boundary。

不得：

- copy/fork 官方 Many2one 源码；
- 重写 autocomplete；
- 重写 search/dropdown；
- 重写 select；
- 重写 create/create-and-edit；
- 重写 clear；
- 重写 display logic；
- 改变 readonly/required/disabled/no-create 等原生 options；
- 在 Widget 内创建 Preview DOM 或持有页面生命周期。

### 8.8 `open_mode` Contract

合法 options：

```text
tab
extend
```

解析结果概念上为：

```text
native | tab | extend
```

CC-01 的 implemented handler 只有 `native`：

| 输入 | capability resolution | CC-01 行为 |
|---|---|---|
| missing | native | native open |
| invalid | native | native open |
| `tab` | tab recognized | handler unavailable → native open |
| `extend` | extend recognized | handler unavailable → native open |

禁止：

- `tab → no-op`；
- `extend → no-op`；
- `tab/extend → error`；
- `tab → browser _blank`；
- `extend → Preview`。

CC-02 才安装 Tab Handler；CC-03 才安装 Extend Handler。CC-01 不创建 Plugin Framework 或未来 handler 的空实现。

### 8.9 Native Compatibility

以下行为属于正式 regression contract：

- display；
- autocomplete；
- search；
- dropdown；
- select；
- create；
- create-and-edit（原生适用时）；
- clear；
- readonly；
- required；
- disabled/no-create 等原生 options；
- access behavior；
- native related-record open。

增强 Widget 除未来相关记录打开方式外，不拥有 Many2one 其他业务行为；CC-01 阶段打开增强尚未正式启用。

## 9. Allowed Files

CC-01 允许创建或修改的正式文件范围：

```text
mymodules/wd_advanced_m2o_record_panel/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── preview_configuration.py
│   └── preview_configuration_line.py
├── security/
│   ├── preview_security.xml
│   └── ir.model.access.csv
├── views/
│   └── preview_configuration_views.xml
├── static/src/fields/
│   └── enhanced_many2one_field.js
├── tests/                 # Python tests
└── static/tests/          # Web/JS tests and fixtures when Odoo harness requires
```

文件结构是授权区域，不要求机械创建空文件。允许在 `tests/` 和 `static/tests/` 内创建 CC-01 Test Contract 所需的 Python/JS test 与 fixture 文件；不得借此创建生产功能。只有需要修改新生产目录、新业务模型、新正式 dependency、上游文档或其他模块时，才需要 Contract Amendment Request。

## 10. Forbidden Files and Operations

禁止修改：

```text
odoo/
official addons/
docs/context/principle/AGENT_OPERATION_PRINCIPLES.md
docs/context/designing/SRS-many2one-related-record-view-enhancement.md
docs/context/designing/TDD-many2one-related-record-view-enhancement.md
docs/context/designing/Implementation-Plan-many2one-related-record-view-enhancement.md
docs/context/verification/TVR-01-many2one-form-preview-feasibility.md
mymodules/wd_spike_02_form_preview/
```

也禁止：

- 修改与 CC-01 无关的现有模块；
- `git reset`、`git checkout`、`git clean`、`git stash` 或覆盖 unrelated files；
- 删除任何文件；
- 直接 PostgreSQL、裸 SQL、手工 schema patch；
- 使用数据库 patch 伪造测试结果；
- 业务数据 `sudo()`；
- HTTP Controller；
- `stock` dependency。

## 11. Implementation Tasks

仅在 CC-01 Frozen 且获得明确实施授权后，按以下顺序执行：

1. 创建 module init、manifest 和 assets registration。
2. 创建 configuration 与 line 模型、初始化导入和管理视图。
3. 建立唯一性、field/model consistency、duplicate field、sequence 和 target model 变更约束。
4. 建立配置管理员 group、ACL、menu/action visibility。
5. 注册 `advanced_many2one`，复用原生 Many2one，不接管默认 registry。
6. 实现 `open_mode` resolution，确认 CC-01 只有 native handler。
7. 建立 Python/JS 测试 fixture 和最小 Browser/HVR 场景。
8. 运行 CC-01 允许的验证；保存 evidence。
9. 在所有 Gate 满足前，不进入 CC-02 或实现任何 Preview 能力。

不得把上述步骤扩展为具体函数名、变量名、逐行 patch 或未验证的官方 API signature。

## 12. Python Test Contract

具体测试函数名由实现决定，但必须覆盖以下可审计契约：

| ID | Contract |
|---|---|
| CFG-01 | Configuration model 可以被配置管理员正常创建 |
| CFG-02 | 同 target model 创建第二套 configuration 被拒绝 |
| CFG-03 | inactive configuration 仍占据唯一 configuration identity |
| CFG-04 | 属于 target model 的合法 field line 被接受 |
| CFG-05 | 其他 model 的 field line 被拒绝 |
| CFG-06 | 同 configuration 重复 field 被拒绝 |
| CFG-07 | sequence ordering deterministic |
| CFG-08 | 配置管理员 read/create/write/unlink 符合 security contract |
| CFG-09 | 普通内部用户可以 read configuration models，但不能 create/write/unlink |
| CFG-10 | target model 变更不会静默留下 invalid lines |

测试必须经 Odoo ORM/test utilities 建立数据；不得直接修改数据库。

## 13. JavaScript Test Contract

至少覆盖：

| ID | Contract |
|---|---|
| M2O-01 | `advanced_many2one` registry entry 存在 |
| M2O-02 | 默认 `many2one` registry entry 未被替换 |
| M2O-03 | missing `open_mode` → native open |
| M2O-04 | invalid `open_mode` → native open |
| M2O-05 | `open_mode=tab` 被识别，但无 Tab handler → native open |
| M2O-06 | `open_mode=extend` 被识别，但无 Extend handler → native open |
| M2O-07 | Enhanced Widget select/search/create/clear 与 native behavior 一致 |
| M2O-08 | 未增强 Many2one 完全不进入 enhanced path |
| M2O-09 | readonly/required/disabled/no-create 等原生 props 不被改变 |

如果 Odoo 18 test harness 不适合自动化某个真实交互，该行为必须移入 Browser/HVR，并记录原因；不得创建无意义的 mock 通过。

## 14. Browser Verification Contract

CC-01 至少需要以下 Browser evidence：

1. 模块安装后标准 Form 正常加载。
2. 普通 Many2one 正常显示。
3. Enhanced Many2one 正常显示。
4. autocomplete 正常。
5. search 正常。
6. select 正常。
7. create 正常（原生适用时）。
8. clear 正常。
9. native related-record open 正常。
10. `open_mode=tab` 和 `open_mode=extend` 在本轮没有空白、无响应或 JavaScript error，并回到 native open。
11. 未增强字段与增强字段对照验证。

可以使用项目已有标准/简单模型作为场景，但不得因此增加 `stock` 正式 dependency。

## 15. HVR Contract

HVR 目标不是验证 Tab 或 Preview，而是验证 Enhanced Widget 没有破坏用户熟悉的原生 Many2one。

至少观察：

```text
click → type → search → select → clear → create → open related record
```

每项记录：

- Expected；
- Actual；
- PASS/FAIL；
- evidence；
- 用户角色和使用模型。

HVR 不得把 CC-02/CC-03 能力当作 CC-01 的通过条件。

## 16. Acceptance Gate

只有以下全部成立，CC-01 才能判定 Complete：

1. 正式模块可以安装。
2. 无 Python import error。
3. 无 asset load error。
4. Configuration models 正常。
5. one model → one config 强制成立。
6. field/model consistency 成立。
7. duplicate field 被阻止。
8. configuration administrator security 成立。
9. ordinary user 可以 read configuration，但不能 create/write/unlink configuration。
10. `advanced_many2one` 正常注册。
11. 默认 Many2one 未被覆盖。
12. native select/search/create/clear/display 没有不可接受回归。
13. `tab/extend` 在 handler 未实现情况下稳定 native fallback。
14. 没有 Preview Host。
15. 没有 Preview State。
16. 没有 Preview Loader。
17. 没有 Tab Builder。
18. 没有业务记录自定义读取。
19. 没有官方源码修改。
20. 没有 `stock` dependency。
21. CC-01 不新增任何用于读取 Preview target business record 的 `sudo()` 或自定义业务读取路径。
22. Python/JS/Browser/HVR evidence 完整。

## 17. Stop Conditions

编码阶段发生以下任一情况，必须停止并记录证据：

| ID | Stop condition |
|---|---|
| STOP-01 | 需要修改 Odoo 官方源码 |
| STOP-02 | 必须复制官方 Many2one 实现才能继续 |
| STOP-03 | 必须覆盖默认 `many2one` registry |
| STOP-04 | 需要 `stock` 正式 dependency |
| STOP-05 | 需要提前实现 Tab |
| STOP-06 | 需要提前实现 Preview |
| STOP-07 | 试图让普通用户 create/write/unlink configuration，或借配置 read 扩大业务模型/记录/字段权限 |
| STOP-08 | Frozen TDD configuration model/security contract 无法实现 |
| STOP-09 | 原生 Many2one 出现无法在 Frozen Architecture 内解决的回归 |
| STOP-10 | 需要修改授权文件范围外的生产文件 |
| STOP-11 | 需要改变 Frozen SRS/TDD/Implementation Plan |

停止后不得自行扩大 Scope；若涉及上游冲突，标记 `CONTRACT BLOCKER` 或 `DESIGN CHANGE REQUIRED`，等待用户决策。

## 18. Contract Amendment Rule

CC-01 Frozen 后，Agent 不得静默修改 Contract。

发现遗漏时必须提出 `CC-01 Amendment Request`，至少包含：

- Issue；
- Evidence；
- Current Contract；
- Requested Change；
- Scope Impact；
- Architecture Impact；
- Test Impact。

等待用户批准后，才能修改 Contract 或继续受影响工作。Amendment 不得通过修改 Frozen SRS/TDD/Implementation Plan 规避。

## 19. Traceability

```text
Frozen SRS
    ↓
Frozen TDD
    ↓
Frozen Implementation Plan / CC-01
    ↓
CC-01 Contract Clause
    ↓
Test / Browser / HVR Evidence
```

| Contract area | SRS | TDD | Implementation Plan | Evidence |
|---|---|---|---|---|
| explicit enhanced widget | 显式配置、native compatibility | §8、TD-001/002 | CC-01 §7 | M2O-01/02/08、HVR |
| one model one config | CFG、configuration uniqueness | §14、TD-009 | CC-01 §7 | CFG-01/02/03 |
| field validation | configured fields、sequence | §14、§15 | CC-01 §7 | CFG-04/05/06/07/10 |
| configuration security | admin maintenance、ordinary user read-only boundary | §16、TD-010 | CC-01 §7 | CFG-08/09、Browser |
| open_mode | `tab`/`extend` parsing、capability resolution、native fallback | §8、TD-001/003 | CC-01 open_mode/native fallback；downstream handler 属于 CC-02/03 | M2O-03～06、Browser |
| native compatibility | selection/search/create/clear/open | §8、§31、TD-002 | CC-01 §7 | M2O-07/09、Browser、HVR |

本 Contract 没有新增上游未定义的业务能力。

## 20. Deliverables

CC-01 实施完成后，且仅在 Acceptance Gate 通过时，预期交付：

- 可安装的正式模块基础；
- Configuration/Line 模型和管理员管理界面；
- 配置 ACL/group；
- 显式 `advanced_many2one` registry entry；
- `open_mode` capability resolution 和 CC-01 native fallback；
- Python/JavaScript/Browser/HVR evidence；
- 不包含 Tab、Preview、Loader、Renderer 或 Full Record 实现。

本节是 CC-01 目标交付物，不代表本 Draft 已经创建这些文件。

## 21. Version History

| 版本 | 日期 | 状态 | 说明 |
|---|---|---|---|
| v0.1.0 | 2026-09-18 | Draft / Not Authorized for Implementation | 基于 Frozen SRS、TDD、Implementation Plan、TVR 和 Odoo 18 官方源码事实起草 CC-01 Foundation / Configuration / Enhanced Many2one Contract；未创建代码、未安装、未执行、未提交、未推送 |
| v0.1.1 | 2026-09-18 | Draft / Not Authorized for Implementation | 根据评审和 TDD v1.0.1 勘误改为普通内部用户 configuration read-only、收窄 `ir.model.fields` 条款、冻结 technical field names、lines 存在时 target model 变更拒绝、`_order = "sequence, id"`、测试目录授权、业务 sudo 表述和 open_mode traceability；未创建代码 |
| v1.0.0 | 2026-09-18 | Frozen / Implementation Authorized for CC-01 only | 用户批准冻结并授权实施 CC-01；Scope、技术契约、文件范围、测试契约、Acceptance Gate 和 Stop Conditions 冻结；不得进入 CC-02，不得 Commit/Push |
