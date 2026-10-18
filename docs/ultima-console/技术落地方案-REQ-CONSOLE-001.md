# Ultima Console 技术落地方案 · REQ-CONSOLE-001

- 版本：v0.9.1（复验口径澄清修订）｜ 日期：2026-10-17 ｜ 状态：**v0.9.1 已冻结（架构治理重审通过，复验 v5 全绿 40/40）**
- 冻结基线：本文件 v0.8（SHA 记录于 `tasks/queue/arch-governance-review-REQ-CONSOLE-001.md`）；v0.9 基线变更经架构治理重审通过；v0.9.1 = 复验 v2 口径澄清（飞书 N8 图内标注 + 评分下降 ≥5 触发统一），经架构治理重审通过并冻结（`tasks/queue/arch-governance-review-REQ-CONSOLE-001-v0.9.1.md`）；冻结后变更唯一通道=需求变更流程（REQ 更新→方案修订→重审）
- 上游输入：`docs/产品策划方案-REQ-CONSOLE-001.md`（v0.2 已冻结）+ `docs/REQ-CONSOLE-001-需求登记.md`（2026-10-17 已更新：飞书灾备推迟第二阶段 + 评分口径 + 预警阈值）+ **`docs/UX方案-REQ-CONSOLE-001.md`（v0.2 已冻结）+ `docs/UI方案-REQ-CONSOLE-001.md`（v0.1 已冻结，2026-10-18 用户拍板）——v1.1 迭代工单的设计依据**
- 审计依据：`console-tech-audit-report.md`（GAP-001~012）+ `-v2.md`（复验残余）+ `-v3.md`（V3-GAP）+ `-v4.md`（V4-GAP）+ `-v5.md`（V5 残余）+ `-v6.md`（V6 残余）+ `-v7.md`（V7 残余）+ `-v8.md`（PASS）逐项修复闭环；**v0.9 = 工单队列审计（console-queue-audit-report.md）P0-02/03/04 基线变更驱动；v0.9.1 = 复验 v2（console-queue-audit-report-v2.md）P0-02/P0-04 口径澄清驱动**
- 下游：`Ultima-工程方法论` 拆工单 → 任务队列 → 看门狗监督

---

## 一、输入清单核验

| 输入 | 状态 |
|---|---|
| 产品策划方案（范围/P0+P1 MVP/指标） | ✅ v0.2 已冻结 |
| 本期 REQ 列表 | ✅ REQ-CONSOLE-001 |
| 非功能约束（鸿蒙/双通道/只出结果/离线可用） | ✅ 见 §六 风险与非功能 |
| 策划成功指标（北极星=每周主动打开≥5 次） | ✅ 技术承载见 §五.4（修复 GAP-001） |

## 二、技术选型

### 2.1 硬约束排除（GAP-003 修复：证据表版本/日期纯化，URL 非 4xx）

核验日期：2026-10-17。证据固定列：**官方页面标题｜完整页面 URL｜关键版本/发布日期（机械口径：只允许裸版本号、裸 ISO 日期、两者组合或单个"—"；页面无版本号则写"—"）｜访问核验日｜结论**。许可证名/商业属性/维护判断及页面无版本号的说明一律放结论列，不占版本列。不适用项单独列于表后并写明理由。

**许可证约束（不采 GPL）**

| 候选 | 官方页面标题 | 完整页面 URL | 关键版本/发布日期 | 访问核验日 | 结论 |
|---|---|---|---|---|---|
| ArkTS/ArkUI | OpenHarmony 主仓 LICENSE 文件 | https://gitee.com/openharmony/openharmony/blob/master/LICENSE | — | 2026-10-17 | Apache-2.0，非 GPL ✅（LICENSE 文件无版本号） |
| Flutter | Flutter 仓库 LICENSE 文件 | https://github.com/flutter/flutter/blob/master/LICENSE | — | 2026-10-17 | BSD-3-Clause，非 GPL ✅（LICENSE 文件无版本号） |
| 鸿蒙 RDB | HarmonyOS RDB 开发指南 | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/database-rdb-guidelines | — | 2026-10-17 | 系统内置 Apache-2.0，非 GPL ✅（页面未标独立版本号） |
| GitHub REST API | GitHub REST API 文档 | https://docs.github.com/en/rest | — | 2026-10-17 | 公有接口，无许可冲突 ✅（API 文档无发布版本号） |
| 飞书 OpenAPI | 飞书开放平台文档 | https://open.feishu.cn/document | — | 2026-10-17 | 公有接口，无许可冲突 ✅（文档无发布版本号） |
| 豆包 API | 豆包开放平台文档 | https://www.volcengine.com/docs/82379 | — | 2026-10-17 | 商业条款，非 GPL ✅（文档无发布版本号） |
| DeepSeek API | DeepSeek API 文档 | https://platform.deepseek.com/api-docs | — | 2026-10-17 | 商业条款，非 GPL ✅（文档无发布版本号） |
| 文件 JSON / 直连本地 | — | — | — | — | **不适用**：自研制式/私有协议，无外部许可证依赖 |

**平台兼容约束（必须兼容鸿蒙 ArkTS/ArkUI）**

| 候选 | 官方页面标题 | 完整页面 URL | 关键版本/发布日期 | 访问核验日 | 结论 |
|---|---|---|---|---|---|
| ArkTS/ArkUI | ArkTS 入门（Getting Started with ArkTS） | https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V5/arkts-get-started-V5 | 10；2025-05-20 | 2026-10-17 | 原生鸿蒙 ✅ 首选（页面标注 Since API version 10、Last updated 2025-05-20） |
| Flutter | Flutter 3.22 Release Notes | https://docs.flutter.dev/release/release-notes/release-notes-3.22.0 | 3.22.0；2024-05-14 | 2026-10-17 | ⚠️ 官方平台未含 OpenHarmony，社区适配，降备选 |
| 鸿蒙 RDB | HarmonyOS RDB 开发指南 | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/database-rdb-guidelines | — | 2026-10-17 | ✅ 系统 API（页面未标独立版本号） |
| WebView 套壳 | ArkUI 组件能力文档 | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/arkui-overview | — | 2026-10-17 | ❌ **一票否决**（不满足旋转/多窗/离线原生需求；页面未标独立版本号） |
| GitHub/飞书/云端 | 各服务方文档 | 见许可证表 URL | — | 2026-10-17 | ✅ 无平台冲突 |
| 直连本地 | — | — | — | — | **不适用**：自研 HTTP 私有协议，与平台无关 |

**维护状态约束（排除停更）**

| 候选 | 官方页面标题 | 完整页面 URL | 关键版本/发布日期 | 访问核验日 | 结论 |
|---|---|---|---|---|---|
| ArkTS/ArkUI | ArkTS 入门（Getting Started with ArkTS） | https://developer.huawei.com/consumer/en/doc/harmonyos-guides-V5/arkts-get-started-V5 | 2025-05-20 | 2026-10-17 | ✅ 官方文档在维护（页面标注 Last updated 2025-05-20，可访问） |
| Flutter | Flutter 3.22 Release Notes | https://docs.flutter.dev/release/release-notes/release-notes-3.22.0 | 3.22.0；2024-05-14 | 2026-10-17 | ✅ 官方发布链在维护（页面可访问） |
| 鸿蒙 RDB | HarmonyOS RDB 开发指南 | https://developer.huawei.com/consumer/cn/doc/harmonyos-guides/database-rdb-guidelines | — | 2026-10-17 | ✅ 官方指南在维护（页面未标独立版本号，可访问） |
| GitHub REST API | GitHub Changelog | https://github.blog/changelog | — | 2026-10-17 | ✅ 服务在维护（页面显示 changelog 条目日期，核验日可访问） |
| 飞书 OpenAPI | 飞书开放平台文档 | https://open.feishu.cn/document | — | 2026-10-17 | ✅ 服务在维护（页面未标独立版本号） |
| 豆包/DeepSeek API | 各平台文档 | 见许可证表 URL | — | 2026-10-17 | ✅ 服务在维护 |
| WebView 套壳 | 已否决 | — | — | — | 不评估 |
| 文件 JSON / 直连本地 | — | — | — | — | **不适用**：自研无外部维护依赖 |

**不适用项理由（移出外部证据要求）**：文件 JSON=自研制式数据格式，无许可证/平台/维护三方外部依赖；直连本地=自研私有协议，无许可证/平台/维护三方外部依赖。

硬约束结论：仅 WebView 套壳被"平台兼容"一票否决；Flutter 因官方 3.22 Release Notes 平台栏目未含 OpenHarmony（社区适配），标记成熟度风险并保留为备选；其余候选全部过筛进入 §2.2 矩阵。

### 2.2 候选加权矩阵（修复 GAP-002：复算，统一保留两位小数）

权重：需求匹配 30% ｜ 成熟度 20% ｜ 鸿蒙生态 20% ｜ 维护 15% ｜ 学习成本 10% ｜ 许可 5%｜总分=Σ(分×权)

**选型 1：端框架**
| 候选 | 需求30% | 成熟20% | 鸿蒙20% | 维护15% | 学习10% | 许可5% | 总分 |
|---|---|---|---|---|---|---|---|
| ArkTS + ArkUI（原生） | 5 | 4 | 5 | 4 | 3 | 5 | 4.45 ✅ |
| 鸿蒙 WebView 套壳（H5） | 3 | 3 | 3 | 3 | 4 | 5 | 3.20 ❌ 硬约束否决 |
| Flutter（鸿蒙适配） | 3 | 4 | 3 | 4 | 4 | 5 | 3.55（备选） |

复算：ArkUI=5×.3+4×.2+5×.2+4×.15+3×.1+5×.05=1.50+0.80+1.00+0.60+0.30+0.25=4.45；WebView=0.90+0.60+0.60+0.45+0.40+0.25=3.20；Flutter=0.90+0.80+0.60+0.60+0.40+0.25=3.55

结论：**原生 ArkTS + ArkUI**（4.45 最高；WebView 被硬约束否决）。

**选型 2：数据桥接通道**
| 候选 | 需求30% | 成熟20% | 鸿蒙20% | 维护15% | 学习10% | 许可5% | 总分 |
|---|---|---|---|---|---|---|---|
| GitHub REST API（桥接） | 5 | 5 | 5 | 5 | 4 | 5 | 4.90 ✅ |
| 直连本地电脑（局域网服务） | 3 | 3 | 2 | 2 | 3 | 5 | 2.75（备选，断电断网不可用） |
| 飞书 OpenAPI 直读（主通道） | 3 | 4 | 4 | 4 | 3 | 5 | 3.65（辅助/灾备） |

复算：GitHub=1.50+1.00+1.00+0.75+0.40+0.25=4.90；直连=0.90+0.60+0.40+0.30+0.30+0.25=2.75；飞书=0.90+0.80+0.80+0.60+0.30+0.25=3.65

结论：**GitHub 为桥接主通道**（APP 不可直连本地电脑），**飞书为灾备/可选数据源（第二阶段 N8）**，本地为权威源（电脑端豆包推送）。

**选型 3：本地离线存储（APP 侧）**
| 候选 | 需求30% | 成熟20% | 鸿蒙20% | 维护15% | 学习10% | 许可5% | 总分 |
|---|---|---|---|---|---|---|---|
| 鸿蒙关系型数据库（RDB） | 5 | 4 | 5 | 4 | 4 | 5 | 4.55 ✅ |
| 文件 JSON 直读 | 3 | 4 | 4 | 3 | 5 | 5 | 3.70（备选，简单场景） |

复算：RDB=1.50+0.80+1.00+0.60+0.40+0.25=4.55；JSON=0.90+0.80+0.80+0.45+0.50+0.25=3.70

结论：**鸿蒙 RDB 存离线快照 + JSON 标准制式文件为同步载体**（断网可读最近一次有效状态，不白屏）。

**选型 4：小助手推理调用**
| 候选 | 需求30% | 成熟20% | 鸿蒙20% | 维护15% | 学习10% | 许可5% | 总分 |
|---|---|---|---|---|---|---|---|
| 云端模型 API（豆包/DeepSeek 按通道） | 5 | 4 | 4 | 4 | 4 | 5 | 4.35 ✅ |
| 端侧小模型 | 2 | 3 | 4 | 3 | 3 | 5 | 3.00（备选，算力受限） |

复算：云端=1.50+0.80+0.80+0.60+0.40+0.25=4.35；端侧=0.60+0.60+0.80+0.45+0.30+0.25=3.00

结论：**小助手调用云端模型 API**，按双通道（A=豆包/B=DeepSeek）路由，密钥存 APP 本地加密存储（HarmonyOS 安全存储）。

### 2.3 选型 ADR（四要素齐：Context/Decision/Consequences/Status）

# ADR-001 · 端框架选型
## Status
accepted
## Context
首版鸿蒙 MatePad mini 原生 APP，需可旋转、多窗联动、离线可用；WebView 套壳被硬约束（平台兼容）否决。
## Decision
原生 ArkTS + ArkUI（加权 4.45）。
## Consequences
+ 旋转/多窗/离线能力原生支持，性能可控。− 后续 iOS/Mac/安卓/Windows 需按各端代码规则重写（发布管理已规划多端路线）。被否方案：WebView 套壳（3.20，硬约束否决）、Flutter（3.55 备选）。

# ADR-002 · 数据桥接通道选型
## Status
accepted（2026-10-17 变更注记：飞书灾备启用时点推迟第二阶段 N8，GitHub 主通道不变，见 v0.9 修复对照）
## Context
APP 不能直连本地电脑（关机/断网不可达）；需中转站，飞书作云端备份（第二阶段启用）。
## Decision
GitHub REST API 为桥接主通道（加权 4.90），飞书 OpenAPI 为灾备/可选数据源（第二阶段 N8），本地为权威源。
## Consequences
+ 本地关机断网仍可经 GitHub 读最近同步；飞书防本地丢失（第二阶段）。− 依赖 GitHub 可用性（限流见风险 R1）；同步延迟 ≤1 天（见指标）。

# ADR-003 · 本地离线存储选型
## Status
accepted
## Context
断网可读最近一次有效状态，不白屏。
## Decision
鸿蒙 RDB 存离线快照（加权 4.55），标准制式 JSON 为同步载体。
## Consequences
+ 离线可用、查询快。− 需维护同步逻辑与一致性（数据新鲜度 ≤1 天）。

# ADR-004 · 小助手推理调用选型
## Status
accepted
## Context
小助手承担审核/总结/建议/关键节点汇报，需较强推理且按双通道隔离。
## Decision
云端模型 API（加权 4.35），A 通道=豆包、B 通道=DeepSeek，密钥存 APP 本地加密存储（HarmonyOS 安全存储）。
## Consequences
+ 推理质量高、双通道隔离。− 需处理限流/退避/成本（AI 工程技能 LLMOps 最小项）。

## 三、整体架构（C4 两级图）

### 3.1 Context 图（系统与外部，修复 V2-GAP-003：电脑端豆包入图、双向清晰）

```
                     ┌─────────────┐
                     │  Owner（用户）│
                     └──────┬──────┘
                            │ 横屏/竖屏交互（本地渲染，无网络依赖）
                            ▼
              ┌─────────────────────────┐
              │   Ultima Console（鸿蒙APP） │
              │   只监督+审核+下达指令      │
              └───────┬────────┬─────────┘
              ①拉取(主)│        │ ④飞书灾备（第二阶段 N8）
                      ▼        ▼
   ┌──────────────────┐   ┌──────────────┐
   │ ②GitHub 仓库       │   │ ⑤飞书云文档     │
   │ sync/*.json      │   │ （第二阶段启用） │
   │ tasks/queue/*.md │   └──────────────┘
   │ docs/*.md        │
   └───────▲──────────┘
           │ ③发布（电脑端豆包推送权威源结果）
   ┌───────┴──────────┐
   │ ⑥电脑端豆包（任务监控器）│
   │ 写方案/下任务队列/监督执行 │
   └───────▲──────────┘
           │ ⑦写入（权威源）
           ▼
   ┌──────────────────┐
   │ ⑧本地 H:\UltimaAI  │
   │ （权威源/执行端产出）│
   └──────────────────┘
```

流向（方向唯一，无歧义）：
- **拉取方向（APP 读）**：① APP→GitHub 拉取 sync/*.json、tasks/queue/*.md、docs/*.md（GET）；④ APP→飞书授权+只读（灾备，**第二阶段 N8，首版不实现**）
- **发布方向（电脑端写）**：⑦ 电脑端豆包→本地权威源写入 → ③ 本地→GitHub 发布（电脑端豆包推送）→ ① APP 下次拉取获得新状态
- **执行端产出**：Codex/DeepSeek 执行工单 → 产出落 ⑧ 本地 → 由 ⑥ 电脑端豆包周期推送 ③ 上 GitHub（详见 §六 M1 数据链路）
- 外部模型：小助手云端 API 见图 3.2（不在 Context 图重复）

### 3.2 Container 图（修复 GAP-004：带流向/协议/外部模型）

```
【外部】GitHub REST API ──HTTPS(JSON)──▶┐
【外部】飞书 OpenAPI（第二阶段 N8，首版不实现）──HTTPS(OAuth2)──▶│
【外部】云端模型 API(豆包/DeepSeek) ──HTTPS(JSON)──▶│
                                        ▼
┌──────────────────────────────────────────────────┐
│            Ultima Console（鸿蒙 APP）                │
│ ┌──────────────┐   调用   ┌──────────────────────┐ │
│ │  UI 层（ArkUI）│◀───────│     数据服务层          │ │
│ │ 仪表盘容器     │   查询   │ · GitHub Sync Service │ │
│ │ 产品钻取页     │◀───────│ · 飞书 OAuth 连接器(N8)  │ │
│ │ 审批视图       │   事件   │ · 本地 RDB 快照        │ │
│ │ 双通道分栏     │         └──────────┬───────────┘ │
│ └──────┬───────┘                    │读写          │
│        │调用                        ▼              │
│        │         ┌──────────────────────────────┐  │
│        └────────▶│  小助手服务                    │  │
│                   │ · 总结/审核/建议（云端 API 路由）│  │
│                   │ · 关键节点汇报触发器            │  │
│                   └──────────────────────────────┘  │
│         ┌──────────────────────────────────────┐   │
│         │ 审计/评分引擎                          │   │
│         │ · 读回执算评分/偏移/问题清单             │   │
│         │ · 制式校验（防漂移）                    │   │
│         └──────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

流向（首版外部源=GitHub 主通道 + 云端模型 API；**飞书为第二阶段 N8，首版不实例化**）：外部源 →(HTTPS/JSON) 数据服务层 →(RDB 读写) 本地快照；UI 层 ←(查询/事件) 数据服务层；UI 层 →(调用) 小助手服务 →(云端 API 路由) 外部模型；审计/评分引擎 ←(回执) 数据服务层 →(结果) UI 层。

### 3.3 关键用例串验证（修复 GAP-005：补失败/回执路径）

1. **看全局（成功）**：启动 → 数据服务层拉 GitHub sync/*.json → RDB 落快照 → UI 渲染四板块 → 用户见评分/偏移。**（失败路径）**：GitHub 429/不可达 → 退避重试 → 仍失败 → 降级读 RDB 快照 → 显示"数据截至 {时间}"，不白屏。
2. **钻取工单（成功）**：点产品 → 数据服务层读 GitHub tasks/queue/*.md + docs/*.md → 渲染工单/审计列表 → 逐层展开。**（失败路径）**：文档缺失/格式错 → 制式校验拦截 → 显示"该层数据缺失"并登记问题，不崩溃。
3. **拍板闭环（成功）**：小助手出建议 → 用户审核 → 同意 → 数据服务层推送指令回执到 GitHub → 电脑端豆包读回执 → 写新任务方案。**（失败/回执路径）**：推送失败 → 保留待投递状态 + 重试；已投递未确认 → 显示"指令已发出，待执行端回执"；执行端回执异常 → 登记问题并提示用户，闭环可追。
4. **断网阅读（成功）**：RDB 快照 → 渲染最近一次有效状态，不白屏。**（失败路径）**：无任何快照（首装未同步）→ 显示引导页"首次同步需要网络"，不白屏。

## 四、接口契约表（GAP-006/007/012 + V2-GAP-002 修复：可实施契约）

### 4.1 契约表（五列 + 逻辑/原生分层 + 鉴权 + 载荷位置 + GitHub 原生映射）

> **层级说明（V4-GAP-001 修复）**：第一列是 **APP 内逻辑操作（适配器方法）**，由 **APP GitHub Adapter** 提供；对外真实 HTTP 见"GitHub 原生 HTTP 契约"列。**转换责任**：Adapter 负责 统一信封 `{code,message,data}` ↔ GitHub 原生载荷 双向转换（目录响应数组/对象→列表；文件写入的 Base64 content、commit message、更新时 sha 冲突处理），转换规则见 4.1.1。契约是 B 通道执行的唯一授权边界。

通用约定：
- **部署拓扑**：APP 内数据服务层直连 GitHub REST API（适配器模式），**不引入本地桥接服务**（与 §3.1/3.2、N7 一致）；**飞书走 OAuth2（第二阶段 N8，首版不实例化）**；云端模型 API 由 APP 内小助手服务直连（按通道路由）
- 鉴权机制：**GitHub PAT** 存 APP 本地加密存储（HarmonyOS 安全存储，不落明文）；**飞书走 OAuth2（第二阶段 N8，首版不实现，§/lark/oauth 换取 access_token 推迟）**；**云端模型 API Key 存 APP 本地加密存储，按通道（A=豆包/B=DeepSeek）取用**（端侧直连，不用"环境变量"表述）
- 载荷位置：请求体统一 `Content-Type: application/json`；响应体 JSON；鉴权放 `Authorization: Bearer <token>`；**GET 一律不带 body，参数走 path/query**
- 响应 schema：APP 逻辑层统一信封 `{code, message, data}`，`code=0` 成功；GitHub 原生层按 GitHub API 原生响应（见 4.1.1）

| 逻辑操作（适配器方法） | 调用方→提供方 | 鉴权 | 载荷位置（入参） | 出参（APP 信封） | 错误码 | 版本策略 | GitHub 原生 HTTP 契约（method + path + 转换要点） |
|---|---|---|---|---|---|---|---|
| listProducts | APP UI/数据服务层→APP GitHub Adapter | Bearer PAT | 无 | 产品列表[{id,name,status,stage,score,deviation}] | E_4001/E_4901/E_4902/E_4903/E_4904 | v1：兼容 3 版；弃用提前 1 版公告；破坏性变更 expand-contract | `GET /repos/{owner}/{repo}/contents/sync`；目录数组→逐文件取 product.json 合并 |
| getProduct | APP UI/数据服务层→APP GitHub Adapter | Bearer PAT | path: product_id | 产品详情（规划/阶段/工单/审计/评分/偏移） | E_4002/E_4901/E_4902/E_4903/E_4904 | 同上 | `GET /repos/{owner}/{repo}/contents/sync/product.json`；文件内容 Base64 解码 |
| listWorkOrders | APP UI/数据服务层→APP GitHub Adapter | Bearer PAT | path: product_id；query: page | 工单列表[{id,title,status,stage,version}] | E_4003/E_4901/E_4902/E_4903/E_4904 | 同上 | `GET /repos/{owner}/{repo}/contents/tasks/queue`（列目录）→ Adapter 按 `.md` 后缀过滤 → 对选中文件逐 `GET /repos/{owner}/{repo}/contents/tasks/queue/{filename}` |
| listAudits | APP UI/数据服务层→APP GitHub Adapter | Bearer PAT | path: product_id | 审计报告列表[{id,title,conclusion,date}] | E_4004/E_4901/E_4902/E_4903/E_4904 | 同上 | `GET /repos/{owner}/{repo}/contents/tasks/queue`（列目录）→ Adapter 按文件名含 `audit` 过滤 → 逐文件 GET |
| approveFeedback | APP UI/审批视图→APP GitHub Adapter | Bearer PAT | body: {decision_id,action:approve/reject,comment} | {code:0,data:{ref}} | E_4101/E_4901/E_4902/E_4903/E_4904/E_4905 | 同上；幂等键=decision_id | `PUT /repos/{owner}/{repo}/contents/tasks/queue/feedback-{decision_id}.md`；body 含 content（Base64）、message（commit）、sha（更新时必带）；409/422→E_4905 冲突 |
| adjustFeedback | APP UI/审批视图→APP GitHub Adapter | Bearer PAT | body: {decision_id,action:adjust,plan} | {code:0,data:{task_ref}} | E_4102/E_4901/E_4902/E_4903/E_4904/E_4905 | 同上；幂等键=decision_id | `PUT /repos/{owner}/{repo}/contents/tasks/queue/feedback-{decision_id}.md`；同上 |
| requestSummary | APP UI→APP 小助手服务→云端模型 API | Bearer（模型 API Key，本地加密存储） | body: {product_id,scope} | {code:0,data:{summary,issues,suggestion}} | E_4201/E_4901/E_4902/E_4903/E_4904 | 同上 | 豆包 `POST https://ark.cn-beijing.volces.com/api/v3/chat/completions`；DeepSeek `POST https://api.deepseek.com/chat/completions`（按通道路由） |
| listNotifications | APP UI/触发器→APP 小助手服务（**本地调用，非网络端点**） | 无（本地进程内） | query: product_id | {code:0,data:{notifications[]}} | E_4202/E_4902（本地端点：E_4901/E_4903/E_4904 不适用） | 同上 | 本地聚合，不直连外部；不套 Bearer 模型 Key |
| larkOAuth | APP 数据服务层→飞书 OAuth2（**第二阶段 N8，首版不实现**） | 无（换取后加密存储） | body: {code} | {code:0,data:{access_token,scope,expires_at}} | E_4301/E_4901/E_4902/E_4903/E_4904 | 同上；token 加密存储 | 飞书 `POST https://open.feishu.cn/open-apis/authen/v2/oauth/token` |
| getLarkDoc | APP 数据服务层→飞书 OpenAPI（**第二阶段 N8，首版不实现**） | Bearer（飞书 access_token） | path: doc_token | 文档内容（只读） | E_4302/E_4901/E_4902/E_4903/E_4904 | 同上 | 飞书 `GET https://open.feishu.cn/open-apis/docx/v1/documents/{token}` |

### 4.1.1 适配器转换规则（V4-GAP-001 补充：完整 HTTP→错误码映射）

| 方向 | 转换内容 |
|---|---|
| GitHub→APP | GitHub Contents API 目录响应（数组/对象）→ APP 列表结构；文件内容 Base64 → UTF-8 解码 → 制式 JSON 校验（§5.3）；HTTP 状态码 → 统一错误码（见下表） |
| APP→GitHub | 统一信封出参 → GitHub 原生请求（写文件：`content` Base64、`message` commit、更新时带 `sha`）；收到 409/422 即按冲突处理（幂等键 decision_id 去重） |
| 小助手 | 请求 summary 用统一信封进、出；模型 API 原生 chat/completions 载荷与 APP 信封转换由小助手服务内部完成 |

**端点属性表（V4-GAP-001 闭合：错误码由属性机械推导，双向 0 差异）**

| 逻辑操作 | external_http | write | 业务主码 | 公共码集合（按属性推导） |
|---|---|---|---|---|
| listProducts | true | false | E_4001 | E_4901/E_4902/E_4903/E_4904 |
| getProduct | true | false | E_4002 | E_4901/E_4902/E_4903/E_4904 |
| listWorkOrders | true | false | E_4003 | E_4901/E_4902/E_4903/E_4904 |
| listAudits | true | false | E_4004 | E_4901/E_4902/E_4903/E_4904 |
| approveFeedback | true | true | E_4101 | E_4901/E_4902/E_4903/E_4904/E_4905 |
| adjustFeedback | true | true | E_4102 | E_4901/E_4902/E_4903/E_4904/E_4905 |
| requestSummary | true | false | E_4201 | E_4901/E_4902/E_4903/E_4904 |
| listNotifications | false | false | E_4202 | E_4902（本地端点，E_4901/E_4903/E_4904 豁免） |
| larkOAuth（第二阶段 N8） | true | false | E_4301 | E_4901/E_4902/E_4903/E_4904 |
| getLarkDoc（第二阶段 N8） | true | false | E_4302 | E_4901/E_4902/E_4903/E_4904 |

推导规则：E_4901（鉴权）/E_4903（限流）/E_4904（网络不可达）仅 external_http=true 的端点；E_4902（参数校验）全部端点；E_4905（冲突）仅 write=true 端点。端点表错误码集合必须与本节属性表推导结果一致（机械校验，双向比对 0 差异）。

**HTTP/网络条件 → 统一错误码 完整映射表**

| HTTP/网络条件 | 统一错误码 | 适用逻辑操作 | 处置 |
|---|---|---|---|
| 200/201 成功 | code=0 | 全部 | 正常返回 |
| 400 参数错误 | E_4902 | 全部（参数校验） | 前端拦截修正 |
| 401 未认证 / 403 无权限 | E_4901 | 全部外部 HTTP 端点（本地端点除外） | 引导重新授权 |
| 404 资源不存在 | E_4001（listProducts 无产品）/ E_4002（getProduct 产品不存在）/ E_4003（listWorkOrders 工单缺失）/ E_4004（listAudits 审计缺失）/ E_4302（getLarkDoc） | 按逻辑操作区分 | 展示可读信息 + 登记问题 |
| 409 冲突（sha 过期/版本冲突） | E_4905 | approveFeedback / adjustFeedback | decision_id 幂等去重，提示重试/查看现状 |
| 422 校验失败（GitHub 写文件内容校验） | E_4905（写操作）/ E_4902（参数校验） | approveFeedback / adjustFeedback | 写失败按冲突处理；参数问题前端修正 |
| 429 限流 | E_4903 | 全部外部 HTTP 端点（本地端点除外） | 指数退避重试（上限 3 次）→ 降级 RDB 快照 |
| 网络不可达/超时/离线 | E_4904 | 全部外部 HTTP 端点（本地端点除外） | 降级 RDB 快照 + 显示数据截至时间 |
| 推理服务 5xx | E_4201 | requestSummary（仅此端点） | 降级：仅展示本地事实，不展示无依据建议 |
| 本地聚合失败（非网络） | E_4202 | listNotifications（V6-GAP-001 修复：不套 HTTP 条件） | 跳过本次汇报，下一节点重试 |

> 契约是 B 通道执行的唯一授权边界；变更走需求管理 RTM 更新。上表"外部 API 映射"列即 GitHub/飞书/豆包/DeepSeek 真实端点，可直接转接口级测试用例。

### 4.2 统一错误语义（GAP-012 + V2-GAP-002 修复：码族自洽）

错误码规则：`E_<业务域><两位序号>`，每端点 1 个业务主码（xx=01 起），加 **5 个公共码**（4901/4902/4903/4904/4905）。**公共码适用范围按端点属性推导（§4.1.1 端点属性表）**：E_4901/E_4903/E_4904 仅外部 HTTP 端点；E_4902 全部端点；E_4905 仅 GitHub 写操作端点——并非机械"各端点通用"。全量码表：

| 错误码 | 业务域 | 语义 | 处理 |
|---|---|---|---|
| E_4001 | sync 业务 | 无产品数据 | 展示可读信息 + 登记问题 |
| E_4002 | sync 业务 | 产品不存在 | 提示 + 刷新列表 |
| E_4003 | sync 业务 | 工单读取失败 | 提示 + 登记问题 |
| E_4004 | sync 业务 | 审计读取失败 | 提示 + 登记问题 |
| E_4101 | feedback 业务 | 指令投递失败 | 保留待投递 + 重试 |
| E_4102 | feedback 业务 | 调整任务失败 | 提示 + 重试 |
| E_4201 | assistant 业务 | 推理调用失败 | 降级：仅展示本地事实，不展示无依据建议 |
| E_4202 | assistant 业务 | 汇报生成失败 | 降级：跳过本次汇报，下一节点重试 |
| E_4301 | lark 业务（第二阶段 N8） | 飞书授权失败 | 引导重新授权 |
| E_4302 | lark 业务（第二阶段 N8） | 文档读取失败 | 降级 GitHub 主通道 |
| E_4901 | 公共 | 鉴权失败（未授权/凭证过期） | 引导重新授权，不白屏 |
| E_4902 | 公共 | 参数校验失败 | 前端拦截，提示修正 |
| E_4903 | 公共 | 限流（429） | 指数退避重试（上限 3 次）→ 降级 RDB 快照 |
| E_4904 | 公共 | 服务不可达（网络/离线） | 降级 RDB 快照 + 显示数据截至时间 |
| E_4905 | 公共 | 冲突（版本/幂等） | decision_id 幂等去重；冲突提示重试/查看现状 |

## 五、数据模型

### 5.1 聚合划分（轻 DDD）

- **产品聚合**（一致性边界=产品档案）：Product + 四板块状态 + 评分 + 偏移 + 问题清单
- **工单聚合**：WorkOrder + TaskUnit（任务单元，逐层展开）+ 回执
- **审计聚合**：AuditReport + 缺口项（GapItem，独立实体）
- **决策聚合**：Decision（审批流/指令回执，幂等键=decision_id）
- 外部只能引用聚合 ID（product_id / workorder_id / audit_id / decision_id）

### 5.2 ER 表结构（修复 GAP-008：3NF 可证明；GAP-009：变更标注列）

| 实体 | 主键/候选键 | 关键字段（函数依赖：全部非主键直接依赖主键） | 破坏性变更标注 |
|---|---|---|---|
| product | PK=product_id | name, status(四板块), stage, score, deviation, updated_at | 无（v1 新表） |
| work_order | PK=workorder_id | product_id(FK→product), title, status, stage, version, channel(A/B) | 无 |
| task_unit | PK=taskunit_id | workorder_id(FK→work_order), seq, title, status, done_at | 无 |
| audit_report | PK=audit_id | product_id(FK→product), title, conclusion, date | 无 |
| gap_item | PK=gap_id | audit_id(FK→audit_report), severity, desc, status | 无（由 gap_list 拆分，消除列表型复合属性） |
| issue | PK=issue_id | product_id(FK→product), severity, status, desc | 无 |
| decision | PK=decision_id | product_id(FK→product), action, status, feedback_ref, created_at | 无 |
| lark_conn | PK=lark_id | product_id(FK→product), token_enc, scope, expires_at | 第二阶段 N8（首版不建表） |
| event_log | PK=event_id | product_id(FK→product), event_type(open), ts(本地时间), device_local_flag | 无（新增，北极星采集；仅本地聚合不上传） |

3NF 说明：gap_item 独立实体后，audit_report 无列表型复合属性；各实体非主键字段均直接依赖主键（product_id/workorder_id/audit_id/decision_id/event_id），无传递依赖（work_order.title/status 直接依赖 workorder_id，不依赖 product_id 除 FK 引用）。候选键：每表主键即唯一候选键。event_log 保留规则：本地 RDB 按自然周聚合后压缩为周计数（open_count_week），超过 8 周的明细可清理（防本地膨胀），聚合结果不上传（隐私，见 N5）。

> 破坏性变更标注规则：删列/改类型/改约束 → 标注"提示发布管理走 expand-contract 排期"；本版 v1 均为新表无存量破坏，后续变更按规则补标。

### 5.3 标准制式 sync/product.json（GAP-010 修复：与磁盘实物完全一致，防漂移门）

> 本节为**当前快照**（非 schema 示例），与磁盘 `sync/product.json` 逐字段一致。**防漂移门**：每次产品档案更新后，方案 §5.3 与磁盘必须字段级一致（version/stage/summary/issues/refs），由治理体检做机器级深比较（JSON 键值全量比对）；不一致即登记 P1 漂移并阻塞冻结。当前快照（2026-10-17 鸿蒙首版发布，version 1.0.0）：

```json
{
  "product": "UltimaConsole",
  "version": "1.0.0",
  "status": "已发布",
  "stage": "已发布 v1.0.0",
  "updated_at": "2026-10-17T23:05:59+08:00",
  "summary": { "progress": 100, "score": 100, "deviation": "无", "blocker": "无" },
  "work_orders": [
    { "id": "wo-console-m1", "title": "M1 数据链路打通", "status": "已完成（m1-frozen）" },
    { "id": "wo-console-m2", "title": "M2 仪表盘容器", "status": "已完成（m2-frozen）" },
    { "id": "wo-console-m3", "title": "M3 产品钻取", "status": "已完成（m3-frozen）" },
    { "id": "wo-console-m4", "title": "M4 审计与评分引擎", "status": "已完成（m4-frozen）" },
    { "id": "wo-console-m5", "title": "M5 双通道与偏离预警", "status": "已完成（m5-frozen）" },
    { "id": "wo-console-m6", "title": "M6 审批流与小助手", "status": "已完成（m6-frozen）" },
    { "id": "wo-console-m7", "title": "M7 旋转布局收尾", "status": "已完成（m7-frozen）" },
    { "id": "wo-console-m8", "title": "M8 端到端验收与发布", "status": "已完成（m8-frozen / v1.0.0）" }
  ],
  "open_issues": [],
  "audit_reports": [
    { "id": "console-queue-audit-report", "conclusion": "需修复后派发" },
    { "id": "console-queue-audit-report-v5", "conclusion": "P0/P1 清零可派发（40/40 PASS）" }
  ],
  "refs": {
    "方案文档": "https://my.feishu.cn/docx/NvrzdEkJgob9hcxkgNYcXJ21nJf",
    "流程问卷": "https://my.feishu.cn/docx/E0oldf9QwoiQ3rxqRgwcKNE4npd"
  }
}
```

### 5.4 北极星指标技术承载（修复 GAP-001）

| 要素 | 设计 |
|---|---|
| 事件定义 | APP 冷启动完成仪表盘渲染 = 1 次"主动打开"；当日多次打开计多次 |
| 采集口径 | 本地匿名计数（event_log 表：event_type=open, ts），**不引入账号体系**（Non-Goal N5） |
| 存储位置 | APP 本地 RDB `event_log` 表（周期聚合，不随 sync 上传） |
| 4 周窗口算法 | 上线后第 1-4 周自然周，周打开次数求和 / 4 ≥ 5 即达标 |
| 验收点 | 里程碑 M8（端到端验收）增加验收门：埋点可采、口径可算；发布后 4 周回填实际值到策划指标台账 |

### 5.5 评分与偏移口径（v0.9 新增，工单审计 P0-03 修复）

**评分公式（机械可复算）**：

```
score = max(0, round(100 - 扣分合计))
扣分规则（输入：audit_report.gap_item + product.open_issues，按 severity + status）：
  P0 未关闭  -10/项
  P1 未关闭   -5/项
  P2 未关闭   -1/项（P2 合计扣分上限 -5）
  P0 已处理   -5/项（半扣）
  P1 已处理  -2.5/项（半扣）
  P2 已处理    0（不扣）
  无任何缺口 = 100
```

- 输入域：该产品当前审计报告的全部 gap_item 与 issue；status 取值 待处理/已处理
- 舍入：`round` 四舍五入取整（.5 进位）
- 边界：扣分合计 >100 时 score=0；P2 合计扣分超 5 按 5 计
- **金样本（验收夹具）**：① 无缺口 → 100；② 1×P0 未关闭+2×P1 未关闭 → 80；③ 1×P0 已处理 → 95；④ 6×P2 未关闭 → 95（上限 5）；⑤ 12×P0 未关闭 → 0（下限 0）
- 数据源：audit_report → gap_item 聚合 + product.open_issues；同一审计报告重复聚合去重（gap_id 唯一）

**偏移判定（相对基线）**：

```
基线 = 上次审计报告的 score（首次无历史时基线 = 策划基线初值）
无偏移：|当前 score - 基线| ≤ 5
负向偏移：当前 score - 基线 < -5（标记"负向偏移"）
正向偏移：当前 score - 基线 > 5（标记"正向偏移"）
纠正建议 = 未关闭缺口清单（按 severity 降序）+ 偏移方向说明
```

- "无漂移"判据（M4 验收）：同一审计报告数据重复计算 score 结果一致（确定性）；连续两次审计 score 变化 ≤5 视为进度稳定无偏移
- 示例：上次 84，本次 80 → 无偏移（|−4|≤5）；上次 84，本次 72 → 负向偏移（−12），建议=未关闭 P0/P1 清单

## 六、技术推进规划

### 6.1 里程碑表（带依赖列 + 高风险前置门）

| 里程碑 | 交付物 | 验收标准 | 前置依赖 | 前置风险门（见 6.3） |
|---|---|---|---|---|
| M1 数据链路打通 | GitHub 桥接拉取 sync/*.json → RDB 快照 → 断网可读 | 本地→GitHub→APP 全链路读通，断网显示快照 | — | — |
| M2 仪表盘容器 | 四板块 + 评分/偏移/阻塞卡片 | 一屏可读全产品状态 | M1 | — |
| M3 产品钻取 | 规划/工单/审计/任务单元逐层展开 | 3 步内到达工单/审计层 | M2 | 制式校验门（R5） |
| M4 审计与评分引擎 | 读回执算评分/偏移/问题清单 | 评分偏移可算可显示，无漂移 | M3 | 证据引用验证门（R4） |
| M5 双通道 + 偏离预警 | A/B 分栏标识 + 阈值主动提示 | 通道分栏正确，达阈值提示 | M4 | A/B 隔离测试门（R6） |
| M6 审批流 + 小助手 | 建议总结/审核拍板/反馈回执 | 决策闭环率回执 ≥80% | M5 | — |
| M7 旋转布局收尾 | 横屏双栏/竖屏独立布局全页面适配 | 两方向均无布局破坏 | M6 | — |
| M8 端到端验收 + 发布 | 全功能验收 + 鸿蒙发布包 + 北极星埋点验收 | DoD 项目级通过、缺陷清零、埋点可采 | M7 | — |

关键路径（最长链）：M1 → M2 → M3 → M4 → M5 → M6 → M7 → M8。链上里程碑延期=整体延期（开发由 Codex 执行，不设日历工期，按 DoD 顺序推进）。

### 6.2 风险登记表（3×3，六列齐）

| 风险 | 概率 | 影响 | 触发信号 | 缓解 | 兜底 |
|---|---|---|---|---|---|
| R1 GitHub API 限流 | 中 | 中 | 429/超频 | 同步频率 ≤1 天 + 指数退避重试 | 降级读 RDB 快照 |
| R2 飞书授权失效 | 低 | 低 | token 过期 401 | 提前刷新 + 授权页引导 | 走 GitHub 主通道 |
| R3 本地关机/断网 | 中 | 中 | 电脑不可达 | 本地→GitHub 推送周期化 | GitHub 最近快照可读 |
| R4 小助手推理误判 | 中 | 高 | 建议与事实不符 | 审核门 + 建议带证据引用 + 前置验证门 | 用户打回，登记问题 |
| R5 多产品供数格式漂移 | 中 | 高 | sync JSON 缺字段 | 制式校验门（M3 前置）+ 治理体检核对 | 标记"数据缺失"不白屏 |
| R6 双通道污染 | 低 | 高 | A/B 数据串线 | 通道字段强制 + 独立存储 + A/B 隔离测试门（M5 前置） | 隔离校验，失败即阻断 |

### 6.3 高风险前置验证门（修复 GAP-011：R4/R5/R6 全前置）

| 风险门 | 挂靠里程碑 | 验收内容 | 失败处置 |
|---|---|---|---|
| 制式校验门（R5） | M3 | sync JSON 缺字段/格式错 → 校验拦截 + 登记，不渲染 | 打回 M2 返工 |
| 证据引用验证门（R4） | M4 | 小助手建议必须带证据引用，无引用即不展示 | 打回 M3 补验证 |
| A/B 隔离测试门（R6） | M5 | 双通道数据隔离测试：A 数据不串入 B 视图 | 阻断 M5，修复后重测 |

### 6.4 偏离预警阈值（v0.9 新增，工单审计 P0-04 修复）

**触发条件（任一命中即提示，全部未命中则不提示）**：

| 触发项 | 判定规则 | 数据来源 |
|---|---|---|
| 评分下降 | 当前 score - 上次审计基线 ≤ -5（即下降 ≥5 分即触发，含恰好 5 分；与 REQ 需求要点 8 一致） | §5.5 偏移判定 |
| P0 缺口存在 | 存在 status=待处理 的 P0 缺口（gap_item 或 open_issues） | 审计/问题清单 |
| 工单阻塞 | 存在 status=阻塞 的工单 | work_order.status |
| 执行超期未冻结 | 工单 status=执行中 且 最近状态变更时间距今 >7 自然日 | work_order.updated_at |

- 时间窗：7 自然日，从工单最近一次状态变更（updated_at）起算
- 比较符：评分下降判定用 `score_now - baseline ≤ -5`（恰好 -5 触发，-6 触发）；阻塞按状态字面值
- 缺失数据行为：基线缺失（无历史审计）时不触发"评分下降"项，其余三项照常判定
- **边界样例（验收夹具）**：① 评分 80→76（-4）→ 不触发；② 评分 80→75（-5）→ 触发（恰好 5 分触发，与 REQ"≥5"一致）；③ 评分 80→74（-6）→ 触发；④ 1 个 P0 待处理 → 触发；⑤ 工单阻塞 0 天 → 触发（状态即触发，与天数无关）；⑥ 执行中 6 天 → 不触发；⑦ 执行中 8 天 → 触发
- 展示：提示卡片（触发项 + 建议动作），不误报判据=上述条件全部未命中时不产生提示

## 七、Non-Goals（本期不做的技术事项）

- N1 不做任务派发/编辑接口（只读监督 + 审批 + 指令回执）
- N2 不做聊天/对话界面（不显示沟通过程）
- N3 不做多语言国际化（首版仅中文）
- N4 不做 iOS/Mac/安卓/Windows 原生端（鸿蒙跑通定型后第二阶段同步）
- N5 不做多人协作/账号体系（单 Owner 私有；北极星埋点用本地匿名计数，不引入账号）
- N6 不做端侧大模型推理（小助手走云端 API）
- N7 不直连本地电脑（经 GitHub 桥接）
- N8 **首版不做飞书灾备**（飞书授权 larkOAuth / 文档读取 getLarkDoc / lark_conn 表全部推迟第二阶段，随 iOS/Mac/安卓/Windows 多端同步规划启用；v0.9 基线变更，原"飞书灾备"表述移出首版范围）

## 八、冻结自检清单（全绿才移交工程方法论）

1. 选型有 ADR（ADR-001~004，Status 均 accepted；矩阵可复算）✅
2. 契约五列齐全 + 调用归属/鉴权/外部映射 + 统一错误语义 ✅
3. 依赖列无环（M1-M8 单向递进）✅
4. 高风险项已前置（R4/R5/R6 前置门在 M3/M4/M5）✅
5. Non-Goals 已列（N1-N8）✅
6. 北极星指标有技术承载（5.4：事件/口径/存储/窗口/验收）✅
7. 评分与偏移口径可复算（5.5：公式/金样本/边界）✅
8. 预警阈值可判定（6.4：触发项/边界样例/不误报）✅

## 九、衔接约定

| 关系 | 技能 | 衔接点 |
|---|---|---|
| 下游 | Ultima-工程方法论 | 冻结后拆工单：按 M1-M8 里程碑边界切，禁止执行端自行改架构 |
| 引用 | Ultima-测试管理 | 接口契约表（4.1）直接转化为接口级用例设计输入 |
| 引用 | Ultima-发布管理 | 多端节奏（鸿蒙→iOS/Mac→安卓/Windows）与发布门 |
| 引用 | Ultima-治理体检 | ADR 状态链随方案落盘，体检交叉核对漂移 |
| 引用 | Ultima-执行端调度 | 方案为交接载荷"设计依据"；B 通道执行时方案是唯一授权边界 |
| 对照 | Ultima-架构治理 | 本方案待架构治理评审确认后冻结 |

## 十、修复对照（v0.1 → v0.2 → v0.3）

### v0.1 → v0.2（对应工程审计 GAP-001~012）

| GAP | 修复 |
|---|---|
| GAP-001 P0 北极星无承载 | §5.4 新增技术承载（事件/口径/存储/窗口/验收） |
| GAP-002 P0 矩阵算错 | §2.2 全矩阵复算，保留两位小数，附复算式 |
| GAP-003 P1 硬约束无证据 | §2.1 逐候选证据（许可/兼容/维护） |
| GAP-004 P0 Container 无流向 | §3.2 带流向/协议/外部模型标注 |
| GAP-005 P1 拍板无失败路径 | §3.3 全用例补失败/回执路径 |
| GAP-006 P0 契约不可实施 | §4.1 补调用方/提供方/鉴权/外部映射/载荷位置 |
| GAP-007 P0 版本策略仅 v1 | §4.1 统一版本策略（兼容期/弃用/expand-contract） |
| GAP-008 P0 3NF 不可证 | §5.2 gap_item 独立实体 + 候选键 + 函数依赖说明 |
| GAP-009 P0 无变更标注列 | §5.2 增加"破坏性变更标注"列 + 规则 |
| GAP-010 P1 制式漂移 | §5.3 与磁盘实物同步（0.3.0）+ 明确为快照 |
| GAP-011 P0 R6 未前置 | §6.3 高风险前置门（R4/R5/R6 全挂靠） |
| GAP-012 P2 错误模型过窄 | §4.2 统一错误语义（鉴权/校验/限流/冲突/离线） |

### v0.2 → v0.3（对应复验审计 v2 残余缺口）

| 缺口 | 修复 |
|---|---|
| GAP-003 硬约束不可回溯 | §2.1 补许可证名称/官方来源/兼容版本/维护日期 + 核验日期 |
| GAP-006 契约缺鉴权/载荷/外部映射 | §4.1 补鉴权机制/凭证位置/载荷位置/响应信封/真实外部 API 端点映射 |
| GAP-010 快照仍漂移 | §5.3 与磁盘 0.3.1 全字段一致 + 建立防漂移门 |
| GAP-001 event_log 未入 ER（V2-GAP-001） | §5.2 新增 event_log 实体（PK/字段/函数依赖/保留聚合规则） |
| GAP-012 错误码族不自洽（V2-GAP-002） | §4.2 改码规则 `E_<域><序号>`，全量 15 码逐域枚举 |
| V2-GAP-003 Context 双向歧义 | §3.1 电脑端豆包入图 + 拉取/发布方向分离标注 |

### v0.3 → v0.4（对应终审审计 v3 残余缺口 V3-GAP-001~004 + GAP 复验）

| 缺口 | 修复 |
|---|---|
| GAP-003 硬约束证据不可定位 | §2.1 证据改"来源入口（官方域名/页面）｜关键版本/日期｜核验结论"三段式，删除笼统站点名 |
| GAP-006/V3-GAP-001 契约引入未建模桥接服务 | §4.1 删除"本地桥接服务"，裁定 APP 数据服务层直连 GitHub REST API（适配器），与 §3/N7 一致 |
| V3-GAP-002 GET 用 body | §4.1 `GET /assistant/summary` 改 `POST /assistant/summary`；`GET /assistant/notify` 参数走 query，全局约定"GET 一律不带 body" |
| V3-GAP-003 模型 Key 口径冲突 | §4.1 统一为"模型 API Key 存 APP 本地加密存储（HarmonyOS 安全存储），按通道取用"，删除"环境变量/服务侧"表述 |
| GAP-010 快照仍漂移 | §5.3 与磁盘逐字段一致（version 0.3.2，refs 飞书 URL），防漂移门改机器级 JSON 深比较 |
| V3-GAP-004 公共码数量矛盾 | §4.2 "3 个公共码"修正为"5 个公共码（4901-4905）" |

### v0.4 → v0.5（对应第四次终审 v4 残余缺口）

| 缺口 | 修复 |
|---|---|
| GAP-003 硬约束证据仍不可定位 | §2.1 重写为逐候选结构化证据表（官方页面标题/完整 URL/关键版本或发布日期/核验日/结论 五列×三约束），纠正"Flutter 官方 RC 分支""ArkTS API 12 起主语言"等无官方支撑断言 |
| V4-GAP-001 逻辑契约与原生 HTTP 混写 | §4.1 契约分层：第一列改"逻辑操作（适配器方法）"，提供方=APP GitHub Adapter；新增"GitHub 原生 HTTP 契约"列（method+path+转换要点）；新增 §4.1.1 适配器转换规则（Base64/commit/sha 冲突/状态码映射） |
| V4-GAP-002 notify 调用归属不完整 | §4.1 listNotifications 明确"APP UI/触发器→APP 小助手服务（本地调用，非网络端点）"，不套 Bearer 模型 Key |

### v0.5 → v0.6（对应第五次终审 v5 残余缺口）

| 缺口 | 修复 |
|---|---|
| GAP-003 证据仍含首页/伪 URL、版本列不纯 | §2.1 三约束表 URL 全部具体到页面级（LICENSE 文件/Release Notes/指南页），版本/发布日期列只放可从页面定位的版本号或日期；不适用项（文件 JSON/直连本地）移出外部证据要求并写明理由 |
| V4-GAP-001 原生 path 含 glob + 错误映射不闭合 | §4.1 listWorkOrders/listAudits 改 `GET .../contents/tasks/queue` 列目录 → Adapter 过滤（`.md`/含`audit`）→ 逐文件 GET，glob 不再入原生 URL；§4.1.1 升级为完整 HTTP→错误码映射表（400/401/403/404 分操作/409/422/429/网络不可达/5xx），各端点错误码补齐 E_4902/E_4904 并加机械校验规则 |

### v0.6 → v0.7（对应第六次终审 v6 残余缺口）

| 缺口 | 修复 |
|---|---|
| GAP-003 版本/日期列不纯 + 2 个 404 URL | §2.1 版本/发布日期列只保留可定位版本号/ISO 日期或"—"（许可证名/商业条款/维护判断全部移入结论列）；删除 404 的 HarmonyOS versions 与 OpenHarmony release 两个 URL，维护证据改用已验证 200 的 ArkTS 入门页（Last updated 2025-05-20）/Flutter Release Notes（3.22.0）/RDB 指南页/GitHub Changelog 等 |
| V4-GAP-001 错误映射不闭合 | §4.1.1 新增"端点属性表"（external_http/write/业务码/公共码集合，机械推导规则），端点表错误码与属性表推导双向 0 差异；401/403/429/网络不可达行限定"外部 HTTP 端点（本地端点除外）"；§4.2 公共码适用范围按属性推导，取消"各端点通用"表述 |
| V6-GAP-001 本地 notify 错入推理 5xx | §4.1.1 5xx 行适用操作限定为 requestSummary（E_4201）；listNotifications 本地聚合失败单列本地条件→E_4202，不套 HTTP 条件；listNotifications 错误码改为 E_4202/E_4902 并豁免 E_4901/E_4903/E_4904 |

### v0.7 → v0.8（对应第七次终审 v7 残余缺口）

| 缺口 | 修复 |
|---|---|
| GAP-003 版本列仍含 14 个说明性单元 | §2.1 版本/发布日期列机械纯化：全部改为裸版本号/裸 ISO 日期/两者组合（`10；2025-05-20`、`3.22.0；2024-05-14`、`2025-05-20`）或单个 `—`；"LICENSE 无版本号/页面未标独立版本号/Since API version/Last updated/changelog 条目日期可访问"等说明全部移入结论列 |

### v0.8 → v0.9（工单队列审计 console-queue-audit-report.md 驱动，基线变更）

| 缺口 | 修复 |
|---|---|
| P0-02 飞书灾备接口无人承接 | 飞书授权/文档读取/lark_conn 全部标注**第二阶段（N8）**并移出首版范围：§3.1 流向④、§4.1 契约两行、§4.1.1 端点属性两行、§4.2 码表 E_4301/E_4302、§5.2 lark_conn 表、Non-Goals 新增 N8；同步 REQ-CONSOLE-001（数据链路主通道=GitHub） |
| P0-03 评分口径未定义 | 新增 §5.5 评分与偏移口径：公式（100 基础分按未关闭缺口严重级扣分，P0-10/P1-5/P2-1 上限 5，已处理半扣，下限 0 取整）+ 金样本 5 例 + 偏移判定（基线 ±5）+ 纠正建议来源；同步 REQ 需求要点 6 |
| P0-04 预警阈值未定义 | 新增 §6.4 偏离预警阈值：四项触发（评分降≥5 越线/P0 待处理存在/工单阻塞/执行中超 7 天）+ 时间窗/比较符/缺失数据行为 + 边界样例 6 例 + 不误报判据；同步 REQ 需求要点 8 |
| P0-01/P0-05/P1 系列 | 属工单层修复（m1 schema 字段、Gate 参数化为测试表、m6 契约闭环、风险门执行时点、m7/m8 验收矩阵），由工单修订闭环，非方案结构变更 |

### v0.9 → v0.9.1（Codex 复验 console-queue-audit-report-v2.md 驱动，口径澄清，不改变产品含义）

| 缺口 | 修复 |
|---|---|
| P0-02 残余：Container 图/通用约定飞书残留 | §3.2 Container 图飞书 OpenAPI/OAuth 连接器标注"第二阶段 N8、首版不实现"；流向行"外部三源"改为"外部源（GitHub 主通道+云端模型 API；飞书第二阶段 N8）"；§4.1 通用约定"飞书走 OAuth2（第二阶段 N8，首版不实例化）" |
| P0-04 残余：-5 边界冲突 | Owner 裁定：**评分下降 ≥5 分即触发（含恰好 5 分）**，与 REQ 需求要点 8 一致；§6.4 触发条件/比较符统一为 `score_now - baseline ≤ -5`，边界样例新增 80→75（-5）触发（由 6 例扩为 7 例） |
| P0-05 残余：Gate 三要素 | 属工单层修复：40 个 T 逐条补 Gate 测试表（测试 ID/固定输入/操作/唯一期望/失败条件/证据路径），由工单修订闭环 |

### v0.9.1 → v1.1 设计依据回填（2026-10-18，用户拍板 UI 方案冻结后）

| 变更 | 内容 |
|---|---|
| 设计依据回填 | UX 方案 v0.2（IA/流程/交互基线）+ UI 方案 v0.1（tokens/栅格/冻结验收规则，验收记录 §十）冻结，作为 v1.1 迭代工单的权威设计依据；UI 方案已同步飞书（docx/WwKAdvo65omGYwxVM6Yc0Fo6nGe） |
| 拆工单范围 | v1.1 拆工单按 UI 方案 §十 冻结规则执行（横竖屏两套布局、产品详情三标签整合、悬浮球拖动/呼吸灯/回位、KPI 与评分条动画仅首播、竖屏滑动切标签、全局隐藏滚动条等） |

---
> 方案状态：**v0.9.1 已冻结（架构治理重审通过，复验 v5 全绿 40/40）；8 张开发工单复验通过（待派发）；v1.1 设计依据已回填（UX v0.2 + UI v0.1 冻结，2026-10-18），待按工程方法论拆 v1.1 工单**。
