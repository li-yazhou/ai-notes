---
type: paper
paper_id: arxiv-2503.16416
title: "Survey on Evaluation of LLM-based Agents"
arxiv: https://arxiv.org/abs/2503.16416
year: 2025
updated: 2026-06-28
status: summarized
primary_category: survey
priority: p0
read_type: deep
tags:
  - paper
  - paper/eval
  - paper/agent
  - paper/survey
  - eval/agent-benchmark
  - agent/methodology
  - year/2025
  - priority/p0
  - read/deep
---

# Survey on Evaluation of LLM-based Agents：LLM Agent 评测综述

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2503.16416
> 发表：2025 ｜ 作者：综述论文作者团队

---

## 一、一句话概括

**Survey on Evaluation of LLM-based Agents** 系统梳理了 LLM Agent 评测的发展，从基础能力、应用场景、通用 Agent、benchmark 维度和评测框架等角度总结现有工作与未来问题。

它的重要性在于：把分散的 Agent benchmark 放进一张体系图里，帮助判断“某个评测到底在测什么”。

---

## 二、为什么需要这类综述

Agent 评测已经快速分化：

- Web Agent 有 WebArena、Mind2Web、VisualWebArena。
- Coding Agent 有 SWE-bench。
- Tool Agent 有 ToolBench、τ-bench。
- General Assistant 有 GAIA。
- Computer Use 有 OSWorld。
- Scientific Agent、Embodied Agent、Multi-Agent 也各有评测。

如果不分类，很容易把不同 benchmark 的分数混在一起比较，得出错误结论。

---

## 三、评测维度

综述将 Agent 评测大致放入几个层次：

| 层次 | 关注点 |
|---|---|
| 核心能力 | 规划、工具使用、记忆、自我反思、多步推理 |
| 应用型评测 | Web、软件工程、科学、对话、具身任务 |
| 通用 Agent | 多任务、多工具、多模态、开放环境 |
| Benchmark 设计 | 任务来源、交互性、动态性、评分方式 |
| 评测框架 / 工具 | 环境封装、轨迹记录、自动评分、复现 |

这个分层有助于避免把“工具调用能力”和“真实任务完成能力”混为一谈。

---

## 四、核心能力评测

LLM Agent 常被拆成几类基础能力：

- **Planning**：能否分解目标、制定步骤、动态重规划。
- **Tool Use**：能否选择工具、填参数、解释工具结果。
- **Memory**：能否保存和利用长期 / 短期上下文。
- **Self-Reflection**：能否根据失败反馈修正策略。
- **Reasoning**：能否进行多步推理和因果判断。

但综述也指出：单独评这些能力有用，却不能完全代表端到端 Agent 表现。

---

## 五、应用型评测

不同应用领域对 Agent 能力要求不同：

| 应用 | 代表问题 |
|---|---|
| Web Agent | 浏览器导航、网页表单、信息检索、状态完成 |
| SWE Agent | repo 理解、issue 修复、测试反馈、patch 生成 |
| Scientific Agent | 文献、实验、数据分析、工具链编排 |
| Conversational Agent | 多轮用户交互、意图维护、安全边界 |
| Computer Use Agent | GUI grounding、文件操作、多应用工作流 |

综述强调：应用型 benchmark 更接近真实部署，但也更难复现和维护。

---

## 六、主要趋势

Agent 评测正在从简单静态任务转向：

- 更真实的环境。
- 更长程的任务。
- 更动态的 benchmark。
- 更细粒度的轨迹分析。
- 更严格的成本与可靠性指标。
- 更关注安全、鲁棒性和可信度。

这和 Agent 从 demo 走向产品的路径一致。

---

## 七、尚未解决的问题

综述中反复出现的缺口包括：

1. **细粒度评测不足**：最终失败后，很难知道是规划、检索、工具还是执行出了问题。
2. **成本指标不足**：很多论文没有系统报告 token、时间、工具调用和计算资源。
3. **动态更新不足**：公开 benchmark 容易污染和过拟合。
4. **安全和鲁棒性不足**：越权、注入攻击、隐私泄露、错误恢复评测不够。
5. **跨环境泛化不足**：在一个环境高分不代表能迁移到另一个真实场景。

---

## 八、为什么重要

这篇综述适合作为 Agent 评测地图。它让我们看到：

```text
Agent 评测不是一个榜单
而是一组围绕能力、环境、任务、成本、安全的评估体系
```

如果要设计自己的 Agent benchmark，应先回答：我要测的是基础能力、领域任务、端到端助手，还是部署可靠性？

---

## 九、对 Agent 的启发

- 评测设计要先定义能力边界，再选任务。
- 端到端成功率要配合轨迹级诊断。
- 通用 Agent 评测不能忽略成本和安全。
- 动态 benchmark 和隐藏集会越来越重要。
- 未来评测应同时服务研究、工程选型和风险治理。

---

## 参考 / 延伸阅读

- 论文：[Survey on Evaluation of LLM-based Agents](https://arxiv.org/abs/2503.16416)
- 相关：[[2407-AI Agents That Matter]]
- 相关：[[2308-AgentBench Evaluating LLMs as Agents]]
- 相关：[[2311-GAIA a benchmark for General AI Assistants]]

