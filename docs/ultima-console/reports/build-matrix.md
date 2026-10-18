# Ultima Console M8 构建矩阵

> 执行日期：2026-10-17  
> 工程根：`H:\UltimaAI\UltimaConsole`  
> DevEco：`H:\Huawei\DevEco Studio`  
> SDK：API 24；compatible API 12；target API 24（模拟器 API 20）  
> Hvigor：6.24.5

## 冻结构建命令

| 测试 ID | 命令 | 参数组合 | 最终结果 | 原始证据 |
|---|---|---|---|---|
| m8-T2-C1 | `H:\Huawei\DevEco Studio\tools\hvigor\bin\hvigorw.bat clean` | product=`default` | exit 0；`BUILD SUCCESSFUL in 188 ms` | `docs/reports/evidence/m8-final-clean.log` |
| m8-T2-C2 | `H:\Huawei\DevEco Studio\tools\hvigor\bin\hvigorw.bat assembleHap` | product=`default`、target=`default`、默认 debug 模式 | exit 0；`BUILD SUCCESSFUL in 9 s 590 ms`；ArkTS `WARN`=0 | `docs/reports/evidence/m8-final-assemble.log` |
| m8-T2-C3 | 核验 `entry/build/default/outputs/default/entry-*.hap` | 固定产物目录 | signed 与 unsigned HAP 均存在 | 本报告产物清单 |

## ArkTS 警告清零

首次复现 13 条，原始输出见 `docs/reports/evidence/m8-assemble-warning-repro.log`；没有使用 suppression。

| 根因 | 位置 | 数量 | 修复 |
|---|---|---:|---|
| 声明可抛异常但无显式处理 | `EntryAbility.ets:16`；`M1Runtime.ets:57,60,61,100,109,111,112×2,113`（修复前行号） | 10 | 为窗口加载、RDB 初始化/写入/查询、ResultSet 读取与关闭建立显式异常边界 |
| 退役 `Scroll.onScroll` | `ProductDetail.ets:56` | 1 | 改用 `onDidScroll` |
| 退役全局 `mediaquery.matchMediaSync` | `Index.ets:36` | 1 | 改用 `UIContext.getMediaQuery().matchMediaSync` |
| 退役全局 `getContext` | `Index.ets:48` | 1 | 改用 `UIContext.getHostContext` |

最终干净构建日志中 `WARN:` 计数为 0，`CompileArkTS` 与 `SignHap` 均完成。

## 产物与签名

`build-profile.json5` 已配置 `signingConfigs.default`，类型 `HarmonyOS`，product `default` 引用该配置；证书、profile、keystore 与 key alias 均已配置，密码材料不在报告中回显。

| 路径 | 字节 | SHA-256 | 签名状态 |
|---|---:|---|---|
| `entry/build/default/outputs/default/entry-default-signed.hap` | 183030 | `7950DBA9C19E661C0AF2854AACFF1C45CC5D2BAE6CF0D0CC1B0AC1CECBB80488` | `SignHap` 成功；模拟器 fresh install 成功；包版本 1.0.0 |
| `entry/build/default/outputs/default/entry-default-unsigned.hap` | 141018 | `6277C117DFFD5C6EFC81F011C307BF417F5E3E116CC349DFE48F045C2C62346F` | unsigned 中间产物，不作为发布包 |

覆盖安装曾因模拟器残留旧签名包返回 `install sign info inconsistent`；该次没有计为成功。卸载旧测试包后，signed HAP fresh install 成功，见 `m8-t3-uninstall-old-signature.log`、`m8-t3-install-fresh.log` 与 `m8-t3-bundle-version.log`。

## T2 Gate

**PASS。** clean/assembleHap 均 exit 0；最终 ArkTS 零警告；固定目录存在可安装的签名 HAP；签名信息、版本、路径与摘要均已登记。
