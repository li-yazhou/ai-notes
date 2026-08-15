---
type: paper
paper_id: arxiv-2606.19348
title: "DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence"
arxiv: https://arxiv.org/abs/2606.19348
year: 2026
updated: 2026-06-29
status: summarized
primary_category: llm-frontier-model
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/frontier-model
  - llm/long-context
  - llm/reasoning-model
  - model/deepseek
  - model/deepseek-v4
  - method/moe
  - method/sparse-attention
  - method/compressed-attention
  - method/muon
  - method/post-training
  - method/distillation
  - agent/long-horizon
  - eval/agent-benchmark
  - year/2026
  - priority/p0
  - read/deep
---

# DeepSeek-V4：百万 token 上下文与高效长程智能

> 更新时间：2026-06-29
> 论文地址：https://arxiv.org/abs/2606.19348
> 提交：2026-04-26 ｜ 机构：DeepSeek-AI
> 模型集合：https://huggingface.co/collections/deepseek-ai/deepseek-v4

---

## 一、一句话概括

**DeepSeek-V4** 是 DeepSeek 面向百万 token 上下文和长程推理/Agent 任务的 frontier MoE 技术报告：发布预览版 **DeepSeek-V4-Pro** 与 **DeepSeek-V4-Flash**，分别为 1.6T 总参数 / 49B 激活参数、284B 总参数 / 13B 激活参数，并通过 CSA + HCA 混合注意力、mHC、Muon 优化器和大规模后训练，将长上下文效率推到核心位置。

它的主问题不是“再做一个更大的模型”，而是：

> 当 test-time scaling、长链推理、工具调用和跨文档任务不断拉长上下文时，模型如何把百万 token 上下文变成可训练、可推理、可服务的能力？

---

## 二、模型概况

| 模型 | 总参数 | 每 token 激活参数 | 上下文长度 | 定位 |
|---|---:|---:|---:|---|
| DeepSeek-V4-Pro | 1.6T | 49B | 1M tokens | 高能力主模型 |
| DeepSeek-V4-Flash | 284B | 13B | 1M tokens | 高性价比模型 |

论文还定义了不同 reasoning effort 模式，例如 Pro-Max / Flash-Max，用更大的推理预算换取更强 reasoning、agent 和长上下文表现。

---

## 三、为什么 V4 重要

V3 / R1 已经证明了：

- MoE 可以把大容量和低激活计算结合起来。
- RL 可以显著增强 reasoning model。
- test-time compute 是提升难题表现的重要变量。

但这些路线都会遇到同一个瓶颈：**上下文和注意力成本**。长链推理、长程 Agent、跨文档分析、代码仓库任务、工具轨迹都会让上下文膨胀。普通 attention 的平方复杂度让百万 token 场景几乎不可持续。

DeepSeek-V4 的核心价值，就是把 long-context efficiency 变成模型架构的一等公民。

---

## 四、架构主线

DeepSeek-V4 继承 DeepSeek-V3 的若干设计：

- Transformer decoder-only 架构。
- DeepSeekMoE。
- Multi-Token Prediction。
- 辅助损失较少的 MoE 负载均衡思想。

同时引入三个关键升级：

1. **CSA + HCA 混合注意力**：降低长上下文 attention FLOPs 与 KV cache。
2. **mHC**：用 Manifold-Constrained Hyper-Connections 增强残差连接。
3. **Muon optimizer**：加速收敛并提高大规模训练稳定性。

---

## 五、CSA + HCA：压缩长上下文注意力

V4 的 attention 不再只依赖传统 dense attention，而是混合使用：

| 组件 | 作用 |
|---|---|
| CSA, Compressed Sparse Attention | 先压缩 KV，再做稀疏选择，保留更重要的远程上下文 |
| HCA, Heavily Compressed Attention | 更激进地压缩 KV，保留 dense attention 形式 |

直觉上：

```text
CSA: 压缩 + 稀疏检索，适合在百万上下文中找关键片段
HCA: 重压缩 + dense attention，适合进一步降低 KV cache 与计算
```

论文报告，在 1M context 场景下，DeepSeek-V4-Pro 相比 DeepSeek-V3.2 只需要约 27% 的 single-token inference FLOPs 和 10% 的 KV cache。相比常见 BF16 GQA8 配置，其 KV cache 在 1M context 下可降到约 2%。

这对 Agent 很关键：工具日志、代码文件、网页集合、历史轨迹都可以更长地留在上下文里，而不是频繁摘要或裁剪。

---

## 六、mHC：增强残差连接

mHC 是 Manifold-Constrained Hyper-Connections，用来增强传统 residual connections。

它的动机是：大模型层数深、MoE 路由复杂、长上下文训练不稳定时，普通残差连接可能不足以提供足够强的层间信息流和稳定性。mHC 通过动态生成混合参数，并对 residual mapping 加约束，把连接结构限制在更稳定的流形上。

从工程角度看，mHC 会增加激活内存和 pipeline 通信，所以论文专门设计了 fused kernel、选择性重计算和 DualPipe 适配，最终把额外 wall-time 开销控制在较低范围内。

---

## 七、Muon 优化器与训练稳定性

V4 对大部分模块使用 Muon 优化器，对 embedding、prediction head、RMSNorm 等保留 AdamW。

Muon 的作用：

- 更快收敛。
- 提升训练稳定性。
- 通过矩阵更新的正交化约束改善大规模训练行为。

论文还讨论了 trillion-parameter MoE 的训练不稳定问题，尤其是 MoE 层 outlier 和路由机制之间的恶性循环。为此引入了 **Anticipatory Routing**：用历史参数提前计算路由，缓解同步更新导致的路由震荡，并在检测到 loss spike 时触发。

这个细节很有价值，因为它说明 V4 的技术难点不仅是模型设计，更是大规模 MoE 训练控制。

---

## 八、预训练

DeepSeek-V4-Flash 与 DeepSeek-V4-Pro 都在超过 32T token 的高质量、多样化语料上预训练：

- Flash：32T tokens。
- Pro：33T tokens。
- 训练上下文从 4K 逐步扩展到 16K、64K、1M。
- 先用 dense attention warmup，再分阶段引入 sparse attention。
- MTP loss 在大部分训练阶段权重为 0.3，学习率衰减阶段降低到 0.1。

这说明百万 token 能力不是训练后简单插值出来的，而是从训练流程上逐步引入长上下文与压缩注意力。

---

## 九、后训练：专门化专家、RL 与 OPD

V4 的后训练流程不仅包括常规 SFT / RL，还强调多专家融合：

1. 先通过领域数据和 RL 得到多个专门化 teacher / expert。
2. 再通过 **On-Policy Distillation, OPD** 把多个专家能力整合到一个统一模型。
3. OPD 使用 full-vocabulary logit distillation，比只在采样 token 上近似 KL 更稳定。

为了让 OPD 在十多个 teacher 上可行，论文设计了：

- teacher 权重按需加载与 offload。
- 缓存最后一层 teacher hidden states，而不是直接物化完整 logits。
- 使用 TileLang kernel 计算 KL。
- preemptible / fault-tolerant rollout service。
- token-granular WAL，用于中断恢复，避免重新生成导致长度偏差。

这些内容对 Agent 训练很重要：长上下文 RL / OPD 的瓶颈往往不是算法公式，而是 rollout、缓存、恢复、数据派发和推理服务。

---

## 十、评测结果

论文给出的主结论：

- **知识**：DeepSeek-V4-Pro-Max 在 SimpleQA-Verified 和 Chinese-SimpleQA 上显著超过既有开源模型，但仍落后 Gemini-3.1-Pro 等领先闭源模型。
- **推理**：DeepSeek-V4-Pro-Max 在多个 reasoning benchmark 上超过此前开源模型，并在部分代码/数学任务上接近或匹配闭源 frontier model。
- **长上下文**：在 1M token 场景下，V4-Pro-Max 在 synthetic 与真实长上下文任务中表现强。
- **Agent**：公开 Agent benchmark 上接近强开源模型，但略弱于最强闭源模型；内部代码 Agent 评测中，V4-Pro 明显超过 Claude Sonnet 4.5，接近 Claude Opus 4.5。

一些具体指标：

| 指标 | DeepSeek-V4-Pro-Max |
|---|---:|
| SimpleQA-Verified Pass@1 | 57.9 |
| Chinese-SimpleQA Pass@1 | 84.4 |
| GPQA Diamond Pass@1 | 90.1 |
| HLE Pass@1 | 37.7 |
| LiveCodeBench Pass@1-COT | 93.5 |
| Codeforces Rating | 3206 |
| LongMRCR 1M MMR | 83.5 |
| CorpusQA 1M ACC | 62.0 |
| Terminal Bench 2.0 Acc | 67.9 |
| SWE Verified Resolved | 80.6 |
| BrowseComp Pass@1 | 83.4 |
| Toolathlon Pass@1 | 51.8 |

这些结果要按论文上下文理解：V4 的亮点是开放模型中的长上下文、reasoning 和 agentic capability 组合，而不是每个单项都压过闭源 frontier model。

---

## 十一、真实任务评测

论文还报告了更接近产品场景的内部评测：

- 中文功能写作：V4-Pro 相比 Gemini-3.1-Pro 有更高 win rate。
- 创意写作：在写作质量上优势明显。
- 搜索问答：相比 V3.2 在 RAG 与 agentic search 中都有提升。
- 办公任务：在分析、生成、编辑等任务上与 Opus 系列接近，但格式美观、复杂约束跟随仍有提升空间。
- 内部代码 Agent：在约 30 个高难内部 R&D 任务上，V4-Pro-Max pass rate 为 67%，接近 Opus 4.5 的 70%，低于 Opus 4.6 Thinking 的 80%。

这部分很适合和 Agent benchmark 一起读，因为它说明标准榜单和真实工作流之间仍有明显差距。

---

## 十二、关键洞察

### 1. 长上下文不是“大窗口”，而是系统工程

百万 token 上下文需要 attention 结构、KV cache、训练计划、推理框架、rollout 服务、数据加载和故障恢复一起工作。

### 2. V4 把 Agent 和 long-horizon task 放进模型主线

论文多次把复杂 Agent workflow、跨文档分析、代码 Agent、在线学习作为目标场景。这说明 frontier model 的能力边界正在从“单轮问答”转向“长程任务执行”。

### 3. Flash / Pro 是能力-成本分层

V4-Flash 参数和激活规模更小，知识任务弱于 Pro，但在更大 thinking budget 下部分 reasoning 能追近强模型。这种分层适合实际系统：常规请求用 Flash，复杂长程任务用 Pro / Pro-Max。

### 4. 后训练进入多专家融合阶段

R1 时代强调 RL 激发推理；V4 进一步强调多个领域专家通过 OPD 合并成统一模型。对未来模型训练来说，“单一后训练配方”可能不够，专家化与统一化会交替进行。

---

## 十三、局限

论文自己承认或可从结果中看到的局限：

- 仍是 preview version，不应视为最终 V4 完整能力形态。
- 知识类 benchmark 仍落后最强闭源模型。
- 公开 Agent benchmark 上还没有全面超过 closed frontier model。
- 长上下文高效不等于长任务可靠，真实长程 Agent 仍会遇到状态管理、工具错误、规划漂移。
- mHC、CSA/HCA、Muon、OPD 等系统复杂度高，外部复现难度大。
- 真实任务评测有不少内部指标，外部可验证性有限。
- 多模态仍在未来方向中，当前报告核心是文本模型。

---

## 十四、和 DeepSeek 系列的关系

| 论文 | 技术位置 |
|---|---|
| DeepSeek LLM | dense 开源基座、scaling law、SFT + DPO |
| DeepSeek-V2 | MLA + DeepSeekMoE，建立高效 MoE 路线 |
| DeepSeek-V3 | 大规模 MoE、FP8、DualPipe、MTP、低成本 frontier 训练 |
| DeepSeek-R1 | 在 V3-Base 上用 RL 激发长链推理 |
| DeepSeek-V4 | 面向百万 token、长程推理、Agent 和 test-time scaling 的高效长上下文架构 |

V4 可以看作把 V3 的高效 MoE 与 R1 的 test-time scaling 需求接起来：当推理预算和任务上下文都继续变长，模型必须先解决长上下文效率问题。

---

## 十五、适合怎么读

建议按这个顺序读：

1. 摘要和 Introduction：确认 V4 的主问题是百万 token 与 long-horizon intelligence。
2. Architecture：重点看 CSA / HCA、mHC、Muon。
3. Pre-Training：看 32T/33T tokens、4K 到 1M 的上下文扩展。
4. Post-Training：重点看 OPD、长上下文 RL、fault-tolerant rollout。
5. Evaluation：分开看知识、推理、长上下文、Agent，不要只看总榜。

如果你的主线是 Agent 研究，最值得读的是 5.2.4、5.2.5、5.4.4 和长上下文评测部分。

