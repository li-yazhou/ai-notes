# CodeRabbit 如何用 Claude 构建一套 agent 编排系统（中英对照）

> **原文标题：** How CodeRabbit used Claude to build an agent orchestration system
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/how-coderabbit-used-claude-to-build-an-agent-orchestration-system
> **发布日期：** 2026-05-27
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

CodeRabbit built a layer on Claude that sits between a coding request and a coding agent, producing a structured coding plan the team can review before any code gets generated.

CodeRabbit 在 Claude 之上构建了一个位于编码请求与编码 agent 之间的层，在任何代码生成之前，先产出一份团队可以评审的结构化编码计划。

In our series, How startups build with Claude, we highlight how startups are transforming their industries with AI. In this article, we share how CodeRabbit built an agent orchestration layer that plans before AI generates code.

在我们的“How startups build with Claude”系列中，我们聚焦初创公司如何用 AI 变革各自的行业。本文分享 CodeRabbit 如何构建一个在 AI 生成代码之前先行规划的 agent 编排层。

**The quick pitch**

| Name | CodeRabbit |
| --- | --- |
| Founded | 2023 |
| Founders | Harjot Gill, CEO |
| Stack | Claude Platform, Claude Code |
| Scale | Reviews 2 million PRs per week across 15,000+ customers |

**快速一览**

| 名称 | CodeRabbit |
| --- | --- |
| 成立时间 | 2023 年 |
| 创始人 | Harjot Gill（CEO） |
| 技术栈 | Claude Platform、Claude Code |
| 规模 | 每周为 15,000+ 家客户评审 200 万个 PR |

AI coding tools have collapsed the time between idea and working prototype. CodeRabbit, an AI code review platform, has noticed a different trend climbing alongside that throughput: code that compiles and passes tests but doesn't do what the team actually meant to build.

AI 编码工具把从想法到可运行原型之间的时间压缩到极短。而 AI 代码评审平台 CodeRabbit 注意到，伴随这种吞吐量一起攀升的还有另一种趋势：代码能编译、能通过测试，却没做团队真正想做的事。

David Loker, VP of AI at CodeRabbit, locates the cause upstream of the model. Experienced developers often assume coding agents understand the same context they do, so they don’t write down requirements that feel obvious to them. The coding agent then fills the gaps with whatever it considers plausible.

CodeRabbit 的 AI 副总裁（VP of AI）David Loker 把原因定位在模型的上游。有经验的开发者常常假设编码 agent 拥有与自己相同的上下文，于是不把那些在自己看来不言自明的需求写下来。编码 agent 随即用自认为合理的东西填补这些空白。

To close that gap, CodeRabbit used Claude to design and build an agent orchestration system that runs a structured planning phase before any code is generated. The team's working thesis is that planning quality determines output quality, and the cheaper code generation gets, the more expensive it becomes to move in the wrong direction.

为了弥合这一差距，CodeRabbit 用 Claude 设计并构建了一套 agent 编排系统，在任何代码生成之前先运行一个结构化的规划阶段。团队的工作假设是：规划质量决定产出质量，而且代码生成越便宜，走错方向的代价就越高。

# 弥合 AI 编码中的内部知识差距（Addressing the internal knowledge gap in AI coding）

When the CodeRabbit team studied AI-generated pull requests across their customer base, the most frequent failure mode was code that compiled and passed tests, yet still didn't solve the problem it was built to solve.

当 CodeRabbit 团队研究客户群体中的 AI 生成 pull request 时，最常见的失败模式是：代码能编译、能通过测试，却仍然没有解决它要解决的问题。

"As we gain experience as developers, we internalize knowledge," Loker says. "All those things are in our head, and we assume other developers know them too. But then we make that assumption of the AI system as well, that it also implicitly understands. We're not even aware that we're assuming those things."

“随着经验的积累，开发者会把知识内化，”Loker 说。“所有这些东西都在我们脑子里，我们还以为其他开发者也知道。可接着我们又把同样的假设套到 AI 系统头上，以为它也隐式地理解。我们甚至意识不到自己正在做这些假设。”

Vague prompts force the underlying system to fill gaps with whatever it considers plausible. That guess often diverges from what the developer had in mind.

含糊的 prompt 迫使底层系统用自认为合理的内容填补空白。这种猜测常常偏离开发者的本意。

Loker offers a personal example. While building a memory system on a side project, he spent hours iterating with a coding agent until everything ran. When he asked the agent how to use it, the instructions told him to pass in a user token. There was no login page. He had specified that the system required users but never said users needed a way to sign in. The agent filled the gap, and hours of work landed in a product missing a front door.

Loker 举了一个亲身例子。在一个副业项目上构建记忆系统时，他与一个编码 agent 迭代了数小时，直到一切都能运行。可当他问 agent 该如何使用时，使用说明却让他传入一个用户 token。可根本没有登录页。他约定过系统需要用户，却从未说过用户需要一种登录方式。Agent 补上了这块空白，于是数小时的工作落成了一个没有正门的产品。

"What ends up happening is you build a lot more stuff on top of it, then much later you find there's a problem," Loker says. "In AI workflows, late validation can be very expensive."

“最终的情形是：你在它之上又堆了很多东西，很久之后才发现有问题，”Loker 说。“在 AI 工作流里，迟到的验证可能非常昂贵。”

# 运行在 AI 编码方案之前的编排层（An orchestration layer that runs before AI coding solutions）

CodeRabbit's response was to insert a planning system in front of code generation. It coordinates multiple Claude models to analyze requirements and surface assumptions before producing a structured execution plan that defines what should be built and what constraints it needs to satisfy.

CodeRabbit 的应对是在代码生成之前插入一个规划系统。它协调多个 Claude 模型来分析需求、把隐含假设暴露出来，然后产出一份结构化执行计划，定义应该构建什么、需要满足哪些约束。

"This planning system is not meant to replace Claude Code's Plan Mode," Loker says. "It's a higher level orchestration that happens before Claude Code, to point it in a really narrow and right direction where everything that needs to be explicit is made explicit, and we are aware of all assumptions that are being made."

“这个规划系统并不是要取代 Claude Code 的 Plan Mode，”Loker 说。“它是在 Claude Code 之前发生的更高一层编排，把 Claude Code 指向一个足够窄且正确的方向：所有需要显式说明的东西都被显式化，我们对正在做出的所有假设也都心中有数。”

The output is a collaborative product requirements document (PRD): a plan created with full context, validated by stakeholders across the team, and reviewed before implementation starts. Claude Code picks up that plan and uses it to generate a fine-grained implementation plan. The plan becomes a shared artifact that captures what was decided and why, which not only helps teams avoid rework and validate later that the output matched the original intent, but also onboard new engineers.

输出是一份协作式的产品需求文档（PRD）：一份带着完整上下文创建、由团队各相关方验证、并在实现开始前经过评审的计划。Claude Code 接过这份计划，用它生成一份细粒度的实现计划。这份计划成为一个共享产物，记录了决定了什么以及为什么，这不仅帮助团队避免返工、事后验证产出是否契合最初意图，还能帮助新工程师上手。

# 在 Claude 模型家族中做路由（Routing across the Claude model family）

CodeRabbit matches each model tier to task complexity to optimize for cost and latency. Opus drives the orchestration loop and the higher-level strategic work of understanding the problem and setting overall direction. Sonnet takes that output and sequences it into structured planning steps. Haiku handles narrowly scoped operations like context distillation and targeted tool use, where the question is specific enough that a smaller model can answer it well.

CodeRabbit 把不同模型档位与任务复杂度相匹配，以优化成本与延迟。Opus 驱动编排循环，以及理解问题、设定总体方向这类更高层的战略工作。Sonnet 接过这些输出，将其编排成结构化的规划步骤。Haiku 处理范围很窄的操作，例如上下文蒸馏（context distillation）与定向工具使用--这些问题足够具体，较小的模型也能给出好答案。

"If Haiku does as well as Sonnet on a given task, we use Haiku," Loker says. "If the evaluation harness tells us the plan quality improves when we give Opus more room, we give it more room. We don't guess."

“如果某项任务上 Haiku 做得和 Sonnet 一样好，我们就用 Haiku，”Loker 说。“如果评估 harness 告诉我们，给 Opus 更多发挥空间能提升计划质量，我们就给它更多空间。我们不靠猜。”

# 为计划质量构建 eval harness（Building an eval harness for plan quality）

CodeRabbit had a mature evaluation system for code review, but nothing for evaluating planning output. Building that infrastructure became its own project.

CodeRabbit 有一套成熟的代码评审评估系统，却没有用于评估规划产出的系统。构建这套基础设施本身就成了一个项目。

The system started with hand-tuned examples and manual inspection. The team developed a library of LLM judges that scored specific dimensions of plan quality. Because plans eventually produce code, the team could also measure whether the generated code worked, whether it contained extra scope, and how many tokens it took to get there. Running the same task with and without the planning step gave them a way to isolate the value of planning itself.

这套系统从手工调校的示例和人工检查起步。团队开发了一个 LLM 裁判（LLM judge）库，为计划质量的特定维度打分。由于计划最终会产生代码，团队还能度量生成的代码能否工作、是否夹带了额外范围、以及为此消耗了多少 token。对同一任务分别在有规划步骤和无规划步骤两种情况下运行，让他们得以单独度量规划本身的价值。

"We didn't realize what the right level of detail was going to be for that plan," Loker says. Plans that were too granular went stale the moment the codebase shifted. Plans that were too high-level left room for the agent to fill in assumptions, which was the original problem the planning layer was meant to solve. Finding the working level of abstraction took iteration, which is what the eval harness made possible.

“我们一开始并不知道那份计划的合适详细程度会是多少，”Loker 说。过细的计划在代码库一变动的那一刻就过时了；太宏观的计划又给 agent 留下了填入假设的空间--那正是规划层本来要解决的问题。找到可行的抽象级别靠的是迭代，而这正是 eval harness 使之成为可能的。

# 在写下任何代码之前拦截错误（Catching errors before any code gets written）

In an AI-native coding workflow, many of the decisions that used to surface during code review are now made earlier, in the planning layer. Building a plan that the team can review and align on before code generation starts catches mistakes early.

在 AI 原生编码工作流中，许多过去在代码评审时才浮现的决策，如今被提前到规划层做出。在代码生成开始之前构建一份团队可以评审并对齐的计划，能尽早抓住错误。

"What we've built, using the Claude ecosystem, is a team-wide planning system," Loker says. "The plan itself becomes a quality gate. If we can make sure the quality of that plan is really good upfront, the downstream effect is very pronounced. You end up with a lot better code at the end of it."

“我们用 Claude 生态构建的，是一套覆盖全团队的规划系统，”Loker 说。“计划本身就成了一道质量闸门。如果我们能确保这份计划一开始就质量过硬，下游的效应会非常显著。最终你会得到好得多的代码。”

**Best practices from the CodeRabbit team**

| What outcome are you actually trying to create, and how do you measure? | Be explicit not just in specifications to the AI but also define what you want in the MPP (maximum possible product). |
| --- | --- |
| What assumptions are still implicit? | Ask Claude: what is missing? Are there any parts of the plan that are coming out as implicit assumptions instead of explicit specifications? |
| What workflows or edge cases are easy to forget? | Ask Claude to help identify places or cases that you may not have taken into account. |
| How will you know the output matches intent before rollout? | Create a record of work: a chronicle of planning artifacts that is saved and reused. |

**CodeRabbit 团队的最佳实践**

| 你真正想创造的结果是什么，你如何度量？ | 不仅对 AI 的规格说明要显式，还要定义你在 MPP（maximum possible product，最大可能产品）中想要什么。 |
| --- | --- |
| 哪些假设仍然是隐式的？ | 问 Claude：缺了什么？计划里有没有哪些部分是以隐式假设而非显式规格的形式出现的？ |
| 哪些工作流或边界情况容易遗忘？ | 请 Claude 帮你找出你可能没有考虑到的位置或情形。 |
| 上线之前，你如何知道产出符合意图？ | 建立工作记录：一份被保存和复用的规划产物编年史。 |

Build your startup on the Claude Platform.

在 Claude Platform 上构建你的初创公司。
