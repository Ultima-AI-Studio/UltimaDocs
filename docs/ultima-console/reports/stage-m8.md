# Ultima Console M8 阶段报告

> 工单：`tasks/queue/wo-console-m8.md` v1.3  
> 执行日期：2026-10-17  
> 前置：`m7-frozen`（`6610e46d69a285c1f7108739ec2fd5b5b4a119f4`）

## 结论

**M8 PASS，允许冻结并发布 v1.0.0。** T0-T4 全绿；最终 clean build 生成可安装签名包且 ArkTS 零警告；模拟器真实 `open` 事件写入 RDB 后回读 `local_count=1`；113/113 自动化回归通过；已知问题清零；无越界。

## T0 · 项目级 DoD

### m8-T0-C1 · M1-M7 frozen

| 阶段 | frozen tag commit | 阶段证据 | 结果 |
|---|---|---|---|
| M1 | `2105a1ef03e116200b7bd4c4129c0027d6546362` | `docs/reports/stage-m1.md` | PASS |
| M2 | `3889f0398fe50902389503ec662e2f8cc836d742` | `docs/reports/stage-m2.md` | PASS |
| M3 | `42888f5b48116aa431126a2a5f302e184af85c8a` | `docs/reports/stage-m3.md` | PASS |
| M4 | `10486ee8692052892ba623dffe964478f4e48b15` | `docs/reports/stage-m4.md` | PASS |
| M5 | `e9741b771872e529796020800edba523aaa1b7a8` | `docs/reports/stage-m5.md` | PASS |
| M6 | `30afb2136badd4011a120199ab50bad6d41a85cf` | `docs/reports/stage-m6.md` | PASS |
| M7 | `6610e46d69a285c1f7108739ec2fd5b5b4a119f4` | `docs/reports/stage-m7.md` | PASS |

### m8-T0-C2 · P0×8 + P1×3

权威：`docs/产品策划方案-REQ-CONSOLE-001.md` v0.2 §五。

| 范围 | 关闭证据 | 状态 |
|---|---|---|
| F1 四板块仪表盘 | M2 | CLOSED |
| F2 产品级钻取；F3 工单逐层展开 | M3 | CLOSED |
| F4 评分评估 | M4 | CLOSED |
| F5 本地→GitHub 数据链路 | M1 | CLOSED |
| F6 鸿蒙原生 + 可旋转 | M7 | CLOSED |
| F7 只出结果 | M2-M7 UI Gate | CLOSED |
| F8 小助手审核/总结/建议/回执 | M6 | CLOSED |
| P1-1 双通道；P1-3 偏离预警 | M5 | CLOSED |
| P1-2 审批流 | M6 | CLOSED |

结论：P0 8/8、P1 3/3，全实现无遗漏。

### m8-T0-C3/C4 · Non-Goals 与冻结自检

权威：`docs/技术落地方案-REQ-CONSOLE-001.md` v0.9.1 §7/§8。N1-N8 无越界；§8 的 ADR、契约、无环依赖、高风险前置、Non-Goals、北极星承载、评分口径、预警边界 8/8 仍为绿色。结论：PASS。

### m8-T0-C5 · 四层完成定义

权威：`C:\Users\Administrator\AppData\Local\Doubao\User Data\Default\.doubao\agent_mode\workspace\.user_skills\ultima-工程方法论\SKILL.md` latest @ 2026-10-17，§4；SHA-256=`A00F9DBCAB921A4C0BC0A0CC47D6BDE1BF25993057872751C662AF9208AF2462`。

任务级、工单级、阶段级、项目级均由本报告的固定 Gate、发布包、阶段链、总范围与归档证据闭环。结论：PASS。

## T1 · 已知问题清零

P0×8+P1×3 范围问题 11/11 CLOSED；`console-queue-audit-report-v5.md` 为 40/40 PASS、0 FAIL；M1-M7 无移交 OPEN/BLOCKED；`sync/product.json` 的 `open_issues=[]`。结论：m8-T1-C1 PASS。

## T2 · 构建矩阵

- `hvigorw clean`：exit 0。
- `hvigorw assembleHap`：exit 0，`BUILD SUCCESSFUL`，ArkTS `WARN`=0。
- 发布包：`entry/build/default/outputs/default/entry-default-signed.hap`，183030 bytes，SHA-256 `7950DBA9C19E661C0AF2854AACFF1C45CC5D2BAE6CF0D0CC1B0AC1CECBB80488`。
- 模拟器 fresh install 成功，设备回读 `versionName=1.0.0`、`versionCode=10000`。

完整矩阵：`docs/reports/build-matrix.md`。结论：m8-T2-C1..C3 PASS。

## T3 · 北极星埋点

### m8-T3-C1 · 模拟器实测

- 设备：`127.0.0.1:5555`。
- 操作：安装 signed HAP，清空 hilog，`aa start -a EntryAbility -b com.ultima.console` 主动打开一次。
- 设备回读：`[NSM] event=open local_count=1`。
- 台账：设备本地 RDB `/data/app/el2/100/database/com.ultima.console/entry/rdb/ultima_console_m1.db` 的 `event_log` 表。
- 查询口径：`product_id='UltimaConsole' AND event_type='open'` 的行数；字段含 `ts` 与 `device_local_flag=1`，不上传。
- 证据：`m8-t3-install-fresh.log`、`m8-t3-bundle-version.log`、`m8-t3-start-fresh.log`、`m8-t3-open-hilog-fresh.log`、`m8-t3-rdb-path.log`。

结论：真实写入成功且计数 ≥1，埋点可采 PASS。

### m8-T3-C2 · 基线与发布后监督

基线：每自然周主动打开 ≥5 次，连续 4 周；按技术方案 §5.4，以发布后第 1-4 周周计数求和 / 4 ≥5 判定。4 周真实数据尚不存在，不预填、不伪造，作为发布后看门狗监督项，不阻塞本次发布。

## T4 · 发布归档

`docs/reports/release-v1.0.0.md` 已汇总版本、M1-M8、P0×8+P1×3、质量、签名产物、北极星、缺陷清零与无越界声明。`sync/product.json` 与技术方案 §5.3 同步为 version 1.0.0 / stage 已发布 v1.0.0；队列索引同步为 M8 已完成。冻结标签：`m8-frozen`、`v1.0.0`（均指向本发布提交）。结论：PASS。

## Gate 汇总

| Gate | 结果 | 证据 |
|---|---|---|
| m8-T0-C1..C5 | PASS | 本报告 T0 |
| m8-T1-C1 | PASS | 本报告 T1 |
| m8-T2-C1..C3 | PASS | `build-matrix.md` + final clean/assemble 日志 |
| m8-T3-C1 | PASS | 设备 `[NSM] event=open local_count=1` |
| m8-T3-C2 | PASS | 基线与监督口径已登记 |
| m8-T4-C1..C2 | PASS | 发布报告 + `m8-frozen` / `v1.0.0` |

## 越界声明

无。未实现 iOS/Mac/安卓/Windows、飞书灾备、任务派发或其他 N1-N8 项；未触碰 `H:\DevEcoStudioProjects\` 与 `H:\UltimaAI\_shared\`；未将令牌或签名密码写入报告、源码或 git。
