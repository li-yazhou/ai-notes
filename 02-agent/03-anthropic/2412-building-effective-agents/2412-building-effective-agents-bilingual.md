# 构建有效的 Agent（中英对照）

> **原文标题：** Building effective agents
> **作者：** Erik S. 与 Barry Zhang（Anthropic 工程团队）
> **原文链接：** https://www.anthropic.com/engineering/building-effective-agents
> **发布日期：** 2024-12-19
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

*Note: Much of the tooling landscape described in this post has changed since December 2024. For our current approach, see [**how we built Claude Managed Agents**](https://www.anthropic.com/engineering/managed-agents)* *and the [**Managed Agents documentation**. ](https://platform.claude.com/docs/en/managed-agents/overview)*  Over the past year, we've worked with dozens of teams building large language model (LLM) agents across industries. Consistently, the most successful implementations weren't using complex frameworks or specialized libraries. Instead, they were building with simple, composable patterns.

*注：本文所描述的绝大部分工具生态自 2024 年 12 月以来已经发生了变化。关于我们目前的方法，请参阅[**我们如何构建 Claude Managed Agents**](https://www.anthropic.com/engineering/managed-agents)**和[**Managed Agents 文档**](https://platform.claude.com/docs/en/managed-agents/overview)。* 在过去一年里，我们与数十个跨行业的团队合作，帮助他们构建大语言模型（large language model，LLM）Agent。始终一致的是，最成功的实现并没有使用复杂的框架或专门的库。相反，他们是用简单、可组合（composable）的模式来构建的。

In this post, we share what we've learned from working with our customers and building agents ourselves, and give practical advice for developers on building effective agents.

在这篇文章中，我们分享从与客户合作以及自己构建 Agent 中学到的东西，并为开发者提供构建有效 Agent 的实用建议。

# 什么是 Agent？（What are agents?）

"Agent" can be defined in several ways. Some customers define agents as fully autonomous systems that operate independently over extended periods, using various tools to accomplish complex tasks. Others use the term to describe more prescriptive implementations that follow predefined workflows. At Anthropic, we categorize all these variations as **agentic systems**, but draw an important architectural distinction between **workflows **and** agents**:

"Agent"可以有多种定义方式。一些客户把 Agent 定义为完全自主的系统，在较长时间内独立运行，使用各种工具完成复杂任务。另一些人则用这个词来描述遵循预定义工作流的、更规范化的实现。在 Anthropic，我们把所有这些变体都归类为**Agentic 系统（agentic systems）**，但在**工作流（workflows）**和**Agent（agents）**之间划出了重要的架构区分：

- **Workflows** are systems where LLMs and tools are orchestrated through predefined code paths.
- **工作流（workflows）**是通过预定义的代码路径来编排 LLM 和工具的系统。
- **Agents**, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks.
- **Agent（agents）**则是 LLM 动态引导自身流程和工具使用的系统，对完成任务的方式保持控制。

Below, we will explore both types of agentic systems in detail. In Appendix 1 ("Agents in Practice"), we describe two domains where customers have found particular value in using these kinds of systems.

下面，我们将详细探讨这两类 Agentic 系统。在附录 1（"实践中的 Agent"）中，我们描述了两个客户认为这类系统特别有价值的领域。

# 何时（以及何时不）使用 Agent（When (and when not) to use agents）

When building applications with LLMs, we recommend finding the simplest solution possible, and only increasing complexity when needed. This might mean not building agentic systems at all. Agentic systems often trade latency and cost for better task performance, and you should consider when this tradeoff makes sense.

在构建 LLM 应用时，我们建议尽可能找到最简单的解决方案，只在必要时才增加复杂性。这可能意味着根本不构建 Agentic 系统。Agentic 系统常常用延迟和成本换取更好的任务性能，你应该考虑这种权衡在什么时候是合理的。

When more complexity is warranted, workflows offer predictability and consistency for well-defined tasks, whereas agents are the better option when flexibility and model-driven decision-making are needed at scale. For many applications, however, optimizing single LLM calls with retrieval and in-context examples is usually enough.

当确实需要更多复杂性时，工作流为定义良好的任务提供了可预测性和一致性；而当需要在规模化场景下具备灵活性和模型驱动的决策时，Agent 是更好的选择。然而，对许多应用来说，用检索（retrieval）和上下文内示例（in-context examples）来优化单个 LLM 调用通常就足够了。

# 何时以及如何使用框架（When and how to use frameworks）

There are many frameworks that make agentic systems easier to implement, including:

有许多框架让 Agentic 系统更容易实现，包括：

- The [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview);
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)；
- [Strands Agents SDK by AWS](https://strandsagents.com/latest/);
- AWS 的 [Strands Agents SDK](https://strandsagents.com/latest/)；
- [Rivet](https://rivet.ironcladapp.com/), a drag and drop GUI LLM workflow builder; and
- [Rivet](https://rivet.ironcladapp.com/)，一个拖放式 GUI LLM 工作流构建器；以及
- [Vellum](https://www.vellum.ai/), another GUI tool for building and testing complex workflows.
- [Vellum](https://www.vellum.ai/)，另一个用于构建和测试复杂工作流的 GUI 工具。

These frameworks make it easy to get started by simplifying standard low-level tasks like calling LLMs, defining and parsing tools, and chaining calls together. However, they often create extra layers of abstraction that can obscure the underlying prompts ​​and responses, making them harder to debug. They can also make it tempting to add complexity when a simpler setup would suffice.

这些框架通过简化标准底层任务（如调用 LLM、定义和解析工具、把调用链接起来）让上手变得容易。然而，它们常常会创建额外的抽象层，这些抽象层可能掩盖底层的提示词和响应，使它们更难调试。它们还可能让人忍不住去增加复杂性，而其实更简单的配置就足够了。

We suggest that developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code. If you do use a framework, ensure you understand the underlying code. Incorrect assumptions about what's under the hood are a common source of customer error.

我们建议开发者直接从使用 LLM API 开始：许多模式只需几行代码就能实现。如果你确实使用框架，请确保你理解底层代码。对引擎盖下内容的错误假设是客户犯错的常见来源。

See our [cookbook](https://platform.claude.com/cookbook/patterns-agents-basic-workflows) for some sample implementations.

一些示例实现请参阅我们的[cookbook（示例手册）](https://platform.claude.com/cookbook/patterns-agents-basic-workflows)。

# 构建模块、工作流与 Agent（Building blocks, workflows, and agents）

In this section, we'll explore the common patterns for agentic systems we've seen in production. We'll start with our foundational building block—the augmented LLM—and progressively increase complexity, from simple compositional workflows to autonomous agents.

在本节中，我们将探讨我们在生产环境中见过的 Agentic 系统的常见模式。我们从基础构建模块——增强型 LLM（augmented LLM）——开始，并逐步增加复杂性，从简单的组合式工作流一直到自主 Agent。

## 构建模块：增强型 LLM（Building block: The augmented LLM）

The basic building block of agentic systems is an LLM enhanced with augmentations such as retrieval, tools, and memory. Our current models can actively use these capabilities—generating their own search queries, selecting appropriate tools, and determining what information to retain.

Agentic 系统的基本构建模块，是一个通过检索、工具和记忆（memory）等增强能力强化过的 LLM。我们当前的模型能够主动使用这些能力——生成自己的搜索查询、选择合适的工具、决定要保留哪些信息。

![增强型 LLM](images/effagents-1.png)

> The augmented LLM
> 增强型 LLM

We recommend focusing on two key aspects of the implementation: tailoring these capabilities to your specific use case and ensuring they provide an easy, well-documented interface for your LLM. While there are many ways to implement these augmentations, one approach is through our recently released [Model Context Protocol](https://www.anthropic.com/news/model-context-protocol), which allows developers to integrate with a growing ecosystem of third-party tools with a simple [client implementation](https://modelcontextprotocol.io/tutorials/building-a-client#building-mcp-clients).

我们建议重点关注实现的两个关键方面：把这些能力定制到你的具体用例，并确保它们为你的 LLM 提供一个简单、文档完善的接口。虽然实现这些增强的方式有很多种，其中一种是通过我们最近发布的[模型上下文协议（Model Context Protocol）](https://www.anthropic.com/news/model-context-protocol)，它让开发者能够通过简单的[客户端实现](https://modelcontextprotocol.io/tutorials/building-a-client#building-mcp-clients)与不断增长的第三方工具生态集成。

For the remainder of this post, we'll assume each LLM call has access to these augmented capabilities.

在本文的其余部分，我们假设每次 LLM 调用都能访问这些增强能力。

## 工作流：提示词链式调用（Workflow: Prompt chaining）

Prompt chaining decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one. You can add programmatic checks (see "gate” in the diagram below) on any intermediate steps to ensure that the process is still on track.

提示词链式调用（prompt chaining）把一个任务分解成一系列步骤，其中每次 LLM 调用都处理前一次调用的输出。你可以在任何中间步骤上添加程序化检查（见下图的"门"gate），以确保流程仍在正轨上。

![提示词链式调用工作流](images/effagents-2.png)

> The prompt chaining workflow
> 提示词链式调用工作流

**When to use this workflow:** This workflow is ideal for situations where the task can be easily and cleanly decomposed into fixed subtasks. The main goal is to trade off latency for higher accuracy, by making each LLM call an easier task.

**何时使用这种工作流：**这种工作流非常适合任务能被轻松、干净地分解为固定子任务的情况。其主要目标是通过让每次 LLM 调用都成为更简单的任务，用延迟换取更高的准确率。

**Examples where prompt chaining is useful:**

**提示词链式调用有用的示例：**

- Generating Marketing copy, then translating it into a different language.
- 生成营销文案，然后把它翻译成另一种语言。
- Writing an outline of a document, checking that the outline meets certain criteria, then writing the document based on the outline.
- 撰写文档大纲，检查大纲是否满足某些标准，然后基于大纲撰写文档。

## 工作流：路由（Workflow: Routing）

Routing classifies an input and directs it to a specialized followup task. This workflow allows for separation of concerns, and building more specialized prompts. Without this workflow, optimizing for one kind of input can hurt performance on other inputs.

路由（routing）对输入进行分类，并将其引导到专门的后续任务。这种工作流允许关注点分离（separation of concerns），并构建更专门的提示词。没有这种工作流，针对某一种输入进行优化可能会损害其他输入的性能。

![路由工作流](images/effagents-3.png)

> The routing workflow
> 路由工作流

**When to use this workflow:** Routing works well for complex tasks where there are distinct categories that are better handled separately, and where classification can be handled accurately, either by an LLM or a more traditional classification model/algorithm.

**何时使用这种工作流：**路由适用于复杂任务——在这些任务中，存在更适合分开处理的不同类别，并且分类可以由 LLM 或更传统的分类模型/算法准确完成。

**Examples where routing is useful:**

**路由有用的示例：**

- Directing different types of customer service queries (general questions, refund requests, technical support) into different downstream processes, prompts, and tools.
- 把不同类型的客服查询（一般问题、退款请求、技术支持）引导到不同的下游流程、提示词和工具中。
- Routing easy/common questions to smaller, cost-efficient models like Claude Haiku 4.5 and hard/unusual questions to more capable models like Claude Sonnet 4.5 to optimize for best performance.
- 把简单/常见的问题路由到更小、更经济的模型（如 Claude Haiku 4.5），把困难/不寻常的问题路由到能力更强的模型（如 Claude Sonnet 4.5），以优化最佳性能。

## 工作流：并行化（Workflow: Parallelization）

LLMs can sometimes work simultaneously on a task and have their outputs aggregated programmatically. This workflow, parallelization, manifests in two key variations:

LLM 有时可以同时处理一个任务，并用程序化方式汇总它们的输出。这种工作流——并行化（parallelization）——表现为两种关键变体：

- **Sectioning**: Breaking a task into independent subtasks run in parallel.
- **切分（sectioning）**：把一个任务分解成并行运行的独立子任务。
- **Voting:** Running the same task multiple times to get diverse outputs.
- **投票（voting）**：多次运行同一个任务，以获得多样化的输出。

![并行化工作流](images/effagents-4.png)

> The parallelization workflow
> 并行化工作流

**When to use this workflow:** Parallelization is effective when the divided subtasks can be parallelized for speed, or when multiple perspectives or attempts are needed for higher confidence results. For complex tasks with multiple considerations, LLMs generally perform better when each consideration is handled by a separate LLM call, allowing focused attention on each specific aspect.

**何时使用这种工作流：**当被划分的子任务可以为了速度而并行化，或者需要多个视角或多次尝试以获得更高置信度的结果时，并行化是有效的。对于有多个考量因素的复杂任务，当每个考量因素由一次独立的 LLM 调用处理时，LLM 通常表现更好，因为这样可以聚焦于每个具体方面。

**Examples where parallelization is useful:**

**并行化有用的示例：**

- **Sectioning**:Implementing guardrails where one model instance processes user queries while another screens them for inappropriate content or requests. This tends to perform better than having the same LLM call handle both guardrails and the core response.Automating evals for evaluating LLM performance, where each LLM call evaluates a different aspect of the model's performance on a given prompt.
- **切分（sectioning）**：实现护栏（guardrails），其中一个模型实例处理用户查询，另一个实例对查询进行不当内容或请求的筛查。这通常比让同一次 LLM 调用同时处理护栏和核心响应表现更好。自动化用于评估 LLM 性能的评测（eval），其中每次 LLM 调用评估模型在给定提示词上性能的一个不同方面。
- **Voting**:Reviewing a piece of code for vulnerabilities, where several different prompts review and flag the code if they find a problem.Evaluating whether a given piece of content is inappropriate, with multiple prompts evaluating different aspects or requiring different vote thresholds to balance false positives and negatives.
- **投票（voting）**：审查一段代码的漏洞，用几个不同的提示词来审查，如果发现问题就标记该代码。评估某段内容是否不当，用多个提示词评估不同方面，或要求不同的投票阈值，以平衡误报和漏报。

## 工作流：编排者-工作者（Workflow: Orchestrator-workers）

In the orchestrator-workers workflow, a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesizes their results.

在编排者-工作者（orchestrator-workers）工作流中，一个中央 LLM 动态地分解任务，把它们委派给工作者 LLM，并综合它们的结果。

![编排者-工作者工作流](images/effagents-5.png)

> The orchestrator-workers workflow
> 编排者-工作者工作流

**When to use this workflow:** This workflow is well-suited for complex tasks where you can't predict the subtasks needed (in coding, for example, the number of files that need to be changed and the nature of the change in each file likely depend on the task). Whereas it's topographically similar, the key difference from parallelization is its flexibility—subtasks aren't pre-defined, but determined by the orchestrator based on the specific input.

**何时使用这种工作流：**这种工作流非常适合那些你无法预测所需子任务的复杂任务（例如在编码中，需要修改的文件数量以及每个文件中修改的性质，很可能取决于任务本身）。虽然它在结构上相似，但与并行化的关键区别在于它的灵活性——子任务不是预先定义的，而是由编排者根据具体输入决定的。

**Example where orchestrator-workers is useful:**

**编排者-工作者有用的示例：**

- Coding products that make complex changes to multiple files each time.
- 每次都要对多个文件进行复杂改动的编码类产品。
- Search tasks that involve gathering and analyzing information from multiple sources for possible relevant information.
- 涉及从多个来源收集和分析信息以寻找可能相关信息的搜索任务。

## 工作流：评估者-优化者（Workflow: Evaluator-optimizer）

In the evaluator-optimizer workflow, one LLM call generates a response while another provides evaluation and feedback in a loop.

在评估者-优化者（evaluator-optimizer）工作流中，一次 LLM 调用生成响应，而另一次调用在循环中提供评估和反馈。

![评估者-优化者工作流](images/effagents-6.png)

> The evaluator-optimizer workflow
> 评估者-优化者工作流

**When to use this workflow:** This workflow is particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value. The two signs of good fit are, first, that LLM responses can be demonstrably improved when a human articulates their feedback; and second, that the LLM can provide such feedback. This is analogous to the iterative writing process a human writer might go through when producing a polished document.

**何时使用这种工作流：**当我们有明确的评估标准，并且迭代式改进能带来可衡量的价值时，这种工作流特别有效。两个适配的标志是：第一，当人类明确表达反馈时，LLM 的响应能够被切实地改进；第二，LLM 能够提供这样的反馈。这类似于人类作者在撰写一篇精雕细琢的文档时可能经历的迭代式写作过程。

**Examples where evaluator-optimizer is useful:**

**评估者-优化者有用的示例：**

- Literary translation where there are nuances that the translator LLM might not capture initially, but where an evaluator LLM can provide useful critiques.
- 文学翻译，其中有些细微之处译者 LLM 最初可能捕捉不到，但评估者 LLM 能提供有用的批评。
- Complex search tasks that require multiple rounds of searching and analysis to gather comprehensive information, where the evaluator decides whether further searches are warranted.
- 需要多轮搜索和分析来收集全面信息的复杂搜索任务，由评估者决定是否值得进行进一步搜索。

## Agent（Agents）

Agents are emerging in production as LLMs mature in key capabilities—understanding complex inputs, engaging in reasoning and planning, using tools reliably, and recovering from errors. Agents begin their work with either a command from, or interactive discussion with, the human user. Once the task is clear, agents plan and operate independently, potentially returning to the human for further information or judgement. During execution, it's crucial for the agents to gain "ground truth" from the environment at each step (such as tool call results or code execution) to assess its progress. Agents can then pause for human feedback at checkpoints or when encountering blockers. The task often terminates upon completion, but it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control.

随着 LLM 在关键能力上不断成熟——理解复杂输入、进行推理和规划、可靠地使用工具、从错误中恢复——Agent 正在生产环境中崭露头角。Agent 从人类用户的命令或交互式讨论开始工作。一旦任务清晰，Agent 就独立地规划和运行，也可能会回到人类那里获取更多信息或判断。在执行过程中，Agent 每一步都从环境中获取"基本事实"（ground truth）（如工具调用结果或代码执行）来评估自己的进展，这一点至关重要。然后 Agent 可以在检查点或遇到阻碍时暂停，等待人类反馈。任务通常在完成后终止，但加入停止条件（如最大迭代次数）以保持控制也很常见。

Agents can handle sophisticated tasks, but their implementation is often straightforward. They are typically just LLMs using tools based on environmental feedback in a loop. It is therefore crucial to design toolsets and their documentation clearly and thoughtfully. We expand on best practices for tool development in Appendix 2 ("Prompt Engineering your Tools").

Agent 可以处理复杂的任务，但它们的实现往往很直接。它们通常只是在一个循环中根据环境反馈使用工具的 LLM。因此，清晰而周到地设计工具集及其文档至关重要。我们会在附录 2（"为你的工具做提示词工程"）中详细阐述工具开发的最佳实践。

![自主 Agent](images/effagents-7.png)

> Autonomous agent
> 自主 Agent

**When to use agents:** Agents can be used for open-ended problems where it's difficult or impossible to predict the required number of steps, and where you can't hardcode a fixed path. The LLM will potentially operate for many turns, and you must have some level of trust in its decision-making. Agents' autonomy makes them ideal for scaling tasks in trusted environments.

**何时使用 Agent：**Agent 可以用于开放式问题——这类问题很难或不可能预测所需的步骤数量，也无法硬编码一条固定路径。LLM 可能会运行很多轮，你必须对其决策有一定程度的信任。Agent 的自主性使它们非常适合在可信环境中扩展任务。

The autonomous nature of agents means higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails.

Agent 的自主特性意味着更高的成本和错误叠加（compounding errors）的潜在风险。我们建议在沙箱环境中进行广泛的测试，并设置适当的护栏。

**Examples where agents are useful:**

**Agent 有用的示例：**

The following examples are from our own implementations:

以下示例来自我们自己的实现：

- A coding Agent to resolve [SWE-bench tasks](https://www.anthropic.com/research/swe-bench-sonnet), which involve edits to many files based on a task description;
- 一个用于解决 [SWE-bench 任务](https://www.anthropic.com/research/swe-bench-sonnet)的编码 Agent，这些任务涉及根据任务描述对许多文件进行编辑；
- Our ["computer use" reference implementation](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo), where Claude uses a computer to accomplish tasks.
- 我们的["计算机使用"（computer use）参考实现](https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo)，其中 Claude 使用计算机来完成各种任务。

![编码 Agent 的高层流程](images/effagents-8.png)

> High-level flow of a coding agent
> 编码 Agent 的高层流程

# 组合与定制这些模式（Combining and customizing these patterns）

These building blocks aren't prescriptive. They're common patterns that developers can shape and combine to fit different use cases. The key to success, as with any LLM features, is measuring performance and iterating on implementations. To repeat: you should consider adding complexity *only* when it demonstrably improves outcomes.

这些构建模块并不是规定性的。它们是开发者可以塑造和组合以适应不同用例的常见模式。与任何 LLM 功能一样，成功的关键是衡量性能并迭代实现。再强调一次：只有在复杂性被证明能改善结果时，你才应考虑增加它。

# 总结（Summary）

Success in the LLM space isn't about building the most sophisticated system. It's about building the *right* system for your needs. Start with simple prompts, optimize them with comprehensive evaluation, and add multi-step agentic systems only when simpler solutions fall short.

在 LLM 领域取得成功，不在于构建最复杂的系统，而在于为你的需求构建*正确*的系统。从简单的提示词开始，用全面的评估来优化它们，只在更简单的解决方案力不从心时，才添加多步骤的 Agentic 系统。

When implementing agents, we try to follow three core principles:

在实现 Agent 时，我们努力遵循三个核心原则：

1. Maintain **simplicity** in your agent's design.
2. 在 Agent 的设计中保持**简洁（simplicity）**。
3. Prioritize **transparency** by explicitly showing the agent's planning steps.
4. 优先考虑**透明性（transparency）**，明确展示 Agent 的规划步骤。
5. Carefully craft your agent-computer interface (ACI) through thorough tool **documentation and testing**.
6. 通过彻底的工具**文档与测试（documentation and testing）**，精心打造你的 Agent-计算机接口（ACI）。

Frameworks can help you get started quickly, but don't hesitate to reduce abstraction layers and build with basic components as you move to production. By following these principles, you can create agents that are not only powerful but also reliable, maintainable, and trusted by their users.

框架可以帮助你快速上手，但在转向生产环境时，不要犹豫去减少抽象层、用基本组件来构建。遵循这些原则，你就能创建不仅强大、而且可靠、可维护、并受用户信任的 Agent。

## 致谢（Acknowledgements）

Written by Erik S. and Barry Zhang. This work draws upon our experiences building agents at Anthropic and the valuable insights shared by our customers, for which we're deeply grateful.

作者为 Erik S. 和 Barry Zhang。这项工作借鉴了我们在 Anthropic 构建 Agent 的经验，以及客户分享的宝贵见解，对此我们深表感谢。

# 附录 1：实践中的 Agent（Appendix 1: Agents in practice）

Our work with customers has revealed two particularly promising applications for AI agents that demonstrate the practical value of the patterns discussed above. Both applications illustrate how agents add the most value for tasks that require both conversation and action, have clear success criteria, enable feedback loops, and integrate meaningful human oversight.

我们与客户的工作揭示了 AI Agent 的两个特别有前景的应用，它们展示了上述模式的实际价值。这两个应用都说明了 Agent 如何为那些既需要对话又需要行动、有明确成功标准、支持反馈循环、并融入有意义的人类监督的任务带来最大价值。

## A. 客户支持（A. Customer support）

Customer support combines familiar chatbot interfaces with enhanced capabilities through tool integration. This is a natural fit for more open-ended agents because:

客户支持通过工具集成，把熟悉的聊天机器人界面与增强的能力结合起来。这天然适合更开放的 Agent，因为：

- Support interactions naturally follow a conversation flow while requiring access to external information and actions;
- 支持类交互自然遵循对话流程，同时需要访问外部信息和执行操作；
- Tools can be integrated to pull customer data, order history, and knowledge base articles;
- 可以集成工具来获取客户数据、订单历史记录和知识库文章；
- Actions such as issuing refunds or updating tickets can be handled programmatically; and
- 诸如发放退款或更新工单等操作可以程序化处理；以及
- Success can be clearly measured through user-defined resolutions.
- 成功可以通过用户定义的解决方案（resolutions）来清晰衡量。

Several companies have demonstrated the viability of this approach through usage-based pricing models that charge only for successful resolutions, showing confidence in their agents' effectiveness.

几家公司已经通过按使用量计价的模式（只为成功解决的工单收费）证明了这种方法的可行性，这体现了它们对自己 Agent 有效性的信心。

## B. 编码 Agent（B. Coding agents）

The software development space has shown remarkable potential for LLM features, with capabilities evolving from code completion to autonomous problem-solving. Agents are particularly effective because:

软件开发领域已展现出 LLM 功能的非凡潜力，其能力从代码补全演进到自主解决问题。Agent 之所以特别有效，是因为：

- Code solutions are verifiable through automated tests;
- 代码解决方案可以通过自动化测试来验证；
- Agents can iterate on solutions using test results as feedback;
- Agent 可以利用测试结果作为反馈来迭代解决方案；
- The problem space is well-defined and structured; and
- 问题空间定义良好且结构清晰；以及
- Output quality can be measured objectively.
- 输出质量可以被客观衡量。

In our own implementation, agents can now solve real GitHub issues in the [SWE-bench Verified](https://www.anthropic.com/research/swe-bench-sonnet) benchmark based on the pull request description alone. However, whereas automated testing helps verify functionality, human review remains crucial for ensuring solutions align with broader system requirements.

在我们自己的实现中，Agent 现在仅凭 pull request（拉取请求）描述，就能解决 [SWE-bench Verified](https://www.anthropic.com/research/swe-bench-sonnet) 基准中的真实 GitHub issue。然而，虽然自动化测试有助于验证功能，但人类审查对于确保解决方案与更广泛的系统需求保持一致仍然至关重要。

# 附录 2：为你的工具做提示词工程（Appendix 2: Prompt engineering your tools）

No matter which agentic system you're building, tools will likely be an important part of your agent. [Tools](https://www.anthropic.com/news/tool-use-ga) enable Claude to interact with external services and APIs by specifying their exact structure and definition in our API. When Claude responds, it will include a [tool use block](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#example-api-response-with-a-tool-use-content-block) in the API response if it plans to invoke a tool. Tool definitions and specifications should be given just as much prompt engineering attention as your overall prompts. In this brief appendix, we describe how to prompt engineer your tools.

无论你在构建哪种 Agentic 系统，工具都很可能是你的 Agent 的重要组成部分。[工具（tools）](https://www.anthropic.com/news/tool-use-ga)通过在 API 中指定其确切结构和定义，让 Claude 能够与外部服务和 API 交互。当 Claude 响应时，如果它计划调用某个工具，它会在 API 响应中包含一个[工具使用块（tool use block）](https://docs.anthropic.com/en/docs/build-with-claude/tool-use#example-api-response-with-a-tool-use-content-block)。工具定义和规格说明应该得到与你的整体提示词同等的提示词工程关注。在这个简短的附录中，我们描述如何为你的工具做提示词工程。

There are often several ways to specify the same action. For instance, you can specify a file edit by writing a diff, or by rewriting the entire file. For structured output, you can return code inside markdown or inside JSON. In software engineering, differences like these are cosmetic and can be converted losslessly from one to the other. However, some formats are much more difficult for an LLM to write than others. Writing a diff requires knowing how many lines are changing in the chunk header before the new code is written. Writing code inside JSON (compared to markdown) requires extra escaping of newlines and quotes.

指定同一个动作往往有几种方式。例如，你可以通过编写 diff（差异补丁）来指定文件编辑，也可以重写整个文件。对于结构化输出，你可以在 markdown 或 JSON 内返回代码。在软件工程中，这类差异是表面的，可以在两者之间无损转换。然而，有些格式对 LLM 来说比其他的难写得多。编写 diff 需要在写出新代码之前，就知道块头中正在变化多少行。在 JSON 中编写代码（与 markdown 相比）需要对换行符和引号进行额外的转义。

Our suggestions for deciding on tool formats are the following:

我们关于决定工具格式的建议如下：

- Give the model enough tokens to "think" before it writes itself into a corner.
- 给模型足够的令牌去"思考"，免得它把自己写进死胡同。
- Keep the format close to what the model has seen naturally occurring in text on the internet.
- 让格式尽量接近模型在互联网文本中自然见过的形式。
- Make sure there's no formatting "overhead" such as having to keep an accurate count of thousands of lines of code, or string-escaping any code it writes.
- 确保没有格式化的"开销"，比如必须准确统计数千行代码的数量，或对它编写的任何代码进行字符串转义。

One rule of thumb is to think about how much effort goes into human-computer interfaces (HCI), and plan to invest just as much effort in creating good *agent*-computer interfaces (ACI). Here are some thoughts on how to do so:

一条经验法则是：想想人们在人机界面（human-computer interface，HCI）上投入了多少精力，并计划投入同样多的精力去创建良好的*Agent*-计算机界面（agent-computer interface，ACI）。以下是一些关于如何做到这一点的想法：

- Put yourself in the model's shoes. Is it obvious how to use this tool, based on the description and parameters, or would you need to think carefully about it? If so, then it's probably also true for the model. A good tool definition often includes example usage, edge cases, input format requirements, and clear boundaries from other tools.
- 站在模型的角度思考。根据描述和参数，这个工具如何使用是否一目了然，还是你需要仔细考虑？如果对你是这样，那么对模型很可能也是如此。一个好的工具定义通常包含示例用法、边界情况、输入格式要求，以及与其他工具的清晰边界。
- How can you change parameter names or descriptions to make things more obvious? Think of this as writing a great docstring for a junior developer on your team. This is especially important when using many similar tools.
- 如何更改参数名称或描述，让事情更显而易见？把这想象成为你团队中的初级开发者撰写一份出色的 docstring（文档字符串）。当使用许多相似的工具时，这一点尤其重要。
- Test how the model uses your tools: Run many example inputs in our [workbench](https://console.anthropic.com/workbench) to see what mistakes the model makes, and iterate.
- 测试模型如何使用你的工具：在我们的 [workbench（工作台）](https://console.anthropic.com/workbench) 中运行许多示例输入，看看模型会犯什么错误，然后迭代。
- [Poka-yoke](https://en.wikipedia.org/wiki/Poka-yoke) your tools. Change the arguments so that it is harder to make mistakes.
- 为你的工具做 [Poka-yoke（防错）](https://en.wikipedia.org/wiki/Poka-yoke)。更改参数，让犯错变得更难。

While building our agent for [SWE-bench](https://www.anthropic.com/research/swe-bench-sonnet), we actually spent more time optimizing our tools than the overall prompt. For example, we found that the model would make mistakes with tools using relative filepaths after the agent had moved out of the root directory. To fix this, we changed the tool to always require absolute filepaths—and we found that the model used this method flawlessly.

在构建我们的 [SWE-bench](https://www.anthropic.com/research/swe-bench-sonnet) Agent 时，我们实际上花了比整体提示词更多的时间来优化工具。例如，我们发现，在 Agent 移出根目录之后，模型在使用相对文件路径的工具时会出错。为了解决这个问题，我们更改了工具，让它始终要求绝对文件路径——结果发现模型完美地使用了这种方法。
