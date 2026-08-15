---
type: paper
paper_id: arxiv-2205.00445
title: "MRKL Systems: A modular, neuro-symbolic architecture"
arxiv: https://arxiv.org/abs/2205.00445
year: 2022
updated: 2026-06-28
status: summarized
primary_category: tool-use
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/tool-use
  - method/tool-calling
  - method/neuro-symbolic
  - year/2022
  - priority/p0
  - read/deep
---

# MRKL Systems：把大模型、工具、知识库和符号推理组合成系统

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2205.00445
> 发表：2022 ｜ 作者：Ehud Karpas, Omri Abend, Yonatan Belinkov, Barak Lenz, Opher Lieber, Nir Ratner, Yoav Shoham 等（AI21 Labs）

---

## 一、一句话概括

**MRKL（Modular Reasoning, Knowledge and Language）** 提出一种模块化神经符号架构：用大语言模型作为自然语言入口和通用能力底座，同时通过路由器调用外部专家模块，例如计算器、数据库、搜索、API、专门模型或符号推理器。

这篇论文是现代 Tool-use / Function-calling / Agent Router 思想的早期系统化表达：**不要指望一个语言模型包办所有能力，而是让模型成为系统的一部分。**

---

## 二、研究动机：为什么单一 LLM 不够

论文指出，大语言模型虽然强，但有天然短板：

| 短板 | 具体表现 | 更合适的解决方式 |
|---|---|---|
| 信息过期 | 不知道当前日期、汇率、天气、股价 | 外部 API / 搜索 / 数据库 |
| 私有知识缺失 | 无法访问企业客户表、内部文档、游戏状态 | 权限受控的私有知识源 |
| 符号/数值推理不稳 | 大数计算、精确逻辑容易错 | 计算器、程序、求解器 |
| 模型爆炸 | 每个任务微调一个大模型不可扩展 | 模块化专家 + 轻量路由 |

核心观点：LLM 很重要，但它不是完整 AI 系统。真正可用的系统应当把语言理解、知识访问和离散推理组合起来。

---

## 三、MRKL 架构

MRKL 系统由两类组件构成：

```text
用户自然语言输入
      ↓
Router / 路由器
      ↓
Expert modules / 专家模块
      ↓
输出，或继续路由到其他模块
```

### 1. Router

Router 决定当前输入该交给哪个模块处理，也可以在多跳任务中串联多个模块。它可以是神经网络、规则系统，或神经+规则混合。

Router 的任务不只是分类，还包括：
- 判断是否需要外部知识。
- 判断是否需要符号工具。
- 抽取工具所需参数。
- 在多个模块之间组合结果。

### 2. Expert modules

论文把专家模块分成两大类：

- **Neural experts**：通用大模型、小型专用模型、分类器、抽取器。
- **Symbolic experts**：计算器、货币转换器、数据库查询、API 调用、规则系统。

这和今天 Agent 框架中的 tool registry、function calling、router agent 很接近。

---

## 四、MRKL 的设计收益

论文总结的几个优势非常像后来的 Agent 工程原则：

1. **Safe fallback**：没有匹配专家时回退到通用 LLM。
2. **Robust extensibility**：新增能力只需添加专家并训练/调整路由器，不必重训整个大模型。
3. **Interpretability**：调用哪个模块本身就是一种解释，例如“答案来自计算器/数据库”。
4. **Up-to-date information**：通过 API 接入动态信息。
5. **Proprietary knowledge**：接入私有知识库和业务系统。
6. **Compositionality**：复杂任务可以路由到多个模块组合完成。

---

## 五、Jurassic-X：MRKL 的实现案例

AI21 Labs 基于 MRKL 思想实现了 Jurassic-X。论文重点讨论了一个看似简单但很关键的案例：**自然语言算术问题如何交给计算器**。

难点不是计算本身，而是从自然语言中可靠抽取：
- 操作数：哪些数字参与计算。
- 操作符：加、减、乘、除或更复杂组合。
- 操作顺序：一操作还是两操作，多步问题如何拆。
- 表达形式：数字可能写成 `12`、`twelve`、`a dozen`，也可能藏在“我丢了一个球”这种语义表达里。

论文的关键判断是：**神经网络负责把自然语言映射成结构化参数，符号模块负责做确定性计算。**

这正是今天 function calling 的核心：模型不直接“心算”，而是生成结构化调用。

---

## 六、与 CoT / ReAct 的关系

MRKL 和 CoT、ReAct 关注点不同：

| 论文 | 核心贡献 | Agent 视角 |
|---|---|---|
| CoT | 让模型显式生成中间推理步骤 | Thought |
| MRKL | 让系统把任务路由给外部专家模块 | Tool / Router |
| ReAct | 让推理和行动交错进行 | Thought + Action + Observation |

可以把三者串成一条演化线：

```text
CoT：模型会“想”
MRKL：系统会“找工具”
ReAct：模型边想边用工具，并根据反馈继续想
```

---

## 七、对 Agent 系统的长期影响

MRKL 的影响不一定体现在某个 benchmark 数字上，而体现在架构思想上：

1. **Agent 不是一个模型，而是一个系统**  
   包括 LLM、工具、路由、状态、权限、错误处理和审计。

2. **工具调用的关键是接口可靠性**  
   工具本身往往很准，难点在于模型能否正确判断何时调用、调用哪个、参数是什么。

3. **模块化比单模型微调更可维护**  
   企业环境尤其需要接入动态数据、私有数据和权限系统，MRKL 比“全部塞进模型”更现实。

4. **可解释性来自可追踪的模块调用链**  
   当答案来自某个 API 或计算器时，比模型自由生成更容易审计。

---

## 八、局限

1. **路由器是系统瓶颈**：错路由、漏路由、参数抽取错误会直接导致失败。
2. **组合任务复杂**：多模块串联时，错误会传播，系统需要状态管理和失败恢复。
3. **论文实验较窄**：主要用算术案例展示神经符号接口，没有像后来的 WebArena、SWE-bench 那样做大规模真实环境评测。
4. **安全与权限问题尚未充分展开**：一旦工具能访问数据库/API，就必须考虑越权调用、注入攻击和审计。

---

## 九、为什么这篇论文重要

1. 它把大模型从“万能黑盒”重新放回“系统组件”的位置。
2. 它提前定义了后来的 tool-use agent 的核心结构：router + tools + fallback。
3. 它强调动态知识、私有知识和精确推理，这些正是纯 LLM 最难可靠解决的部分。
4. 它为 function calling、tool registry、planner-router-executor 等工程范式提供了清晰理论原型。

---

## 十、对我后续工作的启发

- 做 Agent 架构时，先列清楚哪些能力应该由模型承担，哪些应该由工具承担。
- Router 的评测要单独做：意图识别准确率、参数抽取准确率、工具选择准确率、失败回退策略。
- 企业级 Agent 不能只有 prompt，还需要权限、日志、重试、参数校验和工具沙箱。
- MRKL 提醒我们：真正可靠的 Agent 往往不是“更会聊天”，而是“更会把任务交给正确的确定性组件”。

---

## 参考 / 延伸阅读

- 论文：[MRKL Systems: A modular, neuro-symbolic architecture](https://arxiv.org/abs/2205.00445)
- 相关：[[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]
