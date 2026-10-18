# Watchdog 管理复盘：Top Agent 三代看门狗的经验提炼

- **版本**：v1.1 · 2026-10-16
- **性质**：复盘报告（`docs/reports/`）——基于 Top Agent 实际看门狗代码/日志/运行痕迹的逆向复盘（看门狗已按 Owner 拍板于 2026-10-16 清除，脚本归档于 `C:\Guixu\tools\tuppo-loop\.watchdog-disabled-20261016\`）
- **依据**：s3-watchdog.py / s3-watchdog-guard.py / watchdog-light.py / watchdog_runtime.py / watchdog_recovery.py / watchdog-3060.ps1 / observer-watchdog-v1（README+规则表）/ watchdog.log / watchdog-light.log / guard 锁与心跳文件
- **口径**：事实（代码/日志可追溯）、经验（从事实提炼）、Ultima 落点（建议）

---

## 一、三代演进（每次换代解决了什么问题）

| 代 | 载体 | 时间 | 职责与机制 | 换代的动因 |
|---|---|---|---|---|
| 第 0 代 | `watchdog-3060.ps1` | 2026-08 前 | 每 5 分钟查 Ollama 端口 + follower brain loop 进程，**谁挂了直接重启谁** | 最早期的"进程保活"，有控制权 |
| 第 1 代 | `observer-watchdog-v1` | 2026-08 | **只读观察**：`CONTROL_PLANE_WRITE_ACCESS=0`，只读心跳/DEVDBG snapshot，分级提示（WARNING/CRITICAL/STALL），读证据失败不判 Host 失败 | 第 0 代盲重启吃过亏 → 观察与控制分离 |
| 第 2 代 | `s3-watchdog.py` + `s3-watchdog-guard.py` + `watchdog-light.py` | 2026-10 | 任务库状态机守护：完成检测 PASS/FAIL/UNCLEAR 三态、失败修正（≤2 重试）、一次一主派发、心跳+guard 双保活、僵尸回收、过期锁清理 | 从"守护进程"升级为"守护任务状态机" |

**关键转折**：看门狗的职责从"保活服务进程"（第 0 代）→"观察不控制"（第 1 代）→"守护任务状态机 + 只读审计 + 受控派发"（第 2 代）。**看门狗逐渐失去了对产品进程的生杀权，只拥有对任务库状态的回写权。**

---

## 二、经验提炼（每条 = 代码/日志里可追溯的教训）

### A. 能力边界（最重要）

| # | 经验 | 代码/日志依据 | Ultima 落点建议 |
|---|---|---|---|
| A1 | **观察与控制分离**：监控工具默认无控制权，只有明确授权才回写 | observer-v1 明确 `CONTROL_PLANE_WRITE_ACCESS=0`，只产生提示不产生权威状态 | 调度器/监控器只回写任务库状态，**永不直接启停宿主/Brain/产品进程**（Ultima governance 已含 M2 写入域约束，补"进程控制权"维度） |
| A2 | **盲重启 = 二次事故**：不知道"为什么挂"就重启，挂起缺陷未修时重启只会再卡死 | 第 0 代直接 Start-Process 重启 ollama/loop；B5 daemon probe 挂起缺陷 → "重启只会再卡死"纪律（ops-selfcheck） | ops-selfcheck 已有"B5 类缺陷未修复前不重启 daemon"；扩展为通用规则：**重启前必须有根因判断** |

### B. 判定与门控（防误判是自动系统的第一美德）

| # | 经验 | 代码/日志依据 | Ultima 落点建议 |
|---|---|---|---|
| B1 | **证据门控（fail-closed）**：只处理证据明确的 PASS/FAIL，证据不足一律 BLOCKED 留主脑审计——宁可慢，不可错 | s3-watchdog 头部注释："只处理证据明确的 PASS/FAIL，证据不足一律标 BLOCKED 留待主脑审计，防止误判" | 已固化：acceptance-spec §6.1 完成三件套（I1）；再加一条"判定侧 fail-closed"原则 |
| B2 | **失败未修正不推进（串行闸门）**：存在 FAILED/BLOCKED 且无 ~rN 修正排队/完成 → 不派后续任务 | watchdog-light `has_unfixed_failed()` | project-flow 门禁已含重试 ≤2；补"串行闸门"到调度规则 |
| B3 | **人工熔断开关（kill switch）**：`.pause-dispatch` 文件存在 → 只读审计、不修正、不派发 | watchdog-light `PAUSE_FILE` 分支 | 保留为 Ultima 调度器的标准能力：暂停文件 = 治理冻结开关 |

### C. 自保与可靠性（看门狗自己也会挂、也会误判）

| # | 经验 | 代码/日志依据 | Ultima 落点建议 |
|---|---|---|---|
| C1 | **心跳 + guard 双保活**：主看门狗写心跳 JSON（ts/pid），guard 每轮查心跳（<600s 新鲜则不干预，过期则杀旧进程重启）；guard 自身用单实例锁防多开 | s3-watchdog-guard.py + `.watchdog-heartbeat` | 守护者需要被守护：任何常驻调度器配心跳 + 独立保活者 + 单实例锁 |
| C2 | **单实例锁（防多开）**：用 `msvcrt.locking(LK_NBLCK)` 文件锁实现 OS 级单实例，锁文件持久化 | watchdog_runtime `acquire_instance()` | 调度器/监控器必须单实例；多开 = 重复派发/重复修正 |
| C3 | **幂等防重派（三重判定）**：派发进程在跑 / codex 会话在跑 / 有活跃 run → 本轮不派发；**fail-safe：探测失败按"忙"处理，宁可不派也不重派** | watchdog-light `dispatch_alive()/codex_alive()/active_runs()` | 派发唯一性原则：一次一主 + 探测失败默认阻塞（Ultima project-flow 已含"一次一主"） |
| C4 | **进程识别防误判**：用 `CommandLineToArgvW` 解析命令行识别"干活会话"（codex exec/resume、dispatch-task.py），**明确排除常驻服务**（codex-windows-sandbox-ser 永远在跑 ≠ 在干活） | watchdog_runtime `is_development_process()` 注释 | 进程探测必须区分"常驻服务"与"干活会话"，否则误判导致不派发或误回收 |
| C5 | **僵尸任务回收有保护**：EXECUTING 且 run 日志 ≥30 分钟无更新才转 FAILED，**且必须先确认无任何 codex 会话在跑**（孤儿会话可能还在干活） | watchdog-light `stale_executing_to_failed()` | 状态迁移前先确认进程真实消失，再动状态 |

### D. 状态迁移与可观测性（动库的纪律）

| # | 经验 | 代码/日志依据 | Ultima 落点建议 |
|---|---|---|---|
| D1 | **状态迁移 fail-closed 双确认**：超时恢复前先确认执行器空闲（running() 检查两次）+ 任务库字节未变（变了即放弃），恢复前先归档旧状态与日志到 `stale-recovery/<时间戳>/` | watchdog_recovery.py `recover_stale()` | 自动改任务库状态 = 危险动作：先存档、再双确认、才动库（Ultima governance M5 配套） |
| D2 | **锁会残留，要清过期锁**：dispatch 锁持锁 pid 不活跃或超 3600s → guard 清理，否则永久卡死 | s3-watchdog-guard.py 第 2 步 | 所有锁带过期回收策略；锁文件是故障源之一 |
| D3 | **日志纪律**：每轮一行（ts/动作/结果），只增不弹窗；心跳 JSON 化（ts/pid） | watchdog-light `log()`、s3-watchdog `heartbeat()` | 自动系统可观测性 = 日志完整性与心跳可探活 |

### E. 演进元经验（看得最远的一条）

| # | 经验 | 依据 | Ultima 落点建议 |
|---|---|---|---|
| E1 | **自动化只做"确定性收口"，不确定性留给人工**：watchdog 处理证据明确的 PASS/FAIL；UNCLEAR/BLOCKED 一律留主脑 cron 审计——自动与人工的分工边界就是"证据是否明确" | s3-watchdog 三态判定 + 与主脑 cron 并存 | Ultima 审计体系分层固化：机器闸判确定性、主脑判不确定性、Owner 判方向性 |

---

## 三、对 Ultima Agent 的落地建议（新增待固化项）

1. **调度器能力边界**（A1）：补进 governance——调度器/监控器只回写任务库，不得启停产品进程（当前已删除看门狗，Ultima 重建设计按此边界）。
2. **重启根因门**（A2）：ops-selfcheck 通用规则——任何服务重启前必须附根因判断，无根因不重启。
3. **判定 fail-closed**（B1）：acceptance-spec 补"证据不明确 → 不判 PASS，留主脑"。
4. **串行闸门**（B2）：project-flow 补"存在未修正失败任务 → 不派后续"。
5. **暂停开关**（B3）：调度器标配 `.pause-dispatch` 等价物。
6. **单实例 + 心跳 + guard**（C1/C2）：常驻调度器标配三件套。
7. **进程识别规范**（C4）：探测脚本必须区分常驻服务与干活会话，附排除清单。
8. **状态迁移三纪律**（D1/D2）：先存档、双确认、清过期锁。
9. **全程无窗口纪律**（F1，2026-10-16 补充）**已固化** → ops-selfcheck §3（MUST）：派发/看门狗/探活链路所有子进程强制 `CREATE_NO_WINDOW` / `pythonw` / `-WindowStyle Hidden`；禁止裸 `cmd /c`、裸 `os.system`。审计时抽查全部启动点（含计划任务 Action），发现弹窗启动点即生成修正任务。

---

## 四、一句话总结

**看门狗管理的核心经验是"克制"**：能力上不碰产品进程（A1/A2）、判定上证据不明不拍板（B1）、派发上宁漏不重（C3）、动库上先存档再双确认（D1）——**自动系统最大的风险不是"没干活"，而是"瞎干活"**。另有一条硬纪律（F1）：**后台执行全程静默，用户桌面上不允许出现任何控制台窗口**。

---

## 变更日志

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-16 | 初版：三代演进复盘 + A/B/C/D/E 五组 15 条经验 + Ultima 落地建议 8 项 |
| v1.1 | 2026-10-16 | 新增 F1 全程无窗口纪律（已固化 ops-selfcheck §3）；落地建议扩至 9 项 |
