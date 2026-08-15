---
type: paper
paper_id: arxiv-2305.15334
title: "Gorilla: Large Language Model Connected with Massive APIs"
arxiv: https://arxiv.org/abs/2305.15334
year: 2023
updated: 2026-06-28
status: summarized
primary_category: tool-use
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/tool-use
  - method/api-calling
  - eval/api-benchmark
  - year/2023
  - priority/p1
  - read/skim
---

# Gorilla：面向海量 API 调用的大模型

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2305.15334
> 项目：https://gorilla.cs.berkeley.edu/
> 发表：2023 ｜ 作者：Shishir G. Patil, Tianjun Zhang, Xin Wang, Joseph E. Gonzalez

---

## 一、一句话概括

**Gorilla** 通过 API 数据微调和文档检索，让 LLM 更准确地生成 API 调用，减少工具幻觉和参数错误。

它关注的是工具 Agent 的一个核心瓶颈：调用 API 时要写对函数、参数和版本。

---

## 二、核心问题

LLM 调工具容易出错：

- 幻觉不存在的 API。
- 参数名写错。
- 参数类型不匹配。
- API 版本更新后仍使用旧接口。

Gorilla 用检索增强和 APIBench 数据集来提升模型的 API 调用可靠性。

---

## 三、方法与数据

Gorilla 构建 APIBench，包含 HuggingFace、TorchHub、TensorHub 等 API。模型训练目标是根据自然语言需求生成正确 API 调用。

关键设计：

- 用 API 文档作为检索上下文。
- 让模型适应测试时文档变化。
- 评估 API hallucination 和调用准确性。

---

## 四、为什么重要

Gorilla 代表工具调用从 prompt 工程走向数据和模型训练：

```text
工具描述 + 检索 + 微调 + 调用评测
```

它提示我们：工具能力不是只靠 function schema 就能解决，API 文档检索和版本适配同样重要。

---

## 五、局限与启发

局限：

- 重点是单步 API 调用，不是完整长程 Agent。
- 真实 API 还涉及鉴权、状态、副作用和错误恢复。
- 训练数据和 API 文档质量直接影响效果。

启发：

- 工具 Agent 要优先减少 hallucinated tool call。
- 动态文档检索比把所有 API 写进 prompt 更可扩展。

---

## 参考 / 延伸阅读

- 论文：[Gorilla: Large Language Model Connected with Massive APIs](https://arxiv.org/abs/2305.15334)
- 项目：[Gorilla](https://gorilla.cs.berkeley.edu/)

