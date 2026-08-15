---
type: paper
paper_id: openai-2018-gpt1
title: "Improving Language Understanding by Generative Pre-Training"
paper_url: https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
project: https://openai.com/index/language-unsupervised/
year: 2018
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
  - method/generative-pretraining
  - method/fine-tuning
  - year/2018
  - priority/p0
  - read/deep
---

# Improving Language Understanding by Generative Pre-Training：GPT 范式的起点

> 更新时间：2026-06-28
> 论文地址：https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf
> 发布页：https://openai.com/index/language-unsupervised/
> 发表：OpenAI preprint, 2018-06-11 ｜ 作者：Alec Radford, Karthik Narasimhan, Tim Salimans, Ilya Sutskever

---

## 一、一句话概括

这篇论文提出了后来被称为 **GPT-1** 的范式：**先用大规模无标注文本做生成式语言模型预训练，再在具体下游任务上做有监督微调**。

它的重要性不在模型规模本身，而在于把“Transformer + next-token prediction + task-specific fine-tuning”组织成了一个通用语言理解框架。后来的 GPT-2、GPT-3、InstructGPT、ChatGPT 都是在这条路线上继续扩展。

---

## 二、它要解决什么问题

2018 年前后的 NLP 仍高度依赖有标注数据和任务专用架构：

- 文本分类、自然语言推理、问答、语义相似度各自有不同模型设计。
- 大量任务缺少高质量标注数据，纯监督学习难以扩展。
- Word2Vec / GloVe 等词向量能迁移词级信息，但难以迁移长距离语义、篇章结构和世界知识。
- ELMo 等上下文化表示已经显示出预训练价值，但通常仍需要任务定制结构。

这篇论文的核心问题是：**能不能只训练一个通用语言模型，然后用极少架构改动迁移到很多理解任务？**

---

## 三、核心方法：两阶段训练

论文方法非常简单，但影响巨大。

### 1. 无监督生成式预训练

第一阶段在无标注文本上训练语言模型，目标是预测下一个 token：

```text
给定前文 u_1 ... u_{i-1}
最大化 P(u_i | u_1 ... u_{i-1})
```

模型用的是 **decoder-only Transformer**，也就是带 masked self-attention 的 Transformer decoder。输入 token embedding 加上 learned position embedding，经过多层 Transformer block，最后输出词表分布。

这一步让模型从连续文本中学习：

- 词法和句法规律。
- 长距离依赖。
- 常识和世界知识。
- 多句上下文中的语义关系。

### 2. 有监督微调

第二阶段把预训练参数迁移到下游任务。对于带标签数据，取最后一层 Transformer 的最后位置表示，接一个线性分类头预测标签。

微调目标是监督学习损失，同时论文发现加入辅助语言模型目标有帮助：

```text
fine-tuning objective = supervised objective + λ * language modeling objective
```

论文设置中 `λ = 0.5`。作者认为辅助 LM 目标可以改善泛化并加速收敛。

---

## 四、关键设计：把结构化任务转成 token 序列

GPT-1 最聪明的工程设计之一，是不为每个任务设计复杂架构，而是把不同任务统一转换为一段连续 token 序列。

| 任务类型 | 输入变换 |
|---|---|
| 文本分类 | 直接输入文本序列 |
| 文本蕴含 NLI | `premise $ hypothesis` |
| 语义相似度 | 同时处理 `sentence1 $ sentence2` 和 `sentence2 $ sentence1`，再合并表示 |
| 问答 / 常识推理 | 对每个候选答案构造 `context question $ answer_k`，再对候选项 softmax |

这就是后来的 **prompt / input formatting** 思想的早期形态：不改模型主体，只改输入表示方式。

---

## 五、模型与训练细节

论文中的模型规格：

- 架构：12 层 decoder-only Transformer。
- 隐状态维度：768。
- 注意力头数：12。
- FFN 内部维度：3072。
- 上下文长度：512 tokens。
- 词表：BPE，40,000 merges。
- 位置编码：learned position embeddings。
- 激活函数：GELU。
- dropout：residual / embedding / attention dropout 均为 0.1。
- 优化器：Adam，最大学习率 `2.5e-4`，warmup 2000 steps，cosine decay。

预训练数据是 **BooksCorpus**：7000 多本未出版书籍，覆盖 Adventure、Fantasy、Romance 等类型。作者特别强调 BooksCorpus 的价值在于有长段连续文本，适合学习长距离依赖；相比之下，1B Word Benchmark 是句子级打乱的，破坏了篇章结构。

OpenAI 发布页中还给出计算量估算：约 `0.96 petaflop-days`，主要来自 8 张 P600 GPU 训练 30 天。

---

## 六、实验任务

论文评估四类语言理解任务，共 12 个数据集：

| 类型 | 数据集 |
|---|---|
| 自然语言推理 | SNLI, MultiNLI, QNLI, RTE, SciTail |
| 问答 / 常识推理 | RACE, Story Cloze |
| 语义相似度 | MRPC, QQP, STS-B |
| 文本分类 | SST-2, CoLA |

这组任务覆盖了当时 GLUE 的核心任务，也包含阅读理解和常识推理。

---

## 七、关键结果

### 1. 整体：12 个任务中 9 个达到新 SOTA

论文报告在 12 个任务中有 9 个超过此前最好结果。几个代表性提升：

- Story Cloze：`86.5`，比此前最好结果高 `8.9` 个点。
- RACE：`59.0`，比此前最好结果高 `5.7` 个点。
- MultiNLI：matched `82.1`，mismatched `81.4`。
- QNLI：`88.1`，此前最好为 `82.3`。
- CoLA：`45.4`，此前最好为 `35.0`。
- GLUE 总分：`72.8`，此前最好为 `68.9`。

这在当时说明：一个通用预训练 Transformer 可以跨任务迁移，而不必每个任务重新设计模型。

### 2. NLI：大数据集效果强，小数据集仍不稳

在 MNLI、SNLI、SciTail、QNLI 上 GPT-1 都超过或接近此前 SOTA。RTE 例外：GPT-1 得到 `56.0`，低于多任务 BiLSTM 的 `61.7`。

这说明预训练虽然强，但小数据集上微调仍不稳定；后来 BERT、RoBERTa、T5 等大量工作都继续围绕这个问题改进。

### 3. 问答与常识推理：长上下文优势明显

RACE 和 Story Cloze 是论文最重视的结果。它们需要多句推理、阅读理解和常识判断，而 GPT-1 使用长段连续文本预训练，能学到比词级表示更丰富的上下文能力。

### 4. GLUE：预训练范式开始统一 NLU

GLUE 总分从此前最好 `68.9` 提升到 `72.8`。虽然几个月后 BERT 会进一步刷新这个结果，但 GPT-1 已经证明了“预训练 + 微调”可以成为统一 NLU 的主线。

---

## 八、分析与消融

论文的分析部分很值得读，因为它解释了预训练为什么有用。

### 1. 迁移更多层更有效

作者比较了迁移不同数量 Transformer 层到下游任务的效果。结果显示不仅 embedding 有用，越多层迁移通常越好，完整迁移在 MultiNLI 上能带来最高约 9% 的提升。

这说明预训练模型的高层并不是只学到表层统计，而是包含可迁移的任务相关功能。

### 2. 零样本行为会随语言模型训练增强

作者用简单启发式测试预训练模型的 zero-shot 行为：

- 对 CoLA，用句子平均 token log-probability 判断可接受性。
- 对 SST-2，在句子后追加 `very`，比较模型更倾向生成 `positive` 还是 `negative`。
- 对 RACE，选择模型赋予最高平均 log-probability 的候选答案。
- 对 Winograd 类任务，比较不同指代替换后的序列概率。

这些 zero-shot 方法绝对性能不一定高，但会随着 LM 预训练稳定提升。这是一个早期信号：**next-token prediction 本身会诱导模型学习下游任务所需的部分能力。**

### 3. Transformer 比 LSTM 更适合迁移

论文用同样框架比较 Transformer 和单层 2048 hidden units LSTM。LSTM 平均分下降 `5.6`，只在 MRPC 上超过 Transformer。

作者据此认为 Transformer 的归纳偏置更适合从长文本中学习可迁移结构。

### 4. 没有预训练会明显变差

直接从监督任务训练同样架构，平均分下降 `14.8%`。这就是整篇论文最关键的实验证据之一：**强结果不是 Transformer 架构单独带来的，而是预训练 + 微调共同带来的。**

---

## 九、历史意义

这篇论文是现代 LLM 路线的一个清晰起点。

它把几件事连在了一起：

- Transformer 从机器翻译架构变成通用语言模型架构。
- 语言模型目标从“生成文本”变成“学习通用表示”的训练信号。
- 下游任务从专用架构转向统一模型 + 输入格式化 + 微调。
- 预训练数据、模型容量、计算量开始成为语言理解能力的核心变量。

如果说 [[1706-Attention Is All You Need|Attention Is All You Need]] 给出了 Transformer 积木，那么 GPT-1 给出了后来 GPT 系列的第一版工程路线图。

---

## 十、局限

这篇论文的局限也很清楚：

- 模型仍需要每个任务的有监督微调，不是 GPT-3 式 few-shot / in-context learning。
- 预训练数据只有 BooksCorpus，规模约几个 GB，远小于后来 WebText、Common Crawl 等数据。
- 单向 decoder-only LM 不像 BERT 那样天然利用双向上下文，因此在一些 NLU 任务上很快被 BERT 超过。
- 小数据集微调不稳定，RTE 就明显落后于多任务基线。
- 计算成本在当时较高，OpenAI 发布页提到训练约需 8 张 P600 GPU 跑 30 天。
- 从文本中学习世界知识会继承文本偏见，也无法保证知识完整、准确。

---

## 十一、与后续工作的关系

| 后续方向 | 与 GPT-1 的关系 |
|---|---|
| BERT | 同样采用预训练 + 微调，但改用双向 encoder 和 masked LM，更适合 NLU |
| GPT-2 | 扩大模型和数据，弱化监督微调，展示更强开放生成能力 |
| GPT-3 | 进一步规模化，few-shot / in-context learning 成为重点 |
| InstructGPT / ChatGPT | 在预训练模型上增加指令微调和 RLHF，使模型更适合人类意图 |
| Agent | Agent 的规划、工具调用、反思都建立在通用语言模型能力之上，而 GPT-1 是这条通用预训练路线的早期奠基 |

---

## 十二、阅读结论

这篇论文适合作为 LLM 发展史中的 p0 论文来读。

读它不只是为了知道 GPT-1 的结果，而是为了理解一个范式转折：

> 语言理解能力可以先通过大规模自监督语言建模获得，再通过少量任务适配迁移出来。

这句话后来几乎成了整个大模型时代的默认假设。

---

## 十三、关联笔记

- [[1706-Attention Is All You Need|Attention Is All You Need]]
- [[1804-GLUE A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding|GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding]]
- [[1905-SuperGLUE A Stickier Benchmark for General-Purpose Language Understanding Systems|SuperGLUE]]
- [[AI Agent 与大模型评测论文地图]]

