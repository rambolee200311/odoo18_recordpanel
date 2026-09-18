# Many2one 关联记录查看增强技术设计文档（TDD）

> **版本状态：v1.0.0 Frozen / 技术设计已冻结 / 允许进入后续 Implementation Plan**
>
> 本文档是已冻结的技术设计，不是 Implementation Plan 或 Coding Contract，也不单独构成正式编码授权。后续实现必须遵守本文档，并经过单独的 Implementation Plan / Coding Contract 评审。

## 1. Metadata

| 项目 | 内容 |
|---|---|
| Document ID | TDD-M2O-RELATED-RECORD-VIEW |
| 版本 | v1.0.0 Frozen |
| 状态 | 技术设计已冻结；仅允许进入后续 Implementation Plan / Coding Contract 评审，不等同于编码授权 |
| Odoo | 18.0 Community Edition |
| 正式模块 | `mymodules/wd_advanced_m2o_record_panel`（已确认的正式模块名） |
| 正式最小依赖 | `web`（不依赖 `stock`） |
| 上游 | SRS v1.0.0 Frozen、TV-01 v0.1.1 Frozen、TVR-01 v0.2.0 Verification Complete |
| 编写日期 | 2026-09-18 |
| 变更范围 | 基于 v0.1.1 评审意见修订本 TDD Draft；不创建新 TV、不创建正式代码 |

权威优先级固定为：**Agent Principles > Frozen SRS > TVR verified facts/constraints > Official source facts > TDD decisions > Spike reference**。

## 2. Purpose / Scope

本 TDD 将冻结前的业务要求转换为可评审的技术边界：显式配置的 Many2one Widget 提供 `tab` 和 `extend` 两种打开方式；`extend` 在当前页面维护一个只读 Preview Pane；字段、权限、格式化和生命周期均不扩大原生 Odoo 能力。

范围包括前端 Widget、Tab 导航、页面级宿主、页面范围状态、ORM/RPC 读取、配置模型、权限、格式化、响应式、异常与测试设计。不包括正式编码、Implementation Plan、Coding Contract、发布配置和业务数据迁移。

## 3. Authoritative Inputs

1. `docs/context/principle/AGENT_OPERATION_PRINCIPLES.md`：不得修改官方代码、不得直接读写数据库，正式定制放入 `mymodules/`。
2. `docs/context/designing/SRS-many2one-related-record-view-enhancement.md`：Frozen v1.0.0，定义 FR/BR/CFG/NFR。
3. `docs/context/designing/TV-01-many2one-form-preview-feasibility-plan.md`：Frozen v0.1.1，定义验证问题和证据标准。
4. `docs/context/verification/TVR-01-many2one-form-preview-feasibility.md`：v0.2.0 Verification Complete；TVQ-02～05 在验证范围内通过，TVQ-01 和 TVQ-06 为条件通过，无 P0 阻断。
5. `docs/requirement/需求分析报告RAR.md`：业务背景、MVP 单模型单配置、单 Pane 和只读原则。
6. `docs/context/cognition/PROJECT_COGNITION.md`：Odoo 18 工作区、模块路径和工作流约定。
7. Odoo 18 官方源码事实：Many2one、Action Service/Router、FormController/FormView/Layout、OWL、ORM/RPC、field utilities/formatters。
8. `mymodules/wd_spike_02_form_preview/`：仅作为 SPIKE-02 可行性证据，不是生产基线。

## 4. Requirement Traceability

| SRS/业务主题 | TDD 落点 | 验收关注 |
|---|---|---|
| `tab` | §10、§19、§25 | 新标签完整标准 Form，当前页不变 |
| `extend` | §11、§12、§13 | 当前页一个非覆盖只读 Pane |
| 显式配置 | §8、§9 | 未配置 Widget 保持原生行为 |
| fields/config | §14、§15 | 一模型一套配置、顺序、有效性 |
| single Pane | §12、§23 | 后触发替换前触发 |
| source lifecycle | §13、§26 | 只响应当前来源，卸载清理 |
| close/full record | §11、§19、§21 | 关闭不改值，新标签不绕权 |
| permissions/fallback | §16、§21 | 记录拒绝不泄露，字段拒绝省略 |
| formatting | §17、§18 | 复用官方 formatter，禁止 arbitrary HTML |
| narrow/native compatibility | §20、§22 | 窄屏安全降级，原生选择/搜索/创建/清空不变 |

## 5. Verified Technical Baseline

- Many2one 原生字段通过 `orm`、`action` 和 `useOpenMany2XRecord` 处理选择、搜索、创建、清空及打开入口；`openAction()` 可由关系模型、记录 id、字段 context/eval context 形成 Action。
- 标准完整记录仍由 Action Service、Router 和 `web.FormView` 承载；`target="new"` 不等同于浏览器 `_blank`，Tab 需要明确构造标准 Web Client URL。
- Form 页面具有 Controller、Renderer、Layout、`.o_form_view_container` 和主内容容器；官方源码没有专用 Preview slot。
- OWL 提供 `useState`、sub-environment、生命周期钩子和 cleanup；SPIKE-02 运行时证明页面可承载单一状态，来源可替换，Form 离开后可清理。
- ORM/RPC 的 `fields_get`、字段访问检查、记录规则检查和 `read` 形成权限边界；记录无权时不得返回身份信息，字段无权时可省略而继续读取其余字段。
- 官方 field utilities/formatters 覆盖 Boolean、Date、Datetime、Many2one、Monetary、Selection 等基础类型。
- SPIKE-02 的 `web.FormView` template extension + `FormController` patch 只证明 sibling 宿主可行；它不是生产代码、不是 API 保证，也不授权照抄。

## 6. Architecture Overview

```text
显式 Enhanced Many2one
  ├─ 原生选择/搜索/创建/清空/权限能力（复用）
  └─ 打开入口
      ├─ tab → 标准 action/context URL → 新浏览器标签 → 标准 Form
      └─ extend → page-scoped Preview state
                    → page-level Preview host
                    → permission-aware data loader
                    → readonly renderer
```

正式选择为：**FormView template extension + thin FormController integration + 页面范围 Preview service/state**。模板扩展负责在标准 Form 根布局中插入一个 sibling host；薄 Controller 集成负责建立/销毁页面边界并提供 host 所需状态接口，不负责业务字段读取。该选择同时避免修改官方源码、逐个修改业务 Form、复制完整 Action Stack 或把 Pane DOM 生命周期放进 Field Widget。

## 7. Module Structure

正式模块固定为 `mymodules/wd_advanced_m2o_record_panel/`，建议的逻辑组件和参考文件结构如下（仅设计，不代表已创建；职责边界冻结，文件拆分不冻结）：

```text
__manifest__.py
models/
  preview_configuration.py
  preview_configuration_line.py
views/
  preview_configuration_views.xml
security/
  preview_security.xml
  ir.model.access.csv
static/src/
  fields/enhanced_many2one_field.js
  preview/preview_state.js
  preview/preview_components.js
  preview/preview_service.js
  navigation/related_record_url.js
  xml/preview_templates.xml
  scss/preview.scss
tests/
  test_preview_configuration.py
  test_preview_access.py
  test_enhanced_many2one.js
```

正式依赖只声明 `web`；不得因示例模型而依赖 `stock`。正式测试和运行不得依赖 SPIKE-02 已安装。`security/` 负责配置模型 ACL；配置模型仅配置管理员可直接维护和读取，普通业务用户不直接读取配置模型或 `ir.model.fields`。Preview Loader/helper 以当前用户权限计算并返回安全 DTO。

## 8. Enhanced Many2one Widget

Widget 仅在 XML 字段节点**显式指定**增强 widget 时注册并生效；不改变默认 `many2one` registry entry，不增加名为 `official` 的模式。它包装/继承原生 Many2one 的必要 props 和组件能力，复用原生 autocomplete、搜索、创建、清空、active actions、访问判断及 display 行为。

Opening Mode 属于**字段节点配置**，不属于 Preview Configuration。正式 XML contract 为：

```xml
<field name="partner_id"
       widget="advanced_many2one"
       options="{'open_mode': 'extend'}"/>
```

`open_mode` 的允许值只有 `tab` 和 `extend`；缺失或非法值回退到原生打开行为。不得增加“一个 target model 配一个默认 mode”的第二套配置语义。

自定义部分只处理“打开关联记录”分派：

- `mode=tab`：调用 Tab navigation builder；
- `mode=extend`：向当前 page-scoped state dispatch source activation；
- 未知/缺省 mode：安全回退到原生打开行为，不能悄悄改变选择、搜索、创建或清空行为。

不得复制完整 Many2one 实现；不得在 Field Widget 内创建 Pane DOM、监听页面全局卸载、保存 Preview 数据或绕过原生权限。

## 9. Tab Mode

Tab 必须由统一的 record navigation builder 生成标准 Odoo Web Client 记录 URL。输入概念上包括 `model`、`resId`、当前字段/记录的有效 `context` 以及可恢复的 action/view 信息；builder 不持有完整内存 Action Stack。

**TD-003 是正式 TDD Design Decision。** Tab 在用户点击产生的同步事件链中使用统一 Record Navigation Builder，构造 SRS 所需的 `model`、`resId` 和必要的可序列化导航上下文，并通过浏览器 `_blank` 打开标准 Odoo Web Client Record Form。Builder 不复制完整内存 Action Stack。Action key、Router state key、特殊 action context 和 popup blocker 处理属于 Implementation Plan、Coding Contract、JS tests 与 Browser tests，不重新开启 TV Gate。

新标签是 SRS 的硬业务要求；不得静默降级为当前页。若实现阶段发现某个特殊 Action 无法安全表示，应显式返回错误或阻止打开，并保留具体决策记录，不改变普通标准 Record Form 路径。

替代方案：复制完整 Action Service stack（拒绝：过度耦合、不可维护）；打开 Dialog（拒绝：不是 Tab 且不满足完整页面）；未经验证拼接裸 `/web#...`（拒绝：可能丢失 context 或形成错误导航）。

## 10. Extend Mode

Extend 只 dispatch：

```text
Widget → page-scoped Preview state → page-level host → data loader → readonly renderer
```

当前页主区域缩小后与 Pane 持续同屏；Pane 不得是 Modal、Tooltip、overlay 或覆盖式 Drawer。后触发的 extend source 原子替换当前 Pane。关闭只更新状态，不保存、写入或清空源 Many2one。

## 11. Preview Host

候选评估：

| 候选 | 结论 |
|---|---|
| A. FormView template extension + thin FormController integration | **正式选择**：不改官方源码、不逐个 Form，能形成 sibling；风险是依赖 FormView 模板/Controller 内部结构 |
| B. Field Widget 直接插 Pane | 拒绝：无法保证页面唯一 Pane、跨字段生命周期和布局 |
| C. Layout 全局改造 | 拒绝为首选：影响所有视图，升级和回归面过大 |
| D. 每个业务 Form 继承 | 拒绝：不可通用，违反模块公共工具定位 |
| E. Action Service 全局 overlay/service | 拒绝：容易变成覆盖层，难保证 Form 内容和响应式布局 |

正式 host 是轻量组件，作为 FormView 外层 sibling；它不复制 FormController、Chatter、Notebook 或完整 FormRenderer。Controller integration 只建立页面 token、注入 state/dispatch、在 unmount 清理 token。Chatter、Notebook、scroll、responsive 和升级兼容性必须纳入浏览器测试；若官方模板结构变更，模块应安全不显示 Pane 而不破坏主 Form。

## 12. Page-scoped State

每个页面上下文只有一个 Preview Pane。内部技术状态允许 `closed / loading / ready / fallback / access_denied / error`，这些不是新增业务生命周期；业务语义仍是打开、替换、更新、清空、关闭。

状态契约只冻结以下概念：页面范围、单一 Pane、当前 source、当前 target、加载中、已授权展示结果、错误/降级结果和 stale request protection。具体字段名称（例如 `pageToken`、`requestToken`、`rows`）仅为设计示意，不构成最终 JS Store/API。状态单向流动：Widget dispatch，loader 读取，renderer 展示；Preview 绝不写回 source record 或 Many2one 字段。

## 13. Source Identity / Lifecycle

Source Identity 的冻结契约为：

```text
SourceIdentity =
    PageScopeIdentity
  + RecordIdentity
  + FieldIdentity
  [+ FieldInstanceIdentity]
```

`PageScopeIdentity` 表示当前 Form/Action 实例，`RecordIdentity` 表示当前业务 Form record，`FieldIdentity` 表示触发 Preview 的具体字段。只有同一字段在同一 Form 中实际渲染多次时，才增加 `FieldInstanceIdentity`。Source Identity 不使用 target model/resId；两个不同 source field 即使指向同一 target record，也必须被视为不同 source。

只有当前 source 字段的值变化、清空或显式关闭影响 Pane。其他 Many2one 的变化被忽略。Form/action 销毁时清理页面状态、取消/失效请求 token 和 DOM 引用；重新进入页面不得恢复旧 Pane，除非未来另有明确需求。

## 14. Configuration Model

正式模型建议：

- `wd.preview.configuration`：`target_model_id`（`ir.model`）、`active`、`line_ids`；
- `wd.preview.configuration.line`：`configuration_id`、`field_id`（`ir.model.fields`）、`sequence`。

一个 target model 只能有**一套 Preview Configuration**，不是“一套 active 配置”；`active` 是该唯一实体配置的属性，不能用 `active=False` 绕过唯一性。数据库唯一约束（必要时辅以 ORM constraint）必须保证 target model 唯一；line 约束必须保证 `field_id` 所属模型与 target model 相同、同一配置不重复字段、字段存在且可用于展示。配置模型的 `create/write/unlink/read` 仅对配置管理员开放；普通用户不直接读取配置模型。Preview Loader/helper 在当前用户权限边界内解析配置，并只返回安全 DTO。删除/停用配置不得删除业务记录。

配置管理员维护配置；普通业务用户不直接读取配置模型。空字段、停用、缺失配置均是合法状态，由 server-side Preview Loader 生成安全 fallback DTO。

## 15. Preview Data Loading

正式采用最小 server-side Preview Loader model method，不新增 HTTP Controller。普通用户不直接读取配置模型；前端调用 Loader/helper 获取最终安全 DTO。Loader 内部将配置定义读取与业务数据读取分离：

1. 配置定义只通过受控的配置访问语义读取，用于解析 target model、字段和 sequence；
2. 目标业务记录始终使用当前用户 ORM environment，执行模型访问权限、记录规则和字段访问权限校验，禁止 sudo 业务读取；
3. 只返回当前用户实际可见的安全 DTO。

具体采用哪些 Odoo 18 标准 ORM 调用组合属于实现阶段 API 验证内容；本 TDD 冻结 helper 的安全边界和输出契约，不伪造未经验证的调用序列。

推荐安全流程：解析配置 → 确认当前用户对目标记录具有 read 权限 → 确认配置字段对当前用户可读 → 仅读取允许字段 → 返回安全展示数据。记录权限失败必须在读取 `display_name` 或其他身份信息前停止；字段失败逐项省略，其余继续。返回值不含任意 HTML。MVP 不建立 Preview data cache，也不做同 target 去重；每次当前 activation/update 只进行一次尽可能完整的读取，stale response 仅丢弃。

## 16. Permission / Security

配置权限与业务记录权限分离。配置模型仅配置管理员可直接访问；Loader 可以在严格限定的配置元数据读取边界内使用受控特权语义解析配置，但不得以该语义读取任何目标业务记录。业务用户只接收 Loader/helper 基于当前用户业务权限计算出的安全 DTO。目标业务记录始终使用当前用户环境，不 sudo；不能因管理员配置字段而扩大用户模型、记录或字段可见范围。若目标模型本身对当前用户不可读，服务端不得通过配置模型或 helper 间接泄露目标身份。

安全规则：

1. 先检查记录级 read 权限和 record rule，再取 display name/字段；
2. 记录不可访问：只返回通用 `access_denied`，不返回模型名、记录名、id 或字段值；
3. 字段不可读：省略该行，其余可读字段继续；
4. 无配置/停用/空字段：若目标记录可访问，Preview Pane 进入 fallback 状态，显示安全基础身份、无详细 Preview 配置提示和“打开完整记录”；若目标记录不可访问，只显示安全无权提示；
5. RPC 错误统一映射，不把 server traceback、SQL、内部字段名作为用户文本。

## 17. Formatting

复用 Odoo 官方 `getFormattedValue`、field utilities、formatter registry 和当前用户 locale/context。至少覆盖 Char、Text、Integer、Float、Many2one、Selection、Boolean、Date、Datetime、Monetary，并定义空值、长文本换行/截断策略。Many2one 使用已授权的 display value，Selection 使用业务 label，Boolean 使用人类可读状态，Date/Datetime 遵循用户 locale/timezone，Monetary 遵循 currency display。

禁止 arbitrary HTML、模板注入、任意 custom formatter、把技术 value/id 直接当业务文本。格式化失败时该字段可显示安全占位或省略，不影响其他字段。Many2one 只展示已通过权限链路获得的 display value。

## 18. Readonly Renderer

Renderer 只消费已授权、已格式化的 rows，使用 label/value 语义 HTML；不创建编辑 Field Widget、不提供 save/create/delete/complex button，不改变 record model。字段属性如 readonly、不可写和不可创建不能被 Preview 绕过。

Renderer 必须能渲染部分字段、空字段和 fallback；组件卸载时无业务写入。任何“打开完整记录”按钮只调用 §19 builder。

## 19. Full Record Navigation

Preview 的“打开完整记录”与 Tab 模式共享统一 navigation builder，输入必须明确为 source target 的 model/resId/context。使用新浏览器标签并进入标准 Odoo Form；当前页面和 Pane 状态保持不变。该入口不 sudo、不伪造权限、不把 Preview 变成编辑表单。

## 20. Responsive

Desktop 使用主 Form + Preview sibling，主 Form `min-width: 0`，Pane 有可读最小宽度和滚动边界。Small screen 使用 Odoo 标准 small-screen signal（优先 `env.isSmall`）切换为 vertical stacked：主 Form 在前、Preview 在后。该设计不得使用 overlay、modal、drawer 或覆盖主要内容；breakpoint 使用标准 signal，不冻结像素值。

若窄屏内容较长，使用 stacked 布局和 Pane 内滚动；可显示安全 header/fallback 和完整记录入口，但不得隐藏 Extend Pane、改为 overlay 或覆盖主业务区。

## 21. Error / Fallback

错误分类至少包括：无配置、停用、空字段、配置非法、字段类型不支持、记录删除、记录权限撤销、字段权限不足、网络/RPC 错误、过期请求。无配置、停用或没有有效字段时，Extend 不应创建一个伪装成正常 Preview 的空 Pane；应安全保持原生打开能力/完整记录入口，并按 SRS 规定的降级语义处理。只有在 Frozen SRS 明确要求时，才显示配置提示；记录不可访问时只显示安全无权提示。

错误不应破坏源页面或原生 Many2one；renderer 不显示旧记录残留。非法配置逐项跳过，全部无效时 fallback。unsupported type 不允许任意 HTML，采用省略或安全占位。

## 22. Concurrency

每次 activation/update/clear/close 分配递增 request token，并绑定 `pageToken + sourceIdentity + targetIdentity`。RPC 返回时仅当 token、页面仍挂载、source 仍当前且目标仍匹配才提交；否则丢弃 stale response。新目标替换旧目标时旧请求失效；clear/close 立即清除旧内容，不能等待旧请求。

网络异常可显示 error/fallback；不自动写回、不重试造成重复请求。记录删除或权限撤销按 §21 处理。

## 23. Performance

- 每页只创建一个 host/state；不为每个字段创建 Pane。
- 只读取配置字段，按 sequence 排序；去重后一次安全读取，避免逐字段 RPC。
- 不做 Preview data cache 或同 target 去重；每次当前 activation/update 一次读取尽可能完整的数据。
- 延迟加载仅在打开 extend 时发生；关闭后释放 rows 和 DOM。
- Tab 不预取 Preview；未配置字段不请求。
- 监测首次打开延迟、RPC 数、替换竞态、长字段布局和大量字段滚动性能。

## 24. Interfaces

| 接口 | 方向 | 设计约束 |
|---|---|---|
| `EnhancedMany2one` props | XML → Widget | 显式 widget、`mode`、原生 props |
| `preview.dispatch(event)` | Widget → page state | activate/update/clear/close，带 source identity |
| `preview.load(target, fields, context)` | state → ORM/helper | 当前用户、无 sudo、权限先行 |
| `navigation.build(model, resId, context, view)` | widget/renderer → browser | 标准 Form URL，新标签 |
| `preview.state` | state → host/renderer | 单向只读消费 |
| configuration ORM methods | admin UI → server | 一模型一配置、校验、访问控制 |

具体 JS/Python signature 属于实现阶段，不在本 Draft 中伪造为已实现 API。

## 25. Sequence Flows

### 25.1 Tab
1. 用户触发显式 enhanced Many2one 的原生打开入口。
2. Widget 保留原生判断，交给 navigation builder。
3. builder 形成 model/resId/context/view URL。
4. 浏览器 `_blank` 打开标准 Web Client Form。
5. 当前页面不变，新页执行原有权限和业务逻辑。

### 25.2 Extend
1. Widget dispatch activate(source identity, target)。
2. page state 替换单一 source，status=`loading`。
3. host 保持 sibling 布局；loader 先记录权限再取字段。
4. formatter 产生 rows，renderer 只读显示。

### 25.3 Replace
1. B dispatch 时 state 原子失效 A 的 request token。
2. source 切换为 B、旧内容清除或进入 loading。
3. B 成功后只显示 B；迟到的 A 响应丢弃。

### 25.4 Update / Clear
1. 当前 source 值从 A 改为 B：验证 source identity 后重新加载 B。
2. 当前 source 清空：立即 closed，释放 A 内容。
3. 非当前 source 更新/清空：忽略。

### 25.5 Denied
1. loader 通过当前用户 ORM 权限链确认 B 记录可读。
2. 拒绝则不读取身份/字段，status=`access_denied`。
3. renderer 仅显示安全提示；不显示 model/name/id。

## 26. State Transitions

```text
closed --activate--> loading
loading --authorized/read ok--> ready
loading --no config/invalid/unsupported--> fallback
loading --record denied--> access_denied
loading --RPC/error--> error
ready --same source update--> loading
ready --new source--> loading (replace)
ready --current clear/close--> closed
fallback/access_denied/error --new source--> loading
any --page unmount--> closed (request invalidated)
```

## 27. Testing Strategy

### Python

测试一模型唯一配置、同模型字段约束、重复字段、sequence、配置管理员/业务用户访问边界、记录 rule、字段 access、无权不泄露、部分字段省略、删除记录和非法类型。

### JavaScript

测试显式 widget 才增强、未配置字段原生行为、Tab 导航输入契约、dispatch identity、单 Pane replace、update/clear/close、stale request、unmount cleanup、readonly renderer 无写入；补充两个 source field 指向同一 target 的隔离测试。

### Browser

覆盖标准 Form、Notebook、Chatter、滚动、复杂分组、desktop sibling、narrow 安全降级、Tab 新标签、完整记录入口、配置缺失、权限拒绝、记录删除和网络错误。验证主 Form 始终可操作且无 overlay。

### HVR

以真实用户角色验证选择/搜索/创建/清空未改变；Tab 完整页面；Extend 持续同屏、单 Pane、来源切换、只读、关闭；字段权限和记录权限不泄露；新标签和窄屏行为。补充权限竞态、两个字段指向同一 target、配置停用/修改后的下一次 activation/reload 不使用跨页面旧配置。

正式测试不得安装、导入或依赖 `wd_spike_02_form_preview`。

## 28. Upgrade Risks

主要风险是 Odoo 更新 FormView 外层模板、FormController 生命周期、Router URL keys、formatter signature、OWL hook 行为和 CSS 容器结构。通过最薄 template/Controller 集成、版本化 smoke tests、失败安全（不显示 Pane 但主 Form 可用）、不修改官方文件降低风险。每次 Odoo minor/major 升级必须复核官方源码事实和 browser suite。

## 29. Rejected Alternatives

1. 复制完整 Many2one：行为漂移、升级负担、权限/搜索重复实现。
2. 增加 official mode：无业务价值，扩大模式矩阵。
3. Field Widget 持有 Pane DOM：违反页面单一 Pane 和生命周期边界。
4. 多 Pane/Profile：超出 MVP，造成配置优先级和布局复杂度。
5. Modal/overlay/drawer：违反持续同屏和不覆盖约束。
6. 修改官方源码：违反 Agent Principles。
7. 依赖 stock：不属于通用能力，破坏最小依赖。
8. 新增 HTTP Controller：不必要且扩大攻击面；优先 ORM service/标准 model methods。
9. `sudo()` 读取业务数据：违反权限边界。
10. SPIKE-02 直接转生产：只证明可行性，不提供生产 API、错误处理或测试基线。

## 30. TD Decision Log

| 决策 | 正式决定 | 理由/后果 |
|---|---|---|
| TD-001 | 只对显式 enhanced widget 生效 | 保护原生兼容；未配置字段零行为变化 |
| TD-002 | 复用原生选择/搜索/创建/清空/权限 | 避免复制 Many2one；打开行为是唯一增强点 |
| TD-003 | Tab 使用统一 Record Navigation Builder，在同步点击事件链中生成标准 Record URL 并通过 `_blank` 打开 | 满足 SRS 新标签要求；只携带必要可序列化导航上下文，不复制完整 Action Stack；特殊 Action 处理留给实现测试 |
| TD-004 | 不复制完整内存 Action Stack | 降低耦合；复杂 action context 由 builder 明确处理 |
| TD-005 | Host 选择 FormView template extension + thin Controller integration | 通用 sibling、生命周期可控；承担升级风险 |
| TD-006 | Widget 不拥有 Pane DOM 生命周期 | 页面只一个 Pane；通过 page state 单向通信 |
| TD-007 | state page-scoped，内部技术状态只作为 conceptual states | 防止跨 Form 残留；具体 property names 留给实现，不增加业务生命周期 |
| TD-008 | Source Identity 固定为 PageScopeIdentity + RecordIdentity + FieldIdentity，必要时加 FieldInstanceIdentity | target model/resId 只表示内容，不表示 source；避免相同 target 被误更新/误清空 |
| TD-009 | 一个 target model 仅一套配置，active 是属性 | 避免多配置优先级；字段 line 关联 ir.model.fields |
| TD-010 | 正式采用最小 server-side Preview Loader；配置元数据可受控特权读取，业务记录严格当前用户环境且不 sudo | 集中安全边界；防止 display_name 泄露；字段拒绝可部分成功 |
| TD-011 | 复用官方 formatter/field utilities，禁止 arbitrary HTML | 保持 locale/业务可读和安全 |
| TD-012 | desktop horizontal sibling；small screen 使用标准 signal vertical stacked | 满足不覆盖；不冻结像素 breakpoint，不隐藏 Extend Pane |
| TD-013 | 页面卸载清理状态并使请求 token 失效 | 防止 stale RPC 和跨页面残留 |
| TD-014 | 每次请求校验 request/source/page identity | 解决 replace/update/clear 竞态；与 Source Identity 语义组成一致 |

## 31. Constraints

- 不修改 `odoo/` 或官方 `addons/`，不改 Spike、SRS、TV、其他文档。
- 不直接读写数据库；所有业务读写经 Odoo ORM/标准 RPC。
- 不新增 HTTP Controller，除非后续评审证明标准 model method 不足。
- 不依赖 `stock`，正式模块最小依赖为 `web`。
- 不增加 official mode、不提供编辑 Preview、不扩展多 Pane/Profile。
- 不允许 Preview 绕过记录/字段权限或输出技术 id。
- 不将伪代码、Spike 代码或内部官方实现描述成已实现生产 API。
- 本文件是 Frozen TDD，不能替代 Coding Contract 或 Implementation Plan；正式编码仍需后续明确授权。

## 32. Remaining Implementation Questions

以下是实现前仍需评审/验证的实现细节；它们不重新开启 TV Gate：

1. Tab URL 最终携带哪些 action/view/context 信息、特殊 Action 处理和 popup blocker 行为，由 Implementation Plan、Coding Contract、JS tests 与 Browser tests 收口。
2. FormView template extension 的 selector/slot 在支持的 Form、Chatter、Notebook 组合中的最小兼容集。
3. thin Controller integration 采用 sub-env、service 还是显式 host props 的最终接口。
4. server helper 的具体 Odoo 18 ORM 调用组合、DTO 字段和稳定错误码。
5. Monetary currency field 的依赖字段和复杂 relational/display 值的格式化边界。
6. 长文本截断、Pane 最小宽度和浏览器 popup blocker 的产品文案。
7. 配置菜单、访问组 XML ID 和升级迁移策略。
8. 记录被删除或权限在请求期间撤销时的最终 UI 文案。

这些问题必须在 Implementation Plan、Coding Contract 或测试设计中解决。当前没有新的未声明 P0 blocker。

## 33. Exit Criteria

本 TDD 可进入下一阶段的条件：

- 技术评审确认 §6、§8、§11、§12、§13、§15、§16、§20 的正式选择；
- 所有 SRS FR/BR/CFG/NFR 均可追溯到本 TDD 和测试；
- 明确 navigation builder、host、state、loader、renderer 的接口边界；
- Python/JS/browser/HVR 测试策略被接受，且正式测试不依赖 Spike；
- 权限、fallback、stale request、记录删除/撤权、narrow 不覆盖均有测试用例；
- upgrade risk 和 remaining questions 有责任人/后续阶段入口；
- TD-003 的实现约束、测试覆盖和特殊 Action 错误处理已在后续实现阶段明确，且没有新增 P0 blocker；
- 用户另行批准后，才可创建 Implementation Plan 和 Coding Contract，随后才可编码。

## 34. Version History

| 版本 | 日期 | 状态 | 说明 |
|---|---|---|---|
| v0.1.0 | 2026-09-18 | Draft / 仅技术评审 / 不授权编码 | 基于 Agent Principles、SRS Frozen v1.0.0、TV Plan Frozen v0.1.1、TVR v0.2.0 和 SPIKE-02 证据形成技术设计；正式模块、架构、权限、生命周期、测试和决策已列明 |
| v0.1.1 | 2026-09-18 | Draft / 仅技术评审 / 不授权编码 | 根据评审修订 Loader 权限结果契约、配置模型访问边界、Opening Mode 来源、fallback 语义、source/state/responsive 的冻结粒度和测试用例；TD-003 标记为 TV-02 Pending Verification；主架构不变 |
| v0.1.2 | 2026-09-18 | Draft / 仅技术评审 / 不授权编码 | 删除 TV-02 及其 Freeze Gate；冻结 Tab Design Decision、Source Identity 语义、`open_mode` XML contract、server-side Preview Loader、受控配置元数据读取、Frozen SRS fallback、small-screen vertical stacked 和无 Preview cache；主架构不变 |
| v1.0.0 | 2026-09-18 | Frozen / 技术设计已冻结 | 用户最终评审通过；TDD 设计边界、接口契约、权限边界、生命周期、响应式策略、错误处理和测试策略冻结；后续需单独评审 Implementation Plan / Coding Contract |
