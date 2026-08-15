---
type: paper
paper_id: arxiv-2311.12022
title: "GPQA: A Graduate-Level Google-Proof Q&A Benchmark"
arxiv: https://arxiv.org/abs/2311.12022
year: 2023
updated: 2026-06-28
status: summarized
primary_category: model-benchmark
priority: p1
read_type: skim
tags:
  - paper
  - paper/eval
  - eval/model-benchmark
  - eval/knowledge
  - eval/science
  - year/2023
  - priority/p1
  - read/skim
---

# GPQA：研究生级、难以搜索的科学问答评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2311.12022
> 发表：2023 ｜ 作者：David Rein, Betty Li Hou, Asa Cooper Stickland 等

---

## 一、一句话概括

**GPQA** 是由领域专家编写的研究生级科学多选题 benchmark，覆盖生物、物理、化学，题目设计成 skilled non-experts 即使能上网也很难答对。

它是评估前沿模型科学推理与可监督性的关键 benchmark。

---

## 二、数据特点

GPQA 包含 448 道多项选择题：

- 由对应领域专家编写。
- 覆盖 biology、physics、chemistry。
- 题目强调 Google-proof，即不能简单搜索得到答案。
- 专家准确率约 65%，回顾修正后约 74%。
- 高技能非专家即使用网页也只有约 34%。
- GPT-4 基线约 39%。

---

## 三、为什么重要

GPQA 的意义不只是“题更难”，而是它切中了 scalable oversight 问题：

```text
如果未来 AI 超过普通监督者
人类如何判断它在高难科学问题上是否可信？
```

GPQA 让非专家监督难题变得可实验化。

---

## 四、与 HLE 的关系

| 维度 | GPQA | HLE |
|---|---|---|
| 范围 | 生物/物理/化学 | 多学科 |
| 规模 | 448 题 | 约 2,500 题 |
| 重点 | 科学专家题、Google-proof | 前沿人类知识闭端评测 |
| 意义 | 可监督性实验 | 前沿能力压力测试 |

HLE 可以看成更大范围的高难专家评测，GPQA 是其中科学推理方向的重要前身。

---

## 五、局限与启发

局限：

- 题量较小。
- 主要是多选题，不覆盖开放科研过程。
- 专家题目仍可能随模型训练和检索能力提升被追上。

启发：

- 高难评测要防止简单搜索和训练污染。
- 对研究型 Agent，答案正确性之外还要评估证据、推理和不确定性校准。

---

## 参考 / 延伸阅读

- 论文：[GPQA: A Graduate-Level Google-Proof Q&A Benchmark](https://arxiv.org/abs/2311.12022)
- 相关：[[2501-Humanitys Last Exam]]

