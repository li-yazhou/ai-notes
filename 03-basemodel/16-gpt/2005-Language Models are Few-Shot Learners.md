---
type: paper
paper_id: arxiv-2005.14165
title: "Language Models are Few-Shot Learners"
arxiv: https://arxiv.org/abs/2005.14165
year: 2020
updated: 2026-06-28
status: summarized
primary_category: llm-pretraining
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/pretraining
  - llm/decoder-only
  - model/gpt
  - model/gpt-3
  - method/in-context-learning
  - method/few-shot
  - method/scaling
  - year/2020
  - priority/p0
  - read/deep
---

# Language Models are Few-Shot Learners：GPT-3 与 In-Context Learning

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2005.14165
> 发表：NeurIPS 2020 ｜ 作者：Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah 等

---

## 一、一句话概括

**GPT-3** 把 GPT-2 的 zero-shot 现象系统化为 **in-context learning**：模型不做梯度更新，只通过自然语言指令和上下文中的少量示例，在前向推理时适配新任务。

这篇论文的核心结论是：随着语言模型规模扩大，zero-shot、one-shot、few-shot 能力都会提升，尤其 few-shot 能力随规模增长更明显。

---

## 二、它解决什么问题

GPT-1 / BERT 时代的主流范式是：

```text
大规模预训练 -> 每个任务单独微调
```

这个范式虽然强，但仍然依赖任务标注数据和任务特定微调。GPT-3 论文提出的问题是：

> 能不能像人一样，只看任务说明和少量例子，就完成新任务，而不更新模型参数？

论文把这种测试时上下文内的适配称为 **in-context learning**。

---

## 三、三种评测设置

论文清楚地区分了三种设置：

| 设置 | 含义 |
|---|---|
| Zero-shot | 只给自然语言任务说明，不给示例 |
| One-shot | 给任务说明 + 1 个示例 |
| Few-shot | 给任务说明 + 尽可能多的上下文示例，通常 10-100 个 |

关键点：**这三种都不更新权重，也不做任务微调。** few-shot 里的“学习”发生在上下文窗口中，而不是梯度下降中。

---

## 四、模型与训练

GPT-3 使用与 GPT-2 相同的 autoregressive decoder-only Transformer 路线，但规模更大。

论文训练了 8 个规模：

| 模型 | 参数量 | 层数 | hidden size | heads | context |
|---|---:|---:|---:|---:|---:|
| GPT-3 Small | 125M | 12 | 768 | 12 | 2048 |
| GPT-3 Medium | 350M | 24 | 1024 | 16 | 2048 |
| GPT-3 Large | 760M | 24 | 1536 | 16 | 2048 |
| GPT-3 XL | 1.3B | 24 | 2048 | 24 | 2048 |
| GPT-3 2.7B | 2.7B | 32 | 2560 | 32 | 2048 |
| GPT-3 6.7B | 6.7B | 32 | 4096 | 32 | 2048 |
| GPT-3 13B | 13B | 40 | 5140 | 40 | 2048 |
| GPT-3 | 175B | 96 | 12288 | 96 | 2048 |

所有模型训练约 300B tokens。最大模型 GPT-3 有 175B 参数，是当时最大非稀疏语言模型之一。

训练数据混合包括：

- 过滤后的 Common Crawl。
- WebText2。
- Books1 / Books2。
- English Wikipedia。

Common Crawl 原始压缩文本约 45TB，过滤后约 570GB。训练时并非按数据大小比例采样，而是高质量数据采样权重更高。

---

## 五、核心实验结果

论文覆盖两大类评估：标准 NLP benchmark 与专门设计的快速适配任务。

### 1. Cloze / Completion

在 LAMBADA 上，GPT-3 few-shot 准确率达到 `86.4%`，比此前 SOTA 提高约 18 个点。论文强调 few-shot 示例可以把任务“框定”为最后词预测，从而减少模型生成句子续写时的格式误差。

### 2. Closed-book QA

GPT-3 不检索外部知识，只靠参数内知识回答问题：

- TriviaQA：zero-shot `64.3%`，one-shot `68.0%`，few-shot `71.2%`。
- CoQA：zero-shot `81.5 F1`，one-shot `84.0 F1`，few-shot `85.0 F1`。

这说明参数规模扩大后，语言模型不仅能生成文本，也能存储和调用大量知识。

### 3. Translation

GPT-3 的翻译能力来自预训练中的自然双语片段，而非专门翻译训练。结果显示随着模型规模增加，zero/one/few-shot 翻译都平滑提升。

### 4. Winograd / Commonsense

在原始 Winograd Schema 上，GPT-3 达到约 `88%` 左右；在更难的 Winogrande 上，zero-shot `70.2%`、one-shot `73.2%`、few-shot `77.7%`。

但 commonsense reasoning 结果并不全面强，PIQA、ARC 等任务上的 few-shot 增益较混合。

### 5. SuperGLUE

GPT-3 few-shot 在 SuperGLUE 上随模型规模和上下文示例数提升，但仍不稳定。它在 COPA、ReCoRD 等任务上很强，但 WiC 接近随机，RTE / ANLI 等自然语言推理任务仍困难。

这说明 GPT-3 不是“所有 NLU 任务都自动解决”，尤其比较、蕴含、重读长文本等任务仍是弱点。

### 6. 合成任务与新闻生成

GPT-3 在算术、单词重排、造句、语法纠错等任务上展示了 on-the-fly adaptation。论文还评估了新闻生成，发现人类识别 GPT-3 175B 生成新闻的准确率接近随机，这也是论文讨论误用风险的重要依据。

---

## 六、关键洞察

### 1. In-context learning 是规模涌现出来的强趋势

GPT-3 论文不是只报告一个大模型结果，而是训练多个尺寸模型，展示性能随规模平滑提升。few-shot 曲线比 zero-shot 更陡，说明大模型更会利用上下文示例。

### 2. Prompt 成为“任务接口”

任务不再主要通过模型头、微调数据或梯度更新指定，而是通过自然语言说明和示例格式指定。这是现代 prompt engineering、Agent instruction、工具说明、轨迹示范的源头之一。

### 3. 模型能力不等于稳定推理能力

GPT-3 在知识问答、生成和部分补全任务上很强，但在 NLI、WiC、ANLI、部分阅读理解上仍弱。它的能力更像“强大的模式识别与补全”，不是可靠的符号推理器。

---

## 七、局限

论文自己列出的局限很诚实：

- 长文本生成会重复、失去连贯性、前后矛盾。
- 对 common sense physics、ANLI、WiC、RACE、QuAC 等任务表现不佳。
- 单向 autoregressive 架构在需要双向比较、重读和短答案抽取的任务上不占优。
- 预训练目标只是 next-token prediction，可能不是通向通用智能的充分目标。
- 预训练样本效率很低，模型读过的文本远超人类一生阅读量。
- Few-shot learning 的机制不清楚：是在真正学习新任务，还是识别训练中见过的任务模式。
- 模型巨大，推理昂贵，不方便部署。
- 不可解释、校准不足，并继承训练数据偏见。
- 高质量生成会带来虚假新闻、垃圾内容、自动化舆论操纵等风险。

---

## 八、历史意义

GPT-3 是大模型时代最关键的论文之一，因为它把研究重心从“预训练后微调”推向：

```text
规模化预训练 -> 上下文内任务指定 -> 无梯度适配
```

它直接影响了：

- Prompt engineering。
- Instruction following。
- Chain-of-Thought prompting。
- Agent 的工具说明和轨迹示范。
- Few-shot benchmark 设计。
- API 时代的通用语言模型产品形态。

---

## 九、与 Agent 的关系

Agent 能成立，很大程度依赖 GPT-3 打开的接口形态：

- 用自然语言描述角色、目标、工具和约束。
- 用 few-shot 轨迹示范让模型模仿“思考-行动-观察”格式。
- 把任务状态放进上下文窗口，让模型在上下文中持续适配。
- 不为每个任务微调，而是通过 prompt 编排任务。

所以 GPT-3 是理解 ReAct、AutoGPT、WebGPT、多智能体框架之前必须读的基础论文。

---

## 十、关联笔记

- [[1901-Language Models are Unsupervised Multitask Learners|Language Models are Unsupervised Multitask Learners]]
- [[1801-Improving Language Understanding by Generative Pre-Training|Improving Language Understanding by Generative Pre-Training]]
- [[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models|Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
- [[2210-ReAct Synergizing Reasoning and Acting in Language Models|ReAct: Synergizing Reasoning and Acting in Language Models]]
- [[AI Agent 与大模型评测论文地图]]

