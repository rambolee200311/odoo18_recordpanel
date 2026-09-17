# Many2one 关联记录展现增强 — 基础需求分析

> **文档状态**：讨论稿
> **文档性质**：基础需求分析
> **阶段目标**：确认业务需求、产品边界和 MVP 范围，不涉及 DDD、TDD 或具体前端实现方案

---

# 1. 背景

Odoo 标准 Many2one 已经提供成熟的记录选择和关联记录打开能力。

对于普通业务场景，官方行为已经足够，因此本需求**不替代、不包装、不修改 Odoo 原生 Many2one 默认行为**。

实际业务中主要存在两类关联记录查看效率问题：

1. 查看完整关联记录时，希望保留当前业务页面；
2. 对账、审核、匹配等场景，需要持续同时查看当前记录与关联记录。

例如承运商账单对账时，当前账单行可能包含：

* Pickup Code；
* Invoice Amount；
* Currency；
* Description。

关联 Transport Order 则可能需要核对：

* Order No.；
* Pickup Code；
* Carrier；
* Planned Cost；
* Additional Cost；
* Currency；
* Settlement Status。

用户实际工作过程是：

```text
查看当前业务数据
      ↓
查看关联记录
      ↓
比较两边信息
      ↓
作出业务判断
      ↓
继续处理当前记录
```

如果关联记录只能通过页面跳转、Popup 或临时 Tooltip 查看，会产生频繁的上下文切换。

因此需要在保留 Odoo 原生 Many2one 的基础上，为特定字段增加关联记录查看增强能力。

---

# 2. 需求目标

为需要增强关联记录查看体验的 Many2one 字段提供一个通用增强 Widget。

MVP 提供两种模式：

| 模式       | 行为                 | 主要场景        |
| -------- | ------------------ | ----------- |
| `tab`    | 新浏览器标签页打开完整关联记录    | 深入查看或操作     |
| `extend` | 当前页面右侧持续显示关联记录关键字段 | 对账、审核、匹配、核对 |

基本关系：

```text
Many2one
│
├── 未使用增强 Widget
│      └── Odoo 官方默认行为
│
└── 使用增强 Widget
       │
       ├── tab
       │     └── 新标签打开完整记录
       │
       └── extend
             └── 右侧只读关键字段预览
```

---

# 3. 产品定位

本需求解决：

> **Many2one 记录选定以后，如何更高效地查看关联记录。**

本需求不解决：

* Many2one 数据关系；
* Many2one 基础选择；
* Many2one 搜索；
* Many2one 候选记录筛选；
* 关联模型业务逻辑；
* 关联记录权限管理；
* Odoo 官方 Many2one 默认行为。

增强 Widget 职责限定为：

> **增强关联记录查看方式。**

---

# 4. 统一触发原则

增强 Widget 不增加新的业务操作入口。

用户仍通过 Many2one 原有的：

> **打开关联记录入口**

触发查看行为。

增强 Widget 根据配置改变该入口的后续展现方式：

```text
打开关联记录
      │
      ├── tab
      │     └── 新标签页打开完整记录
      │
      └── extend
            └── 右侧打开 Preview Pane
```

Many2one 的记录选择、清空和其他标准操作保持原有用户心智。

---

# 5. Tab 模式

## 5.1 目的

Tab 用于：

> 用户需要查看或操作完整关联记录，但不希望当前业务页面被替换。

## 5.2 行为

Many2one 使用 `tab` 模式时：

1. 用户正常选择 Many2one 记录；
2. 用户触发原有“打开关联记录”入口；
3. 系统在新的浏览器标签页打开该关联记录；
4. 当前业务页面保持不变；
5. 新标签页进入正常 Odoo 记录页面。

## 5.3 完整页面要求

新标签页不得仅提供孤立的记录内容。

应进入正常 Odoo 业务页面，并保持该记录在正常 Odoo 页面中应具有的导航能力，包括适用情况下的：

* 菜单上下文；
* 页面导航；
* 面包屑；
* 标准 Form；
* 标准业务按钮。

用户能够执行哪些操作仍由 Odoo 原有权限及业务规则决定。

## 5.4 Tab 边界

Tab 只改变：

> **关联记录打开的位置。**

不改变：

* Many2one 字段值；
* 记录选择行为；
* 关联记录 Form View；
* 关联记录业务逻辑；
* Odoo 权限。

---

# 6. Extend 模式

## 6.1 目的

Extend 用于：

> **需要持续同时查看当前业务记录和关联记录关键数据的场景。**

典型场景：

* 对账；
* 账单匹配；
* 审核；
* 数据核对；
* 来源单据核对；
* 关联主数据快速查看。

---

# 7. Extend 核心交互

用户触发 Many2one 原有“打开关联记录”入口后：

* 当前业务页面不跳转；
* 页面右侧出现 Preview Pane；
* 当前业务内容继续保留；
* Preview Pane 展示关联记录关键字段；
* 左右区域持续同时可见。

示意：

```text
┌──────────────────────────────┬────────────────────────────┐
│ 当前业务页面                   │ Related Record Preview     │
│                              │                            │
│ Carrier Invoice Line         │ Transport Order            │
│                              │                            │
│ Pickup: ABC123               │ Order: TO-001              │
│ Amount: €850                 │ Pickup: ABC123             │
│ Currency: EUR                │ Carrier: ABC Logistics     │
│                              │ Planned Cost: €800         │
│ Order: TO-001                │ Additional Cost: €50       │
│                              │ Currency: EUR              │
│                              │ Status: Confirmed          │
│                              │                            │
│                              │ [打开完整记录]               │
└──────────────────────────────┴────────────────────────────┘
```

---

# 8. Extend 布局原则

Extend 必须满足：

> **左右持续同屏，而不是右侧内容覆盖左侧内容。**

Preview Pane 打开后：

* 当前业务区域仍然可见；
* 当前业务区域可以因 Preview 打开而缩小；
* Preview 不得覆盖主要业务内容形成伪同屏；
* 用户能够在 Preview 打开状态下继续查看和操作当前业务页面。

MVP 不强制规定：

* Preview Pane 的具体像素宽度；
* 是否支持用户拖拽调整宽度。

这些属于后续交互和技术设计内容。

对于屏幕宽度不足以合理维持左右同屏的情况，应提供明确降级行为；具体阈值和降级方式在后续 SRS/UI 设计中确定。

---

# 9. Extend 与 Popup / Drawer 的区别

Extend 的核心要求是：

> **关联记录关键数据与当前业务页面持续同时可见。**

因此以下方式不能作为 Extend 的等价实现：

### Tooltip / Hover Popup

信息仅临时存在，不适合持续比较。

### Modal Popup

遮挡当前业务页面。

### 覆盖式 Drawer / Offcanvas

即使从右侧打开，如果覆盖当前主要业务区域，仍不能满足持续同屏要求。

因此 Extend 的定义不是：

> “从右侧打开关联记录”。

而是：

> **形成当前业务区域 + 关联记录 Preview 的持续同屏工作状态。**

---

# 10. 单 Preview Pane 原则

同一业务页面同时只存在一个 Preview Pane。

如果页面存在多个使用 `extend` 的 Many2one 字段：

```text
Customer          → extend
Transport Order   → extend
Carrier           → extend
```

用户首先打开 Transport Order：

```text
Preview = Transport Order
```

随后打开 Carrier：

```text
Preview = Carrier
```

新的 Preview **替换**原 Preview。

MVP 不支持：

> 多个 Preview Pane 同时并列显示。

---

# 11. Extend 只读原则

Extend MVP 定位为：

> **Readonly Related Record Preview**

而不是完整 Odoo Form。

Preview Pane 仅负责查看数据。

用户不能直接在 Preview 中：

* 修改关联记录；
* 保存关联记录；
* 创建关联记录；
* 删除关联记录；
* 执行复杂业务按钮。

需要进一步处理关联记录时，通过：

> **打开完整记录**

进入标准 Odoo 页面。

---

# 12. Model Preview Configuration

不同关联模型需要展示的关键字段不同。

因此 Widget 不硬编码业务字段。

系统提供：

> **Model Preview Configuration（模型预览配置）**

由管理员定义某个模型在 Extend 中展示哪些字段。

例如：

### `res.partner`

可能展示：

* Name；
* VAT；
* Phone；
* Email；
* Country。

### `transport.order`

可能展示：

* Order No.；
* Pickup Code；
* Carrier；
* Origin；
* Destination；
* Planned Cost；
* Additional Cost；
* Currency；
* Status。

---

# 13. MVP 配置模型

MVP 采用：

> **一个 Model 对应一套 Preview Configuration。**

基本结构：

```text
Model Preview Configuration
│
├── Model
├── Active
│
└── Preview Fields
       ├── Field
       ├── Sequence
       ├── Field
       ├── Sequence
       └── ...
```

不设计：

* 多 Profile；
* Default Profile；
* 场景 Profile；
* Profile 选择优先级。

---

# 14. Preview Configuration 基础内容

至少包含：

| 配置项            | 说明           |
| -------------- | ------------ |
| Model          | 目标 Odoo 模型   |
| Active         | 是否启用 Preview |
| Preview Fields | 需要展示的字段      |
| Sequence       | 字段展示顺序       |

例如：

### Transport Order Preview

| 顺序 | 字段              |
| -: | --------------- |
| 10 | Order No.       |
| 20 | Pickup Code     |
| 30 | Carrier         |
| 40 | Origin          |
| 50 | Destination     |
| 60 | Planned Cost    |
| 70 | Additional Cost |
| 80 | Currency        |
| 90 | Status          |

---

# 15. Preview 字段展示规则

MVP 对 Preview 字段采用统一展示原则。

## 15.1 字段名称

展示字段的人类可读 Label，不展示技术字段名。

## 15.2 Many2one

展示关联记录的显示名称，不展示数据库 ID。

## 15.3 Selection

展示 Selection 的业务 Label，不展示技术 Value。

## 15.4 Boolean

以明确的人类可读状态展示，不直接暴露技术值。

## 15.5 Date / Datetime

按照当前用户正常 Odoo 日期和时间显示规则展示。

## 15.6 Monetary

按照正常 Odoo 金额及币种规则展示。

## 15.7 空值

空值使用统一的空值表现，不制造虚假业务值。

具体视觉形式可在 UI 设计阶段确定。

## 15.8 长文本

长内容不得破坏 Preview 布局。

允许采用换行、截断等适合 Preview 的展示方式；具体视觉规则在 UI 设计阶段确定。

核心要求为：

> 字段展示应保持业务可读性，不直接暴露 Odoo 技术存储值。

---

# 16. Preview 配置权限

MVP 中 Preview Configuration 由具有配置权限的管理员统一维护。

管理员可以：

* 为模型建立 Preview Configuration；
* 增加字段；
* 删除字段；
* 调整字段顺序；
* 启用或停用配置。

普通业务用户：

* 使用 Extend；
* 查看配置结果；
* 不修改 Preview Configuration。

MVP 不提供用户个人 Preview 配置。

---

# 17. 无权限字段处理

Preview Configuration 是展示配置，不是权限配置。

如果管理员配置的某个字段当前用户无权读取：

> **该字段不在 Preview 中渲染。**

系统不得：

* 因此扩大用户权限；
* 显示受限字段值；
* 以报错方式导致整个 Preview 不可使用。

其他用户有权查看的字段应继续正常展示。

---

# 18. 无 Preview Configuration 时的行为

目标模型不存在有效 Preview Configuration 时，Extend 不得异常。

系统应提供基础降级展示，至少识别当前关联记录，例如：

```text
Transport Order

TO-001

当前模型尚未配置详细预览字段。

[打开完整记录]
```

核心原则：

> **配置缺失不得导致 Extend 报错或页面不可用。**

---

# 19. 关联记录切换

如果当前 Many2one 值发生变化，已打开 Preview 必须同步更新。

例如：

```text
Transport Order = TO-001
        ↓
Preview = TO-001

重新选择 TO-002
        ↓
Preview = TO-002
```

不得继续显示旧记录。

如果当前 Many2one 被清空，对应 Preview 内容应清除。

---

# 20. Preview Pane 关闭

用户可以主动关闭 Preview Pane。

关闭操作：

* 不修改 Many2one；
* 不修改当前业务记录；
* 不修改关联记录；
* 不影响当前业务页面继续操作。

---

# 21. 打开完整记录

Extend Preview 提供：

> **打开完整记录**

入口。

当 Preview 信息不足时，用户可以进入正常 Odoo 记录页面继续查看或处理。

完整页面使用：

* 正常 Odoo 页面；
* 正常 Form View；
* 正常业务按钮；
* 正常权限体系。

---

# 22. 典型场景：承运商账单对账

当前 Carrier Invoice Line：

```text
Pickup Code     ABC123
Invoice Amount  €850
Currency        EUR
Transport Order TO-001
```

用户通过 Transport Order Many2one 的打开记录入口触发 Extend。

右侧持续显示：

```text
Transport Order
────────────────────────
Order No.          TO-001
Pickup Code        ABC123
Carrier            ABC Logistics
Planned Cost       €800
Additional Cost    €50
Currency           EUR
Status             Confirmed

[打开完整记录]
```

用户可以在不离开当前账单的情况下持续比较：

```text
Invoice             Transport Order
€850        ↔        €800 + €50
```

完成判断后继续处理当前业务记录。

---

# 23. MVP In Scope

MVP 包含：

* Many2one 增强 Widget；
* `tab`；
* `extend`；
* 沿用 Many2one 原有打开关联记录入口；
* Tab 新标签打开标准完整记录；
* Extend 右侧 Preview Pane；
* 左右持续同屏；
* 左侧业务区域不被 Preview 覆盖；
* 单 Preview Pane；
* 后触发 Preview 替换前一个 Preview；
* Extend 只读；
* Model Preview Configuration；
* 一个模型一套配置；
* Preview 字段配置；
* Preview 字段排序；
* 基础字段类型的人类可读展示；
* 无权限字段不渲染；
* 无配置时基础降级；
* Many2one 值变化后 Preview 更新；
* Many2one 清空后 Preview 清除；
* Preview 主动关闭；
* 从 Preview 打开完整记录；
* 遵循 Odoo 原有权限。

---

# 24. MVP Out of Scope

MVP 不包含：

* Odoo 官方 Many2one 行为重写；
* `official` 模式；
* Many2one 高级选择器；
* 多 Preview Profile；
* 场景级 Profile；
* Default Profile；
* 用户个人 Preview 配置；
* Preview 内编辑；
* Preview 内保存；
* Preview 内创建或删除记录；
* 完整 Form View 嵌入；
* 双 Form 编辑；
* 双 Form Save / Discard；
* Tooltip Preview；
* Hover Preview；
* Modal Preview；
* 覆盖式 Drawer；
* Preview 页面设计器；
* 多 Preview Pane 同时显示；
* 通用 Split View 框架；
* 强制要求 Preview Pane 可拖拽调整宽度。

---

# 25. 初步验收标准

### AC-01 原生 Many2one 不受影响

未使用增强 Widget 的 Many2one 保持 Odoo 官方行为。

### AC-02 统一触发入口

Tab 和 Extend 均沿用 Many2one 原有打开关联记录入口，不额外增加重复的查看按钮。

### AC-03 Tab 打开

Tab 模式下，关联记录在新浏览器标签页打开。

### AC-04 当前页面保留

Tab 打开后，当前业务页面保持不变。

### AC-05 标准记录页面

Tab 打开的关联记录应进入正常 Odoo 页面，并具备正常业务导航能力。

### AC-06 Extend 打开

Extend 模式下，通过关联记录打开入口在当前页面右侧显示 Preview Pane。

### AC-07 持续同屏

Preview 打开后，当前业务区域与关联记录 Preview 持续同时可见。

### AC-08 不覆盖当前业务区域

Preview 不得通过 Modal、Popup 或覆盖式 Drawer 遮挡当前主要业务内容。

### AC-09 Extend 只读

用户不得通过 Preview 修改关联记录。

### AC-10 模型配置

管理员能够针对模型建立 Preview Configuration。

### AC-11 字段配置

管理员能够选择 Preview 字段并设置展示顺序。

### AC-12 单模型单配置

MVP 中同一模型只存在一套有效 Preview Configuration。

### AC-13 字段可读性

Many2one、Selection、Boolean、Date/Datetime、Monetary 等基础字段应以用户可理解的业务形式展示，而不是技术存储值。

### AC-14 配置缺失降级

目标模型没有有效 Preview Configuration 时不得报错，应提供基础关联记录信息和完整记录入口。

### AC-15 记录同步

Many2one 值发生变化后，当前 Preview 应同步显示新关联记录。

### AC-16 清空同步

Many2one 被清空后，对应 Preview 内容应清除。

### AC-17 单 Pane

同一页面多次触发 Extend 时只保留一个 Preview Pane，后触发记录替换当前 Preview。

### AC-18 权限字段降级

Preview Configuration 中存在当前用户无权读取的字段时，该字段不显示，不得导致整个 Preview 报错。

### AC-19 Preview 关闭

用户能够关闭 Preview，且不得因此修改任何业务数据。

### AC-20 打开完整记录

用户能够从 Preview 进入关联记录完整 Odoo 页面。

### AC-21 权限不扩大

Tab 和 Extend 均不得扩大用户原有模型、记录或字段访问权限。

---

# 26. 后续扩展触发条件

## 26.1 多 Preview Profile

MVP 不实现多 Profile。

只有出现以下实际业务情况时，再评估引入：

> **同一个关联模型已经存在两个或以上实际业务场景，并且这些场景需要展示明显不同的字段集合，使用一套公共 Preview 字段已经造成明显的信息冗余或无法满足操作需要。**

例如未来实际验证：

```text
Transport Order

结算：
Pickup Code
Planned Cost
Additional Cost
Settlement Status

派车：
Route
Driver
Vehicle
Appointment Time
```

如果两套字段差异已经明显影响使用体验，再引入：

```text
Model
  └── Multiple Preview Profiles
```

在此之前保持：

> **一个模型一套 Preview Configuration。**

---

# 27. 需求结论

本需求不开发新的 Many2one 基础能力，也不开发完整 Split View 框架。

产品边界收敛为：

```text
Odoo 原生 Many2one
│
├── 默认
│     └── 完全保持官方行为
│
└── Enhanced Many2one Widget
      │
      ├── tab
      │     └── 新标签打开完整关联记录
      │
      └── extend
            │
            ├── 沿用原打开记录入口
            ├── 当前页面右侧持续同屏
            ├── 单 Preview Pane
            ├── 只读关联记录预览
            │
            └── Model Preview Configuration
                  └── Fields + Sequence
```

**Tab** 解决：

> 我要进入完整关联记录，但不想丢失当前工作页面。

**Extend** 解决：

> 我要继续处理当前记录，同时持续核对关联记录。

**Model Preview Configuration** 解决：

> 不同模型需要查看哪些关键字段，不应硬编码在 Widget 中。

MVP 坚持“一个模型一套配置 + 单 Pane + 只读 Preview + 持续同屏”，只有真实业务使用证明存在不足后，再引入多 Profile、用户个性化或更复杂的 Preview 布局。
