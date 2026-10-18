# UltimaEngine 架构文档

> 依据：`H:\UltimaAI\ULTIMA-STANDARD.md`（Ultima AI Studio 产品顶层架构标准 v1.0）
> 更新：2026-10-18 ｜ 状态：开发中

## 身份
Ultima 体系游戏引擎（热血传奇正式版，TuppoM2 引擎迁移）；纯自研商业传奇引擎，单 EXE 一体化。

## 目录结构（对齐范本）
```
UltimaEngine/
├── README.md            ✗（本次补建 → 见根目录）
├── docs/                ✓（40 份报告，stage1-9 全链路）
│   ├── architecture.md  ✓（本文档）
│   └── reports/         ✓ stage8/9 联调报告等
├── tasks/queue/         ✗（待建工单队列）
└── sync/product.json    ✓
```

## 数据流
GameLaunch 自动安装闭环 → worker multipart 端点 → 引擎服务 → 客户端联调。

## 当前状态
- 热血传奇正式版联调：GameLaunch 自动安装闭环（2026-10-09）
- stage8/9 报告已产出

## 审计（2026-10-18）
- 评分：75/100（报告体系完整，结构缺项）
- 结论：40 份阶段报告强；缺 README/architecture（本次已补）、工单队列（后续建）
