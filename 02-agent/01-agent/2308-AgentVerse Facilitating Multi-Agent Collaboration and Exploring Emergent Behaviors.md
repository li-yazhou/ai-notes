---
type: paper
paper_id: arxiv-2308.10848
title: "AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors"
arxiv: https://arxiv.org/abs/2308.10848
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
  - agent/social-simulation
  - year/2023
  - priority/p1
  - read/skim
---

# AgentVerse：多智能体协作框架与涌现行为探索

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2308.10848
> 项目：https://github.com/OpenBMB/AgentVerse
> 发表：2023 ｜ 作者：Chen Qian, Wei Liu, Hongzhang Liu 等

---

## 一、一句话概括

**AgentVerse** 是一个多智能体协作框架，允许动态组织多个 LLM Agent 完成任务，并研究协作过程中出现的社会行为。

它的重要性在于：将多智能体从固定双人角色扩展到更灵活的群体协作。

---

## 二、核心思想

AgentVerse 的出发点是：现实任务常常需要群体协作，而不是单个 Agent 独立完成。

系统关注：

- 如何组成 Agent 群体。
- 如何分配角色和任务。
- 如何让群体协作优于单 Agent。
- 协作中会出现哪些正面或负面社会行为。

---

## 三、典型流程

多智能体协作通常包括：

```text
任务理解
  ↓
Agent 招募 / 角色分配
  ↓
群体讨论与行动
  ↓
结果汇总
  ↓
反馈与调整
```

AgentVerse 强调根据任务动态调整 group composition，而不是永远固定几个角色。

---

## 四、为什么重要

AgentVerse 提供了研究多 Agent 的几个关键问题：

- 群体是否真的比单体更强？
- 什么任务适合多 Agent？
- 群体中会不会出现无效争论、从众、角色失效？
- 如何利用积极行为、抑制消极行为？

这些问题对后来的 AutoGen、MetaGPT、ChatDev 以及企业内多 Agent 编排都有参考价值。

---

## 五、局限与启发

局限：

- 涌现行为分析偏探索性，工程可控性仍不足。
- 多 Agent 会显著增加成本和复杂度。
- 群体表现依赖角色设计和通信协议。

启发：

- 多 Agent 不是越多越好，应根据任务动态组织。
- 群体协作必须有汇总、裁决和终止机制。
- 评测多 Agent 时，要比较强单 Agent baseline。

---

## 参考 / 延伸阅读

- 论文：[AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors](https://arxiv.org/abs/2308.10848)
- 项目：[OpenBMB/AgentVerse](https://github.com/OpenBMB/AgentVerse)
- 相关：[[2308-AutoGen Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework]]

