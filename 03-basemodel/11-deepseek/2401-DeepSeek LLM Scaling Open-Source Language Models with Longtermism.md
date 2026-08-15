---
type: paper
paper_id: arxiv-2401.02954
title: "DeepSeek LLM: Scaling Open-Source Language Models with Longtermism"
arxiv: https://arxiv.org/abs/2401.02954
year: 2024
updated: 2026-06-29
status: summarized
primary_category: llm-pretraining
priority: p1
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/pretraining
  - llm/decoder-only
  - model/deepseek
  - model/deepseek-llm
  - method/scaling
  - method/sft
  - method/dpo
  - eval/model-benchmark
  - year/2024
  - priority/p1
  - read/deep
---

# DeepSeek LLM：DeepSeek 系列的开源基座模型

> 更新时间：2026-06-29
> 论文地址：https://arxiv.org/abs/2401.02954
> 机构：DeepSeek-AI

---

## 一、一句话概括

**DeepSeek LLM** 是 DeepSeek 系列的第一代开源基座模型报告：从 2T 中英 token 训练 7B / 67B dense decoder-only 模型，并用 SFT + DPO 得到 DeepSeek Chat，目标是在开源模型中建立一个可持续扩展的中英双语底座。

它的价值不只在模型本身，而在于提出了 DeepSeek 后续路线的三个起点：

- 认真研究 scaling law，而不是只堆算力。
- 把中英文、代码、数学、推理放在同一个基座里。
- 用开源模型对标 LLaMA-2、GPT-3.5 等强基线。

---

## 二、它解决什么问题

论文面向的是 2023-2024 年开源 LLM 的核心矛盾：

```text
闭源模型能力强，但不可控、不可复现；
开源模型可用，但中英双语、代码、数学和对齐能力仍不稳定。
```

DeepSeek LLM 试图回答：

> 如果从数据、规模、训练和对齐上系统投入，一个开源 dense LLM 能否接近或超过当时主流开源强模型？

---

## 三、模型与数据

论文发布两档模型：

| 模型 | 参数量 | 层数 | hidden size | heads | 训练 token |
|---|---:|---:|---:|---:|---:|
| DeepSeek LLM 7B | 约 7B | 30 | 4096 | 32 | 2T |
| DeepSeek LLM 67B | 约 67B | 95 | 8192 | 64 | 2T |

架构上基本沿用 LLaMA 风格的 decoder-only Transformer。67B 模型使用 Grouped-Query Attention 来降低推理成本。

训练数据是约 2T tokens 的中英双语语料，并包含代码、数学和推理相关数据。论文强调数据仍在持续扩展，这一点很像 DeepSeek 后续 V2 / V3 的前奏：后续版本会继续把数据规模和数据质量作为能力增长的主杠杆。

---

## 四、Scaling Law 分析

这篇论文一个容易被低估的部分是 scaling law。作者训练了多个小模型来研究：

- model size 与 data size 如何分配更划算。
- 数据质量如何改变最优计算分配。
- 当数据质量更高时，新增 compute 更适合分配给模型规模，而不是盲目增加低质 token。

这给后来的 DeepSeek-V2 / V3 埋下了一个方法论线索：**效率不是单纯靠小模型或省算力，而是靠模型结构、数据质量和训练配方一起优化。**

---

## 五、对齐：SFT + DPO

DeepSeek Chat 的对齐流程主要包括：

- 约 1.5M 指令微调数据。
- 其中大部分是 helpfulness 数据，另有 safety 数据。
- 使用 DPO 进一步做偏好对齐。

论文也提到一个实际经验：数学和代码数据虽然能增强能力，但如果混入不当，也可能提高重复、模板化或可读性问题。这是后续 reasoning model 训练中会不断遇到的取舍。

---

## 六、实验结果

DeepSeek LLM 67B 在多个 benchmark 上超过 LLaMA-2 70B，尤其体现在：

- 代码能力：HumanEval、MBPP 等。
- 数学能力：GSM8K、MATH 等。
- 推理能力：BBH 等。
- 中文能力：中文综合评测中优势明显。

对齐后的 DeepSeek LLM 67B Chat 在开放式评测中表现也很强。论文报告 DPO 版本在 MT-Bench 上优于非 DPO 版本，并在中文开放式评测 AlignBench 中超过多个开源/闭源对照模型。

安全评测方面，论文使用 Do-Not-Answer 等任务检查模型是否拒绝不安全请求。这里的意义不是说模型“已经安全”，而是说明 DeepSeek 从第一代开始就把 helpfulness 与 harmlessness 放进对齐目标。

---

## 七、关键洞察

### 1. DeepSeek 的起点不是 MoE，而是 scaling + 数据

很多人认识 DeepSeek 是从 V2 / V3 的 MoE 和低成本训练开始，但第一代 LLM 报告显示，它更早的主线是：

```text
数据质量 -> scaling law -> 中英双语基座 -> 代码/数学/推理能力 -> 对齐
```

### 2. 中英双语能力是战略变量

这不是一个英文模型顺便支持中文的路线，而是从数据和评测上都把中文能力放在核心位置。

### 3. 开源模型开始逼近强闭源模型体验

DeepSeek LLM 67B Chat 在部分开放式评测中接近或超过 GPT-3.5 级别基线，这在当时强化了一个判断：开源模型不只是研究玩具，而可以成为真实应用底座。

---

## 八、局限

- 模型仍是 dense 架构，训练和推理成本高，难以继续无脑扩大。
- 数据质量与数据组成仍有改进空间，尤其是中文高质量语料覆盖度。
- 对齐主要基于 SFT + DPO，离后来的大规模 reasoning RL 还有距离。
- 评测仍以 benchmark 为主，复杂真实任务与 agent 场景覆盖不足。

---

## 九、和后续 DeepSeek 系列的关系

这篇可以看作 DeepSeek 技术路线的第一个基点：

| 后续论文 | 继承/推进点 |
|---|---|
| DeepSeek-V2 | 从 dense 转向 MoE，引入 MLA 和 DeepSeekMoE，大幅优化训练/推理成本 |
| DeepSeek-V3 | 扩大到 671B total / 37B activated，引入 FP8、DualPipe、MTP、无辅助损失负载均衡 |
| DeepSeek-R1 | 在 V3-Base 上通过大规模 RL 激发推理能力 |

---

## 十、适合怎么读

如果你关注 Agent 和大模型评测，这篇不用陷入每个 benchmark 表格，重点读：

1. 数据与 scaling law 部分。
2. 7B / 67B 架构和训练配方。
3. DeepSeek Chat 的 SFT + DPO 对齐流程。
4. 数学、代码、中文、开放式评测结果。

它是理解 DeepSeek-V2 / V3 / R1 的前史。

