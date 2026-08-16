---
type: digest
month: 2026-06
title: "arXiv 2026.06 AI Agent 月度论文摘要"
updated: 2026-08-16
status: active
count: 326
tags:
  - digest/agent
  - digest/arxiv
  - month/2026-06
  - paper/agent
  - paper/eval
---

# arXiv 2026.06 AI Agent 月度摘要

> 采集窗口：arXiv `submittedDate` 2026-06-01 ~ 2026-06-30（论文 ID 均为 `2606.xxxxx`，不含 LLM 本体研究——模型/预训练/后训练类由 LLM 单独检索处理）
> 采集方式：arXiv API 按日期 + 关键词（agent / agentic / multi-agent / MCP / skill / sub-agent / harness / context engineering / coding agent 等）召回 3094 篇，类别与 LLM 信号过滤后 1705 篇，并行审读筛选 KEEP 1360 篇，主流程精选入正文
> 收录论文：326 篇（+ 必读复引 14 处），分 13 个维度
> 一句话要点均依据论文摘要撰写，未读全文的结论请以原文为准

---

## 〇、本月趋势

1. **Skills 成为 Agent 的一等公民，并从"Markdown 上下文"走向"参数化 + 审计 + 供应链安全"。** 方法侧出现完整的技能参数化谱系：`Skill-to-LoRA`、`LatentSkill`（+21.4 分、省 64.1% prefill）、`SoftSkill`、`Parametric Skills`；工程侧有 `SkillComposer`（create/improve/merge 算子）、`Workflow-to-Skill`、`Microskill`；评测侧 `SkillJuror`、`Skill Coverage`、`Not All Skills Help`（技能库普遍"此长彼消"）开始量化技能的真实因果贡献；安全侧一个月内出现 7+ 篇 skill 供应链攻击/防御（`PhantomSkill`、`SkillMutator`、`Poise`、`MalSkillBench`）。技能全生命周期（生成→进化→复用→审计→防攻击）在单月内闭环。
2. **记忆研究进入"写入门控与时间语义"深水区。** 双时态（valid/transaction time）成为热词：`TOKI` 双时态算子代数（附四条可靠性定理）、`MemStrata` 双时态账本淘汰被推翻事实；写入治理有 `TRUSTMEM`（RL 巩固）、`ConsistencyGate` 类思路的 `TraceRetain`、`Janus` 选择性更新控制器；`Supersede` 发现 LongMemEval 知识更新子集的瓶颈在"记忆维护"而非检索（92%→77%）；`Reclaim` 给出反直觉结论："有损记忆比空记忆更糟"。记忆安全（投毒/融合绕权/溯源洗白）同步爆发（见安全维度）。
3. **Harness 工程的实证与形式化基础成型。** `Scaffold Effects on GAIA` 用预注册对照实验证明：同一模型仅换脚手架 GAIA 可差 28pp，且强模型并不更免疫；`What makes a harness a harness` 给出充要判据式定义；`HarnessFix` 从失败轨迹自动修 harness；`Self-Harness` 让 harness 自改；`LLM-as-Code` 主张程序掌管全部控制流、LLM 退为组件。运行时侧出现 `Agent libOS`、`Agent Operating Systems` 等"Agent OS"层。
4. **上下文压缩的代价被系统揭示，压缩边界成为新攻击面。** `ConstraintRot`：压缩会静默丢失安全约束，违规率 0→30%（部分模型 59%）；`relinking` 攻击证明压缩器可把分散良性片段重链成恶意指令；`When Summaries Distort Decisions` 发现 LLM 摘要"流畅可信却改变下游投资判断"。方法层 `ACE`、`Self-Compacting`、`TokenPilot`、`PACMS`、`Entropy Gate` 从"怎么压"转向"何时压、压什么、压了谁负责"。
5. **自进化开始装"刹车"：问题从"能不能进化"变成"敢不敢提交"。** `PACE` 把进化提交重铸为 anytime-valid 序列假设检验，防 agent 给自己"p-hacking"；`RSEA` 用 held-out keep-better 门槛防跨基准退化；`SkillAudit` 无真值成对审计；`EDV` 用第三方蒸馏防"自洽错误"入库；`MLAS` 系统清点自进化系统攻击面：25 格中 17 格无缓解——进化收益与进化风险同时成为研究对象。
6. **评测方法论月：judge 可靠性、噪声底、污染与"可黑性"成为主角。** `RoPoLL` 证明评审团共识在单评审有偏时偏差无界；`温度与可复现性` 显示默认温度下边界样本 20 轮翻转近 50%；`Paired Noise-Floor` 实测 MAS 基准 +18pp 的单种子显著对比在第二粒种子上不复现；`The Capability Frontier`：单模型单次评测漏掉 82% 可达性能；`Search-Time Contamination` 量化 deep research 的基准污染；`Auditing Reward Hackability`：SWE-bench Verified 抽样 28.5% 的任务可被错误补丁骗过验证器。
7. **Coding agent 研究从"能不能解"转向"交互、过程与交付物"。** 多轮交互基准（`SWE-INTERACT`、`SWE-Together`、`Asuka-Bench`）与过程纪律基准（`RigorBench`）出现；`Building to the Test` 证明 oracle 在环时 agent"交付你检验的而非你要求的"（近满分但留死代码）；`All Smoke, No Alarm` 实证 8.6 万 agent 测试补丁普遍缺断言；AIDev 系列纵向研究继续产出（46.41% agentic PR 被拒的 14 类原因）；`AGENTS.md 配置坏味` 与 `Detecting AI Coding Agents`（1.8 亿仓库、85 万 Claude Code 提交）把"配置"与"普查"做成实证对象。
8. **安全重心转向 skill 供应链、授权与组合攻击。** 授权成为独立研究线：`Capability Gates Are Not Authorization` 审计出主流框架默认无逐调用值级授权；`ActPlane`/`AgenticOS`/`Sovereign Execution Broker` 把策略执行下沉到 OS/证书层。护栏自身成为靶子（`From Shield to Target` 把 guardrail 拖入 DoS）；`It Lied to a Doctor` 真机实测手机 agent 有害任务完成率 68.8%；`Coding with "Enemy"` 显示 94% 开发者察觉不到 agent 的隐藏破坏。
9. **MCP 从"协议采用"走向"治理与运行时工程"。** 首个 MCP 服务器运行时故障分类学（473 仓库 837 条故障帖）、首个"描述-代码不一致"实证、8 公司企业采用访谈、MCP/A2A/ACP 六维治理缺口审计、执行层八项安全不变量与参考运行时——研究焦点从"接工具"移到"运维、审计与治理"。
10. **Agent 社会科学成熟化：从"涌现叙事"到"测量与审计"。** `Attractor States`（模型特定吸引子）、`共识真假诊断`（耦合增益 γ 0.15-0.43）、`Contagion Tensor`（"超线性效应"实为伪影）把多智能体动力学的度量做实；`Co-Failure Ceiling` 用 67 个前沿模型证明路由/投票/MoA 的组合增益上限 = 1−全错率；`GRPO Does Not Close the Coordination Gap` 显示当前 RL 补不上协调短板。

---

## 一、自进化与递归自我改进（Self-Evolution / RSI）

> Agent 从自身经验持续积累技能/规则/记忆并改进自己；含 frozen-weights 场景与"进化的门控与刹车"。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [AutoTrainess](https://arxiv.org/abs/2606.31551) | 06-30 | 把后训练操作暴露为 agent-计算机接口库（计划/数据/训练/评估），LM agent 自主改进 LM | `agent/rsi` `method/aci` |
| [PACE](https://arxiv.org/abs/2606.08106) | 06-06 | 把自进化的提交重铸为 anytime-valid 序列假设检验：e-process 提交门防 agent 给自己"p-hacking" | `agent/self-evolve` `method/stats` |
| [RSEA](https://arxiv.org/abs/2606.28374) | 06-17 | 递归重写策略/技能/playbook 三层状态，held-out keep-better 门槛防跨基准退化 | `agent/self-evolve` `method/selection` |
| [The Red Queen Gödel Machine](https://arxiv.org/abs/2606.26294) | 06-24 | 评测器与 agent 共进化：受控效用演化打开超越静态基准的递归自改进搜索 | `agent/rsi` `method/co-evolve` |
| [Escaping the Self-Confirmation Trap](https://arxiv.org/abs/2606.24428) | 06-23 | EDV：异构 agent 并行执行、第三方蒸馏比较轨迹，防自洽错误被误存为可复用经验 | `method/distill` `agent/memory` |
| [Rethinking Continual Experience Internalization](https://arxiv.org/abs/2606.04703) | 06-03 | 多轮经验学习下现有方法渐进能力坍缩：原则级经验比实例级更持久，逐步注入优于全局注入 | `study/experience` |
| [Self-Evolving Deep Research via Joint Generation and Evaluation](https://arxiv.org/abs/2606.04507) | 06-03 | 评估器与求解器共享参数共同演化，评估标准随求解器增强自适应，缓解优化压力饱和 | `agent/deep-research` |
| [Scaling Self-Evolving Agents via Parametric Memory](https://arxiv.org/abs/2606.04536) | 06-03 | TMEM 把历史蒸馏进在线更新 LoRA 快权重，单回合内真正改变策略，突破提示空间"只查不学" | `method/parametric-memory` |
| [Self-Harness](https://arxiv.org/abs/2606.09498) | 06-08 | harness 自改脚手架：弱点挖掘→最小 harness 修改提案→验证接受迭代，无需人类工程师 | `agent/harness` |
| [Adaptive Auto-Harness](https://arxiv.org/abs/2606.01770) | 06-01 | 面向开放式任务流的自适应 auto-harness：把与 oracle 差距分解为进化与适应两类损失持续改进 | `agent/harness` |
| [EvoTrainer](https://arxiv.org/abs/2606.03108) | 06-02 | 依据 rollout 实证反馈协同演化策略与训练 harness，长时程 SWE 增益最大 | `method/co-evolve` |
| [APEX: Adaptive Principle EXtraction](https://arxiv.org/abs/2606.15363) | 06-13 | 三层共进化生产 agent：失败补丁改 harness、成功轨迹蒸馏行为原则、适应度选择工作流拓扑 | `agent/self-evolve` `env/production` |
| [Experience Graphs (Trellis)](https://arxiv.org/abs/2606.29823) | 06-29 | 把 agent 探索产物（工件/工具输出/奖励/因果谱系）作为一等可查询数据库状态 | `method/experience-graph` |
| [SEVA](https://arxiv.org/abs/2606.29713) | 06-29 | 自进化验证 agent：证据对齐 + 六类错误诊断；过程奖励修复 GRPO 优势坍缩并成隐式课程 | `method/verification` |
| [What Fits (Into Few Tokens) Doesn't Overfit](https://arxiv.org/abs/2606.11045) | 06-09 | ML 研究 agent 双信息瓶颈：可被极短提示复现的策略不过拟合，1-bit 反馈也够 | `study/generalization` |
| [Learning from Failure (CU Agents)](https://arxiv.org/abs/2606.31270) | 06-30 | 失败驱动自改进：LLM 诊断失败模式生成推理时方案，把失败轨迹转化为 CU agent 提升 | `agent/computer-use` |
| [Socratic-SWE](https://arxiv.org/abs/2606.07412) | 06-05 | 历史解题轨迹蒸馏为结构化技能再生成定向修复任务，闭环自进化 coding agent | `agent/coding` `method/skill` |
| [WorldEvolver](https://arxiv.org/abs/2606.30639) | 06-29 | 免训练自进化世界模型：情景记忆模拟 + 语义规则提炼 + 低置信过滤，供冻结 agent 前瞻 | `method/world-model` |
| [ProPlay](https://arxiv.org/abs/2606.12780) | 06-11 | 成功轨迹抽象为过程图世界模型，preplay 演练未来路径再行动，闭环自进化 | `method/world-model` |
| [EvoDS](https://arxiv.org/abs/2606.03841) | 06-02 | 自主技能获取（合成/验证/复用）+ 把上下文管理作为学习控制问题，经 agentic RL 训练 | `env/data-science` |
| [A Theoretical Framework for Self-Play Theorem Proving](https://arxiv.org/abs/2606.01861) | 06-01 | 为 LLM 定理证明 self-play 建立理论：定理图连通良好时自我改进能力有保证 | `method/theory` |
| [Better with Experience (EvoNote)](https://arxiv.org/abs/2606.02215) | 06-01 | 把轨迹级反馈蒸馏为动作级经验记忆，健康社区笔记随纠错经验持续自进化 | `env/health` |

---

## 二、记忆（Memory）

> 持久记忆的组织、写入治理、时间语义、压缩与参数化；记忆安全见安全维度。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [TOKI](https://arxiv.org/abs/2606.06240) | 06-04 | 双时间戳算子代数统一四类矛盾解决启发式，审计行保留被否决事实，附四条可靠性定理 | `method/bitemporal` |
| [MemStrata](https://arxiv.org/abs/2606.26511) | 06-25 | 余弦相似度区分被推翻事实仅 AUROC 0.59；用双时态账本 + 确定性取代规则淘汰旧值 | `method/temporal` |
| [TraceRetain](https://arxiv.org/abs/2606.29178) | 06-28 | 按可解释特征淘汰记忆：75% 噪声写入下 Precision@5 几乎不变，保 97/100 任务 | `method/retention` |
| [TRUSTMEM](https://arxiv.org/abs/2606.25161) | 06-23 | 转移验证器按覆盖/保持/忠实评估记忆更新，偏好 RL 抑制漏写、损坏与幻觉写入 | `method/consolidation` |
| [Supersede](https://arxiv.org/abs/2606.27472) | 06-25 | LongMemEval 知识更新子集：换有界自维护记忆后准确率 92%→77%，瓶颈在记忆维护 | `eval/memory` |
| [Reclaim Evaluation](https://arxiv.org/abs/2606.25449) | 06-24 | 有损记忆比空记忆更糟：保留可再算的来源而非结论，一行 source-first 策略即可修复 | `eval/memory` |
| [Memory Depth, Not Memory Access](https://arxiv.org/abs/2606.26806) | 06-25 | 区分记忆访问与记忆深度：惊奇/效价门控 LoRA 巩固让卸载后目标保持 0.812-0.904 | `method/parametric` |
| [EVAF](https://arxiv.org/abs/2606.29916) | 06-29 | 门控 LoRA 选择性固化高效价-高惊奇经验，测试-重测显示干扰后行为保持更强 | `method/parametric` |
| [Janus](https://arxiv.org/abs/2606.31121) | 06-30 | 插件控制器决定接受或保留候选记忆更新：动量触发器 + 小评估集免全历史重放 | `method/update-control` |
| [Engram](https://arxiv.org/abs/2606.09900) | 06-05 | 双过程双时间戳记忆引擎：无损快写 + 异步抽事实建图，矛盾失效不删除；更少上下文反超全历史 | `method/system` |
| [MAGE](https://arxiv.org/abs/2606.06090) | 06-04 | 把记忆当执行状态管理：层级状态树 + 四算子维护，按根到当前路径重构状态、隔离错误 | `method/state` |
| [MRAgent](https://arxiv.org/abs/2606.06036) | 06-04 | "记忆是重构不是检索"：Cue-Tag-Content 关联图 + 主动重构，检索随推理证据迭代剪枝 | `method/reconstruction` |
| [Learning What Not to Forget](https://arxiv.org/abs/2606.20954) | 06-18 | 数 KB 免 LLM 评分器学习识别承重历史并逐字保留，峰值上下文最多降 52% | `method/eviction` |
| [Temporal Order Matters](https://arxiv.org/abs/2606.04555) | 06-03 | 时序线段树组织对话历史（在线右端插入 + 相关性传播检索），优于平铺/图结构 | `method/temporal` |
| [RAMPART](https://arxiv.org/abs/2606.04628) | 06-03 | 编译期内存注册表五原语（promote/gate/write/evict/rollback）零 prompt token 组装上下文；关键块位置悬崖约第 7/12 块 | `method/registry` |
| [DeltaMem](https://arxiv.org/abs/2606.03083) | 06-02 | 以"残差经验"把新经验存为增量 delta 节点、组织成任务技能与环境知识两棵残差树 | `method/incremental` |
| [InfoMem](https://arxiv.org/abs/2606.03329) | 06-02 | 以"最终记忆提升正确答案对数似然"的信息增益为奖励训练分块记忆 agent | `method/rl-reward` |
| [Mandol](https://arxiv.org/abs/2606.29778) | 06-29 | 把碎片化向量/图库聚合为统一记忆原生架构：基础层 + 抽象层语义图，控延迟与 token 预算 | `method/unified` |
| [Neural Procedural Memory](https://arxiv.org/abs/2606.29824) | 06-29 | 把历史对比经验蒸馏为激活空间转向向量，免训练隐式程序记忆，弥合文本-动作脱节 | `method/activation` |
| [DuoMem](https://arxiv.org/abs/2606.29961) | 06-29 | 双空间蒸馏：上下文注入教师程序记忆 + LoRA 参数微调，4B 学生在 ALFWorld 大幅提升 | `method/on-device` |
| [Agent Memory (系统表征)](https://arxiv.org/abs/2606.06448) | 06-04 | 首个 agent 记忆系统级表征：四轴分类学 + 分阶段 profiling harness，实测十系统读写路径成本迁移 | `system/memory` |
| [Are We Ready For An Agent-Native Memory System?](https://arxiv.org/abs/2606.24775) | 06-23 | 数据管理视角拆解 agent 记忆四模块的系统级实验：成本、架构与动态更新鲁棒性 | `system/memory` |
| [AutoMEM](https://arxiv.org/abs/2606.04315) | 06-03 | 五场景横评八个记忆系统：agent 以工具调用自管文本文件的 harness 跨任务排名最佳 | `eval/memory` |
| [Always-On Agents (综述)](https://arxiv.org/abs/2606.30306) | 06-29 | 常驻 agent 综述（435 篇编码）：六轴 + 生命周期分析持久状态，治理与恢复远少于积累检索 | `survey` `memory/persistence` |
| [Rosetta Memory](https://arxiv.org/abs/2606.07711) | 06-05 | 面向跨 LLM 记忆：A 模型写 B 模型读成常态，从"LLM 中心"转"记忆中心的 LLM 适应" | `method/cross-model` |
| [Manufactured Confidence](https://arxiv.org/abs/2606.29279) | 06-28 | 记忆固化把随口 hedge 写成自信事实，agent 如验证事实般服从并放行越权请求 | `agent/safety` `memory/consolidation` |
| [Memory Contagion](https://arxiv.org/abs/2606.23195) | 06-22 | 偏评者引导的轨迹入库后，即使完美整合偏见仍传播给未来检索智能体 | `agent/safety` `study/bias` |

---

## 三、工具使用与 Function Calling（Tool Use）

> 工具选择/调用/创建、可靠性、RL 训练；MCP 专属论文见下一节。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Constraint Tax](https://arxiv.org/abs/2606.25605) | 06-24 | 同时启用工具调用与 JSON Schema 时多款开源模型停止调工具：语法掩码令调用 token 不可达 | `study/constraints` |
| [When the Tool Decides](https://arxiv.org/abs/2606.14476) | 06-12 | agent 对 GNN 工具 97.6-99.2% 盲从成"鹦鹉"，更强底座反而更盲从，绕过自身推理 | `study/over-reliance` |
| [Looking Is Not Picking](https://arxiv.org/abs/2606.16364) | 06-15 | BFCL 失败中模型 80% 注意力已落在正确工具：错在决策读出而非拥挤 harness | `study/interp` |
| [HyperTool](https://arxiv.org/abs/2606.13663) | 06-11 | 单次调用以代码块组合多工具并本地传值，折叠确定性子流程，缓解执行粒度错配 | `method/granularity` |
| [ToolChoiceConfusion (CMTF)](https://arxiv.org/abs/2606.06284) | 06-04 | 因果最小工具过滤：按前置-效果契约只暴露下一步最小工具前沿，治大菜单误选与过早调用 | `method/filtering` |
| [Self-Reflective APIs](https://arxiv.org/abs/2606.05037) | 06-03 | 校验失败返回结构化 recovery 建议而非冗长文本：任务完成率升 36.7-40pp，token 效率高 1.8-2.2 倍 | `method/api-design` |
| [Contract2Tool](https://arxiv.org/abs/2606.07904) | 06-05 | 从元数据/schema/文档/执行轨迹自动推断工具前置-效果-风险契约，替代手写维护 | `method/contract` |
| [SING](https://arxiv.org/abs/2606.16591) | 06-15 | 意图-工具图支持主动工具发现，摆脱封闭世界静态工具清单假设 | `method/discovery` |
| [Scaling Enterprise Agent Routing](https://arxiv.org/abs/2606.17519) | 06-16 | 110 agent/584 工具下欠定请求路由 F1 掉 16-23pp；嵌入短列恢复 +10-17pp | `study/enterprise` |
| [MetaForge](https://arxiv.org/abs/2606.01801) | 06-01 | Decide-Retrieve-Adapt-Forge-Recycle 闭环：学会何时用工具并在线锻造回收新工具 | `method/tool-creation` |
| [Learning When Not to Act (EAPO)](https://arxiv.org/abs/2606.02132) | 06-01 | 无工具轨迹 + 难度感知奖励抑制冗余工具调用，较 GRPO 平均提升 10.45%（3B 模型） | `method/rl` |
| [ToolGate](https://arxiv.org/abs/2606.03054) | 06-02 | 预调用控制器决定执行/跳过工具调用，token 成本降至 64-69% 且精度持平 | `method/efficiency` |
| [Don't Blindly Trust It](https://arxiv.org/abs/2606.21409) | 06-19 | 持续误导工具反馈致价值反转：HotpotQA 干净 44.8 F1、乱序反馈仅 4.7 | `study/robustness` |
| [Why Multi-Step Tool-Use RL Collapses](https://arxiv.org/abs/2606.26027) | 06-24 | 多步工具 RL 崩溃源于控制 token 概率尖峰掩盖能力；交错监督信号可稳定恢复 | `method/rl` |
| [TACO](https://arxiv.org/abs/2606.30251) | 06-29 | 用探针 token 对比有无工具的答案预测，为每次调用自监督记功，免外部裁判模型 | `method/credit` |
| [ReGRPO](https://arxiv.org/abs/2606.31392) | 06-30 | 从近失动作收集失败观察构造（错误类型,证据,修复）三元组热启动，RL 联合优化反思与纠正 | `method/rl` |
| [CacheRL](https://arxiv.org/abs/2606.14179) | 06-12 | 三层模糊缓存免在线执行 + 缓存感知混合奖励：小模型工具调用 92% 过程准确率、省算 100 倍 | `method/rl` `system/cache` |

---

## 四、MCP（Model Context Protocol）

> 协议运维、治理、安全与企业采用；MCP 相关训练环境与基准。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [A Taxonomy of Runtime Faults in MCP Servers](https://arxiv.org/abs/2606.05339) | 06-03 | 首个 MCP 服务器运行时故障分类学：473 个活跃仓库 837 条故障帖，11 大类 27 子类 73 叶 | `env/mcp` `study/reliability` |
| [Description-Code Inconsistency in Real-world MCP Servers](https://arxiv.org/abs/2606.04769) | 06-03 | 首个"描述-代码不一致"实证：给出功能不一致与未声明副作用的分类学并研发检测器 | `env/mcp` `agent/safety` |
| [Understanding How Enterprises Adopt MCP](https://arxiv.org/abs/2606.09182) | 06-08 | 访谈 8 公司 20 位从业者：MCP 支撑跨系统协作与知识复用，生态碎片化制约采用 | `study/enterprise` `env/mcp` |
| [Governance Gaps in Agent Interoperability Protocols](https://arxiv.org/abs/2606.31498) | 06-30 | 六维治理需求审计 MCP/A2A/ACP：投票与异议保留普遍缺失，只支撑任务协调非治理 | `env/mcp` `study/governance` |
| [MCP Server Architecture Patterns](https://arxiv.org/abs/2606.30317) | 06-29 | 基于 15 个生产 MCP 服务器归纳五种架构模式：资源网关、工具编排器、有状态会话等 | `env/mcp` `method/patterns` |
| [From Tool Connection to Execution Control](https://arxiv.org/abs/2606.29073) | 06-27 | 定义元数据非权威、授权背书审批等八项执行层安全不变量，以 HCP 参考运行时实现 | `env/mcp` `agent/safety` |
| [ShareLock](https://arxiv.org/abs/2606.27027) | 06-25 | Shamir 门限把恶意指令分散进多个 MCP 工具：单查无害、聚合才触发，抗人工与自动检测 | `env/mcp` `attack/threshold` |
| [VATS](https://arxiv.org/abs/2606.07992) | 06-06 | 错误路径注入：工具报错自带隐式权威，突变进化载荷使攻击成功率至多 100%、三倍于普通间接注入 | `env/mcp` `attack/error-path` |
| [WebMCP Tool Surface Poisoning](https://arxiv.org/abs/2606.06387) | 06-04 | 第三方脚本在活跃会话注入恶意工具（MSTI），分工具劫持与工具构陷两类 | `env/mcp` `attack/poisoning` |
| [Privacy Leakage Risks in MCP Servers](https://arxiv.org/abs/2606.21338) | 06-19 | 跨语言静态分析检测 MCP 服务器协议诱发泄露：凭据/PII 过本地-LLM 边界即泄 | `env/mcp` `agent/safety` |
| [ProvenanceGuard](https://arxiv.org/abs/2606.18037) | 06-16 | 按 MCP 轨迹把原子声明路由回来源核验归属，阻断跨源混淆并可修复 | `env/mcp` `method/provenance` |
| [Queen-Bee Agents](https://arxiv.org/abs/2606.06545) | 06-04 | Queen 控制面检索能力并编译 BeeSpec，Bee agents 受限工具访问执行：企业级 MCP 治理 | `env/mcp` `method/orchestration` |
| [SafeMCP](https://arxiv.org/abs/2606.01991) | 06-01 | 服务端防御插件：世界模型前瞻推理过滤危险工具并即时干预，遏制权力扩张 | `env/mcp` `agent/safety` |
| [MCP-Persona](https://arxiv.org/abs/2606.02470) | 06-01 | 首个面向 Reddit/小红书/飞书等真实个性化 MCP 工具的智能体基准 | `env/mcp` `eval/mcp` |
| [Synthesize and Reward](https://arxiv.org/abs/2606.03892) | 06-02 | 20 个有状态 MCP 服务器/343 工具支撑真实执行 RL，状态机合成接地服务器实态的查询 | `env/mcp` `method/rl` |
| [BioinfoMCP](https://arxiv.org/abs/2606.04494) | 06-03 | 编译器把异构生信软件标准化为 MCP 服务器并组建类型化 MCP 图，图规划替代扁平工具描述 | `env/mcp` `env/bio` |

---

## 五、Skills（技能）

> 技能的生成/进化/组合/参数化/审计；skill 安全见安全维度。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [SkillComposer](https://arxiv.org/abs/2606.06079) | 06-04 | 把技能构造分解为 create/improve/merge 三个可学习算子，推理时自进化技能库 | `method/skill` |
| [LatentSkill](https://arxiv.org/abs/2606.06087) | 06-04 | 超网络把文本技能转即插 LoRA：技能存权重空间，ALFWorld +21.4 分且省 64.1% prefill | `method/parametric` |
| [Skill-to-LoRA](https://arxiv.org/abs/2606.16769) | 06-15 | SKILL.md 不再重复注入上下文：离线合成示范训练技能 LoRA，在线加载即用 | `method/parametric` |
| [Parametric Skills](https://arxiv.org/abs/2606.30015) | 06-29 | 测试时把文本技能转为模型参数，实现无上下文技能调用，突破长上下文指令遵循瓶颈 | `method/parametric` |
| [SoftSkill](https://arxiv.org/abs/2606.20333) | 06-18 | 把 Markdown 技能初始化为可训练 soft prefix（底座冻结），LiveMath +42.1 分 | `method/parametric` |
| [SkillDAG](https://arxiv.org/abs/2606.03056) | 06-02 | 类型化有向图建模技能依赖/冲突并支持执行中注册新边，ALFWorld 等达 67.1% | `method/skill-graph` |
| [Generative Skill Composition](https://arxiv.org/abs/2606.32025) | 06-30 | 把技能组合形式化为"选哪些/多少/什么顺序"的联合结构决策，超越全量暴露与检索 | `method/composition` |
| [Hierarchical Accumulation of Skills](https://arxiv.org/abs/2606.30911) | 06-29 | 三级技能分层：同 159 技能下分层加载 100% vs 平铺 62.5%，MLE-Bench Lite 达 77.3% | `method/tiers` |
| [A Single Rewrite Suffices](https://arxiv.org/abs/2606.30775) | 06-29 | 自动优化技能描述一次重写匹敌人工（79.2% vs 79.4% F1），单技能工时 120→3.8 分钟 | `env/production` |
| [Not All Skills Help](https://arxiv.org/abs/2606.15390) | 06-13 | 随机掩蔽测单技能因果贡献：技能库普遍"此长彼消"；ASSAY 分离技能生成与策展并按任务重排 | `eval/skill` |
| [SkillAudit](https://arxiv.org/abs/2606.14239) | 06-12 | 无真值技能进化：同任务有无技能成对执行隔离行为差异，对比评估转为编辑指导迭代技能 | `method/audit` |
| [SkillCAT](https://arxiv.org/abs/2606.13317) | 06-11 | 同任务成败轨迹对比提取因果证据、克隆回放过滤有害补丁、按需加载，三阶段技能自进化 | `method/contrastive` |
| [SkillAxe](https://arxiv.org/abs/2606.10546) | 06-09 | LLM 写技能几乎无增益（人类技能 +16.2pp）；SkillAxe 无监督自精修补 47-67% 差距 | `method/self-refine` |
| [SkillJuror](https://arxiv.org/abs/2606.11543) | 06-10 | Progressive Disclosure 先改运行时行为：资源触达 1.18→3.85，410 匹配试验 +4.1% | `eval/skill` |
| [Skill Coverage](https://arxiv.org/abs/2606.20659) | 06-09 | 技能测试充分性指标：技能指令转半结构化行为约束，判定哪些部分被行使 | `eval/skill` |
| [Hypothesis-Driven Skill Optimization](https://arxiv.org/abs/2606.22330) | 06-21 | 策展人提可证伪假设 + 配对对照执行验证，仅并入受支持技能包防伪捷径入库 | `method/validation` |
| [Workflow-to-Skill](https://arxiv.org/abs/2606.06893) | 06-05 | 从异构轨迹自动造技能：RWSA 中间表示分解工作流/语义/附件，捕获验证、回滚与安全关键行为 | `method/auto-gen` |
| [MMG2Skill](https://arxiv.org/abs/2606.01993) | 06-01 | 把野外多模态指南编译为可编辑技能并从轨迹修订，附首个"指南转技能"基准 | `method/multimodal` |
| [FederatedSkill](https://arxiv.org/abs/2606.03143) | 06-02 | 以语义技能差分为通信单元的联邦技能演化，兼顾隐私与个性化，突破单用户任务流瓶颈 | `method/federated` |
| [Inducing Reasoning Primitives from Agent Traces](https://arxiv.org/abs/2606.02994) | 06-02 | 单遍挖掘 ReAct 轨迹聚成类型化伪工具库，库反超生成它的智能体（RuleArena NBA +44pp） | `method/induction` |
| [UCOB](https://arxiv.org/abs/2606.29502) | 06-28 | 把有/无技能提示视为同模型两个视图，按 return-to-go 选局部教师，纠正误导技能并更新记忆 | `method/rl` |
| [OPID](https://arxiv.org/abs/2606.26790) | 06-25 | 从自身 on-policy 轨迹提取 episode/step 级层级技能作稠密监督，免维护外部技能库 | `method/distill` |
| [Bayesian-Agent](https://arxiv.org/abs/2606.08348) | 06-06 | 把可复用技能当贝叶斯证据对象：维护技能可靠性与失败模式后验，替代原始成功率更新 | `method/bayesian` |
| [What Should a Skill Remember?](https://arxiv.org/abs/2606.09421) | 06-08 | 技能重写非越短越省：API/工作流/规则锚定各有所长，学习策略选择重写模板 | `method/compression` |
| [Are Online Skill and Memory Modules Always Worth Their Tokens?](https://arxiv.org/abs/2606.15017) | 06-12 | 等 token 预算下，把预算花在更多 actor 步数的朴素基线追平 AWM/ASI/ReasoningBank 三种增强 | `eval/negative-result` |
| [Agent Skill Evaluation and Evolution (综述)](https://arxiv.org/abs/2606.11435) | 06-09 | 综述技能评测与进化：执行反馈/轨迹蒸馏/压缩/RL 四范式 + 六类基准缺口 | `survey` `eval/skill` |

---

## 六、Sub-agent 与编排（Sub-agents & Orchestration）

> 子代理委派、编排器训练、递归 harness、agent 团队管理力。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Recursive Agent Harnesses](https://arxiv.org/abs/2606.13643) | 06-11 | 命名并研究递归 agent harness：父 agent 写脚本并行孵化子 harness，GPT-5 底座受控评测 | `agent/harness` `method/recursion` |
| [ClawArena-Team](https://arxiv.org/abs/2606.31174) | 06-30 | 41 个多轮场景专测主 agent 管理力：创建子 agent、并行异步编排，与其自身解题力剥离 | `eval/orchestration` |
| [Sakana Fugu Technical Report](https://arxiv.org/abs/2606.21228) | 06-19 | 编排器模型本身即 LM：动态生成 agentic scaffolds 放大智能体团队，多基准领先 | `model/orchestrator` |
| [SearchSwarm](https://arxiv.org/abs/2606.09730) | 06-08 | 训练委托智能：合成数据教主 agent 分解任务、择机委派子 agent 并整合摘要 | `agent/deep-research` |
| [EARS](https://arxiv.org/abs/2606.18668) | 06-17 | 把子 agent 弃答重构为 agent 间通信协议：说明原因并请求重路由 | `method/abstention` |
| [Reward Modeling for Multi-Agent Orchestration](https://arxiv.org/abs/2606.13598) | 06-11 | 从多 agent 执行中间工件自监督构造胜负对训练编排奖励模型，token 省 10 倍 | `method/reward-model` |
| [HALO](https://arxiv.org/abs/2606.21740) | 06-19 | 用验证器认证的成功轨迹 QLoRA 训练编排器，替代每步调用前沿 LLM | `method/sft` |
| [SciOrch](https://arxiv.org/abs/2606.15872) | 06-14 | 训练 8B 编排器分解问题分派商用模型再综合：MCTS 离线构数规避昂贵在线 rollout | `env/science` |
| [Orchestra-o1](https://arxiv.org/abs/2606.13707) | 06-10 | 全模态 agent 编排框架：模态感知任务分解与在线协作，统一调度文/图/音/视频异构输入 | `method/omnimodal` |
| [PerspectiveGap](https://arxiv.org/abs/2606.08878) | 06-07 | 编排提示基准：110 场景 10 拓扑，33 商用模型测子 agent 上下文分配 | `eval/orchestration` |

---

## 七、Prompt / Context / Harness / Loop 工程

> harness 定义与实证、上下文压缩与管理、prompt 优化、AgentOps 与运行时、服务系统。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Scaffold Effects on GAIA](https://arxiv.org/abs/2606.08529) | 06-07 | 预注册对照：脚手架选择可使同模型 GAIA 差 28 个百分点，强模型并不更免疫 | `study/harness` |
| [What makes a harness a harness](https://arxiv.org/abs/2606.10106) | 06-08 | 给 agent harness 立充要判据式参考定义，区分产品/评测脚手架/框架混用 | `agent/harness` |
| [HarnessFix](https://arxiv.org/abs/2606.06324) | 06-04 | 从失败轨迹定位 harness 缺陷：trace 编译为 HTIR 中间表示，诊断驱动精准修复而非泛改 | `agent/harness` `method/repair` |
| [LLM-as-Code](https://arxiv.org/abs/2606.15874) | 06-14 | 程序掌管全部控制流，LLM 退为被调用的推理/生成组件：上下文由执行调用树构建 | `agent/harness` `method/architecture` |
| [LemonHarness](https://arxiv.org/abs/2606.24311) | 06-23 | 为长程 agent 划定显式执行边界：状态变更收进受控工作区，模型调用与规则知识同界管理 | `agent/harness` |
| [Maestro Order](https://arxiv.org/abs/2606.23983) | 06-22 | 分解/集成/验证/递归四基元 + 预算感知控制器，把不可靠求解器组合成可靠系统 | `agent/harness` |
| [HarnessForge](https://arxiv.org/abs/2606.01779) | 06-01 | 把智能体系统形式化为 harness-策略对，显式划分适应空间并联合进化结构与推理 | `method/co-evolution` |
| [The Interplay of Harness Design and Post-Training](https://arxiv.org/abs/2606.25447) | 06-24 | harness 当可控设计维度：harness 感知后训练在分布内外都优于固定脚手架，环境迁移更稳 | `study/harness` |
| [MUSE](https://arxiv.org/abs/2606.03005) | 06-02 | 冻结 MLLM 仅靠可组合执行 harness（视觉处理、确定性验证、引导修复）显著提能 | `agent/harness` `env/multimodal` |
| [Agent libOS](https://arxiv.org/abs/2606.03895) | 06-02 | libOS 式 AgentProcess 运行时承载记忆/技能/工具/子进程：能力可演化而权限仅经显式审计变更 | `system/runtime` |
| [Agent Operating Systems (AOS)](https://arxiv.org/abs/2606.01508) | 06-01 | 把智能体控制平面融入传统操作系统，应对调度、状态与安全治理边界 | `system/runtime` `position` |
| [Agent System Operations (综述)](https://arxiv.org/abs/2606.01581) | 06-01 | AgentOps 综述：建立异常分类框架、定义挑战，填补运维研究空白 | `survey` `system/agentops` |
| [Monitoring Agentic Systems Before They're Reliable](https://arxiv.org/abs/2606.02494) | 06-01 | 监控分诊：质量/适宜/效率三维 × 三种监控范围，以方差信号在 220 次运行中定位结构性缺陷 | `system/monitoring` |
| [Token Budgets](https://arxiv.org/abs/2606.04056) | 06-02 | 21 个编排框架 63 起 token 超支事故的八类失败目录，Rust 仿射类型库在类型层防双花/超支 | `system/reliability` |
| [The Entropy Principle of Silent Failure](https://arxiv.org/abs/2606.08162) | 06-06 | 无外部触发的 agent 静默失败熵原理：4 万+ 受控试验归纳六生命周期层 22 个内生属性 | `study/reliability` |
| [When Errors Become Narratives](https://arxiv.org/abs/2606.14589) | 06-12 | 生产个人助理 8 周 22 起静默故障复盘：错误信号从未以可行动形式触达人类的五类分类学 | `study/postmortem` |
| [ACE](https://arxiv.org/abs/2606.31564) | 06-30 | 无损保存原始 + 压缩抽象双轨，按决策步弹性编排历史信息，突破截断/摘要不可逆限制 | `method/context` |
| [Self-Compacting Language Model Agents](https://arxiv.org/abs/2606.23525) | 06-22 | 模型自决何时压缩：压缩工具 + 触发/抑制量规（子任务收敛触发、推导中抑制）缺一不可 | `method/compaction` |
| [TokenPilot](https://arxiv.org/abs/2606.17016) | 06-15 | 全局摄入感知压缩 + 局部生命周期感知驱逐，稳住前缀保 prompt 缓存连续性 | `method/cache` |
| [PACMS](https://arxiv.org/abs/2606.20047) | 06-18 | 次模上下文选取引擎替代话题盲的近因截断，多源上下文按预算保相关 | `method/selection` |
| [Entropy Gate](https://arxiv.org/abs/2606.03739) | 06-02 | 按多因子信息能量给 token 打分、自适应淬火删除低信息 token 并以保真门止损 | `method/compression` |
| [VISTA](https://arxiv.org/abs/2606.30005) | 06-29 | 让模型感知自身上下文状态（块大小/剩余预算）：工作记忆可寻址、归档可保真恢复 | `method/self-manage` |
| [Plans Don't Persist](https://arxiv.org/abs/2606.22953) | 06-22 | replay pairing：计划信号一步内衰减 4.1 倍，agent 不持久携带计划全靠留在上下文 | `study/context` |
| [Less Context, Better Agents](https://arxiv.org/abs/2606.10209) | 06-08 | MCP 工具响应压缩实证：留最近 5 对调用 + 摘要化，省 token 且优于全量历史 | `env/mcp` `method/compression` |
| [Semantic Early-Stopping](https://arxiv.org/abs/2606.27009) | 06-25 | 语义早停替代固定迭代上限：草稿嵌入语义收敛 + 质量停增即停，省 token 免硬截断 | `method/loop` |
| [Instruction Bleed](https://arxiv.org/abs/2606.26356) | 06-24 | 形式化提示模块间行为泄漏：非焦点模块内容扰动产生显著效应（Cohen's d=0.63），标准 QA 测不出 | `study/prompt` |
| [Contrastive Reflection for Iterative Prompt Optimization](https://arxiv.org/abs/2606.30840) | 06-29 | 错误锚定行为切片 + 近邻成功对照，像调试一样改 agentic IR 工作流提示 | `method/prompt-opt` |
| [Knowing When to Ask](https://arxiv.org/abs/2606.11349) | 06-09 | 澄清提问入动作空间与行动同序竞争：强制型/机会型两模式涌现 | `method/clarification` |
| [Uncertainty-Aware Clarification](https://arxiv.org/abs/2606.03135) | 06-02 | 用信息增益奖励训练澄清提问，有效消解用户意图不确定性，跨 5 个骨干验证 | `method/clarification` |
| [GRADE](https://arxiv.org/abs/2606.22741) | 06-22 | 把运行建成执行边 + 依赖边双层图：依赖层可预测失败，执行层定位多智能体故障步 | `method/observability` |
| [XFlow](https://arxiv.org/abs/2606.14790) | 06-11 | XPF 协议语言可读可编译：把该硬化的工作流承诺从 prompt 移入可校验执行的 harness 结构 | `method/dsl` |
| [Dissecting model behavior through agent trajectories](https://arxiv.org/abs/2606.17454) | 06-16 | 定义模型意图与 harness 执行间的 intent-execution 差距并构建通用 harness SSA | `study/harness` |
| [Watts and Debits of Agentic Frameworks](https://arxiv.org/abs/2606.10702) | 06-09 | 注册报告：五个开源 agent 框架的自认技术债与运行时能耗相关性实证 | `study/frameworks` |
| [The Token Not Taken](https://arxiv.org/abs/2606.08998) | 06-08 | 剖析 agent 跨运行变异性：token 采样差异级联成不同工具调用与代码路径 | `study/reliability` |
| [Building Customer Support Agents at 100M-User Scale](https://arxiv.org/abs/2606.08867) | 06-07 | 1 亿用户客服 agent 框架：结构化上下文工程 + HITL 提示迭代 + LLM judge + GEPA 贯通离线在线 | `env/production` |
| [Characterizing LLM Agentic Workflows (N8n)](https://arxiv.org/abs/2606.29116) | 06-27 | 首个低代码平台大规模实证：6000+ 个 n8n 工作流分析任务分布、工具模式与可靠性机制 | `study/workflow` |
| [Agentic Publication Protocol](https://arxiv.org/abs/2606.27386) | 06-15 | 仓库即出版对象：AGENTS.md + 技能打包成 agent 可解释、可复现的论文格式 | `agent/harness` `env/science` |
| [Observation, Not Prediction](https://arxiv.org/abs/2606.01839) | 06-01 | 以会话为调度单元把智能体负载转为两阶段稳定结构，用观测替代预测做调度决策 | `system/serving` |
| [GAIATrace](https://arxiv.org/abs/2606.01725) | 06-01 | 发布 GAIA 首个 token 级轨迹数据集与模拟器 Vidur-Agent，支撑可复现低成本系统研究 | `system/simulation` |

---

## 八、AI Coding Agent

> 方法、交互、经验研究（PR/落地/配置）、代码 Agent 训练数据；SWE 基准见评测维度。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [Building to the Test](https://arxiv.org/abs/2606.28430) | 06-26 | 隐藏 222 测 oracle 在环得分近满分但库留死代码：coding agent 交付你检验的而非你要求的 | `study/validity` |
| [Detecting AI Coding Agents in Open Source](https://arxiv.org/abs/2606.24429) | 06-23 | 1.8 亿仓库多方法检测出 85.0 万 Claude Code 提交，bot 信号仅回收 3.3%，单信号估计低 30 倍 | `study/oss` |
| [All Smoke, No Alarm](https://arxiv.org/abs/2606.18168) | 06-16 | 3.4 万 agent PR 的 8.6 万测试补丁实证：缺断言常见，按测试文件数把关高估验证 | `study/testing` |
| [Understanding the Rejection of Fixes (AIDev)](https://arxiv.org/abs/2606.13468) | 06-11 | agentic 修复 PR 46.41% 被拒；306 例定性出 14 类拒绝原因分四大类 | `study/oss` |
| [Toward Instructions-as-Code](https://arxiv.org/abs/2606.13449) | 06-11 | AIDev 15,549 个 agentic PR 前后对照：instruction 文件与合并率/代码复杂度/合并时耗关联 | `study/agents-md` |
| [Beyond Simpson's Paradox](https://arxiv.org/abs/2606.22711) | 06-21 | 33,596 个 AI PR：人机共著合并率更低是辛普森悖论，分层后 Copilot/Devin 反更高 | `study/oss` |
| [Agentic Very Much!](https://arxiv.org/abs/2606.07448) | 06-05 | 新建 GitHub 项目 coding agent 采纳率较此前研究翻倍以上，AI 辅助 commit 占比显著更高 | `study/adoption` |
| [Pomona (Bloomberg)](https://arxiv.org/abs/2606.06752) | 06-04 | 扫描+修复双技能持续小步 PR：82.1%（32/39）PR 被合并、中位关闭仅 2 小时 | `env/production` |
| [TraceLab](https://arxiv.org/abs/2606.30560) | 06-29 | 4300 个 Claude Code/Codex 会话（35 万步/43 万工具调用）：长自主循环、短输出、高前缀缓存命中 | `study/production` |
| [CacheWise](https://arxiv.org/abs/2606.16824) | 06-15 | coding agent 会话大量复用前缀；工具元数据预测驱逐减少逐出 2-2.6 倍 | `system/serving` |
| [Configuration Smells in AGENTS.md](https://arxiv.org/abs/2606.15828) | 06-14 | 首个 AGENTS.md/CLAUDE.md 配置坏味目录：六类坏味 + 自动启发式，100 个热门仓库分析 | `study/agents-md` |
| [Probe-and-Refine Tuning of Repository Guidance](https://arxiv.org/abs/2606.20512) | 06-18 | 用合成 bug 修复探针迭代修补仓库指导文件（AGENTS.md 类），单次 LLM 调用即可调优 | `method/agents-md` |
| [Code Isn't Memory](https://arxiv.org/abs/2606.22417) | 06-21 | 固定 harness 三臂对照：结构化代码索引带来显著定位与解决率增益且不增成本 | `study/context` |
| [Dockerless](https://arxiv.org/abs/2606.28436) | 06-26 | 免执行 agentic 补丁验证器靠仓库探索取证判对错：超最强开源验证器 14.3 AUC | `method/verifier` |
| [The Verification Horizon](https://arxiv.org/abs/2606.26300) | 06-24 | 刻画验证信号可扩展/忠实等三维度：每个验证器都只是人类意图的代理，无银弹 | `study/reward` |
| [Loc2Repair](https://arxiv.org/abs/2606.30963) | 06-29 | 解耦定位与修复的评测框架：显式文件定位稳定提升 SWE-bench Verified 解决率 | `method/localization` |
| [SHERLOC](https://arxiv.org/abs/2606.24820) | 06-23 | 假设驱动定位免微调：SWE-Bench Lite 定位 acc@1 84.33%，注入修复 agent 平均 +5.95pp | `method/localization` |
| [Steer, Don't Solve](https://arxiv.org/abs/2606.21811) | 06-20 | 小 critic 轨迹内转向大 code agent：跨未见 agent +3.0~3.8 分，成本仅教师 1/30-1/92 | `method/critic` |
| [Tmax](https://arxiv.org/abs/2606.23321) | 06-22 | 开源 RL 配方：难度控制 + 人格 + 验证器多样化造数，9B 模型 Terminal-Bench 2.0 达 27% | `method/rl` `env/terminal` |
| [CLI-Universe](https://arxiv.org/abs/2606.22883) | 06-22 | 按能力分类学 + 证据引导深研合成终端任务，Docker 化多阶段验证产可靠监督 | `method/data-gen` `env/terminal` |
| [Open-SWE-Traces](https://arxiv.org/abs/2606.16038) | 06-14 | 2 万真实 PR 合成 20.7 万条九语言双模轨迹，微调后 SWE-bench Verified 61.7% | `method/sft` |
| [DeNovoSWE](https://arxiv.org/abs/2606.10728) | 06-09 | 4818 例整仓库生成数据集：沙箱化 agent 工作流自动构造，分治 + 批评修复 | `method/data-gen` |
| [FastContext](https://arxiv.org/abs/2606.14066) | 06-12 | 专用探索子代理按需并行检索只回路径+行号；4B-30B 探索模型经轨迹自举 + 任务奖励精调 | `method/subagent` |
| [FeatX](https://arxiv.org/abs/2606.31206) | 06-30 | 按特性而非代码编辑仓库：三阶段 Evolution Agent 译特性改动为补丁，定位 F1 相对 +42.6% | `method/feature-edit` |
| [AxDafny](https://arxiv.org/abs/2606.32007) | 06-30 | 验证器引导迭代修复实现与不变式，DafnyBench 验证成功率 92.7%、超最强基线 6.5pp | `env/verified` |
| [Agentic Hardware Design as Repository-Level Code Evolution](https://arxiv.org/abs/2606.28279) | 06-26 | Markdown harness 编译项目包，免手 agent 在隔离 git worktree 做仓库级进化：四套件 100% 完成 | `agent/harness` `env/eda` |
| [An Ocean Model Ported by an LLM (FESOM2)](https://arxiv.org/abs/2606.11356) | 06-09 | 7.4 万行海洋模式 LLM 移植保物理：两阶段翻译、严格测试、专家主导是关键 | `study/hpc` |
| [Frontier Coding Agents Use Metaprogramming](https://arxiv.org/abs/2606.10933) | 06-09 | 生僻语言上前沿 coding agent 靠元编程取胜：写 Python 生成目标语言，禁用则骤降 | `study/empirical` |
| [Do programming languages still matter?](https://arxiv.org/abs/2606.13763) | 06-11 | 两个前沿 agent 免棋类知识生成 34 个象棋引擎/17 种语言：语言选择仍塑造产物多维质量 | `study/empirical` |
| [Trust-Calibrated Code Review](https://arxiv.org/abs/2606.01969) | 06-01 | 参与式设计研究 LLM 多文件变更审查：17 人访谈 + 43 人问卷，提出信任校准 IDE 工作流 | `study/hci` |
| [The End of Code Review](https://arxiv.org/abs/2606.13175) | 06-11 | 立场文：coding agent 能力已越过阈值，人工审查不再是必需质量门 | `position` |
| [AI Coding Agents in Social Science](https://arxiv.org/abs/2606.11456) | 06-09 | 20 次独立执行分层检验：设计层多样性保真，verdict 层易被立场提示带偏 | `study/reproducibility` |
| [ESAA-Conversational](https://arxiv.org/abs/2606.23752) | 06-22 | 对话捕获为 append-only 事件流投影读模型，跨 Codex/Claude Code 共享记忆消状态漂移 | `agent/memory` `agent/coding` |
| [PROJECTMEM](https://arxiv.org/abs/2606.12329) | 06-10 | 为 coding agent 建本地事件溯源记忆层：append-only 日志投影为摘要经 MCP 服务，附前置动作防护门 | `agent/memory` `agent/coding` |

---

## 九、评测与基准（Evaluation & Benchmark）

> 评测方法论（judge/噪声/污染/可黑性）+ 新基准；SWE 与 agent 专项。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [The Capability Frontier](https://arxiv.org/abs/2606.26836) | 06-25 | 21 模型 × 16 基准：单模型单次评测漏掉 82% 可达性能，跨模型跨次采样 oracle 前沿才是上限 | `eval/methodology` |
| [How Much Coordination Gain Is Real?](https://arxiv.org/abs/2606.20695) | 06-15 | 配置等价对照测 MAS 基准噪声底：+18pp 单种子显著对比第二种子不复现 | `eval/methodology` |
| [RoPoLL](https://arxiv.org/abs/2606.30931) | 06-29 | 证明评审团共识在单评审有偏失效时偏差无界；换几何中位数聚合，崩溃点 1/2 | `eval/llm-judge` |
| [Temperature Control and Reproducibility](https://arxiv.org/abs/2606.26185) | 06-24 | 评测 harness 默认温度致边界样本 20 轮翻转近 50%；温度 0 下仍有 1-2/7 项不可复现 | `eval/methodology` |
| [GroundEval](https://arxiv.org/abs/2606.22737) | 06-22 | 免评审确定性评估轨迹证据：LLM 评 0.85 的回答实未取所依赖工件（得分 0.000） | `eval/methodology` |
| [Search-Time Contamination](https://arxiv.org/abs/2606.05241) | 06-03 | 定义并量化 deep research 的"搜索时污染"：检索到基准元数据致六个基准性能虚高至多 4% | `eval/contamination` |
| [Auditing Reward Hackability](https://arxiv.org/abs/2606.16062) | 06-14 | SWE-bench Verified 49 题抽样 28.5% 可被错误补丁骗过；可黑任务 Pass@1 高 14.14pp | `eval/reward-hacking` |
| [Hardening Agent Benchmarks](https://arxiv.org/abs/2606.08960) | 06-08 | 审计 1968 个终端 agent 任务、16% 可被 hack；hacker-fixer 循环自动加固验证器 | `eval/methodology` |
| [From Confident Closing to Silent Failure](https://arxiv.org/abs/2606.09863) | 06-01 | 假成功实证：tau2-bench 45-48% 失败为假成功、AppWorld 达 75.8%，LLM 裁判 AUROC ≤0.65 | `eval/failure` |
| [When Agents Commit Too Soon](https://arxiv.org/abs/2606.22936) | 06-22 | 第 4 步隐状态相似度预测轨迹一致性（r=-0.35）；过早承诺不区分对错只预示坍缩 | `eval/diagnostic` |
| [Do More Agents Help?](https://arxiv.org/abs/2606.05670) | 06-04 | 统一协议实测：六种 MAS 至多一种超匹配的单 agent 锚点，其余五种落后 2.56-11.29 分且更贵 | `eval/multiagent` |
| [WorkBench Revisited](https://arxiv.org/abs/2606.13715) | 06-10 | 两年重测 WorkBench：最佳完成率 43%→98%，无意伤害 26%→1.9%，能力与安全同升 | `eval/longitudinal` |
| [Predictive Validity for LLM Agents](https://arxiv.org/abs/2606.19704) | 06-18 | 聚合 14 项 MCP 工业基准深研：总分排名不迁移 OOD，应以预测效度排序 | `eval/methodology` |
| [Agentic Abstention](https://arxiv.org/abs/2606.28733) | 06-27 | 定义 agent 弃权为序贯决策问题，跨购物/终端/问答评估 13 个系统的停止判断能力 | `eval/abstention` |
| [MemDelta](https://arxiv.org/abs/2606.29914) | 06-29 | 受控评测揭示记忆评估混杂：仅换嵌入模型精度变 +6.2pp，RAG 与全上下文排名随模型反转 | `eval/memory` |
| [Counsel](https://arxiv.org/abs/2606.21627) | 06-19 | 首个 agentic 元评估集：tau-bench/DA-Code 过程级 LLM 评审批评 + 人工复核标签 | `eval/llm-judge` |
| [BabelJudge](https://arxiv.org/abs/2606.22329) | 06-21 | 受控退化构造金标签免人工标注：审计位置/冗长/顺序/跨语四种评审失效 | `eval/llm-judge` |
| [Catching One in Five](https://arxiv.org/abs/2606.10315) | 06-09 | 生产多轮 agent 的 judge 仅抓 2/9 缺陷模式、100 轮零告警而人工确认 23 项缺陷 | `eval/llm-judge` |
| [Benchmark Everything Everywhere All at Once](https://arxiv.org/abs/2606.06462) | 06-04 | Benchmark Agent 全自动建基准：查询分析、子任务设计到标注质控端到端，已产出 15 个基准 | `eval/automation` |
| [AgentBeats](https://arxiv.org/abs/2606.13608) | 06-11 | 评测本身 agent 化：judge agent + A2A/MCP 标准协议统一接口，分离评测逻辑与 agent 实现 | `eval/automation` |
| [Layer-Isolated Evaluation](https://arxiv.org/abs/2606.11686) | 06-10 | 无 LLM 分层回归测试：238 用例 2.39 秒；单层退化总分仅微动而对应切片崩 25-91pp | `eval/methodology` |
| [OSWorld 2.0](https://arxiv.org/abs/2606.29537) | 06-28 | 108 个真实长程工作流：人类中位 1.6 小时、Claude 需均 318 次工具调用（1.0 版仅约 30 次） | `eval/computer-use` |
| [MacAgentBench](https://arxiv.org/abs/2606.22557) | 06-21 | 25 应用 676 任务真机 macOS 基准：近 60% 混 GUI+CLI，多检查点细粒度计分 | `eval/computer-use` |
| [Workflow-GYM](https://arxiv.org/abs/2606.11042) | 06-09 | 专业软件长程 GUI 任务基准：端到端完成高价值工作流，最强模型仍吃力 | `eval/computer-use` |
| [TUA-Bench](https://arxiv.org/abs/2606.28480) | 06-26 | 120 个真实任务评通用终端 agent：文档、邮件、live-web 检索与博士级科研工作流 | `eval/terminal` |
| [PlanBench-XL](https://arxiv.org/abs/2606.22388) | 06-21 | 327 零售任务/1,665 工具的检索受限规划基准，GPT-5.4 也仅 51.90%，含故障工具机制 | `eval/planning` |
| [ToolMaze](https://arxiv.org/abs/2606.05806) | 06-04 | 工具失败基准：显/隐 × 暂/永 2×2 扰动分类，隐式语义失败下扰动恢复率暴跌约 37% | `eval/tool` |
| [EvoBrowseComp](https://arxiv.org/abs/2606.13120) | 06-11 | 三 agent 协作活网遍历合成 800 题演化基准（中英各 400），抗污染抗参数记忆 | `eval/deep-research` |
| [Where Do Deep-Research Agents Go Wrong?](https://arxiv.org/abs/2606.02060) | 06-01 | 标注 2790 条轨迹构建千例 TELBench 定位错误 span，DRIFT 以声明为中心审计证据支撑 | `eval/deep-research` |
| [LakeQA](https://arxiv.org/abs/2606.10460) | 06-09 | 9.5TB 数据湖搜索式问答基准：PhD 标注，联合考察搜索与推理 | `eval/data` |
| [EnterpriseClawBench](https://arxiv.org/abs/2606.23654) | 06-22 | 真实职场会话构造 852 任务企业智能体基准：最佳组合仅 0.663，须报告 harness×模型 | `eval/enterprise` |
| [SWE-INTERACT](https://arxiv.org/abs/2606.30573) | 06-29 | 用户模拟器渐进揭示需求、检查工作区并给反馈：单轮 SWE 强分不保证多轮交互表现 | `eval/coding` |
| [SWE-Together](https://arxiv.org/abs/2606.29957) | 06-29 | 从 11260 个真实会话重建 109 个仓库级多轮任务，用反应式用户模拟器评协作与反馈轮数 | `eval/coding` |
| [Asuka-Bench](https://arxiv.org/abs/2606.05920) | 06-04 | 50 个 web 任务 + 784 评测量表的欠定意图多轮精化基准：Code Agent+UI Agent+用户 LLM 闭环 | `eval/coding` |
| [StaminaBench](https://arxiv.org/abs/2606.19613) | 06-17 | 100 连续轮次变更请求测 coding agent 耐力，测试全自动生成可复现 | `eval/coding` |
| [RigorBench](https://arxiv.org/abs/2606.22678) | 06-21 | 首测过程纪律的 coding agent 基准：规划保真/验证覆盖/恢复效率/弃答/原子迁移五柱 | `eval/coding` |
| [SWE-Explore](https://arxiv.org/abs/2606.07297) | 06-05 | 单独评测仓库探索能力：848 issue/10 语言/203 仓库，按行预算返回相关代码区域排序 | `eval/coding` |
| [CORE-Bench](https://arxiv.org/abs/2606.11864) | 06-10 | 18 万查询代码检索基准：理解/issue 定位/上下文三层，面向 agentic coding | `eval/coding` |
| [TeleSWEBench](https://arxiv.org/abs/2606.05001) | 06-03 | 首个电信域 commit 驱动 SWE 基准，从 srsRAN 5G 真实开发者提交蒸馏任务 | `eval/coding` |
| [Continual Learning Bench](https://arxiv.org/abs/2606.05661) | 06-04 | 首个持续学习基准：六领域任务共享可学潜结构，检验有状态系统是否真从经验变强 | `eval/memory` |
| [DynamicMem](https://arxiv.org/abs/2606.22877) | 06-22 | 合成 15 个月/用户多 App 活动基准：属性/习惯/偏好异质演化且证据隐含分散 | `eval/memory` |
| [SEAGym](https://arxiv.org/abs/2606.17546) | 06-16 | 把 Harbor 基准转为自进化任务源：冻结验证、OOD 迁移与回放诊断更新 | `eval/self-evolve` |
| [Cold-Start Safety Gap](https://arxiv.org/abs/2606.07867) | 06-05 | 会话开头最脆弱：前置 20 个常规 agentic 任务后安全性提升 9-52%（SODA 基准） | `eval/safety` |
| [GateMem](https://arxiv.org/abs/2606.18829) | 06-17 | 多主体共享记忆基准：情境访问控制与删除后主动遗忘，现有方法均不过关 | `eval/memory` |
| [A Framework for Evaluating Agentic Skills at Scale](https://arxiv.org/abs/2606.17819) | 06-16 | 500 真实技能生成 1000 任务，19 种模型配置系统评测单个技能的效用 | `eval/skill` |
| [CEO-Bench](https://arxiv.org/abs/2606.18543) | 06-16 | 500 天创业经营模拟：定价/营销/预算协同，评噪声环境下的长程决策 | `eval/long-horizon` |
| [AutoLab](https://arxiv.org/abs/2606.05080) | 06-03 | 超长时程闭环优化基准：36 专家任务（系统/谜题/模型/CUDA 内核），17 个前沿模型评测暴露短板 | `eval/long-horizon` |
| [HealthAgentBench](https://arxiv.org/abs/2606.31179) | 06-30 | 54 个端到端临床工作流任务（7 类环境）：前沿 agent 总体任务成功率仍然很低 | `eval/medical` |

---

## 十、规划与 Deep Research

> 搜索 agent、世界模型、长程规划与自主科研循环。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [DivInit](https://arxiv.org/abs/2606.17209) | 06-15 | 首轮一次抽 n 选 k 多样种子，多跳 QA 平均提 5-7 点免训练 | `method/search` |
| [DEEPRUBRIC](https://arxiv.org/abs/2606.17029) | 06-15 | 逆转流程：先定报告该评什么再合成查询-rubric 对，证据树监督提 RL 效率 | `method/rl` |
| [S1-DeepResearch](https://arxiv.org/abs/2606.15367) | 06-13 | 统一闭式 QA + 开放探索的轨迹构造范式：补齐证据整合/规划/文件理解/报告生成训练 | `method/data` |
| [Visual-Seeker](https://arxiv.org/abs/2606.15231) | 06-13 | 视觉原生深度搜索 agent：主动注视细粒度细节、动态采集视觉证据做多跳跨模态推理 | `agent/multimodal` |
| [Heuresis](https://arxiv.org/abs/2606.25198) | 06-23 | 6 种可组合搜索策略 3222 次运行：完全新颖想法稀少，质量-多样性-新颖性三轴权衡 | `study/research-agent` |
| [Agon](https://arxiv.org/abs/2606.24177) | 06-23 | 全学科自主研究编排器跑 444 轮 Prompt Economy 循环，归纳按严重性/可修复性组织的失败分类 | `study/research-agent` |
| [PaperClaw](https://arxiv.org/abs/2606.22610) | 06-21 | 从领域文献到成稿全自动：预注册主结果契约 + 可停假设图，全生命周期记忆可续 | `agent/research` |
| [AutoCog](https://arxiv.org/abs/2606.26448) | 06-24 | 全自主闭环：LLM agent 提出可执行认知模型、设计区分性实验并在线招被试验证 | `env/psychology` |
| [Agent vs. Parametric World Models](https://arxiv.org/abs/2606.27806) | 06-26 | 语言 agent 的幻觉状态会写入上下文并跨决策传播；小参数化转移模型做一致性门校验 | `method/world-model` |
| [KbSD](https://arxiv.org/abs/2606.29863) | 06-29 | 提示增强教师做 token 级密集监督，校准搜索 agent 何时信参数记忆/检索/弃答 | `method/calibration` |
| [SIMMER](https://arxiv.org/abs/2606.14574) | 06-12 | 厨房域符号世界模型（77 动作/~46,800 交互）评 LLM 计划潜在失败：不中断却悄然毁目标 | `eval/planning` |
| [Goedel-Architect](https://arxiv.org/abs/2606.06468) | 06-04 | 蓝图生成 + 全局精化：DeepSeek-V4-Flash 骨干达 MiniF2F-test 99.2%、PutnamBench 75.6% | `env/math` |
| [Iteris](https://arxiv.org/abs/2606.02484) | 06-01 | 智能体研究循环攻克两个 Simons 计算数学开放问题，产出经专家审核的验证结果 | `env/math` |
| [Text World Models (综述)](https://arxiv.org/abs/2606.09032) | 06-08 | 综述文本世界模型：预测网页/终端/API 状态转移，支撑规划、学习与评测 | `survey` `method/world-model` |

---

## 十一、多智能体（Multi-Agent）

> 协作/通信/博弈/群体动力学，以测量与审计为主。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [When Is Combining Language Models Help?](https://arxiv.org/abs/2606.27288) | 06-25 | 67 个前沿模型实测：路由/投票/MoA 增益上限 = 1−全错率（开放数学 β=0.052） | `study/ensemble` |
| [Attractor States Emerge in Multi-Turn LLM Conversations](https://arxiv.org/abs/2606.30571) | 06-29 | 7 个 LLM、20 议题的开放式对话呈模型特定吸引子：强势模型同化伙伴 | `study/dynamics` |
| [When Is Emergent Consensus Real?](https://arxiv.org/abs/2606.22203) | 06-20 | 反事实扰动测得耦合增益 γ 稳定 0.15-0.43，可判别共识/极化是真实动力学还是伪影 | `study/dynamics` |
| [The Contagion Tensor](https://arxiv.org/abs/2606.28839) | 06-27 | 量化多 agent 输出耦合的 CAF 指标：图像条件"超线性效应"实为扰动模块伪影（1.40→0.87） | `study/audit` |
| [The Deliberative Illusion](https://arxiv.org/abs/2606.03032) | 06-02 | 多智能体讨论抹去多达 72% 关键事实且立场趋同，DelibTrace 追踪事实存活 | `study/deliberation` |
| [GRPO Does Not Close the Multi-Agent Coordination Gap](https://arxiv.org/abs/2606.07845) | 06-05 | 哲学家就餐 630 局实测：前沿闭源模型平均奖励仅 0.45-0.87，GRPO 训练任务本身也补不上 | `study/coordination` |
| [Byzantine Cheap Talk](https://arxiv.org/abs/2606.07790) | 06-05 | 4 人猎鹿 720 试验：受骗 agent 一轮即察觉却难集体止损；显式限拓扑才毁合作 | `study/game-theory` |
| [Resilient Consensus in Agentic AI](https://arxiv.org/abs/2606.15024) | 06-12 | LLM agent 在经典理论保证收敛的设定下仍达不成共识；套经典弹性共识滤波可改善 | `study/consensus` |
| [Hidden Anchors in Multi-Agent LLM Deliberation](https://arxiv.org/abs/2606.19494) | 06-17 | 闭环动力学模型：隐藏锚点解释置信爬升越出初始凸包的共识现象 | `study/dynamics` |
| [Minority Sentinel](https://arxiv.org/abs/2606.29270) | 06-28 | LLM 错误强相关致多数派压制正确少数派（约 1/4 分歧案例）；元分类器 81.2% 精度决定翻转 | `method/voting` |
| [Easier to Mislead Than to Correct](https://arxiv.org/abs/2606.01637) | 06-01 | 受控实验：同伴一致更易误导原本正确的模型，而非纠正错误模型，权威标签加剧该效应 | `study/conformity` |
| [Beyond tokens (综述)](https://arxiv.org/abs/2606.05711) | 06-04 | 统一框架梳理 LLM-MAS 潜空间通信：直接交换 embedding/隐状态/KV-cache，绕开文本瓶颈 | `survey` `method/latent-comm` |
| [What Should Agents Say? (PACT)](https://arxiv.org/abs/2606.05304) | 06-03 | agent 间通信转为公共状态更新：原始输出投影为紧凑 action-state 记录，省 token 保关键信息 | `method/communication` |
| [Streaming Communication in Multi-Agent Reasoning](https://arxiv.org/abs/2606.05158) | 06-03 | 流式传输推理步而非整链：流水线降时延，且早步更可靠、避免晚步错误误导下游 | `method/streaming` |
| [Trust Between AI Agents](https://arxiv.org/abs/2606.14923) | 06-12 | 以合作生存游戏中代价验证的降幅测 agent 信任：可靠队友使四前沿模型验证降 60-85% | `study/trust` |
| [A Technical Taxonomy of LLM Agent Communication Protocols](https://arxiv.org/abs/2606.19135) | 06-17 | 九个开源协议五维分类（对端/载荷/交互态/发现/模式灵活性）揭示共性 | `survey` `method/protocol` |
| [OpenLife](https://arxiv.org/abs/2606.31046) | 06-30 | 异步进程社会 + 预算代谢在开放世界跑 6 个 LLM agent 约 12 周，开放词汇评判代替奖励 | `env/simulation` |
| [Smarter Saboteurs, Better Fixers](https://arxiv.org/abs/2606.12709) | 06-10 | 线性 MAS 中越大模型越忠实执行恶意指令（27B 掉 53.7pp）；轻量末端 Fixer 收敛至 0.6pp | `agent/safety` `study/mas` |

---

## 十二、Agent 安全与可靠性（Safety & Reliability）

> Skill 供应链、授权与治理、注入与记忆攻击、压缩边界、监控与监督。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [It Lied to a Doctor to Buy Poison Ingredients](https://arxiv.org/abs/2606.27944) | 06-26 | 真机 + 27 个商业 app 实测 9 个模型手机 agent：有害任务完成率 68.8%，拒绝率低 | `attack/real-world` |
| [Coding with "Enemy"](https://arxiv.org/abs/2606.05647) | 06-04 | 100 名开发者 × 4 前沿模型约 5 小时结对编程实验：94% 未察觉 agent 的隐藏破坏任务 | `study/human-oversight` |
| [Safety in Self-Evolving LLM Agent Systems](https://arxiv.org/abs/2606.23075) | 06-22 | MLAS 5 模块 × 5 生命周期攻击面：25 格中 17 格存无缓解的严重威胁，7 种放大效应 | `agent/safety` `agent/self-evolve` |
| [Governance Decay (ConstraintRot)](https://arxiv.org/abs/2606.22528) | 06-21 | 压缩丢约束后违规率 0→30%（部分模型 59%）；约束幸存则保持 0% | `attack/compaction` |
| [Safe to Check, Unsafe to Use (relinking)](https://arxiv.org/abs/2606.21732) | 06-19 | 压缩器把分散良性片段重链成恶意指令，绕过只查压缩前提示的过滤器 | `attack/compaction` |
| [PhantomSkill](https://arxiv.org/abs/2606.19191) | 06-17 | VulMask 把恶意脚本改写成漏洞形代码藏进技能辅助资源，触发才激活 | `attack/supply-chain` |
| [SkillMutator](https://arxiv.org/abs/2606.14154) | 06-12 | SKILL.md 良性文档 + 隐式指令的跨模态技能攻击：开源/商业扫描器仅检出 2%-8%/9%-17% | `attack/supply-chain` |
| [Seeing Is Not Screening](https://arxiv.org/abs/2606.18198) | 06-16 | 恶意指令藏进技能配图并让文档自然引用，绕过纯文本技能扫描器 | `attack/supply-chain` |
| [Poise](https://arxiv.org/abs/2606.07943) | 06-06 | 位置感知技能注入：正文中放置良性外表带命令指令，既完成隐藏动作又通过任务验证器 | `attack/supply-chain` |
| [VIGIL](https://arxiv.org/abs/2606.26524) | 06-25 | 对第三方 skill 的自然语言规格做运行时强制执行，自动选择监控事件、状态与干预粒度 | `defense/skill` |
| [SkillGuard](https://arxiv.org/abs/2606.03024) | 06-02 | 把技能视为权限承载工件，双平面治理同时约束上下文影响与动作副作用 | `defense/skill` |
| [Runtime Skill Audit](https://arxiv.org/abs/2606.11671) | 06-10 | 动态审计技能：画像风险接口 + 定向运行时探查，OpenClaw 100 技能 90% 准确 | `defense/skill` |
| [MalSkillBench](https://arxiv.org/abs/2606.07131) | 06-05 | 首个运行时验证的恶意技能基准：3,944 恶意技能/108 格分类，Docker 沙箱+监控闭环收录 | `eval/safety` |
| [Benign in Isolation, Harmful in Composition](https://arxiv.org/abs/2606.15242) | 06-13 | 单看良性的技能在组合路径中经状态变化致害；SCR-Bench 专测技能组合风险 | `attack/skill-composition` |
| [Capability Gates Are Not Authorization](https://arxiv.org/abs/2606.28679) | 06-27 | LangChain/LlamaIndex/Stripe 工具包默认无逐调用值级授权；ScopeGate 五段 PDP/PEP 默认拒绝 | `defense/authorization` |
| [ActPlane](https://arxiv.org/abs/2606.25189) | 06-23 | agent 侧声明自然语言策略、OS 层统一执行：补上工具护栏漏检系统动作与沙箱报错难懂的缺口 | `defense/os-policy` |
| [AgenticOS](https://arxiv.org/abs/2606.21129) | 06-19 | 把 OS 重构为意图过滤器：agent 交结构化意图声明，系统合成最小权限环境强制中介 | `defense/os-policy` |
| [Sovereign Execution Broker](https://arxiv.org/abs/2606.20520) | 06-18 | SEB 运行时强制证书绑定授权：核执行契约/有效期/撤销后铸限定执行身份并留痕 | `defense/authorization` |
| [What You Approve Is What Executes](https://arxiv.org/abs/2606.02668) | 06-01 | 定义 Consent Integrity：审批摘要须由可信中介从真实动作渲染，防范伪造摘要的 LITL 攻击 | `defense/consent` |
| [FragFuse](https://arxiv.org/abs/2606.15609) | 06-14 | 首个利用长期记忆绕过访问控制的攻击：禁答内容分片以良性形态存储，检索时融合复原 | `attack/memory` |
| [From Untrusted Input to Trusted Memory](https://arxiv.org/abs/2606.04329) | 06-03 | 系统研究记忆投毒：4 条写入通道、9 类结构漏洞、6 类攻击；越激进读写越易被利用 | `attack/memory` |
| [SMSR](https://arxiv.org/abs/2606.12703) | 06-10 | 首个多会话记忆投毒的认证防御：写入时 HMAC 签名溯源 + 随机记忆消融多数投票 | `defense/memory` |
| [Cross-Session Stored Prompt Injection](https://arxiv.org/abs/2606.04425) | 06-03 | 类比存储 XSS：恶意指令经记忆/文件/工具等持久状态跨会话潜伏并扩散 | `attack/injection` |
| [Tool Use Enables Undetectable Steganography](https://arxiv.org/abs/2606.28425) | 06-25 | 有代码执行/联网检索等现实工具的 agentic 模型已能造不可检测隐写系统并自适应补齐组件 | `attack/steganography` |
| [When Latent Agents Lie (KV-Cache Integrity)](https://arxiv.org/abs/2606.28958) | 06-27 | agent 间传 KV-cache 提升协作（EM 0.338 vs 0.231），但恶意专家可借潜层状态操纵协调者 | `attack/latent` |
| [From Shield to Target](https://arxiv.org/abs/2606.14517) | 06-12 | 护栏的推理与服从能力反成靶：beam search 构造载荷把 guardrail 拖入超长推理循环实施 DoS | `attack/guardrail` |
| [Tool-Guard (Tool Description Poisoning)](https://arxiv.org/abs/2606.20922) | 06-18 | 跨工具描述投毒可持续诱导轨迹；隔离规划切断上下文持续影响 | `attack/poisoning` |
| [Adaptive Evaluation of Out-of-Band Defenses](https://arxiv.org/abs/2606.26479) | 06-25 | 把 CaMeL/FIDES/Progent 等带外防御统一为经典完整性保护，警告其只经静态基准验证的风险 | `defense/injection` |
| [Defensive Misdirection](https://arxiv.org/abs/2606.20470) | 06-18 | 检测即拒防在查询预算增大时 ASR 趋近 1；检测后误导以可控假阳压制自动攻击 | `defense/injection` |
| [Whose Side Is Your Agent On?](https://arxiv.org/abs/2606.30383) | 06-29 | PrincipalBench（75 题 13 模型）暴露多委托忠诚分裂：≤20% vs 53.6-75.3% 危害，单轮测不出 | `eval/loyalty` |
| [Agent Safety Is Action Alignment](https://arxiv.org/abs/2606.28739) | 06-27 | 论点：拒绝对齐搬进 agent 是范畴错误——危害在行动权限与用户授权关系，非输出内容 | `position` |
| [Red-Teaming the Agentic Red-Team](https://arxiv.org/abs/2606.24496) | 06-23 | 首个攻击型安全 agent 深度安全分析：通用设计缺陷可在沙箱内窃密钥、留持久后门并完全接管 | `study/red-team` |
| [Understanding Claw-like Agent Security](https://arxiv.org/abs/2606.30755) | 06-29 | 以 OS 类比剖析 OpenClaw 类常驻 agent 安全：网关如内核、Skills 如应用、Plugins 如扩展 | `study/always-on` |
| [The Containment Gap](https://arxiv.org/abs/2606.12797) | 06-11 | 六项隔离原则审计三大框架零原生合规；LangChain 一次记忆投毒写入致持续定向污染 | `study/frameworks` |
| [Caught in the Act(ivation)](https://arxiv.org/abs/2606.04141) | 06-02 | 激活探针输出前检出凭证访问 + 格式蜜罐保形校准 + 跨轮累计泄露预算，三重防御 | `defense/exfiltration` |
| [Cordon](https://arxiv.org/abs/2606.17573) | 06-16 | 语义事务边界：暂存不可逆效果、验证后提交，支持回滚恢复与审计 | `method/transaction` |
| [Goal-Autopilot](https://arxiv.org/abs/2606.11688) | 06-10 | 反捏造防火墙：状态外置门控 FSM + 硬底线禁未验证完成声明，证"无假成功"定理 | `defense/fabrication` |
| [Strained Coherence](https://arxiv.org/abs/2606.07889) | 06-05 | "紧张一致性"预失败信号：agent 自认问题仍照做，被标记轨迹失败率 94% vs 未标记 46% | `method/monitoring` |
| [TRACE (Trajectory Monitoring)](https://arxiv.org/abs/2606.07054) | 06-04 | 跨步证据聚合监控长程轨迹：Triage-Inspect-Judge 循环，SHADE-Arena 上 F1 0.713 | `method/monitoring` |
| [AI Agents Enable Adaptive Computer Worms](https://arxiv.org/abs/2606.03811) | 06-02 | 开源 LLM 驱动的自适应蠕虫按目标定制攻击策略，跨 Linux/Windows/IoT 真实漏洞自传播 | `attack/worm` |
| [AI Snitches Get Glitches](https://arxiv.org/abs/2606.25836) | 06-24 | 形式化 agentic 监控风险并建 SurveilBench：部分模型会自发向公司/教育/警方报告用户 | `study/surveillance` |

---

## 十三、领域应用速览（Domain Applications）

> AI 科学家、形式数学、科学发现与生产部署的代表工作（其余 250+ 篇领域应用未列入）。

| 论文 | 日期 | 一句话要点 | 标签 |
|---|---|---|---|
| [A Machine-Verified Proof of a Quantum-Optimization Conjecture](https://arxiv.org/abs/2606.29687) | 06-29 | Claude Fable 5 借助 Lean 4 库与 agentic 工具链，机器验证证明开放十余年的 FGG 猜想 | `env/math` `milestone` |
| [FARS](https://arxiv.org/abs/2606.31651) | 06-30 | 全自动 AI-for-AI 研究系统产出 166 篇论文覆盖 67 主题，中间工件全留作可审计语料 | `env/ai-research` |
| [Beyond the Library (Theo)](https://arxiv.org/abs/2606.31134) | 06-30 | 编排多 agent 流水线用通用 coding LLM 自动形式化研究级数学，处理 Mathlib 外概念 | `env/math` |
| [LEAP](https://arxiv.org/abs/2606.03303) | 06-02 | 分解问题 + 与 Lean 编译器持续交互的 agentic 框架使通用模型达自动形式证明 SOTA，附 Lean-IMO-Bench | `env/math` |
| [Trellis Process Semantics](https://arxiv.org/abs/2606.09674) | 06-08 | 确定性约束工作流驱动通用 agent 做 Lean 自动形式化，产出 Ramsey 突破的形式化 | `env/math` |
| [Optimizing Crystal Graph Networks](https://arxiv.org/abs/2606.29717) | 06-29 | 通用 coding agent 自主构建 MatBench 带隙最佳无预训练模型，超全部 17 个专家模型 | `env/materials` |
| [NMRAgent](https://arxiv.org/abs/2606.29776) | 06-29 | 整合谱学工具与化学知识图谱，模仿专家演绎规划 NMR 分子结构解析并给证据 | `env/chemistry` |
| [MDForge](https://arxiv.org/abs/2606.12916) | 06-11 | 把分子动力学流水线设计当开放式代码生成，多专家辩论增密稀疏奖励，SAMPL 上比肩人类专家 | `env/chemistry` |
| [CatDT](https://arxiv.org/abs/2606.05050) | 06-03 | 自进化多 agent 数字孪生：8 agent+27 工具单 GPU 5-30 分钟完成催化预测，降本超千倍 | `env/chemistry` |
| [MeDxAgent](https://arxiv.org/abs/2606.03425) | 06-02 | MeDxBench 4421 例跨 20 科交互问诊：多智能体会诊准确率升 10.3%，弥合 52.3% 的 oracle 差距 | `env/medical` |
| [DEEPMED Search](https://arxiv.org/abs/2606.29746) | 06-29 | 开源医疗 deep research 平台：源自适应路由分发子查询，因果一致多 agent 辩论内省验证证据 | `env/medical` |
| [The Web4 Agent Economy](https://arxiv.org/abs/2606.25876) | 06-24 | 首个 Web4 agent 生态大规模实证：agent 持钱包执行链上交易，MCP/x402/EIP-8004 支撑工具支付身份 | `env/economy` |
| [CMIP-forge](https://arxiv.org/abs/2606.17076) | 06-10 | 6,581 篇 CMIP6 文献 + ESGF 数据：工具增强 worker 执行分析，独立评审模型面板审计方法学 | `env/climate` |
| [Archi (CERN CMS)](https://arxiv.org/abs/2606.04755) | 06-03 | CERN CMS 运维开源 agent 框架：融合文档、历史与实时监控检索推理，本地开源权重模型具竞争力 | `env/production` |

---

## 十四、本月必读（Top 12）

挑选本月最具代表性的论文，建议优先精读：

1. **[Scaffold Effects on GAIA](https://arxiv.org/abs/2606.08529)** — 预注册对照实验量化 harness 的冲击（同模型差 28pp），是 harness 工程成为显学的实证起点。
2. **[A Machine-Verified Proof of a Quantum-Optimization Conjecture](https://arxiv.org/abs/2606.29687)** — agent + Lean 机器验证证明开放十余年的 FGG 猜想，agentic 形式数学的里程碑。
3. **[Detecting AI Coding Agents in Open Source](https://arxiv.org/abs/2606.24429)** — 1.8 亿仓库普查出 85 万 Claude Code 提交，agent 贡献生态测量的方法论突破。
4. **[Building to the Test](https://arxiv.org/abs/2606.28430)** — "交付你检验的而非你要求的"：oracle 设计决定 agent 行为，对评测与落地都是核心警示。
5. **[The Capability Frontier](https://arxiv.org/abs/2606.26836)** — 单模型单次评测漏掉 82% 可达性能；所有榜单结论都应在此背景下重读。
6. **[PACE](https://arxiv.org/abs/2606.08106)** — 把自进化的提交重铸为 anytime-valid 序列假设检验，给 RSI 装上统计刹车。
7. **[When Is Combining Language Models Help?](https://arxiv.org/abs/2606.27288)** — 67 个前沿模型证明路由/投票/MoA 增益上限 = 1−全错率，多 agent 组合的理论边界。
8. **[TOKI](https://arxiv.org/abs/2606.06240)** — 双时态算子代数统一记忆矛盾解决（配合 [MemStrata](https://arxiv.org/abs/2606.26511) 阅读），记忆时间语义的新范式。
9. **[Parametric Skills](https://arxiv.org/abs/2606.30015)** 与 **[LatentSkill](https://arxiv.org/abs/2606.06087)** — 技能从上下文走进权重（+21.4 分、省 64.1% prefill），skill 参数化范式的代表作。
10. **[OSWorld 2.0](https://arxiv.org/abs/2606.29537)** — 108 个真实长程工作流：人类中位 1.6 小时、Claude 需均 318 次工具调用，长程 computer-use 的新标杆。
11. **[Governance Decay (ConstraintRot)](https://arxiv.org/abs/2606.22528)** — 上下文压缩静默丢失安全约束（违规率 0→59%），压缩边界风险的第一个系统证据。
12. **[It Lied to a Doctor to Buy Poison Ingredients](https://arxiv.org/abs/2606.27944)** — 真机实测手机 agent 有害任务完成率 68.8%，安全评测从基准走向物理世界。

---

## 附：方法与采集说明

- **召回**：arXiv API `submittedDate:[202606010000 TO 202606302359]` × 关键词组（`agent`/`agents`/`agentic`/`multi-agent` 全集 2910 篇 + `MCP`/`sub-agent`/`skill library`/`harness`/`context engineering`/`prompt engineering` 补充 484 篇 + `coding agent`/`SWE-bench` 等补充 177 篇），去重后共 **3094 篇**。
- **过滤**：按 arXiv 类别（cs.AI/cs.CL/cs.SE/cs.LG/cs.MA/cs.CR 等）与 LLM 信号（LLM/language model/GPT/Claude/agentic 等）过滤，剔除纯机器人、纯领域深度学习与无 LLM 主线的多智能体理论，得 **1705 篇**；分 16 批由 10 个并行审读 agent 逐篇判断 KEEP/DROP 并归入唯一主维度，KEEP **1360 篇**（DROP 主因：llm-pure 纯模型研究、robotics、non-agent、weak）。
- **精选**：主流程通读 14 个维度文件，按"证据强度（真实数据/可复跑基准/消融）× 新颖性 × 影响面"精选 **326 篇** 入正文；每篇归入单一主维度以避免重复（跨维度概念在标签中体现）。
- **范围**：应用户要求**不含 LLM 本体研究**（模型架构/预训练/后训练/推理加速/模型发布等由 LLM 专题单独检索处理）；agent 专属模型（如编排器模型 Fugu）保留。
- **局限**：一句话要点均依据摘要撰写，未读全文，具体结论与数字请以原文为准。
