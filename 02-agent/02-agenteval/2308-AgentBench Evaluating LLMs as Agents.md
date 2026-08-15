---
type: paper
paper_id: arxiv-2308.03688
title: "AgentBench: Evaluating LLMs as Agents"
arxiv: https://arxiv.org/abs/2308.03688
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
  - agent/tool-use
  - year/2023
  - priority/p0
  - read/deep
---

# AgentBench：把大模型当作 Agent 来评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2308.03688
> 项目：https://github.com/THUDM/AgentBench
> 发表：2023 ｜ 作者：Xiao Liu, Hao Yu, Hanchen Zhang 等

---

## 一、一句话概括

**AgentBench** 是一个多维度 Agent 评测基准，用 8 个交互环境评估 LLM 作为 Agent 时的推理、决策、长期规划和指令遵循能力。

它的重要性在于：评测对象从“回答问题的模型”转向“能在环境中行动的模型”。

---

## 二、为什么需要 AgentBench

传统 NLP/LLM benchmark 常见形式是：

```text
输入问题 → 输出答案 → 静态打分
```

但 Agent 需要的是：

```text
观察环境 → 推理 → 行动 → 获得反馈 → 多轮决策 → 完成目标
```

AgentBench 试图回答一个更现实的问题：LLM 能否在复杂交互环境里稳定完成任务，而不是只在单轮问答中表现好。

---

## 三、8 个环境

AgentBench 覆盖三类任务：

| 类型 | 环境 | 主要考察能力 |
|---|---|---|
| 代码 / 工具 | Operating System | shell 操作、长期步骤执行 |
| 代码 / 工具 | Database | SQL 与数据库交互 |
| 代码 / 工具 | Knowledge Graph | 知识图谱检索与推理 |
| 游戏 | Digital Card Game | 策略、规则理解、状态跟踪 |
| 游戏 | Lateral Thinking Puzzles | 多轮询问和假设验证 |
| 游戏 | House-Holding | ALFWorld 风格家务任务 |
| Web | Web Shopping | 商品搜索、筛选、购买决策 |
| Web | Web Browsing | 网页导航与信息查找 |

这些任务共同特点是：模型必须在多轮反馈中调整行动。

---

## 四、评测方法

AgentBench 使用不同任务对应不同指标：

- OS / DB / House-Holding 等任务用成功率（SR）。
- Knowledge Graph 用 answer F1。
- Digital Card Game 用胜率。
- Web Browsing 用 Step Success Rate 等过程指标。
- 最终通过加权方式形成综合表现。

这比单一准确率更贴近 Agent 任务，因为不同环境对“成功”的定义并不一样。

---

## 五、关键发现

论文评测了大量 API 模型和开源模型，主要发现包括：

1. **顶级商业模型明显领先**  
   商业 API 模型在多环境中展现出更强的长期推理与决策能力。

2. **开源模型仍有明显差距**  
   即使是较强的开源模型，也普遍落后于 GPT-3.5 / GPT-4 等商业模型。

3. **失败常来自长期能力不足**  
   典型问题包括长期推理失败、决策不稳定、忽略指令、状态跟踪错误。

4. **代码训练的作用并不单向**  
   代码能力对 OS、WebShop 等程序化任务有帮助，但对策略、逻辑、情境任务未必总是正收益。

---

## 六、为什么重要

AgentBench 把 Agent 评测推向了“交互式、多环境、多指标”的方向。它说明：

```text
会答题 ≠ 会行动
会写代码 ≠ 会长期决策
会使用工具 ≠ 能可靠完成任务
```

这对后续 WebArena、SWE-bench、OSWorld、τ-bench 等评测有很强的承接意义。

---

## 七、局限

1. **环境仍偏封闭**：虽然比静态 QA 更真实，但很多环境仍是受控模拟。
2. **综合分数解释困难**：不同任务指标合并后，可能掩盖具体能力短板。
3. **未充分评估成本**：Agent 的 token、时间和工具调用成本不是主指标。
4. **模型版本变化快**：Agent 评测很容易因模型 API 更新而过时。
5. **轨迹质量不等于最终成功**：有些任务成功率无法完全解释模型行为是否稳健。

---

## 八、对 Agent 的启发

- Agent 评测应包含环境反馈，而不是只看最终文本。
- 长期任务要评估状态跟踪、错误恢复、指令遵循和策略稳定性。
- 不同任务需要不同指标，不能把所有 Agent 任务都压成 accuracy。
- 训练数据中的代码能力有帮助，但不能替代通用决策能力。

---

## 参考 / 延伸阅读

- 论文：[AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688)
- 项目：[THUDM/AgentBench](https://github.com/THUDM/AgentBench)
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]

