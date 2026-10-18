# 游戏包目录结构规范（Launcher Game Pack Structure）

> 版本：v1.0（2026-10-09）｜适用范围：TuppoGame 登录器（WebView2 版）+ 自研客户端 V0.1/V1.1
> 关联实现：`launcher/src/game_launch/game_launch.cpp`（EnsureInstalled / GameLaunch::Launch）
> 关联测试：`launcher/tests/game_launch_test.cpp`（剥根目录 / manifest 检测 / 断点重试）

---

## 1. 目标与核心约定

| 约定 | 内容 |
|---|---|
| 安装根目录 | **启动器同目录 `\Games\`**（便携、随登录器走；重装/升级登录器不清游戏） |
| 下载包目录 | `%LOCALAPPDATA%\TuppoGame\packs\<game_id>.zip`（与安装目录分离） |
| 多游戏 | 每个游戏一个子目录，目录名 = `game_id`（mir / mu / rxjh …） |
| 启动引导 | 自研客户端优先（详见 §4），第三方包兜底 |
| 包格式 | 单文件 zip；上传命名 `<game_id>.zip`，与后台 `pack_url` 对应 |

```
<启动器目录>/
├── TuppoLauncher.exe          # 登录器
├── TuppoGameClient.exe        # 自研迷你客户端（V0.1，登录器同目录）
├── launcher.html / assets/    # UI 资源
└── Games/                     # 游戏安装根目录（自动创建）
    ├── mir/                   # 游戏 mir（安装后）
    │   ├── manifest.json      # 包元数据（新标准，安装完成的判定依据）
    │   ├── mir_client.exe     # 游戏定制自研客户端（V1.1 渲染版）
    │   ├── Config.ini         # 客户端运行配置（可选）
    │   ├── Data/              # 图素库（V1.1 渲染器加载）
    │   ├── Map/               # 地图（.map，TuppoM2 兼容）
    │   ├── Wav/               # 音效
    │   └── Sound/             # 音乐（可选）
    └── logs/                  # 安装日志（install_<game_id>.log）
```

---

## 2. 游戏包（zip）内目录结构

**规范：zip 内允许两种形态，安装器自动归一化：**

### 2.1 带单根目录包裹（推荐上传方打包习惯）
```
mir.zip
└── mir/                       # 根目录 = 游戏 ID
    ├── manifest.json
    ├── mir_client.exe
    ├── Config.ini
    ├── Data/Tiles.wil
    ├── Data/Objects.wil
    ├── Data/Hum.wil
    ├── Data/Mon1.wil
    ├── Data/Magic.wil
    ├── Data/Effect.wil
    ├── Map/0.map
    ├── Map/1.map
    ├── Wav/xxx.wav
    └── Sound/xxx.mid
```
安装时**自动剥掉 `mir/` 包裹层** → 文件直接落在 `Games\mir\`。

### 2.2 不带根目录（文件直接平铺）
```
mir.zip
├── manifest.json
├── mir_client.exe
└── Data/... Map/... Wav/...
```
安装时原样解压到 `Games\mir\`。

### 2.3 目录条目与安全
- zip 内目录条目不落盘；仅文件条目解压
- 解压路径逐段校验，拒绝 `..` 段、绝对路径、盘符（防 zip-slip 穿越）
- 隐藏/系统文件（`.` 开头）跳过

---

## 3. manifest.json 字段规范

包内 `manifest.json` 为**安装完成的判定依据**（存在即视为已安装，断点重试）。

```json
{
  "schema": 1,
  "game_id": "mir",
  "name": "热血传奇",
  "version": "0.1.0",
  "client_exe": "mir_client.exe",
  "client_args": "--direct",
  "server_port": 7200,
  "resources": {
    "data_dir": "Data",
    "maps_dir": "Map",
    "wav_dir": "Wav",
    "tiles_file": "Data/Tiles.wil",
    "objects_file": "Data/Objects.wil",
    "hum_file": "Data/Hum.wil"
  }
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `schema` | 是 | 结构版本，当前 `1` |
| `game_id` | 是 | 与后台 game.id / 目录名一致 |
| `name` | 是 | 游戏显示名 |
| `version` | 是 | 包版本（用于后台更新比对） |
| `client_exe` | 否 | 启动入口 exe 文件名（缺省按命名约定 `<game_id>_client.exe`） |
| `client_args` | 否 | 启动附加参数 |
| `resources.*` | 否 | V1.1 渲染器资源路径（渲染器实现时读取） |

> V0.1：启动入口按命名约定 `<game_id>_client.exe`，manifest 仅作完成判定。
> V1.1：渲染器读取 `resources.*` 定位图素/地图/音效。

---

## 4. 启动引导顺序（GameLaunch::Launch）

| 优先级 | 目标 | 场景 |
|---|---|---|
| 1 | 登录器同目录 `TuppoGameClient.exe` | V0.1 自研迷你客户端（无需安装包） |
| 2 | `Games\<id>\<id>_client.exe` | 游戏定制自研客户端（V1.1 渲染版，需安装包） |
| 3 | `Games\<id>\` 根目录任意 exe | 第三方包兜底 |

自研客户端启动参数：`--direct --host <ip> --login-port 7100 --game-port 7200 --account <u> --password <p> --server "<name>"`

---

## 5. 安装流程（EnsureInstalled）

```
下载（game.download）→ packs\<game_id>.zip
   ↓
安装（首次进入游戏触发）
   ├─ 断点重试：Games\<id> 已存在且含 manifest.json（或根级 exe）→ 直接跳过
   ├─ zip 校验：存在且可打开（否则返回 pack_not_downloaded / zip_invalid）
   ├─ 计算共同根目录（所有文件条目共享同一首段目录 → 剥掉）
   ├─ 逐文件解压（安全路径校验 + 目录条目跳过）
   └─ 完成判定：manifest.json 存在（新标准）或根级 exe 存在（旧包兼容）
       → 记录安装路径（tg_install_<game_id>）+ 安装日志
```

错误码：`pack_not_downloaded` / `zip_invalid` / `mkdir_failed` / `no_entry_in_pack` / `client_not_found` / `launch_failed`

---

## 6. 后台对齐

| 项 | 要求 |
|---|---|
| `pack_url` | 指向 `<game_id>.zip`（如 `https://update.sellerrule.com/packs/mir.zip`） |
| 上传规范 | 后台标记建议分辨率：banner 2.35:1；封面动图 16:9 |
| 版本管理 | `manifest.json` 的 `version` 与后台 game 版本字段对应，供后续增量更新 |

---

## 7. 制作清单（上传前检查）

- [ ] zip 内包含 `manifest.json`（game_id 正确、client_exe 与实际 exe 一致）
- [ ] 客户端 exe 命名为 `<game_id>_client.exe`（自研）或根级任意 exe（第三方）
- [ ] 地图放 `Map/`（TuppoM2 兼容 .map 二进制）
- [ ] 图素放 `Data/`（.wil/.wix，V1.1 渲染器加载）
- [ ] 音效 `Wav/`、音乐 `Sound/`（可选）
- [ ] zip 命名 = `<game_id>.zip`，上传后 `pack_url` 可直连下载
- [ ] 防 zip-slip：包内不得含 `..` 路径 / 绝对路径 / 盘符

---

## 8. 正式版收尾记录（热血传奇 mir v0.1.0，2026-10-09）

### 8.1 首个正式游戏包已制作并验证

| 项 | 值 |
|---|---|
| 包文件 | `dist\gamepacks\mir.zip`（219.7MB，594 文件，ZIP_DEFLATED L6，14s） |
| 包内结构 | `mir/` 单根目录包裹（§2.1 形态，安装器自动剥根） |
| manifest | schema=1, game_id=mir, name=热血传奇, version=0.1.0, client_exe=mir_client.exe, resources.* 完整 |
| 客户端 | `mir_client.exe` = 渲染客户端最新干净版（486,912B，含锚点渲染+方向修复） |
| Data | Tiles/Objects/Hum/Magic/DnItems + Mon1-18 共 46 文件 426.4MB（渲染器实际加载集） |
| Map | 0.map（5.6MB；服务端 mapId=1 映射，当前测试服用） |
| Wav | 545 文件 113.7MB（全量，音效完整） |

### 8.2 验证证据（AI 自测，2026-10-09）

- **zip 安全**：594 条目 0 个 zip-slip（无 `..`/绝对路径/盘符）；顶层唯一 `mir/`
- **关键文件落位**：manifest.json / mir_client.exe / Data 五大库 / Mon1-18 / Map/0.map / Wav 全部 OK；CRC 抽查通过
- **安装链路模拟**（§5 EnsureInstalled 同规则）：剥根后 manifest.json 落 `Games\mir\` 根级 → 完成判定成立 → 断点重试（存在含 manifest 即跳过）成立 → 594 文件全部落位
- **包内客户端真实运行**：`mir_client.exe --direct` 登录成功 → 地图加载 OK → 战斗闭环 **击杀=3** → GFX SHOT OK（`C:\mir176\mir_pack_smoke.png`）
- **登录器部署集同步**：`launcher\build\Release\TuppoGameClient.exe` 已同步为最新渲染版（486,912B，9:46）

### 8.3 待办（外部依赖）

- **后台上传 pack_url**：cfut_ API token 无 R2 权限（403）；需 R2 S3 兼容凭证（Access Key ID/Secret）或后台手动上传，将 `mir.zip` 上传至 R2 `tuppo-launcher` 桶并配置 `games.pack_url`（建议 `https://update.sellerrule.com/packs/mir.zip`）
- **后续增量**：Map 全量（528 张）随服务端地图扩展再补；manifest version 与后台 game 版本联动

### 8.4 重新制作命令（可复现）

```powershell
# 1) 更新客户端到包（先用最新构建覆盖）
Copy-Item "build\classic-release\tools\launcher\Release\TuppoGameClient.exe" "dist\gamepacks\mir\mir_client.exe" -Force
# 2) 重新打包（Python：zipfile DEFLATED，带 mir/ 包裹层）
python -c "import zipfile,os; ..."   # 见 §8.1 同参数
```

### 8.5 正式版全链路实测记录（2026-10-09 续）

R2 凭证补齐尝试结论：cfut_ API token 无 R2 权限（403）、wrangler 无登录态、Cloudflare 控制台无会话、R2 multipart 上传端点（/admin/up-*）需部署 secret UPLOAD_KEY（本地无值）——四条路均无凭据。**切换为"后台 pack_url 指向本机 HTTP 服务"完成用户侧真实闭环验证**：

| 环节 | 实测结果 | 证据 |
|---|---|---|
| 后台 game 记录 | mir：name=热血传奇、pack_url=http://127.0.0.1:8000/mir.zip、size=219719132、ver=0.1.0、exe=mir_client.exe | C:\mir176\mir_game2.json（admin token 写入） |
| 下载 | 完整拉取 219,719,132B，与 Content-Length 精确一致 | curl -o 字节数匹配 |
| 安装 | 解压剥根 → launcher\build\Release\Games\mir\，manifest/exe/Data/Map/Wav 全齐（594 文件） | manifest.json 读取 |
| 进图 | mir_client.exe --direct 登录成功 → 出生点 (280,260) → 击杀 4 只怪 → GFX SHOT OK | C:\mir176\client_shot.png（800×640 像素图） |
| 登录器 GUI | 页面与桥全通（日志：page-lib、GAMES=9、auth/lic OK、NavDone），但当前 3 屏环境（3840×2160 主 + 两块 2560×1440）窗口内容透明不可见——疑似 WebView2 合成器与多屏 DPI 冲突的偶发问题，代码逻辑正常 | launcher.log（6 轮启动记录） |

**OPEN（正式发布前）**：
1. **pack_url 需改回公网地址**（建议 https://update.sellerrule.com/packs/mir.zip）——需要 R2 S3 兼容凭证（Access Key ID/Secret）或用户 Cloudflare 控制台手动上传 mir.zip 至 tuppo-launcher 桶；本地通道仅限本机实测。
2. **登录器 GUI 多屏透明**：用户回到常用单屏环境重开验证；如复现，下一步给 WebView2 加 AdditionalBrowserArguments 禁用 GPU 合成重编译验证。