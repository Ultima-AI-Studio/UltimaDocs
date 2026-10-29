# Ultima AI Studio 产品顶层架构标准（ULTIMA-STANDARD v1.0）

> **适用范围**：所有挂 `Ultima` 前缀的产品（UltimaConsole / UltimaAgent / UltimaEngine / UltimaGold / UltimaRadar 及未来所有 Ultima 产品）。
> **强制对象**：豆包软件中所有 Ultima 相关工程、任何聊天窗中挂 Ultima 前缀的项目——**每个项目更新时都必须同步更新自己的架构文档，每次执行都必须符合本架构标准**。
> **权威源**：本文件为顶层范本；各产品在自身根目录维护 `docs/architecture.md`（引用本范本 + 产品特化）。

---

## 一、产品身份与命名

| 规则 | 要求 |
|---|---|
| 命名 | `Ultima` + 产品名（驼峰），如 UltimaConsole / UltimaRadar |
| 根目录 | `H:\UltimaAI\<ProductName>`（禁止散落在其他盘符的裸目录） |
| 口头/文档称呼 | 一律英文全称（如 UltimaRadar），不使用音译/中文别名 |

## 二、强制目录结构（每产品必须对齐）

```
<ProductName>/
├── README.md               # 产品身份与状态总览（必填：一句话定位/当前状态/北极星指标/入口）
├── docs/                   # 文档体系（见第三节）
│   ├── architecture.md     # 产品架构文档（引用本范本 + 产品特化）
│   ├── <方案文档>.md        # 需求→技术方案→冻结
│   ├── reports/            # 阶段报告 stage-<阶段>.md + 审计报告
│   └── <设计稿/规范>        # UI 定稿/规范类
├── tasks/
│   └── queue/              # 工单队列 wo-<阶段>-mN.md + 队列主表 index
├── sync/
│   └── product.json        # 数据同步模板（终端录取源，见第五节）
└── <代码工程>              # entry/ src/ 等（按技术栈）
```

## 三、文档体系标准（每产品必维护 6 件）

1. **README.md**：身份/定位/当前状态/北极星指标/入口
2. **docs/architecture.md**：产品架构文档（本范本特化版——目录结构/数据流/模块边界）
3. **方案文档**：需求 → 技术方案 → **冻结**（vX.Y 冻结标记）
4. **工单队列**：`tasks/queue/wo-<阶段>-mN.md`（三段式：文件/写什么/验收/禁止）+ 队列主表
5. **阶段报告**：`docs/reports/stage-<阶段>.md`（每阶段冻结产出，含 Gate 结果）
6. **审计报告**：`docs/reports/<审计名>-audit.md`（治理体检结论 + 评分）
7. **文档库 AI 精简**（2026-10-20 新增）：文档库挂载文档的 `content` 由本地千问 14B 生成「精炼版」，客户端点击展开即读完整精简内容、链接回原文，实现"内容都连上"。
   - **引擎**：本地 Ollama `qwen2.5-14b-opencode:8k`（`127.0.0.1:11434`，纯本地无外部授权）
   - **脚本**：`H:\UltimaAI\_shared\queue\doc-summarize.py`（幂等：已精简/相同内容自动跳过）
   - **对象**：各产品 `sync/product.json` 文档库（`docs` 组）中挂载的**本地 md 文档**；飞书介绍类文档（本身为短介绍）保留原文不精简
   - **输出**：每篇生成精炼版 markdown——保留章节结构/关键结论/数据/约束/验收项，压缩冗余至原文 1/3 左右，**完整可读（非一句话摘要）**，不编造原文没有的数据 → 写回 `docs[].content` 并同步 seed
   - **触发**：文档新增/修订后跑一次；数据变化后按五节触发点推送（Gist + Gitee）
   - **验收**：`docs[].content` 长度 >200 字（完整精炼）；客户端文档库点击展开可见完整内容；本地源文档不被删除/改写

## 四、执行标准（每次开发/执行必须符合）

### 全局强制规则 G-DISPATCH-001（2026-10-28 用户拍板自主推进版，取代 2026-10-24 旧版）

**各项目自主推进开发，由项目方直接调用 Codex 执行；开发必须遵守本 STANDARD 与 INDEX 要求的规范队列底线（工单三段式 + DoR 五项 + 全局主表登记 + WIP 上限 + 冻结门 + 打 tag 铁律 + 回执必报），禁止绕过规范裸跑。** 适用于全部现有与后续项目，包括 Manager 自身；UltimaManager 不再作为前置准入闸门，改为可选监督/审计工具，不阻塞产品推进。已受派 worker 仅在其正式契约内执行。

全局登记不等于准入，文档入口不等于授权；原目标、验收、预算、暂停及 Owner 冻结发布门继续有效。该条替代旧文档要求"必须经 Manager 统一调配"的表述，不自动改变历史回执或中止既有进程。规范入口见 [INDEX.md](INDEX.md) 与 [AGENTS.md](AGENTS.md)。

### 既有执行要求

1. **全链路**：需求 → 方案 → 工单 → 执行 → 验收 → 审计（不跳阶段、不省验收）
2. **工单纪律**：三段式（文件精确/写什么可执行/验收封闭清单 + 禁止清单）；每 T 验收门全绿 + 越界声明
3. **冻结门**：阶段报告产出 → AI 复核 → 冻结 tag（`stageN-frozen`），未冻结不进下一阶段
4. **数据同步**：状态/版本/评分变化 → 按触发点更新 `sync/product.json` → 双端同步（**不轮询**）
5. **审计**：对照治理体检基线（结构/文档/工单/验收/同步/活动），产出评分 0-100

## 五、落盘与同步标准（v2 · 具体操作）

> 本节解决"往哪推、用谁推、怎么验证授权、卡住怎么办"。每产品必须三端就绪：
> **GitHub 正式仓（代码）＋ GitHub 公开 Gist（product.json 免 token 主源）＋ Gitee 镜像仓（备份）**。

### 5.1 账号与凭证（不落明文）

| 端 | 账号/标识 | 凭证存放 | 说明 |
|---|---|---|---|
| GitHub | 组织 `Ultima-AI-Studio`；账号 `ArkExlabs` | gh CLI keyring（scope 含 gist） | 建仓/推送/Gist 均用 gh |
| Gitee | 空间 `Ultima-AI-Studio` | 环境变量 `GITEE_TOKEN`（32 字符） | 从 vault 取出后注入环境 |
| 凭证库 | `H:\UltimaAI\_shared\vault\vault.json.enc`（`vault.ps1` 管理） | 加密存储 | root/API key/token 一律存此，**不落明文于文档、仓库、聊天记录** |

> **授权三查（任何"没有授权"报错，先跑这三条再反馈）**：
> 1. **GitHub**：`gh api user --jq .login` 返回 `ArkExlabs` 即有效。`gh auth status` 报 token invalid 多为本机网络校验未走代理的误报：先设 `$env:HTTPS_PROXY="http://127.0.0.1:1080"`、`$env:HTTP_PROXY="http://127.0.0.1:1080"`（仅当 1080 代理在运行）再验证；确认失效才执行 `gh auth refresh -h github.com`（浏览器授权一次）。
> 2. **Gitee**：`$env:GITEE_TOKEN` 长度应为 32；缺失时从 vault 取出（`vault.ps1` 读取对应密钥），不向用户重复索要。
> 3. **出网通道**：本机 git / PowerShell 可直连 GitHub；gh / urllib 被网络设备拦截时，Gist 类调用改走 PowerShell `Invoke-RestMethod`（见 sync-dual.py 实现，勿改回 urllib 直连）。

### 5.2 仓库治理

- 组织根（`Ultima-AI-Studio`）**只允许项目同名仓**：`H:\UltimaAI\<Product>` 每个产品对应一个同名 GitHub 仓；备份/子工程放该仓 `backup/` 子路径，**禁止**在根下再建 `<Project>-backup` 等衍生仓。
- 可见性：默认**私有**（源码/文档/工单）；仅对外发布件公开（如 `UltimaDocs` 文档中心、`Ultima-Agent` Releases 通道）。
- Gitee 镜像命名：`<product>-sync`（全小写，如 `ultimaconsole-sync` / `ultimaradar-sync`），私有，全仓镜像。

### 5.3 怎么上传（标准动作）

**代码/文档落盘（产品根目录执行）：**
```
git add -A
git commit -m "<描述>"
git push origin main        # GitHub 正式仓（remote: origin）
git push gitee main         # Gitee 镜像（remote: gitee）
```

**首次建仓**：`git init` → `git branch -m master main` → `git remote add origin https://github.com/Ultima-AI-Studio/<Product>.git` → `git remote add gitee https://gitee.com/Ultima-AI-Studio/<product>-sync.git` → 提交推送。Gitee 首次推送遇 non-fast-forward 时先 `git pull --rebase gitee main` 再推。

**product.json 数据落盘（双端一次更新）：**
```
python sync-dual.py
```
脚本行为：GitHub Gist PATCH（免 token 匿名主源）＋ Gitee contents PUT（带 sha 更新 `sync/product.json`）。脚本位于产品根目录；缺脚本的产品按 `UltimaConsole/sync-dual.py` / `UltimaRadar/sync-dual.py` 复制改造（GIST_ID 与 GITEE_REPO 换成自己的）。

### 5.4 Gist 登记表（每产品一个公开 Gist 存 product.json）

| 产品 | Gist ID | 免 token 读取 URL |
|---|---|---|
| UltimaConsole | `5d0043cc6fd2441997c686a206053529` | https://gist.githubusercontent.com/ArkExlabs/5d0043cc6fd2441997c686a206053529/raw/product.json |
| UltimaRadar | `49007d6263d79ec13d5c0f6e108bd007` | https://gist.githubusercontent.com/ArkExlabs/49007d6263d79ec13d5c0f6e108bd007/raw/product.json |
| UltimaSkin | `f5ebd9599f5e6cb3601b5125a744cfda` | https://gist.githubusercontent.com/ArkExlabs/f5ebd9599f5e6cb3601b5125a744cfda/raw/product.json |
| 其他产品 | 建仓后回填本表 | — |

### 5.5 各产品落盘状态表（2026-10-20 核查）

| 产品 | GitHub 仓 | Gitee 镜像 | Gist | sync-dual.py | 待补缺口 |
|---|---|---|---|---|---|
| UltimaConsole | ✓ | `ultimaconsole-sync` ✓ | ✓ | ✓ | — |
| UltimaRadar | ✓ | `ultimaradar-sync` ✓ | ✓ | ✓ | — |
| UltimaAgent | ✓（公开发布通道） | 未建 | 未建 | ✗ | Gitee 镜像 + Gist + 脚本 |
| UltimaEngine | 未建 | 未建 | 未建 | ✗ | GitHub 仓 + 镜像 + Gist + 脚本 |
| UltimaGold | 未建 | 未建 | 未建 | ✗ | GitHub 仓 + 镜像 + Gist + 脚本 |
| UltimaScan | ✓（私有） | 未建 | 未建 | ✗ | product.json + 镜像 + Gist + 脚本 |
| UltimaSkin | ✓ | `ultimaskin-sync` ✓ | ✓ | ✓ | 看门狗暂缓（按需启用：项目启动后或 Owner 通知时再接入）；飞书灾备已建（URL 见产品 sync/README） |

### 5.6 执行端读取路径（不再索要授权/账号）

1. 读根标准本文件第五节（本文）；
2. 读本产品 `sync/README.md`「双端落盘方式」小节（Gist ID / 镜像仓 / 命令已写死）；
3. 凭证一律从 `_shared\vault` 取，不向用户重复索要；
4. 遇"没有授权"报错按 5.1 授权三查处理，处理不了再反馈。

### 5.7 触发点与验收（沿用 v1 定义）

| 项 | 标准 |
|---|---|
| 唯一模板 | 每产品 `sync/product.json`（结构遵循 `UltimaConsole/docs/product-sync-template.md`） |
| 触发点 | 版本冻结 / 版本发布 / 数据变更 / 用户指示同步（手动）＋ 常驻自动同步（见 5.8） |
| 动作 | 手动触发执行 sync-dual.py（见 5.3）；常驻自动同步走 5.8 看门狗 |
| 验收 | Gist 匿名可读 / Gitee 可更新 / GitHub 仓 main 最新 / 看门狗日志有最近成功记录 |

### 5.8 常驻同步机制（看门狗 · 15 分钟，2026-10-20 新增）

> 目的：Owner 离开本地后，客户端（Pad/手机，任意网络）仍能拿到最新任务状态。
> 链路：**本地推（看门狗 15 分钟）→ 云端存（Gist 免 token 主源 + Gitee 镜像）→ 客户端拉（15 分钟轮询 Gist）**；客户端无网络时有内置 seed 兜底。

**本地看门狗（Windows 计划任务，本地电脑）：**
- 脚本：`H:\UltimaAI\_shared\queue\watchdog-sync.ps1`（全局共享）。幂等：对比上次推送 hash，无变化跳过不空推；凭证：GitHub PAT（`github-pat`）与 Gitee token（`gitee-token`）均存加密 vault（`_shared\vault\vault.ps1` 管理），不落明文；Gist PATCH 必须用 UTF-8 字节 body（PS5.1 字符串 body 含中文会致 400）。
- 任务：`UltimaWatchdogSync`，每 15 分钟触发，cmd /c + 日志重定向，交互式令牌（当前用户已登录，vault/git 凭证可用）。
- 建任务命令：
  ```
  schtasks /create /tn "UltimaWatchdogSync" /tr "cmd /c powershell.exe -NoProfile -ExecutionPolicy Bypass -File H:\UltimaAI\_shared\queue\watchdog-sync.ps1 >> H:\UltimaAI\_shared\queue\watchdog-sync.log 2>&1" /sc minute /mo 15 /f
  ```
- 每次执行写审计日志 `H:\UltimaAI\_shared\queue\watchdog-sync.log`（SKIP/OK/WARN 可追踪）。
- 新接入产品：复制脚本改 `$ProductFile` / `$GistId` / `$GiteeRepo` 三项（Gist 免 token 主源见 5.4 登记表，Gitee 镜像命名见 5.2）。

**客户端轮询（App / 看门狗 UI）：**
- 每 15 分钟重新拉 Gist（免 token）刷状态：`setInterval(..., 15*60*1000)`，刷新后同步 AppStorage + 当前页 + 详情页选中对象（参考 `UltimaConsole/entry/src/main/ets/pages/Index.ets` 的 `startAutoRefresh`）。
- 无网络降级链：Gist 拉取失败 → RDB 本地快照 → 内置 seed（首次安装离线可用），见产品 `M1Runtime` 实现。

**边界**：电脑关机时段推送暂停，重启后计划任务自动恢复；需要"电脑关机也能同步"时，将脚本部署到 VPS（`198.13.46.208`，4核4G 未启用）做常驻兜底（从 GitHub 仓拉状态再推 Gist/Gitee）。

### 5.9 队列状态同步（防止 Console 数据源滞后 · 2026-10-20 新增）

> 背景事实：看门狗（5.8）**只推送** `sync/product.json`，**不生成**汇总。若 Agent/Console/Sentinel 派发 Codex 后未更新 product.json，客户端（鸿蒙）将一直显示旧队列状态（本次事故：Agent 20:51 续派宿主壳，product.json 仍为 20:07 旧数据，鸿蒙端无"执行中"）。

**规则（派发/回执后必做）：**

1. **每次 Codex 派发 / 回执 / 冻结变更后，必须同步更新对应产品 `sync/product.json`** 的 `queue` / `stage` / `summary`（主脑审计轮或当轮对话内完成，不得只更新全局主表）；
2. 更新路径：读全局主表 `_shared\queue\global-queue-index.md`（唯一权威汇总）→ 按产品更新 product.json `queue` 数组（工单 id + 状态：待派发 / 执行中 / 审计中 / 已冻结）→ 同步 seed 副本（`entry/src/main/resources/rawfile/product-seed.json`）→ 删除 `_shared\queue\.last-push.json` 强制重推（幂等 hash 会跳过未变更）；
3. **长期自动增量**：watchdog-sync.ps1 逐步增加"从 global-queue-index.md 增量读取各产品工单状态并合入 product.json"的步骤（生成职责从人工迁向看门狗，未实现前人工兜底）；
4. 验收：派发/回执后 **15 分钟内**，Gist 与 Gitee 的 product.json 含最新执行中状态，客户端轮询可见。

## 六、合规检查（治理体检 · 每产品按此自查）

- [ ] README + architecture.md 存在且最新（版本/状态同步）
- [ ] 方案文档已冻结（有版本号）
- [ ] 工单队列存在且状态真实（待派发/执行中/已冻结）
- [ ] 阶段报告 + 冻结 tag 齐全（stageN-frozen）
- [ ] 审计报告 + 评分存在（进 product.json）
- [ ] sync/product.json 字段符合模板规范（无未知字段）
- [ ] 双端同步可达（Gist 匿名可读 / Gitee 可更新）

## 七、违规范式（禁止）

- 未挂 Ultima 前缀却进入 Ultima 体系
- 无 README/architecture 的裸工程
- 跳过冻结门直接发布
- 定时轮询同步（必须事件触发）
- product.json 含模板外未知字段
