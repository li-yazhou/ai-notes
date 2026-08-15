---
type: paper
paper_id: arxiv-2303.17651
title: "Self-Refine: Iterative Refinement with Self-Feedback"
arxiv: https://arxiv.org/abs/2303.17651
year: 2023
updated: 2026-06-28
status: summarized
primary_category: agent-loop-memory
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/reflection
  - method/self-feedback
  - year/2023
  - priority/p1
  - read/skim
---

# Self-Refine：用自反馈循环迭代改进输出

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.17651
> 项目：https://selfrefine.info/
> 发表：2023 ｜ 作者：Aman Madaan, Niket Tandon, Prakhar Gupta 等

---

## 一、一句话概括

**Self-Refine** 让同一个 LLM 同时扮演生成器、反馈者和修改者，对初始输出进行多轮自我反馈与迭代优化。

它是“生成-评估-修正”循环在 LLM test-time 推理中的经典形式。

---

## 二、核心流程

```text
Generate 初稿
  ↓
Feedback 找问题
  ↓
Refine 根据反馈修改
  ↓
重复直到达到停止条件
```

它不需要额外监督数据、强化学习或新模型训练，只依赖同一个 LLM 在推理阶段多次调用。

---

## 三、关键结果

论文在 7 类任务上评估，包括对话回复、数学推理、代码、文本生成等。结果显示，Self-Refine 相比一步生成平均提升约 20% 绝对表现，并在人工偏好和自动指标上均有改善。

---

## 四、与 Agent 的关系

Self-Refine 是很多 Agent 反思机制的基础：

- Planner 生成计划后自评。
- Coding Agent 写补丁后检查。
- Research Agent 写答案后找漏洞。
- Tool Agent 调错工具后修正策略。

它和 Reflexion 的区别是：Self-Refine 更关注当前输出的迭代改写，Reflexion 更强调失败经验写入语言记忆。

---

## 五、局限与启发

局限：

- 自反馈可能不可靠，模型未必能发现自己的错误。
- 多轮迭代增加成本。
- 如果没有外部验证器，可能只是把错误说得更像真的。

启发：

- 自我批评最好结合外部信号，如测试、检索、规则检查。
- Agent 的反思不应只是“再想想”，而要转化为可执行修改。

---

## 参考 / 延伸阅读

- 论文：[Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- 相关：[[2303-Reflexion Language Agents with Verbal Reinforcement Learning]]

