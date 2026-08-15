---
type: paper
paper_id: arxiv-2501.12948
title: "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning"
arxiv: https://arxiv.org/abs/2501.12948
year: 2025
updated: 2026-06-29
status: summarized
primary_category: reasoning-model
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - paper/reasoning
  - llm/reasoning-model
  - model/deepseek
  - model/deepseek-r1
  - method/reinforcement-learning
  - method/grpo
  - method/cot
  - method/distillation
  - eval/math
  - eval/code
  - year/2025
  - priority/p0
  - read/deep
---

# DeepSeek-R1：用强化学习激发长链推理

> 更新时间：2026-06-29
> 论文地址：https://arxiv.org/abs/2501.12948
> 机构：DeepSeek-AI

---

## 一、一句话概括

**DeepSeek-R1** 的核心结论是：大模型的推理能力可以通过大规模强化学习从可验证任务中被激发出来，甚至可以在没有人工标注推理轨迹的情况下产生自我反思、验证、回退和策略调整等长链推理行为。

这篇论文最重要的不是“R1 分数很高”，而是提出了一条 reasoning model 的训练路线：

```text
强 base model + 可验证奖励 + GRPO + 大规模采样/RL + 蒸馏
```

---

## 二、R1-Zero：不先 SFT，直接 RL

论文先训练 **DeepSeek-R1-Zero**：

- 基座：DeepSeek-V3-Base。
- 不经过传统 supervised fine-tuning。
- 直接使用 GRPO 做强化学习。
- 奖励主要来自可验证答案，例如数学、代码、逻辑题的最终正确性。

这个实验非常关键，因为它证明：模型不一定必须模仿人类写好的推理链，才能学会长链推理。

训练后，R1-Zero 自发出现：

- 更长的 reasoning trace。
- 自我检查。
- 重新审题。
- 尝试替代路径。
- 发现错误后修正。

论文把其中一个现象称为 “aha moment”：模型在推理中意识到前面路径可能有问题，并主动重新组织解法。

---

## 三、GRPO：不用价值模型的组内相对优化

R1 使用 **Group Relative Policy Optimization**。

PPO 通常需要一个价值模型估计 advantage。GRPO 的思路是：

```text
对同一个问题采样一组答案；
根据组内奖励相对高低估计优势；
用相对优势更新策略。
```

这样可以省掉独立价值模型，降低 RL 训练复杂度，也更适合可验证任务的大规模采样。

对于 reasoning model 来说，这很自然：同一道数学题可以采多个解法，答案正确的轨迹在组内得到更高相对奖励。

---

## 四、R1：在 R1-Zero 之上补齐可读性和通用能力

R1-Zero 虽然推理强，但有问题：

- 可读性差。
- 中英混杂。
- 更偏数学/代码等可验证任务，通用对话能力不足。

因此 DeepSeek-R1 使用多阶段流程：

1. 冷启动数据：少量高质量、人类友好的推理样本。
2. 第一阶段 RL：激发 reasoning 能力。
3. Rejection sampling：从模型生成中筛选高质量样本。
4. SFT：把筛选样本和通用数据混合训练。
5. 第二阶段 RL：同时优化推理、helpfulness 与 harmlessness。

这条路线的意义是：**R1 不是纯 RL 的浪漫故事，而是“纯 RL 探索 + 人类友好格式 + 通用能力对齐”的组合。**

---

## 五、实验结果

论文报告 DeepSeek-R1 在数学、代码和 STEM 推理上达到非常强的水平：

| 任务 | DeepSeek-R1 表现 |
|---|---:|
| AIME 2024 Pass@1 | 79.8 |
| MATH-500 Pass@1 | 97.3 |
| Codeforces percentile | 96.3 |
| Codeforces rating | 2029 |

与 DeepSeek-V3 相比，R1 在竞赛编程和高难数学上提升明显。论文还报告 majority voting 可以继续提升部分数学任务结果，说明 test-time compute 对 reasoning model 很重要。

---

## 六、蒸馏：把大模型推理能力迁移到小模型

R1 论文的另一个贡献是蒸馏。

作者用 DeepSeek-R1 生成约 800K 高质量样本，然后蒸馏到 Qwen / Llama 系列小模型上。结果显示，蒸馏模型的推理能力显著超过原始 instruction-tuned 模型。

这里的结论很有启发：

- 对小模型，直接从大模型长链推理样本蒸馏非常有效。
- 纯 RL 探索在小模型上未必比蒸馏更高效。
- 大模型可以作为 reasoning data generator，推动小模型能力迁移。

---

## 七、关键洞察

### 1. 推理能力可以来自“可验证奖励”，不一定来自人工 CoT

这改变了 CoT 时代的默认假设。过去常见做法是给模型看人类推理过程；R1-Zero 证明只要任务有可靠 verifier，模型可以自己探索有效推理策略。

### 2. Long CoT 是训练结果，不只是 prompt 技巧

R1 的长链推理不是简单写一句“think step by step”，而是在 RL 中被奖励机制塑造出来的行为模式。

### 3. Verifier 决定了 RL 的适用边界

数学、代码、逻辑题适合 RL，因为答案能验证；开放写作、审美、复杂真实任务很难设计可靠奖励，容易 reward hacking。

### 4. Agent 研究需要重新理解 reasoning model

R1 这类模型会更愿意花 token 推理、检查、回退，这对 Agent 是利好；但过度思考、工具调用结构化不足、长上下文成本也会变成新问题。

---

## 八、局限

论文列出的局限对实际使用很重要：

- 结构化输出、函数调用和工具使用能力仍不够理想。
- 有时会过度思考，增加延迟和成本。
- 仍可能出现语言混杂。
- 对 prompt 比较敏感。
- 软件工程任务上相对 V3 的提升没有数学/竞赛编程那么大。
- 纯 RL 依赖可靠 reward signal，开放任务容易出现奖励投机。

---

## 九、和 Agent / 评测的关系

R1 对 Agent 研究有三点直接影响：

1. **推理 token 变成可扩展资源**：test-time compute 成为能力来源。
2. **可验证任务更适合训练和评测**：数学、代码、工具结果、环境状态都能提供 reward。
3. **Agent benchmark 要区分模型推理与系统能力**：强 reasoning model 不自动等于强 Agent，还需要工具调用、状态管理、环境交互和错误恢复。

---

## 十、适合怎么读

阅读顺序建议：

1. 先读 R1-Zero，理解“无 SFT 直接 RL”的实验意义。
2. 再读 R1 多阶段训练，理解为什么纯 RL 不够产品化。
3. 重点看 GRPO 和 reward design。
4. 最后看蒸馏结果，理解 reasoning 能力如何向小模型迁移。

这篇是 reasoning model 时代的核心论文之一，和 CoT、Self-Consistency、ToT、Toolformer、ReAct 一起读，会更容易看清从 prompt reasoning 到 trained reasoning 的迁移。

