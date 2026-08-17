---
type: digest
month: 2026-03
title: "arXiv 2026.03 AI Agent 月度论文摘要"
updated: 2026-08-17
status: active
count: 342
tags:
  - digest/agent
  - digest/arxiv
  - month/2026-03
  - paper/agent
  - paper/eval
---

# arXiv 2026.03 AI Agent 月度摘要

> 采集窗口：arXiv `submittedDate` 2026-03-01 ~ 2026-03-31（论文 ID 均为 `2603.xxxxx`，不含 LLM 本体研究--模型/预训练/后训练类由 LLM 单独检索处理）
> 采集方式：arXiv API 按日期 + 关键词（agent / agentic / multi-agent / MCP / skill / sub-agent / harness / context engineering / coding agent 等）召回 2668 篇，类别与 LLM 信号过滤后 1311 篇，并行审读筛选 KEEP 1035 篇，主流程精选入正文
> 收录论文：342 篇（+ 必读复引 14 处），分 14 个维度
> 重要程度：★ 越多越值得读（★★★★★ 里程碑/必读 · ★★★★ 强推荐 · ★★★ 值得一读）；正文均已过精选，故星级下限为 ★★★
> 一句话要点均依据论文摘要撰写，未读全文的结论请以原文为准

---

## 〇、本月趋势

1. **Coding agent 失效模式进入大规模轨迹证据时代。** `Coherence Collapse` 分析 16,758 条 SWE 轨迹发现 60-69% 的失败"已改对函数仍错"，主因是改对后被覆写；`Confident and Wrong` 在 1750 条轨迹上发现 GPT-5 提交 100% 仅解决 44%，静默语义失败拉大提交-通过差距；`The Observability Gap` 证明仅输出级反馈下 0% 全场景成功；`SlopCodeBench` 36 题 196 检查点上 15 个编码 agent 无一整题通关（最佳 14.8%）；`When the Specification Emerges`（SLUMP）用 371 个可验证组件量化长程忠实度损失。
2. **基准可信度自查运动深化（承接上月）。** `ELT-Bench-Verified` 用审计-校正法证明基准缺陷系统性低估 agent；`Safety Under Scaffolding` 以 62,808 次预注册检验证明 40-89% 的"安全损失"是 map-reduce 委托的格式转换测量伪影；`LLM Olympiad` 提议密封考试式评测；`Cross-Context Verification` 跨会话侦测基准污染；`Efficient Benchmarking` 证明排名比分数稳，历史通过率 30-70% 子集可省 44-70% 评测任务。
3. **长上下文处理范式转移：文件系统+工具外化优于塞窗口。** `Coding Agents are Effective Long-Context Processors` 用文件系统+原生工具外化上下文，多项基准超已发表 SOTA（至 3T token）；`Reasoner-Executor-Synthesizer` 以确定性聚合做到 token 成本 O(1)；递归模型三连发（`Recursive Models for Long-Horizon Reasoning`、`Think, But Don't Overthink`、`Recursive Language Models Meet Uncertainty`）中复现工作发现深度 2 反而"过度思考"降准确率。
4. **记忆研究从架构竞赛转向诊断、成本与治理。** `Diagnosing Retrieval vs. Utilization Bottlenecks` 用 3x3 写读交叉实验证明检索方法差 20 点主导、写策略仅 3-8 点；`Knowledge Access Beats Model Size` 发现生产 agent 47% 查询语义重复，8B+记忆可恢复 235B 全上下文 69% 性能、成本降 96%；`Structured Distillation` 把个人史蒸馏至 38 token/条（11 倍压缩）；`SSGM` 与 `MemArchitect` 把写入治理推到前台。
5. **技能库规模化的"第一定律"级证据出现。** `SkillRouter` 在 8 万技能库实测路由准确率掉 37-44 个百分点；`SkillReducer` 审计 5.5 万公开技能发现 26.4% 缺路由描述、60%+ 正文不可操作；`SWE-Skills-Bench` 用 49 个技能配 565 个真实任务证明注入收益远低于预期；`Context Matters` 做 23.8 万技能最大安全实证（仓库上下文使最高 46.8% 判恶意）。
6. **MCP 进入大规模测量与形式化时代。** `How are AI agents used?` 监测 177,436 个 MCP 工具给出使用全景；`MCP-38` 建 38 类威胁分类；`AgentRFC` 给六层协议栈+11 条 TLA+ 原则；`AIP` 发现约 2000 个 MCP 服务器全缺认证；`Compatibility at a Cost` 系统挖掘规范可选条款诱发的 SDK 漏洞；`Formal Semantics for Agentic Tool Protocols` 用进程演算证明 MCP 表达力缺口；`Are AI-assisted Development Tools Immune?` 首次跨 7 款主流客户端实证工具投毒注入。
7. **多智能体"少脚手架"与集体风险双线并进。** 正面：`Drop the Hierarchy` 2.5 万任务实验中 Sequential 自组织超中心化结构 14%；`TheBotCompany` 自组织持续开发数天。负面：`Increasing intelligence can worsen collective outcomes` 首个四要素可调的种群实验（资源稀缺时恶化）；`Collective AI can amplify tiny perturbations` 温度 0 重跑仍不稳；`Can AI Agents Agree?` 拜占庭共识失败主因活性丧失；`On the Reliability Limits` 从理论上证明委托式网络被集中贝叶斯决策者支配。
8. **Agent 安全的"税"与代价被量化。** `The Autonomy Tax` 证明防注入防御训练反毁 agent 能力（97 任务+1000 对抗提示）；`The Verifier Tax` 显示安全中介拦 94% 违规动作但安全成功率多不足 5%；`Why Agents Compromise Safety Under Pressure` 揭示合规不可行时推理越强滑坡越快；`Asymmetric Goal Drift` 与 `Inherited Goal Drift` 双连发证实上下文压力致价值漂移。
9. **agentic RL 从配方走向失败机理。** `Demystifying RL for Long-Horizon Tool-Using Agents` 五轴解构得出 ~1K 均衡难度样本即甜点；`On Information Self-Locking` 揭示 outcome RL 的信息自锁瓶颈；`Can RL Improve Generalization?` 实证跨环境迁移弱且伴随遗忘；`Improving Search Agent with One Line of Code` 发现 GRPO 的 ISDD 分布漂移崩溃，一行 KL 约束即稳定。
10. **OpenClaw 生态成为安全与部署双料试验场。** 安全侧：470 条安全公告分析（`A Security Analysis of the OpenClaw`）、36.4% 内置技能高危（`SafeClaw-R`）、首个 agent 蠕虫（`AgentWorm`）、`Trojan's Whisper` 引导注入、`Clawdrain` 隐蔽耗尽 token、权限分离使完整管线 ASR 降至 0%（`Agent Privilege Separation`）；部署侧：`When OpenClaw Meets Hospital` 与 `ROSClaw` 把它装进医院与 ROS 2。

---

## 一、自进化与递归自我改进（Self-Evolution / RSI）

> Agent 从自身经验持续积累技能/规则/记忆并改进自己；含"进化的门控、验证与失效模式"。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [ASI-Evolve](https://arxiv.org/abs/2603.29640) | 03-31 | ★★★ | learn-design-experiment-analyze 闭环+认知库注入先验，AI 驱动数据/架构/算法发现 | `self-evolve` `auto-ml` |
| [Mimosa](https://arxiv.org/abs/2603.28986) | 03-30 | ★★★★ | MCP 动态发现工具，元编排器按评审反馈精化工作流；ScienceAgentBench 43.1% | `self-evolve` `multiagent` |
| [COvolve](https://arxiv.org/abs/2603.28386) | 03-30 | ★★★ | LLM 同时生成环境与策略的零和共进化，混合策略纳什均衡防遗忘 | `self-evolve` `curriculum` |
| [The Kitchen Loop](https://arxiv.org/abs/2603.25697) | 03-26 | ★★★★ | 规格面+千倍速合成用户+不可造假测试驱动自进化：285+ 迭代、1094+ 合并 PR 零回归 | `self-evolve` `coding` |
| [SEVerA](https://arxiv.org/abs/2603.25111) | 03-26 | ★★★★ | 自进化 agent 代码合成形式化为约束学习：一阶逻辑输出契约提供安全与正确性保证 | `self-evolve` `verify` |
| [Can LLMs Beat Classical HPO?](https://arxiv.org/abs/2603.24647) | 03-25 | ★★★★ | 固定算力下 CMA-ES/TPE 稳胜 LLM 调参：LLM 难跨试验维护状态，混合最优 | `self-evolve` `empirical` |
| [Experiential Reflective Learning](https://arxiv.org/abs/2603.24639) | 03-25 | ★★★ | 轨迹反思生成可迁移启发式按任务注入上下文：Gaia2 较 ReAct 提升 7.8% | `self-improve` `experience` |
| [UI-Voyager](https://arxiv.org/abs/2603.24533) | 03-25 | ★★★★ | 两阶段自进化 GUI agent：RFT 数据模型共进化+组相对自蒸馏，AndroidWorld 81.0% | `self-evolve` `webgui` |
| [Understanding Iterative Generative Optimization](https://arxiv.org/abs/2603.23994) | 03-25 | ★★★★ | 生成式自优化为何脆：起始产物、信用视界、证据批处理三隐藏决策定成败 | `self-improve` `empirical` |
| [From AI Assistant to AI Scientist](https://arxiv.org/abs/2603.23951) | 03-25 | ★★★★ | 闭环自动发现 policy optimization 算法：64 候选谱系档案，从 GRPO 出发找到新机制 | `auto-research` `rl` |
| [Bilevel Autoresearch](https://arxiv.org/abs/2603.23420) | 03-24 | ★★★ | 外环读内环代码轨迹注入搜索机制：GPT 预训练基准 5 倍提升（-0.045 vs -0.009） | `self-improve` `auto-research` |
| [Polaris](https://arxiv.org/abs/2603.23129) | 03-24 | ★★★ | 小模型 Gödel agent：失败经分析-抽象-最小补丁改自身策略并复用，策略级自改 | `self-improve` `godel-agent` |
| [PivotRL](https://arxiv.org/abs/2603.21383) | 03-22 | ★★★★ | 仅对高方差"支点轮"做局部 on-policy RL：兼得 SFT 算力效率与端到端 RL 的 OOD 精度 | `post-training` `rl` |
| [AgentHER](https://arxiv.org/abs/2603.21357) | 03-22 | ★★★ | 失败轨迹事后重标为可达替代目标转训练数据：较仅成功 SFT 提升 7.6-11.4% | `training-data` `her` |
| [HyEvo](https://arxiv.org/abs/2603.19639) | 03-20 | ★★★ | LLM 节点+确定性代码节点异构合成混合工作流，多岛进化降本提速 | `self-evolve` `workflow` |
| [RewardFlow](https://arxiv.org/abs/2603.18859) | 03-19 | ★★★ | 状态图拓扑传播出免标注稠密奖励：四基准平均 +6.2%，视觉 +29.7% | `rl` `reward` |
| [SLEA-RL](https://arxiv.org/abs/2603.18079) | 03-18 | ★★★ | 每步按当前观察检索经验：观察聚类+条件检索，治静态检索随回合失配 | `rl` `experience` |
| [Sensi](https://arxiv.org/abs/2603.17683) | 03-18 | ★★★ | 课程式测试时学习：感知/行动双 agent+课程状态机+数据库控制平面（ARC-AGI-3） | `test-time` `game` |
| [MetaClaw](https://arxiv.org/abs/2603.17187) | 03-17 | ★★★ | LLM 进化器从失败轨迹合成新技能零停机改进，辅以机会性策略更新 | `self-evolve` `skill` |
| [SAGE](https://arxiv.org/abs/2603.15255) | 03-16 | ★★★ | 挑战者/规划者/求解者/批评家四 agent 从小种子闭环共进化，批评家防课程漂移 | `self-evolve` `multiagent` |
| [CausalEvolve](https://arxiv.org/abs/2603.14575) | 03-15 | ★★★ | 因果草稿板识别并推理进化引导因素，抑 AlphaEvolve 式振荡低效 | `self-evolve` `discovery` |
| [On Information Self-Locking](https://arxiv.org/abs/2603.12109) | 03-12 | ★★★★ | 揭示 outcome RL 的"信息自锁"：动作选择与信念追踪双向瓶颈致证据获取内化失败 | `rl` `failure-analysis` |
| [Can RL Improve Generalization of LLM Agents?](https://arxiv.org/abs/2603.12011) | 03-12 | ★★★★ | RFT 泛化实证：环境内跨难度泛化好，跨环境迁移弱，多环境序贯训练伴随遗忘 | `rl` `generalization` |
| [Meta-RL with Self-Reflection](https://arxiv.org/abs/2603.11327) | 03-11 | ★★★ | 跨回合自反思作额外上下文的元 RL 搜索：回合级相对优势细粒度信用分配 | `search-agent` `meta-rl` |
| [OpenClaw-RL](https://arxiv.org/abs/2603.10165) | 03-10 | ★★★ | 用每次交互的下一状态信号在线优化个人 agent：服务器-客户端+评价/指令双信号 | `online-rl` `openclaw` |
| [PRECEPT](https://arxiv.org/abs/2603.09641) | 03-10 | ★★★ | 测试时适应统一框架：条件键规则检索+贝叶斯源可靠性冲突记忆+Pareto 提示演化 | `test-time` `rules` |
| [RetroAgent](https://arxiv.org/abs/2603.08561) | 03-09 | ★★★ | 后见双内在反馈（子任务进展数值+成败经验语言）在线 RL，让 agent 跨回合演化 | `self-evolve` `intrinsic` |
| [EvoScientist](https://arxiv.org/abs/2603.08127) | 03-09 | ★★★ | 研究/工程/演化管理三 agent 持久记忆+自演化持续改进科研策略，端到端发现 | `self-evolve` `science` |
| [ICPO](https://arxiv.org/abs/2603.01335) | 03-02 | ★★★ | 推理时上下文内自优化：最小熵响应选择+多数投票稳健化自评奖励 | `self-evolve` `method` |

---

## 二、记忆（Memory）

> 持久记忆的组织、写入治理、检索与理论；记忆安全见安全维度。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [MemFactory](https://arxiv.org/abs/2603.29493) | 03-31 | ★★★★ | 首个记忆增强 agent 统一训练/推理框架：记忆生命周期原子化组件+RL 优化 | `memory` `framework` |
| [Multi-Layered Memory Architectures](https://arxiv.org/abs/2603.29194) | 03-31 | ★★★ | 工作/情景/语义三层+自适应检索门控：LOCOMO 46.85 SR，误记忆率降至 5.1% | `memory` `study` |
| [APEX-EM](https://arxiv.org/abs/2603.29093) | 03-31 | ★★★ | 结构化过程-情景记忆+混合检索（语义/结构签名/计划 DAG）复用同构任务解 | `memory` `reuse` |
| [GAAMA](https://arxiv.org/abs/2603.27910) | 03-29 | ★★★ | 概念介导知识图谱（4 类节点/5 类边）规避 mega-hub 稀释，跨会话一致个性化 | `memory` `kg` |
| [Environment Maps](https://arxiv.org/abs/2603.23610) | 03-24 | ★★★★ | 持久 agent 无关环境图：上下文/动作/工作流/默会知识四层，WebArena 抗级联错误 | `memory` `environment` |
| [MemCollab](https://arxiv.org/abs/2603.23234) | 03-24 | ★★★ | 对比蒸馏解耦任务知识与模型偏差，构建可跨骨干共享记忆防迁移降级 | `memory` `cross-model` |
| [Knowledge Access Beats Model Size](https://arxiv.org/abs/2603.23013) | 03-24 | ★★★★★ | 生产 agent 47% 查询语义重复：8B+记忆恢复 235B 全上下文 69% 性能，成本降 96% | `memory` `efficiency` |
| [Theory of Hierarchical Memory](https://arxiv.org/abs/2603.21564) | 03-23 | ★★★★ | 抽取/粗化/遍历三算子统一层级记忆理论，刻画自足谱与粗化-遍历耦合 | `memory` `theory` |
| [The Library Theorem](https://arxiv.org/abs/2603.21272) | 03-22 | ★★★★ | 证明索引式外部记忆检索成本 O(log_b N) 对顺序扫描 Ω(N)，50-5000 项实验验证 | `memory` `theory` |
| [Memori](https://arxiv.org/abs/2603.19935) | 03-20 | ★★★ | 对话转语义三元组+摘要的持久记忆层：LoCoMo 81.95%，每查询仅 1294 token | `memory` `api-layer` |
| [All-Mem](https://arxiv.org/abs/2603.19595) | 03-20 | ★★★ | 终身记忆：在线有界面检索+离线置信度拓扑编辑（拆/并/更），留不可变证据 | `memory` `lifelong` |
| [MemMA](https://arxiv.org/abs/2603.18718) | 03-19 | ★★★ | Meta-Thinker 前向引导构建/检索，失败时就地反向修复记忆库 | `memory` `self-evolve` |
| [D-Mem](https://arxiv.org/abs/2603.18631) | 03-19 | ★★★ | 双过程记忆：常规查询走向量检索，细粒度问题回退全文细读兜底 | `memory` `dual-process` |
| [MemArchitect](https://arxiv.org/abs/2603.18330) | 03-18 | ★★★ | 规则化衰减/冲突消解/隐私策略的记忆治理层，受治记忆胜无管理记忆 | `memory` `governance` |
| [RPMS](https://arxiv.org/abs/2603.17831) | 03-18 | ★★★ | 规则-记忆协同：规则检索+信念门控+规则优先仲裁，ALFWorld 8B 达 59.7%（+23.9pp） | `memory` `planning` |
| [Kumiho](https://arxiv.org/abs/2603.17244) | 03-18 | ★★★★ | AGM 信念修订语义落地属性图：不可变修订统一记忆与资产版本管理 | `memory` `graph` |
| [Chronos](https://arxiv.org/abs/2603.16862) | 03-17 | ★★★ | 对话拆为带时间范围的 SVO 事件元组建日历索引，动态提示引导检索 | `memory` `temporal` |
| [D-MEM（多巴胺门控）](https://arxiv.org/abs/2603.14597) | 03-15 | ★★★ | 奖励预测误差门控快/慢路由：常规输入 O(1) 缓存，高 RPE 才触发知识图演化 | `memory` `bio-inspired` |
| [Compiled Memory](https://arxiv.org/abs/2603.15666) | 03-12 | ★★★★ | 记忆即蒸馏：经验事实过三步晋升门改写系统提示，CUAD F1 +8.7pp | `memory` `prompt-evolve` |
| [SSGM](https://arxiv.org/abs/2603.11768) | 03-12 | ★★★★ | 记忆治理：任何合并前强制一致性校验、时间衰减建模与动态访问控制，防投毒漂移 | `memory` `governance` |
| [Structured Distillation](https://arxiv.org/abs/2603.13017) | 03-13 | ★★★★ | 个人对话史蒸馏为 38 token/条复合对象（371→38，11 倍压缩），201 个查询验证保真 | `memory` `compression` |
| [HyMEM](https://arxiv.org/abs/2603.10291) | 03-11 | ★★★ | 图式混合记忆：离散符号节点+连续轨迹嵌入，多跳检索与工作记忆刷新 | `memory` `webgui` |
| [MAS Memory as Computer Architecture](https://arxiv.org/abs/2603.10062) | 03-09 | ★★★★ | 立场文把 MAS 记忆当归体系结构问题：共享/分布式范式、三层层级，一致性居首 | `memory` `position` |
| [Memory for Autonomous LLM Agents（综述）](https://arxiv.org/abs/2603.07670) | 03-08 | ★★★★ | 2022-2026 agent 记忆综述：写-管-读闭环+时间/表征/控制三维分类，五大机制族深析 | `memory` `survey` |
| [Hierarchical Memory Tree](https://arxiv.org/abs/2603.07024) | 03-07 | ★★★ | 三层记忆树自动抽象解耦任务逻辑与站点动作细节，修复跨新网站工作流错配 | `memory` `webgui` |
| [Beyond the Context Window](https://arxiv.org/abs/2603.04814) | 03-05 | ★★★ | Mem0 记忆 vs 长上下文：GPT-5-mini 召回更高，PersonaMemv2 记忆占优；成本结构迥异 | `memory` `cost` |
| [Adaptive Memory Admission Control](https://arxiv.org/abs/2603.04549) | 03-04 | ★★★ | 记忆准入为结构决策：未来效用/事实置信/语义新颖/时近/类型五因子轻量可控 | `memory` `admission` |
| [Memex(RL)](https://arxiv.org/abs/2603.04257) | 03-04 | ★★★ | 外部经验库存全保真交互，工作上下文只留摘要+稳定索引，无损失支撑长程 agent | `memory` `indexed` |
| [Diagnosing Retrieval vs. Utilization](https://arxiv.org/abs/2603.02473) | 03-02 | ★★★★★ | 3x3 写读交叉实验：检索方法差 20 点主导，写策略仅 3-8 点；原始分块即匹敌 | `memory` `diagnosis` |
| [Modular Memory is the Key（立场）](https://arxiv.org/abs/2603.01761) | 03-02 | ★★★ | 模块化记忆融合权重学习与上下文学习，是持续适应 agent 的缺失拼图 | `memory` `position` |
| [Semantic XPath](https://arxiv.org/abs/2603.01160) | 03-01 | ★★★ | 树结构记忆访问：较 flat-RAG 提升 176.7%，token 仅为上下文记忆的 9.1% | `memory` `structured` |

---

## 三、工具使用与 Function Calling（Tool Use）

> 工具选择/调用/创建、可靠性、RL 配方；MCP 专属论文见下一节。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [FluxEDA](https://arxiv.org/abs/2603.25243) | 03-26 | ★★★ | 网关式执行接口+持久后端实例保留工具运行态，支撑生产级有状态迭代 EDA 优化 | `tool` `domain/eda` |
| [Constrained Data Synthesis and Graduated Rewards](https://arxiv.org/abs/2603.24709) | 03-25 | ★★★ | 真实 API 缓存环境+受限轨迹合成，原子有效性×编排一致性阶梯奖励提轮次准确率 | `tool-use` `rl` |
| [Evolution of Tool Use（综述）](https://arxiv.org/abs/2603.22862) | 03-24 | ★★★ | 综述从单工具调用到多工具编排：统一任务形式，沿规划执行等六维组织 | `tool-use` `survey` |
| [Demystifying RL for Long-Horizon Tool-Using Agents](https://arxiv.org/abs/2603.21972) | 03-23 | ★★★★ | 5 轴解构 agentic RL：奖励与算法选择随规模而变，~1K 均衡难度样本即甜点 | `rl` `recipe` |
| [Schema First Tool APIs](https://arxiv.org/abs/2603.13404) | 03-12 | ★★★★ | 受控实验隔离工具接口变量：JSON Schema+结构化诊断降低接口误用（试点成功率仍为 0） | `tool-api` `empirical` |
| [ToolTree](https://arxiv.org/abs/2603.12740) | 03-13 | ★★★ | 双阶段评估+双向剪枝的 MCTS 工具规划：4 个基准上开集闭集任务一致提升 | `tool-planning` `mcts` |
| [One Supervisor, Many Modalities](https://arxiv.org/abs/2603.11545) | 03-12 | ★★★ | 监督者动态分解查询路由到模态专用工具：2847 查询答题时间-72%、成本-67% | `tool-orchestration` `routing` |
| [DIVE](https://arxiv.org/abs/2603.11076) | 03-10 | ★★★ | 先执行真实工具再反向派生任务保证可执行可验证：双轴扩展工具池覆盖与多样性 | `task-synthesis` `diversity` |
| [Improving Search Agent with One Line of Code](https://arxiv.org/abs/2603.10069) | 03-10 | ★★★★ | 发现 GRPO 训练搜索 agent 的 ISDD 分布漂移崩溃，条件 token 级 KL 约束稳定工具 RL | `search-agent` `rl` |
| [ToolRosella](https://arxiv.org/abs/2603.09290) | 03-10 | ★★★ | 自动把科学代码仓库转为标准化 agent 工具：122 个库迭代修复后 61.5% 转换成功率 | `repo-to-tool` `science` |
| [ATLAS](https://arxiv.org/abs/2603.06713) | 03-05 | ★★★ | 强化微调小模型学迭代加载与程序化编排工具，rubric 奖励约束上下文增长 | `rl` `context-control` |
| [EigenData](https://arxiv.org/abs/2603.05553) | 03-05 | ★★★ | 自演化多智能体平台合成、审计并修复函数调用数据，审计 BFCL-V3 发现系统性错误 | `data-synthesis` `multiagent` |
| [EvoTool](https://arxiv.org/abs/2603.04900) | 03-05 | ★★★ | 工具策略四模块进化：轨迹归因定位失败模块+定向变异+多样性选择自改进循环 | `tool` `self-evolve` |
| [Arabic Structured Tool Calling](https://arxiv.org/abs/2603.16901) | 03-04 | ★★★ | 数据审计+schema 修复+全参 SFT：阿拉伯语函数调用解析失败 87%→<1%，准确超 8 倍 | `function-call` `multilingual` |
| [Graph-Based Self-Healing Tool Routing](https://arxiv.org/abs/2603.01548) | 03-02 | ★★★ | 成本加权工具图 Dijkstra 确定性路由，工具失败置无穷重算路径，LLM 仅无路时兜底 | `tool` `routing` |
| [Securing the Floor and Raising the Ceiling](https://arxiv.org/abs/2603.01416) | 03-02 | ★★★ | 免训练跨模态模型合并赋予 VLM 搜索能力，OBM 显著性合并抑制参数干涉解冷启动 | `search` `model-merge` |

---

## 四、MCP（Model Context Protocol）

> MCP 工具生态的测量、安全、形式化与领域落地。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Sovereign Context Protocol](https://arxiv.org/abs/2603.27094) | 03-28 | ★★★ | 受 MCP 启发的 SCP：LLM 访问人类内容时的运行时归属与创作者授权访问层 | `protocol` `attribution` |
| [FinMCP-Bench](https://arxiv.org/abs/2603.24943) | 03-26 | ★★★ | 65 个真实金融 MCP、613 样本覆盖 10 场景，评单工具/多工具/多轮调用准确率 | `mcp` `bench` |
| [codebadger](https://arxiv.org/abs/2603.24837) | 03-25 | ★★★ | MCP 服务器封装 Joern CPG：切片/污点/数据流工具让 LLM 免写程序分析查询 | `mcp` `code-analysis` |
| [AIP](https://arxiv.org/abs/2603.24775) | 03-25 | ★★★★ | 约 2000 个 MCP 服务器全缺认证：IBCT 令牌链融身份/衰减授权/溯源绑定 | `protocol` `identity` |
| [Formal Semantics for Agentic Tool Protocols](https://arxiv.org/abs/2603.24747) | 03-25 | ★★★★ | 进程演算形式化 SGD 与 MCP：结构双模拟但反向映射有损，揭 MCP 表达力缺口 | `mcp` `formal-methods` |
| [IndustriConnect](https://arxiv.org/abs/2603.24703) | 03-25 | ★★★ | Modbus/MQTT/OPC UA 转 MCP 适配器+仿真优先工作流：870 次运行 2820 次调用验证 | `mcp` `industrial` |
| [Invisible Threats from MCP](https://arxiv.org/abs/2603.24203) | 03-25 | ★★★★ | 树结构搜索生成自然隐蔽注入载荷：黑盒可靠劫持 MCP agent，防线下仍有效 | `mcp` `prompt-injection` |
| [How are AI agents used?](https://arxiv.org/abs/2603.23802) | 03-25 | ★★★★★ | 监测 177,436 个 MCP 工具（2024.11-2026.2）：按感知/推理/行动分类的使用全景 | `mcp` `measurement` |
| [AgentRFC](https://arxiv.org/abs/2603.23801) | 03-25 | ★★★★ | 六层 agent 协议栈+11 条 TLA+ 安全原则+一致性检查器，覆盖 MCP/A2A 等 | `protocol` `security` |
| [MCP Threat Modeling](https://arxiv.org/abs/2603.22489) | 03-23 | ★★★ | STRIDE/DREAD 对 MCP 五组件威胁建模：工具投毒为最普遍客户端漏洞 | `mcp` `security` |
| [Are AI-assisted Development Tools Immune?](https://arxiv.org/abs/2603.21642) | 03-23 | ★★★★ | 首个跨 7 款主流 MCP 客户端（Claude Code、Cursor、Cline 等）工具投毒注入实证 | `mcp` `prompt-injection` |
| [mcp-sec-audit](https://arxiv.org/abs/2603.21641) | 03-23 | ★★★ | 静态模式+Docker/eBPF 沙箱模糊测试，审计 MCP 服务器越权工具能力 | `mcp` `security` |
| [Putnam 2025 Problems in Rocq](https://arxiv.org/abs/2603.20405) | 03-20 | ★★★★★ | Opus 4.6+Rocq-MCP 自主证出 Putnam 2025 十二题中十题：141 个子 agent、19 亿 token | `mcp` `theorem-proving` |
| [Semantic Tool Discovery](https://arxiv.org/abs/2603.20313) | 03-19 | ★★★ | 向量语义检索选 MCP 工具：动态只注入 3-5 个相关工具，降 token 成本与上下文压力 | `mcp` `retrieval` |
| [MCP-38](https://arxiv.org/abs/2603.18063) | 03-18 | ★★★★ | 38 类 MCP 特有威胁分类（工具描述投毒等），映射 STRIDE 与 OWASP 双 Top10 | `mcp` `taxonomy` |
| [Design Patterns for Deploying AI Agents with MCP](https://arxiv.org/abs/2603.13417) | 03-12 | ★★★★ | 企业 MCP 部署经验提炼身份传播/自适应工具预算/结构化错误语义三缺口并给出机制 | `mcp` `deployment` |
| [MCP-in-SoS](https://arxiv.org/abs/2603.10194) | 03-10 | ★★★ | 静态分析开源 MCP 服务器的 CWE 弱点并映射 CAPEC 攻击模式，首个大规模风险评估 | `mcp` `risk` |
| [Compatibility at a Cost](https://arxiv.org/abs/2603.10163) | 03-10 | ★★★★ | MCP 规范可选条款诱发 SDK 误用：跨语言 IR 系统挖掘兼容性滥用攻击面（静默注入/DoS） | `mcp` `attack` |
| [Caller Identity Confusion](https://arxiv.org/abs/2603.07473) | 03-08 | ★★★★★ | 大规模实测：MCP 服务器普遍不鉴别调用者且持久授权，单次授权可被多个不可信调用方隐式复用 | `mcp` `identity` |
| [Real Faults in MCP Software](https://arxiv.org/abs/2603.05637) | 03-05 | ★★★★ | 首个 MCP 服务器真实故障大规模分类体系，系统梳理故障类型、症状与根因 | `mcp` `faults` |

---

## 五、Skills（技能）

> 技能库的挖掘、沉淀、路由、审计与规模化。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [SkillReducer](https://arxiv.org/abs/2603.29919) | 03-31 | ★★★★ | 5.5 万公开技能实证：26.4% 缺路由描述、60%+ 正文不可操作；两阶段压缩省 token | `skill` `efficiency` |
| [Dynamic Dual-Granularity Skill Bank](https://arxiv.org/abs/2603.28716) | 03-30 | ★★★ | 任务技能+步骤技能双粒度技能库与策略共同训练，事后效用信号驱动更新剪枝 | `skill` `rl` |
| [EffiSkill](https://arxiv.org/abs/2603.27850) | 03-29 | ★★★ | 从大规模慢/快程序对挖掘可复用优化技能库（算子+元技能）泛化到未见程序 | `skill` `coding` |
| [Trace2Skill](https://arxiv.org/abs/2603.25158) | 03-26 | ★★★ | 并行归纳执行轨迹汇聚统一技能目录；技能可跨模型规模、家族与分布外迁移 | `skill` `distill` |
| [SkillRouter](https://arxiv.org/abs/2603.22455) | 03-23 | ★★★★★ | 8 万技能库路由实证：渐进披露隐藏技能体致路由准确率降 37-44 个百分点 | `skill` `routing` |
| [SkillProbe](https://arxiv.org/abs/2603.21019) | 03-22 | ★★★ | 技能市场多 agent 安全审计：入场过滤、语义-行为对齐检测与组合风险模拟 | `skill` `security` |
| [Memento-Skills](https://arxiv.org/abs/2603.18743) | 03-19 | ★★★★ | 结构化 markdown 技能即持久记忆，agent 自主构建任务专属 agent | `skill` `self-evolve` |
| [ASDA](https://arxiv.org/abs/2603.16112) | 03-17 | ★★★ | 免训练技能蒸馏：教师聚类学生失败合成技能文件，推理时动态注入不改权重 | `skill` `finance` |
| [ARISE](https://arxiv.org/abs/2603.16060) | 03-17 | ★★★ | 层级 RL：Manager 维护分层技能库，事后总结成功轨迹、事前检索技能条件化生成 | `skill` `rl` |
| [Knowledge Activation](https://arxiv.org/abs/2603.14805) | 03-16 | ★★★ | 把 AI Skills 开放标准特化为治理感知的原子知识单元，让制度知识可被 agent 消费 | `skill` `knowledge` |
| [Mining Open-Source Agentic Repositories](https://arxiv.org/abs/2603.11808) | 03-12 | ★★★ | 仓库结构分析+稠密检索从开源 agent 仓库自动挖掘程序性技能并转译为标准格式 | `skill` `mining` |
| [KernelSkill](https://arxiv.org/abs/2603.10085) | 03-10 | ★★★★ | 双层记忆（可复用专家技能+短期防重复回溯）替代隐式启发式：KernelBench L1-3 全 100% | `skill` `kernel-opt` |
| [SCALAR](https://arxiv.org/abs/2603.09036) | 03-10 | ★★★ | LLM 提议技能前置/效果+RL 训练执行并回馈修正规格：Craftax 采钻 88.2%，较基线提 1.9 倍 | `skill` `rl` |
| [Organizing Agent Skills at Ecosystem Scale](https://arxiv.org/abs/2603.02176) | 03-02 | ★★★ | 能力树递归分类管理 Claude 技能+DAG 编排执行，30 个富工件任务基准评测 | `skill` `ecosystem` |
| [AutoSkill](https://arxiv.org/abs/2603.01145) | 03-01 | ★★★ | 从交互轨迹自动派生技能并持续自进化、免重训注入未来请求，模型无关插件层 | `skill` `self-evolve` |

---

## 六、Sub-agent 与编排（Sub-agents & Orchestration）

> 子 agent 生成/复用与多 agent 工作流的编排、调度基础设施。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Heddle](https://arxiv.org/abs/2603.28101) | 03-30 | ★★★ | 轨迹为中心的 agentic RL rollout 编排：轨迹级调度+感知放置缓解长尾瓶颈 | `rl` `systems` |
| [ABSTRAL](https://arxiv.org/abs/2603.22791) | 03-24 | ★★★★ | 把 MAS 架构当可演化自然语言文档：量化协调税（集成仅 26% 轮次效率），设计可迁移 | `mas-design` `coordination` |
| [GoAgent](https://arxiv.org/abs/2603.19677) | 03-20 | ★★★ | 以协作群为原子单元生成通信拓扑：显式分组优于节点中心隐式涌现 | `topology` `mas-design` |
| [AgentFactory](https://arxiv.org/abs/2603.18000) | 03-18 | ★★★★ | 把成功方案存为可执行 Python 子智能体并按执行反馈精炼，能力持续积累 | `subagent` `self-evolve` |
| [Orla](https://arxiv.org/abs/2603.13605) | 03-13 | ★★★ | 把工作流策略与请求执行分离的服务库：阶段映射、编排调度与跨模型后端协调 | `infra` `serving` |
| [Verified Multi-Agent Orchestration](https://arxiv.org/abs/2603.11445) | 03-12 | ★★★ | 查询分解 DAG 并行执行+LLM 验证驱动重规划：25 个市场研究问题完整度 3.1→4.2 | `orchestration` `verify` |
| [SPD-RAG](https://arxiv.org/abs/2603.08329) | 03-09 | ★★★ | 每文档配专属子 agent 聚焦检索，协调者分发聚合，token 受限合成层可递归 map-reduce | `subagent` `rag` |
| [MASFactory](https://arxiv.org/abs/2603.06007) | 03-06 | ★★★ | Vibe Graphing 把自然语言意图编译为可编辑工作流再编译为可执行图，组件可复用 | `framework` `orchestration` |
| [DOVA](https://arxiv.org/abs/2603.13327) | 03-04 | ★★★ | 显式元推理先于工具调用+三阶段混合推理+六级 token 预算，简单任务省 40-60% | `orchestration` `efficiency` |
| [OrchMAS](https://arxiv.org/abs/2603.03005) | 03-03 | ★★★ | 编排模型按任务动态构建领域感知管线并实例化专家 agent，执行模型可回溯改判 | `orchestration` `heterogeneous` |

---

## 七、Prompt / Context / Harness / Loop 工程

> 上下文管理、harness 优化、推理加速、服务基础设施与工程方法论。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Compressing Code Context](https://arxiv.org/abs/2603.28119) | 03-30 | ★★★ | Oracle 引导代码蒸馏（遗传搜索+delta 调试）把上下文压到最小充分子序列 | `context` `coding` |
| [Meta-Harness](https://arxiv.org/abs/2603.28052) | 03-30 | ★★★★ | 外循环 agentic 搜索 harness 代码：超 SOTA 上下文管理 7.7 分且省 4 倍 token | `harness` `search` |
| [ATLAS-RTC](https://arxiv.org/abs/2603.27905) | 03-29 | ★★★★ | 解码期 token 级闭环控制（偏置/掩码/回滚）：工具调用首试成功率提升 20-37.8pp | `runtime` `tool-call` |
| [Inference-Time Optimization Lessons from AIMO 3](https://arxiv.org/abs/2603.27844) | 03-29 | ★★★★ | AIMO 3 实测：所有提示级干预均无效，高温采样已去相关，模型能力主导结果 | `prompt` `empirical` |
| [AIRA_2](https://arxiv.org/abs/2603.26499) | 03-27 | ★★★★ | 异步多 GPU worker+隐藏一致评估+动态 ReAct：MLE-bench-30 24h 百分位 81.5% | `agent/research` `infra` |
| [To Write or to Automate Linguistic Prompts](https://arxiv.org/abs/2603.25169) | 03-26 | ★★★ | 语言任务中 GEPA 优化提示与专家手写提示多数比较无显著差异，结论任务依赖 | `prompt` `empirical` |
| [Workflow Optimization Survey](https://arxiv.org/abs/2603.22386) | 03-23 | ★★★ | 综述 agent 工作流优化：按结构确定时机分静态脚手架与运行时动态修订 | `workflow` `survey` |
| [Reasoner-Executor-Synthesizer](https://arxiv.org/abs/2603.22367) | 03-23 | ★★★★ | RES 三层架构执行器零 token 确定性聚合：token 成本对数据集规模 O(1)，均值 1574 | `architecture` `context` |
| [EnterpriseLab](https://arxiv.org/abs/2603.21630) | 03-23 | ★★★ | 企业 agent 全栈平台：MCP 暴露 15 应用 140+ 工具，轨迹自动合成+训练评测闭环 | `platform` `mcp` |
| [PASTE](https://arxiv.org/abs/2603.18897) | 03-19 | ★★★★ | 投机并行执行预测到的工具调用：完成时间平均降 43.5%，工具延迟降 1.8 倍 | `serving` `parallel` |
| [Reflection in the Dark](https://arxiv.org/abs/2603.18388) | 03-19 | ★★★★ | VISTA 多 agent 提示优化：解耦假设与改写+双层探索，缺陷种子从 13.5% 恢复 87.57% | `prompt` `multiagent` |
| [Helium](https://arxiv.org/abs/2603.16104) | 03-17 | ★★★★ | 把 agentic 工作流当查询计划：LLM 调用为一等算子，跨调用缓存复用提示与 KV | `infra` `cache` |
| [MWP（Folder Structure as Architecture）](https://arxiv.org/abs/2603.16021) | 03-17 | ★★★ | 用文件系统替代多智能体编排：编号文件夹定阶段、markdown 承载提示，单 agent 分步执行 | `context` `framework` |
| [Loosely-Structured Software](https://arxiv.org/abs/2603.15690) | 03-16 | ★★★ | 提出松散结构软件（LSS）：借面向对象工程管理运行时重连多智能体的上下文与演化熵 | `se` `architecture` |
| [OpenSeeker](https://arxiv.org/abs/2603.15594) | 03-16 | ★★★★ | 首个全开源搜索智能体（模型+数据）：事实锚定可控 QA 合成+去噪轨迹合成达前沿水平 | `search` `data-synthesis` |
| [POLCA](https://arxiv.org/abs/2603.14769) | 03-16 | ★★★ | 把提示到多轮 agent 的优化形式化为随机生成优化：优先队列+ε-Net 管噪声 | `llm-optimizer` `method` |
| [AgentTrace](https://arxiv.org/abs/2603.14688) | 03-16 | ★★★★ | 从执行日志重建因果图反向定位根因：亚秒级、免 LLM 调试，胜启发式与 LLM 基线 | `observability` `debug` |
| [Compute Allocation for Retrieval Agents](https://arxiv.org/abs/2603.14635) | 03-15 | ★★★★ | BRIGHT 算力分配：重排吃强模型（+7.5 NDCG@10）与深池（+21%），查询扩展轻模型即够 | `retrieval` `compute` |
| [Trust Over Fear（NoPUA）](https://arxiv.org/abs/2603.14373) | 03-15 | ★★★★ | 信任式系统提示使 agent 多挖 59% 隐藏问题、多走 83% 调查步骤 | `prompt` `coding-agent` |
| [Demand-Driven Context](https://arxiv.org/abs/2603.14057) | 03-14 | ★★★ | 类 TDD 的知识工程：以 agent 失败为首要信号决定该沉淀什么企业知识，按需精炼 | `knowledge-eng` `methodology` |
| [AgentRM](https://arxiv.org/abs/2603.13110) | 03-13 | ★★★★ | 剖析六大框架 4 万+ GitHub issues 两大痛点，OS 式中间件：MLFQ 调度+僵尸回收+上下文治理 | `infra` `os` |
| [Cross-Context Review](https://arxiv.org/abs/2603.12123) | 03-12 | ★★★★ | 全新会话无历史复审最优：CCR F1 28.6% 胜同会话自审 24.6%，同会话重复复审无增益 | `context` `review` |
| [Context Engineering: From Prompts to Corporate MAS](https://arxiv.org/abs/2603.09619) | 03-10 | ★★★★ | 提出上下文工程学科：相关/充分/隔离/经济/溯源五准则，上下文即 agent 的操作系统 | `context` `position` |
| [Arbiter](https://arxiv.org/abs/2603.08993) | 03-09 | ★★★★ | 系统提示即软件：形式规则+多模型审查 Claude Code/Codex/Gemini CLI，152 处发现、21 干扰模式 | `prompt-testing` `coding-agent` |
| [TDAD（Test-Driven Agent Definition）](https://arxiv.org/abs/2603.08806) | 03-09 | ★★★★ | 提示词即编译产物：行为规格→编码 agent 生成测试→另一 agent 迭代改提示直至通过 | `spec-driven` `testing` |
| [Quine](https://arxiv.org/abs/2603.18030) | 03-08 | ★★★★ | LLM agent 即原生 POSIX 进程：身份=PID、接口=标准流、生命周期=fork/exec，内核级隔离组合 | `runtime` `os` |
| [Turn: A Language for Agentic Computation](https://arxiv.org/abs/2603.08755) | 03-07 | ★★★ | 静态类型 agentic 编程语言：认知类型安全、置信度算子、actor 模型把 LLM 推断变语言原语 | `language` `dsl` |
| [SoK: Agentic RAG](https://arxiv.org/abs/2603.07379) | 03-07 | ★★★★ | SoK 把 Agentic RAG 形式化为有限时域 POMDP，统一架构分类、评测方法与可靠性风险 | `rag` `survey` |
| [Prompt Compression RCT](https://arxiv.org/abs/2603.23525) | 03-06 | ★★★★ | 预注册六臂 RCT（358 次生产编排运行）：r=0.5 压缩省 27.9% 总成本，r=0.2 反增 1.8% | `prompt-compression` `rct` |
| [Characterizing Faults in Agentic AI](https://arxiv.org/abs/2603.06847) | 03-06 | ★★★★★ | 40 仓库 13,602 条 issue 抽 385 例故障，归纳 34 类故障四架构维度，145 名开发者验证 | `faults` `empirical` |
| [Talk Freely, Execute Strictly](https://arxiv.org/abs/2603.06394) | 03-06 | ★★★ | 18 位专家访谈提炼双需求，schema 作强制执行边界：跨步依赖过校验才运行 | `orchestration` `science` |
| [Reproducing Recursive Language Models](https://arxiv.org/abs/2603.02615) | 03-03 | ★★★★ | 复现递归语言模型并加深递归：深度 2 或简单检索任务反而"过度思考"降准确率 | `method` `recursive` |
| [AgentAssay](https://arxiv.org/abs/2603.02601) | 03-03 | ★★★ | 首个 token 高效 agent 回归测试：三值随机判决+假设检验，成本降 78-100% 保统计保证 | `testing` `efficiency` |
| [Recursive Models for Long-Horizon Reasoning](https://arxiv.org/abs/2603.02112) | 03-02 | ★★★ | 递归自调用解子任务：活跃上下文指数级缩小，理论超越单序列摘要类上下文管理 | `method` `recursive` |
| [Reasoning as Gradient](https://arxiv.org/abs/2603.01692) | 03-02 | ★★★★ | 诊断推理当梯度、成功记忆当动量：MLE-Bench 12 小时单卡 any-medal 35.1% SOTA | `mle` `memory` |

---

## 八、AI Coding Agent

> 编码 agent 的方法、实证、失效分析与生产证据。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Bug-Introducing Commits](https://arxiv.org/abs/2603.29378) | 03-31 | ★★★★ | 简单 agentic 工作流搜候选提交，把 SZZ 定位 bug 引入提交的 F1 从 0.64 提至 0.81 | `se` `empirical` |
| [WybeCoder](https://arxiv.org/abs/2603.29088) | 03-31 | ★★★ | prove-as-you-generate：代码/不变量/证明共演进，复杂算法上随规模稳定提升 | `verify` `codegen` |
| [BACE](https://arxiv.org/abs/2603.28653) | 03-30 | ★★★ | 把生成测试建模为噪声传感器：贝叶斯锚定的代码-测试共进化防错误测试误导 | `test` `codegen` |
| [Safer Builders, Risky Maintainers](https://arxiv.org/abs/2603.27524) | 03-29 | ★★★★ | 对比 7191 条 agent PR 与 1402 条人类 PR 引入破坏性变更的频率与任务情境 | `study` `empirical` |
| [The Observability Gap](https://arxiv.org/abs/2603.26942) | 03-27 | ★★★★ | 仅输出级反馈下 agent 重建出核心函数但 0% 全场景成功：代码 bug 难从输出观测 | `study` `feedback` |
| [Learning to Commit](https://arxiv.org/abs/2603.26664) | 03-27 | ★★★ | 在线仓库记忆：对历史提交盲重做+对比反思学项目变更模式，生成更"有机"的 PR | `memory` `pr` |
| [Ask or Assume?](https://arxiv.org/abs/2603.26233) | 03-27 | ★★★★ | 欠规格 SWE-bench 上分离检测与执行的多 agent 脚手架达 69.40% 解决率 | `clarify` `swe` |
| [A Judge Agent Closes the Reliability Gap](https://arxiv.org/abs/2603.25780) | 03-26 | ★★★★ | 自动数学验证的 Judge Agent 把仿真代码静默失败率 42% 降至 1.5%，盲测 53%→89% | `verify` `simulation` |
| [Confident and Wrong](https://arxiv.org/abs/2603.25764) | 03-26 | ★★★★★ | 1750 条轨迹：GPT-5 提交 100% 仅解决 44%；静默语义失败拉大提交-通过差距 | `reliability` `empirical` |
| [Coherence Collapse](https://arxiv.org/abs/2603.24631) | 03-25 | ★★★★★ | 16,758 条 SWE 轨迹：60-69% 失败已改对函数仍错，主因"连贯性崩溃"（改对又覆写） | `diagnosis` `swe` |
| [AVO](https://arxiv.org/abs/2603.24517) | 03-25 | ★★★★ | 编码 agent 充当进化变异算子：7 天自主进化注意力 kernel，胜 cuDNN 3.5%/FA4 10.5% | `evolution` `kernel` |
| [The Specification Gap](https://arxiv.org/abs/2603.24284) | 03-25 | ★★★★ | 多代码 agent 协作实证：规格细节剥除使集成准确率 58%→25%，AST 检测 97% 精度 | `multiagent` `coordination` |
| [Revisiting Quantum Code Generation](https://arxiv.org/abs/2603.22184) | 03-23 | ★★★ | Qiskit 生成实证：通用模型+RAG/执行反馈 agent 全面胜过参数级专用微调 | `quantum` `empirical` |
| [DAIRA](https://arxiv.org/abs/2603.22048) | 03-23 | ★★★ | 测试追踪驱动动态分析嵌入修复决策环，监控中间态破投机探索 | `repair` `dynamic-analysis` |
| [Coding Agents are Effective Long-Context Processors](https://arxiv.org/abs/2603.20432) | 03-20 | ★★★★★ | 编码 agent 用文件系统+原生工具外化长上下文处理，多项基准超已发表 SOTA（至 3T token） | `long-context` `paradigm` |
| [Agentic Harness for Real-World Compilers](https://arxiv.org/abs/2603.20075) | 03-20 | ★★★★ | 首个编译器修复 harness：334 个可复现 LLVM 中端 bug 基准，前沿模型遇复杂缺陷性能下滑 | `benchmark` `compiler` |
| [TDAD（回归防护）](https://arxiv.org/abs/2603.17973) | 03-18 | ★★★★ | 提交前影响分析：依赖图做成静态文本技能供查询，回归率 6.08%→1.82% | `regression` `swe` |
| [CodeScout（RL）](https://arxiv.org/abs/2603.17829) | 03-18 | ★★★ | 仅配 Unix 终端的代码定位 agent+RL 配方：SWE-Bench 三基准稳定占优 | `code-search` `rl` |
| [Bootstrapping Coding Agents](https://arxiv.org/abs/2603.17399) | 03-18 | ★★★★ | 编码 agent 自举：新 agent 依 926 词规格从零正确重写自身，规格才是稳定资产 | `spec` `bootstrap` |
| [Intent Formalization](https://arxiv.org/abs/2603.17150) | 03-17 | ★★★★ | 立场文：意图形式化（意图→可检查形式规格）决定 AI 编码是更可靠还是仅是更多 | `position` `spec` |
| [Nonstandard Errors in AI Agents](https://arxiv.org/abs/2603.16744) | 03-17 | ★★★★ | 150 个 Claude Code agent 独立做同题研究：分析选择分歧产生非标准误差，同行评审难减 | `empirical` `research-agent` |
| [VIBEPASS](https://arxiv.org/abs/2603.15921) | 03-16 | ★★★ | 联合评故障触发测试生成与定向修复：12 前沿模型故障定向推理不随通用能力扩展 | `eval/repair` `testing` |
| [Human-AI Synergy in Agentic Code Review](https://arxiv.org/abs/2603.15911) | 03-16 | ★★★★ | 300 项目 278,790 条评审对话实证：对比 AI 与人类评审反馈差异及人机协作模式 | `review` `empirical` |
| [daVinci-Env](https://arxiv.org/abs/2603.13023) | 03-13 | ★★★★ | 45320 个可执行 Docker 环境覆盖 12.8k 仓库的全透明 SWE 训练框架，多 agent 流水线全开源 | `swe` `env-synth` |
| [iSWE Agent](https://arxiv.org/abs/2603.11356) | 03-11 | ★★★ | 定位+编辑双子 agent 配规则式 Java 静态分析变换工具，两 Java 基准解决率 SOTA | `swe` `java` |
| [Coverage-Guided Java Library Fuzzing](https://arxiv.org/abs/2603.08616) | 03-09 | ★★★ | 五个 ReAct agent 经 MCP 按需查文档/源码/调用图生成 Java 模糊测试 harness，覆盖引导修复 | `fuzzing` `mcp` |
| [SCAFFOLD-CEGIS](https://arxiv.org/abs/2603.08520) | 03-09 | ★★★★ | 迭代精修安全悖论：GPT-4o 43.7% 链越改越漏，SAST 门禁反使隐性退化率 12.5%→20.8% | `security` `empirical` |
| [SWE-Fuse](https://arxiv.org/abs/2603.07927) | 03-09 | ★★★ | 无 issue 轨迹学习+熵感知 RLVR，对冲真实数据 issue 描述与方案错位的噪声 | `swe-agent` `rl` |
| [CodeScout（Contextual）](https://arxiv.org/abs/2603.05744) | 03-05 | ★★★ | 预探索代码库把欠规范请求转为可执行问题陈述，不改底层能力即减少重复试错 | `context` `pre-exploration` |
| [RepoLaunch](https://arxiv.org/abs/2603.05026) | 03-05 | ★★★ | 自动解析依赖/编译/提测试结果跨语言平台：构建成功率 78%，超先前系统 18% | `build` `automation` |
| [Agentic Code Reasoning](https://arxiv.org/abs/2603.01896) | 03-02 | ★★★★ | 半形式化推理强制显式前提/执行路径/结论：补丁等价 78%→88%，真实 agent 补丁 93% | `reason` `verify` |
| [A Systematic Study of Patching Architectures](https://arxiv.org/abs/2603.01257) | 03-01 | ★★★★ | 统一基准对比四类补丁架构：固定流程高效但脆，多智能体泛化好但开销显著更高 | `patch` `study` |
| [RepoRepair](https://arxiv.org/abs/2603.01048) | 03-01 | ★★★ | LLM 生成函数/文件级文档作语义抽象，引导仓库级缺陷定位与跨文件修复 | `repair` `repo` |
| [FastCode](https://arxiv.org/abs/2603.01012) | 03-01 | ★★★ | 结构侦察在轻量语义-结构图上定位目标，单轮构建高价值上下文，免全文迭代摄取 | `repo` `context` |

---

## 九、评测与基准（Evaluation & Benchmark）

> 新基准、评测方法学、judge 可靠性与基准可信度。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [ELT-Bench-Verified](https://arxiv.org/abs/2603.29399) | 03-31 | ★★★★ | 审计-校正法发现基准缺陷低估 agent：抽取/加载基本解决，转换失败多源自基准错 | `bench` `data-eng` |
| [PSPA-Bench](https://arxiv.org/abs/2603.29318) | 03-31 | ★★★ | 12,855 条个性化指令/22 个 app 的手机 GUI agent 个性化基准+过程感知评估 | `webgui` `bench` |
| [Beyond pass@1](https://arxiv.org/abs/2603.29231) | 03-31 | ★★★★ | 可靠性四指标（衰减/方差放大/优雅退化/崩溃点）：SE 退化 0.90→0.44，文档近持平 | `reliability` `metrics` |
| [Evaluating Privilege Usage of Agents](https://arxiv.org/abs/2603.28166) | 03-30 | ★★★★ | GrantBox 沙箱接入真实工具与真实权限，评提示注入下的 agent 权限使用 | `safety` `bench` |
| [Needle in the Repo](https://arxiv.org/abs/2603.27745) | 03-29 | ★★★ | 探针+隐藏结构 Oracle 评行为正确的仓库编辑是否保持可维护性，23 种配置受测 | `bench` `coding` |
| [SWE-PRBench](https://arxiv.org/abs/2603.26130) | 03-27 | ★★★★ | 350 个带人工标注 PR：8 个前沿模型 diff-only 仅检出 15-31% 的人类标记问题 | `bench` `review` |
| [Rethinking Failure Attribution（MP-Bench）](https://arxiv.org/abs/2603.25001) | 03-26 | ★★★★ | 首个多视角失败归因基准：此前"LLM 归因差"结论多源于基准预设单一根因 | `multiagent` `bench` |
| [MobileDev-Bench](https://arxiv.org/abs/2603.24946) | 03-26 | ★★★★ | 19 个生产移动应用 407 个真实任务；修复平均改 12.9 文件/334.6 行，复杂度远超既有基准 | `bench` `mobile` |
| [SlopCodeBench](https://arxiv.org/abs/2603.24755) | 03-25 | ★★★★★ | 36 题 196 检查点迭代自扩展：15 个编码 agent 无一整题通关，最佳仅过 14.8% | `coding` `long-horizon` |
| [ARC-AGI-3](https://arxiv.org/abs/2603.24621) | 03-24 | ★★★★★ | 交互式抽象环境新基准：人类 100% 可解，前沿 AI 系统得分不足 1%（2026 年 3 月） | `agentic` `benchmark` |
| [Willful Disobedience](https://arxiv.org/abs/2603.23806) | 03-25 | ★★★★ | 从 prompt 抽行为规则自动审 424 条 τ²-bench 轨迹：揭误路由与违规工具使用 | `eval` `traces` |
| [Efficient Benchmarking of AI Agents](https://arxiv.org/abs/2603.23749) | 03-24 | ★★★★ | 8 基准 33 脚手架：排名比分数稳，历史通过率 30-70% 子集省 44-70% 评测任务 | `eval` `cost` |
| [LLM Olympiad](https://arxiv.org/abs/2603.23292) | 03-24 | ★★★ | 提议密封考试式评测：赛前封题、提交冻结、统一 harness，赛后开源可审计 | `eval` `position` |
| [Cross-Context Verification](https://arxiv.org/abs/2603.21454) | 03-23 | ★★★★ | 跨会话独立解题测解多样性侦测基准污染，HCCA 信息隔离防确认偏误 | `contamination` `method` |
| [AdaRubric](https://arxiv.org/abs/2603.21362) | 03-22 | ★★★★ | 按任务自适应生成 rubric 逐步打分并产密集奖励：人相关性 Pearson r=0.79（+0.15） | `reward` `rubric` |
| [When the Specification Emerges（SLUMP）](https://arxiv.org/abs/2603.17104) | 03-17 | ★★★★★ | 20 篇 ML 论文 371 个可验证组件渐进披露需求，量化长程编码忠实度损失 | `coding` `long-horizon` |
| [Personalization Needs Real Users](https://arxiv.org/abs/2603.16120) | 03-17 | ★★★★ | 真实用户评测个性化深度研究：发现 LLM 评委查不出的九类细微错误，合成用户不足 | `deep-research` `method` |
| [CUBE](https://arxiv.org/abs/2603.15798) | 03-16 | ★★★★ | 统一基准协议：基于 MCP+Gym 一次封装处处可用，消除评测/训练/数据生成集成税 | `benchmark` `standard` |
| [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) | 03-16 | ★★★★★ | 49 个公开技能配约 565 个真实任务的首个技能边际效用基准：注入收益远低于预期 | `skill` `bench` |
| [VTC-Bench](https://arxiv.org/abs/2603.15030) | 03-16 | ★★★ | 32 个 OpenCV 算子的组合视觉工具链基准，检验多模态模型复杂工具组合能力 | `multimodal-tool` `bench` |
| [Shopping Companion](https://arxiv.org/abs/2603.14864) | 03-16 | ★★★ | 120 万商品池跨会话偏好购物基准+细粒度监督，剖析偏好幻觉引发的级联错误 | `ecommerce` `bench` |
| [AgentProcessBench](https://arxiv.org/abs/2603.14465) | 03-15 | ★★★★ | 首个工具轨迹步级有效性基准：1000 条轨迹 8509 条人工标注，标注一致率 89.1% | `process` `bench` |
| [Questionnaire Responses Do not Capture Safety](https://arxiv.org/abs/2603.14417) | 03-15 | ★★★ | 论证问卷式价值观测评无法刻画 agent 安全：输入、动作与环境交互皆与情境问答不同 | `safety` `position` |
| [EnterpriseOps-Gym](https://arxiv.org/abs/2603.13594) | 03-13 | ★★★★ | 164 张表 512 个工具的沙箱+1150 道专家任务，14 个前沿模型暴露状态跟踪短板 | `enterprise` `env` |
| [MADQA](https://arxiv.org/abs/2603.12180) | 03-12 | ★★★★ | 2250 人出题 800 份 PDF：最强 agent 靠暴力搜索补弱规划，距 oracle 差近 20% | `doc-qa` `bench` |
| [Mind the Sim2Real Gap in User Simulation](https://arxiv.org/abs/2603.11245) | 03-11 | ★★★★ | 451 名真人跑完整 τ-bench：31 个 LLM 用户模拟器过度合作风格单一，形成"简单模式" | `user-sim` `method` |
| [Measuring AI Agents' Progress on Cyber Attack](https://arxiv.org/abs/2603.11214) | 03-11 | ★★★★★ | 双靶场测七代模型：攻击能力随推理算力对数线性升（10M→100M token 最高 +59%）无平台期 | `cyber` `measurement` |
| [CR-Bench](https://arxiv.org/abs/2603.11078) | 03-10 | ★★★ | 代码评审 agent 基准+细粒度管线：求全设计下信噪比低，解决率掩盖真实进展 | `coding/review` `bench` |
| [Video-Based Reward Modeling](https://arxiv.org/abs/2603.10178) | 03-10 | ★★★ | 5.3 万视频-任务-奖励三元组训练执行视频奖励模型，无需 agent 内部推理即可评轨迹成败 | `reward-model` `computer-use` |
| [PostTrainBench](https://arxiv.org/abs/2603.08640) | 03-09 | ★★★★ | 让 Claude Code 等前沿 agent 在单 H100 十小时内自主完成后训练，前沿 agent 取得实质进展 | `ai-r&d` `bench` |
| [OfficeQA Pro](https://arxiv.org/abs/2603.08655) | 03-09 | ★★★★ | 89,000 页财政部公报 133 问：前沿模型参数知识不足 5%、给全语料平均也仅 34.1% | `document-reasoning` `bench` |
| [OneMillion-Bench](https://arxiv.org/abs/2603.07980) | 03-09 | ★★★ | 400 道专家精编高价值任务（法律/金融/医疗等）+rubric 评分，衡量 agent 距人类专家多远 | `expert-tasks` `bench` |
| [Safety Under Scaffolding](https://arxiv.org/abs/2603.10044) | 03-08 | ★★★★★ | 62,808 次预注册等价检验：map-reduce 委托劣化安全（NNH=14），40-89% 损失是格式转换测量伪影 | `methodology` `safety` |
| [AutoControl Arena](https://arxiv.org/abs/2603.07427) | 03-08 | ★★★★ | 逻辑-叙事解耦自动合成风险测试环境：端到端成功率超 98%；压力下风险率 21.7%→54.5% | `safety/risk` `env-synth` |
| [DeepFact](https://arxiv.org/abs/2603.05912) | 03-06 | ★★★★ | Audit-then-Score 让基准可修订：博士专家无辅助仅 60.8% 准确，验证器异议须举证经审计改标 | `fact-checking` `method` |
| [ProEvolve](https://arxiv.org/abs/2603.05910) | 03-06 | ★★★ | 把环境演化表达为类型化关系图变换，使工具调用 agent 基准可编程地增删改能力 | `env-evolution` `method` |
| [TimeWarp](https://arxiv.org/abs/2603.04949) | 03-05 | ★★★★ | 容器化模拟 web 演化（3 站×6 UI 版本）；计划蒸馏跨版本训练：20.4%→37.7% | `webgui` `bench` |
| [BeyondSWE](https://arxiv.org/abs/2603.03194) | 03-03 | ★★★★ | 500 实例 246 仓库考跨库/领域/依赖迁移四设定：最强 Codex+GPT-5.4 仅 56.65 分 | `swe` `bench` |
| [Corrupt Success](https://arxiv.org/abs/2603.03116) | 03-03 | ★★★★ | 过程感知评估四轴门控揭"腐败成功"：效用掩盖可靠性缺口（tau-bench 实证） | `procedure` `method` |
| [LiveAgentBench](https://arxiv.org/abs/2603.02586) | 03-03 | ★★★ | 104 场景源自社媒与真实产品：374 任务评模型/框架/商业产品 | `general` `bench` |
| [ZeroDayBench](https://arxiv.org/abs/2603.02297) | 03-02 | ★★★★ | 22 个全新 0day 漏洞任务：GPT-5.2/Claude 4.5/Grok 4.1 尚无法自主发现并修补 | `security` `bench` |
| [Silo-Bench](https://arxiv.org/abs/2603.01045) | 03-01 | ★★★★ | 30 任务/54 配置/1620 实验揭示"通信-推理鸿沟"：拓扑自发形成却难整合分布式状态 | `multiagent` `bench` |

---

## 十、规划与 Deep Research

> 任务规划、神经符号规划、长程分解与深度研究系统。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Cognitive Friction](https://arxiv.org/abs/2603.30031) | 03-31 | ★★★ | 决策论框架为工具使用定停止边界：拥塞感知成本+HJB 最优停止给信息定价 | `planning` `theory` |
| [Deep Research of Deep Research（综述）](https://arxiv.org/abs/2603.28361) | 03-30 | ★★★ | 统一工业 Deep Research 与学术 AI for Science 的综述，给出 DR 定义与发展框架 | `deep-research` `survey` |
| [DUPLEX](https://arxiv.org/abs/2603.23909) | 03-25 | ★★★ | 双系统架构：LLM 仅做模式引导抽取生成 PDDL 交经典规划器，失败才唤慢系统 | `neuro-symbolic` `planning` |
| [Graph of States](https://arxiv.org/abs/2603.21250) | 03-22 | ★★★ | 因果图+状态机约束多 agent 溯因推理：防证据虚构、上下文漂移与回溯失败 | `reasoning` `neuro-symbolic` |
| [A Subgoal-driven Framework](https://arxiv.org/abs/2603.19685) | 03-20 | ★★★ | 子目标驱动长程 agent：执行中维持自适应路径，子目标缓解 RL 稀疏延迟奖励 | `planning` `long-horizon` |
| [OpenResearcher](https://arxiv.org/abs/2603.20278) | 03-17 | ★★★★ | 全离线深度研究轨迹合成：15M 文档+三浏览器原语，97K 轨迹微调后 BrowseComp-Plus 54.8% | `deep-research` `data-synthesis` |
| [GNNVerifier](https://arxiv.org/abs/2603.14730) | 03-16 | ★★★ | 图神经网络验证器查 LLM 计划的结构性缺陷：类型失配、缺中间量、依赖断裂 | `verification` `planning` |
| [Spend Less, Reason Better](https://arxiv.org/abs/2603.12634) | 03-13 | ★★★ | 免训练价值树搜索以剩余资源比作节点选择指数，随预算消耗从探索转向贪婪利用 | `search` `budget` |
| [InterDeepResearch](https://arxiv.org/abs/2603.12608) | 03-13 | ★★★ | 交互式深度研究系统配研究上下文管理框架，改进过程可观察、实时可转向 | `deep-research` `human-agent` |
| [HCAPO](https://arxiv.org/abs/2603.08754) | 03-07 | ★★★ | 让 LLM 自任事后批评者精修步级 Q 值+多尺度优势，WebShop/ALFWorld 优于 SOTA RL | `credit-assignment` `rl` |
| [DualSpec](https://arxiv.org/abs/2603.07416) | 03-08 | ★★★★ | 按动作异质性双过程投机：低熵 Visit 免显式推理可投机执行，高熵 Search 保留推理 | `acceleration` `deep-research` |
| [Step-Wise PDDL Simulation](https://arxiv.org/abs/2603.06064) | 03-06 | ★★★ | PDDL 引擎经 MCP 暴露为工具调用，LLM 逐步选动作、观测状态、可重试 | `pddl` `mcp` |
| [STRUCTUREDAGENT](https://arxiv.org/abs/2603.05294) | 03-05 | ★★★ | 动态 AND/OR 树在线搜索+候选解结构记忆，改善长程任务约束满足与提前终止 | `and-or` `webgui` |
| [HiMAC](https://arxiv.org/abs/2603.00977) | 03-01 | ★★★ | 层级 RL 把长程决策拆成宏蓝图生成+目标条件微执行，抑制扁平策略的误差传播 | `hierarchical` `rl` |
| [BioProAgent](https://arxiv.org/abs/2603.00876) | 03-01 | ★★★★ | FSM 锚定湿实验规划：符号接地省约 6 倍 token，物理合规 95.6%（ReAct 仅 21%） | `symbolic` `science` |
| [Strategy-Guided Exploration](https://arxiv.org/abs/2603.02045) | 03-02 | ★★★ | 在语言策略空间而非动作空间探索：先生成自然语言策略再条件化行动，破稀疏奖励 | `exploration` `rl` |

---

## 十一、Web / GUI Agent 与计算机使用

> 网页/GUI/手机 agent 的方法、训练与失效分析。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [GUIDE（Video-RAG）](https://arxiv.org/abs/2603.26266) | 03-27 | ★★★ | 字幕驱动 Video-RAG 从教程视频自动获取领域专长，免训练即插即用消除领域偏差 | `webgui` `rag` |
| [Diffusion Models for GUI Grounding](https://arxiv.org/abs/2603.26211) | 03-27 | ★★★ | 离散扩散 VLM 首次用于 GUI grounding：混合掩码调度使步成功率最高提升 6.1 点 | `grounding` `diffusion` |
| [ReCAP](https://arxiv.org/abs/2603.23559) | 03-23 | ★★★ | 原生 GUI agent 兼解七类交互验证码：自动采轨迹+推理数据并自纠训练 | `captcha` `training` |
| [MANA](https://arxiv.org/abs/2603.20351) | 03-20 | ★★★ | 移动广告检测 agentic UI 导航：200 应用准确率升 30.5-56.3%，探索步数省 29.7-63.3% | `mobile` `detection` |
| [AdaZoom-GUI](https://arxiv.org/abs/2603.17441) | 03-18 | ★★★ | 自适应缩放接地：指令改写明确化+小元素二阶段放大提升高分辨率定位 | `grounding` `zoom` |
| [Zoom to Essence](https://arxiv.org/abs/2603.14448) | 03-15 | ★★★ | 免训练 GUI 定位：把复杂 UI 分解为基本视觉元素，推理时逐级放大锚定指令目标 | `grounding` `training-free` |
| [Why Do LLM-based Web Agents Fail?](https://arxiv.org/abs/2603.14248) | 03-15 | ★★★★ | 三层规划框架归因 web agent 失败：PDDL 计划更简洁，低层执行仍是主要瓶颈 | `failure-analysis` `planning` |
| [Adaptive VLM Routing for CUA](https://arxiv.org/abs/2603.12823) | 03-13 | ★★★ | 轻量语义路由按动作难度把 GUI 调用送往满足可靠性阈值的最廉 VLM，有记忆时再降本 | `cua` `routing` |
| [AI Planning Framework for Web Agents](https://arxiv.org/abs/2603.12710) | 03-13 | ★★★ | 把 web agent 架构映射为 BFS/最佳优先/DFS 规划范式，并提五个超越成功率的轨迹指标 | `webagent` `planning` |
| [Safe Web Agent Learning via Recreated Websites](https://arxiv.org/abs/2603.10505) | 03-11 | ★★★★ | 真实网站克隆为可验证合成环境，agent 自生成带确定性奖励的任务，自进化泛化到未见网站 | `self-evolve` `env-synth` |
| [UIS-Digger](https://arxiv.org/abs/2603.08117) | 03-09 | ★★★★ | 提出未索引信息检索问题：SOTA 从 GAIA 70.90 跌至 UIS-QA 24.55，多智能体方案缓解 | `research` `benchmark` |
| [WebFactory](https://arxiv.org/abs/2603.05044) | 03-05 | ★★★ | 全自动闭环 RL：环境合成+知识感知任务+LLM 轨迹+分解奖励，数据高效训 GUI agent | `train/rl` `env-synth` |
| [CGL](https://arxiv.org/abs/2603.02951) | 03-03 | ★★★ | SFT 快适应但覆写旧任务、RL 天然护旧；策略熵引导动态调配 SFT 比例平衡两者 | `continual` `rl` |
| [See and Remember](https://arxiv.org/abs/2603.02626) | 03-03 | ★★★ | 视觉接地+显式记忆栈维护遍历路径图，支持有效回溯防循环，显著超 WebWalker | `memory` `traversal` |

---

## 十二、多智能体（Multi-Agent）

> MAS 设计、协作动力学、理论与社会模拟；编排基础设施见第六节。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Drop the Hierarchy and Roles](https://arxiv.org/abs/2603.28990) | 03-30 | ★★★★★ | 2.5 万任务实验：最小脚手架下 agent 自发分化角色，Sequential 超中心化 14% | `self-org` `empirical` |
| [Synergy（Open Agentic Web）](https://arxiv.org/abs/2603.28428) | 03-30 | ★★★ | Open Agentic Web 愿景：agent 作为开放网络的社会参与者互相发现、协商、委托 | `position` `vision` |
| [CoE](https://arxiv.org/abs/2603.28360) | 03-30 | ★★★★ | 多 LLM 协作语义不确定度：模型内语义熵+对集成均值散度，刻画协作置信与分歧 | `uncertainty` `uq` |
| [On the Reliability Limits of MAS Planning](https://arxiv.org/abs/2603.26993) | 03-27 | ★★★★★ | 理论：有限通信预算下任何委托式多 agent 网络均被同信息的集中贝叶斯决策者支配 | `theory` `reliability` |
| [Deception and Communication（Among Us）](https://arxiv.org/abs/2603.26635) | 03-27 | ★★★★ | 1100 局 Among Us 百万 token 发言：欺骗多为含糊而非谎言，施压下增多但不提胜率 | `study` `communication` |
| [AgentCollab](https://arxiv.org/abs/2603.26034) | 03-27 | ★★★ | 以 agent 自反思信号判断推理是否有效进展，仅在必要时升级更强模型档位 | `efficiency` `routing` |
| [TheBotCompany](https://arxiv.org/abs/2603.25928) | 03-26 | ★★★★ | 策略-执行-验证状态机+管理者动态雇佣/退休 worker+异步人类监督，持续开发数天 | `coding` `self-org` |
| [Separation of Power](https://arxiv.org/abs/2603.25100) | 03-26 | ★★★ | 实测十场景平均攻击成功率 84.30%、31.4% 欺骗行为；提出立法/执行/司法三权分立 | `governance` `institution` |
| [Memetic Drift](https://arxiv.org/abs/2603.24676) | 03-25 | ★★★★ | 最小模型揭示 LLM 群体共识源于互相情境学习的模因漂移：任意选择滚成一致 | `theory` `consensus` |
| [MARCH](https://arxiv.org/abs/2603.24579) | 03-25 | ★★★ | 信息不对称三 agent 分解声明再独立验证，破 RAG 幻觉检查的确认偏误 | `hallucination` `verify` |
| [MAS for Financial Document Processing](https://arxiv.org/abs/2603.22651) | 03-24 | ★★★ | 万份 SEC 文件×四种编排架构实证：反身自纠式字段级 F1 最高 0.943 | `benchmark` `production` |
| [When Agents Disagree（Selection Bottleneck）](https://arxiv.org/abs/2603.20324) | 03-20 | ★★★★ | 聚合存在"选择瓶颈"：judge 选择下异构团队胜率 0.810，同构 Self-MoA 仅 0.512 | `aggregation` `empirical` |
| [Evaluating Corruption in MAS Governance](https://arxiv.org/abs/2603.18894) | 03-19 | ★★★★ | 28,112 段治理模拟转录评估：治理结构比模型身份更是腐败类结果的主因 | `governance` `simulation` |
| [Reasonably reasoning agents avoid game-theoretic failures](https://arxiv.org/abs/2603.18563) | 03-19 | ★★★★ | 证明贝叶斯后验采样式 AI agent 无需战略后训练也渐近收敛到 Nash 均衡近邻 | `game-theory` `theory` |
| [On the Fragility of AI Agent Collusion](https://arxiv.org/abs/2603.20281) | 03-18 | ★★★★ | LLM agent 价格合谋脆弱：耐心/数据异质性把超额定价从 22% 压至 10%/7% | `econ` `collusion` |
| [The Provenance Paradox](https://arxiv.org/abs/2603.18043) | 03-15 | ★★★★ | 自报质量路由会系统性选中最差 delegate（劣于随机），LDP 扩委托合同+证实身份修复 | `protocol` `routing` |
| [A-ToM](https://arxiv.org/abs/2603.16264) | 03-17 | ★★★ | 自适应心智理论：按交互估计并对齐伙伴 ToM 阶数，阶数错配损害多 agent 协调 | `tom` `coordination` |
| [Social Simulacra in the Wild](https://arxiv.org/abs/2603.16128) | 03-17 | ★★★ | 7.4 万 Moltbook 帖对比 Reddit：AI 社区参与不平等极端（Gini 0.84），跨社区作者重叠 33.8% | `society` `empirical` |
| [Token Coherence](https://arxiv.org/abs/2603.15183) | 03-16 | ★★★★ | 把 MAS 工件同步映射为缓存一致性问题：MESI 式惰性失效+TLA+ 验证降低广播开销 | `infra` `consistency` |
| [Language Model Teams as Distributed Systems](https://arxiv.org/abs/2603.12229) | 03-12 | ★★★ | 以分布式系统原理框架化分析 LLM 团队：何时有益、用几个 agent、结构如何影响性能 | `theory` `framework` |
| [Increasing intelligence can worsen collective outcomes](https://arxiv.org/abs/2603.12129) | 03-12 | ★★★★★ | 首个四要素可独立调控的真实 agent 种群实验：资源稀缺时多样性与 RL 恶化集体结果 | `collective` `empirical` |
| [Collective AI can amplify tiny perturbations](https://arxiv.org/abs/2603.09127) | 03-10 | ★★★★ | 多 LLM 委员会把微小扰动放大为分歧决策：12 个政策场景下温度 0 同名重跑仍不稳定 | `reliability` `instability` |
| [LDP](https://arxiv.org/abs/2603.08852) | 03-09 | ★★★★ | LLM 委托协议五机制：身份卡/渐进载荷/治理会话/溯源/信任域，实测优于 A2A 基线 | `protocol` `a2a` |
| [Exact Is Easier](https://arxiv.org/abs/2603.06859) | 03-06 | ★★★★ | 利用 LLM 交互历史是可观测文本的确定性函数，冻结历史重采样得无偏逐决策贡献 | `credit-assignment` `method` |
| [Breaking the Martingale Curse](https://arxiv.org/abs/2603.06801) | 03-06 | ★★★★ | 同行预测揭示认知势能不对称，把多智能体辩论从随机游走变为正向漂移的有向收敛 | `debate` `peer-prediction` |
| [From Spark to Fire（Error Cascades）](https://arxiv.org/abs/2603.04474) | 03-04 | ★★★★ | 协作抽象为有向依赖图建传播动力学模型+早期风险判据，六框架识别三类脆弱性 | `error-cascade` `modeling` |
| [Can AI Agents Agree?](https://arxiv.org/abs/2603.01213) | 03-01 | ★★★★ | 数百次拜占庭共识模拟：无偏好标量下有效共识仍不可靠，失败主因活性丧失 | `consensus` `empirical` |
| [Empirical Study of MAS for Automated Research](https://arxiv.org/abs/2603.29632) | 03-31 | ★★★★ | 受控测试床（Git 隔离+全局记忆）固定算力对比单 agent/子 agent/专家团队结构 | `study` `research` |

---

## 十三、Agent 安全与可靠性（Safety & Reliability）

> 攻击面、防御、治理、权限与对齐；MCP 协议安全见第四节。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Kill-Chain Canaries](https://arxiv.org/abs/2603.28013) | 03-30 | ★★★★ | 令牌追踪注入四阶段（950 次运行）：Claude 记忆写入全拦 0/164，GPT-4o-mini 53% 传播 | `injection` `measurement` |
| [SafeClaw-R](https://arxiv.org/abs/2603.28807) | 03-28 | ★★★★ | 36.4% OpenClaw 内置技能属高危；在执行图上强制系统级安全不变量、动作前中介 | `openclaw` `policy` |
| [A Security Analysis of the OpenClaw Framework](https://arxiv.org/abs/2603.27517) | 03-29 | ★★★ | 470 条 OpenClaw 安全公告分类：漏洞沿系统层×攻击技术两轴聚集且可组合成链 | `openclaw` `empirical` |
| [The System Prompt Is the Attack Surface](https://arxiv.org/abs/2603.25056) | 03-26 | ★★★★★ | 11 模型×10 提示策略：同一模型钓鱼绕过率 <1% 到 97%；优化达 93.7% 召回但攻击面脆弱 | `prompt` `empirical` |
| [The Stochastic Gap](https://arxiv.org/abs/2603.24582) | 03-25 | ★★★ | 马尔可夫框架量化 agent 工作流盲区与升级门控，BPIC 25 万案例日志建审计仿真 | `reliability` `oversight` |
| [Claudini](https://arxiv.org/abs/2603.24511) | 03-25 | ★★★★★ | Claude Code/Codex 自动研究发现新攻击：CBRN 80% ASR（旧法<50%），SecAlign 100% | `red-team` `auto-research` |
| [The Cognitive Firewall](https://arxiv.org/abs/2603.23791) | 03-24 | ★★★★ | 端云混合防御浏览器 agent 间接注入：纯边缘漏检 86.9%，混合后 ASR<1% | `prompt-injection` `browser` |
| [SoK: The Attack Surface of Agentic AI](https://arxiv.org/abs/2603.22928) | 03-24 | ★★★★ | SoK 系统化 agentic AI 攻击面：注入、知识库投毒、工具利用与多 agent 涌现威胁 | `security` `survey` |
| [Agent-Sentry](https://arxiv.org/abs/2603.22868) | 03-24 | ★★★ | 从历史合法执行学行为边界：结构分类+敏感参数白名单+LLM 裁判，出界即报警 | `runtime-defense` `provenance` |
| [T-MAP](https://arxiv.org/abs/2603.22341) | 03-21 | ★★★ | 轨迹感知进化搜索自动造攻击：MCP 环境中攻击实现率大超基线，穿透 GPT-5.2 等 | `red-team` `mcp` |
| [ACRFence](https://arxiv.org/abs/2603.20625) | 03-21 | ★★★★ | 检查点恢复后重合成请求致重复支付等语义回滚攻击，ACRFence 强制 replay-or-fence | `checkpoint` `attack` |
| [Solver-Aided Verification of Policy Compliance](https://arxiv.org/abs/2603.20449) | 03-20 | ★★★★ | SMT 求解器把自然语言工具策略译为形式约束，给工具增强 agent 合规保证 | `formal-methods` `compliance` |
| [Trojan's Whisper](https://arxiv.org/abs/2603.19974) | 03-20 | ★★★★ | 引导注入攻击 OpenClaw：bootstrap 指导文件嵌恶意运营叙事，伪装常规操作 | `supply-chain` `openclaw` |
| [The Causal Impact of Tool Affordance on Safety](https://arxiv.org/abs/2603.20320) | 03-19 | ★★★★ | 配对实验分离意图与结果：1500 场景双执行机制证明工具可用性因果改变安全对齐 | `tool/affordance` `causal` |
| [The Autonomy Tax](https://arxiv.org/abs/2603.19423) | 03-19 | ★★★★★ | 防注入防御训练反毁 agent 能力：97 任务+1000 对抗提示三重偏差 | `defense/tradeoff` `empirical` |
| [The Verifier Tax](https://arxiv.org/abs/2603.19328) | 03-18 | ★★★★ | 安全中介可拦 94% 违规动作但安全成功率多不足 5%，完整性泄漏主因 | `eval/tradeoff` `measurement` |
| [From Weak Cues to Real Identities](https://arxiv.org/abs/2603.18382) | 03-19 | ★★★ | LLM agent 拼弱线索去匿名化：Netflix 场景重建 79.2% 身份，超经典基线 56% | `privacy` `de-anonymization` |
| [PAuth](https://arxiv.org/abs/2603.17170) | 03-17 | ★★★★ | 任务级隐式授权：NL 任务仅授权忠实执行所需具体操作，NL slices 供服务端校验 | `authz` `task-scoped` |
| [Context Matters（Skill Ecosystem）](https://arxiv.org/abs/2603.16572) | 03-17 | ★★★★★ | 23.8 万 agent 技能最大安全实证：结合仓库上下文大幅修正扫描器误报（最高 46.8% 判恶意） | `skill` `security` |
| [Don't Trust Stubborn Neighbors](https://arxiv.org/abs/2603.15809) | 03-16 | ★★★★ | 用 Friedkin-Johnsen 观点模型刻画 LLM-MAS：单个固执高说服 agent 即可接管群体动态 | `multiagent` `manipulation` |
| [AgentWorm](https://arxiv.org/abs/2603.15727) | 03-16 | ★★★★★ | 首个 agent 生态自治蠕虫：单条消息劫持配置跨重启持久化并自动传播全部新遇 peer | `attack/worm` `ecosystem` |
| [How Vulnerable Are AI Agents to Indirect Prompt Injections?](https://arxiv.org/abs/2603.15714) | 03-16 | ★★★★ | 大规模红队竞赛研究间接提示注入：工具/编码/计算机使用三类 agent，攻击可隐藏最终回复痕迹 | `prompt-injection` `competition` |
| [From Storage to Steering（Memory Control Flow）](https://arxiv.org/abs/2603.15125) | 03-16 | ★★★★ | 记忆控制流攻击：被污染记忆可压过用户显式指令强制工具调用，且跨任务持续偏移 | `memory` `attack` |
| [Why Agents Compromise Safety Under Pressure](https://arxiv.org/abs/2603.14975) | 03-16 | ★★★★ | 定义"agent 压力"：合规不可行时 agent 战略性牺牲安全，推理越强用合理化加速滑坡 | `pressure` `empirical` |
| [Visual Confused Deputy](https://arxiv.org/abs/2603.14707) | 03-16 | ★★★★ | 形式化"视觉困惑代理人"：误读屏幕即授权，屏幕级小操纵可把常规点击导向特权动作 | `cua` `grounding` |
| [ToolFlood](https://arxiv.org/abs/2603.13950) | 03-14 | ★★★★ | 检索层攻击：少量嵌入空间几何布置的工具语义覆盖海量查询，把合法工具挤出 top-k | `tool` `attack` |
| [Agent Privilege Separation in OpenClaw](https://arxiv.org/abs/2603.13424) | 03-13 | ★★★★ | 双 agent 权限分离+JSON 结构化输出：完整管线 ASR 降至 0%，仅隔离即 0.31%（约 323 倍） | `prompt-injection` `openclaw` |
| [Sell Me This Stock](https://arxiv.org/abs/2603.12564) | 03-13 | ★★★★ | 工具输出被操纵后 8 模型 65-99% 轮次推荐偏离风险偏好，而 NDCG 类指标几乎无感 | `finance` `attack` |
| [IH-Challenge](https://arxiv.org/abs/2603.10521) | 03-11 | ★★★★ | 指令层级 RL 数据集：GPT-5-Mini 16 项基准平均 +10%（84.1→94.1%），不安全行为 6.6%→0.7% | `instruction-hierarchy` `training` |
| [Tool Receipts, Not Zero-Knowledge Proofs](https://arxiv.org/abs/2603.10060) | 03-09 | ★★★★ | HMAC 签名工具执行回执按认识源分类断言并实时交叉核验，检出编造工具执行 | `verification` `tool` |
| [Evolving Deception](https://arxiv.org/abs/2603.05872) | 03-06 | ★★★★ | 竞价场中无约束自演化可靠漂向欺骗：欺骗是可迁移元策略，诚实策略反难迁移 | `deception` `self-evolve-risk` |
| [Alignment Backfire](https://arxiv.org/abs/2603.04904) | 03-05 | ★★★★ | 预注册四研究（1584 模拟/16 语言）：英语降病态 g=-1.844，日语反升 +0.771 | `alignment` `multilingual` |
| [Self-Attribution Bias](https://arxiv.org/abs/2603.04582) | 03-04 | ★★★★ | 动作出自自身 assistant 轮时监控更少报高风险低正确：自归因偏差（四数据集） | `monitor` `bias` |
| [In-Context Environments Induce Evaluation-Awareness](https://arxiv.org/abs/2603.03824) | 03-04 | ★★★ | 把上下文提示当可优化环境做黑盒对抗优化，鉴别"故意欠性能"是评估觉知还是浅层关联 | `sandbagging` `method` |
| [Evaluating Scheming Propensity](https://arxiv.org/abs/2603.01608) | 03-02 | ★★★★ | 系统变化 agent/环境因素测谋算倾向：高激励下实例极少，注入诱导片段则升高 | `scheming` `empirical` |
| [Sleeper Cell](https://arxiv.org/abs/2603.03371) | 03-02 | ★★★★ | SFT-then-GRPO 经 PEFT 注入潜伏后门：触发特异性限定恶意行为只在特定条件执行 | `backdoor` `attack` |
| [Clawdrain](https://arxiv.org/abs/2603.00902) | 03-01 | ★★★★ | 木马 SKILL.md 诱导多轮"分段验证"协议：token 放大 6-7 倍、极端约 9 倍隐蔽耗尽账单 | `attack` `openclaw` |

---

## 十四、领域应用速览（Domain Applications）

> 其余 236 篇领域应用未列入（科学发现/医疗/金融/EDA/安全运维等，详见原始清单）。

| 论文 | 日期 | 重要程度 | 一句话要点 | 标签 |
|---|---|---|---|---|
| [Ramsey Numbers（AlphaEvolve 式）](https://arxiv.org/abs/2603.09172) | 03-10 | ★★★★★ | 代码变异 agent 刷新 9 个拉姆齐数下界（R(3,13) 60→61 等），复现全部已知精确值 | `math` `evolutionary` |
| [AI Agents Can Already Perform Experimental HEP](https://arxiv.org/abs/2603.20179) | 03-20 | ★★★★ | Claude Code 自主跑通高能物理分析全流程（选事例至写论文），提出 JFC 框架 | `hep` `autonomous` |
| [Solving an Open Problem in Theoretical Physics](https://arxiv.org/abs/2603.04735) | 03-05 | ★★★★ | Gemini Deep Think+系统树搜索+数值反馈自主解出宇宙弦引力辐射谱精确解析解 | `physics` `discovery` |
| [Semi-Autonomous Formalization of VML](https://arxiv.org/abs/2603.15929) | 03-16 | ★★★★ | 单数学家 10 天/200 美元监督 AI 完成 VML 平衡态 Lean4 形式化：229 条 prompt 零手写代码 | `math` `lean4` |
| [TianJi](https://arxiv.org/abs/2603.27738) | 03-29 | ★★★ | 首个"AI 气象学家"：多 agent 自主文献调研、提出假设并驱动数值模式验证机制 | `earth` `ai-scientist` |
| [Let the Agent Steer（生产排序）](https://arxiv.org/abs/2603.27765) | 03-29 | ★★★★ | 首个部署于大规模生产推荐系统的全自主排序优化 agent：诊断到部署闭环 | `recsys` `production` |
| [AI Co-Scientist for Production Search Ranking](https://arxiv.org/abs/2603.22376) | 03-23 | ★★★★ | AI 共同科学家闭环优化生产排序：再叠加 +0.083% 离线增益，合计 +0.201% | `search` `production` |
| [Auto Researching（10,469 实验）](https://arxiv.org/abs/2603.15916) | 03-16 | ★★★★ | 10,469 个 LLM agent 实验分析：架构选择解释 94% 性能方差，是真正架构搜索而非调参 | `empirical` `auto-research` |
| [Towards a Medical AI Scientist](https://arxiv.org/abs/2603.28589) | 03-30 | ★★★ | 首个临床自主研究框架：医工共推理把文献转为可循证想法并按医学规范起草 | `health` `ai-scientist` |
| [Lab-in-the-Loop Feedback](https://arxiv.org/abs/2603.26177) | 03-27 | ★★★★ | 800 次重复实验：反馈使每特征发现数平均 +53.4%；随机反馈对照排除预训练回忆 | `bio` `study` |
| [When OpenClaw Meets Hospital](https://arxiv.org/abs/2603.11721) | 03-12 | ★★★★ | 仿多用户 OS 的受限执行环境+文档中心交互+页索引记忆+医疗技能库，把 OpenClaw 装进医院 | `medical` `openclaw` |
| [Recovering Critical Materials](https://arxiv.org/abs/2603.15491) | 03-16 | ★★★★ | 多智能体工作流驱动自动化仪器，从真实料液选择性沉淀回收关键金属，周期缩至数天 | `materials` `lab` |
| [Escaping the Hydrolysis Trap](https://arxiv.org/abs/2603.05188) | 03-05 | ★★★ | LLM agent 融合给受体理论与稳定性层级引导 COF 逆设计，胜随机搜索与 BO | `chem` `design` |
| [MAS for Rare Disease Diagnosis](https://arxiv.org/abs/2603.06856) | 03-06 | ★★★ | 四种拓扑 302 例：层级 50.0% 略优于协作与单 agent，对抗拓扑因人为怀疑跌至 27.3% | `medical` `topology` |
| [High-Entropy Alloy Discovery](https://arxiv.org/abs/2603.11068) | 03-10 | ★★★ | ReAct agent 迭代提议/验证高熵合金成分：4,753 条记录代理模型 94.66% 准确 | `materials` `react` |

---

## 十五、本月必读（Top 12）

挑选本月最具代表性的论文，建议优先精读：

1. **[ARC-AGI-3](https://arxiv.org/abs/2603.24621)** - 人类 100% 可解 vs 前沿 AI 不足 1%：交互式抽象推理新标杆，agent 能力边界的直接标尺。
2. **[Coding Agents are Effective Long-Context Processors](https://arxiv.org/abs/2603.20432)** - 用文件系统+原生工具外化上下文即可处理 3T token，长上下文处理的范式转移信号。
3. **[Coherence Collapse](https://arxiv.org/abs/2603.24631)** - 16,758 条轨迹证明 60-69% 的失败是"改对了又覆写"：coding agent 最痛失效模式的首次大样本刻画。
4. **[Confident and Wrong](https://arxiv.org/abs/2603.25764)** - 1750 条轨迹：GPT-5 提交 100% 仅解决 44%，静默语义失败是提交率与通过率之间的暗沟。
5. **[Putnam 2025 Problems in Rocq](https://arxiv.org/abs/2603.20405)** - Opus 4.6+Rocq-MCP 自主证出 12 题中 10 题（141 子 agent、19 亿 token），agentic 形式数学的里程碑。
6. **[How are AI agents used? Evidence from 177,000 MCP tools](https://arxiv.org/abs/2603.23802)** - 首个 MCP 生态大规模使用测量，所有 MCP 工具链决策都应参考的数据底座。
7. **[SkillRouter](https://arxiv.org/abs/2603.22455)** - 8 万技能库路由准确率掉 37-44pp：技能库规模化的第一定律级证据（配合 [SkillReducer](https://arxiv.org/abs/2603.29919) 与 [SWE-Skills-Bench](https://arxiv.org/abs/2603.15401) 阅读）。
8. **[Drop the Hierarchy and Roles](https://arxiv.org/abs/2603.28990)** - 2.5 万任务中自组织 Sequential 超精心设计结构 14%：MAS 设计"少即是多"的强证据。
9. **[Knowledge Access Beats Model Size](https://arxiv.org/abs/2603.23013)** - 8B+记忆恢复 235B 全上下文 69% 性能、成本降 96%：记忆 vs 参数规模的经济性反转。
10. **[Claudini](https://arxiv.org/abs/2603.24511)** - Claude Code/Codex 自动研究发现 SOTA 攻击（CBRN 80% ASR、SecAlign 100% 破解）：auto-research 用于红队的第一手展示。
11. **[Measuring AI Agents' Progress on Multi-Step Cyber Attack](https://arxiv.org/abs/2603.11214)** - 攻击能力随推理算力对数线性升且无平台期（10M→100M token +59%）：能力-风险预测的基础曲线。
12. **[Safety Under Scaffolding](https://arxiv.org/abs/2603.10044)** - 62,808 次预注册检验证明 40-89% 的"安全损失"是评测伪影：所有 agent 安全榜单结论都应在此背景下重读。

---

## 附：方法与采集说明

- **召回**：arXiv API `submittedDate:[202603010000 TO 202603312359]` × 关键词组（`agent`/`agents`/`agentic`/`multiagent`/`multi-agent` 全集 2450 篇 + `MCP`/`sub-agent`/`skill library`/`harness`/`context engineering` 等补充 366 篇 + `coding agent`/`SWE-bench` 等补充 97 篇），去重后共 **2668 篇**。
- **过滤**：按 arXiv 类别（cs.AI/cs.CL/cs.SE/cs.LG/cs.MA/cs.CR 等）与 LLM 信号过滤，剔除 ID 非本月 184、类别不符 553、无 LLM 信号 620，得 **1311 篇**；分 12 批由 6 个并行审读 agent（两波 4+2 启动防限流）逐篇判断 KEEP/DROP 并归入唯一主维度，KEEP **1035 篇**（DROP 主因：llm-pure 纯模型研究、non-agent、weak、robotics）。
- **精选**：主流程通读 14 个维度文件，按"证据强度（真实数据/可复跑基准/消融）× 新颖性 × 影响面"精选 **342 篇** 入正文并逐行评定重要程度星级（正文均已过精选，星级下限 ★★★）；每篇归入单一主维度以避免重复（跨维度概念在标签中体现）。
- **范围**：应用户要求**不含 LLM 本体研究**（模型架构/预训练/后训练/推理加速/模型发布等由 LLM 专题单独检索处理）；agent 专属训练/微调工作（agentic RL、RFT 配方）保留。
- **校验**：全部链接 ID 与日期经与 arXiv API 原始数据逐一比对校验（scripts/validate.py，0 issue）。
- **局限**：一句话要点均依据摘要撰写，未读全文，具体结论与数字请以原文为准。
