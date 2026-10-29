# Ultima Console 标准管理中枢范式（Standard Management Hub）

> 版本：v1.0；日期：2026-10-29。
> 状态：用户 2026-10-29 拍板建立——"把 Ultima Console 的标准管理标准建立起来，以后方便给 Ultima Agent 来读。以后 Ultima Console 也要转换为 Ultima Agent 里边的一个基础能力"。
> 本地权威：`H:\UltimaAI\_shared\paradigms\UltimaAI-Console标准管理中枢范式.md`。
> 适用范围：全系产品（Agent / Gold / Console / Sentinel / Scan / Radar / Pay 及后续新产品）的**标准注册、同步、审计、版本基线**统一由 Ultima Console 承担；Ultima Agent 及其执行适配器（Codex / DeepSeek / 未来模型）读取本范式获得全系标准入口。
> 依据：G-TASKFLOW-001 任务工作流范式、G-DISPATCH-001 自主推进、ULTIMA-STANDARD §5.9 落盘与同步标准、产品接入 UltimaAdmin CMS 范式。

## 0. 一句话规则

**Ultima Console 是全系标准的唯一管理中枢（不是某一款产品的界面）：所有标准在 Console 侧注册与审计，Agent 侧只读执行；Console 同时登记为 Ultima Agent 的标准基础能力（m30），任何执行端（Codex/DeepSeek/未来模型）都必须读取它获得标准基线。**

## 1. 定位与分层

| 层 | 归属 | 职责 |
|---|---|---|
| 标准定义 | `_shared\paradigms\` + `_shared\server-assets.md` | 范式/台账唯一权威（不变，仍由主脑维护） |
| **标准管理中枢（Console）** | UltimaConsole 项目 + UltimaAdmin CMS（8913） | 标准清单登记、状态聚合、审计入口、版本基线；Agent 读取的**标准入口** |
| 标准执行（Agent） | UltimaAgent 及其适配器 | 读取 Console 标准 → 照标准执行 → 回执 |
| 用户管理/产品管理 | UltimaAdmin CMS | 统一用户中心 + 产品功能管理（与 Console 数据同源） |

## 2. Console 标准管理职责（Agent 读取后应执行的契约）

### 2.1 标准注册表（Console 维护，Agent 必读）

Console 维护全系标准注册表，Agent 在执行任何任务前必须读取对应标准：

| 标准域 | 权威源 | Agent 用途 |
|---|---|---|
| 任务工作流 | `_shared/paradigms/UltimaAI-任务工作流范式.md`（G-TASKFLOW-001） | 任务全流程（登记→评审→执行→审计→修复→验收→冻结） |
| 工单命名 | `_shared/paradigms/UltimaAI-全局工单命名标准.md`（G-WO-NAME-001） | 工单 ID/标题/文件命名 |
| 执行端调用 | `_shared/paradigms/Codex-外部执行端调用范式.md` | Codex 派发/回执/WIP/DoR |
| 队列登记 | `_shared/queue/global-queue-index.md` | 全局主表登记（派单前必须） |
| 产品接入 CMS | `_shared/paradigms/UltimaAI-产品接入UltimaAdminCMS范式.md` | 产品登记/数据/菜单/验收 |
| 服务器资产 | `_shared/server-assets.md` | 域名/端口/凭证指针（§6.4 本地访问地址） |
| 能力注册 | `_shared/registry.md` | 防重复开发，未登记不使用 |

### 2.2 版本基线（打 tag 铁律）

- 标准/范式/关键修改必须打 tag（`<标准名>-v<X.Y.Z>` 或 `<工单号>-closed-<日期>`），Agent 执行前先核对 tag 版本，缺 tag = 标准未闭环，禁止照旧版执行。
- 标准更新：主脑改权威源 → 打 tag → 同步 UltimaDocs 镜像 → 通知 Agent。Agent 不得在副本上改标准。

### 2.3 审计入口

- Console 侧审计 = 独立审计员按 G-TASKFLOW-001 执行；Agent 回执必须含：工单号/执行端/完成状态/根因结论/产出路径/验收证据/越界声明/环境声明。
- 标准偏差（Agent 执行与标准不符）→ 记入全局主表 blocked + 上报主脑复核。

## 3. Console 作为 Ultima Agent 基础能力（m30）

- 能力登记：UltimaAgent registry 组件 `ultima-console-standard-hub` + 能力 m30（登记见 `_shared/registry.md` 三节）。
- 能力语义：Console 向 Agent 提供**标准读取入口**（标准注册表 + 版本基线 + 审计门），Agent 任务执行的第一步 = 读 Console 标准注册表。
- 与 m28（任务工作流）/ m29（Manager 控制面）的关系：m28 定义流程本体，m29 负责编号/队列登记控制面，m30 提供标准基线入口——三者组合为 Agent 的标准执行闭环。

## 4. 读取顺序（Agent 必读链）

1. `H:\UltimaAI\INDEX.md`（根导航，2026-10-29 已加 Console 标准管理中枢引用）
2. `_shared/paradigms/UltimaAI-Console标准管理中枢范式.md`（本文件，m30）
3. 按任务类型进入 §2.1 标准注册表对应权威源

## 5. 边界（禁止项）

1. **Console 只管理标准，不派发任务**——派发仍走 G-DISPATCH-001 各项目自主 + Manager 可选监督。
2. **Console 不改写范式正文**——标准正文唯一权威仍在 `_shared/paradigms\`，Console 只维护注册表/状态/审计。
3. **Agent 不得绕过 Console 标准读取直接执行**——未读标准=裸跑，按 G-DISPATCH-001 越界处理。
4. **不新增唯一派发中枢**——本范式不改变 G-DISPATCH-001 自主推进版语义。

## 6. 验收（本范式生效门）

- [x] 范式落盘 `_shared/paradigms/`
- [x] registry.md 登记组件 `ultima-console-standard-hub` + 能力 m30
- [x] INDEX 引用本范式（阅读顺序 + 引用表）
- [ ] UltimaAgent 侧 registry 同步（登记后由 Agent 项目读入，不阻塞本范式生效）

## 7. 维护

- 本范式由主脑维护；标准注册表随新范式产生而增行（先补本表再通知 Agent）；变更走评审，旧版归档只读。
