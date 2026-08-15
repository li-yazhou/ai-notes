# 面向 AI Agent 的有效上下文工程（中英对照）

> **原文标题：** Effective context engineering for AI agents
> **作者：** Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, Jeremy Hadfield 等（Anthropic 应用 AI 团队）
> **原文链接：** https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
> **发布日期：** 2025-09-29
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

After a few years of prompt engineering being the focus of attention in applied AI, a new term has come to prominence: **context engineering**. Building with language models is becoming less about finding the right words and phrases for your prompts, and more about answering the broader question of "what configuration of context is most likely to generate our model's desired behavior?"

在提示词工程（prompt engineering）成为应用 AI 领域关注焦点的几年之后，一个新术语逐渐崭露头角：**上下文工程（context engineering）**。使用语言模型进行构建，正在变得越发不关乎为提示词找到恰当的措辞，而更关乎回答一个更宏大的问题："什么样的上下文配置最有可能产生我们模型期望的行为？"

**Context** refers to the set of tokens included when sampling from a large-language model (LLM). The **engineering** problem at hand is optimizing the utility of those tokens against the inherent constraints of LLMs in order to consistently achieve a desired outcome. Effectively wrangling LLMs often requires *thinking in context* — in other words: considering the holistic state available to the LLM at any given time and what potential behaviors that state might yield.

**上下文（Context）**指的是从大语言模型（LLM）采样时包含的令牌（token）集合。当前的**工程（engineering）**问题，是在 LLM 固有限制下优化这些令牌的效用，以稳定达成期望的结果。有效驾驭 LLM 通常需要*在上下文中思考（thinking in context）*——换句话说，就是考虑 LLM 在任意时刻可用的整体状态，以及这种状态可能催生出的潜在行为。

In this post, we'll explore the emerging art of context engineering and offer a refined mental model for building steerable, effective agents.

在本文中，我们将探讨上下文工程这门新兴的艺术，并提供一个精炼的心智模型，用于构建可操控（steerable）、高效的 Agent。

# 上下文工程 vs. 提示词工程（Context engineering vs. prompt engineering）

At Anthropic, we view context engineering as the natural progression of prompt engineering. Prompt engineering refers to methods for writing and organizing LLM instructions for optimal outcomes (see [our docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) for an overview and useful prompt engineering strategies). **Context engineering** refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference, including all the other information that may land there outside of the prompts.

在 Anthropic，我们把上下文工程视为提示词工程的自然演进。提示词工程指编写和组织 LLM 指令以达成最优结果的方法（关于概览和实用的提示词工程策略，请参阅[我们的文档](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)）。**上下文工程（context engineering）**指在 LLM 推理期间策划（curate）和维护最优令牌（信息）集合的一系列策略，其中还包括提示词之外可能进入上下文的所有其他信息。

In the early days of engineering with LLMs, prompting was the biggest component of AI engineering work, as the majority of use cases outside of everyday chat interactions required prompts optimized for one-shot classification or text generation tasks. As the term implies, the primary focus of prompt engineering is how to write effective prompts, particularly system prompts. However, as we move towards engineering more capable agents that operate over multiple turns of inference and longer time horizons, we need strategies for managing the entire context state (system instructions, tools, [Model Context Protocol](https://modelcontextprotocol.io/docs/getting-started/intro) (MCP), external data, message history, etc).

在早期使用 LLM 进行工程开发的阶段，提示词是 AI 工程工作最大的组成部分，因为除日常聊天交互外的大多数用例，都需要针对一次性分类或文本生成任务优化的提示词。正如这个术语所暗示的，提示词工程的主要焦点是如何编写有效的提示词，尤其是系统提示词（system prompt）。然而，随着我们转向构建更强大、能够在多轮推理和更长时间跨度上运行的 Agent，我们需要管理整个上下文状态（系统指令、工具、[模型上下文协议（Model Context Protocol，MCP）](https://modelcontextprotocol.io/docs/getting-started/intro)、外部数据、消息历史等）的策略。

An agent running in a loop generates more and more data that *could* be relevant for the next turn of inference, and this information must be cyclically refined. Context engineering is the [art and science](https://x.com/karpathy/status/1937902205765607626?lang=en) of curating what will go into the limited context window from that constantly evolving universe of possible information.

在循环中运行的 Agent 会不断产生更多*可能*与下一轮推理相关的数据，而这些信息必须周期性地加以提炼。上下文工程就是这样一门[艺术与科学](https://x.com/karpathy/status/1937902205765607626?lang=en)：从那个不断演化的可能信息宇宙中，策划出将进入有限上下文窗口的内容。

![上下文工程与提示词工程的对比：提示词是离散的一次性任务，而上下文工程是迭代式的策划过程](images/ctxeng-1.png)

> In contrast to the discrete task of writing a prompt, context engineering is iterative and the curation phase happens each time we decide what to pass to the model.
> 与编写提示词这种离散任务不同，上下文工程是迭代式的，每当我们决定把什么传给模型时，策划阶段就会发生。

# 为什么上下文工程对构建强大 Agent 很重要（Why context engineering is important to building capable agents）

Despite their speed and ability to manage larger and larger volumes of data, we've observed that LLMs, like humans, lose focus or experience confusion at a certain point. Studies on needle-in-a-haystack-style benchmarking have uncovered the concept of [context rot](https://research.trychroma.com/context-rot): as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases.

尽管 LLM 速度快、能处理越来越庞大的数据量，但我们观察到，与人类一样，LLM 也会在某个临界点上失去焦点或产生混乱。对"大海捞针"（needle-in-a-haystack）式基准测试的研究揭示了[上下文腐烂（context rot）](https://research.trychroma.com/context-rot)这一概念：随着上下文窗口中的令牌数量增加，模型准确回忆该上下文中信息的能力会下降。

While some models exhibit more gentle degradation than others, this characteristic emerges across all models. Context, therefore, must be treated as a finite resource with diminishing marginal returns. Like humans, who have [limited working memory capacity](https://journals.sagepub.com/doi/abs/10.1177/0963721409359277), LLMs have an "attention budget" that they draw on when parsing large volumes of context. Every new token introduced depletes this budget by some amount, increasing the need to carefully curate the tokens available to the LLM.

虽然有些模型的性能退化比另一些更平缓，但这一特性在所有模型中都会出现。因此，上下文必须被视为一种边际收益递减的有限资源。与[工作记忆容量有限](https://journals.sagepub.com/doi/abs/10.1177/0963721409359277)的人类一样，LLM 也有一笔"注意力预算"（attention budget），在解析大量上下文时会从中支取。每引入一个新令牌都会消耗一部分预算，这更增加了仔细策划 LLM 可用令牌的必要性。

This attention scarcity stems from architectural constraints of LLMs. LLMs are based on the [transformer architecture](https://arxiv.org/abs/1706.03762), which enables every token to [attend to every other token](https://huggingface.co/blog/Esmail-AGumaan/attention-is-all-you-need) across the entire context. This results in n² pairwise relationships for n tokens.

这种注意力的稀缺源于 LLM 的架构约束。LLM 基于 [Transformer 架构](https://arxiv.org/abs/1706.03762)，它使每个令牌都能在整个上下文中[关注其他所有令牌](https://huggingface.co/blog/Esmail-AGumaan/attention-is-all-you-need)。对于 n 个令牌，这会产生 n² 个两两之间的关系。

As its context length increases, a model's ability to capture these pairwise relationships gets stretched thin, creating a natural tension between context size and attention focus. Additionally, models develop their attention patterns from training data distributions where shorter sequences are typically more common than longer ones. This means models have less experience with, and fewer specialized parameters for, context-wide dependencies.

随着上下文长度增加，模型捕捉这些两两关系的能力会被摊薄，从而在上下文规模与注意力聚焦之间产生天然的张力。此外，模型的注意力模式是从训练数据分布中发展而来的，而较短的序列通常比较长的序列更常见。这意味着模型对全上下文依赖的经验更少，用于处理这类依赖的专门参数也更少。

Techniques like [position encoding interpolation](https://arxiv.org/pdf/2306.15595) allow models to handle longer sequences by adapting them to the originally trained smaller context, though with some degradation in token position understanding. These factors create a performance gradient rather than a hard cliff: models remain highly capable at longer contexts but may show reduced precision for information retrieval and long-range reasoning compared to their performance on shorter contexts.

[位置编码插值（position encoding interpolation）](https://arxiv.org/pdf/2306.15595)等技术，通过把长序列适配到原本训练的较小上下文中，让模型能够处理更长的序列，不过在令牌位置理解上会有一些退化。这些因素造成的是性能的渐次下降（gradient）而非陡峭的悬崖：模型在更长上下文上仍然高度能干，但与在较短上下文上的表现相比，在信息检索和长程推理上的精确度可能会降低。

These realities mean that thoughtful context engineering is essential for building capable agents.

这些现实意味着，深思熟虑的上下文工程对于构建强大 Agent 至关重要。

# 有效上下文的解剖（The anatomy of effective context）

Given that LLMs are constrained by a finite attention budget, *good* context engineering means finding the *smallest* *possible* set of high-signal tokens that maximize the likelihood of some desired outcome. Implementing this practice is much easier said than done, but in the following section, we outline what this guiding principle means in practice across the different components of context.

鉴于 LLM 受到有限注意力预算的约束，*好的*上下文工程意味着找到*尽可能小*的高信号（high-signal）令牌集合，以最大程度提高某种期望结果出现的可能性。实践这一原则说起来容易做起来难，但在接下来的章节中，我们将概述这一指导原则在上下文的不同组成部分中究竟意味着什么。

**System prompts** should be extremely clear and use simple, direct language that presents ideas at the *right altitude* for the agent. The right altitude is the Goldilocks zone between two common failure modes. At one extreme, we see engineers hardcoding complex, brittle logic in their prompts to elicit exact agentic behavior. This approach creates fragility and increases maintenance complexity over time. At the other extreme, engineers sometimes provide vague, high-level guidance that fails to give the LLM concrete signals for desired outputs or falsely assumes shared context. The optimal altitude strikes a balance: specific enough to guide behavior effectively, yet flexible enough to provide the model with strong heuristics to guide behavior.

**系统提示词（system prompt）**应当极其清晰，使用简单直接的语言，以对 Agent 而言*恰当的高度（altitude）*呈现想法。恰当的高度是两种常见失败模式之间的"金发姑娘区"（Goldilocks zone）。在一种极端情况下，我们看到工程师在提示词中硬编码复杂、脆弱的逻辑，以诱导出确切的 Agent 行为。这种做法会带来脆弱性，并随时间推移增加维护复杂度。在另一种极端情况下，工程师有时提供模糊、笼统的指导，无法给 LLM 传递关于期望输出的具体信号，或错误地假设了共享上下文。最优的高度是在两者之间取得平衡：既具体得足以有效引导行为，又灵活得足以给模型提供强有力的启发式规则（heuristics）来指导行为。

![提示词的两种极端：一端是脆弱的 if-else 硬编码提示词，另一端是过于笼统或错误假设共享上下文的提示词](images/ctxeng-2.png)

> At one end of the spectrum, we see brittle if-else hardcoded prompts, and at the other end we see prompts that are overly general or falsely assume shared context.
> 光谱的一端是脆弱的 if-else 硬编码提示词，另一端则是过于笼统或错误假设共享上下文的提示词。

We recommend organizing prompts into distinct sections (like `<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`, etc) and using techniques like XML tagging or Markdown headers to delineate these sections, although the exact formatting of prompts is likely becoming less important as models become more capable.

我们建议把提示词组织成不同的部分（如 `<background_information>`、`<instructions>`、`## Tool guidance`、`## Output description` 等），并使用 XML 标签或 Markdown 标题等技巧来划分这些部分，尽管随着模型能力越来越强，提示词的确切格式可能已不那么重要。

Regardless of how you decide to structure your system prompt, you should be striving for the minimal set of information that fully outlines your expected behavior. (Note that minimal does not necessarily mean short; you still need to give the agent sufficient information up front to ensure it adheres to the desired behavior.) It's best to start by testing a minimal prompt with the best model available to see how it performs on your task, and then add clear instructions and examples to improve performance based on failure modes found during initial testing.

无论你决定如何组织系统提示词的结构，你都应追求用最少的信息完整勾勒出你期望的行为。（注意：最少并不一定意味着短；你仍然需要事先给 Agent 足够的信息，以确保它遵循期望的行为。）最好的做法是先用可用的最佳模型测试一个最小化的提示词，看看它在你的任务上表现如何，然后根据初步测试中发现的失败模式，添加清晰的指令和示例来改进性能。

**Tools** allow agents to operate with their environment and pull in new, additional context as they work. Because tools define the contract between agents and their information/action space, it's extremely important that tools promote efficiency, both by returning information that is token efficient and by encouraging efficient agent behaviors.

**工具（tool）**让 Agent 能与环境交互，并在工作时拉入新的、额外的上下文。由于工具定义了 Agent 与其信息/行动空间之间的契约，工具必须促进效率，这一点极其重要——既要返回令牌高效的（token-efficient）信息，也要鼓励高效的 Agent 行为。

In [Writing tools for AI agents – with AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents), we discussed building tools that are well understood by LLMs and have minimal overlap in functionality. Similar to the functions of a well-designed codebase, tools should be self-contained, robust to error, and extremely clear with respect to their intended use. Input parameters should similarly be descriptive, unambiguous, and play to the inherent strengths of the model.

在[用 AI Agent 为 AI Agent 编写工具（Writing tools for AI agents – with AI agents）](https://www.anthropic.com/engineering/writing-tools-for-agents)中，我们讨论了构建被 LLM 充分理解、功能重叠最小的工具。与设计良好的代码库中的函数类似，工具应当自包含、对错误鲁棒，并且在预期用途上极其清晰。输入参数也应当具有描述性、不含歧义，并发挥模型的固有优势。

One of the most common failure modes we see is bloated tool sets that cover too much functionality or lead to ambiguous decision points about which tool to use. If a human engineer can't definitively say which tool should be used in a given situation, an AI agent can't be expected to do better. As we'll discuss later, curating a minimal viable set of tools for the agent can also lead to more reliable maintenance and pruning of context over long interactions.

我们见到的最常见失败模式之一是臃肿的工具集——覆盖了过多功能，或导致关于该用哪个工具的决策点含糊不清。如果人类工程师都无法确定在特定情况下该用哪个工具，就不能指望 AI Agent 做得更好。正如我们稍后讨论的，为 Agent 策划一个最小可行（minimal viable）的工具集，还能在长交互中带来更可靠的维护和上下文修剪。

Providing examples, otherwise known as few-shot prompting, is a well known best practice that we continue to strongly advise. However, teams will often stuff a laundry list of edge cases into a prompt in an attempt to articulate every possible rule the LLM should follow for a particular task. We do not recommend this. Instead, we recommend working to curate a set of diverse, canonical examples that effectively portray the expected behavior of the agent. For an LLM, examples are the "pictures" worth a thousand words.

提供示例（即少样本提示，few-shot prompting）是众所周知的最佳实践，我们继续强烈建议这样做。然而，团队常常会把一长串边界情况塞进提示词，试图阐明 LLM 在特定任务上应遵循的每一条规则。我们不推荐这种做法。相反，我们建议精心策划一组多样化、典型的示例，有效地描绘出 Agent 的期望行为。对 LLM 而言，示例就是"一图胜千言"的图画。

Our overall guidance across the different components of context (system prompts, tools, examples, message history, etc) is to be thoughtful and keep your context informative, yet tight. Now let's dive into dynamically retrieving context at runtime.

我们对上下文各个组成部分（系统提示词、工具、示例、消息历史等）的总体建议是：深思熟虑，让上下文既有信息量，又保持紧凑。现在，让我们深入探讨在运行时动态检索上下文。

# 上下文检索与 Agent 化搜索（Context retrieval and agentic search）

In [Building effective AI agents](https://www.anthropic.com/research/building-effective-agents), we highlighted the differences between LLM-based workflows and agents. Since we wrote that post, we've gravitated towards a [simple definition](https://simonwillison.net/2025/Sep/18/agents/) for agents: LLMs autonomously using tools in a loop.

在[构建有效的 AI Agent（Building effective AI agents）](https://www.anthropic.com/research/building-effective-agents)中，我们强调了基于 LLM 的工作流与 Agent 之间的差异。自从写下那篇文章以来，我们逐渐倾向于一个[简单的定义](https://simonwillison.net/2025/Sep/18/agents/)：Agent 就是 LLM 在循环中自主使用工具。

Working alongside our customers, we've seen the field converging on this simple paradigm. As the underlying models become more capable, the level of autonomy of agents can scale: smarter models allow agents to independently navigate nuanced problem spaces and recover from errors.

在与客户的合作中，我们看到业界正汇聚到这一简单范式上。随着底层模型能力越来越强，Agent 的自主程度也可以随之扩展：更聪明的模型让 Agent 能够独立地在微妙的（nuanced）问题空间中穿行，并从错误中恢复。

We're now seeing a shift in how engineers think about designing context for agents. Today, many AI-native applications employ some form of embedding-based pre-inference time retrieval to surface important context for the agent to reason over. As the field transitions to more agentic approaches, we increasingly see teams augmenting these retrieval systems with "just in time" context strategies.

我们现在看到工程师在思考如何为 Agent 设计上下文时发生了转变。如今，许多 AI 原生应用采用某种基于嵌入（embedding）的推理前检索，来呈现供 Agent 推理的重要上下文。随着业界转向更"Agent 化"的方法，我们越来越多地看到团队用"即时"（just-in-time）上下文策略来增强这些检索系统。

Rather than pre-processing all relevant data up front, agents built with the "just in time" approach maintain lightweight identifiers (file paths, stored queries, web links, etc.) and use these references to dynamically load data into context at runtime using tools. Anthropic's agentic coding solution [Claude Code](https://www.anthropic.com/claude-code) uses this approach to perform complex data analysis over large databases. The model can write targeted queries, store results, and leverage Bash commands like head and tail to analyze large volumes of data without ever loading the full data objects into context. This approach mirrors human cognition: we generally don't memorize entire corpuses of information, but rather introduce external organization and indexing systems like file systems, inboxes, and bookmarks to retrieve relevant information on demand.

采用"即时"方法的 Agent 不会预先处理所有相关数据，而是维护轻量级的标识符（文件路径、已保存的查询、网页链接等），并使用这些引用在运行时通过工具把数据动态加载进上下文。Anthropic 的 Agent 化编程解决方案 [Claude Code](https://www.anthropic.com/claude-code) 就是用这种方法在大型数据库上执行复杂的数据分析。模型可以编写有针对性的查询、保存结果，并利用 head、tail 等 Bash 命令分析大量数据，而无需把完整的数据对象加载进上下文。这种方法映照着人类认知：我们通常不会记住整个信息语料，而是借助文件系统、收件箱、书签等外部组织与索引系统，按需检索相关信息。

Beyond storage efficiency, the metadata of these references provides a mechanism to efficiently refine behavior, whether explicitly provided or intuitive. To an agent operating in a file system, the presence of a file named `test_utils.py` in a `tests` folder implies a different purpose than a file with the same name located in `src/core_logic/`. Folder hierarchies, naming conventions, and timestamps all provide important signals that help both humans and agents understand how and when to utilize information.

除了存储效率之外，这些引用的元数据还提供了一种高效提炼行为的机制，无论这些元数据是显式提供的还是直觉可感的。对于在文件系统中运行的 Agent 来说，一个名为 `test_utils.py` 的文件出现在 `tests` 文件夹中，与同名文件位于 `src/core_logic/` 中意味着不同的用途。文件夹层级、命名约定和时间戳都提供了重要的信号，帮助人类和 Agent 理解如何以及何时利用信息。

Letting agents navigate and retrieve data autonomously also enables progressive disclosure—in other words, allows agents to incrementally discover relevant context through exploration. Each interaction yields context that informs the next decision: file sizes suggest complexity; naming conventions hint at purpose; timestamps can be a proxy for relevance. Agents can assemble understanding layer by layer, maintaining only what's necessary in working memory and leveraging note-taking strategies for additional persistence. This self-managed context window keeps the agent focused on relevant subsets rather than drowning in exhaustive but potentially irrelevant information.

让 Agent 自主地导航和检索数据，也实现了渐进式披露（progressive disclosure）——换句话说，让 Agent 能够通过探索逐步发现相关上下文。每一次交互都会产生指导下一个决策的上下文：文件大小暗示复杂度；命名约定提示用途；时间戳可以作为相关性的代理。Agent 可以一层层地拼装理解，只在工作记忆中保留必要的内容，并利用笔记策略实现额外的持久化。这种自我管理的上下文窗口让 Agent 专注于相关的子集，而不是淹没在详尽但可能无关的信息中。

Of course, there's a trade-off: runtime exploration is slower than retrieving pre-computed data. Not only that, but opinionated and thoughtful engineering is required to ensure that an LLM has the right tools and heuristics for effectively navigating its information landscape. Without proper guidance, an agent can waste context by misusing tools, chasing dead-ends, or failing to identify key information.

当然，这里有权衡：运行时探索比检索预计算数据更慢。不仅如此，还需要有主见、深思熟虑的工程，以确保 LLM 拥有正确的工具和启发式规则，能够有效地在信息疆域中导航。没有恰当的指导，Agent 就可能因误用工具、追逐死胡同或未能识别关键信息而浪费上下文。

In certain settings, the most effective agents might employ a hybrid strategy, retrieving some data up front for speed, and pursuing further autonomous exploration at its discretion. The decision boundary for the 'right' level of autonomy depends on the task. Claude Code is an agent that employs this hybrid model: [CLAUDE.md](http://claude.md) files are naively dropped into context up front, while primitives like glob and grep allow it to navigate its environment and retrieve files just-in-time, effectively bypassing the issues of stale indexing and complex syntax trees.

在特定场景下，最有效的 Agent 可能采用混合策略：预先检索一些数据以获得速度，再自行决定是否进一步自主探索。"合适"自主程度的决策边界取决于任务。Claude Code 就是采用这种混合模型的 Agent：[CLAUDE.md](http://claude.md) 文件会在前期被直接丢进上下文，而 glob、grep 等原语让它可以导航环境、即时检索文件，从而有效避开过期索引和复杂语法树的问题。

The hybrid strategy might be better suited for contexts with less dynamic content, such as legal or finance work. As model capabilities improve, agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation. Given the rapid pace of progress in the field, "do the simplest thing that works" will likely remain our best advice for teams building agents on top of Claude.

混合策略可能更适合内容动态性较低的场景，比如法律或金融工作。随着模型能力提升，Agent 化设计将趋向于让智能模型自主行动，人类策划的成分会越来越少。鉴于该领域进展神速，"做最简单可行的方案"（do the simplest thing that works）很可能仍是我们给基于 Claude 构建 Agent 的团队的最佳建议。

## 长时程任务的上下文工程（Context engineering for long-horizon tasks）

Long-horizon tasks require agents to maintain coherence, context, and goal-directed behavior over sequences of actions where the token count exceeds the LLM's context window. For tasks that span tens of minutes to multiple hours of continuous work, like large codebase migrations or comprehensive research projects, agents require specialized techniques to work around the context window size limitation.

长时程（long-horizon）任务要求 Agent 在令牌数超过 LLM 上下文窗口的动作序列上保持连贯性、上下文和目标导向行为。对于持续数十分钟到数小时的任务，如大型代码库迁移或综合研究项目，Agent 需要专门的技术来绕开上下文窗口大小的限制。

Waiting for larger context windows might seem like an obvious tactic. But it's likely that for the foreseeable future, context windows of all sizes will be subject to context pollution and information relevance concerns—at least for situations where the strongest agent performance is desired. To enable agents to work effectively across extended time horizons, we've developed a few techniques that address these context pollution constraints directly: compaction, structured note-taking, and multi-agent architectures.

等待更大的上下文窗口似乎是一个显而易见的策略。但在可预见的未来，各种大小的上下文窗口都可能面临上下文污染和信息相关性方面的担忧——至少在追求最强 Agent 性能的场景下是如此。为了让 Agent 能在更长的时间跨度上高效工作，我们开发了几种直接应对这些上下文污染约束的技术：压缩（compaction）、结构化笔记（structured note-taking）和多 Agent 架构（multi-agent architectures）。

**Compaction**

**压缩（Compaction）**

Compaction is the practice of taking a conversation nearing the context window limit, summarizing its contents, and reinitiating a new context window with the summary. Compaction typically serves as the first lever in context engineering to drive better long-term coherence. At its core, compaction distills the contents of a context window in a high-fidelity manner, enabling the agent to continue with minimal performance degradation.

压缩是对接近上下文窗口上限的对话进行内容总结，并用这份总结开启一个新的上下文窗口的做法。压缩通常是上下文工程中推动更好长期连贯性的第一根杠杆。其核心是以高保真的方式提炼上下文窗口的内容，让 Agent 能够以最小的性能损失继续工作。

In Claude Code, for example, we implement this by passing the message history to the model to summarize and compress the most critical details. The model preserves architectural decisions, unresolved bugs, and implementation details while discarding redundant tool outputs or messages. The agent can then continue with this compressed context plus the five most recently accessed files. Users get continuity without worrying about context window limitations.

例如，在 Claude Code 中，我们通过把消息历史传给模型来总结并压缩最关键细节，从而实现这一功能。模型会保留架构决策、未解决的 bug 和实现细节，同时丢弃冗余的工具输出或消息。随后，Agent 可以带着这份压缩后的上下文以及最近访问的五个文件继续工作。用户既获得了连续性，又不必担心上下文窗口的限制。

The art of compaction lies in the selection of what to keep versus what to discard, as overly aggressive compaction can result in the loss of subtle but critical context whose importance only becomes apparent later. For engineers implementing compaction systems, we recommend carefully tuning your prompt on complex agent traces. Start by maximizing recall to ensure your compaction prompt captures every relevant piece of information from the trace, then iterate to improve precision by eliminating superfluous content.

压缩的艺术在于保留什么与丢弃什么的选择，因为过于激进的压缩可能导致微妙却关键的上下文丢失，而这些上下文的重要性只有在后来才会显现。对于实现压缩系统的工程师，我们建议在复杂的 Agent 轨迹（trace）上仔细调优你的提示词。先以最大化召回（recall）为目标，确保你的压缩提示词捕捉到轨迹中的每一条相关信息，然后通过消除多余内容来迭代提高精确度（precision）。

An example of low-hanging superfluous content is clearing tool calls and results – once a tool has been called deep in the message history, why would the agent need to see the raw result again? One of the safest lightest touch forms of compaction is tool result clearing, most recently launched as a [feature on the Claude Developer Platform](https://www.anthropic.com/news/context-management).

一个唾手可得的冗余内容例子是清除工具调用及其结果——一旦某个工具在消息历史深处被调用过，Agent 为什么还需要再看一遍原始结果呢？最安全、最轻量的压缩形式之一是清除工具结果（tool result clearing），它最近已作为[ Claude 开发者平台的一项功能](https://www.anthropic.com/news/context-management)发布。

**Structured note-taking**

**结构化笔记（Structured note-taking）**

Structured note-taking, or agentic memory, is a technique where the agent regularly writes notes persisted to memory outside of the context window. These notes get pulled back into the context window at later times.

结构化笔记，也称 Agent 记忆（agentic memory），是一种让 Agent 定期把笔记写入上下文窗口之外的持久化记忆的技术。这些笔记会在之后的某个时刻被拉回上下文窗口。

This strategy provides persistent memory with minimal overhead. Like Claude Code creating a to-do list, or your custom agent maintaining a NOTES.md file, this simple pattern allows the agent to track progress across complex tasks, maintaining critical context and dependencies that would otherwise be lost across dozens of tool calls.

这一策略以极小的开销提供持久记忆。就像 Claude Code 创建待办清单，或你的自定义 Agent 维护一个 NOTES.md 文件一样，这种简单的模式让 Agent 能够在复杂任务中跟踪进度，保住那些否则会在几十次工具调用中丢失的关键上下文和依赖。

[Claude playing Pokémon](https://www.twitch.tv/claudeplayspokemon) demonstrates how memory transforms agent capabilities in non-coding domains. The agent maintains precise tallies across thousands of game steps—tracking objectives like "for the last 1,234 steps I've been training my Pokémon in Route 1, Pikachu has gained 8 levels toward the target of 10." Without any prompting about memory structure, it develops maps of explored regions, remembers which key achievements it has unlocked, and maintains strategic notes of combat strategies that help it learn which attacks work best against different opponents.

[Claude 玩宝可梦（Claude playing Pokémon）](https://www.twitch.tv/claudeplayspokemon)展示了记忆如何在非编程领域转变 Agent 的能力。这个 Agent 在数千个游戏步骤中保持着精确的统计——跟踪诸如"在过去的 1,234 步里，我一直在 1 号道路训练我的宝可梦，皮卡丘已经升了 8 级，目标 10 级"这样的目标。在没有任何关于记忆结构的提示下，它会绘制已探索区域的地图、记住自己解锁了哪些关键成就，并维护战斗策略的战略笔记，帮助它学习哪些招式对不同对手最有效。

After context resets, the agent reads its own notes and continues multi-hour training sequences or dungeon explorations. This coherence across summarization steps enables long-horizon strategies that would be impossible when keeping all the information in the LLM's context window alone.

上下文重置之后，Agent 会阅读自己的笔记，继续长达数小时的训练序列或地牢探索。这种跨总结步骤的连贯性，使得那些仅靠把全部信息留在 LLM 上下文窗口里根本无法实现的长时程策略成为可能。

As part of our [Sonnet 4.5 launch](https://www.anthropic.com/effective-context-engineering-for-ai-agents), we released [a memory tool](http://anthropic.com/news/context-management) in public beta on the Claude Developer Platform that makes it easier to store and consult information outside the context window through a file-based system. This allows agents to build up knowledge bases over time, maintain project state across sessions, and reference previous work without keeping everything in context.

作为 [Sonnet 4.5 发布](https://www.anthropic.com/effective-context-engineering-for-ai-agents)的一部分，我们在 Claude 开发者平台上以公开测试版发布了一个[记忆工具（memory tool）](http://anthropic.com/news/context-management)，通过基于文件的系统，让在上下文窗口之外存储和查阅信息变得更加容易。这让 Agent 能够随时间积累知识库、跨会话维护项目状态、引用之前的工作，而无需把所有内容都留在上下文中。

**Sub-agent architectures**

**子 Agent 架构（Sub-agent architectures）**

Sub-agent architectures provide another way around context limitations. Rather than one agent attempting to maintain state across an entire project, specialized sub-agents can handle focused tasks with clean context windows. The main agent coordinates with a high-level plan while subagents perform deep technical work or use tools to find relevant information. Each subagent might explore extensively, using tens of thousands of tokens or more, but returns only a condensed, distilled summary of its work (often 1,000-2,000 tokens).

子 Agent（subagent）架构提供了另一种绕开上下文限制的方法。与其让一个 Agent 试图在整个项目中维护状态，不如让专业的子 Agent 用干净的上下文窗口处理聚焦的任务。主 Agent 用高层计划进行协调，而子 Agent 执行深入的技术工作，或使用工具查找相关信息。每个子 Agent 都可能进行广泛探索，消耗数万甚至更多令牌，但只会返回一份浓缩、提炼的工作总结（通常 1,000-2,000 令牌）。

This approach achieves a clear separation of concerns—the detailed search context remains isolated within sub-agents, while the lead agent focuses on synthesizing and analyzing the results. This pattern, discussed in [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system), showed a substantial improvement over single-agent systems on complex research tasks.

这种方法实现了清晰的关注点分离（separation of concerns）——详细的搜索上下文被隔离在子 Agent 内部，而主导 Agent 专注于综合和分析结果。这一模式在[我们如何构建多 Agent 研究系统（How we built our multi-agent research system）](https://www.anthropic.com/engineering/multi-agent-research-system)中讨论过，它在复杂研究任务上相比单 Agent 系统表现出大幅改进。

The choice between these approaches depends on task characteristics. For example:

在这些方法之间做选择取决于任务特征。例如：

- Compaction maintains conversational flow for tasks requiring extensive back-and-forth;
  - 压缩（compaction）为需要大量来回交流的任务保持对话的流畅；
- Note-taking excels for iterative development with clear milestones;
  - 笔记（note-taking）擅长带有清晰里程碑的迭代式开发；
- Multi-agent architectures handle complex research and analysis where parallel exploration pays dividends.
  - 多 Agent 架构（multi-agent architectures）处理并行探索回报丰厚的复杂研究与分析。

Even as models continue to improve, the challenge of maintaining coherence across extended interactions will remain central to building more effective agents.

即便模型持续改进，在扩展交互中保持连贯性的挑战，仍将是构建更高效 Agent 的核心问题。

# 结论（Conclusion）

Context engineering represents a fundamental shift in how we build with LLMs. As models become more capable, the challenge isn't just crafting the perfect prompt—it's thoughtfully curating what information enters the model's limited attention budget at each step. Whether you're implementing compaction for long-horizon tasks, designing token-efficient tools, or enabling agents to explore their environment just-in-time, the guiding principle remains the same: find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome.

上下文工程代表了我们在使用 LLM 构建方式上的根本转变。随着模型能力越来越强，挑战不再仅仅是写出完美的提示词——而是在每一步都深思熟虑地策划，什么样的信息进入模型有限的注意力预算。无论你是在为长时程任务实现压缩、设计令牌高效的工具，还是让 Agent 即时探索环境，指导原则始终如一：找到最小的、高信号的令牌集合，以最大程度提高期望结果出现的可能性。

The techniques we've outlined will continue evolving as models improve. We're already seeing that smarter models require less prescriptive engineering, allowing agents to operate with more autonomy. But even as capabilities scale, treating context as a precious, finite resource will remain central to building reliable, effective agents.

我们概述的这些技术会随着模型的改进而不断演进。我们已经看到，更聪明的模型需要更少的规范性（prescriptive）工程，让 Agent 能够以更高的自主性运作。但即便能力持续扩展，把上下文视为宝贵而有限的资源，仍将是构建可靠、高效 Agent 的核心。

Get started with context engineering in the Claude Developer Platform today, and access helpful tips and best practices via our [memory and context management](https://platform.claude.com/cookbook/tool-use-memory-cookbook) cookbook.

今天就在 Claude 开发者平台上开始上下文工程实践，并通过我们的[记忆与上下文管理（memory and context management）](https://platform.claude.com/cookbook/tool-use-memory-cookbook)手册获取实用的技巧和最佳实践。

# 致谢（Acknowledgements）

Written by Anthropic's Applied AI team: Prithvi Rajasekaran, Ethan Dixon, Carly Ryan, and Jeremy Hadfield, with contributions from team members Rafi Ayub, Hannah Moran, Cal Rueb, and Connor Jennings. Special thanks to Molly Vorwerck, Stuart Ritchie, and Maggie Vo for their support.

由 Anthropic 应用 AI 团队撰写：Prithvi Rajasekaran、Ethan Dixon、Carly Ryan 和 Jeremy Hadfield，团队成员 Rafi Ayub、Hannah Moran、Cal Rueb 和 Connor Jennings 亦有贡献。特别感谢 Molly Vorwerck、Stuart Ritchie 和 Maggie Vo 的支持。
