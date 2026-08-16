# 在生产环境中运行 auto mode（中英对照）

> **原文标题：** Running auto mode in production
> **作者：** Molly Vorwerck
> **原文链接：** https://claude.com/blog/auto-mode-in-production
> **发布日期：** 2026-08-07
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

How customers like Nuro, Gusto, and Garner Health use auto mode to drive safer, longer running coding workflows.

Nuro、Gusto 和 Garner Health 等客户如何用 auto mode 驱动更安全、更长时运行的编程工作流。

How the teams at Nuro, Gusto, and Garner Health use auto mode to balance speed and safety at production scale.

Nuro、Gusto 和 Garner Health 的团队如何在生产规模下用 auto mode 平衡速度与安全。

Auto mode is now the default setting in Claude Code. Instead of asking you to approve every command an agent wants to run, a classifier evaluates each action and blocks ones that look potentially harmful.

auto mode 现已是 Claude Code 的默认设置。它不再要求你逐条批准智能体要运行的每个命令，而是由一个分类器（classifier）评估每个动作，并拦截看起来可能有害的那些。

Auto mode's design resolves a common agentic coding tradeoff: speed vs. safety. Reviewing every command keeps a human in the loop, but once sessions stretch to hours or multiply in parallel, that oversight becomes the bottleneck. Skipping permission checks entirely is faster-and it's also how prompt injection, scope drift, and the occasional deleted production resource get through.

auto mode 的设计解决了一个智能体编程中常见的权衡：速度与安全。逐条审查命令让人保持在回路（in the loop）中，可一旦会话拉长到数小时或并行开多个，这种监督就成了瓶颈。完全跳过权限检查当然更快--但提示词注入（prompt injection）、范围漂移（scope drift），以及偶尔被删掉的生产资源，也正是这么溜进来的。

Auto mode closes most of that gap. In internal evaluations, the classifier caught more dangerous actions than developers did when clicking through permission prompts by hand, and its performance held up under third-party red-teaming. And because sessions pause less often, Claude works 9x longer between interruptions than under the previous default-across all Claude Code usage.

auto mode 弥合了这一差距的大部分。在内部评估中，分类器抓到的危险动作比开发者手动点权限提示时抓到的更多，其表现也在第三方红队测试（red-teaming）下站得住脚。而且由于会话暂停得更少，在全部 Claude Code 使用中，Claude 两次打断之间的工作时间比上一个默认设置长了 9 倍。

To see how auto mode holds up in production, we spoke with teams at Nuro, Gusto, and Garner Health about how and why they use auto mode as their daily driver to balance speed with safety in their production environments.

为了解 auto mode 在生产中的实际表现，我们与 Nuro、Gusto 和 Garner Health 的团队聊了聊：他们如何以及为何把 auto mode 当作日常主力，在生产环境中平衡速度与安全。

## 在 Nuro 驱动更长时运行的自主智能体（Powering longer running autonomous agents at Nuro）

Nuro, the physical AI company developing universal Level 4 autonomous driving technology, adopted Claude Code in late 2025, and by March it was the most popular agentic coding tool at the company.

Nuro 是一家开发通用 L4 级自动驾驶技术的实体 AI（physical AI）公司，于 2025 年底引入 Claude Code，到三月份它已成为公司里最受欢迎的智能体编程工具。

Before auto mode shipped, staff software engineer Kai Zhou had already started prototyping an internal stand-in: a hook that sent each pending action to a small model, auto-approved the routine 90 percent of the time, and routed anything sensitive to Slack for a human to review. The prototype answered a real tension: engineers hated babysitting approval prompts, but from a company security and legal standpoint, skipping permissions outright was too dangerous to sanction. When auto mode shipped, Kai shelved the side project.

在 auto mode 发布之前，资深软件工程师 Kai Zhou 已经开始做一个内部替代品的原型：一个 hook，把每个待执行动作发给一个小模型，90% 的情况下自动放行常规操作，敏感操作则路由到 Slack 交由人工审查。这个原型回应了一组真实的矛盾：工程师讨厌盯着批准提示当保姆，但从公司安全与法务的角度看，彻底跳过权限又危险得无法获批。auto mode 一发布，Kai 就把这个副业项目束之高阁了。

Today, Kai runs auto mode for everything he writes.

如今，Kai 写的所有东西都开着 auto mode 跑。

"I don't want to sit there and click approve all the time," said Kai. "I use auto mode for 100 percent of my coding work. Most of the time, I open three or four sessions running auto mode in parallel and just check in when I need to."

“我不想坐在那儿一直点头批准，”Kai 说，“我 100% 的编程工作都用 auto mode。大多数时候，我会并行开三四个跑着 auto mode 的会话，需要时去看一眼就行。”

The exception is work that touches other teams. For instance, when Claude Code reviews a Pull Request on his behalf, Kai switches back to interactive mode and reviews each one before it goes out.

例外是涉及其他团队的工作。比如，当 Claude Code 代表他审查 Pull Request 时，Kai 会切回交互模式（interactive mode），在发出去之前逐条审查。

Auto mode doesn't run unconstrained, either. Nuro leans heavily on skills, and engineers deny the most dangerous commands, like recursive deletes, outright in their settings. The classifier makes its judgment calls inside those guardrails.

auto mode 也不是毫无约束地运行。Nuro 大量依赖 skills，工程师们在设置里直接禁用了最危险的命令，比如递归删除。分类器在这些护栏之内做判断。

The bigger auto mode unlock, however, has been the ability to kick off work that keeps running after engineers are done for the day. Specifically, Kai's team uses auto mode to power long-running research agents that hill-climb the evaluation metrics behind its autonomous-driving stack: tasks with a clear, measurable signal an agent can iterate against on its own.

不过，auto mode 带来的更大解锁，是可以启动在工程师下班后仍然继续运行的工作。具体来说，Kai 的团队用 auto mode 驱动长时运行的研究智能体，去爬坡（hill-climb）其自动驾驶技术栈背后的评估指标：这类任务有清晰、可度量的信号，智能体可以自行对着迭代。

Overnight, an agent can study false negatives flagged by the evaluation suite, draft a proposal, run experiments, and keep iterating on the results. The approach extends to any task with a clear evaluation method-another team at Nuro uses it to shrink the memory footprint of a specific binary-because the metric itself tells the agent whether it's improving or regressing.

一夜之间，智能体可以研究评估套件标记的假阴性（false negative）、起草提案、运行实验，并不断在结果上迭代。这个方法可以推广到任何有清晰评估方法的任务--Nuro 的另一个团队用它压缩某个特定二进制的内存占用--因为指标本身就会告诉智能体它是在进步还是在退步。

"The other day, I kicked off an agent at 10 p.m. and it kept running until 5 a.m.-and it gave me three PRs in the morning," Kai said. "I think it's pretty impressive. Only auto mode enables this kind of workload."

“前几天，我晚上 10 点启动了一个智能体，它一直跑到早上 5 点--早上给了我三个 PR，”Kai 说，“我觉得相当了不起。只有 auto mode 能支撑这种工作负载。”

## 在 Gusto 更快也更安全地交付 PR（Shipping PRs faster and safer at Gusto）

At Gusto, a leading SMB technology company, the move to auto mode started as a proactive security upgrade.

Gusto 是一家领先的中小企业（SMB）技术公司，转向 auto mode 最初是一次主动的安全升级。

Martin Emde, who works on the company's AI Dev Tools team, had watched permission fatigue slow the team down. Auto mode gave them the same velocity without sacrificing control or security, and since adoption took hold across engineering, the overall permissions burden has noticeably declined.

在该公司 AI Dev Tools 团队工作的 Martin Emde 亲眼看着权限疲劳（permission fatigue）拖慢团队。auto mode 让他们在不牺牲控制力或安全性的前提下保持了同样的速度，而且随着它在整个工程部门落地，整体权限负担已明显下降。

Martin has kicked off 2,425 Claude Code sessions since December, with auto mode as his daily driver. Cross-repo work that used to stall on folder-access approvals now runs uninterrupted, and unattended jobs, like compiling daily notes from GitHub, Slack, and Jira, run on their own. In his team's own analysis, roughly 10% of session transcripts since mid-May 2026 included an auto mode denial, evidence the classifier is doing real work without dragging on legitimate tasks.

自十二月起，Martin 已启动过 2,425 个 Claude Code 会话，auto mode 是他的日常主力。过去常因文件夹访问审批而卡壳的跨仓库工作现在一路畅通，像从 GitHub、Slack 和 Jira 汇编每日笔记这类无人值守的任务也自动运行。在他团队自己的分析中，2026 年五月中旬以来约有 10% 的会话记录里出现过一次 auto mode 拦截，这证明分类器在切实干活，同时没有拖累正当任务。

"Auto mode gave us a safer balance between speed and control," Martin said. "We were able to remove the repeated prompts and increase productivity without compromising safety. We can see that auto mode blocks at the right time, which gives us the confidence to move quickly."

“auto mode 在速度和控制之间给了我们一个更安全的平衡点，”Martin 说，“我们得以去掉重复的提示、提升生产力，而不牺牲安全性。我们看到 auto mode 在正确的时机拦截，这给了我们快速行动的信心。”

Chad Kunsman, a member of Gusto's AIT Cloud Engineering team, came to the same conclusion from the other direction. His work-endpoint investigations, log audits, connector management, doc ingestion across a stack of MCP servers-runs in short, twenty-minute bursts rather than overnight marathons. He wasn't looking for longer runs; he wanted the hands-off pace of bypass permissions without the exposure of a bad prompt, or a prompt injection, slipping through.

Gusto AIT 云工程团队的 Chad Kunsman 则从另一个方向得出了同样的结论。他的工作--端点排查、日志审计、连接器管理、跨一堆 MCP 服务器的文档摄取--以二十分钟的短促冲刺进行，而非通宵马拉松。他要的不是更长的运行，而是 bypass permissions 那种放手节奏，又不必承担一条坏提示、或一次提示词注入溜进来的风险。

"Given the protection against prompt injection, and the way it checks that what you're doing actually lines up with what you asked for, it's the better choice than bypass permissions and far faster than permission prompts," said Chad.

“鉴于它对提示词注入的防护，以及它会检查你正在做的与你所要求的是否真正一致，它是比 bypass permissions 更好的选择，又远快于权限提示，”Chad 说。

On the rare occasions the classifier does step in, Chad says it's on the mark. "When it stopped me, it made sense and explained why. It was drifting from what I'd originally asked, and it checked in. It wasn't off base at all."

至于分类器罕见的出手，Chad 说它拦得在点上。“它拦住我的时候，理由说得通，还解释了原因。当时任务正偏离我最初的要求，它就来确认了。一点都不离谱。”

Chad still steps out of auto mode for his most sensitive work. When a session has its teeth into production infrastructure-Terraform, AWS, direct POST calls against live APIs-he switches to accept edits and verifies each tool call by hand. "You have to weigh the amount of time you're saving against what it could reasonably make a mistake on, and how catastrophic that would be," he said. "Ultimately, you're still responsible for what happens."

最敏感的工作，Chad 仍会退出 auto mode。当会话咬住生产基础设施不放时--Terraform、AWS、直接对线上 API 发 POST 请求--他会切换到 accept edits 模式，逐个手工核对工具调用。“你必须权衡省下的时间，与它合理范围内可能出错的地方，以及那会有多灾难性，”他说，“说到底，出什么事你仍然要负责。”

That judgment operates inside a broader defense-in-depth setup: Gusto routes its MCP traffic through a governed proxy layer with tool guards and prompt inspection, so agents work with tightly scoped permissions before auto mode ever weighs in.

这一判断运行在更广的纵深防御（defense-in-depth）体系之内：Gusto 把 MCP 流量经由一个带工具防护和提示检查的受治理代理层路由，因此在 auto mode 出场之前，智能体就已经在严格限定的权限下工作了。

## 在 Garner Health 加速软件开发生命周期（SDLC）（Accelerating the software development lifecycle (SDLC) at Garner Health）

Garner Health, the healthcare technology company, rolled out Claude Code in February to all 550 employees across every function. The tool is wired into all the core systems including Salesforce, Zendesk, and Snowflake, and employees are encouraged to spend about two hours a week automating the most repeatable parts of their job.

医疗技术公司 Garner Health 于二月向全部 550 名员工、所有职能推出了 Claude Code。这款工具接入了包括 Salesforce、Zendesk 和 Snowflake 在内的所有核心系统，公司鼓励员工每周花约两小时，把自己工作中最可重复的部分自动化。

Before auto mode, that scale came with overhead. Evan Magnussen, Garner's platform engineering manager, describes permission management as a tedious cycle of hand-curating approved command lists and watching piped commands get rejected.

在 auto mode 之前，这种规模伴随着开销。Garner 的平台工程经理 Evan Magnussen 把权限管理描述成一个乏味的循环：手工整理获批准的命令清单，然后眼看着管道命令被拒。

Today, Evan and most of his colleagues use auto mode in every session, from researching the codebase to managing external integrations through MCP.

如今，Evan 和他的大多数同事在每个会话里都用 auto mode，从研究代码库到通过 MCP 管理外部集成。

"We've built out a standardized software development lifecycle for the entire engineering organization that is really only possible because of auto mode," Evan said. "Employees view it as a weight off their shoulders. They don't have to monitor their agents for hours on end anymore."

“我们为整个工程组织建起了一套标准化的软件开发生命周期，这真的只有靠 auto mode 才能实现，”Evan 说，“员工们把它看作卸下的一副重担。他们不用再一连几个小时盯着自己的智能体了。”

That lifecycle runs as a plugin of standardized skills. An agent picks up a task, explores the context it has access to, commits context files to the repository, runs what Evan calls "antagonistic research" to pressure-test its own assumptions, and then moves on to implementation-pausing for a human only when it needs context it can't find on its own. The research-heavy stages, Evan notes, weren't possible before auto mode.

这套生命周期以一个标准化 skills 插件的形式运行。智能体接起一个任务，探索它能访问的上下文，把上下文文件提交进仓库，运行一段 Evan 称之为“对抗性研究（antagonistic research）”的流程来压力测试自己的假设，然后进入实现--只有在需要它自己找不到的上下文时才暂停等人。Evan 指出，这些重研究的阶段在 auto mode 之前是不可能实现的。

Out of the box, the classifier has needed little tuning. Evan's one adjustment mirrors Kai's at Nuro: he configured auto mode not to approve actions that communicate with other people, like sending Slack messages or emails.

开箱即用，分类器几乎不需要调校。Evan 唯一的调整与 Nuro 的 Kai 如出一辙：他把 auto mode 配置为不批准与人沟通的动作，比如发 Slack 消息或电子邮件。

"I personally don't like Claude to just act on my behalf when I'm communicating with another person," he said. Teams working on core intellectual property-the most skeptical of skipping permissions before auto mode-learned to tune the classifier's injected prompts to be more or less permissive for their work.

“就我个人而言，我不喜欢 Claude 在我和别人沟通时替我擅自动作，”他说。那些负责核心知识产权的团队--在 auto mode 之前对跳过权限最持怀疑态度的人--则学会了调整分类器注入提示的松紧，使其对自己的工作更宽松或更严格。

His advice for other enterprises rolling it out? Lean in and build the right controls so that you can empower engineers while ensuring safe deployment. "If we were to say, everyone go build your own workflows, and we have no telemetry, that would be very dangerous," Evan said. "Because we have the telemetry, because we've built out workflows that are relatively standard, we have much more confidence."

他给其他正在推广 auto mode 的企业的建议？大胆采用，并建好正确的管控，从而在确保安全部署的同时赋能工程师。“如果我们说，大家都去自建工作流吧，而我们没有任何遥测（telemetry），那会非常危险，”Evan 说，“正因为我们有遥测，因为我们建出的工作流相对标准，我们才有了大得多的信心。”

Get started with auto mode in Claude Code.

开始使用 Claude Code 中的 auto mode。
