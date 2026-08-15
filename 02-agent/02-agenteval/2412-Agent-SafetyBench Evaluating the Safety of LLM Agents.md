---
type: paper
paper_id: arxiv-2412.14470
title: "Agent-SafetyBench: Evaluating the Safety of LLM Agents"
arxiv: https://arxiv.org/abs/2412.14470
year: 2024
updated: 2026-06-28
status: summarized
primary_category: safety-reliability
priority: p1
read_type: skim
tags:
  - paper
  - paper/eval
  - paper/safety
  - eval/safety
  - agent/safety
  - eval/agent-benchmark
  - year/2024
  - priority/p1
  - read/skim
---

# Agent-SafetyBench：系统评测 LLM Agent 安全性

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2412.14470
> 项目：https://github.com/thu-coai/Agent-SafetyBench/
> 发表：2024 ｜ 作者：THU CoAI 等

---

## 一、一句话概括

**Agent-SafetyBench** 是一个综合 LLM Agent 安全评测 benchmark，包含 349 个交互环境和 2,000 个测试用例，覆盖 8 类安全风险和 10 类常见失败模式。

它的重要性在于：把 Agent 安全从零散红队案例推进到结构化 benchmark。

---

## 二、核心动机

LLM 变成 Agent 后，安全问题不再只是输出文本：

- 可以调用工具。
- 可以与环境交互。
- 可以产生真实副作用。
- 可以在多轮任务中逐步偏离安全边界。

因此，需要专门面向 Agent 的安全评测，而不是复用聊天模型安全集。

---

## 三、Benchmark 设计

Agent-SafetyBench 包含：

- 349 个交互环境。
- 2,000 个测试用例。
- 8 类安全风险。
- 10 类不安全交互中常见失败模式。
- 对 16 个流行 LLM Agent 的评估。

它同时分析 failure mode 和 helpfulness，避免把安全和可用性割裂。

---

## 四、关键发现

论文发现，没有一个被评估的 Agent 安全分数超过 60%。作者总结当前 LLM Agent 的两个基础安全缺陷：

- 缺乏鲁棒性。
- 缺乏风险意识。

此外，仅依赖防御 prompt 可能不足以解决安全问题。

---

## 五、局限与启发

局限：

- 安全风险开放且不断变化，benchmark 需要持续更新。
- 不同 Agent 工具集和权限差异会影响分数可比性。
- 自动评估安全仍有偏差风险。

启发：

- Agent 安全需要系统级防护：权限、沙箱、审计、确认、回滚。
- 安全评测应成为 Agent 上线前的固定环节，而不是事后补丁。

---

## 参考 / 延伸阅读

- 论文：[Agent-SafetyBench: Evaluating the Safety of LLM Agents](https://arxiv.org/abs/2412.14470)
- 项目：[Agent-SafetyBench](https://github.com/thu-coai/Agent-SafetyBench/)
- 相关：[[2410-AgentHarm A Benchmark for Measuring Harmfulness of LLM Agents]]

