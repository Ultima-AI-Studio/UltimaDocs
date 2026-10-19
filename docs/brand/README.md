# Ultima AI 品牌资产库

> 唯一权威：Ultima 全系产品（UltimaConsole / UltimaRadar / UltimaGold / UltimaEngine / UltimaAgent / UltimaScan / UltimaSentinel 等）的品牌 logo、图标、启动页品牌图统一存放于此。
> 建立：2026-10-19 ｜ 本地权威：`H:\UltimaAI\_shared\brand\` ｜ 镜像：ultima-docs-repo `docs/brand/`（GitHub）
> 规则：品牌资产一律从本库引用，禁止各项目自行散存新版本；新增/变更品牌资产须登记本清单并同步镜像。

## 一、资产清单

### 主 logo（头盔标）

| 文件 | 说明 | 源 |
|---|---|---|
| `ultima-logo/helmet.png` | 头盔主标源图（金属银盔体 + 深蓝面罩星空 + 蓝星芒） | UltimaConsole docs |
| `ultima-logo/helmet-preview.png` | 头盔主标预览版 | UltimaConsole docs |

### 应用图标

| 文件 | 说明 | 源 |
|---|---|---|
| `ultima-logo/app-icon.png` | 应用图标（AppScope/entry 同源去重） | UltimaConsole AppScope media |

### 启动页品牌图

| 文件 | 说明 | 源 |
|---|---|---|
| `splash/splash-landscape.png` | 启动页品牌图（横屏 2560×1600 适配） | UltimaConsole docs |
| `splash/splash-portrait.png` | 启动页品牌图（竖屏 1600×2560 适配） | UltimaConsole docs |

### 品牌区渲染参考

| 文件 | 说明 | 源 |
|---|---|---|
| `references/brand-zone-landscape.jpeg` | 品牌区横屏渲染参考（Ultima + Console accent 副标） | v11-brand 验收证据 |
| `references/brand-zone-portrait.jpeg` | 品牌区竖屏渲染参考 | v11-brand 验收证据 |

## 二、品牌规范要点

- 品牌区组合：主标 Ultima（accent 色）+ 副标（如 Console = "工程调度管理中心"），横竖屏同构
- 悬浮球浮窗：头盔 logo + 镜片推光同框锁死 108vp，无圆底、无呼吸灯（v1.1-N3 定稿）
- 启动页：自定义首帧 + 星星闪烁全程 + 镜片推光 1.5s + 整体渐隐 0.5s，总 2s 进主界面（v1.1-N4 定稿）
- 新增产品使用品牌：主标统一用本库 helmet 系；各产品副标文案由产品自己定，渲染效果对照 `references/` 参考图

## 三、维护规则

1. 各产品引用品牌资产时优先指向本库路径，不复制进产品目录（产品内打包资源除外）。
2. 品牌资产变更：更新本清单 → 同步镜像 `ultima-docs-repo/docs/brand/` → push GitHub。
3. 禁止删除/改名在库资产而不更新本 README。
