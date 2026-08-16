# 顾问策略：给智能体一次智力升级（中英对照）

> **原文标题：** The advisor strategy: Give agents an intelligence boost
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/the-advisor-strategy
> **发布日期：** 2026-04-09
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Pair Opus as an advisor with Sonnet or Haiku as an executor, and get Opus-level intelligence in your agents at a fraction of the cost.

让 Opus 担任顾问（advisor），搭配 Sonnet 或 Haiku 担任执行者（executor），以零头的成本为你的智能体带来 Opus 级别的智能。

Pair Opus as an advisor with Sonnet or Haiku as an executor, and get near Opus-level intelligence in your agents at a fraction of the cost.

让 Opus 担任顾问（advisor），搭配 Sonnet 或 Haiku 担任执行者（executor），以零头的成本为你的智能体带来接近 Opus 级别的智能。

Developers who want to better balance intelligence and cost have converged on what we call the advisor strategy: pair Opus as an advisor with Sonnet or Haiku as an executor. This brings near Opus-level intelligence to your agents while keeping costs near Sonnet levels.

希望在智能与成本之间取得更好平衡的开发者，已经收敛到我们所说的"顾问策略"（advisor strategy）：让 Opus 做顾问，Sonnet 或 Haiku 做执行者。这能为你的智能体带来接近 Opus 级别的智能，同时把成本维持在接近 Sonnet 的水平。

Today we're introducing the advisor tool on the Claude Platform to make the advisor strategy a one-line change in your API call.

今天，我们在 Claude Platform 上推出 advisor 工具，让顾问策略在你的 API 调用中只需一行改动即可启用。

# 用顾问策略构建高性价比智能体（Build cost-effective agents with the advisor strategy）

![顾问策略示意图：执行者向顾问请教](images/advisor-1.png)

With the advisor strategy, Sonnet or Haiku runs the task end-to-end as the executor, calling tools, reading results, and iterating toward a solution. When the executor hits a decision it can't reasonably solve, it consults Opus for guidance as the advisor. Opus accesses the shared context and returns a plan, a correction, or a stop signal, and the executor resumes. The advisor never calls tools or produces user-facing output, and only provides guidance to the executor.

在顾问策略中，Sonnet 或 Haiku 作为执行者端到端地运行任务：调用工具、读取结果、迭代逼近解决方案。当执行者遇到一个自己难以合理解决的决策点时，它会向作为顾问的 Opus 请教。Opus 访问共享上下文，返回一份计划、一处纠正或一个停止信号，执行者随后继续。顾问从不调用工具、也不产出面向用户的输出，只为执行者提供指导。

This inverts a common sub-agent pattern, where a larger orchestrator model decomposes work and delegates to smaller worker models. In the advisor strategy, a smaller, more cost-effective model drives and escalates without decomposition, a worker pool, or orchestration logic. Frontier-level reasoning applies only when the executor needs it, and the rest of the run stays at executor-level cost.

这与常见的子智能体（sub-agent）模式正好相反：后者由更大的编排模型分解工作并委派给更小的工作模型；而在顾问策略中，由更小、更具性价比的模型全程驱动并按需上报（escalate），无需任务分解、无需工作池、也无需编排逻辑。前沿级推理只在执行者需要时才登场，其余运行时间都停留在执行者级别的成本上。

In our evaluations, Sonnet with Opus as an advisor showed a 2.7 percentage point increase on SWE-bench Multilingual1 over Sonnet alone, while reducing cost per agentic task by 11.9%.

在我们的评测中，搭配 Opus 顾问的 Sonnet 在 SWE-bench Multilingual1 上比单独使用 Sonnet 高出 2.7 个百分点，同时把每个智能体任务的成本降低了 11.9%。

![SWE-bench Multilingual 评测结果对比图](images/advisor-2.png)

# advisor 工具（The advisor tool）

We're bringing the advisor strategy to our API with the advisor tool, a server-side tool which Sonnet and Haiku know to invoke when they need guidance or help with a specific task.

我们通过 advisor 工具把顾问策略带入 API。这是一个服务端工具，Sonnet 和 Haiku 知道在需要指导或需要针对特定任务获得帮助时调用它。

In our evaluations, Sonnet with an Opus advisor improved scores across BrowseComp2 and Terminal-Bench 2.03 benchmarks while costing less per task than Sonnet alone.

在我们的评测中，搭配 Opus 顾问的 Sonnet 在 BrowseComp2 和 Terminal-Bench 2.03 基准上得分均有所提升，而单任务成本比单独使用 Sonnet 还要低。

![BrowseComp 与 Terminal-Bench 评测结果对比图](images/advisor-3.png)

The advisor strategy also works with Haiku as the executor. On BrowseComp, Haiku with an Opus advisor scored 41.2%, more than double its solo score of 19.7%. Haiku with an Opus advisor trails Sonnet solo by 29% in score but costs 85% less per task. The advisor adds cost relative to Haiku alone, but the combined price is still a fraction of what Sonnet costs, making it a strong option for high-volume tasks that require a balance of intelligence and cost.

顾问策略同样适用于以 Haiku 为执行者。在 BrowseComp 上，搭配 Opus 顾问的 Haiku 拿到 41.2% 的成绩，是其单独使用时 19.7% 的两倍还多。与单独使用的 Sonnet 相比，搭配 Opus 顾问的 Haiku 得分落后 29%，但单任务成本低 85%。顾问相对单独使用 Haiku 会增加成本，但合计价格仍只是 Sonnet 的一小部分，这使它成为需要平衡智能与成本的高吞吐任务的强力选项。

![Haiku 搭配 Opus 顾问的评测结果对比图](images/advisor-4.png)

Declare advisor_20260301 in your Messages API request, and the model handoff happens inside a single /v1/messages request-no extra round-trips or context management. The executor model decides when to invoke it. When it does, we route the curated context to the advisor model, return the plan, and the executor continues all within the same request.

在你的 Messages API 请求中声明 advisor_20260301，模型交接就会在单次 /v1/messages 请求内完成--没有额外的往返，也不需要上下文管理。执行者模型自行决定何时调用它。一旦调用，我们会把精选的上下文路由给顾问模型，返回计划，执行者在同一请求内继续工作。

```python
response = client.messages.create(
    model="claude-sonnet-4-6",  # executor
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-6",
            "max_uses": 3,
        },
        # ... your other tools
    ],
    messages=[...]
)
# Advisor tokens reported separately
# in the usage block.
```

Pricing. Advisor tokens are billed at the advisor model's rates; executor tokens are billed at the executor model's rates. Since the advisor only generates a short plan (typically 400-700 text tokens) while the executor handles the full output at its lower rate, the overall cost stays well below running the advisor model end-to-end. Built-in cost controls. Set max_uses to cap advisor calls per request. Advisor tokens are reported separately in the usage block so you can track spend per tier.

定价。顾问 token 按顾问模型的费率计费；执行者 token 按执行者模型的费率计费。由于顾问只生成一份简短的计划（通常 400-700 个文本 token），而完整输出由执行者以更低的费率处理，总成本远低于端到端运行顾问模型。内置成本控制。设置 max_uses 可为每次请求的顾问调用设限。顾问 token 在 usage 块中单独报告，方便你按层级追踪开销。

Works alongside your existing tools. The advisor tool is just another entry in your Messages API request. Your agent can search the web, execute code, and consult Opus in the same loop.

与现有工具协同工作。advisor 工具只是 Messages API 请求中的又一个条目。你的智能体可以在同一个循环里搜索网页、执行代码，并向 Opus 请教。

![Logo](images/advisor-5.svg)

![Logo](images/advisor-6.svg)

"It makes better architectural decisions on complex tasks while adding no overhead on simple ones. The plans and trajectories are night and day different."

"它在复杂任务上做出更好的架构决策，同时在简单任务上零额外开销。产出的计划和轨迹有天壤之别。"

![Logo](images/advisor-7.svg)

![Logo](images/advisor-8.svg)

"We saw clear improvements in agent turns, tool calls, and overall score - better than a planning tool we built ourselves."

"我们看到智能体轮次、工具调用和总分的明显提升--比我们自己构建的一个规划工具还要好。"

![Logo](images/advisor-9.svg)

![Logo](images/advisor-10.svg)

"On structured document extraction tasks, the advisor tool enables Haiku 4.5 to dynamically scale intelligence by consulting Opus 4.6 as complexity demands, matching frontier-model quality at 5× lower cost."

"在结构化文档抽取任务上，advisor 工具让 Haiku 4.5 能随复杂度需要动态向 Opus 4.6 请教、按需扩展智能，以低 5 倍的成本匹配前沿模型的质量。"

# 开始使用（Get started）

The advisor tool is available now in beta natively on the Claude Platform. To get started:

advisor 工具现已在 Claude Platform 上以 beta 形式原生提供。开始使用：

- Add the beta feature header: anthropic-beta: advisor-tool-2026-03-01
- Add the advisor_20260301 to your Messages API request
- Modify your system prompt based on your use case

- 添加 beta 功能请求头：`anthropic-beta: advisor-tool-2026-03-01`
- 将 `advisor_20260301` 添加到你的 Messages API 请求中
- 根据你的用例修改系统提示词

We recommend running your existing eval suite against Sonnet solo, Sonnet executor with Opus advisor, and Opus solo. Explore the docs to learn more.

我们建议用你现有的评测套件分别测试：单独的 Sonnet、Sonnet 执行者 + Opus 顾问，以及单独的 Opus。查阅文档了解更多。

# 脚注（Footnotes）

- SWE-bench Multilingual: Sonnet 4.6 solo used adaptive thinking. Sonnet 4.6 + Advisor used our suggested system prompt for coding with thinking turned off. Both runs used high effort with bash and file editing tools. Scores are averaged over five trials of 300 problems across nine languages. Opus 4.6 was used as the advisor model in all runs.
- BrowseComp: All runs used thinking turned off with web search and web fetch tools. Sonnet 4.6 runs used medium effort. Sonnet 4.6 + Advisor used our suggested system prompt for coding; Haiku 4.5 + Advisor did not. No programmatic tool calling or context compaction. Scores are based on 1,266 problems with one attempt per problem. Opus 4.6 was used as the advisor model in all runs.
- Terminal-Bench 2.0: All runs used thinking turned off with bash and file editing tools. Sonnet 4.6 runs used medium effort. Neither advisor run used our suggested system prompt for coding. Each task ran in an isolated pod with 3x resource allocation and a 1x timeout. Scores are averaged over five attempts per task across 89 tasks. Opus 4.6 was used as the advisor model in all runs.

- SWE-bench Multilingual：单独运行的 Sonnet 4.6 使用了自适应思考（adaptive thinking）。Sonnet 4.6 + Advisor 使用了我们推荐的编码系统提示词并关闭思考。两组运行都以高强度（high effort）配合 bash 和文件编辑工具。得分为 300 道题目、九种语言、五次试验的平均值。所有运行均以 Opus 4.6 作为顾问模型。
- BrowseComp：所有运行均关闭思考，并使用网页搜索（web search）和网页抓取（web fetch）工具。单独运行的 Sonnet 4.6 使用中等强度（medium effort）。Sonnet 4.6 + Advisor 使用了我们推荐的编码系统提示词；Haiku 4.5 + Advisor 则没有。未使用程序化工具调用或上下文压缩（context compaction）。得分基于 1,266 道题目、每题一次尝试。所有运行均以 Opus 4.6 作为顾问模型。
- Terminal-Bench 2.0：所有运行均关闭思考，并使用 bash 和文件编辑工具。单独运行的 Sonnet 4.6 使用中等强度。两次 Advisor 运行均未使用我们推荐的编码系统提示词。每个任务在隔离的 pod 中运行，分配 3 倍资源、1 倍超时。得分为 89 个任务、每任务五次尝试的平均值。所有运行均以 Opus 4.6 作为顾问模型。
