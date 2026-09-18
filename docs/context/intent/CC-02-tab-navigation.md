# CC-02 Tab Navigation

> **Status: v1.0.0 FROZEN — IMPLEMENTATION AUTHORIZED**
>
> 本文档只起草 CC-02 Coding Contract。它不授权编码、Freeze、修改 CC-01 production implementation、实现 Extend/Preview、Commit 或 Push。完成本 Draft 后停止，等待用户评审。

## 1. Contract Metadata

| 项目 | 内容 |
|---|---|
| Contract ID | CC-02 |
| Contract Name | Tab Navigation |
| 版本 | v1.0.0 Frozen |
| 状态 | Frozen / Implementation Authorized |
| Odoo | 18.0 Community Edition |
| 正式模块 | `mymodules/wd_advanced_m2o_record_panel/` |
| 最小正式依赖 | `web` |
| 上游 SRS | v1.0.0 Frozen |
| 上游 TDD | v1.0.1 Frozen |
| 上游 Implementation Plan | v1.0.0 Frozen |
| 前置 Contract | CC-01 v1.0.0 Frozen / HVR PASS |
| 当前 branch | `main` |
| 当前 HEAD | `b7f30efc0cc460f7e0048657fc165e5c1f595eb7` |
| `origin/main` | `b7f30efc0cc460f7e0048657fc165e5c1f595eb7` |
| 工作区 | 有未提交的 CC-01 实现、证据文档和 TDD 勘误；本 Draft 不覆盖这些变更 |

## 2. Authorization

用户本轮授权：

- 基于 Frozen SRS、TDD、Implementation Plan 和已完成 CC-01 起草 CC-02 Draft；
- 重新读取并核对权威基线、正式模块代码和 Odoo 18 官方相关源码；
- 创建本 CC-02 Draft 及起草报告。

本轮授权：

- 将 CC-02 v0.1.1 Draft 冻结为 v1.0.0 Frozen；
- 实施 Tab Handler 和 Navigation Builder；
- 完成自动化验证和 Browser/HVR Checklist。

本轮未授权：

- 实现 Extend、Preview Pane、Preview State、Server Preview Loader 或 Renderer；
- 修改 Frozen SRS、TDD、Implementation Plan、TVR、Spike 或 CC-01；
- 创建 CC-03 或 CC-04；
- Commit、Push 或删除任何文件。

流程必须保持：

```text
CC-02 Draft
    ↓
CC-02 Frozen
    ↓
Implementation
    ↓
Automated Validation + Browser/HVR
    ↓
STOP
```

## 3. Re-read Baseline

本 Draft 起草前重新读取了：

1. [Agent Operation Principles](../principle/AGENT_OPERATION_PRINCIPLES.md)
2. [Frozen SRS](../designing/SRS-many2one-related-record-view-enhancement.md)
3. [Frozen TDD](../designing/TDD-many2one-related-record-view-enhancement.md)
4. [Frozen Implementation Plan](../designing/Implementation-Plan-many2one-related-record-view-enhancement.md)
5. [TVR-01](../verification/TVR-01-many2one-form-preview-feasibility.md)
6. [Frozen CC-01](CC-01-foundation-configuration-enhanced-many2one.md)
7. [CC-01 IHR](../handoff/IHR-CC-01-foundation-configuration-enhanced-many2one.md)
8. [CC-01 ATR](../verification/ATR-CC-01-foundation-configuration-enhanced-many2one.md)
9. [CC-01 HVR](../verification/HVR-CC-01-foundation-configuration-enhanced-many2one.md)
10. 当前正式模块代码
11. Odoo 18 Community related-record navigation 官方源码
12. 当前 branch、HEAD、`origin/main` 和 working tree

### 3.1 CC-01 baseline result

CC-01 HVR 1–15 已由用户报告 PASS，自动化 ATR 也已 PASS。CC-01 当前实现包括：

- 显式 `advanced_many2one` registry entry；
- `open_mode` 的 `native` / `tab` / `extend` capability resolution；
- CC-01 阶段所有合法和非法模式均 native fallback；
- 未实现 Tab Handler、Navigation Builder、Preview、Loader 或业务记录读取。

未发现影响 CC-02 的 `CONTRACT BLOCKER`。CC-01 的配置权限勘误与 Tab 导航无直接冲突；Implementation Plan 中早期关于配置 read 的旧文字不改变 CC-02 的导航边界，且不得在 CC-02 中修正文档漂移。

## 4. Goal

CC-02 唯一目标：

```text
advanced_many2one
        ↓
open_mode = tab
        ↓
Tab Handler
        ↓
Record Navigation Builder
        ↓
standard Odoo record URL
        ↓
browser "_blank"
        ↓
complete standard Odoo Form
```

当用户通过 Enhanced Many2one 的原生 related-record open entry 打开关联记录，且字段节点的 `open_mode` 为 `tab` 时：

- 新浏览器标签页打开完整标准 Odoo 记录页面；
- 当前业务页面保持不变；
- 当前 Form、Many2one 值和未保存 UI 状态不被主动清除；
- 目标页面继续由标准 Odoo 权限和业务规则处理。

## 5. In Scope

1. Tab Handler。
2. Record Navigation Builder。
3. 从原生 Many2one related-record open entry 接入 Tab dispatch。
4. 使用 Odoo Web Client 标准 Router URL state 表达必要的记录导航。
5. 输入 `target model`、`target resId` 和必要的可安全序列化 navigation context。
6. 在用户点击同步事件链内调用浏览器 `_blank` opening。
7. 新标签加载标准 Odoo Web Client 完整 Record Form。
8. 保持当前业务页面、Many2one 值和当前页面状态。
9. `missing` / `invalid` mode 的 native behavior regression。
10. `extend` 在 CC-03 尚未实现时继续 native fallback。
11. CC-03 “打开完整记录”可复用的最小 Navigation Builder contract。
12. CC-02 JS/Browser/HVR 直接相关的验证证据；仅在本轮存在 server-side change 时增加 Python tests。

## 6. Out of Scope

禁止实现：

- Extend Handler；
- Preview Pane、Preview Host、Preview State；
- Source Identity runtime；
- Server Preview Loader、Safe DTO、Preview RPC；
- Readonly Preview Renderer、formatter pipeline；
- stale Preview request handling；
- responsive Preview layout；
- multiple Pane、editable Preview、generic Split View；
- Preview Full Record button；
- custom business record loader；
- HTTP Controller；
- `stock` dependency；
- Odoo official source 或 official addons 修改；
- 重写或复制完整 Many2one；
- 修改默认 `many2one` registry；
- 修改 CC-01 production implementation 以绕过本 Contract 问题。

CC-02 不新增“Open in Tab”按钮。用户继续使用原生 related-record open entry。

## 7. Upstream Contracts

### 7.1 Mode dispatch

```text
native / missing / invalid
    → native open

tab
    → Tab Handler → new browser tab

extend
    → Extend Handler unavailable in CC-02 → native fallback
```

`tab` 和 `extend` 只来自 XML field node 的 options：

```xml
<field
    name="partner_id"
    widget="advanced_many2one"
    options="{'open_mode': 'tab'}"/>
```

直接使用普通 `many2one` 的字段必须完全保持原生。

### 7.2 Native entry

CC-02 必须接入当前 Many2one 的：

- readonly click related-record entry；
- non-dialog external related-record entry。

选择、搜索、autocomplete、create、create-and-edit、clear、display、readonly、required、disabled 和 no-create 行为不由 Tab Handler 接管。

Dialog 中的原生 Many2one Dialog 路径保持 Odoo native behavior。CC-02 MVP 不扩大 Dialog navigation semantics。

## 8. Navigation Builder Contract

### 8.1 Responsibilities

Builder 只负责：

1. 接收目标 `model` 和正整数 `resId`；
2. 接收必要且可序列化的 navigation context；
3. 根据 Odoo 18 Router 的标准 URL state 规则生成可恢复的标准 Web Client record URL；
4. 返回可由浏览器 `_blank` 打开的 navigation target；
5. 对缺失、非法或不可安全序列化的输入返回显式失败结果。

Builder 不负责：

- 读取目标业务记录；
- 检查或绕过业务权限；
- 调用 Preview Loader；
- 保存 Action Stack；
- 创建自定义 route；
- 生成 simplified form、iframe、modal 或 Preview 页面。

### 8.2 Target identity

目标内容身份至少为：

```text
target model + target resId
```

`resId` 必须是当前 Many2one 已有的有效关联记录 id。CC-02 不为了构建 URL 预读目标业务记录。

### 8.3 Standard URL semantics

Odoo 18 官方 Router 事实：

- `PATH_KEYS` 包含 `resId`、`action`、`active_id` 和 `model`；
- `stateToUrl()` 生成 `/odoo/...` 或 `/scoped_app/...`；
- `urlToState()` 可从路径恢复 action/model/resId state；
- `browser.open(url, "_blank")` 是官方新标签打开能力；
- `target="new"` 是 Action Service 的 Dialog/Window Action 语义，不等同于浏览器 `_blank`。

CC-02 应优先采用 Router 已验证的标准 state-to-URL 机制，而不是猜测裸 URL。Builder 的稳定最小契约是：

```text
targetModel + targetResId + optional proven-safe target navigation state
    → standard Router record URL
```

其中 `targetModel + targetResId` 是目标记录身份。`action/menu` 只能作为可选的、已经证明适用于 target model 的导航装饰；不得为了 breadcrumb/menu 完整度复用与 target model 不匹配的 source action。默认不继承 source `active_id`；只有当 Odoo 官方 Router 的目标记录 URL 语义明确要求、且该 identity 明确属于目标导航语义时，才允许携带。

Builder 只保留恢复目标完整 Record Form 所需的最小可序列化导航信息，例如：

- target `model`；
- target `resId`；
- 已证明适用于 target model 的可选 action/menu anchor；
- Odoo Web Client 能识别且明确属于目标导航语义的必要 state。

不得无差别复制：

- 完整当前 Action Stack；
- OWL component；
- service、env、record、model 实例；
- 当前页面所有 context；
- 不可序列化对象；
- 当前业务 Form 的未保存数据。

### 8.4 Context boundary

`necessary navigation context` 不等于 `entire current action context`。

允许携带的内容必须同时满足：

1. 标准目标 Record Form 恢复确实需要；
2. 可安全序列化为 URL/navigation target；
3. 不包含当前页面的临时组件状态；
4. 不扩大权限；
5. 不泄露敏感数据；
6. 不让目标页面误认为当前业务记录已写入。

无法安全序列化或无法证明必要性的 context 必须舍弃，而不是复制整个 context。若舍弃后无法满足标准完整记录页面，必须显式失败并记录诊断原因。

### 8.5 Action/view handling

普通标准记录导航优先使用可由 Router URL 恢复的 model/resId。只有已证明适用于 target model 的 optional target action anchor 才可携带；CC-02 不将 source action、source `active_id`、完整 `get_formview_action()` 结果或 Action Service 内存对象塞入 URL。

如某个特殊 action 需要异步 RPC 才能获得不可替代的 action/view 信息，则属于实现阻断：必须停止并提交证据。不得在点击后先 `await RPC`，再尝试创建新窗口，从而把浏览器打开移出同步用户点击链。

## 9. User-click Synchronization

Tab opening 必须发生在用户点击 related-record open entry 触发的同步浏览器交互链中：

```text
user click
    ↓
validate current model/resId
    ↓
build serializable standard URL synchronously
    ↓
browser.open(url, "_blank")
```

禁止默认设计：

```text
user click
    ↓
await RPC
    ↓
await action service
    ↓
window.open
```

当实现能够可靠识别 browser new-tab opening failure 或 popup blocking 时：

- 不伪装成成功；
- 不写业务数据；
- 当前页面保持安全；
- 使用标准、最小、可诊断的 warning/diagnostic behavior；
- 不自动改为当前页打开，除非后续 Contract Amendment 明确批准。

## 10. Current Page Preservation

成功的 `tab` 操作必须保证：

- 当前业务页面 URL 不被替换；
- 当前 Form 不重新加载；
- 当前 Many2one value 不变化；
- 当前未保存 UI state 不因 Tab navigation 主动清除；
- 不触发业务 write；
- 不创建 Preview State；
- 重复点击可以打开多个独立标准 Tab，而不会污染源页面。

## 11. Target Page Contract

新标签必须是正常 Odoo Web Client 完整记录页面，至少验证：

- 正确 target model；
- 正确 target resId；
- 标准 Form；
- 目标 Form 本身定义的标准 breadcrumb/navigation environment（适用时）；
- 目标 Form 本身定义的 Notebook、Chatter 和标准业务按钮（适用时）；
- 标准记录/字段权限；
- 非 modal、非 drawer、非 iframe、非 simplified clone。

目标页面的访问权限仍由标准 Odoo 页面处理。CC-02 不提前读取目标业务记录，不调用 `sudo()`，不自行伪造 access-denied 页面。

## 12. Error / Fallback Contract

| 情况 | CC-02 行为 |
|---|---|
| missing mode | native open |
| invalid mode | native open |
| `extend` | Extend Handler 尚未实现，native fallback |
| `tab` 且 target 合法 | 同步构建 URL，尝试 `_blank` |
| target model 缺失 | 不打开 blank/no-op；保留当前页并产生可诊断失败 |
| target resId 缺失/非法 | 不打开 blank/no-op；保留当前页并产生可诊断失败 |
| context 不可安全序列化 | 舍弃非必要部分；若无法形成标准目标则显式失败 |
| popup 被阻止 | 不伪装成功；当前页安全，显示最小诊断 warning |
| 目标记录无权访问 | 新 Tab 按标准 Odoo 目标页面权限行为处理 |
| 目标特殊 action 无法同步表达 | 标记实现约束并停止该路径，不引入异步 popup workaround |

普通标准路径不得静默降级为当前页；否则会违反 `tab` 业务语义。

## 13. Reuse Boundary for CC-03

CC-02 提供的可复用职责是：

```text
navigation.build(targetModel, targetResId, necessaryContext)
    → standardRecordUrl
```

CC-03 将来可以复用它实现 Preview 的“打开完整记录”，但 CC-02 不得：

- import Preview service/state；
- 接收 source identity；
- 接收 pane state；
- 添加 Preview-specific parameters；
- 创建 Full Record button；
- 依赖 CC-03 文件。

依赖方向必须是：

```text
CC-02 Navigation Builder
          ↑
          │ reused later
CC-03 Full Record action
```

## 14. Allowed Files

CC-02 允许修改或新增的最小区域：

```text
mymodules/wd_advanced_m2o_record_panel/
├── static/src/fields/
│   └── enhanced_many2one_field.js
├── static/src/navigation/
│   └── record_navigation.js
├── tests/
└── static/tests/
```

职责必须存在，但可以根据 Odoo 18 测试和模块结构将 Navigation Builder 合并到合理的同域文件。测试文件和 fixtures 可在已授权测试目录内创建。

如需修改其他生产目录、新模型、新 dependency、HTTP Controller、官方源码、Spike 或其他模块，必须 Stop / Contract Amendment。

## 15. Forbidden Files and Operations

禁止修改：

- `odoo/`；
- 官方 `addons/`；
- Frozen SRS、TDD、Implementation Plan、TVR；
- Frozen CC-01；
- CC-01 IHR、ATR、HVR；
- `mymodules/wd_spike_02_form_preview/`；
- 与 CC-02 无关的现有模块。

禁止：

- Commit；
- Push；
- 删除文件；
- `sudo()` 读取目标业务记录；
- 裸 SQL、直接 PostgreSQL 或数据库 patch；
- 复制完整 Many2one；
- 覆盖默认 `many2one` registry；
- 新增 `stock` dependency；
- 新增 HTTP Controller；
- 实现 Preview/Extend。

## 16. JavaScript Test Contract

至少覆盖以下可审计契约：

| ID | Contract |
|---|---|
| TAB-01 | missing `open_mode` 继续 native open |
| TAB-02 | invalid `open_mode` 继续 native open |
| TAB-03 | `open_mode=extend` 在 Extend Handler 不存在时继续 native fallback |
| TAB-04 | `open_mode=tab` 进入 Tab Handler |
| TAB-05 | Builder 使用正确 target model/resId |
| TAB-06 | Builder 产生标准 Odoo record URL 并调用 `_blank` |
| TAB-07 | 当前页面 navigation 不被替换 |
| TAB-08 | Many2one value 不发生变化 |
| TAB-09 | native search/select/create/clear 不被 Tab Handler 改写 |
| TAB-10 | 普通 `many2one` 完全不进入 enhanced/Tab path |
| TAB-11 | Builder 不需要 target business-record RPC/read |
| TAB-12 | 非法/不可构建 target 安全失败，不产生 blank/no-op/JS crash |
| TAB-13 | popup blocked 不伪装成功且当前页保持安全 |
| TAB-14 | 必要 navigation context 可序列化，完整 Action Stack 不被复制 |

不要为了增加测试数量制造无意义 mock。无法通过稳定 JS harness 证明的真实浏览器行为必须转移到 Browser/HVR。

## 17. Browser Verification Contract

必须在真实 Odoo 18 runtime 验证：

1. 普通 Many2one native open；
2. Enhanced missing mode native open；
3. Enhanced invalid mode native open；
4. Enhanced `extend` native fallback；
5. Enhanced `tab` 打开新浏览器标签；
6. 新标签 target model 正确；
7. 新标签 resId 正确；
8. 新标签加载完整标准 Odoo Form；
9. 目标 Form 本身定义的 breadcrumb/navigation environment、Notebook、Chatter 和业务按钮在适用时正常存在；
10. 原业务页面仍保持打开和可操作；
11. 原页面 Form/value 未意外变化；
12. 重复打开产生独立新标签；
13. 没有新的 JavaScript error；
14. 没有新的 asset load error；
15. 无权 target 按标准 Odoo 目标页面行为处理。

## 18. HVR Contract

人工重点场景：

```text
current business page
        +
click native Many2one related-record open entry
        ↓
new browser tab
        ↓
full related record
```

每项记录：

- Expected；
- Actual；
- PASS/FAIL；
- 浏览器页面/URL evidence；
- 用户角色；
- 使用模型和 record id。

必须确认：

- 当前页面仍在；
- 新 Tab 是完整 Odoo Record Form；
- 不是 modal、drawer、iframe、Preview 或 simplified page；
- target model/resId 正确；
- 当前 Form、Many2one value 和未保存状态未被主动改变。

## 19. Acceptance Gate

CC-02 Complete 至少要求：

1. Tab Handler 正常安装；
2. missing/invalid mode 仍 native；
3. `extend` 仍 native fallback；
4. `tab` 打开新浏览器 Tab；
5. current page 保持；
6. target model/resId 正确；
7. 新 Tab 加载标准完整 Odoo Record Form；
8. navigation context 满足 Frozen TDD；
9. 不复制完整 Action Stack；
10. 不增加 target business-record read；
11. 不使用 business `sudo()`；
12. 不新增 HTTP Controller；
13. 不实现 Preview；
14. 不改变 native Many2one；
15. 不修改官方源码；
16. 不增加 `stock` dependency；
17. automated evidence PASS；
18. Browser/HVR evidence PASS。

## 20. Stop Conditions

发生任一条件，保存证据并停止 CC-02：

| ID | Stop condition |
|---|---|
| STOP-01 | 需要修改 Odoo 官方源码 |
| STOP-02 | 必须复制/重写官方 Many2one |
| STOP-03 | 必须修改默认 `many2one` registry |
| STOP-04 | 必须引入 HTTP Controller |
| STOP-05 | 必须读取 target business record 才能构建 Tab navigation |
| STOP-06 | 必须使用 business `sudo()` |
| STOP-07 | 需要提前实现 Preview/Extend |
| STOP-08 | 需要完整复制 Action Stack |
| STOP-09 | 需要新增 `stock` 或无关 dependency |
| STOP-10 | 需要改变 Frozen SRS/TDD/Implementation Plan |
| STOP-11 | 需要修改 CC-01 Frozen contract 或修复 CC-01 scope defect |
| STOP-12 | 无法在用户点击同步链内可靠打开新 Tab，只能依赖异步 popup workaround |
| STOP-13 | 标准 URL 无法加载完整目标 Record Form，必须创建 custom route/page |

不得以 CC-02 偷修 CC-01；如触及上游契约，提交 Amendment/Design Change 请求并等待用户决策。

## 21. Contract Amendment

CC-02 Freeze 后不得静默改变。本 Draft 发现新问题时，必须提交：

- Issue；
- Evidence；
- Current Contract；
- Requested Change；
- Scope Impact；
- Architecture Impact；
- Test Impact。

## 22. Traceability

| CC-02 area | Frozen SRS | Frozen TDD | Implementation Plan | Evidence |
|---|---|---|---|---|
| Tab mode | FR-M2O-02/03、AC-02/03/04 | §8、§9、§19、§25、TD-003/004 | §8 CC-02 | TAB tests / Browser / HVR |
| current page preservation | FR-M2O-03、NFR-M2O-02、AC-03/19 | §9、§19、§25 | §8 CC-02 | Browser / HVR |
| standard complete Form | FR-M2O-03、BR-M2O-12 | §5、§9、§19 | §8 CC-02 | TVR RUN-003/004/007 + Browser |
| permission preservation | FR-M2O-03、AC-04 | §16、§19 | §8 CC-02 | Browser target-page behavior |
| native compatibility | FR-M2O-01、AC-01/20 | §8、TD-001/002 | CC-01 regression + §8 CC-02 | JS / Browser / HVR |
| Navigation Builder reuse | FR-M2O-13 | §9、§19、TD-003 | §11 Cross-CC map | CC-02 builder contract |

本 Draft 没有新增上游业务需求；它只收敛 Frozen TDD 已定义的 Tab 技术边界。

## 23. Open Questions

### Contract Review Questions

None. The target identity, optional target-only navigation decoration, source `active_id` boundary, Dialog behavior, and popup-blocking contract are closed in this Draft.

### Implementation Detail

1. `record_navigation.js` 与 `enhanced_many2one_field.js` 的具体 export/import signature。
2. 使用 `router.current`、`router.stateToUrl()` 还是等价的标准 URL helper。
3. Browser wrapper 的可测试注入方式。
4. 已证明适用于 target model 的 optional action anchor 测试 fixture。
5. Odoo 18 asset test bundle 中的测试文件组织。

### CONTRACT BLOCKER

当前无已确认的 CC-02 Contract Blocker。

如果实现验证证明：标准 Odoo URL 必须先异步 RPC 才能获得关键 action/view 信息，且同步 `_blank` 无法可靠保留用户点击链，则必须停止并提交证据，不得自行引入异步 popup workaround。

## 24. Boundary Confirmation

本 Draft 明确：

- no Extend；
- no Preview；
- no Preview State；
- no Preview Loader；
- no business record read；
- no business `sudo()`；
- no HTTP Controller；
- no official source changes；
- no `stock` dependency；
- no CC-03 / CC-04；
- no CC-01 production modification；
- no Commit；
- no Push。

## 25. Draft Self-Check

- [x] Status 更新为 v1.0.0 Frozen / Implementation Authorized
- [x] 重新读取 Frozen SRS/TDD/Implementation Plan、TVR、CC-01 和 CC-01 evidence
- [x] 重新读取正式模块代码和 Odoo 18 官方 Many2one/Router/Action/browser source
- [x] 明确 Tab Handler 与 Navigation Builder 职责
- [x] 明确同步用户点击链
- [x] 明确必要 context 与完整 Action Stack 边界
- [x] 明确 current page preservation
- [x] 明确 permission preservation
- [x] 明确 native fallback 和错误路径
- [x] 明确 allowed/forbidden files
- [x] 明确 JS/Browser/HVR/Acceptance/Stop contracts
- [x] 明确 CC-03 reuse boundary
- [x] 未修改 Frozen 上游文档、CC-01、Spike 或官方源码
- [x] 已按 Frozen CC-02 实施 Tab Handler + Navigation Builder
- [x] 已创建 ATR 和 Browser/HVR Checklist；新 Tab 的人工 HVR 仍待完成
- [x] 未创建 CC-03/CC-04
- [x] 未 Commit/Push

## 26. Version History

| 版本 | 日期 | 状态 | 说明 |
|---|---|---|---|
| v0.1.0 | 2026-09-18 | Draft / Not Authorized for Implementation | 基于 Frozen SRS、TDD、Implementation Plan、TVR、CC-01 evidence 和 Odoo 18 官方源码起草 CC-02 Tab Navigation Contract；未实施、未 Commit、未 Push |
| v0.1.1 | 2026-09-18 | Draft / Not Authorized for Implementation | 根据评审收口 target model/resId identity、target-only optional navigation state、source `active_id` 边界、Dialog native semantics、popup failure contract、Router URL 表述、适用的 Form 元素和测试类型；Contract Review Questions = none；未实施、未 Commit、未 Push |
| v1.0.0 | 2026-09-18 | Frozen / Implementation Authorized | 用户批准冻结并授权实施 Tab Handler + Navigation Builder；禁止进入 CC-03、实现 Extend/Preview、Commit 或 Push；完成自动化验证和 Browser/HVR 后停止 |
