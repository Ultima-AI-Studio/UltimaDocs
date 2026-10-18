# 技能分配逻辑（Skill Dispatch）

- **版本**：v1.1 · 2026-10-16
- **性质**：范式文件（冻结区，变更走评审）；与《项目强制范式标准》M1–M8 共同生效
- **核心**：技能分配 = **路由（选谁）** ＋ **技能（怎么干）** 两层

## 1. 分配流程

```
任务卡（goal / category / skill / fileDomain / 复杂度）
   ↓ ① 任务分类（Taxonomy）：交付类型 × 复杂度 × 领域
   ↓ ② 技能匹配（路由）：任务卡声明 > 自动映射 > 兜底
   ↓ ③ 技能执行：该技能的专属流程（读范式→查注册表→声明域→执行→自检）
   ↓ ④ 回执验收：产出路径 + 证据 + acceptance 核对（M5）
```

## 2. 任务分类维度（Taxonomy）

| 维度 | 取值 |
|---|---|
| 交付类型 | code / ui / audit / security / arch / database / test / infra / voice / docs / generic |
| 复杂度 | S（单步，直派）/ M（多步，带规划）/ L（跨技能，需组合 + 评审） |
| 领域 | core / sys / skill / plugin / ui / rel / host / server（任务卡 `category` 字段） |

## 3. 专家技能库

| 技能 ID | 角色 | 职责边界 |
|---|---|---|
| `eng.code` | 智能工程师 | 写代码 / 修 bug / 重构 / 单元自检 |
| `eng.ui` | UI 工程师 | 组件 / 界面 / 动效实现，遵循 UI 积木规格与主题标准 |
| `eng.audit` | 审计工程师 | 一致性 / 质量 / 回执核对 / 生成修正任务（独立于开发）；工程治理体检执行 `project-governance-audit` skill（基准清单 18+6 项 → 缺口矩阵 P0/P1/P2） |
| `eng.security` | 安全工程师 | 越界 / 权限 / 凭证 / 漏洞 / 受控执行核查 |
| `eng.arch` | 架构工程师 | 分层 / 接口契约 / 技术选型 / 依赖分析 |
| `eng.database` | 数据库工程师 | 数据建模 / 存储 / 查询 / 迁移 |
| `eng.test` | 测试工程师 | 验证 / 回归 / 验收证据 |
| `eng.infra` | 运维工程师 | 部署 / 环境 / 守护 / 日志 / 设备集群 |
| `eng.voice` | 语音/多媒体 | 语音链路 / 音色 / 音频 / CV3 类接线 |
| `eng.docs` | 文档工程师 | 范式 / 规格 / 纪要 / 调研落盘 |
| `eng.generic` | 通用执行器 | 无法判定任务兜底，或主脑人工裁决 |

## 4. 分配规则（Dispatch Rules，强制）

1. **任务卡声明优先**：立项时任务卡必须声明 `category` + `skill`（主技能）；缺省声明不派发。
2. **无声明自动映射**：按 goal 关键词 + 领域字段启发式映射，映射结果写回任务卡供审计。
3. **组合模式**：L 复杂度任务 = 主技能 + 协作技能（如 `eng.ui` 开发后必须 `eng.audit` 复核；`eng.code` 涉及数据时配 `eng.database`）。
4. **审计独立原则**：开发技能与审计技能分离，谁开发谁不能自审（防自证清白）。
5. **兜底**：无法判定走 `eng.generic` 或回主脑人工裁决，不硬猜。
6. **一次一主**：同一时刻一个任务只有一个主技能；协作技能在主技能完成后按需接入。

## 5. 技能注册条目结构（registry.md 登记内容）

每条技能在 `docs/specs/registry.md` 登记：**ID / 角色 / 职责边界 / 适用任务类型 / 输入要求 / 执行流程 / 工具集 / 产出标准 / 验收口径**。

- 新增技能必须先登记（M1），未登记不得使用。
- 技能本身受 M1–M8 全部约束：查注册表、声明 fileDomain、版本标识、DoD 回执。

## 6. 与治理的关系

- 分配器（skill dispatcher）是任务执行器的一部分，不单独建任务。
- 审计轮除核对产物外，还需核对"任务卡声明技能 vs 实际执行技能"是否一致。
- 技能挂接（M4 配套）：eng.audit 的治理体检执行 = `project-governance-audit` skill；开发/下发/验收全链路执行标准 = `engineering-standard` skill（见 acceptance-spec §9 / project-flow §1）。范式定义"选谁/查什么"，Skill 定义"怎么干/怎么查"。

## 7. 变更日志

| 版本 | 日期 | 变更内容 | 授权人 |
|---|---|---|---|
| v1.0 | 2026-10-16 | 初版：分配流程 + Taxonomy + 专家技能库 + 分配规则 + 注册条目结构 | Owner |
| v1.1 | 2026-10-16 | eng.audit 挂接 project-governance-audit（治理体检执行）；§6 补技能挂接说明（engineering-standard / project-governance-audit）；评审：Owner | Owner |
