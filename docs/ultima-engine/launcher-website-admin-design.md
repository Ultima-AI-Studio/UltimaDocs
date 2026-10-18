# TuppoGame 官网 + 多游戏管理后台 设计方案（v0.3 裁定）

> 日期：2026-10-07（v0.1 草案 → v0.2 裁决落地 → v0.3 技术栈裁定）
> v0.3 裁定：① 后台采用**开源 admin 框架 Arco Design Pro Vue（字节跳动开源，MIT）** 改造，不重复造轮子；② 官网采用**纯 HTML/CSS/JS 完整版**（零构建直传 Pages），复用登录器设计语言 + Steam 式科技感游戏动效；③ 两者均接入既有 Worker API（tuppo-api）+ D1（tuppo-db）。
>
> **部署状态（2026-10-07 更新）**：官网完整版 V2 已上线 **https://sellerrule.com/**（Hero 粒子+轮播、游戏库 9 卡跑马灯光锥、最新动态、最新版本、中英切换、count-up 全部生效；API 数据打通——游戏库/版本/在线人数 2,240 均实时来自 tuppo-api，news 表空时回退静态）。**后台完整 CMS 已上线 https://admin.sellerrule.com/（Arco Design Pro Vue 改造版，Version 6a3487c5，index 9896fac7）**：登录、Dashboard（5 统计卡+游戏状态环形图+区服 Top10 柱状图）、游戏/区服/动态/版本/会员订阅/用户 6 个管理页全部可读写（新增/编辑/删除已验证）、SPA 直开路由（/games/list 等）正常。
>
> **CMS 部署方式（重要记录）**：
> - **根因修复**：上传页部署失败因 `_redirects` 文件 `/* /index.html 200` 被 Cloudflare 判为**无限循环**（`/index.html` 匹配 `/*`），部署被拒（PUT 400）。**修复**：删除 `_redirects`，改用 **wrangler 部署 + `not_found_handling = "single-page-application"`** 配置级 SPA 回退。
> - **⚠️ public/_redirects 必须保持删除**：vite build 会把 `public/` 下任何 `_redirects` 复制进 `dist/`，wrangler 部署时再次引爆 Infinite loop（code 100324，本次 2026-10-07 第二次踩坑）。改完代码构建后 deploy 前检查 `dist/_redirects` 不存在。
> - **wrangler 部署法**（已装 4.147.0 + OAuth 登录 exorcist.info@gmail.com）：`wrangler.toml`（name=tuppo-admin、[assets] directory=./dist、not_found_handling=single-page-application、html_handling=auto-trailing-slash）+ `npx wrangler deploy`。**纯静态部署不需要 main script**（带 `env.ASSETS.fetch` 的 script 会导致 SPA fallback 500）。
> - 部署产物：`web/admin-cms/arco-design-pro-vite/dist/`（index 9896fac7），线上 Version 6a3487c5（纯静态 SPA 版）。Worker API 对应 Version 35fc3238（active）。
> - 注意：Dashboard 上传页 zip 部署也可用（但不能带上述 _redirects；且其默认 not_found_handling=none 无 SPA 回退）。
>
> **后台细节完善（2026-10-07 定版，本次同步）**：
> - **编辑不再重复插入**：crud.vue 编辑走 PUT、id 字段编辑时 disabledOnEdit（主键禁改）；后端 games/plans/servers/news/versions 全部 `INSERT ... ON CONFLICT(id) DO UPDATE SET ...` UPSERT（本次为 servers/news/versions 补齐 id 绑定 + ON CONFLICT，news 补 img_zh/img_en；`b.id || null` 处理新增自增）。API 实测：news 8 条 → PUT id=8 编辑 → 仍 8 条（无重复），标题已还原。
> - **状态中文映射**：Column.tagMap + crud.tagText() 统一中文：games（已发布/即将发布/隐藏）、servers（正常/火爆/拥挤/维护）、news（显示/隐藏）、versions（强制 否/是）、plans（标准套餐/高级版）；select 选项文案同步中文化。
> - **users.vue 修复**：interceptor 已解包 `{ok,data}`，原 `r.data.data` 双重解包取到 undefined → 改 `r.data || []`；套餐/状态中文（标准套餐/高级版、正常）。
> - **表单校验**：crud.vue 保存前 formRef.validate()。

> 依据：登录器三层原型 v203 冻结版（`web/launcher-prototype/launcher.html`）设计体系；外部服务层审计（`docs/external-service-layer-audit.md`）；EXE 方案 v1.5（`docs/launcher-webview2-design.md`）。
> 定位：**游戏合集平台**的对外官网 + 运营方多游戏管理后台。不是单传奇，是 9 款游戏（后续可扩展）的统一平台。
> 开发方式：由 Doubao 直接推进编码（不再使用 Codex）。

---

## 1. 设计目标与范围

- 官网：玩家入口——了解平台/游戏、下载启动器、查看公告与更新日志。
- 后台：运营入口——管理多款游戏、区服、版本/更新、内容（轮播/公告/新闻）、用户、授权、数据。
- 两者共享同一设计体系与同一数据源（Cloudflare），与登录器接口同栈。
- 多游戏核心：**Game 为一级业务实体，所有业务对象挂 game_id**；平台级内容 game_id 为空。

## 2. 设计体系（复用登录器，不再新造）

| 令牌 | 值 | 用途 |
|---|---|---|
| `--bg` | `#0e1119` | 全局背景（深蓝黑） |
| `--panel` / `--panel2` | `#151927` / `#1b2133` | 卡片/面板 |
| `--line` | `#262d42` | 边框/分割线 |
| `--gold` / `--gold-hi` | `#c9a24b` / `#e6c87a` | 主强调色（按钮/标题/数值） |
| `--txt` / `--dim` | `#d8dae2` / `#8c92a4` | 正文亮白 / 次级文字 |
| `--danger`/`--success`/`--info` | `#c64c4c`/`#4caf6e`/`#4a8fd8` | 状态色 |
| 字体 | 中文微软雅黑；数字/日期 Symbol 字体 | 与登录器一致 |
| 圆角 | 卡片 14px、控件 9px | 与登录器一致 |
| 版本标签色 | 1.76 金 / 1.80 蓝 / 1.85 粉 | 与登录器第三层一致 |
| 状态灯 | 正常绿 / 拥挤黄 / 火爆红 / 维护灰 | 与登录器第三层一致 |

## 3. 官网前端设计

### 3.1 信息架构

```
官网（单页为主 + 少量子页）
├─ 首页
│   ├─ Hero：品牌徽章 + 「复古游戏中心，重拾青春岁月」+ 下载启动器（突出按钮 → R2 EXE）
│   ├─ 游戏库：9 款游戏卡片（复用登录器第二层卡片样式，点击进详情）
│   ├─ 最新动态：轮播/列表（launch_news，平台级 + 游戏级）
│   └─ 最新版本：更新日志（launch_changelog）
├─ 游戏详情页 /game/:key
│   ├─ banner（含标题/副标题/版本标签行，复用登录器第三层 banner 版式）
│   ├─ 简介 + 区服状态预览（实时，来自后端接口）
│   └─ 下载启动器
├─ 下载页 /download：启动器下载 + 更新日志 + 系统要求（Win10/11）
└─ 关于/帮助（轻量）
```

### 3.2 页面要点

- **首页游戏卡片**：与登录器第二层一致——封面图 + 磨砂标题蒙版 + 开始/即将发布按钮；已发布游戏点击进详情，未发布显示"即将发布"。
- **下载按钮**：全局唯一主 CTA，指向 R2 最新版安装包（`https://update.sellerrule.com/...`），版本号从 version.json 读取。
- **多语言**：沿用登录器 I18N 方案（zh/en 词典 + lang 参数），图片按语言配（img_zh/img_en）。
- **响应式**：PC 为主（游戏玩家场景），移动端降级为单列。

## 4. 多游戏管理后台设计

### 4.1 设计思想

- **Game 一级实体**：后台顶部常驻「游戏切换器」（全部 / 热血传奇 / 奇迹MU / …），切换后所有模块的数据与操作作用域随之切换。
- **模板化接入**：新游戏上线 = 后台加一行游戏记录 + 上传素材（logo/封面/banner/视频），无需改代码。
- **平台级 vs 游戏级**：公告/轮播/更新日志支持两种粒度——平台级（game_id 空，全站可见）与游戏级（挂具体游戏）。

### 4.2 模块清单（左侧导航）

| 模块 | 功能 | 多游戏维度 |
|---|---|---|
| 工作台 | 全局统计（游戏数/区服数/在线/今日下载）、待办（待审核） | 聚合 + 单游戏切换 |
| 游戏管理 | 游戏增删改/排序/上下架；logo/封面/banner/视频/简介/版本标签配置 | 列表本身 |
| 区服管理 | 区号/名称/版本标签/状态灯/在线人数/开服时间/维护开关/排序 | 每游戏独立列表 |
| 更新管理 | 启动器版本 + 各游戏客户端/补丁版本；包上传（R2）、sha256、强制更新开关、更新日志 | 每游戏 + 平台 |
| 内容管理 | 轮播图、公告（launch_news）、更新日志（launch_changelog）；多语言文案 | 平台级 + 游戏级 |
| 用户管理 | 玩家账号、封禁、在线状态、会员订阅（标准/高级/到期） | 聚合搜索 |
| 授权管理 | 商家授权签发/吊销/续期（独立签发，与引擎授权一致） | 平台 |
| 数据统计 | 下载量/安装量/在线趋势/区服热度 | 聚合 + 单游戏 |
| 系统设置 | 管理员、RBAC 角色、操作日志 | 平台 |

### 4.3 关键界面逻辑

- **区服管理列表**：直接复用登录器第三层行样式（一区 · 服务器名 + 版本实心标签 + 状态灯 + 在线人数右对齐），后台所见即玩家所见。
- **更新管理**：上传安装包到 R2 → 自动算 sha256 → 写 version.json / game_version → 控制 force 字段（强制更新）与 channel（stable/beta）。
- **内容发布**：填写 → 多语言字段（zh/en）→ 预览（复用登录器卡片样式）→ 发布（即刻对登录器/官网生效）。

### 4.4 权限模型（初期两级，后续扩）

- 超级管理员：全部模块。
- 运营/服主：按游戏授权（可管理指定游戏的区服、内容、更新）。
- 登录方式：邮箱 + 密码 + 2FA（复用账号中心，或后台独立账号体系，待裁决）。

## 5. 数据模型（核心表，D1 SQLite）

```sql
game(id TEXT PK, key TEXT UNIQUE, name TEXT, en_name TEXT, status TEXT, sort INT,
     logo TEXT, cover TEXT, banner TEXT, video TEXT, intro TEXT, ver_tag TEXT)

server(id INTEGER PK, game_id TEXT, zone INT, name TEXT, ver_tag TEXT,
       status TEXT, online INT, open_time TEXT, sort INT)  -- 状态: normal/crowded/hot/maintain

launcher_version(id INTEGER PK, channel TEXT, version TEXT, url TEXT, sha256 TEXT,
                 force INT, notes TEXT, created_at TEXT)   -- stable/beta

game_version(id INTEGER PK, game_id TEXT, channel TEXT, version TEXT, url TEXT,
             sha256 TEXT, force INT, notes TEXT, created_at TEXT)

launch_news(id INTEGER PK, game_id TEXT NULL, img_zh TEXT, img_en TEXT, title_zh TEXT,
            title_en TEXT, link TEXT, sort INT, status TEXT, created_at TEXT)

launch_changelog(id INTEGER PK, game_id TEXT NULL, ver TEXT, date TEXT, items_zh TEXT,
                 items_en TEXT, created_at TEXT)

user(id INTEGER PK, uid TEXT UNIQUE, nickname TEXT, email TEXT, pass_hash TEXT,
     tfa_secret TEXT NULL, status TEXT, created_at TEXT)

member_sub(user_id INTEGER PK, plan TEXT, expire_at TEXT)   -- 标准/高级
```

## 6. 技术架构（建议：Cloudflare 全家桶，零成本）

| 层 | 选型 | 说明 |
|---|---|---|
| 官网前端 | Cloudflare Pages | 静态站 + JS，CDN/HTTPS 免费 |
| 后台前端 | Cloudflare Pages（独立项目） | 与官网同设计体系 |
| 后端接口 | Cloudflare Workers | 官网/后台/登录器共用；servers/news/version/report/auth |
| 数据库 | Cloudflare D1（SQLite） | 免费 5GB，够用 |
| 文件存储 | R2（已有桶 tuppo-launcher） | 封面/视频/安装包，0 出口费 |
| 域名 | sellerrule.com（更新/API）、growthcalc.xyz（官网，待裁决） | 正式域名后置 |

> 备选：NestJS + MySQL（外部服务层审计 32 建议），需自购服务器，成本与维护更高；当前 Cloudflare 免费栈可覆盖全部需求，建议优先。是否坚持 NestJS 待裁决。

## 7. 与登录器的关系

- **接口同栈**：登录器 L3 对接的 servers/news/version/report 就是后台写入、官网读取的同一批 Workers 端点。
- **数据同源**：区服状态、版本号、公告在后台维护一次，登录器与官网同时消费。
- **更新链路**：后台「更新管理」上传 → R2 → version.json；登录器自动/手动/强制更新读取同一份。

## 8. 待裁决项

- [x] 后台技术栈：**Arco Design Pro Vue（开源，MIT）+ Worker API + D1**（v0.3 裁定，替代 NestJS 备选）
- [x] 官网交付形态：**纯 HTML/CSS/JS 完整版，零构建直传 Pages**（v0.3 裁定）
- [x] 官网域名：sellerrule.com（v0.3 已绑定 tuppo-site 生效）
- [x] 后台域名：admin.sellerrule.com（v0.3 已绑定 tuppo-admin 生效）
- [ ] 后台账号体系：独立后台账号 vs 并入账号中心（玩家/管理员统一）？
- [ ] 后台权限：初期是否引入服主（按游戏授权）角色？
- [ ] 官网子页：游戏详情页 / 下载页是否本轮一并做（或后续迭代）？

---

## 9. 本轮全绿实测与修复记录（v0.4，2026-10-07）

### 9.1 后端（tuppo-api，活动版本 79024b95）

- **根因修复**：ensureSchema() 从"仅 /init 分支调用"改为 **fetch handler 开头每次请求执行**（OPTIONS 之后），解决 5 新表 no such table（banner/game_charge/license/admin_log/wallet）。
- **全链路实测**（浏览器 fetch，wrangler 部署）：health_tables=18；/admin/login OK；9 个管理端点全 200；POST banner/license/charge 成功；DELETE 全 200；操作日志正常落库；公开端点 /banners /changelog /gversion /gcharges /license/verify 全 200。
- **用户注册**：/register 成功，**UID=10000001**（符合"UID 与默认用户名从 10000001 递增"锁定口径），昵称"我是一个菜鸟"。
- **用户管理端点实测**：金币 /admin/users/coin（coin=888 入账）✓；会员 PUT /admin/users（plan=premium/cycle=year/expire_at）✓；封禁/解封 /admin/users/ban（status banned→active）✓。

### 9.2 前端（tuppo-admin，活动版本 0485bd46）

- **根因修复：Arco 新版 a-table-column 子组件写法表格不渲染**（列头/行全空）→ 统一改为 **:columns 数组 + slotName 具名插槽**（crud.vue 同款已验证写法）：
  - users.vue：11 列（id/uid/nickname/email/plan/cycle/expire_at/coin/status/created_at/ops），实测表格渲染 + 搜索框 + 分页"共 1 条"。
  - settings.vue：管理员表 7 列 + 操作日志表 5 列，实测 admin@sellerrule.com 行与 8 条日志（新增/删除/封禁等动作）正常渲染。
- **crud.vue 修复**（上轮）：save() 新增走 POST、编辑走 PUT（无 id POST / 有 id PUT），实测轮播图新增（ID=2）与删除成功。
- **部署验证注意**：SPA 导航可能命中浏览器缓存旧 chunk，实测需带版本号硬刷新（?v=<version>）。

### 9.3 验证死路记录（勿重试）

- Cloudflare Worker 在线编辑器位于跨源 iframe（quick-edit-workers.devprod.cloudflare.dev），bu.find/点击/粘贴均不可达 → **一律走 wrangler 部署**。
- public/dist 内 _redirects 会导致 wrangler 部署 Infinite loop → 构建前确认不存在。
- wrangler 自定义 main + env.ASSETS.fetch 的 SPA 子路由 500 → 纯静态部署（无 main）。
- curl/node fetch/Invoke-WebRequest 宿主出站超时 → API 实测走浏览器 bu.js fetch 或 wrangler CLI。
