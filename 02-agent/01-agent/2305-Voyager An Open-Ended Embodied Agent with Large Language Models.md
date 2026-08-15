---
type: paper
paper_id: arxiv-2305.16291
title: "Voyager: An Open-Ended Embodied Agent with Large Language Models"
arxiv: https://arxiv.org/abs/2305.16291
year: 2023
updated: 2026-06-28
status: summarized
primary_category: agent-loop-memory
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/memory
  - agent/skill-learning
  - agent/embodied-agent
  - env/game
  - year/2023
  - priority/p0
  - read/deep
---

# Voyager：在 Minecraft 中开放式终身学习的 LLM Agent

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2305.16291
> 项目主页：https://voyager.minedojo.org/
> 发表：2023 ｜ 作者：Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke Zhu, Linxi Fan, Anima Anandkumar

---

## 一、一句话概括

**Voyager** 是一个基于 GPT-4 的 Minecraft 具身终身学习 Agent。它不靠模型微调，而是通过自动课程、技能库和迭代式代码生成，在开放世界中不断探索、学习技能、复用技能，并完成越来越复杂的任务。

它的重要性在于：把 Agent 从“完成给定任务”推进到“开放式探索 + 终身技能积累”。

---

## 二、核心问题

许多 Agent benchmark 给定明确任务和终止条件，但真实开放环境中，Agent 还需要：

- 自己决定下一步探索什么。
- 从失败中修正程序。
- 把成功经验沉淀成可复用技能。
- 避免每次从零开始。
- 在新世界中迁移已有技能。

Voyager 选择 Minecraft 作为测试环境，因为它有复杂物品、工具、合成链和长程探索目标。

---

## 三、系统三大组件

### 1. Automatic Curriculum

自动课程负责给 Agent 提出当前合适的探索目标。目标不是固定的“通关”，而是最大化新发现和技能增长。

它会根据当前状态生成任务，例如：

- 收集某种新材料。
- 制作某个工具。
- 探索新地形。
- 解锁 tech tree 的下一步。

### 2. Skill Library

Voyager 不直接把经验只存在聊天历史里，而是把成功行为保存为可执行代码技能。

技能库的特点：

- 持续增长。
- 可检索。
- 可组合。
- 可解释。
- 在新 Minecraft 世界中可复用。

这解决了长期 Agent 的关键问题：**经验要变成可调用能力，而不只是文字记忆。**

### 3. Iterative Prompting

Voyager 让 GPT-4 生成代码执行任务，如果执行失败，则把环境反馈、错误信息、自我验证结果重新喂给模型，让它修复代码。

循环如下：

```text
生成任务
  ↓
检索相关技能
  ↓
生成代码
  ↓
执行代码
  ↓
根据环境反馈和错误修复
  ↓
成功后写入技能库
```

---

## 四、实验结果

论文报告 Voyager 在 Minecraft 中表现显著优于 prior SOTA：

- 获得 **3.3x** 更多独特物品。
- 行走距离 **2.3x** 更长。
- 解锁关键 tech tree milestone 最快提升到 **15.3x**。
- 学到的技能库可以迁移到新世界，解决从零开始的新任务。

这些结果说明：开放式探索中，长期技能积累比一次性规划更重要。

---

## 五、与前序论文的关系

| 论文 | Voyager 继承/扩展的点 |
|---|---|
| ReAct | 根据环境反馈迭代行动 |
| Reflexion | 从失败中改进后续尝试 |
| Generative Agents | 长期记忆与行为连续性 |
| Toolformer / MRKL | 把外部执行器作为能力扩展 |

Voyager 的独特之处是：它把记忆落成了**可执行技能代码**，让 Agent 的能力可以复利增长。

---

## 六、为什么重要

1. **开放式 Agent 的代表作**：没有固定单任务，而是持续探索。
2. **技能库范式清晰**：经验以代码形式保存，便于复用和组合。
3. **环境反馈驱动修复**：错误不只是失败信号，而是代码改进输入。
4. **证明 LLM + 执行环境 + 记忆库可以形成终身学习雏形**。

---

## 七、局限

1. **强依赖 GPT-4 和 Minecraft API**：迁移到真实机器人或网页环境并不直接。
2. **技能质量控制困难**：错误技能进入库后可能污染后续行为。
3. **安全问题更突出**：能生成和执行代码的 Agent 需要沙箱和权限控制。
4. **开放式评测难**：探索多样性、长期成长和泛化能力比静态准确率更难评估。
5. **世界模型有限**：仍依赖环境 API 和反馈，缺少真正的物理理解。

---

## 八、对 Agent 的启发

- 长期 Agent 的记忆最好沉淀成可执行技能，而不是纯文本摘要。
- 经验库要支持检索、组合、去重和验证。
- 自动课程是开放式学习的关键，没有目标生成器就容易停在局部行为。
- 代码执行型 Agent 必须把错误日志、环境反馈和验证结果纳入修复循环。

---

## 参考 / 延伸阅读

- 论文：[Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)
- 项目：[voyager.minedojo.org](https://voyager.minedojo.org/)
- 相关：[[2303-Reflexion Language Agents with Verbal Reinforcement Learning]]
- 相关：[[2304-Generative Agents Interactive Simulacra of Human Behavior]]
