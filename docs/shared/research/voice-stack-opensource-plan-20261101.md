# UltimaAgent 语音链路（KWS/ASR/TTS）开源代码对照与修复方案

- **方案编号**：G-PLAN-20261101-voice-stack
- **创建日期**：2026-11-01
- **方案性质**：基于 GitHub 开源代码的代码级对照调研 + 修复方案（先方案、后工单，G-PLAN-001）
- **关联背景**：真机三要点验收（完整语音唤起 3/3 · 随意问可答 5/5 · 回答准确性 ≥80%）；云端 DeepSeek 对照实验已接入
- **关联文档**：`docs/specs/kws-wakeup-params-baseline.md`（KWS 参数权威基线）、`docs/reports/voice-e2e-acceptance-20261101.md`（验收口径）

---

## 一、背景与目标

### 1.1 问题陈述

真机复测暴露两个核心问题：

1. **唤醒不稳定**：用户喊"幂幂"2-3 次才命中（16:41-16:42 实测：强信号 peak=0.0808/0.0478 未命中，弱信号 peak=0.0002 反而命中）
2. **正常问题被挡**："今天有什么新闻？"ASR 识别一字不差，但路由门 `ABSTAIN low_similarity:0.3360` → 回复"我没听清，请再说一遍。"，云端 DeepSeek 与本地 8B 均无机会回答
3. **TTS 漏句**：CV3 对"X点/时Y分+星期X"及"二十四分"等组合确定性漏内容（1.2-2.3s 只出声尾），拆句单独合成均正常

### 1.2 已确认的架构判断

问题归属为**系统链路/编排策略**，而非引擎能力：

- 引擎层面（sherpa KWS / SenseVoice / CosyVoice3）已是本地最优组合，无需换云端引擎
- 换云端 KWS/ASR/TTS 无法解决——"理解判定、回答约束、调用方式"均为编排层问题
- 本方案通过 GitHub 开源代码对照，定位代码级根因并给出修复路径

---

## 二、调研范围与开源来源（GitHub）

### 2.1 已抓取的开源代码

| 仓库 | 文件 | 用途 |
|---|---|---|
| k2-fsa/sherpa-onnx | `python-api-examples/keyword-spotter.py` | KWS 官方调用范式（含动态关键词） |
| k2-fsa/sherpa-onnx | `python-api-examples/offline-decode-files.py`（参考） | 离线解码/热词用法 |
| k2-fsa/sherpa-onnx | 官方文档 `kws/`、`hotwords/` 页 | keywords 格式、热词支持边界 |
| FunAudioLLM/CosyVoice | `cosyvoice/cli/cosyvoice.py` | TTS 官方推理（split=True 逐句 yield） |

### 2.2 本地现状事实（已核对）

- `config/voice-profile.json`：`voice.engine=cv3`，ref=`data/voice/yangmi-ref/yangmi_cv3_full_s6_v54.wav`
- `models/sherpa/kws/keywords.txt`：8 行（6 贾维斯变体 + `m ì m ì @幂幂` 1 行 + ULTIMA）
- ASR 模型：`models/sherpa/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-2024-07-17`（2024 版）
- TTS 源码：`v0r3/cv3/TtsProbe/source/CosyVoice-074ca6dc...`（确认是 CosyVoice 3，`cosyvoice3.yaml`）
- ASR 主链路：`asr_transcribe()` 已以 sherpa SenseVoice 为首选（2024-07-17 版 int8），faster-whisper 为兜底

---

## 三、代码级对照与根因分析

### 3.1 TTS 漏句根因（实锤）：官方逐句 yield，我们 `break` 只取第一段

**CosyVoice 官方源码（`cosyvoice.py` → `inference_zero_shot`）：**

```python
def inference_zero_shot(self, tts_text, prompt_text, prompt_wav,
                        zero_shot_spk_id='', stream=False, speed=1.0,
                        text_frontend=True):
    prompt_text = self.frontend.text_normalize(prompt_text, split=False,
                                               text_frontend=text_frontend)
    for i in tqdm(self.frontend.text_normalize(tts_text, split=True,
                                               text_frontend=text_frontend)):
        # split=True：文本按标点切分为多句，逐句处理
        if (not isinstance(i, Generator)) and len(i) < 0.5 * len(prompt_text):
            logging.warning('synthesis text %s too short than prompt text %s, '
                            'this may lead to bad performance', i, prompt_text)
        model_input = self.frontend.frontend_zero_shot(
            i, prompt_text, prompt_wav, self.sample_rate, zero_shot_spk_id)
        for model_output in self.model.tts(**model_input, stream=stream,
                                          speed=speed):
            yield model_output   # 每句 yield 一段音频（生成器）
```

**我们的实现（`src/brain/voice/tts.py` L121-126）：**

```python
speech = None
for block in cosy.inference_zero_shot(text, prompt_text, str(prompt_wav),
                                      stream=False, speed=1.0):
    speech = block["tts_speech"]
    break          # ← 只取第一个 yield，后续分句全部丢失
if speech is None:
    raise RuntimeError("no speech block produced")
```

**根因结论：**

- 官方 `text_normalize(split=True)` 把整句按标点切分，逐句合成并 yield 多段音频
- 我们 `break` 只取第一段，长句/多句文本的后续分句被丢弃 → 确定性漏内容
- 与实测完全吻合：拆句单独传（单段）正常；整句传（官方切多句）只拿到第一段 → 漏
- 官方另警告：分句过短（< prompt_text 一半长度）克隆性能差——"星期日。"等短句会触发该警告

**修复方向：** 收集全部 yield 段并按时间轴拼接，去掉 `break`。

### 3.2 KWS 换唤醒词：官方支持 per-stream 动态关键词，我们绕了远路

**sherpa 官方示例（`keyword-spotter.py`）：**

```python
# 预定义关键词
s = kws.create_stream()
# 运行时动态加一个关键词（无需改文件、无需重启）
s = kws.create_stream("y ǎn y uán @演员")
# 一次动态加两个关键词（'/' 分隔）
s = kws.create_stream("y ǎn y uán @演员/zh ī m íng @知名")
```

**我们的实现（0014 链路）：** 重写 `keywords.txt` + daemon 热重载。

**结论：** 官方有原生 per-stream 动态关键词机制，换唤醒词应直接 `create_stream(新拼音 @新词)`，链路更短、无文件竞态。现有"文件+热重载"可作为持久化后备（重启后仍需 keywords.txt 落盘），但运行时切换应走原生机制。

### 3.3 keywords 逐词参数：官方支持每词独立 score / threshold

**官方 keywords 文件格式（kws 文档）：**

```
小爱同学 :2.0 #0.6 @小爱同学
你好问问 :3.5 @你好问问
小艺小艺 #0.6 @小艺小艺
x iǎo y ì x iǎo y ì #0.6 @小艺小艺
```

- `:N` = boosting score（该词独立增强分，越大越易检出）
- `#N` = trigger threshold（该词独立触发阈值）
- `@词` = 原始词面（fpinyin/ppinyin 类型必填，词面不能含空格）

**我们的现状：** 幂幂仅 `m ì m ì @幂幂`，无独立参数、无变体。

**结论：** 幂幂灵敏度问题可通过"补变体 + 逐词 `:score`"解决，**全局 `keywords_threshold=0.08` 红线不动**，符合基线文档约束。

### 3.4 ASR 热词边界：SenseVoice 不支持 hotwords（官方文档铁证）

**官方 Hotwords 文档明确：**

> Only transducer models support hotwords in sherpa-onnx. ... All other models don't support hotwords. Also, you have to change the decoding method to modified_beam_search to use hotwords. The default greedy_search does not support hotwords.

- SenseVoice 是 encoder-only 非自回归模型，**不支持 hotwords**
- 要热词/上下文纠错，必须用 transducer 类模型（流式 zipformer 中文 / paraformer，需 modified_beam_search）
- 现有"近音映射（如 水量天听→天气）+ VAD 精切"是 SenseVoice 下的正确补救手段

---

## 四、修复方案（改动清单）

### 改动 1：TTS 收集全部分句段并拼接（根治漏句）

**文件**：`src/brain/voice/tts.py`（`_INLINE_SCRIPT` 内 L121-134）

**修复前：**

```python
speech = None
for block in cosy.inference_zero_shot(text, prompt_text, str(prompt_wav),
                                      stream=False, speed=1.0):
    speech = block["tts_speech"]
    break
if speech is None:
    raise RuntimeError("no speech block produced")
```

**修复后（示意，实施时以实际 tensor 维度为准）：**

```python
import torch
blocks = []
for block in cosy.inference_zero_shot(text, prompt_text, str(prompt_wav),
                                      stream=False, speed=1.0):
    seg = block["tts_speech"]
    if seg is not None and seg.shape[1] > 0:
        blocks.append(seg)
if not blocks:
    raise RuntimeError("no speech block produced")
speech = torch.cat(blocks, dim=1)   # 官方 tts_speech 第二维为时间轴
```

**要点：**

- 收集全部 yield 段，按时间轴（dim=1）拼接
- 拼接后保留现有峰值归一化逻辑（L127-133）不变
- 现有 daemon `_guard_tts_completeness` 防护保留为二级兜底，不删除

### 改动 2：幂幂补发音变体 + 逐词 boosting score

**文件**：`models/sherpa/kws/keywords.txt`（经 0014 用户入口写入，不手工直改）

**候选变体（实施前用 sherpa-onnx-cli 校验音素在位）：**

```
m ì m ì :2.5 @幂幂
m í m i :2.5 @幂幂
m í m ì :2.5 @幂幂
m ì m i :2.5 @幂幂
m í m :3.0 @幂幂
```

**约束：**

- 全局 `keywords_threshold=0.08`、`keywords_score=2.0`、`num_trailing_blanks=8` 红线不动
- 变体补全后需同步 `config/voice-profile.json` 的 `wakeword.words` 与基线文档
- 真机回归：单次唤醒即应，且不新增误唤醒；若误唤醒增多，回退 score 并登记

### 改动 3：换唤醒词运行时改用官方动态机制

**文件**：`src/brain/voice/kws_listener.py` / daemon KWS 调用段

**方向：**

- 运行时切换：`create_stream("拼音 @新词")` 动态生效，不再依赖文件热重载
- `keywords.txt` 保留为持久化层（重启后加载），用户入口同时写文件 + 动态 create_stream
- 需评估现有热重载逻辑与动态机制的统一出口，避免双路径

### 改动 4：路由门宽进（架构项，与本方案同步排期）

**文件**：`src/brain/routing/intent_gate.py`、`src/brain/interaction.py`

**方向：**

- `ABSTAIN` 从"我没听清"改为**放行到云脑/本地模型**（宽进）
- `DENY` 才拒绝（有害内容/规则）
- 安全校验移至出口（回答校验器）与执行层（工具权限），入口不再挡正常提问
- 云脑（DeepSeek，5.8 节）已接入，宽进后即对真机开放域问题生效

### 改动 5（备选）：ASR 升级或换通道

**低成本路径（5A）：**

- SenseVoice 升级到 `sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2025-09-09` 新版
- 开启 `use_itn=1`（数字/时间逆文本归一化，治"几点"类偏差）
- 保留近音映射 + VAD 精切

**热词路径（5B，仅 5A 后丢字仍不达标时启用）：**

- 换 sherpa-onnx 流式 zipformer 中文 transducer（支持 hotwords + modified_beam_search）
- 热词表：幂幂/贾维斯/天气/新闻/时间/几点/任务
- 代价：需重测冻结 ASR 参数并更新基线文档

---

## 五、验收标准（对齐三要点）

### 5.1 完整语音唤起 3/3

- 连续 3 次"幂幂"单次命中即唤醒（无需喊多次）
- 无新增误唤醒（背景声/指令词不触发）

### 5.2 随意问可答 5/5

- 5 个开放域问题（含"今天有什么新闻？"）不再出现"我没听清"
- 路由门宽进后，问题进入云脑/本地模型并产生有效回答

### 5.3 回答准确性 ≥80%

- 时间句（"X点/时Y分+星期X"、"二十四分"等）TTS 全段完整，无漏内容
- 验证音频时长与文本长度匹配（完整句 ≥4.8s；漏句特征 1.2-2.3s 不再出现）
- 回放采样率 44100（WASAPI idx24），重采样链路正常

### 5.4 回归验证

- 改动 1 后真机复测时间句：同一文本连合 3 次均完整
- 改动 2 后真机复测唤醒：变体覆盖语速/声调变化
- 既有 TTS 防护、重采样、时间直达逻辑不回归

---

## 六、实施顺序与风险

### 6.1 推荐顺序

1. **改动 1（TTS 拼接）**——代码改动小、根因明确、可立即真机验证
2. **改动 4（路由门宽进）**——解锁开放域问题，云脑随即生效
3. **改动 2（幂幂变体+score）**——解决唤醒灵敏度
4. **改动 3（动态 create_stream）**——简化换词链路
5. **改动 5A（ASR 升级+ITN）**——按需推进；5B 作为备选

### 6.2 风险与约束

| 风险 | 说明 | 应对 |
|---|---|---|
| 全局参数红线 | 基线禁止动态自适应阈值 | 改动 2 仅用逐词参数，不动全局 0.08/2.0/8 |
| 变体音素 | 新拼音可能不在 tokens.txt | 实施前 sherpa-onnx-cli 校验 |
| 误唤醒 | score 提高可能增加误触发 | 真机回归，增多则回退 |
| 拼接维度 | tts_speech 维度需与官方一致 | 实施时核对 shape，dim=1 拼接 |
| 双路径 | 动态机制与文件热重载并存 | 统一出口，文件仅作持久化 |
| 未提交代码 | interaction.py 时格式+云脑、daemon 防护未 commit | 实施前先收口现有改动，再排新工单 |

### 6.3 待确认决策

1. 改动 1-4 是否按 6.1 顺序整体派发（单工单或拆分）
2. 改动 5 先走 5A 还是直接评估 5B
3. 云脑在宽进后的优先级（云优先 vs 本地优先、云失败降级）
4. 实施完成后 git tag 命名与冻结口径

---

## 七、引用来源

- k2-fsa/sherpa-onnx KWS 示例：`python-api-examples/keyword-spotter.py`（GitHub）
- k2-fsa/sherpa-onnx 官方文档：Keyword spotting（kws/）、Hotwords (Contextual biasing)（hotwords/）
- FunAudioLLM/CosyVoice 官方推理：`cosyvoice/cli/cosyvoice.py`（GitHub）
- 本地权威基线：`docs/specs/kws-wakeup-params-baseline.md`
