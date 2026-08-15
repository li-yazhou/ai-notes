---
type: paper
paper_id: arxiv-2308.08155
title: "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework"
arxiv: https://arxiv.org/abs/2308.08155
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
  - agent/framework
  - method/conversation-programming
  - year/2023
  - priority/p0
  - read/deep
---

# AutoGen：用可编程多智能体对话构建 LLM 应用

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2308.08155
> 项目：https://github.com/microsoft/autogen
> 发表：2023 ｜ 作者：Qingyun Wu 等（Microsoft Research）

---

## 一、一句话概括

**AutoGen** 是一个开源多智能体对话框架，允许开发者创建可对话、可定制、可接入 LLM/人类/工具/代码执行的 Agent，并通过“conversation programming”组织复杂 LLM 应用。

它的重要性在于：把多 Agent 从论文里的角色扮演，推进成可工程化编排的应用框架。

---

## 二、核心思想

AutoGen 认为复杂 LLM 应用可以统一抽象为：

```text
多个 conversable agents
  +
可编程 conversation flow
```

每个 Agent 都能接收消息、处理消息、回复消息。Agent 可以由不同能力支撑：

- LLM。
- 人类输入。
- 工具调用。
- 代码执行。
- 自定义 reply function。

---

## 三、Conversable Agent

AutoGen 的基础抽象是 `ConversableAgent`。论文中强调它具备：

- 统一消息接口。
- 自动回复机制。
- 可混合 LLM、人类、工具能力。
- 可配置角色和系统提示。
- 可注册自定义回复函数。

典型内置 Agent：

| Agent | 作用 |
|---|---|
| AssistantAgent | LLM 支持的任务解决者 |
| UserProxyAgent | 人类代理，也可执行代码或函数 |
| GroupChatManager | 管理多人群聊和下一发言者选择 |

---

## 四、Conversation Programming

AutoGen 的工程创新是把应用逻辑写成对话流，而不是写成单一 prompt。

控制流可以来自：

1. **自然语言控制**：system message 指示何时修复、何时终止。
2. **代码控制**：Python 函数定义终止条件、执行逻辑、路由。
3. **混合控制**：LLM 生成函数调用，代码执行后把结果送回对话。

这让不同应用可以复用同一种模式：

```text
Assistant 生成方案/代码
  ↓
UserProxy 执行代码或请求人类输入
  ↓
执行结果返回 Assistant
  ↓
Assistant 修复或终止
```

---

## 五、论文展示的应用

AutoGen 论文展示了多个应用场景：

| 应用 | 说明 |
|---|---|
| 数学解题 | Assistant 写代码，UserProxy 执行验证 |
| Retrieval-Augmented Chat | 通过检索代理增强问答 |
| ALFWorld | 多 Agent 分工做交互决策 |
| OptiGuide | 面向优化问题的代码分析与修改 |
| Dynamic Group Chat | 多角色动态群聊，自动选择下一发言者 |
| Conversational Chess / MiniWobChat | 引入规则/环境执行代理进行交互 |

论文结果显示，多 Agent 对话在数学、检索、ALFWorld、代码相关任务中可提升性能或降低人工交互成本。

---

## 六、与 CAMEL 的差异

CAMEL 强调“角色扮演产生协作行为”，AutoGen 强调“把协作行为工程化”。

| 维度 | CAMEL | AutoGen |
|---|---|---|
| 核心 | role-playing | conversation programming |
| 重点 | 多智能体行为与数据 | 应用开发框架 |
| 工具执行 | 较弱 | 强，支持代码/函数执行 |
| 人类参与 | 不是核心 | 可配置 human-in-the-loop |
| 控制流 | prompt 协议 | prompt + Python 代码 |

---

## 七、工程价值

AutoGen 把 Agent 系统拆成几个可复用部件：

- 角色定义。
- 消息协议。
- 自动回复。
- 工具/代码执行。
- 人类介入模式。
- 群聊管理。
- 终止条件。

这基本覆盖了一个多 Agent 应用框架的骨架。

---

## 八、局限

1. **框架不等于可靠性**：AutoGen 提供编排能力，但任务成败仍依赖模型、工具和验证器。
2. **对话流可能失控**：如果终止条件和回复函数设计不好，会循环或跑偏。
3. **成本较高**：多 Agent 多轮对话会带来更多 token 和工具调用。
4. **调试复杂**：错误可能来自 prompt、工具、执行环境、消息路由或模型本身。
5. **安全挑战**：代码执行和工具调用必须有沙箱、权限和审计。

---

## 九、为什么重要

AutoGen 是多 Agent 工程化的重要节点。它把 ReAct / CAMEL 等思想落到了开发者可用的抽象里：

```text
Agent = 可对话对象
Workflow = 对话控制流
Tool use = 特殊 Agent 或 reply function
Human-in-the-loop = 可配置代理能力
```

后来的很多 Agent 框架都在解决类似问题：如何让多个模型、工具、人类和执行环境通过明确协议协作。

---

## 十、对 Agent 的启发

- 多 Agent 系统需要消息协议，而不是只靠自然语言自由聊天。
- 代码执行 Agent 和规划 Agent 最好分开，避免模型既写又“假装执行”。
- Human-in-the-loop 应是框架级能力，而不是临时打断。
- 群聊要有 manager 或 speaker selection，否则很容易发散。

---

## 参考 / 延伸阅读

- 论文：[AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework](https://arxiv.org/abs/2308.08155)
- 项目：[microsoft/autogen](https://github.com/microsoft/autogen)
- 相关：[[2303-CAMEL Communicative Agents for Mind Exploration of Large Language Model Society]]
