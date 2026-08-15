---
type: paper
paper_id: arxiv-2211.10435
title: "PAL: Program-aided Language Models"
arxiv: https://arxiv.org/abs/2211.10435
year: 2022
updated: 2026-06-28
status: summarized
primary_category: reasoning-planning
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/reasoning-planning
  - agent/tool-use
  - method/code-execution
  - year/2022
  - priority/p1
  - read/skim
---

# PAL：让语言模型写程序，把计算交给解释器

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2211.10435
> 项目：http://reasonwithpal.com/
> 发表：2022 ｜ 作者：Luyu Gao, Aman Madaan, Shuyan Zhou 等

---

## 一、一句话概括

**PAL（Program-Aided Language Models）** 让 LLM 把自然语言问题转成可执行程序，再由 Python 等解释器完成精确计算。

它的重要性在于：把“推理”和“求值”分离，避免模型在算术和符号执行中硬算出错。

---

## 二、核心思想

CoT 让模型自己写步骤并自己算结果。问题是模型可能分解正确，但计算错误。

PAL 的流程是：

```text
自然语言问题
  ↓
LLM 生成程序作为中间推理
  ↓
解释器执行程序
  ↓
得到答案
```

LLM 负责理解和建模，运行时负责精确执行。

---

## 三、关键结果

论文在 13 个数学、符号和算法推理任务上验证 PAL。典型结论是：在 GSM8K 等任务中，Codex + PAL 可超过更大模型的纯 CoT 表现。

这说明：工具调用不是锦上添花，而是可以改变模型能力边界。

---

## 四、与 Agent 的关系

PAL 是“代码解释器 Agent”的前身之一。它提示：

- LLM 适合把问题翻译成程序。
- 程序运行时适合做精确计算。
- 中间程序比自然语言推理更可验证。

Code Interpreter、Advanced Data Analysis、ReAct + Python、Coding Agent 都继承了类似结构。

---

## 五、局限与启发

局限：

- 依赖模型生成正确程序。
- 程序执行有安全风险，需要沙箱。
- 不适合所有开放式语义任务。

启发：

- 能交给确定性工具的，不要让 LLM 口算。
- Agent 设计应优先把高风险计算外包给可靠执行器。

---

## 参考 / 延伸阅读

- 论文：[PAL: Program-aided Language Models](https://arxiv.org/abs/2211.10435)
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]

