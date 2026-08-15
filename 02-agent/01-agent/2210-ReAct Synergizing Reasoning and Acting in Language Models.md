---
type: paper
paper_id: arxiv-2210.03629
title: "ReAct: Synergizing Reasoning and Acting in Language Models"
arxiv: https://arxiv.org/abs/2210.03629
year: 2022
updated: 2026-06-28
status: summarized
primary_category: agent-loop
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/react-loop
  - agent/tool-use
  - method/reason-act
  - year/2022
  - priority/p0
  - read/deep
---

# ReAct：在语言模型中协同推理与行动

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2210.03629
> 项目主页：https://react-lm.github.io/
> 代码：https://github.com/ysymyth/ReAct
> 发表：ICLR 2023 ｜ 作者：Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du 等（Princeton + Google）

---

## 一、一句话概括

让大语言模型以**交错（interleaved）**的方式，同时生成**推理轨迹（Thought）**和**面向任务的行动（Act）**，使"思考"和"动手"互相赋能——推理引导动作，动作从外部环境取回证据反过来修正推理。

这是 Agent 范式的奠基性论文之一（被引 11000+），后来的 LangChain、各类 Tool-use / Function-calling 框架都源于此。

---

## 二、研究动机（要解决什么问题）

论文之前，LLM 的能力沿两条独立路线发展：

| 路线 | 代表方法 | 优点 | 致命缺陷 |
|------|----------|------|----------|
| **推理 (Reasoning)** | Chain-of-Thought (CoT) | 能拆解复杂问题、可解释 | **幻觉严重**：全程闭门造车，无法获取外部新信息 |
| **行动 (Acting)** | Act-only / WebGPT 等 | 可与外部环境交互、拿真实证据 | **缺乏规划**：不先想就做，复杂任务中错误传播、难收敛 |

**核心洞察**：人类解决新任务时，是"边想边做、边做边修正"的。论文把这两条线**缝合**起来——让模型在同一个生成过程中既思考又行动。

---

## 三、方法：ReAct 范式

### 1. 三种内部状态（reasoning trace 的作用）

论文明确指出 Thought（思考）承担四种功能：
- **分析目标**：拆解任务、翻译问题
- **提取信息**：从观察中抽取关键证据
- **更新/追踪**：维护中间结论与进度
- **规划下一步**：决定接下来做什么动作

### 2. 经典轨迹结构

ReAct 的输出是一个**交错循环**：

```
Thought 1:  先分析问题，决定第一步查什么
Action 1:   Search[xxx]          ← 与外部环境交互
Observation 1: <环境返回的结果>
Thought 2:  根据观察，更新认知，决定下一步
Action 2:   Lookup[xxx] / Finish[answer]
Observation 2: ...
...
Thought N:  信息已足够，给出最终答案
Action N:   Finish[最终答案]
```

- **Thought**：模型的内部推理（对人类可读、可调试）
- **Action**：与外部工具/环境交互（搜索、查找、提交答案）
- **Observation**：环境返回的结果，作为下一轮 Thought 的输入

### 3. 实现方式：少样本 prompting（Few-shot）

ReAct **不训练、不改模型权重**，而是用**手工设计的 few-shot 模板**（包含 6 个左右的示例轨迹）来引导 GPT-3 (text-davinci-002) 模仿这种"思考—行动—观察"的格式生成。

> 这意味着 ReAct 是一个**通用的 prompting 范式**，可即插即用到任何 LLM 上。

---

## 四、实验

### 1. 任务与外部环境

| 任务类型 | 数据集                   | 外部动作空间                                               |
| ---- | --------------------- | ---------------------------------------------------- |
| 多跳问答 | **HotpotQA**          | Wikipedia: `Search[x]`, `Lookup[x]`                  |
| 事实验证 | **FEVER**             | Wikipedia: `Search[x]`, `Lookup[x]`, `Finish[claim]` |
| 交互决策 | **ALFWorld**（文本化家庭场景） | 导航、拿放物体等                                             |
| 交互决策 | **WebShop**（网上购物）     | 搜索、点击、购买                                             |

### 2. 对比基线

- **Standard**：直接 prompting
- **CoT**：纯链式推理，不与外部交互
- **CoT-SC**：CoT + 自我一致性（多次采样取多数）
- **Act**：只行动不推理
- **ReAct**：推理 + 行动交错

### 3. 关键结论

**(1) ReAct 全面优于纯推理或纯行动**
- 在 HotpotQA、FEVER 上，ReAct 比 Standard / CoT 更准，且**幻觉明显减少**（因为有外部证据校验）。
- 在 ALFWorld 上，ReAct 成功率**大幅领先**（如 71% vs Act 的基线），证明推理对复杂决策的规划价值。

**(2) 推理 ↔ 行动 互相成就**
- **推理引导行动**：Thought 帮模型决定"该查什么、何时停止"。
- **行动修正推理**：Observation 提供真实外部信息，切断 CoT 的幻觉链条。

**(3) ReAct 与 CoT-SC 互补，组合最强**
- 纯 ReAct 偶尔会因"证据不足 + 过度推理"出错；
- 论文提出 **ReAct → CoT-SC 蒸馏 / 结合**：当 ReAct 失败时回退到 CoT-SC，或反之，能拿到最佳整体表现。
- 结论：**外部知识（Act）+ 内部推理（Reason）结合 > 任一单独使用**。

**(4) 可解释性**
- Thought 轨迹天然可读，便于人工调试与定位失败原因（这是 ReAct 相比黑盒方法的一大工程优势）。

---

## 五、经典示例（论文原图范式）

以 HotpotQA 问题为例：

```
Q: 科罗拉多造山运动东段延伸到的区域，其所属行政区划的政府所在地是哪？

Thought 1: 我需要先找"科罗拉多造山运动东段延伸到哪个区域"。
Action 1: Search[科罗拉多造山运动]
Observation 1: (Wikipedia 摘要) ... 其东段延伸至大平原 (Great Plains) ...
Thought 2: 东段延伸到大平原。现在我需要找大平原所属行政区划的政府所在地。
Action 2: Search[Great Plains]
Observation 2: ... 大平原主要横跨美国中部诸州 ...
Thought 3: 信息不够具体，需要进一步 Lookup 关键词。
Action 3: Lookup[capital]
Observation 3: ...
Thought 4: 已获得答案，提交。
Action 4: Finish[xxx]
```

> 关键点：每一步 Thought 都**明确解释了为什么做这个 Action**，形成可审计的决策链。

---

## 六、局限与不足（论文坦诚）

1. **过度依赖少样本模板**：示例设计耗时，且泛化到新领域需要重写模板。
2. **推理可能"跑偏"**：当外部证据不足时，Thought 仍会发散、编造。
3. **延迟与成本**：多轮交互 → 多次模型调用 / 更长 token，推理成本高于单次 CoT。
4. **受限于当时模型能力**（GPT-3），更强模型下 ReAct 的相对优势会变化。

---

## 七、为什么这篇论文重要（历史地位）

1. **Agent 范式的范式定义**：确立了"**Thought-Action-Observation 循环**"这一直到今天仍是几乎所有 Agent 框架（LangChain、LlamaIndex、AutoGPT、各 Coding Agent）的底层结构。
2. **让 Tool-use 有了"思考层"**：区别于裸函数调用，ReAct 强调调用前后都要有显式推理。
3. **可解释性**：Thought 轨迹让 Agent 行为可审计，这是产品化 Agent 的刚需。
4. **推理 vs 检索的辩证关系**：为后来 RAG + 推理、Self-Ask、Reflexion 等工作奠定基调。

---

## 八、对我后续工作的启发

- 构建 Agent 时，**别只做 Tool 调用，要让模型在调用前后显式 Thought**——这是 ReAct 的灵魂。
- 评测 Agent 时，**Thought 轨迹是可观测、可归因的关键信号**，应纳入评测维度（错误定位、规划质量）。
- ReAct 的"交错循环"结构，本质上就是 **Coding Agent 的工具调用循环（Agent Loop）** 的理论原型，可与 nanobot-agent 的两层循环对照理解。

---

## 九、放在 Agent 与评测发展线中的位置

ReAct 可以看作前两篇工作的合流：

| 前置思想 | ReAct 中的对应部分 |
|---|---|
| CoT：显式中间推理 | `Thought` |
| MRKL：调用外部专家/工具 | `Action` |
| 环境/工具返回结果 | `Observation` |

它的真正贡献是把三者组织成循环：

```text
Thought → Action → Observation → Thought → ...
```

因此，ReAct 之后的 Agent 评测不再只问“答案对不对”，而会继续追问：

- 工具是否选对？
- 检索到的证据是否支撑结论？
- 中间步骤是否发生幻觉？
- 环境反馈能否修正错误路线？
- 多步任务中是否能正确停止？

这条线直接通向后来的 AgentBench、WebArena、SWE-bench、GAIA、OSWorld 等 benchmark：评测对象从静态问答模型，变成了能在环境中连续行动的系统。

---

## 参考 / 延伸阅读

- 论文：[arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- 项目主页：[react-lm.github.io](https://react-lm.github.io/)
- 代码：[github.com/ysymyth/ReAct](https://github.com/ysymyth/ReAct)
- 后续工作：**Reflexion**（Yao et al., 反思机制）、**Self-Ask**、**Toolformer**、**CoT-SC**
- 本仓库关联：[[Agent 构建与评测学习路线]]、[[nanobot-agent 执行流程]]
