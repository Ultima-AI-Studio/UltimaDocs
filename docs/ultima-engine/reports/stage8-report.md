# 阶段8 报告：加固兼容 v1.1（T0~T6）

> 生成：2026-10-03 ｜ 工单：25-Codex工单-阶段8-加固兼容.md ｜ 前置：stage7-frozen ✅
> 结论：**通过**（4 项验收以真实口径登记，非缺陷项见问题清单）

---

## 1. 阶段概览

阶段8（稳定性加固 + 兼容性 + BUG 闭环 + 容灾）25 工单 T0~T6 全部完成并提交。
冻结证据：全量单测 9459 断言 / 268 用例（重跑全绿）、双构建冒烟 PASS、一键回归 7 项实质全绿、
容灾四 Gate 实测通过。**建议冻结 stage8-frozen**。

## 2. 任务完成情况

| 任务 | 状态 | 证据 |
|---|---|---|
| T0 CrashDump | ✅ | TestStability 子进程注入 → dump 生成（阶段8 已提交基线） |
| T1 MemAudit | ✅ | 内存巡检/泄漏报告单测（阶段8 已提交基线） |
| T2 TamperCheck | ✅ | 篡改内存 License 结构 60s 内检出退出（阶段8 已提交基线） |
| T3 兼容性矩阵 | ✅（Win10 真实口径登记） | compat-matrix-20261003-0049/0116.md：classic+extended 冒烟 PASS（本机 Win11 x64）；Win10 x64 pending 已登记（15 台账） |
| T4 BUG 回归闭环 | ✅ | 键漂移修复 / OPEN-13 死亡掉落接线 / OPEN-14 脚本事务桥 / @siege/@enhance 接线 / ResDropEntry 改名 / regression.ps1 7 项一键回归 / flaky 面登记 |
| T5 容灾备份恢复 | ✅ | 看门狗杀进程自动重启（22048→44276→39616）+ 崩溃风暴第 4 次超限停止告警 / 备份→恢复演练（篡改拒绝 + 正常恢复 + 引擎自检） / BackupMgr 回档单测 49 断言 / @rollback GM 接线 200 断言 |
| T6 总验收 | ✅ | 本报告 + 25 工单验收打勾（7/8 项 ✅；Win10 矩阵按真实口径登记）+ stage8-frozen |

## 3. 问题清单

| 问题 | 影响 | 处置 | 状态 |
|---|---|---|---|
| 全量单测网络时序 flaky（TestGameMsg 661/663/2039/2339 组队 RESULT、1781 广播限速、TestLogin 157/235/510、TestNet 223） | 全量首跑偶发 1 个失败 | 重跑对照：本次首跑 2339 失败→重跑 **All tests passed（9459 断言/268 用例）**；单跑隔离全绿；判定端口 TIME_WAIT/顺序级联 flaky（非缺陷） | 📋 登记（15 台账 flaky 面） |
| OPEN-16（query-chr 高峰超时）/ OPEN-17（S3 千人 PBKDF2）/ OPEN-18（S4 AOI 热点）/ OPEN-19（FakeClient.cpp 源损坏） | 已知限制（非本阶段缺陷） | 按真实口径登记，不就地膨胀；归 v1.1 后续轮/真实素材环境核验 | 📋 登记 |
| Win10 x64 矩阵未实测 | 兼容矩阵第 8 项 P2 + Win10 行 pending | 按真实口径登记（15 台账/compat 报告注明"待 CI/备用机"），不以"范围内未见"代替 | 📋 登记 |
| regression.ps1 判定经 4 版修复（PowerShell 解析坑：函数内嵌 if-else/中文 BOM/引号直传数组索引） | 脚本可用性 | 最终版 0 语法错误 + BOM + 判定读报告文件 | ✅ 闭环 |
| backup/restore/watchdog 三脚本首测修复（sqlite3 CLI 缺失回退 / NativeCommandError 自检 / 数组固定大小 / BOM 乱码） | 容灾工具可靠性 | 实测通过（见 T5 证据） | ✅ 闭环 |

## 4. 越界与变更声明

- 清单外改动：**无**（所有改动均在 25 工单 T0~T6 范围内；新增 src/sys/BackupMgr 属 T5 回档工具契约内，02 §2.16b 已登记表结构）
- 文档同步：02 §3 补权威键（broadcast_max_pkt_ps/aoi_view_radius）、02 §2.16b 新增 backup_snapshots 表、15 台账 T4/T5 闭环登记、25 工单验收打勾
- 未决项（OPEN）：仅 16/17/18/19 + flaky 面（已知限制登记，非缺陷）

## 5. 验收证据汇总

| 项 | 结果 |
|---|---|
| 构建 | classic/extended 双构建冒烟 PASS（compat-matrix-20261003-0116.md） |
| 全量单测 | 9459 断言 / 268 用例 全绿（重跑确认；首跑 1 flaky 已登记） |
| [backup] 单测 | 49 断言全绿（快照回滚一致/无快照拒绝/enable=false 拒绝/转义往返） |
| [gm] 单测 | 200 断言全绿（含 @rollback 全流程） |
| 手感回放 | 通过（伤害偏差 0 / 时序偏差 0 / 轨迹偏差 0） |
| 压测 | S1 avgTick 1.73ms / S2 avgTick 2.93ms（阈值 10ms ✅，内存增长 0MB） |
| 资源冒烟 | MiniResGen exit=0 |
| 授权链路 | [license] 5 路径 PASS（篡改/过期/正常） |
| 存档迁移 | T6:* PASS |
| 容灾 Gate ① | 杀进程 → 3 次自动重启成功，数据不丢（WAL） |
| 容灾 Gate ② | 备份→恢复演练通过；篡改备份拒绝恢复（SHA256 校验） |
| 容灾 Gate ③ | 回档工具单测通过（资产与备份点一致 + admin_logs op_type 13） |
| 容灾 Gate ④ | 循环崩溃风暴：窗口内 4 次 > max_restarts=3 → 停止拉起 + 告警文件 |

## 6. 下一阶段前置核验（阶段9 发布扩展，26 工单）

- [ ] stage8-frozen 已打（本报告结论通过后）
- [ ] 26 工单 T0 打包（package.ps1 单 EXE 三合一）+ T1 SHA256 清单就绪
- [ ] Win10 x64 兼容实测（归 26 工单或 P2，真实口径登记）
- [ ] 一键回归 7 项可在发布前重跑（tools/regression.ps1 已落地）

## 7. 冻结建议

**建议：冻结（tag stage8-frozen）**——25 工单 T0~T6 全部完成，验收证据真实可复核，已知限制已按真实口径登记。
