# 在前沿工作：Hebbia 如何打造不容错漏任何细节的金融尽调 AI（中英对照）

> **原文标题：** Working at the frontier: How Hebbia builds AI for financial diligence that can't miss a detail
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/working-at-the-frontier-how-hebbia-builds-ai-for-financial-diligence-that-cant-miss-a-detail
> **发布日期：** 2026-07-13
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

How Anthropic's Claude Fable 5 beat Hebbia's finance-specific model evaluations, achieving their biggest accuracy gain yet.

Anthropic 的 Claude Fable 5 如何在 Hebbia 的金融专用模型评估中胜出，创下他们迄今最大的准确率提升。

Hebbia builds research and diligence software for financial professionals, and tests every new model against finance evals tied to expert outcomes. In testing, Claude Fable 5 posted the biggest accuracy gain its research team has recorded, and tracked complex queries that prior models kept dropping.

Hebbia 为金融专业人士构建研究与尽调（diligence）软件，并用与专家工作成果挂钩的金融 evals（评估）来测试每一代新模型。在测试中，Claude Fable 5 创下了其研究团队记录过的最大准确率提升，并能持续追踪此前模型总是遗漏的复杂查询。

Hebbia is an AI platform built for the rigor of institutional finance, serving more than a third of the top 50 asset managers along with tier-1 investment banks and law firms. Divya Mehta, the company's founding product manager, spends roughly half her time with its largest investment banking, private equity, and credit customers.

Hebbia 是一个为机构金融的严苛标准而生的 AI 平台，服务的客户包括前 50 大资产管理公司中超过三分之一的公司，以及一线投资银行（tier-1 investment banks）和律师事务所。公司的创始产品经理（founding product manager）Divya Mehta 大约一半的时间都花在与公司最大的投行、私募股权和信贷客户打交道上。

Those customers make decisions based on analyses that span thousands of dense documents, where a wrong number can change the outcome of an entire deal.

这些客户的决策依据是横跨数千份密集文档的分析，其中一个数字出错就可能改变整笔交易的结果。

# Hebbia 如何守住准确率的底线（How Hebbia holds the line on accuracy）

A banker or investor weighing an opportunity has to work through all the data that could impact the decision, including the company's public filings, its credit agreements, internal documents, and structured data like information from a CRM. Hebbia's meta-prompting turns plain-language requests into prompts, and then Claude runs each step of the analysis across hundreds of documents. Each answer lands in its own cell on a grid in Hebbia's Matrix, enabling full transparency, traceability, and steerability.

一位正在权衡某个机会的银行家或投资者，必须处理所有可能影响决策的数据，包括公司的公开披露文件、信贷协议、内部文档，以及来自 CRM 之类的结构化数据。Hebbia 的元提示（meta-prompting）技术把自然语言请求转化为提示词，然后由 Claude 在数百份文档上执行分析的每一个步骤。每个答案都落在 Hebbia Matrix 网格中一个独立的单元格里，实现完全的透明性、可追溯性和可引导性。

Keeping those answers accurate at scale is the work of Hebbia's applied AI research team, led by Adithya Ramanathan. For Ramanathan, the point of that work is finding signals: getting a model to draw on the right data, in the right context, and surface what a customer wants to know.

让这些答案在大规模下保持准确，是 Hebbia 应用 AI 研究团队的工作，团队由 Adithya Ramanathan 领导。对 Ramanathan 而言，这项工作的核心在于找到信号：让模型在正确的上下文中调用正确的数据，并浮现出客户真正想知道的东西。

"When you're connecting it to the right data and putting it in the right ecosystem," Ramanathan says, "that's when you get the alpha that finance professionals actually chase."

"当你把它连接到正确的数据、放进正确的生态系统时，"Ramanathan 说，"你才能得到金融专业人士真正追逐的 alpha（超额收益）。"

Getting there means running every new model through Hebbia's finance-specific benchmark, head to head against the model it would replace, and expanding what the benchmark measures with each release to keep pace as models improve. The benchmark is built to be hard on purpose.

要做到这一点，就意味着让每一代新模型都跑一遍 Hebbia 的金融专用基准测试，与它将要取代的模型正面对决，并随着每次发布不断扩展基准测试的测量范围，以跟上模型进步的速度。这个基准测试是刻意做得很难的。

"The bar is extremely high, and our customers hold us to that extremely high bar—and rightfully so," Mehta says. "At the end of the day, they're making investment decisions at a very large scale based on the analysis and final work product built in Hebbia."

"这个标准极高，而我们的客户也用这个极高的标准来要求我们--这是理所当然的，"Mehta 说，"归根结底，他们是基于在 Hebbia 中完成的分析和最终工作成果，在做非常大规模的投资决策。"

![Hebbia 团队用金融专用基准测试评估每一代新的 Claude 模型](images/hebbia-1.jpeg)

> The team at Hebbia runs every new Claude model through finance-specific benchmarks that run head-to-head against the model it would replace.
> Hebbia 团队会让每一代新的 Claude 模型跑过金融专用基准测试，与它将要取代的模型正面对决。

# 以迄今最大优势通过 Hebbia 的评估（Clearing Hebbia's evals by the widest margin yet）

Joe Renner, a researcher on the applied AI team, runs each new Claude model against that benchmark, with a battery of tests replicating key finance knowledge worker use cases. One such test covers question answering and citation finding over financial documents. Another test runs through Hebbia's agent system, with the tools its chat product uses, on the kind of open-ended, multi-source analysis a customer actually does.

应用 AI 团队的研究员 Joe Renner 负责让每一代新的 Claude 模型接受该基准测试的检验，整套测试复现了金融行业知识工作者的关键用例。其中一项测试覆盖对金融文档的问答与引文定位。另一项测试则通过 Hebbia 的智能体系统及其聊天产品所使用的工具，完成客户实际会做的那种开放式、多来源分析。

Claude Fable 5 cleared both by the widest margin Renner had measured. On the question-answering and citation test, it posted about a 20% relative gain in accuracy over financial documents, the best he had seen from any new model. Citation match held roughly steady—Renner believes the gain comes from the model better understanding the evidence it finds.

Claude Fable 5 以 Renner 测量过的最大优势通过了这两项测试。在问答与引文测试中，它在金融文档上的准确率取得了约 20% 的相对提升，这是他见过的所有新模型中最好的成绩。引文匹配率大致持平--Renner 认为提升来自模型对它所找到的证据理解得更加到位。

"It comes down to two seemingly fundamental qualities: the ability to find the right information from a dense data set, and then synthesize it correctly," Divya says. "These seem like fundamental model capabilities, but they have massive impact when we think about finance and research workflows." On the agent run, it held every part of a multi-part request at once, answering all of them and citing each answer back to its source.

"归根结底是两项看似基础的能力：从密集数据集中找到正确信息的能力，以及随后对其进行正确综合的能力，"Divya 说，"这些看似是模型的基础能力，但在我们考虑金融与研究工作流时，它们的影响是巨大的。"在智能体运行测试中，它把一个多部分请求的每一个部分同时记挂于心，逐一作答，并将每个答案都引回其出处。

Claude Fable 5 also showed more reach. On open-ended analysis, it reasoned from a wider cross-section of the data and arrived at conclusions the team thought were worth a closer look. Renner traces that to how the model holds a long task together: it keeps every part of a request in view, prompts its own sub-agents and tools so the right facts come back, and grounds each claim in the source rather than inferring it.

Claude Fable 5 还展现出更强的覆盖面。在开放式分析中，它从更广的数据横截面进行推理，得出的结论让团队认为值得进一步细看。Renner 把这一点归因于模型维系长任务的方式：它始终把请求的每个部分纳入视野，驱动自己的 sub-agent（子智能体）和工具取回正确的事实，并让每个论断都立足于来源文档而不是凭空推断。

# 用 Claude Fable 5 为交易尽调设立新标准（Setting a new standard for deal diligence with Claude Fable 5）

The information that gives customers an edge usually sits in unstructured, proprietary documents.

能给客户带来优势的信息，通常藏在非结构化的专有文档里。

Those have been harder to analyze at scale than the structured, quantitative data finance already models well. Hebbia built Matrix to make that qualitative work systematic, and every model generation widens what it can take on.

与金融界已经善于建模的结构化定量数据相比，这类文档一直更难大规模分析。Hebbia 构建 Matrix 就是为了让这类定性工作系统化，而每一代模型都在拓宽它能承担的范围。

That might be a data room with thousands of documents, where the work is finding the relevant signal, citing it, and drafting each section of an investment memo. Or it might be analyzing every document tied to a credit deal (the credit agreement, amendments, side letters, each running hundreds of dense technical pages) and extracting the full covenant package, financial terms and operating restrictions alike, from that unstructured mass.

这可能是一个装着数千份文档的数据室（data room），工作是从中找到相关信号、给出引文、起草投资备忘录的每个章节。也可能是分析与某笔信贷交易相关的所有文档（信贷协议、修订案、附加协议（side letters），每份都有数百页密集的技术内容），并从这堆非结构化的材料中提取出完整的契约条款包（covenant package）--既包括财务条款，也包括运营限制。

"These are actually the types of documents that Anthropic models have always done really well at," Mehta says.

"这些其实正是 Anthropic 模型一直都非常擅长处理的那类文档，"Mehta 说。

With earlier Sonnet and Opus models, Matrix could already pull out and synthesize a credit agreement's covenants—the dense protections a lender writes in for itself. With Claude Fable 5, Hebbia is reaching for the rest of the job: the multi-step analysis on top of those covenants, comparing them against live monitoring data, flagging risks, all the way to a first draft of the covenant review and an internal memo. That review is something credit firms used to pay outside teams a great deal to produce by hand.

借助早期的 Sonnet 和 Opus 模型，Matrix 已经能够提取并综合信贷协议中的契约条款（covenants）--即贷款人为自己写进协议的那些密集的保护性条款。有了 Claude Fable 5，Hebbia 开始触及这项工作的其余部分：在这些契约条款之上进行多步分析，将其与实时监控数据对比，标记风险，直至产出契约条款评审的初稿和一份内部备忘录。这种评审过去信贷机构要花大价钱请外部团队手工完成。

![Claude Fable 5 让 Hebbia Matrix 承担运行时间更长、步骤更多的任务](images/hebbia-2.jpeg)

> Claude Fable 5 enables Matrix, Hebbia's AI platform built for financial professionals, to take on longer-running, multi-step tasks like synthesizing credit agreement coven
> Claude Fable 5 让 Matrix--Hebbia 为金融专业人士构建的 AI 平台--得以承担运行时间更长、步骤更多的任务，比如综合提炼信贷协议的契约条款。

# 下一步（What's next）

Now that models like Claude Fable 5 can carry this work end to end, the comparison is the specialist hours it replaces.

既然像 Claude Fable 5 这样的模型已经能把这类工作从头到尾扛下来，衡量标准就变成了它所取代的专家工时。

Before AI, when a managing director needed a deck to pitch a CEO, it would take a junior banker 2-3 days to learn the company, pull financials, and build slides. In the pre-Opus days, the timeline to produce a first draft compressed by 12 to 24 hours, and with earlier Opus models on Hebbia, Mehta says, it dropped even further, taking about a day to run end-to-end. Hebbia has since codified the whole job into a Matrix that gathers the data across sources in a set of deterministic agentic steps, does the analysis, and builds the final deck, financial model, and internal research in a couple of minutes, so the banker can spend the time on which buyers to pursue and how to position them. Claude Fable 5 tightens it further, she says.

在 AI 出现之前，当一位董事总经理（managing director）需要一份用来向 CEO 推介的材料时，一名初级银行家要花 2-3 天时间研究公司、拉取财务数据、制作幻灯片。在 Opus 问世之前，产出初稿的时间线压缩了 12 到 24 个小时；Mehta 说，随着早期 Opus 模型上线 Hebbia，时间进一步缩短，端到端跑完大约只需一天。此后，Hebbia 把整项工作固化成了一个 Matrix：以一组确定性的智能体步骤跨来源收集数据、完成分析，并在几分钟内生成最终的推介材料、财务模型和内部研究，让银行家把时间花在追踪哪些买家、如何定位他们上。她说，Claude Fable 5 让这一切进一步提速。

Decomposing the work into steps still matters, "no matter how brilliant the model is," because firms want control over which documents feed the analysis and how each step is built. So Hebbia is adopting the Claude Agent SDK to compose these jobs as smaller, repeatable, checked steps rather than a single model run.

"无论模型多么出色，"把工作分解成步骤依然重要，因为机构希望控制哪些文档进入分析、每个步骤如何构建。因此，Hebbia 正在采用 Claude Agent SDK，把这些工作组织成更小、可复用、可校验的步骤，而不是一次单一的模型运行。

"Compressing the deal lifecycle has a massive impact on a firm's ability to compete for those investments," Mehta says. She hears it in customer conversations. Two or three years ago the questions were defensive, about hallucinations and whether the math was right. "Today, those conversations have changed completely. They're: how can I automate more of my workflow? How do I sequence more steps together? How can I generate ten, fifteen, twenty slide decks in one click with high fidelity and consistency?"

"压缩交易生命周期，对一家机构争夺这些投资的竞争力有着巨大影响，"Mehta 说。她在客户对话中亲耳听到这一点。两三年前，客户的问题还是防御性的，关心的是幻觉（hallucinations）和计算是否正确。"如今，这些对话已经彻底变了。他们问的是：我怎么把更多工作流自动化？怎么把更多步骤串联起来？我怎么一键生成十份、十五份、二十份高保真、风格一致的推介材料？"

Get started with Claude Fable 5.

开始使用 Claude Fable 5。
