# UltimaAI 能力注册表（Registry）

> 强制机制 M1：立项/开发前必查本表，防重复开发。未登记的能力/组件不得使用。
> 新增能力/产品必须先登记（M1）。登记规则见 `Ultima-工程方法论` §6。

## 〇、全局资源导航（2026-10-20 定版）

| 资源 | 位置 | 说明 |
|---|---|---|
| 范式权威源 | `H:\UltimaAI\_shared\paradigms\` | UI 样式 / Codex 调用 / 全局根目录 / 存档总纲 |
| 品牌资产 | `H:\UltimaAI\_shared\brand\` | 主 logo（astronaut.png）/ 组合规范 / showcase |
| 模板 | `H:\UltimaAI\_shared\templates\` | 工单 / 审计 / 报告 / **项目引导索引** |
| 全局队列主表 | `H:\UltimaAI\_shared\queue\global-queue-index.md` | 全项目派单登记 + 看门狗巡检 |
| 各项目入口 | `<产品>\docs\INDEX.md` | **项目引导索引（必读，派单首段强制引用）** |
| GitHub | 组织 `Ultima-AI-Studio`：`UltimaDocs`（全局文档库）+ 各项目同名仓库 | 根路径只允许项目同名仓库，备份落内部子路径（§5.1） |
| VPS | `161.33.167.206`（一核1G·Radar 在用）｜ `198.13.46.208`（四核4G·未启用） | 域名 `namechatai.space` |
| 飞书 | 范式 docx（全局根目录 v2 等） | 三层数据备份层，经 `C:\Users\Administrator\Doubao\lark-sync\` 中转 |

## 一、产品注册

| 产品 | 目录 | 定位 | 通道 | 状态 |
|---|---|---|---|---|
| UltimaAgent | H:\UltimaAI\UltimaAgent | AI 代理体系（Tuppo Agent 逻辑等） | A/B | 开发中 |
| UltimaEngine | H:\UltimaAI\UltimaEngine | 游戏引擎（原 MirServer M2 Code，含 Game 端） | A | 开发中 |
| UltimaGold | H:\UltimaAI\UltimaGold | XAUUSD 黄金推送（原 TuppoAU） | A | 开发中 |
| UltimaRadar | H:\UltimaAI\UltimaRadar | Solana 聪明钱监控 | B | 开发中 |
| UltimaScan | H:\UltimaAI\UltimaScan | 加密项目全量归档+多维打标（永不剔除，标签表达风险） | A | 开发中（2026-10-19 补登） |
| UltimaSentinel | H:\UltimaAI\UltimaSentinel | 智能合约+网站应用双域全 AI 自动审计（Scan→Audit 闭环） | A | 开发中（阶段0已冻结，原定名 UltimaAudit） |
| UltimaConsole | H:\UltimaAI\UltimaConsole | 全产品监督仪表盘（鸿蒙 Pad，只监督不派发） | A | **v1.0.0 鸿蒙首版已发布（M1-M8 全部冻结）** |
| UltimaOps（规划） | （待立项） | 运营管理产品：多平台账号配置 + 多账号管理 + 内容分发 + 数据回传（渠道运营技能的能力层载体） | A | 沟通规划中 |

## 二、技能注册（23 技能）

| 技能 | 职责 | 触发 |
|---|---|---|
| Ultima-产品经理 | 顶层统帅：阶段判断/技能统筹/决策把关/多产品组合 | 判断走哪步/统筹多技能/跨产品分精力 |
| Ultima-产品工作流 | 全流程主干/问卷/管理语言 | 推进/策划产品 |
| Ultima-需求管理 | 需求池/优先级/变更/追溯 | 记需求/定优先级/变更 |
| Ultima-产品策划 | 想法→策划方案（画像/竞品/MVP/指标） | 做产品策划/定MVP/成功指标 |
| Ultima-UX设计 | 策划→UX 方案（IA/流程/交互/可用性/无障碍/验收门；UX 资源库=交互模式/方法论） | 设计信息架构/画流程/定交互/可用性与无障碍/UX 验收 |
| Ultima-UI设计 | UX→UI 视觉方案（tokens/组件/栅格/设计系统/素材；UI 资源库=图片/图标/字体/范本） | 定视觉规范/选配色字体/组件外观/选素材图标/UI 验收 |
| Ultima-技术落地方案 | 策划→技术方案（选型/架构/接口/推进规划） | 技术选型/画架构/定接口 |
| Ultima-架构治理 | 架构评审/ADR/技术债/演进 | 评审方案/记ADR/管技术债 |
| Ultima-网络安全 | 安全设计/密钥/漏洞/合规门 | 安全设计/密钥管理/合规 |
| Ultima-数据架构 | 数据建模/存储/质量/备份 | 数据建模/存储选型/备份 |
| Ultima-性能工程 | 性能基线/基准/优化/容量 | 性能基线/压测/优化 |
| Ultima-AI工程 | 模型选型/Prompt/Agent编排/评测 | 选模型/写Prompt/评测AI |
| Ultima-工程效能 | CI/CD/构建/部署/监控 | 搭流水线/构建/监控 |
| Ultima-执行端调度 | 派活/编排/审批门/交接 | 派任务/编排多端 |
| Ultima-工程方法论 | 工单/DoD/冻结门/治理 | 拆任务/开工单/防膨胀 |
| Ultima-测试管理 | 用例/派发/缺陷/质量门 | 定测试/管缺陷/验收 |
| Ultima-治理体检 | 查缺补漏/根目录合规 | 体检/审计/查缺 |
| Ultima-发布管理 | 版本/灰度/回滚/多端 | 规划版本/发布/回滚 |
| Ultima-运营内容 | 画像/卖点/定价/物料（策略层） | 写介绍/定价/运营策略 |
| Ultima-文案写作 | 各平台文案成品（执行层） | 写社媒文案/落地页/公告 |
| Ultima-用户运营 | 用户分层/社群/反馈闭环 | 收集反馈/运营内测群 |
| Ultima-增长实验 | AARRR/AB测试/激活留存 | 验证假设/AB测试/漏斗 |
| Ultima-渠道运营 | 平台矩阵/分发/账号管理（方法论层） | 定分发计划/发布SOP/渠道数据 |

## 三、已登记能力（组件/模块）

（随开发登记，防重复开发）

## 四、待办工单（任务队列登记）

| 工单 | 产品 | 位置 | 状态 |
|---|---|---|---|
| wo-skill21-recheck（21 技能体系复检审计） | UltimaConsole（体系级） | `H:\UltimaAI\UltimaConsole\tasks\queue\wo-skill21-recheck.md` | 已完成，报告产出（3 个 P1 缺口，已闭环） |
| wo-skill21-fix-naming（21 技能命名漂移修复） | UltimaConsole（体系级） | `H:\UltimaAI\UltimaConsole\tasks\queue\wo-skill21-fix-naming.md` | 已完成，4 文件修复 + 复验全绿 |
| wo-console-prd-audit（Ultima Console 产品策划方案审计） | UltimaConsole | `H:\UltimaAI\UltimaConsole\tasks\queue\wo-console-prd-audit.md` | 已完成，有条件 PASS（1 个 P1 已修复，可冻结） |
| wo-console-tech-audit（Ultima Console 工程方案审计） | UltimaConsole | `H:\UltimaAI\UltimaConsole\tasks\queue\wo-console-tech-audit.md` | 已 8 轮：首审不 PASS（12 缺口已修）→ 复验不 PASS（6 残余已修）→ 终审不 PASS（V3 残余已修）→ 第 4 轮不 PASS（V4 残余已修）→ 第 5 轮不 PASS（GAP-003/V4-GAP-001 已修）→ 第 6 轮不 PASS（V4/V6 已修，GAP-003 残余）→ 第 7 轮不 PASS（GAP-003 版本列已机械纯化）→ **第 8 轮 PASS（v0.8 全 Gate 通过）**；架构治理评审（A 通道）通过，**技术方案 v0.8 已冻结**；开发工单队列已建（wo-console-m1~m8）+ 看门狗定时任务已启动（每天 10:30） |
| wo-console-queue-audit（Ultima Console 工单队列审计+复验） | UltimaConsole | `H:\UltimaAI\UltimaConsole\tasks\queue\console-queue-audit-report.md`~`-v5.md` | 复验 v5「P0/P1 清零可派发」（40/40 PASS）；技术方案 v0.9.1 冻结。**开发执行：M1-M8 全部冻结交付（m1-frozen~m8-frozen）**——M1 数据链路（真实私库拉取/校验/RDB 快照/离线降级）、M2 仪表盘容器、M3 产品钻取、M4 审计与评分、M5 双通道与预警、M6 审批流与小助手、M7 旋转布局（横竖屏矩阵）、M8 验收与发布；自动化回归 **113/113 PASS**；签名发布包 entry-default-signed.hap（SHA-256 7950DBA9…）；**v1.0.0 已发布**（tag v1.0.0 = 5c7df7f）；北极星 4 周数据=发布后监督项（看门狗复核）。第二阶段：iOS/Mac/安卓/Windows 多端 + 飞书灾备（N8） |
