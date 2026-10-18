# UltimaGold

XAUUSD 黄金交易辅助与推送系统（原名 TuppoAU，2026-10-17 迁移入 UltimaAI 改名）。

## 定位

黄金（XAUUSD）行情监控、信号推送与交易辅助全栈系统，覆盖 Web 后台 / 移动端 / 桌面端 / 信号推送链路。

## 目录结构（Ultima 范式对齐，2026-10-17）

```
UltimaGold/
├── docs/           # 技术档案（00-架构设计 ~ 18-工单模板，编号体系完整）
│   ├── reports/    # 存量审计报告（UGP-01 ~ UGP-13）
│   └── work-orders/ # 存量工单（G1-G6 + Codex P0-P3）
├── tasks/          # 任务与工单（范式目录，待新工单落单）
├── reports/        # 审计报告（范式目录，存量在 docs/reports/）
├── sync/           # 标准制式导出（product.json，喂给 Ultima Console）
├── ops/            # 市场运营档案（待上线启用）
├── artifacts/      # 版本产物（只读归档）
├── src/            # 代码（范式占位，实际代码在各业务目录）
├── backend/        # 核心服务（存量结构）
├── ml-engine/      # 机器学习引擎（存量）
├── mt5-bridge/     # MT5 桥接（存量）
├── mt5sdk/         # MT5 SDK（存量）
├── news-feed/      # 新闻采集（存量）
├── admin-panel/    # 管理后台（存量）
├── admin-panel-vue-element/  # 后台前端（存量）
├── pc-client/      # 桌面客户端（存量）
├── app-android/    # 安卓端（存量）
├── web-user/       # 用户 Web 端（存量）
├── ultima-gold-site/ # 官网（存量）
├── ultima-pay/     # 支付（存量）
├── scripts/        # 脚本（存量）
├── tests/          # 测试（存量）
└── tools/          # 工具（存量）
```

> 规则：新增文档/工单/报告/产物一律落范式目录；存量业务目录不再写新管理内容。

## 文档体系

- 技术档案编号 00-18 完整（架构/接口/数据/参数/验收/安全/构建/流程/骨架/枚举/ADR/台账/功能范围等）
- 存量工单：G1-G6 六阶段 + Codex P0-P3 系列
- 存量审计：UGP-01 ~ UGP-13

## 快速启动

见 `start-ultima-service.bat` / `打开Ultima后台.bat`（存量启动脚本）。
