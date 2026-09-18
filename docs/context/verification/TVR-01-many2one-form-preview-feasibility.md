# TV-01 Many2one + Form Preview 技术可行性验证报告

> **报告状态：Draft / Verification Complete**
>
> 本报告只记录 TV-01 Phase A 已取得的技术事实、证据、限制和未解决问题，不冻结 TDD，不宣布最终架构，也不授权 Phase B Spike。

## 1. Document Metadata

| 项目 | 内容 |
|---|---|
| Report ID | TVR-01 |
| 关联 TV | TV-01 Many2one + Form Preview 技术可行性验证计划 |
| 报告版本 | v0.2.0 |
| 状态 | Draft / Verification Complete |
| 日期 | 2026-09-18 |
| Odoo 版本 | 18.0 Community Edition |
| 当前 Git HEAD | `e5141a4` |
| origin/main | `e5141a4` |
| TV Plan 源码基线 | `2d43189`（当前 HEAD 的父提交，官方源码未变化） |
| SRS 基线 | v1.0.0 Frozen |
| TV Plan 基线 | v0.1.1 Frozen |
| 执行者 | AI assistant |
| 批准状态 | Phase A 和 SPIKE-02 已获授权；报告待用户最终评审 |

## 2. Executive Verification Summary

本轮已完成 Phase A，并执行了唯一获批的 Phase B 技术 Spike：`SPIKE-02 — Form Preview Host & Page-scoped State Feasibility`。

| 项目 | 结果 |
|---|---|
| 已检查 TVQ | TVQ-01 ～ TVQ-06 |
| 官方源码证据 | 已取得 |
| 第三方参考源码 | 未发现 |
| 非破坏性运行时观察 | EXECUTED |
| Phase B Spike | SPIKE-02 EXECUTED |
| PASS | TVQ-02、TVQ-03、TVQ-04、TVQ-05 |
| CONDITIONAL PASS | TVQ-01、TVQ-06 |
| FAIL | 0 |
| BLOCKED | 无（Phase A 各 TVQ 均已取得阶段性结论） |
| TVQ-01 | CONDITIONAL PASS |
| TVQ-02 | PASS — within TV scope |
| TVQ-05 | PASS — within TV scope |
| TVQ-03 | PASS — within SPIKE-02 scope |
| TVQ-04 | PASS — within SPIKE-02 scope |
| TVQ-06 | CONDITIONAL PASS |
| P0 阻断 | 无 |
| 是否需要继续 Phase B | 否；SPIKE-02 已完成，剩余事项转为 TDD / Implementation / Test Constraint |

当前结论不是“方案不可行”，而是：

> 官方源码、标准 Form、记录导航 URL、ORM 权限边界以及 SPIKE-02 的实际运行时证据共同表明：当前 SRS 没有发现不可行的技术事实阻断。最终组件选择、CSS 参数、断点、正式 Widget/API 和自动化测试仍属于后续 TDD/Implementation 范围。

## 3. Environment and Baseline Evidence

### 3.1 Git 基线

- 当前分支：`main`。
- `HEAD` 与 `origin/main`：均为 `e5141a4`。
- TV Plan 记录的仓库基线：`2d43189`。
- `e5141a4` 只增加了已冻结的 TV Plan，官方 Odoo 源码相对于 `2d43189` 未变化。
- 工作区存在一项与 TV 无关的未提交修改：
  - `docs/context/cognition/PROJECT_COGNITION.md`
- 本报告没有覆盖、清理、提交或修改该无关变更。

### 3.2 Odoo 源码

- `odoo/release.py` 的 `version_info` 为 `(18, 0, 0, FINAL, 0, '')`。
- 同文件声明 `license = 'LGPL-3'`。
- 当前验证使用工作区中的 Odoo 18 Community 官方源码。

### 3.3 运行时环境

| 条件 | 状态 | 说明 |
|---|---|---|
| 当前项目 Python/Odoo 运行环境 | CONFIRMED | `venv/bin/python` 可用，可导入 Odoo 18，`odoo-bin --help` 正常 |
| 当前项目 Odoo Web Client 服务 | CONFIRMED | 使用 `odoo-bin -c odoo.conf --dev=all` 启动，`127.0.0.1:8091` 正在监听并响应 `/web` |
| 当前项目运行配置 | CONFIRMED | `odoo.conf` 使用 `db_host = 127.0.0.1`、`db_port = 5555`、`db_name = odoo18ce`，addons 路径包含 `mymodules` |
| 当前项目测试数据库 | UNKNOWN | 未创建、未连接、未修改 |
| 当前项目浏览器开发工具 | UNKNOWN | 未进行页面观察 |
| 当前项目测试账号和权限数据 | UNKNOWN | 未创建、未修改 |
| 第三方参考模块 | NOT FOUND | `mymodules/` 只有 `.DS_Store`，没有可检查模块源码 |
| SPIKE-02 隔离模块 | INSTALLED | `wd_spike_02_form_preview` 通过 Odoo ORM 安装；仅注入技术占位和技术事件源，不修改业务数据 |

本机存在其他工作区的 Odoo/ PostgreSQL 进程，但它们不属于当前项目。本报告没有连接、观察或修改这些环境。前一版检查曾错误使用默认 `8069`；根据当前项目 `odoo.conf` 复核后，已改为检查 `8091`。当前项目 Web 服务已由本轮授权命令启动。

## 4. Evidence Index

### 4.1 官方源码证据

| Evidence ID | Type | Related TVQ | Source / Location | Observation | Supports | Does Not Prove |
|---|---|---|---|---|---|---|
| SRC-001 | OFFICIAL_SOURCE | TVQ-01 | `addons/web/static/src/views/fields/many2one/many2one_field.js`；`Many2OneField.setup()` | Many2one 通过 `useService("orm")`、`useService("action")` 和 `useOpenMany2XRecord()` 建立字段能力 | 官方 Field 组件与服务边界 | 不证明自定义打开行为已有专用公共 API |
| SRC-002 | OFFICIAL_SOURCE | TVQ-01 | 同文件 `openAction()`、`onClick()`、`onExternalBtnClick()` | 只读可打开点击入口调用 `openAction()`；外部按钮在非 Dialog 情况也调用 `openAction()` | 原生打开入口和入口条件 | 不证明新标签页行为 |
| SRC-003 | OFFICIAL_SOURCE | TVQ-01 | 同文件 `openAction()` | 从 `props.relation`、当前 record 字段 context 和 `record.evalContext` 形成 context，再 ORM 调用 `get_formview_action`，最后调用 `action.doAction(action)` | model、record id、context 到 Action Service 的链路 | 不证明 action 可直接在新标签页复用 |
| SRC-004 | OFFICIAL_SOURCE | TVQ-01 | `addons/web/static/src/views/fields/relational_utils.js`；`useOpenMany2XRecord()` | Many2X Dialog 打开路径独立于 Many2one 的标准页面 `openAction()`，通过 `get_formview_id` 和 `FormViewDialog` 打开 | 原生选择/搜索/创建/Dialog 能力与页面打开路径可区分 | 不证明业务增强必须复制作法 |
| SRC-005 | OFFICIAL_SOURCE | TVQ-01 | `addons/web/static/src/views/fields/field.js`；`getFieldFromRegistry()`、`Field.parseFieldNode()` | Field 类型和 widget 由 Field Registry 解析，字段节点可指定 widget | 显式字段可以通过 registry 选择不同组件 | 不证明具体增强组件的最终注册方式 |
| SRC-006 | OFFICIAL_SOURCE | TVQ-02 | `addons/web/static/src/webclient/actions/action_service.js`；`_executeActWindowAction()`、`doAction()` | Window Action 由 Action Service 创建 Controller；`target === "new"` 对 Form 有特殊处理，且普通 Window Action 不等同于浏览器 `_blank` | 普通记录 Action 的内部执行边界 | 不证明普通 Window Action 可稳定新标签 |
| SRC-007 | OFFICIAL_SOURCE | TVQ-02 | 同文件 `_executeActURLAction()` | `ir.actions.act_url` 的非 `self` 路径调用 `browser.open(url, "_blank")`，并处理 Popup 被阻止的情况 | 存在官方新标签 URL Action 机制 | 不证明它能自动生成带完整 Action/context 的记录 URL |
| SRC-008 | OFFICIAL_SOURCE | TVQ-02 | `addons/web/static/src/core/browser/router.js`；`PATH_KEYS`、`stateToUrl()`、`urlToState()`、`pushState()` | Router 序列化 `resId`、`action`、`active_id`、`model` 等状态，并可从 URL 恢复状态；代码注释允许在 custom webclient 中 patch state/URL 转换 | 标准 URL State 可表达部分记录导航状态 | 不证明 context、完整 action stack 和业务导航上下文全部可恢复 |
| SRC-009 | OFFICIAL_SOURCE | TVQ-03 | `addons/web/static/src/views/form/form_controller.js`；`FormController` | FormController 是 `web.FormView` 的 Controller，持有 action、dialog、orm、view、ui、company 等服务，并使用 `useModel()`、`useSetupAction()`、`useBus()` | 页面级 Form Controller 是候选观察层 | 不冻结最终宿主或组件架构 |
| SRC-010 | OFFICIAL_SOURCE | TVQ-03 / TVQ-06 | `addons/web/static/src/views/form/form_controller.xml`；`web.FormView` | 外层结构为 root → `.o_form_view_container` → `Layout` → Form Renderer；Renderer 作为 Layout 默认内容 | 页面存在主容器、Layout 和 Renderer 的层级事实 | 不证明插入 sibling 后布局一定非覆盖 |
| SRC-011 | OFFICIAL_SOURCE | TVQ-03 / TVQ-06 | `addons/web/static/src/search/layout.xml`；`web.Layout` | Layout 包含 ControlPanel、可选 SearchPanel、`.o_content` 和 default slot；`contentRef` 指向内容容器 | Layout 是页面内容容器候选观察层 | 不证明 Layout 提供 Preview 专用 slot 或 split layout |
| SRC-012 | OFFICIAL_SOURCE | TVQ-03 | `addons/web/static/src/views/form/form_view.js`；`formView`、`registry.category("views")` | Form View 注册包含 Controller、Renderer、ArchParser、Model、Compiler 和 buttonTemplate | 可评估 View Registry/Controller/Renderer 级扩展 | 不证明最终扩展不会依赖内部 API |
| SRC-013 | OFFICIAL_SOURCE | TVQ-03 / TVQ-04 | `addons/web/static/src/views/form/form_renderer.js`；`FormRenderer.setup()` | Renderer 使用 `useState({})`、`useSubEnv({ model })`、`onMounted()`、`onWillUnmount()`；其模板来自编译后的 Form Arch | Renderer 的局部状态和生命周期边界 | 不证明它适合作为页面唯一状态宿主 |
| SRC-014 | OFFICIAL_SOURCE | TVQ-04 | `addons/web/static/lib/owl/owl.js`；`useState()`、`useSubEnv()`、`useChildSubEnv()`、`useEffect()`、`onMounted()`、`onWillUnmount()` | OWL 提供响应式状态、子环境和挂载/卸载清理机制；`useEffect()` 在卸载时执行 cleanup | 存在实现页面范围状态和清理的底层机制 | 不证明多个真实 Many2one 实例已可靠共享单 Pane |
| SRC-015 | OFFICIAL_SOURCE | TVQ-04 | `addons/web/static/src/views/form/form_controller.js`；`useSetupAction()`、`getLocalState()` | Form Controller 将 `modelState`、`resId` 和 Notebook 状态纳入 Action 本地状态，并参与 beforeLeave/beforeUnload | Form 与 Action 有状态边界和离开钩子 | 不证明 Preview 状态自动纳入或自动清理 |
| SRC-016 | OFFICIAL_SOURCE | TVQ-05 | `odoo/models.py`；`fields_get()`、`check_field_access_rights()`、`read()`、`check_access_rule()` | ORM 提供字段元数据、字段访问检查、记录读取和记录规则检查入口 | 动态字段集合可以通过正式 ORM/RPC 机制表达，且存在权限检查层 | 不证明未授权场景的实际响应不会泄露身份，需运行时权限证据 |
| SRC-017 | OFFICIAL_SOURCE | `addons/web/static/src/core/orm_service.js`；`read()`、`call()` | Web ORM Service 将模型读取和方法调用通过正式 RPC/ORM 入口发送 | 动态字段读取有正式前端调用路径 | 不证明当前用户在具体数据和规则下的返回边界 |
| SRC-018 | OFFICIAL_SOURCE | TVQ-05 | `addons/web/static/src/views/utils.js`；`getFormattedValue()` | 根据 record field type 从 formatter registry 取 formatter，并传递 field/data/options | 字段类型到业务可读 formatter 有标准入口 | 不证明任意动态字段都可无损展示 |
| SRC-019 | OFFICIAL_SOURCE | TVQ-05 | `addons/web/static/src/views/fields/formatters.js`；formatter registry | 已注册 Boolean、Date、Datetime、Many2one、Monetary、Selection 等 formatter | 基础字段类型存在可复用格式化机制 | 不证明权限失败时 formatter 会自动安全降级 |
| SRC-020 | OFFICIAL_SOURCE | TVQ-06 | `addons/web/static/src/views/form/form_renderer.js`、`form_controller.xml` | Form Renderer 使用 Notebook；Form 外层还存在按钮、Layout 和内容容器 | 复杂 Form 结构有已知兼容边界 | 不证明增加外部 sibling 后 Notebook/Chatter/滚动行为正常 |

### 4.2 第三方参考证据

本项目 `mymodules/` 未发现第三方参考模块源码，因此没有 `REF-*` 证据。不能把其他工作区或网络模块当作本项目已提供的参考实现。

### 4.3 运行时证据

| Evidence ID | Type | Related TVQ | Source / Location | Observation | Supports | Does Not Prove |
|---|---|---|---|---|---|---|
| RUN-001 | RUNTIME_OBSERVATION | TVQ-01～06 | `odoo.conf`、`127.0.0.1:8091/web`、浏览器页面 | 按配置启动 Odoo 后，服务监听 `8091`，`/web` 返回登录重定向；用户完成登录后进入 `/odoo/discuss` | 当前 Odoo Web Client、认证和浏览器观察条件已建立 | 不证明 Many2one、Tab、Preview、权限或布局行为 |
| RUN-002 | RUNTIME_OBSERVATION | TVQ-02 | 浏览器访问 `/odoo/contacts` | 当前数据库没有名为 `contacts` 的 Action，页面显示 “The action contacts does not exist” | 当前 Action 路由必须使用数据库中真实存在的 Action，不能凭模型/菜单名称猜测 | 不证明标准记录页面或新标签行为不可行 |
| RUN-003 | RUNTIME_OBSERVATION | TVQ-01、TVQ-03、TVQ-06 | Inventory → Receipts → `WH/IN/00005`；`Receive From` Many2one 的 `Internal link` | 标准 Receipt Form 包含 `Receive From`、`Operation Type`、`Product` 等 Many2one，并包含 Notebook、Chatter；点击 `Receive From` 的 `Internal link` 后进入 `/odoo/receipts/12/res.partner/9` 的标准 `res.partner` Form，原 Receipt 面包屑仍可见 | 真实 Many2one 入口、关联 model/record 页面和复杂 Form 运行时存在 | 不证明增强 Widget、Preview Pane 或新标签行为 |
| RUN-004 | RUNTIME_OBSERVATION | TVQ-02 | 新浏览器页打开已观察到的 `/odoo/receipts/12/res.partner/9` | 新页面加载正常 `res.partner` Form，显示 Wood Corner、字段、Notebook、Chatter，并保留 Receipt 面包屑 | 记录 URL 可以加载完整标准 Form，并保留部分导航上下文 | 不证明官方 Many2one 点击入口已经自动以 `_blank` 打开，也不证明全部 action/context 可恢复 |
| RUN-005 | ORM_RUNTIME_OBSERVATION | TVQ-05 | Odoo Shell + ORM；`res.partner` id `9`；现有 `portal` 用户 id `7` | Portal 用户对目标关联记录执行 `check_access_rule('read')` 和 `read(['name', 'display_name'])` 均被 `AccessError` 拒绝；拒绝后再次读取仍被拒绝 | 记录级拒绝不会返回记录名称、`display_name` 或字段值 | 不证明所有模型和所有规则组合行为完全一致 |
| RUN-006 | ORM_RUNTIME_OBSERVATION | TVQ-05 | Odoo Shell + ORM；`res.partner` id `9`；现有内部 `demo` 用户 id `6` | `fields_get()` 只返回 `name`、`email` 等可读字段，不返回受 `base.group_erp_manager` 限制的 `signup_type`；读取 `name/email` 成功，单独读取 `signup_type` 被 `AccessError` 拒绝 | 字段级权限可以与记录级权限区分；可读字段可继续读取，不可读字段不会出现在元数据集合 | 不证明前端 Preview 的最终过滤实现 |
| RUN-007 | RUNTIME_OBSERVATION | TVQ-02 | 两个已共享浏览器页面；`/odoo/receipts/12/res.partner/9` | 两个页面均加载同一 `res.partner` 记录的完整 Form，均可见 Receipt 面包屑、标准字段、Notebook、Chatter 和业务操作区域；两个页面相互独立存在 | 记录导航 URL 可在新页面稳定恢复 SRS 所需的完整记录查看上下文，当前页面不被替换 | 不证明浏览器原生 Many2one 点击本身自动使用 `_blank`，也不证明复制完整内存 Action Stack |

当前运行时已可用，并已取得 Inventory 标准 Receipt Form、Many2one 关联记录、Notebook、Chatter 和 SPIKE-02 技术占位场景。RUN-005/RUN-006 使用既有用户和 ORM 完成权限观察；SPIKE-02 未创建业务数据，未修改业务记录。

### 4.4 Spike 证据

| Evidence ID | Related TVQ | Environment / Setup | Actual observation | Result | Supports | Does Not Prove |
|---|---|---|---|---|---|---|
| EXP-002-A | TVQ-03、TVQ-06 | 已安装隔离模块 `wd_spike_02_form_preview`；标准 `res.partner` Form；`web.FormView` template extension + FormController patch | 技术占位作为 Form 根容器的 sibling 出现；桌面 viewport 1132px 下 Form 约 812px、Placeholder 约 320px，同一 y 坐标、无水平重叠 | PASS | 无需修改官方源码或逐个业务 Form 即可形成右侧占位 sibling | 不证明最终 Preview 宿主或正式 CSS |
| EXP-002-B | TVQ-03、TVQ-06 | 同一标准 Form；Notebook、Chatter、字段和操作区域 | Notebook 页面可切换；Chatter、字段和主 Form 操作区域仍存在；Placeholder 保持独立布局区域 | PASS | 复杂 Form 基础结构在技术占位实验下保持可用 | 不证明所有 Form 类型和所有 Chatter 组合 |
| EXP-002-C | TVQ-06 | viewport 调整为 640×900 | 根布局切换为纵向；Placeholder 位于主 Form 下方，宽度与页面一致，无覆盖；恢复桌面 viewport 后回到右侧 sibling | PASS / CONDITIONAL | 窄屏存在不覆盖式安全降级基础 | 不冻结最终 breakpoint、断点或响应式设计 |
| EXP-002-D | TVQ-04 | 技术 Source A / Source B 按 B1–B5 顺序触发 | A 激活后显示 A；B 激活替换 A；A 非当前更新被忽略；B 当前更新生效；A 清空不影响 B | PASS | 单页面单状态和当前来源归属具备可行行为 | 不证明正式 Many2one Widget 或业务 API |
| EXP-002-E | TVQ-04 | 按 B6–B7 触发 B 清空、A 激活和主动关闭 | B 清空后状态为 closed；A 主动关闭后状态清除；Form 数据未改变 | PASS | 当前来源清空和主动关闭行为可区分 | 不证明正式 Preview 数据和权限逻辑 |
| EXP-002-F | TVQ-04 | A 激活后离开到 Discuss，再返回同一 Form | 离开 Form 后返回时 Placeholder 重新挂载且状态为 closed；未残留旧 source/value | PASS | 页面级状态可随 Form/Action 生命周期清理 | 不证明所有异步竞态和跨标签生命周期 |
| EXP-002-G | TVQ-03、TVQ-06 | 首次桌面布局观察后发现 Odoo 默认 column 规则覆盖实验 row 规则；仅修改 Spike CSS 后重载 | 使用实验 CSS 修正后恢复真正右侧 sibling；未修改官方源码 | PASS with recorded iteration | 记录了候选路径的实际 CSS 冲突和可修正性 | 不证明最终 CSS 方案无需 TDD 调整 |

### 4.5 文档证据

| Evidence ID | Type | Related TVQ | Source | Observation |
|---|---|---|---|---|
| DOC-001 | UPSTREAM_DOCUMENT | TVQ-01～06 | Frozen SRS v1.0.0 | 规定 `tab`、`extend`、单 Pane、来源字段、权限边界、非覆盖布局和窄屏原则 |
| DOC-002 | UPSTREAM_DOCUMENT | TVQ-01～06 | Frozen TV Plan v0.1.1 | 规定 Phase A/Phase B Gate、第三方证据只能辅助、EXP-02～04 需二次批准 |
| DOC-003 | UPSTREAM_DOCUMENT | TVQ-01～06 | Agent Operation Principles | 禁止修改官方代码、直接读写数据库、未经许可删除文件 |

## 5. TVQ-01 Verification Result

### Question

Odoo 18 Many2one 的官方打开入口如何传递 model、record id、context 并进入 Action Service？是否存在不复制完整 Many2one 实现、只扩展显式字段打开行为的合法扩展路径？

### Verified Facts

1. `Many2OneField` 通过 `this.relation` 获取目标模型，通过 `this.value[0]` 获取关联 record id。
2. `openAction()` 将 `openActionContext`、字段 context 和 `record.evalContext` 合成为 ORM context。
3. `openAction()` 调用目标模型的 `get_formview_action`，再调用 `this.action.doAction(action)`。
4. readonly 点击和外部按钮入口均可进入 `openAction()`；Dialog 场景使用不同的 `useOpenMany2XRecord()` 路径。
5. Field Registry 根据字段类型、widget、view type 和 jsClass 解析组件，因此显式配置字段可以选择增强组件。
6. Many2XAutocomplete、选择、搜索、创建和 Dialog 打开路径由组件/工具分别承载，原生页面打开动作不是整个 Many2one 行为的唯一实现点。

### Unverified Facts

- 当前没有证据证明存在一个专门命名的公开 `openAction` 扩展 API。
- 尚未通过运行时确认自定义 Field 组件或 patch 能否在不改变选择、搜索、清空、创建和权限行为的情况下只替换页面打开动作。
- 尚未验证不同字段配置、readonly 状态和 Dialog 上下文的组合行为。

### Constraints and Risks

- 允许评估 Field Registry、标准 patch/inheritance 或其他 Odoo Web Client 扩展机制；不得复制完整官方 Many2one 或修改官方源码。
- 依赖内部方法或组件结构时必须在 TDD 中记录升级风险，不能伪称为稳定公共 API。

### Decision

**PASS — within TV scope**

源码已回答官方链路；Inventory Receipt Form 的 `Receive From` Many2one 运行时验证了标准内部打开入口，目标 `res.partner` Form 可正常加载。只增强打开动作且完整保留选择、搜索、清空、创建和权限行为仍未验证，因此该结论受限于后续扩展验证。

## 6. TVQ-02 Verification Result

### Question

是否可以在保留当前页面的情况下，新标签打开标准完整 Odoo 关联记录页面，并保留足够的 action、model、record、context、view 和导航上下文？

### Verified Facts

1. 普通 Many2one 页面打开通过 `get_formview_action` 和 `doAction()` 进入 Window Action 执行。
2. Action Service 对 Window Action 创建 View Controller；`target="new"` 是 Action 层语义，不等于浏览器新标签。
3. `ir.actions.act_url` 的非 `self` 路径明确调用 `browser.open(url, "_blank")`。
4. Router 可序列化并恢复 `action`、`model`、`resId`、`active_id` 等部分状态。
5. Router 的 `stateToUrl()` / `urlToState()` 是可检查和可扩展的状态转换边界，但当前源码没有证明完整 action/context 栈能由任意记录 URL 恢复。

### Unverified Facts

- 普通关联记录 Window Action 是否能在不退化为 URL Action 的情况下稳定新标签打开。
- 使用记录 URL 或 `act_url` 时，原始 action、view、context、breadcrumb、active_id 和业务按钮是否完整恢复。
- 新标签中的权限、Form、按钮和导航上下文是否与标准 Action 打开完全一致。

### Decision

**PASS — within TV scope**

运行时已证明稳定的关联记录 URL 可以在独立浏览器页面加载完整 `res.partner` Form，并保留 Receipt 面包屑、标准字段、Notebook、Chatter 和业务操作区域；原业务页面仍然存在且未被替换。结合官方 Router 对 `model`、`resId`、`action` 等状态的表达能力，已足以确认满足 SRS 的新标签完整记录导航具备技术基础。

本结论不要求复制原标签的全部内存 Action Stack、不可序列化 context 或浏览器历史；Frozen SRS 未将这些内部状态定义为强制结果。具体增强入口如何触发 `_blank` 仍属于后续 TDD/实现约束，不构成当前 TV Scope 内的可行性阻断。

## 7. TVQ-03 Verification Result

### Question

是否存在无需修改官方源码、无需逐个修改业务 Form 的可维护页面级 Preview 扩展路径？

### Candidate Extension Layers

以下只是基于源码的候选比较，不是最终 TDD 选择：

| Candidate | 源码事实 | 已知限制 |
|---|---|---|
| A：Many2one Field 层 | Field Registry 支持按字段 widget 解析；Many2one 有独立入口 | 天然是字段范围，不能单独证明页面唯一 Pane 或页面 sibling |
| B：Form View/Controller 层 | Form View 注册 Controller、Renderer、Model、Compiler；FormController 持有 Layout、Action、Bus、生命周期 | 需要确认扩展是否依赖内部 View/Controller 结构，尚无运行时证据 |
| C：模板/Layout/页面容器层 | `web.FormView` 有 root、`.o_form_view_container`、Layout 和 Renderer；Layout 有 `.o_content` 与 default slot | 没有专用 Preview slot；非覆盖 sibling 和复杂 Form 兼容未验证 |
| D：Service/environment 层 | OWL 提供 service、env/subEnv、bus 和生命周期钩子 | 状态传递机制存在，但页面宿主和销毁绑定尚未证明 |

### Verified Facts

- 官方 Form 页面有明确的 Controller、Renderer、Layout 和外层模板边界。
- Form View Registry 允许以 View 描述关联 Controller、Renderer、Model 和 Compiler。
- Layout 默认承担 ControlPanel、SearchPanel 和 `.o_content`，源码没有显示专用 Preview slot。
- OWL 提供 environment、service、bus 和生命周期机制。

### Unverified Facts

- 是否存在无需逐个业务 Form 改造的可维护 sibling 扩展路径。
- 哪个候选层级能同时满足页面范围、非覆盖布局、Form 可继续操作和生命周期清理。
- 没有专用 Preview slot 时，标准 patch/template inheritance 是否足够稳定。

### Decision

**PASS — within SPIKE-02 scope**

SPIKE-02 已在标准 `res.partner` Form 上证明：通过 `web.FormView` template extension 和 FormController patch，可以在不修改官方源码、不逐个修改业务 Form 的情况下形成真正占据布局空间的右侧技术 sibling。主 Form、Notebook、Chatter 和操作区域仍可用。没有专用 Preview slot 不构成 FAIL，且本结论不冻结最终宿主或 TDD 方案。

实际 Preview 业务内容、最终组件选择和正式 CSS 仍属于 TDD/Implementation 范围。

## 8. TVQ-04 Verification Result

### Question

Odoo 18 OWL 页面生命周期是否允许多个 Many2one Field Widget 与一个页面级 Preview 状态建立可靠关系？

### Verified Facts

- Field、FormRenderer 和 FormController 都是 OWL Component。
- OWL 提供 `useState()`、`useSubEnv()`、`useEffect()`、`onMounted()`、`onWillUpdateProps()` 和 `onWillUnmount()`。
- `useEffect()` 在组件卸载时执行 cleanup。
- FormController 通过 `useSetupAction()` 参与 beforeLeave/beforeUnload，并保存部分本地状态。
- FormRenderer 使用 `useSubEnv({ model })`，说明环境可以向子树传播。

### Unverified Facts

- 多个实际 Many2one Field Widget 是否能在页面范围安全区分当前来源字段。
- Form 切换、Action 切换、rerender 和异步读取时，来源状态是否会残留或误触发。
- 是否有现成 Service、bus 或 environment 边界可以在不构造正式业务组件的情况下承载该状态。

### Decision

**PASS — within SPIKE-02 scope**

SPIKE-02 的 Source A/B 运行时证据证明：一个 Form 页面可以承载单一技术状态；B 可以替换 A；非当前来源变化不影响当前状态；当前来源更新、清空和主动关闭均有效；离开 Form/Action 后返回不会残留旧状态。正式 Many2one Widget、业务 API 和所有异步竞态仍属于 TDD/Implementation/Test 范围。

## 9. TVQ-05 Verification Result

### Question

给定运行时动态字段名集合，是否可以通过 Odoo 正式机制安全读取关联记录并业务可读展示？

### Verified Facts

- ORM 的 `fields_get()`、`check_field_access_rights()`、`read()` 和 `check_access_rule()` 分别提供字段元数据、字段访问、记录读取和记录规则检查入口。
- Web ORM Service 提供 `read()` 和 `call()` 等正式 RPC 调用路径。
- `getFormattedValue()` 通过字段类型查找 formatter，并把 field/data/options 传给 formatter。
- Formatter Registry 已注册 Boolean、Date、Datetime、Many2one、Monetary、Selection 等基础类型。
- Many2one formatter 使用记录返回的 id/display value；源码本身不能证明该 display value 在记录权限检查前后何时可见。

### Unverified Facts

- 记录级无权限时后端是否会在返回前阻断 display_name 和其他身份信息。
- 字段级无权限时，动态 field-name list 的实际响应是拒绝、忽略还是部分返回。
- 部分字段不可读、空字段集合和无详细配置时的安全降级行为。
- 各基础类型的实际本地化和业务展示结果。

### Decision

**PASS — within TV scope**

正式 ORM/RPC 和 formatter 基础已确认。通过现有 `portal` 与内部 `demo` 用户的 Odoo Shell + ORM 观察，已证明：

- 记录级无权访问时，`check_access_rule('read')` 和后续 `read()` 均拒绝，不返回记录名称或 `display_name`；
- 字段级无权访问时，受限字段不出现在 `fields_get()`，可读字段仍可读取，直接读取受限字段被拒绝。

因此，SRS 要求的记录级不泄露和字段级省略具备正式权限链路基础。TVQ-05 在当前 TV Scope 内通过；其他模型、复杂规则组合和前端最终过滤属于 TDD、实现和自动化测试约束，不能仅依赖 formatter。

## 10. TVQ-06 Verification Result

### Question

Odoo 18 Form 页面是否存在形成真正非覆盖 sibling layout 的技术基础，并能在窄屏安全降级？

### Verified Facts

- `web.FormView` 的外层是 root、`.o_form_view_container`、Layout 和 Form Renderer。
- Layout 使用 `.o_content` 承载默认内容，并可渲染 ControlPanel/SearchPanel。
- FormRenderer 负责 Notebook 等 Form 内部组件，并监听 resize。
- Form Controller 会根据 `env.isSmall` 调整部分按钮和控制面板行为。

### Unverified Facts

- Preview 是否能作为真正占用布局空间的 sibling，而不是覆盖 `.o_content`。
- Chatter、Notebook、复杂分组、滚动容器和分页在 sibling 布局下是否保持可操作。
- 窄屏是否能在不覆盖主要业务区域的前提下安全降级。

### Decision

**CONDITIONAL PASS**

SPIKE-02 已通过标准 Form、Notebook、Chatter、桌面布局和 640×900 窄屏观察证明：桌面可形成右侧非覆盖 sibling；窄屏可切换为纵向布局，Placeholder 位于主 Form 下方，不覆盖主要业务区域。

Condition：最终 breakpoint、复杂 Form 类型覆盖范围和正式降级规则仍需在 TDD/Implementation 中确定；本 Spike 不冻结这些参数。

## 11. Cross-TVQ Findings

1. **Tab 与 Extend 的共同基础**：两者都可以从 Many2one 的 `openAction()` 入口追踪到 ORM `get_formview_action()` 和 Action Service，但新标签和页面级 Preview 的后续路径不同，不能假设共享同一个最终扩展实现。
2. **页面宿主与状态生命周期耦合**：FormController、FormRenderer、Layout 和 OWL environment 都有候选事实，但没有 Phase A 证据证明哪个层级同时满足布局和状态清理。
3. **权限是后端边界问题**：formatter 只能负责展示，不能替代 ORM 的记录规则和字段访问检查；Preview 必须先确认记录级授权，再考虑 display_name 和字段格式化。
4. **官方源码没有显示专用 Preview slot**：这不是 FAIL 证据，只意味着 TDD 需要在合法 Web Client 扩展机制中评估候选路径和升级风险。
5. **Phase A 证据与 Phase B 证据必须分开**：当前 Web 服务、标准 Form 和 ORM 权限观察已足够形成 Phase A 阶段性结论；实际 Preview sibling 和跨字段状态行为仍只能通过获批的 Phase B Spike 验证。

## 12. TDD Input Constraints

以下只是已验证事实和边界，不是技术方案：

### TDD-C-01 — 保留官方 Many2one 分层行为

- Constraint：后续设计必须区分 Many2one 原生选择/搜索/创建/清空能力与关联记录页面打开动作，不得默认复制完整官方 Many2one。
- Evidence：SRC-001、SRC-002、SRC-004、SRC-005。
- Related TVQ：TVQ-01。

### TDD-C-02 — 官方打开链路的数据来源

- Constraint：任何扩展必须明确处理 relation/resModel、resId 和由字段 context/eval context 形成的 context。
- Evidence：SRC-003。
- Related TVQ：TVQ-01、TVQ-02。

### TDD-C-03 — Window Action 与新标签 URL 不能混同

- Constraint：设计不能把 `target="new"` 自动当作浏览器新标签；必须单独验证 Window Action、URL Action 和 Router state 的上下文保留。
- Evidence：SRC-006、SRC-007、SRC-008。
- Related TVQ：TVQ-02。

### TDD-C-04 — 页面宿主必须来自合法扩展边界

- Constraint：候选路径不得修改 Odoo 官方源码或逐个修改业务 Form；没有专用 Preview slot 时，必须明确记录所采用扩展机制的维护和升级风险。
- Evidence：SRC-009、SRC-010、SRC-011、SRC-012。
- Related TVQ：TVQ-03、TVQ-06。

### TDD-C-05 — 状态生命周期必须绑定页面边界

- Constraint：任何页面级状态设计都必须处理 OWL unmount、Form/Action 离开和来源字段归属；不能仅因 `useState()` 存在就假设生命周期可靠。
- Evidence：SRC-013、SRC-014、SRC-015。
- Related TVQ：TVQ-04。

### TDD-C-06 — 动态字段读取必须使用正式权限链路

- Constraint：动态字段集合只能通过正式 ORM/RPC 和 Odoo 权限机制处理；formatter 不得被当作权限检查。
- Evidence：SRC-016、SRC-017、SRC-018、SRC-019。
- Related TVQ：TVQ-05。

### TDD-C-07 — 非覆盖布局仍需运行时证据

- Constraint：Form 容器、Layout 或 `.o_content` 的静态存在不能作为非覆盖布局已实现的证明；复杂 Form 和窄屏必须单独确认。
- Evidence：SRC-010、SRC-011、SRC-020。
- Related TVQ：TVQ-06。

## 13. Remaining Unknowns

| UNKNOWN-ID | Related TVQ | Question | Why unresolved | Blocking | Required next evidence |
|---|---|---|---|---|---|
| UNKNOWN-01 | TVQ-01 | 只扩展打开动作是否保留所有原生 Many2one 行为 | 尚未创建增强 Widget；官方分层和 Field Registry 已确认合法扩展基础 | TDD / Implementation Constraint | 后续实现必须保留选择、搜索、创建、清空和权限行为，并补自动化测试 |
| UNKNOWN-02 | TVQ-02 | 稳定记录 URL 是否能在新页面打开完整记录 | RUN-004、RUN-007 已确认完整 Form、Notebook、Chatter、面包屑和业务区域可恢复 | Closed | — |
| UNKNOWN-03 | TVQ-02 | 是否复制原标签完整 action/context 内存栈 | Frozen SRS 未要求复制不可序列化内存状态；必要记录导航上下文已观察 | Reclassified: Implementation/Test Concern | TDD/实现中明确 URL 与 Action/context 的必要映射 |
| UNKNOWN-04 | TVQ-03 | 实际 sibling 插入后的布局基础 | EXP-002-A/B 已证明标准 Form 下技术 sibling 可占位且主区域可用 | Closed | 最终宿主选择和业务内容转 TDD |
| UNKNOWN-05 | TVQ-04 | 单 Pane 当前来源和清理是否可靠 | EXP-002-D/E/F 已验证 Source A/B、清空、关闭和 Form/Action 清理 | Closed | 正式 Widget/API 和自动化测试转 TDD |
| UNKNOWN-06 | TVQ-05 | 其他模型和复杂规则组合下是否泄露 display_name | 当前仅验证 `res.partner` 的 portal 规则；正式 ORM 权限基础已确认 | Implementation/Test Concern | TDD/实现和目标模型自动化测试中复核 |
| UNKNOWN-07 | TVQ-05 | 前端动态字段过滤和格式化的最终组合行为 | ORM 元数据、字段读取拒绝和 formatter 基础已确认；未创建 Preview | Implementation/Test Concern | TDD/实现中先过滤权限，再格式化；不需要 TV Spike |
| UNKNOWN-08 | TVQ-06 | sibling 布局是否破坏 Chatter/Notebook/滚动 | EXP-002-B 已观察标准 Form、Notebook、Chatter 和主区域可用 | Closed within Spike scope | 更复杂 Form 类型转 TDD/Test |
| UNKNOWN-09 | TVQ-06 | 窄屏降级是否不覆盖主要区域 | EXP-002-C 已观察 640×900 下纵向、不覆盖降级 | TDD / Implementation Constraint | 由 TDD 确定 breakpoint 和最终降级规则 |
| UNKNOWN-10 | TVQ-01～06 | 当前项目可用的第三方参考模块 | 当前 `mymodules/` 无模块源码 | P2 / Non-blocking | 如后续发现具体参考模块再单独检查 |

## 14. SPIKE-02 Execution Record

### SPIKE-02 — Form Preview Host & Page-scoped State Feasibility

状态：

> **EXECUTED — PASS WITH CONDITIONS**

- Related TVQ：TVQ-03、TVQ-04、TVQ-06。
- Candidate used：`web.FormView` template extension + `FormController` patch；选择理由是它是已确认的页面级 Form 边界中最薄的实验路径。
- Objective A result：右侧技术 Placeholder 在标准 Form 中形成真实 sibling，主 Form、Notebook、Chatter 和操作区域保持可用。
- Objective B result：Source A/B 共享一个页面级技术状态，完成替换、当前来源更新、非当前来源忽略、清空、关闭和 Form/Action 清理。
- Narrow result：640×900 下切换为纵向布局，Placeholder 位于主 Form 下方，不覆盖主要业务区域。
- Conditions：实验只证明技术可行路径；最终宿主、正式 Widget/API、CSS、breakpoint、复杂 Form 覆盖范围和自动化测试必须在 TDD/Implementation/Test 中确定。
- Files created：见本报告第 17 节；均明确标记为 `TECHNICAL SPIKE — NOT PRODUCTION CODE`。
- Database impact：安装隔离模块 `wd_spike_02_form_preview`；未创建或修改业务数据。
- Official source impact：未修改 `odoo/` 或官方 `addons/`。

> `SPIKE-03` 已在 v0.1.1 合并至 `SPIKE-02`，编号不重新使用。
>
> `SPIKE-04` 已在 v0.1.1 移除：RUN-005/RUN-006 已回答 TV Scope 内的权限可行性问题。

## 15. Version History

| Version | Date | Change |
|---|---|---|
| v0.1.0 | 2026-09-17 | Phase A 初始报告，记录官方源码、RUN-001～RUN-006 和条件性/阻断结论 |
| v0.1.1 | 2026-09-18 | 根据 RUN-005/RUN-006 将 TVQ-05 收口为 PASS；补充 RUN-007 和 TVQ-02 最后一轮运行时观察；重新分类 UNKNOWN-01/06/07；关闭 UNKNOWN-02；合并 SPIKE-02/SPIKE-03；移除 SPIKE-04；修正 Summary 与 Final Status 一致性 |
| v0.2.0 | 2026-09-18 | 获授权执行 SPIKE-02；完成 EXP-002-A～G；回写 TVQ-03、TVQ-04、TVQ-06；关闭布局、状态和不覆盖技术可行性未知；更新 Final Status |

## 16. Final TV Status

**TV-01：VERIFICATION COMPLETE — READY FOR USER FINAL REVIEW**

Phase A 的官方源码静态检查、当前项目 Web Client 运行时观察和 ORM 权限观察已完成。唯一获批的 SPIKE-02 也已执行并取得实际运行时证据。TVQ-02、TVQ-03、TVQ-04、TVQ-05 在当前 TV Scope 内通过；TVQ-01 保持条件性通过；TVQ-06 为带 TDD 条件的条件性通过。

当前没有 P0 技术可行性阻断，没有发现违反 Frozen SRS 的结果，也不再提出新的 Phase B Spike。剩余事项均属于 TDD、Implementation 或 Test Constraint。

本报告完成后立即停止。不得自动进入 TDD、Implementation Plan、Coding Contract 或正式模块开发，等待用户最终评审 TVR v0.2.0。

## 17. Spike Files

本轮创建以下隔离实验文件，均为：

> **TECHNICAL SPIKE — NOT PRODUCTION CODE**

- `mymodules/wd_spike_02_form_preview/__init__.py`
- `mymodules/wd_spike_02_form_preview/__manifest__.py`
- `mymodules/wd_spike_02_form_preview/static/src/js/spike_02.js`
- `mymodules/wd_spike_02_form_preview/static/src/xml/spike_02.xml`
- `mymodules/wd_spike_02_form_preview/static/src/scss/spike_02.scss`

未修改任何 Odoo 官方源码、官方 addons 或现有正式业务模块。实验模块保持已安装状态；删除实验文件或卸载模块需要另行授权。
