---
type: paper
paper_id: arxiv-2305.14325
title: "Improving Factuality and Reasoning in Language Models through Multiagent Debate"
arxiv: https://arxiv.org/abs/2305.14325
year: 2023
updated: 2026-06-28
status: summarized
primary_category: multi-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/multi-agent
  - method/multi-agent-debate
  - agent/reasoning-planning
  - year/2023
  - priority/p1
  - read/skim
---

# Multiagent Debate：用多模型辩论提升事实性与推理

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2305.14325
> 项目：https://composable-models.github.io/llm_debate/
> 发表：2023 ｜ 作者：Yilun Du, Shuang Li, Antonio Torralba 等

---

## 一、一句话概括

**Multiagent Debate** 让多个语言模型实例提出各自答案和推理，并通过多轮辩论收敛到共同最终答案，从而提升数学、策略推理和事实性。

它是“社会化推理”在 LLM 上的代表方法。

---

## 二、核心流程

```text
多个 Agent 独立回答
  ↓
展示各自推理
  ↓
多轮互相批评和修正
  ↓
形成最终答案
```

它可以直接应用于黑盒模型，不需要训练新模型。

---

## 三、为什么有效

多 Agent debate 的直觉是：

- 单个模型可能犯错，但不同采样/实例可能犯不同错误。
- 让模型看到其他推理路径，可以发现自己忽略的问题。
- 多轮辩论可减少明显幻觉和逻辑漏洞。

这和 Self-Consistency 类似，但不是只投票最终答案，而是让推理过程互相影响。

---

## 四、与多智能体系统的关系

Debate 是一种特殊多 Agent 协作模式：

| 模式 | 目标 |
|---|---|
| Debate | 通过分歧和批评提升答案质量 |
| Role-play | 通过分工完成复杂任务 |
| Orchestrator-worker | 中央规划，子 Agent 执行 |
| Reviewer | 生成者和审查者分离 |

Debate 更适合推理、事实核查、方案比较，不一定适合所有执行型任务。

---

## 五、局限与启发

局限：

- 多个 Agent 可能共享同一模型偏差。
- 辩论可能变成冗长重复，成本较高。
- 没有外部事实源时，辩论不保证正确。

启发：

- 高风险答案可以引入独立 reviewer 或 adversarial critic。
- 多 Agent 应避免只“互相附和”，需要保留真实分歧和证据。

---

## 参考 / 延伸阅读

- 论文：[Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325)
- 相关：[[2203-Self-Consistency Improves Chain of Thought Reasoning in Language Models]]

