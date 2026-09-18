# Many2one 关联记录查看增强 Implementation Plan

> **版本状态：v1.0.0 Frozen / Planning Baseline Frozen / Not Authorized for Coding**
>
> 本文档只定义 Frozen TDD 到正式实现的开发顺序、Coding Contract 边界和验证门槛。不创建正式代码、不创建 Coding Contract、不修改 Frozen SRS/TDD、不修改 Spike，也不授权进入 CC-01。

## 1. Metadata

| 项目 | 内容 |
|---|---|
| Document ID | IP-M2O-RELATED-RECORD-VIEW |
| 版本 | v1.0.0 Frozen |
| 状态 | Planning Baseline Frozen / Not Authorized for Coding |
| Odoo | 18.0 Community Edition |
| 正式模块 | `mymodules/wd_advanced_m2o_record_panel/` |
| 正式最小依赖 | `web`；不依赖 `stock` 或 SPIKE-02 |
| 上游 | SRS v1.0.0 Frozen、TV-01 v0.1.1 Frozen、TVR-01 v0.2.0 Verification Complete、TDD v1.0.0 Frozen |
| 计划日期 | 2026-09-18 |

## 2. Purpose

本计划回答：

> 按照什么开发顺序，把 Frozen TDD 安全地实现为正式生产模块，并让每一轮 Coding Contract 都形成可独立验证的闭环？

本计划不重新设计产品行为或技术架构。Frozen TDD 已确定：

```text
Enhanced Many2one
        ├── tab
        │     └── Record Navigation Builder → browser _blank → Standard Odoo Form
        └── extend
              └── Page-scoped State → FormView Sibling Host
                    → Server Preview Loader → Safe DTO
                    → Readonly Renderer
```

## 3. Authoritative Inputs

1. [Agent Operation Principles](../principle/AGENT_OPERATION_PRINCIPLES.md)：不得修改官方代码、不得直接读写数据库、正式定制必须位于 `mymodules/`。
2. [Frozen SRS](SRS-many2one-related-record-view-enhancement.md)：业务范围、`tab`/`extend`、配置、权限、fallback 和验收要求。
3. [Frozen TV Plan](TV-01-many2one-form-preview-feasibility-plan.md)：TV-01 验证范围和 Gate。
4. [TVR](../verification/TVR-01-many2one-form-preview-feasibility.md)：已验证的 Many2one、Tab、Form Host、生命周期、权限和窄屏事实。
5. [Frozen TDD](TDD-many2one-related-record-view-enhancement.md)：正式模块、四层架构、权限边界、Source Identity、`open_mode` contract、vertical stacked 和无 Preview cache。
6. `docs/requirement/需求分析报告RAR.md`：业务背景和 MVP 边界。
7. Odoo 18 官方源码：只作为实现阶段核对依据，不以未验证的内部 API 作为本计划的既定事实。
8. [SPIKE-02](../../mymodules/wd_spike_02_form_preview/)：仅作为历史可行性证据，不是生产代码基线或正式测试依赖。

权威优先级：

```text
Agent Principles
    > Frozen SRS
    > Frozen TDD
    > Verified TVR Facts / Constraints
    > Official Odoo 18 Source Facts
    > Implementation Plan
    > Spike Reference
```

## 4. Planning Principles

1. 计划基线固定为四轮 Coding Contract：CC-01、CC-02、CC-03、CC-04。Agent 不得自行新增、拆分或合并 Coding Contract；任何增加第五轮的需要必须停止并取得用户明确批准。
2. 每轮先形成最小能力闭环，再进入下一轮；任何 Gate 未通过都停止推进。
3. 生产模块从空目录开始，由 CC-01 创建；不得把 Spike 重命名、复制或改造成生产模块。
4. 每轮 Coding Contract 由本计划派生，但本计划不写具体生产 API signature、函数体或逐行修改。
5. 未增强的原生 Many2one 必须零行为变化。
6. Preview 只能读取，不写回 Many2one 或业务记录；业务记录读取不得使用 `sudo()`。
7. 不新增 HTTP Controller、`stock` 依赖、editable Preview、multiple Pane/Profile 或官方源码修改。
8. 任何需要改变 Frozen SRS/TDD 的情况必须标记 `DESIGN CHANGE REQUIRED` 并停止相关工作。

## 5. Frozen Architecture Summary

### 5.1 Field Node and Opening Mode

Opening Mode 属于 XML field node configuration，不属于 Model Preview Configuration：

```xml
<field name="partner_id"
       widget="advanced_many2one"
       options="{'open_mode': 'extend'}"/>
```

允许值仅为 `tab`、`extend`；缺失或非法值回退原生打开行为。默认 `many2one` registry entry 不改变。

### 5.2 Configuration and Loader

- 一个 target model 只有一套 Preview Configuration。
- Configuration Line 关联该模型的 `ir.model.fields` 并按 sequence 排序。
- 配置模型由配置管理员维护和读取；普通用户不直接读取配置模型。
- Server-side Preview Loader 解析配置并返回安全 DTO。
- 配置元数据可在严格限定范围内使用受控特权语义读取；业务记录始终使用当前用户环境，不得 sudo。

### 5.3 Preview State and Source

- 每个 Form/Action page 只有一个 Preview Pane。
- Source Identity 语义为 `PageScopeIdentity + RecordIdentity + FieldIdentity`，必要时增加 `FieldInstanceIdentity`。
- target model/resId 只表示 Preview 内容，不表示 source。
- clear、close、unmount 和 stale response 不得重新污染当前 Pane。

### 5.4 Layout and Navigation

- Desktop：主 Form 与 Preview horizontal sibling。
- Small screen：使用 Odoo 标准 small-screen signal，vertical stacked。
- 不使用 overlay、modal、drawer 或覆盖主要业务区域。
- Tab 和 Full Record 共用 Record Navigation Builder，通过 browser `_blank` 进入标准 Form。

## 6. Delivery Strategy

| 阶段 | 目标闭环 | 主要风险 |
|---|---|---|
| CC-01 | 正式模块可安装，配置可维护，增强 Widget 保持原生 Many2one | Widget 包装、配置约束、原生回归 |
| CC-02 | `tab` 独立打开新标签标准 Form | URL/context、浏览器标签、权限和当前页保持 |
| CC-03 | `extend` 完整 Preview happy path | Host、page state、Loader、DTO、Renderer、生命周期 |
| CC-04 | 生产级攻击性验证和集成回归 | 竞态、安全边界、配置变化、响应式和升级回归 |

依赖顺序固定为：

```text
CC-01 Foundation
       ↓
CC-02 Tab Navigation
       ↓
CC-03 Extend Preview Core
       ↓
CC-04 Hardening & Integration
```

## 7. CC-01 — Foundation / Configuration / Enhanced Many2one

### 7.1 Goal

建立正式模块骨架、配置模型和显式 Enhanced Many2one 最小框架，使模块可以安装，并证明原生 Many2one 行为没有被破坏。

### 7.2 Entry Criteria

- TDD v1.0.0 Frozen。
- 当前工作区没有需要修改的官方源码变更。
- 正式模块名和最小依赖已确认。
- 本 CC 的 Coding Contract 已单独评审并授权。

### 7.3 In Scope

- 正式模块 skeleton、manifest、assets 和初始化文件。
- `wd.preview.configuration` 与 configuration line 模型。
- 一个 target model 一套配置的唯一性。
- line 所属模型校验、重复 field 防止、sequence 和有效性约束。
- 配置管理员访问边界；普通业务用户不得直接读取配置模型。
- `advanced_many2one` registry 注册。
- `open_mode` options 解析边界：`tab`、`extend`、缺失/非法回退原生。
- 复用原生 Many2one 的 autocomplete、search、create、clear、display 和权限行为。
- 未使用增强 Widget 的字段保持原生。

### 7.4 Out of Scope

- Preview Pane、FormView Host、Preview State、Server Preview Loader、Readonly Renderer。
- Extend 完整流程。
- Tab 正式导航实现。
- Full Record Navigation。
- 任何业务记录的自定义读取。
- 修改 Spike、官方源码或 `stock` 依赖。

### 7.5 Expected Files / Components

预计由 CC-01 创建或负责：

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
└── tests/
    └── test_preview_configuration.py
```

上述是规划级文件边界，不冻结最终文件数量或未经验证的 API signature。

### 7.6 Implementation Tasks

1. 创建正式模块 manifest，声明 `web`，注册前端 assets 和 data files。
2. 定义 configuration 与 line 的模型字段、关系和排序语义。
3. 建立 target model 唯一性及 line 所属模型/重复字段约束。
4. 建立配置管理员组、ACL 和管理视图；不赋予普通业务用户直接配置模型 read。
5. 注册显式 Enhanced Many2one，保留原生 props 和原生 interaction path。
6. 解析 `open_mode` 并解析为 capability state：`native`、`tab` 或 `extend`。在 CC-01 中 Tab/Extend handler 尚未安装，因此合法 `tab` 和 `extend` 均安全走原生打开行为；缺失或非法值同样走原生打开行为。
7. 在没有 Tab/Preview handler 和业务读取的前提下，验证选择、搜索、创建、清空、显示和未增强字段。

### 7.7 Test Tasks

**Python：**

- 模型安装和配置模型加载。
- target model 唯一性。
- line 同模型、重复 field、sequence 和无效 field。
- 配置管理员可维护；普通业务用户不能直接读写配置模型。

**JavaScript：**

- registry 注册和显式 widget 生效。
- `open_mode` 合法值、缺失值、非法值。
- 未增强字段走原生路径。

**Browser：**

- 本轮只验证模块安装后的标准 Form 能加载。
- 验证 Enhanced Widget 不破坏原生选择、搜索、创建和清空。

**HVR：**

- 以真实用户操作确认原生 Many2one 交互未改变。

### 7.8 Acceptance Gate

进入 CC-02 前必须同时满足：

1. 正式模块在目标数据库安装成功，无 Python/asset load error。
2. 配置模型唯一性、字段归属、重复字段和访问边界测试全部通过。
3. 合法 `open_mode` 可被识别为 capability state；由于 CC-01 尚未安装 handler，`tab`、`extend`、缺失和非法值均稳定回退原生打开行为。
4. Enhanced 和未增强字段的 select/search/create/clear/display 行为均通过自动化或 HVR 对照。
5. 未创建 Preview Host、Loader、Renderer 或 page-scoped state。

### 7.9 Failure / Stop Conditions

- 原生 Many2one 选择、搜索、创建或清空发生不可接受回归。
- 配置模型唯一性或普通用户访问边界无法满足 Frozen TDD。
- 需要 `stock`、官方源码修改或业务记录 `sudo()` 才能安装。
- `open_mode` contract 需要改变 Frozen TDD。

### 7.10 Traceability

- SRS：显式增强字段、配置唯一性、原生兼容、配置权限。
- TDD：§7、§8、§14、§16、TD-001、TD-002、TD-009。
- TVR：标准 Many2one 行为和权限事实。

## 8. CC-02 — Tab Navigation

### 8.1 Goal

独立完成 `mode=tab`：从 Enhanced Many2one 触发标准 Record Navigation Builder，在新浏览器标签打开标准 Odoo Record Form；Extend 不参与本轮。

### 8.2 Entry Criteria

- CC-01 Acceptance Gate 通过。
- `advanced_many2one` 的 `open_mode` contract 已稳定。
- Coding Contract 明确只增加 Tab，不引入 Preview State 或 Preview Host。

### 8.3 In Scope

- Record Navigation Builder。
- target `model`、`resId` 和必要可序列化导航 context。
- action/view 信息的实现阶段解析。
- 浏览器 `_blank` 新标签。
- 新标签标准 Odoo Form、权限保持和当前页面保持不变。
- popup/URL/context 异常路径的显式错误或阻止打开。
- 为 CC-03 Full Record 复用的导航接口边界。

### 8.4 Out of Scope

- Preview Pane、Preview Loader、Readonly Renderer、page state。
- 裸 URL 猜测或把 `target="new"` 当作 `_blank`。
- 复制完整 Action Stack。
- 特殊业务 Action 的额外产品行为。

### 8.5 Expected Files / Components

```text
static/src/
├── fields/enhanced_many2one_field.js  # 增加 tab dispatch
└── navigation/related_record_url.js   # Navigation Builder
tests/
└── test_enhanced_many2one.js           # Tab contract tests
```

具体文件合并方式可在 Coding Contract 中决定，但 Navigation Builder 的逻辑职责不得消失。

### 8.6 Implementation Tasks

1. 从原生 Many2one 打开入口取得 target model、record id 和当前有效 context。
2. 实现只负责标准 Record Form 导航的 builder，不持有完整 Action Stack。
3. 在用户点击同步事件链中调用浏览器新标签能力。
4. 使新标签进入标准 Web Client Record Form，并由标准权限链继续处理。
5. 保持源页面 action、Form 状态和 Preview 无关能力不变。
6. 对缺失 target、无法安全表示的导航上下文和 popup blocker 产生显式可诊断结果，不静默当前页降级。
7. 暴露可供 CC-03 Full Record 复用的内部导航边界，不冻结未经验证的公共 API signature。

### 8.7 Test Tasks

**JavaScript：**

- `tab` 的 model/resId/context 输入。
- `_blank` 调用与 `target="new"` 区分。
- 缺失/非法 target 和 builder 错误。
- 非 `tab` 模式不进入 Tab builder。

**Browser：**

- 从真实 Form 触发关联记录，验证新标签加载标准 Form。
- 当前页保持不变。
- Notebook、Chatter、breadcrumb、业务权限在新标签正常。
- popup blocker 或 URL/context 异常显示显式结果。

**HVR：**

- 真实用户验证新标签行为、权限行为和当前页面保持。

### 8.8 Acceptance Gate

进入 CC-03 前必须满足：

1. `mode=tab` 在目标验证场景打开新浏览器标签，而不是当前页或 Dialog。
2. 新标签加载标准 Odoo Record Form，且权限、breadcrumb、Notebook、Chatter 通过验证。
3. 当前业务页面保持可操作，Tab 不依赖 Extend。
4. Navigation Builder 的错误路径无静默当前页降级。
5. 自动化与 Browser/HVR 结果形成可审计证据。

### 8.9 Failure / Stop Conditions

- 无法从标准入口稳定得到目标 model/resId。
- 新标签不能加载标准 Record Form，或需要复制完整 Action Stack。
- popup/context 异常只能通过静默改为当前页解决。
- 新标签绕过记录权限或字段权限。

### 8.10 Traceability

- SRS：Tab 新标签、标准完整记录、当前页保持和权限。
- TDD：§9、§19、§24、§25、TD-003、TD-004。
- TVR：TVQ-01、TVQ-02、RUN-001～RUN-004。

## 9. CC-03 — Extend Preview Core

### 9.1 Goal

形成 Extend 的完整用户闭环：

```text
Enhanced Many2one
    → Extend Dispatch
    → Page-scoped State
    → FormView Sibling Host
    → Server Preview Loader
    → Safe DTO / Formatting Boundary
    → Readonly Renderer
```

### 9.2 Entry Criteria

- CC-01 和 CC-02 Acceptance Gate 均通过。
- Navigation Builder 已可供 Full Record 复用。
- Coding Contract 明确不得改变 CC-01/02 的原生和 Tab 行为。

### 9.3 In Scope

- FormView template extension 和 thin FormController integration。
- page-scoped single Preview State。
- Source Identity、activate、replace、current update、current clear、close 和基本 unmount cleanup。
- Server-side Preview Loader。
- 受控配置元数据读取与当前用户业务记录权限链。
- 安全 DTO、字段过滤和官方 formatter/field utilities。
- loading、ready、fallback、access_denied、error。
- Readonly Renderer。
- Full Record 复用 CC-02 Navigation Builder。
- Desktop sibling、small-screen vertical stacked。
- Notebook、Chatter、scroll 和主 Form 可操作性。

### 9.4 Out of Scope

- 复杂缓存、同 target 去重、跨页面持久状态。
- Editable Preview、完整 FormRenderer、业务按钮、multi-profile 或 multiple Pane。
- 新增 HTTP Controller。
- 修改 Spike 或官方源码。
- CC-04 的组合竞态攻击矩阵、权限变化攻击和最终回归。

### 9.5 Expected Files / Components

```text
static/src/
├── fields/enhanced_many2one_field.js
├── navigation/related_record_url.js
├── preview/
│   ├── preview_state.js
│   ├── preview_components.js
│   └── preview_service.js
├── xml/preview_templates.xml
└── scss/preview.scss
models/
└── preview_loader.py  # 参考文件名；Server-side Preview Loader logical component 为必需
tests/
├── test_preview_access.py
└── test_enhanced_many2one.js
```

这是逻辑组件规划；最终文件可按职责合并，但不得合并成 Field Widget 自持有整个 Pane 生命周期。

### 9.6 Implementation Tasks

1. 在 FormView 外层建立 scoped sibling host，不逐个业务 Form 改造。
2. 由 thin Controller integration 建立 page scope、注入 state/dispatch 并在 unmount 清理。
3. 由 Enhanced Many2one dispatch `activate/update/clear/close`，不写回 source。
4. 实现 Source Identity 的 PageScope/Record/Field 语义。
5. 实现单 Pane 状态和 source replacement；当前 source update/clear 只影响当前 source。
6. 实现**必需的**最小 server-side Preview Loader logical component（最终是否独立为 `preview_loader.py` 由本 CC 决定）：
   - 受控读取配置定义；
   - 使用当前用户环境验证目标业务记录；
   - 过滤不可读和失效字段；
   - 一次读取当前 activation 所需字段；
   - 返回不含 arbitrary HTML、technical id 或 traceback 的安全 DTO。
7. 接入官方 formatter/field utilities，覆盖 Frozen TDD 规定的字段类型。
8. 实现 readonly renderer、loading/fallback/denied/error 和 Full Record。
9. 实现 desktop sibling 与 `env.isSmall` vertical stacked，并确保主 Form、Notebook、Chatter、scroll 可用。
10. 在完成主链路前实现基础 stale protection：为请求绑定 page/source/target/request identity；clear、close、unmount 立即失效旧请求；迟到响应不得提交。至少加入一个基本 race 自动化测试。

### 9.7 Test Tasks

**Python：**

- 配置解析、字段过滤和安全 DTO。
- 记录不可读不泄露身份。
- 字段不可读时省略该字段而保留其他字段。
- 配置缺失、停用、空字段、无效字段。
- 不使用业务记录 sudo。

**JavaScript：**

- page-scoped state、single Pane、source replacement。
- current update/clear、non-current update/clear、close、unmount。
- 两个 source field 指向相同 target 的隔离。
- Loader 结果到 renderer 的只读边界。

**Browser：**

- Field A → Preview A → Field B → Preview B。
- Close 不改 Many2one。
- Full Record 新标签。
- 标准 Form、Notebook、Chatter、desktop sibling、small-screen stacked。
- fallback、access denied、partial fields 和 error。

**HVR：**

- 真实内部用户和受限用户验证只读、权限、主 Form 可操作和布局。

### 9.8 Acceptance Gate

进入 CC-04 前必须满足：

1. Field A/B 可激活 Preview，B 能原子替换 A，页面只有一个 Pane。
2. Close 不修改 source；Full Record 复用 Tab 导航并打开新标签。
3. Preview 只读，不写业务记录，不使用业务 sudo。
4. 记录无权不泄露身份；字段无权只省略该字段。
5. 无配置/停用/空字段按 Frozen SRS 显示 fallback。
6. Desktop sibling 和 small-screen vertical stacked 不覆盖主 Form。
7. Notebook、Chatter、scroll 和主 Form 操作通过 Browser/HVR。

### 9.9 Failure / Stop Conditions

- FormView host 只能通过修改官方源码或逐个业务 Form 才能工作。
- Loader 无法同时满足配置元数据受控读取和业务记录当前用户权限。
- Renderer 需要嵌入完整 Form、编辑 Widget 或业务按钮。
- Source replacement、current clear 或 unmount 会污染旧 Pane。
- Preview 错误破坏主 Form 或发生身份泄露。

### 9.10 Traceability

- SRS：Extend、single Pane、source lifecycle、权限、fallback、格式化、只读和响应式。
- TDD：§10～§24、§25～§26、TD-005～TD-014。
- TVR：EXP-002-A～G、RUN-005～RUN-007、TVQ-03～TVQ-06。

## 10. CC-04 — Hardening & Integration

### 10.1 Goal

系统性攻击 CC-01～CC-03 已完成能力，完成生产级生命周期、安全、竞态、布局、配置变化和回归闭环。本轮不是零散补 Bug，而是独立的 Hardening & Integration Contract。

### 10.2 Entry Criteria

- CC-03 Acceptance Gate 通过。
- Python、JavaScript、Browser、HVR 基础结果已保存。
- 正式测试不安装、不导入、不依赖 SPIKE-02。

### 10.3 In Scope

- activate、replace、update、clear、close、unmount、re-enter。
- rapid A→B、stale RPC、clear/close during loading、source change during loading、unmount during request。
- Source A/B 指向同一 target 的隔离。
- model/record/field permission、partial visibility、deleted record、permission revoked。
- 不泄露 display_name、technical id、internal field、traceback、SQL。
- no/disabled/empty/invalid/changed configuration。
- 标准 Form、Notebook、Chatter、复杂分组、scroll、desktop、small-screen、Tab+Extend 混合。
- popup behavior、Full Record、离开/返回和未安装 Spike 的正式环境。
- 最终回归、升级风险 smoke checks 和测试分层汇总。

### 10.4 Out of Scope

- 任何新的业务需求或 UX 模式。
- Editable Preview、multiple Pane/Profile、generic Split View。
- 跨页面 Preview cache、同 target cache、后台刷新。
- 改动 Frozen SRS/TDD 或开启新的 TV。
- 生产代码之外的 Spike 清理或卸载。

### 10.5 Expected Files / Components

预计主要修改 CC-01～CC-03 已拥有的正式模型、Loader、state、navigation、host、renderer、模板、SCSS 和测试文件；可能新增：

```text
tests/
├── test_preview_configuration.py
├── test_preview_access.py
├── test_preview_loader.py
├── test_enhanced_many2one.js
└── test_preview_state.js
```

最终文件按现有项目测试组织方式决定，不创建与 Spike 的依赖关系。

### 10.6 Implementation Tasks

1. 建立完整生命周期矩阵，并为每个 transition 添加自动化或 Browser/HVR 证据。
2. 攻击 CC-03 已实现的 page/source/target/request identity：验证 rapid A→B→A、重复 activation 和异步返回乱序。
3. 验证 clear/close/unmount during loading、source change during loading 和 permission change during request；确认 CC-03 的基础失效机制在组合场景中可靠。
4. 以受限用户和变化中的权限状态攻击 Loader。
5. 验证配置停用、字段失效和配置变化不会使用跨页面旧缓存。
6. 验证同 target 不同 source 的更新/清空隔离。
7. 运行完整 Form/Notebook/Chatter/复杂布局/窄屏/Tab+Extend 回归。
8. 检查正式模块在无 Spike 安装状态下可安装、加载和测试。
9. 汇总失败证据；若触及 Frozen TDD，停止并标记 DESIGN CHANGE REQUIRED。

### 10.7 Test Tasks

**Python：**

- 配置变化、无效字段、ACL、记录规则、字段权限和 DTO 安全。
- 记录删除、权限撤销和错误分类。

**JavaScript：**

- rapid A→B、stale request、clear/close/unmount during loading。
- Source Identity 同 target 隔离。
- state re-enter cleanup、renderer fallback 和 error。

**Browser：**

- 标准 Form、Notebook、Chatter、复杂分组、scroll。
- Desktop sibling、small-screen vertical stacked、Tab+Extend 混合。
- Full Record、popup behavior、离开/返回。

**HVR：**

- 内部用户、受限用户和配置变化后的真实角色验证。
- 原生 Many2one select/search/create/clear/display/open 回归。

### 10.8 Acceptance Gate

Implementation Plan 的实现阶段仅在以下条件全部满足后闭环：

1. 四轮 CC 的 Python/JS/Browser/HVR 结果均可追溯。
2. 全部 lifecycle 和 concurrency 场景通过，旧响应不能污染当前 Pane。
3. 同 target 不同 source 的隔离通过。
4. 记录、字段、模型权限和配置变化场景无信息泄露。
5. 无配置、停用、空配置、无效字段和错误路径符合 Frozen SRS/TDD。
6. Desktop、小屏、Notebook、Chatter、复杂分组和 scroll 不破坏主 Form。
7. 正式模块不依赖 Spike、不修改官方源码、不依赖 `stock`、不使用业务 sudo。
8. 回归结果满足发布前的明确阈值；任何失败均有明确记录和处理决定。

### 10.9 Failure / Stop Conditions

- 任一 security case 泄露 display_name、technical id、internal field 或 traceback。
- stale response 在 clear/close/unmount 后重新污染 Pane。
- 原生 Many2one 或标准 Tab 回归。
- 小屏覆盖主业务区域，或 Notebook/Chatter/scroll 不可用。
- 配置变化需要跨页面长期缓存才能工作。
- 任何需求或 Frozen TDD 需要修改。

### 10.10 Traceability

- SRS：全部 MVP、异常、权限、NFR 和验收标准。
- TDD：§13、§16、§20～§28、§31～§33、TD-007～TD-014。
- TVR：RUN-005/RUN-006、EXP-002-A～G 和 TVQ-05/06。

## 11. Cross-CC Dependency Map

```text
Configuration Model / ACL ───────┐
                                 ├── Extend Preview Core
Enhanced Many2one ───────────────┘

Navigation Builder ──────────────┬── CC-02 Tab
                                 └── CC-03 Full Record

Page Scope / Controller Host ────┐
Preview State ───────────────────┤
Server Preview Loader ───────────┼── CC-03 Extend
Formatter Boundary ──────────────┤
Readonly Renderer ───────────────┘

CC-01 + CC-02 + CC-03 ──────────────── CC-04 Hardening
```

不得在 CC-03 重新实现 CC-02 Navigation Builder，也不得在 CC-04 新增第二套 State、Loader 或 navigation path。

## 12. File Ownership Matrix

| 文件/逻辑组件 | 初始 Owner | 后续允许修改 | 约束 |
|---|---|---|---|
| `__manifest__.py` / module init | CC-01 | CC-04 | 依赖只保留 `web` |
| `models/preview_configuration.py` | CC-01 | CC-04 | 一模型一配置、无业务 sudo |
| `models/preview_configuration_line.py` | CC-01 | CC-04 | 模型归属、重复和 sequence |
| `security/*` / config views | CC-01 | CC-04 | 配置管理员边界 |
| `static/src/fields/enhanced_many2one_field.js` | CC-01 | CC-02/03/04 | 原生行为和 options contract |
| `static/src/navigation/related_record_url.js` | CC-02 | CC-03/04 | Tab 与 Full Record 共用 |
| `static/src/preview/preview_state.js` | CC-03 | CC-04 | page-scoped、single Pane、stale protection |
| `static/src/preview/preview_components.js` | CC-03 | CC-04 | Host/Renderer 逻辑，不嵌入完整 Form |
| `static/src/preview/preview_service.js` | CC-03 | CC-04 | Loader dispatch 和错误边界 |
| `models/preview_loader.py` | CC-03 | CC-04 | 配置受控读取，业务记录当前用户环境 |
| `static/src/xml/preview_templates.xml` | CC-03 | CC-04 | scoped FormView host |
| `static/src/scss/preview.scss` | CC-03 | CC-04 | scoped sibling/stacked，不污染全局 |
| `tests/*` | 对应 CC | CC-04 | 正式测试不依赖 Spike |

File ownership 表示主责任，不禁止后续 Contract 在同一文件增加兼容性修改。

## 13. Test Growth Matrix

| 测试领域 | CC-01 | CC-02 | CC-03 | CC-04 |
|---|---|---|---|---|
| Configuration | 模型/约束/ACL | 回归 | Loader/变化 | 攻击性配置变化 |
| Native Many2one | 基线 | Tab 不回归 | Extend 不回归 | 最终回归 |
| Tab | — | builder/新标签 | Full Record 复用 | 混合/异常/权限 |
| Preview State | — | — | open/replace/clear/close + 基础 stale protection | stale/concurrency/unmount 组合攻击 |
| Loader/Security | — | 标准权限 | 基本 DTO/字段权限 | record rule/撤权/删除/泄露攻击 |
| Formatting | — | — | 基础类型/只读 | 异常类型/locale/长文本 |
| Responsive | 安装加载 | 当前页保持 | desktop/stacked | 复杂 Form/scroll/回归 |
| HVR | 原生交互 | Tab | Preview happy path | 最终真实角色验收 |

测试随能力增长；CC-04 不能成为第一次运行所有测试的阶段。

## 14. Requirement / TDD Traceability

| 计划阶段 | Frozen SRS | Frozen TDD | TVR / Evidence |
|---|---|---|---|
| CC-01 | CFG、native compatibility、显式 widget | §7、§8、§14、§16 | Many2one 原生链路、权限事实 |
| CC-02 | Tab、完整记录、当前页保持 | §9、§19、TD-003/004 | TVQ-01/02、RUN-001～004 |
| CC-03 | Extend、single Pane、source、readonly、fallback | §10～§24、TD-005～012 | EXP-002、RUN-005～007 |
| CC-04 | lifecycle、security、responsive、NFR、AC | §13、§16、§20～§33、TD-007～014 | TVQ-05/06、EXP-002-A～G |

## 15. Risk Burn-down

| 阶段 | 被消除的风险 | 仍保留的风险 | 下降证据 |
|---|---|---|---|
| CC-01 | Widget 包装、配置唯一性、原生回归 | Tab、Host、Loader 未实现 | 安装、Python、JS、HVR |
| CC-02 | 新标签、URL/context、标准 Form 恢复 | Preview state、权限 DTO、竞态 | Browser/HVR 新标签证据 |
| CC-03 | Host、page state、Loader、Renderer、核心生命周期 | 快速竞态、权限撤销、复杂布局 | Python/JS/Browser happy path |
| CC-04 | stale RPC、安全边界、配置变化、响应式和集成回归 | 未来 Odoo 升级风险 | 完整测试矩阵和升级 smoke check |

四轮拆分避免把 Widget、导航、Preview 和安全硬化同时引入一个不可定位的中间状态。

## 16. Integration & Regression Strategy

1. 每轮只在正式模块中工作；Spike 保持独立且不安装为正式测试依赖。
2. 每轮结束保存自动化结果、Browser 证据和 HVR 记录。
3. CC-02 必须运行 CC-01 的 native regression；CC-03 必须运行 CC-01/02 的完整回归；CC-04 运行全部分层测试。
4. 任何前端模板、Controller、Router 或 formatter 依赖都必须在目标 Odoo 18 运行环境复核。
5. 不使用直接数据库写入伪造测试数据；测试数据经 Odoo ORM/test utilities 建立。
6. 不为测试引入 `stock` 正式依赖；若需要业务场景，作为测试环境能力而非 manifest dependency。
7. 发布前确认正式模块在 `wd_spike_02_form_preview` 未安装时仍可安装和运行。

## 17. Stop / Escalation Conditions

以下任一情况发生，停止当前 CC，不进入下一轮：

- Frozen SRS 或 TDD 无法满足，标记 `DESIGN CHANGE REQUIRED`。
- 需要修改 `odoo/`、官方 `addons/`、Frozen SRS、Frozen TDD 或 Spike。
- 需要新增 HTTP Controller、`stock` dependency、editable Preview、multiple Pane/Profile 或业务 sudo。
- 原生 Many2one、标准 Tab、记录权限或字段权限发生不可接受回归。
- 无法证明普通用户请求使用当前业务权限，或发生身份/技术信息泄露。
- 无法可靠丢弃 stale response，或旧 response 能污染新 source。
- 主 Form、Notebook、Chatter、scroll 或 small-screen layout 不可用。

处理方式：记录证据、停止相关 Contract、提出设计评审；不得在 Plan 或代码中偷偷改变 Frozen 架构。

## 18. Final Exit Criteria

Implementation Plan 的实现阶段闭环必须满足：

- CC-01～CC-04 均已独立完成并通过各自 Acceptance Gate；
- 四轮输入、输出、文件责任和测试证据完整；
- Native Many2one、Tab、Extend、Full Record、权限、fallback、formatter、responsive 和 lifecycle 均有最终证据；
- 没有 Spike、`stock`、官方源码、业务 sudo 或未批准 HTTP Controller 依赖；
- 正式测试可在 Spike 未安装时运行；
- 无未解决的 `DESIGN CHANGE REQUIRED`；
- 交付前形成最终回归报告和待发布风险清单。

这些是实现闭环条件，不代表当前已授权实现。

## 19. Open Implementation Questions

以下问题来自 Frozen TDD §32，已按阶段分配，不改变 TDD：

| 问题 | 分类 | 解决阶段 |
|---|---|---|
| Tab URL 的 action/view/context 具体取值、特殊 Action 和 popup blocker | B：对应 CC 内实现验证 | CC-02；必要时在 CC-04 回归 |
| FormView selector/slot 在 Form、Notebook、Chatter 组合中的兼容集 | B：对应 CC 内实现验证 | CC-03 |
| thin Controller 使用 sub-env、service 或 host props | C：纯实现细节 | CC-03 Coding Contract |
| Server Loader 的具体 ORM 调用、DTO 字段和错误码 | A：Coding 前必须在 CC-03 Contract 明确 | CC-03 |
| Monetary currency 依赖和 relational/display 格式化边界 | B：实现验证 | CC-03，CC-04 异常回归 |
| 长文本、Pane 宽度和 popup 文案 | C：实现/验收细节 | CC-03/04 |
| 配置菜单、访问组 XML ID 和升级迁移 | C：实现细节 | CC-01，CC-04 回归 |
| 删除记录或请求中撤权的 UI 文案 | B：实现验证 | CC-03，CC-04 |

当前没有 D 类 `DESIGN CHANGE REQUIRED`。如果任何问题需要修改 Frozen TDD，必须停止并升级评审。

## 20. Version History

| 版本 | 日期 | 状态 | 说明 |
|---|---|---|---|
| v0.1.0 | 2026-09-18 | Draft / Planning Only / Not Authorized for Coding | 基于 Frozen SRS、TVR、TDD 和 Spike 证据拆分 CC-01～CC-04；未创建代码、Coding Contract 或正式模块文件 |
| v0.1.1 | 2026-09-18 | Draft / Planning Only / Not Authorized for Coding | 根据评审修订 CC-01 capability fallback、CC-03 required Loader 与基础 stale protection、CC-04 组合竞态边界、四轮变更治理措辞；未改变四轮结构，未创建代码或 Coding Contract |
| v1.0.0 | 2026-09-18 | Frozen / Planning Baseline Frozen / Not Authorized for Coding | 用户最终评审通过；CC-01～CC-04、依赖关系、文件责任、测试增长、风险收敛和停止条件冻结；后续每轮仍需单独评审 Coding Contract，当前不授权编码 |
