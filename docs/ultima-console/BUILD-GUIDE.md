# UltimaConsole 构建指南（BUILD-GUIDE）

> 落盘：2026-10-20 · 适用范围：UltimaConsole（鸿蒙 ArkTS 原生 APP）
> 权威源：`H:\UltimaAI\UltimaConsole\README.md` 构建规范节；本文为 UltimaDocs 库镜像。

## 环境要求（必须遵守）

构建时 **JAVA_HOME 必须指向 DevEco 自带 JBR**（`H:\Huawei\DevEco Studio\jbr`，JDK 21）。

> 根因：系统默认 java 为 1.8.0_31，无法解析新版 p12 密钥算法参数，导致 `SignHap → 11014003 Init keystore failed`；换 JBR 21 后签名成功（2026-10-20 实测）。

## 构建命令

```powershell
$env:DEVECO_SDK_HOME="H:\Huawei\DevEco Studio\sdk"
$env:DEVECO_HOME="H:\Huawei\DevEco Studio"
$env:JAVA_HOME="H:\Huawei\DevEco Studio\jbr"
$env:PATH="H:\Huawei\DevEco Studio\jbr\bin;" + $env:PATH
cd H:\UltimaAI\UltimaConsole
# debug（模拟器）
& "H:\Huawei\DevEco Studio\tools\hvigor\bin\hvigorw.bat" assembleHap --mode module -p product=default -p buildMode=debug --no-daemon
# release（真机/发布，含正式签名）
& "H:\Huawei\DevEco Studio\tools\hvigor\bin\hvigorw.bat" assembleHap --mode module -p product=default -p buildMode=release --no-daemon
```

## 签名

- 自动签名材料：`C:\Users\Administrator\.ohos\config\`（DevEco 自动生成，含 .cer/.p7b/.p12），由 build-profile.json5 引用
- 签名损坏/失效时：DevEco「文件 → 项目结构 → 签名配置 → 自动生成签名」重新生成

## 产物

`H:\UltimaAI\UltimaConsole\entry\build\default\outputs\default\`
- debug → `entry-default-unsigned.hap`
- release → `entry-default-signed.hap`

## 安装（hdc 路径：`H:\Huawei\DevEco Studio\sdk\default\openharmony\toolchains\hdc.exe`）

- 模拟器：`hdc install <hap>`
- 真机无线（台式机无 Type-C 口方案）：
  1. 设备开启「无线调试」，显示 `IP:端口`
  2. `hdc tconn <设备IP>:<端口>` 连接
  3. `hdc -t <设备IP>:<端口> install <hap>`
  4. `hdc -t <设备IP>:<端口> shell "aa start -a EntryAbility -b com.ultima.console"`

## 真机验证记录

- 2026-10-20：release 正式签名包（`entry-default-signed.hap`，5270KB）已无线安装到 **HUAWEI MatePad Mini 悦读版（MLR-AL00，API 26）** 并运行成功（PID 15052）
