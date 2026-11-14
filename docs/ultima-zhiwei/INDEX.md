# UltimaZhiWei（知微｜银发AI守护）项目引导索引（INDEX）

> **本文件是 UltimaZhiWei 的执行入口**：任何开发 / 审计 / 同步动作前，先读本文件定位权威源，再读对应范式，最后动手。
> 版本：2026-11-14 ｜ 制式：Ultima AI 项目引导索引（由 `_shared\templates\项目引导索引模板.md` 生成）
> 产品目录：`H:\UltimaAI\UltimaZhiWei`（根目录范式 v1.0 合规：Ultima 开头 + 七目录骨架）

> 2026-11-14 状态签注（立项）：**V1.0 产品方案已落盘，开发未启动、未派发任何工单**。方案权威源 `docs/plans/UltimaZhiWei-产品方案-v1.0-20261114.md`（编号 ZHIWEI-PLAN-001，状态 DRAFT_OWNER_REVIEW）。技术方案 / UX-UI 方案 / Sentinel 规则库接口契约 / 上架合规清单 / 工单拆分五项待补齐（见方案附录 A），按 G-PLAN-001 补齐前不得派发工单。产品已登记 `_shared/registry.md` §一 产品注册（M1）。

> 2026-11-14 状态签注（边界冻结 · ZHIWEI-DEC-001）：**本轮仅立项，处于立项冻结态**。GitHub 项目远端仓库与推送、飞书备份、云端出口机分配、Sentinel 规则库接口契约、技术方案编制、工单拆单**全部暂不做**（Owner 有需求时另下指令）；下一道门 = **Owner 指定的其他大模型做一轮方案审计**，结论回来前不进入技术方案。**无障碍权限已确认为 V1.0 必做项**（页面文本识别在不上传原文、不 root、不截屏前提下唯一可行通道）；同步登记审核口径红线：对外一律写「适老化辅助阅读」，禁用「监控屏幕 / 读取他人内容」类表述，Google Play 不沿用国内口径；形态（可选授权 + 无授权降级）与渠道范围待 Owner 拍板 D1-D3。详见 `docs/references/决-2026-11-14-立项边界与无障碍权限专项.md`。

## 0. 三条铁律

1. **先读本 INDEX → 再读权威范式 → 再动手**（Codex 派单 prompt 首段强制引用本文件）
2. **权威源只有一份**：本地 `H:\UltimaAI\_shared\`（唯一权威）｜ GitHub `Ultima-AI-Studio/UltimaDocs`（云端镜像）｜ 飞书（备份）。项目 `docs\shared\` 只是同步副本，改内容一律改 `_shared` 权威源再同步，禁止在副本上直接改。
3. **各项目自主推进开发，直接调用 Codex，遵守规范队列标准**：派发前先登记全局主表，禁止绕过规范裸跑（G-DISPATCH-001 自主推进版，2026-10-28 Owner 拍板）。

## 1. 权威源地图

| 内容 | 本地权威 | 云端镜像 |
|---|---|---|
| 范式（UI / Codex / 全局根目录 / 存档总纲） | `H:\UltimaAI\_shared\paradigms\` | GitHub UltimaDocs `docs/shared/paradigms/` |
| 品牌资产（logo / 图标 / 组合规范） | `H:\UltimaAI\_shared\brand\` | GitHub UltimaDocs `docs/shared/brand/` |
| 模板（工单 / 审计 / 报告 / 项目引导索引） | `H:\UltimaAI\_shared\templates\` | GitHub UltimaDocs `docs/shared/templates/` |
| 全局队列主表 | `H:\UltimaAI\_shared\queue\global-queue-index.md` | 本地权威（不镜像） |
| **本产品方案（唯一权威）** | `docs\plans\UltimaZhiWei-产品方案-v1.0-20261114.md` | UltimaDocs 镜像（待同步） |

## 2. 本项目必读规范（按序，缺一不可）

1. `docs\INDEX.md`（本文件）
2. **`docs\plans\UltimaZhiWei-产品方案-v1.0-20261114.md`（ZHIWEI-PLAN-001）** —— 产品边界、八条设计原则、V1.0 功能范围、产品局限、合规口径的唯一依据；任何实现与之冲突以本方案为准（变更须走 Owner 评审）
   - 本轮边界与暂停项、无障碍权限专项：`docs\references\决-2026-11-14-立项边界与无障碍权限专项.md`（ZHIWEI-DEC-001）
3. `H:\UltimaAI\_shared\paradigms\UltimaAI-任务工作流范式.md` —— G-TASKFLOW-001：登记 → 计划评审 → 执行 → 复核 → 有界修复 → 验收 → 冻结
4. `H:\UltimaAI\_shared\paradigms\Codex-外部执行端调用范式.md` —— 派单 / 回执 / WIP / DoR
5. `H:\UltimaAI\_shared\paradigms\UltimaAI-全局根目录范式-方案.md` —— 目录骨架 / 三层数据 / GitHub 桥接
6. `H:\UltimaAI\_shared\paradigms\Ultima-UI样式范式.md` —— 涉及界面 / 图标 / 卡片时必须读
7. `H:\UltimaAI\_shared\paradigms\UltimaAI-全局工单命名标准.md` —— G-WO-NAME-001（新单 `wo-ultimazhiwei-<YYYYMMDD>-<NNNN>`）
8. 跨产品依赖：`H:\UltimaAI\UltimaSentinel\docs\INDEX.md` —— 风险规则库 / 反诈知识库生产方（**只读依赖，不在本项目写域内**）

## 3. GitHub 与三层同步

- **组织**：`Ultima-AI-Studio`（**根路径只允许与项目同名的仓库**；备份等放同名仓库内部子路径）
- **全局文档库**：`UltimaDocs` → https://github.com/Ultima-AI-Studio/UltimaDocs
- **本项目仓库**：本地 Git 已建（2026-11-14 首次提交 + tag `zhiwei-plan-v1.0-20261114`）；**远端 `Ultima-AI-Studio/UltimaZhiWei` 未创建、未推送** —— Owner 2026-11-14 明确暂不做（ZHIWEI-DEC-001）
- **三层链路**：本地权威（`_shared\` + 产品目录）→ 复制 `ultima-docs-repo\docs\ultima-zhiwei\` → commit/push UltimaDocs → 飞书导入备份（**飞书层本轮暂不做**，同上）
- **认证**：Git Credential Manager + PAT（禁硬编码 token，凭证入加密 vault）
- **失效排查**：401=PAT 失效；`Repository not found`=仓库不存在或无权（用 GitHub MCP 创建后续推）；网络=保留 commit 续推

## 4. VPS 资产台账

> **唯一权威**：`H:\UltimaAI\_shared\server-assets.md`（全系共享：§一服务器清单 / §二工具链 / §三安全基线 / §四密钥台账 / §五凭证管理；变更只改该文件）。

| IP | 本项目用途 |
|---|---|
| 暂无分配 | Owner 2026-11-14 明确：**云端出口机本轮暂不做**，有需求时另行指定；V1.0 云端 AI 研判与规则下发实际需要一台出口机，进技术方案阶段再定。**候选资产（已实测存在）**：阿里云主账号名下唯一 ECS —— 深圳 `cn-shenzhen` / 实例 `i-wz97a4ek6qb2o6cfytxh` / `ecs.e-c1m1.large` 2 核 2G / Ubuntu 26.04 / 公网 `47.106.12.198` / 3Mbps / 包年包月到期 2027-09-30。详见 `_shared\server-assets.md` §七 |

**凭证管理（强制）**：API key / Token / 服务器凭证**不写入本项目任何文件**，集中存于主脑加密 vault（`H:\UltimaAI\_shared\vault\`，DPAPI 加密，**禁入 git / 云盘 / 飞书 / 聊天**）；需用时向主脑申请，`vault.ps1 get <名称>` 解密取用，用后即弃。

## 5. 全局调度与监察

- **全局主表**：`_shared\queue\global-queue-index.md`（所有项目派 Codex 必须登记一行：项目/工单/状态/冻结门/回执）
- **派单模型（强制）**：一单一进程——一张工单 = 一次 `codex exec` = 一个独立进程/会话
- **WIP 双层（强制）**：每项目执行中 ≤1 + 全项目执行进程 ≤3；审计中 ≤1
- **看门狗**：定时巡检全局主表，发现阻塞 / 越界 / 回执缺失 / 冻结门未闭合即上报
- **本产品队列**：`tasks\queue\index.md`（**当前无工单**；本轮立项冻结，不拆单；解冻条件 = 外部大模型方案审计通过 + Owner 放行技术方案阶段）
- **新请求引导门**：本项目工单范式引用已核验（本条 §2/§5/§6 与方案已落盘）；**准入状态=待外部大模型方案审计通过**，未通过前不引导到工单队列

## 6. 本产品状态速览

**一句话**：面向国内安卓老年机用户的陪伴式云端 AI 反诈风险解读工具，公益免费、无商业变现；只讲清风险、不替老人做决定。

### 定位与边界（继承自 ZHIWEI-PLAN-001）

- **独立 C 端产品**，不属于 Ultima Sentinel；Sentinel 只负责生产 / 评审 / 迭代风险规则库与反诈知识库，经远端策略托管无感下发。
- **反主流路线**：不做拦截 / 拉黑 / 强制退出 / 替用户决策；只做识别 + 解释 + 温和提示。
- **双引擎**：本地规则引擎兜底（断网可用）+ 云端 AI 语义研判（识别谐音、拆字、分段等变种话术）；手机端**零 LLM**，包体与内存优先。
- **隐私最小化**：日志仅存本机、仅存结构化摘要；云端研判必须老人手动点击触发，仅上传脱敏摘要。
- **监护人模块默认关闭**，开启须老人本人授权，可随时一键关闭，监护人只能看结构化日志。

### V1.0 功能范围（内置能力，方案 §六）

1. 实时风险识别与陪伴解读：页面文本扫描 + 全局大字卡片（继续浏览 / 我要退出 / 【让AI帮我看一看】）+ TTS 朗读
2. 剪贴板链接自动识别（钓鱼 / 高危链接）
3. 风险话术分层解读：规则基础版（离线）/ AI 增强版（家属可切换为固定文案模式，关闭 AI 后完全离线可用）
4. 云端 AI 反诈套件：变种话术语义研判 / 反诈语音问答（RAG）/ 话术润色（断网则入口置灰）
5. 设置中心：语音、提醒强度、监护人授权、白名单
6. 本地风险日志（默认不上传）

### V1.0 明确不做（范围外）

来电与通话识别、APP 本地安全扫描、自动线索上报与社区协同、官方认证申报、任何商业变现 —— 前两项留 V2；后三项仅预留架构接口、默认不打包。

### 当前进度

| 项 | 状态 |
|---|---|
| 产品方案 V1.0 | ✅ 已落盘（ZHIWEI-PLAN-001，待 Owner 评审） |
| 产品登记（M1） | ✅ `_shared/registry.md` §一 |
| 根索引入口 | ✅ `H:\UltimaAI\INDEX.md` 项目入口表 |
| **方案审计（外部大模型）** | ⏳ 待 Owner 指定执行 —— 立项冻结门，未过不进技术方案 |
| 无障碍权限 | ✅ 定为 V1.0 必做项（审核口径 + 信任对策见 ZHIWEI-DEC-001 §二）；形态待拍板 D1 |
| 技术落地方案 | ⏸ 本轮暂停（ZHIWEI-DEC-001） |
| UX / UI 方案 | ⏸ 本轮暂停 |
| Sentinel 规则库接口契约 | ⏸ 本轮暂停（跨产品边界，进技术方案阶段再谈） |
| 上架合规清单 | ⏸ 本轮暂停（无障碍上架材料清单已在 ZHIWEI-DEC-001 §二.5 预立） |
| 工单拆分与派发 | ⏸ 本轮暂停（队列保持为空） |
| GitHub 远端仓库 / 飞书备份 / 云端出口机 | ⏸ 本轮暂停，等 Owner 指令 |

---

**对齐方式**：本 INDEX 由主脑统一维护；内容变更走 `_shared` 权威源 + 三层同步，项目无需自行改动。

## G-SESSION-001 会话翻篇（全局规则，2026-11-01）

长会话按「及时落盘 → 上下文翻篇 → 新窗口接力」执行：可迁移状态落盘到权威源，主线到干净验收点后开新窗口，新窗口首轮按最小读取恢复（根 INDEX → 项目 INDEX → 目标文档），禁止贪读。细则见 `_shared/paradigms/UltimaAI-会话落盘与上下文翻篇范式.md`。
