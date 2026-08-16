# 运营一个 AI 原生的工程组织（中英对照）

> **原文标题：** Running an AI-native engineering org
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/running-an-ai-native-engineering-org
> **发布日期：** 2026-06-03
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

How the Claude Code engineering team's processes and structure changed once agentic coding became the default way of working.

当智能体编码成为默认工作方式后，Claude Code 工程团队的流程与结构发生了怎样的变化。

At Code w/ Claude SF 2026, Director of Engineering for Claude Code and Claude Cowork Fiona Fung walked through how the team's processes and structure changed once agentic coding became the default way of working.

在 Code w/ Claude SF 2026 大会上，Claude Code 与 Claude Cowork 工程总监 Fiona Fung 讲解了当智能体编码（agentic coding）成为默认工作方式后，团队的流程与结构发生了哪些变化。

For years, engineering bandwidth was the expensive part of building applications. Every process we used to have around software planning and shipping, first waterfall and then agile, was built around that cost.

多年来，工程带宽（engineering bandwidth）一直是构建应用中最昂贵的部分。我们过去围绕软件规划和交付建立的每一个流程--先是瀑布式（waterfall），后来是敏捷（agile）--都是围绕这一成本设计的。

I started my career in the early 2000s working on Visual Studio. In those days we shipped software on CD-ROMs with hard manufacturing deadlines. Once we could distribute software online, we began increasing to shipping updates continuously. Now we're changing the way we work again, this time around the time and people it takes to write software.

我在 2000 年代初入行，从事 Visual Studio 的开发。那时我们用 CD-ROM 交付软件，有刚性的制造截止日期。当软件可以在线分发后，我们开始不断提高发布更新的频率，走向持续交付。现在，我们又一次在改变工作方式，这次围绕的是编写软件所需的时间和人力。

On the Claude Code team, writing code, writing tests, and refactoring rarely slows us down anymore. But the bottlenecks didn't go away when agentic coding took away the actual need to type code. Verification, code review, and security took their place.

在 Claude Code 团队，写代码、写测试和重构已经很少拖慢我们的进度。但当智能体编码免去了亲手敲代码的需要时，瓶颈并没有消失。验证（verification）、代码审查（code review）和安全（security）取而代之。

We can all generate a lot of code really fast now, but this also brings up new questions: Is this code correct? How is it maintained? And one of the top questions I get from fellow engineering leaders: "How are humans keeping up with how you're doing code reviews?"

如今我们都能飞快地生成大量代码，但这也带来了新问题：这段代码正确吗？它如何维护？工程负责人同行们问得最多的一个问题就是："人类怎么跟得上你们的代码审查？"

# 悄然失效的流程（The processes that quietly stopped working）

We all put processes in place for a reason, to close a gap or make something work better. But when that gap no longer exists and those processes become obsolete, they rarely go away on their own. When the Claude Code team began using agentic coding as our default way of working, a lot of our existing processes stopped working. Here are the norms we rewrote, and why.

我们设立每个流程都有原因--填补某个缺口，或让某件事运转得更好。但当缺口不复存在、流程变得过时时，它们很少会自行消失。当 Claude Code 团队开始把智能体编码作为默认工作方式时，许多既有流程失效了。以下是我们重写的规范，以及原因。

## 规划：把路线图转为即时制（Planning: shift roadmaps to just in time）

The old norm was to spend a lot more time pre-planning because coding time was expensive. When I first joined the Claude Code team, we wrote a pretty good six month roadmap, and then because of Claude Code, so many things changed that it was out of date by month three.

过去的惯例是在预规划上投入多得多的时间，因为编码时间很昂贵。我刚加入 Claude Code 团队时，我们写了一份相当不错的六个月路线图，但受 Claude Code 的影响，变化太多，到第三个月它就过时了。

Engineering speed and throughput is different now, so the way we plan sprints has changed. I call it just-in-time (JIT) planning, almost like JIT compiling: how do you do just the right amount at the right time? Our planning ritual shifted away from design docs toward discussions in PRs or prototypes. The space moves fast so we don't do a lot of product reviews. Our process now is let's prototype, get a lot of internal users on it, and start acting on their feedback.

如今的工程速度和吞吐量都不一样了，所以我们规划迭代（sprint）的方式也变了。我称之为即时（just-in-time，JIT）规划，很像 JIT 编译：怎样在恰当的时机只做恰当的量？我们的规划仪式从设计文档转向了在 PR 或原型中讨论。这个领域变化太快，所以我们不做很多产品评审。我们现在的流程是：先做原型，让大量内部用户用起来，然后开始根据他们的反馈行动。

## 收集上下文：问 Claude，而不是问作者（Context gathering: ask Claude, not the author）

When engineers wrote code, the first step to getting an answer to most questions was to find the person who wrote the code. Now, since all our PRs are assisted by Claude, "Who made this change?" is no longer sufficient. Our new norm is to go a level deeper: what do you actually need to know? For instance: Are you looking for who caused a regression? An expert to answer a customer question? Or context on a decision? You ask Claude that question, and consider whether Claude can answer it directly, also with more data and context.

在工程师亲手写代码的年代，大多数问题的求解第一步是找到写代码的人。而现在，由于我们所有的 PR 都有 Claude 参与，"这是谁改的？"已经不够了。我们的新规范是再往深一层：你到底需要知道什么？比如：你在找引入回归（regression）的人？找能回答客户问题的专家？还是某项决策的背景？你把这个问题问给 Claude，并考虑 Claude 能否直接回答--它还掌握着更多的数据和上下文。

On the Claude Code team, no matter what that question is, our process is to also ask "Is there a way to automate it?" For example, having Claude summarize customer feedback channels every morning went from a ritual I did manually with my coffee to something I just have running automatically in the background.

在 Claude Code 团队，无论问题是什么，我们的流程都会再追问一句："这件事能不能自动化？"比如，让 Claude 每天早晨汇总客户反馈渠道，这从我喝着咖啡手动完成的例行公事，变成了在后台自动运行的事。

## 代码审查：信任但验证（Code review: trust but verify）

We use Code Review heavily. Claude handles all the style and linting, PR feedback requests, catching bugs and fixing them before a full commit, and adding tests. Where we still definitely want a human is expertise.

我们大量使用 Code Review。Claude 负责所有风格和 lint 检查、PR 反馈请求、在完整提交前发现并修复 bug，以及补充测试。我们仍然绝对需要人类介入的地方，是专业判断。

The new norm is human review where it matters: for legal review, I always want my legal partner involved in risk tolerance. For trust boundaries and security-sensitive code, I want the domain experts. Product managers and designers also need to be involved with product sense and taste.

新规范是让人类在关键处评审：法务评审上，我始终希望我的法务搭档参与风险容忍度的判断；涉及信任边界（trust boundary）和安全敏感代码，我要领域专家把关；产品经理和设计师也需要参与进来，贡献产品直觉和品味。

It's important to continually evaluate, though, because the right balance of trust vs. verify will keep changing as the models improve. What you need humans for today might look different with the next model.

不过，持续评估很重要，因为"信任 vs. 验证"的恰当平衡会随模型进步而不断变化。今天需要人类做的事，到了下一个模型可能就不同了。

## 团队构成：模糊的角色边界（Team makeup: blurring roles）

Claude and AI have reshaped roles across the team. Our PMs code a lot now, which is fun to see. With Claude, you have nontraditional coders now being able to do more engineering, and you have engineers who take on things like content and design, work that were traditionally not on the technical side.

Claude 和 AI 重塑了团队中的各种角色。我们的产品经理现在写很多代码，这很让人开心。有了 Claude，非传统意义上的编码者可以做更多工程工作，而工程师也开始承担内容和设计这类传统上不属于技术侧的工作。

On the Claude Code engineering team, I've indexed heavily on two profiles. One is creative builders with product sense: the dreamers who are deeply curious and passionate about shipping products that solve problems. The other one is engineers with deep systems expertise. For example, when I joined the team, I noticed we were missing experts with systems backgrounds and we needed that when building Claude Code on the Web, to ensure we can run Claude everywhere.

在 Claude Code 工程团队，我特别看重两类人。一类是有产品直觉的创造性构建者：那些深度好奇、热衷于交付能解决实际问题的产品的梦想家。另一类是具备深厚系统专业知识的工程师。比如我刚加入团队时，发现我们缺少有系统背景的专家，而在构建 Claude Code on the Web 时我们正需要这样的人才，以确保 Claude 能在任何地方运行。

What I index on less, on the other hand, is raw throughput; the models handle that. The more important question is where you still need human expertise, and that's where I'd focus.

另一方面，我较少看重原始吞吐量；模型会处理这些。更重要的问题是：哪里仍然需要人类的专业判断--那才是我会聚焦的地方。

| | Before | After |
|---|---|---|
| **Planning** | Six-month product roadmaps. | Just-in-time (JIT) planning: prototype, put internal users on it, and act on their feedback. |
| **Context gathering** | Find the person who wrote the code and ask them. | Ask Claude first. Then ask whether what you are asking about can be automated. |
| **Code review** | Humans review everything. | Claude handles style, bugs, and tests. Humans review where domain expertise is important. |
| **Team makeup** | Fixed roles: engineers write code, PMs plan, designers design. | Roles blur: PMs prototype, engineers take on design and context. Hire for creative builders and deep systems expertise. |

| | 之前 | 之后 |
|---|---|---|
| **规划** | 六个月的产品路线图。 | 即时（JIT）规划：做原型，让内部用户用起来，并根据反馈行动。 |
| **收集上下文** | 找到写代码的人当面问。 | 先问 Claude。再追问这件事能否自动化。 |
| **代码审查** | 人类审查一切。 | Claude 处理风格、bug 和测试。人类在领域专业知识重要的地方审查。 |
| **团队构成** | 固定角色：工程师写代码，PM 做规划，设计师做设计。 | 角色模糊：PM 做原型，工程师承担设计和上下文工作。招聘创造性构建者和深厚系统专长的人才。 |

# 我们如何推行新规范（How we rolled out our new norms）

As these norms changed, some aspects were mandated as team principles and others we let small sub-teams (pods) figure out on their own. There is a set of the Claude Code core team principles that are non-negotiable "must dos":

随着这些规范的变化，有些内容被确立为必须遵守的团队原则，另一些则放手让小型子团队（pod）自行摸索。Claude Code 核心团队有一系列没有商量余地的"必做事项"：

- Relentlessly dogfood your product: Every Claude Code team member, including cross-functional partners, uses Claude Code (and also Claude Cowork). We're always thinking of ways to get Claude to help us do our work faster, and more efficiently.
- Keep the team flat as possible. When I joined Claude Code I wanted every manager to start out as an IC first, learn how to be an effective engineer on the team by shipping, and really live through and understand what it's like to be an engineer at Anthropic. We have one overall team mission on Claude Code and Claude Cowork. Managers support pods of work while keeping the team agile so people can move to where the work is.
- Don't hesitate to kill processes that no longer work: Finally, we relentlessly question why we do things the way we do. When something doesn't make sense anymore, team members have explicit permission to question and kill old processes.

- 不遗余力地吃自家狗粮（dogfood）：每位 Claude Code 团队成员，包括跨职能伙伴，都在使用 Claude Code（以及 Claude Cowork）。我们总在思考怎样让 Claude 帮我们更快、更高效地完成工作。
- 让团队尽可能扁平。我加入 Claude Code 时，希望每位经理都先从 IC（individual contributor，个人贡献者）做起，通过实际交付学会如何成为团队中高效的工程师，真正亲历并理解在 Anthropic 做工程师是什么感受。Claude Code 和 Claude Cowork 只有一个共同的团队使命。经理们支撑各个工作 pod，同时保持团队敏捷，让人能流动到工作所在的地方。
- 毫不犹豫地砍掉不再有效的流程：最后，我们会不断追问为什么事情要这样做。当某件事不再合理时，团队成员有明确的授权去质疑并终结旧流程。

Within these few rules, though, each pod has a lot of agency. They have room to adapt how they use Claude to do triage, how they run any planning rituals or standups, and which workflows get "Claudified" first.

不过，在这几条规则之内，每个 pod 都有很大的自主权。他们可以自行调整如何用 Claude 做分诊（triage）、如何运作各自的规划仪式或站会，以及优先把哪些工作流"Claude 化（Claudified）"。

# 如何判断新流程是否扎下了根（How to know your new processes are sticking）

Here are three numbers every engineering leader should start tracking now as they roll out changes.

以下是每位工程负责人在推行变革时都应立即开始跟踪的三个数字。

- Onboarding ramp time goes down: How soon can an engineer, a designer, or a PM start being effective? On our team this is much faster than a year ago, and engineers ship real code now within their first week.
- PR cycle time goes down: This one's interesting to dig into because it might help you identify where your pipeline is struggling to scale. As we're generating so much more code, sometimes build systems and continuous integration (CI) may struggle to keep up.
- Claude-assisted commits going up: For us, by default, every commit is Claude-assisted. I don't think I've seen a non-Claude-assisted commit in the last four months.

- 新人爬坡（onboarding ramp）时间下降：一位工程师、设计师或 PM 多快能开始产出？在我们团队，这比一年前快得多，工程师现在入职第一周就能交付真实代码。
- PR 周期时间下降：这个指标值得深挖，因为它可能帮你发现流水线在哪里难以扩展。随着我们生成的代码量大增，构建系统和持续集成（CI）有时会跟不上。
- Claude 辅助的提交占比上升：对我们来说，默认情况下每次提交都有 Claude 参与。过去四个月里，我想我没见过一次没有 Claude 辅助的提交。

On the third bullet, don't confuse throughput with success. Throughput is one metric, but the real metric is measuring the thing you're trying to solve. With the right alignment, throughput can help you solve problems faster.

关于第三条，不要把吞吐量等同于成功。吞吐量是一个指标，但真正的指标是衡量你试图解决的那个问题本身。只要方向对齐，吞吐量能帮你更快地解决问题。

# 开始行动（Getting started）

If I were to leave you with one thing: pick your noisiest workflow. That could be your most expensive workflow, the one you might be dreading, or that your team doesn't look forward to. And ask: is it still serving its purpose? If so, can you automate it?

如果只让你记住一件事，那就是：挑出你最"吵"的那个工作流。它可能是你最昂贵的工作流、你最发怵的那个，或者你的团队最不想碰的那个。然后问：它还在实现它的目的吗？如果在，能把它自动化吗？

I was once on a team that had an expensive weekly review, with a large number of people in a meeting room. I noticed everybody was on their laptops except when it was their time to give a status report. They would pop their head up, say the status, and go back down to their laptops. I asked one simple question: "Why are we having this meeting again? It seems like an expensive use of our time." And just that one question made everyone realize it wasn't needed. So we canceled it.

我曾经在一个团队里，那里有个成本高昂的周会评审，一大群人坐在会议室里。我注意到，除了轮到自己汇报状态的时候，所有人都盯着自己的笔记本电脑。他们抬起头说完状态，又低头回到电脑上。我问了一个简单的问题："我们为什么还要开这个会？这好像很浪费大家的时间。"就这一个问题，让所有人都意识到它并无必要。于是我们把它取消了。

So, ask yourself: what's one piece of your engineering workflow that you might consider automating or even dropping altogether?

所以，问问自己：你的工程工作流中，有哪一件事是你可能考虑自动化、甚至干脆放弃的？
