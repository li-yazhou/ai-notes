# 在前沿工作：Thomson Reuters 如何为高风险专业工作构建 AI（中英对照）

> **原文标题：** Working at the frontier: How Thomson Reuters builds AI for high-stakes professional work
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/working-at-the-frontier-how-thomson-reuters-builds-ai-for-high--stakes-professional-work
> **发布日期：** 2026-07-08
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Why the team at Thomson Reuters considers Claude Fable 5 a critical evolution in what’s possible with AI for knowledge work.

为什么 Thomson Reuters 团队认为 Claude Fable 5 是 AI 在知识工作能力上的一次关键演进。

Joel Hron, CTO at Thomson Reuters, has spent years putting AI inside products trusted by lawyers and accountants. Here is why he considers Claude Fable 5 a critical evolution in what’s possible with AI for knowledge work.

Thomson Reuters 首席技术官（CTO）Joel Hron 多年来一直致力于把 AI 嵌入律师和会计师所信赖的产品。以下是他认为 Claude Fable 5 是 AI 知识工作能力关键演进的原因。

Thomson Reuters, a global content and technology company, has spent more than 175 years building trusted content and technology for professionals and institutions making consequential decisions. Today, that same mission is shaping how the company builds AI for legal, tax, accounting, compliance, and other high-stakes professional workflows.

Thomson Reuters 是一家全球性的内容与技术公司，175 年多来一直在为做出重大决策的专业人士和机构构建值得信赖的内容与技术。今天，同样的使命正在塑造这家公司为法律、税务、会计、合规及其他高风险专业工作流构建 AI 的方式。

"We're a technology company focused on professions that demand accuracy and precision," says Joel Hron, CTO of Thomson Reuters.

“我们是一家技术公司，专注于那些对准确性与精确性有苛刻要求的行业，”Thomson Reuters CTO Joel Hron 说。

Its products are the reference tools those professions run on: Westlaw and Practical Law for legal research and practical guidance, CoCounsel Legal, Thomson Reuters professional-grade legal AI platform, is designed to make legal professionals better at their jobs, with answers they can defend and outcomes that provide real value. Hron joined Thomson Reuters four years ago when his startup was acquired by the company, working at the intersection of product, technology, and strategy. In that time period, he says, AI has reshaped what it means to build software. Choosing the right technology partners has never been more important.

它的产品是这些行业赖以运转的参考工具：用于法律研究与实务指引的 Westlaw 与 Practical Law；CoCounsel Legal--Thomson Reuters 的专业级法律 AI 平台--旨在让法律专业人士更出色地完成工作，给出他们能够为之辩护的答案与创造真实价值的结果。Hron 四年前加入 Thomson Reuters，当时他的初创公司被收购，他一直工作在产品、技术与战略的交汇处。他说，在这段时间里，AI 重新定义了“构建软件”的含义。选择合适的技术伙伴，从未像现在这样重要。

The bar for selecting which LLMs to use to power these products is unusually concrete. Hron and his team evaluate a new model by asking whether its work can withstand the level of professional review lawyers apply before relying on it in their work.

为这些产品选择底层 LLM 的标准异常具体。Hron 和团队评估一个新模型的方式，是问：它的工作成果能否经受住律师在工作中依赖它之前所施加的那种专业级评审。

## 为法律工作评估模型（Evaluating models for legal work）

Plenty of companies can build a legal AI tool, but far fewer can build one a lawyer would put their name on. Thomson Reuters brings three advantages to professional AI that general-purpose systems cannot easily replicate: authoritative content, deep domain expertise, and workflow integration.

很多公司都能做出一个法律 AI 工具，但能做出让律师愿意署名背书的则少得多。Thomson Reuters 为专业 AI 带来了三样通用系统难以复制的优势：权威内容、深厚的领域专业知识，以及工作流集成。

The reason a lawyer can rely on a Westlaw answer is not the model on its own, says Hron. It is decades of curated case law, the work of 2,700+ domain experts across the globe who annotate and enhance that content every day, and the evaluations Thomson Reuters builds on top of models like Claude. "That human professional is still the one who is accountable for the end work product."

Hron 说，律师之所以能信赖一条 Westlaw 答案，原因不在模型本身，而在数十年精心策展的判例法、全球 2700 余名每天对内容进行标注与增强的领域专家，以及 Thomson Reuters 在 Claude 这类模型之上构建的评估体系。“最终对工作成果负责的，仍然是那位人类专业人士。”

Claude is a valuable model partner, but the professional-grade system comes from the combination of Anthropic's frontier models with Thomson Reuters' authoritative content, deep domain expertise, workflow integration, and evaluation infrastructure.

Claude 是宝贵的模型伙伴，但专业级系统来自 Anthropic 前沿模型与 Thomson Reuters 的权威内容、深厚领域专业知识、工作流集成和评估基础设施的结合。

Thomson Reuters describes this approach as Fiduciary-Grade AI™: AI grounded in authoritative content, shaped by deep domain expertise, and embedded directly into professional workflows, so outputs are transparent, verifiable, and defensible when the stakes are high.

Thomson Reuters 把这套方法称为 Fiduciary-Grade AI™（受托级 AI）：以权威内容为根基、由深厚领域专业知识塑造、并直接嵌入专业工作流的 AI，因此在高风险场景下，其输出是透明、可验证、可辩护的。

That accountability is why verification matters more here than fluency. Thomson Reuters rebuilt legal research around agents tuned for "not just search and not just retrieval, but citation validation and verification." The requirement is a system that helps validate citations and surface sources clearly, so professionals can review, verify, and apply their judgment with confidence.

正是这种问责性，让验证在这里比流利更重要。Thomson Reuters 围绕为“不仅是搜索、也不仅是检索，而是引用验证与核查”而调优的 agent 重建了法律研究。其要求是一个能帮助验证引用、清晰呈现来源的系统，让专业人士能够带着信心去评审、核实并运用自己的判断。

The change shows up in what customers report. Research that "would take dozens of hours," Hron says, now arrives "in a matter of minutes," giving professionals a high-quality starting point they can evaluate, refine, and act on. "Deep research has been a profound shift in how to think about legal research."

这种变化体现在客户的反馈里。Hron 说，过去“要花几十个小时”的研究，现在“几分钟内”就能到手，给专业人士一个可以评估、打磨并据以行动的高质量起点。“Deep research（深度研究）彻底改变了思考法律研究的方式。”

## 构建以 agent 为先的产品（Building an agent-first product）

For Thomson Reuters, building agents isn't about creating a smarter chatbot. It reflects a new way to deliver existing products. Hron and his team set out to teach an agent to use all the tools the company used to offer as standalone software. A single agent now has access to hundreds of company tools — simultaneously.

对 Thomson Reuters 而言，构建 agent 不是为了做一个更聪明的聊天机器人，而是体现了一种交付现有产品的新方式。Hron 和团队着手教一个 agent 使用公司过去作为独立软件提供的所有工具。如今，单个 agent 可以同时访问公司的数百个工具。

That shift changed how Thomson Reuters evaluated models. "Our big test for Claude is to really assess how good it is at making plans and using these tools effectively and correctly," he says.

这一转变也改变了 Thomson Reuters 评估模型的方式。“我们对 Claude 的大考，是真正评估它制定计划以及有效、正确地使用这些工具的能力，”他说。

CoCounsel Legal shows what that looks like. It used to run separate skills one after another. Rebuilt on the Claude Agent SDK, it now plans, delegates, and orchestrates across tools and content sources in real time, so a professional can define the outcome instead of dictating every step. Customer data remains protected and is not used to train third-party models.

CoCounsel Legal 展示了这一切的样子。它过去是一项接一项地运行各项独立技能。在 Claude Agent SDK 上重建之后，它如今可以实时地跨工具与内容源进行规划、委派和编排，专业人士因此可以定义结果，而不必口述每一个步骤。客户数据始终受到保护，不会被用于训练第三方模型。

Hron traces the choice back to how the two companies started working together. Thomson Reuters was one of Anthropic's earliest enterprise customers, and the deciding factor wasn't a benchmark. "The number one thing that spoke to us was Anthropic's approach to building enterprise AI," he says, citing transparency, safety, and responsible AI development. The first proof point was deep research in legal, built together as both teams noticed how Anthropic's engineers used the tools the way Thomson Reuters was already shipping them.

Hron 把这一选择追溯到两家公司最初合作的契机。Thomson Reuters 是 Anthropic 最早的企业客户之一，而决定性因素并不是某个基准测试。“最打动我们的是 Anthropic 构建企业 AI 的方式，”他说，并提到了透明性、安全性以及负责任的 AI 开发。第一个实证是法律领域的 deep research：双方注意到 Anthropic 的工程师使用这些工具的方式，恰是 Thomson Reuters 已经在交付的方式，于是共同把它构建了出来。

## 知识工作对模型的要求（What knowledge work demands of a model）

![公司各团队使用 Claude Cowork 的场景](images/thomson-1.jpg)

> Product, operations, and business teams across the company use Claude Cowork for process automation and light prototyping.
> 公司内部的产品、运营和业务团队使用 Claude Cowork 进行流程自动化和轻量原型设计。

Across those projects, Hron's team has settled on four things a model has to do before Thomson Reuters trusts it.

在这些项目中，Hron 的团队总结出模型必须做到的四件事，Thomson Reuters 才会信任它。

First, the model, as part of the CoCounsel Legal system, has to check its own citations. Rather than retrieve a source and move on, the system has to validate what it cites before presenting its findings to a human for final review and verification.

第一，模型作为 CoCounsel Legal 系统的一部分，必须核查自己的引用。系统不能只是检索到来源就继续，而必须在把发现呈现给人类做最终评审与核查之前，先验证它引用的内容。

In this system, the model also has to hold steady across long chains of tool calls. Longer tasks demand better context management and dependable tool use over an extended run. A model has to keep the thread across many steps and many systems, so an agent finishes real work instead of stalling halfway through.

在这个系统中，模型还必须在长长的工具调用链中保持稳定。更长的任务要求更好的上下文管理和长时间运行中可靠的工具使用。模型必须跨越许多步骤和许多系统守住主线，agent 才能完成真正的工作，而不是中途搁浅。

It also has to bring a person into the work, not just the answer. For the hardest jobs, Hron wants a model that will "bring the human into the loop of developing a work product rather than just relying on the agent to one shot an answer."

它还必须把人带进工作本身，而不只是给出答案。对最难的任务，Hron 希望模型能“把人带进工作成果打磨的闭环里，而不是只依赖 agent 一次性给出答案”。

And finally, it has to free up time for work the Thomson Reuters team didn't have bandwidth to tackle before. Thomson Reuters is developing advanced drafting capabilities for complex legal work, including motion drafting, filings that professionals would otherwise "spend days or weeks perfecting," he says. The task "always required far too much context and precision" for earlier models. With Claude Fable 5, it's now within reach.

最后，它必须为 Thomson Reuters 团队腾出时间，去做以前没有余力处理的工作。Thomson Reuters 正在为复杂法律工作开发高级起草能力，包括动议（motion）起草--这些法律文件专业人士原本要“花上数天乃至数周去打磨”，他说。这类任务“一直都要求远超早前模型的上下文与精度”。有了 Claude Fable 5，它如今触手可及。

## AI 的投资回报（The ROI of AI）

Hron takes a contrarian view on AI's return on investment, one other leaders rolling out models might find useful. "If you try to optimize too much for the rate of return calculation, you miss the forest for the trees," he says. He wants teams to feel the cultural and mindset shift before they tune for cost per task. Once that mindset shift happens, the returns follow on their own.

Hron 对 AI 的投资回报持一种反主流的看法，其他正在铺开模型的领导者或许会觉得有用。“如果你过度优化投资回报率的计算，就会见木不见林，”他说。他希望团队先感受到文化与心态的转变，再去精调每任务成本。而一旦心态转变发生，回报会随之而来。

He still tracks traditional engineering measures like DevOps Research and Assessment (DORA) and time from idea to production, and he points to an internal error-remediation tool built on Claude that turned a production issue from three hours of root cause analysis into a four-minute fix. "The ability to get back to health within minutes versus hours is a material difference."

他仍然跟踪 DevOps Research and Assessment（DORA）和从想法到生产的时间这类传统工程指标，并提到一个基于 Claude 构建的内部错误修复工具，把一个生产问题从三小时的根因分析缩短为四分钟修复。“几分钟而不是几小时就恢复健康，是实质性的差别。”

The deeper change, according to Hron, is to the work itself.

而按 Hron 的说法，更深层的改变发生在工作本身。

"The act of writing lines of code is no longer the job," Hron says of his engineers; the skills that matter most now are systems thinking, judgment, and taste. He sees the same pattern spreading past engineering, with AI making people "more T-shaped," able to reach across product, design, and finance rather than staying in one lane.

“‘写一行行代码’这件事已经不再是工作本身，”Hron 谈到他的工程师时说；如今最重要的技能是系统思维、判断力和品味。他看到同样的模式正在蔓延到工程之外--AI 让人变得“更 T 型”（T-shaped），能够横跨产品、设计和财务，而不是困在一条车道里。

## 下一步（What's next）

![Thomson Reuters 员工使用 Claude Code 的场景](images/thomson-2.jpg)

> Employees at Thomson Reuters use Claude Code to get up to speed on code bases and build long-running agents.
> Thomson Reuters 的员工使用 Claude Code 快速上手代码库，并构建长时间运行的 agent。

Hron and his team are eager to push the boundaries with Claude Fable 5 and future Claude models: longer-horizon work, better context management, and tool calling they can count on across the chain of tasks an agent runs.

Hron 和团队渴望与 Claude Fable 5 及未来的 Claude 模型一起拓展边界：更长时程的工作、更好的上下文管理，以及在整个 agent 任务链上都靠得住的工具调用。

He is just as eager to use these models in his own work. Claude Code has let him "be far more technical again," coming up to speed on a codebase he hasn't touched in months within minutes rather than a day, and he turns to Claude Cowork to take on the perspective of a CFO or strategy officer and pressure-test ideas.

他同样渴望在自己的工作中使用这些模型。Claude Code 让他“重新变得更有技术底气”--一个几个月没碰的代码库，几分钟而不是一天就能重新上手；他还借助 Claude Cowork 切换到 CFO 或战略负责人的视角，对想法进行压力测试。

Those are the directions models like Claude Fable 5 are being built around, and for work that ultimately has to hold up in court, Hron sees that as the frontier worth pushing on next. After all, professional AI has to work in environments where being almost right is not good enough.

这些正是 Claude Fable 5 这类模型围绕构建的方向，而对于最终必须经得起法庭检验的工作，Hron 认为这就是下一个值得推进的前沿。毕竟，专业 AI 必须在“几乎正确也远远不够”的环境里工作。

Get started with Claude Fable 5.

开始使用 Claude Fable 5。
