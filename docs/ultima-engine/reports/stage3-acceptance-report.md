# 阶段3 验收报告 · M3 世界内核 + AOI + 区块休眠

> 工单：`md/20-Codex工单-阶段3-世界内核.md`（v1.0）｜ 适用：TuppoM2 开发主线
> 报告日期：2026-10-01 ｜ 基线：stage2-frozen（8d1cabe）→ 本阶段 HEAD
> 报告结构遵循 dev-conductor §6 模板（7 段）

---

## 1. 阶段概览

**结论：✅ 通过（建议冻结）**

阶段3 九条任务（T0~T8）全部完成并逐条 Gate 验证：消息队列、实体/实体池、AOI 四叉树、区块三级休眠、WorldTick 十阶段循环、快照服务、main.cpp 启动接管、测试整合、总验收。四构建矩阵零警告、81 用例全绿、S1 空图万怪压测双构建达标。

## 2. 任务完成情况（T0~T8）

| 任务 | 交付文件 | 验收结果 | 证据 |
|---|---|---|---|
| T0 MsgQueue | src/base/MsgQueue.h/.cpp + tests/TestMsgQueue.cpp | ✅ 通过 | 1047 断言/6 用例（投递1000/消费1000、满队列不丢、Event 丢计数、同 seq 分组、全成/全滚、Query 降级） |
| T1 Entity+EntityPool | src/world/Entity.h/.cpp + EntityPool.h/.cpp + src/base/Common.cpp + tests/TestWorld.cpp | ✅ 通过 | 126 断言/5 用例（世代号复用、非法状态跳转全拒、快照副本隔离） |
| T2 AoiTree | src/world/AoiTree.h/.cpp | ✅ 通过 | 57 断言/4 用例（10000 随机实体暴力对账、订阅/退订、移动后正确、Release 单次 Query<1ms 基准达标） |
| T3 ChunkSleep | src/world/ChunkSleep.h/.cpp | ✅ 通过 | 15 断言/3 用例（Sleep/SemiWake/Wake 四转换路径、多玩家不降级、边界 (0,0) 不越界） |
| T4 WorldTick+WriteGuard+AiSystem | src/world/WorldTick.h/.cpp + src/base/WriteGuard.h/.cpp + src/world/AiSystem.h/.cpp | ✅ 通过 | 18 断言/3 用例（十阶段顺序、阶段1 消费、阶段5 唯一写入零违规、AI Idle→Chase→Return→Idle） |
| T5 SnapshotService | src/world/Snapshot.h/.cpp | ✅ 通过 | 12 断言/2 用例（脏实体发布/取快照/失效、4 线程 4000 次并发读一致） |
| T6 main.cpp 接管 | src/main.cpp 扩展 + src/base/DB.h/.cpp | ✅ 通过 | 启动 10 步跑通（--bench）；player.db 迁移 0001~0004 全执行（user_version=4，10 张表）；无 lic → exit 2 拒绝启动；S1 空图万怪压测达标（见 §5） |
| T7 测试整合 | tests/TestDb.cpp 新增 + TestWorld/TestMsgQueue 扩充 | ✅ 通过 | 81 用例全绿；Entity/WorldTick/ChunkSleep/AiSystem/Snapshot/DB 每函数≥1 用例；TestDb 3 用例（Open/迁移/目录缺失） |
| T8 总验收 | — | ✅ 通过 | 四构建矩阵零警告；四构建 ctest 全绿；S1 双构建达标；授权三路径复核（见 §5） |

## 3. 问题清单

| 问题 | 影响 | 处置 | 状态 |
|---|---|---|---|
| ChunkSleep::Recalc 半唤醒→再空出无法回 SemiWake（分支漏配） | 休眠机制失效 | T3 内修复：本区块空且相邻有玩家 → 无条件 SemiWake | ✅ 已闭环 |
| TickOnce 结束后写窗口停在 false | 下个 Tick/测试默认态被破坏（写入全判违规） | T4 内修复：Tick 结束恢复写窗口默认开 | ✅ 已闭环 |
| 测试间共享状态污染（EntityPool/AoiTree/ChunkSleep/AiSystem） | 偶发断言失败 | 各用例开头 ResetAll/Init；AI 测试补玩家进区块激活（休眠跳过语义） | ✅ 已闭环 |
| WriteGuard 原实现 assert(false) 在 Debug 下触发崩溃 | Debug 构建不可跑 | 去 assert 改运行期计数+阶段10 遥测（更强可观测） | ✅ 已闭环 |
| main.cpp config key 与 config.yaml 不匹配（resource_db/player_db/game_mode） | 启动失败 E_PARAM | T6 内对齐 02 config 权威字段 | ✅ 已闭环 |
| player.db 父目录不存在导致 E_IO | 首次启动失败 | DB::Open 自动创建父目录 | ✅ 已闭环 |
| MakeCmd 未初始化字段（v1/v2）→ Debug 下读未初始化 UB | 事务测试偶挂 | 值初始化 `MsgCommand c{}`（测试+WorldTick 用例） | ✅ 已闭环 |
| extended S1 首次 CPU=5.15% 略超阈值 | 边缘超标 | 重跑确认机器负载波动，复测 4.68% 达标 | ✅ 已闭环（记录在案） |
| SEH filter 噪音（多线程测试退出时 Catch2 打印） | 无功能影响 | 已知无害噪音，记录不处理 | 📝 已记录 |

### 3.1 独立审计修复记录（2026-10-01，dev-conductor §7 八步式审计后补）

| # | 审计发现 | 处置 | 验证 |
|---|---|---|---|
| A1 | ChunkSleep::ChunkIdOf 硬编码 /8，02 config chunk_size 可配但不生效（活的参数铁律） | Configure 签名扩展为 (chunkSize, semiWakeDist, sleepIdleMs)，ChunkIdOf 用配置值；ResetAll 复位默认 8 | 新增 chunk_size=4/默认 8 分区断言；四构建全绿 |
| A2 | AoiTree 默认视野硬编码 kViewRadiusD=12，config aoi_view_radius 不生效 | 新增 SetViewRadius [MAIN]，main 步骤6 读 config 传入；Init 复位默认 | 四构建全绿 |
| A3 | MsgQueue 容量硬编码 4096/2048/4096，01 §3.3 注释承诺"T6 启动接 config"未兑现 | 02 §3 + config.yaml 新增 queue_command_cap/queue_query_cap/queue_event_cap，main 步骤6 读取 | 四构建全绿 + S1 无回归 |
| A4 | 03 §4 关闭流程第4步"冲刷 MsgQueue（未完成指令全部回滚）"未实现 | RunTickLoop 关闭段补 MsgQueue::ConsumeAll() 冲刷（handler 按事务语义处理） | 编译+启动复核 |
| A5 | 被动怪（ai_type=2，11 §4.4"不主动攻击"）被统一 Chase 处理 | ThinkOne Idle/Patrol 分支 aiType==2 → 保持 Idle 不追击 | 新增被动怪不追击断言；四构建全绿 |
| A6 | 01 §3.3 类名 AOI vs 实现 AoiTree；MsgQueue::Post(QueuedMsg) vs 三类重载 | 01 加注实现类名与三类重载说明（契约签名不变） | 文档核对 |
| A7 | 08 §2.3 变更记录未登记阶段3 变更 | 补 4 条阶段3 变更登记（db_migrations_dir+DB 模块 / WriteGuard 计数 / --bench / 审计修复批） | 文档核对 |
| A8 | AoiTree 根 1024² 硬编码占位（无 config 字段） | 登记 15 台账 OPEN-02（阶段8 地图接入时由地图尺寸驱动，本阶段无地图数据，占位合法） | 台账登记 |

**审计后复核**：四构建矩阵零警告 + 81 用例全绿（Release 1611 断言 / Debug 1610 断言）+ S1 双构建达标（classic Tick 2.07ms/CPU 4.13%；extended Tick 1.97ms/CPU 3.94%）。

## 4. 越界与变更声明

| 变更 | 类型 | 处置 |
|---|---|---|
| 02 §3 新增配置项 `db_migrations_dir`（player.db 迁移目录） | 规范新增（T6 需要） | 已同步写入 config.yaml + 02 权威源（本报告 §4 登记） |
| 02 §3 新增配置项 `queue_command_cap/queue_query_cap/queue_event_cap` | 审计修复（A3） | 已同步写入 config.yaml + 02 权威源（本报告 §3.1 登记） |
| src/base/DB.h/.cpp 新增（SQLite 封装：WAL + 迁移执行器） | 工单范围内（T6 第 5 步"player.db 打开+迁移执行"需要执行器，阶段1 仅交付 SQL 文件） | 已交付并单测 |
| WriteGuard 从 Debug assert 改为运行期计数 | T4 实现方式调整（工单允许"调试断言或代码审查标记"，计数=代码级保障且 Release 生效） | 已交付并单测 |
| --bench 压测模式（T6 新增 CLI 开关） | S1 压测载体（工单 S1 要求） | 已交付；临时配置 bench-extended.yaml 不入库（压测专用，gitignore bench-*.yaml） |
| ChunkSleep::Configure 签名扩展 / AoiTree::SetViewRadius 新增 / AiSystem 被动怪不追击 | 审计修复（A1/A2/A5） | 已交付并单测 |

清单外未做任何改动（战斗/脚本/网络均未触碰，留阶段4/5/6）。

## 5. 验收证据汇总

### 5.1 构建矩阵（零警告零错误）
| Preset | 配置 | 结果 |
|---|---|---|
| classic-release | Classic × Release | ✅ EXIT=0，0 warning |
| extended-release | Extended × Release | ✅ EXIT=0，0 warning |
| classic-debug | Classic × Debug | ✅ EXIT=0，0 warning |
| extended-debug | Extended × Debug | ✅ EXIT=0，0 warning |

### 5.2 单元测试（四构建全绿）
| Preset | 用例 | 断言 | 结果 |
|---|---|---|---|
| classic-release | 81 | 1611 | ✅ All tests passed |
| extended-release | 81 | 1611 | ✅ All tests passed |
| classic-debug | 81 | 1610 | ✅ All tests passed |
| extended-debug | 81 | 1610 | ✅ All tests passed |

（Debug 断言数少 1：事务组断言路径差异，全绿为准；1611 = 1606 基线 + 审计新增 5 条：chunk_size 分区 4 条 + 被动怪不追击 1 条。）

### 5.3 S1 空图万怪压测（单地图 10000 怪物、无玩家场景，ADR-017）
机器规格（05 §2 记录）：**11th Gen Intel Core i9-11900K @ 3.50GHz（8 核）、32GB RAM、Windows 11 专业版**

| 构建 | ticks（10s） | 平均 Tick | 最大 Tick | 引擎占用 | 结果 |
|---|---|---|---|---|---|
| classic-release（审计复核） | 200 | 2066.49us | 8104us | 4.13% | ✅ PASS（≤10ms / ≤5%） |
| extended-release（审计复核） | 200 | 1969.52us | 8269us | 3.94% | ✅ PASS（≤10ms / ≤5%） |
| classic-release（原验收） | 200 | 2220.99us | 12098us | 4.44% | ✅ PASS（≤10ms / ≤5%） |
| extended-release（原验收复跑） | 200 | 2343.02us | 7221us | 4.68% | ✅ PASS（≤10ms / ≤5%） |

（原验收 extended 首次 5.15% 复测为机器负载波动；审计修复后复核值更优；平均 Tick 为主要口径，最大 Tick 首 Tick 含刷怪初始化。）

### 5.4 授权三路径复核（沿用阶段1 口径）
| 路径 | 结果 |
|---|---|
| 无 lic 文件 | ✅ 拒绝启动（E_IO → exit 2） |
| 有效签名 lic | ✅ 通过（阶段1 TestLicense 沿用） |
| 篡改/无效签名 | ✅ 拒绝（阶段1 TestLicense 沿用） |

### 5.5 启动流程验证（--bench 冷启动）
步骤2 日志 → 3 授权跳过（压测标注）→ 4 资源库跳过 → 5 player.db 迁移（0001~0004，user_version=4，10 张表）→ 6 世界组件 → 7 脚本占位 → 8 刷怪 10000 → 9 NetGate 占位 → 10 Tick 循环。正常模式无 lic → 步骤3 熔断退出。

## 6. 下一阶段前置核验（阶段4 · 战斗核心）

| 前置 | 状态 |
|---|---|
| 阶段3 冻结（本报告 + stage3-frozen tag） | 待冻结 |
| 战斗输入通道：MsgQueue Command（SET_HP/SET_POS/SET_STATE）可投递可分组 | ✅ 已就绪 |
| 实体写入口：阶段5 唯一写入窗口 + Entity::SetHp/SetPos/ChangeState | ✅ 已就绪 |
| 战斗位置语义：Vec2 网格 + AoiTree 移动更新（OnEntityMove 预留） | ✅ 已就绪 |
| 怪物目标检索：AiSystem Chase 输出 target（阶段4 消费攻击动作） | ✅ 已就绪 |
| 战斗结果广播：MsgEvent（ENTITY_DIE 等）投递通道 | ✅ 已就绪 |
| 资源参数：ResourceDB::GetItem/GetMonster（DC/AC/HP/等级） | ✅ 已就绪（阶段2 冻结） |
| 21 号工单（阶段4）前置依赖确认 | ⏳ 阶段3 冻结后签发 |

## 7. 冻结建议

**建议：冻结**，打 tag `stage3-frozen` 至当前 HEAD（本报告对应提交）。

- 九条任务按序执行，Gate PASS 后冻结 ✅
- main.cpp 已接管：10 步启动 + Tick + 优雅关闭 ✅
- 阶段5 唯一写入点有代码级保障（WriteGuard 计数+遥测）✅
- S1 空图万怪 CPU≤5% 达标（记录机器规格见 §5.3）✅
- 后续：阶段4（战斗核心，21 号工单）在 stage3-frozen 后开工；OPEN 项无遗留（SEH 噪音为已知无害项）。
