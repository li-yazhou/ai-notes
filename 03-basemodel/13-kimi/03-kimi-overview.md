---
type: overview
title: "Kimi（月之暗面 / Moonshot AI）模型与开源工具总览（时间线）"
created: 2026-08-15
updated: 2026-08-15
status: active
tags:
  - vendor/kimi
  - paper/foundation-model
  - paper/release
  - tool/open-source
---

# Kimi（月之暗面 / Moonshot AI）模型与开源工具总览（时间线）

> 范围：月之暗面（Moonshot AI）官方发布的**模型**（Kimi 助手 / k0-math / k1.5 / Kimi-VL / Kimi-Audio / Kimina-Prover / Kimi-Dev / K 系列）与**开源工具**（Muon / Moonlight / Mooncake / Kimi Code CLI 等），按发布时间排序
> 信息来源：arXiv 官方页面、[Hugging Face moonshotai](https://huggingface.co/moonshotai)、[GitHub MoonshotAI](https://github.com/MoonshotAI)、[Kimi 开放平台 changelog](https://platform.kimi.com/blog/posts/changelog)；标 ✱ 的条目为无论文发布（模型卡 / 官方博客 / 产品公告）
> 关联：[[2607-arxiv-llms]]（月度厂商 digest，Kimi 新论文按月收录）、[[01-deepseek-overview]]（同类厂商总览）

---

## 〇、公司背景（一页）

- **2023-03 成立**：北京月之暗面科技有限公司，创始人杨植麟（Transformer-XL / XLNet 作者）、周昕宇、吴育昕等清华系团队；公司名取自 Pink Floyd 专辑《The Dark Side of the Moon》（发布 50 周年之际）。
- **融资线**：2024-02 阿里领投约 10 亿美元（估值 ~$2.5B）→ 2024-08 腾讯 + 高榕 ~$3 亿（~$3.3B）→ 2025-10 IDG 领投 ~$6 亿（投前 ~$3.8B）；2026-03 传筹划港股 IPO。
- **"Kimi 时刻"**：2025-07 K2 开源次日登顶 Hugging Face 下载榜，Nature News（643: 889–890）称其为 "another DeepSeek moment"。

---

## 一、一页时间线

| 时间 | 发布物 | 论文 / 来源 | 一句话要点 |
| --- | --- | --- | --- |
| 2023-10-09 | Kimi 智能助手 | 产品 | 国内首批 ToC 助手，主打 20 万字长文本 |
| 2024-03-18 | 200 万字无损上下文 | 产品 | 长文本 10× 扩展引发国内"长文本大战"；三天后因流量激增宕机，长文本算力瓶颈成名案例 |
| 2024-06 | **Mooncake**（服务 infra） | [arXiv:2407.00079](https://arxiv.org/abs/2407.00079)（FAST'25 最佳论文） | KVCache 为中心的解耦服务架构，Kimi 生产线（日处理 ~100B token） |
| 2024-10-11 | Kimi 探索版 | 产品 | AI 自主搜索，单次任务搜索量为普通版 10 倍 |
| 2024-11 | k0-math ✱ | [官方公告](http://www.duozhi.com/industry/insight/2024111916744.shtml) | 首个数学推理模型（RL 路线），对标 OpenAI o1，四项基准场景超 o1-preview |
| 2025-01-20 | **k1.5**（多模态推理） | [arXiv:2501.12599](https://arxiv.org/abs/2501.12599) | "RL 是预训练数据瓶颈之外的新扩展轴"；数学 / 代码 / 视觉推理全面对标 o1 |
| 2025-02 | **Moonlight + Muon 开源** | [arXiv:2502.16982](https://arxiv.org/abs/2502.16982) | 首证 Muon 优化器可扩展至 LLM 大规模训练（~2× 计算效率），K2 优化器前哨 |
| 2025-04-10 | **Kimi-VL**（A3B / Thinking） | [arXiv:2504.07491](https://arxiv.org/abs/2504.07491) | 16B MoE（2.8B 激活）+ MoonViT 原生分辨率视觉编码，128K 上下文 |
| 2025-04 | Kimina-Prover Preview | [arXiv:2504.11354](https://arxiv.org/abs/2504.11354) | Lean 4 形式化证明，miniF2F 首破 80%（80.7%，pass@8192） |
| 2025-04-25 | **Kimi-Audio** | [arXiv:2504.18425](https://arxiv.org/abs/2504.18425) | 7B 语音基座，1300 万小时音频预训练，理解 / 生成 / 对话统一 |
| 2025-06 | Kimi-Dev（72B SWE 智能体） | [arXiv:2509.23045](https://arxiv.org/abs/2509.23045) | text-to-patch 端到端 RL，SWE-bench Verified 60.4%（当时开源 SOTA） |
| 2025-06 | Kimi-VL-Thinking-2506 | [模型卡](https://huggingface.co/moonshotai)（✱） | 长链思考 SFT+RL 升级，MMMU 64.0 / MathVista 80.1 |
| 2025-07 | Kimina-Prover 完整版 | [HF 博客](https://huggingface.co/blog/AI-MO/kimina-prover)（✱） | 测试时 RL 搜索，miniF2F 92.2% SOTA（72B，与 AI-MO 合作） |
| 2025-07-11 | **Kimi K2** | [arXiv:2507.20534](https://arxiv.org/abs/2507.20534) | 1T 总参 / 32B 激活 MoE + MuonClip，15.5T token，agentic 能力开源 SOTA |
| 2025-08-11 | Kimi Researcher ✱ | [官方博客](https://zhuanlan.zhihu.com/p/1921119537757140195) | 端到端 RL 深度研究智能体：单任务平均 23 步推理、探索 200+ 网页 |
| 2025-09-05 | Kimi-K2-Instruct-0905 ✱ | [HF 模型卡](https://huggingface.co/moonshotai) | K2 小版本：agentic 编码增强，上下文 128K → 256K |
| 2025-11-06 | **K2 Thinking** ✱ | [HF 模型卡](https://huggingface.co/moonshotai/Kimi-K2-Thinking) / [技术博客](https://moonshotai.github.io/Kimi-K2/thinking.html) | 首个开源万亿参数推理模型；原生 INT4；200–300 步工具链不脱轨 |
| 2026-01 末 | **Kimi K2.5** | [arXiv:2602.02276](https://arxiv.org/abs/2602.02276)（论文 02-02） | K 系列首个原生多模态（~15T 视觉+文本续训）；Agent Swarm 并行编排 |
| 2026-04-20 | **Kimi K2.6** ✱ | [HF / kimi.com](https://www.kimi.com/ai-models/kimi-k2-6) | 长程编码 + swarm（300 子代理 / 4000 协调步）；SWE-Bench Pro 58.6% 平 GPT-5.5 |
| 2026-07-16 | **Kimi K3**（+ PerceptionBench） | [arXiv:2607.24653](https://arxiv.org/abs/2607.24653)（权重 07-27 开放） | 2.8T 总参 / 104B 激活、1M 上下文、原生视觉；首个开放 3T 级前沿模型 |

---

## 二、模型详解

### 1. 2023–2024：长文本起家

- **Kimi 智能助手（2023-10-09 上线）**：出道即主打 20 万字中文长文本输入，凭"长文本"心智快速破圈。
- **200 万字无损上下文（2024-03-18）**：上下文 10× 扩展并开启内测；引发国内大厂"长文本大战"。三天后（03-21）因请求量破历史纪录宕机，成为"长文本推理算力极限"的标志性事件——这也是 Mooncake（§三）加速落地的直接背景。
- **Kimi 探索版（2024-10-11）**：AI 自主搜索，单次任务的搜索量达普通版 10 倍，通过数百次搜索自主完成复杂任务，为后来 agentic 路线的雏形。

### 2. 2024-11 ~ 2025-01：RL 推理路线确立（k0-math → k1.5）

- **k0-math（2024-11，✱）**：Kimi 首个数学推理模型，RL 训练、逐步思考，官方称四项基准场景（中考 / 高考 / 中考几何 / 初等竞赛）超 o1-preview、两项持平。无独立论文，技术细节并入 k1.5 报告。
- **k1.5（2025-01-20 发布，论文 01-22）**：[Kimi k1.5: Scaling Reinforcement Learning with LLMs](https://arxiv.org/abs/2501.12599)。多模态推理模型，论文的核心论点：**预训练数据见顶后，RL 是新的扩展轴**。技术要点：不用 MCTS / 价值函数 / PPO 变体，而以简化的 **online policy mirror descent** 做 RL；**context length scaling**（短链 → 长链课程式扩展）；**long2short** 方法把长思考能力蒸馏进短链输出。数学（AIME / MATH-500）、代码（LiveCodeBench）与视觉多模态推理全面对标 OpenAI o1 系列。该论文与 DeepSeek-R1 同期，共同定义了 2025 年"RL 推理"范式。

### 3. 2025 春：开源矩阵（VL / Kimina / Audio / Dev）

- **Kimi-VL（2025-04-10）**：[Kimi-VL Technical Report](https://arxiv.org/abs/2504.07491)。Kimi-VL-A3B：16B 总参 MoE、每 token 仅激活 2.8B；自研 **MoonViT** 原生分辨率视觉编码器（任意分辨率不切块，高分辨率理解强于固定切块方案）；128K 上下文。同步开源 **Kimi-VL-A3B-Thinking**（长链 CoT SFT + RL）；2025-06 迭代 **Kimi-VL-Thinking-2506**（MMMU 64.0、MathVista 80.1、OSWorld 智能体任务提升显著）。代码 [MoonshotAI/Kimi-VL](https://github.com/MoonshotAI/Kimi-VL)，MIT。
- **Kimina-Prover Preview（2025-04）**：[arXiv:2504.11354](https://arxiv.org/abs/2504.11354)。**Kimina** 是 Kimi 的形式化数学（Lean 4）开源项目：把 RL 推理模型与形式化证明搜索结合，"推理驱动探索"（reasoning-driven exploration）替代传统树搜索，miniF2F-test 达 **80.7%**（pass@8192），为公开报道中首个破 80% 的结果。**完整版 Kimina-Prover（2025-07，72B，与 AI-MO 合作）**：引入测试时 RL 搜索，miniF2F 提至 **92.2%** SOTA（[HF 博客](https://huggingface.co/blog/AI-MO/kimina-prover)，✱）。
- **Kimi-Audio（2025-04-25）**：[Kimi-Audio Technical Report](https://arxiv.org/abs/2504.18425)。Kimi-Audio-7B-Instruct：音频 tokenizer + LLM（Qwen2.5-7B 基座）+ 流式 detokenizer 的混合架构，**1300 万小时**语音 / 音乐 / 环境音预训练，语音理解、生成、对话三合一；开源代码（MIT，涉 Qwen 部分 Apache 2.0）与权重，配套评测框架 [Kimi-Audio-Evalkit](https://github.com/MoonshotAI/Kimi-Audio-Evalkit)。
- **Kimi-Dev（2025-06）**：论文 [Kimi-Dev: Agentless Training as Skill Prior for SWE-Agents](https://arxiv.org/abs/2509.23045)（2025-09）。开源软件工程智能体 **Kimi-Dev-72B**（Qwen2.5-72B 基座）：把"无智能体式的 text-to-patch 全流程"作为技能先验端到端 RL 训练，而非多阶段 SFT/RL 流水线；SWE-bench Verified **60.4%**，发布时开源 SOTA。仓库 [MoonshotAI/Kimi-Dev](https://github.com/MoonshotAI/Kimi-Dev)。

### 4. 2025-07 ~ 11：K2 世代

- **Kimi K2（2025-07-11 开源权重，论文 07-28）**：[Kimi K2: Open Agentic Intelligence](https://arxiv.org/abs/2507.20534)。**1T 总参 / 32B 激活** MoE：61 层、384 专家（每 token 选 8 + 1 共享）、MLA 注意力 + SwiGLU、词表 160K；15.5T token 预训练。两大关键工程：
	- **MuonClip 优化器** = Muon（矩阵正交化）+ **QK-Clip**——从架构层面消除注意力 QK logits 爆炸，使 Muon 稳定扩展到万亿参数、端到端无训练尖峰（Moonlight 论文的规模化续章）；
	- **复合 agentic RL 管线**：通用 HF（可帮助性 / 忠实性）RL → 自我批评迭代 → 分领域专项 RL（可验证奖励），支持 200–300 步连续工具调用，发布时为开源非思考模型 SOTA（agentic / 代码 / 数学全面领先）。
	Modified MIT 许可（权重 + 代码）。开源次日登顶 HF 下载榜，Nature News 称"another DeepSeek moment"。社区 vLLM / SGLang / TensorRT-LLM day-0 适配。
- **Kimi Researcher（2025-08-11，✱）**："模型即 Agent"理念的端到端 RL 深度研究智能体：单任务平均 **23 步推理、探索 200+ 网页**，输出带引用的完整研究报告；2025-10 逐步全量开放。同期智能体产品：OK Computer（通用任务 Agent）。
- **Kimi-K2-Instruct-0905（2025-09-05，✱）**：K2 权重小版本：agentic 编码增强、上下文 128K → **256K**。
- **K2 Thinking（2025-11-06，✱ 技术博客）**：[HF moonshotai/Kimi-K2-Thinking](https://huggingface.co/moonshotai/Kimi-K2-Thinking)。**首个开源万亿参数推理模型**：在 K2 基座上继续 RL，使用 **200–300B token 的思考数据**（社区测算算力成本约 $4.6M）；**原生 INT4 QAT 量化**（部署显存减半、~2× 无损加速）；可稳定执行 200–300 次连续工具调用。成绩：HLE（带工具）44.9、BrowseComp 60.2、AIME25 94.5（配 Python 99.1）、SWE-bench Verified 71.3；上线当日 LMArena Elo +302。同日 Kimi 应用上线 **Agent Swarm**（最多 100 个子智能体并行编排）。Modified MIT（附加条款：>1 亿 MAU 或 >$20M/月收入需署名）。

### 5. 2026：K2.5 / K2.6 / K3

- **Kimi K2.5（2026-01 末开源权重，论文 2026-02-02）**：[Kimi K2.5: Visual Agentic Intelligence](https://arxiv.org/abs/2602.02276)。K 系列首次**原生多模态**：在 Kimi-K2-Base 上以 **~15T 混合视觉 + 文本 token 持续预训练**，接入 MoonViT（400M）视觉编码器；架构延续 1T/32B、256K 上下文、原生 INT4。训练法：联合文本-视觉预训练 → **zero-vision SFT** → 联合文本-视觉 RL；提供 Instant / Thinking 双模式。**Agent Swarm**（自导向并行智能体编排）：复杂任务拆为异构子问题并行执行，延迟最高降 4.5×，BrowseComp（Agent Swarm）78.4；HLE-Full（带工具）50.2、SWE-bench Verified 76.8。Modified MIT；配套开源 WorldVQA 基准（[MoonshotAI/WorldVQA](https://github.com/MoonshotAI/WorldVQA)）。
- **Kimi K2.6（2026-04-20，✱）**：[HF moonshotai/Kimi-K2.6](https://huggingface.co/moonshotai/Kimi-K2.6) / [kimi.com](https://www.kimi.com/ai-models/kimi-k2-6)。从"Code Preview"分支毕业的稳定版：主打长程编码（long-horizon coding），Agent Swarm 扩展至 **300 子代理 / 4000 协调步**；SWE-Bench Pro 58.6% 平 GPT-5.5。注：kimi-k2 系列 API 已于 2026-05-25 停用，引导迁移至 K3。
- **Kimi K3（2026-07-16 发布，权重 07-27 全量开放）**：[Kimi K3: Open Frontier Intelligence](https://arxiv.org/abs/2607.24653) / [官方博客](https://www.kimi.com/blog/kimi-k3) / [MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3)。**2.8T 总参 / 104B 激活**，896 专家（每 token 16 路由 + 2 共享）；新架构组件：**Kimi Delta Attention + Attention Residuals**、**LatentMoE**（经 3584 维潜空间路由）；**原生视觉**、**1M token 上下文**——目前最大的开放权重前沿模型（首个开放 3T 级）。LMArena Elo 1547（较 K2.6 +732），官方评测超越 Claude Opus 4.8 max 与 GPT-5.5 high；演示能力覆盖 GPU 内核优化、前沿物理研究，甚至自行剪辑 56 段素材生成了官方宣传片。API 定价约 Claude Sonnet 档；同场开源 **PerceptionBench**（视觉感知基准）。

---

## 三、开源工具与基础设施

| 工具 / 仓库 | 时间 | 定位 | 要点 |
| --- | --- | --- | --- |
| [Mooncake](https://github.com/kvcache-ai/Mooncake) | 2024-06（[arXiv:2407.00079](https://arxiv.org/abs/2407.00079)，FAST'25 最佳论文） | KVCache 中心解耦推理服务 | 预填充 / 解码集群分离，用集群闲置 CPU/DRAM/SSD 组成全局 KVCache 池；支撑 Kimi 生产线（日处理 ~100B token）；2025-05 与 LMCache 合作 |
| [Moonlight + Muon](https://github.com/MoonshotAI/Moonlight) | 2025-02（[arXiv:2502.16982](https://arxiv.org/abs/2502.16982)） | 优化器 + 参照模型 | Moonlight 3B/16B MoE（5.7T token）证明 Muon 较 AdamW ~2× 计算效率、优化器内存 -48%；开源优化器实现与检查点，后被 PyTorch/DeepSpeed 官方集成；K2 的 MuonClip 直接源于此 |
| [Kimi-VL](https://github.com/MoonshotAI/Kimi-VL) | 2025-04 | 开源 VLM | A3B / A3B-Thinking / Thinking-2506，MIT |
| [Kimina-Prover](https://github.com/MoonshotAI/Kimina-Prover-Preview) | 2025-04 / 2025-07 | Lean 4 形式化证明 | miniF2F 80.7% → 92.2% SOTA |
| [Kimi-Audio](https://github.com/MoonshotAI/Kimi-Audio) | 2025-04 | 开源语音基座 | 7B，13M 小时音频；配套 Evalkit 评测框架 |
| [Kimi-Dev](https://github.com/MoonshotAI/Kimi-Dev) | 2025-06 | SWE 智能体 | 72B，端到端 RL，SWE-bench Verified 60.4% |
| K 系列权重（[HF moonshotai](https://huggingface.co/moonshotai)） | 2025-07 起 | 开放权重 | K2 / K2-Instruct-0905 / K2-Thinking / K2.5 / K2.6 / K3，Modified MIT（大商业化规模需署名）；GitHub 配套仓库 Kimi-K2 / Kimi-K2.5 / Kimi-K3 |
| [Kimi Code CLI](https://github.com/MoonshotAI/kimi-code) | 2026-01 前后（随 K2.5 生态） | 终端编码智能体 | TypeScript 编写（读写代码 / 跑命令 / 搜文件 / 抓网页），MIT；kimi.com/code |
| [WorldVQA](https://github.com/MoonshotAI/WorldVQA) / PerceptionBench | 2026-01 / 2026-07 | 开源基准 | 分别随 K2.5、K3 发布（世界知识视觉问答 / 感知） |

---

## 四、技术演进主线

- **优化器**：Muon 规模化首证（Moonlight，2502）→ MuonClip / QK-Clip（K2，万亿参数端到端无尖峰）——K 系列区别于 DeepSeek（AdamW+辅助策略）的底座差异
- **RL 路线**：k0-math（数学 RL）→ k1.5（RL scaling + context scaling + long2short）→ K2（复合 agentic RL）→ K2 Thinking（200–300B 思考 token 长程推理）→ K2.5 / K3（Agent Swarm 并行编排），一条"模型即 Agent"主线贯穿
- **架构**：MLA + 细粒度 MoE（K2：1T/32B/384 专家）→ 原生 INT4 QAT（Thinking / K2.5，部署成本减半）→ K3：Kimi Delta Attention + Attention Residuals + LatentMoE（2.8T/104B）
- **上下文**：20 万字 → 200 万字 → 128K（K2）→ 256K（0905 / Thinking / K2.5）→ 1M（K3）
- **多模态**：MoonViT（Kimi-VL → K2.5 持续预训练接入）→ K3 原生视觉
- **推理服务**：Mooncake（KVCache 中心解耦）自 2024 起支撑 Kimi 生产线，是学界工业界解耦 serving 的代表工作
