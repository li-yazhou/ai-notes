---
type: paper
paper_id: arxiv-2310.08560
title: "MemGPT: Towards LLMs as Operating Systems"
arxiv: https://arxiv.org/abs/2310.08560
year: 2023
updated: 2026-06-28
status: summarized
primary_category: agent-loop-memory
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/memory
  - method/context-management
  - year/2023
  - priority/p1
  - read/skim
---

# MemGPT：把大模型记忆管理做成操作系统式虚拟上下文

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2310.08560
> 项目：https://memgpt.ai/
> 发表：2023 ｜ 作者：Charles Packer, Vivian Fang, Shishir G. Patil 等

---

## 一、一句话概括

**MemGPT** 借鉴操作系统的分层内存管理，让 LLM 在有限上下文窗口内主动管理短期和长期记忆，从而支持长文档分析和跨会话对话。

它的重要性在于：把“上下文窗口不够”转化为“记忆分页和调度”问题。

---

## 二、核心思想

MemGPT 提出 **virtual context management**：

```text
有限上下文窗口 = 快速内存
外部存储 / 长期记忆 = 慢速内存
LLM = 决定何时读写、换入换出的控制器
```

模型可以通过函数调用管理不同记忆层，并使用类似 interrupt 的机制与用户或系统交互。

---

## 三、应用场景

论文评估两个代表场景：

| 场景 | 解决的问题 |
|---|---|
| 长文档分析 | 文档长度超过上下文窗口 |
| 多会话聊天 | Agent 需要长期记住用户和历史互动 |

MemGPT 让 Agent 能在有限窗口内维护“看起来更大的上下文”。

---

## 四、为什么重要

Agent 长期运行必然遇到记忆问题。MemGPT 的贡献是把记忆从“把所有历史塞进 prompt”推进为：

- 分层存储。
- 主动换入换出。
- 显式读写工具。
- 长期用户状态。
- 可持续对话代理。

这和后续 memory provider、personal agent、long-running agent 的设计密切相关。

---

## 五、局限与启发

局限：

- 模型自己决定记忆读写，可能写错、漏写或污染记忆。
- 记忆检索质量影响后续行为。
- 长期记忆涉及隐私、删除、权限和审计问题。

启发：

- Agent 记忆不应只靠长上下文，应设计为外部状态系统。
- 记忆写入要有策略和约束，否则长期会积累噪声。

---

## 参考 / 延伸阅读

- 论文：[MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- 项目：[MemGPT](https://memgpt.ai/)

