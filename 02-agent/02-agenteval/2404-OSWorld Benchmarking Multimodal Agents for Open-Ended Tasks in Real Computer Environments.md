---
type: paper
paper_id: arxiv-2404.07972
title: "OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments"
arxiv: https://arxiv.org/abs/2404.07972
year: 2024
updated: 2026-06-28
status: summarized
primary_category: os-agent
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/os-agent
  - agent/multimodal
  - eval/agent-benchmark
  - env/os
  - year/2024
  - priority/p0
  - read/deep
---

# OSWorld：在真实电脑环境中评测多模态 Agent

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2404.07972
> 项目：https://os-world.github.io/
> 发表：2024 ｜ 作者：Tianbao Xie, Danyang Zhang, Jixuan Chen 等

---

## 一、一句话概括

**OSWorld** 是一个面向真实操作系统和桌面应用的多模态 Agent 评测环境，包含 369 个开放式电脑任务，并通过执行结果脚本判断任务是否完成。

它的重要性在于：把 Agent 评测从网页、游戏、代码环境进一步推进到“真实电脑使用”。

---

## 二、核心动机

如果 AI Agent 要成为真正的电脑助手，它需要能操作：

- 浏览器。
- 桌面软件。
- 文件系统。
- 多应用工作流。
- 操作系统设置。

但很多早期 benchmark 不是静态任务，就是只覆盖某个单一应用。OSWorld 试图提供一个统一、可扩展、可复现的真实电脑环境。

---

## 三、环境设计

OSWorld 支持跨操作系统的任务设置和评测：

- Ubuntu。
- Windows。
- macOS。

它强调三件事：

1. **任务初始状态可配置**：每个任务都有详细的 setup。
2. **Agent 在真实 GUI / 应用中行动**：不是只调用文本 API。
3. **结果用执行脚本验证**：通过文件、应用状态、配置变化等判断成功。

---

## 四、任务类型

OSWorld 包含 369 个真实电脑任务，覆盖：

| 类型 | 示例能力 |
|---|---|
| Web + Desktop | 浏览器和本地应用协同 |
| OS File I/O | 文件查找、修改、移动、转换 |
| Office / Productivity | 文档、表格、邮件、日程等工作流 |
| System Settings | 系统配置和应用设置 |
| Multi-Application Workflow | 多应用之间复制、处理、保存信息 |

这些任务通常需要视觉理解、GUI 定位、操作知识和长期步骤执行。

---

## 五、关键结果

论文报告的差距非常大：

| 执行者 | 成功率 |
|---|---|
| 人类 | 72.36%+ |
| 最强模型 Agent | 约 12.24% |

主要失败原因：

- GUI grounding 不稳：看得见界面，但点不准、理解不准。
- 操作知识不足：不知道软件功能在哪里。
- 长程任务中忘记目标或中间状态。
- 多应用切换时上下文丢失。
- 对文件和系统状态变化缺少可靠验证。

---

## 六、为什么重要

OSWorld 是“电脑使用 Agent”方向的关键评测节点。它把任务从 WebArena 的网页扩展到了更广义的人机交互：

```text
视觉理解
+ 鼠标键盘操作
+ 文件系统
+ 多应用工作流
+ 执行式验证
```

这对 GUI Agent、Computer Use、桌面自动化助手、VLM Agent 都很重要。

---

## 七、局限

1. **环境搭建复杂**：真实 OS、应用、状态重置和执行脚本维护成本高。
2. **动作空间大**：GUI 操作自由度高，评测稳定性比文本任务更难保证。
3. **不同 OS 差异明显**：跨系统泛化仍是挑战。
4. **任务数量有限**：369 个任务质量较高，但覆盖真实电脑使用仍只是开始。
5. **安全问题突出**：真实电脑 Agent 涉及文件、隐私、权限和误操作风险。

---

## 八、对 Agent 的启发

- 电脑 Agent 不能只会“看图说话”，还必须会精确定位和执行。
- GUI 任务需要可恢复的状态管理和动作验证。
- 真实办公任务经常跨应用，单应用 benchmark 不够。
- 评测应尽量用最终系统状态，而不是动作轨迹相似度。

---

## 参考 / 延伸阅读

- 论文：[OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments](https://arxiv.org/abs/2404.07972)
- 项目：[OSWorld](https://os-world.github.io/)
- 相关：[[2307-WebArena A Realistic Web Environment for Building Autonomous Agents]]

