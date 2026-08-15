---
type: paper
paper_id: arxiv-2206.04615
title: "Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models"
arxiv: https://arxiv.org/abs/2206.04615
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
  - eval/capability-map
  - year/2022
  - priority/p1
  - read/skim
---

# BIG-bench：大规模、多任务、难能力评测集合

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2206.04615
> 项目：https://github.com/google/BIG-bench
> 发表：2022 ｜ 作者：BIG-bench authors

---

## 一、一句话概括

**BIG-bench（Beyond the Imitation Game benchmark）** 汇集 204 个多样化任务，用于量化和外推语言模型随规模增长出现的能力与限制。

它的重要性在于：把模型评测从少数标准数据集扩展成社区共建的大规模能力地图。

---

## 二、核心设计

BIG-bench 的任务由 450 位作者、132 个机构贡献，覆盖：

- 语言学。
- 儿童发展。
- 数学和常识推理。
- 生物、物理。
- 社会偏见。
- 软件开发。
- 多步骤或组合能力。

许多任务被设计为当时模型难以完成，用来观察规模化带来的能力变化。

---

## 三、关键发现

论文评估从百万到数千亿参数级别的多类模型，并与人类专家基线比较。重要发现包括：

- 模型性能和校准总体随规模提升，但绝对表现仍有限。
- 某些任务随规模平滑提升，常与知识或记忆有关。
- 某些任务呈现“突破式”变化，通常涉及多步骤或脆弱评价指标。
- 在模糊上下文中，社会偏见可能随规模增强，但可通过提示缓解。

---

## 四、为什么重要

BIG-bench 对后续评测的影响在于：

- 证明单一 benchmark 无法覆盖模型能力。
- 推动社区式任务贡献。
- 让“emergent abilities”成为大模型讨论核心话题之一。
- 为 HELM 等多维评测框架提供思想基础。

---

## 五、局限与启发

局限：

- 任务质量和难度不完全均匀。
- 许多任务仍是静态问答或文本任务。
- 公开任务容易被训练污染。

启发：

- 大模型评测应覆盖能力长尾，而不只看热门标准题。
- Agent 评测也需要多场景、多任务、多指标，而不是单一环境。

---

## 参考 / 延伸阅读

- 论文：[Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models](https://arxiv.org/abs/2206.04615)
- 项目：[BIG-bench](https://github.com/google/BIG-bench)
- 相关：[[2211-HELM Holistic Evaluation of Language Models]]

