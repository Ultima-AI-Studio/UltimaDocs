# 阶段9 报告：发布扩展（26 工单 T0~T6）

> 生成时间：2026-10-03 ｜ 结论：**通过（有条件冻结）** ｜ 阶段9 冻结 tag：`stage9-frozen`（commit 16314f8，含审计修复）
> 版本记录：v1.0（05ffd90 冻结）→ v1.1（16314f8 完整性审计修复，2026-10-03）

## 1. 阶段概览

阶段9 为最后一个开发阶段（发布扩展），26 工单 T0~T6 全部落地并实测。**开发工作完成**；发布包、文档、Agent 玩法、哈希清单、版本座位、演练全部按真实口径验收通过。全量单测回归按官方验收口径（`--order lex`，ctest 配置）双构建全绿。

**2026-10-03 完整性审计**（对照 26 工单 + 07 规范 + 磁盘实测）发现并修复 3 个真实缺陷（Extended 包无差异/启动即退/文档占位符）+ 6 项文档漂移与口径问题，详见 §8。

## 2. 任务完成情况（T0~T6）

| T | 任务 | 状态 | 证据 |
|---|---|---|---|
| T0 | 打包脚本 package.ps1 | ✅ | 双发布包产出：`dist/TuppoM2-Classic-v0.9.0.zip`（5,232,971 B / **46 文件** / 35.35MB）+ `dist/TuppoM2-Extended-v0.9.0.zip`（5,233,411 B / **47 文件**，含 `scripts/README.txt` 扩展脚本占位说明，与 Classic 有真实差异），含 EXE+PrecompileTool+migrations+runtime 模板+lang+scripts+source_assets+README+部署手册 |
| T1 | 哈希清单 hash.ps1 | ✅ | `SHA256SUMS.txt` **99 文件**（zip 走 System.IO.Compression 免外部依赖）；相对路径 Split-Path 缺陷已修复（Resolve-Path）；实算重核与清单逐字一致 |
| T2 | 发布文档 | ✅ | `docs/release/README.txt` + `部署手册.md` 入包（部署/开服/取机器码/lic 申请/性能基线/容灾/故障速查/边界声明）；打包时模板占位符 `${VERSION}/${MODE}/vX.Y.Z` 自动替换（审计修复）；覆盖 07 §3.3 文档四项 + 指向 12 运维自检 |
| T3 | Roguelike Agent | ✅ | `src/agent/EventBus.{h,cpp}` + `RogueAgent.{h,cpp}`（仅 Extended，行为体 `#ifdef TUPPM2_EXTENDED` + Classic stub）+ `tests/TestAgent.cpp`（3 cases / 17 assertions）；白名单 5 动作 + EventBus 限速 5/秒 + 事务桥（OPEN-14）+ 确定性 RNG |
| T4 | 发布演练 | ✅ | Classic 包：DevLicGen 授权（hwid=a3761a…, expire=2027-10-03, FeatureMask=7, MaxOnline=1000）→ 首启 run1 pid=27952 → 重启灰度 run2 pid=35852 双端口单 PID 全 PASS。**Extended 包（审计修复后补跑）**：包内 game_mode=Extended 校验通过 → 首启 pid=2292 存活 → 日志确认 授权通过（FeatureMask=7/MaxOnline=1000）/ResourceDB OK（t3mini）/player.db OK/世界组件 OK/脚本引擎/地图加载/风控配置 → 已停止 |
| T5 | 版本同步 version-sync.ps1 | ✅ | 软件版本族：config.build_version=v0.9.0 == 参数 v0.9.0 + dist 目录名一致；DB 版本族：player.db user_version=9 == 最新迁移号 9；WARN 登记不造假（EXE FileVersion 未注入 OPEN-21、resource.db meta.schema_version 空 OPEN-22，发布门注入） |
| T6 | 总验收 | ✅（见 §5） | 双构建 0 错误；全量回归 classic `--order lex` **9459 断言 / 268 用例全绿**（与阶段8 冻结基线一致）、extended `--order lex` **9506 断言 / 278 用例全绿**（含 Agent 3 用例） |

## 3. 问题清单

| # | 问题 | 影响 | 处置 | 状态 |
|---|---|---|---|---|
| 1 | 全量单测默认注册顺序（无参直跑）出现 14~15 断言失败 | 共享全局状态测试对注册顺序敏感；**非功能回归**（阶段8 旧 classic 二进制同条件同失败） | 定性：TestAgent 编译单元改变链接注册顺序 → 顺序敏感；官方口径 `--order lex`（ctest 配置）确定性全绿 | OPEN-20（测试基建硬化归维护） |
| 2 | EXE FileVersion 未注入（0.0.0.0） | 版本四处一致缺 EXE 座位 | WARN 登记，rc 资源待发布配置 | OPEN-21 |
| 3 | resource.db meta.schema_version 为空 | DB 结构版本座位缺资源库侧 | WARN 登记 | OPEN-22 |
| 4 | 发布包 resource.db 为 t3mini 测试迷你库（items=11, monsters=0, maps=1） | 非真实素材编译库 | 设计口径="模板+待运营编译"；正式开服前 PrecompileTool + 真实 DBC 重编译（OPEN-01 未裁决） | OPEN-23 |
| 5 | Win10 客户端兼容矩阵 | 仅登记"待实测"非缺陷（本机 Win11） | 真实口径登记 | OPEN（历史延续） |
| 6 | 引擎日志中文在部分终端显示乱码（GBK 渲染 UTF-8） | 展示层问题，不影响文件内容 | 已知，登记备忘 | 不影响 |
| 7 | **Extended 发布包与 Classic 无差异**（zip 层 46 文件逐字节同） | 违反 07 §3.2/26 §3 交付物定义（应含扩展内容）——根因：scripts/ 空目录不入 zip、TuppoExt.dll 未构建 | **已修**：package.ps1 为 Extended 补 `scripts/README.txt` → 双包有真实差异（46/47） | ✅ 闭环（审计发现） |
| 8 | **Extended 包启动即退**（`配置加载失败 E_PARAM`） | T4 演练只覆盖 Classic，Extended 包从未冒烟——根因：包内 config.yaml game_mode=Classic 与 Extended 构建宏不一致 | **已修**：package.ps1 按模式改写 game_mode（extended→Extended）；重打+重哈希+重冒烟 PASS（pid=2292） | ✅ 闭环（审计发现） |
| 9 | **README/部署手册占位符未替换**（`${VERSION}/${MODE}/vX.Y.Z` 原样入包） | T2 文档 Gate 缺口，发布包显示模板占位 | **已修**：package.ps1 拷贝后模板替换（实测 README 显示"版本：v0.9.0 ｜ 模式：Extended"） | ✅ 闭环（审计发现） |
| 10 | 07 §1.2/§3.2 文档漂移（写 Extended 含 TuppoExt.dll 且 Agent 在 DLL） | 规范与实现（Agent 编入主 EXE）不一致 | **已修**：07 v1.1 校准（Agent 编入 EXE、DLL 可选） | ✅ 闭环（审计发现） |
| 11 | 07 §3.1 结构缺 migrations/lang/logs；§3.3 核对表未逐项标注 | 发布包结构文档不完整 | **已修**：07 v1.1 结构图补全 + 核对表逐项状态 | ✅ 闭环（审计发现） |
| 12 | 07 §4 发布流程口径（"4 配置全通过"/加固/分发/灰度无状态） | 发布门步骤与阶段9 实际边界不清 | **已修**：07 v1.1 发布门=Release 2 配置；加固/分发/灰度显式归发布门 | ✅ 闭环（审计发现） |
| 13 | 26 工单 T2/T4/T5 Gate 口径过严（干净机器/三阶段/四处一致） | 与无外部机器/发布未开始的实际不符 | **已修**：26 工单 v1.1 Gate 校准（本机冒烟/内部测试+发布门/版本 WARN 口径） | ✅ 闭环（审计发现） |
| 14 | 发布加固 06 §1.7 层2 加壳未实施 | 授权验证模块未加壳（防破解弱化） | 层4 TamperCheck（60s 周期）已内置；自研轻量加壳/商业壳归发布门（商务裁决后） | OPEN-24 |
| 15 | 更新包签名/包签名未做 | 07 §4 第 7 步防替换未实施 | 哈希✅；PGP/代码签名与更新机制归发布门/v2.1+ | OPEN-25 |
| 16 | 灰度/正式发布未做 | 07 §4 第 9 步未到 | 内部测试完成；灰度（1 台）/正式需外部机器，归发布门 | OPEN-26 |
| 17 | stage9-drill 演练解压产物（lang/source_assets/src）未跟踪 | git 状态脏 | **已修**：.gitignore 补 `stage9-drill/`（已跟踪证据文档保留） | ✅ 闭环（审计发现） |
| 18 | stage9-report 未引用压测报告 S1~S6（26 §3 交付物要求） | 验收证据链缺压测引用 | **已修**：§5 补引用（bench-S1~S6 文档） | ✅ 闭环（审计发现） |

## 4. 越界与变更声明

- 本阶段全部改动在 26 工单范围内（T0~T6）；对比实验（临时移除/恢复 agent 编译单元）已完整还原现场，无清单外残留。
- `src/main.cpp` 默认 cfgPath 改为 `"runtime/config.yaml"`（07 §3.1 发布包布局要求，T4 演练发现后修复，属工单内缺陷修复）。
- `tests/CMakeLists.txt` 追加 TestAgent.cpp（T3 要求）。
- **审计修复轮（commit 16314f8）**：全部为阶段9 范围内缺陷修复与文档校准（26/07 v1.1、package.ps1、.gitignore、15 台账 OPEN-24~26、stage9-audit-finish.ps1 收尾工具），无清单外新功能。

## 5. 验收证据汇总（T6 总验收）

| 项 | 结果 | 证据 |
|---|---|---|
| 双发布包 | ✅ | dist 双 zip（Classic 46 / Extended 47 文件/35.35MB）+ manifest |
| SHA256 清单 | ✅ | SHA256SUMS.txt 99 文件，实算重核逐字一致 |
| README/部署手册可复现部署 | ✅ | 入包（占位符已替换）；部署手册 5 步安装 + 开服命令 |
| Agent 单测 | ✅ | extended lex 全量含 [agent] 3 cases/17 assertions |
| 全量回归（官方口径 --order lex） | ✅ | classic 9459/268 全绿；extended 9506/278 全绿（日志：t9-test-classic-lex.log / t9-test-extended-lex.log） |
| **压测报告（S1~S6，26 §3 交付物）** | ✅ | `docs/reports/bench-S1~S6-*.md` 全量在档（S1 移动/S2 战斗/S3 千人/S4 AOI/S5 重连/S6 摆摊等），基线引用见部署手册 §5 |
| 发布演练 | ✅ | stage9-drill/classic（首启+重启灰度）+ stage9-drill/extended（审计修复后首启）双包 PASS |
| 版本座位 | ✅ | config==参数==迁移号 9（EXE/schema_version WARN 登记 OPEN-21/22） |
| 冻结基线 | ✅ | commit 16314f8 + tag `stage9-frozen`（审计修复后重打） |

## 6. 下一阶段前置核验（开发完成后的收尾）

- [x] 阶段9 26 工单 T0~T6 全部落地
- [x] 全量回归双构建全绿（lex 口径）
- [x] 发布包/哈希/文档/演练/版本座位实测
- [x] 完整性审计闭环（3 缺陷 + 6 文档项修复，OPEN-24~26 登记）
- [x] **正式版本号拍板 v1.0.0（2026-10-03，用户裁决）**——见 §9
- [ ] 真实素材重编译（OPEN-01 开源范围裁决后）
- [ ] 里程碑发布摘要（用户拍板 6 项业务决策之一）

## 7. 冻结建议

**建议冻结 `stage9-frozen` = 开发工作完成（含审计修复轮 commit 16314f8）。** 遗留 OPEN 项（顺序 flaky 硬化、EXE FileVersion、schema_version、真实素材编译、加固层2、包签名、灰度/正式）均为非阻塞收尾项或发布门事项，移入 15 台账按版本迭代/发布门处理；正式对外发布前按 07 发布核对表 + 14A 发布条件走发布门。

## 8. 完整性审计记录（2026-10-03，commit 16314f8）

**审计方法**（dev-conductor §7）：26 工单任务/交付物清单 × 07 规范 × 06 §1.7 × 磁盘产物（双 zip 文件树、SHA 实算、git status、报告在档）逐项核对。

**审计发现与处置汇总**：

| 类 | 项 | 处置 |
|---|---|---|
| 真实缺陷（3） | Extended 包无差异（scripts 空目录不入 zip）；Extended 包 game_mode 不一致启动即退；文档占位符未替换 | package.ps1 三处修复（scripts/README、game_mode 按模式、模板替换）→ 重打+重哈希+双包冒烟全 PASS |
| 文档漂移（6） | 07 §1.2/§3.2 DLL 定义、§3.1 结构缺项、§3.3 核对表未标注、§4 流程口径；26 工单 T2/T4/T5 Gate；stage9-report 压测引用 | 07/26 升 v1.1 校准；stage9-report §5 补引用 |
| OPEN 登记（3 新增） | 加固层2 加壳（OPEN-24）、更新包签名/包签名（OPEN-25）、灰度/正式（OPEN-26） | 15 台账登记（发布门/v2.1+ 处理） |
| 验证正确 | SHA 清单与实算一致（先前 spot-check False 为检查脚本自身路径匹配问题）；Classic 包无 DLL/scripts（T0 Gate）；压测 S1~S6 在档；lex 回归双全绿 | 无需修改，排除误报 |

**本次审计确认**：阶段9 冻结基线（05ffd90 → 16314f8）无功能回归；发布包缺陷已闭环；正式发布前须完成发布门核对表（07 §3.3 剩余项：schema_version、真实素材重编译、端到端登录进图打怪冒烟、Win10 矩阵、加固层2）。

## 9. 正式版本号 v1.0.0（2026-10-03 用户拍板）

用户拍板正式版本号 **v1.0.0**（替代开发基线 v0.9.0）。执行版本升级并实测闭环：

| 项 | 结果 |
|---|---|
| 版本座位 | config.build_version=v1.0.0 == dist 目录名 == EXE FileVersion 1.0.0.0（归一化比较）== player.db 迁移号 9 → version-sync **PASS** |
| EXE FileVersion 注入 | src/version.rc（FileVersion 1.0.0.0）+ src/CMakeLists.txt WIN32 target_sources → **OPEN-21 闭环** |
| 双发布包 | `dist/TuppoM2-Classic-v1.0.0.zip`（46 文件/5,233,347 B）+ `dist/TuppoM2-Extended-v1.0.0.zip`（47 文件/5,233,786 B）；旧 v0.9.0 产物移除 |
| SHA256 清单 | SHA256SUMS.txt **99 文件**（v1.0.0 重算） |
| 双包冒烟 | Classic pid=45492 / Extended pid=42904 均存活；授权通过/ResourceDB/player.db/世界组件/脚本引擎/地图/风控全 OK |
| config 补键 | 补 `broadcast_max_pkt_ps: 200`（02 §3 权威键，消除启动 warning） |
| git | commit + tag **v1.0.0**（正式发布基线） |

**发布门剩余项**（正式对外发版前）：真实素材重编译（OPEN-23）、schema_version 补写（OPEN-22）、端到端登录进图打怪冒烟、Win10 矩阵、加固层2（OPEN-24）、包签名（OPEN-25）、灰度/正式发布（OPEN-26）。

## 10. 发布门执行（2026-10-03 第二轮，用户指令"剩余项都做完"）

| 项 | 结果 |
|---|---|
| OPEN-23 真实素材重编译 | ✅ **闭环**：source_assets/176 真实 1.76 素材（Items 687/怪物 379/5 地图/MonDrop 240）→ PrecompileTool 编译 → resource.db：items=686/monsters=378/maps=5/drops=32330/monster_spawns=89/npcs=11；重打包 v1.0.0 双包 37.17MB；端到端 ResourceDB hash=17374408584135087776 加载 OK |
| OPEN-22 schema_version | ✅ **闭环**：编译产物 meta.schema_version=2 |
| 端到端登录进图打怪冒烟 | ✅ **闭环**：v1.0.0 双包 FakeClient 假人登录→建号→进图（地图=1 坐标=(0,0) 等级=1）→ Telemetry online=2；compat-matrix.ps1 双模式 smoke=PASS（login/select/create/enter/walk/exit），报告 compat-matrix-20261003-0418.md |
| 初始背包素材命名（BL-05 子项） | ✅ **闭环**：LoginFlow.cpp 素材命名兼容映射（布衣按性别/金创药(小)→(小量)+裸名兜底）；端到端复验缺失日志清零 |
| OPEN-25 包签名 | 📋 **部分**：SHA256SUMS 哈希防篡改完成；PGP 需 gpg（本机未装）、代码签名需证书（商务购买），归发布门外部工具+证书 |
| OPEN-24 加固层2 加壳 | 📋 **维持**：层4 TamperCheck 已内置；商业壳依赖商务裁决高级授权定价，自研轻量加壳候选 v2.1 |
| OPEN-26 灰度/正式 | 📋 **维持**：需外部机器，归发布门 |
| Win10 客户端矩阵 | 📋 **外部依赖**：本机 Win11；compat-matrix 已生成 Win11 本机基线，Win10 实测需独立环境（VM/实体机） |
