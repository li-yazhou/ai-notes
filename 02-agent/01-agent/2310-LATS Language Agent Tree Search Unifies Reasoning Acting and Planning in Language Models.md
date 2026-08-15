---
type: paper
paper_id: arxiv-2310.04406
title: "Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models"
arxiv: https://arxiv.org/abs/2310.04406
year: 2023
updated: 2026-06-28
status: summarized
primary_category: reasoning-planning
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/reasoning-planning
  - agent/react-loop
  - method/tree-search
  - method/mcts
  - year/2023
  - priority/p1
  - read/skim
---

# LATS：用树搜索统一语言 Agent 的推理、行动与规划

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2310.04406
> 项目：https://github.com/lapisrocks/LanguageAgentTreeSearch
> 发表：2023 ｜ 作者：Andy Zhou, Kai Yan, Michihiro Yasunaga 等

---

## 一、一句话概括

**Language Agent Tree Search（LATS）** 将 Monte Carlo Tree Search 引入语言 Agent，让模型在环境反馈、自我反思和价值评估的帮助下探索多条行动路径。

它把 ReAct 的线性行动循环升级成可搜索、可回溯的决策树。

---

## 二、核心设计

LATS 将每个状态视为树节点，每条边是一个 action。Agent 不再只做：

```text
Thought → Action → Observation → Thought ...
```

而是做：

```text
扩展候选行动
  ↓
环境反馈
  ↓
LM 价值评估
  ↓
自我反思
  ↓
MCTS 选择更优路径
```

模型既生成动作，也参与状态价值评估和失败反思。

---

## 三、关键结果

论文在编程、交互问答、Web 导航、数学等任务上验证 LATS：

- GPT-4 + LATS 在 HumanEval 上达到 92.7% pass@1。
- 在 WebShop 上，GPT-3.5 + LATS 平均分 75.9，接近梯度微调方法。

这说明 tree search 能在不训练模型的情况下提升 Agent 决策质量。

---

## 四、为什么重要

LATS 是 ToT 与 ReAct 的自然融合：

- ToT 提供树状搜索。
- ReAct 提供环境行动与观察。
- Reflexion 提供失败反馈。
- MCTS 提供探索-利用平衡。

它让 Agent planning 更像经典 AI 搜索，而不是单条语言链条。

---

## 五、局限与启发

局限：

- 成本高，多次扩展和评估需要大量模型调用。
- 价值函数仍由 LM 估计，可能不可靠。
- 对高分支环境，搜索空间很快膨胀。

启发：

- 对高价值任务，Agent 应支持分支探索和回滚。
- 如果有环境反馈，优先用反馈校正搜索，而不是只靠自评。

---

## 参考 / 延伸阅读

- 论文：[Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models](https://arxiv.org/abs/2310.04406)
- 相关：[[2305-Tree of Thoughts Deliberate Problem Solving with Large Language Models]]
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]

