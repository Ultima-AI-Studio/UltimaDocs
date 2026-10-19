# Ultima AI 品牌资产库

> 唯一权威：Ultima 全系产品（UltimaConsole / UltimaRadar / UltimaGold / UltimaEngine / UltimaAgent / UltimaScan / UltimaSentinel 等）的品牌 logo、图标、启动页品牌图统一存放于此。
> 建立：2026-10-19 ｜ 本地权威：`H:\UltimaAI\_shared\brand\` ｜ 镜像：ultima-docs-repo `docs/brand/`（GitHub）
> 规则：品牌资产一律从本库引用，禁止各项目自行散存新版本；新增/变更品牌资产须登记本清单并同步镜像。

## 一、资产清单

### 主 logo（头盔标）

| 文件 | 说明 | 源 |
|---|---|---|
| `ultima-logo/helmet.png` | 头盔主标源图（**透明底 RGBA**，2048²，可直接叠任意背景；金属银盔体 + 深蓝面罩星空 + 蓝星芒） | UltimaConsole docs |
| `ultima-logo/helmet-preview.png` | 头盔主标预览版 | UltimaConsole docs |

> **透明要求**：应用 logo 时一律使用透明底 `helmet.png`（已确认无白边残留），禁止白底版本直接叠到深色/彩色背景上。

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

### logo + 文字组合标准（v1.1，含深/浅双背景系列）

**深色底系列（`combo/deep/`）——白字版**

| 文件 | 说明 |
|---|---|
| `combo/deep/ultima-console-landscape.png` | 组合图-横屏深色（logo 左置 + 文字右置，1200×400 基准） |
| `combo/deep/ultima-console-portrait.png` | 组合图-竖屏深色（logo 上置 + 文字下置，640×960 基准） |
| `combo/deep/combo-landscape.html` | 可编辑源（横屏深色） |
| `combo/deep/combo-portrait.html` | 可编辑源（竖屏深色） |

**浅色底系列（`combo/light/`）——黑字版**

| 文件 | 说明 |
|---|---|
| `combo/light/ultima-console-landscape.png` | 组合图-横屏浅色（Ultima 黑字 + 产品名深蓝） |
| `combo/light/ultima-console-portrait.png` | 组合图-竖屏浅色 |
| `combo/light/combo-landscape.html` | 可编辑源（横屏浅色） |
| `combo/light/combo-portrait.html` | 可编辑源（竖屏浅色） |

## 二、品牌规范要点

### 2.1 logo + 文字组合标准（v1.1，2026-10-19 定版）

组合构成（自左至右 / 自上至下）：**头盔 logo（透明底）→ 主标**（无副标）。

- **深色底（deep）**：主标 `Ultima` = 近白 `#EAF2FF`；产品名（如 `Console`）= accent 蓝 `#4D9FFF`；底 = 深蓝渐变（#101A30 → #0A0F1E → #070B14）
- **浅色底（light）**：主标 `Ultima` = 黑 `#0B1220`；产品名（如 `Console`）= 深蓝 `#1D6FFF`；底 = 浅蓝白渐变（#FFFFFF → #F1F5FB → #E4EBF5）
- **横屏布局**（1200×400 基准）：logo 高 200 左置，主标右置、垂直居中；logo 与文字间距 32；主标 88px 粗体
- **竖屏布局**（640×960 基准）：logo 高 280 上置居中，主标下置居中；logo 与文字间距 32；主标 68px（不超出卡片边界）
- **光效**：logo 光晕——深色底用蓝晕 `drop-shadow(0 0 34~40px rgba(70,150,255,.55))`；浅色底用深蓝投影 `drop-shadow(0 4px 18px rgba(30,80,200,.22))`
- **产品适配**：其他产品复用组合模板，改产品名即可（如 Radar = "UltimaRadar"，accent 色可按产品调整，结构比例不变）

### 2.2 使用标准（何时用横 / 何时用竖 / 深 / 浅）

| 场景 | 用哪版 |
|---|---|
| 宽屏界面品牌区（导航头部、横幅 Banner、横屏 2560×1600） | **横屏**（logo 左 + 文字右） |
| 窄屏/竖屏界面品牌区（启动页、竖屏 1600×2560 顶部） | **竖屏**（logo 上 + 文字下） |
| 深色主题界面 / 深色封面 / 深色启动帧 | **deep（白字）** |
| 浅色主题界面 / 浅色封面 / 浅色 Banner / 打印白底文档 | **light（黑字）** |
| 单独图标、悬浮球、角标、小尺寸控件 | 直接用透明底 `helmet.png`（不带文字） |

### 2.3 其他要点

- 品牌区文字组合：主标 Ultima（accent 色）+ 副标（如 Console = "工程调度管理中心"），横竖屏同构
- 悬浮球浮窗：头盔 logo + 镜片推光同框锁死 108vp，无圆底、无呼吸灯（v1.1-N3 定稿）
- 启动页：自定义首帧 + 星星闪烁全程 + 镜片推光 1.5s + 整体渐隐 0.5s，总 2s 进主界面（v1.1-N4 定稿）
- 新增产品使用品牌：主标统一用本库 helmet 系；各产品副标文案由产品自己定，渲染效果对照 `references/` 参考图与 `combo/` 组合标准

## 三、维护规则

1. 各产品引用品牌资产时优先指向本库路径，不复制进产品目录（产品内打包资源除外）。
2. 品牌资产变更：更新本清单 → 同步镜像 `ultima-docs-repo/docs/brand/` → push GitHub。
3. 禁止删除/改名在库资产而不更新本 README。
