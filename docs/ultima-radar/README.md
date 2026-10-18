# UltimaRadar

Solana memecoin 聪明钱跟监与机会信号桌面应用（M1 walking skeleton）。

## 架构

- `backend/`：Python 数据管道（标准库，无需 pip 安装）
  - 地址库导入（`backend/data/smart_money.csv`）→ 清洗 → 评分 → Top10
  - 行情快照与异动检测（DexScreener API，已实测可用）
  - 多源信号融合（GMGN 聪明钱 / MadeOnSol KOL / pump.fun 新币 / 新闻热度共振 → 分级信号）
  - 模拟跟单（纸面验证）+ 回测闭环
  - 本地 HTTP API（127.0.0.1:8721）
- `frontend/`：Electron 桌面壳，4 主视图（聪明钱 Top10 / 信号流 / 市场监控 / 我的）

## 目录结构（Ultima 范式，2026-10-17 补建）

```
UltimaRadar/
├── docs/          # 技术档案（00-架构设计 / 08-流程清单 / 存量方案与报告）
├── tasks/         # 任务与工单（工单-阶段X.md，待立项后落单）
├── reports/       # 审计报告（审计-存量核查-20261017.md 首份）
├── ops/           # 市场运营档案（待上线启用）
├── sync/          # 标准制式导出（product.json，喂给 Ultima Console）
├── artifacts/     # 版本产物（只读归档，待首版本落档）
├── src/           # 代码（当前实际在 backend/ + frontend/，src 为范式对齐占位）
├── backend/       # Python 数据管道（存量结构，保留）
├── frontend/      # Electron 桌面壳（存量结构，保留）
├── scripts/       # 启动 + 19 个 verify_*.py 验证脚本（存量）
└── tests/         # 单元测试 15 项（存量）
```

> 规则：新增文档/工单/报告/产物一律落范式目录；存量 backend/frontend 不再写新内容。

## 快速开始

1. 启动后端：

   ```bash
   cd backend
   python main.py
   ```

2. 启动桌面应用（另一终端）：

   ```bash
   cd frontend
   npm install   # 首次
   npm start
   ```

   或双击 `scripts/run_backend.bat` 与 `scripts/start_app.bat`。

## 配置

- 聪明钱地址：编辑 `backend/data/smart_money.csv`（列：address,label）
- 候选币种（关注币行情）：**DB watchlist 表**（软件内市场监控页可添加/移除；`backend/data/watchlist.csv` 仅作首启迁移源）
- 数据源 Key（GMGN/MadeOnSol/Birdeye/Helius）：**软件内"数据源"页填写即用**（DPAPI 加密存储）
- 轮询间隔、API 端口、评分阈值：`backend/config.py`（权威参数见 docs/04-参数基线.md）

## 现状（2026-10-18 更新）

- 行情快照 / 异动检测：真实实现（DexScreener API）
- 聪明钱清洗与评分：多因子评分 + 连续亏损护栏（见 docs/14-ADR.md ADR-004）
- 聪明钱数据（Top10 净流入/胜率/上榜理由/买入事件）：GMGN API（软件内填 key 即用；gmgn-cli 需 `npm install -g gmgn-cli`）
- 新闻热度：Google News 真实采集（免 key）+ X/Reddit 待 key
- 关注币行情：手动关注 + 热度自动并入（前端可增删）
- 模拟跟单：纸面验证（paper 账户），实盘自动跟单冻结待安全评审
- 治理文档：docs/ 全套（00-16 + B 类），权威清单见 docs/08-流程清单.md

## 数据表

SQLite 位于 `backend/data/ultimaradar.db`：`addresses` / `token_snapshots` / `signals`。
