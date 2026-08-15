---
type: paper
paper_id: arxiv-2203.11171
title: "Self-Consistency Improves Chain of Thought Reasoning in Language Models"
arxiv: https://arxiv.org/abs/2203.11171
year: 2022
updated: 2026-06-28
status: summarized
primary_category: reasoning-planning
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/reasoning-planning
  - method/cot
  - method/self-consistency
  - year/2022
  - priority/p1
  - read/skim
---

# Self-Consistency：用多条推理路径提升 CoT 稳定性

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2203.11171
> 发表：2022 ｜ 作者：Xuezhi Wang, Jason Wei, Dale Schuurmans 等

---

## 一、一句话概括

**Self-Consistency** 不再贪心生成一条 Chain-of-Thought，而是采样多条推理路径，并选择最一致的最终答案。

它把 CoT 从“单路径推理”推进到“多路径采样 + 答案投票”。

---

## 二、核心方法

传统 CoT：

```text
问题 → 一条推理链 → 答案
```

Self-Consistency：

```text
问题
  → 采样多条推理链
  → 抽取每条链的最终答案
  → 选择出现频率最高或概率质量最大的答案
```

直觉是：复杂问题可能有多种推理路径，但正确答案应在多条合理路径中收敛。

---

## 三、关键结果

论文在多个算术和常识推理任务上显著提升 CoT：

- GSM8K 提升约 17.9 个百分点。
- SVAMP 提升约 11.0 个百分点。
- AQuA 提升约 12.2 个百分点。
- StrategyQA、ARC-Challenge 也有提升。

这证明 test-time compute 可以显著改变模型表现。

---

## 四、与 Agent 的关系

Self-Consistency 不是完整 Agent，但它是 Agent 规划和决策的重要组件：

- 多采样计划。
- 多路径推理。
- 多候选动作投票。
- 对高风险结论做一致性检查。

后来的 ToT、LATS、多 Agent debate、self-consistency eval 都继承了这个思想。

---

## 五、局限与启发

局限：

- 成本线性增加。
- 多数投票不保证正确，可能共同偏误。
- 对开放式任务，答案聚合比选择题更难。

启发：

- Agent 不应只跑一次就行动，关键节点应做多候选检查。
- 报告结果时要同时报告采样次数和成本，否则不可比较。

---

## 参考 / 延伸阅读

- 论文：[Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)
- 相关：[[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]

