---
type: paper
paper_id: arxiv-2310.11667
title: "SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents"
arxiv: https://arxiv.org/abs/2310.11667
year: 2023
updated: 2026-06-28
status: summarized
primary_category: multi-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/multi-agent
  - agent/social-intelligence
  - eval/agent-benchmark
  - env/social
  - year/2023
  - priority/p1
  - read/skim
---

# SOTOPIA：评测语言 Agent 的社会智能

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2310.11667
> 发表：2023 ｜ 作者：Xuhui Zhou, Hao Zhu, Akhila Yerukola 等

---

## 一、一句话概括

**SOTOPIA** 构建开放式社会互动环境，让 LLM Agent 在角色扮演场景中协商、合作、竞争，并用 SOTOPIA-Eval 评估其社会智能。

它把 Agent 评测从任务完成扩展到社会互动能力。

---

## 二、核心问题

很多 Agent benchmark 评估的是：

- 是否完成网页任务。
- 是否修复代码。
- 是否调用正确工具。

但真实助手还需要社会智能：

- 理解他人目标。
- 沟通和谈判。
- 在冲突中保持策略。
- 遵守社会常识和边界。

SOTOPIA 试图评估这些能力。

---

## 三、环境与评测

SOTOPIA 中，Agent 会在不同社会场景中扮演角色，并与另一个 Agent 或人类互动。任务可能涉及协作、交换、竞争、说服等。

SOTOPIA-Eval 以更整体的方式评估：

- 目标完成。
- 社会常识。
- 沟通策略。
- 角色一致性。
- 互动质量。

---

## 四、关键发现

论文发现，不同模型在社会智能上差异明显。GPT-4 在 SOTOPIA-hard 子集上仍显著低于人类，尤其在社会常识推理和策略沟通上存在困难。

这说明语言流畅不等于社会智能成熟。

---

## 五、局限与启发

局限：

- 社会互动评测主观性强。
- LLM-as-judge 可能引入偏差。
- 模拟互动与真实人类关系仍有差距。

启发：

- 评测 Agent 不能只看任务成功，还要看互动方式。
- 面向用户的 Agent 需要评估礼貌、边界、沟通策略和社会后果。

---

## 参考 / 延伸阅读

- 论文：[SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents](https://arxiv.org/abs/2310.11667)
- 相关：[[2304-Generative Agents Interactive Simulacra of Human Behavior]]

