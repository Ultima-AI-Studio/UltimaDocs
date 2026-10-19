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

### logo + 文字组合标准（v1.0）

| 文件 | 说明 |
|---|---|
| `combo/ultima-console-landscape.png` | 组合标准图-横屏（logo 左置 + 文字右置，1200×400 基准） |
| `combo/ultima-console-portrait.png` | 组合标准图-竖屏（logo 上置 + 文字下置，640×960 基准） |
| `combo/combo-landscape.html` | 组合标准可编辑源（横屏，改文案/配色后重渲） |
| `combo/combo-portrait.html` | 组合标准可编辑源（竖屏） |

## 二、品牌规范要点

### 2.1 logo + 文字组合标准（2026-10-19 定稿）

组合构成（自左至右 / 自上至下）：**头盔 logo（透明底）→ 主标 → 副标**。

- **配色**：主标 `Ultima` = 近白 `#EAF2FF`；产品名（如 `Console`）= accent 蓝 `#4D9FFF`；副标 = 次级灰 `#8A94A6`；底 = 深蓝渐变（#101A30 → #0A0F1E → #070B14）
- **横屏布局**（1200×400 基准）：logo 高 200 左置，文字组右置、垂直居中；logo 与文字间距 52；主标 88px 粗体，副标 30px、字距 14px、行距 16
- **竖屏布局**（640×960 基准）：logo 高 280 上置居中，文字组下置居中；主标 96px，副标 32px、字距 14px、行距 20
- **光效**：logo 带蓝色光晕 `drop-shadow(0 0 34~40px rgba(70,150,255,.55))`，呼应头盔面罩蓝星芒
- **产品适配**：其他产品复用组合模板，改产品名与副标文案即可（如 Radar = "聪明钱雷达监控"，accent 色可按产品调整，结构比例不变）

### 2.2 其他要点

- 品牌区文字组合：主标 Ultima（accent 色）+ 副标（如 Console = "工程调度管理中心"），横竖屏同构
- 悬浮球浮窗：头盔 logo + 镜片推光同框锁死 108vp，无圆底、无呼吸灯（v1.1-N3 定稿）
- 启动页：自定义首帧 + 星星闪烁全程 + 镜片推光 1.5s + 整体渐隐 0.5s，总 2s 进主界面（v1.1-N4 定稿）
- 新增产品使用品牌：主标统一用本库 helmet 系；各产品副标文案由产品自己定，渲染效果对照 `references/` 参考图与 `combo/` 组合标准

## 三、维护规则

1. 各产品引用品牌资产时优先指向本库路径，不复制进产品目录（产品内打包资源除外）。
2. 品牌资产变更：更新本清单 → 同步镜像 `ultima-docs-repo/docs/brand/` → push GitHub。
3. 禁止删除/改名在库资产而不更新本 README。
