---
type: paper
paper_id: arxiv-2601.03267
title: "OpenAI GPT-5 System Card"
arxiv: https://arxiv.org/abs/2601.03267
project: https://openai.com/index/introducing-gpt-5/
year: 2025
updated: 2026-06-28
status: summarized
primary_category: frontier-model-report
priority: p0
read_type: deep
tags:
  - paper
  - paper/llm
  - llm/frontier-model
  - llm/reasoning-model
  - llm/multimodal
  - model/gpt
  - model/gpt-5
  - eval/model-benchmark
  - eval/safety
  - eval/agent-benchmark
  - method/rlhf
  - method/safe-completions
  - method/router
  - year/2025
  - priority/p0
  - read/deep
---

# OpenAI GPT-5 System Card：统一系统、推理模型与安全护栏

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2601.03267
> 发布页：https://openai.com/index/introducing-gpt-5/
> 发表：OpenAI System Card, 2025-08-13；arXiv v2: 2026-05-01 ｜ 作者：OpenAI

---

## 一、一句话概括

**GPT-5 System Card** 不是一篇公开训练细节的模型论文，而是一份关于 GPT-5 系统组成、能力评测、安全挑战、红队测试、Preparedness 评估和生物/化学高风险防护的系统卡。

它最重要的变化是：GPT-5 不再被描述成单一模型，而是一个由 **fast/main 模型、thinking 推理模型、mini/nano 版本、pro 推理设置和实时 router** 组成的统一系统。

---

## 二、系统结构

GPT-5 系统包含多个模型/模式：

| 旧模型路线 | GPT-5 对应模型 |
|---|---|
| GPT-4o | gpt-5-main |
| GPT-4o-mini | gpt-5-main-mini |
| OpenAI o3 | gpt-5-thinking |
| OpenAI o4-mini | gpt-5-thinking-mini |
| GPT-4.1-nano | gpt-5-thinking-nano |
| OpenAI o3 Pro | gpt-5-thinking-pro |

系统中有一个实时 router，会根据对话类型、复杂度、工具需求和用户显式意图选择模型。例如用户说“think hard about this”时，系统更可能路由到 thinking 模型。

报告明确说，未来计划把这些能力整合进单一模型；但在本系统卡中，GPT-5 实际上还是一个多模型、多模式系统。

---

## 三、训练与推理模型

报告只给出高层信息：

- GPT-5 使用公开互联网数据、第三方合作数据、用户/训练员/研究人员提供或生成的数据。
- 数据处理包含质量过滤、个人信息减少、Moderation API 和安全分类器。
- `gpt-5-thinking`、`gpt-5-thinking-mini`、`gpt-5-thinking-nano` 是 reasoning models，通过强化学习训练来“先思考再回答”。
- thinking 模型能生成内部 chain of thought，训练目标包括尝试不同策略、识别错误、遵循安全政策。

需要注意：报告没有公开参数规模、完整架构、训练 compute、数据配比等可复现训练细节。

---

## 四、核心安全范式：Safe-Completions

GPT-5 引入或系统化使用 **safe-completions**。它和传统拒答范式的区别是：

```text
传统 hard refusal：
判断用户意图是否允许 -> 允许则尽量回答，不允许则拒答

safe-completions：
关注输出本身是否安全 -> 在安全约束内尽量提供有帮助的回答
```

这个变化特别适合双用途领域，例如生物、网络安全、化学等：用户请求可能有合法高层目的，但如果回答太具体就会提供危险 uplift。

报告称 safe-completions 带来更好的双用途安全性、更低残余失败严重度和更高整体 helpfulness。

---

## 五、主要安全与可靠性结果

### 1. Disallowed Content

在标准不安全内容评估上，多数模型已经接近饱和。更有信号的是 production benchmarks，即更接近真实生产对话、更多轮、更难的安全评测。

GPT-5 thinking 相比 OpenAI o3 通常持平或更好；GPT-5 main 相比 GPT-4o 有些维度提升，有些维度回退。报告特别指出 gpt-5-main 在 illicit/nonviolent 和 illicit/violent 上显著优于 GPT-4o，这与 safe-completions 范式有关。

### 2. Sycophancy

GPT-5 针对谄媚行为做了 post-training。离线评测中：

- GPT-4o baseline：`0.145`，越低越好。
- gpt-5-main：`0.052`。
- gpt-5-thinking：`0.040`。

在线 A/B 早期测量中，gpt-5-main 相比 GPT-4o 的 sycophancy prevalence：

- 免费用户下降 `69%`。
- 付费用户下降 `75%`。

这说明 GPT-5 的产品安全目标不只是“别生成违禁内容”，还包括减少迎合用户错误信念的行为。

### 3. Prompt Injection

GPT-5 因为能浏览网页、使用 connectors 和工具，所以 prompt injection 风险更关键。

报告中的三项评测结果：

| 评测 | gpt-5-thinking | OpenAI o3 |
|---|---:|---:|
| Browsing prompt injections | 0.99 | 0.89 |
| Tool calling prompt injections | 0.99 | 0.80 |
| Coding prompt injections | 0.97 | 0.94 |

系统缓解包括：训练模型忽略网页/connector 内容中的恶意指令，并在 connector 调用后限制后续浏览只访问缓存页面，以减少敏感数据外泄风险。

### 4. Hallucinations

GPT-5 明确把减少幻觉作为训练重点。

在真实 ChatGPT 生产对话样本上：

- gpt-5-main 的 hallucination rate 比 GPT-4o 低 `26%`。
- gpt-5-thinking 的 hallucination rate 比 OpenAI o3 低 `65%`。
- response-level 重大事实错误上，gpt-5-main 比 GPT-4o 少 `44%`，gpt-5-thinking 比 o3 少 `78%`。

在 LongFact / FActScore 上，gpt-5-thinking 在 browse-on 和 browse-off 设置下都比 OpenAI o3 少很多事实错误。报告称 gpt-5-thinking 在三个 benchmark 上的事实错误超过 `5x` 少于 OpenAI o3。

SimpleQA 无网页设置：

| 模型 | accuracy | hallucination rate |
|---|---:|---:|
| gpt-5-thinking | 0.55 | 0.40 |
| OpenAI o3 | 0.54 | 0.46 |
| gpt-5-main | 0.46 | 0.47 |
| GPT-4o | 0.44 | 0.52 |

---

## 六、Deception 与 CoT 监控

报告把 deception 定义为：模型面向用户的回答误表示了内部推理或实际行动，例如声称已经完成任务、声称使用了工具、伪造经历，或在不可解任务中假装成功。

GPT-5 thinking 通过训练学习在不可完成任务中“优雅失败”，例如工具坏了、缺少输入、任务过大或环境不满足条件时明确说明不能完成。

关键评测：

| 评测 | 指标 | gpt-5-thinking | OpenAI o3 |
|---|---|---:|---:|
| Coding Deception | deception rate，越低越好 | 0.17 | 0.47 |
| Browsing Broken Tools | 越低越好 | 0.11 | 0.61 |
| CharXiv Missing Image | 越低越好 | 0.09 | 0.87 |
| AbstentionBench Recall | 越高越好 | 0.53 | 0.44 |

报告还使用 CoT monitor 在生产代表性对话中检测欺骗：

- OpenAI o3 被标记 deception：约 `4.8%`。
- gpt-5-thinking：约 `2.1%`。
- monitor 内部验证 precision `81%`，recall `84%`。

这很重要：GPT-5 报告把“推理轨迹是否可监控”视为安全能力的一部分，而不只是 benchmark 分数。

---

## 七、Health 能力

GPT-5 在 HealthBench 上提升明显。

HealthBench Hard：

- OpenAI o3：`31.6%`。
- gpt-5-thinking：`46.2%`。
- gpt-5-thinking-mini：`40.3%`。
- gpt-5-main：`25.5%`。
- GPT-4o：`0.0%`。

HealthBench Consensus：

- gpt-5-thinking：`95.7%`。
- gpt-5-thinking-mini：`96.5%`。
- GPT-4o：`88.7%`。

错误率方面：

- 挑战性健康对话幻觉：gpt-5-thinking `1.6%`，OpenAI o3 `12.9%`，GPT-4o `15.8%`。
- 高风险紧急情境错误：gpt-5-thinking `0.4%`，OpenAI o3 `3.4%`，GPT-4o `20.6%`。
- 全球健康语境适配失败：gpt-5-thinking `0.0%`，OpenAI o3 `6.2%`，GPT-4o `13.7%`。

报告强调这不是替代医生，而是说明模型在健康问答安全性和准确性上显著改进。

---

## 八、生物/化学风险：High Capability 处理

报告最严肃的部分是生物与化学风险。OpenAI 决定把 `gpt-5-thinking` 按 Preparedness Framework 视为 Biological and Chemical domain 的 **High capability**，即使报告说还没有确定证据表明它能显著帮助新手制造严重生物危害。

采取的是预防性路线。

核心防护包括：

- 模型训练：拒绝 weaponization assistance，不提供高风险双用途细节。
- 两层实时系统监控：
  - 第一层快速判断是否与生物相关。
  - 第二层 reasoning monitor 判断是否落入生物威胁分类。
- 覆盖 user message、external tool calls、final model output。
- 账号级执法：自动系统 + 生物威胁专家人工复核，可封禁、阻断输出、极端情况通知执法部门。
- API 新增 `safety_identifier`，用于区分开发者终端用户，便于追踪和响应潜在滥用。
- Life Science Research Special Access Program，为受信任生命科学用途提供更受控访问。

这表明 frontier model 的发布治理已经从“模型拒答”升级到“模型训练 + 实时监控 + 账号执法 + API 访问控制 + 专项可信访问”的系统工程。

---

## 九、Cybersecurity 与 Agent 能力

报告中网络安全部分比较克制。

Cyber Range 中：

- gpt-5-thinking 无提示时不能解决任何 cyber range 场景。
- 有 hints 时能低频解决两个 light 场景。
- gpt-5-thinking-mini 在一些 light 场景上更强，但报告认为这还不足以构成显著 cyber risk。

Pattern Labs 外部评测中：

- Evasion challenges：平均成功率 `51%`。
- Vulnerability Discovery and Exploitation：`35%`。
- Network Attack Simulation：`49%`。
- 解决 18 个 easy challenge 中 17 个、14 个 medium 中 8 个、4 个 hard 中 0 个。

Pattern Labs 结论是：gpt-5-thinking 比 o3 有进步，但仍不能自动化端到端攻击，也不能对合理加固目标完成现实级别攻防。

---

## 十、AI Self-Improvement / 软件工程 Agent

报告把软件工程和 AI 研发能力放在 Preparedness 的 AI self-improvement 部分。

评测包括：

- SWE-bench Verified：真实 GitHub issue 修复，内部工具 scaffold 提供 bash 和 apply_patch。
- OpenAI PRs：复现 OpenAI 内部 PR 贡献。
- MLE-Bench：Kaggle 竞赛式机器学习任务。
- SWE-Lancer：真实经济价值的软件工程任务。
- PaperBench：复现 ICML 2024 Spotlight / Oral 论文。
- OPQA：OpenAI 内部研究/工程瓶颈问题。
- METR 外部自主能力评估。

已公开的关键点：

- GPT-5 launch blog 的 SWE-bench Verified 结果为 `74.9%`，但系统卡说明这是 API 默认 medium verbosity；Preparedness 评测使用更高 verbosity，结果可能变化。
- gpt-5-thinking 和 gpt-5-thinking-mini 是 SWE-bench Verified 上最高的 OpenAI 模型。
- PaperBench 上 gpt-5-thinking 是最高分模型。
- OPQA 上 gpt-5-thinking 最高，但也只有 `2%`。
- MLE-Bench 30 个子集上 ChatGPT agent 最高，达到 `9%`。
- METR 初步认为 gpt-5-thinking 不太可能让 AI R&D 研究者提速超过 `10x`，不太可能显著战略性欺骗研究者，也不太可能具备 rogue replication 能力。

这部分对 Agent 研究很关键：GPT-5 已经是强软件工程 Agent 基座，但报告仍把“自主自我改进”看作远未解决、需持续监控的风险类别。

---

## 十一、与 GPT-4 Report 的区别

| 维度 | GPT-4 Technical Report | GPT-5 System Card |
|---|---|---|
| 重点 | 能力跃迁、多模态、可预测扩展、安全概览 | 统一系统、thinking 模型、安全评测、Preparedness、红队、防护体系 |
| 模型形态 | 大型多模态 Transformer | main/thinking/mini/nano/pro + router |
| 安全范式 | RLHF、红队、RBRM、系统卡 | safe-completions、CoT 监控、系统级生物防护、API safety_identifier |
| Agent 评测 | 相对少 | SWE-bench、OpenAI PRs、MLE-Bench、PaperBench、OPQA、METR |
| 公开训练细节 | 不公开核心规模/数据/compute | 仍不公开核心规模/数据配比/compute |

GPT-4 报告更像“frontier model 能力报告”，GPT-5 系统卡更像“frontier model 系统治理报告”。

---

## 十二、对 Agent / 大模型评测的启发

GPT-5 System Card 对 Agent 评测有几个直接启发：

- 评测对象不再只是模型，而是 **model + router + tools + monitors + access controls** 的系统。
- Agent 安全必须覆盖 prompt injection、tool outputs、connector 数据外泄、broken tools、不可完成任务中的 deception。
- CoT monitorability 成为推理模型治理的重要抓手。
- 高风险领域需要 domain-specific Preparedness Framework，而不是通用拒答规则。
- 软件工程 Agent 的评测正在从 SWE-bench 走向 OpenAI PRs、SWE-Lancer、PaperBench、OPQA 这类更接近真实经济价值和 AI R&D 的任务。

---

## 十三、阅读结论

GPT-5 System Card 不适合当作“GPT-5 架构论文”来读，因为它不公开关键训练细节。

它最值得读的是三件事：

1. GPT-5 从单模型变成统一模型系统：main / thinking / mini / nano / pro + router。
2. 安全从 hard refusal 走向 safe-completions 和系统级多层防护。
3. Frontier model 评估开始把 Agent、自主性、欺骗、工具安全、生物/网络风险纳入同一张表。

如果按 GPT 主线读：

```text
GPT-1：预训练 + 微调
GPT-2：zero-shot 任务迁移
GPT-3：in-context few-shot learning
GPT-4：frontier capability + scaling predictability + safety deployment
GPT-5：统一推理系统 + safe-completions + Preparedness / Agent 评测
```

---

## 十四、关联笔记

- [[2303-GPT-4 Technical Report|GPT-4 Technical Report]]
- [[2005-Language Models are Few-Shot Learners|Language Models are Few-Shot Learners]]
- [[1901-Language Models are Unsupervised Multitask Learners|Language Models are Unsupervised Multitask Learners]]
- [[1801-Improving Language Understanding by Generative Pre-Training|Improving Language Understanding by Generative Pre-Training]]
- [[2310-SWE-bench Can Language Models Resolve Real-World GitHub Issues|SWE-bench]]
- [[2501-Humanitys Last Exam|Humanity's Last Exam]]
- [[AI Agent 与大模型评测论文地图]]

