---
type: paper
paper_id: arxiv-2303.17580
title: "HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face"
arxiv: https://arxiv.org/abs/2303.17580
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
  - agent/model-orchestration
  - method/tool-calling
  - year/2023
  - priority/p1
  - read/skim
---

# HuggingGPT：让 LLM 作为控制器调用专家模型

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.17580
> 发表：2023 ｜ 作者：Yongliang Shen, Kaitao Song, Xu Tan 等

---

## 一、一句话概括

**HuggingGPT** 使用 ChatGPT 作为任务控制器，规划复杂 AI 任务、选择 Hugging Face 上的专家模型执行子任务，并汇总结果。

它是“LLM 作为模型编排器”的经典方案。

---

## 二、核心流程

HuggingGPT 将复杂任务拆成四步：

```text
任务规划 → 模型选择 → 模型执行 → 响应汇总
```

例子：

- 用户提出多模态复杂请求。
- ChatGPT 将其拆解成图像理解、文本生成、语音处理等子任务。
- 系统根据模型描述选择对应 Hugging Face 模型。
- 执行后由 ChatGPT 汇总输出。

---

## 三、为什么重要

HuggingGPT 说明 LLM 可以成为统一自然语言接口，连接大量专用模型：

- LLM 不必自己掌握所有能力。
- 专家模型负责视觉、语音、生成等具体任务。
- 自然语言成为模型之间的胶水。

这和后来的 tool calling、MCP、model routing、agentic workflow 有直接关系。

---

## 四、局限

1. **模型选择依赖描述质量**：描述不准会选错模型。
2. **执行链条长**：子任务越多，错误传播越明显。
3. **没有强验证机制**：模型输出是否满足上游目标不一定可验证。
4. **成本和延迟较高**：多模型串联天然更慢。

---

## 五、对 Agent 的启发

- Agent 可以是“控制器”，不必拥有所有底层能力。
- 工具和模型描述要面向模型理解，而不是只给工程师看。
- 多工具任务需要规划、路由、执行结果校验和最终汇总。

---

## 参考 / 延伸阅读

- 论文：[HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face](https://arxiv.org/abs/2303.17580)
- 相关：[[2205-MRKL Systems]]

