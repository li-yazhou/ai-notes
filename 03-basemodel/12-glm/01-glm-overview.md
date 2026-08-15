---
type: overview
title: "GLM 基础模型与开源工具总览（时间线）"
created: 2026-08-15
updated: 2026-08-15
status: active
tags:
  - vendor/glm
  - paper/foundation-model
  - paper/release
  - tool/open-source
---

# GLM 基础模型与开源工具总览（时间线）

> 范围：清华 KEG × 智谱 AI（Zhipu AI，国际品牌 **Z.ai**）官方发布的 **GLM 系列模型**（GLM / ChatGLM / GLM-4 / Z1 / GLM-4.5 ~ 4.7 / GLM-5.x / OCR / TTS / ASR / V 系视觉）与**多模态产品线**（CodeGeeX / CogVLM / CogAgent / CogView / CogVideo）及 **GitHub 开源生态**（THUDM → zai-org 两大组织），按发布时间排序
> 信息来源：arXiv 官方页面、[Z.ai Release Notes](https://docs.z.ai/release-notes/new-released)、[zai-org GitHub](https://github.com/zai-org)、[THUDM GitHub](https://github.com/THUDM)；标 ✱ 的条目为无论文发布（模型卡 / 博客 / API 公告）
> 关联：[[2607-arxiv-llms]]（月度厂商 digest，GLM 新论文按月收录）、[[01-deepseek-overview]]（姊妹篇：DeepSeek 时间线）

---

## 〇、一页时间线

| 时间 | 发布物 | 论文 / 来源 | 一句话要点 |
| --- | --- | --- | --- |
| 2021-03 | **GLM** 预训练框架 | [arXiv:2103.10360](https://arxiv.org/abs/2103.10360)（ACL 2022） | 自回归空白填充（autoregressive blank infilling）统一自编码/自回归范式，GLM 全系起点 |
| 2021-05 | CogView 4B | [arXiv:2105.13290](https://arxiv.org/abs/2105.13290)（NeurIPS 2021） | 首个大规模中文文生图（VQ-VAE + Transformer），Cog 生成线起点 |
| 2022-05 | CogVideo 9.4B | [arXiv:2205.15868](https://arxiv.org/abs/2205.15868)（ICLR 2023） | 首批开源大规模文生视频模型（基于 CogView2） |
| 2022-08 | **GLM-130B** | [arXiv:2210.02414](https://arxiv.org/abs/2210.02414)（ICLR 2023） | 130B 双语 dense 模型，权重与训练细节全公开，早于 LLaMA 的"透明百亿级"尝试 |
| 2022-09 | CodeGeeX 13B | [arXiv:2303.17568](https://arxiv.org/abs/2303.17568)（KDD 2023） | 22 种语言代码生成模型 + IDE 插件，代码线起点 |
| 2023-03-14 | **ChatGLM-6B** ✱ | [GitHub](https://github.com/zai-org/ChatGLM-6B)（41k★） | 62 亿双语对话模型，消费级显卡（INT4 约 6GB）可跑，国产开源 LLM 时代开启 |
| 2023-03 | VisualGLM-6B ✱ | [GitHub](https://github.com/zai-org/VisualGLM-6B) | ChatGLM-6B + 视觉编码的多模态对话初代 |
| 2023-06-25 | ChatGLM2-6B ✱ | [GitHub](https://github.com/zai-org/ChatGLM2-6B) | 上下文 8K→32K、推理提速 42%，C-Eval 一度登顶 |
| 2023-07 | CodeGeeX2-6B ✱ | [GitHub](https://github.com/zai-org/CodeGeeX2) | 基于 ChatGLM2 架构的代码模型 |
| 2023-10-25 | ChatGLM3-6B ✱ | [GitHub](https://github.com/zai-org/ChatGLM3)（14k★） | 原生工具调用 / 代码解释器 / Agent 任务，chat 模型即智能体雏形 |
| 2023-11 | CogVLM 17B/19B | [arXiv:2311.03079](https://arxiv.org/abs/2311.03079) | **视觉专家**（Visual Expert）架构：冻结 LLM、注入可训练视觉模块 |
| 2023-12 | CogAgent 18B | [arXiv:2312.08914](https://arxiv.org/abs/2312.08914) | GUI Agent VLM，高分辨率截图理解，CogAgent-9B 后续开源 |
| 2024-01-16 | **GLM-4**（API）✱ | [官方发布](https://docs.z.ai/release-notes/new-released) | GLM-4 / GLM-4V / GLM-4-All Tools，中文基准整体对标 GPT-4 |
| 2024-03 | CogView3 | [arXiv:2403.05121](https://arxiv.org/abs/2403.05121)（ECCV 2024） | Relay Diffusion（中继扩散），更细更快 |
| 2024-06-05 | **GLM-4-9B**（开源） | [arXiv:2406.12793](https://arxiv.org/abs/2406.12793)（06-18，家族综述） | 9B 对标 GPT-3.5-turbo；另有 1M 上下文版 GLM-4-9B-Chat-1M |
| 2024-08 | GLM-4-Plus / GLM-4-Long ✱ | API 公告 | API 旗舰模型；1M 长文本模型 |
| 2024-08 | CogVideoX 2B/5B | [arXiv:2408.06072](https://arxiv.org/abs/2408.06072) | 3D 全注意力专家 Transformer 文生视频；11 月迭代 CogVideoX1.5-5B |
| 2024-10 | **AutoGLM**（研究预览） | [arXiv:2411.00820](https://arxiv.org/abs/2411.00820) | 手机 / 网页 GUI 基础智能体（Phone / Web），AndroidLab 36.2%、中文常用 App 89.7% |
| 2024-10 | GLM-4-Voice 9B（开源） | [arXiv:2412.02612](https://arxiv.org/abs/2412.02612) | 端到端中英语音对话，免 ASR/TTS 级联，情感/语速可控 |
| 2025-02 | CogView4-6B ✱ | [HF](https://huggingface.co/zai-org/CogView4-6B) | 支持中文字符渲染的开放文生图 |
| 2025-03-31 | AutoGLM 沉思 ✱ | 产品发布 | 免费深度研究智能体（搜索-推理-反思迭代），Z1-Rumination 支撑 |
| 2025-04-14 | **GLM-4-32B-0414 / GLM-Z1 系列**（MIT）✱ | [GitHub](https://github.com/zai-org/GLM-4) | 15T token 的 32B；Z1 推理版（RL 延伸）对标 o1，Z1-Rumination 对标 Deep Research |
| 2025-07-28 | **GLM-4.5 / 4.5-Air** | [arXiv:2508.06471](https://arxiv.org/abs/2508.06471) | 355B-A32B / 106B-A12B MoE，ARC（Agentic/Reasoning/Coding）融合模型；23T token |
| 2025-08-08 | GLM-4.1V-9B-Thinking | [arXiv:2507.01006](https://arxiv.org/abs/2507.01006) | 9B 视觉推理，scalable RL + CoT，9B 级对标闭源大杯 VLM |
| 2025-08-11 | **GLM-4.5V** ✱ | [HF 模型卡](https://huggingface.co/zai-org/GLM-4.5V) | 106B-A12B VLM（基于 4.5-Air），41 项基准开源同档 SOTA；FP8 版；vLLM 官方支持 |
| 2025-09-30 | **GLM-4.6**（MIT）✱ | [HF 模型卡](https://huggingface.co/zai-org/GLM-4.6) | 357B-A32B，上下文 128K→**200K**，真实编码增强（CC-Bench token −15%） |
| 2025-12-08 | GLM-4.6V + **Open-AutoGLM** ✱ | [GLM-V 仓库](https://github.com/zai-org/GLM-V) / [Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM) | 128K 视觉推理 VLM；**开源手机智能体框架**（可下载模型 + ADB 操作，26k★） |
| 2025-12-10 | GLM-ASR-2512 ✱ | [GitHub](https://github.com/zai-org/GLM-ASR) | 1.5B 开源 ASR，CER 0.0717，自定义词典/术语 |
| 2025-12 | GLM-TTS | [arXiv:2512.14291](https://arxiv.org/abs/2512.14291) | 多奖励 RL 的零样本可控情感 TTS |
| 2025-12-11 | AutoGLM-Phone-Multilingual ✱ | API 公告 | ADB 手机自动化，50+ App，中英双语 |
| 2025-12-22 | **GLM-4.7**（MIT）✱ | [HF 模型卡](https://huggingface.co/zai-org/GLM-4.7) | 约 357B MoE，agentic coding + 多步推理强化；发布时为开源权重智能指数第一（Artificial Analysis v4.0） |
| 2026-01-14 | GLM-Image ✱ | [GitHub](https://github.com/zai-org/GLM-Image) | 自回归 × 扩散混合文生图，**国产芯片训练**，图内文字渲染强 |
| 2026-01-19 | GLM-4.7-Flash（MIT）✱ | [Z.ai Release Notes](https://docs.z.ai/release-notes/new-released) | 30B-A3B 轻量免费档，低延迟高吞吐 |
| 2026-02-03 | GLM-OCR ✱ | [GitHub](https://github.com/zai-org/GLM-OCR)（7.3k★） | CogViT + GLM-0.5B 编码器-解码器，"Accurate × Fast × Comprehensive" 紧凑 OCR |
| 2026-02-11 | **GLM-5** | [arXiv:2602.15763](https://arxiv.org/abs/2602.15763) | 744B-A~42B，28.5T token，200K 上下文；"From Vibe Coding to Agentic Engineering"，Chat + Agent 双模式 |
| 2026-03-15 | GLM-5-Turbo ✱ | API 公告 | 高吞吐长链 Agent 任务，Skills 集成、复杂指令分解 |
| 2026-04-01 | GLM-5V-Turbo | [arXiv:2604.26752](https://arxiv.org/abs/2604.26752) | 面向视觉编码与 GUI Agent 工作流的原生多模态 |
| 2026-04-07 | **GLM-5.1** ✱ | [Z.ai Release Notes](https://docs.z.ai/release-notes/new-released) | 单次自主运行最长 **8 小时**，对标 Claude Opus 4.6，开源 |
| 2026-06-13 | **GLM-5.2**（MIT）✱ | [Z.ai 博客](https://z.ai/blog/glm-5.2) | ~744B，**1M 无损上下文**，可调思考力度（high/max），长时程编码旗舰 |
| 2026-08 | **GLM-5.3**（官宣/预览）✱ | [Z.ai Docs 模型页](https://docs.z.ai/guides/llm/glm-5.3) | 1M 输入 / 128K 输出；Z.ai Code Bench 编码较 5.2 **+~50%**，主打长时程工程与**网络安全**（CyberGym 84.5%） |

---

## 一、语言模型主线

### 1. 2021 ~ 2022：预训练范式与百亿级透明化

- **GLM（2021-03）**：论文 [GLM: General Language Model Pretraining with Autoregressive Blank Infilling](https://arxiv.org/abs/2103.10360)（ACL 2022，杜政晓/唐杰团队）。用"自回归空白填充"统一 BERT 式自编码与 GPT 式自回归预训练，兼顾理解与生成，是后来所有 GLM 模型的架构与名字来源。
- **GLM-130B（2022-08 权重开放，论文 10 月）**：论文 [GLM-130B: An Open Bilingual Pre-trained Model](https://arxiv.org/abs/2210.02414)（ICLR 2023）。130B 中英双语 dense 模型，早于 LLaMA 公开百亿级权重，并完整披露训练稳定性设计（BF16 混合精度、梯度范数监测等），成为早期开源社区最重要的中文底座之一。

### 2. 2023：ChatGLM 三代——国产开源对话模型的起点

- **ChatGLM-6B（2023-03-14）**✱：基于 GLM-130B 同源架构缩至 62 亿，双语对话微调；INT4 量化约 6GB 显存即可本地部署，GitHub 41k star，是 2023 年中文开源社区最热的模型。
- **ChatGLM2-6B（2023-06-25）**✱：上下文 8K→32K、推理提速 42%、许可更开放（含商用），C-Eval 中文能力一度登顶。
- **ChatGLM3-6B（2023-10-25）**✱：原生支持**工具调用（Function Call）、代码解释器、Agent 任务**，把"chat 模型即智能体执行器"做进开源权重；同期的 CodeGeeX2-6B（2023-07）把代码线切到 ChatGLM2 架构上。
- 这三代均无论文，官方技术细节后收录于 2024 年的家族综述（见下）。

### 3. 2024：GLM-4 登场，All Tools 与多模态并举

- **GLM-4（2024-01-16，API）**✱：GLM-4 / GLM-4V（视觉）/ **GLM-4-All Tools**（自主调用联网、绘图、代码解释器的智能体模式）三线齐发，中文基准整体对标 GPT-4。
- **GLM-4-9B（2024-06-05 开源）**：家族综述论文 [ChatGLM: A Family of Large Language Models from GLM-130B to GLM-4 All Tools](https://arxiv.org/abs/2406.12793)（2024-06-18）系统复盘 GLM-130B→ChatGLM 1/2/3→GLM-4 的预训练、对齐（RLHF/自蒸馏）与 All Tools 技术；GLM-4-9B 对标 GPT-3.5-turbo，另发布 1M 上下文的 GLM-4-9B-Chat-1M。
- **GLM-4-Plus / GLM-4-Long（2024-08，API）**✱：API 旗舰与 1M 长文本模型。
- **GLM-4-Voice（2024-10 开源，9B）**：论文 [GLM-4-Voice: Towards Intelligent and Human-Like End-to-End Spoken Chatbot](https://arxiv.org/abs/2412.02612)。端到端语音对话（直接理解/生成语音 token，不经 ASR-TTS 级联），可按指令调整情感、语调、语速。
- **GLM-Edge 系列（2024 年末）**：1.5B/4B/9B 端侧小模型（GitHub zai-org/GLM-Edge）。

### 4. 2025-04：0414 系列与 Z1——推理与沉思

- **GLM-4-32B-0414 系列（2025-04-14，MIT）**✱：15T token 预训练的 32B 开源家族——基座 / Chat / 推理（GLM-Z1-32B-0414，冷启动 + 延伸 RL，数学与复杂问题求解对标 o1）/ **GLM-Z1-Rumination-32B-0414**（带搜索的"沉思"深度研究模型，对标 Deep Research）；随后补充 9B 版本。无论文，官方以博客 + 仓库说明发布。
- **AutoGLM 沉思（2025-03-31 上线）**✱：面向 C 端的免费深度研究智能体，搜索-推理-反思迭代求解开放问题，即 Z1-Rumination 的产品化。

### 5. 2025-07 ~ 12：GLM-4.5 世代——ARC 融合与开源最强编码线

- **GLM-4.5 / GLM-4.5-Air（2025-07-28；Air 权重 08-12）**：论文 [GLM-4.5: Agentic, Reasoning, and Coding (ARC) Foundation Models](https://arxiv.org/abs/2508.06471)。355B-A32B / 106B-A12B MoE，23T token 预训练；核心理念是把 **Agentic、Reasoning、Coding 三能力融进一个模型**（单模型可开/关思考模式），TAU-Bench 70.1、AIME24 91.0；MIT 开源，vLLM/SGLang 生态当天跟进。
- **GLM-4.6（2025-09-30，MIT）**✱：357B-A32B，上下文 128K→**200K**；面向真实编码场景（Claude Code 兼容），CC-Bench 较 4.5 省 ~15% token，成为开源编码模型的性价比标杆。
- **GLM-4.7（2025-12-22，MIT）**✱：约 357B MoE，agentic coding 与多步推理进一步强化，发布时为 Artificial Analysis Intelligence Index v4.0 **开源权重第一**；次日配套 **GLM-4.7-Flash**（2026-01-19，30B-A3B，免费档）。
- 语音/OCR/图像多模态同期密集开源，见 §二。

### 6. 2026：GLM-5 世代——Agentic Engineering 与 1M 上下文

- **GLM-5（2026-02-11）**：论文 [GLM-5: from Vibe Coding to Agentic Engineering](https://arxiv.org/abs/2602.15763)。744B 总参 / ~42B 激活 MoE，预训练 23T→**28.5T token**，200K 上下文；主题是把"氛围编程"（vibe coding）升级为**智能体工程**（agentic engineering）：Chat + Agent 双模式、长链工具编排、真实软件工程基准开源 SOTA；官方 release notes 称引入稀疏注意力优化 token 效率。
- **GLM-5-Turbo（2026-03-15）**✱：高吞吐长链 Agent 专用，Skills 集成与复杂指令分解。
- **GLM-5V-Turbo（2026-04-01）**：论文 [arXiv:2604.26752](https://arxiv.org/abs/2604.26752)，原生多模态（视觉编码 / GUI Agent 工作流）。
- **GLM-5.1（2026-04-07，开源）**✱：主打长时程自主性——**单次运行最长 8 小时**，官方对标 Claude Opus 4.6。
- **GLM-5.2（2026-06-13，MIT）**✱：~744B，**1M 无损上下文** + 可调思考力度（high / max 两档），针对长时程任务的上下文漂移与目标遗忘优化；发布时未附官方基准，引发社区讨论，随后开源权重。
- **GLM-5.3（2026-08 官宣，截至 08-15 预览中）**✱：官方 docs 已上线模型页（[docs.z.ai/guides/llm/glm-5.3](https://docs.z.ai/guides/llm/glm-5.3)）——1M 输入 / 128K 输出，纯文本 I/O，支持思考模式、函数调用、上下文缓存、结构化输出与 MCP；官方称 Z.ai Code Bench 编码较 5.2 提升 ~50%，并公布 Terminal-Bench 3.0 28.3、DeepSWE v1.1 66.9、Agents' Last Exam 28.5、**CyberGym 84.5%、ExploitBench 54.4%**，主打长时程工程、agent 工作流与**网络安全**（漏洞发现、代码审查）；API 标注 "coming soon"，GLM Coding Plan 订阅用户先行；暂无论文、权重未开放（GLM-5 仓库与官方 release notes 尚未收录），正式发布后待更新本条。

---

## 二、多模态 / 语音 / 生成 / 代码专线

### 视觉理解线：VisualGLM → CogVLM → CogAgent → GLM-4.xV

- **VisualGLM-6B（2023-03）**✱：ChatGLM-6B + ViT 的初代多模态对话。
- **CogVLM（2023-11）**：论文 [CogVLM: Visual Expert for Pretrained Language Models](https://arxiv.org/abs/2311.03079)。**视觉专家**架构——冻结 LLM 权重、在每层注入可训练视觉模块，17B/19B 在当年刷屏多项多模态基准；后续 **CogVLM2**（2024，Llama3-8B 底座）与 CogVLM2-Video。
- **CogAgent（2023-12）**：论文 [CogAgent: A Visual Language Model for GUI Agents](https://arxiv.org/abs/2312.08914)。18B 高分辨率（1120×1120）截图理解，专为 GUI 操作智能体设计，后迭代开源 CogAgent-9B。
- **GLM-4V / GLM-4V-9B（2024）**：GLM-4 系视觉版（含 2024-06 开源的 GLM-4V-9B-Flash）。
- **GLM-4.1V-9B-Thinking（2025-08-08）**：论文 [GLM-4.1V-Thinking: Towards Versatile Multimodal Reasoning with Scalable Reinforcement Learning](https://arxiv.org/abs/2507.01006)（07-01 挂出）。9B 级视觉推理，用**可扩展 RL + CoT 范式**统一图像推理 / GUI Agent / 视频理解 / 视觉定位 / 空间认知。
- **GLM-4.5V（2025-08-11）**✱：106B-A12B（基于 GLM-4.5-Air 底座），官方称 41 项基准开源同档 SOTA；提供 FP8 权重，08-19 获 vLLM 官方支持。
- **GLM-4.6V（2025-12-08）**✱：视觉推理 + **128K 上下文**，与 Open-AutoGLM 同日发布。

### 语音线：4-Voice → ASR → TTS

- **GLM-4-Voice（2024-10，9B）**：端到端中英语音对话（arXiv:2412.02612，见 §一）。
- **GLM-ASR-2512（2025-12-10，1.5B）**✱：开源 ASR，CER 0.0717，支持自定义词典与专业术语。
- **GLM-TTS（2025-12）**：论文 [GLM-TTS Technical Report](https://arxiv.org/abs/2512.14291)。生产级零样本 TTS，多奖励 RL 对齐，情感表达与韵律可控。

### 生成线：CogView / CogVideo / GLM-Image

- **CogView（2021，NeurIPS）**：4B VQ-VAE + Transformer，首个大规模中文文生图；**CogView2**（[arXiv:2204.14217](https://arxiv.org/abs/2204.14217)，层级 Transformer）；**CogView3 / 3-Plus**（[arXiv:2403.05121](https://arxiv.org/abs/2403.05121)，ECCV 2024，Relay Diffusion）；**CogView4-6B（2025-02）**✱ 支持中文字符渲染。
- **CogVideo（2022-05，ICLR 2023）**：9.4B 文生视频；**CogVideoX（2024-08）**：论文 [CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072)，3D 全注意力专家 Transformer，2B/5B 开源；CogVideoX1.5（2024-11）→ **CogVideoX-3（2025-07-15）**✱ 增加首尾帧生成。配套 **ImageReward / VisionReward** 人类偏好奖励模型（NeurIPS 2023 / AAAI 2026）。
- **GLM-Image（2026-01-14）**✱：自回归 × 扩散混合的文生图，**在国产芯片上训练**，图内中英文字渲染是其招牌能力。

### 代码线：CodeGeeX → 融入主线

- **CodeGeeX（2022-09，13B）**：22 种语言代码预训练 + IDE 插件（KDD 2023）；**CodeGeeX2-6B（2023-07）** 基于 ChatGLM2；**CodeGeeX4-ALL-9B（2024-07）**✱ 面向 AI 软件开发全场景（代码补全/问答/生成）。此后代码能力并入 GLM-4.5→4.6→4.7→GLM-5 主线（Z.ai 主打"Coding Plan"，深度接入 Claude Code / Cline / Kilo Code 等编码智能体）。

---

## 三、Agent 与开源工具生态（THUDM → zai-org）

### AutoGLM：从论文到开源手机智能体

- **AutoGLM（2024-10-25 研究预览）**：论文 [AutoGLM: Autonomous Foundation Agents for GUIs](https://arxiv.org/abs/2411.00820)。ChatGLM 家族的 GUI 基础智能体系列（Phone / Web），AndroidLab 36.2%、中文常用 App 任务 89.7% 成功率。
- **AutoGLM 沉思（2025-03-31）**✱：免费深度研究智能体产品。
- **Open-AutoGLM（2025-12-08 开源）**✱：[zai-org/Open-AutoGLM](https://github.com/zai-org/Open-AutoGLM)（26k★）——**可下载模型的开放手机智能体框架**：多模态理解屏幕 + ADB 自动操作，唐杰称历时 32 个月；配套 **AutoGLM-Phone-Multilingual**（2025-12-11，50+ App 中英双语）。

### 开源仓库组织（GitHub）

- **THUDM**（清华 KEG，早期仓库）：GLM-130B、ChatGLM-6B/2/3、CodeGeeX 1/2、CogVLM/CogView/CogVideo 等。
- **zai-org**（智谱官方，现主组织，51+ 仓库）：模型仓库 **GLM-4 / GLM-4.5 / GLM-V（4.1V-Thinking·4.5V·4.6V）/ GLM-5 / GLM-OCR / GLM-TTS / GLM-ASR / GLM-Image / GLM-Edge**；生成线 CogVideo / CogView4 / RealVideo / Kaleido / SCAIL（CVPR 2026 Findings）/ Inf-DiT / RelayDiffusion。
- **开发工具**：
  - [GLM-4 仓库](https://github.com/zai-org/GLM-4)（7.1k★）：GLM-4 / 9B / 0414 / Z1 系列的权重入口 + 微调与推理（vLLM 等）指引；
  - **GLM-skills**：GLM 家族官方 skills 集合；**zai-coding-plugins**：Claude Code 插件市场（GLM Coding Plan 生态）；**Synapse**：自托管 AI 工作台（队友/记忆/MCP）。
- **评测基准**：glm-simple-evals（GLM-4.5 系评测）、LVBench（超长视频理解，ICCV 2025）、MotionBench（CVPR 2025）、ComplexFuncBench（复杂函数调用）、AISE-Bench / RPC-Bench / SurveyReview（KDD/ACL 2026）；早期 THUDM 的 **AgentBench**（[arXiv:2308.03688](https://arxiv.org/abs/2308.03688)）、**AgentTuning**（[arXiv:2310.12823](https://arxiv.org/abs/2310.12823)）、**LongBench**（[arXiv:2308.14586](https://arxiv.org/abs/2308.14586)）至今仍是 agent / 长文本评测的通用底座。
- **权重与许可**：HF 组织 [zai-org](https://huggingface.co/zai-org)；GLM-4.5 起主力模型均为 **MIT**（早期 ChatGLM-6B 为自定义许可，CogVLM/CodeGeeX 为 Apache-2.0 系）。

---

## 四、技术演进主线

- **架构**：自回归空白填充（GLM 2021）→ 130B dense 透明训练（GLM-130B）→ 对话化开源（ChatGLM 三代）→ 工具调用原生（GLM-4 / All Tools）→ MoE + 可开关思考（GLM-4.5）→ 200K/1M 长上下文（4.6 → 5.2）+ 稀疏注意力提效（GLM-5）
- **后训练**：RLHF → 冷启动 + 延伸 RL（Z1）→ 大规模可扩展 RL（4.1V-Thinking / GLM-4.5）→ 长时程自主 RL（GLM-5.1"8 小时"）
- **定位迁移**：对话模型（2023）→ All Tools（2024-01）→ GUI Agent（AutoGLM）→ **ARC 融合**：Agentic × Reasoning × Coding（GLM-4.5）→ Agentic Engineering / 长时程工程智能体（GLM-5 → 5.1 → 5.2）
- **多模态全覆盖**：理解（CogVLM→4.5V→4.6V→5V-Turbo）、语音（4-Voice/ASR/TTS 全链路开源）、生成（CogView/CogVideo→GLM-Image，国产芯片训练）
- **生态策略**：早期靠 6B 级开源占领社区（41k★），后期以 MIT 权重 + Claude Code/Cline 等编码智能体接入 + vLLM/SGLang day-0 支持 + 官方插件市场（zai-coding-plugins / GLM-skills）构筑开发者生态；GitHub 组织从 THUDM 平移至 zai-org
