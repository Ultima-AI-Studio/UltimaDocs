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

## 四、执行标准（每次开发/执行必须符合）

1. **全链路**：需求 → 方案 → 工单 → 执行 → 验收 → 审计（不跳阶段、不省验收）
2. **工单纪律**：三段式（文件精确/写什么可执行/验收封闭清单 + 禁止清单）；每 T 验收门全绿 + 越界声明
3. **冻结门**：阶段报告产出 → AI 复核 → 冻结 tag（`stageN-frozen`），未冻结不进下一阶段
4. **数据同步**：状态/版本/评分变化 → 按触发点更新 `sync/product.json` → 双端同步（**不轮询**）
5. **审计**：对照治理体检基线（结构/文档/工单/验收/同步/活动），产出评分 0-100

## 五、数据同步标准

| 项 | 标准 |
|---|---|
| 唯一模板 | 每产品 `sync/product.json`（结构遵循 `UltimaConsole/docs/product-sync-template.md`） |
| 双端目标 | GitHub 公开 Gist（App 匿名主源）+ Gitee 镜像仓库（备份端） |
| 触发点 | 版本冻结 / 版本发布 / 数据变更 / 用户指示同步 |
| 动作 | 更新模板后执行双端同步脚本，一次命令两端更新 |

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
