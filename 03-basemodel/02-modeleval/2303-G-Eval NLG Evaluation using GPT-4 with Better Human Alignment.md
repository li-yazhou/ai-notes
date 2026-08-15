---
type: paper
paper_id: arxiv-2303.16634
title: "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"
arxiv: https://arxiv.org/abs/2303.16634
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
  - eval/open-ended
  - method/cot
  - year/2023
  - priority/p1
  - read/skim
---

# G-Eval：用 GPT-4 和 CoT 做开放文本评价

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.16634
> 项目：https://github.com/nlpyang/geval
> 发表：2023 ｜ 作者：Yang Liu, Dan Iter, Yichong Xu 等

---

## 一、一句话概括

**G-Eval** 使用 GPT-4 结合 Chain-of-Thought 和表单化评分范式，评估摘要、对话等开放式自然语言生成结果，并取得更高的人类相关性。

它是 LLM-as-a-Judge 从经验做法走向系统方法的重要论文。

---

## 二、核心动机

BLEU、ROUGE 等传统指标对开放生成质量相关性有限，尤其难评估创造性、连贯性、事实性和对话质量。

G-Eval 试图用强 LLM 直接评估生成文本，并通过结构化 rubric 和 CoT 提升稳定性。

---

## 三、方法

G-Eval 的基本流程：

```text
输入任务说明 + 待评文本 + 评价标准
  ↓
GPT-4 生成评估步骤 / 理由
  ↓
按表单输出分数
```

它不依赖参考答案，因此适合摘要、对话、开放回答等 reference-free 场景。

---

## 四、关键结果

论文在文本摘要和对话生成任务上评估，G-Eval with GPT-4 在摘要任务上与人类判断的 Spearman 相关达到 0.514，显著超过以往自动指标。

论文也指出：LLM-based evaluator 可能偏爱 LLM 生成文本。

---

## 五、与 Agent 评测的关系

Agent 输出常常没有唯一答案：

- 调研报告质量。
- 多步计划质量。
- 工具轨迹是否合理。
- 对话是否有帮助。

这些都需要类似 G-Eval 的 judge/rubric 机制。但 Agent 评测还要额外考虑工具副作用、成本、安全和轨迹。

---

## 六、局限与启发

局限：

- Judge 可能偏好自己模型族生成的文本。
- 打分容易受格式、长度、位置影响。
- 分数可解释性依赖 rubric 质量。

启发：

- LLM-as-a-Judge 必须配合校准集和偏差分析。
- 对 Agent 轨迹评价，理由比单个分数更重要。

---

## 参考 / 延伸阅读

- 论文：[G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment](https://arxiv.org/abs/2303.16634)
- 项目：[G-Eval](https://github.com/nlpyang/geval)
- 相关：[[2306-MT-Bench and Chatbot Arena Judging LLM-as-a-Judge]]

