# 如何以及何时在 Claude Code 中使用 subagents（中英对照）

> **原文标题：** How and when to use subagents in Claude Code
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/subagents-in-claude-code
> **发布日期：** 2026-04-07
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

When to delegate research, parallelize tasks, or get a fresh review with Claude Code subagents-and when to stick with the main session.

何时用 Claude Code subagents 委派研究、并行执行任务或获取全新视角的审查--以及何时该坚守主会话。

A practical guide to Claude Code subagents: when they help, how to direct them, and the signals that tell you delegation is worth it.

一份 Claude Code subagents 的实用指南：它们何时有用、如何指挥它们，以及哪些信号表明值得委派。

Claude Code handles complex, multi-step projects well, but long sessions accumulate weight. Every file read, every tangent explored, every half-finished thought stays in the context window, slowing responses and driving up token costs.

Claude Code 能很好地处理复杂的多步骤项目，但漫长的会话会不断累积负担。读过的每个文件、探索过的每条岔路、每个未完成的想法，都会留在上下文窗口（context window）里，拖慢响应速度并推高 token 成本。

Consider building a new feature in a large TypeScript monorepo. The main work is the implementation, but side tasks keep appearing: trace how an existing service handles auth, find the shared util for date formatting, check whether the design system already has a component close to what you need. None of these need the full project context, and running them inside the main session adds noise. What if you could run them in parallel?

设想在一个大型 TypeScript monorepo 中构建一个新功能。主要工作是实现本身，但杂项任务不断冒出来：追踪某个现有服务如何处理认证、找到日期格式化的共享工具函数、检查设计系统里是否已有接近你需求的组件。这些都不需要完整的项目上下文，放在主会话里执行只会增加噪音。要是能并行处理它们呢？

Enter subagents. A subagent is an isolated Claude instance with its own context window. It takes a task, does the work, and returns only the result. Think of subagents as the browser tabs of a Claude Code session: a place to chase a tangent without losing the main thread.

于是 subagents 登场。subagent 是一个拥有独立上下文窗口的隔离 Claude 实例。它接收一项任务、完成工作，然后只返回结果。可以把 subagents 想象成 Claude Code 会话的浏览器标签页：一个追查岔路而不丢失主线的地方。

In this article, we discuss when it makes sense to use subagents, how to invoke them, and when the overhead isn't worth it.

在本文中，我们将讨论什么时候适合使用 subagents、如何调用它们，以及什么时候不值得付出这点开销。

# 什么是 subagent？（What is a subagent?）

Subagents are self-contained agents that operate with their own context windows. When Claude spawns a subagent, that assistant works independently to read files, explore code, or make changes. When it completes its task, the subagent returns only the relevant results to the main conversation.

subagents 是用各自独立的上下文窗口运行的自包含智能体（agent）。当 Claude 派生（spawn）一个 subagent 时，这个助手会独立地读取文件、探索代码或进行修改。任务完成后，subagent 只把相关结果返回给主对话。

Each subagent starts fresh, unburdened by the history of the conversation or invoked skills. Multiple subagents can run in parallel, and each can have different permissions: a research subagent might have read-only access, while an implementation subagent gets full editing capabilities.

每个 subagent 都是全新启动的，不受对话历史或已调用 skills 的拖累。多个 subagents 可以并行运行，而且各自可以拥有不同的权限：研究型 subagent 可能只有只读权限，而实现型 subagent 则拥有完整的编辑能力。

Claude Code includes several built-in subagent types, including:

Claude Code 内置了几种 subagent 类型，包括：

- General-purpose agents for complex multi-step tasks
- Plan agents that research codebases before presenting implementation strategies
- Explore agents optimized for fast, read-only code search

- 用于复杂多步骤任务的通用（general-purpose）智能体
- 在提出实现策略之前先研究代码库的规划（plan）智能体
- 为快速、只读的代码检索而优化的探索（explore）智能体

Claude Code often spawns subagents on its own to handle assigned tasks. It's also possible to direct that behavior explicitly and to define reusable specialists that Claude delegates to automatically. Knowing when to reach for subagents is what makes the feature useful.

Claude Code 常常会自行派生 subagents 来处理分配的任务。你也可以显式地引导这一行为，并定义可复用的专家型智能体，让 Claude 自动把任务委派给它。知道什么时候该用 subagents，才能让这个功能真正发挥价值。

# 什么时候应该使用 subagents？（When should you use subagents?）

Certain categories of work benefit clearly from subagent delegation. Learning to recognize them makes the feature far more effective.

有几类工作明显能从 subagent 委派中受益。学会识别它们，能让这个功能的效果大为提升。

## 研究密集型任务（Research-heavy tasks）

When understanding how something works is a prerequisite to changing it, a subagent can explore the codebase and return a summary rather than dumping dozens of files into the conversation.

当理解某个东西的工作原理是修改它的前提时，subagent 可以去探索代码库并返回一份摘要，而不是把几十个文件一股脑倒进对话里。

The signal: Gathering context requires reading dozens of files.

信号：收集上下文需要阅读几十个文件。

The benefit: The main conversation stays clean, and synthesized findings arrive instead of raw content.

收益：主对话保持干净，送来的是提炼后的发现而非原始内容。

## 多个独立任务（Multiple independent tasks）

When fixing errors across several files, updating patterns in multiple components, or making changes that don't depend on each other, parallel subagents complete the task faster.

当需要跨多个文件修错、更新多个组件中的模式，或进行互不依赖的修改时，并行的 subagents 能更快完成任务。

The signal: Sub-tasks have no dependencies between them.

信号：各子任务之间没有依赖关系。

The benefit: Three subagents working simultaneously generally finish the task in less time.

收益：三个 subagents 同时工作，通常能用更少的时间完成任务。

## 需要全新视角（Fresh perspective needed）

When an unbiased review of an implementation is the goal, a subagent provides a clean slate because it doesn't inherit the assumptions, context, or blind spots from the primary conversation.

当目标是对某项实现做一次不带偏见的审查时，subagent 能提供一张白纸，因为它不会继承主对话中的假设、上下文或盲点。

The signal: Verification is needed without conversation history influencing the analysis.

信号：需要验证，但不想让对话历史影响分析。

The benefit: Cleaner, more objective feedback.

收益：更干净、更客观的反馈。

Pro-tip: The /clear command also resets context and conversation history, providing a similarly unbiased slate, but at the cost of losing that history entirely. A subagent achieves the same fresh perspective while the main conversation stays intact.

专业提示：/clear 命令也会重置上下文和对话历史，提供同样不带偏见的白纸，但代价是彻底丢失这些历史。而 subagent 在保持主对话完好无损的同时，实现了同样的全新视角。

## 提交前验证（Verification before committing）

Before finalizing changes, an independent subagent can verify the implementation isn't overfitting to tests or missing edge cases.

在最终敲定改动之前，可以让一个独立的 subagent 验证实现是否过拟合（overfitting）于测试、或遗漏了边界情况（edge case）。

The signal: A second opinion is warranted before committing code.

信号：在提交代码之前需要第二意见。

The benefit: Catches issues that familiarity with the code might obscure.

收益：能抓住对代码过于熟悉可能掩盖的问题。

## 流水线式工作流（Pipeline workflows）

When a task has distinct phases (i.e., design, then implement, then test), each stage benefits from focused attention.

当任务有明显分阶段（比如先设计、再实现、后测试）时，每个阶段都能从专注的处理中受益。

The signal: Sequential stages with clear handoffs.

信号：顺序推进的阶段，且有清晰的交接。

The benefit: Each subagent concentrates on its phase, without context from other stages creating noise.

收益：每个 subagent 专注于自己的阶段，不会受到其他阶段上下文的噪音干扰。

Pro-tip: When a task requires exploring ten or more files, or involves three or more independent pieces of work, that's a strong signal to direct Claude toward subagents.

专业提示：当一项任务需要探索十个以上文件，或涉及三个以上独立工作块时，这就是引导 Claude 使用 subagents 的强烈信号。

# 如何引导 subagent 的使用（How to direct subagent usage）

Several methods exist for invoking subagents, ranging from simple conversation to automated workflows. The right starting point depends on the workflow, and sophistication can be layered on as patterns emerge.

调用 subagents 的方法有多种，从简单的对话到自动化工作流不等。合适的起点取决于具体工作流，随着模式逐渐清晰，再逐步叠加更复杂的机制。

## 对话式调用（Conversational invocation）

The most flexible approach is simply asking Claude to use subagents in conversation. This works across all Claude Code interfaces: terminal, VS Code, JetBrains, the web, and desktop applications.

最灵活的方式就是在对话中直接让 Claude 使用 subagents。这适用于所有 Claude Code 界面：终端、VS Code、JetBrains、网页版和桌面应用。

Natural language patterns that reliably invoke subagents include:

能够可靠触发 subagents 的自然语言模式包括：

- "Use a subagent to explore how authentication works in this codebase"
- "Have a separate agent review this code for security issues"
- "Research this in parallel. Check the API routes, database models, and frontend components simultaneously"
- "Spin up subagents to fix these TypeScript errors across the different packages"

- “用一个 subagent 探索这个代码库里的认证是怎么实现的”
- “让一个单独的智能体审查这段代码的安全问题”
- “并行研究这个问题。同时检查 API 路由、数据库模型和前端组件”
- “拉起几个 subagents，在不同 package 里修复这些 TypeScript 错误”

Being explicit matters. Specify the scope, request parallel execution when tasks are independent, and describe the desired output.

把话说清楚很重要。明确范围，任务独立时请求并行执行，并描述期望的输出。

Here's an effective prompt structure:

下面是一个有效的提示词结构：

This prompt works because it clearly defines three independent tasks, explicitly requests parallel execution, and specifies the output format. Claude understands the intent and spawns appropriate subagents.

这个提示词之所以有效，是因为它清晰定义了三个独立任务、明确请求并行执行，并指定了输出格式。Claude 理解意图后就会派生合适的 subagents。

Tips for effective conversational invocation include:

有效进行对话式调用的一些技巧包括：

- Scope tasks clearly. "Explore how payments work" beats "explore everything."
- Request parallelization explicitly. Say "these can run in parallel" or "work on all three simultaneously."
- Specify what should be returned. Summaries, specific findings, or recommendations. Naming the output format helps Claude deliver it.
- Ask for fresh context when unbiased analysis matters. "Use a subagent that does not see our previous discussion" ensures clean evaluation.

- 把任务范围说清楚。“探索支付是如何工作的”胜过“探索一切”。
- 明确请求并行化。说“这些可以并行运行”或“同时处理这三件事”。
- 指定应返回什么。摘要、具体发现或建议。点明输出格式有助于 Claude 交付结果。
- 当无偏分析很重要时，要求使用全新上下文。“使用一个看不到我们先前讨论的 subagent”可以确保干净的评估。

Pro-tip: When a subagent is taking a while, Ctrl+B sends it to the background. The conversation can continue while it runs, and results surface automatically when it finishes. The /tasks command shows anything running in the background.

专业提示：当某个 subagent 运行时间较长时，Ctrl+B 可以把它转到后台。它运行期间对话可以继续，完成后结果会自动浮现。/tasks 命令可以查看后台正在运行的任务。

## 自定义 subagents（Custom subagents）

When the same kind of subagent keeps getting requested (a security reviewer, a test writer, a docs proofreader), it can be defined once as a custom subagent.

当同一类 subagent 被反复请求时（比如安全审查者、测试编写者、文档校对者），可以把它一次性定义为自定义 subagent。

Claude then delegates to it automatically whenever a task matches its description, no prompting required.

之后只要任务与其描述匹配，Claude 就会自动委派给它，无需额外提示。

Custom subagents live as markdown files in .claude/agents/ (project-level, shared with the team) or ~/.claude/agents/ (user-level, available across all projects). Each one gets its own system prompt, tool permissions, and optionally its own model.

自定义 subagents 以 markdown 文件的形式存在于 .claude/agents/（项目级，与团队共享）或 ~/.claude/agents/（用户级，所有项目可用）。每个 subagent 都有自己的 system prompt、工具权限，还可以有自己的模型。

The easiest way to create one is the /agents command, which walks through setup interactively and can generate a first draft from a description. The file can also be written by hand, for example:

创建它最简单的方式是 /agents 命令，它会以交互方式引导你完成设置，还能根据描述生成初稿。这个文件也可以手写，例如：

With this in place, Claude routes matching work to the subagent automatically. It can also be invoked by name: "Have the security-reviewer look at the staged changes."

配置好后，Claude 会自动把匹配的工作路由给该 subagent。也可以按名字调用它：“让 security-reviewer 看看已暂存的改动。”

Custom subagents work best when:

自定义 subagents 最适合这些场景：

- A specialist should be available for Claude to delegate to automatically when a task matches
- The work benefits from a tightly scoped system prompt and restricted tools
- The configuration should be shared across a team or reused across projects

- 希望有一位专家型智能体待命，任务匹配时由 Claude 自动委派
- 工作能从严格限定范围的 system prompt 和受限工具中受益
- 配置需要在团队内共享或跨项目复用

Pro-tip: The description field is what Claude uses to decide when to delegate. Be specific about the trigger conditions, not just the capability. "Reviews code for security issues before commits" routes better than "security expert."

专业提示：description 字段是 Claude 决定何时委派的依据。要把触发条件写具体，而不只是能力。“在提交前审查代码的安全问题”比“安全专家”能更好地完成路由。

For the full configuration reference, including permission modes and how project and user subagents interact, see our Claude Code subagents docs.

完整的配置参考（包括权限模式以及项目级与用户级 subagents 如何交互），请参阅我们的 Claude Code subagents 文档。

## CLAUDE.md 指令（CLAUDE.md instructions）

Custom subagents define who the specialists are. CLAUDE.md files define the rules for when Claude should reach for them. If every code review should go through a read-only subagent, or every architecture question should trigger a research pass first, CLAUDE.md is where that policy lives. Claude reads it at the start of every conversation, so the behavior stays consistent across sessions and teammates without anyone needing to remember to ask.

自定义 subagents 定义了专家是谁，CLAUDE.md 文件则定义了 Claude 何时应该启用它们的规则。如果每次代码审查都应经由只读 subagent 进行，或每个架构问题都应先触发一轮研究，那么这项策略就写在 CLAUDE.md 里。Claude 在每次对话开始时都会读取它，因此这一行为在不同会话和不同团队成员之间保持一致，谁都不必特意记得去要求。

CLAUDE.md is a good fit for subagent instructions when:

当满足以下情形时，CLAUDE.md 很适合承载 subagent 指令：

- Code reviews should always use read-only subagents
- The project has specific research patterns Claude should follow
- Consistent behavior is needed across team members and sessions

- 代码审查应始终使用只读 subagents
- 项目有 Claude 应遵循的特定研究模式
- 需要在团队成员和会话之间保持行为一致

Here's an example of a simple CLAUDE.md file that triggers a subagent given specific conditions:

下面是一个简单 CLAUDE.md 文件的示例，它在特定条件下触发 subagent：

With the above CLAUDE.md file, every code review request automatically uses the defined pattern, eliminating the need to specify it each time.

有了上面这个 CLAUDE.md 文件，每个代码审查请求都会自动采用定义好的模式，省去了每次都要说明的麻烦。

For more on CLAUDE.md files, see Customizing Claude Code for your codebase: setting up a CLAUDE.md file and our Claude Code CLAUDE.md file docs.

关于 CLAUDE.md 文件的更多内容，请参阅《为你的代码库自定义 Claude Code：配置 CLAUDE.md 文件》以及我们的 Claude Code CLAUDE.md 文件文档。

## Skills

For complex multi-step workflows that run repeatedly, skills provide a reusable interface. Define a skill once in .claude/skills/, then invoke it with /skill-name or let Claude load it automatically when a task matches its description.

对于反复运行的复杂多步骤工作流，skills 提供了可复用的接口。在 .claude/skills/ 中定义一次 skill，之后用 /skill-name 调用，或在任务与其描述匹配时让 Claude 自动加载。

Skills differ from CLAUDE.md files in scope. CLAUDE.md files are always loaded and shapes every interaction. A skill is loaded on demand, either because it was invoked explicitly or because Claude matched the current task to the skill's description field. That makes skills the right place for workflows that should be available but not applied to every prompt.

skills 与 CLAUDE.md 文件的区别在于作用范围。CLAUDE.md 文件总是被加载，并影响每一次交互；skill 则按需加载--要么被显式调用，要么因为 Claude 把当前任务与 skill 的 description 字段匹配上。因此，那些应当随时可用、但不必应用到每条提示的工作流，放在 skills 里最合适。

Skills fit well when:

skills 适合这些场景：

- Certain actions get run regularly
- Different team members need access to the same complex operation
- Standardizing how certain tasks are performed across the team matters

- 某些操作会被定期执行
- 不同团队成员需要使用同一个复杂操作
- 需要把团队执行某些任务的方式标准化

Here's an example of a deep-review skill for comprehensive code review:

下面是一个用于全面代码审查的 deep-review skill 示例：

In the code snippet above, /deep-review triggers a three-part subagent analysis on demand. Because the description mentions reviewing staged changes before commits, Claude can also reach for this skill automatically when that context comes up.

在上面的代码片段中，/deep-review 按需触发一次由三部分组成的 subagent 分析。由于 description 中提到了在提交前审查已暂存的改动，当该场景出现时，Claude 也能自动启用这个 skill。

A skill is a directory, not a single file. Alongside SKILL.md, it can hold templates Claude fills in, example outputs showing the expected format, or scripts Claude executes as part of the workflow. The legacy .claude/commands/ format was a single flat file, so everything had to live in the prompt itself.

skill 是一个目录，而不是单个文件。除了 SKILL.md，它还可以存放供 Claude 填充的模板、展示预期格式的示例输出，或 Claude 在工作流中执行的脚本。旧的 .claude/commands/ 格式是单个扁平文件，所有内容都必须写进提示词本身。

For more on using skills with Claude Code, see our Claude Code skills docs.

关于在 Claude Code 中使用 skills 的更多内容，请参阅我们的 Claude Code skills 文档。

## Hooks

Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code's lifecycle. Hooks can automate subagent workflows based on events. Hooks trigger on specific actions and run subagent tasks without manual invocation.

hooks 是用户定义的 shell 命令、HTTP 端点或 LLM 提示，会在 Claude Code 生命周期的特定节点自动执行。hooks 可以基于事件自动化 subagent 工作流：在特定动作上触发，无需人工调用即可运行 subagent 任务。

Hooks are the right tool when:

在以下情形，hooks 是合适的工具：

- Every commit should be reviewed automatically before it's created
- Security checks should run without anyone remembering to ask
- CI-like quality gates belong in the local development process

- 每个提交在创建之前都应被自动审查
- 安全检查应自动运行，而不依赖有人记得发起
- 类似 CI 的质量关卡应纳入本地开发流程

Here is an example of a Stop hook that blocks Claude from ending its turn until a test is passed:

下面是一个 Stop hook 示例，它会阻止 Claude 结束当前回合，直到测试通过：

And the script at .claude/hooks/check-tests.sh:

以及位于 .claude/hooks/check-tests.sh 的脚本：

When Claude finishes its turn, the Stop event fires. The script runs the test suite-if tests fail, it returns JSON with decision: "block" and a reason. Claude Code reads that, doesn't let Claude stop, and feeds the reason back into the conversation as instruction to keep working. The stop_hook_active guard at the top prevents infinite loops: if Claude is already continuing because of a previous stop-hook block, the script lets it exit.

当 Claude 结束回合时，Stop 事件触发。脚本运行测试套件--若测试失败，它会返回带有 decision: "block" 和原因的 JSON。Claude Code 读取后不让 Claude 停下，并把原因作为继续工作的指令回馈到对话中。脚本顶部的 stop_hook_active 防护可防止无限循环：如果 Claude 已经因上一次 stop-hook 阻止而继续工作，脚本就放行退出。

Hooks represent the most automated approach to subagent orchestration. Conversational invocation or CLAUDE.md instructions are the better starting point; hooks come later, as workflows mature.

hooks 是 subagent 编排（orchestration）自动化程度最高的方式。对话式调用或 CLAUDE.md 指令是更好的起点；hooks 可以等日后工作流成熟了再上。

For complete hooks configuration, see Claude Code power user customization: how to configure hooks or our Claude Code hooks docs.

完整的 hooks 配置请参阅《Claude Code 高级用户自定义：如何配置 hooks》或我们的 Claude Code hooks 文档。

# 使用 subagents 的实用模式（Practical patterns for using subagents）

The following patterns demonstrate subagent direction applied to common scenarios.

以下模式展示了把 subagent 引导应用于常见场景的方法。

## 先研究后实现（Research before implementing）

When adding a feature to unfamiliar code, delegating research to a subagent first keeps the implementation discussion informed rather than exploratory, for example:

向不熟悉的代码添加功能时，先把研究工作委派给 subagent，可以让后续的实现讨论建立在充分信息之上，而不是边做边摸索，例如：

A synthesized summary arrives instead of twenty files of raw context, and the implementation discussion starts from a solid foundation.

送来的是一份提炼过的摘要，而不是二十个文件的原始上下文，实现讨论从一个坚实的基础开始。

## 并行修改（Parallel modifications）

When the same pattern needs updating across multiple files, parallel subagents finish faster and maintain focus, for example:

当同一个模式需要在多个文件中更新时，并行 subagents 完成得更快且更能保持专注，例如：

Three subagents working in parallel complete in roughly the time one would take. Each focuses on its file without context from the others creating confusion or inconsistency.

三个 subagents 并行工作大约只需单个所需的时间即可完成。每个 subagent 专注于自己的文件，不会因其他 subagent 的上下文而产生混乱或不一致。

## 独立审查（Independent review）

After implementing something complex, verification from a subagent that hasn't been influenced by the implementation journey catches what familiarity obscures, for example:

实现完复杂功能后，由一个未受实现过程影响的 subagent 来验证，能抓住被熟悉感掩盖的问题，例如：

The review subagent evaluates the code without knowing what tradeoffs were considered, what approaches were rejected, or what assumptions were made. This outside perspective surfaces issues the main conversation might miss.

审查 subagent 在评估代码时，并不知道当初考虑过哪些权衡、否决过哪些方案、做过哪些假设。这种外部视角能暴露主对话可能遗漏的问题。

## 流水线工作流（Pipeline workflow）

For multi-stage tasks, chaining subagents with explicit handoffs between phases keeps each stage focused, for example:

对于多阶段任务，用显式交接把 subagents 串联起来可以让每个阶段保持专注，例如：

Using a pipeline workflow, each stage in the task receives focused context. The design subagent isn't distracted by implementation concerns, the implementation subagent works from a clean spec, and the testing subagent evaluates the result independently.

采用流水线工作流后，任务的每个阶段都获得聚焦的上下文。设计 subagent 不会因实现问题分心，实现 subagent 基于干净的规格工作，测试 subagent 则独立评估结果。

# 什么时候不该使用 subagents？（When shouldn't you use subagents?）

While subagents are a useful feature, subagents carry overhead. Each one spins up its own context, consumes tokens, and adds a layer of indirection between the developer and the work. They're worth that cost when context isolation, parallelism, or a fresh perspective actually helps.

subagents 虽然有用，但也带来开销。每个 subagent 都要建立自己的上下文、消耗 token，并在开发者和工作之间增加一层间接性。当上下文隔离、并行化或全新视角确有帮助时，这份成本才花得值。

For smaller or tightly sequential tasks, sticking to the main conversation is usually simpler, for example:

对于较小或严格串行的任务，坚守主对话通常更简单，例如：

- Sequential, dependent work. When step two needs the full output of step one, and step three needs both, a single session handling the chain is usually cleaner than a relay of subagents passing state through files.
- Same-file edits. Two subagents editing the same file in parallel is a recipe for conflict. In this scenario, keep tightly coupled changes in one context window.
- Small tasks. For a quick fix or a focused question, the overhead of delegation outweighs the benefit. Just prompt or ask in your main conversation.
- Too many specialist agents. It's tempting to define a custom subagent for everything, but flooding Claude with options makes automatic delegation less reliable. Most teams settle on a handful of well-scoped agents rather than a sprawling roster.
- Work that needs agents to coordinate with each other. Subagents report back to the main conversation but can't talk to one another. For tasks where subagents need to communicate, use agent teams. With agent teams, subagents coordinate across separate sessions rather than within one, which makes them heavier and more expensive. For more guidance on when to use subagents vs Agent Teams, check out our Claude Code agent teams docs.

- 顺序依赖的工作。当第二步需要第一步的完整输出，第三步又需要前两者时，用一个会话处理整条链，通常比一串 subagents 通过文件传递状态更干净。
- 同文件编辑。两个 subagents 并行编辑同一个文件必然引发冲突。这种情况下，应把紧耦合的改动放在同一个上下文窗口里。
- 小任务。快速修复或针对性提问时，委派的开销得不偿失。直接在主对话里提需求或提问即可。
- 专家智能体过多。为所有事都定义一个自定义 subagent 很诱人，但给 Claude 塞太多选项会让自动委派变得不可靠。大多数团队最终只保留少数几个范围明确的智能体，而非一支臃肿的队伍。
- 需要智能体相互协作的工作。subagents 只向主对话汇报，彼此之间无法交流。如果任务需要 subagents 通信，请使用 agent teams（智能体团队）。agent teams 中的 subagents 跨独立会话协调而非在同一会话内，因此更重、更贵。关于何时使用 subagents 与 Agent Teams 的更多指引，请查阅我们的 Claude Code agent teams 文档。

The signals described earlier (i.e., needing a second opinion, a lack of dependencies between sub-tasks, and extensive research) make it clear when delegation to a subagent is worth it.

前文描述的信号（即需要第二意见、子任务之间没有依赖、以及大量研究工作）可以清楚地表明何时值得委派给 subagent。

# 从对话开始，之后再自动化（Start conversational, automate later）

Subagents deliver their full value when used deliberately. The automatic invocation Claude provides is helpful, but knowing when to delegate research, parallelize work, and request a fresh perspective produces better results than leaving it to chance.

有意识地使用 subagents，才能释放它们的全部价值。Claude 提供的自动调用固然有用，但清楚何时委派研究、并行工作、请求全新视角，会比听凭运气带来更好的结果。

When using subagents, start with conversational prompts. Notice which requests keep occurring and build automation as those patterns clarify. The goal is to make subagent delegation effortless, so your attention stays on the work that matters.

使用 subagents 时，先从对话式提示开始。留意哪些请求反复出现，等模式清晰后再逐步构建自动化。目标是让 subagent 委派变得毫不费力，让你的注意力始终留在真正重要的工作上。
