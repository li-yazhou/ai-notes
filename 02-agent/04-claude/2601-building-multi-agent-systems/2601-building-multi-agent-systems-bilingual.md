# 构建多智能体系统：何时使用与如何使用（中英对照）

> **原文标题：** Building multi-agent systems: When and how to use them
> **作者：** Cara Phillips（贡献者：Paul Chen、Andy Schumeister、Brad Abrams、Theo Chu）
> **原文链接：** https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them
> **发布日期：** 2026-01-23
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

When to use multi-agent systems-and when not to. Anthropic's guidance on orchestrator patterns, building on our multi-agent research system.

何时使用多智能体系统--以及何时不使用。Anthropic 基于我们的多智能体研究系统给出的编排器（orchestrator）模式指南。

While single-agent systems handle most enterprise workflows effectively, multi-agent architectures can unlock additional value for your organization. Learn when and how to use them.

虽然单智能体系统就能有效处理大多数企业工作流，但多智能体架构可以为你的组织解锁额外价值。本文将介绍何时以及如何使用它们。

# 什么是多智能体系统？（What is a multi-agent system?）

A multi-agent system is an architecture where multiple LLM instances run with separate conversation contexts, coordinated through code. Each agent handles a distinct slice of a task - a subagent researches while an orchestrator plans, for example - which protects context, enables parallel work, and allows specialization a single agent can't sustain.

多智能体系统（multi-agent system）是一种由多个 LLM 实例在各自独立的对话上下文中运行、并通过代码进行协调的架构。每个智能体负责任务的一个明确切片--例如，一个子智能体（subagent）负责调研，而编排器（orchestrator）负责规划--这样可以保护上下文、支持并行工作，并实现单个智能体难以维系的专门化（specialization）。

Multiple coordination patterns exist (agent swarms, capability-based systems, and message bus architectures), but this article focuses on the orchestrator-subagent pattern: a hierarchical model where a lead agent spawns and manages specialized subagents for specific subtasks. This pattern offers a straightforward coordination model and is a good starting point for teams new to multi-agent systems. We'll explore other patterns in detail in our next article.

现存的协调模式有多种（智能体集群（agent swarm）、基于能力的系统、消息总线架构等），但本文聚焦于编排器-子智能体（orchestrator-subagent）模式：一种由主智能体（lead agent）为特定子任务生成并管理专门化子智能体的分层模型。这种模式提供了直观的协调模型，是初次接触多智能体系统的团队的良好起点。我们将在下一篇文章中详细探讨其他模式。

Today, multi-agent systems are often applied in situations where a single agent would perform better, though this calculus continues to evolve as models improve. At Anthropic, we've seen teams invest months building elaborate multi-agent architectures only to discover that improved prompting on a single agent achieved equivalent results.

如今，多智能体系统常常被用在单智能体本可以表现更好的场景中，不过随着模型改进，这种权衡还在持续变化。在 Anthropic，我们见过团队投入数月构建复杂的多智能体架构，结果却发现只需改进单个智能体的提示词（prompting）就能取得同等效果。

After building multi-agent systems and working with teams deploying them in production, we've identified three situations where multiple agents consistently outperform a single agent: when context pollution degrades performance, when tasks can run in parallel, and when specialization improves tool selection or task focus. Outside these situations, the coordination costs typically exceed the benefits.In this article, we share how to recognize single-agent limits, identify the three scenarios where multi-agent systems excel, and avoid common implementation mistakes.

在构建多智能体系统并与在生产环境中部署它们的团队合作之后，我们总结出多个智能体始终优于单个智能体的三种情形：上下文污染（context pollution）降低性能时、任务可以并行运行时、以及专门化能改善工具选择或任务专注度时。在这些情形之外，协调成本通常超过收益。在本文中，我们将分享如何识别单智能体的极限、找出多智能体系统擅长的三种场景，并避免常见的实现错误。

# 从单智能体起步的理由（The case for starting with a single agent）

A well-designed single agent with appropriate tools can accomplish far more than many developers expect.

一个设计良好、配备合适工具的单智能体，能完成的工作远超许多开发者的预期。

Multi-agent systems introduce overhead. Every additional agent represents another potential point of failure, another set of prompts to maintain, and another source of unexpected behavior.

多智能体系统会引入额外开销。每增加一个智能体，就意味着多一个潜在故障点、多一组需要维护的提示词，以及多一个意外行为的来源。

We've observed teams build elaborate multi-agent systems with separate agents for planning, execution, review, and iteration, only to discover that they suffered from lost context at each handoff and spent more tokens coordinating than executing. In our testing, multi-agent implementations typically use 3-10x more tokens than single-agent approaches for equivalent tasks. This overhead stems from duplicating context across agents, coordination messages between agents, and summarizing results for handoffs.

我们观察到一些团队构建了复杂的多智能体系统，分别设置规划、执行、评审和迭代的独立智能体，结果却发现每次交接都会丢失上下文，而且用于协调的 token 比用于执行的还多。在我们的测试中，完成同等任务时，多智能体实现所消耗的 token 通常是单智能体方案的 3-10 倍。这种开销来自跨智能体复制上下文、智能体之间的协调消息，以及为交接而做的结果摘要。

# 多智能体系统的决策框架（A decision framework for multi-agent systems）

Multi-agent architectures provide value when they address specific constraints that a single agent cannot overcome. This means multi-agent architectures should be reserved for cases where they provide clear benefits that justify the additional cost. Managed infrastructure can also handle this for you (see multiagent orchestration in Claude Managed Agents).

只有当多智能体架构能够解决单智能体无法突破的特定约束时，它才创造价值。这意味着应把多智能体架构留给那些收益明确、足以抵偿额外成本的场合。托管基础设施也可以替你处理这些事（参见 Claude Managed Agents 中的 multiagent orchestration）。

The patterns below represent cases where we consistently observe positive returns on this investment.

以下模式是我们在实践中持续观察到这类投入获得正向回报的场景。

## 上下文保护（Context protection）

Large language models have finite context windows, and response quality can degrade as context grows. When an agent's context accumulates information from one subtask that is irrelevant to subsequent subtasks, context pollution occurs. Subagents provide isolation, with each operating in its own clean context focused on its specific task.

大语言模型的上下文窗口（context window）是有限的，且随着上下文增长，响应质量可能下降。当智能体的上下文中积累了来自某个子任务、但与后续子任务无关的信息时，就会发生上下文污染。子智能体提供了隔离性--每个子智能体都在自己干净的上下文中专注于特定任务。

Consider a customer support agent that needs to retrieve order history while diagnosing technical issues. If every order lookup adds thousands of tokens to the context, the agent's ability to reason about the technical problem degrades.

设想一个客户支持智能体，需要在诊断技术问题的同时检索订单历史。如果每次订单查询都往上下文里塞进数千个 token，智能体推理技术问题的能力就会下降。

The single-agent approach:

单智能体方案：

```python
# Single agent accumulates everything in context
conversation_history = [
    {"role": "user", "content": "My order #12345 isn't working"},
    {"role": "assistant", "content": "Let me check your order..."},
    # Tool result adds 2000+ tokens of order history
    {"role": "user", "content": "... (order details, past purchases, shipping info) ..."},
    {"role": "assistant", "content": "Now let me diagnose the technical issue..."},
    # Context is now polluted with order details the agent doesn't need
]
```

The agent must reason about the technical issue while maintaining 2000+ tokens of irrelevant order history in context, diluting attention and reducing response quality.

这个智能体必须在上下文中保留 2000 多个 token 的无关订单历史的同时推理技术问题，这会稀释注意力并降低响应质量。

The multi-agent approach:

多智能体方案：

```python
from anthropic import Anthropic

client = Anthropic()

class OrderLookupAgent:
    def lookup_order(self, order_id: str) -> dict:
        # Separate agent with its own context
        messages = [
            {"role": "user", "content": f"Get essential details for order {order_id}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            messages=messages,
            tools=[get_order_details_tool]
        )
        # Returns only essential information
        return extract_summary(response)

class SupportAgent:
    def handle_issue(self, user_message: str):
        if needs_order_info(user_message):
            order_id = extract_order_id(user_message)
            # Get only what's needed, not full history
            order_summary = OrderLookupAgent().lookup_order(order_id)
            # Inject compact summary, not full context
            context = f"Order {order_id}: {order_summary['status']}, purchased {order_summary['date']}"
            # Main agent context stays clean
        messages = [
            {"role": "user", "content": f"{context}\n\nUser issue: {user_message}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2048,
            messages=messages
        )
        return response
```

The order lookup agent processes the full order history and extracts a summary. The main agent receives only the 50-100 tokens it actually needs, keeping context focused.

订单查询智能体处理完整的订单历史并提取摘要。主智能体只接收它真正需要的 50-100 个 token，从而保持上下文聚焦。

Context isolation is most effective when subtasks generate high context volume (more than 1000 tokens) but most of that information is irrelevant to the main task, when the subtask is well-defined with clear criteria for what information to extract, and for lookup or retrieval operations that require filtering before use.

上下文隔离在以下情况最为有效：子任务产生大量上下文（超过 1000 个 token）但其中大部分信息与主任务无关；子任务定义明确、对要提取哪些信息有清晰的标准；以及那些在使用前需要先行过滤的查询或检索操作。

## 并行化（Parallelization）

Running multiple agents in parallel allows you to explore a larger search space than a single agent can cover. This pattern has proven particularly valuable for search and research tasks.

并行运行多个智能体，可以探索单个智能体无法覆盖的更大搜索空间。这种模式在搜索和研究类任务中已被证明尤其有价值。

Anthropic's research team documented this in how we built our multi-agent research system. A lead agent analyzes a query and spawns multiple subagents to investigate different facets in parallel. Each subagent searches independently, then returns distilled findings. Multi-agent search has shown substantial accuracy improvements over single-agent approaches by allowing exploration across larger information spaces.

Anthropic 的研究团队在"我们如何构建多智能体研究系统"（how we built our multi-agent research system）一文中记录了这一点。主智能体分析查询，然后生成多个子智能体并行调查不同的侧面。每个子智能体独立搜索，然后返回提炼后的发现。凭借在更大信息空间中的探索能力，多智能体搜索相较单智能体方案已展现出显著的准确性提升。

The core implementation decomposes a question into independent facets, runs subagents concurrently, then synthesizes the results.

核心实现是将问题分解为相互独立的侧面，并发运行子智能体，然后综合结果。

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def research_topic(query: str) -> dict:
    # Lead agent breaks query into research facets
    facets = await lead_agent.decompose_query(query)

    # Spawn subagents to research each facet in parallel
    tasks = [
        research_subagent(facet)
        for facet in facets
    ]
    results = await asyncio.gather(*tasks)

    # Lead agent synthesizes findings
    return await lead_agent.synthesize(results)

async def research_subagent(facet: str) -> dict:
    """Each subagent has its own context window"""
    messages = [
        {"role": "user", "content": f"Research: {facet}"}
    ]
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4096,
        messages=messages,
        tools=[web_search, read_document]
    )
    return extract_findings(response)
```

This improved coverage comes at a cost. Multi-agent systems typically consume 3 to 10 times more tokens than single-agent approaches for equivalent tasks. This happens because each agent needs its own context, agents must exchange messages to coordinate, and results must be summarized when passed between agents. While parallelism helps reduce total execution time compared to running all that work sequentially, multi-agent systems often take longer overall than single-agent systems because of the sheer increase in total computation.

覆盖面的提升是有代价的。完成同等任务时，多智能体系统通常消耗 3 到 10 倍于单智能体方案的 token。原因在于：每个智能体都需要自己的上下文，智能体之间必须交换消息来协调，结果在智能体之间传递时还必须被摘要。虽然与顺序执行全部工作相比，并行有助于缩短总执行时间，但由于总计算量大幅增加，多智能体系统的整体耗时往往仍长于单智能体系统。

The primary benefit of parallelization is thoroughness, not speed. When you need to search across a large information space or investigate many angles of a complex question, parallel agents can cover more ground than a single agent working within its context limits. The tradeoff is higher token usage and often longer total execution time in exchange for more comprehensive results.

并行化的首要收益是彻底性，而非速度。当你需要在庞大的信息空间中搜索，或从多个角度调查一个复杂问题时，并行智能体所能覆盖的范围比在自身上下文限制内工作的单个智能体更大。其权衡是更高的 token 用量、往往更长的总执行时间，换来更全面的结果。

## 专门化（Specialization）

Different tasks sometimes benefit from different tool sets, system prompts, or domains of expertise. Rather than providing a single agent with access to dozens of tools, specialized agents with focused toolsets matched to their responsibilities can improve reliability.

不同的任务有时会受益于不同的工具集、系统提示词（system prompt）或专业领域。与其让单个智能体访问几十个工具，不如让专门化智能体拥有与其职责匹配的精简工具集，这样可以提升可靠性。

### 工具集专门化（Tool set specialization）

When an agent has access to too many tools, performance suffers. Three signals indicate tool specialization would help:

当智能体可以访问的工具过多时，性能会受损。以下三个信号表明工具专门化会有帮助：

- Quantity. An agent with too many tools (often 20+) struggles to select the appropriate one.
- Domain confusion. When tools span multiple unrelated domains (database operations, API calls, file system operations), the agent confuses which domain applies to a given task.
- Degraded performance. Adding new tools degrades performance on existing tasks, suggesting the agent has reached its capacity for tool management.

- 数量。工具太多（通常超过 20 个）的智能体难以选出合适的工具。
- 领域混淆。当工具横跨多个不相关的领域（数据库操作、API 调用、文件系统操作）时，智能体会搞不清哪个领域适用于当前任务。
- 性能下降。新增工具会拖累现有任务的表现，说明智能体管理工具的能力已经达到上限。

### 系统提示词专门化（System prompt specialization）

Different tasks sometimes require different personas, constraints, or instructions that conflict when combined. A customer support agent needs to be empathetic and patient; a code review agent needs to be precise and critical. A compliance-checking agent needs rigid rule-following; a brainstorming agent needs creative flexibility. When a single agent must switch between conflicting behavioral modes, separating into specialized agents with tailored system prompts produces more consistent results.

不同的任务有时需要不同的人设、约束或指令，而它们组合在一起会相互冲突。客户支持智能体需要富于同理心且有耐心；代码评审智能体需要精确而挑剔。合规检查智能体需要严格照章办事；头脑风暴智能体需要创造性的灵活。当单个智能体必须在相互冲突的行为模式之间切换时，拆分成拥有各自定制系统提示词的专门化智能体会产生更稳定一致的结果。

Each specialized agent is only as good as its instructions - the same prompt engineering best practices that improve a single agent's outputs apply to every subagent's system prompt.

每个专门化智能体的表现取决于其指令--那些能改善单智能体输出的提示词工程（prompt engineering）最佳实践，同样适用于每个子智能体的系统提示词。

### 领域专长专门化（Domain expertise specialization）

Some tasks benefit from deep domain context that would overwhelm a generalist agent. A legal analysis agent might need extensive context about case law and regulatory frameworks. A medical research agent might need specialized knowledge about clinical trial methodology. Rather than loading all domain context into a single agent, specialized agents can carry focused expertise relevant to their specific responsibilities.

有些任务受益于深度的领域上下文，而这些上下文会把一个通用型智能体压垮。法律分析智能体可能需要关于判例法和监管框架的大量背景；医学研究智能体可能需要关于临床试验方法论的专业知识。与其把所有领域上下文都装进单个智能体，不如让专门化智能体各自携带与其具体职责相关的聚焦专长。

Example: Multi-platform integration. Consider an integration system where agents need to work across CRM, marketing automation, and messaging platforms. Each platform has 10-15 relevant API endpoints. A single agent with 40+ tools often struggles to select correctly, confusing similar operations across platforms. Splitting into specialized agents with focused toolsets and tailored prompts resolves selection errors.

示例：多平台集成。设想一个集成系统，智能体需要在 CRM、营销自动化和消息平台之间协同工作。每个平台有 10-15 个相关的 API 端点。拥有 40 多个工具的单智能体常常难以正确选择，把各平台之间的相似操作混为一谈。拆分成拥有精简工具集和定制提示词的专门化智能体后，选择错误便得以消除。

```python
from anthropic import Anthropic

client = Anthropic()

# Specialized agents with focused toolsets and tailored prompts
class CRMAgent:
    """Handles customer relationship management operations"""
    system_prompt = """You are a CRM specialist. You manage contacts, opportunities, and account records. Always verify record ownership before updates and maintain data integrity across related records."""
    tools = [
        crm_get_contacts,
        crm_create_opportunity,
        # 8-10 CRM-specific tools
    ]

class MarketingAgent:
    """Handles marketing automation operations"""
    system_prompt = """You are a marketing automation specialist. You manage campaigns, lead scoring, and email sequences. Prioritize data hygiene and respect contact preferences."""
    tools = [
        marketing_get_campaigns,
        marketing_create_lead,
        # 8-10 marketing-specific tools
    ]

class OrchestratorAgent:
    """Routes requests to specialized agents"""
    def execute(self, user_request: str):
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system="""You coordinate platform integrations. Route requests to the appropriate specialist: - CRM: Contact records, opportunities, accounts, sales pipeline - Marketing: Campaigns, lead nurturing, email sequences, scoring - Messaging: Notifications, alerts, team communication""",
            messages=[
                {"role": "user", "content": user_request}
            ],
            tools=[delegate_to_crm, delegate_to_marketing, delegate_to_messaging]
        )
        return response
```

This pattern mirrors effective professional collaboration, where specialists with tools matched to their roles collaborate more effectively than generalists attempting to maintain expertise across all domains. However, specialization introduces routing complexity. The orchestrator must correctly classify requests and delegate to the right agent, and misrouting leads to poor results. Maintaining multiple specialized agents also increases prompt maintenance overhead. Specialization works best when domains are clearly separable and routing decisions are unambiguous.

这种模式反映了高效的专业协作：工具与角色相匹配的专家，比试图在所有领域保持专业水准的通才协作得更有效。不过，专门化也引入了路由复杂性。编排器必须正确分类请求并委派给合适的智能体，路由错误会导致糟糕的结果。维护多个专门化智能体还会增加提示词维护开销。当领域可以清晰分离且路由决策毫无歧义时，专门化的效果最好。

# 当单智能体架构不再够用时（Outgrowing single-agent architectures）

Beyond the general framework, certain concrete signals suggest that single-agent patterns have been outgrown:

除上述总体框架外，还有一些具体信号表明单智能体模式已经不够用了：

Approaching context limits.If an agent routinely uses large amounts of context and performance is degrading, context pressure may be the bottleneck. Note that recent advances in context management (such as compaction) are reducing this limitation, allowing single agents to maintain effective memory across much longer horizons.

逼近上下文限制。如果智能体经常使用大量上下文且性能持续下降，上下文压力可能就是瓶颈。请注意，上下文管理方面的最新进展（如压缩（compaction））正在削弱这一限制，使单智能体能够在长得多的时间跨度上维持有效记忆。

Managing many tools. When an agent has 15-20+ tools, the model spends significant context and attention understanding its options. Before adopting a multi-agent architecture, consider using the Tool Search Tool, which lets Claude dynamically discover tools on-demand rather than loading all definitions upfront. This can reduce token usage by up to 85% while improving tool selection accuracy.

管理过多工具。当智能体拥有 15-20 个以上的工具时，模型要花费大量上下文和注意力来理解自己的可选项。在采用多智能体架构之前，可以考虑使用 Tool Search Tool，它让 Claude 按需动态发现工具，而不是预先加载全部定义。这最多可减少 85% 的 token 用量，同时提升工具选择的准确性。

Parallelizable subtasks. When tasks naturally decompose into independent pieces (research across multiple sources, tests for multiple components), parallel subagents can provide substantial speedups.

可并行的子任务。当任务可以自然分解为独立的部分（跨多个来源的调研、针对多个组件的测试）时，并行子智能体能带来大幅提速。

These thresholds will shift as models improve. Current limits represent practical guidelines, not fundamental constraints.

随着模型改进，这些阈值也会变化。当前的限制只是实践参考，并非根本性约束。

# 以上下文为中心的任务分解（Context-centric decomposition）

When adopting a multi-agent architecture, the most important design decision is how to divide work between agents. We've observed that teams frequently make this choice incorrectly, leading to coordination overhead that negates the benefits of multi-agent design.

采用多智能体架构时，最重要的设计决策是如何在智能体之间划分工作。我们观察到，团队常常在这件事上做出错误选择，导致协调开销抵消了多智能体设计的收益。

The key insight is to adopt a context-centric view rather than a problem-centric view when decomposing work.

关键在于：分解工作时应采取以上下文为中心的视角，而不是以问题为中心的视角。

Problem-centric decomposition (often counterproductive). Dividing by type of work (one agent writes features, another writes tests, a third reviews code) creates constant coordination overhead. Each handoff loses context. The test-writing agent lacks knowledge of why certain implementation decisions were made and the code reviewer lacks the context of exploration and iteration.

以问题为中心的分解（往往适得其反）。按工作类型划分（一个智能体写功能、另一个写测试、第三个评审代码）会带来持续不断的协调开销。每次交接都会丢失上下文：写测试的智能体不了解某些实现决策的缘由，代码评审者也缺乏探索与迭代过程的上下文。

Context-centric decomposition (usually effective). Dividing by context boundaries means an agent handling a feature should also handle its tests, because it already possesses the necessary context. Work should only be split when context can be truly isolated.

以上下文为中心的分解（通常有效）。按上下文边界划分意味着负责某个功能的智能体也应负责该功能的测试，因为它已经具备所需的上下文。只有当上下文能够被真正隔离时，才应该拆分工作。

This principle emerges from observing failure modes in multi-agent systems. When agents are split by problem type, they engage in a "telephone game," passing information back and forth with each handoff degrading fidelity. In one experiment with agents specialized by software development role (planner, implementer, tester, reviewer), the subagents spent more tokens on coordination than on actual work.

这一原则来自对多智能体系统失败模式的观察。当智能体按问题类型拆分时，它们会陷入"传话游戏"（telephone game），信息来回传递，每次交接都在损失保真度。在一个按软件开发角色（规划者、实现者、测试者、评审者）专门化智能体的实验中，子智能体花在协调上的 token 比花在实际工作上的还多。

Effective decomposition boundaries include:

有效的分解边界包括：

- Independent research paths. Investigating "market trends in Asia" versus "market trends in Europe" can proceed in parallel with no shared context.
- Separate components with clean interfaces. With a well-defined API contract, frontend and backend work can proceed in parallel.
- Blackbox verification. A verifier that only needs to run tests and report results does not require implementation context.

- 相互独立的研究路径。调研"亚洲市场趋势"与"欧洲市场趋势"可以并行推进，无需共享上下文。
- 接口清晰的独立组件。只要有定义良好的 API 契约，前端与后端工作就能并行推进。
- 黑盒验证。只需运行测试并报告结果的验证者，不需要实现上下文。

Problematic decomposition boundaries include:

有问题的分解边界包括：

- Sequential phases of the same work. Planning, implementation, and testing of the same feature share too much context.
- Tightly coupled components. Components requiring constant back-and-forth belong in the same agent.
- Work requiring shared state. Agents that would need to frequently synchronize understanding should remain together.

- 同一工作的顺序阶段。同一功能的规划、实现与测试共享的上下文太多。
- 紧耦合的组件。需要不断来回沟通的组件应放在同一个智能体里。
- 需要共享状态的工作。需要频繁同步认知的智能体应当保持在一起。

# 验证子智能体模式（The verification subagent pattern）

One multi-agent pattern that consistently works well across domains is the verification subagent. This is a dedicated agent whose sole responsibility is testing or validating the main agent's work.

有一种在各领域都始终表现良好的多智能体模式：验证子智能体（verification subagent）。这是一个专职智能体，其唯一职责就是测试或验证主智能体的工作。

It's worth noting that more capable orchestrator models (like Claude Opus 4.5) are increasingly able to evaluate subagent work directly without a separate verification step. However, verification subagents remain valuable when using less capable orchestrators, when verification requires specialized tools, or when you want to enforce explicit verification checkpoints in your workflow.

值得注意的是，能力更强的编排器模型（如 Claude Opus 4.5）越来越能够直接评估子智能体的工作，而无需单独的验证步骤。不过，在使用能力较弱的编排器、验证需要专门工具、或者你希望在工作流中强制设置显式验证检查点时，验证子智能体仍然很有价值。

Verification subagents succeed because they sidestep the telephone game problem. Verification requires minimal context transfer by nature, so a verifier can blackbox-test a system without needing the full history of how it was built.

验证子智能体之所以有效，是因为它绕开了传话游戏问题。验证天然只需极少的上下文传递，因此验证者可以对系统做黑盒测试，而无须了解系统构建的完整历史。

## 实现多智能体系统（Implementating a multi-agent system）

The main agent completes a unit of work. Before proceeding, it spawns a verification subagent with the artifact to verify, clear success criteria, and tools to perform verification.

主智能体完成一个工作单元。在继续之前，它会生成一个验证子智能体，把待验证的产出物（artifact）、清晰的成功标准和执行验证所需的工具一并交给它。

The verifier does not need to understand why the artifact was built as it was. It only needs to determine whether the artifact meets the specified criteria.

验证者不需要理解产出物为何被构建成这样，只需要判定它是否满足指定的标准。

```python
from anthropic import Anthropic

client = Anthropic()

class CodingAgent:
    def implement_feature(self, requirements: str) -> dict:
        """Main agent implements the feature"""
        messages = [
            {"role": "user", "content": f"Implement: {requirements}"}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[read_file, write_file, list_directory]
        )
        return {
            "code": response.content,
            "files_changed": extract_files(response)
        }

class VerificationAgent:
    def verify_implementation(self, requirements: str, files_changed: list) -> dict:
        """Separate agent verifies the work"""
        messages = [
            {"role": "user", "content": f"""
Requirements: {requirements}

Files changed: {files_changed}

Run the test suite and verify:
1. All existing tests pass
2. New functionality works as specified
3. No obvious errors or security issues

You MUST run the complete test suite before marking as passed. Do not mark as passing after only running a few tests. Run: pytest --verbose
Only mark as PASSED if ALL tests pass with no failures.
"""}
        ]
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            messages=messages,
            tools=[run_tests, execute_code, read_file]
        )
        return {
            "passed": extract_pass_fail(response),
            "issues": extract_issues(response)
        }

def implement_with_verification(requirements: str, max_attempts: int = 3):
    for attempt in range(max_attempts):
        result = CodingAgent().implement_feature(requirements)
        verification = VerificationAgent().verify_implementation(
            requirements,
            result['files_changed']
        )
        if verification['passed']:
            return result
        requirements += f"\n\nPrevious attempt failed: {verification['issues']}"
    raise Exception(f"Failed verification after {max_attempts} attempts")
```

## 多智能体系统的应用（Multi-agent system applications）

Verification subagents are effective for:

验证子智能体适用于：

- Quality assurance. Running test suites, linting code, validating outputs against schemas.
- Compliance checking. Verifying documents meet policy requirements, checking outputs against rules.
- Output validation. Confirming generated content meets specifications before delivery.
- Factual verification. Having a separate agent verify claims or citations in generated content.

- 质量保障。运行测试套件、对代码做 lint 检查、按 schema 校验输出。
- 合规检查。核验文档是否满足政策要求、按规则检查输出。
- 输出校验。在交付前确认生成内容符合规范。
- 事实核查。由另一个智能体验证生成内容中的论断或引用。

## "提前宣告胜利"问题（The early victory problem）

The most significant failure mode for verification subagents is marking outputs as passing without thorough testing. The verifier runs one or two tests, observes them pass, and declares success.

验证子智能体最显著的失败模式是：未经过彻底测试就把输出标记为通过。验证者跑了一两个测试，看到它们通过，便宜宣告大功告成。

Mitigation strategies include:

缓解策略包括：

- Concrete criteria. Specify "Run the full test suite and report all failures" rather than "make sure it works."
- Comprehensive checks. Require the verifier to test multiple scenarios and edge cases.
- Negative tests. Direct the verifier to attempt inputs that should fail and confirm they do.
- Explicit instructions. The instruction "You MUST run the complete test suite before marking as passed" is essential. Without explicit requirements for comprehensive validation, verification agents take shortcuts.

- 具体的标准。明确规定"运行完整测试套件并报告所有失败"，而不是"确保它能用"。
- 全面的检查。要求验证者测试多种场景和边界情况。
- 负向测试。指示验证者尝试那些本应失败的输入，并确认它们确实失败。
- 明确的指令。"You MUST run the complete test suite before marking as passed"（在标记为通过之前必须运行完整测试套件）这条指令必不可少。如果没有对全面验证的明确要求，验证智能体会走捷径。

# 在单智能体与多智能体系统之间做选择（Choosing between single-agent and multi-agent systems）

Multi-agent systems are powerful, but not universally appropriate. Before adding the complexity of multiple coordinated agents, confirm that:

多智能体系统很强大，但并非放之四海而皆准。在引入多个协调智能体的复杂性之前，请确认：

- Genuine constraints exist that multi-agent solves, such as context limits, parallelization opportunities, or need for specialization.
- Decomposition follows context, not problem type. Group work by what context it requires, not by what kind of work it is.
- Clear verification points exist where subagents can validate work without requiring full context.

- 确实存在多智能体才能解决的约束，例如上下文限制、并行化机会或专门化需求。
- 分解遵循上下文而非问题类型。按工作需要什么上下文来分组，而不是按工作的类型。
- 存在清晰的验证点，让子智能体无需完整上下文即可验证工作。

Our advice? Start with the simplest approach that works, and add complexity only when evidence supports it.

我们的建议？从可行的最简单方案开始，只在有证据支持时才增加复杂性。

This is the first in a series of posts on multi-agent systems. For more on single-agent patterns, see Building effective agents. For context management strategies, see Effective context engineering for AI agents. For a deep dive into how we built our multi-agent research system, see How we built our multi-agent research system.

这是多智能体系列文章的第一篇。关于单智能体模式，请参阅 Building effective agents；关于上下文管理策略，请参阅 Effective context engineering for AI agents；想深入了解我们如何构建多智能体研究系统，请参阅 How we built our multi-agent research system。

# 致谢（Acknowledgements）

Written by Cara Phillips, with contributions from Paul Chen, Andy Schumeister, Brad Abrams, and Theo Chu.

本文由 Cara Phillips 撰写，Paul Chen、Andy Schumeister、Brad Abrams 和 Theo Chu 参与贡献。
