---
type: paper
paper_id: arxiv-2401.13649
title: "VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks"
arxiv: https://arxiv.org/abs/2401.13649
year: 2024
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
  - agent/multimodal
  - eval/agent-benchmark
  - env/web
  - year/2024
  - priority/p1
  - read/skim
---

# VisualWebArena：评测多模态 Web Agent 的视觉网页任务

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2401.13649
> 项目：https://jykoh.com/vwa
> 发表：2024 ｜ 作者：Jing Yu Koh, Robert Lo, Lawrence Jang 等

---

## 一、一句话概括

**VisualWebArena** 在 WebArena 思路上进一步强调视觉信息，构建需要图文理解和网页操作的真实视觉网页任务，用于评测多模态 Web Agent。

它补上了文本 DOM 评测忽视视觉界面的短板。

---

## 二、核心动机

很多网页任务不能只靠文本 DOM 完成：

- 商品图片差异。
- 图标按钮。
- 页面布局和视觉位置。
- 截图中的关键信息。
- 人类界面本来就是为视觉感知设计的。

文本 Agent 可能读到 HTML，却无法理解视觉上显而易见的信息。

---

## 三、任务要求

VisualWebArena 要求 Agent：

```text
理解自然语言指令
  ↓
处理图像 + 文本网页输入
  ↓
在网站上执行动作
  ↓
完成用户目标
```

这更接近真实浏览器自动化和电脑使用 Agent。

---

## 四、关键意义

VisualWebArena 揭示了一个重要事实：多模态模型会看图，并不等于能当网页 Agent。

Web Agent 需要综合：

- 视觉 grounding。
- DOM / 元素理解。
- 动作执行。
- 长程规划。
- 状态跟踪。

---

## 五、局限与启发

局限：

- 视觉网页任务评测成本高。
- 多模态输入增加延迟和费用。
- 视觉与 DOM 对齐仍是难点。

启发：

- 电脑/浏览器 Agent 不能只评文本网页任务。
- GUI grounding 应成为多模态 Agent 的核心指标。

---

## 参考 / 延伸阅读

- 论文：[VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks](https://arxiv.org/abs/2401.13649)
- 项目：[VisualWebArena](https://jykoh.com/vwa)
- 相关：[[2307-WebArena A Realistic Web Environment for Building Autonomous Agents]]

