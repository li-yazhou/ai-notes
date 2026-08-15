---
type: paper
paper_id: arxiv-2305.10601
title: "Tree of Thoughts: Deliberate Problem Solving with Large Language Models"
arxiv: https://arxiv.org/abs/2305.10601
year: 2023
updated: 2026-06-28
status: summarized
primary_category: reasoning-planning
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/reasoning-planning
  - method/search
  - method/tree-search
  - year/2023
  - priority/p0
  - read/deep
---

# Tree of Thoughts：把大模型推理变成可搜索的思维树

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2305.10601
> 发表：2023 ｜ 作者：Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao, Karthik Narasimhan

---

## 一、一句话概括

**Tree of Thoughts（ToT）** 把语言模型的问题求解过程建模为一棵“思维树”：每个节点是一个中间想法，模型可以生成多个候选、评估候选价值，并用 BFS / DFS 等搜索算法探索更优路径。

它把 CoT 的“单条推理链”扩展成“多路径搜索”。

---

## 二、为什么 CoT 不够

CoT 通常是一条连续轨迹：

```text
Thought 1 → Thought 2 → Thought 3 → Answer
```

问题是，一旦早期步骤走错，后面会沿着错误路径继续。Self-consistency 虽然能采样多条链，但每条链之间没有系统化搜索和回退。

ToT 的核心想法是：复杂问题求解本来就是在状态空间中搜索。语言模型可以同时承担：

- 生成候选 thought。
- 评估 thought 是否有希望。
- 在搜索算法中提供启发式。

---

## 三、核心框架

ToT 实例化时需要回答四个问题：

1. **Thought 如何表示？**  
   可以是一行算式、一个写作计划、一个填字候选。

2. **如何生成候选 thought？**  
   可以独立采样，也可以用 propose prompt 顺序生成。

3. **如何评估候选 thought？**  
   让 LM 判断可行性、打分、投票，或用任务验证器。

4. **用什么搜索算法？**  
   论文使用 BFS 和 DFS，保留最有希望的状态，必要时回溯。

---

## 四、实验任务

论文选择了三个需要规划或搜索的任务：

| 任务 | Thought 粒度 | 搜索方式 |
|---|---|---|
| Game of 24 | 一步算式变换 | BFS |
| Creative Writing | 写作计划/段落构思 | BFS |
| Mini Crosswords | 单词填充候选 | DFS + 回溯 |

---

## 五、关键结果

### 1. Game of 24

GPT-4 + CoT 在 Game of 24 上成功率很低，而 ToT 明显提升：

- CoT 约 4%。
- CoT-SC 约 9%。
- ToT b=1 达到 45%。
- ToT b=5 达到 74%。

这说明在需要探索和回退的任务里，单链推理远不如树搜索。

### 2. Creative Writing

ToT 先生成多个写作计划，再生成文章。GPT-4 评分和人工偏好都显示 ToT 比 CoT 更连贯。

### 3. Mini Crosswords

ToT 使用 DFS 和剪枝，在填字任务上显著提升 word-level 和 game-level 表现。但论文也指出，剪枝启发式会影响最终表现。

---

## 六、与 Agent 的关系

ToT 本身不是环境交互 Agent，但它提供了 Agent 规划层的重要形式：

```text
多个候选计划
  ↓
自评估 / 外部评估
  ↓
搜索、剪枝、回溯
  ↓
选择可执行路径
```

后来的 LATS、Tree Search Agent、多智能体辩论、planner-executor 架构，都可以看成 ToT 思想的延伸。

---

## 七、局限

1. **成本高**：需要多次生成和评估，token 与调用成本远高于 CoT。
2. **依赖评估器质量**：LM 自评估不一定可靠。
3. **任务需要可分解**：不是所有问题都有清晰 thought 粒度。
4. **搜索启发式难设计**：不同任务需要不同 prompt 和剪枝策略。
5. **未直接处理外部环境反馈**：ToT 偏内部思考搜索，不是完整行动循环。

---

## 八、为什么重要

ToT 把 LLM 推理从“生成文本”推进到“搜索状态空间”。它提示我们：对难题而言，关键不是让模型一次说对，而是给模型一个能探索、比较、回退的结构。

这对 Agent 很关键，因为复杂任务通常不是线性执行，而是不断做计划分支、试错、验证和重规划。

---

## 九、对 Agent 的启发

- 对高风险任务，不要只采样一条计划，应生成多个候选计划并评估。
- 搜索宽度、深度和验证器强度是成本-效果权衡的核心。
- ToT 适合放在 Agent 的 planner 层，而 ReAct 适合放在 executor loop。
- 如果有外部可验证器，应优先用验证器评估 thought，而不是只靠 LLM 自评。

---

## 参考 / 延伸阅读

- 论文：[Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
- 相关：[[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]
