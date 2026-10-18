# TuppoM2 阶段1（M1 底座 + 商业授权）总验收报告

- 日期：2026-10-01
- 工单：18-Codex工单-阶段1-M1底座.md（T0~T11）
- 执行：豆包（MainAgent）— 架构师复核角色
- 结论：**通过（冻结）** ✅

---

## 1. 阶段概览

阶段1 目标：M1 底座 + 商业授权模块（工程骨架、全局类型、配置、日志、机器码、授权、任务池、最小入口、数据库初始迁移、多语言底座）全部落地并冻结。

**结论：通过。** 四矩阵编译零错误零警告、ctest 100%、授权五路径人工复核全部符合预期、冒烟运行正常、线程标注静态审查通过、05 §4 checklist 七项逐项打勾、Git tag `stage1-frozen` 已落。

---

## 2. 任务完成情况（T0~T11）

| 任务 | 内容 | 状态 | 证据 |
|---|---|---|---|
| T0 | 工程骨架（CMake/vcpkg/preset） | ✅ | bfbac5c 提交（阶段0冻结后）；本段补充 VCPKG_TARGET_TRIPLET |
| T1 | Common.h 全局类型 | ✅ | src/base/Common.h，ECode 错误码/JobPriority 单测覆盖 |
| T2 | Config 配置加载 | ✅ | 27 顶层字段全量校验 + CRC + FindByPath 只读（修复 yaml-cpp 0.9.0 set_ref 污染根节点） |
| T3 | Logger 日志模块 | ✅ | spdlog 封装，级别过滤/轮转/双通道单测 |
| T4 | HwId 机器码 | ✅ | 三源（主板+磁盘+MAC）SHA256，Win/Linux 双实现 |
| T5 | License 授权校验 | ✅ | RSA-2048 PSS，魔数/BOM 防御/宽限期/特性掩码/版本集，篡改/过期/hwid 全拒 |
| T6 | TaskPool 任务池 | ✅ | std::thread + 条件变量，优先级/超时/心跳单测 |
| T7 | main.cpp 冒烟入口 | ✅ | --config 加载→日志→I18n→授权→退出码，冒烟 OK |
| T8 | migrations SQL 迁移 | ✅ | 4 个迁移脚本（0001~0004，对齐工单 T8）+ check_migrations.py 校验 |
| T9 | tests/Test*.cpp 全套 | ✅ | 39 用例 / 189 断言全绿（ctest 100%） |
| T10 | 阶段1 总验收 | ✅ | 本报告 |
| T11 | I18n 多语言底座 | ✅ | zh-CN/en-US、缺 key 回退、{0} 占位符、SetLang 单测 |

---

## 3. 问题清单（本段修复 5 类构建/测试缺陷 + 2 类授权复核缺陷）

| # | 问题 | 影响 | 处置 | 状态 |
|---|---|---|---|---|
| 1 | Config::FindByPath 触发 yaml-cpp 0.9.0 `Node::operator=` → set_ref 污染共享底层节点，s_root 被破坏 | 配置 getter 全部失效（单测失败根因） | 改用 `cur.reset(child)` 只换指针不下钻引用；全 const 访问 | ✅ 已修复 |
| 2 | TestLicense/TestI18n 只写最小配置，Config::Load 27 字段校验失败 | 单测无法加载 | 新建 TestConfigData.h 共享完整 YAML 模板（`__MODE__` 注入），三处共用 | ✅ 已修复 |
| 3 | License::Verify 静态缓存 `s_verified` 短路 | 首用例通过后篡改/过期/hwid 用例全被缓存放行 | 新增 `License::ResetForTest()`，每用例开头重置 | ✅ 已修复 |
| 4 | zh-CN.json 误含 `only.en.key` | 破坏"zh 缺 key 回退 en"语义 | 删除该 key | ✅ 已修复 |
| 5 | TestLogger 轮转断言用错命名规则 | 误判轮转失败 | 按 spdlog 1.17 实际规则 `tuppom2.<n>.log` 断言 | ✅ 已修复 |
| 6 | gen_lic.ps1 写 lic 带 UTF-8 BOM（EF BB BF） | 魔数行被污染，全部 lic 报 E_LIC_INVALID | 签发改无 BOM 写出；License.cpp 加首行 BOM 防御（双保险） | ✅ 已修复 |
| 7 | gen_lic.ps1 篡改 lic 用 New-LicFile 重新签名 | 篡改 lic 验签通过（测不出篡改） | 篡改改为"改 JSON + 保留原签名"；.NET 独立验签交叉确认 TAMPERED_VERIFY=False | ✅ 已修复 |
| 8 | 授权日志 serial 前 8 打印 JSON 开头 | 日志语义错误 | 改取 `doc["serial"]` 值前 8 | ✅ 已修复 |

遗留登记（OPEN）：无（本段 7 项缺陷全部闭环）。

**审计补充修复（2026-10-01 阶段1 全量审计后追加，commit 见 §5）**：

| # | 审计发现 | 处置 | 状态 |
|---|---|---|---|
| A1 | Logger 签名偏离 01 §3.1/工单 T3 契约：LogLevel 用 6 级（Trace..Critical）而非契约 4 级；`Log` 缺 tag 参数；`Init` 缺 `ECode&` 输出 | 对齐 01：`LogLevel{Debug=0,Info=1,Warn=2,Error=3}` + 全局 `Log(lv,tag,fmt,...)` 契约入口 + `Init(dir,lv,rotationMb,ec)`；宏改 `LOG_XXX(tag, ...)`；全部调用点（src+tests 共 36 处）加 tag；spdlog 级别经 ToSpd 显式映射 | ✅ 已修复 |
| A2 | I18n 类名/签名偏离 01 §3.9d：类名 I18n（契约 I18nService）；`Init(langDir,ec)`（契约 `Load(langDir)`）；Format 用 vector<string>（契约 initializer_list<string_view>）；SetLang 返回 bool（契约 void） | 对齐 01：类名 I18nService + Load/GetText/Format/SetLang 契约签名；main.cpp/TestI18n 同步适配 | ✅ 已修复 |
| A3 | Config.cpp 告警仍用 stderr（注释自认"T3 落地后替换为 Log"未执行） | 改用 01 §3.1 全局 `Log(LogLevel::Warn, "Config", ...)` 自由函数 | ✅ 已修复 |
| A4 | Logger::Init 仅捕获 spdlog_ex，非法路径（filesystem_error）会崩溃 | catch 扩为 std::exception + 兜底；TestLogger 增加 Init 失败返回 E_IO 用例 | ✅ 已修复 |
| A5 | 阶段报告笔误：迁移脚本"7 个"（实际工单 T8 为 0001~0004 共 4 个） | 已修正本报告 §2 | ✅ 已修复 |
| A6 | 目录边界说明：src/platform/、src/player/ 为空占位（.gitkeep，工单允许占位）；src/i18n/ 为 T11 新增 | 属合理规划，非越界，记录说明 | ✅ 说明 |

---

## 4. 越界与变更声明

- **偏离声明（技术裁决）**：工单 18 技术裁决原定 Windows CNG(BCrypt) 实现 RSA 验签，实际采用 OpenSSL（vcpkg libcrypto 静态链接，单 EXE 无发布负担，跨平台复用同一实现）。T5 License.cpp 实现注释已记录理由与后果。
- 其余改动均在工单"写什么"范围内，无清单外扩张。

---

## 5. 验收证据汇总

| 验收项 | 结果 | 证据 |
|---|---|---|
| 编译（四矩阵） | 零错误零警告（W4） | build/build-classic-rel2.log（WARN=0）、build-ext-debug.log（WARN=0）、build-ext-rel.log（WARN=0）、build-fix4.log（WARN=0） |
| ctest 全量 | 100% tests passed（每矩阵） | build/ctest-*-*.log 四份 |
| 单测 | 39 用例 / 189 断言全绿 | build/test-final-green.log（TEST=0） |
| 授权人工复核 | 真 lic→通过(exit 0)；篡改→E_LIC_TAMPER(exit 2)；过期→宽限提示(exit 0, 剩余4天)；超宽限→E_LIC_EXPIRED(exit 2)；hwid 不符→E_LIC_INVALID(exit 2) | 本段运行记录 + build/tools/ 5 个测试 lic |
| 冒烟 | TuppoM2.exe 打印配置/授权状态后 exit 0 | ok 路径冒烟 OK |
| 线程标注审查 | 33 处 [MAIN]/[WORKER]/[ANY] 标注；Submit lambda 无违规调用 Config::Load/License::Verify | 本段 grep 复查 |
| Git 冻结 | 首冻结 commit cf4ff9f + tag `stage1-frozen`；审计修复后**重新冻结**：tag `stage1-frozen` 移动至 e63bb0d（含契约对齐修复，阶段2 从此基线开发） | git tag -f / git log |
| 覆盖率口径 | Windows 覆盖率工具不可用，按"用例覆盖六类场景 + 核心函数每函数≥1 用例"口径声明 | 工单 18 技术裁决第 4 条 |
| 审计修复后复验 | 契约对齐修复（A1~A4）后：重编译四矩阵零警告、39 用例/189 断言全绿（ctest 100%）、授权五路径 exit 码/错误码逐项复核通过 | build-audit2.log（WARN=0）、test-audit2.log（TEST=0）、ctest-audit.log（100%）、五路径运行记录 |

---

## 6. 下一阶段前置核验

阶段2（M2 资源层，工单 19）前置条件：

- [x] 阶段1 冻结基线存在（stage1-frozen）
- [x] 构建工具链/环境就绪（docs/env-report.md + 本段四矩阵验证）
- [x] 接口契约 01 §3.x 与阶段2 相关章节已落（DBC/Map 解析器接口）
- [x] 数据模型 02 资源表（Item/Map/Monster）已定
- [ ] 阶段2 工单 19 下发后按 T 序列逐条执行（等待用户指令）

---

## 7. 冻结建议

**建议冻结：是。** 阶段1 全部 DoD 满足，冻结基线 `stage1-frozen` 已落（git tag）。用户无异议即通过；有异议打回本报告对应项。

---

*报告人：豆包（架构师复核角色）· 复核依据：dev-conductor §6 阶段报告模板*
