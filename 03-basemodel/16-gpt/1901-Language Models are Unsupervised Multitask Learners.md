---
type: paper
paper_id: openai-2019-gpt2
title: "Language Models are Unsupervised Multitask Learners"
paper_url: https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
year: 2019
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
  - model/gpt-2
  - method/zero-shot
  - method/unsupervised-multitask
  - year/2019
  - priority/p0
  - read/deep
---

# Language Models are Unsupervised Multitask Learners：GPT-2 与 Zero-Shot 任务迁移

> 更新时间：2026-06-28
> 论文地址：https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf
> 发表：OpenAI technical report / ICML 2019 proceedings metadata ｜ 作者：Alec Radford, Jeffrey Wu, Rewon Child, David Luan, Dario Amodei, Ilya Sutskever

---

## 一、一句话概括

**GPT-2** 证明了一个重要转折：只用语言模型目标在大规模高质量网页文本上训练，模型会开始在没有微调、没有参数更新、没有任务专用架构的情况下完成问答、翻译、阅读理解、摘要等任务。

如果 [[1801-Improving Language Understanding by Generative Pre-Training|GPT-1]] 的关键词是 **pre-train + fine-tune**，GPT-2 的关键词就是 **zero-shot task transfer**。

---

## 二、核心问题

传统 NLP 系统一般要为每个任务收集标注数据、设计训练目标、训练或微调模型。GPT-2 论文想验证一个更激进的假设：

> 如果语言模型在足够大、足够多样的文本上训练，它会不会从自然文本中自动学习任务示范，从而在测试时只靠自然语言上下文完成任务？

论文把这种现象称为 **unsupervised multitask learning**。这里的“多任务”不是显式给模型多个任务数据集，而是认为网页文本中自然包含很多任务示范，例如翻译、问答、摘要、解释、列表、代码片段等。

---

## 三、方法

### 1. WebText 数据集

GPT-2 没有直接使用未过滤 Common Crawl，而是构建了 **WebText**：

- 从 Reddit 外链抓取网页。
- 只保留获得至少 3 karma 的链接，作为“人类过滤质量”的启发式指标。
- 使用 Dragnet 和 Newspaper 抽取正文。
- 去重和清洗后，约 800 多万文档、40GB 文本。
- 移除 Wikipedia，避免和常见评测集产生明显重叠。

这一步很关键：GPT-2 的效果不只是模型变大，也来自训练数据从 BooksCorpus 变成了更开放、更丰富的网页文本。

### 2. 输入表示：Byte-level BPE

GPT-2 使用 byte-level BPE，词表大小 50,257。它保留了 BPE 对常见词片段建模的效率，同时避免传统词表的 OOV 问题，使模型能给任意 Unicode 字符串分配概率。

这也是后来 GPT 系列 tokenizer 设计的重要源头。

### 3. 模型结构

GPT-2 仍是 decoder-only Transformer，但相对 GPT-1 做了放大和工程修改：

| 模型 | 层数 | hidden size | 参数量 |
|---|---:|---:|---:|
| small | 12 | 768 | 117M |
| medium | 24 | 1024 | 345M |
| large | 36 | 1280 | 762M |
| GPT-2 | 48 | 1600 | 1542M |

其他关键点：

- context length 从 512 扩到 1024。
- 使用 pre-activation 风格 LayerNorm。
- 残差路径初始化按深度缩放。
- batch size 为 512。

---

## 四、实验：Zero-Shot 评测

GPT-2 的评测原则是：**不微调，不改架构，只通过 prompt / context 指定任务。**

覆盖任务包括：

- 语言建模。
- LAMBADA 长距离依赖。
- Winograd Schema。
- CoQA 阅读理解。
- CNN / Daily Mail 摘要。
- WMT 翻译。
- Natural Questions 闭卷问答。

---

## 五、关键结果

### 1. 语言建模：7/8 数据集 zero-shot SOTA

GPT-2 在 8 个语言建模数据集中的 7 个达到当时 zero-shot SOTA。论文还指出，即使是最大 GPT-2 也仍然 underfit WebText，意味着继续扩大模型或训练可能还有收益。

这个结论后来被 GPT-3 和 scaling laws 继续放大。

### 2. LAMBADA：长距离依赖大幅提升

GPT-2 把 LAMBADA perplexity 从此前约 `99.8` 降到 `8.6`，准确率提升到约 `63.2%`。这说明大规模语言模型不只是局部续写，而是在一定程度上能利用跨句上下文。

### 3. CoQA：zero-shot 接近部分监督基线

在 CoQA 上，GPT-2 不使用 12.7 万训练样例，仍达到约 `55 F1`，匹配或超过 4 个基线系统中的 3 个。

这在当时很有冲击力：阅读理解不再只能来自显式监督训练。

### 4. Winograd：达到 70.70%

GPT-2 在 Winograd Schema Challenge 上达到 `70.70%`，比此前 SOTA 高约 7 个点。不过论文也做了重叠检查，说明部分测试样例在 WebText 中存在近似重叠，结果需要谨慎解释。

### 5. 摘要与翻译：能做，但还粗糙

GPT-2 可以通过自然语言 prompt 做摘要和翻译，但摘要 ROUGE 远不如专门监督模型。论文在 Discussion 里明确承认：在摘要等任务上，zero-shot 表现还只是 rudimentary，离实际可用很远。

---

## 六、历史意义

GPT-2 的最大意义是把 GPT 路线从“预训练后再微调”推进到“预训练本身诱导任务能力”：

- 任务能力可以从自然文本中的隐式示范中学到。
- prompt 不再只是输入格式，而开始变成任务指定机制。
- 模型规模与 zero-shot 能力呈现明显相关。
- 生成质量和开放文本能力进入公众视野。

它是 GPT-3 few-shot / in-context learning 的直接前奏。

---

## 七、局限

- zero-shot 能力在很多任务上还不可用，尤其是摘要、翻译和部分问答。
- 结果受 WebText 与评测集重叠影响，需要污染检查。
- 单向 decoder-only 表示在某些 NLU 任务上不如 BERT 式双向模型。
- WebText 来自 Reddit 外链，质量更高但也带有社区偏差。
- 生成文本更连贯，也带来滥用、虚假内容、垃圾信息生产等风险。

---

## 八、与 Agent / 大模型评测的关系

GPT-2 对 Agent 的启发在于：**任务可以通过自然语言上下文指定，而不一定通过梯度更新指定。**

后来的 Agent prompt、工具说明、轨迹格式、few-shot demonstration，都是沿着这个方向发展：把任务协议写进上下文，让模型在推理时“识别任务并执行”。

---

## 九、关联笔记

- [[1801-Improving Language Understanding by Generative Pre-Training|Improving Language Understanding by Generative Pre-Training]]
- [[2005-Language Models are Few-Shot Learners|Language Models are Few-Shot Learners]]
- [[1706-Attention Is All You Need|Attention Is All You Need]]
- [[AI Agent 与大模型评测论文地图]]

