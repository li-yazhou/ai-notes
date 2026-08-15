---
type: paper
paper_id: arxiv-2303.08774
title: "GPT-4 Technical Report"
arxiv: https://arxiv.org/abs/2303.08774
year: 2023
updated: 2026-06-28
status: summarized
primary_category: frontier-model-report
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/frontier-model
  - llm/multimodal
  - model/gpt
  - model/gpt-4
  - eval/model-benchmark
  - eval/safety
  - method/rlhf
  - method/scaling
  - year/2023
  - priority/p0
  - read/deep
---

# GPT-4 Technical Report：能力跃迁、可预测扩展与安全报告

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2303.08774
> 发表：OpenAI technical report, 2023；arXiv v6: 2024-03-04 ｜ 作者：OpenAI

---

## 一、一句话概括

**GPT-4 Technical Report** 不是一篇完整公开训练细节的模型论文，而是一份关于 GPT-4 能力、局限、安全缓解和可预测扩展的技术报告。

它的核心信息是：GPT-4 是一个可处理图像和文本输入、输出文本的大规模多模态 Transformer，经 next-token pretraining 和 RLHF 后，在大量专业考试、学术 benchmark、代码和数学任务上显著超过 GPT-3.5。

---

## 二、报告边界

论文明确说明：由于竞争和安全考虑，报告**不公开**以下信息：

- 模型规模。
- 具体架构细节。
- 硬件配置。
- 训练 compute。
- 数据集构造。
- 训练方法细节。

因此，GPT-4 Technical Report 更适合被理解为：

```text
能力评估报告 + 安全系统卡 + 部分 scaling 可信度说明
```

而不是像 GPT-2 / GPT-3 那样相对完整的训练论文。

---

## 三、模型概况

报告公开的信息包括：

- GPT-4 是 Transformer-style 模型。
- 预训练目标仍是预测文档中的下一个 token。
- 训练数据包含公开数据、互联网数据和第三方授权数据。
- 经过 RLHF 进行对齐微调。
- 模型可接受图像和文本输入，输出文本。

这说明 GPT-4 延续 GPT 系列的语言模型主线，但加入了多模态输入能力和更系统的 post-training 安全流程。

---

## 四、Predictable Scaling

GPT-4 项目的一个重点是构建可预测扩展的训练栈。

报告强调：像 GPT-4 这样的大训练跑法，无法在目标规模上反复试错，因此必须用小规模模型预测大模型行为。

### 1. Loss prediction

OpenAI 用比 GPT-4 少 `1,000x` 到 `10,000x` compute 的小模型，拟合 scaling law 来预测 GPT-4 在内部代码数据集上的最终 loss。预测在训练早期完成，没有使用最终训练结果。

报告称最终 loss 被高精度预测。

### 2. Capability prediction

除了 loss，团队还尝试预测更可解释的能力指标，例如 HumanEval pass rate。方法是用小模型在不同 compute 下的结果外推 GPT-4。

这部分的意义不只是工程炫技，而是安全治理：如果能在训练完成前预测能力，就能更早规划 alignment、红队测试和部署边界。

---

## 五、能力评测

### 1. 专业与学术考试

GPT-4 在大量人类考试上表现接近或超过多数人类考生。最著名结果是：

- 模拟 Uniform Bar Exam：约位于考生前 10%。
- GPT-3.5 在同一考试上约位于后 10%。

报告还覆盖 SAT、GRE、AP、医学、法律等考试。需要注意，这些是模拟考试环境，不等于真实职业能力。

### 2. 标准 NLP / 推理 benchmark

报告中的代表性结果：

| Benchmark | GPT-4 | GPT-3.5 | 备注 |
|---|---:|---:|---|
| MMLU | 86.4% | 70.0% | 57 个学科多选题 |
| HellaSwag | 95.3% | 85.5% | 常识事件推理 |
| ARC-Challenge | 96.3% | 85.2% | 小学科学题 |
| WinoGrande | 87.5% | 81.6% | 指代/常识 |
| HumanEval | 67.0% | 48.1% | Python 代码生成 |
| DROP | 80.9 F1 | 64.1 F1 | 阅读理解 + 算术 |
| GSM-8K | 92.0% | 57.1% | 小学数学，使用 CoT |

报告称 GPT-4 在这些任务上超过已有 LM，并在除 DROP 外的大多数任务上超过带任务特定训练的 SOTA。

### 3. 多语言 MMLU

GPT-4 在翻译版 MMLU 中表现强，报告称在 26 种语言中的 24 种超过当时英文语言模型 SOTA。这说明 GPT-4 的能力不只局限于英文 benchmark。

### 4. 用户偏好

在来自 ChatGPT 和 OpenAI API 的 5,214 个 prompt 上，人类标注者更偏好 GPT-4 回答而非 GPT-3.5 回答，比例为 `70.2%`。

---

## 六、多模态能力

GPT-4 可以处理图像和文本混合 prompt。报告只给了少量示例和窄范围视觉 benchmark 的说明，更多视觉能力细节留给后续工作。

因此阅读时要注意：这篇报告确认了 GPT-4 的多模态方向，但并没有系统公开视觉训练数据、视觉编码结构或完整多模态评测。

---

## 七、局限

报告非常明确地列出 GPT-4 的局限：

- 仍会 hallucinate。
- 仍会出现推理错误。
- 上下文窗口有限。
- 不会从使用经验中持续学习。
- 多数预训练数据截止到 2021 年 9 月前，后续事件知识有限。
- 可能自信地犯错，不一定主动复核。
- post-training 改善行为但会降低校准。
- 仍存在偏见和安全风险。

这点对 Agent 特别重要：更强模型不等于可靠自治系统，工具验证、检索增强、执行约束和人工审核仍然必要。

---

## 八、安全与对齐

报告和系统卡讨论了 GPT-4 的风险与缓解：

- 邀请 50 多位领域专家做 adversarial testing / red teaming。
- 使用 RLHF 改善遵循用户意图的行为。
- 使用 rule-based reward models 作为额外奖励信号，强化拒绝不安全请求、避免过度拒绝安全请求。
- 与 GPT-3.5 相比，GPT-4 对 disallowed content 的响应倾向降低 `82%`。
- 对 sensitive requests 的合规回应提升 `29%`。
- RealToxicityPrompts 上 toxic generations 为 `0.73%`，而 GPT-3.5 为 `6.48%`。

但报告也承认：模型层面的干预不能完全防止 jailbreak，需要部署期监控和快速迭代。

---

## 九、历史意义

GPT-4 Technical Report 的历史意义有三层：

1. **能力层面**：GPT-4 把通用语言模型能力推进到可在很多专业考试和复杂 benchmark 上达到高水平的阶段。
2. **工程层面**：报告强调大训练必须可预测，不能靠目标规模反复试错。
3. **治理层面**：模型发布不再只是论文和 benchmark，而是同时包含系统卡、安全评估、红队和部署缓解。

---

## 十、与 Agent 的关系

GPT-4 是 2023 年大量 Agent 工作的默认强基座：WebGPT 后续、Voyager、WebArena、AutoGen / MetaGPT 实验、工具调用和代码修复都大量依赖 GPT-4 的推理、代码、长上下文和指令遵循能力。

但这篇报告也提醒：

- Agent 不能只靠模型自信输出。
- 高风险任务需要外部验证和权限边界。
- 评测应同时覆盖能力、安全、可靠性、滥用风险。
- 可预测扩展和危险能力预评估会成为 frontier model 时代的重要基础设施。

---

## 十一、阅读结论

GPT-4 报告不是“教你如何训练 GPT-4”的论文，而是“如何评估和部署 frontier model”的关键文献。

如果按发展脉络读：

```text
GPT-1：预训练 + 微调
GPT-2：zero-shot 任务迁移
GPT-3：in-context few-shot learning
GPT-4：frontier capability + scaling predictability + safety deployment
```

这四篇合起来，就是 GPT 系列从语言模型到通用助手基座的主线。

---

## 十二、关联笔记

- [[2005-Language Models are Few-Shot Learners|Language Models are Few-Shot Learners]]
- [[1901-Language Models are Unsupervised Multitask Learners|Language Models are Unsupervised Multitask Learners]]
- [[1801-Improving Language Understanding by Generative Pre-Training|Improving Language Understanding by Generative Pre-Training]]
- [[2501-Humanitys Last Exam|Humanity's Last Exam]]
- [[2009-MMLU Measuring Massive Multitask Language Understanding|Measuring Massive Multitask Language Understanding]]
- [[AI Agent 与大模型评测论文地图]]

