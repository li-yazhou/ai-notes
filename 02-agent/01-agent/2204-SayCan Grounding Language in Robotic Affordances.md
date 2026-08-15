---
type: paper
paper_id: arxiv-2204.01691
title: "Do As I Can, Not As I Say: Grounding Language in Robotic Affordances"
arxiv: https://arxiv.org/abs/2204.01691
year: 2022
updated: 2026-06-28
status: summarized
primary_category: embodied-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/embodied-agent
  - agent/reasoning-planning
  - env/robot
  - year/2022
  - priority/p1
  - read/skim
---

# SayCan：把语言模型规划落到机器人可执行动作上

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2204.01691
> 项目：https://say-can.github.io/
> 发表：2022 ｜ 作者：Michael Ahn, Anthony Brohan, Noah Brown 等

---

## 一、一句话概括

**SayCan** 将大语言模型的高层语义规划与机器人低层技能的可执行性评分结合起来，让机器人选择“既合理、又做得到”的动作。

它的核心不是“模型想做什么”，而是“模型想做且当前机器人能做什么”。

---

## 二、核心问题

LLM 知道很多常识，例如“清理洒出的水要找毛巾”。但机器人在具体环境里可能：

- 没有毛巾。
- 够不到桌子。
- 当前技能集中没有相关动作。
- 执行动作的成功概率很低。

因此，纯语言规划会产生不可执行方案。SayCan 用 affordance grounding 解决这个问题。

---

## 三、方法设计

SayCan 对每个候选自然语言动作计算两个分数：

```text
语言模型分数：这个动作对完成任务是否有意义
技能价值函数分数：这个动作在当前环境中是否可执行
```

然后选择综合分数最高的动作：

```text
action_score = P_LM(action | task, history) × P_affordance(success | state, action)
```

LLM 提供任务常识，机器人技能价值函数提供物理可行性约束。

---

## 四、为什么重要

SayCan 是 Embodied Agent 方向的关键论文，说明 Agent 行动必须被环境能力约束。

对软件 Agent 也有类比意义：

- LLM 可能想调用某个工具，但工具未授权。
- LLM 可能想修改某个系统，但当前环境不可写。
- LLM 可能给出计划，但执行器没有相应能力。

所以 Agent 系统需要把“可执行性”作为决策信号，而不是只做语言层规划。

---

## 五、局限与启发

局限：

- 依赖预训练低层技能，不能凭空创造新动作。
- 环境覆盖有限，泛化到开放世界仍难。
- 高层规划仍可能受 LLM 幻觉影响。

启发：

- 工具型 Agent 也需要 affordance：工具权限、状态、成本、风险都应参与动作选择。
- 好的 planner 不只是“想出合理步骤”，还要知道当前 executor 能不能做。

---

## 参考 / 延伸阅读

- 论文：[Do As I Can, Not As I Say: Grounding Language in Robotic Affordances](https://arxiv.org/abs/2204.01691)
- 项目：[SayCan](https://say-can.github.io/)

