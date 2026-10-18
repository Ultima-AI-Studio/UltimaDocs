# Ultima Console 数据同步模板规范（Sync Template）

> 定位：`sync/product.json` 是**终端（App/鸿蒙端）唯一标准录取模板**——所有产品状态数据以本模板为唯一权威源（single source of truth）。
> 终端按本模板结构录取渲染（评分汇总/KPI/需关注/产品卡片），**任何更新都是更新这个模板**，然后同步到两个公开端。

## 一、模板文件与双端同步

| 端 | 位置 | 用途 |
|---|---|---|
| 模板源 | `sync/product.json`（本仓库） | 唯一权威源，人工/触发时更新 |
| GitHub 公开 Gist | `gist.github.com/ArkExlabs/5d0043cc6fd2441997c686a206053529` | App 匿名读取**主源**（raw URL） |
| Gitee 镜像仓库 | `gitee.com/Ultima-AI-Studio/ultimaconsole-sync` | 工程端镜像**备份端**（数据双写） |

同步动作：`sync-dual.py`（一次性脚本，同时更新 Gist + Gitee）。

## 二、模板结构（终端录取标准，覆盖设计稿全部功能读取点）

```json
{
  "updated_at": "ISO8601 时间戳（本地时区，如 2026-10-18T18:30:00+08:00）",
  "products": [
    {
      "product": "产品名（与终端产品标识一致，如 UltimaConsole）",
      "version": "语义化版本号，未评级产品填 \"—\"",
      "status": "产品状态枚举：开发中 / 开发完成 / 已发布 / 规划中 / 卡壳",
      "stage": "阶段描述（当前所处工程阶段/冻结状态一句话）",
      "summary": {
        "progress": "0-100 整数，总进度",
        "score": "0-100 整数，达标评分（未评级填 0，配合 deviation=未评级）",
        "deviation": "无 / 偏移 −N / 未评级",
        "blocker": "阻塞描述，无则填 无"
      },
      "intro": "产品介绍段落（详情页·介绍标签数据）",
      "metrics": [
        { "name": "指标名（如 北极星指标）", "value": "指标值（如 每周主动打开 ≥5 次）" }
      ],
      "queue": [
        { "id": "工单号（如 M1）", "title": "标题", "version": "v1.1", "status": "已完成/进行中/待办/已冻结", "priority": "high|medium|low" }
      ],
      "docs": [
        { "group": "文档分组（如 产品方案/设计稿/工程报告）", "count": 6, "items": [
          { "type": "方案|设计|报告|规范|说明", "name": "文档名", "version": "v0.2", "status": "已冻结/已发布/进行中", "source": "本地|GitHub|飞书", "updated": "MM-DD" }
        ] }
      ],
      "open_issues": [ "未关闭问题列表，无则空数组" ],
      "audit_reports": [
        { "id": "报告号", "conclusion": "审计结论一句话" }
      ],
      "refs": { "方案文档": "URL 或相对路径" }
    }
  ],
  "approvals": [
    { "product": "产品名", "title": "待审批事项标题", "source": "来源（飞书/GitHub）", "status": "待审批", "summary": "小助手总结一句话" }
  ],
  "refs": { "同步规范": "docs/product-sync-template.md" }
}
```

### 与设计稿功能读取点对照（模板必须覆盖的）

| 设计稿功能区块 | 模板字段（终端读取） |
|---|---|
| 总览·KPI（产品总数/开发中/已上线/卡壳/待拍板） | `products[]` 长度 + 各 `status` + `open_issues` 非空计数 + `approvals[]` 长度 |
| 总览·评分汇总（产品行：名/进度条/评分/偏移） | 遍历 `products[]` → `product` / `summary.progress` / `summary.score` / `summary.deviation` |
| 总览·需关注（预警/待拍板行） | `summary.deviation≠无` + `open_issues` + `approvals.length`（终端派生） |
| 总览·待审批（审批卡：产品/标题/来源/评分/总结） | `approvals[]` |
| 产品页·卡片集合（按状态分组卡片） | `products[]` → `status` 分组 + `summary.score` / `summary.deviation` |
| 产品详情·头部（名/大评分/偏移标签） | `product` / `summary.score` / `summary.deviation` |
| 产品详情·介绍（描述/北极星指标） | `intro` / `metrics[]` |
| 产品详情·任务队列（工单行：T0/T1/版本/状态/优先级） | `queue[]` |
| 产品详情·文档库（分组文档行：类型/名/版本/状态/来源/时间） | `docs[]`（group/count/items） |
| 文档库页（全库分组列表） | 聚合所有 `products[].docs[]` |
| 悬浮球角标（待拍板数） | `approvals.length` |

### status 枚举

| 值 | 含义 |
|---|---|
| 开发中 | 有未闭环工单 |
| 开发完成 | 工单全闭环、待发布验收 |
| 已发布 | 版本已发布（可含版本号说明） |
| 规划中 | 待立项/信息架构阶段（summary 记未评级） |
| 卡壳 | 存在阻塞项（summary.blocker 必填） |

### 更新约束

- `summary.score`：与审计结论一致（100=无偏离）；未评级产品填 `0` + `deviation=未评级`
- `queue.status` / `docs[].status`：与工程队列/文档状态一致（frozen/closed 等）
- 未知字段禁止写入模板（App 白名单校验拒收）

## 三、同步触发规则（事件触发，非定时）

**触发点（满足任一即执行一次 `sync-dual.py`）**：

1. **版本冻结**：某阶段全部工单冻结（打 frozen tag / 生成阶段报告）时
2. **版本发布**：发布门通过（RELEASE）时
3. **数据变更**：本地/飞书文档更新导致产品状态（version/status/stage/summary/work_orders）变化时
4. **用户指示**：用户说"同步本地文档 / 同步飞书 / 同步模板"时

**禁止**：定时轮询、定时任务。同步只在触发点发生。

## 四、同步动作

```bash
# 更新模板源 sync/product.json 后执行
python sync-dual.py
# 输出: OK gist updated / OK gitee updated sha=xxx
```

验证：App 匿名读取 Gist raw（主源）应返回最新模板内容。
