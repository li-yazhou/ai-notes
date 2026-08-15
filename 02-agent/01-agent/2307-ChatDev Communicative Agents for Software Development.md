---
type: paper
paper_id: arxiv-2307.07924
title: "ChatDev: Communicative Agents for Software Development"
arxiv: https://arxiv.org/abs/2307.07924
year: 2023
updated: 2026-06-28
status: summarized
primary_category: multi-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/multi-agent
  - agent/software-agent
  - env/code
  - year/2023
  - priority/p1
  - read/skim
---

# ChatDev：用多智能体对话模拟软件公司开发流程

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2307.07924
> 项目：https://github.com/OpenBMB/ChatDev
> 发表：2023 ｜ 作者：Chen Qian, Xin Cong, Cheng Yang 等

---

## 一、一句话概括

**ChatDev** 将软件开发过程建模为一个由多个 LLM Agent 组成的虚拟软件公司，通过自然语言和代码语言对话完成设计、编码、测试等阶段。

它是多智能体软件开发方向中非常早期且有影响力的系统。

---

## 二、核心设计

ChatDev 关注两个问题：

- 多个专业 Agent 应该交流什么。
- 如何减少交流中的幻觉和不一致。

系统使用 **chat chain** 组织软件开发阶段，让不同角色在固定流程中协作，例如 CEO、CTO、程序员、测试员等。

---

## 三、关键机制

### 1. Chat Chain

将软件开发拆成多个阶段：

```text
需求 → 设计 → 编码 → 测试 → 文档
```

每个阶段由对应角色通过对话完成。

### 2. Communicative Dehallucination

通过结构化沟通和阶段约束减少幻觉。例如要求 Agent 在调试中使用更具体的代码语言交流，而不是泛泛讨论。

---

## 四、与 MetaGPT 的关系

ChatDev 和 MetaGPT 都把软件开发映射成多角色协作：

| 维度 | ChatDev | MetaGPT |
|---|---|---|
| 核心 | 对话驱动的软件公司 | SOP 驱动的软件团队 |
| 重点 | 多角色交流过程 | 标准化产物和流程 |
| 风格 | 更像模拟公司 | 更像工程流水线 |

两者共同推动了“多智能体软件工程”这一范式。

---

## 五、局限与启发

局限：

- 任务规模偏小，距离真实工程项目仍远。
- 对话越长越容易积累错误。
- 自动测试和真实运行反馈不足时，代码质量难保证。

启发：

- 多 Agent 协作不能自由聊天，必须有阶段、角色和交付物。
- 软件开发 Agent 最好把设计、实现、测试拆开，让错误更容易定位。

---

## 参考 / 延伸阅读

- 论文：[ChatDev: Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924)
- 项目：[OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)
- 相关：[[2308-MetaGPT Meta Programming for A Multi-Agent Collaborative Framework]]

