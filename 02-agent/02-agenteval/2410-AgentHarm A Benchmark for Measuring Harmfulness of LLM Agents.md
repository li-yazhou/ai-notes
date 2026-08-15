---
type: paper
paper_id: arxiv-2410.09024
title: "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents"
arxiv: https://arxiv.org/abs/2410.09024
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
  - year/2024
  - priority/p1
  - read/skim
---

# AgentHarm：评测 LLM Agent 的有害任务执行风险

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2410.09024
> 数据：https://huggingface.co/datasets/ai-safety-institute/AgentHarm
> 发表：2024 ｜ 作者：UK AI Safety Institute 等

---

## 一、一句话概括

**AgentHarm** 是一个评测 LLM Agent 有害性和越狱风险的 benchmark，包含 110 个明确恶意的多步 Agent 任务，覆盖欺诈、网络犯罪、骚扰等 11 类危害。

它关注的问题是：Agent 不只是会说坏话，还可能真的执行多步有害行动。

---

## 二、核心动机

传统 jailbreak 研究多关注聊天模型是否输出违规内容。但 Agent 有工具和多步执行能力，风险更高：

- 可能收集信息。
- 可能调用工具。
- 可能完成攻击流程。
- 可能在越狱后仍保持任务能力。

AgentHarm 因此评测“拒绝有害任务”和“被越狱后是否能执行有害多步任务”。

---

## 三、数据与任务

AgentHarm 包含：

- 110 个显式恶意 Agent 任务。
- 扩增后 440 个任务。
- 11 类危害类别。
- 多步 agentic request，而不是单轮违规问答。

评分不仅看模型是否拒绝，也看被攻击后是否还能连贯完成恶意任务。

---

## 四、关键发现

论文发现：

- 一些领先 LLM 对恶意 Agent 请求出人意料地顺从。
- 简单通用 jailbreak 模板可适配并有效攻击 Agent。
- 越狱后 Agent 能保持多步任务能力并执行连贯有害行为。

这说明 Agent 安全不能只靠普通聊天安全评测。

---

## 五、局限与启发

局限：

- 恶意任务集合无法覆盖所有攻击。
- 安全评测需要谨慎处理复现和披露边界。
- 工具真实可用性会改变风险水平。

启发：

- Agent 安全评测要覆盖任务级危害，而不是只测单句拒答。
- 工具权限、沙箱、审计和人类确认是必要防线。

---

## 参考 / 延伸阅读

- 论文：[AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents](https://arxiv.org/abs/2410.09024)
- 数据：[AgentHarm](https://huggingface.co/datasets/ai-safety-institute/AgentHarm)
- 相关：[[2309-ToolEmu Identifying the Risks of LM Agents with an LM-Emulated Sandbox]]

