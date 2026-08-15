---
type: paper
paper_id: arxiv-2306.05685
title: "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena"
arxiv: https://arxiv.org/abs/2306.05685
year: 2023
updated: 2026-06-28
status: summarized
primary_category: llm-judge
priority: p1
read_type: skim
tags:
  - paper
  - paper/eval
  - eval/llm-judge
  - eval/preference
  - eval/chatbot
  - year/2023
  - priority/p1
  - read/skim
---

# MT-Bench / Chatbot Arena：用 LLM-as-a-Judge 评测聊天助手

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2306.05685
> 项目：https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge
> 发表：2023 ｜ 作者：Lianmin Zheng, Wei-Lin Chiang, Ying Sheng 等

---

## 一、一句话概括

这篇论文系统研究用强 LLM 作为评委评测聊天助手，并提出 **MT-Bench** 多轮问题集和 **Chatbot Arena** 众包对战平台。

它是 LLM-as-a-Judge 和 Elo 式偏好评测的重要源头。

---

## 二、核心问题

开放式聊天助手很难用传统准确率评估，因为答案可能多样且没有唯一标准答案。

论文探索：

- GPT-4 等强模型能否近似人类偏好。
- LLM judge 有哪些偏差。
- 如何用 controlled evaluation 和 crowdsourced battle 结合评测模型。

---

## 三、关键贡献

| 组件 | 作用 |
|---|---|
| MT-Bench | 多轮开放问题集，评估对话能力 |
| Chatbot Arena | 用户盲测两个模型回答并投票 |
| LLM-as-a-Judge 分析 | 研究位置偏差、冗长偏差、自我增强偏差等 |

论文发现强 LLM judge 与人类偏好可达到 80%+ 一致性，接近人类之间一致水平。

---

## 四、与 Agent 评测的关系

Agent 评测经常需要判断开放轨迹和复杂输出：

- 研究报告好不好。
- 规划是否合理。
- 工具调用轨迹是否高效。
- 用户体验是否自然。

这些场景常需要 LLM-as-a-Judge。但论文提醒：judge 不是免疫偏差的真理机器。

---

## 五、局限与启发

局限：

- LLM judge 有位置、长度、格式和自偏好问题。
- 多轮真实任务比 MT-Bench 更复杂。
- Judge 模型版本变化会影响可复现性。

启发：

- Agent 评测中使用 judge 时应随机交换顺序、校准人工 golden set。
- Pairwise comparison 通常比绝对打分更稳。

---

## 参考 / 延伸阅读

- 论文：[Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685)
- 项目：[FastChat LLM Judge](https://github.com/lm-sys/FastChat/tree/main/fastchat/llm_judge)

