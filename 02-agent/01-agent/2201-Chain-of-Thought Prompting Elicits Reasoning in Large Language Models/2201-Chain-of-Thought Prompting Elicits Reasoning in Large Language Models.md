---
type: paper
paper_id: arxiv-2201.11903
title: "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
arxiv: https://arxiv.org/abs/2201.11903
year: 2022
updated: 2026-06-28
status: summarized
primary_category: reasoning-planning
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/reasoning-planning
  - method/cot
  - year/2022
  - priority/p0
  - read/deep
---

# Chain-of-Thought Prompting：用中间推理步骤释放大模型推理能力

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2201.11903
> 发表：NeurIPS 2022 ｜ 作者：Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le, Denny Zhou（Google Research / Brain Team）

---

## 一、一句话概括

**Chain-of-Thought Prompting（CoT）** 证明：只要在 few-shot prompt 里给出“问题 → 中间推理步骤 → 答案”的示例，足够大的语言模型会自然生成分步推理过程，并显著提升算术、常识和符号推理任务的表现。

这篇论文的重要性不只是“让模型一步一步想”，而是打开了后续 Agent 的第一道门：**模型输出不再只是答案，也可以是可观察、可调试、可组合的中间认知过程**。

---

## 二、研究动机：为什么标准 prompting 不够

论文之前，few-shot prompting 主要给模型看输入-输出对：

```text
Q: ...
A: ...
```

这种方式适合简单问答，但在多步推理任务中常常失败。作者认为问题在于：模型虽然可能拥有相关知识，但标准提示没有显式要求它把问题拆开、逐步计算、维护中间状态。

CoT 的做法是把输出从“直接答案”扩展成：

```text
Q: 问题
A: 中间步骤 1。中间步骤 2。... 所以答案是 X。
```

它结合了两条路线的优点：
- **自然语言 rationale / explanation**：让推理过程显式化。
- **in-context learning**：不需要微调，只靠少量示例诱导模型行为。

---

## 三、方法：Chain-of-Thought Prompting

### 1. 基本形式

CoT prompt 中的每个示例是三元组：

```text
<input, chain of thought, output>
```

其中 chain of thought 是一串自然语言中间推理步骤。论文强调它不是额外训练目标，而是一种 prompting 格式。

### 2. CoT 的四个关键价值

论文总结了 CoT 的几个吸引力：

1. **分解问题**：复杂任务可拆成多个中间步骤。
2. **增加计算预算**：需要更多推理的问题可以自然生成更长过程。
3. **可解释/可调试**：人可以看到模型大致沿什么路径得到答案。
4. **通用性**：任何可用语言表达步骤的任务，理论上都能尝试 CoT。

### 3. 与 Agent 的关系

CoT 还不是完整 Agent，因为它没有外部动作和环境反馈。但它提供了 Agent 最重要的内部机制之一：**显式 reasoning trace**。

后续 ReAct、Reflexion、Tree of Thoughts、LATS、多智能体辩论等方法，本质上都继承了 CoT 的核心思想：不要只让模型给终点，要让模型生成可被检查、复用和修正的中间过程。

---

## 四、实验设计

论文在三类任务上验证 CoT：

| 任务类型 | 数据集/任务 | 衡量能力 |
|---|---|---|
| 算术推理 | GSM8K、SVAMP、ASDiv、AQuA、MAWPS | 多步数学文字题 |
| 常识推理 | CSQA、StrategyQA、Date Understanding、Sports Understanding、SayCan | 背景知识、多跳策略、行动选择 |
| 符号推理 | Last Letter Concatenation、Coin Flip | 抽象规则、长度泛化 |

使用的模型包括 LaMDA、GPT-3、Codex、PaLM 等不同规模模型。核心比较是 **Standard Prompting vs Chain-of-Thought Prompting**。

---

## 五、关键结果

### 1. 算术推理：大模型提升非常明显

在 GSM8K 上，CoT 带来大幅提升：

| 模型 | Standard | CoT |
|---|---:|---:|
| GPT-3 175B | 15.6 | 46.9 |
| Codex | 19.7 | 63.1 |
| PaLM 540B | 17.9 | 56.9 |

论文还尝试在 CoT 产生的方程上接一个外部计算器，PaLM 540B 的 GSM8K 结果从 56.9 提升到 58.6。这一点很重要：**CoT 负责语义分解，外部工具负责精确计算**，这已经接近后来的 Tool-use Agent 思路。

### 2. 能力呈现出“规模涌现”

小模型并不会稳定受益，甚至可能变差；CoT 的优势主要在足够大模型上出现。论文明确把这称为一种随模型规模出现的 emergent ability。

这对大模型评测有一个直接启发：**同一 benchmark 上，standard prompt 只能给出模型能力的下界；prompting 方法会改变模型可表现出的能力边界。**

### 3. 常识推理：不只适用于数学

PaLM 540B 在多个常识任务上也受益。论文中特别提到：
- StrategyQA 上，PaLM 540B + CoT 达到 75.6，超过当时单模型 prior SOTA 69.4。
- Sports Understanding 上，PaLM 540B + CoT 达到 95.4，超过论文引用的 unaided sports enthusiast 84。

说明 CoT 不是“数学技巧”，而是一种语言化的中间状态建模方式。

### 4. 符号推理：帮助长度外推

在 last-letter concatenation 和 coin flip 这类 toy symbolic task 上，CoT 让模型更容易把示例中的步骤模板迁移到更长输入。

但论文也提醒：这些任务结构清晰，示例已经给出完美解题流程，所以不能过度解读为模型获得了强符号系统能力。

---

## 六、局限

1. **不等于真正理解模型是否在“推理”**：CoT 是外显轨迹，不证明神经网络内部计算等同于人类推理。
2. **推理路径不保证正确**：模型可能写出看似合理但错误的中间步骤。
3. **依赖大模型规模**：CoT 在小模型上不稳定，实际部署成本高。
4. **示例构造仍有成本**：few-shot 时代成本较低，但如果用于大规模微调，人工标注 chain of thought 会很贵。
5. **可能暴露或诱导错误理由**：可解释性是优势，但“看起来可解释”不等于可靠因果解释。

---

## 七、为什么这篇论文重要

1. **确立了“显式中间推理”范式**：后续几乎所有 reasoning-agent 方法都从这里出发。
2. **改变了评测方式**：评测模型不能只看题目和答案，还要看提示格式、推理预算、采样策略。
3. **连接工具调用**：论文里“CoT + external calculator”的结果预示了后来的 Toolformer、ReAct、MRKL、function calling。
4. **提供 Agent 内部循环的雏形**：CoT 是 Thought；ReAct 在此基础上加入 Action 和 Observation。

---

## 八、与后续论文的关系

```text
CoT
  ↓ 显式推理轨迹
ReAct
  ↓ 推理 + 行动 + 环境反馈
Reflexion / LATS
  ↓ 失败后反思、搜索、重试
AgentBench / WebArena / SWE-bench
  ↓ 在真实或半真实环境中评测多步任务
```

CoT 的历史地位在于：它让大模型从“答案生成器”变成“过程生成器”。Agent 研究正是在这个过程空间上继续叠加工具、记忆、规划、验证和多智能体协作。

---

## 九、对我后续工作的启发

- 设计 Agent 时，先把任务拆成“哪些地方需要 Thought，哪些地方需要 Tool”。
- 评测 Agent 时，不能只看最终答案；还要分析中间推理是否稳定、是否可验证、是否能被外部反馈纠错。
- CoT 适合做“语义分解”，但不要让它承担精确计算、实时信息和数据库查询，这些应该交给工具。

---

## 参考 / 延伸阅读

- 论文：[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)
- 相关：[[2205-MRKL Systems]]
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]
