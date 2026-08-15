---
type: paper
paper_id: arxiv-2211.09110
title: "Holistic Evaluation of Language Models"
arxiv: https://arxiv.org/abs/2211.09110
year: 2022
updated: 2026-06-28
status: summarized
primary_category: model-benchmark
priority: p1
read_type: skim
tags:
  - paper
  - paper/eval
  - eval/model-benchmark
  - eval/multi-metric
  - eval/reliability
  - year/2022
  - priority/p1
  - read/skim
---

# HELM：语言模型的整体性评测框架

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2211.09110
> 项目：https://crfm.stanford.edu/helm/
> 发表：2022 ｜ 作者：Percy Liang, Rishi Bommasani, Tony Lee 等

---

## 一、一句话概括

**HELM（Holistic Evaluation of Language Models）** 提出从多场景、多指标整体评估语言模型，而不是只用单一准确率判断模型好坏。

它是大模型评测从“跑分”走向“透明、多维、可复现”的关键工作。

---

## 二、核心思想

HELM 先对评测空间做 taxonomy，再在可行范围内选择代表场景和指标。

它强调：

- 覆盖不同 use cases。
- 不只看 accuracy。
- 同一批模型在相同场景和指标下密集评测。
- 公开 prompts、completions 和工具链，提高透明度。

---

## 三、七类核心指标

HELM 在核心场景中尽可能评估：

| 指标 | 含义 |
|---|---|
| Accuracy | 任务正确性 |
| Calibration | 置信度是否可靠 |
| Robustness | 扰动下是否稳定 |
| Fairness | 群体公平性 |
| Bias | 偏见 |
| Toxicity | 毒性 |
| Efficiency | 成本与效率 |

这比只报告一个分数更接近真实模型选型。

---

## 四、为什么重要

HELM 对 Agent 评测有直接启发：

```text
Agent 也不能只看 success rate
还要看成本、鲁棒性、安全、公平、效率和可复现性
```

后来 AI Agents That Matter 对 Agent benchmark 的批评，与 HELM 的多维评测精神是一脉相承的。

---

## 五、局限与启发

局限：

- HELM 主要是模型评测，不是交互式 Agent 评测。
- 覆盖广带来维护成本高。
- 指标多后，如何综合决策仍需业务权衡。

启发：

- 评测报告应公开提示词、模型版本、采样参数和原始输出。
- 模型/Agent 选型要看多维 trade-off，而不是榜单第一。

---

## 参考 / 延伸阅读

- 论文：[Holistic Evaluation of Language Models](https://arxiv.org/abs/2211.09110)
- 项目：[HELM](https://crfm.stanford.edu/helm/)
- 相关：[[2407-AI Agents That Matter]]

