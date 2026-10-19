# Ultima AI 品牌资产库

> 唯一权威：Ultima 全系产品（UltimaConsole / UltimaRadar / UltimaGold / UltimaEngine / UltimaAgent / UltimaScan / UltimaSentinel 等）的品牌 logo、图标、启动页品牌图统一存放于此。
> 建立：2026-10-19 ｜ 本地权威：`H:\UltimaAI\_shared\brand\` ｜ 镜像：ultima-docs-repo `docs/brand/`（GitHub）
> 规则：品牌资产一律从本库引用，禁止各项目自行散存新版本；新增/变更品牌资产须登记本清单并同步镜像。

## 一、资产清单

### 主 logo（头盔标）——唯一 logo 资产

| 文件 | 说明 |
|---|---|
| `ultima-logo/helmet.png` | 头盔主标（**透明底 RGBA**，2048²，可直接叠任意背景；金属银盔体 + 深蓝面罩星空 + 蓝星芒）。**应用时一律用本文件，禁止白底版本直接叠背景** |
| `ultima-logo/helmet-preview.png` | 头盔主标预览版（仅供参考） |

### 应用图标

| 文件 | 说明 |
|---|---|
| `ultima-logo/app-icon.png` | 应用图标（AppScope/entry 同源去重） |

### 启动页品牌图

| 文件 | 说明 |
|---|---|
| `splash/splash-landscape.png` | 启动页品牌图（横屏 2560×1600 适配） |
| `splash/splash-portrait.png` | 启动页品牌图（竖屏 1600×2560 适配） |

### 品牌区渲染参考（旧版视觉基线，仅参考）

| 文件 | 说明 |
|---|---|
| `references/brand-zone-landscape.jpeg` | 品牌区横屏渲染参考（v11 验收证据） |
| `references/brand-zone-portrait.jpeg` | 品牌区竖屏渲染参考（v11 验收证据） |

### 组合参考渲染（可选，非必用）

| 文件 | 说明 |
|---|---|
| `combo/deep/ultima-console-landscape.png` 等 4 张 | 按参数规范渲染出的参考示例图。**应用时直接用 logo + 字体文字实时渲染，无需合成图**；需要预览图时可改 HTML 源重渲 |

### 品牌字体（HarmonyOS Sans，唯一字库）

| 文件 | 说明 |
|---|---|
| `fonts/HarmonyOS_Sans.ttf` | 品牌英文字体（主标 `Ultima` + 产品名用），HarmonyOS Sans，0.33MB |
| `fonts/HarmonyOS_Sans_SC.ttf` | 品牌中文字体（副标/中文文案用），HarmonyOS Sans SC，19.66MB |

> 来源：DevEco Studio SDK（华为官方字体，可商用）。品牌文字统一用本字库，禁止改用其他字体。

## 二、品牌规范要点

### 2.1 品牌组合参数规范（v1.3，2026-10-19 定版）

**组合 = 透明底头盔 logo + 字体文字（实时渲染，不拼合成图）**

**① logo（头盔标）**
- 文件：`ultima-logo/helmet.png`（透明底 RGBA）
- **不加阴影/光晕**，保持原始图形
- 尺寸不单独定，按「④ 尺寸与间距」比例自动换算（横屏 = 字号 × 2.25；竖屏 = 字号 × 4）

**② 英文字体**
- 字体：**HarmonyOS Sans**（`fonts/HarmonyOS_Sans.ttf`）；中文用 HarmonyOS Sans SC
- **加粗：Bold 700**
- **字间距：主标 0.5px；副标 1px**
- 禁止改用 Segoe UI / 微软雅黑等其他字体

**③ 文字颜色**

| 场景 | Ultima（主品牌） | 子品牌产品名（Console / Radar / Gold …） |
|---|---|---|
| 深色底（deep） | `#EAF2FF`（近白） | 默认 `#4D9FFF`（accent 蓝）；可按产品主题换色（需登记） |
| 浅色底（light） | `#0B1220`（黑） | 默认 `#1D6FFF`（深蓝）；可按产品主题换色（需登记） |

- **子品牌换色规则**：默认全系统一 accent 蓝；产品可自定义 accent 色（如 UltimaGold → 金色 `#D4AF37`、UltimaRadar → 雷达主题色），**自定义须在品牌库 README 登记**，结构保持"Ultima 主色 + 子品牌 accent"两段式不变。

**④ 尺寸与间距（缩放只定字号，其余按比例换算）**

- 基准：**2560×1600 设计稿下主标字号 = 48px**（预览 HTML 实测，Bold 700）
- 缩放公式：`主标字号 = 48px × min(目标宽 ÷ 2560, 目标高 ÷ 1600)`

| 形态 | 布局 | logo 高 | 主标字号 | logo↔文字间距 |
|---|---|---|---|---|
| **横屏** | logo 左 + 文字右，垂直居中 | 字号 × **2.25**（48px → 108px） | **48px**（2560 基准） | **列间距 = 字号 × 0.36**（48px → ≈17px） |
| **竖屏** | logo 上 + 文字下，水平居中 | 字号 × **4**（48px → 192px） | **48px**（1600×2560 基准） | **行间距 = 字号 × 0.47**（48px → ≈23px） |

> 注：组合参考图（`combo/`）为独立横幅物料参数（88px@1200 宽），仅作视觉示例，APP 界面一律按上表 48px 基准与缩放公式执行。

**⑤ 产品适配**：其他产品改产品名文字即可（子品牌色按 ③ 规则），参数结构不变。

### 2.2 使用标准（何时用横 / 竖 / 深 / 浅）

| 场景 | 形态 |
|---|---|
| APP 界面品牌区（左上角）且**界面内已有 logo 浮窗**（如右下角悬浮球） | **纯文字**（Ultima + 产品名，按 deep/light 着色），**不加 logo**，避免重复 |
| 无 logo 浮窗场景（启动页、Banner、外部物料、横屏 2560×1600 宽屏品牌区） | **横屏组合**（logo 左 + 文字右） |
| 窄屏/竖屏界面品牌区（竖屏 1600×2560 顶部、启动页竖版） | **竖屏组合**（logo 上 + 文字下） |
| 深色主题界面 / 深色封面 / 深色启动帧 | **deep（白字）** |
| 浅色主题界面 / 浅色封面 / 白底文档 | **light（黑字）** |
| 悬浮球、角标、小尺寸控件 | 直接用透明底 helmet（不带文字） |

### 2.3 其他要点

- 悬浮球浮窗：头盔 logo + 镜片推光同框锁死 108vp，无圆底、无呼吸灯（v1.1-N3 定稿）
- 启动页：自定义首帧 + 星星闪烁全程 + 镜片推光 1.5s + 整体渐隐 0.5s，总 2s 进主界面（v1.1-N4 定稿）

## 三、维护规则

1. 各产品引用品牌资产时优先指向本库路径，不复制进产品目录（产品内打包资源除外）。
2. 品牌资产变更：更新本清单 → 同步镜像 `ultima-docs-repo/docs/brand/` → push GitHub。
3. 禁止删除/改名在库资产而不更新本 README。
