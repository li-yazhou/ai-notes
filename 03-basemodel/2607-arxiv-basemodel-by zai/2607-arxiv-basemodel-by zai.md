---
type: digest
month: 2026-07
title: "arXiv 2026.07 LLM 基础模型月度论文摘要（按厂商）"
updated: 2026-08-14
status: active
count: 67
tags:
  - digest/llms
  - digest/arxiv
  - month/2026-07
  - paper/foundation-model
  - paper/release
---

# arXiv 2026.07 LLM 基础模型月度摘要（按厂商分类）

> 采集窗口：arXiv `submittedDate` 2026-07-01 ~ 2026-07-31（少量 2608.xxxxx 为 7 月底提交、8 月初公告）
> 采集方式：arXiv API 按日期 + 关键词（pretrain / post-train / MoE / long-context / quantization / technical report 等 12 组）三轮召回 ~935 篇候选，交叉 Hugging Face 2026.07 Daily Papers 602 篇（表中 `HF↑N` 为当月最高点赞数），人工筛选 67 篇
> 分类维度：**模型厂商**（官方发布 → 生态研究 → 通用方法）；agent 应用层论文见 [[02-agent/2607-arxiv-ai agent llm papers-by zai]]
> 厂商归属依据论文标题/摘要/作者团队署名推断，arXiv 页不含机构字段，个别标注"疑似"；一句话要点均依据摘要撰写，未读全文的结论请以原文为准

---

## 〇、本月趋势

1. **开源 frontier 竞争白热化：Kimi K3 对标闭源第一梯队。** [Kimi K3](https://arxiv.org/abs/2607.24653)（2.8T MoE / 104B 激活 / 1M 上下文 / 原生视觉，权重全开）是本月最重要发布，HF 单月 491 赞；同月 [Gemma 4](https://arxiv.org/abs/2607.02770)（2.3B–31B，dense + MoE）和 [Solar Open 2](https://arxiv.org/abs/2607.20062)（250B-A15B）把开源阵线的梯度从 3B 拉到万亿级。
2. **MoE 已是中型以上模型的默认形态。** 本月新发布里 Kimi K3（16/896 专家）、Solar Open 2（A15B）、DiffusionGemma（3.8B/25.2B）、Soofi S（A3B）、Mach-Mind-4-Flash（A3B）、Audex（A3B）、Puzzle-75B（A9B）清一色 MoE；配套研究（专家路由、MoE 投机解码、PD 分离路由）同步井喷。
3. **扩散语言模型（dLLM）从概念走向工程。** [DiffusionGemma](https://arxiv.org/abs/2608.00146)（256 token 并行精炼，~20 token/步）与 [Nemotron-Labs-Diffusion](https://arxiv.org/abs/2607.05722)（AR+扩散+自投机三模态）两篇技术报告，加上 dOPSD 等后训练方法，标志着"非 AR 生成"进入可部署区间。
4. **1M 上下文成为旗舰标配，2M+ RL 出现。** Kimi K3、Solar Open 2 原生 1M；[LongStraw](https://arxiv.org/abs/2607.14952) 把长上下文 RL 推到 2M token；Puzzle-75B 把单 H100 上 1M-token 并发从 1 路提到 8 路。注意力侧 HiLS（DeepSeek 系）用分层稀疏逼近全注意力。
5. **混合线性注意力进入产品化。** Solar Open 2（每 3 层线性注意力夹 1 层 softmax、无位置编码）与 Soofi S（Mamba-Transformer 混合）把线性 RNN 复兴落进开放权重；第三方研究（Linear Attention Architectures、Chimera）开始把 Kimi Delta Attention 当作标准基线比较。
6. **音频多模态是本月最密集的新战场。** 阿里连发 Qwen-Music / Qwen-Audio-VAE / Qwen-Audio-3.0-Gen 三篇 + WanSong；Gemma 4 全尺寸带音频编码器；NVIDIA Audex 统一音频-文本；Sber GigaChat Audio 做到 120 分钟时间戳级理解。
7. **后训练研究聚焦"熵、蒸馏、低精度"三件事。** GEPO（分组熵控制）、On-Policy Delta Distillation / Proxy OPD / Flux-OPD（on-policy 蒸馏家族）、HiFloat4（首个端到端 FP4 RL）分别在稳定性、信号密度、成本上压榨 RL 后训练。
8. **主权与垂域模型持续分化。** 德国 Soofi S（主权 MoE）、俄罗斯 GigaChat Audio、医疗 Cura 1T、推荐 RecGPT-V3（淘宝）、Bilibili Index-1.9B、小米机器人 VLA——"自己的模型"成为组织默认选项。
9. **中国算力生态上桌。** [SLAI T-Rex](https://arxiv.org/abs/2607.20145) 在华为昇腾 SuperPOD 上对 DeepSeek-V4 家族做全参后训练，HiFA4 在昇腾 NPU 上跑 FP4 推理——非 CUDA 栈的 LLM 训练/推理闭环开始有公开论文。

---

## 一、头部厂商：官方发布与技术报告

### 1. Moonshot AI（月之暗面）

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) | 07-27 | **2.8T MoE / 104B 激活 / 1M 上下文 / 原生视觉**；Kimi Delta Attention + Attention Residuals + Stable LatentMoE（16/896 专家），相对 K2 整体缩放效率 ~2.5×，权重全开（HF↑491） | `model/frontier` `model/moe` |

> 生态注记：Kimi Delta Attention 本月被多篇第三方研究作为标准基线（[Linear Attention Architectures](https://arxiv.org/abs/2607.07953)、[Chimera](https://arxiv.org/abs/2607.28611)）；基于 Kimi-K2.6 的医疗专模型 Cura 1T 见垂域节。

### 2. Google（DeepMind / Gemma 团队）

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Gemma 4 Technical Report](https://arxiv.org/abs/2607.02770) | 07-02 | 开放权重、原生多模态系列：dense + MoE 双形态、2.3B–31B；全尺寸配更强视觉/音频编码器，12B 版采用**无编码器统一架构**直接摄取原始音频与图像（HF↑76） | `model/release` `model/multimodal` |
| [DiffusionGemma Technical Report](https://arxiv.org/abs/2608.00146) | 07-31 | 实验性开放权重扩散 LM：由 Gemma 4 MoE（3.8B 激活/25.2B 总参）微调而来，并行精炼 256-token 块；两阶段（双向去噪 SFT → RL+采样器蒸馏）仅用原 AR 预算 <10% token，~20 token/前向，速度-能力新 Pareto 前沿 | `model/diffusion` `model/release` |

### 3. 阿里巴巴 / Qwen 系（本月产出最密的厂商）

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Qwen-Music Technical Report](https://arxiv.org/abs/2607.11699) | 07-13 | 高保真带人声完整歌曲生成：文生音乐 + 翻唱双任务，支持歌词/风格/演唱属性控制（HF↑30） | `model/audio` `model/release` |
| [Qwen-Audio-VAE Technical Report](https://arxiv.org/abs/2607.11738) | 07-13 | 低码率、快编码的连续音频自编码器套件：因果编解码 + 高保真重建，为大规模 text-to-audio 训练供紧凑隐空间 | `model/audio` `method/vae` |
| [Qwen-Audio-3.0-Gen-Preview Technical Report](https://arxiv.org/abs/2607.27011) | 07-29 | 统一**非自回归**音频生成：DiT + 共享 VAE 直接输出完整混合波形，把环境音/多角色/长时场景组织进一段生成 | `model/audio` `method/non-ar` |
| [Qwen-UI-Agent Technical Report](https://arxiv.org/abs/2607.28227) | 07-30 | 面向真实设备的基础 GUI Agent 模型：跨平台工作流、GUI+CLI 混合执行、长程任务、主动服务与自主改进（HF↑302） | `model/gui-agent` `model/release` |
| [WanSong v1.0 Technical Report](https://arxiv.org/abs/2607.14749) | 07-16 | DAMO 团队（周靖人等）商用级长篇幅歌曲生成：不走 AR/级联管线，一条路径兼顾效率、长音频高保真与可控性（HF↑17） | `model/audio` `model/release` |
| [OvisOCR2 Technical Report](https://arxiv.org/abs/2607.13639) | 07-15 | 0.8B 端到端文档解析模型：页面图直出自然阅读序 Markdown（文本/公式/表格/图表），真值+同源 HTML 合成双数据引擎（HF↑56） | `model/document` `model/small` |
| [RecGPT-V3 Technical Report](https://arxiv.org/abs/2607.15591) | 07-17 | 淘宝生产部署的推荐 LLM 第三代：把"推理式推荐"从多 agent 编排收敛回单模型，解决规模化成本问题（HF↑30） | `model/vertical` `model/recommend` |

### 4. NVIDIA（Nemotron-Labs 系列）

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Nemotron-Labs-3-Puzzle-75B-A9B](https://arxiv.org/abs/2607.04371) | 07-05 | Nemotron-3-Super 的压缩变体：多阶段压缩管线，8×B200 上交互吞吐 ~2×，单 H100 上 1M-token 并发 1→8 路 | `model/moe` `method/compression` |
| [Nemotron-Labs-Diffusion](https://arxiv.org/abs/2607.05722) | 07-07 | 三模态语言模型：AR / 扩散 / 自投机解码统一在单一架构，联合 AR-扩散目标训练；扩散起草+AR 校验优于 MTP | `model/diffusion` `method/hybrid-decode` |
| [Unified Audio Intelligence Without Regressing on Text](https://arxiv.org/abs/2607.05196) | 07-06 | Audex-30B-A3B：基于 Nemotron-Cascade-2 文本 MoE 的统一音频-文本模型，音频投影进文本嵌入空间，加音频不掉文本智力（HF↑23） | `model/audio` `model/multimodal` |

### 5. DeepSeek（本月无官方技术报告，但研究产出与生态活跃）

| 论文                                                                           | 日期    | 一句话要点                                                                                                     | 标签                                  |
| ---------------------------------------------------------------------------- | ----- | --------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| [Hierarchical Sparse Attention Done Right](https://arxiv.org/abs/2607.02980) | 07-03 | DeepSeek 研究团队（作者含 Yushi Bai、Tian Liang 等）；HiLS：chunk 选择端到端随 LM loss 学习，检索分并入前向计算，性能逼近甚至超过全注意力且外推更强（HF↑84） | `method/attention` `model/deepseek` |

> 生态注记：DeepSeek-V4 家族已开放权重并成为第三方后训练目标（SLAI T-Rex，见下）；MLA / NSA 机制本月有多篇第三方分析（见第三节）。

### 6. Microsoft

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [VibeVoice-ASR-BitNet Technical Report](https://arxiv.org/abs/2607.21075) | 07-23 | 边缘 CPU 实时 ASR：VAE 声学塔 INT8 + 自回归 LM BitNet 三值权重（I2_S）异构量化 + 蒸馏恢复精度 | `model/audio` `method/quantization` |

### 7. Upstage（韩国）

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Solar Open 2 Technical Report](https://arxiv.org/abs/2607.20062) | 07-22 | 250B-A15B 长程 agentic MoE：混合注意力栈（每 3 层线性注意力夹 1 层 softmax、无位置编码、门控 delta 规则扩展到负特征值）撑起 **1M token** 窗口 | `model/frontier` `method/linear-attention` |

### 8. Meta / OpenAI / Anthropic / xAI / Mistral / Cohere

> 本月召回范围内**无**上述厂商的 LLM 基础模型技术报告或官方方法论文；其模型仅作为第三方研究的评测基线出现（GPT-5.x / Claude / Llama / Gemini 见第三节与通用研究节）。Z.ai/GLM、ByteDance、腾讯混元、百度、StepFun、MiniMax 本月同样无基础模型 arXiv 发布。

---

## 二、中国厂商与新玩家

| 厂商 | 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|---|
| Bilibili | [Index SLM Technical Report](https://arxiv.org/abs/2607.09885) | 07-10 | Index-1.9B 系列：1.9B 非嵌入参数、2.8T 中英 token 预训练；Base/Pure/Chat/角色扮演四件套，Pure 为严格过滤指令数据的对照变体 | `model/small` `model/release` |
| Xiaomi | [Xiaomi-Robotics-1](https://arxiv.org/abs/2607.15330) | 07-16 | VLA 基础模型：10 万+ 小时真实轨迹，两阶段（大规模预训练→轻样本适配），未知环境开箱即用移动操作（HF↑73） | `model/vla` `model/embodied` |
| Nanbeige Lab | [Nanbeige4.2-3B](https://arxiv.org/abs/2607.22083) | 07-24 | 3B 紧凑 agentic 模型：Looped Transformer 复用层堆叠扩容量不加参数，28T token 从头预训练；code/office/tool-agent 全线超同量级 | `model/small` `model/agentic` |
| actAVA AI | [Cura 1T](https://arxiv.org/abs/2607.15314) | 07-15 | 基于 Kimi-K2.6 开放权重的医疗专模型：human-gated 递归自改进（RSI）循环逐轮规划-训练-评测-人审，覆盖问诊/多模态推理/EHR 工具 | `model/vertical` `method/rsi` |
| SLAI | [T-Rex](https://arxiv.org/abs/2607.20145) | 07-22 | 在**华为昇腾 SuperPOD** 上对 DeepSeek-V4 家族做全参后训练的系统实践：层级式优化（并行策略、计算-通信编排、算子），万亿 MoE 的非 CUDA 栈端到端样板（HF↑74） | `model/deepseek` `system/npu` |
| Mach Mind | [Mach-Mind-4-Flash TR](https://arxiv.org/abs/2607.09375) | 07-10 | 35B MoE（A3B）agentic 模型：不动预训练算力、纯后训练（可扩展 agentic 交互环境 + 大规模 RL）追平 100B 级 | `model/moe` `model/agentic` |
| KAT 团队 | [KAT-Coder-V2.5 TR](https://arxiv.org/abs/2607.05471) | 07-06 | agentic coding 模型：AutoBuilder 把多语言仓库重建为沙箱 + 过程过滤 + 多专家 on-policy 蒸馏；瓶颈在可复现环境而非模型规模 | `model/coding` `method/distillation` |

### 其他机构 / 未具名团队

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Athena-Brain Technical Report](https://arxiv.org/abs/2607.18985) | 07-21 | 端侧"机器人大脑"：压缩 LLM 保留通用智能 + 高层具身交互，兼顾通用性与效率 | `model/embodied` `model/edge` |
| [DeepResearch Agent System](https://arxiv.org/abs/2607.27562) | 07-30 | 30B/3B 激活稀疏检索系统：多步推理 + 自主研究，HLE 87.3%（全开源） | `model/moe` `agent/deep-research` |
| [S1-Omni](https://arxiv.org/abs/2607.15686) | 07-17 | 统一多模态科学推理模型：理解/预测/生成一体，联合建模异构科学数据（HF↑16） | `model/multimodal` `model/vertical` |
| [Infinity-Parser2 TR](https://arxiv.org/abs/2607.07836) | 07-08 | 端到端文档解析多模态大模型：可控渲染+迭代精炼的合成引擎 + 多任务 RL，开源解析语料 | `model/document` `method/synthesis` |
| [Prompt Generation TR](https://arxiv.org/abs/2607.11326) | 07-13 | 工业搜索/推荐/广告的生成式检索系统：用 LLM 生成式建模特征工程，替代重迭代的人工特征管线 | `model/vertical` `method/gen-retrieval` |

---

## 三、海外其他厂商

| 厂商 | 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|---|
| Sber（俄罗斯） | [GigaChat Audio](https://arxiv.org/abs/2607.10387) | 07-11 | 时间感知音频 LLM：周期时间标记与连续音频 token 交错，级联合成监督，120 分钟录音上带显式时间戳问答（HF↑37） | `model/audio` `model/vertical` |
| Soofi 联盟（德国主权） | [Soofi S 30B-A3B](https://arxiv.org/abs/2607.09424) | 07-10 | 德英主权开源 MoE：Mamba-Transformer 混合，A3B 激活、推理缓存近常数，长上下文高并发吞吐优势（HF↑15） | `model/sovereign` `method/linear-attention` |
| Pangram Labs | [Pangram 4 TR](https://arxiv.org/abs/2607.27183) | 07-29 | AI 文本检测模型：AUROC 0.9916、误报率 0.0041%，OOD 泛化与抗对抗鲁棒性显著提升 | `model/detection` `model/vertical` |
| Harrison.ai | [Harrison.Rad 1.5 TR](https://arxiv.org/abs/2607.05880) | 07-07 | 放射科基础模型：可直接从影像起草结构化放射报告 | `model/vertical` `model/medical` |
| NAVER AI Lab | [On-Policy Delta Distillation](https://arxiv.org/abs/2607.15161) | 07-16 | 系统研究 on-policy 蒸馏的设计空间：证明跟踪 teacher-student 差分（delta）而非绝对分布更稳，给出统一理论框架（HF↑38） | `method/distillation` |

---

## 四、围绕厂商模型的第三方研究（精选）

> 研究对象为具体厂商模型家族（MLA / NSA / MoE / MTP / Qwen 权重等），非厂商官方出品。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Through the Bottleneck](https://arxiv.org/abs/2607.23054) | 07-25 | 首个对 DeepSeek **MLA** 低秩瓶颈的机制分析：cKV 压缩 81% KV 缓存的同时把内容与位置信息分离，重塑内部表征几何 | `study/interp` `model/deepseek` |
| [COBS: Cumulant Order Block Sparse Attention](https://arxiv.org/abs/2607.09052) | 07-10 | 分析 DeepSeek **NSA** 为何未被主流开放权重模型采用，提出累积量阶块稀疏注意力改进 KV 读瓶颈 | `method/attention` `model/deepseek` |
| [Less Experts, Faster Decoding](https://arxiv.org/abs/2607.12696) | 07-14 | MoE 感知的投机解码：draft 选择考虑专家激活成本，按"少激活专家"选高接受率 token | `method/spec-decode` `model/moe` |
| [Windowed-MTP](https://arxiv.org/abs/2607.21535) | 07-23 | 揭示百万 token 上下文下内置 MTP/NEXTN 草稿头的"全上下文 draft-KV 税"，窗口化草稿将其移除 | `method/spec-decode` `method/long-context` |
| [Beyond KV Reconstruction](https://arxiv.org/abs/2607.27269) | 07-29 | MLA 架构下投机解码 draft 模型的"功能重建"训练：对齐目标模型行为而非 KV 逐位重建 | `method/spec-decode` `model/deepseek` |
| [Jet-Long](https://arxiv.org/abs/2607.07740) | 07-08 | 动态双焦 RoPE：零训练把开放权重 checkpoint 上下文外推一个数量级，适配 RAG/仓库级编码场景（HF↑24） | `method/long-context` `method/rope` |
| [Quantize the Target, Quantize the Drafter](https://arxiv.org/abs/2607.04244) | 07-05 | Efficient Qwen 竞赛报告：Qwen3.5-4B 在 A10G 上量化目标模型 + 投机解码 + 量化感知蒸馏恢复精度 | `method/quantization` `model/qwen` |
| [Linear Attention Architectures](https://arxiv.org/abs/2607.07953) | 07-08 | DeltaNet / Gated DeltaNet / **Kimi Delta Attention** / GDN-2 四种线性注意力统一形式化对比：机制、权衡与跨层路由（HF↑16） | `study/survey` `method/linear-attention` |
| [Chimera](https://arxiv.org/abs/2607.28611) | 07-30 | 混合视觉扩散骨干：结合 Kimi Delta Attention 与门控卷积、无位置嵌入的 Chinchilla 式缩放配方（HF↑22） | `method/architecture` `model/diffusion` |

---

## 五、通用基础模型研究（学术 / 多机构）

### 1. 架构与注意力

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Program-as-Weights](https://arxiv.org/abs/2607.02512) | 07-02 | "模糊函数编程"范式：把自然语言函数编译进模型权重，兼顾 LLM 能力与局部性/可复现/低成本（HF↑309） | `method/paradigm` |
| [Convolution for Large Language Models](https://arxiv.org/abs/2607.18413) | 07-20 | 系统消融：轻量深度卷积注入局部归纳偏置，不显著增参即可补足自注意力的局部性缺失 | `method/architecture` |
| [EntropyMoE](https://arxiv.org/abs/2608.06398) | 07-31 | 无分词器 byte-patch LLM 的熵感知稀疏专家路由：按 patch 信息量自适应分配 FFN 容量 | `method/moe` `method/tokenizer-free` |
| [Understanding Is Done Early](https://arxiv.org/abs/2607.28263) | 07-30 | 机制发现：LLM 理解集中在浅层、生成集中在深层——"深度分工"可用于免额外训练的能力解绑 | `study/interp` |

### 2. 长上下文

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [LongStraw](https://arxiv.org/abs/2607.14952) | 07-16 | 固定 GPU 预算下 2M+ token 长上下文 RL 后训练：约束是状态/梯度存活期而非注意力算力，重建 GRPO 内存布局（HF↑212） | `method/rl` `method/long-context` |
| [KVpop](https://arxiv.org/abs/2607.05061) | 07-06 | 学习式固定预算 KV 逐出：预测未来 token 效用做在线剪枝，优于静态启发式（HF↑24） | `method/kv-cache` |
| [SeDeM](https://arxiv.org/abs/2608.00311) | 07-31 | 选择性解压隐状态记忆：软压缩上下文按需恢复，兼顾长上下文成本与证据可靠性 | `method/long-context` |
| [Self-Guided Test-Time Training](https://arxiv.org/abs/2607.09415) | 07-10 | 测试时训练利用长输入自监督：无需外部标注即可让模型学会定位并使用相关证据（HF↑19） | `method/long-context` `method/ttt` |
| [RIS-Kernel](https://arxiv.org/abs/2607.21927) | 07-24 | 模型无关的稀疏注意力推理引擎：不改权重把 O(N²) 注意力降到长文档分析可用区间 | `method/long-context` `system/serving` |
| [Logit-Contribution Scoring](https://arxiv.org/abs/2607.01002) | 07-01 | 识别"非字面"检索头：长上下文答案多为语义综合而非复制粘贴，现有检测器按构造漏掉这类头（HF↑19） | `study/interp` `method/long-context` |

### 3. 后训练与 RL

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [GEPO](https://arxiv.org/abs/2607.16850) | 07-18 | 分组熵控制策略优化：异质任务混合下全局/词元级熵调节都不足，按组控熵平衡探索-利用（HF↑29） | `method/rl` |
| [Understanding Reasoning from Pretraining to Post-Training](https://arxiv.org/abs/2607.16097) | 07-17 | 打通预训练与 RL 视角：预训练选择（规模/数据）如何决定 RL 回报，RL 又对模型做了什么（HF↑29） | `study/analysis` `method/rl` |
| [Is One Layer Enough?](https://arxiv.org/abs/2607.01232) | 07-01 | RL 增益在层间高度不均匀：训练单个 Transformer 层即可匹敌全参 RL，挑战"均匀更新"默认假设（HF↑8） | `method/rl` `study/interp` |
| [Spectral Rewiring](https://arxiv.org/abs/2607.03065) | 07-03 | 谱重连：低秩子空间更新替代稠密全参，缓解 RL 的推理早饱和与多域能力互扰，天然利于模型合并（HF↑25） | `method/rl` `method/merging` |
| [HiFloat4](https://arxiv.org/abs/2607.26515) | 07-29 | 首个端到端 FP4 RL 后训练：rollout 与训练前向/反向全程 4-bit；发现主要退化源是 rollout 激活量化而非训练侧误差 | `method/rl` `method/quantization` |
| [dOPSD](https://arxiv.org/abs/2607.04428) | 07-05 | 扩散语言模型的 on-policy 自蒸馏：解 SFT 曝光偏置与 RL 稀疏奖励两难（HF↑19） | `method/distillation` `model/diffusion` |

### 4. 蒸馏

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Flux-OPD](https://arxiv.org/abs/2607.28022) | 07-30 | 开放域无验证奖励场景的 on-policy 蒸馏：用随学生能力演化的上下文传递偏好（HF↑44） | `method/distillation` |
| [Proxy OPD](https://arxiv.org/abs/2607.11505) | 07-13 | 可迁移相对代理更新：匹配专家相对分布而非绝对分布，复用探索期高奖励行为（HF↑19） | `method/distillation` |

### 5. 量化与推理效率

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [DSpark](https://arxiv.org/abs/2607.05147) | 07-06 | 置信度调度的半自回归投机解码：并行起草 + 按接受衰减调度验证块，兼得速度与接受率（HF↑43） | `method/spec-decode` |
| [KronQ](https://arxiv.org/abs/2607.07964) | 07-08 | Kronecker 分解 Hessian 的二阶 PTQ：修正 GPTQ 隐含的"输出通道等贡献"假设（HF↑33） | `method/quantization` |
| [ELDR](https://arxiv.org/abs/2607.00466) | 07-01 | PD 分离 MoE 服务的专家局部性路由：等载解码 worker 延迟仍不同，按激活专家聚合路由（HF↑32） | `system/serving` `model/moe` |
| [Silent Failures in Quantized LLM Reasoning](https://arxiv.org/abs/2607.09999) | 07-10 | 量化推理的"空洛收敛"失败分类学：分数正常但推理链悄悄断裂 | `study/quantization` |
| [GaugeQuant](https://arxiv.org/abs/2607.20757) | 07-22 | 利用 LLM 权重对称性的在线量化最优基学习 | `method/quantization` |

### 6. 新范式与基础模型延伸

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Metis: Memory Foundation Model](https://arxiv.org/abs/2607.26760) | 07-29 | 首个"记忆基础模型"：把持久演化记忆态与记忆过程内化进 backbone，前向即更新（HF↑271） | `method/memory-foundation` |
| [Mage-VL](https://arxiv.org/abs/2607.24904) | 07-27 | 编解码器原生流式多模态基础模型：自研 Mage-ViT 分词器替代 patch，实时流感知补 VLM 短板（HF↑37） | `model/multimodal` `method/streaming` |

---

## 六、本月必读（Top 10）

1. **[Kimi K3](https://arxiv.org/abs/2607.24653)** — 月度最重要开源 frontier：2.8T MoE / 1M 上下文，观察开源-闭源差距的基准参照。
2. **[Gemma 4 Technical Report](https://arxiv.org/abs/2607.02770)** — Google 开放权重主线更新：dense+MoE 全谱系、无编码器统一多模态架构。
3. **[DiffusionGemma Technical Report](https://arxiv.org/abs/2608.00146)** — AR 模型改造为扩散 LM 的完整工程路径（<10% token 预算），dLLM 落地里程碑。
4. **[Solar Open 2](https://arxiv.org/abs/2607.20062)** — 混合线性注意力 + 1M 窗口的产品级验证，线性 RNN 复兴的代表作。
5. **[HiLS Attention](https://arxiv.org/abs/2607.02980)** — DeepSeek 系的稀疏注意力新作：chunk 选择端到端可学，逼近全注意力。
6. **[LongStraw](https://arxiv.org/abs/2607.14952)** — 2M token 长上下文 RL 的系统级解法，本月社区最高讨论度方法论文之一。
7. **[Nemotron-Labs-Diffusion](https://arxiv.org/abs/2607.05722)** — AR/扩散/自投机三模态统一，NVIDIA 对解码范式的押注。
8. **[Program-as-Weights](https://arxiv.org/abs/2607.02512)** — 把 NL 函数编译进权重的编程范式，HF↑309 的思想实验级论文。
9. **[Metis](https://arxiv.org/abs/2607.26760)** — 记忆基础模型开山之作，HF↑271，agent 记忆与基础模型的合流点。
10. **[SLAI T-Rex](https://arxiv.org/abs/2607.20145)** — 昇腾 SuperPOD 上万亿 MoE 全参后训练首份公开论文，非 CUDA 生态的标志性节点。

---

## 附：方法与采集说明

- **召回**：arXiv API `submittedDate:[202607010000 TO 202607312359]` × 12 组关键词（posttrain / pretrain / arch / efficiency / reasoning / reports / vendor_labs / vendor_models 等，每组按相关度或日期取前 180–300），三轮共去重 ~935 篇候选；另用 `ti:"technical report"` 全量核对 7 月模型发布（41 篇）。
- **交叉信号**：Hugging Face Daily Papers API 按 `date=2026-07-DD` 逐日抓取 602 篇，`HF↑N` = 该论文在 7 月内被 HF Daily Papers 收录时的最高 upvote 数。
- **厂商归属**：arXiv API 不返回机构署名，归属依据 ①标题/摘要中的模型家族与团队名（"Qwen Team"、"Gemma Team"、"Xiaomi Robotics Team"）②作者名单与已知研究者重合度（如 WanSong 含周靖人→阿里 DAMO；HiLS 含 Yushi Bai/Tian Liang→DeepSeek 系）③摘要自述（"developed at Bilibili"、"on Taobao"）。无法确认机构的归入"其他/未具名"，不做强行归属。
- **收录口径**：LLM 基础模型 = 模型发布/技术报告、预训练、后训练（SFT/RLHF/DPO/GRPO/蒸馏）、架构（MoE/注意力/位置编码）、长上下文、量化与推理效率；纯 agent 应用/评测/benchmark 见 `02-agent/` 月报，本文仅保留与基础模型强相关条目。
- **局限**：一句话要点仅依据摘要；未读全文，数字与结论以原文为准。7 月底提交、8 月初公告的论文 ID 为 `2608.xxxxx`，仍按 7 月口径收录。Meta/OpenAI/Anthropic/xAI/Mistral/GLM/ByteDance 等本月"无发布"仅指本召回范围（arXiv 官方技术报告），不排除其他渠道发布。
