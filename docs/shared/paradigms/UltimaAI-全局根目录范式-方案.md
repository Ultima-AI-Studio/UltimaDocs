# UltimaAI 全局根目录范式（方案）

> 版本：v1.0 · 状态：待批准 · 适用范围：Ultima 全系 + Tuppo 系（改名并入）
> 本方案为 Ultima 开发体系的全项目根目录规范，批准后作为唯一权威源。

## 一、根目录定义

统一开发根目录为 **`H:\UltimaAI\`**。

- **UltimaAI** 为合成名，AI 与 Ultima **并列**，AI 不是 Ultima 的子目录。
- 所有 Ultima 系产品、以及并入的 Tuppo 系产品，一律在此根下建目录。
- 根目录之外不再另起任何产品开发路径（硬约束）。

## 二、目录骨架（每产品统一结构）

```
H:\UltimaAI\
├── <产品名>\              # 每个产品一个目录（Ultima 开头）
│   ├── docs\             # 技术档案（00-架构/01-接口/数据模型…）
│   ├── tasks\            # 任务与工单（工单-阶段X.md + 问题日志）
│   ├── reports\          # 审计报告（审计-工单X.md + 评分）
│   ├── ops\              # 市场运营档案（仅已上线产品）
│   ├── src\              # 代码
│   ├── artifacts\<版本>\  # 版本产物（只读归档）
│   └── sync\             # 标准制式导出区（JSON，喂给 GitHub）
├── _shared\              # 公共：能力注册表、规范、模板、范式
│   ├── registry.md       # 能力/组件注册表
│   ├── paradigms\        # 范式冻结区（本范式存档于此）
│   └── templates\        # 工单/审计/报告模板
└── _archive\             # 归档：迁移进来的旧产品/旧版本（只读）
```

## 三、命名规范

1. **根目录**：`UltimaAI`（唯一，固定）。
2. **产品目录**：一律 **Ultima 开头** + 产品名，如 `UltimaConsole`、`UltimaRadar`、`UltimaPay`、`UltimaEngine`。
3. **Tuppo 系改名**：所有 Tuppo 相关项目统一改为 Ultima 开头——`TuppoM2 / TuppoGame（MirServer 引擎及 Game 端）→ UltimaEngine`、`TuppoAU → UltimaGold`，存量路径与文档同步更名。
4. 目录/文件用中文语义名 + 统一编号（REQ/工单/审计），不散名、不混名。

## 四、存量整合规则

| 现有路径 | 目标 | 说明 |
|---|---|---|
| H:\Ultima Agent | H:\UltimaAI\UltimaAgent | 已有 docs/tasks 结构，保留迁移 |
| H:\UltimaRadar | H:\UltimaAI\UltimaRadar | 已有较规范结构，保留迁移 |
| H:\TuppoAU | H:\UltimaAI\UltimaGold | 改名并入（黄金推送项目） |
| H:\MirServer M2 Code（含 M2 引擎 + Game 端） | H:\UltimaAI\UltimaEngine | 改名并入（引擎与游戏端合一） |
| H:\DeliveryOptimization / driverpro / FriendAgentTest 等 | 评估后并入或归档 | 属 Ultima 开发体系的一并纳入 |

整合原则：
- 迁移到根下后统一 `docs/tasks/reports/ops/src/artifacts/sync` 结构
- 旧内容进 `_archive\` 只读，不就地散放
- 迁移过程留痕（迁移清单 + 时间）

## 五、三层数据架构（落地）

```
本地权威源（H:\UltimaAI\）→ GitHub 桥接（私有仓）→ 飞书备份（灾备）
```

| 层 | 角色 | 存什么 | 谁写 |
|---|---|---|---|
| 本地 H:\UltimaAI | 权威源 | 全部 | 豆包/执行端 |
| GitHub | 桥接中转 | docs+meta+src 现行版（私有仓） | 同步器自动推 |
| 飞书 | 云端备份 | 关键管理数据（档案/工单/审计/评分） | 豆包定时备份 |

### 5.1 GitHub 桥接与授权规范（2026-10-20 定版）

**① 组织与仓库清单**（统一 GitHub 组织 **Ultima-AI-Studio**，全部私有仓）

> **根路径命名规则（强制）**：组织根路径**只允许创建与项目同名的仓库**（如 `UltimaScan` / `UltimaConsole`）；项目的备份、文档等一律放同名仓库**内部子路径**（如 `UltimaScan/backup/`），禁止在根路径创建 `<项目>-backup` 之类的衍生仓库。

| 仓库 | 用途 | 同步来源 |
|---|---|---|
| `Ultima-AI-Studio/UltimaDocs` | 全局文档库（独立文档项目，项目同名库；范式/品牌/模板镜像） | `_shared\` + 各产品 `docs\shared\`（本地权威 → 镜像 → push） |
| `Ultima-AI-Studio/UltimaScan` | UltimaScan 项目仓库；**备份落 `backup/` 子路径** | `UltimaScan\scanner\backup_to_github.py`（REMOTE=org/UltimaScan.git，内容统一 `backup/` 前缀） |

**② 授权方式（统一，禁止散用）**
- 认证走**本机 Git Credential Manager（GCM）+ PAT**：`git config --global credential.helper manager`；日常 push/clone 免密由 GCM 管理（git config user：`ArkExlabs` / `ArkExlabs@users.noreply.github.com`）。
- **禁止**在脚本、代码、仓库内硬编码 token / PAT / 密码；敏感凭证一律入本地加密凭证库 vault（DPAPI 加密，见服务器台账）。
- 组织内仓库权限不足时走组织管理，不在代码里绕行。

**③ 三层同步流程（标准制式）**
```
本地权威（_shared\ + 产品目录）→ 复制到 ultima-docs-repo\docs\shared\ → git add/commit/push → 飞书导入/覆盖备份
```
- 镜像与 7 产品目录 `docs\shared\` 同步后再统一 push；品牌资产（brand\）同步 8 位置（镜像 + 7 产品）。
- 飞书侧：文档用 `lark-cli drive +import`（md→docx），图片/资产用 `drive +upload`（经 `C:\Users\Administrator\Doubao\lark-sync\` 中转，H:\ 路径不在 --file 白名单）。

**④ 失效/异常排查 SOP**
- `401` / `Authentication failed` → PAT 失效或 scope 不足 → 重新生成 PAT 写入 GCM（`git credential-manager` 或重跑一次交互认证）。
- `Repository not found` → **仓库不存在或当前账号无权限**（非网络问题）→ 用 GitHub MCP `create_repository` 在组织下创建（private=true），再重跑同步/备份脚本续推。
- 网络类失败 → 脚本保留本地 commit，网络恢复后重跑同命令自动续推（不丢数据）。
- 每日备份类脚本（如 backup_to_github.py）失败退出码非 0 时，查看其输出定位是凭证 / 仓库 / 网络哪一类，按上表处置。

**⑤ 新建仓库 SOP**
- 一律在组织 `Ultima-AI-Studio` 下创建、private=true；**仓库名与项目名一致**（禁止 `<项目>-backup` 类衍生名）；
- 项目内部子路径自行规划（如备份 → `backup/`、文档 → `docs/`）；
- 创建后登记进 ① 仓库清单 + 本范式，并在对应产品文档标注 remote 地址。

## 六、硬约束（治理体检项）

1. 所有新开发一律在 `H:\UltimaAI\` 下建目录，不得另起路径。
2. 产品目录必须 Ultima 开头；Tuppo 字样不再作为产品名。
3. 根之外产出 = 治理体检违规项（对应工程方法论 M2 写入域约束）。
4. 范式变更必须走评审，旧版归档 `_shared\paradigms\`。

## 七、执行步骤

1. 批准本方案 → 建立 `H:\UltimaAI\` 骨架 + `_shared\`（registry/paradigms/templates）。
2. 制定存量迁移清单（含 Tuppo 改名映射）。
3. 逐个迁移并留痕，更新各产品引用路径。
4. 本范式存档进 `_shared\paradigms\` + 范式存档总纲。
5. 治理体检新增「根目录合规」审计项。

## 八、待确认

- 无（改名映射已全部确认）。DeliveryOptimization、driverpro、FriendAgentTest 为 H 盘散落独立项目，不属于 Ultima 开发体系，**不纳入**整合范围。

## 九、落地状态（2026-10-17 校验）

迁移已完成：4 产品全部入根并改名（UltimaAgent / UltimaEngine / UltimaGold / UltimaRadar），源目录已清空。

### 结构合规对照（校验自检）

| 产品 | 范式骨架（docs/tasks/reports/ops/src/artifacts/sync） | 现状 | 缺口 |
|---|---|---|---|
| UltimaAgent | 应含 7 目录 | docs/execution/legacy-topo/logs/tasks/Topo Backup/README | 缺 reports/ops/src/artifacts/sync；execution/legacy-topo/Topo Backup 为存量目录 |
| UltimaEngine | 应含 7 目录 | 原 MirServer 结构（build/data/src/launcher…） | 缺 tasks/reports/ops/sync/artifacts |
| UltimaGold | 应含 7 目录 | 原 TuppoAU 结构（backend/ml-engine/mt5sdk…） | 缺 tasks/reports/ops/sync/artifacts |
| UltimaRadar | 应含 7 目录 | backend/frontend/docs/scripts/tests/README | 缺 tasks/reports/ops/sync/artifacts |

### 校验结论与更新项

1. **公共区未就绪**：`_shared\templates\` 为空（未放模板）；`_shared\registry.md` 不存在（未建能力注册表）——P1，需补建。
2. **产品骨架未统一**：4 产品均为存量原结构，未补建范式 7 目录——P1，允许逐步补齐（存量已登记，不阻塞；新增内容必须落范式目录）。
3. **存量目录处置**：UltimaAgent 的 execution/legacy-topo/Topo Backup 等存量目录，保留但不新增内容；后续按范式收敛或归档。
4. **新增内容硬规则**：从校验日起，任何产品新增的文档/任务/报告/产物，必须落范式目录（docs/tasks/reports/ops/src/artifacts/sync），存量原目录不再写新内容。

### 后续动作（P0/P1 待办）

- [ ] 补建 `_shared\registry.md`（能力注册表初始条目：4 产品 + 8 技能）
- [ ] 往 `_shared\templates\` 放模板（工单/审计/报告模板，取自工程方法论 references）
- [ ] 产品骨架逐步补齐：新建内容按范式落位，存量目录不再写新内容
- [ ] 治理体检 U1 根目录合规每次必查（已加进 Ultima-治理体检）
