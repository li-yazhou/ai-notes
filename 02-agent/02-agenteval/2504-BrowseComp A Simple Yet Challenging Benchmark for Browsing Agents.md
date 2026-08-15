---
type: paper
paper_id: arxiv-2504.12516
title: "BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents"
arxiv: https://arxiv.org/abs/2504.12516
year: 2025
updated: 2026-06-28
status: summarized
primary_category: web-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/web-agent
  - agent/browsing
  - eval/agent-benchmark
  - env/web
  - year/2025
  - priority/p1
  - read/skim
---

# BrowseComp：面向浏览 Agent 的简洁高难信息检索评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2504.12516
> 项目：https://github.com/openai/simple-evals
> 发表：2025 ｜ 作者：OpenAI

---

## 一、一句话概括

**BrowseComp** 是一个用于评测浏览 Agent 的高难 benchmark，包含 1,266 个需要持续互联网导航、查找隐蔽且交织信息的问题，答案短且易验证。

它关注浏览 Agent 的核心能力：持续、有创造性地找到难找的信息。

---

## 二、核心设计

BrowseComp 的题目特点：

- 需要真正浏览网页，而不是凭记忆回答。
- 信息通常分散、隐蔽、需要多步搜索。
- 最终答案很短，便于自动校验。
- 避免开放长答案评测的主观性。

论文把 BrowseComp 类比为编程竞赛对 coding agent 的作用：不完整，但能测核心能力。

---

## 三、为什么重要

很多浏览 Agent 在简单搜索题上表现不错，但真实研究型任务经常需要：

- 换关键词。
- 交叉验证。
- 跳转多站点。
- 从线索中反推目标。
- 长时间坚持查找。

BrowseComp 正是测试这类“搜索毅力”和“信息侦查能力”。

---

## 四、局限与启发

局限：

- 不代表完整用户查询分布。
- 不评估长报告写作、歧义处理和用户交互。
- 网页内容变化可能影响稳定性。

启发：

- Deep Research / 浏览 Agent 不能只看最终报告质量，还要测 hard-to-find facts。
- 短答案可验证题适合作为浏览能力基础回归集。

---

## 参考 / 延伸阅读

- 论文：[BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents](https://arxiv.org/abs/2504.12516)
- 项目：[openai/simple-evals](https://github.com/openai/simple-evals)
- 相关：[[2311-GAIA a benchmark for General AI Assistants]]

