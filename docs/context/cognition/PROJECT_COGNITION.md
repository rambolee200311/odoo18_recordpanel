# 项目认知

## 项目基本信息

- 项目类型：Odoo 源码及定制开发工作区
- Odoo 版本：18.0
- 版本类型：Community Edition（社区版）
- 官方代码目录：`odoo/` 和官方 `addons/`
- Agent 操作原则：见 [`AGENT_OPERATION_PRINCIPLES.md`](../principle/AGENT_OPERATION_PRINCIPLES.md)

## GitHub 仓库信息

- GitHub 仓库：[rambolee200311/odoo18_recordpanel](https://github.com/rambolee200311/odoo18_recordpanel)
- SSH 远程地址：`git@github.com:rambolee200311/odoo18_recordpanel.git`
- 远程名称：`origin`
- Fetch 地址：`git@github.com:rambolee200311/odoo18_recordpanel.git`
- Push 地址：`git@github.com:rambolee200311/odoo18_recordpanel.git`
- 主分支：`main`
- 远程默认分支：`origin/main`
- 已确认的远程分支：`main`
- 当前基线提交：`7357e4b8069f49fb2976f5b18d7dbf89a7a23794`
- 当前基线提交说明：`first commit`

## 仓库工作约定

- 当前工作区以 `origin/main` 作为远程基线。
- 修改前应确认当前分支和工作区状态。
- 不应擅自修改 Odoo 官方代码；应通过自定义模块、继承机制或标准扩展点实现需求。
- 不允许直接读写数据库；需要数据操作时使用目标 Odoo 版本的 `odoo-bin shell` 和 ORM。
- 删除任何文件前必须取得用户明确许可。

## 模块目录约定

- 本项目后续新增或修改的定制模块统一放在 `mymodules/` 下。
- Many2one 关联记录查看增强模块目录固定为 `mymodules/wd_advanced_m2o_record_panel/`。
- 该目录用于存放模块代码、模块清单、视图、数据、测试和静态资源。
- Odoo 官方核心代码和官方模块仍位于原官方目录，不得移动或修改。

## 迭代开发文档约定

- 每一轮开发开始前，必须编写对应的 Coding Contract。
- Coding Contract 文件统一放在 `docs/context/intent/`。
- 每一轮契约的实施过程都必须留有记录。
- 实施记录统一放在 `docs/context/history/`。
- 多轮开发完成后，按照用户要求编写阶段性或项目报告。
- 报告统一放在 `docs/context/report/`。
- Coding Contract、实施记录和报告必须保持可追溯关系，能够对应到具体轮次、需求、变更和验证结果。

### 轮次契约与审批规则

- 每轮契约使用 `CC-xx-description.md` 命名。
- `xx` 按项目全局递增且唯一，例如 `CC-01-客户档案.md`、`CC-02-权限调整.md`。
- 我只能先创建和维护 Draft 契约。
- Draft 契约必须放在 `docs/context/intent/`。
- 未经用户明确允许，我不得冻结契约，也不得开始实施。
- 用户明确允许后，在同一契约文件中将状态标记为 Frozen，然后才能开始实施。
- 契约冻结后不得静默修改范围、验收标准或技术方案。
- 如确需变化，必须暂停实施、记录变化原因，并重新请求用户批准解冻或创建下一轮契约。

### 单轮记录命名规则

单轮记录统一放在 `docs/context/history/`，并沿用对应的 CC 编号：

- `IHR-CC-xx-description.md`：实施历史记录；
- `ATR-CC-xx-description.md`：自动化测试记录；
- `HVR-CC-xx-description.md`：人工验证记录（如需要）；
- `FR-CC-xx-description.md`：本轮完成报告。

### 项目级报告命名规则

项目级报告统一放在 `docs/context/report/`：

- `PVR-project-name.md`：项目验证报告；
- `PCR-project-name.md`：项目收口报告；
- `Project-Final-Review-project-name.md`：项目最终复核；
- `Release-Decision-project-name.md`：发布决策。

## 项目完整工作流

项目按以下顺序推进：

```text
Business Guide
→ Business Ready Gate
→ SRS
→ DDD (optional)
→ TV (as needed)
→ TDD
→ Implementation Plan
→ CC
→ Implementation
→ IHR
→ ATR
→ HVR (if required)
→ FR
→ [下一轮 CC → ... → FR] × N
→ PVR
→ PCR
→ Project Final Review
→ Release Decision
```

工作流含义：

- `Business Guide`：梳理和澄清业务需求。
- `Business Ready Gate`：确认业务需求已经足够明确，可以进入软件需求分析。
- `SRS`：建立软件需求规格基线。
- `DDD`：在领域模型或业务边界复杂时补充领域设计，可选。
- `TV`：在存在技术不确定性时验证 Odoo 或相关技术事实，按需执行。
- `TDD`：形成技术设计基线。
- `Implementation Plan`：将技术设计拆解为可执行的实施步骤。
- `CC`：冻结当前轮次的 Coding Contract、范围、约束和验收标准。
- `Implementation`：严格按照当前轮次契约实施。
- `IHR`：记录实际实施过程、变更、偏差和处理结果。
- `ATR`：记录自动化测试及其结果。
- `HVR`：在需要人工、界面或真实业务流程验证时记录人工验证。
- `FR`：确认当前轮次是否完成；`FR` 不是整个项目的最终完成判定。
- `CC → ... → FR`：项目可以进行多轮增量开发，每轮都必须有独立契约和完整记录。
- `PVR`：汇总多轮开发的验证证据和遗留问题。
- `PCR`：对项目整体是否满足收口条件做项目级判定。
- `Project Final Review`：在 PCR 之后进行最终项目复核。
- `Release Decision`：基于最终复核结果决定是否发布，而不是由某一轮 `FR` 直接决定。

## 核实记录

以上 GitHub 信息由本地 Git 元数据和远程查询确认：

```text
origin  git@github.com:rambolee200311/odoo18_recordpanel.git
main -> origin/main
origin/main -> 7357e4b8069f49fb2976f5b18d7dbf89a7a23794
```
