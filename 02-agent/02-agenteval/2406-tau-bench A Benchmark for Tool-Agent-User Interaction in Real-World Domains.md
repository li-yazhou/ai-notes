---
type: paper
paper_id: arxiv-2406.12045
title: "tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains"
arxiv: https://arxiv.org/abs/2406.12045
year: 2024
updated: 2026-06-28
status: summarized
primary_category: agent-benchmark
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/tool-use
  - eval/agent-benchmark
  - eval/reliability
  - env/business
  - year/2024
  - priority/p0
  - read/deep
---

# τ-bench：评测工具 Agent 与用户的真实交互

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2406.12045
> 发表：2024 ｜ 作者：Shunyu Yao, Noah Shinn, Pedram Razavi, Karthik Narasimhan

---

## 一、一句话概括

**τ-bench** 评测语言 Agent 在真实业务领域中与模拟用户多轮对话、调用 API 工具、遵守领域规则并完成数据库状态变更的能力。

它的重要性在于：把工具调用评测从“函数参数对不对”推进到“在真实用户交互和业务规则下是否可靠完成任务”。

---

## 二、核心动机

现实中的工具 Agent 通常不是直接收到完整指令就调用 API，而是要处理：

- 用户表达不完整。
- 用户会追加、修改或纠正需求。
- 业务规则限制很多。
- 工具调用会改变数据库状态。
- 最终成功取决于状态是否正确，而不只是回复是否好看。

τ-bench 关注的正是这类动态交互。

---

## 三、评测框架

基本流程：

```text
模拟用户提出目标
  ↓
Agent 与用户多轮对话
  ↓
Agent 根据领域政策调用 API 工具
  ↓
数据库状态发生变化
  ↓
比较最终数据库状态与标注目标状态
```

这意味着 τ-bench 不是只看最终文本，而是看 Agent 是否真的把业务状态改对。

---

## 四、任务领域

论文构造了真实业务风格领域，例如：

| 领域 | 典型任务 |
|---|---|
| Retail | 订单查询、退货、换货、退款、商品替换 |
| Airline | 航班预订、改签、取消、政策约束处理 |

这些任务要求 Agent 同时理解用户意图、调用工具、遵守政策，并避免越权操作。

---

## 五、核心指标：pass^k

τ-bench 提出用 **pass^k** 衡量 Agent 的可靠性。

直觉是：同一个任务重复运行 k 次，Agent 是否每次都能成功？

这很重要，因为实际部署中，“偶尔成功”远远不够。用户需要的是稳定一致地成功。

---

## 六、关键结果

论文发现，即使是较强的函数调用模型，也表现不稳定：

- GPT-4o 等 state-of-the-art function calling agents 成功率低于 50%。
- 多次运行的一致性更差，retail 领域 pass^8 低于 25%。

这说明当前工具 Agent 的瓶颈不只是 API schema 理解，而是：

- 规则遵守。
- 对话状态维护。
- 多步业务流程。
- 工具结果解释。
- 一致性和可重复性。

---

## 七、为什么重要

τ-bench 很适合评估将来企业级 Agent 的核心问题：

```text
用户交互 + 业务规则 + 工具调用 + 数据库状态 + 多次可靠性
```

它比单次函数调用 benchmark 更接近客服、运营、旅行、金融等真实应用。

---

## 八、局限

1. **用户是模拟的**：模拟用户可控，但不能完全代表真实用户行为。
2. **领域有限**：主要覆盖少数结构化业务场景。
3. **评测依赖目标状态标注**：复杂任务的目标状态设计成本较高。
4. **未覆盖高风险安全场景**：例如欺诈、隐私、恶意用户、合规审计。
5. **对话质量不是主指标**：礼貌、解释、用户体验可能没有被充分衡量。

---

## 九、对 Agent 的启发

- 工具 Agent 应把“政策约束”作为一等公民，而不是只看函数签名。
- 评测要检查数据库最终状态，不能只看模型回复。
- 多次运行一致性比单次成功率更接近部署可靠性。
- 真实业务 Agent 需要显式状态机、权限控制和操作确认机制。

---

## 参考 / 延伸阅读

- 论文：[τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains](https://arxiv.org/abs/2406.12045)
- 相关：[[2302-Toolformer Language Models Can Teach Themselves to Use Tools]]
- 相关：[[2308-AgentBench Evaluating LLMs as Agents]]

