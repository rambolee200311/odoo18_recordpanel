# CC-03 Extend Preview Core

> **Status: v1.0.0 FROZEN — IMPLEMENTATION AUTHORIZED**
>
> 本文档只起草 CC-03 Coding Contract。它不授权编码、Freeze、修改 CC-01/CC-02 production implementation、Commit、Push 或进入 CC-04。完成本 Draft 后停止，等待用户评审。

## 1. Contract Metadata

| 项目 | 内容 |
|---|---|
| Contract ID | CC-03 |
| Contract Name | Extend Preview Core |
| 版本 | v1.0.0 Frozen |
| 状态 | Frozen / Implementation Authorized |
| Odoo | 18.0 Community Edition |
| 正式模块 | `mymodules/wd_advanced_m2o_record_panel/` |
| 最小正式依赖 | `web` |
| 上游 SRS | v1.0.0 Frozen |
| 上游 TDD | v1.0.1 Frozen |
| 上游 Implementation Plan | v1.0.0 Frozen |
| 前置 Contract | CC-01 v1.0.0 Frozen / CC-02 v1.0.0 Frozen |
| CC-02 状态 | PASS / COMPLETE |
| 当前 branch | `main` |
| 当前 HEAD | `515d270 Implement CC-02 tab navigation` |
| `origin/main` | `515d270 Implement CC-02 tab navigation` |

## 2. Authorization

本轮授权：

- 将 CC-03 v0.1.1 Draft 冻结为 v1.0.0 Frozen；
- 实施 Extend Preview Core；
- 完成 Python/JS ATR 和精简的 6 项 Browser/HVR。

本轮仍不授权：

- 修改任何 production code；
- 修改 Frozen SRS、TDD、Implementation Plan、TVR、CC-01 或 CC-02；
- 实现 multiple Pane、editable Preview、cache、generic Split View、HTTP Controller、business `sudo()`、`stock` dependency 或官方源码修改；
- 创建 CC-04；
- Commit、Push 或删除文件。

流程必须保持：

```text
CC-03 Frozen
    ↓
Coding
    ↓
Automated Validation + Browser/HVR
    ↓
Python/JS ATR + 6-item Browser/HVR
    ↓
STOP before CC-04
```

## 3. Re-read Baseline

本 Draft 以以下内容为权威输入：

1. Frozen SRS v1.0.0；
2. Frozen TDD v1.0.1；
3. Frozen Implementation Plan v1.0.0；
4. Frozen CC-01 v1.0.0；
5. Frozen CC-02 v1.0.0；
6. CC-01 IHR/ATR/HVR；
7. CC-02 IHR/ATR/HVR；
8. Odoo 18 FormView、FormController、Many2one、Router 和 browser 官方源码。

CC-01 已建立配置模型、ACL 和 enhanced widget。CC-02 已建立可复用的 `buildRecordNavigation(targetModel, targetResId)`，并验证 `tab`、native fallback、标准 Record URL 和当前页保持。CC-03 不重新实现这些能力。

## 4. Goal

CC-03 唯一目标：

```text
advanced_many2one + open_mode="extend"
        ↓
Extend Handler
        ↓
page-scoped Preview State
        ↓
FormView sibling Preview Host
        ↓
required Server-side Preview Loader
        ↓
safe authorized DTO
        ↓
readonly Preview Renderer
```

当显式配置的 enhanced Many2one 字段以 `extend` 模式触发时：

- 当前 Form 页面显示一个持续同屏的只读 Preview Pane；
- Pane 是当前 FormView 的 sibling，不是 modal、drawer、tooltip、overlay 或 iframe；
- 后触发的 source 原子替换先前 source；
- Preview 只读取，不写回 Many2one 或业务记录；
- 用户仍可通过 CC-02 Navigation Builder 打开完整目标记录；
- 缺失配置、无权、空字段、错误和 stale response 均安全处理。

## 5. In Scope

1. `extend` dispatch 和 Extend Handler。
2. page-scoped、单一 Preview Pane 状态。
3. FormView template extension + thin FormController integration。
4. required logical Server-side Preview Loader。
5. 安全 DTO 和错误分类。
6. 只读 Preview Renderer 和官方格式化边界。
7. source identity、page token、request token 和生命周期清理。
8. source 替换、update、clear、close 和 unmount。
9. desktop horizontal sibling 与 small-screen vertical stacked。
10. “打开完整记录”入口复用 CC-02 Navigation Builder。
11. Extend/native/Tab regression。
12. Python、JS、Browser 和 HVR 相关验证证据。

## 6. Out of Scope

禁止实现：

- CC-04 攻击性竞态矩阵和升级 hardening；
- multiple Pane、Profile、editable Preview、generic Split View；
- Preview cache、跨页面 cache、同 target 去重；
- Preview 中的 save/create/delete/edit Field Widget；
- HTTP Controller；
- 业务记录 `sudo()`；
- 修改官方 Odoo source；
- `stock` dependency；
- 改写完整 Many2one 或默认 `many2one` registry；
- 修改 Frozen SRS/TDD/Implementation Plan/CC-01/CC-02 以绕过问题；
- 直接操作数据库或裸 SQL。

## 7. Upstream Dispatch Contract

```text
native / missing / invalid
    → inherited native behavior

tab
    → CC-02 Tab Handler

extend
    → CC-03 Extend Handler
```

只有 XML field node options 可以决定 `open_mode`。普通 `many2one` 和没有显式 enhanced widget 的字段必须保持原生。

Extend 不接管选择、搜索、autocomplete、create、create-and-edit、clear、display、readonly、required、disabled 或 no-create 行为。

## 8. Preview Host Contract

正式 host 采用 TDD 冻结的：

```text
FormView template extension
        +
thin FormController integration
        +
page-scoped state
```

必须满足：

- 每个 Form/Action page 最多一个 Preview Pane；
- Pane 作为 FormView 外层 sibling；
- 主 Form、Notebook、Chatter、scroll 和业务按钮继续可用；
- desktop 为 horizontal sibling；
- small screen 使用 vertical stacked，不覆盖主业务区域；
- host 不复制 FormController、FormRenderer、Chatter 或 Notebook；
- controller 只负责 page token、state/dispatch 注入和 unmount cleanup；
- 官方模板结构不兼容时，安全不显示 Pane，但主 Form 仍可用。

## 9. Source Identity and State Contract

Source identity 必须是：

```text
PageScopeIdentity
+ RecordIdentity
+ FieldIdentity
[+ FieldInstanceIdentity]
```

target model/resId 不是 source identity。两个不同 source field 即使指向同一 target，也必须隔离。

状态至少表达：

```text
closed
loading
ready
fallback
access_denied
error
```

推荐的逻辑状态内容：

- current source identity；
- target model/resId；
- loading/authorized/error status；
- authorized DTO；
- current page token；
- current request token。

具体 JS store/API 字段名由实现决定，但不得削弱上述语义。

状态转换必须满足：

```text
closed --activate--> loading
loading --authorized--> ready
loading --no config/empty/unsupported--> fallback
loading --record denied--> access_denied
loading --RPC error--> error
ready --same source update--> loading
ready --new source--> loading (atomic replace)
ready --current clear/close--> closed
any --unmount--> closed + invalidate request
```

CC-03 必须实现基础 stale protection：

- 每次 activation/update/clear/close 分配或失效 request token；
- response 提交前校验 page token、request token、source identity、target identity 和 mounted 状态；
- 旧 source response 不得污染新 source；
- clear/close/unmount 立即失效旧请求，不等待 RPC。

CC-04 负责 rapid A→B→A、权限改变、删除中请求等组合攻击矩阵；CC-03 不能因此省略基础 token 架构。

## 10. Server-side Preview Loader Contract

Server-side Preview Loader 是 CC-03 的 **REQUIRED logical responsibility**。是否独立为 `preview_loader.py` 属于实现选择，但不得以“如实现需要”省略。

Loader 必须：

1. 通过当前用户环境读取唯一 Preview Configuration metadata；
2. 解析 target model、active、configured fields 和 sequence；
3. 先验证目标业务记录的模型访问、记录规则和 read 权限；
4. 在读取 `display_name` 或其他身份数据前拒绝不可访问记录；
5. 逐字段遵守 field access/readability；
6. 对可读字段部分成功，对不可读字段省略；
7. 对无配置、停用、空字段、非法字段、删除记录、无权、错误返回安全分类；
8. 返回 JSON-safe、无 HTML、无 traceback、无 SQL、无内部异常文本的 DTO；
9. 不修改任何业务记录；
10. 不使用业务 `sudo()`；
11. 不建立 Preview data cache 或同 target 去重。

DTO 至少需要表达：

```text
status
authorized target identity when authorized
safe header/fallback information when authorized
ordered authorized rows
safe error/fallback code
```

状态相关 DTO 必须满足：

```text
ready / authorized fallback:
    status
    authorized target identity
    safe header
    authorized rows
    safe code/message

access_denied:
    status
    safe code/message only
```

`access_denied` DTO **不得**包含 `targetModel`、`targetResId`、display name、model name、record name、id 或任何业务字段/value。Renderer 也不得从 source Many2one value、source record 或其他前端状态补回 denied identity。配置 read 不等于业务记录或字段 read。

只有已确认 target record 当前用户可访问后，fallback 才能包含 safe basic identity、解释性 message 和 “Open Full Record”。`access_denied` 不提供 “Open Full Record”。

## 11. Renderer and Formatting Contract

Renderer 只消费 Loader 返回的已授权 DTO：

- 只读 label/value 语义 HTML；
- 不创建编辑 Field Widget；
- 不提供 save/create/delete；
- 不写回 source record 或 Many2one；
- 支持部分字段、空字段、fallback、access denied 和 error；
- 复用 Odoo 官方 field utilities / formatter；
- relational 字段不得扩展为递归 Preview；
- HTML、任意模板片段和未经安全处理的用户文本不得直接注入；
- `ready` 和已授权 `fallback` 可显示 “Open Full Record”，只复用 CC-02 Navigation Builder；
- `access_denied` 不显示、不调用 “Open Full Record”，也不得从 source Many2one 补回目标身份。

CC-03 不冻结未经验证的具体 formatter API signature；实现必须以 Odoo 18 官方源码和测试为准。

## 12. Configuration and Permission Boundary

CC-03 使用 CC-01 已实现的配置模型和权限：

- 普通内部用户可 read configuration metadata；
- 配置管理员可 create/write/unlink；
- 普通用户不可通过配置 read 获得业务数据；
- 配置停用或修改不得删除业务记录；
- 下一次 activation/reload 必须读取当前配置，不使用跨页面旧配置。

Loader 的配置 metadata 读取和业务 record/field 读取必须保持分离。

## 13. Error and Fallback Contract

| 情况 | 行为 |
|---|---|
| missing/invalid mode | native behavior |
| target authorized + no configuration | authorized `fallback`，包含 safe basic identity、解释性 message 和 “Open Full Record” |
| target authorized + inactive configuration | authorized `fallback` |
| target authorized + no usable configured fields | authorized `fallback` |
| target authorized + some valid/readable fields | `ready`，只显示 permitted rows |
| target authorized + some field denied | `ready`，省略 denied fields，其余继续 |
| target authorized + all fields denied | authorized `fallback`，不误判为 record access denied |
| target record denied | `access_denied`，不泄露身份 |
| record deleted | safe error/fallback |
| RPC/network error | safe error，不显示 traceback |
| stale response | 丢弃，不更新 Pane |
| clear/close | 立即 closed 并失效请求 |
| unmount | 清理 Pane、state、DOM 引用并失效请求 |

对于 target 尚未确认可访问的请求，客户端不得收到任何依赖 target identity 或 configuration 状态的可观察业务信息。Loader 内部可以按效率选择配置解析与 access check 的调用顺序，但外部 response classification 必须遵守该 information-disclosure boundary。

无配置、停用或无有效字段时，在 target 已确认可访问的前提下进入 authorized `fallback`，不得创建一个看似正常但内容为空的 ready Pane。

## 14. Reuse of CC-02

CC-03 只复用：

```text
navigation.build(targetModel, targetResId, safeTargetNavigationState)
```

CC-03 不修改 CC-02 Builder 的 target identity、同步 `_blank`、Dialog native 或 source context 边界。

## 15. Allowed Files

拟授权区域仅限：

```text
mymodules/wd_advanced_m2o_record_panel/
├── models/
│   └── preview_loader.py        # 或等价 server-side logical component
├── static/src/fields/
│   └── enhanced_many2one_field.js
├── static/src/preview/
│   ├── preview_state.js
│   ├── preview_host.js
│   ├── preview_renderer.js
│   └── preview_formatting.js
├── static/src/navigation/
│   └── record_navigation.js     # 仅在 reuse boundary 内必要修改
├── static/tests/
├── tests/
└── __manifest__.py              # 仅在必要 asset 更新范围内
```

职责必须存在，但不机械冻结文件数量。新增 production directory、dependency、model 或 security surface 必须在 Freeze 前明确。

## 16. Test Contract

### Python

至少覆盖：

- loader configuration resolution；
- authorized record DTO；
- record read denial without identity leakage；
- field denial with partial success；
- no configuration/inactive/empty fields；
- invalid/deleted target；
- ordered sequence；
- no business sudo；
- no business write；
- current-user permission chain。

### JavaScript

至少覆盖：

- extend dispatch；
- single Pane；
- source identity isolation；
- A→B atomic replacement；
- same-source update；
- current-source clear/close；
- non-current source ignored；
- request/page/source/target stale discard；
- unmount cleanup；
- readonly renderer no write；
- missing/invalid/denied/error/fallback states；
- CC-02 navigation reuse；
- native and tab regression。

### Browser/HVR

HVR 只覆盖指定的人工用户体验场景，不重复 Python/JS contract coverage：

1. 点击 `extend` 后出现持续同屏的右侧 Preview Pane；主 Form 与 Pane 同时可见，且不是 modal/drawer/overlay。
2. Preview 显示正确目标记录的已配置字段，并且为只读。
3. source 切换后 Pane 正确更新；clear/close 后界面行为正确。
4. 无权 target 只显示安全提示，不显示 identity 或业务数据。
5. “Open Full Record” 复用 CC-02，在新 Tab 打开正确完整记录。
6. 窄屏变为 vertical stacked，主 Form 仍可正常使用。

字段省略、删除记录、网络错误、两个 source 指向同一 target、配置变化、stale response、unmount cleanup 等主要由 Python/JS ATR 覆盖，不要求人工重复操作。

## 17. Acceptance Gate

CC-03 Complete 至少要求：

1. `extend` dispatch installed only for explicit enhanced fields；
2. FormView sibling host and single Pane；
3. required Server-side Preview Loader；
4. current-user permission chain with no business sudo；
5. safe DTO and renderer；
6. source identity and page/request token lifecycle；
7. stale response basic protection；
8. update/clear/close/unmount；
9. desktop and narrow layout；
10. CC-02 full-record navigation reuse；
11. native/tab regression；
12. Python/JS evidence PASS；
13. Browser/HVR evidence PASS（仅限指定人工场景，不重复 Python/JS coverage）；
14. no official-source modification；
15. no HTTP Controller or stock dependency；
16. no CC-04-only attack matrix claimed as complete；
17. no Commit/Push until separately authorized。

## 18. Stop Conditions

| ID | Stop condition |
|---|---|
| STOP-01 | Must modify Odoo official source |
| STOP-02 | Must copy/rewrite complete Many2one |
| STOP-03 | Must use business `sudo()` or custom business read path outside Loader contract |
| STOP-04 | Must add HTTP Controller or unrelated dependency |
| STOP-05 | Cannot maintain single page-scoped Pane |
| STOP-06 | Cannot establish FormView/Controller lifecycle cleanup |
| STOP-07 | Cannot safely discard stale responses |
| STOP-08 | Loader would leak denied record identity |
| STOP-09 | Renderer would create editable/write-capable controls |
| STOP-10 | Must modify Frozen SRS/TDD/Implementation Plan/CC-01/CC-02 |
| STOP-11 | Official FormView structure makes safe sibling host impossible |
| STOP-12 | Narrow layout would overlay or hide the main Form |
| STOP-13 | Requires cache, recursive Preview or multiple Pane to pass |
| STOP-14 | Requires entering CC-04 to make the CC-03 happy path safe |

## 19. Open Questions

### Contract Review Questions

1. None intentionally left unresolved at this Draft stage for the security, identity, lifecycle and scope boundaries above.

### Implementation Detail

- exact Loader method name and Python file;
- exact DTO key names and error code constants;
- exact FormView selector/template extension point;
- sub-environment versus service/host prop wiring;
- formatter helper imports and supported field type matrix;
- CSS class names and responsive breakpoint implementation;
- Hoot fixture and test asset organization.

### CONTRACT BLOCKER

If Odoo 18 does not provide a stable, safe FormView sibling extension point without modifying official source or breaking the main Form, stop and submit evidence. Do not fall back to a global overlay or field-owned Pane.

## 20. Boundary Confirmation

This Draft does not:

- implement Extend or Preview；
- modify CC-01/CC-02 production code；
- modify Frozen upstream documents；
- create CC-04；
- modify Spike；
- Commit or Push。

## 21. Freeze and Implementation Self-Check

- [x] Status updated to v1.0.0 Frozen / Implementation Authorized
- [x] CC-01 and CC-02 boundaries preserved
- [x] Server-side Preview Loader marked required logical responsibility
- [x] Basic stale protection assigned to CC-03
- [x] CC-04 attack matrix boundary explicit
- [x] Permission, DTO and no-business-sudo boundary explicit
- [x] Form host, page state, renderer and responsive boundary explicit
- [x] Python/JS/Browser/HVR contracts defined
- [x] Stop conditions defined
- [x] Implementation scope limited to Extend Preview Core
- [x] No CC-04 implementation authorized
- [x] No Commit/Push performed

## 22. Version History

| 版本 | 日期 | 状态 | 说明 |
|---|---|---|---|
| v0.1.0 | 2026-09-18 | Draft / Not Authorized for Freeze or Implementation | 基于 Frozen SRS、TDD、Implementation Plan、CC-01、CC-02 和 Odoo 18 官方源码起草 CC-03 Extend Preview Core；仅起草，未实施、未 Freeze、未 Commit、未 Push |
| v0.1.1 | 2026-09-18 | Draft / Not Authorized for Freeze or Implementation | 根据评审收口 authorized fallback、access_denied DTO、Full Record 权限、information-disclosure ordering、all-fields-denied 分类、HVR 六项范围、HVR 与 Python/JS coverage 边界，并将 CC-02 metadata 改为 PASS / COMPLETE；未实施、未 Freeze、未 Commit、未 Push |
| v1.0.0 | 2026-09-18 | Frozen / Implementation Authorized | 用户批准冻结并授权实施 Extend Preview Core；完成 Python/JS ATR 和 6 项 Browser/HVR 后停止，不进入 CC-04 |
