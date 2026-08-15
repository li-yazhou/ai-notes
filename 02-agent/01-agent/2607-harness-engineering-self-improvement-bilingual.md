# Harness 工程与自我改进（中英对照）

> **原文标题：** Harness Engineering for Self-Improvement
> **作者：** Lilian Weng
> **原文链接：** https://lilianweng.github.io/posts/2026-07-04-harness/
> 排版：每段英文原文在前，中文翻译紧随其后。

The concept of recursive self-improvement (RSI) dates back to I. J. Good (1965), where he defined an “ultraintelligent machine” as a system that can surpass humans in all intellectual activities and design better machines to improve itself. Yudkowsky (2008) used the phrase “recursive self-improvement” for a specific feedback loop: an AI uses its current intelligence to improve the cognitive machinery that produces its intelligence.

递归式自我改进（Recursive Self-Improvement, RSI）的概念可以追溯到 I. J. Good（1965），他将"超级智能机器"（ultraintelligent machine）定义为一种能够在所有智力活动中超越人类、并能设计出更好的机器来改进自身的系统。Yudkowsky（2008）用"递归式自我改进"来描述一个特定的反馈回路：AI 利用其当前的智能来改进产生其智能的认知机制。

This feedback loop in modern AI may indicate the model rewriting its own weights directly, or more broadly the model improves the training pipeline and the deployment system, which in turn enables a better successor model with improved performance across economically valuable tasks. The speed of research development in AI has been shown to drastically accelerated in frontier labs (Anthropic; OpenAI).

在现代 AI 中，这一反馈回路可能意味着模型直接重写自己的权重；更广义地说，也可能是模型改进训练流水线和部署系统，从而催生一个在经济上有价值的任务上表现更好的后继模型。前沿实验室（Anthropic；OpenAI）的研究表明，AI 研究发展的速度已被大幅加速。

I explicitly mention “deployment system” because the layer between the raw model and the real-world context seems to be as important as the model’s raw intelligence (i.e. the evals right after pretraining). Harnesses are important components of AI deployment, as shown by successful coding agent products such as Claude Code and Codex. A harness is the system surrounding a base model that orchestrates execution and decides how the model thinks and plans, calls tools and acts, perceives and manages context, stores artifacts, and evaluates results.

我特意提到"部署系统"，是因为原始模型与现实世界情境之间的那一层，似乎与模型的原始智能（即预训练刚结束时的评测结果）同样重要。Harness 是 AI 部署的重要组成部分，Claude Code、Codex 等成功编码智能体产品已经证明了这一点。Harness 就是围绕基础模型构建的系统，它编排执行过程，并决定模型如何思考与规划、如何调用工具与行动、如何感知与管理上下文、如何存储产物以及如何评估结果。

This one post will focus on research around harness engineering and how it contributes to RSI. Much recent work on auto-research, self-improving agents, and evolutionary program search can be organized around this question. Other work on model self-play, synthetic data, test-time training and a broader theme of continual learning also matches the RSI vision (e.g. Yuan et al. 2024, Chen et al. 2024), Zhao et al. 2025, Choi et al. 2026)) but they will not be the focus of this post.

这篇文章将聚焦于 harness 工程相关的研究，以及它如何促进 RSI。近期许多关于自动研究、自我改进智能体以及进化式程序搜索的工作，都可以围绕这个问题来组织。其他关于模型自我对弈、合成数据、测试时训练以及更广义的持续学习主题的工作，也符合 RSI 的愿景（例如 Yuan et al. 2024, Chen et al. 2024, Zhao et al. 2025, Choi et al. 2026），但它们不是本文的重点。


# Harness 设计模式（Harness Design Patterns）

Compared with early agent frameworks, “agent = LLM + memory + tools + planning + action”, harnesses engineering additionally include workflow design (e.g. loop engineering), evaluation, permission controls, and persistent state management. It is no longer only prompt templates, but closer to runtime and software system design: how the model observes, acts, memorizes, checks itself, and improves.

与早期的智能体框架"智能体 = LLM + 记忆 + 工具 + 规划 + 行动"相比，harness 工程还额外包括工作流设计（如循环工程）、评测、权限控制以及持久化状态管理。它不再只是提示词模板，而更接近运行时与软件系统设计：模型如何观察、行动、记忆、自我检查以及改进。

The design should be deliberately simple and generic to enable generalization, likely with reference to existing software engineering practices to benefit from prertaining knowlege. There is also a strong analogy between operating systems and harnesses. Similar to an OS, a harness should encapsulate complicated logic while keeping the interface simple. Meanwhile, configs, tool interfaces and other protocols may gradually become standardized across the industry.

设计应当刻意保持简单和通用，以便实现泛化，并且很可能要参考现有的软件工程实践，以受益于预训练知识。操作系统与 harness 之间也存在强烈的类比关系。类似于操作系统，harness 应当封装复杂的逻辑，同时保持接口简单。与此同时，配置、工具接口和其他协议可能会逐渐在整个行业实现标准化。


## 模式 1：工作流自动化（Workflow Automation）

Defining a workflow in which the model can operate, test, and iterate is a key design for automation. Karpathy’s autoresearch repo (https://github.com/karpathy/autoresearch) is a clean example of how such a workflow can be constructed. A common workflow follows a goal-oriented loop of plan, execute, observe/test, improve, and execute again until the goal is achieved. The process may trigger proactive requests to users for clarity in task specification or execution preference.

定义一种让模型可以在其中操作、测试和迭代的工作流，是自动化设计的关键。Karpathy 的 autoresearch 仓库（https://github.com/karpathy/autoresearch）是构建此类工作流的一个简洁范例。常见的工作流遵循一个目标导向的循环：规划、执行、观察/测试、改进，然后再次执行，直到目标达成。该过程可能会主动向用户发起请求，以澄清任务说明或执行偏好。

> A simplified Codex agent loop: the agent calls tools and tool responses affect the model's next generation. (Image source: OpenAI codex agent post)
> 一个简化的 Codex 智能体循环：智能体调用工具，工具响应会影响模型的下一次生成。
> （图片来源：OpenAI codex agent 博客）

The workflow graph also emphasizes the model analyzing its own trajectories and failure cases and then iterating on its progress through an “agent runtime” rather than a static prompt template.

工作流图还强调模型对自身轨迹（trajectory）和失败案例进行分析，然后通过"智能体运行时"（agent runtime）而非静态的提示词模板来迭代其进展。


## 模式 2：把文件系统当作持久化记忆（File System as Persistent Memory）

A recurring pattern in long-horizon agent systems is simple control over rich states and artifacts. A harness should not carry the entire workflow and all logs in context; instead, it should keep durable state in files. In long-horizon agentic rollout, artifacts such as experiment logs, code diffs, paper summaries, error traces, and past rollout trajectories often grow much longer than the context window that the model has trained for.

在长周期（long-horizon）智能体系统中，一个反复出现的模式是对丰富状态与产物的简单控制。Harness 不应把整个工作流和所有日志都塞进上下文中；相反，它应该把持久状态保存在文件里。在长周期的智能体运行（rollout）中，实验日志、代码差异（diff）、论文摘要、错误追踪和过往的运行轨迹等产物，往往增长到远超模型训练所用上下文窗口的长度。

Learning how to read, write, and edit the file system (commonly via bash commands) is a foundation skill for LLMs, and thus managing persistent memory in the simple form of files naturally benefits from improvements in core model capability.

学会如何读写和编辑文件系统（通常通过 bash 命令）是 LLM 的一项基础技能，因此以文件这种简单形式来管理持久化记忆，自然能从核心模型能力的提升中受益。


## 模式 3：子智能体与后端任务（Sub-agent and Backend Jobs）

A harness can spawn multiple subagents to execute in parallel and monitor backend jobs. This is useful when the main agent needs to search multiple hypotheses, run experiments concurrently, or delegate isolated subtasks without polluting the main context. The parent agent then needs a small process manager: launch jobs, inspect logs, cancel failed runs, and merge results back into the main agent thread.

Harness 可以生成多个子智能体并行执行，并监控后端任务。当主智能体需要搜索多个假设、并发运行实验，或在不污染主上下文的情况下委派隔离的子任务时，这一模式非常有用。父智能体随后需要一个小型进程管理器：启动任务、检查日志、取消失败的运行，并将结果合并回主智能体线程。

The key design choice is to make parallelism explicit and inspectable. If subagent outputs only live in a transient chat context, they quickly become obselete and hidden. If they are stored as files, logs, and status records, the model can recover after interruptions and reason over its own execution history.

关键的设计选择是让并行性变得显式且可检查。如果子智能体的输出只存在于临时的聊天上下文中，它们很快就会过时并被隐藏。如果它们被存储为文件、日志和状态记录，模型就可以在中断后恢复，并能对自身的执行历史进行推理。


## 案例研究：编码智能体 Harness（Coding Agent Harness）

The core interface of mainstream coding agents has become stabilized across Claude Code, Codex, OpenCode, and Cursor-style agents. They commonly use a loop like:

主流编码智能体的核心接口已经在 Claude Code、Codex、OpenCode 和 Cursor 风格的智能体中趋于稳定。它们通常使用这样的循环：

With access to a set of tools, the coding agent is able to develop and debug issues in a given repository, similar to how human developers are equipped with IDEs.

有了工具集，编码智能体就能在给定仓库中开发和调试问题，就像人类开发者配备 IDE 一样。

(Not a comprenhensive list; shown for demonstration. Read this if interested.)

（并非完整清单；仅作展示。如有兴趣可阅读原文。）

**英文原表：**

| Group | Tool definitions |
|---|---|
| File system | - File discovery: glob, grep, ls / - File read: read, read_many / - File modification: write (a whole new file); edit (string exact-match replacement); multi_edit; apply_patch (applies a structured patch/diff) |
| Shell execution | Run commands: bash, PowerShell |
| IO | lsp, git tools like git_status, git_diff, git_commit |
| External context | MCP tools, Skills |
| Web search | web_search, web_fetch, browser tools |
| Artifacts | Read docs, images; generate HTML, images |
| Backend processes | Such as: CronCreate, CronDelete, CronList |
| Agent delegation | Such as: spawn_agent, resume_agent, wait_agent, list_agents, close_agent, interrupt_agent, etc. |

---

**中文对照：**

| 分组 | 工具定义 |
|---|---|
| 文件系统 | - 文件发现：glob, grep, ls<br>- 文件读取：read, read_many<br>- 文件修改：write（写入全新文件）；edit（字符串精确匹配替换）；multi_edit；apply_patch（应用结构化的补丁/diff） |
| Shell 执行 | 运行命令：bash, PowerShell |
| IO | lsp，以及 git_status、git_diff、git_commit 等 git 工具 |
| 外部上下文 | MCP 工具、Skills |
| 网页搜索 | web_search, web_fetch, 浏览器工具 |
| 产物（Artifacts） | 读取文档、图片；生成 HTML、图片 |
| 后端进程 | 例如：CronCreate, CronDelete, CronList |
| 智能体委派 | 例如：spawn_agent, resume_agent, wait_agent, list_agents, close_agent, interrupt_agent 等 |


## Harness 层 vs 核心智能？（Harness Layer vs Core Intelligence?）

It is hard to forecast how much the future of RSI will rely on harness engineering, but the near-term path of RSI is unlikely to start as a model directly rewriting its weights. My prediction of a practical near-term path is:

很难预测 RSI 的未来有多大程度依赖于 harness 工程，但 RSI 的近中期路径不太可能始于模型直接重写自身权重。我对切实可行的近期路径的预测是：

- Harness engineering will evolve in the direction of meta-methodology (i.e. improving the machinery for getting better answers, not just improving the answer itself). The harness system itself becomes an optimization target, with fewer heuristic rules and more general mechanisms.
- Harness 工程将朝着"元方法论"（meta-methodology）的方向演进（即改进获取更好答案的机制，而不仅仅是改进答案本身）。Harness 系统本身成为优化目标，更少的启发式规则、更多的通用机制。

- In turn, mature harnesses enable auto-research for model self-improvement loop and smarter models prevents harnesses from overengineering and keep the system sustainable.
- 反过来，成熟的 harness 能够支持模型自我改进循环中的自动研究；而更聪明的模型又能防止 harness 过度工程化，保持系统的可持续性。

Eventually it is possible that many harness improvements will be internalized into core model behavior, but the interface with external context and tools should remain. We have seen a softer version of this pattern with prompt engineering: manual prompt tricks became less central as instruction tuning and model reasoning improved, but the need to specify goals, constraints, context, and evaluation did not disappear.

最终，许多 harness 的改进可能会被内化到核心模型行为中，但与外部上下文和工具的接口应当保留。我们在提示词工程上已经看到了这一模式的较柔和版本：随着指令微调和模型推理能力的提升，手工提示词技巧变得不那么重要，但对目标、约束、上下文和评测的指定需求并没有消失。


# Harness 优化（Harness Optimization）

The progression in the object being optimized in the harness system is roughly: instruction prompts → structured context → workflow → harness code → optimizer code. As the model becomes more intelligent and powerful, we move toward more complex targets and generic methods.

harness 系统中被优化对象的演进大致是：指令提示词 → 结构化上下文 → 工作流 → harness 代码 → 优化器代码。随着模型变得更加智能和强大，我们走向更复杂的目标和更通用的方法。


## 上下文工程（Context Engineering）

Simply appending all the tool responses and model generations into the context can quickly grow out of control as the agentic job horizon increases significantly. Context management is a layer to construct a more structed and concise context for LLM and manage persistant states. There is no doubt that long-context research will keep on making progress but at the moment long-context intelligence and context engineering sometime intertwines.

随着智能体任务周期大幅增长，简单地把所有工具响应和模型生成都追加到上下文中，很快就会失控。上下文管理是一个构建更结构化、更简洁的 LLM 上下文并管理持久状态的层。毫无疑问，长上下文研究会持续取得进展，但眼下长上下文智能与上下文工程有时相互交织。

Agentic Context Engineering (ACE; Zhang et al. 2025) treats context as an evolving playbook rather than an increasingly lengthening prompt. It has three components to maintain one context playbook of bullet points, each with an identifier and a description.

智能体上下文工程（Agentic Context Engineering, ACE；Zhang et al. 2025）把上下文视为一份不断演进的"战术手册"（playbook），而不是一个越来越长的提示词。它由三个组件维护一份由要点条目组成的上下文手册，每个条目都有一个标识符和描述。

- Generator: produces task trajectories, with reference to bullet points.
- 生成器（Generator）：参照要点条目，产生任务轨迹。

- Reflector: distills insights from successful and failed trajectories.
- 反思器（Reflector）：从成功和失败的轨迹中提炼洞见。

- Curator: updates the structured context with incremental, itemized entries.
- 策展器（Curator）：以增量的、逐条的方式更新结构化上下文。

> The framework of Agentic Context Engineering (ACE). (Image source: Zhang et al. 2025)
> 智能体上下文工程（ACE）的框架。（图片来源：Zhang et al. 2025）

To prevent context collapse and brevity bias during iterative rewrites, one key design choice in ACE is that the curator does not rewrite a full prompt blob. It instead outputs a collection of structured, itemized bullets in the form of (identifier, description), and these bullets are merged into a structured context logbook with deterministic logic. The context items are refined and deduplicated periodically.

为防止迭代重写过程中的上下文坍缩和简洁性偏差，ACE 的一个关键设计选择是：策展器不重写整块提示词。相反，它输出一组结构化、逐条化的要点，形式为（标识符，描述），这些要点通过确定性逻辑合并到结构化的上下文日志中。上下文条目会被定期精炼和去重。

The fact that ACE learns insights from rollouts helps us move toward self-managed memory, but the update rules and the overall workflow are still handcrafted. To move toward a more self-improving loop, Meta Context Engineering (MCE; Ye et al. 2026) separates the mechanism (how to manage context) from the artifact content (what is in context), running skill evolution at the meta-optimization level and context optimization at the base level.

ACE 从运行（rollout）中学习洞见这一事实，帮助我们走向自我管理的记忆，但更新规则和整体工作流仍是手工打造的。为了走向更自我改进的循环，元上下文工程（Meta Context Engineering, MCE；Ye et al. 2026）把机制（如何管理上下文）与产物内容（上下文里有什么）分离开来，在元优化层面进行技能进化，在基础层面进行上下文优化。

An MCE skill $s \in \mathcal{S}$ defines a context function $c_s=(\rho_s,F_s)$ and maps an input $x$ to context $c = F_s(x;\rho_s)$, where:

一个 MCE 技能 $s \in \mathcal{S}$ 定义了一个上下文函数 $c_s=(\rho_s,F_s)$，将输入 $x$ 映射为上下文 $c = F_s(x;\rho_s)$，其中：

- $\rho_s = \{\rho_1,\dots,\rho_m\}$ are static components (prompts, knowledge bases, code libraries).
- $\rho_s = \{\rho_1,\dots,\rho_m\}$ 是静态组件（提示词、知识库、代码库）。

- $F_s = \{F_1,\dots,F_k\}$ are dynamic operators (search, selection, filtering, formatting).
- $F_s = \{F_1,\dots,F_k\}$ 是动态算子（搜索、选择、过滤、格式化）。

The bi-level optimization is to find the best context $c_s^*$ given skill $s$ on the training data, while the outer loop finds the optimal skill that provides the best performance on the validation set:

双层优化（bi-level optimization）是在给定技能 $s$ 和训练数据的情况下，找到最优上下文 $c_s^*$；而外层循环则找到能在验证集上提供最佳表现的技能：

$$
\text{Inner: }c_s^*=\arg\max_{c_s}J_\text{train}(c_s;s)\quad
\text{Outer: }s^*=\arg\max_{s\in\mathcal{S}}J_\text{val}(c_s^*)
$$

The skill database tracks the history of previous skills, context functions and eval metrics $\mathcal{H}_{k-1} = \{(s_i,c_i,J_i^\text{train}, J_i^\text{val})\}_{i=1}^{k-1}$. A meta-level agent performs agentic crossover over prior skills to create a new skill given a task $\tau$: $s_k=\text{crossover}(\tau,\mathcal{H}_{k-1})$.

技能数据库跟踪过往技能、上下文函数和评测指标的历史 $\mathcal{H}_{k-1} = \{(s_i,c_i,J_i^\text{train}, J_i^\text{val})\}_{i=1}^{k-1}$。元层智能体对先前的技能进行智能体式交叉（crossover），为给定任务 $\tau$ 生成新技能：$s_k=\text{crossover}(\tau,\mathcal{H}_{k-1})$。

Then a base-level context engineer executes the skill $s_k$ and learns the context function from rollout feedback $\mathcal{R}_k$, guided by the current skill: $c_k=\text{engineer}(\tau,s_k;c_{k-1}^*,\mathcal{R}_k)$.

然后，基础层的上下文工程师执行技能 $s_k$，并在当前技能的引导下，从运行反馈 $\mathcal{R}_k$ 中学习上下文函数：$c_k=\text{engineer}(\tau,s_k;c_{k-1}^*,\mathcal{R}_k)$。

> The framework of Meta Context Engineering (MCE): meta-level skill evolution searches over context-management mechanisms, while the base level optimizes the task context. (Image source: Ye et al. 2026)
> 元上下文工程（MCE）的框架：元层技能进化搜索上下文管理机制，而基础层优化任务上下文。（图片来源：Ye et al. 2026）

MCE does not enforce a heuristic rule for how to structure context as ACE does. It uses free-form skills to store the most important knowledge for a task, and evolves the skill and the skill-conditioned context iteratively together. Implementation-wise, a context function $c$ is instantiated as a collection of files in a dedicated directory, including both static (skill.md) and dynamic (context and data rollouts) components. Both meta-level and base-level optimization are executed in agentic coding envs with a standard tool set,

MCE 不像 ACE 那样对如何组织上下文强制执行启发式规则。它使用自由形式的技能来存储任务最重要的知识，并让技能与技能条件化上下文一起迭代进化。在实现层面，上下文函数 $c$ 被实例化为专用目录中的一组文件，包括静态组件（skill.md）和动态组件（上下文与数据运行）。元层和基础层的优化都在智能体编码环境中执行，使用一组标准工具：

$$
\mathcal{T}=\{\texttt{Read},\texttt{Write},\texttt{Edit},\texttt{Bash},\texttt{Glob},\texttt{Grep},\texttt{TodoWrite}\}
$$

Meta-Harness (Lee et al. 2026) moves another level deeper: the optimized object is the code that determines and optimizes what information should be stored, retrieved, and presented to the model. “Meta-” in its name means it is a harness for optimizing harnesses.

Meta-Harness（Lee et al. 2026）再深入了一层：被优化的对象是决定并优化"应存储、检索和呈现给模型的哪些信息"的代码。其名称中的"Meta-"意味着它是用来优化 harness 的 harness。

> The Meta-Harness outer-loop optimization algorithm. (Image source: Lee et al. 2026)
> Meta-Harness 的外层循环优化算法。（图片来源：Lee et al. 2026）

The proposer for creating a new harness is itself a coding agent and the final output is a collection of harness candidates on the Pareto frontier.

用于创建新 harness 的提议者（proposer）本身就是一个编码智能体，最终输出是帕累托前沿（Pareto frontier）上的一组 harness 候选。

- The entire execution history is accessible via a file system, and thus the coding agent uses commands like grep or cat to read through it instead of shoveling everything into a single prompt context.
- 整个执行历史都可以通过文件系统访问，因此编码智能体使用 grep 或 cat 等命令来阅读历史，而不是把所有东西都塞进单一提示词上下文。

- The proposed harness is a dictionary in the file system containing its own source code, scores, rollout trajectories, and state updates.
- 提议的 harness 是文件系统中的一个字典（目录），包含其自身的源代码、得分、运行轨迹和状态更新。

- The mete-harness loop iteratively creates new harnesses, and only qualified ones are kept.
- Meta-harness 循环迭代地创建新 harness，只保留合格的。

> The performance of Meta-Harness on (Left) text classification with a small number of iterations and (Right) TerminalBench-2. Note that the search in the TerminalBench-2 experiment is initialized from Terminus-KIRA and Terminus-2, two very strong harnesses. (Image source: Lee et al. 2026)
> Meta-Harness 在（左）少量迭代下的文本分类，和（右）TerminalBench-2 上的表现。注意 TerminalBench-2 实验中的搜索是从 Terminus-KIRA 和 Terminus-2 这两个非常强的 harness 初始化的。（图片来源：Lee et al. 2026）

Still, the important lesson is clear: once harness design becomes an executable search space, a strong coding agent can exploit the same design space human engineers use.

尽管如此，重要的教训是清晰的：一旦 harness 设计成为一个可执行的搜索空间，一个强大的编码智能体就能利用人类工程师所使用的同一个设计空间。


## 工作流设计（Workflow Design）

Workflow design in harness engineering can be handcrafted by domain experts. Taking auto-research as an example, various frameworks have been proposed and tested. The AI Scientist system (Lu et al. 2026) builds a pipeline to propose research ideas, write code, run experiments, analyze results, write a manuscript, and perform peer review. Meng et al. (2026) make verifiability the central design constraint in ScientistOne, where every claim (citation, numerical, methodological, conclusion) must trace to an evidence source and is audited by Chain-of-Evidence checks.

Harness 工程中的工作流设计可以由领域专家手工完成。以自动研究为例，已经提出了并测试了各种框架。AI Scientist 系统（Lu et al. 2026）构建了一条流水线：提出研究想法、编写代码、运行实验、分析结果、撰写论文稿件、进行同行评审。Meng et al.（2026）在 ScientistOne 中把可验证性作为核心设计约束，其中每一个主张（引用、数值、方法论、结论）都必须追溯到证据来源，并通过"证据链"（Chain-of-Evidence）检查进行审计。

> AI Scientist pipeline for idea generation, experimentation, paper writing, and review. (Image source: Lu et al. 2026)
> AI Scientist 流水线：想法生成、实验、论文写作与评审。（图片来源：Lu et al. 2026）

The Autodata agent (Kulikov et al. 2026) is designed to work as a data scientist for generating training and evaluation data. The main agent manages a challenger that proposes problems, a weak solver, a strong solver, and a verifier/judge, aiming to synthesize data at the “just right” level of difficulty, meaning that the strong solver succeeds but the weak solver fails.

Autodata 智能体（Kulikov et al. 2026）被设计为一位数据科学家，用于生成训练和评估数据。主智能体管理一个提出问题的挑战者（challenger）、一个弱求解器（weak solver）、一个强求解器（strong solver）以及一个验证器/裁判（verifier/judge），目标是以"恰到好处"的难度合成数据——即强求解器能成功、而弱求解器会失败的难度。

In Autodata, the challenger prompt is updated iteratively according to feedback from the solvers and verifier. The limitation here is that synthesized tasks are used to fine-tune weak solvers but not strong solvers; if the loop cannot iteratively improve the strong model, it is more like indirect distillation over a generated prompt distribution, with less RSI flavor.

在 Autodata 中，挑战者提示词会根据求解器和验证器的反馈进行迭代更新。这里的局限是：合成任务被用来微调弱求解器，而非强求解器；如果循环无法迭代地改进强模型，它就更像是在生成的提示词分布上进行间接蒸馏，RSI 的味道较弱。

> Autodata agentic workflow design for generating synthetic training and evaluation data around challenger, solver, and verifier roles. (Image source: Kulikov et al. 2026)
> Autodata 智能体工作流设计：围绕挑战者、求解器和验证器角色生成合成训练与评估数据。（图片来源：Kulikov et al. 2026）

The design space for workflow is enormous, and naturally we can think of workflow design as a search problem, and therefore we should be able to find good solutions by algorithms rather than only manually craft them. Following this direction, Automated Design of Agentic Systems (ADAS; Hu et al. 2025) formulates agent design itself as an optimization problem, “meta-agent search” where a meta-agent proposes new designs of agentic workflows.

工作流的设计空间极其庞大，我们自然可以把工作流设计看作一个搜索问题，因此应该能够通过算法而非仅靠手工来找到好的解决方案。沿着这个方向，智能体系统自动化设计（Automated Design of Agentic Systems, ADAS；Hu et al. 2025）把智能体设计本身形式化为一个优化问题，即"元智能体搜索"（meta-agent search）：由一个元智能体提出智能体工作流的新设计。

- Initialize an archive of agentic workflows with simple agents such as CoT and self-refine.
- 用 CoT、self-refine 等简单智能体初始化一个智能体工作流存档（archive）。

- Ask a meta-agent to program new agents, all in code, inspired by existing solutions in the archive.
- 请元智能体受存档中现有解决方案的启发，以纯代码方式编写新智能体。

- The meta-agent first generates a high-level description of the new workflow, and then implements it in code.
- 元智能体首先生成新工作流的高层描述，然后用代码实现。

- The draft program then goes through two self-refine steps (i.e. ask the model to provide feedback and then ask the same model to refine the previously generated outputs based on the feedback; Madaan et al. 2023) by the meta-agent to check its novelty.
- 草稿程序随后经过元智能体的两个 self-refine 步骤（即让模型提供反馈，再让同一模型基于反馈精炼先前生成的输出；Madaan et al. 2023）来检查其新颖性。

- Evaluate each new candidate and add successful ones back to the archive.
- 评估每个新候选，并将成功的加回存档。

- Repeat steps 2-3 until the maximum iteration count is reached.
- 重复步骤 2-3，直到达到最大迭代次数。

> Illustration of Automated Design of Agentic Systems (ADAS). (Image source: Hu et al. 2025)
> 智能体系统自动化设计（ADAS）的示意图。（图片来源：Hu et al. 2025）

AFlow (Zhang et al. 2025) represents an agentic workflow as a graph, where nodes represent LLM-invoking actions and edges implement logical operations in code. The workflow optimization relies on MCTS (Monte Carlo Tree Search):

AFlow（Zhang et al. 2025）将智能体工作流表示为图：节点是调用 LLM 的动作，边以代码实现逻辑运算。工作流优化依赖于 MCTS（蒙特卡洛树搜索）：

- Initialize the starting workflow $W_0$ in the tree with a template.
- 在树中以模板初始化起始工作流 $W_0$。

- Select a workflow node using a soft mixture of score and uniform exploration.
- 使用得分与均匀探索的软混合方式选择一个工作流节点。

- Expand it by asking an LLM to produce a modified workflow conditioned on its evaluation performance.
- 让 LLM 基于其评估表现生成一个修改后的工作流，从而扩展该节点。

- Execute and evaluate the new workflow.
- 执行并评估新工作流。

- Add it back to the tree if the new workflow shows improvement within a budget of $N$ rounds.
- 如果新工作流在 $N$ 轮预算内展现出改进，就把它加回树中。

- Repeat steps 2-5 and stop when the top-$k$ average score plateaus or hit the budget.
- 重复步骤 2-5，直到 top-$k$ 平均得分趋于平稳或触及预算。

> AFlow optimization process over a tree of workflow candidates. (Image source: Zhang et al. 2025)
> AFlow 在工作流候选树上的优化过程。（图片来源：Zhang et al. 2025）

Experiments of AFlow in QA, code, and math tasks showed decent improvement of AFlow over manually designed workflows and ADAS.

AFlow 在 QA、代码和数学任务上的实验显示，它相比手工设计的工作流和 ADAS 有可观的改进。

> AFlow experiments in comparison to manual methods and ADAS. (Image source: Zhang et al. 2025)
> AFlow 与手工方法及 ADAS 的对比实验。（图片来源：Zhang et al. 2025）


## 自我改进的 Harness（Self-Improving Harness）

Either context engineering or workflow design is only one part of a harness. We need to search through the entire design space and optimize context-management logic, workflow, permissions, and many other harness components together. As we have seen in work like Meta-Harness, ADAS, and AFlow, ✨code✨ is a universal language for defining programs and systems. In simple words, a harness is code that programs how prompts, tool calls, subagents, control flow, memory, and workflow logic work together. If an LLM can optimize the code that executes agents, it can access a much larger design space than hand-written prompts.

无论是上下文工程还是工作流设计，都只是 harness 的一部分。我们需要搜索整个设计空间，把上下文管理逻辑、工作流、权限和其他许多 harness 组件放在一起优化。正如我们在 Meta-Harness、ADAS 和 AFlow 等工作中看到的，✨代码✨是定义程序和系统的通用语言。简言之，harness 就是代码，它编排提示词、工具调用、子智能体、控制流、记忆和工作流逻辑如何协同工作。如果 LLM 能优化执行智能体的代码，它就能触及比手写提示词大得多的设计空间。

Self-Taught Optimizer (STOP; Zelikman et al. 2023) is one of the early examples of recursive scaffolding improvement. A seed improver $I_0$ at step $t=0$ takes an initial solution $s$, a utility function $u$, and a black-box language model $M$, and returns an improved solution $s’$, that is, $s’ = I(u, s; M)$. The goal of STOP is not directly to improve $s$ but to improve the improver $I$ itself.

自学优化器（Self-Taught Optimizer, STOP；Zelikman et al. 2023）是递归脚手架改进的早期例子之一。在 $t=0$ 时刻，一个种子改进器（seed improver）$I_0$ 接受初始解 $s$、效用函数 $u$ 和一个黑盒语言模型 $M$，返回改进后的解 $s'$，即 $s' = I(u, s; M)$。STOP 的目标不是直接改进 $s$，而是改进改进器 $I$ 本身。

First, let’s define the meta-utility as the average utility of a given improver function $I$ over a collection of downstream tasks $\mathcal{D}$:

首先，把元效用（meta-utility）定义为给定改进器函数 $I$ 在一组下游任务 $\mathcal{D}$ 上的平均效用：

$$
\hat{u}(I) \triangleq \frac{1}{\vert\mathcal{D}\vert}\mathbb{E}_{(u,s)\sim \mathcal{D}}[u(I(u,s; M))]
$$

Because improving the improver function is an optimization problem itself, we can recursively get a new version of $I_t$ based on $I_{t-1}$’s performance measured by meta-utility via a self-improvement update:

因为改进改进器函数本身就是一个优化问题，我们可以根据 $I_{t-1}$ 在元效用度量下的表现，通过自我改进更新递归地得到 $I_t$ 的新版本：

$$
I_t=I_{t-1}(\hat{u},I_{t-1};M)
$$

> Algorithm of Self-Taught Optimizer (STOP). (Image source: Zelikman et al. 2023)
> 自学优化器（STOP）的算法。（图片来源：Zelikman et al. 2023）

In their experiments, the improved improver discovered various strategies, such as genetic algorithms, decomposing and improving parts, multi-armed prompt bandits, simulated annealing, varying temperature, and beam/tree search. This is analogous to how a harness workflow can be represented as an object for optimization.

在他们的实验中，改进后的改进器发现了各种策略，例如遗传算法、分解并改进各部分、多臂提示词老虎机（bandit）、模拟退火、温度变化以及束搜索/树搜索。这与 harness 工作流可以作为优化对象来表示的方式类似。

> Examples of self-improvement strategies discovered by STOP. (Image source: Zelikman et al. 2023)
> STOP 发现的一些自我改进策略示例。（图片来源：Zelikman et al. 2023）

A cautionary result in Zelikman et al. (2023)’s findings is that STOP improved mean downstream performance across iterations with GPT-4 but degraded with weaker models like GPT-3.5 and Mixtral. Recursive structure alone is not enough. The base model must be capable enough to improve the mechanism. This implies that harness improvement enables better deployment of the model but intelligence is still the core.

Zelikman et al.（2023）的发现中一个值得警惕的结果是：使用 GPT-4 时 STOP 在迭代中提升了平均下游表现，但使用 GPT-3.5、Mixtral 等较弱的模型时表现反而下降。仅靠递归结构是不够的。基础模型必须足够有能力来改进机制。这意味着 harness 的改进能带来更好的模型部署，但智能仍然是核心。

Lin et al. (2026) investigated the dependency of harness evolution on model capabilities in more details. They disentangled two axes: (1) harness-updating refers to the capability of producing useful harness edits and (2) harness-benefit denotes the capability of utilizing the updated harness, to achieve better task solving. Interestingly a range of model of different sizes and core intelligence, from Qwen3.5-9B to Claude Opus 4.6, were observed in their experiments to show similar harness updating capability; the 9B harness proposer/evolver is able to write a skill procedurally isomorphic to Opus. To best utilize a harness, a model needs to invoke skills/tools correctly and timely and be good at long-horizon instruction following.

Lin et al.（2026）更详细地研究了 harness 进化对模型能力的依赖。他们解耦了两个维度：（1）harness 更新能力（harness-updating），指产生有用的 harness 编辑的能力；（2）harness 收益能力（harness-benefit），指利用更新后的 harness 来更好地完成任务求解的能力。有趣的是，从 Qwen3.5-9B 到 Claude Opus 4.6，不同大小和核心智能水平的模型，在他们的实验中表现出相似的 harness 更新能力；9B 的 harness 提议者/进化器能够写出与 Opus 程序同构的技能。而要最好地利用 harness，模型需要正确且及时地调用技能/工具，并擅长长周期的指令跟随。

> Main results: (A) harness updating capability is measured flat across a range of models from Qwen2-32B to Opus 4.6; (B) harness benefit capability is non-monotonic where middle tier models benefit the most. (Image source: Lin et al. 2026)
> 主要结果：（A）从 Qwen2-32B 到 Opus 4.6 的一系列模型，harness 更新能力被测量为持平；（B）harness 收益能力是非单调的，中等层级的模型受益最大。（图片来源：Lin et al. 2026）

A more recent work, Self-Harness (Zhang et al. 2026), relies on LLM agents to improve their own harness via a propose-evaluate-accept loop.

更近期的研究 Self-Harness（Zhang et al. 2026）依赖 LLM 智能体通过"提出-评估-接受"循环来改进自身的 harness。

> Self-Harness uses a loop of weakness mining, bounded harness proposal, and validation to update a harness. (Image source: Zhang et al. 2026)
> Self-Harness 使用弱点挖掘、有界 harness 提议和验证的循环来更新 harness。（图片来源：Zhang et al. 2026）

The loop in Self-Harness has three stages:

Self-Harness 的循环分为三个阶段：

- Weakness mining: cluster failures into verifier-grounded failure patterns.
- 弱点挖掘：把失败聚类为基于验证器的失败模式。

- The current harness $h_t$ is used to evaluate on tasks and execution traces are collected for analysis.
- 当前 harness $h_t$ 被用来在任务上评估，并收集执行轨迹进行分析。

- Note that two runs can share the same verifier outcome in the error logs on the surface, such as timeout or missing artifact, while having different causal mechanisms. Therefore we need a failure record of rich information, containing the terminal verifier-level cause, the causal status of the relevant agent behavior, and the abstract agent mechanism exposed by the trace, to uncover the root causes.
- 注意，两次运行在错误日志表面上可能共享相同的验证器结果（如超时或缺少产物），但因果机制却不同。因此，我们需要一份信息丰富的失败记录，包含终端验证器层面的原因、相关智能体行为的因果状态，以及轨迹暴露出的抽象智能体机制，以揭示根本原因。

- Harness proposal: propose bounded harness edits based on mined failure patterns.
- Harness 提议：基于挖掘出的失败模式，提出有界的 harness 编辑。

- The same model is invoked under $h_t$ as a proposer.
- 在 $h_t$ 下调用同一个模型作为提议者。

- The model is provided with a bounded proposal context: (1) the editable surfaces of the current harness, (2) the verifier-grounded failure patterns from the evaluation system, (3) records of passing behaviors that should be preserved, and (4) summaries of previously attempted edits.
- 模型被提供一个有界的提议上下文：（1）当前 harness 可编辑的表面；（2）来自评估系统的基于验证器的失败模式；（3）应保留的通过行为的记录；（4）先前尝试过的编辑的摘要。

- Harness edits should prefer recurrent error patterns that are addressable (e.g. not task-specific difficulty) and can be resolved by narrow changes.
- Harness 编辑应优先处理可处理（例如不是任务特异的难度）且能通过窄范围修改解决的反复出现的错误模式。

- Harness edit candidates should be distinct and diverse.
- Harness 编辑候选应当独特且多样。

- Proposal validation: validate and merge qualified edits to create a new harness $h_{t+1}$.
- 提议验证：验证并合并合格的编辑，以创建新 harness $h_{t+1}$。

- Candidate edits are evaluated by regression tests on held-in $D_\text{in}$ (for testing whether the weakness is resolved) and held-out $D_\text{out}$ (for checking whether other unknown issues were introduced) splits.
- 候选编辑通过回归测试来评估，分为保留集 $D_\text{in}$（测试弱点是否解决）和留出集 $D_\text{out}$（检查是否引入了其他未知问题）。

- Candidates are accepted only if they have no regression on both held-in and held-out data.
- 候选只有在保留集和留出集数据上都没有回归时才被接受。

- Accepted candidates are merged to update the harness to $h_{t+1}$, while rejected candidates are logged without changing the active harness.
- 被接受的候选被合并以将 harness 更新为 $h_{t+1}$，而被拒绝的候选仅被记录，不改变当前活跃的 harness。

When running MiniMax M2.5, Qwen3.5-35B-A3B, and GLM-5 on Terminal-Bench-2, Self-Harness was shown to learn model-specific harness instructions that target at different weaknesses of different base models and improve held-out pass rates.

在 Terminal-Bench-2 上运行 MiniMax M2.5、Qwen3.5-35B-A3B 和 GLM-5 时，Self-Harness 被证明能学习到模型特定的 harness 指令，这些指令针对不同基础模型的不同弱点，并提高了留出集通过率。

Self-harness type of work does raise my concerns that if a program is allowed to edit the OS system, abstraction boundaries are broken. The editable surface needs to be properly designed and the permission control and security layers need to live outside this loop. All the challenges around reward hacking still remain.

Self-harness 这类工作确实引起我的担忧：如果允许程序编辑操作系统，抽象边界就被打破了。可编辑表面需要妥善设计，权限控制和安全层需要位于这个循环之外。所有与奖励破解（reward hacking）相关的挑战依然存在。

Agentic Harness Engineering (AHE; Lin et al. 2026) see the bottlenecks of harness evolution are around observability—that is, when a rollout fails, we need to know which component is responsible for that and every edit should be grounded by evidence.

智能体 Harness 工程（Agentic Harness Engineering, AHE；Lin et al. 2026）认为 harness 进化的瓶颈在于可观测性——也就是说，当一次运行失败时，我们需要知道是哪个组件造成的，而每一次编辑都应有证据支撑。

The framework creates a closed loop with 3 observability pillars:

该框架创建了一个闭环，包含 3 个可观测性支柱：

- Component observability: every editable harness component has a representation in the file system so the action space is explicit and tracable.
- 组件可观测性：每个可编辑的 harness 组件在文件系统中都有表示，因此动作空间是显式且可追踪的。

- A harness contains 7 components: system prompt, tool description, tool implementation, middleware, skill, sub-agent configuration, and long-term memory.
- 一个 harness 包含 7 个组件：系统提示词、工具描述、工具实现、中间件（middleware）、技能、子智能体配置和长期记忆。

- Each failure pattern is mapped to one component so the edit can be more targeted.
- 每个失败模式都映射到一个组件，这样编辑可以更有针对性。

- Experience observability: analysize and summarize a large amount of raw trajectories into a hierarchy of evidence and failure patterns.
- 经验可观测性：将大量原始轨迹分析、总结为证据与失败模式的层级结构。

- Each harness generates $k$ traces.
- 每个 harness 生成 $k$ 条轨迹。

- Use an agent (“Agent debugger”) to analysis the trajectories each stored in one file and generate per-task analysis report on the root cause for the failure or success.
- 使用一个智能体（"Agent debugger"）来分析每条存储在独立文件中的轨迹，为每个任务生成关于失败或成功根本原因的分析报告。

- All the per-task reports are aggregated into a benchmark overview for the next step, and raw traces can be accessed if needed. This layered access structure is more token efficient.
- 所有按任务生成的报告被汇总为下一步的基准概览，必要时可以访问原始轨迹。这种分层访问结构更节省 token。

- Decision observability: every edit is paired with a prediction for the next round to validate.
- 决策可观测性：每次编辑都配对一个下一轮验证的预测。

- An agent (“Evolve agent”) reads the repo and decides which component to edit, and then produces the edit and the reasoning behind it.
- 一个智能体（"Evolve agent"）读取仓库，决定编辑哪个组件，然后产生编辑及其背后的推理。

- Every edit is a file-level, falsifiable claim and can be verified in the next round, under two constraints:
- 每次编辑都是一条文件级别的、可证伪的主张，可以在下一轮验证，并受到两个约束：

- (1) Edits are only applied to the harness workspace. the runs directory, tracer, verifier, and LLM configuration are read-only, which disables a set of reward hacking (e.g  disabling the verifier, swapping the model, or raising the reasoning budget) and thus it can keep every recorded gain attributable to harness edits.
- （1）编辑只应用于 harness 工作区。runs 目录、追踪器、验证器和 LLM 配置都是只读的，这禁掉了一整套奖励破解手段（例如禁用验证器、更换模型或提高推理预算），从而可以保证每个记录下来的增益都归因于 harness 编辑。

- (2) Edits are evidence-driven, with a manifesto entry: the failure evidence’s name, the inferred root cause, the targeted fix, and a predicted impact comprising both expected fixes and at-risk regressions.
- （2）编辑由证据驱动，带有"宣言"条目：失败证据的名称、推断的根本原因、目标修复，以及包含预期修复和风险回归的预测影响。

On Terminal-Bench-2, AHE achieved better than human-designed harness (OpenCode, Terminus-2, Codex) except for Hard tier and a few other self-evolve baselines (ACE, TF-GRPO). The same frozen harness, without further evolving, transfers to SWE-bench-verified, indicating that the evolved harness is able to encode engineering experience into harness components rather than doing benchmark-specific optimization.

在 Terminal-Bench-2 上，AHE 的表现优于人工设计的 harness（OpenCode、Terminus-2、Codex），除了 Hard 难度层和少数其他自进化基线（ACE、TF-GRPO）。同一个冻结的 harness，在不进一步进化的情况下，可以迁移到 SWE-bench-verified，这表明进化出的 harness 能够把工程经验编码进 harness 组件，而不是做针对特定基准的优化。


## 进化式搜索（Evolutionary Search）

Evolutionary search is an optimization method inspired by natural selection (see my old post on evolutionary algorithm). It evolves a population of solutions by mutating them and only keeping those with high “fitness” in the crowd. Evolutionary search comes in handy when (1) the search space is extensive or weirdly shaped; and (2) it is hard to optimize directly with gradients but easy to evaluate solutions. Harness search seems to be a good fit here.

进化式搜索是一种受自然选择启发的优化方法（参见我关于进化算法的旧文）。它通过变异来进化一个解的种群，并且只保留群体中"适应度"高的个体。当（1）搜索空间很大或形状怪异；以及（2）难以用梯度直接优化但容易评估解的质量时，进化式搜索就派上用场了。Harness 搜索似乎非常适合这里。

Evolutionary search has been used in prompt engineering in the past studies. Promptbreeder (Fernando et al. 2023) optimizes task-specific prompts through a rich set of mutation operations, and interestingly the mutation prompts (i.e. instructions to an LLM to mutate a task prompt) are themselves also improved through evolution. GEPA (Agrawal et al. 2025) combines reflection-based prompting with evolutionary search and uses natural language reflection over trajectories of trial and error to propose prompt updates.

进化式搜索在过去的提示词工程研究中已被使用。Promptbreeder（Fernando et al. 2023）通过丰富的变异操作集优化任务特定提示词，有趣的是，变异提示词（即指示 LLM 变异任务提示词的指令）本身也通过进化得到改进。GEPA（Agrawal et al. 2025）将基于反思的提示与进化式搜索相结合，并利用试错轨迹上的自然语言反思来提出提示词更新。

Novikov et al. (2025) introduced AlphaEvolve as a coding-agent evolutionary search system, which stores a pool of candidate programs and prompts frozen LLMs to generate diffs for improvement. As the system repeatedly evaluates child programs and keeps successful ones, it discovers better solutions in time.

Novikov et al.（2025）提出了 AlphaEvolve，一个编码智能体进化式搜索系统：它维护一个候选程序池，并提示冻结的 LLM 生成用于改进的 diff。随着系统反复评估子程序并保留成功的程序，它能够及时地发现更好的解决方案。

> How AlphaEvolve works. (Image source: Novikov et al. 2025)
> AlphaEvolve 的工作原理。（图片来源：Novikov et al. 2025）

A few details matter in the design of AlphaEvolve:

AlphaEvolve 的设计中有几个值得注意的细节：

- The prompt includes parent programs, results, instructions, and sometimes meta information.
- 提示词包含父程序、结果、指令，有时还有元信息。

- The coding agent has access to the full repo, but code regions for improvement are explicitly marked with # EVOLVE-BLOCK-START and # EVOLVE-BLOCK-END.
- 编码智能体可以访问整个仓库，但需要改进的代码区域会用 # EVOLVE-BLOCK-START 和 # EVOLVE-BLOCK-END 显式标记。

- Meta-prompt co-evolves with instructions and context as suggested by LLM, in a similar way as how we evolve solution programs.
- 元提示词（meta-prompt）与指令和上下文一起共同进化（由 LLM 建议），方式与我们进化解程序类似。

Ablations show the evolution procedure, context in prompts, meta-prompts, full-file evolution and the use of stronger LLMs.

消融实验展示了进化过程、提示词中的上下文、元提示词、全文件进化以及使用更强 LLM 的价值。

> Ablations show the value of everal designs in AlphaEvolve. (Image source: Novikov et al. 2025)
> 消融实验展示了 AlphaEvolve 中若干设计的价值。（图片来源：Novikov et al. 2025）

Recent variants such as ThetaEvolve (Wang et al. 2025) combines evolutionary search with RL and in-context learning, and DemoEvolve (Che, et al. 2026) augments the self-rollout archive with human expert demonstrations as reference experience for harness-level diagnosis and editing. ShinkaEvolve (Lange et al. 2025), on the other hand, introduced three new components to improve LLM sampling efficiency:

近期变体如 ThetaEvolve（Wang et al. 2025）将进化式搜索与 RL 和上下文学习相结合；DemoEvolve（Che et al. 2026）用人类专家演示来扩充自运行存档，作为 harness 层面诊断和编辑的参考经验。另一方面，ShinkaEvolve（Lange et al. 2025）引入了三个新组件来提高 LLM 采样效率：

- More sample-efficient exploration by designing parent sampling to balance performance rank and offspring count.
- 通过设计父样本采样来平衡性能排名和后代数量，实现更高采样效率的探索。

- Code-novelty rejection sampling by discarding candidates that are too similar to the existing population based on embedding-based cosine similarity.
- 代码新颖性拒绝采样：基于嵌入的余弦相似度，丢弃与现有种群过于相似的候选。

- Identifying good patterns in successful solutions in a meta-scratchpad to guide future mutation.
- 在元草稿本（meta-scratchpad）中识别成功解中的良好模式，以指导未来的变异。

Unlike the methods above, which focus on solution improvement, Darwin Gödel Machine (DGM; Zhang et al. 2025) explicitly targets the evolution of an editable harness-code repository with an LLM-based coding agent. Precisely, this agent is allowed to modify its own harness. A follow-up work on Hyperagents (Zhang et al. 2026) introduced a meta-agent to control how to modify existing task agents to create new ones.

与上述专注于解改进的方法不同，达尔文-哥德尔机器（Darwin Gödel Machine, DGM；Zhang et al. 2025）明确地以基于 LLM 的编码智能体来进化一个可编辑的 harness 代码仓库为目标。确切地说，这个智能体被允许修改它自己的 harness。后续工作 Hyperagents（Zhang et al. 2026）引入了一个元智能体来控制如何修改现有任务智能体以创造新智能体。

- Start with one coding agent in the pool.
- 从池中的一个编码智能体开始。

- In each iteration, pick one parent with a probability proportional to its performance and inversely to the number of children it has, to modify and branch off to produce new agents.
- 在每次迭代中，以与其性能成正比、与其子代数量成反比的概率选择一个父智能体，进行修改并分支以产生新智能体。

- The selected parent agent examines its own benchmark evaluation log and then proposes improvements to its own harness codebase to generate a new version of the coding agent. Code editing is implemented with two basic tools: (1) bash (args: <bash_command>) and (2) editor (args: view/create/edit <file_path>).
- 被选中的父智能体会检查自己的基准评估日志，然后对其自身的 harness 代码库提出改进，以生成编码智能体的新版本。代码编辑通过两个基本工具实现：（1）bash（参数：<bash_command>）和（2）editor（参数：view/create/edit <file_path>）。

- New coding agents are evaluated, and only those with sufficiently high performance are added back into the pool.
- 新编码智能体会被评估，只有性能足够高的才会被加回池中。

- Repeat steps 2-4 until some stop criteria hit.
- 重复步骤 2-4，直到达到某个停止标准。

DGM is harness evolution under a fixed model. In experiments with Claude 3.5 Sonnet as the base LLM and simple initial harness configs, the DGM-discovered agents are comparable to or outperform handcrafted agents on SWE-bench Verified (20% to 50%) and Polyglot (14.2% to 30.7%).

DGM 是在固定模型下的 harness 进化。在以 Claude 3.5 Sonnet 为基础 LLM、初始 harness 配置简单的实验中，DGM 发现的智能体在 SWE-bench Verified（20% 到 50%）和 Polyglot（14.2% 到 30.7%）上与手工智能体相当或更优。

This family of methods works well when candidate solutions are automatically evaluable and candidate fitness is easy to quantify, such as matrix multiplication, GPU kernel optimization, algorithm contests, datacenter scheduling. It struggles with domains where evaluation is slow, ambiguous, or mostly heuristic-based. The compute efficiency and effectiveness of evolution are also concerns.

这类方法在候选解可以自动评估、候选适应度容易量化的情况下表现良好，例如矩阵乘法、GPU 内核优化、算法竞赛、数据中心调度。它不擅长评估缓慢、模糊或主要基于启发式的领域。进化的计算效率和有效性也是令人担忧的问题。


## 与模型权重的联合优化（Joint Optimization with Model Weights）

Harness evolution changes the non-parametric system around the model. To enable full self-improvement, the model can totally be allowed to update its own weights at the same time. The weight update can be implemented via improvements in the model training pipeline or continual learning at test time. The topic of continual learning is worthy of its own post in the future.

Harness 进化改变的是模型周围的非参数系统。要实现完整的自我改进，可以完全允许模型同时更新自己的权重。权重更新可以通过改进模型训练流水线或测试时的持续学习来实现。持续学习这个话题值得将来单独写一篇文章。

SIA (Hebbar et al. 2026) is an early attempt to combine harness improvement and model-parameter updates in the same optimization loop, with three components in the design:

SIA（Hebbar et al. 2026）是早期把 harness 改进和模型参数更新结合在同一个优化循环中的尝试，设计中包含三个组件：

- Meta-Agent: proposes the initial harness.
- 元智能体（Meta-Agent）：提出初始 harness。

- Task-Specific Agent: executes the task.
- 任务特定智能体（Task-Specific Agent）：执行任务。

- Feedback-Agent: chooses whether to update the harness or the model weights based on recent trajectories.
- 反馈智能体（Feedback-Agent）：根据最近的轨迹，决定是更新 harness 还是更新模型权重。

> The Feedback-Agent in SIA decides the next iteration type. (Image source: Hebbar et al. 2026)
> SIA 中的反馈智能体决定下一次迭代的类型。（图片来源：Hebbar et al. 2026）

There are a few confounding choices in SIA’s experiments that make the results hard to interpret. For example, the task-specific agent is much weaker than the models used for the Meta-Agent and Feedback-Agent (gpt-oss-120b vs Claude Sonnet 4.6), and the baselines are too weak to cross-reference cleanly against related methods. I would consider the direction interesting, but the evidence provisional. Yet many challenges, such as training stability and Goodhart effect, still remain open.

SIA 的实验中有几个混淆因素使结果难以解读。例如，任务特定智能体远弱于用于元智能体和反馈智能体的模型（gpt-oss-120b vs Claude Sonnet 4.6），而基线又太弱，无法与相关方法进行干净的交叉参照。我认为这个方向很有趣，但证据仍是暂时性的。而且，训练稳定性和古德哈特定律（Goodhart effect）等许多挑战依然悬而未决。

Continual Harness (Karten et al. 2026) experimented in long-horizon gameplay setting with harness updating and co-learning a policy model by distilling a strong teacher model’s labels on low-reward trajectories.

Continual Harness（Karten et al. 2026）在长周期游戏场景中进行了实验，结合 harness 更新，并通过在低奖励轨迹上蒸馏强教师模型的标签来共同学习一个策略模型。


# 未来挑战（Future Challenges）

The AI Scientist line of work is a strong demonstration that an expert-designed harness can coordinate a large portion of auto-research loop, experimented in the form of writing research papers. But paper production is not identical to scientific discovery. A system can write a plausible manuscript while still having fabricated citations, implementation drift, or weak experimental results.

AI Scientist 系列工作有力地证明了：专家设计的 harness 可以协调自动研究循环的很大一部分，并以撰写研究论文的形式进行了实验。但论文生产并不等同于科学发现。一个系统可以写出一篇像模像样的稿件，却仍然有捏造的引用、实现漂移或薄弱的实验结果。

Trehan & Chopra (2026) tested whether LLMs can go from a research idea to a paper with minimal scaffolding and basic tools (i.e., read_file, write_file, llm_search, list_files). Each idea had a dedicated workspace where agents could generate and read documents as part of context. They experimented in three domains (world models, multi-agent RL, AI safety & alignment), with each domain containing 45-50 high-quality seed documents to inspire new ideas. Only four ideas were selected by human experts to run through the full pipeline, and only one was fully executed into a paper. They observed six recurring failure modes in the experiments:

Trehan & Chopra（2026）测试了 LLM 能否在极简脚手架和基本工具（即 read_file、write_file、llm_search、list_files）下从研究想法走到论文。每个想法都有专用的工作空间，智能体可以在其中生成和阅读文档作为上下文的一部分。他们在三个领域进行了实验（世界模型、多智能体强化学习、AI 安全与对齐），每个领域包含 45-50 份高质量的种子文档来激发新想法。只有 4 个想法被人类专家选中进入完整流水线，其中只有 1 个被完整执行成一篇论文。他们在实验中观察到六个反复出现的失败模式：

- Bias toward training-data defaults: use old libraries, stale commands, standard formats, or assumptions not grounded in the actual repository or dataset.
- 偏向训练数据默认值：使用旧的库、过时的命令、标准格式，或基于与真实仓库/数据集不符的假设。

- Implementation drift under execution pressure: when implementation becomes technically complex, the model may move toward a common simpler solution rather than the proposed method.
- 执行压力下的实现漂移：当实现变得技术上复杂时，模型可能转向常见的更简单解法，而不是所提出的方法。

- Memory and context degradation: long-horizon projects lose critical details unless logs are written as persistent artifacts.
- 记忆与上下文退化：长周期项目会丢失关键细节，除非日志被写成持久化产物。

- Over-optimism: the model declares success despite noisy or failed experiments, similarly observed as “p-hacking and eureka-ing” pattern by Bubeck et al. (2025) where models can introduce “numerical duct tape” and declare victory when signals are still noise.
- 过度乐观：模型在实验嘈杂或失败时仍宣称成功，这与 Bubeck et al.（2025）观察到的"p-hacking 和 eureka-ing"模式类似——模型可以引入"数值胶带"（numerical duct tape），在信号仍是噪声时就宣布胜利。

- Insufficient domain intelligence: the model lacks tacit craft knowledge, e.g. predicting implementation complexity, judging whether an experimental result is plausible, or knowing which baselines matter.
- 领域智能不足：模型缺乏隐性的手艺知识，例如预测实现复杂性、判断实验结果是否合理、或知道哪些基线重要。

- Weak scientific taste: experiments may be executable but fail to answer the right question.
- 科学品味薄弱：实验也许可执行，但未能回答正确的问题。

Toward full RSI, researchers have made real progress, but several bottlenecks remain.

朝着完整的 RSI 前进，研究者们已经取得了真正的进展，但仍有几个瓶颈。

1. Weak and fuzzy evaluators. Many research claims do not have a fast and precise verifier, and the same is true for many real-world tasks. Current self-improvement loops work best for tasks when evaluation metrics are measurable and objective, similar as how RL works.

Research taste, novelty, and long-term scientific value are much harder to measure. For example, research taste often mixes problem framing, experimental design, and judgment about which surprising results are worth pursuing and which failure cases are worth retries.

1. 薄弱和模糊的评估器。许多研究主张没有快速而精确的验证器，许多现实世界任务也是如此。当前的自我改进循环在评测指标可测量且客观的任务上效果最好，就像 RL 的运作方式一样。研究品味、新颖性和长期科学价值则更难衡量。例如，研究品味常常混合了问题框架、实验设计，以及判断哪些惊人结果值得深究、哪些失败案例值得重试。

2. Context and memory lifecycle. Memory grows as AI agents become more autonomous and independent. A useful harness needs to manage context and memory to complement existing limitation in long-context generation while still maximizing the success of long-horizon tasks. Since humans are able to maintain memory through our life time, I see an anoloy here that context engineering will and should become a core part of intelligence, rather than staying in the software system layer.

2. 上下文与记忆的生命周期。随着 AI 智能体变得更加自主和独立，记忆也在增长。一个有用的 harness 需要管理上下文和记忆，以弥补长上下文生成的现有局限，同时最大化长周期任务的成功率。由于人类能够在一生中维持记忆，我认为这里存在一个类比：上下文工程将而且应该成为智能的核心部分，而不是停留在软件系统层。

3. Negative results. Researchers are incentivized to publish successful results and thus literature is biased toward successes. LLMs trained on a vast amount of data (mostly human created, at least for now, lol) may be bad at deciding when to abandon a hypothesis, report a negative result, or even acknowledge a failure due to the imablance of success vs failure cases in data. A research harness should make failed attempts easy to preserve, as learning from failure is the best way to trim down the task search space.

3. 负面结果。研究者有动力发表成功的结果，因此文献偏向成功。在大量数据（至少目前主要是人类创造的，哈哈）上训练的 LLM，由于数据中成功与失败案例的不平衡，可能在决定何时放弃假设、报告负面结果、甚至承认失败方面表现不佳。研究型 harness 应该让失败的尝试易于保留，因为从失败中学习是缩减任务搜索空间的最佳方式。

4. Diversity collapse. Evolutionary and RL loops tend to exploit known high-reward patterns. We need mechanisms to prevent the population from collapsing into variants of the same solution. This is especially critical for open-ended research, where the best path may initially look worse under the current evaluator.

4. 多样性坍缩。进化式和 RL 循环倾向于利用已知的高奖励模式。我们需要机制来防止种群坍缩成同一解法的变体。这对开放式研究尤其关键，因为在开放式研究中，最好的路径在当前评估器下最初可能看起来更差。

5. Reward hacking. A self-improvement loop optimizes whatever signal it is given. If the reward comes from unit tests, the agent may overfit to tests; if it comes from a judge model, it may learn reward hacking tricks specific to this judge; if it comes from benchmark scores, it may exploit benchmark artifacts.

5. 奖励破解。自我改进循环会优化给它的任何信号。如果奖励来自单元测试，智能体可能过度拟合测试；如果来自裁判模型，它可能学习针对该裁判的奖励破解技巧；如果来自基准分数，它可能利用基准的工件（artifact）。

The evaluator and permission control should likely sit outside the loop that evolves harness, with held-out tests, trace audits, and human review at decision points that matter—how much oversight can be scaled up and automated remains an open research area.

评估器和权限控制很可能应该位于进化 harness 的循环之外，配以留出测试、轨迹审计，以及在关键决策点上的人工审查——监督能扩展到多大程度、能自动化到什么程度，仍然是一个开放的研究领域。

6. Long-term success. An extrinsic loop of optimization works on rewards outside of individual rollouts that we can simulate in training sandbox.

Take coding agent as an example. Coding agents have already increased daily productivity in software engineering, but many optimization goals are still too short-term. It can often complete the task at hand, but less obvious how it should protect the long-term health of a repo collectively maintained by hundreds or thousands of engineers. Standard sandbox-based RLVR-style training rarely captures maintainability, ownership boundaries, migration cost, backwards compatibility, or future debugging burden.

6. 长期成功。一个外在的优化循环作用于单个运行之外、我们可以在训练沙盒中模拟的奖励。以编码智能体为例。编码智能体已经提高了软件工程的日常生产力，但许多优化目标仍然过于短期。它常常能完成手头的任务，但如何保护由成百上千名工程师共同维护的仓库的长期健康，就不那么清楚了。标准的基于沙盒的 RLVR 式训练很少捕捉可维护性、所有权边界、迁移成本、向后兼容性或未来的调试负担。

7. The role of humans. Humans should move up the stack, not be removed from the loop, meaning that human should provide oversight at the right time, at the right abstraction level and our system design should consider when and how to set up such touch points.

Many challenges listed above need human’s feedback and steering. After all, we are building the technology for better future of humanity, not other way around.

7. 人类的角色。人类应该向技术栈的上层移动，而不是被移出循环之外——这意味着人类应该在正确的时间、正确的抽象层级提供监督，而我们的系统设计应该考虑何时以及如何设置这些触点。上面列出的许多挑战都需要人类的反馈和引导。毕竟，我们是在为人类更美好的未来构建技术，而不是反过来。


# 引用（Citation）

Please cite this work as:

请按如下方式引用本文：

Weng, Lilian. “Harness Engineering for Self-Improvement”. Lil’Log (Jul 2026). https://lilianweng.github.io/posts/2026-07-04-harness/

Or use the BibTeX citation:

或使用 BibTeX：

```
@article{weng2026harness,
  title = {Harness Engineering for Self-Improvement},
  author = {Weng, Lilian},
  journal = {lilianweng.github.io},
  year = {2026},
  month = {July},
  url = "https://lilianweng.github.io/posts/2026-07-04-harness/"
}
```


# 附录：一些有用的基准（Appendix: Some useful benchmarks）

- PaperBench: replicate 20 ICML 2024 Spotlight and Oral papers from scratch, including understanding paper contributions, developing a codebase, and successfully executing experiments.
- PaperBench：从零复现 20 篇 ICML 2024 Spotlight 和 Oral 论文，包括理解论文贡献、开发代码库、成功执行实验。

- Each replication task is decomposed into smaller, individually gradable tasks.
- 每个复现任务被分解为更小的、可单独评分的子任务。

- 8,316 rubrics in total, co-developed with the paper authors.
- 共 8,316 条评分细则（rubrics），与论文作者共同开发。

- The best model at the time (Claude 3.5 Sonnet, ~21%) does not outperform ML PhDs.
- 当时最好的模型（Claude 3.5 Sonnet，约 21%）未超过 ML 博士的表现。

- Includes PaperBench, PaperBench Code-Dev (a lighter version), and JudgeEval.
- 包括 PaperBench、PaperBench Code-Dev（一个更轻量的版本）和 JudgeEval。

- CORE-Bench: evaluate computational reproducibility of published research.
- CORE-Bench：评估已发表研究的计算可复现性。

- 270 tasks based on 90 scientific papers across computer science, social science, and medicine.
- 基于跨计算机科学、社会科学和医学的 90 篇科学论文的 270 个任务。

- Tasks involve reproducing results from provided code and data.
- 任务涉及从提供的代码和数据中复现结果。

- Includes multiple difficulty levels and both language-only and vision-language tasks.
- 包括多个难度级别，以及纯语言和视觉-语言任务。

- The best reported agent at the time (GPT-4o and GPT-4o-mini) achieved only 21% accuracy on the hardest task.
- 当时报告的最好智能体（GPT-4o 和 GPT-4o-mini）在最难任务上仅达到 21% 的准确率。

- ScienceAgentBench: evaluate LLM agents for data-driven scientific discovery.
- ScienceAgentBench：评估用于数据驱动科学发现的 LLM 智能体。

- Extracts 102 tasks from 44 peer-reviewed publications in four disciplines (math, chemistry, biology, geography).
- 从四个学科（数学、化学、生物学、地理学）的 44 篇同行评审出版物中提取 102 个任务。

- Covers basic data-science tasks in these domains: data processing, model development, data analysis, and information visualization.
- 涵盖这些领域的基础数据科学任务：数据处理、模型开发、数据分析和信息可视化。

- RE-Bench: evaluate frontier AI agents on realistic ML research-engineering envs against human experts.
- RE-Bench：在真实的 ML 研究工程环境中，将前沿 AI 智能体与人类专家进行比较。

- 7 challenging, open-ended ML research-engineering environments.
- 7 个具有挑战性、开放式的 ML 研究工程环境。

- Each environment = (scoring function, starting solution, reference solution); each can be run with 8 or fewer H100 GPUs.
- 每个环境 =（评分函数、起始解、参考解）；每个环境可以用 8 块或更少的 H100 GPU 运行。

- Examples: optimize a kernel, run a scaling-law experiment, fix an embedding, fine-tune GPT-2 for QA, etc.
- 示例：优化内核、运行标度律实验、修复 embedding、为 QA 微调 GPT-2 等。

- Includes data from 71 eight-hour attempts by 61 distinct human experts.
- 包括来自 61 位不同人类专家的 71 次 8 小时尝试的数据。

- Human experts achieved non-zero score in 82% of 8-hour attempts; 24% matched or exceeded strong reference solutions.
- 人类专家在 82% 的 8 小时尝试中获得了非零分数；24% 达到或超过了强参考解。

- Best AI agents scored 4× higher than humans at a 2-hour budget, but humans had better returns to longer budgets and exceeded agents at 8-hour and 32-hour settings.
- 最好的 AI 智能体在 2 小时预算下得分比人类高 4 倍，但人类在更长预算下有更好的回报，并在 8 小时和 32 小时设置下超过了智能体。

- MLE-bench: evaluate ML engineering agents on offline Kaggle competitions.
- MLE-bench：在离线 Kaggle 竞赛上评估 ML 工程智能体。

- Contains 75 ML-engineering competitions curated from Kaggle.
- 包含从 Kaggle 精选的 75 个 ML 工程竞赛。

- Tests training models, preparing datasets, running experiments, and submitting predictions to grading scripts.
- 测试训练模型、准备数据集、运行实验、向评分脚本提交预测。

- Uses Kaggle public leaderboards as human baselines.
- 使用 Kaggle 公开排行榜作为人类基线。

- Best setup in the paper, o1-preview with AIDE scaffolding, reached at least Kaggle bronze-medal level in 16.9% of competitions.
- 论文中最好的设置（带 AIDE 脚手架的 o1-preview）在 16.9% 的竞赛中达到了至少 Kaggle 铜牌水平。

- Includes resource-scaling and contamination analyses.
- 包括资源扩展和污染分析。

- KernelBench: evaluate correctness and speed for generated GPU kernels.
- KernelBench：评估生成的 GPU 内核的正确性和速度。

- 250 PyTorch tasks to evaluate whether LLM can write fast and correct kernels.
- 250 个 PyTorch 任务，评估 LLM 能否编写快速且正确的内核。

- The evaluation metric fast_p = the percentage of generated kernels that are correct and faster than baseline.
- 评估指标 fast_p = 生成内核中正确且快于基线的百分比。


# 参考文献（References）

[1] Good, I. J. “Speculations Concerning the First Ultraintelligent Machine.” Advances in Computers, 6:31–88, 1965.

[2] Yudkowsky, Eliezer. “Recursive Self-Improvement.” LessWrong, 2008.

[3] Choi, et al. “Anchored Self-Play for Code Repair.” ICML 2026.

[4] Zhao, et al. “Absolute Zero: Reinforced Self-play Reasoning with Zero Data.” arXiv preprint arXiv:2505.03335, 2025.

[5] Yuan, et al. “Self-Rewarding Language Models.” arXiv preprint arXiv:2401.10020, 2024.

[6] Chen, et al. “Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models.” ICML 2024.

[7] Zhang, et al. “Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models.” ICLR 2026.

[8] Ye, et al. “Meta Context Engineering via Agentic Skill Evolution.” arXiv preprint arXiv:2601.21557, 2026.

[9] Lee, et al. “Meta-Harness: End-to-End Optimization of Model Harnesses.” arXiv preprint arXiv:2603.28052, 2026.

[10] Lu, et al. “Towards end-to-end automation of AI research.” Nature, 651:914–919, 2026.

[11] Meng, et al. “ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence.” arXiv preprint arXiv:2605.26340, 2026.

[12] Kulikov, et al. “Autodata: An agentic data scientist to create high quality synthetic data.” arXiv preprint arXiv:2606.25996, 2026.

[13] Hu, Lu, and Clune. “Automated Design of Agentic Systems.” ICLR 2025.

[14] Madaan, et al. “Self-Refine: Iterative Refinement with Self-Feedback.” NeurIPS 2023.

[15] Zhang, et al. “AFlow: Automating Agentic Workflow Generation.” ICLR 2025.

[16] Zelikman, et al. “Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation.” COLM 2024.

[17] Zhang, et al. “Self-Harness: Harnesses That Improve Themselves.” arXiv preprint arXiv:2606.09498, 2026.

[18] Fernando, et al. “Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution.” arXiv preprint arXiv:2309.16797, 2023.

[19] Agrawal, A. et al. “GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning.” arXiv preprint arXiv:2507.19457, 2025.

[20] Novikov, et al. “AlphaEvolve: A coding agent for scientific and algorithmic discovery.” arXiv preprint arXiv:2506.13131, 2025.

[21] Lange, Imajuku, and Cetin. “ShinkaEvolve: Towards Open-Ended And Sample-Efficient Program Evolution.” arXiv preprint arXiv:2509.19349, 2025.

[22] Wang, et al. “ThetaEvolve: Test-time Learning on Open Problems.” arXiv preprint arXiv:2511.23473, 2025.

[23] Zhang, et al. “Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents.” arXiv preprint arXiv:2505.22954, 2025.

[24] Zhang, et al. “Hyperagents.” arXiv preprint arXiv:2603.19461, 2026.

[25] Yuksekgonul, et al. “Learning to Discover at Test Time.” arXiv preprint arXiv:2601.16175, 2026.

[26] Riaz, et al. “Epistemic Uncertainty for Test-Time Discovery.” arXiv preprint arXiv:2605.11328, 2026.

[27] Hebbar, et al. “SIA: Self Improving AI with Harness & Weight Updates.” arXiv preprint arXiv:2605.27276, 2026.

[28] Trehan and Chopra. “Why LLMs Aren’t Scientists Yet: Lessons from Four Autonomous Research Attempts.” arXiv preprint arXiv:2601.03315, 2026.

[29] Bubeck, et al. “Early science acceleration experiments with GPT-5.” arXiv preprint arXiv:2511.16072, 2025.

[30] Starace, et al. “PaperBench: Evaluating AI’s Ability to Replicate AI Research.” ICML 2025.

[31] Wijk, et al. “RE-Bench: Evaluating frontier AI R&D capabilities of language model agents against human experts.” ICML 2025.

[32] Chan, et al. “MLE-bench: Evaluating Machine Learning Agents on Machine Learning Engineering.” arXiv preprint arXiv:2410.07095, 2024.

[33] Chen, et al. “ScienceAgentBench: Toward Rigorous Assessment of Language Agents for Data-Driven Scientific Discovery.” ICLR 2025.

[34] Siegel, et al. “CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility Agent Benchmark.” TMLR 2024.

[35] Ouyang, et al. “KernelBench: Can LLMs Write Efficient GPU Kernels?” arXiv preprint arXiv:2502.10517, 2025.

[36] Lin, et al. “Harness Updating Is Not Harness Benefit: Disentangling Evolution Capabilities in Self-Evolving LLM Agents.” arXiv preprint arXiv:2605.30621, 2026.

[37] Lin, et al. “Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses.” arXiv preprint arXiv:2604.25850, 2026.

[38] Karten, et al. “Continual Harness: Online Adaptation for Self-Improving Foundation Agents.” arXiv preprint arXiv:2605.09998, 2026.

[39] Che, et al. “DemoEvolve: Overcoming Sparse Feedback in Agentic Harness Evolution with Demonstrations.” arXiv preprint arXiv:2605.24539, 2026.