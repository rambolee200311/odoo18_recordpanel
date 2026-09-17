# TV-01 Many2one + Form Preview 技术可行性验证计划

> **文档状态：Draft**
>
> 本文件只定义技术事实验证计划，不是 TDD、Implementation Plan、Coding Contract 或正式实现方案。

## 1. Document Metadata

| 项目 | 内容 |
|---|---|
| TV ID | TV-01 |
| 标题 | Many2one + Form Preview 技术可行性验证计划 |
| 文档路径 | `docs/context/designing/TV-01-many2one-form-preview-feasibility-plan.md` |
| 版本 | v0.1.1 |
| 状态 | Draft |
| 日期 | 2026-09-17 |
| Odoo 版本 | 18.0 Community Edition |
| 仓库基线 | `2d43189`（`main`，与 `origin/main` 一致） |
| SRS 基线 | `SRS-many2one-related-record-view-enhancement.md` v1.0.0，Frozen |
| 上游需求 | `docs/requirement/需求分析报告RAR.md`，讨论稿 |
| Agent 原则 | `docs/context/principle/AGENT_OPERATION_PRINCIPLES.md` |
| 作者 | AI assistant |
| 审批状态 | 待用户评审和明确批准 |

### 1.3 文档目录依据

本文件保留在 `docs/context/designing/`，因为当前项目已将设计阶段的 SRS 和 TV Plan 统一放置于该目录。本次不新建或迁移到第二套 TV 专用目录。

### 1.1 当前工作区说明

TV Plan 起草时工作区存在项目认知文件的未提交变更。该变更不属于本 TV Plan，也不作为 TV 证据。TV 计划阶段不得提交、推送或修改该变更。

### 1.2 版本和状态边界

- 本计划依据的是已冻结的 SRS v1.0.0，不把上游讨论稿当作冻结需求。
- SRS 后续若发生需求变更，必须重新检查本计划的 TVQ、验收标准和实验范围。
- 本文件是 Draft，未获批准前不得执行其中的运行时观察或最小实验。

---

## 2. Verification Objective

本 TV 的目标是分阶段通过 Odoo 18.0 Community Edition 官方源码、可选的第三方参考源码和后续受控验证，确认 Many2one 关联记录查看增强在进入 TDD 前必须明确的技术事实。

本 TV 重点回答：

1. 是否可以复用官方 Many2one 的记录选择、搜索、清空和权限行为，只扩展显式使用增强能力的字段的“打开关联记录”行为；
2. 是否存在保持当前页面并在新标签页打开完整 Odoo 记录页面的标准路径；
3. Preview Pane 应位于哪个扩展层级，才能成为页面级、非覆盖式、可复用的宿主；
4. 单 Preview Pane 和当前来源 Many2one 的生命周期能否在 Odoo 18 页面生命周期中可靠维护；
5. 动态 Preview 字段、业务可读展示和 Odoo 原有权限边界能否安全组合；
6. Extend 的持续同屏和窄屏安全降级是否具备标准 Web Client 层面的可行路径。

这些问题会阻断或约束后续 TDD，但本 TV 不冻结最终组件架构、数据模型、服务 API 或实现文件。

### 2.1 分阶段执行 Gate

TV 执行分为两个阶段：

```text
TV Plan Draft
      ↓ 用户批准
Phase A：官方源码 + 第三方参考源码 + 非破坏性运行时观察
      ↓
Phase A Evidence / 每个 TVQ 初步结论
      │
      ├── 证据充分 → PASS / CONDITIONAL PASS
      │
      └── 仍有 P0 NOT VERIFIED
                  ↓
Phase B：Minimal Technical Spike
                  ↓ 用户再次明确批准
             仅执行获批的条件性 EXP
```

- Phase A 是默认允许的 TV 执行范围；
- EXP-01 属于 Phase A 的观察型实验；
- EXP-02、EXP-03、EXP-04 均为 `CONDITIONAL`，只有 Phase A 仍无法回答对应 P0 问题时，才可提出并再次申请执行；
- Phase B 不得借实验之名预先实现正式 Widget、Preview、Store、Configuration 模型或业务模块；
- Phase A 证据充分时，不得为了“证明方案”而启动 Phase B。

---

## 3. In Scope

本次 TV 覆盖以下六个 Verification Questions：

- **TVQ-01**：Odoo 18 Many2one 官方打开关联记录链路；
- **TVQ-02**：Tab 模式新标签页打开完整关联记录；
- **TVQ-03**：Extend Preview Pane 的页面级宿主；
- **TVQ-04**：单 Preview Pane 与当前来源生命周期；
- **TVQ-05**：动态 Preview 字段读取、格式化和权限；
- **TVQ-06**：非覆盖式布局和窄屏降级。

验证范围只限于当前 SRS v1.0.0 Frozen 的 MVP：

- 保持未增强 Many2one 的官方行为；
- `tab`；
- `extend`；
- 单 Preview Pane；
- 当前 Preview 来源 Many2one；
- 只读 Preview；
- 单模型一套 Preview Configuration；
- 字段级和记录级权限边界；
- 无可用详细配置时的安全降级；
- 非覆盖式同屏和窄屏安全原则。

---

## 4. Out of Scope

本 TV 明确不包含：

- 正式模块设计；
- 最终组件架构；
- DDD；
- TDD；
- 数据模型设计；
- 完整 UI 设计；
- 具体页面样式、像素尺寸或 breakpoint；
- 性能优化、压测或容量指标；
- 正式业务代码；
- 自定义模块代码；
- Coding Contract；
- Implementation Plan；
- Implementation；
- 多 Preview Profile；
- 用户个人 Preview 配置；
- Preview 内编辑或完整 Form 嵌入；
- 多 Preview Pane；
- 通用 Split View 框架；
- Preview 页面设计器；
- Preview 宽度拖拽；
- 生产数据验证；
- 直接数据库读写；
- 修改 Odoo 官方代码或官方 addons；
- 修改项目自定义业务代码；
- 安装模块、升级模块或修改数据库；
- Commit、Push 或 Release。

---

## 5. Preconditions

| 前置条件 | 状态 | 说明 |
|---|---|---|
| Odoo 18 官方源码存在 | CONFIRMED | 当前工作区包含 `odoo/`、官方 `addons/` 和 `addons/web/` |
| Odoo 版本 | CONFIRMED | `odoo/release.py` 标识为 18.0 Community Edition |
| Git 仓库基线 | CONFIRMED | `2d43189`，`main` 与 `origin/main` 一致 |
| SRS 基线 | CONFIRMED | SRS v1.0.0，状态 Frozen |
| Agent 操作原则 | CONFIRMED | 已阅读 `docs/context/principle/AGENT_OPERATION_PRINCIPLES.md` |
| 项目认知 | CONFIRMED | 已阅读 `docs/context/cognition/PROJECT_COGNITION.md` |
| 基础需求分析 | CONFIRMED | 已全文阅读 `docs/requirement/需求分析报告RAR.md` |
| 可运行的 Odoo 18 Web Client 环境 | UNKNOWN | 本 TV Plan 阶段不启动服务、不执行浏览器观察 |
| 可用的受控测试数据库 | UNKNOWN | 不假设存在，不在本阶段创建或修改 |
| 可用的浏览器开发工具观察条件 | UNKNOWN | 运行时验证前再确认 |
| 可创建隔离实验模块的批准 | NOT GRANTED | 当前只允许制定计划，禁止创建实验模块 |
| 第三方参考模块源码及版本 | UNKNOWN | 仅在来源、版本和许可证可确认后作为辅助证据检查 |

若任一运行时前置条件在 TV 执行前仍为 UNKNOWN，必须将对应 TVQ 标记为 BLOCKED 或降低结论等级，不得以假设替代证据。第三方参考模块不是必要前置条件；其缺失不得被第三方实现经验替代官方证据。

---

## 6. Verification Questions

### TVQ-01 — Odoo 18 Many2one 官方打开关联记录链路

**Question：**  
Odoo 18 Many2one 的官方“打开关联记录”入口经过哪些 Component、Method、Service 和 Action？record id、resModel、context 如何传递？是否存在不复制完整 Many2one 实现、只扩展打开行为的标准扩展路径？

**Why it matters：**

- SRS 要求保留记录选择、搜索、清空和其他官方行为；
- 自定义实现若复制完整 Many2one，可能造成升级和行为漂移风险；
- TVQ-01 是 `tab` 和 `extend` 复用官方入口的基础。

**Expected evidence：**

- Many2one 字段入口组件和注册信息；
- readonly 点击或外部打开入口到打开动作的调用关系；
- `get_formview_action`、action service 和关联记录页面之间的参数传递；
- resModel、record id、context 的来源和去向；
- 官方支持的 Field、Registry、Hook 或其他扩展边界；
- 区分公开扩展机制、Odoo Web Client 自身使用的标准 patch/inheritance 等扩展机制、复制官方代码和修改官方代码；
- 明确哪些路径是可维护的合法扩展路径，哪些只是内部实现细节。

**Blocking level：** P0。若无法只扩展显式增强字段而保留官方 Many2one 行为，TDD 不得进入正式实现。

### TVQ-02 — Tab 模式技术可行性

**Question：**  
是否存在可复用的 Odoo 18 Action、Router 或 URL 机制，使增强 Many2one 的原有打开入口能够在新浏览器标签页打开正常完整关联记录页面，并保留足够的 action、model、record、context 和适用导航上下文？

**Why it matters：**

- SRS 要求当前业务页面保持不变；
- 新标签页不能退化为孤立字段页面；
- 完整页面必须继续使用 Odoo 原有 Form、权限和业务按钮。

**Expected evidence：**

- 标准 action service 对 action、target 和 URL 的处理；
- router state 与 URL 的相互转换；
- 新标签页打开路径的浏览器行为证据；
- 普通记录 action 与 URL action 的差异；
- 新标签页是否能恢复正常页面上下文；
- 若只能打开新窗口、Dialog 或孤立页面，必须明确记录为限制。

**Blocking level：** P0。若无法可靠打开标准完整记录页面，Tab 模式不能进入 TDD；Extend 的“打开完整记录”入口也需要重新评估。

### TVQ-03 — Extend Preview Pane 页面级宿主

**Question：**  
Odoo 18 Web Client 中，Preview Pane 应挂在哪个标准扩展层级，才能不侵入具体业务 Form，同时保持当前业务区域可继续操作并形成非覆盖式布局？

**Why it matters：**

- Field Widget 只天然知道字段自身，不一定适合作为页面级 Pane 宿主；
- SRS 要求整个页面只存在一个 Preview Pane；
- 如果没有页面级宿主，单 Pane、来源切换和同屏布局可能只能通过侵入业务 Form 实现。

**Expected evidence：**

- Many2one Field Widget 的组件边界；
- FormRenderer、FormController 的职责和可扩展边界；
- Form View 外层页面结构；
- Action、Layout、Service、Registry、environment 等标准扩展机制；
- 可能承载页面级 Pane 的候选层级；
- 当前业务区域缩窄而非被覆盖的结构证据；
- 每个候选层级的通用性、侵入性和限制。

**Blocking level：** P0。若只能通过修改官方 Form 或侵入每个业务 Form 实现，必须阻断当前 MVP 的 TDD。

### TVQ-04 — 单 Preview Pane 与来源生命周期

**Question：**  
在 Odoo 18 OWL 生命周期下，多个 Many2one Field Widget 能否安全共享一个页面级 Preview 状态，并保证当前来源、替换、更新、清空、关闭、Form 切换和销毁行为符合 SRS？

**Why it matters：**

- 页面可以有多个 `extend` Many2one，但只能有一个 Pane；
- 只有当前 Preview 来源字段变化才更新或关闭 Pane；
- Widget 销毁或 Form 切换后不能残留旧 Preview。

**Expected evidence：**

- Field Widget、Form 层、Service、environment 或其他页面级对象的生命周期边界；
- OWL setup、mount、update、unmount 的可观察顺序；
- 页面级状态在 Form 切换和 Action 销毁时的清理点；
- 多个 Field Widget 共享状态而不互相误触发的可行机制；
- 跨 Action、跨 Form 或 Widget 销毁后状态残留的风险。

**Blocking level：** P0。若来源归属或生命周期无法可靠维护，单 Pane 需求不能进入 TDD。

### TVQ-05 — 动态 Preview 字段读取与权限

**Question：**  
Odoo 18 是否提供安全、通用的路径，按配置动态读取目标模型字段，并使用业务可读格式展示，同时区分字段级无权限和记录级无权限？

**Why it matters：**

- Preview Fields 不硬编码；
- SRS 要求 Many2one、Selection、Boolean、Date、Datetime、Monetary 等业务可读展示；
- 记录级无权限时不得泄露模型名、记录名或字段值；
- 不能绕过 Odoo 原权限体系。

**Expected evidence：**

- 动态字段元数据和字段集合获取方式；
- 业务可读 Label / Value 的官方格式化能力；
- Many2one 显示值是否会提前读取或泄露 display name；
- 字段级访问失败和记录级访问失败的实际业务表现；
- 只通过 Odoo 正式应用层和 ORM/RPC 时的权限边界；
- 无详细配置、部分字段不可读和整条记录不可读的安全降级依据。

**Blocking level：** P0。若无法证明记录级无权限不泄露信息，Preview 不得进入 TDD。

### TVQ-06 — 非覆盖式布局与窄屏降级

**Question：**  
Odoo 18 Form 页面结构是否具备标准扩展路径，使 Preview 成为真正占据布局空间的 sibling 区域，并在窄屏时安全降级而不覆盖当前主要业务区域？

**Why it matters：**

- SRS 明确禁止 Modal、Tooltip 和覆盖式 Drawer；
- Extend 的核心业务价值是持续同屏；
- Notebook、Chatter 和复杂 Form 布局可能改变可用宿主和兼容边界。

**Expected evidence：**

- Form 页面主要布局容器；
- 主业务区域与页面级附加区域的结构关系；
- Preview 作为 sibling 区域而非覆盖层的候选路径；
- Form 内部 Notebook、Chatter 等复杂区域的兼容风险；
- 窄屏时不覆盖主要区域的安全降级候选；
- 是否需要区分 desktop 和 narrow viewport，以及该判断的业务层边界。

**Blocking level：** P0。若只能通过覆盖当前业务区域实现，Extend 不满足 SRS；若只能在单一 Form 类型工作，必须标记为 CONDITIONAL PASS 并限制 TDD 范围。

---

## 7. Source Inspection Plan

以下是已从当前 Odoo 18 官方源码中定位出的候选证据区域。它们是源码检查计划和初步定位结果，不代表 TV 已经完成或任何 TVQ 已经 VERIFIED。

### 7.0 证据层级与第三方参考源码

按以下优先级收集证据：

1. **Level 1：Odoo 18 官方源码静态检查**；
2. **Level 2：Odoo 18 第三方参考实现源码检查**；
3. **Level 3：非破坏性运行时观察**；
4. **Level 4：Minimal Technical Spike**。

第三方参考模块只用于辅助识别已有人实践过的扩展方式，不能证明该方式属于稳定的 Odoo 官方公共 API，也不能替代官方源码或运行时证据。参考模块的具体路径、版本、许可证和可检查范围必须在执行报告中记录；未确认来源时不得引用其结论。

### 7.1 TVQ-01：Many2one 与关联记录打开链路

优先检查：

- `addons/web/static/src/views/fields/many2one/many2one_field.js`
  - `Many2OneField.setup()`
  - `openAction()`
  - `onExternalBtnClick()`
  - `onClick()`
  - 字段注册区域
- `addons/web/static/src/views/fields/relational_utils.js`
  - `useOpenMany2XRecord()`
  - `Many2XAutocomplete`
- `addons/web/static/src/webclient/actions/action_service.js`
  - `doAction` 及关联 action 执行路径

需要确认：

- `get_formview_action` 的调用参数；
- `action.doAction()` 接收的 action 结构；
- resModel、record id、context 的传递边界；
- Field Registry 是否支持只替换打开行为；
- 选择、搜索、清空逻辑是否可以完全复用。

### 7.2 TVQ-02：Action、Router、URL 与新标签

优先检查：

- `addons/web/static/src/webclient/actions/action_service.js`
  - `makeActionManager()`
  - `_executeActURLAction()`
  - `pushState()`
  - `stateToUrl()` 相关调用
- `addons/web/static/src/core/browser/router.js`
  - `PATH_KEYS`
  - `stateToUrl()`
  - `urlToState()`
- `addons/web/static/src/core/browser/browser.js` 或同等浏览器服务文件（待定位）

需要确认：

- 普通记录 action 与 `ir.actions.act_url` 的差别；
- `target="new"` 的实际语义；
- `_blank` 是否只对 URL action 生效；
- 新标签页是否可复用标准 Web Client URL state；
- action/context 是否完整可恢复。

### 7.3 TVQ-03：Form 页面级宿主

优先检查：

- `addons/web/static/src/views/form/form_controller.js`
  - `FormController`
  - `setup()`
  - `useModel()`
  - `useSetupAction()`
  - `useBus()`
  - `usePager()`
  - `static template`
- `addons/web/static/src/views/form/form_renderer.js`
  - `FormRenderer`
  - `static template`
  - `useSubEnv()`
  - `onMounted()`
  - `onWillUnmount()`
- `addons/web/static/src/search/layout.js`
  - `Layout`
  - `extractLayoutComponents()`
  - `contentRef`
- Form View 模板和 View 注册区域（具体路径待定位）
- Action、Registry、Service、environment 相关官方注册文件（具体路径待定位）

需要确认：

- FormController 与 FormRenderer 哪一层可承载页面级扩展；
- Layout 是否只承担 ControlPanel/SearchPanel，不能直接作为 Preview 宿主；
- 是否存在标准页面级 slot、service、registry、template extension、patch 或其他合法扩展入口；
- 是否存在不修改官方源码且不要求逐个修改业务 Form 的可维护扩展路径；
- 若不存在专用 Preview slot，记录可接受的标准扩展机制及其边界，不得因此自动判定为 FAIL。

### 7.4 TVQ-04：OWL 生命周期和共享状态

优先检查：

- `addons/web/static/src/views/fields/many2one/many2one_field.js`
  - `useState()`
  - `onWillUpdateProps()`
- `addons/web/static/src/views/form/form_renderer.js`
  - `useState()`
  - `useSubEnv()`
  - `useEffect()`
  - `onMounted()`
  - `onWillUnmount()`
- `addons/web/static/src/views/form/form_controller.js`
  - `useBus()`
  - `useState()`
  - `useEffect()`
  - `onMounted()`
  - `onRendered()`
- `addons/web/static/lib/owl/owl.js`
  - `useState()`
  - `useEffect()`
  - `useSubEnv()`
  - `useChildSubEnv()`
  - `onMounted()`
  - `onWillUpdateProps()`
  - `onWillUnmount()`

需要确认：

- environment 共享的边界；
- Form 切换、Action 销毁和 Widget 销毁的清理顺序；
- 官方 bus、service 或页面对象是否适合作为候选状态承载者；
- 不引入最终 Store/API 设计前，能否证明状态生命周期可靠。

### 7.5 TVQ-05：动态字段、格式化和权限

优先检查：

- `addons/web/static/src/views/fields/field.js`
  - `getFieldFromRegistry()`
  - `Field.parseFieldNode()`
  - `getFieldContext()`
  - `fieldVisualFeedback()`
- `addons/web/static/src/views/fields/formatters.js`
  - `formatMany2one()`
  - `formatReference()`
  - `formatMany2oneReference()`
- `addons/web/static/src/views/fields/many2one/many2one_field.js`
  - `extractProps()`
  - `canOpen`
  - `canCreate`
  - `canWrite`
- `addons/web/static/src/views/fields/relational_utils.js`
  - `useActiveActions()`
- `addons/web/static/src/views/form/form_controller.js`
  - `extractFieldsFromArchInfo()`
  - `addFieldDependencies()`
- 后端字段描述、读取权限和 ORM 读取路径（具体服务端路径待定位）

需要确认：

- 动态字段集合是否能通过官方数据访问路径读取；
- 业务可读格式化是否可复用，或仅适用于已有 Field Widget；
- 记录级访问失败是否会在 display name 读取前阻断；
- 字段级读取失败能否逐字段安全省略；
- 不使用裸 SQL、数据库驱动或游标绕过权限的前提下是否可行。

### 7.6 TVQ-06：布局和响应式边界

优先检查：

- `addons/web/static/src/views/form/form_controller.js`
- `addons/web/static/src/views/form/form_renderer.js`
- `addons/web/static/src/search/layout.js`
- Form View 外层模板（具体路径待定位）
- Chatter、Notebook 和 Form 内部布局相关官方模板（具体路径待定位）
- 官方响应式布局和 viewport 相关服务/组件（具体路径待定位）

需要确认：

- 是否存在 sibling 布局宿主；
- 主内容区域是否可以在不覆盖的情况下缩窄；
- Preview 是否会破坏 Notebook、Chatter、分页或复杂表单布局；
- 窄屏降级能否保持 SRS 的“不覆盖”原则；
- 哪些结论只能通过浏览器运行时观察获得。

### 7.7 初步定位但尚未形成结论的源码事实

当前源码定位已经显示出以下候选事实，但在 TV 执行前不标记为 VERIFIED：

- Many2one 的 `openAction()` 候选链路包含 `get_formview_action` 和 `action.doAction()`；
- Action Service 存在 router、state-to-URL 和 URL action 处理；
- Router 存在 model、resId、action 等路径状态；
- FormController、FormRenderer 和 Layout 分属不同层级；
- OWL 提供 `useState`、`useSubEnv` 和生命周期钩子；
- 官方存在 `formatMany2one()` 等字段显示格式化入口。

---

## 8. Runtime Observation Plan

运行时观察属于 Phase A。只有在源码和参考源码仍无法回答关键问题时，才进入对应的 Phase B Spike。

运行时观察只在源码静态验证不足时进行，并且必须先获得 TV Plan 批准。

### 8.1 TVQ-01 / TVQ-02 运行时观察

观察内容：

- 用户点击 Many2one 原有打开入口时的 action 调用；
- action 的 model、record id、context 和 view 信息；
- 当前页面 URL 状态变化；
- 新标签页的 URL、页面类型、Form、导航和业务按钮；
- 当前页面是否保持不变；
- 普通 action、URL action 和 `target="new"` 的实际差异。

证据要求：

- 浏览器 Network / Console / Action 日志或等价非破坏性证据；
- 不修改官方代码；
- 不改变正式业务数据。

### 8.2 TVQ-03 / TVQ-04 运行时观察

观察内容：

- FormController、FormRenderer、Field Widget 的挂载和销毁顺序；
- 同一页面多个 Many2one 的实例关系；
- Form 切换、返回、Action 切换时的清理行为；
- 页面级布局区域是否可形成 sibling；
- 一个页面范围内共享状态的自然生命周期。

证据要求：

- OWL 生命周期日志、开发模式组件树或等价非破坏性观察；
- 观察结束后不得留下服务、状态或数据残留。

### 8.3 TVQ-05 运行时观察

观察内容：

- 已授权记录和未授权记录的读取结果；
- 记录级无权限时是否泄露 display name 或模型信息；
- 字段级无权限时是否可以只隐藏该字段；
- Selection、Many2one、Boolean、Date、Datetime、Monetary 的实际显示值；
- 无配置、停用配置和空 Preview Fields 的降级行为。

证据要求：

- 使用隔离测试数据和最小权限账号；
- 不使用直接数据库读取；
- 如需数据准备，只能在获批后通过 Odoo Shell + ORM；
- 不把前端“没有显示”直接等同于后端“没有泄露”，必须观察实际返回边界。

### 8.4 TVQ-06 运行时观察

观察内容：

- 普通 Form、包含 Notebook 的 Form、包含 Chatter 的 Form；
- Preview 打开后主区域是否缩窄；
- 是否发生覆盖、滚动容器破坏或主要内容不可操作；
- desktop 和 narrow viewport 下的行为；
- 安全降级候选是否保持不覆盖原则。

---

## 9. Minimal Experiment Plan

本节只定义实验，不执行实验，不创建实验模块。EXP-01 是 Phase A 观察型实验；EXP-02～EXP-04 是 Phase B 条件性 Spike，必须在 Phase A 形成证据缺口后逐项重新申请批准。

### EXP-01 — 官方关联记录打开链路观察

| 项目 | 内容 |
|---|---|
| 关联 TVQ | TVQ-01、TVQ-02 |
| 假设 | 官方 Many2one 打开链路可以被观察并区分普通 action、URL action 和新标签路径 |
| 最小设置 | 一个标准 Form 页面，一个标准 Many2one 字段，一个可访问关联记录 |
| 步骤 | 记录原有入口；观察 action/service/router；分别观察普通打开和新标签候选路径 |
| 预期观察 | 获得 model、resId、context、action、URL 和页面类型的证据 |
| Pass | 能明确复用官方入口并判断完整页面新标签路径 |
| Fail | 只能复制官方 Many2one 或无法获得标准完整页面 |
| Cleanup | 不创建模块；关闭测试页面；不修改业务数据 |
| 风险 | 浏览器策略可能影响新标签行为；Action 内部 API 可能不是稳定扩展点 |

### EXP-02 — 页面级 Preview 宿主与非覆盖布局 Spike（CONDITIONAL）

| 项目 | 内容 |
|---|---|
| 关联 TVQ | TVQ-03、TVQ-06 |
| 启动条件 | Phase A 源码、参考源码和运行时观察仍无法确认页面级扩展路径，且存在 P0 NOT VERIFIED |
| 假设 | 某种合法 Web Client 扩展机制可以承载页面级区域，不要求 Odoo 已提供专用 Preview slot |
| 最小设置 | 一个隔离标准 Form 页面；只验证候选扩展机制的布局占位，不实现正式 Preview 业务能力 |
| 步骤 | 在再次获批后，针对一个候选扩展机制建立最小技术 Spike，观察主区域与附加区域的占位关系 |
| 预期观察 | 主区域可缩窄，附加区域不覆盖主要内容，当前 Form 仍可操作 |
| Pass | 证明至少一个允许的扩展路径具备非覆盖布局基础，并记录其限制 |
| Fail | 允许的扩展路径只能使用 Modal/Drawer/覆盖层，或必须修改官方源码/逐个业务 Form |
| Cleanup | 按二次批准范围撤销 Spike；不得删除用户文件；仅在用户明确许可后清理获批实验产物 |
| 风险 | Notebook、Chatter、复杂 Form 和窄屏可能导致候选路径只具备 CONDITIONAL PASS |

### EXP-03 — 单 Pane 与来源字段生命周期 Spike（CONDITIONAL）

| 项目 | 内容 |
|---|---|
| 关联 TVQ | TVQ-04 |
| 启动条件 | Phase A 仍无法仅通过官方生命周期和状态边界判断来源归属与清理可靠性，且存在 P0 NOT VERIFIED |
| 假设 | 页面级状态机制可以区分来源字段，且 Form/Action 销毁时自然清理 |
| 最小设置 | 一个隔离 Form 页面和两个占位事件源；不实现正式 `extend` Widget、Preview Pane 或业务状态 API |
| 步骤 | 在再次获批后，以最小事件/状态 Spike 模拟打开 A、打开 B、修改 A、修改 B、清空来源、关闭和 Form 切换 |
| 预期观察 | B 成为来源；A 变化不影响状态；B 变化更新；来源清空关闭；Form 销毁清理 |
| Pass | 只证明 Odoo 页面生命周期支持所需的来源隔离和清理边界，不冻结最终 Store/API |
| Fail | 生命周期无法区分来源、出现跨 Form 残留，或必须实现正式业务组件才能得到结论 |
| Cleanup | 关闭并撤销隔离 Spike；不修改正式业务数据 |
| 风险 | OWL 重渲染、Action 切换和异步读取可能产生竞态或延迟状态；Spike 结果不得外推为正式实现结论 |

### EXP-04 — 动态字段和权限边界 Spike（CONDITIONAL）

| 项目 | 内容 |
|---|---|
| 关联 TVQ | TVQ-05 |
| 启动条件 | Phase A 仍无法确认动态字段集合的安全读取、格式化或权限边界，且存在 P0 NOT VERIFIED |
| 假设 | 给定运行时动态 field-name list 时，可以遵守记录级和字段级权限并安全格式化可读值 |
| 最小设置 | 一个目标模型、TV 内固定的动态字段集合（例如 `name`、`country_id`、`active`、`date`、`amount`），记录级授权/无权账号和字段级差异权限；不创建 Preview Configuration 模型 |
| 步骤 | 在再次获批后，以固定字段集合模拟“未来配置返回的字段名列表”；观察字段元数据、读取返回、格式化和权限异常 |
| 预期观察 | 记录级无权不泄露身份；字段级无权只隐藏字段；可读字段按业务形式显示；字段集合为空时可安全降级 |
| Pass | 所有权限边界和格式化结果均有实际返回或页面证据，且未创建正式配置模型或业务模块 |
| Fail | 读取 display name 即泄露记录身份、权限异常无法区分或必须绕过 ORM |
| Cleanup | 撤销隔离 Spike；任何测试数据清理必须经过用户明确许可 |
| 风险 | 后端字段描述和前端格式化结果可能存在差异；必须区分“不返回”和“前端不渲染” |

本阶段不建立其他实验。若上述实验无法回答问题，必须先追加具体实验计划并重新获得批准。

---

## 10. Evidence Standard

### VERIFIED

仅当满足以下全部条件时使用：

- 结论直接来自当前 Odoo 18 官方源码或受控运行时证据；
- 记录了文件路径、类/组件、方法或可复现观察步骤；
- 证据与结论一一对应；
- 没有依赖未验证的浏览器、权限或生命周期假设。

### PARTIALLY VERIFIED

源码或实验已经确认了部分路径，但仍有一个或多个关键边界未确认。必须列出已确认和未确认部分，不得用于无条件冻结 TDD。

### NOT VERIFIED

当前只有问题定义或候选路径，尚未有足够源码或运行时证据。

### BLOCKED

由于环境、权限、测试数据、批准或工具条件缺失，无法按计划获得证据。必须记录阻断原因。

### NOT FEASIBLE

证据已经表明当前 SRS 要求与 Odoo 18 官方扩展边界冲突，或只能违反 Agent 原则才能实现。

禁止使用以下内容单独标记 VERIFIED：

- “看起来可行”；
- 其他版本 Odoo 的记忆；
- 仅有接口名称但无调用关系；
- 仅有页面没有报错；
- 仅有前端隐藏但没有权限返回证据。

---

## 11. Decision Rules

### 11.1 通用判定

- **PASS**：TVQ 的关键问题已由源码和必要运行时证据回答，未发现当前 SRS 阻断。
- **CONDITIONAL PASS**：存在可行路径，但依赖明确限制、特定 Form 场景、后续设计约束或尚未完成的非阻断证据。
- **FAIL**：证据表明当前 SRS 行为不能通过允许的标准扩展机制实现。
- **BLOCKED**：尚未获得足够证据，原因是环境、批准或实验条件不足。

### 11.2 分题判定

| TVQ | PASS 条件 | CONDITIONAL PASS 条件 | FAIL / BLOCKED 条件 |
|---|---|---|---|
| TVQ-01 | 可复用官方 Many2one 行为，只扩展打开动作；路径可以是公开扩展机制或 Odoo Web Client 自身采用的可维护 patch/inheritance 等机制 | 需要稳定的显式配置约束、有限扩展入口或对内部机制有明确升级风险控制 | 必须复制官方 Many2one、修改官方代码，或关键链路无法确认 |
| TVQ-02 | 能在新标签打开正常完整记录页面，且上下文和权限可保留 | 只在特定 action/context 场景可靠 | 只能打开孤立内容、覆盖当前页面或无法安全传递上下文 |
| TVQ-03 | 存在符合 Odoo 18 Web Client 扩展机制、无需修改官方源码且无需逐个修改业务 Form 的可维护页面级扩展路径 | 只能对明确 Form 范围或特定宿主成立，或依赖某种合法扩展机制的内部边界 | 必须修改官方源码、逐个侵入业务 Form，或只能由字段承担页面级 Pane |
| TVQ-04 | 来源、替换、更新、清空、关闭和销毁均可可靠区分 | 需要明确页面边界或有限生命周期约束 | 出现跨 Form 残留、来源误触发或无法清理 |
| TVQ-05 | 动态字段、格式化和两级权限边界均有安全证据 | 部分字段类型或展示规则需要限制 | 记录级身份泄露、必须绕过权限或无法安全降级 |
| TVQ-06 | 可形成非覆盖 sibling 布局并定义安全窄屏路径 | 仅部分 Form 类型可靠，需限制 MVP | 只能使用覆盖层，或窄屏必然覆盖主要业务区域 |

TV 完成后仍不得直接冻结 TDD。TV 只提供技术事实、约束和候选路径，最终技术方案必须在 TDD 中单独设计和评审。

---

## 12. Risks

- 复制官方 Many2one 逻辑造成升级风险和行为漂移；
- 官方内部 API 或组件结构变化导致扩展点不稳定；
- Preview 宿主侵入业务 Form，导致每个业务页面需要单独适配；
- 页面级状态泄漏到其他 Action 或 Form；
- 当前 Preview 来源丢失，导致其他 Many2one 误更新或误清除；
- Action 或 context 丢失，导致新标签页无法恢复标准页面；
- 记录级或字段级权限信息泄露；
- `display_name` 或其他标识在权限判断前被读取；
- 非覆盖式布局破坏标准 Form、Notebook、Chatter 或分页；
- 窄屏行为退化为覆盖式 Drawer 或不可操作页面；
- OWL 重渲染、异步读取和页面销毁之间出现竞态；
- 官方源码内部实现被误当成稳定公共扩展 API；
- 受控实验污染正式业务数据或留下状态残留。

---

## 13. Expected Deliverables

TV 执行完成后，预期形成：

- TV Verification Report；
- TVQ-01 ～ TVQ-06 的逐题结论；
- 官方源码证据矩阵；
- 运行时观察证据；
- 必要实验记录；
- PASS / CONDITIONAL PASS / FAIL / BLOCKED 判定；
- 进入 TDD 的技术事实约束；
- 不得进入 TDD 的实现假设；
- 未解决问题和后续决策项。

TV Verification Report 不得把候选方案直接写成最终架构，也不得替代 TDD。

---

## 14. Exit Criteria

只有满足以下条件，TV 才可以标记完成：

- TVQ-01 ～ TVQ-06 均有明确结论；
- 每个结论都有对应源码、运行时或受控实验依据；
- 所有 P0 阻断项均已明确；
- 没有用推测、记忆或“看起来可行”替代验证；
- 记录级无权限与字段级无权限均有安全结论；
- 新标签完整页面和 action/context 行为有明确结论；
- 单 Pane、来源字段和页面销毁生命周期有明确结论；
- 非覆盖布局和窄屏安全降级有明确结论；
- 所有实验均可追溯、可撤销且未污染正式业务；
- 可以明确判断是否具备进入 TDD 的技术基础；
- 用户已评审 TV Verification Report。

当前 TV Plan 不满足 Exit Criteria，也不应被标记为 TV 完成。

---

## 15. 当前阶段结论

本文件仅为 **TV Plan v0.1.1 Draft**。

当前可以确认：

- Odoo 18 官方源码和 SRS 基线存在；
- 已定位若干需要检查的 Many2one、Action、Router、Form、OWL 和格式化源码区域；
- 六个 TVQ 已建立；
- Phase A / Phase B 执行 Gate 已建立；
- EXP-01 已定义为 Phase A 观察型实验，EXP-02～EXP-04 已标记为需二次批准的条件性 Spike；
- 第三方参考源码已加入辅助证据层，但不得替代官方证据；
- EXP-04 使用固定动态字段集合，不创建 Preview Configuration 模型；
- 运行时环境、测试数据和实验批准状态仍有 UNKNOWN 或 NOT GRANTED 项。

当前不能确认：

- Tab 是否能够稳定打开保留完整上下文的标准记录页面；
- Preview Pane 的最终页面级宿主；
- 单 Pane 来源状态的可靠生命周期；
- 动态字段读取与记录级权限安全边界；
- 非覆盖布局和窄屏降级在标准 Form 中的可靠性。

等待用户评审和明确批准后，才允许进入 TV 执行阶段。
