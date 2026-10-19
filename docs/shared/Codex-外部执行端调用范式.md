# Codex 外部执行端调用范式

> 版本：v1.0 ｜ 状态：批准生效 ｜ 适用范围：Ultima 全系产品（UltimaConsole / UltimaRadar / UltimaGold / UltimaEngine / UltimaAgent / UltimaScan / UltimaSentinel 等所有挂 Ultima 前缀项目）及后续新项目
> 唯一权威源：`H:\UltimaAI\_shared\paradigms\Codex-外部执行端调用范式.md`（镜像：ultima-docs-repo `docs/shared/`）
> 依据：本范式由 2026-10-19 UltimaConsole v1.1-N6 实战（Codex 会话 01a15071）验证后固化。模型/工具链变化时按 §8 维护更新。

---

## 0. 定位与角色分工

| 角色 | 是谁 | 职责 |
|---|---|---|
| 主脑（调度端） | 豆包 | 制定任务、写工单、派发、监控执行顺序/目标/进度/结果、定时审计、验收冻结 |
| 执行端 | Codex（`codex exec` 非交互会话） | 照工单逐 T 执行，每 T 自证 Gate 证据，输出标准化回执 |
| 门禁 | 用户 | 只在立项/方案/发布/大变更门介入，不逐行盯实现 |

铁律：**豆包只监控执行顺序/目标/进度/结果并分派给 Codex，不规划不拆解**；审查与执行分离（开发方不自审）；人只在门禁介入。

---

## 1. 模型版本（2026-10-19 实测可用清单）

| 用途 | 模型名 | 说明 |
|---|---|---|
| 默认主力（主体工程/诊断） | `gpt-5.6-sol` | 本次 N6 排查实际使用，workhorse |
| 架构级/高复杂度 | `gpt-5.6-terra` | 备用升级档 |
| 快速机械任务 | `gpt-reserve` | 低配快速档 |
| 独立评审/批评 | `codex-auto-review` | 自审/生成批评模式 |

硬约束：
- **config.toml 默认模型 `gpt-6.1-sol` 已从账户移除（报 not supported）**，派发必须显式 `-m <模型>`，禁止依赖默认。
- 模型可用性以 `codex models` 实测为准；变更后由主脑更新本表并走范式登记（§8）。

---

## 2. 调用方式（Windows 已验证命令形态）

```powershell
cmd /c "codex.exe exec -m gpt-5.6-sol --dangerously-bypass-approvals-and-sandbox - < tasks\queue\dispatch-<工单号>-prompt.txt"
```

- codex.exe 绝对路径：`C:\Users\Administrator\AppData\Local\Programs\OpenAI\Codex\bin\codex.exe`
- 工作目录：**项目根**（如 `H:\UltimaAI\UltimaConsole`），prompt 文件用相对路径
- 会话模型：`codex exec` 非交互；会话 originator 必须是 `codex_exec`（仅归档工单+同步状态 ≠ 派发，必须真正触发 exec 才算派发）

### 2.1 参数铁律（每条都是踩坑结论）

| 规则 | 说明 |
|---|---|
| `- < 文件` 喂 stdin | 直接命令行传参会被当 stdin 卡死；必须把派发 prompt 写成文件用 `- <` 输入 |
| 显式 `-m` | 默认模型已失效（§1），不传必报 not supported |
| 沙箱 | 本机存在 helper 缺失 / SID 解析失败（`CodexSandboxOffline 1332`）时，配合用户完全访问授权使用 `--dangerously-bypass-approvals-and-sandbox`；有正常沙箱环境的机器不得滥用 |
| 后台执行 | 长任务用 `run_in_background` 挂起，轮询回执，不阻塞主脑 |

### 2.2 派发 prompt 文件（`tasks\queue\dispatch-<工单号>-prompt.txt`）必含内容

1. 扮演声明：`Act as the Ultima coding executor`
2. 工单路径：`tasks/queue/wo-<工单号>.md`
3. 执行顺序：按 T0→Tn 逐条，Gate PASS 再进下一条
4. 证据落盘：每 T 记录 Gate 证据到 `docs/reports/stage-<阶段>.md` + `docs/reports/evidence/<阶段>/`
5. 回执字段：根因结论 / 产出路径 / 验收证据 / 越界声明（无=明确写"无"）
6. 临时文件：执行完由主脑清理（dispatch prompt 不入仓）

---

## 3. 队列方式（工单队列三件套）

| 件 | 路径 | 职责 |
|---|---|---|
| 工单文件 | `tasks/queue/wo-<product>-<阶段>.md` | 三段式工单（模板 `_shared\templates\工单模板.md`），逐 T 可执行 |
| 队列主表 | `tasks/queue/console-queue-index.md` | **唯一权威**：每张工单状态/任务数/前置冻结/验收门/closeout |
| 状态镜像 | `tasks/queue/queue-status.json` | `queue-status-gen.py` 生成：total/frozen/in_progress/blocked/wip |

状态流转：`待派发 → 执行中 → 逐 T 验收 → 已完成（frozen）`

硬约束：
- WIP 上限：**执行中 ≤2 张、审计中 ≤1 张**
- 前置冻结门：未冻结不进下一阶段；`mN-frozen` tag/阶段报告 `docs/reports/stage-mN.md` 缺失=冻结门未闭合
- 队列主表是唯一权威，queue-status.json 只是其镜像，改状态先改主表再重新生成

---

## 4. 派单方式（DoR 就绪门，五项全绿才派）

1. **验收 Gate 可判定**：每条 pass/fail 有固定输入/唯一期望/证据位置
2. **无未决依赖**：前置冻结 tag 存在
3. **写入域已声明**：各 T 精确到文件路径
4. **推理强度已声明**：high 主体工程 / medium 规则 / low 机械
5. **禁止项已写**：每条 T 有明确"禁止"清单

工单三段式细则（防 AI 自行发挥）：**文件**精确到路径 / **写什么**逐条可执行编号 / **验收**封闭清单全绿才过 / **禁止**明确不做什么。

---

## 5. 交接载荷与回执

派发即交接，必须携带：目标端（Codex）/ 工单引用 / 上一步结论与证据指针 / 本端边界清单（允许/禁止）/ 期望输出结构（回执字段）/ 指令 / 验收门。

执行端回执必报字段：

| 字段 | 说明 |
|---|---|
| 链路号/工单号 | 追踪标识 |
| 执行端 | 谁做的 |
| 完成状态 | 已完成 / 阻塞 / 已终止 |
| 根因结论 | 问题根因一句话（诊断类必填） |
| 产出路径 | 改动文件 + 报告 + 证据目录 |
| 验收证据 | 构建/连拍/像素测量/日志输出摘要 |
| 越界声明 | 无=明确写"无"；含未动范围（冻结 UI/未发布/未打 tag） |
| 环境声明 | 模拟器 vs 真机：真机未验证必须写"仅真机预期"，禁止冒充已验证 |

---

## 6. 验收与闭环（监督端=豆包执行）

1. 读阶段报告 `docs/reports/stage-<v>-<n>.md`：Gate 逐条核对（T0-C1/C2、T1-C1/C2、Tn 全 PASS）
2. 核证据目录 `docs/reports/evidence/<阶段>/` 存在且与报告路径一致
3. 冻结：主表状态改 `已完成（<tag>-frozen）` → 重跑 `queue-status-gen.py`
4. commit + push GitHub（修复源码 + 报告 + 证据 + 主表 + queue-status）
5. 三端同步（§7）
6. 验证截图不污染主仓（fab-* 等过程截图不入仓，evidence 正式证据入仓）

---

## 7. 同步通道（队列状态三端一致）

| 端 | 位置 | 方式 |
|---|---|---|
| GitHub 正式仓 | `Ultima-AI-Studio/<product>` | git push（主） |
| Gist | `ArkExlabs/<gist-id>/raw/queue-status.json` | 免 token 公开读取通道（App 读取用） |
| Gitee 镜像 | `Ultima-AI-Studio/ultimaconsole-sync` (master) | `sync-queue.py` 或 git clone+push |
| docs 镜像 | `H:\UltimaAI\ultima-docs-repo` → `Ultima-AI-Studio/ultima-docs` | 公共文档/范式推送 |

已知缺陷（sync-queue.py，未修）：Gitee contents GET 遇空 list 崩溃、文件不存在需 POST 创建（PUT 强制 sha）、token 须放 query。**Gitee 首建/异常时备用通道 = git clone + push（已验证可用）**。
凭证规则：token 不写入范式/工单/仓库明文，存本机环境变量或 git 凭据管理器。

---

## 8. 故障预案（全部为本次实测处置）

| 故障现象 | 处置 |
|---|---|
| `model not supported`（默认模型失效） | 查可用模型 → 显式 `-m gpt-5.6-sol` |
| helper `codex-windows-sandbox-setup.exe` program not found | 补 PATH；仍失败走 bypass（见下） |
| `CodexSandboxOffline: 1332`（SID 解析失败） | 用户完全访问授权下 `--dangerously-bypass-approvals-and-sandbox` |
| 参数未传入卡 stdin | `- < dispatch-<id>-prompt.txt` 喂文件 |
| 长时间无回执 | 先确认是否真正触发 exec（会话 originator=codex_exec）；只归档+同步≠派发 |
| 执行端报"无法处理" | 升级回主脑（一次一主），不自行换路 |

---

## 9. 维护与登记

- 本范式为跨项目硬约束；模型清单、命令形态、故障预案变更必须经主脑更新并在此登记，旧版归档只读。
- 登记入口：`H:\UltimaAI\_shared\paradigms\Ultima-范式存档总纲.md`（本范式已登记）。
- 同步：本地权威（`_shared\paradigms\`）→ docs 镜像（ultima-docs-repo `docs/shared/`）→ GitHub。
- 每个挂 Ultima 前缀的项目每次派 Codex 都必须符合本范式；项目级差异只能加约束，不能删减。
