---
type: paper
paper_id: arxiv-2309.15817
title: "Identifying the Risks of LM Agents with an LM-Emulated Sandbox"
arxiv: https://arxiv.org/abs/2309.15817
year: 2023
updated: 2026-06-28
status: summarized
primary_category: safety-reliability
priority: p1
read_type: skim
tags:
  - paper
  - paper/eval
  - paper/safety
  - eval/safety
  - agent/tool-use
  - method/sandbox
  - year/2023
  - priority/p1
  - read/skim
---

# ToolEmu：用语言模型模拟沙箱识别 Agent 工具风险

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2309.15817
> 发表：2023 ｜ 作者：Zhang 等

---

## 一、一句话概括

**ToolEmu** 使用语言模型模拟工具执行环境，低成本测试 LM Agent 在高风险工具场景中的失败和安全风险。

它的重要性在于：Agent 一旦能调用工具，评测就必须关注副作用、隐私泄露、经济损失等真实风险。

---

## 二、核心动机

真实测试 Agent 工具风险很昂贵：

- 要实现工具。
- 要搭环境和状态。
- 要构造危险场景。
- 真实执行可能造成副作用。

ToolEmu 用 LM-emulated sandbox 模拟工具执行，降低风险发现成本。

---

## 三、方法

ToolEmu 包含：

```text
LM 工具模拟器
  +
LM 安全评估器
  +
高风险工具与测试用例
```

模拟器生成工具执行结果，评估器检查 Agent 行为是否导致风险。

论文初始 benchmark 包含 36 个高风险工具和 144 个测试用例。

---

## 四、关键发现

人工评估显示，ToolEmu 识别出的失败中有 68.8% 会是真实世界有效失败。即使最安全的 LM Agent，也在 evaluator 下出现 23.9% 的潜在严重失败。

这说明工具 Agent 的安全风险不是边缘问题，而是部署前必须系统评测的核心问题。

---

## 五、局限与启发

局限：

- LM 模拟工具不等于真实工具，可能漏报或误报。
- 安全评估器本身也可能有偏差。
- 高风险场景覆盖永远不完备。

启发：

- 上线前应先用模拟环境做红队测试。
- 工具调用安全需要场景级评测，而不是只看模型拒答。

---

## 参考 / 延伸阅读

- 论文：[Identifying the Risks of LM Agents with an LM-Emulated Sandbox](https://arxiv.org/abs/2309.15817)
- 相关：[[2407-AI Agents That Matter]]

