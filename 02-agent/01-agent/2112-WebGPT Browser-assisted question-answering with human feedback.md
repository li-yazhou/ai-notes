---
type: paper
paper_id: arxiv-2112.09332
title: "WebGPT: Browser-assisted question-answering with human feedback"
arxiv: https://arxiv.org/abs/2112.09332
year: 2021
updated: 2026-06-28
status: summarized
primary_category: web-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/web-agent
  - agent/browsing
  - method/rlhf
  - env/web
  - year/2021
  - priority/p1
  - read/skim
---

# WebGPT：用浏览器和人类反馈训练可引用的问答 Agent

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2112.09332
> 发表：2021 ｜ 作者：Reiichiro Nakano 等（OpenAI）

---

## 一、一句话概括

**WebGPT** 让 GPT-3 在文本浏览器环境中搜索、打开网页、收集引用并回答长问题，再用人类偏好训练提升答案质量。

它是“浏览器辅助问答 Agent”的早期代表：模型不只靠参数记忆回答，而是先查资料、再带引用回答。

---

## 二、核心方法

WebGPT 的任务流程是：

```text
用户问题 → 搜索网页 → 浏览页面 → 收集 references → 生成长答案
```

训练方式包括：

- 让人类演示如何在浏览器环境中查资料并回答。
- 用行为克隆训练模型模仿人类浏览和回答。
- 训练 reward model 预测人类偏好。
- 用 rejection sampling 选择更优答案。

论文要求模型给出引用，降低人类评估事实准确性的成本。

---

## 三、关键结果

在 ELI5 长问答任务上，最佳模型答案：

- 相比人类示范者，约 56% 情况下更受人类偏好。
- 相比 Reddit 最高赞答案，约 69% 情况下更受偏好。

这说明“检索 + 浏览 + 引用 + 人类反馈”可以显著改善开放问答质量。

---

## 四、为什么重要

WebGPT 是后续 Browse Agent、Deep Research、RAG Agent 的重要前身。它奠定了几个关键思想：

- 外部信息源比纯参数记忆更可靠。
- Agent 需要可审计引用，而不是只输出答案。
- 人类反馈可以用于优化整个查证-回答流程。
- 浏览轨迹本身是可训练、可评估的数据。

---

## 五、局限与启发

局限：

- 主要是文本浏览器，不等同真实网页 GUI 操作。
- 引用存在不充分或误用风险。
- 人类偏好不完全等于事实正确。
- 搜索环境和网页内容会随时间变化。

启发：

- 研究型 Agent 要把“证据链”作为输出的一部分。
- 问答系统应评估引用质量、证据覆盖和最终答案，而不是只评文本流畅度。

---

## 参考 / 延伸阅读

- 论文：[WebGPT: Browser-assisted question-answering with human feedback](https://arxiv.org/abs/2112.09332)
- 相关：[[2307-WebArena A Realistic Web Environment for Building Autonomous Agents]]

