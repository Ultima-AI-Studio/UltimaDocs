# UltimaAI 根目录索引

> 更新：2026-10-24。此文件提供根级导航，链接既有权威源，不复制项目队列或授予执行权限。

## 全局强制规则 G-DISPATCH-001

**各项目自主推进开发，由项目方直接调用 Codex 执行；开发必须遵守本 INDEX 要求的规范队列标准（工单三段式 + DoR 五项 + 全局主表登记 + WIP 上限 + 冻结门 + 打 tag 铁律），禁止绕过规范裸跑。** 此规则于 2026-10-28 由用户明确批准（取代 2026-10-24"所有项目必须经 UltimaManager 统一调配"旧版；Manager 因 Owner 冻结门未闭合且无产品接续权，不再作为唯一派发中枢）。各项目按各自 `docs/INDEX.md` 与范式自主登记、自主派发、独立验收；Manager 保留为可选监督/审计工具，不阻塞产品推进。入口约束见 [AGENTS.md](AGENTS.md)。

## 全局任务工作流 G-TASKFLOW-001（2026-10-29 用户批准建立）

**所有任务的处理与下发统一走[任务工作流范式](_shared/paradigms/UltimaAI-任务工作流范式.md)**：登记 → 计划评审 → 执行 → 独立审计 → 有界修复 → 验收 → 冻结。**执行端无关**——Codex API / DeepSeek API / 未来模型都只是可替换执行适配器，替换入口不改变工作流本体；Codex 适配器细则见[Codex-外部执行端调用范式](_shared/paradigms/Codex-外部执行端调用范式.md)。规划/开发/独立审查分离，越界保护 fail-closed，缺 tag = 闭环未完成。

**UltimaManager（任务控制面）已登记为 UltimaAgent 标准基础能力（2026-10-29）**：工单编号核发（G-WO-NAME-001）、全局队列主表登记、接管/来源/授权与前置核验；G-DISPATCH-001 自主推进版下为可选监督/审计工具，不阻塞产品推进。登记见[能力注册表](_shared/registry.md)（组件 `ultima-manager` + 能力 m29）与 `UltimaManager/docs/INDEX.md`。

## 阅读顺序

1. 阅读既有[启动入口](_shared/启动入口.md)与[顶层架构标准](ULTIMA-STANDARD.md)。
2. 查阅[范式存档总纲](_shared/paradigms/Ultima-范式存档总纲.md)，再进入目标项目的 `docs/INDEX.md`。
3. 涉及任务处理/下发时，先读[任务工作流范式](_shared/paradigms/UltimaAI-任务工作流范式.md)（G-TASKFLOW-001，执行端无关）与[Codex 外部执行端调用范式](_shared/paradigms/Codex-外部执行端调用范式.md)（当前默认执行适配器）。
4. 涉及项目接入、任务入队或接续时，阅读[项目接入与任务队列派发范式](_shared/paradigms/UltimaAI-项目接入与任务队列派发范式.md)。其中 G-DISPATCH-001 自主推进版已由用户批准生效（2026-10-28），其余新增接入细则仍待复核；原工单验收和 Owner 决定保留。
5. 按项目工单和真实执行证据核对就绪条件，各项目自主准入、自主派发 Codex，独立验收后登记冻结。

## 全局工单命名 G-WO-NAME-001

全部项目新工单统一使用 `wo-<project-key>-<YYYYMMDD>-<NNNN>` 作为原单 ID，显示标题使用 `项目名｜类型｜对象与交付目标`，文件名使用 `<原单ID>--<topic-slug>.md`。正式编号由 Manager 控制面核重登记；已有工单保留原 ID、路径、历史和累计预算，后续阶段继续关联原单。创建、阅读或提交工单前必读[全局工单命名标准](_shared/paradigms/UltimaAI-全局工单命名标准.md)。命名合规不等于已获执行准入。

## 全局入口

### 新请求接入前置：先更新范式，再引导入队

2026-10-24 用户明确要求：**尚未更新工单范式的项目，不引导到工单队列。** 对新请求先核对项目 INDEX 已正确引用全局调配规则、工单命名与接入范式，项目申请/工单目录职责和原单身份清楚，并由 Manager 核验接管、来源、授权与前置；缺项只读登记为“待范式更新/待接入”，不显示为可提交、可派发或自动扫描准入。引用文本存在只是文档检查，不等于正式准入。

重新读取项目队列应先生成只读盘点与旧记录对账，再由 Manager 去重、关联原单并逐项准入；禁止清空队列、批量重命名、重开已关闭工单或重置失败/预算。已登记契约保留原门，新规则不自动撤销、重建或放行。目录存在不构成扫描授权，自动扫描实现仍须验收。

本次只读盘点：[项目请求与队列清单](_shared/queue/request-intake-inventory-20261024.json)。该快照是核对证据，不是自动导入清单或派发白名单；项目入口表继续仅用于阅读文档。

| 内容 | 入口 | 用途 |
|---|---|---|
| 项目接入、入队与接续 | [接入与派发范式](_shared/paradigms/UltimaAI-项目接入与任务队列派发范式.md) | 身份隔离、执行权威、准入清单、独立审计和人工门 |
| 执行端调用 | [Codex 外部执行端调用范式](_shared/paradigms/Codex-外部执行端调用范式.md) | 既有工单、派发、回执及并发规则；**v1.2 已固化派发执行环境：Codex ≥0.165.0 + 精简 CODEX_HOME（静默无弹窗）**；历史命令与环境清单仍须在实际执行时重新核验 |
| 全局工单登记 | [全局队列主表](_shared/queue/global-queue-index.md) | 聚合、预登记与证据入口；不是另一套派发器 |
| 工单命名 | [全局工单命名标准](_shared/paradigms/UltimaAI-全局工单命名标准.md) | 新单 ID、显示标题、文件名、阶段关联和存量兼容 |
| 能力登记 | [能力注册表](_shared/registry.md) | 复用能力和项目登记 |
| 服务器资产台账 | [_shared/server-assets.md](_shared/server-assets.md) | 全系服务器唯一权威（规格/工具链/凭证指针）；变更只改该文件 |
| 新项目索引 | [项目引导索引模板](_shared/templates/项目引导索引模板.md) | 新项目必读入口模板 |

## 项目入口

| 项目 | 引导索引 |
|---|---|
| UltimaManager | [docs/INDEX.md](UltimaManager/docs/INDEX.md) |
| UltimaAgent | [docs/INDEX.md](UltimaAgent/docs/INDEX.md) |
| UltimaConsole | [docs/INDEX.md](UltimaConsole/docs/INDEX.md) |
| UltimaSentinel | [docs/INDEX.md](UltimaSentinel/docs/INDEX.md) |
| UltimaEngine | [docs/INDEX.md](UltimaEngine/docs/INDEX.md) |
| UltimaGold | [docs/INDEX.md](UltimaGold/docs/INDEX.md) |
| UltimaRadar | [docs/INDEX.md](UltimaRadar/docs/INDEX.md) |
| UltimaScan | [docs/INDEX.md](UltimaScan/docs/INDEX.md) |
| UltimaConsoleSdkRecovery | [docs/INDEX.md](UltimaConsoleSdkRecovery/docs/INDEX.md) |
| UltimaSentinelRuntimeRecovery | [docs/INDEX.md](UltimaSentinelRuntimeRecovery/docs/INDEX.md) |

目录存在或列入本表仅表示有文档入口，不表示已接管、已授权或可派发。未列出的项目先查能力注册表与本项目文档，禁止套用相邻项目的任务或权限。

## 接入边界

- 各项目自主推进开发并直接调用 Codex；原观察器、旧恢复器、独立脚本和定时监督只能监督，不得成为另类的唯一派发者（自主派发以项目方名义进行）。
- 未建队列的项目先按范式补建 `tasks\queue\` 并登记全局主表，再派发；禁止绕过全局登记裸派 Codex。
- 项目工单决定目标、写域和验收；正式执行登记与持久回执决定实际执行状态；界面、Markdown 聚合表和状态镜像不能替代这些证据。
- 已批准的人工门、冻结门和条件接续继续有效；自主推进不解除 Owner 冻结/发布门。
- 正在执行或已绑定来源哈希的项目 INDEX、工单和权威文档，须经各自管线安全接入新链接；本次根级导航不直接改写它们。
