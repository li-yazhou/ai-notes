---
type: index
updated: 2026-06-29
status: active
tags:
  - index/papers
  - paper/agent
  - paper/eval
  - map/ai-agent
---

# AI Agent 与大模型评测论文地图

> 更新时间：2026-06-29
> 覆盖范围：`02-agent`（41 篇）与 `03-basemodel`（22 篇）共 63 篇论文笔记（61 篇 arXiv + 2 篇 OpenAI technical/preprint）

---

## 一、分类码体系

每篇论文都已加入 Obsidian YAML frontmatter，核心字段包括：

```yaml
type: paper
paper_id: arxiv-2210.03629
primary_category: agent-loop
priority: p0
read_type: deep
tags:
  - paper/agent
  - agent/react-loop
  - eval/agent-benchmark
```

常用分类码：

| 前缀 | 用途 | 示例 |
|---|---|---|
| `paper/*` | 论文大类 | `paper/agent`, `paper/eval`, `paper/safety` |
| `agent/*` | Agent 能力/形态 | `agent/tool-use`, `agent/multi-agent`, `agent/web-agent` |
| `eval/*` | 评测类型 | `eval/model-benchmark`, `eval/llm-judge`, `eval/safety` |
| `method/*` | 方法范式 | `method/cot`, `method/tree-search`, `method/reflection` |
| `env/*` | 环境类型 | `env/web`, `env/code`, `env/os`, `env/business` |
| `priority/*` | 阅读优先级 | `priority/p0`, `priority/p1`, `priority/p2` |
| `read/*` | 阅读方式 | `read/deep`, `read/skim`, `read/reference` |

---

## 二、推荐阅读路径

1. **先读 p0**：建立 LLM / Agent 主干：Attention、GPT-1、GPT-2、GPT-3、GPT-4、GPT-5、DeepSeek-V2、DeepSeek-V3、DeepSeek-R1、DeepSeek-V4、CoT、MRKL、ReAct、Toolformer、Reflexion、ToT、Voyager、CAMEL、AutoGen、MetaGPT、AgentBench、WebArena、SWE-bench、GAIA、OSWorld、tau-bench、AI Agents That Matter、HLE、Survey。
2. **再补 p1**：补齐工具调用、Web/OS/安全、LLM Judge 和多智能体协作细节。
3. **最后查 p2**：GLUE / SuperGLUE 等主要作为大模型评测发展背景。

---

## 三、按主题分类

### 0. 大模型基础架构与预训练

理解 Transformer 与 GPT 预训练路线作为后续 LLM / Agent 的底座。

| 论文                                                                  |   年份 | 优先级  | 阅读方式   | 关键标签                                   |
| ------------------------------------------------------------------- | ---: | ---- | ------ | -------------------------------------- |
| [[1706-Attention Is All You Need\|Attention Is All You Need]] | 2017 | `p0` | `deep` | `llm/architecture, method/transformer` |
| [[1801-Improving Language Understanding by Generative Pre-Training\|Improving Language Understanding by Generative Pre-Training]] | 2018 | `p0` | `deep` | `llm/pretraining, llm/decoder-only, model/gpt, method/generative-pretraining` |
| [[1901-Language Models are Unsupervised Multitask Learners\|Language Models are Unsupervised Multitask Learners]] | 2019 | `p0` | `deep` | `llm/pretraining, llm/decoder-only, model/gpt-2, method/zero-shot` |
| [[2005-Language Models are Few-Shot Learners\|Language Models are Few-Shot Learners]] | 2020 | `p0` | `deep` | `llm/pretraining, model/gpt-3, method/in-context-learning, method/few-shot` |
| [[2303-GPT-4 Technical Report\|GPT-4 Technical Report]] | 2023 | `p0` | `deep` | `llm/frontier-model, llm/multimodal, model/gpt-4, eval/safety` |
| [[2601-OpenAI GPT-5 System Card\|OpenAI GPT-5 System Card]] | 2025 | `p0` | `deep` | `llm/frontier-model, llm/reasoning-model, model/gpt-5, eval/safety, eval/agent-benchmark` |
| [[2401-DeepSeek LLM Scaling Open-Source Language Models with Longtermism\|DeepSeek LLM: Scaling Open-Source Language Models with Longtermism]] | 2024 | `p1` | `deep` | `llm/pretraining, model/deepseek-llm, method/scaling` |
| [[2405-DeepSeek-V2 A Strong Economical and Efficient Mixture-of-Experts Language Model\|DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model]] | 2024 | `p0` | `deep` | `llm/architecture, model/deepseek-v2, method/moe, method/mla` |
| [[2412-DeepSeek-V3 Technical Report\|DeepSeek-V3 Technical Report]] | 2024 | `p0` | `deep` | `llm/frontier-model, model/deepseek-v3, method/moe, method/fp8, method/multi-token-prediction` |
| [[2501-DeepSeek-R1 Incentivizing Reasoning Capability in LLMs via Reinforcement Learning\|DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning]] | 2025 | `p0` | `deep` | `llm/reasoning-model, model/deepseek-r1, method/reinforcement-learning, method/grpo` |
| [[2606-DeepSeek-V4 Towards Highly Efficient Million-Token Context Intelligence\|DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence]] | 2026 | `p0` | `deep` | `llm/frontier-model, llm/long-context, model/deepseek-v4, method/compressed-attention, agent/long-horizon` |

### 1. 基础模型与传统大模型评测

回答“模型懂不懂语言、知识和专家级难题”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2501-Humanitys Last Exam\|Humanity's Last Exam]] | 2025 | `p0` | `deep` | `eval/model-benchmark, eval/knowledge, eval/frontier` |
| [[2009-MMLU Measuring Massive Multitask Language Understanding\|Measuring Massive Multitask Language Understanding]] | 2020 | `p1` | `skim` | `eval/model-benchmark, eval/knowledge` |
| [[2206-BIG-bench Beyond the Imitation Game\|Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models]] | 2022 | `p1` | `skim` | `eval/model-benchmark, eval/capability-map` |
| [[2211-HELM Holistic Evaluation of Language Models\|Holistic Evaluation of Language Models]] | 2022 | `p1` | `skim` | `eval/model-benchmark, eval/multi-metric, eval/reliability` |
| [[2311-GPQA A Graduate-Level Google-Proof QA Benchmark\|GPQA: A Graduate-Level Google-Proof Q&A Benchmark]] | 2023 | `p1` | `skim` | `eval/model-benchmark, eval/knowledge, eval/science` |
| [[1804-GLUE A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding\|GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding]] | 2018 | `p2` | `reference` | `eval/model-benchmark, eval/nlu` |
| [[1905-SuperGLUE A Stickier Benchmark for General-Purpose Language Understanding Systems\|SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems]] | 2019 | `p2` | `reference` | `eval/model-benchmark, eval/nlu` |

### 2. 推理与规划方法

回答“模型如何分解、搜索、回退和借助程序推理”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models\|Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]] | 2022 | `p0` | `deep` | `agent/reasoning-planning, method/cot` |
| [[2305-Tree of Thoughts Deliberate Problem Solving with Large Language Models\|Tree of Thoughts: Deliberate Problem Solving with Large Language Models]] | 2023 | `p0` | `deep` | `agent/reasoning-planning, method/search, method/tree-search` |
| [[2211-PAL Program-aided Language Models\|PAL: Program-aided Language Models]] | 2022 | `p1` | `skim` | `agent/reasoning-planning, agent/tool-use, method/code-execution` |
| [[2203-Self-Consistency Improves Chain of Thought Reasoning in Language Models\|Self-Consistency Improves Chain of Thought Reasoning in Language Models]] | 2022 | `p1` | `skim` | `agent/reasoning-planning, method/cot, method/self-consistency` |
| [[2310-LATS Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models\|Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models]] | 2023 | `p1` | `skim` | `agent/reasoning-planning, agent/react-loop, method/tree-search, method/mcts` |

### 3. 工具使用与模型/工具编排

回答“模型如何选择工具、调用 API、组合专家系统”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2205-MRKL Systems\|MRKL Systems: A modular, neuro-symbolic architecture]] | 2022 | `p0` | `deep` | `agent/tool-use, method/tool-calling, method/neuro-symbolic` |
| [[2302-Toolformer Language Models Can Teach Themselves to Use Tools\|Toolformer: Language Models Can Teach Themselves to Use Tools]] | 2023 | `p0` | `deep` | `agent/tool-use, method/tool-calling, method/self-supervised` |
| [[2305-Gorilla Large Language Model Connected with Massive APIs\|Gorilla: Large Language Model Connected with Massive APIs]] | 2023 | `p1` | `skim` | `agent/tool-use, method/api-calling, eval/api-benchmark` |
| [[2303-HuggingGPT Solving AI Tasks with ChatGPT and its Friends in Hugging Face\|HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face]] | 2023 | `p1` | `skim` | `agent/tool-use, agent/model-orchestration, method/tool-calling` |
| [[2307-ToolLLM Facilitating Large Language Models to Master Real-world APIs\|ToolLLM: Facilitating Large Language Models to Master Real-world APIs]] | 2023 | `p1` | `skim` | `agent/tool-use, method/tool-calling, eval/tool-benchmark` |

### 4. Agent Loop 与推理-行动闭环

回答“模型如何边想边做、观察反馈并继续行动”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2210-ReAct Synergizing Reasoning and Acting in Language Models\|ReAct: Synergizing Reasoning and Acting in Language Models]] | 2022 | `p0` | `deep` | `agent/react-loop, agent/tool-use, method/reason-act` |

### 5. 反思、记忆与自我改进

回答“Agent 如何跨轮次积累经验、保存记忆、形成技能”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2304-Generative Agents Interactive Simulacra of Human Behavior\|Generative Agents: Interactive Simulacra of Human Behavior]] | 2023 | `p0` | `deep` | `agent/memory, agent/social-simulation` |
| [[2303-Reflexion Language Agents with Verbal Reinforcement Learning\|Reflexion: Language Agents with Verbal Reinforcement Learning]] | 2023 | `p0` | `deep` | `agent/react-loop, agent/reflection, agent/memory, method/reflection` |
| [[2305-Voyager An Open-Ended Embodied Agent with Large Language Models\|Voyager: An Open-Ended Embodied Agent with Large Language Models]] | 2023 | `p0` | `deep` | `agent/memory, agent/skill-learning, agent/embodied-agent, env/game` |
| [[2310-MemGPT Towards LLMs as Operating Systems\|MemGPT: Towards LLMs as Operating Systems]] | 2023 | `p1` | `skim` | `agent/memory, method/context-management` |
| [[2303-Self-Refine Iterative Refinement with Self-Feedback\|Self-Refine: Iterative Refinement with Self-Feedback]] | 2023 | `p1` | `skim` | `agent/reflection, method/self-feedback` |

### 6. 多智能体协作与社会智能

回答“多个 Agent 如何分工、辩论、协商、审查和协作”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2308-AutoGen Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework\|AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework]] | 2023 | `p0` | `deep` | `agent/multi-agent, agent/framework, method/conversation-programming` |
| [[2303-CAMEL Communicative Agents for Mind Exploration of Large Language Model Society\|CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society]] | 2023 | `p0` | `deep` | `agent/multi-agent, method/role-playing` |
| [[2308-MetaGPT Meta Programming for A Multi-Agent Collaborative Framework\|MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework]] | 2023 | `p0` | `deep` | `agent/multi-agent, agent/software-agent, agent/framework, env/code` |
| [[2308-AgentVerse Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors\|AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors]] | 2023 | `p1` | `skim` | `agent/multi-agent, agent/social-simulation` |
| [[2307-ChatDev Communicative Agents for Software Development\|ChatDev: Communicative Agents for Software Development]] | 2023 | `p1` | `skim` | `agent/multi-agent, agent/software-agent, env/code` |
| [[2305-Multiagent Debate Improving Factuality and Reasoning in Language Models\|Improving Factuality and Reasoning in Language Models through Multiagent Debate]] | 2023 | `p1` | `skim` | `agent/multi-agent, method/multi-agent-debate, agent/reasoning-planning` |
| [[2310-SOTOPIA Interactive Evaluation for Social Intelligence in Language Agents\|SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents]] | 2023 | `p1` | `skim` | `agent/multi-agent, agent/social-intelligence, eval/agent-benchmark, env/social` |

### 7. Web / 浏览器 Agent

回答“Agent 如何在真实或半真实网页环境里完成任务”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2307-WebArena A Realistic Web Environment for Building Autonomous Agents\|WebArena: A Realistic Web Environment for Building Autonomous Agents]] | 2023 | `p0` | `deep` | `agent/web-agent, eval/agent-benchmark, env/web` |
| [[2112-WebGPT Browser-assisted question-answering with human feedback\|WebGPT: Browser-assisted question-answering with human feedback]] | 2021 | `p1` | `skim` | `agent/web-agent, agent/browsing, method/rlhf, env/web` |
| [[2306-Mind2Web Towards a Generalist Agent for the Web\|Mind2Web: Towards a Generalist Agent for the Web]] | 2023 | `p1` | `skim` | `agent/web-agent, eval/agent-benchmark, env/web` |
| [[2401-VisualWebArena Evaluating Multimodal Agents on Realistic Visual Web Tasks\|VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks]] | 2024 | `p1` | `skim` | `agent/web-agent, agent/multimodal, eval/agent-benchmark, env/web` |
| [[2401-WebVoyager Building an End-to-End Web Agent with Large Multimodal Models\|WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models]] | 2024 | `p1` | `skim` | `agent/web-agent, agent/multimodal, env/web` |
| [[2403-WorkArena How Capable Are Web Agents at Solving Common Knowledge Work Tasks\|WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?]] | 2024 | `p1` | `skim` | `agent/web-agent, eval/agent-benchmark, env/business, env/web` |
| [[2504-BrowseComp A Simple Yet Challenging Benchmark for Browsing Agents\|BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents]] | 2025 | `p1` | `skim` | `agent/web-agent, agent/browsing, eval/agent-benchmark, env/web` |

### 8. 软件工程 Agent

回答“Agent 能否理解真实代码库并修复真实 issue”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2310-SWE-bench Can Language Models Resolve Real-World GitHub Issues\|SWE-bench: Can Language Models Resolve Real-World GitHub Issues?]] | 2023 | `p0` | `deep` | `agent/software-agent, eval/agent-benchmark, env/code` |

### 9. OS / 桌面 Agent

回答“Agent 能否在真实电脑和多应用环境中完成任务”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2404-OSWorld Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments\|OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments]] | 2024 | `p0` | `deep` | `agent/os-agent, agent/multimodal, eval/agent-benchmark, env/os` |

### 10. 具身 Agent

回答“语言规划如何落到物理可执行动作”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2204-SayCan Grounding Language in Robotic Affordances\|Do As I Can, Not As I Say: Grounding Language in Robotic Affordances]] | 2022 | `p1` | `skim` | `agent/embodied-agent, agent/reasoning-planning, env/robot` |

### 11. 通用 Agent Benchmark

回答“Agent 作为完整系统在多环境、多工具、多步任务中的能力边界”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2308-AgentBench Evaluating LLMs as Agents\|AgentBench: Evaluating LLMs as Agents]] | 2023 | `p0` | `deep` | `eval/agent-benchmark, agent/tool-use` |
| [[2311-GAIA a benchmark for General AI Assistants\|GAIA: a benchmark for General AI Assistants]] | 2023 | `p0` | `deep` | `eval/agent-benchmark, agent/general-assistant, env/web` |
| [[2406-tau-bench A Benchmark for Tool-Agent-User Interaction in Real-World Domains\|tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains]] | 2024 | `p0` | `deep` | `agent/tool-use, eval/agent-benchmark, eval/reliability, env/business` |

### 12. LLM-as-a-Judge 与开放偏好评测

回答“开放答案没有标准答案时如何评价”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2303-G-Eval NLG Evaluation using GPT-4 with Better Human Alignment\|G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment]] | 2023 | `p1` | `skim` | `eval/llm-judge, eval/open-ended, method/cot` |
| [[2306-MT-Bench and Chatbot Arena Judging LLM-as-a-Judge\|Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena]] | 2023 | `p1` | `skim` | `eval/llm-judge, eval/preference, eval/chatbot` |
| [[2404-Length-Controlled AlpacaEval A Simple Way to Debias Automatic Evaluators\|Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators]] | 2024 | `p1` | `skim` | `eval/llm-judge, eval/preference, eval/bias` |
| [[2606-Ask Dont Judge Binary Questions for Interpretable LLM Evaluation and Self-Improvement\|Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement]] | 2026 | `p1` | `skim` | `eval/llm-judge, eval/open-ended, eval/interpretable, method/binary-question` |

### 13. Agent 安全、可靠性与方法论

回答“Agent 是否安全、稳定、可复现、成本合理”。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2407-AI Agents That Matter\|AI Agents That Matter]] | 2024 | `p0` | `deep` | `eval/cost-reliability, eval/reproducibility, agent/methodology` |
| [[2309-ToolEmu Identifying the Risks of LM Agents with an LM-Emulated Sandbox\|Identifying the Risks of LM Agents with an LM-Emulated Sandbox]] | 2023 | `p1` | `skim` | `eval/safety, agent/tool-use, method/sandbox` |
| [[2412-Agent-SafetyBench Evaluating the Safety of LLM Agents\|Agent-SafetyBench: Evaluating the Safety of LLM Agents]] | 2024 | `p1` | `skim` | `eval/safety, agent/safety, eval/agent-benchmark` |
| [[2410-AgentHarm A Benchmark for Measuring Harmfulness of LLM Agents\|AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents]] | 2024 | `p1` | `skim` | `eval/safety, agent/safety` |

### 14. 综述与总览

用于建立全局地图和查漏补缺。

| 论文 | 年份 | 优先级 | 阅读方式 | 关键标签 |
|---|---:|---|---|---|
| [[2503-Survey on Evaluation of LLM-based Agents\|Survey on Evaluation of LLM-based Agents]] | 2025 | `p0` | `deep` | `eval/agent-benchmark, agent/methodology` |

---

## 四、按优先级

### p0

- [[1706-Attention Is All You Need|Attention Is All You Need]]
- [[1801-Improving Language Understanding by Generative Pre-Training|Improving Language Understanding by Generative Pre-Training]]
- [[1901-Language Models are Unsupervised Multitask Learners|Language Models are Unsupervised Multitask Learners]]
- [[2005-Language Models are Few-Shot Learners|Language Models are Few-Shot Learners]]
- [[2303-GPT-4 Technical Report|GPT-4 Technical Report]]
- [[2601-OpenAI GPT-5 System Card|OpenAI GPT-5 System Card]]
- [[2405-DeepSeek-V2 A Strong Economical and Efficient Mixture-of-Experts Language Model|DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model]]
- [[2412-DeepSeek-V3 Technical Report|DeepSeek-V3 Technical Report]]
- [[2501-DeepSeek-R1 Incentivizing Reasoning Capability in LLMs via Reinforcement Learning|DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning]]
- [[2606-DeepSeek-V4 Towards Highly Efficient Million-Token Context Intelligence|DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence]]
- [[2201-Chain-of-Thought Prompting Elicits Reasoning in Large Language Models|Chain-of-Thought Prompting Elicits Reasoning in Large Language Models]]
- [[2205-MRKL Systems|MRKL Systems: A modular, neuro-symbolic architecture]]
- [[2210-ReAct Synergizing Reasoning and Acting in Language Models|ReAct: Synergizing Reasoning and Acting in Language Models]]
- [[2308-AgentBench Evaluating LLMs as Agents|AgentBench: Evaluating LLMs as Agents]]
- [[2308-AutoGen Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework|AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation Framework]]
- [[2303-CAMEL Communicative Agents for Mind Exploration of Large Language Model Society|CAMEL: Communicative Agents for Mind Exploration of Large Language Model Society]]
- [[2311-GAIA a benchmark for General AI Assistants|GAIA: a benchmark for General AI Assistants]]
- [[2304-Generative Agents Interactive Simulacra of Human Behavior|Generative Agents: Interactive Simulacra of Human Behavior]]
- [[2308-MetaGPT Meta Programming for A Multi-Agent Collaborative Framework|MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework]]
- [[2303-Reflexion Language Agents with Verbal Reinforcement Learning|Reflexion: Language Agents with Verbal Reinforcement Learning]]
- [[2310-SWE-bench Can Language Models Resolve Real-World GitHub Issues|SWE-bench: Can Language Models Resolve Real-World GitHub Issues?]]
- [[2302-Toolformer Language Models Can Teach Themselves to Use Tools|Toolformer: Language Models Can Teach Themselves to Use Tools]]
- [[2305-Tree of Thoughts Deliberate Problem Solving with Large Language Models|Tree of Thoughts: Deliberate Problem Solving with Large Language Models]]
- [[2305-Voyager An Open-Ended Embodied Agent with Large Language Models|Voyager: An Open-Ended Embodied Agent with Large Language Models]]
- [[2307-WebArena A Realistic Web Environment for Building Autonomous Agents|WebArena: A Realistic Web Environment for Building Autonomous Agents]]
- [[2407-AI Agents That Matter|AI Agents That Matter]]
- [[2404-OSWorld Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments|OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments]]
- [[2406-tau-bench A Benchmark for Tool-Agent-User Interaction in Real-World Domains|tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains]]
- [[2501-Humanitys Last Exam|Humanity's Last Exam]]
- [[2503-Survey on Evaluation of LLM-based Agents|Survey on Evaluation of LLM-based Agents]]

### p1

- [[2401-DeepSeek LLM Scaling Open-Source Language Models with Longtermism|DeepSeek LLM: Scaling Open-Source Language Models with Longtermism]]
- [[2009-MMLU Measuring Massive Multitask Language Understanding|Measuring Massive Multitask Language Understanding]]
- [[2112-WebGPT Browser-assisted question-answering with human feedback|WebGPT: Browser-assisted question-answering with human feedback]]
- [[2206-BIG-bench Beyond the Imitation Game|Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models]]
- [[2204-SayCan Grounding Language in Robotic Affordances|Do As I Can, Not As I Say: Grounding Language in Robotic Affordances]]
- [[2211-HELM Holistic Evaluation of Language Models|Holistic Evaluation of Language Models]]
- [[2211-PAL Program-aided Language Models|PAL: Program-aided Language Models]]
- [[2203-Self-Consistency Improves Chain of Thought Reasoning in Language Models|Self-Consistency Improves Chain of Thought Reasoning in Language Models]]
- [[2308-AgentVerse Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors|AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors]]
- [[2307-ChatDev Communicative Agents for Software Development|ChatDev: Communicative Agents for Software Development]]
- [[2303-G-Eval NLG Evaluation using GPT-4 with Better Human Alignment|G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment]]
- [[2311-GPQA A Graduate-Level Google-Proof QA Benchmark|GPQA: A Graduate-Level Google-Proof Q&A Benchmark]]
- [[2305-Gorilla Large Language Model Connected with Massive APIs|Gorilla: Large Language Model Connected with Massive APIs]]
- [[2303-HuggingGPT Solving AI Tasks with ChatGPT and its Friends in Hugging Face|HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face]]
- [[2309-ToolEmu Identifying the Risks of LM Agents with an LM-Emulated Sandbox|Identifying the Risks of LM Agents with an LM-Emulated Sandbox]]
- [[2305-Multiagent Debate Improving Factuality and Reasoning in Language Models|Improving Factuality and Reasoning in Language Models through Multiagent Debate]]
- [[2306-MT-Bench and Chatbot Arena Judging LLM-as-a-Judge|Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena]]
- [[2310-LATS Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models|Language Agent Tree Search Unifies Reasoning Acting and Planning in Language Models]]
- [[2310-MemGPT Towards LLMs as Operating Systems|MemGPT: Towards LLMs as Operating Systems]]
- [[2306-Mind2Web Towards a Generalist Agent for the Web|Mind2Web: Towards a Generalist Agent for the Web]]
- [[2310-SOTOPIA Interactive Evaluation for Social Intelligence in Language Agents|SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents]]
- [[2303-Self-Refine Iterative Refinement with Self-Feedback|Self-Refine: Iterative Refinement with Self-Feedback]]
- [[2307-ToolLLM Facilitating Large Language Models to Master Real-world APIs|ToolLLM: Facilitating Large Language Models to Master Real-world APIs]]
- [[2412-Agent-SafetyBench Evaluating the Safety of LLM Agents|Agent-SafetyBench: Evaluating the Safety of LLM Agents]]
- [[2410-AgentHarm A Benchmark for Measuring Harmfulness of LLM Agents|AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents]]
- [[2404-Length-Controlled AlpacaEval A Simple Way to Debias Automatic Evaluators|Length-Controlled AlpacaEval: A Simple Way to Debias Automatic Evaluators]]
- [[2401-VisualWebArena Evaluating Multimodal Agents on Realistic Visual Web Tasks|VisualWebArena: Evaluating Multimodal Agents on Realistic Visual Web Tasks]]
- [[2401-WebVoyager Building an End-to-End Web Agent with Large Multimodal Models|WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models]]
- [[2403-WorkArena How Capable Are Web Agents at Solving Common Knowledge Work Tasks|WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?]]
- [[2504-BrowseComp A Simple Yet Challenging Benchmark for Browsing Agents|BrowseComp: A Simple Yet Challenging Benchmark for Browsing Agents]]
- [[2606-Ask Dont Judge Binary Questions for Interpretable LLM Evaluation and Self-Improvement|Ask, Don't Judge: Binary Questions for Interpretable LLM Evaluation and Self-Improvement]]

### p2

- [[1804-GLUE A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding|GLUE: A Multi-Task Benchmark and Analysis Platform for Natural Language Understanding]]
- [[1905-SuperGLUE A Stickier Benchmark for General-Purpose Language Understanding Systems|SuperGLUE: A Stickier Benchmark for General-Purpose Language Understanding Systems]]

---

## 五、Dataview 查询示例

如果启用了 Obsidian Dataview，可以直接复制下面的查询。

### P0 精读论文

```dataview
TABLE year, primary_category, read_type
FROM "02-agent" OR "03-basemodel"
WHERE type = "paper" AND priority = "p0"
SORT year ASC
```

### Agent Benchmark

```dataview
TABLE year, priority, read_type
FROM "02-agent" OR "03-basemodel"
WHERE contains(tags, "eval/agent-benchmark")
SORT year ASC
```

### 多智能体论文

```dataview
TABLE year, priority, read_type
FROM "02-agent" OR "03-basemodel"
WHERE contains(tags, "agent/multi-agent")
SORT year ASC
```

### 安全与可靠性

```dataview
TABLE year, priority, read_type
FROM "02-agent" OR "03-basemodel"
WHERE contains(tags, "eval/safety") OR contains(tags, "eval/cost-reliability")
SORT year ASC
```
