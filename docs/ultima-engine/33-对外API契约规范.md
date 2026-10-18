# TuppoGame 对外 API 契约规范 v1.0（登录器 / 官网消费端）

> 日期：2026-10-07 · 对应后台设计 `launcher-website-admin-design.md` v0.4 · 对应登录器设计 `launcher-webview2-design.md` v1.5
> 本文件为 **登录器 L3 数据接入与官网消费的契约唯一真源**；契约变更需同步三端（登录器 / 官网 / 后台写侧）。

## 1. 总览

| 项 | 值 |
|---|---|
| API Base | `https://tuppo-api.exorcist-info.workers.dev`（生产；登录器 Net 模块可配置） |
| 响应包络 | 成功 `{ok:true, data:...}`；失败 `{error:"<code>"}`（HTTP 400/401/404/409/500） |
| 鉴权 | **公开端点**：无需 token；**管理端点** `/admin/*`：`Authorization: Bearer <token>`（后台登录获得，3 天有效） |
| 编码 | UTF-8，`Content-Type: application/json`；CORS 全放开（桌面端 WebView2 无同源限制） |
| 版本 | 契约版本 v1.0；端点只增不改（破坏性变更必须升契约版本） |

## 2. 登录器消费矩阵（三层 → 端点）

| 登录器层 | 数据 | 端点 | 状态 |
|---|---|---|---|
| 第一层 | 轮播图 | `GET /banners[?game_id]` | ✅ 已上线 |
| 第一层 | 最新动态（卡片轮播） | `GET /news[?game_id]` | ✅ 已上线 |
| 第一层 | 更新日志（最新版本区块） | `GET /changelog[?game_id]` | ✅ 已上线 |
| 第一层 | 最新版本号展示 | 登录器更新 manifest（R2，见 §8） | ✅ 已上线 |
| 第二层 | 游戏库列表 | `GET /games` | ✅ 已上线 |
| 第二层 | 荣誉馆 | 规划中（沿用 /games + 本地成就），本轮占位 | ⏳ 后续 |
| 第二层 | 集市 | 建设中，占位 | ⏳ 后续 |
| 第三层 | 服务器列表 | `GET /servers?game_id=<id>` | ✅ 已上线 |
| 第三层 | 单服实时状态 | 轮询 `/servers`（L3 起）；实时推送后续 | ✅ 已上线 |
| 用户侧 | 注册 | `POST /register` | ✅ 已上线 |
| 用户侧 | 登录（含两步认证） | `POST /login` | ✅ 已上线 |
| 用户侧 | 金币余额 / 会员信息 | `/member`、`/wallet`（用户侧视图，待补） | ⏳ 后续 |
| 授权侧 | 商家授权/游戏授权校验 | `GET /license/verify?email&game_id` | ✅ 已上线 |
| 消费侧 | 游戏点卡点券列表 | `GET /gcharges?game_id` | ✅ 已上线 |
| 消费侧 | 游戏版本 | `GET /gversion?game_id&channel` | ✅ 已上线 |

## 3. 端点契约

### 3.1 `GET /games` — 游戏库

参数：无。返回 `data: Game[]`：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | string | 游戏标识（mir/mu/bwdl/rxjh/jtdd/yt2/sqsd/xjro/qn） |
| key | string | 唯一键（同 id） |
| name | string | 中文名，如《热血传奇》 |
| en_name | string | 英文名（MU 等） |
| status | string | active / hidden（hidden 不展示） |
| sort | int | 排序 |
| logo | string | 品牌徽章 PNG（登录器第二层卡片中心图） |
| cover | string | 封面图（卡片背景，静态帧） |
| banner | string | banner 图（第三层顶部） |
| video | string | 封面视频（卡片悬停播放，可为空） |
| intro | string | 简介 |
| ver_tag | string | 版本标签（1.76/1.80/1.85…） |
| pack_url | string | 游戏包 URL（zip，Beta 静默下载源） |
| pack_size | int | 包大小（字节，安装进度计算源） |
| pack_version | string | 包版本（如 `0.1.0-beta`；后台"游戏管理"可配） |
| launch_exe | string | 启动程序相对路径（如 `mir_client.exe`；解压到 `Games/<game_id>/` 后由登录器拉起） |

> 登录器映射：卡片背景 cover → 悬停 video；中心徽章 logo；标题 name；"即将发布"判定 = status ≠ published（后台 game 表暂以 active/coming 表达，coming 显示"即将发布"按钮）。Beta 通道：`pack_url` 为空 → 隐藏下载；安装根 = 启动器 exe 同目录 `Games/<game_id>/`（见 `launcher-webview2-design.md` §17）。

### 3.2 `GET /servers?game_id=<id>` — 服务器列表

参数：`game_id`（缺省 mir）。返回 `data: Server[]`（按 zone 升序）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键 |
| game_id | string | 所属游戏 |
| zone | int | 区号（1..20；显示名 = `一区 · 服务器名`，区号转中文数字，分隔为"空格·空格"） |
| name | string | 服务器名（≤4 字） |
| ver_tag | string | 版本号（1.76 / 1.80 / 1.85，阿拉伯数字） |
| type | string | **复古 / 扩展**（本轮补列；后台表单可配） |
| exp_rate | int | 经验倍率（显示 `Nx`，N 为整数；支持 1x/2x/3x/4x/5x…） |
| drop_rate | int | 掉落倍率（同 exp_rate 显示规则，支持 10x 等） |
| mall | int | 商城（1=有商城，0=无；无商城显示"无商城"标签） |
| tags | string | **逗号分隔标签**（本轮补列；如"原汁原味,新开区"） |
| status | string | normal / crowded / hot / maintain |
| online | int | 在线人数（右对齐展示） |
| open_time | string | 开服时间 `YYYY-MM-DD`；**新开区判定：登录器端计算 now−open_time ≤ 3 天** |
| sort | int | 排序 |

**状态灯映射（登录器第三层）**：

| status | 灯色 | 文案 |
|---|---|---|
| normal | 绿 | 正常 |
| crowded | 黄 | 拥挤 |
| hot | 红 | 火爆 |
| maintain | 灰 | 维护（不可进入；点"进入游戏"弹提示） |

**类型/倍率标签顺序**（用户口径）：① 类型（复古/扩展）→ ② 经验 Nx → ③ 掉落 Nx → ④ 商城（"商城"或有/无）。版本号标签独立一列（实心标签，1.76 黄 / 1.80 蓝 / 1.85 粉）。

### 3.3 `GET /news[?game_id]` — 最新动态

参数：`game_id` 可选（不传 = 全站）。返回 `data: News[]`（status=active，按 sort,created_at 倒序，LIMIT 10）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键 |
| game_id | string | 所属游戏（'' = 全站） |
| title_zh / title_en | string | 标题（登录器按当前语言取 zh/en） |
| summary | string | 摘要（卡片副文案） |
| img_zh / img_en | string | 卡片图（多语言图后置：当前语言图缺失时降级取另一语言图） |
| link | string | 点击跳转链接（每图可点，打开对应内容页） |
| sort | int | 排序 |

### 3.4 `GET /changelog[?game_id]` — 更新日志

参数同 /news。返回 `data: Changelog[]`（date 倒序 LIMIT 10）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键 |
| game_id | string | 所属游戏 |
| date | string | 日期 |
| content | string | 日志内容 |
| sort | int | 排序 |

### 3.5 `GET /banners[?game_id]` — 轮播图

参数同 /news。返回 `data: Banner[]`（status=active，按 sort）：

| 字段 | 类型 | 说明 |
|---|---|---|
| id | int | 主键 |
| game_id | string | 所属游戏（'' = 全站） |
| img_zh / img_en | string | 轮播图（登录器按语言取；图内文字按语言人工出图） |
| link | string | 点击跳转链接（每图可点） |
| sort | int | 排序 |

### 3.6 `GET /gversion?game_id&channel` — 游戏版本

参数：`game_id`（缺省 mir）、`channel`（stable/beta，缺省 stable）。返回 `data: GameVersion | null`：

`{ version, url, sha256, force, notes, created_at }`（版本号/下载/哈希/强制/说明/时间）。

### 3.7 `GET /gcharges?game_id` — 游戏点卡点券

参数：`game_id`。返回 `data: Charge[]`（status=active）：`{ id, game_id, name, type(card/point), amount, price, sort, status }`。

### 3.8 `GET /license/verify?email&game_id` — 授权校验

参数：`email`（必填）、`game_id`（选填）。返回：

```json
{ "ok": true, "valid": true|false,
  "data": { "id": 1, "name": "...", "game_ids": "*|mir,mu", "expire_at": "2027-..", "status": "active" } | null }
```

口径：`valid = 未过期 && 授权含该游戏`；无授权记录 → `valid:false, data:null`。

### 3.9 `POST /register` — 用户注册

Body：`{ email, password(≥6), nickname? }`。成功返回 `{ok:true, data:{uid, nickname, email, coin}}`。
规则：**UID 从 10000001 递增**（`用户`+8 位数字为默认昵称）；昵称上限 6 汉字长度字符；错误：`email_exists`(409) / `invalid_input`(400)。

### 3.10 `POST /login` — 用户登录（含两步认证）

Body：`{ email, password, code? }`。返回 `{ok:true, data:{ token, user:{uid,nickname,email,plan,cycle,expire_at,coin,twofa,tfa_enabled,sub} }}`（`tfa_enabled`/`sub` 为 `twofa` 同义兼容字段）。
两步认证口径（登录器）：默认不显示验证码输入 → 提交账号密码后若 `user.twofa=true`（**此时响应不含 token**）→ 转步骤二（输入谷歌验证器 code）→ 再提交完成登录；未开通直接登录成功。code 错误 → `bad_code`(401)；未传 code → 返回 `user`（无 token）。

### 3.11 `POST /register/send-code` — 注册验证码

Body：`{ email }`。向邮箱发送 6 位注册验证码（10 分钟有效，一次性）。错误：`email_exists`(409) / `mail_not_configured`(503)。

### 3.12 `POST /forgot/send-code` — 找回密码验证码

Body：`{ email }`。向已注册邮箱发送重置验证码。错误：`no_user`(401) / `mail_not_configured`(503)。

### 3.13 `POST /forgot/reset` — 找回密码重置

Body：`{ email, code, password(≥6) }`。校验验证码后重置密码。错误：`bad_code`(401，含 `expired`) / `no_user`(401) / `mail_not_configured`(503)。
口径：**注册时若 body 携带 `code`，后端同步校验注册验证码**（`/register` 扩展字段），`bad_code`(401)。

### 3.14 `GET /me` — 当前用户信息（Bearer）

Header：`Authorization: Bearer <token>`。返回 `{ok:true, data:{uid,nickname,email,tfa_enabled,coin,sub:{plan,cycle,expire_at}}}`。错误：`unauthorized`(401)。

### 3.15 `POST /me/password` — 修改登录密码（Bearer）

Body：`{ old, next(≥6) }`。旧密码 PBKDF2 校验后更新。错误：`bad_password`(401) / `invalid_input`(400)。

### 3.16 `GET /me/sessions` — 登录设备列表（Bearer）

返回 `{ok:true, data:[{token,kind,created_at,expire_at}]}`（按时间倒序，≤20 条）。第一条为当前设备。

### 3.17 `POST /me/sessions/kill` — 下线指定设备（Bearer）

Body：`{ token }`。删除该会话。错误：`not_found`(404)。

### 3.18 `POST /me/mail/send-code` — 换绑邮箱验证码（Bearer，两步）

Body：`{ email, step:"old"|"new" }`。step=old 校验 email=当前绑定邮箱（`not_current`(400)）；step=new 校验新邮箱未占用（`email_exists`(409)）。错误：`mail_not_configured`(503)。

### 3.19 `POST /me/mail/rebind` — 确认换绑（Bearer）

Body：`{ old_email, old_code, new_email, new_code }`。双码校验后更新绑定邮箱。错误：`bad_old_code`(401) / `bad_new_code`(401) / `mail_not_configured`(503)。

### 3.20 `POST /me/twofa/enable` — 两步验证开启（Bearer，第 1 步）

返回 `{ok:true, data:{secret}}`（TOTP 密钥，供谷歌验证器录入）。该 secret 同时作为本次开启的邮箱确认码（`f2a_pending`），**不依赖邮件**。错误：`unauthorized`(401) / `already_enabled`(409)。

### 3.21 `POST /me/twofa/confirm` — 两步验证开启确认（Bearer，第 2 步）

Body：`{ code(上一步返回的 secret), totp(谷歌验证器 6 位动态码) }`。双校验通过后写入 `tfa_secret`。错误：`bad_code`(401) / `bad_totp`(401) / `not_pending`(400)。

### 3.22 `POST /me/twofa/disable` — 两步验证关闭（Bearer）

Body：`{ totp }`。TOTP 校验通过后清除 `tfa_secret`。错误：`bad_totp`(401)。

### 3.23 `GET /plans` + `POST /me/sub/order` — 套餐与会员开通（金币支付）

`GET /plans` 返回 `["standard/0/0","premium/58/498"]`（key/月价/年价，单位：**金币**）。
`POST /me/sub/order` Body：`{ plan:"premium", cycle:"month"|"year" }`。服务端校验 `wallet.coin >= 面额`：不足返回 `402 insufficient_coin{need,coin}`；充足则扣金币 → `coin_transaction(delta=-面额, reason='sub:premium')` → `member_sub(plan,cycle,expire_at)` 到期叠加 → `sub_order(plan,cycle,amount,status)` 订单流水。返回 `{ok:true, data:{plan,cycle,expire_at,coin}}`。错误：`unauthorized`(401) / `bad_plan`(400) / `insufficient_coin`(402)。
口径：**卡密充值得到的是金币，金币再用于开通会员/购买游戏点卡**；卡密不直接开会员。

### 3.24 `POST /report` — 登录器上报（公开）

Body：`{ kind:"boot"|"enter"|"leave"|"error"|"install"|"update", game_id?, server_id?, ver?, os?, detail? }`。
写入 `launcher_report` 表（后端 `created_at` 自动）。返回 `{ok:true}`。口径：登录器在启动/进服/退服/错误/安装/更新节点静默上报；后台"上报统计"页按类型与近 24h 聚合展示。

### 3.25 `GET /me/wallet/trans` + `GET /me/sub/orders` — 用户侧流水（Bearer）

`/me/wallet/trans` 返回当前用户 `coin_transaction` 流水（时间倒序）：`{delta,balance,reason,created_at}`。
`/me/sub/orders` 返回当前用户 `sub_order` 记录：`{plan,cycle,amount,status,created_at}`。
错误：`unauthorized`(401)。

### 3.26 `POST /admin/upload` — 图片上传（管理端 Bearer）

Body：`{ name, mime, data_b64 }`（base64 图片，≤8MB）。写入 R2 桶 `tuppo-launcher` 的 `assets/<ts>-<name>`，返回 `{ok:true, data:{url:"https://update.sellerrule.com/assets/..."}}`。
口径：后台表单 upload 字段（游戏 Logo/封面/Banner、动态图等）统一走此端点；URL 可直接用于登录器/官网展示。

### 3.27 `GET /admin/reports` — 上报查看（管理端 Bearer）

返回 `{ok:true, data:{list:[...], by_kind:[{kind,n}], last_24h:n}}`。`list` 按时间倒序 LIMIT 200。

### 3.28 `GET /admin/orders` — 订阅订单查看（管理端 Bearer）

返回 `{ok:true, data:[{id,user_id,plan,cycle,amount,status,created_at,uid,email}]}`（JOIN user，时间倒序 LIMIT 200）。

### 3.29 `POST /admin/users/coin` — 金币调整（管理端 Bearer，扩展）

Body：`{ user_id, coin, reason? }`。将目标用户余额**调整为** `coin`，并写入 `coin_transaction(delta=新-旧, balance=新, reason)`。返回 `{ok:true}`。口径：后台"用户管理"余额调整统一走此端点，流水可在用户侧 `/me/wallet/trans` 与后台日志追溯。

### 3.30 `POST /me/card/redeem` — 卡密兑换（用户端 Bearer，按卡型分流）

Body：`{ secret:"XXXX-XXXX-XXXX-XXXX" }`（16 位卡密，大小写不敏感）。服务端按 secret 查 `vip_card`：不存在 → `404 card_not_found`；`status` 非 `new/sold`（已使用/已作废）→ `400 card_used`。校验通过后按卡型分流：

- **充值卡（plan='coin'）**：金币入 `wallet.coin += amount` → `coin_transaction(delta=amount, reason='card_redeem:code')` → 卡置 `used` 并绑定 `user_id/used_at`。返回 `{ok:true, data:{plan:'coin', delta, coin, card}}`。
- **会员卡（plan='premium'）**：直接开通高级版会员——`member_sub` 按 `cycle`（month=30 天 / year=365 天）**在现有到期时间上叠加**（无订阅则从当前起算），写入 `sub_order(plan='premium', cycle, amount, status='paid')`，**不产生金币流水、不扣金币**。返回 `{ok:true, data:{plan:'premium', cycle, delta:0, coin, expire_at, card}}`。

口径：**两条会员开通路径等效**——金币支付订阅（3.23）与会员卡兑换（本端点）均走同一 `member_sub` 叠加逻辑；充值卡兑的是金币（金币是消费用的）。

### 3.31 `POST /admin/cards/generate` — 批量生成虚拟卡（管理端 Bearer，支持充值卡/会员卡）

Body：
- **充值卡**：`{ count:1~500, plan:'coin', amount:金币面额 }`。`amount` 必填 1~100000（档位 50/100/500/1000/2000），非法 → `400 invalid_amount`。插入 `vip_card(plan='coin', cycle='once', amount, status='new')`。
- **会员卡**：`{ count:1~500, plan:'premium', cycle:'month'|'year' }`。`amount` 由服务端按 `subscription_plan` 定价自动取（月 58 / 年 498），**不接受自定义面额**；`cycle` 缺省按 `month`。插入 `vip_card(plan='premium', cycle, amount, status='new')`。

返回 `{ok:true, data:{count, amount, plan, cycle, cards:[{code,secret}]}}`（实际插入张数）。
口径：**充值卡 ≠ 会员卡**——充值卡兑换后得金币（3.30 coin 分支）；会员卡兑换后直接开通高级版（3.30 premium 分支），与金币支付订阅（3.23）等效。

### 3.32 `GET /admin/cards/list` — 卡列表（管理端 Bearer）

Query：`?status=new|sold|used|void&cycle=month|year&page&size`（size 上限 500）。返回 `{ok:true, data:{list:[{id,code,secret,plan,cycle,amount,status,user_id,used_at,created_at,uid,email}]（LEFT JOIN user）, total, page, pageSize}}`，按 `id DESC` 排序。

### 3.33 `POST /admin/cards/void` — 作废卡（管理端 Bearer）

Body：`{ ids:[number,...] }`。仅 `status IN ('new','sold')` 的卡被置 `void`（已用/已作废跳过）。返回 `{ok:true}`。错误：`invalid_input`(400)。

### 3.34 `GET /admin/cards/export` — 导出卡密 txt（管理端 Bearer）

Query：`?status`。返回 `text/plain` 附件（`vip_cards.txt`）：首行注释 `# TuppoGame 虚拟卡清单  code  secret  plan  cycle  amount  status  created_at`，每行 `code secret plan cycle amount status created_at` 双空格分隔，按 `id` 升序。口径：发卡渠道（闲鱼自动发货）直接读取该文件。

### 3.35 管理端通用 CRUD `/admin/:res`（管理端 Bearer）

后台各管理页面（游戏/区服/动态/更新日志/轮播/套餐/点卡/授权/管理员/日志/用户）统一走 `GET /admin/games|servers|news|changelogs|banners|plans|charges|licenses|admins|logs|users` 与 `POST|PUT /admin/:res`（写操作以 `{id}` 判定新建/更新，主键 `id` 冲突即 UPSERT）。

- `GET`：整表读取（各资源按业务排序，见下）。`users` 为聚合视图（JOIN member_sub/wallet，含 `coin`、`plan`、`cycle`、`expire_at`）。
- `POST|PUT`：按资源各自校验必填（games 需 `key,name`；servers 需 `game_id,zone`；news 需 `title_zh`；versions 需 `version`；gversions 需 `game_id,version`；changelogs 需 `ver,items_zh`；banners 需 `title_zh` 等），UPSERT 后写 `admin_log`，返回 `{ok:true}`。
- `DELETE /admin/:res?id=<id>`：按主键删除，写 `admin_log`，返回 `{ok:true}`。
- 通用错误：`invalid_input`(400)、`unauthorized`(401)、`no_such_table`(500)。

### 3.36 `POST /me/charge/buy` — 集市金币购买游戏点卡/点券（用户端 Bearer）

Body：`{ game_id:"mir", charge_id:1 }`。服务端校验 `game_charge` 商品（`id+game_id` 且 `status='active'`）与 `wallet.coin >= price`：不足 → `402 insufficient_coin{need,coin}`；商品不存在/下架 → `404 not_found`。通过后：扣 `wallet.coin -= price` → `coin_transaction(delta=-price, reason='charge:<game>:<name>')` → `charge_buy(user_id,game_id,charge_id,name,amount,price)` 购买记录。返回 `{ok:true, data:{name, amount, price, coin}}`。错误：`unauthorized`(401) / `invalid_input`(400) / `not_found`(404) / `insufficient_coin`(402)。
口径：**集市 = 金币消费场景**——充值卡兑换得金币（3.30 coin 分支）→ 金币购买游戏点卡/点券（本端点）/ 金币开通会员（3.23）；点卡购买记录落 `charge_buy` 表，后台可扩展查询。

### 3.37 `GET /assets` — 荣誉馆公开资产库（公开）

返回 `{ok:true, data:[{key,name,name_en,type,rarity,limited,total,image,sort}]}`（仅 `status='active'`，按 `sort,id` 升序）。口径：`type='avatar'|'badge'`——头像属性可作个人头像，勋章属性不可作头像；登录器展品/头像选择网格均以本端点为数据源。

### 3.38 `GET /me/items` — 我的荣誉展品（用户端 Bearer）

返回 `{ok:true, data:[{asset_key,no,name,name_en,type,rarity,limited,total,image,sort}]}`（JOIN honor_asset，仅 active，按 `sort,id`）。口径：`no` 为该资产发放序号（如 No.1 初心 = `no:1`，限量 `total:1000` 显示为 `1/1000`）；注册新用户自动发放 `n1`（初心·幼龙守护灵，`no`=已发数+1，cap=`total`），资产缺失时静默跳过。

### 3.39 `POST /me/avatar` — 设置头像（用户端 Bearer）

Body：`{ asset_key:"n1" }`。服务端校验：资产存在且 active → `404 no_asset`；`type!=='avatar'`（勋章不可作头像）→ `400 not_avatar`；未持有 → `403 not_owned`。通过后写 `user.avatar=key`，返回 `{ok:true, data:{avatar, image}}`。口径：个人中心换头像 → 从荣誉馆已解锁头像选择（本端点）→ 成功即全局头像更新（`/me` 返回 `avatar` 字段，默认 `n1`）。

### 3.40 `POST /admin/assets` + `/admin/assets/update` + `/admin/assets/status` + `GET /admin/assets/list` — 荣誉馆资产库管理（管理端 Bearer）

- `POST /admin/assets` Body：`{key,name,name_en?,type:'avatar'|'badge',rarity?,limited?,total?,image,sort?,status?}`。`key` 唯一冲突 → `409 asset_exists`（同时写 `admin_log`）。返回 `{ok:true}`。
- `POST /admin/assets/update` Body：同上传（`key` 只读定位，改 `name/type/rarity/limited/total/image/sort/status` 等）。返回 `{ok:true}`。
- `POST /admin/assets/status` Body：`{ key, status:'active'|'hidden' }`。返回 `{ok:true}`（隐藏后登录器展品/头像网格自动不再显示，已持有用户展品同步隐藏）。
- `GET /admin/assets/list?page&size`：分页返回 `{ok:true, data:{list, total, page, pageSize}}`。
- 错误：`unauthorized`(401) / `invalid_input`(400) / `asset_exists`(409) / `no_asset`(404)。

## 4. 错误码表

| code | HTTP | 场景 |
|---|---|---|
| invalid_input | 400 | 参数缺失/格式错误 |
| unauthorized | 401 | 管理 token 无效/过期 |
| no_user | 401 | 登录账号不存在 |
| bad_password | 401 | 密码错误 |
| twofa_required | 401 | 需两步认证验证码 |
| bad_code | 401 | 两步认证验证码错误 |
| expired | 401 | 验证码过期（bad_code 同义） |
| bad_totp | 401 | 谷歌验证器动态码错误 |
| bad_old_code | 401 | 换绑第 1 步（当前邮箱）验证码错误 |
| bad_new_code | 401 | 换绑第 2 步（新邮箱）验证码错误 |
| not_current | 400 | 换绑 step=old 时 email 与当前绑定不一致 |
| not_pending | 400 | 两步验证开启未处于待确认状态 |
| already_enabled | 409 | 两步验证已开启 |
| bad_plan | 400 | 套餐参数错误 |
| invalid_amount | 400 | 卡面额非法（≤0 或 >100000，或会员卡 cycle 缺失） |
| card_used | 400 | 卡密已使用/已作废 |
| card_invalid | 400 | 会员卡 cycle 非法（非 month/year） |
| insufficient_coin | 402 | 金币余额不足（data 含 need/coin） |
| card_not_found | 404 | 卡密不存在 |
| not_found | 404 | 会话/资源不存在 |
| mail_not_configured | 503 | 邮件服务未配置（MAIL_API_URL/KEY/FROM 未设） |
| mail_send_failed | 503 | 邮件发送失败（第三方邮箱服务拒绝/网络错误） |
| email_exists | 409 | 注册邮箱已存在 |
| asset_exists | 409 | 荣誉馆资产 key 已存在 |
| no_asset | 404 | 荣誉馆资产不存在 |
| not_avatar | 400 | 勋章资产不可作头像（type=badge） |
| not_owned | 403 | 未持有该荣誉资产 |
| no_such_table | 500 | 表未建（worker 启动建表失败——正常情况下不会出现） |

## 5. 写侧对应（后台管理端 → 表）

| 后台页面 | 表 | 本契约字段 |
|---|---|---|
| 游戏管理 | game | games 全字段 |
| 区服管理 | server | servers 全字段（**本轮补 type/tags 列**） |
| 动态管理 | launch_news | news 全字段 |
| 更新日志 | launch_changelog | changelog 全字段 |
| 轮播图管理 | banner | banners 全字段 |
| 启动器版本 | launcher_version | 登录器自更新 manifest 来源 |
| 游戏版本 | game_version | gversion 全字段 |
| 点卡点券 | game_charge | gcharges 全字段 |
| 授权管理 | license | license/verify 全字段 |
| 用户管理 | user/member_sub/wallet | register/login 用户侧 |

## 6. 登录器本地逻辑（不入 API）

- **安装状态**：游戏是否已安装 → 登录器本地记录（`store`），非 API 字段。
- **新开区**：`now − open_time ≤ 3 天`（登录器端计算，与后台无关）。
- **在线人数**：列表轮询刷新（L3 起每 30s 一次 `/servers`）；实时推送后续（WebSocket/长轮询）。
- **状态灯颜色**：§3.2 映射表，UI 层实现。
- **登录器自更新**：不经过本 API，走 R2 manifest（§8）。

## 7. 版本与变更

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.3 | 2026-10-08 | 荣誉馆后端化：3.37 `/assets` 公开资产库 + 3.38 `/me/items` 我的展品 + 3.39 `/me/avatar` 头像设置 + 3.40 资产库管理四端点；错误码 asset_exists/no_asset/not_avatar/not_owned；注册自动发放 n1（初心·幼龙守护灵） |
| v1.2 | 2026-10-08 | 虚拟卡双卡型（3.30 兑换分流 coin/premium、3.31 生成 plan/cycle 定价自动取、3.34 导出带 plan）+ 新增 3.35 管理端通用 CRUD `/admin/:res` + 错误码 card_invalid |
| v1.1 | 2026-10-07 | 账户安全/会员 13 端点补齐（3.11~3.23）+ 错误码扩展 + 页面真桥化（安全中心/换绑/F2A/会员/注册找回验证码） |
| v1.0 | 2026-10-07 | 定稿：10 公开端点 + 错误码 + 三层映射；server 表补 type/tags 列（待落库） |

## 8. 登录器自更新 manifest（R2，独立于 API）

- URL：`https://update.sellerrule.com/version.json` / `version-beta.json`（R2 桶 tuppo-launcher / stable、beta 双 manifest）
- 通道：stable（默认）/ beta（设置切换）；强制更新无视通道。
- **线上实际字段**（以 C++ Check/Apply 实现为准）：
  ```
  { "version": "0.1.1", "url": "https://update.sellerrule.com/tuppo-launcher-0.1.1b.zip",
    "sha256": "8f28977f...", "force": false, "notes": "更新说明", "updated_at": "ISO8601" }
  ```
  - `force` 为**布尔**（worker 写 `r.force ? true : false`；C++ 兼容 `true` / `1` 两种形态）。
  - `url` 指向**版本化 key**（`tuppo-launcher-<version>.zip`，新版本发新 key）：R2 自定义域存在 CDN 缓存，覆盖同 key 在缓存 TTL 内可能返回旧包导致 sha256 校验失败（联调实测复现），**发版必须换新 key**。
- 后台写侧：`POST/PUT/DELETE /admin/versions` 后由 worker `syncVersionManifest` 自动同步 R2 双 manifest（D1 表 launcher_version 为唯一数据源）。
- 校验链：下载 → sha256 比对 → 解压 stage → `UpdateApply.bat` 接力替换重启；`bad_sha256` 拒绝安装并前端提示。
