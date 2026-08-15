---
type: paper
paper_id: arxiv-2307.16789
title: "ToolLLM: Facilitating Large Language Models to Master Real-world APIs"
arxiv: https://arxiv.org/abs/2307.16789
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
  - method/tool-calling
  - eval/tool-benchmark
  - year/2023
  - priority/p1
  - read/skim
---

# ToolLLM：让开源大模型掌握真实世界 API

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2307.16789
> 发表：2023 ｜ 作者：Yujia Qin, Shihao Liang, Yining Ye 等

---

## 一、一句话概括

**ToolLLM** 构建 ToolBench 数据集，覆盖 16,000+ 个真实 RESTful API，并训练 ToolLLaMA，使开源 LLM 更擅长复杂工具调用。

它是工具调用数据构造、训练和评测体系的代表工作。

---

## 二、数据构造

ToolBench 的构造包括三步：

1. **API collection**：从 RapidAPI 收集 16,464 个真实 API，覆盖 49 类。
2. **Instruction generation**：用 ChatGPT 生成单工具和多工具任务指令。
3. **Solution path annotation**：用 ChatGPT 搜索并标注 API 调用链。

这让模型不只学习函数格式，还学习多步工具路径。

---

## 三、模型与评测

ToolLLM 提出：

- ToolLLaMA：基于 LLaMA 微调的工具调用模型。
- API retriever：为任务推荐相关 API。
- ToolEval：自动评估工具调用路径的有效性。
- DFS-based decision tree：扩展和搜索多条工具调用轨迹。

---

## 四、为什么重要

ToolLLM 把工具使用能力拆成完整 pipeline：

```text
API 收集 → 指令生成 → 调用链标注 → 模型训练 → API 检索 → 自动评测
```

这比单纯 function calling benchmark 更接近真实工具生态。

---

## 五、局限与启发

局限：

- 很多标注依赖 ChatGPT 自动生成，可能有噪声。
- 真实 API 副作用、鉴权、速率限制和错误恢复仍难覆盖。
- ToolEval 本身也可能有评估偏差。

启发：

- 工具 Agent 需要工具检索器，否则 API 数量一多上下文会爆炸。
- 多工具任务要评估调用链，而不是只看单次参数是否正确。

---

## 参考 / 延伸阅读

- 论文：[ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs](https://arxiv.org/abs/2307.16789)
- 相关：[[2302-Toolformer Language Models Can Teach Themselves to Use Tools]]

