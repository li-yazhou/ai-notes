---
type: overview
title: "Qwen 基础模型与开源工具总览（时间线）"
created: 2026-08-15
updated: 2026-08-15
status: active
tags:
  - vendor/qwen
  - paper/foundation-model
  - paper/release
  - tool/open-source
---

# Qwen 基础模型与开源工具总览（时间线）

> 范围：阿里通义实验室 **Qwen（通义千问）** 官方发布的**基础模型**（语言 / VL 视觉 / Omni 全模态 / Coder / Math / Image 生成 / QwQ·QVQ 推理 / Embedding / TTS·ASR·音乐）与**开源工具生态**（QwenLM GitHub 组织、Qwen-Agent、Qwen Code、ms-swift / EvalScope 等），按发布时间排序；兄弟团队**通义万相 Wan**（视频生成）、AIDC Marco 简记
> 信息来源：arXiv 官方页面、Qwen 官方博客（[qwenlm.github.io/blog](https://qwenlm.github.io/blog/) → [qwen.ai/blog](https://qwen.ai/blog)）、[QwenLM GitHub](https://github.com/QwenLM)、[HF Qwen 组织](https://huggingface.co/Qwen)；标 ✱ 的条目为无论文发布（博客 / 模型卡 / API 公告）
> 关联：[[01-deepseek-overview]]、[[01-glm-overview]]（姊妹篇）、[[2607-arxiv-llms]]（月度厂商 digest，Qwen 新论文按月收录）

---

## 〇、一页时间线

| 时间         | 发布物                                           | 论文 / 来源                                                                                                                                                                                           | 一句话要点                                                                                 |
| ---------- | --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| 2023-04-11 | 通义千问（闭源产品）✱                                   | 阿里云峰会                                                                                                                                                                                             | 千亿参数对话模型接入钉钉/天猫精灵，9 月公众开放，10 月云栖大会发布 2.0                                              |
| 2023-08-03 | **Qwen-7B**                                   | [arXiv:2309.16609](https://arxiv.org/abs/2309.16609)                                                                                                                                              | 首个开源版本，2.2T token、原生 8K 上下文，Tongyi Qianwen LICENSE                                    |
| 2023-08    | Qwen-VL / VL-Chat                             | [arXiv:2308.12966](https://arxiv.org/abs/2308.12966)                                                                                                                                              | 基于 Qwen-7B 的 VLM，grounding + OCR 同规模领先                                                |
| 2023-09-25 | Qwen-14B ✱                                    | GitHub                                                                                                                                                                                            | 同日发布 qwen.cpp 与 Qwen-Agent（工具生态起点）                                                    |
| 2023-11    | Qwen-Audio                                    | [arXiv:2311.07919](https://arxiv.org/abs/2311.07919)                                                                                                                                              | 30+ 音频任务统一音频-语言模型，层级标签多任务预训练                                                          |
| 2023-11-30 | Qwen-1.8B / 72B ✱                             | [博客](https://qwenlm.github.io/blog/qwen/)                                                                                                                                                         | 72B 训练 3T token、32K 上下文，L-Eval 超 ChatGPT-3.5-16k                                      |
| 2024-02-04 | **Qwen1.5 全家**（0.5B–72B）✱                     | [博客](https://qwenlm.github.io/blog/qwen1.5/)                                                                                                                                                      | 6 档尺寸、首次并入 HF transformers；后续补 32B/110B/MoE-A2.7B                                     |
| 2024-04-16 | CodeQwen1.5-7B ✱                              | [博客](https://qwenlm.github.io/blog/codeqwen1.5/)                                                                                                                                                  | 92 种语言、64K 上下文代码模型，代码线起点                                                              |
| 2024-06-07 | **Qwen2**（+57B-A14B MoE）                      | [arXiv:2407.10671](https://arxiv.org/abs/2407.10671)                                                                                                                                              | 0.5B–72B 六档 + 首个 MoE；约 30 种语言、128K（YaRN）；主力转 Apache 2.0                               |
| 2024-07    | Qwen2-Audio-7B                                | [arXiv:2407.10759](https://arxiv.org/abs/2407.10759)                                                                                                                                              | 语音对话/音频分析双模式自动切换，SFT+DPO                                                              |
| 2024-08-08 | Qwen2-Math ✱                                  | [博客](https://qwenlm.github.io/blog/qwen2-math/)                                                                                                                                                   | 1.5B/7B/72B 英文数学专用（方法并入 2.5-Math TR）                                                  |
| 2024-08-29 | **Qwen2-VL** 2B/7B                            | [arXiv:2409.12191](https://arxiv.org/abs/2409.12191)                                                                                                                                              | **Naive Dynamic Resolution** + M-RoPE，统一图文/视频范式，多模态比肩 GPT-4o                          |
| 2024-09-19 | **Qwen2.5 家族** 0.5B–72B                       | [arXiv:2412.15115](https://arxiv.org/abs/2412.15115)                                                                                                                                              | 18T token 预训练、多数 128K 上下文，开源全系最长命的底座                                                  |
| 2024-09    | Qwen2.5-Math + Qwen2.5-Coder                  | [2409.12122](https://arxiv.org/abs/2409.12122) / [2409.12186](https://arxiv.org/abs/2409.12186)                                                                                                   | Math：CoT/TIR 自改进；Coder 11 月补全 0.5B–32B，32B 比肩 GPT-4o                                  |
| 2024-11-21 | Marco-o1（AIDC，相关）                             | [arXiv:2411.14405](https://arxiv.org/abs/2411.14405)                                                                                                                                              | 阿里国际团队面向开放式问题的 o1 式推理（非 Qwen 团队）                                                      |
| 2024-11-28 | **QwQ-32B-Preview** ✱                         | [博客](https://qwenlm.github.io/blog/qwq-32b-preview/)                                                                                                                                              | 首个开源推理实验模型，AIME 50.0 / MATH-500 90.6                                                  |
| 2024-12-25 | QVQ-72B-Preview ✱                             | [博客](https://qwenlm.github.io/blog/qvq-72b-preview/)                                                                                                                                              | 基于 Qwen2-VL-72B 的视觉推理，MathVista 微超 o1                                                 |
| 2025-01-26 | **Qwen2.5-VL** 3B/7B/72B                      | [arXiv:2502.13923](https://arxiv.org/abs/2502.13923)                                                                                                                                              | 原生动态分辨率 ViT、长视频理解 + 秒级定位、面向电脑/手机操作 Agent                                              |
| 2025-01-27 | Qwen2.5-1M-Preview ✱                          | [博客](https://qwenlm.github.io/blog/qwen2.5-1m/)                                                                                                                                                   | 上下文 128K→1M，同 token 单价约为 128K 版 1/7                                                   |
| 2025-01-28 | Qwen2.5-Max（闭源 API）✱                          | [博客](https://qwenlm.github.io/blog/qwen2.5-max/)                                                                                                                                                  | 20T+ token MoE 旗舰，多项对标超 DeepSeek-V3 / GPT-4o                                          |
| 2025-02-25 | Wan2.1（通义万相，开源）                               | [arXiv:2503.20314](https://arxiv.org/abs/2503.20314)                                                                                                                                              | 开源 SOTA 文/图生视频，1.3B 消费级显卡可跑                                                           |
| 2025-03-06 | **QwQ-32B** ✱                                 | [博客](https://qwenlm.github.io/blog/qwq-32b/)                                                                                                                                                      | 大规模两阶段 RL，1/20 激活参数对标 DeepSeek-R1-671B                                                |
| 2025-03-26 | Qwen2.5-Omni-7B                               | [arXiv:2503.20215](https://arxiv.org/abs/2503.20215)                                                                                                                                              | 端到端全模态，**Thinker-Talker** 架构 + TMRoPE，流式语音输出                                          |
| 2025-04-29 | **Qwen3**（235B-A22B + 30B-A3B + 6 dense）      | [arXiv:2505.09388](https://arxiv.org/abs/2505.09388)                                                                                                                                              | **混合思考模式** + 思考预算，36T token、119 语言，全系 Apache 2.0                                      |
| 2025-06-05 | Qwen3-Embedding / Reranker                    | [arXiv:2506.05176](https://arxiv.org/abs/2506.05176)                                                                                                                                              | 0.6B–8B 指令感知嵌入 + 重排，多语 MTEB 登顶                                                        |
| 2025-07-22 | **Qwen3-Coder-480B-A35B** ✱                   | [博客](https://qwenlm.github.io/blog/qwen3-coder/) / [GitHub](https://github.com/QwenLM/Qwen3-Coder)                                                                                                | 原生 256K→1M，课程式 Agent 训练 + 执行反馈 Code RL；配套 **Qwen Code CLI**                           |
| 2025-07~08 | Qwen3-2507 系列更新 ✱                             | [Qwen3 仓库 News](https://github.com/QwenLM/Qwen3)                                                                                                                                                  | 235B/30B 双线更新 Instruct/Thinking-2507，8 月全系支持 1M token                                 |
| 2025-08-04 | **Qwen-Image** 20B + Image-Edit               | [arXiv:2508.02324](https://arxiv.org/abs/2508.02324)                                                                                                                                              | MMDiT 文生图，中文长文本渲染招牌；Edit（08-19）专用编辑版                                                  |
| 2025-09-11 | Qwen3-Next-80B-A3B ✱                          | [博客](https://qwen.ai/blog/qwen3-next)                                                                                                                                                             | **门控注意力 + Gated DeltaNet 混合架构**，512 专家超稀疏 MoE，解码 2–3×                                 |
| 2025-09-22 | Qwen3-Omni-30B-A3B                            | [arXiv:2509.17765](https://arxiv.org/abs/2509.17765)                                                                                                                                              | Thinker-Talker MoE，首包 234ms，36 项音频/视听基准 32 项开源 SOTA                                   |
| 2025-09-23 | **Qwen3-VL**（235B-A22B / 30B-A3B 起）           | [arXiv:2511.21631](https://arxiv.org/abs/2511.21631)                                                                                                                                              | Interleaved-MRoPE + **DeepStack**，256K→1M，GUI Agent + 视觉转代码                           |
| 2025-09-24 | Qwen3-Max（闭源 API）✱                            | [博客](https://qwen.ai/blog?id=qwen3-max)                                                                                                                                                           | 万亿+参数旗舰（快照 0828），对标 GPT-5 / Gemini 2.5 Pro                                            |
| 2025-09    | Tongyi DeepResearch 30B-A3B ✱                 | [HF 模型卡](https://huggingface.co/Qwen)                                                                                                                                                             | 开源网页深度研究 Agent（同期另有 Qwen3Guard 安全护栏开源）                                                |
| 2026-01-08 | Qwen3-VL-Embedding / Reranker                 | [arXiv:2601.04720](https://arxiv.org/abs/2601.04720)                                                                                                                                              | 统一多模态检索排序框架，文本/图像/截图/视频混合输入                                                           |
| 2026-01-22 | **Qwen3-TTS** 系列（开源）                          | [arXiv:2601.15621](https://arxiv.org/abs/2601.15621)                                                                                                                                              | 双轨 LM（25Hz 语义 + 12Hz 多码本），500 万小时语音，首包低至 97ms                                         |
| 2026-01-29 | **Qwen3-ASR** 系列（开源）                          | [arXiv:2601.21337](https://arxiv.org/abs/2601.21337)                                                                                                                                              | 52 语言/方言 + 歌唱/BGM 一体识别，1.7B 声称开源 ASR SOTA                                             |
| 2026-02-02 | Qwen3-Coder-Next（80B-A3B）                     | [arXiv:2603.00729](https://arxiv.org/abs/2603.00729)                                                                                                                                              | Qwen3-Next 正统续作，可验证任务大规模合成 + 可执行环境 RL                                                 |
| 2026-02-16 | **Qwen3.5** 397B-A17B + Plus（API）✱            | [官方博客](https://qwen.ai/blog?id=qwen3.5) / [仓库](https://github.com/QwenLM/Qwen3.6)                                                                                                                 | **原生多模态**（早期融合）+ Gated Delta 混合架构，201 种语言，无总 TR                                       |
| 2026-02~03 | Qwen3.5 全谱系开放 ✱                               | Qwen3.5/3.6 仓库 News                                                                                                                                                                               | 122B-A10B/35B-A3B/27B（02-24）→ 9B/4B/2B/0.8B（03-02），全系 Apache 2.0                      |
| 2026-04    | **Qwen3.6**（27B / 35B-A3B 开源 + Plus/Max API）✱ | [仓库](https://github.com/QwenLM/Qwen3.6)                                                                                                                                                           | Agentic Coding + "Thinking Preservation" 跨轮保留思考，SWE-bench Verified 73.4%（35B）         |
| 2026-04-17 | Qwen3.5-Omni                                  | [arXiv:2604.15804](https://arxiv.org/abs/2604.15804)                                                                                                                                              | Thinker/Talker 均为混合注意力 MoE + ARIA 动态对齐；仅 API（Plus/Flash），未开源权重                        |
| 2026-05-20 | Qwen3.7-Max（API）✱                             | [官方博客](https://qwen.ai/blog?id=qwen3.7)                                                                                                                                                           | "The Agent Frontier"：1M 上下文、长程 Agent 可持续自主 35 小时                                      |
| 2026-07    | 音频/UI Agent 四连                                | [2607.11699](https://arxiv.org/abs/2607.11699) / [2607.11738](https://arxiv.org/abs/2607.11738) / [2607.27011](https://arxiv.org/abs/2607.27011) / [2607.28227](https://arxiv.org/abs/2607.28227) | Qwen-Music（人声歌曲生成）/ Audio-VAE / Audio-3.0-Gen（非自回归）/ UI-Agent（真实设备 GUI）               |
| 2026-08-03 | **Qwen3.8-Max**（API）✱                         | [官方博客](https://qwen.ai/blog?id=qwen3.8)                                                                                                                                                           | 2.4T-A95B、1M 上下文，主题 "Coding and Cowork"；07-19 WAIC 预览                                 |
| 2026-08 上旬 | **Qwen3.8-27B**（开源）✱                          | [HF 模型卡](https://huggingface.co/Qwen/Qwen3.8-27B)                                                                                                                                                 | 27B dense **原生多模态**（图像 + 小时级视频），256K→1M，**Apache 2.0**；SWE-bench Pro 61.7 为 27B 级开源最强 |
| 2026-08-12 | **Qwen3.8-2.4T-A95B 开源权重** ✱                  | [HF Qwen](https://huggingface.co/Qwen)                                                                                                                                                            | Max 系列史上首次开源；自定义许可（年营收 ≥5000 万美元需商业授权）                                                |

---

## 一、语言模型主线

### 1. 2023：从闭源产品到全面开源

- **通义千问（2023-04-11）**✱：阿里云峰会发布千亿参数对话模型，率先接入钉钉、天猫精灵；2023-09-13 面向公众开放，10-31 云栖大会发布 2.0 与 Qwen-Max API。
- **Qwen-7B / 14B / 1.8B / 72B（2023-08 ~ 11）**：论文 [Qwen Technical Report](https://arxiv.org/abs/2309.16609)。RoPE + SwiGLU + RMSNorm、tiktoken 词表 151,851；7B 以 2.2T token 开源（初版 Tongyi Qianwen LICENSE，商用需申请）；72B（2023-11-30）训练 3T token、32K 上下文，L-Eval 62.30 超 ChatGPT-3.5-16k。9 月发布 14B 的同日开源 **qwen.cpp** 与 **Qwen-Agent**——工具生态与模型同步生长。

### 2. 2024：Qwen1.5 → Qwen2 → Qwen2.5 三连跳

- **Qwen1.5（2024-02-04）**✱：无论文。0.5B–72B 六档首发（后续补 32B、110B 与首个 MoE 试验 Qwen1.5-MoE-A2.7B），首次并入 HF transformers 主干；**Qwen2 起（2024-06-07）开放权重主力转 Apache 2.0**（72B 暂留 Tongyi 许可）。
- **Qwen2（[arXiv:2407.10671](https://arxiv.org/abs/2407.10671)）**：0.5B–72B + 57B-A14B 首个正式 MoE；约 30 种语言、GQA、32K–128K（YaRN）；72B MMLU 84.2、MT-Bench 9.12。
- **Qwen2.5（2024-09-19；TR [arXiv:2412.15115](https://arxiv.org/abs/2412.15115)）**：0.5B–72B 七档、**预训练 7T→18T token**、多数 128K 上下文；72B-base 以 1/5 参数媲美 Llama-3-405B，成为此后一年多全球衍生模型最多的开源底座之一。
- 专项线同年成型：**CodeQwen1.5-7B**（2024-04）→ **Qwen2-Math**（2024-08）→ **Qwen2.5-Math**（[arXiv:2409.12122](https://arxiv.org/abs/2409.12122)，CoT/TIR 自改进，MATH 92.9@TIR）与 **Qwen2.5-Coder**（[arXiv:2409.12186](https://arxiv.org/abs/2409.12186)，追加 5.5T token，11 月补全 0.5B–32B，32B Aider 73.7 比肩 GPT-4o）。

### 3. 2024-11 ~ 2025-03：QwQ 推理线与 Max 旗舰

- **QwQ-32B-Preview（2024-11-28）**✱：32B 推理实验模型（AIME 50.0），开源社区最早可用的 o1 式权重之一；同期阿里国际 AIDC 团队的 **Marco-o1**（[arXiv:2411.14405](https://arxiv.org/abs/2411.14405)，CoT 微调 + MCTS 面向开放式问题）与之呼应。
- **QwQ-32B（2025-03-06）**✱：无论文。冷启动检查点出发的大规模两阶段 RL（数学答案校验器 / 代码执行服务器结果奖励 → 通用对齐 RL），以 **1/20 激活参数对标 DeepSeek-R1-671B**，Apache 2.0。
- **Qwen2.5-Max（2025-01-28）**✱：闭源 API 的 20T+ token MoE 旗舰（参数量未官方披露，媒体称 1T+），MMLU-Pro / LiveCodeBench 等多项超 DeepSeek-V3 与 GPT-4o；2 月补 QwQ-Max-Preview 推理档。

### 4. 2025-04 ~ 12：Qwen3 世代——混合思考与 Agent 化

- **Qwen3（2025-04-29；TR [arXiv:2505.09388](https://arxiv.org/abs/2505.09388)）**：2 个 MoE（旗舰 235B-A22B、性价比 30B-A3B）+ 6 个 dense（0.6B–32B）全系 Apache 2.0。核心是**混合思考模式**（单模型 `/think`、`/no_think` 软切换 + 思考预算）与四阶段后训练（CoT 冷启动 → 推理 RL → 思考模式融合 → 通用 RL）；约 36T token、119 种语言。
- **Qwen3-Coder-480B-A35B（2025-07-22）**✱：无论文（后继 Coder-Next 有 TR）。原生 256K（YaRN 至 1M），课程式 Agent 训练 + 执行反馈 Code RL + 长程 Agent RL（阿里云 2 万并行环境）；开源代码模型 SWE-bench Verified SOTA、对标 Claude Sonnet 4，同日推出 **Qwen Code CLI**；7-31 补 30B-A3B。
- **Qwen3-2507 系列（2025-07~08）**✱：235B/30B 双线分别更新 Instruct（非思考）与 Thinking 版，原生 256K、8 月全系扩展到 1M token。
- **Qwen3-Next-80B-A3B（2025-09-11）**✱：架构试验田——**门控注意力 + Gated DeltaNet 线性注意力 3:1 混合** + 512 专家激活 8 的超稀疏 MoE；约 Qwen3-32B 性能、激活参数 1/10、解码吞吐 2–3×。该路线直接孕育了 2026 年的 Qwen3.5/Qwen3.6 与 Coder-Next（仓库后滚动改名为 Qwen3.6）。
- **Qwen3-Max（2025-09-24）**✱：万亿+参数 API 旗舰（快照 qwen3-max-0828），对标 GPT-5 / Gemini 2.5 Pro / Claude Opus 4.1，Agent 与工具调用强项。

### 5. 2026：Qwen3.5 → 3.8 高频"半代际"迭代

- **Qwen3.5（2025 除夕 2026-02-16 起）**✱：**原生多模态**（视觉-语言早期融合统一基座）+ Gated Delta 混合注意力 + 稀疏 MoE，201 种语言/方言（上代 82），256K 上下文；开源旗舰 397B-A17B + API 版 Plus，**无总技术报告**（仅 Omni 分支有 TR）；02-24 补 122B-A10B / 35B-A3B / 27B，03-02 补 9B/4B/2B/0.8B，0.8B→397B 全谱系 Apache 2.0；03-25 Qwen3.5-Max-Preview 登陆 LM Arena。
- **Qwen3.6（2026-04）**✱：开源 35B-A3B（04-16）与 27B dense（04-22）+ API Plus/Max-Preview；主打稳定性与实用 Agentic Coding（与 Qwen Code 协同）、"Thinking Preservation" 跨轮保留思考上下文；35B SWE-bench Verified 73.4%、27B 编码表现称超自家上代 400B 级旗舰。
- **Qwen3.7-Max（2026-05-20）**✱："The Agent Frontier"——1M 上下文、原生扩展思考，长程 Agent 任务可持续自主 **35 小时**（内部完成 1000+ 工具调用将某内核推理提速 ~10×）；6-02 补多模态输入的 Qwen3.7-Plus。
- **Qwen3.8-Max（2026-08-03）**✱：2.4T 总参 / ~95B 激活、1M 上下文，主题 "Coding and Cowork"（07-19 WAIC 预览）；**08-12 史上首次开源 Max 级权重** Qwen3.8-2.4T-A95B，采用自定义许可（年营收 ≥5000 万美元需商业授权）——Apache 2.0 惯例的首次例外。
- **Qwen3.8-27B（2026-08 上旬开源，Apache 2.0）**✱：与 2.4T 同代的开源 dense 旗舰，HF 仓库 08-05 建立、08-13 补 FP8 版。**27B 参数 + 视觉编码器的原生多模态**（image-text-to-text，支持小时级视频理解），架构延续 Qwen3.5 混合注意力模板（64 层，"3×Gated DeltaNet → 1×门控注意力"循环堆叠）并训练 **MTP**；上下文 262K 原生、YaRN 扩展 1M。思考控制细化为 `reasoning_effort`（xhigh / medium / low）+ `preserve_thinking` 跨轮保留（Qwen3.6 机制延续）。基准：SWE-bench Pro **61.7**（Qwen3.6-27B 53.5、Qwen3.7-Plus 57.6）、DeepSWE 1.1 42.2、Terminal Bench 2.1 73.0（Opus 4.6 Max 78.2）、GPQA-Diamond 89.2、LiveCodeBench v6 90.3；视觉 agent：OSWorld-Verified 84.3 / AndroidWorld 81.9 / WebArena 64.8——当前 27B 级开源最强 agentic coding + GUI agent，上线一周 HF 已衍生 198 个量化版。暂无专用 GitHub 仓库（模型卡 + 官方博客 + ModelScope 渠道发布）。

---

## 二、多模态 / 专用模型专线

### 视觉理解线：Qwen-VL → 2-VL → 2.5-VL → 3-VL → 并入原生多模态

- **Qwen-VL（2023-08）**：三阶段训练、grounding + OCR。
- **Qwen2-VL（2024-08-29）**：[arXiv:2409.12191](https://arxiv.org/abs/2409.12191)，**Naive Dynamic Resolution**（任意分辨率动态 token）+ **M-RoPE**（多模态位置编码），统一图文/视频；72B 多模态比肩 GPT-4o。
- **Qwen2.5-VL（2025-01-26 开源，3B/7B/72B；3 月补 32B）**：[arXiv:2502.13923](https://arxiv.org/abs/2502.13923)。原生动态分辨率 ViT 从零训练（窗口注意力 + 少量全注意力层）、动态 FPS + 绝对时间编码对齐 mRoPE（1 小时长视频理解与秒级定位）、面向电脑/手机操作 Agent 与绝对坐标 grounding。
- **Qwen3-VL（2025-09-23 起分批开源：235B-A22B / 30B-A3B → dense 2B–32B 与 Thinking 版；TR [arXiv:2511.21631](https://arxiv.org/abs/2511.21631)）**：Interleaved-MRoPE（时空建模）+ **DeepStack**（多层 ViT 特征注入）+ 文本时间戳对齐；256K→1M 上下文，视觉 Agent（GUI 操作）、视觉转代码（Draw.io/HTML）、OCR 32 语。
- 2026 年主系列无新 VL 独立版本——视觉能力并入 Qwen3.5 原生多模态；1 月补 **Qwen3-VL-Embedding / Reranker**（[arXiv:2601.04720](https://arxiv.org/abs/2601.04720)，统一多模态检索排序）。
- 视觉推理：**QVQ-72B-Preview（2024-12-25）**✱ → **QVQ-Max（2025-03-28）**✱（图/视频推理 + 视觉 Agent）。

### 音频 / 全模态线：Audio → 2-Audio → 2.5-Omni → 3-Omni → TTS/ASR/音乐全栈

- **Qwen-Audio（2023-11）**：层级标签多任务预训练统一 30+ 音频任务；**Qwen2-Audio（2024-07）**：语音对话/音频分析双模式自动切换，SFT+DPO。
- **Qwen2.5-Omni-7B（2025-03-26）**：[arXiv:2503.20215](https://arxiv.org/abs/2503.20215)。端到端全模态输入 + 流式语音输出，**Thinker-Talker** 架构（Talker 可拆卸退化回 Qwen2.5）+ TMRoPE。
- **Qwen3-Omni-30B-A3B（2025-09-22）**：[arXiv:2509.17765](https://arxiv.org/abs/2509.17765)。Thinker-Talker MoE，多码本离散 codec + 轻量 ConvNet，首包延迟 234ms；36 项基准 32 项开源 SOTA，"全模态不牺牲单模态性能"。
- **Qwen3.5-Omni（2026-03-15 Flash / 03-30 Plus，仅 API）**：TR [arXiv:2604.15804](https://arxiv.org/abs/2604.15804)。Thinker/Talker 均为混合注意力 MoE，100 万+ 小时音视频训练，ARIA 组件动态对齐文本/语音 token；10 小时音频输入、400 秒 720P 视频。
- 2026 年语音全栈开源：**Qwen3-TTS（2026-01-22，[arXiv:2601.15621](https://arxiv.org/abs/2601.15621)）** 双轨 LM + 3 秒声音克隆、首包 97ms；**Qwen3-ASR（2026-01-29，[arXiv:2601.21337](https://arxiv.org/abs/2601.21337)）** 52 语言/方言 + 歌唱/BGM 一体识别；2026-07 音频三连——**Qwen-Music**（[arXiv:2607.11699](https://arxiv.org/abs/2607.11699)，高保真带人声完整歌曲生成）、**Qwen-Audio-VAE**（[arXiv:2607.11738](https://arxiv.org/abs/2607.11738)）、**Qwen-Audio-3.0-Gen-Preview**（[arXiv:2607.27011](https://arxiv.org/abs/2607.27011)，DiT + 共享 VAE 的非自回归音频生成）。更早的闭源 API：Qwen-TTS（2025-06）→ Qwen3-TTS-Flash（2025-09）。

### 代码线：CodeQwen1.5 → Qwen2.5-Coder → Qwen3-Coder → Coder-Next

- **CodeQwen1.5-7B（2024-04）**✱ → **Qwen2.5-Coder（2024-09~11 全家族 0.5B–32B，[arXiv:2409.12186](https://arxiv.org/abs/2409.12186)）** → **Qwen3-Coder-480B-A35B / 30B-A3B（2025-07，无论文）** → **Qwen3-Coder-Next 80B-A3B（2026-02-02，[arXiv:2603.00729](https://arxiv.org/abs/2603.00729)）**：358 种编程语言、可验证编码任务大规模合成 + 可执行环境 RL、SWE-bench Verified ~70.6%。CLI 工具线见 §三 Qwen Code。

### 图像生成线：VLo → Qwen-Image → 2.0

- **Qwen VLo（2025-06-26）**✱：API 文生图/编辑。**Qwen-Image 20B（2025-08-04，[arXiv:2508.02324](https://arxiv.org/abs/2508.02324)）**：MMDiT、双流文本编码（Qwen2.5-VL 字符级 + CLIP-L 语义），中文长文本渲染与海报排版为招牌；同报告覆盖 **Qwen-Image-Edit（08-19）**，9 月升级 **Edit-2509**（多图一致性编辑）。**Qwen-Image-2.0（2026-02-10）**✱：千 token 级指令生成信息图/PPT/漫画、原生 2K，未见开放权重。
- 兄弟团队通义万相 **Wan**：Wan2.1（2025-02-25，[arXiv:2503.20314](https://arxiv.org/abs/2503.20314)，开源 SOTA 文/图生视频）→ Wan2.2（2025-07-28，首批开源 MoE 视频生成）→ Wan2.7-Image（2026-04）→ **Wan 3.0（2026-08-06 公测，原生 30 秒视频 + Omni-Reference）**。

### 检索 / 嵌入线

- **gte 系列**（Alibaba-NLP，gte-Qwen2/Qwen2.5 底座）→ **Qwen3-Embedding / Reranker（2025-06-05，[arXiv:2506.05176](https://arxiv.org/abs/2506.05176)）**：0.6B–8B 指令感知 + MRL 灵活维度，多语 MTEB 登顶 → **Qwen3-VL-Embedding / Reranker（2026-01-08，[arXiv:2601.04720](https://arxiv.org/abs/2601.04720)）**：文本/图像/截图/视频统一多模态检索。

### Agent / 具身研究线（2026 集中开源，QwenLM 仓库）

- **Qwen-UI-Agent（2026-07-30，[arXiv:2607.28227](https://arxiv.org/abs/2607.28227)）**：面向真实设备的基础 GUI Agent（跨平台工作流、GUI+CLI 混合执行、长程任务）。
- 2026 上半年研究仓库：WebWorld（02）、Qwen-VLA（05）、Qwen-RobotManip（06）、Qwen-RobotNav（06）、Qwen-AgentWorld"语言世界模型"（07）——具身/环境智能方向铺开；另有 **Qwen-MM-Plugins**（2026-08-13，让任意 Agent harness 多模态原生化）。

---

## 三、开源工具与生态

### GitHub 组织 QwenLM（约 50 仓库，"滚动改名"传统）

- 主模型仓库随代际改名复用：Qwen → Qwen2 → Qwen2.5 → **Qwen3**（同一仓库）；Qwen2-VL → Qwen2.5-VL → **Qwen3-VL**；Qwen3-Next → **Qwen3.6**（旧链接自动重定向）。主力仓库：Qwen3（27.5k★）、Qwen3-VL（19.8k★）、Qwen3-Coder（16.8k★）、Qwen-Image（8.2k★）、Qwen3-Omni（4.2k★）。
- 研究向新仓库（2026）：Qwen3-TTS、Qwen3-ASR、Qwen3-VL-Embedding、Qwen-MM-Plugins、FlashQLA（线性注意力内核）、Qwen-VLA / RobotManip / RobotNav / AgentWorld / WebWorld 等。

### 官方工具

- **Qwen-Agent（2023-09-22 首发随 Qwen-14B，17k★，Apache 2.0）**：官方 Agent 框架（pip `qwen-agent`）——Function Calling（并行）、MCP、Docker 沙箱代码解释器、百万上下文 RAG、Chrome 扩展 BrowserQwen、Gradio GUI；**Qwen Chat 的后端框架**。
- **Qwen Code（2025-06-26 创建，27k★，Apache 2.0）**：终端 AI 编码代理，fork 自 Gemini CLI 起家、v0.1 后独立演进；SubAgents/Agent Teams、Auto-Memory、Auto-Skills、hooks、MCP、Plan Mode、LSP、沙箱、Git worktree；多协议（OpenAI/Anthropic/Gemini/Qwen + 本地 Ollama/vLLM）；形态含 TUI、VS Code/JetBrains/Zed 插件、桌面端、daemon 与 SDK。截至 2026-08 无 2.0，稳定版 v0.21.x（nightly 高频发布）；配套 qwen-code-action（GitHub Action）。
- **训练 / 评测栈（modelscope 组织，官方推荐路径）**：**ms-swift**（15.2k★，AAAI 2025；600+ LLM 的 CPT/SFT/DPO/GRPO、LoRA/全参、Megatron/DeepSpeed/FSDP、vLLM/SGLang 部署与量化，v4.x 已支持 Qwen3.6）；**EvalScope**（3.2k★，评测 + 推理压测一站式，Qwen 各模型 README 引用）；**ChatLearn**（阿里对齐/RL 训练框架，600B+ GRPO/GSPO，2025-10 后不活跃）；**AgentScope**（阿里系多智能体框架，2.0）。
- **ModelScope（魔搭）**：阿里 2022 年推出的模型社区（国内 HF 对标），Qwen 国内权重分发主渠道。

### 分发与许可

- **HF 组织 [Qwen](https://huggingface.co/Qwen)**：HF 下载量最大的模型组织之一（第三方报告月下载 ~399M 居第一）；2025 年公开报道衍生模型数超 10 万、超越 Llama 系。
- **许可演进**：Tongyi Qianwen LICENSE（2023 Qwen1/VL，商用需申请）→ **Qwen1.5 起开放权重主力转 Apache 2.0**（Qwen2/2.5/3/3.5/3.6 一以贯之，"All our open-weight models are licensed under Apache 2.0"）→ 唯一例外：**Qwen3.8-2.4T-A95B（2026-08-12）自定义许可**（年营收 ≥5000 万美元需商业授权）；同代开源的 Qwen3.8-27B 仍为 Apache 2.0。

### API 平台与产品（非开源）

- **DashScope / 阿里云百炼 Model Studio**：OpenAI 兼容接口售卖 Qwen-Max/Plus/Turbo 与 Wan 系列；**qwen.ai**（官网 + API 平台 + 博客）、**chat.qwen.ai**（Qwen Chat，Qwen-Agent 后端）。产品侧：2026-01-15 Qwen App 接入阿里生态 Agent 操作（点外卖/叫车/发红包）；**2026-07-16 Apple Intelligence 中国区获批（与阿里/Qwen 合作）**。

---

## 四、技术演进主线

- **架构**：dense + GQA（Qwen1/1.5）→ 首个 MoE 57B-A14B（Qwen2）→ 大型 MoE 常态化（235B-A22B → 480B-A35B → 397B-A17B）→ **门控注意力 + Gated DeltaNet 混合架构 + 超稀疏 MoE**（Qwen3-Next，2025-09）成为 3.5/3.6/Coder-Next 的模板 → 2.4T-A95B（Qwen3.8）
- **后训练**：SFT/DPO → 大规模结果奖励 RL（QwQ 两阶段）→ 四阶段"冷启动-融合"后训练（Qwen3）→ 课程式 Agent RL + 执行反馈 Code RL + 万级并行环境（Qwen3-Coder）→ 长程自主 RL（Qwen3.7-Max "35 小时"）
- **上下文**：8K（Qwen1）→ 128K（Qwen2/2.5，YaRN）→ 256K 原生 + 1M 外推（Qwen3/3-Coder）→ 1M 原生（Qwen3.7/3.8-Max）
- **多模态**：外挂 ViT（Qwen-VL）→ 动态分辨率 + M-RoPE（Qwen2-VL/2.5-VL）→ Interleaved-MRoPE + DeepStack（Qwen3-VL）→ **原生早期融合**（Qwen3.5，视觉并入主基座）；语音侧 Thinker-Talker 贯穿 Omni 系并长成 TTS/ASR/音乐全栈
- **开源策略**：Tongyi 许可 → Apache 2.0 全谱系（0.8B–397B）→ HF 第一大模型组织、衍生模型超 Llama；"滚动改名"复用仓库 + ms-swift/EvalScope 官方工具链 + vLLM/SGLang 生态同步；Max 旗舰长期闭源走 API，至 Qwen3.8（2026-08）首次开放权重（附营收门槛许可）
- **定位迁移**：对话模型（2023）→ 全尺寸家族 + 专项线（2024）→ 混合思考 + 推理（2025 上半年）→ Agentic Coding（2025-07）→ 原生多模态 Agent 与长程自主（2026）
