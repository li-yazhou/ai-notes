# Agentic 时代的产品开发（中英对照）

> **原文标题：** Product development in the agentic era
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/product-development-in-the-agentic-era
> **发布日期：** 2026-04-29
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Jess Yan, Claude Managed Agents product manager, shares how she uses the product to unblock herself and free up time to hone her craft.

Claude Managed Agents 产品经理 Jess Yan 分享她如何使用这款产品为自己扫清障碍、腾出时间来打磨自己的技艺。

One of the ironies of being a product manager in the age of AI is that my work feels more human than ever.

在 AI 时代做产品经理的讽刺之处之一在于：我的工作感觉比以往任何时候都更有人情味。

The job of product management has always been a mix of craft and alignment. For most of my career, my week was occupied by the latter: meetings with cross-functional stakeholders and teammates, status reports, and ticket backlogs with my engineering team. I got used to making instinctive, quick decisions followed by uphill battles advocating, convincing, and resourcing; shipping impactful products often felt more transactional than generative.

产品管理这份工作向来是技艺（craft）与对齐（alignment）的混合体。在我职业生涯的大部分时间里，我的每一周都被后者占据：与跨职能利益相关者和队友开会、写状态报告、处理与工程团队之间的工单积压（ticket backlog）。我习惯了凭直觉快速决策，随后再经历游说、说服、争取资源的艰苦拉锯；发布有影响力的产品常常让人感觉更像交易式（transactional）而非生成式（generative）的工作。

With Claude, I can pressure test ideas, automate workflows, and get unstuck. I'm finally spending real time with our users and my team on the part of the job that always mattered most: the craft. While these new workflows changed my day-to-day, the most meaningful shifts happened when we started developing Claude Managed Agents (currently in beta), a suite of composable APIs for building and deploying cloud-hosted agents at scale.

有了 Claude，我可以对想法做压力测试、自动化各种工作流程，并摆脱卡壳的状态。我终于能把实实在在的时间花在我们的用户和我的团队身上，投入到这份工作中始终最重要的那部分：技艺本身。这些新工作流改变了我的日常，而最有意义的转变发生在我们开始开发 Claude Managed Agents（目前处于 beta 阶段）的时候--这是一套用于大规模构建和部署云端托管智能体（cloud-hosted agents）的可组合 API。

In this post, I'll share how Managed Agents has changed the way I work as a product manager, and a few patterns you can borrow for your own workflows.

在这篇文章中，我将分享 Managed Agents 如何改变了我作为产品经理的工作方式，以及几个你可以借鉴到自己工作流中的模式。

# 产品开发的今与昔（Product development, then and now）

API design used to live in documents and comment threads; on the AI exponential, we build with what we ship. A spec that reads elegantly in a doc can fall apart the first time you try to build against it. With Claude Code, I can sketch out an agent against pre-production versions of our API specs, and within an afternoon be running a real prototype end-to-end.

API 设计过去存在于文档和评论串里；而在 AI 指数级发展的当下，我们用自己发布的东西来构建。一份在文档里读起来优雅的规格说明（spec），第一次尝试照着它构建时可能就四分五裂。借助 Claude Code，我可以基于预发布（pre-production）版本的 API 规格勾勒出一个 agent，并在一个下午之内端到端地跑通一个真实的原型。

We reshaped API abstractions and Claude Console UX several times based on what we learned building with our own primitives–changes that even a multi-week doc review would never have surfaced, and otherwise would've come up too late via user feedback. We still litigate shapes and run raw curl requests to make sure we're happy with the bare-metal experience, but Claude Code gets me from the basic "hello world" test to a functional agent in the same sitting. As I build these agents, I'm able to more concretely anticipate ways our harness and API can flex for the next wave of model and task evolution.

我们曾根据用自家原语（primitives）构建时的体会，多次重塑 API 抽象和 Claude Console 的用户体验--这些改动即使是一场持续数周的文档评审也永远无法暴露出来，而若依靠用户反馈，发现时又为时已晚。我们仍然会反复推敲接口形态（shapes）、直接运行原始的 curl 请求，以确保我们对"裸机"（bare-metal）体验足够满意，但 Claude Code 能让我在同一次工作时段里从基本的 "hello world" 测试一路走到一个可用的 agent。在构建这些 agent 的过程中，我能够更具体地预判我们的 harness（agent 运行框架）和 API 该如何灵活应变，以迎接下一波模型与任务的演进。

Initially, these prototypes were just for shaping the product, but they now are evolving my day-to-day work as well. My workflow as a PM now splits cleanly across our products. I use Claude and Claude Cowork for open-ended research and discovery–the murky, early-stage exploration where I want an ongoing conversation. Once I have greater clarity on the job to be done, I use Claude Code to write and ship a custom agent for it, built atop of Managed Agents.

起初，这些原型只是为了塑造产品，但如今它们也在改变我的日常工作。作为产品经理，我的工作流现在清晰地分布在我们各个产品之间。我用 Claude 和 Claude Cowork 来做开放式的研究与发现--即那些混沌不清的早期摸索，这时我希望有一段可以持续进行的对话。而一旦对要完成的任务（job to be done）有了更清晰的认识，我就用 Claude Code 为其编写并上线一个定制 agent，构建在 Managed Agents 之上。

The two-pronged payoff has been the biggest unlock. On one side, being able to build against my own product easily raises the ceiling on what I can imagine shipping next. On the other, once the product is live, the same development muscle lets me automate the long tail of operational work that used to stall in my backlog.

这种双重的回报是最大的一种解锁。一方面，能够轻松地基于自己的产品进行构建，抬升了我对下一步可以发布什么的想象上限；另一方面，产品上线后，同样的开发能力让我得以自动化那些过去一直积压在待办事项中、迟迟无法推进的长尾运营工作。

# 面向产品经理的 Managed Agents 用例（Managed Agents use cases for product managers）

Now I spin up bespoke agents for any "job to be done." Building one is simple: I load the Managed Agents skill in Claude Code and outline a quick sketch of what I'm looking for. Developers can also use the latest version of Claude Code and built-in claude-api skill to build with Managed Agents–just prompt Claude with "start onboarding for managed agents in Claude API" to get started. After invoking this skill, Claude builds the agent, explaining its integration steps along the way, so I can easily shift direction as needed.

现在，我会为任何"待完成的任务"（job to be done）快速搭建定制 agent。构建过程很简单：我在 Claude Code 中加载 Managed Agents skill，并勾勒一份我想要的简短草案。开发者也可以使用最新版本的 Claude Code 和内置的 `claude-api` skill 来基于 Managed Agents 进行构建--只需向 Claude 发送提示词 "start onboarding for managed agents in Claude API" 即可开始。调用这个 skill 之后，Claude 会构建 agent，并一路解释各个集成步骤，这样我在需要时可以轻松调整方向。

Examples of these agents include:

这些 agent 的例子包括：

- Adoption analytics. An agent with persistent access to our internal databases and skills for understanding our data schemas runs queries to surface interesting outliers and patterns. With memory of prior runs, it can build on prior findings and continuously advance its perspective.
- Developer sentiment monitoring. An agent with the pre-built web search tool and guidance on focus areas scans a specific list of domains for the latest developer feedback, reporting back on common themes. Since there is so much content to analyze, it fans out research to multiple agents in parallel, waits for results, and synthesizes findings.
- Demo building. An agent with access to demo GitHub repos, branding assets, and an event deck turns prebuilt templates into a polished demo tailored to the relevant audience, such as a conference or customer meeting.

- 使用情况分析（Adoption analytics）。一个对内部数据库拥有持久访问权限、并具备理解数据模式（data schema）的 skills 的 agent，会运行查询以发现有趣的异常值和规律。凭借对以往运行的记忆，它可以在先前发现的基础上继续推进，不断深化自己的视角。
- 开发者情绪监测（Developer sentiment monitoring）。一个配备预置 web search 工具和重点领域指引的 agent，会扫描一份特定的域名列表以获取最新的开发者反馈，并汇报其中的共性主题。由于需要分析的内容非常多，它会把研究工作分派（fan out）给多个 agent 并行执行，等待结果，然后综合出结论。
- 演示构建（Demo building）。一个可以访问演示用 GitHub 仓库、品牌素材和活动演示文稿（event deck）的 agent，能把预置模板打磨成面向相应受众（比如一场技术大会或一次客户会议）的精美演示。

Managed Agents sessions run in the cloud, so I can walk away and come back to find the work done. Processes that could never scale because every launch has its own quirks are now easy to automate using Managed Agents, and every agent run feels energizing instead of tedious.

Managed Agents 会话在云端运行，所以我可以离开一会儿，回来时发现工作已经完成。那些因为每次发布都各有其特殊性而永远无法规模化的流程，现在用 Managed Agents 都很容易实现自动化，而且每一次 agent 运行都让人干劲十足，而不是索然无味。

# 腾出空间打磨技艺（Freeing up space to hone my craft）

A year ago, all of this kind of work would've crawled along in cross-functional staffing requests, chaotic spreadsheets, or half-baked concepts I just never got to try out. Now, with Claude and Managed Agents, I can scale myself, using my time to partner with my team on developing the most impactful products. My day now spans generating innovative ideas with customers, digging into murky and ambiguous problems with my engineering counterparts, and investing real creative energy in frontier product work.

一年前，所有这类工作都会在跨职能的人力申请、乱糟糟的电子表格，或者我始终没机会尝试的半成品构想中缓慢爬行。而现在，有了 Claude 和 Managed Agents，我可以放大自己的效能，把时间用来与团队一起开发最有影响力的产品。我如今的一天涵盖：与客户一起产生创新想法、与工程侧的伙伴一起钻研混沌而模糊的问题，并把真正的创造性精力投入到前沿产品工作中。

If you're a product manager and you haven't built an agent yet, that's where I'd start this week. The experiments and tools you've always wished existed are a single prompt and a few API calls away.

如果你是一名产品经理却还没有构建过 agent，这就是我建议你本周着手去做的事。那些你一直希望存在的实验和工具，距离你只有一个提示词和几次 API 调用之遥。

Learn more in our docs.

欢迎在我们的文档中了解更多。
