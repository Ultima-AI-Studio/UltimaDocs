# 阿里云 CLI 能力与凭证使用手册（根能力）

> 版本：v1.0 ｜ 建立：2026-11-14 ｜ 归属：Ultima AI Studio 根能力层
> 定位：**全系产品调用阿里云 API 的唯一标准通道**。任何项目要用阿里云（ECS / RDS / OSS / DNS / 账单…），一律走本手册，禁止各项目自行拼签名、自行存密钥。
> 权威源：本文件（本地唯一，含凭证指针，**禁止镜像含明文内容**；镜像版本只保留指针与用法）

## 一、账号与凭证（唯一托管点）

| 项 | 值 |
|---|---|
| 阿里云账号 ID | `1035610218742193` |
| 凭证级别 | **主账号 root 级 AccessKey**（`acs:ram::1035610218742193:root`），即全账号最高权限 |
| vault 条目（ID） | `aliyun-accesskey-id` |
| vault 条目（Secret） | `aliyun-accesskey-secret` |
| 存放位置 | `H:\UltimaAI\_shared\vault\vault.json.enc`（DPAPI CurrentUser 加密，仅本机当前用户可解密） |
| 登记位置 | `H:\UltimaAI\_shared\server-assets.md` §四 密钥台账（只登记指针，不登记明文） |

### 取用方式（唯一姿势）

```powershell
$v = "H:\UltimaAI\_shared\vault\vault.ps1"
$env:ALIYUN_AK_ID     = (& $v get aliyun-accesskey-id)       # Python 脚本用这组
$env:ALIYUN_AK_SECRET = (& $v get aliyun-accesskey-secret)
# 或
$env:ALIBABA_CLOUD_ACCESS_KEY_ID     = (& $v get aliyun-accesskey-id)      # 官方 CLI 用这组
$env:ALIBABA_CLOUD_ACCESS_KEY_SECRET = (& $v get aliyun-accesskey-secret)
```

**硬规矩（与 `server-assets.md` §五 一致）**

1. 明文**不写入任何文件**（含本文档、项目 docs、README、`.env`）、不入 git、不进云盘/飞书/聊天回显。
2. 需要长期保存的只有「vault 条目名」；需要用时即时解密、用完即弃。
3. 想让所有项目都能用 → 认这两条 vault 条目名，不各自复制密钥。
4. 轮转密钥（阿里云控制台禁用旧 AK → 生成新 AK → `vault.ps1 add` 覆盖 → 登记 `server-assets.md` §四 → 复测 `sts GetCallerIdentity`），**轮转须 Owner 放行**。

> 为什么不把密钥明文写进 `_shared\registry.md`：该文件镜像到 GitHub `Ultima-AI-Studio/UltimaDocs`，等同把主账号全权密钥推到公网。故根能力层只登记**能力 + 指针**。

## 二、CLI 安装形态

| 项 | 值 |
|---|---|
| 版本 | **aliyun CLI 3.5.3**（官方 v3.5.3 release） |
| 平台包 | `aliyun-cli-windows-3.5.3-amd64.zip` |
| 安装路径 | `H:\UltimaAI\tools\bin\aliyun-cli\aliyun.exe` |
| 完整性 | 已对官方 `SHASUMS256.txt` 校验通过：`5728fbbd3480cfcba8b77bd04773553c9c69e60487b7668c32f241a610373bab` |
| 包装脚本 | `H:\UltimaAI\tools\aliyun-ultima.ps1`（vault → 环境变量 → CLI，固定 `--profile default`） |
| 是否需要 PATH | 不需要；一律用包装脚本或全路径调用 |

## 三、标准用法（推荐路径）

```powershell
$w = "H:\UltimaAI\tools\aliyun-ultima.ps1"

& $w sts GetCallerIdentity                                  # 身份核验（应为 root）
& $w ecs DescribeInstances --RegionId cn-shenzhen            # 列实例（完整 JSON）
& $w ecs DescribeRegions                                     # 可见地域
& $w rds DescribeDBInstances --RegionId cn-shenzhen          # RDS
& $w alidns DescribeDomains --PageSize 50                    # 云解析域名
& $w oss ls                                                  # OSS bucket（CLI 自带 oss 子命令）
```

输出解析（本版无 `--jmespath`）：

```powershell
$json = & $w ecs DescribeInstances --RegionId cn-shenzhen | Out-String
($json | ConvertFrom-Json).Instances.Instance | Select-Object InstanceId,Status,InstanceType
```

### 需要执行机器命令（云助手）

CLI 的多值参数写法与 ECS API 不一致（`--InstanceIds.1` 会被拒），且长脚本经 Windows 命令行转义易坏。
**统一改用 Python 脚本**（同一套凭证，只是环境变量名不同 `ALIYUN_AK_ID/SECRET`）：

```powershell
python "H:\UltimaAI\tools\aliyun_run_cmd.py" "uname -a; df -h /"
```

其余只读探针：
- `tools\aliyun_probe.py` —— 账号级能力盘点（ECS/轻量/VPC/SLB/RDS/DNS/CDN/RAM/余额/OSS）
- `tools\aliyun_ecs_detail.py` —— 单机详情 + 云助手状态

## 四、已知坑（都实测过，别再踩）

| # | 坑 | 现象 | 正确做法 |
|---|---|---|---|
| P1 | **本机已有历史 profile 抢凭证** | `~/.aliyun/config.json` 里 `current=tuppo-web`（子账号 `tuppo-web-ops`），直接跑 CLI 会用它，而非 vault 里的密钥 | 包装脚本固定加 `--profile default`（空 profile）→ CLI 才会回落读环境变量 |
| P2 | 多值参数写法不同 | `--InstanceIds.1 xxx` 报 `not a valid parameter` | 这类调用改用 python 脚本 |
| P3 | 无 jmespath | `--jmespath` 报非法参数 | 取全量 JSON，PowerShell `ConvertFrom-Json` 过滤 |
| P4 | `--output cols=` 对嵌套数组无效 | 输出 `<nil>` | 同上，走 JSON 解析 |
| P5 | 云助手 `RunCommand` 的 `ContentEncoding` | 不显式 `Base64` 会把 base64 串当脚本执行（`ExitCode=127`） | 用 `tools\aliyun_run_cmd.py`（已内置 `ContentEncoding=Base64`） |
| P6 | `DescribeInvocationResults` 结果结构嵌套 | 顶层取不到结果 | 结果在 `Invocation.InvocationResults.InvocationResult` |

## 五、现有风险（承接 `server-assets.md` §七 R8）

本机 `~/.aliyun/config.json` 中已有历史 profile **`tuppo-web`**（子账号 `tuppo-web-ops`，region `cn-shenzhen`，语言 zh），**AK 明文落盘**，且实测具备 ECS 读权限。

- 处置建议：该密钥按“已暴露”对待，轮转一次；日常调用改走本手册的 vault 路径。
- **未擅自删除**：该 profile 可能是既有业务在用，删除须 Owner 确认。
- 查看现状：`& "H:\UltimaAI\tools\bin\aliyun-cli\aliyun.exe" configure list`（密钥自动打码）。

## 六、变更记录

| 日期 | 变更 |
|---|---|
| 2026-11-14 | 建档：CLI 3.5.3 安装（SHA256 校验通过）、包装脚本 `aliyun-ultima.ps1`、凭证入 vault、能力登记入 `registry.md`；记录坑 P1-P6 与风险 R8 |
