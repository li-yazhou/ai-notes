---
type: paper
paper_id: arxiv-1706.03762
title: "Attention Is All You Need"
arxiv: https://arxiv.org/abs/1706.03762
year: 2017
updated: 2026-06-28
status: summarized
primary_category: llm-architecture
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/architecture
  - method/transformer
  - year/2017
  - priority/p0
  - read/deep
---

# Attention Is All You Need：Transformer 的诞生

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/1706.03762
> 发表：NeurIPS 2017 ｜ 作者：Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin（Google Brain / Google Research / 多伦多大学）
> 代码：第一方实现见 tensor2tensor 库

---

## 一、一句话概括

**完全抛弃循环（RNN）和卷积（CNN）结构，仅用注意力机制（Attention）** 构建了一个编码器-解码器（Encoder-Decoder）序列转录模型——这就是 **Transformer**，今天几乎所有大语言模型（GPT / BERT / LLaMA…）的共同祖先。

> 这是现代深度学习最重要的"分水岭"论文之一（被引 18 万+），把自然语言处理从"序列模型"时代推进到了"注意力时代"。

---

## 二、研究动机（要解决什么问题）

论文之前的序列转录（翻译、摘要等）主流是 **RNN / LSTM / GRU**，有时搭配 CNN：

| 结构 | 致命缺陷 |
|------|----------|
| **RNN / LSTM** | **必须串行**计算（$h_t$ 依赖 $h_{t-1}$），无法并行 → 训练慢；长距离依赖仍难建模 |
| **CNN**（局部窗口） | 要堆很多层才能让远处 token 交互，路径长度 $O(\log_k n)$，且感受野受限 |
| 当时的注意力机制 | 只作为 RNN 的**附加配件**（add-on），主干仍是循环网络 → 串行瓶颈仍在 |

**核心问题**：能不能让序列中**任意两个位置直接交互**（$O(1)$ 路径），同时**完全并行**计算？

**洞察**：注意力机制本身就具备"全局视野"——为什么还要留着 RNN/CNN 当主干？**把它们全部删掉，只保留注意力。**

---

## 三、方法：Transformer 架构

### 1. 总体：Encoder-Decoder

```
输入序列 → [Encoder × 6 层] → 编码序列
                                  ↓（注意力连接）
输出序列 ← [Decoder × 6 层] ← ────┘
```

- **Encoder**：6 层堆叠，每层两个子层（Self-Attention + Feed-Forward）
- **Decoder**：6 层堆叠，每层三个子层（**Masked** Self-Attention + Cross-Attention + Feed-Forward）
- 所有子层都用 **残差连接（Residual）+ Layer Normalization**：$y = \text{LayerNorm}(x + \text{Sublayer}(x))$
- 每层的输出维度 $d_{\text{model}} = 512$

### 2. 核心创新一：Scaled Dot-Product Attention

$$
\text{Attention}(Q, K, V) = \text{softmax}\!\left(\frac{QK^T}{\sqrt{d_k}}\right) V
$$

- **Q（Query）/ K（Key）/ V（Value）**：输入分别经过三个线性变换得到
- 直觉：Q 和每个 K 算相似度 → softmax 得权重 → 用权重对 V 加权求和
- **为什么除以 $\sqrt{d_k}$（Scaling）**：当维度 $d_k$ 大时，点积结果方差变大，softmax 会落入**梯度极小**的饱和区。除以 $\sqrt{d_k}$ 把方差压回 1，稳定训练。这是相对加性注意力（additive attention）的一个关键工程细节。

> 对比：论文对比了"点积注意力"和"加性注意力"，两者理论相似，但点积可用矩阵乘法大幅加速（所以选点积，并加 scaling）。

### 3. 核心创新二：Multi-Head Attention（多头注意力）

与其做一个 512 维的大注意力，不如**拆成 $h=8$ 个并行的"头"**，每个头维度 $d_k = d_v = 64$，独立做注意力，最后拼接再线性映射：

$$
\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,\dots,\text{head}_h) W^O
$$

**为什么多头**：不同头能学到**不同子空间的关注模式**（有的关注语法、有的关注长距离语义、有的关注局部），比单头表达力更强。这是 Transformer 表征能力的关键来源。

### 4. 三种注意力使用方式（论文 §3.2.3）

| 类型 | Q 来自 | K/V 来自 | 作用 |
|------|--------|----------|------|
| **Self-Attention（Encoder）** | 编码器输入 | 编码器输入 | 源序列内部全局交互 |
| **Masked Self-Attention（Decoder）** | 解码器输入 | 解码器输入 | 目标序列内部交互，但**屏蔽未来位置**（防止"偷看"右侧 token，保证自回归） |
| **Cross-Attention（Encoder-Decoder）** | 解码器上一层输出 | **编码器输出** | 让解码器决定"源句的哪一部分与当前生成最相关" |

> Mask 实现：在 softmax 前把"未来位置"的点积置为 $-\infty$（softmax 后归零）。

### 5. Position-wise Feed-Forward Network（FFN）

每个位置独立、相同地过一个两层 MLP：

$$
\text{FFN}(x) = \max(0, xW_1 + b_1) W_2 + b_2
$$

- 输入/输出维度 512，**隐藏层维度 2048**（扩大 4 倍，引入非线性容量）
- 跨位置共享权重，但每个位置独立计算（等价于对每个 token 做 1D 卷积）

### 6. 核心创新三：Positional Encoding（位置编码）

注意力本身是**置换等变的**（没有顺序概念）——必须显式注入位置信息。

论文用**正弦/余弦函数**（无需学习）：

$$
PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d})，\quad PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d})
$$

- 不同维度用不同频率的正余弦波
- 优点：可外推到训练时没见过的更长序列；相对位置可由线性函数表示
- （后来 BERT/GPT 等更多用**可学习位置编码** Learned PE，论文也做了对比，两者效果接近）

---

## 四、训练细节

- **优化器**：Adam，$\beta_1=0.9,\ \beta_2=0.98,\ \epsilon=10^{-9}$
- **学习率调度**（关键，被后世广泛沿用）：

$$
lr = d_{\text{model}}^{-0.5} \cdot \min(\text{step}^{-0.5},\ \text{step} \cdot \text{warmup\_steps}^{-1.5})
$$

  - 前 warmup 步线性增（避免初期不稳），之后按 $\sqrt{\text{step}}$ 衰减
- **正则化**：
  1. **Dropout**（$P=0.1$）：作用于每个子层输出和 embedding
  2. **Label Smoothing**（$\epsilon_{ls}=0.1$）：降低过拟合、提升 BLEU 和置信度校准
- 训练基础模型在 8× P100 GPU 上约 12 小时

---

## 五、实验结果

### 1. 机器翻译（核心战场）

| 任务 | 指标 | Transformer (big) | 当时 SOTA |
|------|------|------------------|----------|
| **WMT 2014 英→德** | BLEU | **28.4** | 26.30（集成模型）|
| **WMT 2014 英→法** | BLEU | **41.8** | 41.16（集成模型）|

> 英→德提升 **2.0+ BLEU**，是当时单模型超越最强集成模型的**断层式进步**。

### 2. 训练成本（决定性优势）

- 训练成本仅为当时最优模型（by GNMT+RL 等组合）的**一小部分**
- 并行度高，可在更短时间、更少算力下达到更好效果

### 3. 英语句法分析（泛化性验证）

- 在 WSJ 任务上，即便用 4 倍更小数据训练，Transformer 仍达到接近 SOTA 的 F1
- 证明：**大且可并行训练的模型 = 更少任务专属调参 → 更好泛化**

---

## 六、关键设计权衡（论文的工程智慧）

| 决策 | 选择 | 理由 |
|------|------|------|
| 注意力函数 | 点积 > 加性 | 可用矩阵乘法大规模并行加速 |
| 点积缩放 | 除以 $\sqrt{d_k}$ | 防止高维下方差过大 → softmax 饱和 → 梯度消失 |
| 单头 vs 多头 | 多头（h=8） | 在不同表示子空间并行关注不同模式 |
| 位置编码 | 正弦 | 可外推到更长序列，无需学习 |
| 层数/维度 | 6 层 / d=512 | 在算力与效果之间取平衡（big 变体 d=1024）|

---

## 七、局限与不足（论文坦诚 + 后续认知）

1. **长序列复杂度 $O(n^2)$**：自注意力对序列长度的计算/内存是平方级，处理超长文本/图像/视频代价高昂（→ 后来催生 Sparse Attention、Linformer、FlashAttention、Mamba 等）。
2. **位置编码外推能力有限**：固定 PE 在远超训练长度的序列上仍会退化。
3. **纯注意力对某些结构化任务不如 RNN/CNN**：如细粒度位置建模、小数据场景。
4. **论文只解决序列转录**：生成式预训练、上下文学习等能力当时还未被揭示（由 GPT/BERT 等后续工作补全）。

---

## 八、为什么这篇论文重要（历史地位）

1. **终结了"序列模型"时代**：证明了"**纯注意力 + 残差 + MLP**"足以在序列任务上全面碾压 RNN/CNN，从此 RNN 几乎从主流 NLP 退场。
2. **极致并行 = 规模化的前提**：正是因为没有循环依赖，Transformer 才能堆到百亿、千亿参数，撑起 **Scaling Law** 时代——它是 GPT-3/4、LLaMA、Gemini 的共同骨架。
3. **跨模态统一**：文本、图像（ViT）、音频、蛋白质（AlphaFold2）、代码…… 都被"注意力化"，Transformer 成为**通用近似架构**。
4. **工程范式输出**：残差 + LayerNorm + 预训练 LR warmup + Label Smoothing 等成为后世深度学习训练的标准配方。

---

## 九、对我后续工作的启发

- **理解一切现代 LLM 的起点**：读 GPT/BERT/LLaMA 的任何架构改动（RoPE、GQA、SwiGLU、RMSNorm…）都是"在 Transformer 基础上做什么替换"，不懂原文就难理解改动的动机。
- **$O(n^2)$ 瓶颈是当前很多工程优化（KV Cache、PagedAttention、FlashAttention）要解决的核心矛盾**——回到原论文能看清矛盾从何而来。
- **"删繁就简"的方法论**：论文最大胆之处是**敢把主流组件（RNN/CNN）整个删掉**，这种"能不能更简单"的追问值得迁移到自己的系统设计中。

---

## 参考 / 延伸阅读

- 论文：[arxiv.org/abs/1706.03762](https://arxiv.org/abs/1706.03762)
- 经典注解：The Annotated Transformer（Harvard NLP）、Jay Alammar《The Illustrated Transformer》
- 直接后续：
  - **BERT**（Devlin et al., 2018）：仅用 Encoder，双向预训练
  - **GPT 系列**（OpenAI）：仅用 Decoder，自回归生成
  - **T5**（Raffel et al., 2019）：Encoder-Decoder，统一为 text-to-text
- 本仓库关联：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]（Transformer 是其底层模型基础）
