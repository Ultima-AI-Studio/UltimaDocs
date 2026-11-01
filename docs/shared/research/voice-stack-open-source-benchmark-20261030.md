# 开源语音助手/Agent 语音栈源码级基准（ASR / KWS / TTS 逻辑对照）

- **版本**：v1.0 · 2026-10-30
- **性质**：调研资料（源码级核实），非开发决策；落地改动需用户拍板
- **触发**：用户质疑"白龙马是不是并行流式？市售/开源产品 ASR/KWS/TTS 用的什么逻辑？"，并明确要求把已拉取源码逐一拆开分析
- **源码来源（浅克隆/zip，只读未改动）**：
  - 白龙马 BaiLongma `xiaoyuanda666-ship-it/BaiLongma`（main）— 已有（10-29 审计）
  - 大飞鱼 dsh-pet `PC2005-cloud/dsh-pet`（npm 0.3.8）— 已有（10-29 审计）
  - **新增** OpenVoiceOS ovos-core（dev）— 智能音箱/语音 Agent 平台核心
  - **新增** OpenVoiceOS ovos-listener（dev）— 唤醒 + STT 编排
  - **新增** OpenVoiceOS ovos-audio（dev）— TTS/播放编排
  - **新增** whisper-real-time `davabase/whisper_real_time`（master）— 流式转写参考实现
  - **新增** whisper-openai `openai/whisper`（main）— 离线整段转写参考
- **克隆位置**：`docs/research/sources/{ovos-core,ovos-listener,ovos-audio,whisper-real-time,whisper-openai}/`
- **代理说明**：本机 git 全局代理 127.0.0.1:1080 未运行（Test-NetConnection open=False），但 GitHub 443 直连通；git clone 全部走代理失败，改用 python urllib 直连 codeload 下载 zip 解压成功

---

## 一、结论（先行）

**所有成熟语音助手/Agent 都走"流式 + 并行"路线，我们现网是三处串行。差距不是算力，是架构。**

| 产品 | KWS | ASR | TTS | 判定 |
|---|---|---|---|---|
| 白龙马 | 本地 sherpa streaming transducer（chunk-16） | **云端流式为主**（阿里 Paraformer realtime-v2 duplex 首选）+ 本地 Whisper 兜底 | **云端流式为主**（豆包 Chunked/OpenAI/ElevenLabs）+ 无本地 | 端云分离 + 双流式 |
| 大飞鱼 | 无 | 无 | 云端 Edge-TTS 串行队列 | 仅配音，非对话链路 |
| OVOS（Mycroft 系） | 本地多引擎（每 200ms 查一次 + 环缓冲） | **Producer/Consumer 双线程 + STT 流式接口**（边说边送） | 线程化播放 + 插件化流式 TTS | 全并行流水线 |
| whisper-real-time | — | 伪流式（每次整段重转写 + phrase_timeout 判句界） | — | 半流式参考 |
| whisper-openai | — | 离线整段 transcribe | — | 非流式 |
| **我们现网** | 本地 sherpa（2 变体、score 1.0） | **本地离线整段**（SenseVoice CPU，等 3s 静音） | **本地整段合成再播**（CV3 克隆，串行） | 三处串行 |

---

## 二、白龙马（BaiLongma）—— 端云分离 + 双流式

### ASR（`src/voice/cloud-asr.js`）
- **首选云端流式**：阿里云百炼 Paraformer `paraformer-realtime-v2`，sample_rate 16000，pcm，**streaming duplex**（WebSocket 双向：run-task → PCM binary chunks → finish-task）
- 同轨：腾讯云 ASR / 科大讯飞 RTASR / 火山引擎豆包流式 ASR / macOS Speech.framework
- `MAX_PENDING_CHUNKS=16`（~4s 防堆积）
- **本地兜底**：`whisper_server.py`（openai-whisper 包，Python 子进程，WebSocket 3723；VAD 阈值静默 0.005/有声 0.010/峰值 0.015 + 幻觉过滤 + YAMNet 可选）

### KWS（`electron/kws-process.cjs` + `src/voice/kws-model/`）
- **本地 sherpa-onnx**，独立 utilityProcess 隔离 onnxruntime 冲突
- **streaming transducer 模型**：`epoch-13-avg-2-chunk-16-left-64`（chunk=16，上下文 left=64）
- 参数：`KEYWORDS_THRESHOLD=0.35`（从 0.25 上调减误触发）、`KEYWORDS_SCORE=3.0`（实测 score=3 召回 13/17 vs 2.0 的 9/17）、`COOLDOWN_MS=800`
- **唤醒词 6 个发音变体**（keywords.txt 原文）：xiǎo bái lóng / xiǎo bái le / xiǎo bái róng / xiào bái lóng / xiǎo huái lóng / xiǎo bái ma —— 全部映射"小白龙"，覆盖口音/吞音

### TTS（`src/voice/tts-providers.js`）
- **云端流式为主**：豆包方舟（HTTP Chunked，decodeDoubaoStream 按行解析 base64 音频，seed-tts-2.0/1.0 自动选）、OpenAI TTS、ElevenLabs
- 非流式：MiniMax、火山引擎
- **无本地 TTS、无克隆音色**

### 语音策略层
- voice-core + **voice-continuous（连续对话）** + voice-ptt（按住说话）+ voice-panel；barge-in 打断检测

---

## 三、大飞鱼（dsh-pet）—— 仅配音，非对话链路

- `host/voice`：Edge-TTS 云端合成（`@andresaya/edge-tts`，WebSocket/SSML，15s 超时）+ **串行队列**（MAX_QUEUE=3 先点先响）+ 缓存键含来源 + 发起端一次性标记防双播
- **无 ASR、无 KWS、无本地克隆** —— 定位是"气泡配音"，不参与识别对比

---

## 四、OpenVoiceOS（ovos-core + ovos-listener + ovos-audio）—— 全并行流水线参考

### ovos-listener（`ovos_listener/listener.py` + `mic.py` + `silence.py`）
- **Producer/Consumer 双线程并行**：`AudioProducer`（持续采集 + 唤醒检测）→ Queue → `AudioConsumer`（消费音频做 STT）。采集与识别互不阻塞。
- **STT 流式接口**：`self.loop.stt.can_stream` 为真时启用 `AudioStreamHandler`，`stream_start()/stream_chunk(chunk, lang)/stream_stop()` —— **边说边送**，不是等整段录完
- **唤醒词引擎**：`create_hotword_engines()` 支持多词（wakeup/listen/stopword 三类）；`_wait_until_wake_word()` 用 **CyclicAudioBuffer 环缓冲**（保留最近 N 秒）+ `SEC_BETWEEN_WW_CHECKS = 0.2`（**每 200ms 查一次**）
- **VAD 端点检测（替代固定静音）**：`SilenceDetector` 用 **Silero VAD**（`vad_threshold=0.2`，chunk 960=60ms，`silence_seconds=0.5` —— 说完成 0.5s 静音即判 PHRASE_END）；另有 `MIN_SILENCE_AT_END = 0.25` 兜底。**没有"等满 N 秒"的固定静音**
- 连续对话：`ListenerState.CONTINUOUS / HYBRID`，唤醒后持续听（listen_timeout=45s 回退唤醒态）
- `MIN_AUDIO_SIZE = 0.5`（过短音频丢弃）；`recording_timeout=10.0` / `recording_timeout_with_silence=3.0`

### ovos-audio（`ovos_audio/service.py`）
- `PlaybackService(Thread)`：**独立播放线程**，TTS 插件化（`TTSFactory`），支持流式 TTS 插件；`playback_lock` + 队列管理播放

### 对 UltimaAgent 的可抄点（源码级）
1. **Producer/Consumer 双线程**：采集线程与 STT 消费线程解耦，采集不阻塞识别（现网是单线程串行）
2. **STT 流式接口**：can_stream → stream_chunk 边说边送（现网整段 WAV 喂离线识别）
3. **Silero VAD 端点检测**：说完成 0.5s 即断句，替代现网 `QUIET_AFTER_SPEECH=3.0` 固定静音（**最大的单点延迟**）
4. **唤醒每 200ms 查一次 + 环缓冲**：现网按 chunk（8820 采样 ≈ 0.55s）粒度，可减延迟
5. **多唤醒词分类**（wakeup/listen/stopword）：现网只有单一命中逻辑

---

## 五、whisper-real-time / whisper-openai —— 流式参考与反例

### whisper-real-time（`transcribe_demo.py`）
- **伪流式**：后台线程持续采集入 Queue，每 0.25s 轮询；**每次有新音频就把整段累积缓冲重新 `transcribe` 一遍**（覆盖式刷新显示）
- 判句界：`phrase_timeout=3`（两次录音间隔超 3s 视为新句）—— 即"重转全量 + 时间窗断句"，非增量解码
- 结论：不是真正 streaming，但展示了"边说边出字"的用户体验形态（CLI 逐句刷新）

### whisper-openai（`whisper/transcribe.py`）
- **离线整段**：`transcribe(audio)` 一次吃整段，无流式接口（社区流式方案都是在其上包伪流式）
- 我们现网 faster-whisper 同源

---

## 六、对现网差距的量化结论（源码级对照）

| 环节 | 白龙马/OVOS | 现网 UltimaAgent | 差距 |
|---|---|---|---|
| 唤醒 | 6 变体 / score 3.0 / 每 200ms | 2 变体 / score 1.0 / 每 ~0.55s | 变体少、评分低、轮询粗 |
| 说完判定 | Silero VAD 0.5s | 固定静音 **3.0s** | **吃掉 ~2.5s/次** |
| ASR | 云端流式/双线程流式 | 本地离线整段（CPU num_threads=2） | 边说边出 vs 等完再认 |
| TTS | 流式/线程播放 | 整段合成再播 | 首帧延迟大 |
| 架构 | 采集∥识别∥合成 | 采集→识别→合成 串行 | 并行 vs 串行 |

**一句话**：人家快在"说话的同时系统就在干活"（流式 + 并行 + VAD 端点检测），我们快不了是因为"等你说完 → 等 3s 静音 → 整段识别 → 整段合成"四段全串行，且 ASR 没用上本地 GPU。

---

## 七、建议落地方向（均需用户拍板，属参数/架构外改动）

1. **立即止损（低风险）**：`QUIET_AFTER_SPEECH` 3.0 → 引入 Silero VAD 端点检测（sherpa-onnx 已带 SileroVadModelConfig，asr.py 已有加载代码但未用于断句）
2. **KWS 对标白龙马**：补充"贾维斯"发音变体（快读/吞音写法）+ `keywords_score` 1.0→3.0（白龙马实测召回 13/17 vs 2.0 的 9/17）
3. **架构改造（中风险）**：采集/识别拆双线程（Producer/Consumer），STT 支持流式 chunk 送入；TTS 播放线程化
4. **算力利用**：ASR 从 CPU（num_threads=2）切 3060/3080 Ti GPU，识别从"秒级"降"百毫秒级"

---

## 八、变更登记

| 版本 | 日期 | 变更 |
|---|---|---|
| v1.0 | 2026-10-30 | 新建；补拉 ovos-core/ovos-listener/ovos-audio/whisper-real-time/whisper-openai 源码并逐一拆解 ASR/KWS/TTS 逻辑；与白龙马/大飞鱼对照形成结论 |
