# UltimaAI 产品接入 UltimaAdmin CMS 范式

> 版本：v1.0；日期：2026-10-28。
> 状态：用户 2026-10-28 明确要求建立（“立一个规则，建立一个规范，让他们读取之后知道怎么在自己的产品下面怎么去添加到 Ultima Admin 那个 CMS 管理系统里”）。
> 本地权威：`H:\UltimaAI\_shared\paradigms\UltimaAI-产品接入UltimaAdminCMS范式.md`。
> 适用范围：全系产品（UltimaAgent / UltimaGold / UltimaConsole / UltimaSentinel / UltimaScan / UltimaRadar 及后续新产品）接入 UltimaAdmin 统一主控后台（CMS）的登记、数据、前端与验收规则。
> 依据：UltimaAdmin 执行入口（docs/INDEX.md）、平台路由 platform.ts、通用模板 product-console.vue、聚合接口 admin_server.py、全局队列主表、ULTIMA-STANDARD §5.9 落盘与同步标准。

## 0. 一句话规则

**每个产品必须让 UltimaAdmin 能通过“登记 → 数据 → 菜单 → 页面”四步读取到你的运行状态；禁止手写 8 套后台页面，禁止改别人的 product.json，禁止绕过登记直接挂菜单。**

## 1. 接入目标与分层边界

UltimaAdmin 是**统一主控后台（CMS，端口 8913）**，不是用户侧产品前端。接入它 ≠ 你的用户网站挂在 Admin 上。

| 层次 | 归属 | 说明 |
|---|---|---|
| 用户侧前端（官网/APP/桌面端） | 各产品自建 | Gold 官网/Web/安卓、Radar Electron 桌面、Console/Agent 鸿蒙原生、Scan 单页、Sentinel Web 审计台（web/frontend），形态各异，独立迭代，与 Admin 解耦 |
| 统一管理端（CMS） | UltimaAdmin 唯一承载 | 每产品一个二级菜单；通用三件套页面（运行状态/定价/API 能力）；产品专属深度管理页可渐进挂载 |
| 监督看板 | UltimaConsole（鸿蒙） | 数据底座的只读视图，与 Admin 共用同一数据源，不托管前端、不重复管理逻辑 |
| 数据底座 | 各产品 `sync/product.json` + 全局队列主表 | 只读聚合源，Admin/Console 统一从这读，不改写产品文件 |

## 2. 接入前置条件（DoR）

接入前必须满足，缺项保持“未接入”登记状态，不能默认补为通过：

1. 项目根路径存在，目录名 `Ultima` 开头，位于 `H:\UltimaAI\` 下。
2. `docs/INDEX.md` 存在，且已引用 G-DISPATCH-001、G-WO-NAME-001、本接入范式。
3. `sync/product.json` 存在且结构合法（见 §4 字段契约）。
4. 项目队列主表存在（`tasks\queue\`），有队列则状态同步，无队列先补建。
5. 无独立绕过全局登记的派发通道；开发任务仍走 UltimaManager 统一调配（G-DISPATCH-001）。

## 3. 接入四步（唯一路径）

### Step 1 · 登记（platform_products 表）

在 UltimaAdmin 数据库 `platform_products` 表登记一行产品记录，字段：

| 字段 | 说明 | 示例 |
|---|---|---|
| `code` | 产品代码（小写，唯一主键） | `ultimascan` |
| `name` | 显示名 | `UltimaScan` |
| `full_name` | 全称/描述 | `加密项目全量扫描` |
| `status` | 启停状态 | `enabled` |
| `entry` | 产品入口路径 | `/ultimascan/dashboard` |

登记动作由 UltimaAdmin 侧管理员执行（或经工单派发），**产品侧不得直接改 admin.db**。登记完成后菜单骨架即可挂出。

### Step 2 · 数据（sync/product.json 聚合）

产品侧维护好自己的 `sync/product.json`（本文件是 Admin 读你状态的口子）。Admin 通过 `GET /api/ultima/products` 聚合读取，字段契约见 §4。**Admin 只读你的 product.json，不改写；你更新它即实时反映到 CMS。**

### Step 3 · 菜单（路由注册）

前端路由 `admin-panel/src/router/routes/modules/platform.ts` 中，在 `ULTIMA_PRODUCT_ROUTES` 数组追加一行（模板函数已封装好，禁止手写整套路由）：

```ts
ultimaProductRoute('<path>', '<Name>', 'menu.<key>', '<code>'),
```

同时在 `src/locale/zh-CN.ts` 与 `en-US.ts` 补对应菜单文案（`menu.<key>`）。

三件套子页（运行状态 / 定价 / API 能力）由通用模板 `views/ultima/product-console.vue` 自动带出，**不需要也不允许为每个产品复制一套页面**。

### Step 4 · 验证（验收门）

1. `npm run build` 通过（vue-tsc + vite，exit 0）。
2. `GET /api/ultima/products` 返回你的产品，含 `status/version/score/deviation/queue/capabilities`，缺失字段按契约兜底，不整单报错。
3. `GET /api/ultima/status`、`GET /api/ultima/pricing` 正常；`POST /api/ultima/pricing` 无 token 必须 401（鉴权写门生效）。
4. 登录 8913 后菜单可见、三件套页面渲染正常、定价保存成功（人工验收门，由 Owner 确认）。

## 4. sync/product.json 字段契约

```json
{
  "product": "UltimaXxx",
  "version": "0.1.0",
  "status": "开发中",
  "stage": "阶段说明",
  "updated_at": "2026-10-28T00:00:00+08:00",
  "summary": {
    "progress": 68,
    "score": 72,
    "deviation": "无",
    "blocker": "无"
  },
  "capabilities": ["能力1", "能力2"]
}
```

| 字段 | 必填 | 说明 | 缺失兜底 |
|---|---|---|---|
| `product` | 是 | 产品名，必须与登记 code 对应产品一致 | 用登记名 |
| `version` | 是 | 当前版本号（SemVer） | 空串 |
| `status` | 是 | 开发状态（开发中/开发完成/已上线等） | `未知` |
| `stage` | 否 | 阶段/版本说明，人可读 | 不显示 |
| `summary.progress` | 是 | 完成度 0-100 | 0 |
| `summary.score` | 是 | 质量评分 0-100 | 0（显示“未评级”由 Admin 判断） |
| `summary.deviation` | 否 | 偏移状态（无/轻微/有偏移） | `未评级` |
| `summary.blocker` | 否 | 当前阻塞项 | 无 |
| `capabilities` | 否 | API/能力清单（字符串数组或对象数组） | 空，页面显示“能力清单待补” |

**规则**：
- 无已执行任务的产品，评分保持 0 即可，Admin 端显示“未评级”，**不要塞假评分**。
- `deviation` 取值建议：`无` / `轻微偏移` / `有偏移`，未评级不写空串写 `未评级`。
- 复杂能力清单可另建 `sync/capability-manifest.json`（`capabilities` 数组），Admin 优先读它。

## 5. 产品专属深度管理页（可选，渐进挂载）

通用三件套覆盖不了产品专属能力（如 Gold 的新闻/推送管理、Radar 的监控配置）时：

1. 在对应产品的路由组 children 下追加子路由，`component` 指向**产品自己的视图文件**（`views/<product>/xxx.vue`），复用 Admin 的 Vue3+Arco 技术栈与样式范式。
2. 子页开发仍走产品自己的开发流程（工单 → Codex → 验收），完成后提交路由文件合并。
3. **禁止**在 Admin 里复制整套后台框架给单一产品用；专属页只在三件套之外做增量。

## 6. 禁止项（红线）

1. **禁止手写 6/8 套后台页面**：所有产品的基础管理（状态/定价/API）一律走 `product-console.vue` 通用模板，route meta 传 `productCode/productMode` 区分。
2. **禁止改其他产品的 `sync/product.json`**：每产品只写自己的；Admin 只读不写。
3. **禁止绕过登记直接挂菜单**：路由注册必须与 `platform_products` 登记一一对应，未登记=越界。
4. **禁止删/改 `platform_products` 表结构或已有行**：新增走登记流程，已有行（含 ultimapay 等）保留。
5. **禁止删除既有分组**：tuppoau / agent / ultimapay 等存量分组保留，新产品在 `ULTIMA_PRODUCT_ROUTES` 追加。
6. **禁止直接改 `admin.db`**：数据库写操作（登记/定价）经 Admin 接口与管理流程，产品侧不直连。
7. **禁止以“接入完成”代替真实验收**：构建 + 接口 + 人工点击验收通过才算完成；未验证不宣称已接入。
8. **禁止推 GitHub/Gitee 触发双端同步混淆**：Admin 自身同步按 ULTIMA-STANDARD §5.9 走，产品接入动作不另行推送。

## 7. 验收与状态机

接入状态与工单一致：`待接入 → 登记中 → 数据就绪 → 菜单挂出 → 验收中 → 已接入`。

- 数据就绪 = product.json 合法且接口可读。
- 菜单挂出 = 路由 + locale + 登记三者齐。
- 已接入 = Owner 登录人工验收通过（菜单/三件套/定价保存）。

## 8. 已接入产品登记（2026-10-28 快照）

| 产品 | code | 菜单位置 | 接入状态 |
|---|---|---|---|
| Ultima Agent | `agent` | 产品管理（既有组，走通用模板改造） | 已接入 |
| Ultima Gold | `ultimagold`/`tuppoau` | 产品管理（保留旧完整后台组） | 已接入 |
| Ultima Console | `ultimaconsole` | 产品管理（通用模板组） | 已接入 |
| Ultima Sentinel | `ultimasentinel` | 产品管理（通用模板组） | 已接入 |
| UltimaScan | `ultimascan` | 产品管理（通用模板组） | 已接入 |
| UltimaRadar | `ultimaradar` | 产品管理（通用模板组） | 已接入 |
| Ultima Pay | `ultimapay` | 产品管理（既有组） | 存量保留 |

## 9. 维护

- 本范式由主脑维护；变更走评审，旧版归档只读。
- 新增产品接入时，若遇到本范式未覆盖的情况，先补范式再接入，不临时绕过。
