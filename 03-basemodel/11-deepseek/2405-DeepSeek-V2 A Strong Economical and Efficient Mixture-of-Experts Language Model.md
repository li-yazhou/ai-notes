---
type: paper
paper_id: arxiv-2405.04434
title: "DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model"
arxiv: https://arxiv.org/abs/2405.04434
year: 2024
updated: 2026-06-29
status: summarized
primary_category: llm-architecture
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/architecture
  - llm/frontier-model
  - model/deepseek
  - model/deepseek-v2
  - method/moe
  - method/mla
  - method/grpo
  - method/long-context
  - eval/model-benchmark
  - year/2024
  - priority/p0
  - read/deep
---

# DeepSeek-V2：用 MLA + MoE 把能力和成本一起重写

> 更新时间：2026-06-29
> 论文地址：https://arxiv.org/abs/2405.04434
> 机构：DeepSeek-AI

---

## 一、一句话概括

**DeepSeek-V2** 是 DeepSeek 从 dense LLM 走向高效 MoE frontier model 的关键论文：模型总参数 236B，但每个 token 只激活约 21B 参数，并通过 **MLA** 压缩 KV cache、通过 **DeepSeekMoE** 降低稀疏计算成本，在能力增强的同时显著降低训练和推理开销。

如果 DeepSeek LLM 证明了“开源 dense 模型能做强”，V2 证明的是：

> frontier model 不一定只能靠更贵的 dense scaling，结构效率本身可以成为竞争力。

---

## 二、核心问题

传统 dense Transformer 的困难是：

- 参数越大，训练成本几乎线性变贵。
- 长上下文会带来沉重 KV cache。
- 推理时每个 token 都要走完整模型，吞吐受限。

DeepSeek-V2 的目标是同时解决三件事：

```text
更强能力 + 更低训练成本 + 更低推理成本
```

---

## 三、模型概况

| 项目 | DeepSeek-V2 |
|---|---:|
| 总参数 | 236B |
| 每 token 激活参数 | 约 21B |
| 架构 | MoE decoder-only Transformer |
| 核心模块 | MLA + DeepSeekMoE |
| 预训练数据 | 8.1T tokens |
| 长上下文 | 扩展到 128K |

论文报告，相比 DeepSeek 67B，DeepSeek-V2：

- 训练成本节省约 42.5%。
- KV cache 减少约 93.3%。
- 最大生成吞吐提升到约 5.76 倍。

这些数字让 V2 成为后来 DeepSeek 低成本叙事的技术起点。

---

## 四、MLA：压缩 KV Cache

MLA 是 Multi-head Latent Attention。它的思想可以粗略理解为：

```text
不要把每层每头完整 K/V 都直接存下来，
而是先把 K/V 压到低维 latent 表示，
推理时再从 latent 中恢复需要的信息。
```

这样做的直接收益是大幅降低长上下文推理中的 KV cache 占用。

为什么重要？

- 对聊天模型，KV cache 是长对话和高并发推理的瓶颈。
- 对 Agent，长轨迹、工具日志、环境状态都会吃上下文。
- 对服务部署，KV cache 直接影响单卡/单机并发能力。

MLA 把 attention 的内存瓶颈变成可优化对象，是 V2 到 V3 都保留的关键设计。

---

## 五、DeepSeekMoE：细粒度专家与共享专家

DeepSeekMoE 的核心是稀疏激活：

- 总参数很多，但每个 token 只走一小部分专家。
- 通过细粒度专家拆分，让专家专门化更充分。
- 通过共享专家保留通用能力，降低路由带来的不稳定。

这和普通 dense 模型的区别是：

```text
dense: 每个 token 都用全部参数
MoE: 每个 token 按路由选择部分专家
```

MoE 的难点是专家负载、通信成本和训练稳定性。V2 的价值在于把 MoE 做到强能力和可部署之间的平衡，而不是只追求参数规模好看。

---

## 六、训练与长上下文

DeepSeek-V2 预训练在 8.1T tokens 上完成，语料来自多源高质量数据，中文 token 数量略多于英文。

初始训练上下文长度为 4K，随后用 YaRN 扩展上下文。论文报告模型在 32K 训练后可以泛化到 128K 长上下文。

这对 Agent 很关键：真实任务的上下文经常包含网页、代码仓库、日志、工具调用历史和用户约束。模型是否能稳定处理长上下文，直接影响 Agent 上限。

---

## 七、对齐：SFT 与 GRPO

V2 的后训练包括 SFT 与 RL。RL 部分使用 **GRPO**，这是后来 DeepSeek-R1 中非常关键的算法线索。

GRPO 的直觉是：不再依赖一个单独价值模型，而是对同一问题采样一组输出，用组内相对表现估计优势，从而降低 RL 训练复杂度。

V2 中 RL 主要用于：

- 推理能力对齐。
- 人类偏好对齐。
- 提升开放式对话质量。

---

## 八、实验结果

论文结论可以概括为：

- V2 只激活 21B 参数，却整体超过 DeepSeek 67B。
- 在开源模型中达到第一梯队。
- 在代码、数学和中文任务上表现强。
- 英文任务上和 LLaMA 3 等强模型有竞争，但论文也承认英文 token 配比可能带来差异。

开放式评测中，RL 版本相对 SFT 版本在 AlpacaEval 2.0 等评测上有明显提升。中文 AlignBench 中，论文报告 V2 Chat 超过当时多个开源模型，并可与部分闭源模型竞争。

---

## 九、关键洞察

### 1. 成本是模型能力的一部分

V2 的贡献不是“便宜一点”，而是把训练成本、KV cache、吞吐量这些工程指标放到模型论文的核心位置。

### 2. MLA 是长上下文时代的基础设施

对 Agent 来说，上下文越长，KV cache 越是瓶颈。MLA 使长上下文和高并发服务更可行。

### 3. GRPO 是 R1 的前奏

V2 中已经出现 GRPO，用于后训练对齐。到 R1，这条线被推到极致：用 RL 直接激发推理能力。

---

## 十、局限

- 仍是文本模型，不处理多模态。
- MoE 部署比 dense 模型复杂，对通信和推理框架要求高。
- 论文承认模型没有持续知识更新，仍会幻觉。
- 长上下文能力不等于长任务可靠性，Agent 场景还需要额外评测。

---

## 十一、和后续论文的关系

| 后续论文 | 继承/推进 |
|---|---|
| DeepSeek-V3 | 保留 MLA + DeepSeekMoE，扩大到 671B total / 37B activated，并加入 FP8、DualPipe、MTP、无辅助损失负载均衡 |
| DeepSeek-R1 | 在 V3-Base 上使用 GRPO 进行大规模 reasoning RL |

DeepSeek-V2 是理解 DeepSeek 为什么能在 V3 / R1 阶段同时讲“强能力”和“低成本”的中枢论文。

