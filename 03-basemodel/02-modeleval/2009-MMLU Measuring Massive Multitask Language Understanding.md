---
type: paper
paper_id: arxiv-2009.03300
title: "Measuring Massive Multitask Language Understanding"
arxiv: https://arxiv.org/abs/2009.03300
year: 2020
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
  - year/2020
  - priority/p1
  - read/skim
---

# MMLU：大规模多任务语言理解评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2009.03300
> 项目：https://github.com/hendrycks/test
> 发表：2020 ｜ 作者：Dan Hendrycks, Collin Burns, Steven Basart 等

---

## 一、一句话概括

**MMLU** 用 57 个学科的多项选择题评估语言模型的知识广度和问题解决能力，是大模型时代最有影响力的基础能力 benchmark 之一。

它不是 Agent benchmark，但长期作为模型底座能力的重要参照。

---

## 二、评测内容

MMLU 覆盖：

- 基础数学。
- 美国历史。
- 计算机科学。
- 法律。
- 医学。
- 道德与社会科学。
- 专业学科知识。

目标是衡量模型是否具备跨学科的学术和专业理解能力。

---

## 三、历史意义

MMLU 在 GPT-3 时代非常困难。论文指出，当时最大 GPT-3 相比随机猜测平均提升约 20 个百分点，但距离专家水平仍有明显差距。

后来随着模型能力提升，MMLU 被快速刷高，成为观察 benchmark 饱和问题的典型案例。

---

## 四、与 Agent 评测的关系

MMLU 衡量的是模型基础能力，不是 Agent 完成任务的能力。

```text
MMLU 高分
  ≠ 会调用工具
  ≠ 会长期规划
  ≠ 会修复真实代码库
  ≠ 会在网页/桌面环境行动
```

但模型知识和推理能力仍然是 Agent 能力上限的一部分。

---

## 五、局限与启发

局限：

- 多项选择题与真实任务差距大。
- 容易被训练数据污染。
- 高分后区分度下降。
- 不评估成本、工具、环境交互和安全。

启发：

- 选模型可以看 MMLU，但评估 Agent 必须看 Agent benchmark。
- Benchmark 会饱和，需要持续引入更难、更动态的评测。

---

## 参考 / 延伸阅读

- 论文：[Measuring Massive Multitask Language Understanding](https://arxiv.org/abs/2009.03300)
- 相关：[[2501-Humanitys Last Exam]]

