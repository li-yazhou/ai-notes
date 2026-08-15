---
type: digest
month: 2026-07
title: "arXiv 2026.07 AI Agent / LLM 月度论文摘要"
updated: 2026-08-12
status: active
count: 219
tags:
  - digest/agent
  - digest/arxiv
  - month/2026-07
  - paper/agent
  - paper/eval
---

# arXiv 2026.07 AI Agent / LLM 月度摘要

> 采集窗口：arXiv `submittedDate` 2026-07-01 ~ 2026-07-31（少量 2608.xxxxx 为 7 月底提交、8 月初公告）
> 采集方式：arXiv API 按日期 + 关键词（agent / tool / memory / benchmark / coding / self-evolv 等）召回，去重后人工筛选
> 收录论文：219 篇唯一论文（+ 12 篇在"本月必读"复引），分 9 个维度
> 一句话要点均依据论文摘要撰写，未读全文的结论请以原文为准

---

## 〇、本月趋势

1. **Harness Engineering（harness 工程）成为显学。** 本月最密集的主题不再是"更强的模型"，而是围绕模型的 *编排层*——提示、工具、上下文、验证、循环——做工程化。`Don't Blame the LLM`、`TTHE`、`Living-Harness`、`Harness Handbook`、`Agentic Routing`、`ToFu`、`SHarD`、`Harness Engineering for GPU Kernels` 都把 harness 当成一等公民来设计、演化、可读化甚至自我重写。
2. **记忆从"存储检索"走向"工程化、事务化、参数化"。** 记忆被当成数据库/操作系统来治理：事务提交与回滚（`MemTxn` / `MemTX`）、版本控制（`ChronoMem`）、写时防污染（`ConsistencyGate`、`AM-Sentry`、`PPMF`）、参数化记忆底座（`Metis` memory foundation model、`TransMem`、`UniMem`）。`Ground Truth First` 还发现记忆架构排名会随历史长度"反转"。
3. **自进化 / 递归自我改进（RSI）正式进入主流议程。** `AREX`（递归自改进 deep research）、`RSIBench-Data`（RSI 基准）、`Skill Self-Play`（技能共进化）、`SEED`（自进化 on-policy 蒸馏）、`Living-Harness`、`Cura 1T`（human-gated RSI）把"agent 能否持续改进自己"变成可评测、可训练的对象。
4. **Coding Agent 经验研究井喷，且大量基于真实数据集。** `AIDev` / `AIDev-pop` 数据集催生了一批纵向研究：agentic PR、合并后命运、安全债、测试质量、上下文腐烂、context file 是否有用、企业落地（微软 Claude Code/Copilot CLI 滚动）。同时 SWE-bench 衍生基准持续细分（`DeepSWE`、`LoopsBench`、`SWE-Doctor`、`RuBench`、`SWE-NFI`）。
5. **安全重心从 prompt injection 扩展到 *供应链、MCP、skill 文件、组合状态攻击*。** `SkillGate`（恶意 skill 文件）、`IssueTrojanBench`（恶意 issue）、`MOSAIC`（CLI 命令组合）、分布式后门、`ADI`（agent 数据注入）、记忆投毒（`GhostWriter`）说明：单步检查已不够，危害正在 *组合化、跨会话化*。
6. **MCP（Model Context Protocol）成为工具基础设施。** 多篇基准与防御围绕 MCP：`MCPEvol-Bench`、`DynamicMCPBench`、`AgentCheck`、`ChainWatch`、`MTGuard`、`Unicode TAG-Block Concealment`。
7. **长程可靠性的瓶颈是上下文，不是模型。** `PRO-LONG`（ARC-AGI-3 +18pp）、`context rot` 研究、`SLEUTH`（epistemic working memory）、`AI Agents Do Not Fail Alone: The Context Fails First` 一致指向：长上下文下 *状态组织* 是决定性变量。
8. **模型发布：开源 frontier 持续逼近闭源。** `Kimi K3`（2.8T MoE / 104B 激活，1M 上下文，权重全开）是本月最重要的开源发布；另有 `Nanbeige4.2-3B`（紧凑 agentic）、`Cura 1T`（医疗 RSI）、`KAT-Coder-V2.5`（agentic coding）、`DeepResearch Agent System`（30B/3B 激活稀疏检索系统）。

---

## 一、自进化与递归自我改进（Self-Evolution / RSI）

> Agent 如何从自身经验中持续积累技能、规则、记忆并改进自己（含 frozen-weights 场景下的"无权重更新进化"）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [CrystalMem](https://arxiv.org/abs/2608.00303) | 07-31 | 提出"记忆磁滞"现象：预算压缩后再恢复，能力不会回弹；用四态结晶化侧边栏做弹性记忆 | `agent/memory` `method/crystallization` |
| [AgentStream](https://arxiv.org/abs/2608.00155) | 07-31 | 用 Isolated/Sequential/Interleaved 任务流评测自进化 agent，发现进化收益受模型能力门控、非单调 | `eval/self-evolve` |
| [MANTA](https://arxiv.org/abs/2607.28527) | 07-30 | 让多智能体 *通信拓扑* 在推理时自我演化（改角色/链路/顺序），5 基准均分 74.0 | `agent/multi-agent` `method/topology-adapt` |
| [SciToolAgent-Evo](https://arxiv.org/abs/2607.28692) | 07-30 | 本体感知的自进化科研工具 agent，LinUCB 门控探索/利用，随附 OpenSciToolBench（900 任务） | `agent/tool-use` `env/science` |
| [Code Is the Body](https://arxiv.org/abs/2607.28691) | 07-30 | 提出"agent 自有的软件躯体"概念，支持递归进化与"继承/谱系" | `agent/self-evolve` |
| [Living-Harness](https://arxiv.org/abs/2607.26598) | 07-29 | 把每条轨迹+评估信号转成 harness 后验证据，写 episodic memory + 状态图；τ²-Bench / MultiWOZ 上 +10pp | `agent/harness` `method/evolution-sop` |
| [RSIBench-Data](https://arxiv.org/abs/2607.25886) | 07-28 | 固定后训练栈下评测 agent 做"数据中心 RSI 研究"的能力：58% 设定能改进，但 78% 后续修订反而劣化 | `eval/rsi` |
| [Skill Self-Play](https://arxiv.org/abs/2607.22529) | 07-24 | Qwen 团队；proposer/solver/skill-controller 三方共进化，平衡"可验证执行"与"开放式探索" | `method/self-play` `method/skill` |
| [Learning on the Job](https://arxiv.org/abs/2607.22157) | 07-24 | frozen 模型 + 外部规则记忆，仅靠 1-bit 结果信号即可在 τ-bank 把成功率提到 2.6× | `method/continual-learning` |
| [AREX](https://arxiv.org/abs/2607.21461) | 07-23 | 递归自改进 deep research agent：内层取证+外层约束级审计；BrowseComp/HLE 上显著超同量级基线 | `agent/self-evolve` `agent/deep-research` |
| [AgentBrew](https://arxiv.org/abs/2607.16851) | 07-18 | 把强 teacher 的交互经验"酿"成学生可执行的外部记忆，免权重更新/免 teacher 在线 | `method/distillation` `agent/memory` |
| [SEED](https://arxiv.org/abs/2607.14777) | 07-16 | 把 on-policy 轨迹转成 hindsight 技能再蒸馏回策略，给 agentic RL 提供稠密 token 级信号 | `method/on-policy-distill` |
| [Causal-AgentIR](https://arxiv.org/abs/2607.21125) | 07-23 | 图像修复 agent 的自进化因果记忆图，支持增加/更新/合并/遗忘 | `agent/memory` `env/vision` |
| [SPyCE](https://arxiv.org/abs/2607.13854) | 07-15 | 多模态 agent 的 skill-policy 共进化：执行技能 + 工作流技能分层库，RL 中闭环更新 | `method/skill` `agent/multimodal` |
| [ABot-AgentOS](https://arxiv.org/abs/2607.10350) | 07-11 | 通用机器人 Agent OS + 终身多模态图记忆；失败驱动自进化，仅晋升到后续 split 防泄漏 | `agent/embodied` `agent/memory` |
| [Self-Improving AI Coding Agents](https://arxiv.org/abs/2607.13091) | 07-13 | 把每条 review 意见固化为持久行为规则，35+ 微服务落地，被规则错误类复发率 0% | `agent/coding` `method/rules` |
| [WebDesignIter](https://arxiv.org/abs/2607.10621) | 07-12 | 前端仓库级共进化设计知识图（WebAppArchKG），Web-Bench 上 Pass@2 +9.55pp | `agent/coding` `method/knowledge-graph` |
| [VITAL-RAG](https://arxiv.org/abs/2607.26937) | 07-29 | coding agent 上下文分配的"不变性竞赛"：按代码对象归组，Recall@4K 39.6%→63.7% | `agent/coding` `method/rag` |
| [From Atomic Actions to SOPs](https://arxiv.org/abs/2607.07321) | 07-08 | EvoSOP：把原子动作合成可复用 SOP 作为高阶工具，迭代构建/合并/评估/剪枝 | `method/sop` `agent/tool-use` |
| [DeepSearch-World](https://arxiv.org/abs/2607.07820) | 07-08 | 可验证检索环境上的自蒸馏框架，420K 多跳 QA；9B 模型 BrowseComp 31.2% | `agent/deep-research` `method/self-distill` |
| [SelfMem](https://arxiv.org/abs/2607.03726) | 07-04 | "授人以渔"：让 agent 自行探索/评估/改进记忆策略，BEAM 官方分 +48.7%~+41.9% | `agent/memory` `method/self-optimize` |
| [SkillOpt-Lite](https://arxiv.org/abs/2607.03451) | 07-03 | 用零阶优化形式化技能优化，给出最小可行管线；GPT-5.4-nano 超 GPT-5.5 标准管线 | `method/skill` `agent/harness` |
| [OpenForgeRL](https://arxiv.org/abs/2607.21557) | 07-23 | 开源框架：用 proxy + K8s 让任意 harness（Claude Code/Codex/OpenClaw）端到端做 RL | `method/rl` `agent/harness` |

---

## 二、记忆（Memory）

> 持久记忆的组织、写入治理、版本化、压缩与参数化；含记忆安全（投毒/溯源）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Zero-Mem](https://arxiv.org/abs/2607.29377) | 07-31 | 零 token 记忆操作：除最终问答外不调用 LLM，用实体-上下文图 + 时间层级，时延降 57.6% | `method/zero-token` |
| [Shared Organizational Memory](https://arxiv.org/abs/2608.00122) | 07-31 | 企业 coding agent 的共享组织记忆系统：平台级捕获 + 策划 Q&A 记忆 + 检索复用 | `agent/coding` `agent/memory` |
| [TransMem](https://arxiv.org/abs/2607.29032) | 07-31 | 把冻结 backbone 的稀疏历史 hidden state 变成可复用记忆；LoCoMo +11.6~29.3 F1 | `method/parametric-memory` |
| [Know It, Act on It](https://arxiv.org/abs/2607.29433) | 07-31 | 解耦 Know/Act 评测：agent 常能"记住"偏好却不"照做"，健康/治疗类尤甚 | `eval/memory` |
| [MemHarness](https://arxiv.org/abs/2607.28272) | 07-30 | "记忆是重构不是回放"：按当前状态重构检索经验，GRPO 训练，抗负迁移 | `method/reconstruction` |
| [MemTxn](https://arxiv.org/abs/2607.27834) | 07-30 | 记忆事务边界：Ordered PatchTest 验写、Temporal Resolver 选版本、快照恢复 | `method/transaction` |
| [ChronoMem](https://arxiv.org/abs/2607.27773) | 07-30 | 接入 Google ADK 的语义版本控制层：整记忆快照 + 自然语言回滚 + 反事实评测 | `method/version-control` |
| [Metis](https://arxiv.org/abs/2607.26760) | 07-29 | 首个"记忆基础模型"：把持久演化记忆态与原生记忆过程内化进 backbone，前向即更新 | `method/memory-foundation` |
| [Filesystem-Based Memory](https://arxiv.org/abs/2607.26637) | 07-29 | 系统研究"文件系统即记忆"：组织能把检索成本减半，但当前 agent 难把组织转化为更好答案 | `eval/memory` |
| [Bitemporal Memory Store](https://arxiv.org/abs/2607.26520) | 07-29 | Neo4j + HNSW + 双时态（valid/transaction time）的 agent 本地图记忆 | `method/graph-memory` |
| [UniMem](https://arxiv.org/abs/2607.26017) | 07-28 | episodic↔parametric 互补记忆 + 可学习路由 token，缓解稳定-可塑困境 | `method/routing` |
| [MemChain](https://arxiv.org/abs/2607.24097) | 07-27 | 可训练的检索后记忆策略：把候选转成紧凑、有据可查的"证据链"再回答 | `method/post-retrieval` |
| [MemTX](https://arxiv.org/abs/2607.23929) | 07-27 | 事务化信念提交协议：快照隔离 + 验证-提交 + 级联修复，5.5M 状态机检验零违反 | `method/transaction` |
| [ConsistencyGate](https://arxiv.org/abs/2607.22962) | 07-25 | 写时准入门控：K 次自一致性平均分过阈才提交事实，防"记忆污染" | `method/admission-control` |
| [Agentic Context Management](https://arxiv.org/abs/2607.21503) | 07-23 | 把记忆/成本当作 *生命周期与架构* 问题；五原语 + Maximem 实现，LongMemEval 92% | `method/acm` |
| [AttriMem](https://arxiv.org/abs/2607.21106) | 07-23 | 用 token 级归因给记忆构建策略提供过程反馈，缓解细粒度信用分配瓶颈 | `method/attribution` |
| [PRO-LONG](https://arxiv.org/abs/2607.20064) | 07-22 | 程序化记忆：完整结构化交互日志 + coding agent 式检索；ARC-AGI-3 +18pp、省 4.2-5.8× token | `method/programmatic-memory` |
| [SLEUTH (Track, Rank, Crack)](https://arxiv.org/abs/2607.12267) | 07-14 | 结构化认知工作记忆（已证事实/活跃假设/开放问题），多跳越难优势越大（4 跳 +11） | `method/epistemic-memory` |
| [ToolAtlas](https://arxiv.org/abs/2607.11126) | 07-13 | 工具侧记忆：由 *工具提供方* 维护可复用工具能力图，跨 agent/环境迁移 | `agent/tool-use` `method/provider-memory` |
| [Shared Selective Persistent Memory](https://arxiv.org/abs/2607.09493) | 07-10 | 选择性持久记忆（4 类可复用上下文）+ 共享 + 零 token 数据刷新，完成率 79%→96% | `method/selective-memory` |
| [From Passive Retrieval to Active Memory Navigation](https://arxiv.org/abs/2607.05794) | 07-07 | NapMem：把记忆当结构化动作空间来学习（多粒度金字塔 + 记忆工具 RL） | `method/action-space` |
| [Σ-Mem](https://arxiv.org/abs/2607.27958) | 07-30 | 多智能体在线"可靠性记忆"：记录同伴能力/关系证据，Weyl 不等式保证稳定更新 | `agent/multi-agent` |
| [Ground Truth First](https://arxiv.org/abs/2607.21962) | 07-24 | 倒置记忆基准管线（先事实后对话）；发现记忆架构排名随历史长度 *反转* | `eval/memory` |
| [When Agents Remember Too Much](https://arxiv.org/abs/2607.06595) | 07-06 | GhostWriter 记忆投毒攻击：注入率 ~98%、激活率 ~60%；提 AM-Sentry 防御 | `agent/safety` `attack/memory-poison` |
| [Memory Provenance Laundering](https://arxiv.org/abs/2607.29167) | 07-31 | 记忆溯源洗白：LLM 巩固时把低信源抹成"用户历史"；提 PPMF 非放大防火墙 | `agent/safety` |

---

## 三、工具使用与 Function Calling（Tool Use）

> 工具发现/选择/调用、MCP、可靠性、可验证执行、RL 训练。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [HyperAgent](https://arxiv.org/abs/2608.02650) | 07-31 | 用工具-模式有向超图建模工具关系，动态规划+执行，AppWorld 上减冗余调用 | `method/hypergraph` |
| [A Few Neurons Reveal...](https://arxiv.org/abs/2608.00218) | 07-31 | 1-16 个 MLP 神经元即可检测工具误用（过调/漏调/无效参），并双向干预 | `method/steering` |
| [Verified Tool Calls](https://arxiv.org/abs/2608.02645) | 07-31 | 轻量验证包装器：后置条件验证 + 重试前校验 + 幂等键，抗"非原子失败" | `method/reliability` |
| [Data Turnstile](https://arxiv.org/abs/2607.29250) | 07-31 | 开源 function-calling 合成数据框架；0.6B 微调后逼近 4B，τ²-bench 超 32B | `method/data-gen` |
| [CAGE](https://arxiv.org/abs/2607.29190) | 07-31 | 证明分类/数值通道分别认证 *不* 复合；对 typed-return 不确定性做认证授权 | `method/certified-authz` |
| [SpatialCLI](https://arxiv.org/abs/2607.27703) | 07-30 | 先用空间工具推理再"内化"为自身能力；MindCube 把 Qwen3-VL-8B 29.3%→84.6% | `method/internalize` |
| [Scores Are Not Decisions](https://arxiv.org/abs/2607.27083) | 07-29 | 异质成本下的成本感知停步（CAM-DF）：把工具排名转成"选几个"的决策 | `method/cost-aware` |
| [Speculate While You Reason](https://arxiv.org/abs/2607.25816) | 07-28 | 自推测 agent：同模型兼 agent/speculator，预执行下一工具调用隐藏时延，Hit@1 44→61 | `method/speculation` |
| [Tools Are Not Islands](https://arxiv.org/abs/2607.25718) | 07-28 | HYSET：工具检索建模为查询条件超边预测，把"工具集"整体打分 | `method/set-retrieval` |
| [Explanation-Bound Tool Execution](https://arxiv.org/abs/2607.25364) | 07-28 | 把自由理由转成 typed action claim，服务端核对意图/策略/载荷/溯源/新鲜度 | `method/verified-exec` |
| [Lomekwi](https://arxiv.org/abs/2607.16961) | 07-18 | 区分"工具使用"与"工具发现"（好奇/识别/效率），发现识别能力随模型规模 *反向* 缩放 | `eval/tool-discovery` |
| [ToolVerse](https://arxiv.org/abs/2607.15660) | 07-17 | 用 ~400 真实 MCP/~4500 工具构建大规模 agentic RL 环境 + Turn-Aware 相对优势算法 | `method/rl` `env/mcp` |
| [Multi-Head Latent Control](https://arxiv.org/abs/2607.14277) | 07-15 | 读 hidden state 轨迹输出"是否该升级/澄清/调用工具/弃答"，大模型用量降 90.7% | `method/latent-control` |
| [TRACE](https://arxiv.org/abs/2607.13988) | 07-15 | 长程 agent 的 turn 级信用分配：log-ratio TD 逐动作奖励；BrowseComp-Plus 7.2→35.6 | `method/credit-assignment` |
| [Reason Less, Verify More](https://arxiv.org/abs/2607.07405) | 07-08 | 确定性只读前置门恢复"静默违规写"失败模式；τ²-bench 29.6%→42.0% | `method/deterministic-gate` |
| ["I Don't Know" Filter](https://arxiv.org/abs/2607.04034) | 07-04 | 轻量可训练过滤器量化函数调用不确定性，删除潜在有害调用 | `method/abstention` |
| [Natural Language Tools（复现）](https://arxiv.org/abs/2607.03953) | 07-04 | 跨 14 模型复现 NLT：准确率 +14.9pp、关键错误 −93%、token −25%；收益随模型能力而变 | `eval/tool-use` |
| [Can Agents Generalize to the Open World?](https://arxiv.org/abs/2607.01084) | 07-01 | 形式化 OpenAgent 开放世界设定，四层环境漂移诊断 SFT/RL 的泛化脆弱性 | `eval/generalization` |
| [AgentLTL](https://arxiv.org/abs/2607.02599) | 07-01 | 一阶线性时序逻辑描述过程合规，同一规约驱动 harness 评分/在线门控/微调 | `method/compliance` |
| [Attributing Structured-Output Gains](https://arxiv.org/abs/2607.02595) | 07-01 | 拆解 function-calling 增益来源：很多"技能"增益实为接口对齐而非过程迁移 | `eval/function-calling` |
| [Beyond Document Grounding](https://arxiv.org/abs/2607.00895) | 07-01 | 统一 code/tool output/文档的 span 级幻觉检测基准 + Qwen3.5-2B 检测器 | `eval/hallucination` |
| [MCPEvol-Bench](https://arxiv.org/abs/2607.14642) | 07-16 | 11 种变异算子模拟 MCP 工具演化；GPT-5.4/Claude-Sonnet-4.6 在演化工具上掉 13.7%/14.4% | `eval/mcp` `env/mcp` |
| [DynamicMCPBench](https://arxiv.org/abs/2607.20531) | 07-10 | 可在自有 MCP 上重跑的框架：按"效果检查点"而非最终答案打分，pass^3 严格 | `eval/mcp` `env/mcp` |
| [ToolFailBench](https://arxiv.org/abs/2607.04686) | 07-06 | 1000 任务诊断工具使用失败（跳过/忽略/捏造/滥用）；相似总分模型失败模式迥异 | `eval/tool-use` |
| [AllocBench](https://arxiv.org/abs/2607.23332) | 07-25 | 测"在线工具分配"意识：前沿模型在抽象任务近最优，迁移到写脚本即崩 | `eval/tool-use` |
| [AgentCheck](https://arxiv.org/abs/2607.11098) | 07-13 | MCP 工作台：录制工具响应→注入 12 类故障→重放验证"复现-干预-确认"闭环 | `eval/mcp` `env/mcp` |
| [Tool Specifications Matter](https://arxiv.org/abs/2607.29254) | 07-31 | schema 工具规格会 *削弱* 模型内部拒答信号；SafeKeep 用扁平文本判安全，ASR 25.6%→2.5% | `agent/safety` |

---

## 四、评测（Evaluation & Benchmark）

> 新基准 + 评测方法论（统计严谨性、IRT、轨迹诊断、成本感知）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [LoopsBench](https://arxiv.org/abs/2608.00267) | 07-31 | 从 harness 工程到 *loop 工程*：112 个长程依赖 DAG 任务，最强配置仅解 25% | `eval/coding` |
| [ExtractBench](https://arxiv.org/abs/2607.29677) | 07-31 | schema 引导企业文档抽取基准（4869 页/370 文档），同时评价值/完整性/溯源/成本 | `eval/document` |
| [MerchantBench](https://arxiv.org/abs/2607.28956) | 07-31 | 365 天电商运营仿真，测"长期一致性"；最佳 LLM 仅达人类均值净资产 27.3% | `eval/long-horizon` `env/business` |
| [ORCA-bench](https://arxiv.org/abs/2607.28545) | 07-30 | 生产级 oncall 根因分析基准（OTel 微服务+1079 任务）；最强 RCA 仅 25.3% | `eval/sre` `env/ops` |
| [SWE-NFI](https://arxiv.org/abs/2607.27409) | 07-29 | 评测 coding agent 的 *行为保持非功能改进*；结构改进上远落后人类 | `eval/coding` |
| [OmegaUse-OfficeVal](https://arxiv.org/abs/2607.27155) | 07-29 | 办公套件长程任务基准，每任务配"人工工时+价格"经济信号做价值加权 | `eval/office` |
| [TREK](https://arxiv.org/abs/2607.26977) | 07-29 | 旅行规划基准：完全确定性规则评分（无 LLM judge），最强 GPT-5.6 仅 46.2% 可行 | `eval/planning` |
| [Messier](https://arxiv.org/abs/2607.25891) | 07-28 | 统一 95.7 万条记录跨 30 基准/714 agent；function calling 已饱和、企业工作流最难 | `eval/meta` |
| [WorkSurface-Bench](https://arxiv.org/abs/2607.25765) | 07-28 | 评测"知识面路由"：路由 F1 高但答案仍只 56-75%，路由正确 ≠ 任务完成 | `eval/enterprise` |
| [HANDBOOK.md](https://arxiv.org/abs/2607.25398) | 07-28 | 长上下文 agentic *指令手册遵循* 基准；最强模型严格通过率仅 36.2% | `eval/instruction-follow` |
| [E-Bench](https://arxiv.org/abs/2607.23722) | 07-26 | 真实产品场景（王者荣耀/QQ 音乐/腾讯会议）323 个状态变更多步任务，Pass^3<60% | `eval/multi-step` |
| [SQBench](https://arxiv.org/abs/2607.23123) | 07-25 | 把"受限工作流内交付的可验证产物"作为评测单位；含 10D 风险矩阵 | `eval/production` |
| [ICAE-Bench](https://arxiv.org/abs/2607.21217) | 07-23 | 评测 coding agent 作"交互式项目构建者"：模糊需求 + User Agent 澄清 | `eval/coding` |
| [GuardianAgentBench](https://arxiv.org/abs/2607.20982) | 07-23 | 580 场景 × 三框架（LangChain/LlamaIndex/Vectara）；强模型漏调、弱模型误选 | `eval/safety` |
| [Can We Trust IRT?](https://arxiv.org/abs/2607.15190) | 07-16 | 系统检验 IRT 用于 AI 评测的可靠性：小/非正态模型集下排序推断可能失真 | `eval/methodology` |
| [evalci](https://arxiv.org/abs/2607.04429) | 07-05 | Python 库：把逐项结果表一键变成"带 CI + 配对显著性 + 多比较校正"的结论 | `eval/methodology` |
| [AppWorld-UL](https://arxiv.org/abs/2607.20536) | 07-10 | user-in-the-loop 工具使用基准；Claude Opus 4.7 仅 48.6%，组合子集 35.7% | `eval/tool-use` |
| [LongMedBench](https://arxiv.org/abs/2607.09322) | 07-10 | MIMIC-IV 电子病历长程临床决策基准；RAG/记忆助检索但决策仍依赖即时上下文 | `eval/medical` |
| [CausalDS](https://arxiv.org/abs/2607.08093) | 07-09 | 数据科学 agent 因果推理基准（结构因果模型三 rung）；弃答作为一类结果 | `eval/data-science` |
| [RuBench](https://arxiv.org/abs/2607.06411) | 07-07 | 原生俄语任务规格的仓库级 agentic coding 基准 | `eval/coding` |
| [PolyWorkBench](https://arxiv.org/abs/2607.06008) | 07-07 | 多语言长程 LLM agent 基准 | `eval/multilingual` |
| [Beyond Static Evaluation](https://arxiv.org/abs/2607.05773) | 07-07 | 为可扩展 agentic RL 构建仿真环境（而非静态数据集） | `eval/methodology` |
| [AtomicCommitBench](https://arxiv.org/abs/2607.03332) | 07-03 | 测 coding agent 能否从 squash patch 重建提交历史 | `eval/coding` |
| [GameEngineBench](https://arxiv.org/abs/2607.03525) | 07-03 | 在真实 C++ 运行时上评测 coding agent（游戏引擎） | `eval/coding` |
| [PERFOPT-Bench](https://arxiv.org/abs/2607.07744) | 07-08 | 评测 coding agent 做软件性能优化 | `eval/coding` |
| [AgentLens](https://arxiv.org/abs/2607.06624) | 07-07 | 生产级 *整条轨迹* 评审基准（正式验证 + LLM 评审 + 并排比较） | `eval/coding` |
| [Agent Retrieval Bench](https://arxiv.org/abs/2607.24882) | 07-27 | 评测 coding agent 的仓库上下文检索 | `eval/coding` `method/rag` |
| [PAIChecker](https://arxiv.org/abs/2607.28587) | 07-30 | 揭示并校验 SWE-bench 类基准中 PR 与 issue 的 *错配* | `eval/methodology` |
| [Benchmarks Are Not Validation](https://arxiv.org/abs/2607.28840) | 07-30 | 金融 LLM 应用的系统级验证观：基准 ≠ 验证 | `eval/methodology` |
| [Alipay-PIBench](https://arxiv.org/abs/2607.14573) | 07-16 | 真实支付集成 coding agent 基准 | `eval/coding` |
| [SecRespond](https://arxiv.org/abs/2607.26791) | 07-29 | 真实事后入侵响应 agent 基准 | `eval/security` |
| [IH-Benchmark](https://arxiv.org/abs/2607.25987) | 07-28 | 指令层级鲁棒性基准 | `eval/safety` |
| [Frontier AI in Business](https://arxiv.org/abs/2607.16057) | 07-17 | 跨商业学科的 case-grounded 知识工作/分析推理基准 | `eval/knowledge-work` |
| [ExplainBench](https://arxiv.org/abs/2607.26451) | 07-29 | 评测 agent 生成的代码解释质量 | `eval/coding` |

---

## 五、AI Coding Agent

> 方法、轨迹优化、经验研究（PR/落地/上下文）、benchmark（详见评测维度的 SWE-* 系列）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Agentic Coding in the Wild](https://arxiv.org/abs/2608.00101) | 07-30 | **首个生产规模 Copilot 轨迹刻画**（3.2M 用户/761M 调用/95T token）：KV 命命中 90%，跨轮骤降 | `study/production` |
| [From Code Review to Code Critique](https://arxiv.org/abs/2607.29516) | 07-31 | ARCTIC：意图预测 + 漂移检测 + 代码聚光，重定义 AI 代码评审 | `agent/coding` `method/critique` |
| [Automated Testing & Repair for Verified Compilers](https://arxiv.org/abs/2607.28928) | 07-31 | agent 为"agent 生成的已验证编译器"做测试与修复，并排查 reward hacking | `agent/coding` `method/repair` |
| [Preventing Premature Commitment](https://arxiv.org/abs/2607.28815) | 07-30 | ECLoop：证据条件执行层，SWE-bench Verified Pass@1 +4.8~11.8pp 且省 token | `method/evidence-gate` |
| [Change2Task](https://arxiv.org/abs/2607.28591) | 07-30 | 从仓库历史合并 PR 反推出可执行 coding 任务与环境（79.6% 构造成功） | `method/data-gen` |
| [MindForge](https://arxiv.org/abs/2607.27146) | 07-29 | source-free 环境教 SLM 做全生命周期 SE；Qwen3.6-27B 在 ProgramBench 37.98%→49.51% | `method/sft` `agent/coding` |
| [Coding Agents' Compliance with AI Rules](https://arxiv.org/abs/2607.26819) | 07-29 | RepoComplianceBench：agent 几乎从不主动读 OSS 的 AI 贡献规则，禁令仓也照提交 | `study/oss` |
| [CodeSpec](https://arxiv.org/abs/2607.26777) | 07-29 | 双可执行规格（架构+行为）支撑仓库级特性开发；FeatureBench 70.7% | `method/specification` |
| [(Im)Paired Programming](https://arxiv.org/abs/2607.26375) | 07-29 | 控制实验：coding agent 提升产出但 *损害* 用户对代码的理解 | `study/hci` |
| [Try Again, Don't Look Back](https://arxiv.org/abs/2607.26117) | 07-28 | 小模型上"盲重采样"优于自我修复：自我条件化造成锚定（1.5B 掉 6.1 分） | `method/self-repair` |
| [Who is scientific code for?](https://arxiv.org/abs/2607.25975) | 07-28 | 科学家用 coding agent 时的"地标化策略"：区分人类可读 vs agent 上下文 | `study/hci` |
| [Do Context Files Help?](https://arxiv.org/abs/2607.27250) | 07-28 | AGENTS.md/CLAU.md 消融：对正确性无可测影响，失败多在实现技能而非缺知识 | `study/context` |
| [OwlPath](https://arxiv.org/abs/2607.27249) | 07-28 | OWL2 本体做无损知识压缩供 bug 修复，token −28.8%、recall ×2.06 | `method/ontology` |
| [CodeNib](https://arxiv.org/abs/2607.25431) | 07-28 | 多视图（词法/稠密/结构）仓库上下文服务系统，跨编辑保持视图 | `method/context-serving` |
| [Agent Team Work Zone](https://arxiv.org/abs/2607.22917) | 07-24 | 文件系统层固化 Claude Code Agent Teams 状态：可恢复/抗压缩/减技术债 | `agent/coding` `agent/harness` |
| [How Do AI Coding Agents Contribute?](https://arxiv.org/abs/2607.21832) | 07-23 | AIDev 数据纵向研究：agentic PR 特征随开发生命周期的演化 | `study/oss` |
| [PerfAgent](https://arxiv.org/abs/2607.19653) | 07-22 | profiler 引导的仓库级优化工作流；GSO 19.6%→39.2%、SWE-fficiency 26%→74% | `method/profiler` |
| [CodeRescue](https://arxiv.org/abs/2607.19338) | 07-21 | 预算校准的"恢复路由"：失败后决定再投便宜算力还是升级；CRC 适配多变预算 | `method/cost-aware` |
| [CORVUS](https://arxiv.org/abs/2607.22711) | 07-20 | 解耦文件读与观察的同步注册表，消除陈旧快照；input token −9~50% | `method/trajectory` |
| [TRIM](https://arxiv.org/abs/2607.18161) | 07-20 | 定义 CodeSlop；通过最小化轨迹间接减冗余代码 17.9-32.9% | `method/trajectory` |
| [When and How Context Rot Appears](https://arxiv.org/abs/2607.17937) | 07-20 | 白盒研究：相关/无关长上下文都使技能通过率从 8/10 掉到 3/10（趋势级） | `study/context` |
| [Trajectory Data Curation for LoRA](https://arxiv.org/abs/2607.17205) | 07-19 | 67K 轨迹系统研究：质量-数量权衡随规模变化，error-retry 是主导子维 | `method/sft` |
| [Harness Handbook](https://arxiv.org/abs/2607.13285) | 07-14 | 自动合成"行为中心"表示，做 harness 行为定位与渐进披露，助 harness 演化 | `agent/harness` |
| [Function-Aware FIM Mid-Training](https://arxiv.org/abs/2607.12463) | 07-14 | 把 agent 的动作-观察-续写同构于函数调用做 FIM 中训，SWE-bench +2.8~5.4pp | `method/mid-training` |
| [Beyond Test Presence](https://arxiv.org/abs/2607.12068) | 07-13 | 20 万测试件实证：agent 边界覆盖更好但 flakiness 更高（环境感知差） | `study/testing` |
| [Predicting PR Acceptance](https://arxiv.org/abs/2607.12057) | 07-13 | 用提交时特征预测人/agent PR 的接受与评审负担（F1>0.95） | `study/oss` |
| [FlowArk](https://arxiv.org/abs/2607.11308) | 07-13 | 批量 Android 数据流分析的知识复用，API 成本 −26.8% | `method/knowledge-reuse` |
| [Inference Economics of Enterprise Agents](https://arxiv.org/abs/2607.13080) | 07-13 | 云 vs 本地（NVFP4 量化）coding agent 案例研究：缓存使 API 更便宜，本地缺陷率更高 | `study/economics` |
| [Know Before Fix](https://arxiv.org/abs/2607.11111) | 07-13 | ACQUIRE：修复前先 QA 式获取仓库知识，SWE-bench Verified Pass@1 +4.4pp | `method/knowledge-acq` |
| [Imaging-101](https://arxiv.org/abs/2607.10789) | 07-12 | 计算成像 57 任务 coding agent 基准，揭示算法选择/物理约定/流水线集成差距 | `eval/coding` `env/science` |
| [Failure as a Process](https://arxiv.org/abs/2607.09510) | 07-10 | 1794 条 CLI agent 轨迹解剖：失败多源于认知错误、起于前几步、常隐藏到不可恢复 | `study/failure` |
| [SCATE](https://arxiv.org/abs/2607.08983) | 07-09 | 把监督 coding agent 建模为 contextual bandit，治"懒惰生成"，覆盖 +32.3% | `method/bandit` |
| [DeepSWE](https://arxiv.org/abs/2607.07946) | 07-08 | 113 个 *原创* 长程 SE 任务（不回流上游防污染）+ 手写 verifier，拉开 frontier 差距 | `eval/coding` |
| [What Resolve Rate Hides](https://arxiv.org/abs/2607.06184) | 07-07 | TraceProbe：把轨迹标准化为 9 类动作，诊断 resolve rate 之外的反模式 | `study/trajectory` |
| [Agents That Teach](https://arxiv.org/abs/2607.06101) | 07-07 | 提出"知识债"，设计 SHIELD 把偶发学习重新设计进 agent 辅助开发 | `study/hci` |
| [SWE-Review](https://arxiv.org/abs/2607.06065) | 07-07 | 生成-评审-修订闭环；agentic review 持续改进 PR 且可迁移到 issue 解决 | `method/code-review` |
| [From Conversation to Contribution](https://arxiv.org/abs/2607.05677) | 07-06 | 13K AI 会话 × OSS 历史：AI 采用后贡献者更活跃，无广泛代码质量退化 | `study/oss` |
| [Latent Programming Horizons](https://arxiv.org/abs/2607.05188) | 07-06 | 残差流线性编码程序属性，且 *超前* 于 agent 自己的编辑（提前 ~25 步） | `study/interp` |
| [AI Agent PRs on GitHub](https://arxiv.org/abs/2607.04697) | 07-06 | 首个 agent 并发提交研究：40% 仓含同时活跃 agent-PR 对，跨 agent 冲突率 41.7% | `study/oss` |
| [Don't Blame the LLM](https://arxiv.org/abs/2607.03691) | 07-04 | 固定模型变 harness：35 个 Qwen Code CLI 连续版本的 *harness* 对质量的冲击 | `study/harness` |
| [CoACT](https://arxiv.org/abs/2607.02911) | 07-03 | 动作保持的观察压缩：以"下一动作不变"为信号，token −33% 维持效果 | `method/compression` |
| [SwarmResearch](https://arxiv.org/abs/2607.02807) | 07-02 | shepherd+search agents 各持本地上下文与 git 分支，治"单 agent 收敛单一解" | `agent/multi-agent` |
| [Steerability via Constraints](https://arxiv.org/abs/2607.02389) | 07-02 | 用访问控制/网络策略/编码规范做 coding agent 的可扩展监督；后门召回 54.5%→90.9% | `agent/safety` |
| [Coding Agents Are Guessing](https://arxiv.org/abs/2607.02294) | 07-02 | UnderSpecBench：欠规格指令下 55.8-67.8% 运行违反至少一个边界 | `eval/safety` |
| [Coding-agents Replicate Sci-ML Papers](https://arxiv.org/abs/2607.02134) | 07-02 | 把论文声明变目标+证据+验证的工作流，12 次运行全过完成门 | `agent/coding` `env/science` |
| [Adoption and Impact of CLI Agents](https://arxiv.org/abs/2607.01418) | 07-01 | 微软 2026 初 Claude Code/Copilot CLI 滚动研究：采用者多合并 ~24% 更多 PR | `study/adoption` |
| [SWE-Doctor](https://arxiv.org/abs/2607.00990) | 07-01 | 用多面 bug 复现测试的运行时诊断引导补丁生成；SWE-bench Verified 75.7% | `method/diagnosis` |
| [Cheap Code, Costly Judgment](https://arxiv.org/abs/2607.01087) | 07-01 | 12 周单人 case study：提出"治理转换"理论，把 agentic 失败转为持久治理机制 | `study/governance` |
| [From Registry to Repository](https://arxiv.org/abs/2607.00911) | 07-01 | 首个 agent skill 工件实证：4 万+ skill，复用多为一次性拷贝、53% 不再改 | `study/skills` |
| [KAT-Coder-V2.5](https://arxiv.org/abs/2607.05471) | 07-06 | agentic coding 模型技术报告；AutoBuilder 重建可执行环境 + 多专家 on-policy 蒸馏 | `model/coding` |
| [PeepholeBench](https://arxiv.org/abs/2607.02684) | 07-02 | 评测 coding agent 实现 LLVM 漏掉的窥孔优化；正确性与盈利性难兼得 | `eval/coding` |
| [Refploit](https://arxiv.org/abs/2607.01760) | 07-02 | 用 code-agent 轨迹修复从公开 exploit 参考重建 Java 漏洞 exploit（80.2%） | `agent/coding` `agent/safety` |
| [PatchFusion](https://arxiv.org/abs/2607.01597) | 07-02 | 确定性原子证据融合候选补丁：SWE-bench Verified 解 426/500 | `method/fusion` |
| [Post-Merge Fate of Agentic Code](https://arxiv.org/abs/2607.09902) | 07-10 | 纵向研究：agentic 代码合并后需更高纠正维护、引入更多安全弱点 | `study/oss` |

---

## 六、规划与长程推理（Planning & Long-Horizon Reasoning）

> Deep research / 搜索 agent、长程信用分配、上下文管理。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Bayesian and Motivated Reasoning](https://arxiv.org/abs/2608.00339) | 07-31 | 证据相同、仅框架不同时 agent 结论被先验显著影响（医学/选举/预测） | `study/reasoning-bias` |
| [Baikal](https://arxiv.org/abs/2607.27726) | 07-30 | 把 data lake 上的 deep research 建模为预算搜索，语义区域探索-利用平衡 | `agent/deep-research` |
| [DeepResearch Agent System](https://arxiv.org/abs/2607.27562) | 07-30 | 30B/3B 激活稀疏检索系统，128K 上下文，HLE 87.3%（全开源） | `agent/deep-research` |
| [CHILL-Harness](https://arxiv.org/abs/2607.25825) | 07-28 | 用反事实因果干预做 harness 工作流自适应，保成功率同时省 token/时间 | `method/causal-harness` |
| [SearchArt](https://arxiv.org/abs/2607.24850) | 07-25 | 验证驱动的任务合成 + 多阶段后训练训长程搜索 agent；27B 在 BrowseComp 70.06 | `method/training` |
| [Progress-conditioned GPO](https://arxiv.org/abs/2607.22724) | 07-22 | ProGPO：全零奖励组用首次访问新状态覆盖破"信用陷阱" | `method/rl` |
| [Delegation Intelligence in Deep Search](https://arxiv.org/abs/2607.23524) | 07-26 | 把 deep search 能力解耦为"搜索决策"与"信息综合验证"分别评测 | `eval/deep-search` |
| [Beyond the Leaderboard](https://arxiv.org/abs/2607.05775) | 07-07 | 综合 27 篇基准/审计，给出 6 类 agent 失败集群的统一分类法 | `eval/synthesis` |

---

## 七、Agent 安全与可靠性（Safety & Reliability）

> 工具/MCP/供应链/skill 文件/组合攻击、监控、可验证授权、记忆安全（记忆投毒见记忆维度）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Distributing Security Controls (SHarD)](https://arxiv.org/abs/2607.25890) | 07-28 | 在 Pi harness 上把沙箱/skill 扫描/工具限制打包成可分发的安全 harness | `agent/safety` `agent/harness` |
| [SkillGate](https://arxiv.org/abs/2607.25619) | 07-28 | 恶意 skill 文件检测网关（regex+LLM judge），F1 0.817、token −77% | `agent/safety` `attack/supply-chain` |
| [Cyber-Capable AI Agents](https://arxiv.org/abs/2607.25379) | 07-28 | 综述：评测环境本身即安全边界（引 2026-07 HF/OpenAI 评测入侵事件） | `agent/safety` `eval/containment` |
| [Hybrid Analysis for MCP (MTGuard)](https://arxiv.org/abs/2607.25297) | 07-28 | 生命周期感知的静态-动态协同分析防御 MCP 工具恶意使用 | `agent/safety` `env/mcp` |
| [ToolGuardian](https://arxiv.org/abs/2607.21835) | 07-23 | 用 Answer Set Programming 做声明式 agent-工具安全策略与运行时授权 | `agent/safety` `method/asp` |
| [Cryptographically Verifiable Authorization](https://arxiv.org/abs/2607.21325) | 07-23 | 把 agent 授权形式化为密码可验证关系，Groth16 zk-SNARK 概念验证 | `agent/safety` `method/crypto` |
| [IssueTrojanBench](https://arxiv.org/abs/2607.20759) | 07-22 | 恶意 issue 攻击 coding agent（Cursor/Claude Code/Codex）；66.5% 穿透所有护栏 | `agent/safety` `attack/malicious-issue` |
| [JANUS (Vanguard)](https://arxiv.org/abs/2607.19913) | 07-22 | 预见式长程安全：从部分轨迹预测延迟风险，执行前拦截（+15.9pp） | `agent/safety` `method/foresight` |
| [Guardrails as Scapegoats](https://arxiv.org/abs/2607.19449) | 07-21 | 工具静默失败时 agent 多直接捏造；安全措辞使"不忠拒答"放大 15.6× | `agent/safety` `eval/silent-fail` |
| [ChainWatch](https://arxiv.org/abs/2607.19432) | 07-20 | 用 6 阶段 kill chain + HMM 检测 MCP 多步攻击序列 | `agent/safety` `env/mcp` |
| [Operational Hallucination & Safety Drift](https://arxiv.org/abs/2607.18366) | 07-20 | 多轮中安全意图逐步侵蚀 + 工具活锁；提议 Action-Aware 监督层 | `agent/safety` |
| [Self-State Attacks](https://arxiv.org/abs/2607.17986) | 07-20 | 自托管 agent 的"自状态攻击"四维空间，评估 OS 防御极限 | `agent/safety` `attack/self-state` |
| [Code-Poisoning Property Inference](https://arxiv.org/abs/2607.15970) | 07-17 | 首个代码级属性推断攻击（GitHub/Codex 投毒代码），100% 攻击准确率 | `agent/safety` `attack/code-poison` |
| [Neural→Cryptographic Authorization (NCS)](https://arxiv.org/abs/2607.15596) | 07-17 | 神经规划器起草、符号控制器用哈希链签名门控执行，ASR 近零 | `agent/safety` `method/neuro-symbolic` |
| [Beyond Success Rate (安全 agent)](https://arxiv.org/abs/2607.15263) | 07-16 | 成本感知评测攻防安全 agent：进攻随算力扩、防御靠纪律而非算力 | `eval/security` `method/cost-aware` |
| [Democratizing Agent Safety (IFG)](https://arxiv.org/abs/2607.14570) | 07-16 | 信息流图监控基础设施级破坏；同步模式把主+隐蔽任务成功率 74.4%→0% | `agent/safety` `method/ifg` |
| [Trust but Verify? Security Debt](https://arxiv.org/abs/2607.12428) | 07-14 | AIDev 实证：38.9% agent-PR 含安全 smell，供应链占 82.3% | `study/security` |
| [Distributed Backdoors (Multi-Agent)](https://arxiv.org/abs/2607.11751) | 07-13 | 证明局部 benign 时单步监控原理上抓不到组合危害 | `agent/safety` `attack/distributed` |
| [NetInjectBench](https://arxiv.org/abs/2607.10490) | 07-11 | 网络运维场景间接注入基准；metadata 感知策略门把不安全动作降到 ~0 | `eval/security` `env/network` |
| [Untrusted Content Masking](https://arxiv.org/abs/2607.05277) | 07-06 | 用 DOM 结构屏蔽 web agent 的不可信区域，恢复可证明防御的信任边界 | `agent/safety` `agent/web-agent` |
| [Agent Data Injection (ADI)](https://arxiv.org/abs/2607.05120) | 07-06 | 新 IPI 类别：伪装可信数据/元数据；在 Claude/Codex/Gemini CLI 实现 RCE/供应链攻击 | `agent/safety` `attack/adi` |
| [Refused in Chat, Written in Code](https://arxiv.org/abs/2607.03968) | 07-04 | IDE coding agent 的 *工作流级越狱*：直接拒答的 prompt 经工作流后 816/816 成功 | `agent/safety` `attack/workflow-jailbreak` |
| [MOSAIC](https://arxiv.org/abs/2607.02857) | 07-03 | CLI 命令组合攻击（CCR）：良性命令串成生产者-消费者利用，ASR 96.59% | `agent/safety` `attack/cli-composition` |
| [Distributed Attacks in Persistent-State](https://arxiv.org/abs/2607.02514) | 07-02 | Iterative VibeCoding：把攻击分散到多个 PR，单一监控无法同时堵住渐变与突变 | `agent/safety` `attack/iterative` |
| [Jailbreaking Function-Calling via SMT](https://arxiv.org/abs/2607.00481) | 07-01 | 伪造审核轨迹多轮绕过 function-calling LLM 安全约束 | `agent/safety` `attack/jailbreak` |
| [HexStrike Orchestration Limits](https://arxiv.org/abs/2607.02873) | 07-03 | 研究 LLM 安全工具编排的决定因素与边界 | `agent/safety` |
| [Unicode TAG-Block Concealment](https://arxiv.org/abs/2607.05744) | 07-07 | MCP 工具元数据载荷的 Unicode 隐藏，跨三实现审批视图保真度缺口 | `agent/safety` `env/mcp` |

---

## 八、多智能体（Multi-Agent）

> 拓扑/协作/博弈/信息流。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [AgentRadio](https://arxiv.org/abs/2607.28430) | 07-30 | 异步消息层让 coding agent 执行中被动感知队友；4 agent 在 SWE-Atlas QnA 62.1% | `agent/multi-agent` `method/async` |
| [SKIMIX](https://arxiv.org/abs/2607.27994) | 07-30 | 多 agent 持不同技能组合协作；对开放数学推理有效、对选择题有限 | `agent/multi-agent` `method/skill-mixture` |
| [Belief Coevolution](https://arxiv.org/abs/2607.27512) | 07-29 | CoevolveSim：专才 LLM（非 persona）才显著改变群体共识 | `agent/multi-agent` `study/belief` |
| [UrbanDS](https://arxiv.org/abs/2607.26724) | 07-29 | 图引导多 agent 做数据密集型城市任务（数据集图 + 多角色），已部署武汉东西湖 | `agent/multi-agent` `env/urban` |
| [Focus Is All You Need (AGAO)](https://arxiv.org/abs/2607.23678) | 07-26 | 把 Transformer 式注意力扩展到 agent 图编排，聚焦目标关键路径 | `agent/multi-agent` `method/attention-orch` |
| [Reliability-Contagion Feasibility](https://arxiv.org/abs/2607.21912) | 07-24 | 校正感知网络模型推导可靠性与错误传播的对偶图约束 | `agent/multi-agent` `method/epidemic` |
| [GRADRAG](https://arxiv.org/abs/2607.21324) | 07-23 | 跨组件 prompt 自适应：把 RAG 当计算图，沿图回传结构化反馈 | `agent/multi-agent` `method/rag` |
| [Commitment to Cooperation](https://arxiv.org/abs/2607.22750) | 07-23 | 用自协商 *合约*（可编译为代码）实现 LLM agent 间可信合作 | `agent/multi-agent` `method/contract` |
| [Dynamic Coalition Formation](https://arxiv.org/abs/2608.07532) | 07-24 | 合作博弈 + Shapley 估值决定激活哪些 agent 与通信边，贪心路由达 99.5% 最优 | `agent/multi-agent` `method/game-theory` |

---

## 九、模型与系统（Models & Systems）

> 新模型发布 + agent 推理/服务系统。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Kimi K3](https://arxiv.org/abs/2607.24653) | 07-27 | **2.8T MoE / 104B 激活 / 1M 上下文**，Kimi Delta Attention + Attention Residuals，权重全开；逼近 Claude Fable 5 / GPT-5.6 Sol | `model/frontier` `model/kimi` |
| [Nanbeige4.2-3B](https://arxiv.org/abs/2607.22083) | 07-24 | 紧凑 agentic 模型（Looped Transformer，28T token），超 Qwen3.5-9B/Gemma4-12B | `model/compact` |
| [Cura 1T](https://arxiv.org/abs/2607.15314) | 07-15 | 基于 Kimi-K2.6 的医疗专模型，human-gated RSI 循环训练 | `model/healthcare` `method/rsi` |
| [KAT-Coder-V2.5](https://arxiv.org/abs/2607.05471) | 07-06 | agentic coding 模型（见 coding 维度）；PinchBench 最佳工具使用 | `model/coding` |
| [SpecBox](https://arxiv.org/abs/2607.23933) | 07-27 | MCP 沙箱投机预热+上下文随机预取，P99 时延 ×2.9 降、峰值内存 −45.9% | `system/serving` |
| [TokTier](https://arxiv.org/abs/2607.29678) | 07-31 | 有状态 CPU+GPU 分词服务，保证与全量分词恒等；TTFT 降 16-34% | `system/serving` |
| [Talaria](https://arxiv.org/abs/2607.17181) | 07-19 | 会话感知的 serverless 多模型服务（百亿参数），p50 SCT 1000s→189s | `system/serving` |
| [Cache-Aware Prompt Compression](https://arxiv.org/abs/2607.15516) | 07-17 | 两层缓存成本模型：查询无关压缩 + 缓存控制，16/16 配置最省 | `system/cost` |
| [Agentic Routing (OpenSquilla)](https://arxiv.org/abs/2607.11399) | 07-13 | harness 原生步级路由（单/多模型），路由记录构成"数据飞轮" | `system/routing` `agent/harness` |
| [ToFu](https://arxiv.org/abs/2607.11423) | 07-13 | 面向研究者的白盒、token 高效 agent harness（MIT 许可，可本地部署） | `agent/harness` |
| [Workflow as Knowledge](https://arxiv.org/abs/2607.08740) | 07-09 | Lisp 启发的语义持久模型：区分 derive（确定计算）与 infer（LLM 判断） | `method/semantic-persistence` |
| [Harness Eng for GPU Kernels](https://arxiv.org/abs/2607.17979) | 07-20 | 以 harness 为中心的 GPU kernel 生成系统（MLSys 2026 FlashInfer 竞赛） | `agent/harness` `env/gpu` |

---

## 十、本月必读（Top 12）

挑选本月最具代表性的论文，建议优先精读：

1. **[Kimi K3](https://arxiv.org/abs/2607.24653)** — 月度最重要开源 frontier 发布，2.8T MoE / 1M 上下文，是观察开源-闭源差距的关键参照。
2. **[AREX](https://arxiv.org/abs/2607.21461)** — 递归自改进 deep research agent 的清晰范本（内层取证 + 外层约束审计 + 自主上下文更新工具）。
3. **[Agentic Coding in the Wild](https://arxiv.org/abs/2608.00101)** — 首个生产规模 Copilot 轨迹刻画，重新定义"agent 原生"基础设施假设。
4. **[DeepSWE](https://arxiv.org/abs/2607.07946)** — 用原创任务 + 手写 verifier 规避 SWE-bench 污染，是 coding agent 评测的方法论升级。
5. **[SelfMem](https://arxiv.org/abs/2607.03726)** — "授 agent 以渔"的记忆自优化，BEAM 上 +48.7%，思路优雅。
6. **[Metis](https://arxiv.org/abs/2607.26760)** — 首个"记忆基础模型"，把记忆内化进 backbone，是记忆方向的新范式。
7. **[Skill Self-Play](https://arxiv.org/abs/2607.22529)** — Qwen 团队的技能共进化自训练，平衡可验证性与开放性。
8. **[TRACE](https://arxiv.org/abs/2607.13988)** — 长程 agent turn 级信用分配，BrowseComp-Plus 7.2→35.6，RL 训练关键。
9. **[Don't Blame the LLM](https://arxiv.org/abs/2607.03691)** — 用固定模型变 harness 证明"质量回归常被错怪到模型"，harness 工程的实证基础。
10. **[Beyond the Leaderboard](https://arxiv.org/abs/2607.05775)** — 跨 27 篇综合出 6 类 agent 失败的统一分类法，适合做评测总览。
11. **[RSIBench-Data](https://arxiv.org/abs/2607.25886)** — 把"递归自我改进"变成可评测对象，揭示当前 agent 难把反馈稳定转成改进。
12. **[KAT-Coder-V2.5](https://arxiv.org/abs/2607.05471)** — 完整的 agentic coding 模型后训练栈（环境重建 + 过程过滤 + 多专家蒸馏），工程参考价值高。

---

## 附：方法与采集说明

- **召回**：arXiv API `submittedDate:[202607010000 TO 202607312359]` × 关键词组（`LLM agent` / `AI agent` / `tool use` / `memory` / `benchmark` / `coding agent` / `self-evolv` 等），共去重得 ~532 篇候选。
- **筛选**：保留 cs.AI / cs.CL / cs.SE / cs.MA / cs.CR / cs.LG 等相关类别，按标题+摘要做主维度归类，剔除纯机器人/网络/量子/医学影像等与 LLM-agent 主线弱相关的论文。
- **归类**：每篇论文归入 *单一主维度* 以避免重复（跨维度概念在标签中体现，如记忆安全同时标 `agent/safety`）。
- **局限**：仅依据摘要撰写一句话要点；未读全文，具体结论与数字请以原文为准。7 月底提交、8 月初公告的少量论文 ID 为 `2608.xxxxx`，仍按 7 月口径收录。
