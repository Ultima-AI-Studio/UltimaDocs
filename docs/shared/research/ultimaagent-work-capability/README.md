# UltimaAgent 工作能力改造镜像

权威源为 H:/UltimaAI/UltimaAgent 项目 docs；本目录保持方案、契约和阶段报告的原始字节副本。状态以原单 wo-ultimaagent-20261101-0021 和阶段回执为准。

T0 r2 独立计划评审 PASS，项目检查点 ultimaagent-work-capability-t0-plan-pass-20261101，项目提交 6b70aa6f9223829682ec995fecc7d51952a3e717。该检查点仅允许下一步 T1，不表示产品能力、原单完成、Owner 冻结或发布。

- [实施计划](plans/jarvis-work-capability-delivery-plan-20261101.md)
- [目标契约](specs/jarvis-work-capability-contract-20261101.md)
- [T0报告](reports/jarvis-work-capability-t0-20261101.md)
- [独立评审](evidence/independent-plan-review-r2.json)
- [完整项目证据](https://github.com/Ultima-AI-Studio/Ultima-Agent/tree/6b70aa6f9223829682ec995fecc7d51952a3e717/data/evidence/jarvis-work-capability/T0)

T1 文件交付链技术门 PASS：60 项新鲜回归通过，三个独立候选进程和运行/输出目录完成真实 CLI → NativeReAct → SDK 文件工具 → 外部读回。项目检查点 `ultimaagent-work-capability-t1-technical-pass-20261102` 解析至 `c600c5c854d3ee6968d18c0a264430c3b80756e9`，测试与独立审查绑定的产品代码为 `2e0682c2d4b0a79928fd3d8ad2325d017015f7fd`；其后仅补文档和证据。原运行服务未切换，T2—T5 与 Owner 验收仍待完成。

- [T1报告](reports/jarvis-work-capability-t1-20261102.md)
- [T1独立审查](evidence/T1/independent-task-review-r1.json)
- [T1技术门](evidence/T1/t1-gate.json)

2026-11-02 T2 停点为 **BLOCKED / 真实验收 FAIL**：最终源码10fec03，149项测试通过且覆盖原60项；E01真实三轮通过，E02第一轮因报告参数和来源事实不符失败，E03最终候选未启动。修复2/2已用，T3—T5不放行，生产代码/语音/KWS未切换。失败检查点 `ultimaagent-work-capability-t2-blocked-20261102` 只保存工作与证据，不是技术PASS或冻结。

- [T2停点报告](reports/jarvis-work-capability-t2-20261102.md)
- [研究执行补充契约](specs/jarvis-work-research-execution-contract-20261102.md)
- [独立实际验收](evidence/T2/independent-final-live-review.json)
- [T2门状态](evidence/T2/t2-gate.json)
- [待决定的模型对照提案](plans/jarvis-work-model-comparison-proposal-20261102.md)（未执行、不改生产默认模型）

T1报告同步增加了旧兼容测试H根隔离缺口及当前C候选隔离补证，保留原T1不可变tag/日志，不以新结果抹掉历史。
