---
type: paper
paper_id: arxiv-1804.07461
title: "GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding"
arxiv: https://arxiv.org/abs/1804.07461
year: 2018
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
  - year/2018
  - priority/p2
  - read/reference
---

# GLUE：自然语言理解的多任务评测基准

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/1804.07461
> 项目：https://gluebenchmark.com/
> 发表：2018 ｜ 作者：Alex Wang, Amanpreet Singh, Julian Michael 等

---

## 一、一句话概括

**GLUE** 是一个面向自然语言理解（NLU）的多任务评测基准和分析平台，用一组不同类型的语言理解任务评估模型的通用迁移能力。

它是大模型评测发展线的早期关键节点：从单任务分数，走向统一 leaderboard 和跨任务综合评估。

---

## 二、核心动机

GLUE 关注的问题是：一个 NLU 系统是否具备通用语言理解能力，而不是只在某个特定数据集上调得很好。

它把多个已有任务整合到统一评测框架中，并鼓励模型在低资源任务上通过预训练、迁移学习和多任务学习共享知识。

---

## 三、评测内容

GLUE 覆盖多种 NLU 能力：

- 句子可接受性判断。
- 情感分类。
- 语义相似度。
- 自然语言推断。
- 问题匹配。
- 释义识别。

此外，GLUE 还提供 diagnostic test suite，用于分析模型在语言现象上的具体短板。

---

## 四、为什么重要

GLUE 的历史意义在于：

- 把 NLU 评测标准化。
- 推动预训练语言模型在统一榜单上比较。
- 让“通用语言理解能力”成为可量化目标。
- 为后续 SuperGLUE、MMLU、HELM 等综合评测铺路。

---

## 五、局限与启发

局限：

- 主要是静态文本任务，不涉及工具、环境和交互。
- 很快被 BERT 等预训练模型刷高。
- 单一综合分数容易掩盖不同能力维度。

启发：

- Benchmark 一旦成为主流，就会被快速优化甚至饱和。
- Agent 评测也需要像 GLUE 一样统一接口，但必须避免只看单一分数。

---

## 参考 / 延伸阅读

- 论文：[GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding](https://arxiv.org/abs/1804.07461)
- 项目：[GLUE Benchmark](https://gluebenchmark.com/)
- 相关：[[1905-SuperGLUE A Stickier Benchmark for General-Purpose Language Understanding Systems]]

