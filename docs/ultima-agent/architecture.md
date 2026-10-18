# UltimaAgent 架构文档

> 依据：`H:\UltimaAI\ULTIMA-STANDARD.md`（Ultima AI Studio 产品顶层架构标准 v1.0）
> 更新：2026-10-18 ｜ 状态：开发中

## 身份
Ultima 体系智能体执行端：看门狗调度、零弹窗治理、自动化执行闭环。

## 目录结构（对齐范本）
```
UltimaAgent/
├── README.md            ✓
├── docs/                ✓（9 份报告）
│   ├── architecture.md  ✓（本文档）
│   └── reports/         ✓ stage/审计报告
├── tasks/queue/         ✓（10 张工单）
└── sync/product.json    ✓
```

## 数据流
Owner 指令/定时触发 → 看门狗（UltimaAgent）→ 执行端调度 → 回执 → UltimaConsole 仪表盘。

## 当前状态
- 看门狗管理复盘闭环（2026-10-16）
- 零弹窗根因分析与修复闭环（2026-10-16）

## 审计（2026-10-18）
- 评分：78/100（基本合规）
- 结论：报告/工单齐全；缺产品特化数据流文档（已列入后续补）
