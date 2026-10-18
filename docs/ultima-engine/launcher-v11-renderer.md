# TuppoM2 热血传奇正式版 V1.1 — 真实画面渲染器交付说明

> 状态：V1.1 渲染核心已落地并自测闭环（2026-10-09）
> 前置：V0.1 链路（WebView2 登录器 → 选区 → 拉起 800×640 自研 GDI 客户端 → 移动/攻击/白圈/飘伤）已冻结；
> V1.1 = 在迷你客户端之上用真实传奇图素渲染，替换 V0.1 绿块方案。

## 1. 素材与格式破解结论（已实证，勿再改）

| 项 | 结论 |
|---|---|
| 素材根 | `C:\Users\Administrator\Downloads\传奇私服1.76客户端\`（Data\ 图库 + Map\0.map + Wav\545 音效） |
| WIL/WIX 格式 | WIX：count u32@44 + 偏移表 @48+i*4（绝对文件偏移）；WIL：count u32@44、colorCount=256@48、paletteSize=1024@52、调色板@56 起 256 项×4B（BGR 序）；图块=8B 头（w u16,h u16,px int16,py int16）+ 连续 w×h 调色板索引（0=透明，无 RLE 无压缩） |
| npal.idx | 弃用——调色板在 WIL 内部，外部调色板映射全部失败（历史已试） |
| 0.map（HGE 2B/格） | 头 20B（w u16+h u16+title 16B）+ 每格 2B；位域方案 B：`tile=v>>10`（高 6 位→Tiles.wil）、`obj=v&0x3FF`（低 10 位→Objects.wil） |
| 1×1 占位块 | Objects 前 ~19 块 1×1 占位必须跳过（w*h<64 判定） |
| TuppoM2 MapParser | OpenMir2 新版格式（52B 头+12B/格），与此 .map 不同——客户端自解析，碰撞仍以 M2 服务端权威为准 |

## 2. 渲染管线（本版交付）

```
TuppoGameClient.exe
  ├─ WilLib        WIL/WIX 解析：小端读取、调色板@56、GetBitmap→w/h/px/py/indices
  ├─ MapView       0.map + Tiles/Objects：kCellPx=48 整块地表 SetDIBitsToDevice、
  │                CreateDIBSection+AlphaBlend 物件、objCache 按 w*h<64 跳过
  ├─ SpriteView    Hum/Mon 精灵帧缓存：BGRA + DIBSection，空帧(8×5)跳过
  └─ GameDraw      集成：真实地图背景 + 玩家 Hum 帧 + 怪物 Mon1 帧 + 掉落金块
                   + HUD（等级/坐标/击杀/拾取/背包 + 系统消息）
```

## 3. 视口调整（与 V0.1 的差异）

| 项 | V0.1 | V1.1 |
|---|---|---|
| 格像素 kCell | 32 | **48**（传奇地表标准） |
| 视口 | 24×18 格（768×576） | **16×12 格（768×576）** |
| HUD | 64px | 64px（不变，640=576+64） |
| 窗口 | 800×640 | 800×640（不变） |

## 4. 修复的关键坑（本版闭环）

1. **fread 读 0 字节**：fseek(SEEK_END) 后未回 SEEK_SET → 文件指针在末尾读空；WilLib/MapView 两处 ReadFile 已修。
2. **AlphaBlend 未链接 msimg32** → LNK2019；TuppoLauncher/TuppoGameClient 均已加。
3. **GDI+ 未初始化存 PNG 失败(2)**：RunMap/RunSpriteShot 补 UiGdiPlusStart；img 析构先于 UiGdiPlusStop（作用域块）。
4. **中文路径 fopen 失败**：双修复——①main 入口用 `CommandLineToArgvW(GetCommandLineW())` 重建 UTF-8 argv（argv 为 ANSI 会损坏中文）；②ReadFile 改 `_wfopen_s` 宽字符打开。**中文安装路径现可正常加载素材**。
5. **TuppoLauncher 被误覆盖**：tools\launcher 的 TuppoLauncher（老版 GDI）与 launcher\ 的 WebView2 正式版同名；已从 launcher\ 工程重编恢复 659,456B。**铁律不变：只同步 TuppoGameClient.exe 到 launcher\build\Release\，绝不覆盖 TuppoLauncher.exe**。
6. **人物"反的/倒立"（WIL 行序自下而上）**：用户反馈画面角色上下颠倒。三重实证：①像素质心分析——未翻转时肤皮质心 y/h=0.56（偏下）、阴影质心 0.34（偏上）= 头朝下；②权威 npm wil-parser 对照——getBitmap 原始索引直写 BMP（BMP 高度为正时像素自下而上，jimp 正确还原为正立）→ **WIL 图块数据行序自下而上**；③翻转前后 gfx-shot 对比——翻转前阴影在角色"旁边/上方"、翻转后"角色脚下对应阴影、蓝内裤站立正常"。**修复：SpriteView（Hum/Mon）与 MapView 物件（Objects）渲染时 Y 翻转（srcY=h-1-y）；地表 Tiles 无方向性纹理保持原序**。修复后 ASCII 场与中文生产路径全链路 GFX SHOT 均 OK。

## 5. 自测证据链（命令行 Session 无 GUI 窗口，全部离屏 PNG 自证）

| 验证 | 结果 |
|---|---|
| `--map --shot` 三坐标 (300,300)/(150,150)/(500,400) | MAP SHOT OK×3，Read 复核：真实沙地+水域+植被+石块 |
| `--sprite-shot` Hum 40-79 / 80-119 / Mon1 0-39 | 站立/走路/倒挂人物 + 持兵器怪物帧，PNG 保存成功 |
| Hum 帧节奏 | 每 8 帧一组 = 4 有效 + 4 空（f40-43 有效 60×75、f44 空 8×5、f48-51 有效、f52 空…） |
| 中文路径 `--map --shot` | MAP SHOT OK（GetCommandLineW+_wfopen 修复后） |
| 全链路 `--direct --data <中文路径> --gfx-shot` | 登录 charId=25 → 地图加载 OK（700×700）→ 精灵 OK（Hum=10800 Mon=1086）→ GFX SHOT OK；Read 复核：真实地图 + 站立角色 + HUD |
| 人物朝向修复（WIL 行序） | 翻转前后 zoom 对比：翻转前"阴影在旁侧"→ 翻转后"脚下对应阴影、蓝内裤站立正常"；ASCII 场 + 中文生产路径均 GFX SHOT OK |

产物：`C:\mir176\map_shot1/2/3.png`、`hum_40.png`、`mon1_0.png`、`gfx_v11.png`、`gfx_v11_cn.png` 等。

## 6. 二进制（正式版目录，已同步）

| 文件 | 大小 | 说明 |
|---|---|---|
| `launcher\build\Release\TuppoLauncher.exe` | 659,456B | WebView2 正式版登录器（含 game.launch 新增 `--data` 传参） |
| `launcher\build\Release\TuppoGameClient.exe` | 483,840B | V1.2 精修版渲染客户端（Mon1-18 多库；--direct/--map/--sprite-shot/--gfx-shot/--smoke） |

## 7. 遗留（V1.2 迭代项，不影响 V1.1 验收）

**V1.2 六项已全部实现（2026/10/9）**：

- **V1.2-1 方向映射**：Hum 帧结构实证定案——40=站立；41-43=待机；48-51=跑；56-59=攻击；64 起行走 4 方向×6 帧（64=北 dir0 背面、72=西 dir2、80=南 dir4 正面、88=东 dir6）。GameTryWalk 记 selfDir、S_MOVE 确认回写；行走 `HumWalkBase(selfDir)+step%6`，站立固定 40。`--sprite-shot` 已同步 Y 翻转。
- **V1.2-2 怪物多库渲染（V1.2 精修-1 已闭环，2026/10/9）**：
  - 客户端 SpriteView 改为 Mon1-18 多库数组（`mons_[19]`/`monCaches_[19]`，缺库不阻塞）；新增 `MonLib(lib,idx)`/`Mon(idx)`。
  - 服务端 9304 外观字段语义修正为 **race**（BroadcastMgr.cpp `RaceOf(defId)`，ResourceDB 怪表 `monsters(id,name,race)`）。
  - 客户端 `Game::MonSpecFor(race)` 映射：11 卫士{Mon1,0}、51 鸡{Mon17,0}、52 鹿{Mon17,360}、81 多钩猫/钉耙猫/幻影寒虎/山洞蝙蝠/半兽战士{Mon8,100}、82 毒蜘蛛{Mon13,0}、83 半兽人/蛤蟆/森林雪人/稻草人{Mon1,360}、84 蝎子{Mon12,0}、85 食人花{Mon2,0}、86-89 骷髅系{Mon3,0}、90 洞蛆{Mon10,0}、97 沃玛系{Mon5,0}、default{Mon1,0}；攻击帧=base+112+(now/120)%4。
  - **AOI 四叉树根 bug 修复（关键）**：`AoiTree::Insert` 扩展分支旧代码 `st.root = Quad{}` 后再自赋值，读的是重置后的 {0,0}，导致根边界被清成 {0,0}-{0,0} 零大小——Intersects 永远 false、CollectInRange 永远空、全部实体落入零根 ids（rootIds 堆积、nodes=1、AOI 查询全 0、9304 不下发、gfx-shot 视野 0 实体）。修复：先保存扩展后的边界再重建树。修复后 `Query(280,260,12)=12` 与暴力遍历一致、nodes=294、树正常分裂、9304 正常下发（gfx-shot 视野实体=12）。
  - **叠点修复**：`main.cpp` 步骤8 初始刷怪 `spread>0` 时 ±spread 格随机散布（修复前 40 只鸡全叠 (280,260) 同格）。
- **V1.2-3 mapId 映射**：登录响应 mapId → 客户端 `Map\{mapId}.map`，不存在回退 0.map（测试服 map=1 无 1.map，已验证回退日志）。
- **V1.2-4 Magic 特效**：Magic.wil/WIX（4010 块）接入；攻击目标格播 Magic 帧 0-7（火球/发光融合特效）替代白描边；自身攻击播 Hum 56-59 挥砍帧。
- **V1.2-5 掉落物**：DnItems.wil/WIX（566 块）接入；掉落物渲染真实物品图标（**V1.2 精修-2 已闭环**：610 协议带 looks + 真实图标 3 倍放大 + 6 帧旋转动画，见下）。
- **V1.2-6 音效**：WinMM PlaySound 异步接入；Wav 目录（544 个）挂载；攻击=60、受伤=65、死亡=60（编号精调待后续）；触发点：C_ATTACK/S_DAMAGE/S_DEATH。

**V1.2 精修-1 自测证据（2026/10/9 gfx-shot 最终）**：服务端日志 `AOI 验证：tree=2969 nearby12=12 near3=2 near补怪点1=1 nodes=294`、`AOI 暴力对照：12格内实体=12`；客户端 `视野实体=12`；`gfx_v12_final.png`（800×640）中央角色 + 狼形怪（Mon8）+ 左右红色怪（Mon1 系）清晰渲染。

## 7a. V1.2 精修-2 掉落物真实图标（2026/10/9 闭环）

**目标**：掉落物从「DnItem(0) 木板占位」升级为「服务端物品真实 Looks + 地面真实图标动画渲染」。

**数据链路（全程打通）**：

1. `source_assets\real_176\StdItems_geem2.tsv`（GEEM2 标准物品库，含 Looks 列）→ `tools\scripts\gen_assets_176.py`（表头加 `looks` 列 + `cl('Looks','0')`）→ `source_assets\176\Items.tsv`（686 行，第 22 列=looks）。
2. `tools\PrecompileTool`（DbParser.cpp `ParseItemsTsv` 读 looks；CompilePipeline.cpp items 表/INSERT 加 looks 列）→ `runtime\resource.db`（重建 hash=2949369758690174451；`runtime\resource.db.bak-polish2` 备份）。
3. `src\res\ResourceDB`（ItemDef 增 `uint32_t looks`，SELECT 第 22 列）。
4. `src\net\GameMsg.cpp` 两处 610 编码加 `WriteU32(looks)`：L227-238 战斗死亡掉落 AoIBroadcast、L1078-1088 玩家丢包。
5. `tools\launcher\src\Game.cpp`：DropEnt 增 looks；610 解析读 looks；`DrawSpriteFrame` 加 dw/dh 缩放参数；`kDropAnimFrames=6`；掉落渲染段移至实体/自身渲染之后 = `DnItem(looks + (nowDrop/120)%6)` + `DrawSpriteFrame(..., t->w*3, t->h*3)`（动画+3 倍放大，绘制于实体之上避免被精灵覆盖）。
6. `source_assets\176\MonDrop.txt` 追加「蝙蝠 金创药(小量) 魔法药(小量) 金币1」；概率手动调 `0.8`（**临时值**，重建 db 还原 0.01）。

**DnItems.wil 图库实证**：count=566；0-511 为物品图标区；块 390-409 为掉落旋转闪烁动画组（6 帧一轮，8×13 小帧 + 16×14 大帧交替）；looks 对应块（16/394/396/398/400/402）均有效；Items.wil count=571 为背包大图标库。

**引擎级缺陷修复（三连，均为 AI 自测发现）**：

1. **AI 追击建议从未被消费**（`WorldTick::Phase9Dispatch` 只调 `AiSystem::ThinkAll` 记录 actions 后丢弃）→ 主动怪（蝙蝠 race=81 ai_type=0 aggro_range=5）从不追击玩家、玩家也追不上怪、30s 无击杀。修复：Phase9Dispatch 追加 actions 消费循环——主线程逐条校验存活/不同格 → 单步位移 → `Move::Validate`（occupant=DropItem）→ `e->SetPos` + `AoiTree::OnEntityMove` + `CommandMessage + Protocol::EncodePacket + BroadcastMgr::AoIBroadcast(S_MOVE_WALK)` 广播。
2. **ChunkSleep 区块唤醒从未接线**（`OnPlayerEnter` 无调用者，Chunk 默认 state=Sleep，全图区块恒休眠 → `AiSystem::ThinkAll` L54 全 continue → 怪 AI 冻结；Telemetry `chunks(wake=0/sleep=0)` 为铁证）→ 修复：`PlayerRuntime::EnterWorld` 加 `ChunkSleep::OnPlayerEnter(ChunkIdOf(st.pos), eid)`；`LeaveWorld` 对称加 `OnPlayerLeave`。
3. **怪物死亡后死尸残留 AOI**（`ResolveHit` 只 `ChangeState(Dead)` 不 Despawn，死尸永久留在视野 → 客户端反复攻击尸体 → 服务端 `Combat::Attack` 返回 E_STATE=3「普攻拒绝」刷屏）→ 修复：`ResolveAttackHit` 怪物死亡分支（掉落/经验结算后）`AoiTree::Remove + EntityPool::Despawn`。

**自测证据（2026/10/9，连续两次稳定）**：

- `gfx_v12_polish2_drops16.png`：击杀=1 地面掉落=5（looks 400/396/16/402/394 全真实，坐标 (280,260) 与角色相邻）。
- `gfx_v12_polish2_drops17.png`：击杀=2 地面掉落=14（looks 400/396/16/402/398/394/0；放大图可见红/棕/蓝紫像素块 = DnItems 药瓶/材料真实图标 3 倍放大动画渲染）。
- 服务端日志：`怪物掉落 mon=100 命中=N 件`；普攻拒绝刷屏消失（死尸 Despawn 后）。

**后续精调项（非阻塞）**：其余怪素材位置微调、音效编号精确化（V1.2 精修-3）、怪物复活机制（当前死亡即 Despawn，杀空不刷新）、掉落概率 0.8 临时值定稿。

## 7b. V1.2 精修-3 音效精确化 + 怪物复活机制（2026/10/9 闭环）

### 音效编号精确化（客户端 `tools\launcher\src\Game.h/.cpp`）
- **Wav 库实证**（`C:\Users\Administrator\Downloads\传奇私服1.76客户端\Wav`，544 个）：171 纯数字 + 373 个 `XXXX-N` 怪音效。
- 语义来源：爱给网「传奇游戏 3246 首」作品集（60=大剑挥舞/54=斧头/51=木剑/72=铁棍攻击肉体/144=男性死亡）+ 传奇素材网帖（`XXXX-N` 六态：-0 发现/-1 待机/-2/-3 攻击/-4 受击/-5 死亡，编号=怪 Appr×10+200）。
- **编号定案**：`sfxAtkId=60`（攻击，实证确认）、`sfxHurtId=62`（受伤，波形高能打击实证，可调）、`sfxDieId=144`（玩家死亡，实证"男性死亡"）。
- **怪专属音效**：新增 `PlaySfxMon(v, appr, state)` → `Wav\{(appr*10+200)-state}.wav`；S_DAMAGE/S_DEATH 按实体 type 分流（怪→XXXX-4/-5，玩家→62/144）。蝙蝠 appr=81 → 1010-2/1010-4/1010-5 均存在（已核实）。

### 怪物复活机制（服务端 `src\world\RespawnMgr.h/.cpp` 新建 + 接入）
- 死亡分支（GameMsg.cpp）：怪死亡 → `AoiTree::Remove + EntityPool::Despawn + RespawnMgr::Schedule(defId, mapId, pos, md->respawn_ms)`（替代精修-2 的立即移除）。
- `RespawnMgr::Tick`（WorldTick Phase9 主线程调用）：到期槽 → `EntityPool::Spawn + AoiTree::Insert + AiSystem::Register` 原位复活。
- **时钟基准 bug 修复**：初版 Schedule 用 steady_clock、Tick 收逻辑时钟 nowMs → 永不复活；改为 Schedule/Tick 内部统一 steady_clock + `std::mutex`（网络线程 Schedule / 主线程 Tick 跨线程安全）。

### 自测证据（AI 离屏 Session，无 GUI）
- 击杀自测：`击杀=1 地面掉落=7`；服务端日志 `击杀确认 target=2969 dmg=4 type=1` → `怪物掉落 mon=100 命中=7 件`。
- 复活：08:48:04 击杀 → **08:48:34 服务端日志「怪物复活 defId=100 map=1 pos=(280,260)」（30s 整）**。
- 二次进图：`ent id=2968 type=1 x=280 y=260 appr=81`（复活蝙蝠可见）+ `击杀=2 地面掉落=12`。
- 截图：`C:\mir176\gfx_v12_polish3_kill2.png` / `gfx_v12_polish3_respawn.png`。

### 已知缺口（登记，不影响本轮验收）
- ~~复活的怪对当前在线玩家不广播 9304~~ **已闭环（见 §7c）**：此前"缺口"为测试工具缺陷（FakeClient 每 10s 段无条件退出 + 高攻击频率触发反作弊 L2 踢）造成的观察中断假象，非引擎广播缺陷。
- 音效为 PlaySound 异步播放，无法离屏截图自证；已按文件存在性 + 语义来源 + 代码路径验证，62/65 受伤编号可后续试听微调。

### §7c 在线视野增量广播闭环（2026-10-09 实证）

**P0 修复 1 — AoiTree::RemoveFrom 四叉树数据丢失**（`src\world\AoiTree.cpp`）
- 原"子节点全空→合并回叶子"仅查 `c->ids.empty()`，**split 子树（ids 空但孙节点有实体）被误判为空并 reset → 击杀后同象限多实体从树中消失**（实测在线玩家视野 `cur 12→2`，10 只实体丢失）。
- 修复：`std::function hasAny` 递归判空后才合并（新增 `#include <functional>`）。修复后击杀一只怪 `cur 12→11`，正确。**此修复必须保留。**

**P0 修复 2 — FakeClient 时长参数失效**（`tools\FakeClient.cpp`）
- 行为循环 `BotLoopOnce(...)==0 → leftMs=0; break` 无条件退出 → **durationSec 参数无效，任何"在线观察"只跑一个 10s 段就断线**，30s 复活永远等不到。
- 修复：`segRet==1` 才走重连；`segRet==0` 继续下一段直至 durationSec 耗尽。

**9304 增量广播端到端证据（双 bot 在线，服务端日志 `logs\tuppom2.log`）**
- `09:17:09.609 怪物复活 defId=100 pos=(0,0) aoi=1 nearby=6`
- `09:17:09.656 9304 enter sid=12 eid=8589937564` ← **复活怪 47ms 内增量广播给在线玩家**
- `09:17:10.503 击杀确认 sid=12 target=2972 dmg=4 type=1` ← **在线玩家收到广播后击杀复活怪**
- 后续 `09:17:12/13/40/42/44` 多轮复活→9304→击杀，**全链闭环**。

**反作弊干扰（验证过程中的关键认知）**
- FakeClient 行为循环 60ms/轮：attack=100 必触发「攻击加速（间隔<300ms）×5 → L2 踢」；walk≥20 触发「move-speed ×5 → L2 踢」。此前多轮"复活后无广播"全部因此误判。低频参数（walk=0 attack=8）可正常驻留。
- 9304 中出现超大 eid（4294967378/8589937560 等，约 uint32 高位），疑 EntityPool id 回绕/复用异常，**待后续核查（不阻塞）**。

**掉落概率定稿**：`drops.probability` 全量 0.01（32333 行/300 组怪）重启后实测 `怪物掉落 mon=100 命中=0 件`（击杀 2968/2973/2972 均 0 掉落），先前临时 0.8 已废弃。冒烟 `击杀=1 地面掉落=0`。

**本轮改动**：AoiTree.cpp（递归判空，保留）、FakeClient.cpp（段循环修复，保留）、BroadcastMgr.cpp（移除临时 9304/tick 调试日志，干净版已重建重启）。

### §7d 怪素材位置微调：WIL 帧锚点化渲染（2026-10-09 闭环）

**根因**：`Game.cpp::DrawSpriteFrame` 硬编码"水平居中 + 脚底对齐格底"（`dx=sx+(48-dw)/2; dy=sy+48-dh`），**完全忽略 WIL 帧头自带的 px/py 锚点**（`WilBitmap{int16 px, py}`）。该近似把**所有**精灵内容底压到格底（y=48），而传奇原生渲染语义是内容底 ≈ 格中心偏下（`py + h ≈ 30~45px`），导致怪整体视觉偏下、窄帧（鸡 24px）与宽帧（守卫 104px）水平落位不精确。

**修复（客户端 `tools\launcher\src\`）**：
- `SpriteView.h`：`SpriteTile` 增加 `px/py`（帧锚点，行序翻转不影响格坐标参考系）。
- `SpriteView.cpp GetCached`：填充 `t.px = bmp.px; t.py = bmp.py`。
- `Game.cpp`：新增 `DrawSpriteFrameAnchor(mem, t, sx, sy, ox=0, oy=0)`（`dx=sx+t->px+ox; dy=sy+t->py+oy`）；**怪绘制**（实体循环）与**攻击特效**（Magic 叠加帧）改用锚点渲染；`MonSpec` 扩展 `{lib, base, dx, dy}`——dx/dy 为每类怪额外补偿（默认 0，供后续按观察微调）。

**关键帧锚点实证（Data 目录 WIL 帧头）**：
| 素材 | 帧 | w×h | px | py | 内容底 py+h |
|---|---|---|---|---|---|
| Mon17 鸡 | 0 | 24×53 | +17 | -19 | 34px |
| Mon17 鹿 | 360 | 60×82 | +10 | -51 | 31px |
| Mon8 猫/蝙蝠 | 100 | 72×29 | -8 | -10 | 19px |
| Mon1 守卫 | 0 | 104×95 | +1 | -74 | 21px |
| Mon13 毒蜘蛛 | 0 | 88×83 | -19 | -39 | 44px |
| Mon12 蝎子 | 0 | 80×66 | -5 | -39 | 27px |
| Mon2 食人花 | 0 | 140×101 | -46 | -65 | 36px |
| Mon3 骷髅 | 0 | 80×76 | -1 | -59 | 17px |
| Mon10 洞蛆 | 0 | 72×63 | -11 | -27 | 36px |
| Mon5 沃玛 | 0 | 72×78 | +1 | -54 | 24px |
| Hum 玩家 | 40 | 56×71 | +14 | -47 | 24px |
| Magic 特效 | 0-7 | 44-84×66-82 | -17~3 | -50~-40 | 26-45px |

**自测证据（AI 离屏 Session，fake_0 出生 280,260 视野 12 实体）**：
- 战斗前含活怪帧（10 鸡分布在周围格 + 1 蝙蝠与玩家重叠格）：`gfx_pre.png` 4 倍放大可见**鸡上移贴格中心偏下、多只分布左右/上/下**——锚点渲染生效。
- 战斗帧 `gfx_v12_anchor2.png`：击杀 2（含蝙蝠 #2972）、伤害飘字正常、特效随怪锚点对齐。
- 干净版重建 `TuppoGameClient.exe` 冒烟 `击杀=2 地面掉落=0`，GFX SHOT OK。

**验证后清理**：main.cpp gfx-shot 分支两段临时调试代码（四方向走动 + 战斗前存图）已删除，客户端为干净版。

## 7e. V1.2 精修-4 玩法手感 + 怪死亡音对齐（2026-10-09 闭环）

**诉求**：客户端玩法与正版传奇差别大（移动/寻路/操作感），且打死怪的死亡配音不对。全库核查（源码 `tools\launcher\src\`）锁定 4 个根因，全部修复并编译通过。

### 根因 1 — 移动方向反了（服务端 Mir 标准 vs 客户端注释）
- 服务端 Move 方向表（`GameMsg.cpp` kDirDx/kDirDy）：0北 1东北 2东 3东南 4南 5西南 6西 7西北（`kDirDx={0,1,1,1,0,-1,-1,-1} kDirDy={-1,-1,0,1,1,1,0,-1}`）。
- 旧客户端注释错写"2西 6东"，A/D 横向相反。
- 修复：统一 `DirFromVec(dx,dy)` 八方向编码（dx>0→东系，dy>0→南系，主对角按 |dx|≥|dy| 取横），walk/自动战斗/headless 寻路全部走八方向。

### 根因 2 — 死亡音效被挥砍声顶掉
- 旧实现 `PlaySoundA` 单通道 SND_ASYNC：挥砍声一起，死亡嚎叫立即被打断；且怪死即删实体，9305 先到会误判玩家死亡音。
- 修复（客户端新增 `SfxMixer.h/.cpp`，waveOut 8 通道混音器）：
  - 解析 RIFF/PCM（Probe 校验位深）；`Play(name, priority)`，0=低（挥砍 60/受击 62/怪受击 -4），1=高（死亡嚎叫 -5 / 玩家死亡 144）；高优先级可抢占最老低优先级通道，全忙丢弃。
  - 怪死亡 → 尸体滞留 1s（半透明淡出）+ 高优先级死亡音；`S_TP_ENTITY_LEAVE` 登记 `gone` 兜底判别玩家/怪死亡音。
- `--sfx-test <wav目录>` 子命令：解析整个素材包，报告 8bit/16bit/解析失败数 + 怪死亡音（-5）覆盖清单。

### 根因 3 — 无鼠标操作
- 左键点怪 = 锁定攻击（自动走近贴身再砍 + 黄色选中框）；点空地 = 寻路走格；键盘 8 方向合成移动（A/D/W/S+方向键，kx/ky→DirFromVec），键盘输入即打断自动目标。

### 根因 4 — 素材/映射核实
- 游戏包 Wav 544 个全部 16bit PCM 可解析（`--sfx-test PASS`）；怪外观 = 服务端 9304 appr（race≈Appr），音 = appr*10+200-N（N：4 受击/5 死亡，如 鸡 51→710-5、多钩猫 81→1010-5）。
- 缺 7 个 -5 死亡音（1040/1050/1060/1070/1080/1090/1170，蝎子/食人花/骷髅系/沃玛系）——正版素材本身缺失，保留静默（与官方一致）。

### 编译与端到端验证（2026-10-09）
- CMakeLists：两个目标加 SfxMixer.cpp；TuppoLauncher 补 winmm。修复 windows.h min/max 宏冲突（std::max 换三元）。
- `cmake --build . --target TuppoGameClient TuppoLauncher --config Release` exit=0；`TuppoGameClient.exe` 496,640 B。
- `--sfx-test dist\gamepacks\mir\Wav` → `SFX PASS（总数=544 8bit=0 16bit=544 解析失败=0）`。
- 服务端（项目根 CWD，7100/7200）启动后冒烟：`击杀=3` SMOKE PASS（八方向寻怪，15s）。
- `--direct --gfx-shot`（真实 1.76 Data/Map）：地图/精灵全加载 OK，击杀 1 + 尸体滞留帧正常，GFX SHOT OK。

### 已登记（不阻塞）
- 骷髅系/沃玛死亡音正版素材缺失 → 保持官方静默；如后续要加，需自录/替换素材并在 `PlaySfxMon` 做缺省回退。

## 8. 运行日志

自测过程日志见 `build\classic-release\tools\launcher\Release\` 控制台输出；登录器运行上报走 `/report`（后台可见）。

### §8a V1.1/V1.2 全链路实测收尾（2026-10-09 闭环）

**一键回归脚本已固化**：`tools\launcher\scripts\v11_selftest.ps1`（UTF-8 BOM，PS5.1 中文正则必须）——`powershell -ExecutionPolicy Bypass -File v11_selftest.ps1`，6/6 PASS：
1. 服务端 TuppoM2 进程在
2. gfx-shot 冒烟（fake_0 登录→进图→战斗，重定向 stdout 到文件绕开 PS5.1 管道中文编码坑）
3. WIL 图库加载（Tiles/Objects/Hum/Mon1-13/Magic/DnItems）
4. 渲染 PNG 落盘
5. 战斗击杀 ≥1（0 时等 35s 复活窗口重试一次）
6. 服务端机制日志（怪物复活/怪物掉落/击杀确认，-Tail 2000 窗口 ≥3 条——绕开 27MB 大日志全量读取卡顿）

**本次实测修复（自测工具侧，非引擎/渲染缺陷）**：
- `main.cpp` gfx-shot 战斗循环方向映射反了（目标在 +x 应走 dir=6 东，原代码走 dir=2 西）——修复后击杀 0→2/3/5 稳定。**此修复必须保留。**

**全链路证据（重启后服务端 PID 44028，09:52-09:54）**：
- 客户端 `击杀=1/2/3 地面掉落=0`（0.01 定稿预期）；服务端日志 `击杀确认→怪物掉落 命中=0 件→怪物复活 defId=100 pos=(280,260)` 多轮闭环；9304 增量广播全天累计 133 条（§7c 已闭环）。

**OPEN 项登记（不阻塞，后续核查）**：
- 9304 畸形 eid（uint32 高位如 8589937564，EntityPool id 回绕复用疑点）。
- Wav 纯数字 100-145 号段语义未定、40-49 号段 Wav 库缺失。
- 09:48:25 服务端日志停写约 4 分钟（Telemetry tick 中断，重启后未复现；疑与 sid=33 注册失败处理/DB 锁竞争相关，单次未复现，登记观察）。
- 音效为 PlaySound 异步播放无法离屏截图自证（文件存在性+语义来源已验）。

---

## §7f V1.2 精修-5：原版传奇操作体系（删WASD/右键跑/F1-F8技能/数字键道具）+ 服务端反作弊误判修复

**背景（用户裁定）**：正版传奇 F1-F8=技能、主键盘数字键=快捷道具、鼠标右键=跑、左键=走、左键点怪=普通攻击；**原版传奇没有 WASD**。此前客户端用 WASD/方向键/空格移动，与本位不符。

### 客户端改动（tools/launcher/src）

- **Game.h**：GameView 增 `hasRunTarget/runTx/runTy/lastRunMs`、`lastSkillMs[8]/lastItemMs`；新增 `GameTryRun / GameCastSkill / GameUseQuickItem / GameEntityAtCell` 声明。
- **Game.cpp**：`kRunMs=180`（服务端跑速基准 150ms，留余量）、`kSkillMs=800`、`kItemMs=400`；
  - `GameTryRun`：发 C_RUN（dir U8 + seq U8）并维护 runTx/runTy 目标；
  - `GameEntityAtCell`：指定格存活怪查询；
  - `GameCastSkill`：悬停怪=目标实体，否则目标格地面（targetId=0）；施法转向 + Magic 特效 + 按技能 ID 冷却；
  - `GameUseQuickItem`：快捷位 N ↔ 背包格 N-1 顺位发送 C_USE_ITEM；
  - `GameAutoCombat` 增右键跑分支（持续朝目标跑，到达即停）；优先级 攻击锁定 > 右键跑 > 寻路走；
  - HUD 右下操作提示"左键走·右键跑·点怪攻击·F1-F8技能·1-8道具"。
- **main.cpp GameWndProc**：`WM_RBUTTONDOWN`=跑（打断攻击锁定/寻路）；`WM_KEYDOWN` 增 F1–F8→GameCastSkill（光标所在格取怪，无怪则地面）、'1'–'8'→GameUseQuickItem；`FrameTick` 删除 WASD/方向键/空格移动，仅 GameAutoCombat + GameAutoPickup。`main_webview2.bak.cpp` 为备份仍含旧 WASD（勿动）。

### 服务端修复（自测发现的真实缺陷，src/net/GameMsg.cpp + src/player/PlayerRuntime.h）

原版操作 headless 自测（临时 --input-test，验证后已删）首轮即暴露两个误判：

1. **正常移动失败误计反作弊**：`HandleMoveCommon` 对所有 `Move::Validate` 失败都 `AntiCheat::Strike`，玩家点向墙壁/地形阻挡/被怪堵路 5 次即被 L2 踢下线。修正：仅 `E_TOO_FAST`（超速）与 `cheatMoveDetected`（穿人）计数；撞墙越界 E_PARAM、地形/普通碰撞 E_BLOCKED 只回 S_MOVE_FAIL 不计数。
2. **跑速=走速导致跑动持续超速**：服务端 `moveSpeedMs=300ms`（characters.move_speed），客户端跑节流 180ms 快于 300ms → 每两次跑中一次被判超速，累计 5 次踢下线。修正：跑动校验间隔=走速/`combat.run_speed_divisor`（默认 2，活参数）=150ms；客户端 180ms > 150ms 留 30ms 余量。
3. **超速计次加窗口防误判**：走路↔跑快速切换会单次触发 E_TOO_FAST。改为 PlayerState 维护 `tooFastCount/lastTooFastMs`，2s 窗口内连续 3 次超速才计外挂特征（真加速器每秒数十次必命中）。

### 验证证据（2026-10-09，本地测试服 127.0.0.1:7100/7200）

- 编译：客户端+登录器 Release 零警告；TuppoGameClient.exe 498,688 B（11:44:22）。
- `--smoke` 回归：击杀=6，SMOKE PASS（修正后 bot 移动效率更高）。
- `--input-test` headless（已删分支，证据留存于输入自测输出）：
  `登录成功 charId=38 → 视野实体=4 → [RUN] 跑前 x=0 跑后 x=11（东移=11）→ [MAGIC] 刺杀103 已发 连接=1 → [MAGIC] 火球201 已发 连接=1（未实现技能被服务端丢包不计数）→ [ITEM] 快捷道具0 已发 连接=1 → INPUT TEST PASS`。
- 服务端日志：修正后跑动全程无 move-speed 误踢（此前 sid=4/8 均在 5 次误计数后 L2 踢）。

**OPEN（后续增强，非阻塞）**：F1-F8 技能与数字键快捷栏的**配置 UI**（拖放设置技能/道具位）未做，当前为硬编码顺位（F1-F8=技能 ID 1-8；数字 N ↔ 背包格 N-1）；服务端技能仅 Thrust 有实际效果，其余 C_MAGIC 静默丢包（不计数不踢人，已实测）；快捷栏需背包明细推送（S_ 背包全量/更新）后才有真实道具数据。
