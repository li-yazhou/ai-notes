---
type: paper
paper_id: arxiv-2303.17760
title: "CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society"
arxiv: https://arxiv.org/abs/2303.17760
year: 2023
updated: 2026-06-28
status: summarized
primary_category: multi-agent
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/multi-agent
  - method/role-playing
  - year/2023
  - priority/p0
  - read/deep
---

# CAMEL：用角色扮演研究多智能体自主协作

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.17760
> 项目：https://github.com/camel-ai/camel
> 发表：2023 ｜ 作者：Guohao Li 等

---

## 一、一句话概括

**CAMEL** 提出一种 role-playing 多智能体框架，让两个或多个 LLM Agent 通过分配角色、任务细化和“inception prompting”进行自主对话协作，以完成复杂任务并生成大规模协作数据。

它是现代多智能体 LLM 系统的早期代表：**让 Agent 不只是调用工具，而是通过角色分工和对话协作完成任务。**

---

## 二、研究动机

复杂任务通常需要多步推理、专业分工和持续沟通。单个 LLM 容易：

- 忘记任务目标。
- 角色不清。
- 输出泛泛而谈。
- 难以持续推进多轮任务。

CAMEL 的问题是：如果让多个聊天 Agent 自主协作，如何让它们不跑偏，并保持与人类意图一致？

---

## 三、Role-Playing 框架

CAMEL 的典型设置包含：

| 角色 | 作用 |
|---|---|
| Human Input | 给出初始想法 |
| Task Specifier Agent | 把模糊想法具体化为明确任务 |
| AI User Agent | 扮演需求方，持续提出指令并判断完成 |
| AI Assistant Agent | 扮演执行方，给出方案、代码或解释 |
| Critic Agent | 可选，对候选方案做选择或反馈 |

核心流程：

```text
人类给出初始想法
  ↓
Task Specifier 细化任务
  ↓
分配 AI User / AI Assistant 角色
  ↓
双方按协议多轮对话
  ↓
AI User 判断任务完成并发出终止标记
```

---

## 四、Inception Prompting

CAMEL 的关键不是普通聊天，而是通过系统提示预先植入：

- 角色身份。
- 共同任务。
- 对话格式。
- 谁负责指导，谁负责执行。
- 终止条件。
- 不要忘记任务的约束。

论文引入 `<CAMEL_TASK_DONE>` 作为任务完成标记，帮助对话有明确终止点。

这对应多智能体工程中的一个核心经验：**角色、协议和终止条件比“多叫几个模型聊天”更重要。**

---

## 五、数据与实验

CAMEL 生成了多个数据集：

- AI Society：大量角色协作任务对话。
- Code：程序员与领域用户协作完成代码任务。
- Math / Science：问题-解答类数据。

论文报告：

- AI Society 数据集中，生成 50 个 assistant roles、50 个 user roles，每组 10 个任务，共约 25,000 段对话。
- 人类评估中，CAMEL Agent 方案在 AI Society 任务上明显优于 gpt-3.5-turbo single-shot。
- GPT-4 评估也显示 CAMEL 多轮协作方案优于单轮方案。

---

## 六、典型问题与观察

论文也记录了多智能体对话中的失败模式：

- **Flake replies**：回复“我会做……”但没有推进任务。
- **循环客套**：互相感谢、告别，但任务未完成。
- **终止困难**：不恰当地提前或延迟结束。
- **角色漂移**：Agent 忘记自己是需求方还是执行方。
- **安全风险**：角色组合可能生成危险任务。

这些问题后来成为多智能体框架的基本工程挑战。

---

## 七、与 AutoGen / MetaGPT 的关系

CAMEL 更偏研究范式和数据生成，AutoGen 更偏工程框架，MetaGPT 更偏软件工程组织结构。

```text
CAMEL：角色扮演 + 协作数据 + 多智能体行为研究
AutoGen：可编程 conversable agents 框架
MetaGPT：把软件公司 SOP 映射成多智能体流程
```

---

## 八、局限

1. **任务完成评估难**：很多开放任务没有可验证答案。
2. **多轮对话不等于有效协作**：可能产生冗长但低效的交流。
3. **容易角色漂移**：prompt 约束不能完全保证长期稳定。
4. **安全风险**：自动生成角色和任务可能覆盖危险场景。
5. **缺少真实工具闭环**：早期 CAMEL 更多是对话协作，不是强工具执行系统。

---

## 九、为什么重要

CAMEL 提供了多智能体协作的三个基本元素：

1. 角色分工。
2. 对话协议。
3. 终止条件。

这三个元素今天仍是构建多 Agent 系统的基础。没有它们，多智能体很容易变成“热闹但没产出”的聊天。

---

## 十、对 Agent 的启发

- 多智能体协作前必须先定义角色边界。
- 对话要有格式协议和完成条件。
- 至少需要一个任务推进者和一个结果审查者。
- 开放任务应尽量转成可验证子任务，否则很难判断协作是否有效。

---

## 参考 / 延伸阅读

- 论文：[CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society](https://arxiv.org/abs/2303.17760)
- 代码：[camel-ai/camel](https://github.com/camel-ai/camel)
- 相关：[[2308-AutoGen Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework]]
