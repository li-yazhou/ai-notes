---
type: paper
paper_id: arxiv-2303.11366
title: "Reflexion: Language Agents with Verbal Reinforcement Learning"
arxiv: https://arxiv.org/abs/2303.11366
year: 2023
updated: 2026-06-28
status: summarized
primary_category: agent-loop-memory
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/react-loop
  - agent/reflection
  - agent/memory
  - method/reflection
  - year/2023
  - priority/p0
  - read/deep
---

# Reflexion：用语言反思让 Agent 从失败中学习

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.11366
> 发表：2023 ｜ 作者：Noah Shinn 等

---

## 一、一句话概括

**Reflexion** 提出一种“语言形式的强化学习”：Agent 执行任务失败后，不更新模型参数，而是把环境反馈、失败轨迹和自我总结转成一段自然语言反思，写入记忆，在下一次尝试中作为经验使用。

它把 Agent 从“一次性执行器”推进到“能跨 trial 总结经验、修正策略的学习体”。

---

## 二、核心问题

ReAct 让模型能边想边行动，但一个 ReAct Agent 失败后通常会重新开始，过去的错误没有被系统化利用。

传统强化学习可以从 reward 中学习，但对 LLM Agent 来说：

- 训练成本高。
- 需要大量样本。
- 策略更新不透明。
- 很多任务只有稀疏的成功/失败反馈。

Reflexion 的洞察是：**对语言模型来说，最自然的学习介质也是语言。**

---

## 三、系统结构

Reflexion 由三个核心模块组成：

| 模块 | 作用 |
|---|---|
| Actor | 执行动作或生成答案，常用 ReAct / CoT 作为基础策略 |
| Evaluator | 根据环境、测试用例或 LLM 判断成功/失败 |
| Self-Reflection | 把失败轨迹和反馈总结成自然语言经验 |

记忆分成两类：

- **短期记忆**：当前 trial 的轨迹。
- **长期记忆**：过去失败后的反思总结。

循环如下：

```text
执行任务
  ↓
Evaluator 判断成功/失败
  ↓
失败则生成 self-reflection
  ↓
写入长期记忆
  ↓
下一轮 Actor 带着经验重试
```

---

## 四、实验任务

论文覆盖三类 Agent 场景：

| 类型 | 任务 | 说明 |
|---|---|---|
| 序列决策 | ALFWorld | 长轨迹文本环境决策 |
| 搜索问答 | HotPotQA | 多跳 QA，可结合 ReAct 检索 |
| 代码生成 | HumanEval、MBPP、LeetcodeHard | 利用测试结果反思和修复代码 |

---

## 五、关键结果

- ALFWorld：ReAct + Reflexion 完成 130 / 134 个任务，显著优于纯 ReAct。
- HotPotQA：Reflexion 相比基线带来明显提升，论文报告约 20% 改善。
- HumanEval Python：Reflexion 达到 91.0 pass@1，论文中超过当时强基线。
- HumanEval Rust 子集：去掉 self-reflection 后性能下降，说明不是简单重试带来的提升。

这些结果说明：**语言反思能够把稀疏 reward 放大成更可用的经验信号。**

---

## 六、为什么它像“强化学习”，又不是传统 RL

传统 RL 更新参数：

```text
reward → gradient update → policy changes
```

Reflexion 更新上下文：

```text
failure → verbal reflection → memory changes → behavior changes
```

它没有改模型权重，但改变了下一轮决策条件。对 LLM Agent 来说，这种“上下文层面的策略优化”更轻、更可解释，也更容易接入现有系统。

---

## 七、局限

1. **容易陷入局部最优**：如果反思方向错，后续会持续带偏。
2. **依赖 evaluator**：反馈信号不准时，反思也会错。
3. **记忆容量有限**：论文中通常只保留最近几条反思，长周期任务需要更复杂记忆管理。
4. **不是所有任务都有效**：论文提到 WebShop 这类需要多样策略的任务上提升不明显。
5. **反思可解释但不保证真实**：模型可能写出听起来合理但并非真正失败原因的总结。

---

## 八、历史地位

Reflexion 是 Agent 研究里“记忆与自我改进”路线的代表。它补上了 ReAct 的一个缺口：ReAct 能在一次轨迹中根据 Observation 修正，Reflexion 能在多次尝试之间积累经验。

```text
CoT：一步步想
ReAct：边想边行动
Reflexion：失败后总结，下次更好
```

---

## 九、对 Agent 的启发

- 每个 Agent 系统都应该记录失败轨迹和失败原因。
- 反思要尽量结构化，例如：错误动作、错误原因、下次策略、验证标准。
- 反思不能无限追加，需要去重、压缩、过期和检索。
- evaluator 是关键模块，最好用可验证信号而不是纯主观判断。

---

## 参考 / 延伸阅读

- 论文：[Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]
- 相关：[[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
