---
type: overview
title: "DeepSeek 基础模型与开源工具总览（时间线）"
created: 2026-08-14
updated: 2026-08-14
status: active
tags:
  - vendor/deepseek
  - paper/foundation-model
  - paper/release
  - tool/open-source
---

# DeepSeek 基础模型与开源工具总览（时间线）

> 范围：DeepSeek-AI 官方发布的**基础模型**（LLM / Coder / Math / Prover / VL / Janus / OCR / R 系 / V 系）与**开源基础设施工具**（"开源周"六件套等），按发布时间排序
> 信息来源：arXiv 官方页面、[DeepSeek API 更新日志](https://api-docs.deepseek.com/updates/)、[deepseek-ai GitHub](https://github.com/deepseek-ai)；标 ✱ 的条目为无论文发布（模型卡 / API 公告）
> 关联：[[2607-arxiv-llms]]（月度厂商 digest，DeepSeek 新论文按月收录）

---

## 〇、一页时间线

| 时间            | 发布物                               | 论文 / 来源                                                                       | 一句话要点                                                                       |
| ------------- | --------------------------------- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| 2023-11       | DeepSeek LLM 7B/67B               | [arXiv:2401.02954](https://arxiv.org/abs/2401.02954)                          | 首代通用模型，2T token"长期主义"预训练，67B 对标并超越 Llama2-70B                               |
| 2023-11       | DeepSeek Coder 1.3B/6.7B/33B      | [arXiv:2401.14196](https://arxiv.org/abs/2401.14196)                          | 87 种语言代码预训练 + 仓库级预训练 + FIM，最早一批国产开源代码模型                                     |
| 2024-01       | DeepSeekMoE 16B                   | [arXiv:2401.06066](https://arxiv.org/abs/2401.06066)                          | 细粒度专家切分 + 共享专家隔离，约 40% 计算量对齐同尺寸 dense                                       |
| 2024-02       | DeepSeekMath 7B / 7B-RL           | [arXiv:2402.03300](https://arxiv.org/abs/2402.03300)                          | 120B token 数学语料；提出 **GRPO**，R1 强化学习算法的前身                                    |
| 2024-03       | DeepSeek-VL 1.3B/7B               | [arXiv:2403.05525](https://arxiv.org/abs/2403.05525)                          | SigLIP + SAM 混合视觉编码，1024×1024 高分辨率 VLM                                      |
| 2024-05       | DeepSeek-V2 16B / 236B-A21B       | [arXiv:2405.04434](https://arxiv.org/abs/2405.04434)                          | **MLA**（KV cache ↓93.3%）+ DeepSeekMoE；API 定价引发行业价格战                         |
| 2024-05       | DeepSeek-Prover 7B                | [arXiv:2405.14333](https://arxiv.org/abs/2405.14333)                          | Lean 4 大规模合成定理证明数据                                                          |
| 2024-06       | DeepSeek-Coder-V2 16B / 236B-A21B | [arXiv:2406.11931](https://arxiv.org/abs/2406.11931)                          | 代码+数学+自然语言统一，338 语言 / 128K 上下文，首个代码能力超 GPT-4-Turbo 的开源模型                    |
| 2024-08       | Fire-Flyer AI/HPC（infra 论文）       | [arXiv:2408.14158](https://arxiv.org/abs/2408.14158)（SC 2024）                 | 万卡 PCIe A100 集群软硬件协同设计，3FS 与"开源周"的工程前身                                      |
| 2024-09-05    | DeepSeek-V2.5 ✱                   | [API 公告](https://api-docs.deepseek.com/updates/)                              | V2-Chat 与 Coder-V2 融合为单模型，写作/指令遵循/编码提升                                      |
| 2024-10       | Janus 1.3B                        | [arXiv:2410.13848](https://arxiv.org/abs/2410.13848)                          | 解耦视觉编码（理解/生成各用一路）的统一多模态模型                                                   |
| 2024-12       | DeepSeek-VL2（3 尺寸）                | [arXiv:2412.10302](https://arxiv.org/abs/2412.10302)                          | 动态切块（dynamic tiling）+ DeepSeekMoE/MLA 的 VLM，激活 1.0B/2.8B/4.5B               |
| 2024-12-26    | **DeepSeek-V3** 671B-A37B         | [arXiv:2412.19437](https://arxiv.org/abs/2412.19437)                          | 14.8T token、FP8 训练、MTP、无辅助损失负载均衡；2048×H800 约 557.6 万美元                      |
| 2025-01-20    | **DeepSeek-R1** / R1-Zero + 6 蒸馏  | [arXiv:2501.12948](https://arxiv.org/abs/2501.12948)                          | 纯 RL 激发推理能力；2025-09 登 Nature 封面                                             |
| 2025-01-27    | Janus-Pro 1.5B/7B                 | [arXiv:2501.17811](https://arxiv.org/abs/2501.17811)                          | Janus 在训练策略/数据/规模上全面升级，文生图显著增强                                              |
| 2025-02-24~28 | 开源周（详见 §二）                        | GitHub                                                                        | FlashMLA / DeepEP / DeepGEMM / DualPipe / 3FS + smallpond（后续追加 EPLB）        |
| 2025-03-24    | DeepSeek-V3-0324 ✱                | [API 公告](https://api-docs.deepseek.com/updates/)                              | V3 小版本：推理、前端代码、中文写作、函数调用增强                                                  |
| 2025-04-30    | DeepSeek-Prover-V2 7B / 671B      | [arXiv:2504.21801](https://arxiv.org/abs/2504.21801)                          | 递归证明搜索（子目标分解 + 课程学习）；671B 在 miniF2F-test 达 88.9% SOTA                       |
| 2025-05-28    | DeepSeek-R1-0528 ✱                | [API 公告](https://api-docs.deepseek.com/updates/) / HF                         | V3 架构继续 RL 训练，AIME 2025 提至 87.5%，幻觉与函数调用改善                                  |
| 2025-08-21    | DeepSeek-V3.1                     | [V3.1 Approach 定性总结](https://huggingface.co/deepseek-ai/DeepSeek-V3.1)（✱ 无论文） | 单模型**混合思考**（thinking / non-thinking 双模式），agent 与工具调用强化                      |
| 2025-09-22    | DeepSeek-V3.1-Terminus ✱          | [API 公告](https://api-docs.deepseek.com/news/news250922/)                      | V3 世代收官稳定版：语言一致性、输出稳定性、Code/Search Agent 行为优化                               |
| 2025-09-29    | DeepSeek-V3.2-Exp                 | [API 公告](https://api-docs.deepseek.com/news/news250929/)                      | **DSA 稀疏注意力**首秀（685B），长上下文成本大降，vLLM / SGLang day-0 支持                       |
| 2025-10       | DeepSeek-OCR 3B                   | [arXiv:2510.18234](https://arxiv.org/abs/2510.18234)                          | "光学压缩"：文本渲染为图像做长上下文压缩，~10× 近无损；DeepEncoder 动态分辨率双编码器                        |
| 2025-12-01    | **DeepSeek-V3.2**（+Speciale）      | [arXiv:2512.02556](https://arxiv.org/abs/2512.02556)                          | DSA 正式版 + 可扩展 RL 后训练；Speciale 对标 GPT-5 / Gemini 3 Pro，IMO/IOI 2025 金牌水准     |
| 2026-01       | DeepSeek-OCR 2                    | [arXiv:2601.20552](https://arxiv.org/abs/2601.20552)                          | 视觉因果流：两级级联 1D 因果推理替代 2D 编码，DeepEncoder V2 动态重排视觉 token                      |
| 2026-04-24    | **DeepSeek-V4** Pro / Flash       | [arXiv:2606.19348](https://arxiv.org/abs/2606.19348)（2026-06 公告）              | Pro 1.6T-A49B / Flash 284B-A13B；原生 1M 上下文；CSA+HCA / mHC / Muon / 32T+ token |

---

## 一、基础模型详解

### 1. 2023：通用 + 代码双线出道

- **DeepSeek LLM（7B/67B，2023-11-29 开源）**：论文 [DeepSeek LLM: Scaling Open-Source Language Models with Longtermism](https://arxiv.org/abs/2401.02954)。以 2T token（远超同期惯用量）"长期主义"预训练，67B 在中英文综合与数学上超越 Llama2-70B，是中国团队首次进入全球开源第一梯队。
- **DeepSeek Coder（1.3B/6.7B/33B，2023-11 开源）**：论文 [DeepSeek Coder: When the Large Language Model Meets Programming](https://arxiv.org/abs/2401.14196)。87 种编程语言、仓库级预训练（以文件级依赖拓扑重排语料）、fill-in-the-middle；33B 在 HumanEval 上首个超过 GPT-3.5-Turbo 的开源代码模型。

### 2. 2024：MoE、MLA 与专用模型矩阵

- **DeepSeekMoE 16B**（[arXiv:2401.06066](https://arxiv.org/abs/2401.06066)）：把专家切得更细并隔离共享专家，追求"极致专家特化"；16B-MoE 用约 40% 计算量对齐 DeepSeek 7B，架构延续到 V2/V3/V4。
- **DeepSeekMath 7B / 7B-RL**（[arXiv:2402.03300](https://arxiv.org/abs/2402.03300)）：从 Common Crawl 迭代筛选出 120B-token DeepSeekMath Corpus；提出 **GRPO**（Group Relative Policy Optimization，砍去 critic 的 PPO 变体），7B-RL 在 MATH 上达 51.7%，是后来 R1 的 RL 基石。
- **DeepSeek-VL**（[arXiv:2403.05525](https://arxiv.org/abs/2403.05525)）：SigLIP（语义）+ SAM（细节）混合视觉编码 + 数据混合策略，支持 1024×1024 高分辨率。
- **DeepSeek-V2（236B-A21B / 16B，2024-05 开源）**：论文 [DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model](https://arxiv.org/abs/2405.04434)。两大招牌：**MLA**（Multi-head Latent Attention，把 KV cache 压缩进低维潜在向量，缓存↓93.3%、推理成本大降）+ DeepSeekMoE 细粒度专家；API 定价仅为 GPT-4-Turbo 的约百分之一，直接引发国内大模型价格战。
- **DeepSeek-Prover 7B**（[arXiv:2405.14333](https://arxiv.org/abs/2405.14333)）：用国家/国际数学竞赛题 + Lean 4 编译器反馈大规模合成证明数据，后续 Prover-V2 的数据基础。
- **DeepSeek-Coder-V2（236B-A21B / 16B，2024-06-17 开源）**：在 V2 基座上追加 6T token（代码+数学+自然语言），扩展到 338 种编程/自然语言、128K 上下文；首个在代码能力上超越 GPT-4-Turbo 的开源模型。
- **DeepSeek-V2.5（2024-09-05，✱）**：V2-Chat 与 Coder-V2 融合升级，无论文。
- **Janus 1.3B**（[arXiv:2410.13848](https://arxiv.org/abs/2410.13848)）：理解走 SigLIP、生成走 VQ tokenizer 的**解耦视觉编码**，统一多模态理解与生成。
- **DeepSeek-VL2（2024-12）**：论文 [DeepSeek-VL2: Mixture-of-Experts Vision-Language Models for Advanced Multimodal Understanding](https://arxiv.org/abs/2412.10302)。动态切块处理任意宽高比高分辨率图像，语言侧为 DeepSeekMoE + MLA；Tiny/Small/Base 三档（激活 1.0B/2.8B/4.5B）。

### 3. 2024-12 ~ 2025-01：V3 与 R1 的现象级出圈

- **DeepSeek-V3（671B-A37B，2024-12-26 开源，MIT）**：论文 [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)。14.8T token 预训练；关键工程：**无辅助损失的负载均衡**（bias 调节取代 aux loss）、**MTP**（多 token 预测，兼作推测解码）、**FP8 混合精度**超大规模训练验证、MLA + DeepSeekMoE；2048 张 H800、278.8 万 GPU 时（≈557.6 万美元）训练成本震惊业界。配套 infra 即后来的"开源周"六件套（§二）。
- **DeepSeek-R1 / R1-Zero（2025-01-20 开源，MIT）**：论文 [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)。R1-Zero 证明**纯 RL（GRPO）无需任何 SFT** 即可激发推理，并自发涌现自我反思、验证、"aha moment"；R1 用冷启动 SFT → 推理 RL → 拒绝采样 SFT → 全场景 RL 四阶段兼顾能力与对齐；蒸馏出 Qwen 1.5B/7B/14B/32B + Llama 8B/70B 六个小模型。**2025-09-17 登 Nature 封面**（Nature 645: 633–638，中国大模型研究首次），披露 R1 训练成本仅约 29.4 万美元；梁文锋入选 Nature 2025 年度十大科学人物。
- **Janus-Pro（1.5B/7B，2025-01-27）**：[arXiv:2501.17811](https://arxiv.org/abs/2501.17811)，Janus 的训练策略/数据/规模三重升级。

### 4. 2025：V3 世代收官（V3.1 / V3.2 / OCR）

- **V3-0324（2025-03-24，✱）**：小版本，推理/前端代码/函数调用增强。
- **DeepSeek-Prover-V2（7B / 671B，2025-04-30）**：[arXiv:2504.21801](https://arxiv.org/abs/2504.21801)。用 DeepSeek-V3 做递归证明搜索——定理分解为子目标（引理）分别证明，已证子目标构成合成训练数据（课程学习式冷启动）；671B 在 miniF2F-test 达 **88.9%** SOTA，7B 亦刷新同档纪录。
- **R1-0528（2025-05-28，✱）**：V3 架构继续大规模 RL，AIME 2025 提至 87.5%；幻觉显著降低、支持函数调用/JSON 输出；同步更新全部蒸馏小模型。
- **V3.1（2025-08-21）**：无 arXiv 论文，仅模型卡附带定性总结《DeepSeek-V3.1 Approach》。核心是**混合思考架构**：单模型同时支持 thinking / non-thinking 两种模式（终结 V3-chat 与 R1 分立），agent / 工具调用大幅强化。
- **V3.1-Terminus（2025-09-22，✱）**：V3 世代收官稳定版（语言一致性、输出稳定性、Code/Search Agent 行为优化）。
- **V3.2-Exp（2025-09-29）**：[API 公告](https://api-docs.deepseek.com/news/news250929/)（技术细节并入 V3.2 论文）。首次实用化 **DSA（DeepSeek Sparse Attention）**：轻量索引选 top-k token + 重排序，长上下文质量几乎无损而计算大降；vLLM / SGLang day-0 支持。
- **DeepSeek-OCR（3B，2025-10）**：[arXiv:2510.18234](https://arxiv.org/abs/2510.18234)，"Contexts Optical Compression"——把长文本渲染成图像、用视觉编码器压缩回少量 token，~10× 压缩近无损（20× 仍保留约六成效果）；DeepEncoder（SAM 细节 + CLIP 语义双编码器、动态分辨率），并统一 OCR / 视觉定位 / 布局分析任务。
- **V3.2 + V3.2-Speciale（2025-12-01）**：论文 [DeepSeek-V3.2: Pushing the Frontier of Open Large Language Models](https://arxiv.org/abs/2512.02556)。DSA 正式化 + **可扩展 RL 后训练** + 大规模 agentic 任务合成管线；Speciale（高算力推理变体，限时端点至 2025-12-15）性能对标 GPT-5 / Gemini 3 Pro，达 IMO / IOI 2025 金牌水准。

### 5. 2026：V4 世代（1M 上下文）

- **DeepSeek-V4 Pro / Flash（API 2026-04-24 上线，论文 2026-06）**：论文 [DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](https://arxiv.org/abs/2606.19348)。V4-Pro 1.6T 总参 / 49B 激活、V4-Flash 284B / 13B 激活，原生 **1M token 上下文**；架构要点：CSA（压缩稀疏注意力）+ HCA（重度压缩注意力）混合注意力、**mHC**（流形约束超连接）替代普通残差、**Muon 优化器**；32T+ token 预训练。效率：1M 上下文下单 token 推理 FLOPs 仅为 V3.2 的 27%、KV cache 为 10%。权重开放于 [HF deepseek-ai](https://huggingface.co/deepseek-ai)。
- **DeepSeek-OCR 2（2026-01）**：[arXiv:2601.20552](https://arxiv.org/abs/2601.20552)，"Visual Causal Flow"——探索用两级级联的 1D 因果推理替代 2D 视觉编码；DeepEncoder V2 可在输入时动态重排视觉 token，极低视觉 token 预算下仍有约 91% 性能。
- 生态注记：第三方工作 [FlashMemory-DeepSeek-V4](https://arxiv.org/abs/2606.09079)（2026-06，非官方）在 V4 上加 Lookahead 稀疏注意力 + 神经记忆索引，KV cache 再降至基线 13.5%。

---

## 二、开源工具（deepseek-ai GitHub）

### 开源周（2025-02-24 ~ 02-28，"Day N" 连续开源）

| Day | 日期 | 仓库 | 定位 | 要点 |
|---|---|---|---|---|
| 1 | 02-24 | [FlashMLA](https://github.com/deepseek-ai/FlashMLA) | MLA 解码内核 | Hopper（H800）优化：~3000 GB/s 访存 + 580 TFLOPS 计算变体，支持 64B 分页 KV cache |
| 2 | 02-25 | [DeepEP](https://github.com/deepseek-ai/DeepEP) | MoE 专家并行通信库 | 首个开源 EP all-to-all 通信库；NVLink+RDMA 常规训练内核 + 纯 RDMA 低延迟（~数十 µs 级）解码内核 |
| 3 | 02-26 | [DeepGEMM](https://github.com/deepseek-ai/DeepGEMM) | FP8 GEMM 库 | JIT 编译、零繁重依赖；H800 上最高 1350+ TFLOPS，较 CUTLASS 快至 ~2.7×；普通与 MoE（masked 分组）两类内核 |
| 4 | 02-27 | [DualPipe](https://github.com/deepseek-ai/DualPipe) | 双向流水线并行算法 | 计算-通信完全重叠、流水线气泡趋近于零（V3 训练所用；代码极简，仅 ~10 个文件） |
| 5 | 02-28 | [3FS](https://github.com/deepseek-ai/3FS) + [smallpond](https://github.com/deepseek-ai/smallpond) | 分布式文件系统 + 数据处理框架 | 3FS：RDMA + 全 SSD，为 AI 训练/推理设计（含 KVCache 直接加载），仓库附设计文档；smallpond：基于 DuckDB 的轻量数据处理 |
| 追加 | 2025-03 | [EPLB](https://github.com/deepseek-ai/EPLB) | 专家并行负载均衡器 | 冗余专家复制 + 静态/动态重排，与 DeepEP 配套解决 MoE 专家负载倾斜 |

### 前置与配套

- **Fire-Flyer AI/HPC**（[arXiv:2408.14158](https://arxiv.org/abs/2408.14158)，发表 SC 2024）：万卡 PCIe A100（无 NVLink/IB）集群的软硬件协同设计——用 2 万卡时级别的互联/存储优化（3FS 即诞生于此体系）逼近 DGX-A100 级算力利用率，成本大幅降低。"开源周"本质上是该论文 + V3 训练栈（自研 HAI-LLM 框架）的逐步开源化。
- **模型与权重仓库**：GitHub `deepseek-ai/DeepSeek-V3`、`DeepSeek-R1`、`DeepSeek-OCR(-2)`、`DeepSeek-V3.2-Exp` 等；权重在 [HF deepseek-ai](https://huggingface.co/deepseek-ai)（V3 / R1 系为 MIT 许可，VL2 论文 CC BY 4.0）。
- **推理生态联动**：自 V3.2-Exp 起，vLLM 与 SGLang 对 DSA 稀疏注意力提供 day-0 支持（[vLLM 博客](https://vllm.ai/blog/2025-09-29-deepseek-v3-2/)、[SGLang 博客](https://www.lmsys.org/blog/2025-09-29-deepseek-V32/)）。

---

## 三、技术演进主线

- **模型架构**：DeepSeekMoE 细粒度专家（2401）→ MLA + MoE（V2）→ FP8 / MTP / 无辅助损失负载均衡（V3）→ GRPO 纯 RL（Math → R1）→ 混合思考（V3.1）→ DSA 稀疏注意力（V3.2）→ CSA+HCA + mHC + Muon + 1M 上下文（V4）
- **系统与算力**：自建 PCIe A100 集群（Fire-Flyer AI/HPC）→ 自研 HAI-LLM 训练框架 → "开源周"把注意力内核 / EP 通信 / FP8 GEMM / 流水线 / 存储全栈开源
- **开源策略**：从开放权重（MIT）到开放基础设施 + day-0 生态联动（vLLM / SGLang），"越是开源，越能扩大生态"
- **RL 与推理**：GRPO（Math）→ 纯 RL 涌现（R1-Zero）→ 继续规模化 RL（R1-0528）→ 可扩展 RL 后训练（V3.2），一条主线贯穿 2024-02 至今
