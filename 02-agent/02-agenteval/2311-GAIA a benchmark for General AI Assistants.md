---
type: paper
paper_id: arxiv-2311.12983
title: "GAIA: a benchmark for General AI Assistants"
arxiv: https://arxiv.org/abs/2311.12983
year: 2023
updated: 2026-06-28
status: summarized
primary_category: agent-benchmark
priority: p0
read_type: deep
tags:
  - paper
  - paper/eval
  - paper/agent
  - eval/agent-benchmark
  - agent/general-assistant
  - env/web
  - year/2023
  - priority/p0
  - read/deep
---

# GAIA：面向通用 AI 助手的真实世界问题评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2311.12983
> 项目：https://huggingface.co/gaia-benchmark
> 发表：2023 ｜ 作者：Grégoire Mialon, Clémentine Fourrier, Craig Swift 等

---

## 一、一句话概括

**GAIA** 是一个评测通用 AI 助手的基准，包含 466 个对人类相对简单、但对 LLM Agent 很难的真实世界问题，要求模型综合使用推理、多模态理解、网页浏览、工具和文件处理能力。

它的重要性在于：评测目标从“知识考试”转向“能不能像助手一样完成开放信息任务”。

---

## 二、核心动机

很多 benchmark 中，模型已经接近或超过人类，但这不代表它能做好真实助手任务。

GAIA 选择了一个反直觉标准：

```text
人类容易完成
但 AI 助手很难完成
```

论文报告中，人类表现约 92%，而 GPT-4 加插件约 15%。这说明真实助手能力和静态问答能力之间有很大差距。

---

## 三、任务特点

GAIA 的题目通常需要多种能力组合：

- 网页浏览。
- 多步推理。
- 多模态理解。
- 代码或计算工具。
- 读取不同文件类型。
- 信息交叉验证。

题目设计强调：

- 有唯一、简短、可验证答案。
- 对人类来说概念上不复杂。
- 不依赖主观判断。
- 可自动评分。

---

## 四、难度分级

GAIA 将任务分为 3 个等级：

| Level | 含义 |
|---|---|
| Level 1 | 相对直接，但可能需要工具或检索 |
| Level 2 | 多步检索、计算或文件处理 |
| Level 3 | 更复杂的组合任务，需要更强规划和验证 |

越高等级越能暴露 Agent 的工具使用、记忆、规划和错误恢复问题。

---

## 五、关键结果

论文的代表性结果：

- 人类达到约 92%。
- GPT-4 + 插件约 15%。
- 即使在最简单等级，GPT-4 + 工具也不到 30%。
- 最难等级上，模型表现接近 0。

这显示通用 AI 助手的瓶颈并不只是知识，而是：

- 知道该查什么。
- 会选择工具。
- 能组织多步过程。
- 能验证中间信息。
- 能输出精确最终答案。

---

## 六、为什么重要

GAIA 把“AGI 风格助手能力”变成了相对可评测的问题集。它不像传统考试那样只问知识点，而是考察：

```text
检索 + 工具 + 文件 + 推理 + 精确答案
```

这对后来通用 Agent、Deep Research、浏览器 Agent、多工具助手评测都很有启发。

---

## 七、局限

1. **只评最终答案**：GAIA 不直接评估轨迹质量、工具调用是否高效、推理是否可靠。
2. **题量较小**：466 题适合高质量评测，但覆盖面有限。
3. **网页信息会变化**：真实世界问题可能随时间漂移。
4. **工具环境差异大**：不同系统接入的搜索、浏览、文件解析能力会影响结果。
5. **可能被训练污染**：公开题目越流行，越需要隐藏集和动态更新。

---

## 八、对 Agent 的启发

- 通用助手评测要看工具组合能力，而不是只看语言推理。
- 最终答案要短、明确、可验证，便于自动评分。
- 真实助手需要自我验证机制，否则很容易给出看似合理但错误的答案。
- 评测应区分模型能力、工具能力和系统编排能力。

---

## 参考 / 延伸阅读

- 论文：[GAIA: a benchmark for General AI Assistants](https://arxiv.org/abs/2311.12983)
- 数据：[GAIA Benchmark](https://huggingface.co/gaia-benchmark)
- 相关：[[2308-AgentBench Evaluating LLMs as Agents]]

