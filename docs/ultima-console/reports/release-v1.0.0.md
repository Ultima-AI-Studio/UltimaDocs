# Ultima Console v1.0.0 发布报告

> 发布日期：2026-10-17  
> 发布里程碑：M8  
> 冻结标签：`m8-frozen` / `v1.0.0`

## 1. 版本

HarmonyOS 首版 `v1.0.0`；bundle `com.ultima.console`；设备回读 `versionName=1.0.0`、`versionCode=10000`。

## 2. M1-M8 阶段归档

M1 数据链路、M2 仪表盘、M3 产品钻取、M4 审计评分、M5 双通道与预警、M6 审批与小助手、M7 旋转布局均已有 `m1-frozen` 至 `m7-frozen`；M8 项目级 DoD 全绿，以 `m8-frozen` 冻结。阶段证据见 `docs/reports/stage-m1.md` 至 `stage-m8.md`。

## 3. 功能范围

产品策划方案 v0.2 §五的 P0×8（F1-F8）与 P1×3 全部纳入，11/11 CLOSED；MVP 未裁剪 P1。飞书灾备按 N8 留在第二阶段。

## 4. 质量

- Node 全量回归：113 tests / 113 pass / 0 fail。
- ArkTS：首次 13 条警告均按根因修复；最终干净构建 0 warning、0 error。
- 缺陷：产品范围 11/11 CLOSED；队列审计 40/40 PASS；`open_issues=[]`。
- 构建：`clean` 与 `assembleHap` 均 exit 0。

## 5. 构建产物与签名

发布包：`entry/build/default/outputs/default/entry-default-signed.hap`；183030 bytes；SHA-256 `7950DBA9C19E661C0AF2854AACFF1C45CC5D2BAE6CF0D0CC1B0AC1CECBB80488`。Hvigor `SignHap` 成功，模拟器 fresh install 成功。unsigned HAP 仅为中间产物，不列为发布包。

## 6. 北极星基线

设备本地 RDB `event_log` 已实测写入一次 `open`，设备回读 `local_count=1`。台账路径：`/data/app/el2/100/database/com.ultima.console/entry/rdb/ultima_console_m1.db`。基线为每自然周主动打开 ≥5 次、连续 4 周；发布后第 1-4 周真实数据由看门狗监督复核，本次不预填、不上传、不阻塞发布。

## 7. 缺陷与风险

本次发布无 OPEN/BLOCKED 已知缺陷。模拟器曾残留不同签名的旧包，覆盖安装被明确拒绝；卸载旧测试包后用本轮 signed HAP fresh install 成功，该环境残留不构成发布包缺陷。

## 8. 越界声明

无。未实现 N1-N8 排除项，未触碰禁止目录，未持久化 GitHub 令牌或签名密码。

## 9. 归档与证据

- 发布提交：本报告所在提交。
- 标签：`m8-frozen`、`v1.0.0`，均指向发布提交。
- 构建：`docs/reports/build-matrix.md`。
- 阶段：`docs/reports/stage-m8.md`。
- 原始日志：`docs/reports/evidence/m8-final-*.log`、`m8-t3-*.log`。
