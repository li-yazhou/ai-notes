---
type: paper
paper_id: arxiv-1905.00537
title: "SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems"
arxiv: https://arxiv.org/abs/1905.00537
year: 2019
updated: 2026-06-28
status: summarized
primary_category: model-benchmark
priority: p2
read_type: reference
tags:
  - paper
  - paper/eval
  - eval/model-benchmark
  - eval/nlu
  - year/2019
  - priority/p2
  - read/reference
---

# SuperGLUE：更难的通用语言理解评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/1905.00537
> 项目：https://super.gluebenchmark.com/
> 发表：2019 ｜ 作者：Alex Wang, Yada Pruksachatkun, Nikita Nangia 等

---

## 一、一句话概括

**SuperGLUE** 是 GLUE 的升级版，在 GLUE 被模型快速追平甚至超过非专家人类后，提出一组更难的语言理解任务、工具包和公开 leaderboard。

它体现了模型评测的一条基本规律：热门 benchmark 会被迅速饱和，评测必须不断加难。

---

## 二、核心动机

GLUE 发布后，预训练和迁移学习方法快速提升，榜单分数很快超过非专家人类水平，导致继续区分模型能力的空间变小。

SuperGLUE 因此选择更难、更少捷径、更需要推理的任务，希望延长评测寿命。

---

## 三、评测特点

SuperGLUE 延续 GLUE 的统一评测思想，但任务更具挑战性：

- 更强调阅读理解和推理。
- 数据集规模普遍更小，降低纯数据拟合优势。
- 包含自然语言推断、常识推理、指代消解、问答等任务。

---

## 四、为什么重要

SuperGLUE 的意义不只是“GLUE Plus”，而是说明：

```text
评测集必须跟随模型能力升级
否则很快无法区分前沿模型
```

这条逻辑后来在 MMLU → GPQA/HLE、WebArena → VisualWebArena/OSWorld 等方向反复出现。

---

## 五、局限与启发

局限：

- 仍然是静态文本评测，不覆盖 Agent 行动能力。
- 后来同样被大模型快速刷高。
- 单一榜单分数仍有过度简化问题。

启发：

- 大模型评测需要动态更新和防污染机制。
- Agent 评测也会经历“提出-刷高-升级”的循环。

---

## 参考 / 延伸阅读

- 论文：[SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems](https://arxiv.org/abs/1905.00537)
- 项目：[SuperGLUE](https://super.gluebenchmark.com/)
- 相关：[[1804-GLUE A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding]]

