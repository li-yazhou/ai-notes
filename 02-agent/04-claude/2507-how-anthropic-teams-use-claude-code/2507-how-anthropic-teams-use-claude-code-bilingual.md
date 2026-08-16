# Anthropic 各团队如何使用 Claude Code（中英对照）

> **原文标题：** How Anthropic teams use Claude Code
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/how-anthropic-teams-use-claude-code
> **发布日期：** 2025-07-24
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Teams across Anthropic use Claude Code for everything from debugging production issues and navigating unfamiliar codebases to building custom automation tools. Here's how.

Anthropic 的各个团队把 Claude Code 用于一切工作--从调试生产问题、浏览陌生代码库，到构建自定义自动化工具。以下是他们的做法。

Agentic coding tools like Claude Code help developers accelerate workflows, automate repetitive tasks, and tackle complex programming projects. As the field evolves, we're learning about new applications everyday from users, including our own employees.

像 Claude Code 这样的智能体编码（agentic coding）工具帮助开发者加速工作流、自动化重复性任务，并攻克复杂的编程项目。随着这一领域的发展，我们每天都在从用户（包括我们自己的员工）那里了解到新的应用方式。

To learn more, we sat down with employees across Anthropic to understand how they use Claude Code at work.

为了解更多，我们与 Anthropic 各部门的员工坐下来交流，了解他们如何在工作中使用 Claude Code。

While many of their use cases were predictable-debugging, navigating codebases, managing workflows-others surprised us. Lawyers built phone tree systems. Marketers generated hundreds of ad variations in seconds. Data scientists created complex visualizations without knowing JavaScript.

他们的许多用例在意料之中--调试、浏览代码库、管理工作流--但另一些让我们大吃一惊。法务团队搭建了电话树（phone tree）系统。营销人员在几秒钟内生成了数百个广告变体。数据科学家在不懂 JavaScript 的情况下创建了复杂的可视化。

The pattern became clear: agentic coding isn't just accelerating traditional development. It's dissolving the boundary between technical and non-technical work, turning anyone who can describe a problem into someone who can build a solution.

规律已经清晰：智能体编码不只是加速传统开发。它正在消解技术工作与非技术工作之间的边界，让任何能描述问题的人，都成为能构建解决方案的人。

Here's what we learned.

以下是我们的发现。

## 代码库导航与理解（Codebase navigation and understanding）

Teams across the company use Claude Code to help new hires and even long-time employees get up to speed on our codebases.

公司各部门的团队都在用 Claude Code 帮助新员工、甚至资深员工快速熟悉我们的代码库。

New data scientists on our Infrastructure team feed Claude Code their entire codebase to get productive quickly. Claude reads the codebase's CLAUDE.md files, identifies relevant ones, explains data pipeline dependencies, and shows which upstream sources feed into dashboards, replacing traditional data catalog tools.

基础设施团队新入职的数据科学家把整个代码库喂给 Claude Code，以快速进入产出状态。Claude 会读取代码库的 CLAUDE.md 文件、识别相关内容、解释数据管道（data pipeline）依赖，并展示哪些上游数据源汇入了哪些仪表盘，从而取代传统的数据目录（data catalog）工具。

Our Product Engineering team refers to Claude Code as their "first stop" for any programming task. They ask it to identify which files to examine for bug fixes, features, or analysis, eliminating the time-consuming process of manually gathering context before building new features.

我们的产品工程团队把 Claude Code 称为任何编程任务的"第一站"。他们让它指出修复 bug、开发功能或做分析时应检查哪些文件，省去了构建新功能前手动收集上下文的耗时过程。

## 测试与代码审查（Testing and code review）

Agentic coding tools are particularly popular for their ability to automate two critical but tedious programming tasks: writing unit tests and reviewing code.

智能体编码工具尤其受欢迎的一点，是它们能自动化两项关键却枯燥的编程任务：编写单元测试和审查代码。

The Product Design team uses Claude Code to write comprehensive tests for new features. They've automated Pull Request comments through GitHub Actions, with Claude handling formatting issues and test case refactoring automatically.

产品设计团队用 Claude Code 为新功能编写全面的测试。他们通过 GitHub Actions 自动化了 Pull Request 评论，由 Claude 自动处理格式问题并重构测试用例。

The Security Engineering team transformed their workflow from "design doc -> janky code -> refactor -> give up on tests" to asking Claude for pseudocode, guiding it through test-driven development, and checking in periodically. This results in more reliable, testable code.

安全工程团队把他们的工作流从"设计文档 -> 粗糙代码 -> 重构 -> 放弃测试"改造成了：向 Claude 要伪代码、引导它进行测试驱动开发（test-driven development），并定期跟进查看。这让代码更可靠、更可测。

Agentic coding can also be used to translate tests into other programming languages. For instance, when the Inference team needs to test functionality in unfamiliar languages like Rust, they explain what they want to test and Claude writes the logic in the native language of the codebase.

智能体编码还可用于把测试翻译成其他编程语言。例如，当推理（Inference）团队需要用 Rust 这类陌生语言测试功能时，他们描述想测什么，Claude 就用代码库的原生语言写出逻辑。

## 调试与排障（Debugging and troubleshooting）

Production issues demand quick resolution, but trying to reason about unfamiliar code under pressure often leads to delays. For many teams at the company, Claude Code accelerates diagnosis and fixes by analyzing stack traces, documentation, and system behavior in real-time.

生产问题要求快速解决，但在压力下理解陌生代码往往导致延误。对公司许多团队来说，Claude Code 通过实时分析堆栈跟踪（stack trace）、文档和系统行为，加速了诊断和修复。

During incidents, the Security Engineering team feeds Claude Code stack traces and documentation to trace control flow through the codebase. Problems that typically take 10-15 minutes of manual scanning now resolve 3x as quickly.

在事故期间，安全工程团队把堆栈跟踪和文档喂给 Claude Code，在代码库中追踪控制流。通常需要 10-15 分钟手工排查的问题，现在的解决速度快了 3 倍。

With Claude Code, the Product Engineering team gained confidence to tackle bugs in unfamiliar codebases. They ask Claude: "Can you fix this bug? This is the behavior I'm seeing" and review the proposed solution without needing to rely on other engineering teams for assistance.

借助 Claude Code，产品工程团队有了攻克陌生代码库中 bug 的信心。他们对 Claude 说："你能修这个 bug 吗？我看到的现象是这样的"，然后审查它提出的方案，无需再依赖其他工程团队协助。

In one instance, when Kubernetes clusters stopped scheduling pods, the Data Infrastructure team used Claude Code to diagnose the issue. They fed it dashboard screenshots, and Claude guided them menu-by-menu through Google Cloud's UI until they found pod IP address exhaustion. Claude then provided the exact commands to create a new IP pool and add it to the cluster, saving them 20 minutes of valuable time during a system outage.

有一次，Kubernetes 集群停止调度 pod，数据基础设施团队用 Claude Code 诊断问题。他们把仪表盘截图喂给它，Claude 引导他们逐个菜单地穿过 Google Cloud 的 UI，最终发现是 pod IP 地址耗尽。随后 Claude 给出了创建新 IP 池并将其加入集群的确切命令，在系统故障期间为他们节省了 20 分钟的宝贵时间。

## 原型与功能开发（Prototyping and feature development）

Building new features traditionally requires deep technical knowledge and significant time investment. Claude Code enables rapid prototyping and even full application development, letting teams validate ideas quickly regardless of their programming expertise.

构建新功能传统上需要深厚的技术知识和大量的时间投入。Claude Code 支持快速原型设计甚至完整的应用开发，让团队无论编程水平如何都能快速验证想法。

Members of the Product Design team would feed Figma design files to Claude Code and then set up autonomous loops where Claude Code writes the code for the new feature, runs tests, and iterates continuously. They give Claude abstract problems, let it work autonomously, then review solutions before final refinements. In one case, they had Claude build Vim key bindings for itself with minimal human review.

产品设计团队的成员把 Figma 设计文件喂给 Claude Code，然后建立自主循环：由 Claude Code 编写新功能代码、运行测试并持续迭代。他们给 Claude 抽象的问题，让它自主工作，然后在最终打磨前审查方案。有一次，他们让 Claude 以最少的人工审查为自己构建了 Vim 快捷键。

With Claude Code, the Product Design team discovered an unexpected use: mapping out error states, logic flows, and system statuses to identify edge cases during design rather than discovering them in development. This fundamentally improves their initial design quality and saves them hours of debugging later on.

产品设计团队还发现了 Claude Code 的一个意外用途：在设计阶段梳理错误状态、逻辑流和系统状态，从而在设计期而非开发期发现边界情况（edge case）。这从根本上提升了初始设计质量，为他们省去了日后数小时的调试。

Despite not being fluent in TypeScript, data scientists use Claude Code to build entire React applications for visualizing RL model performance. After one-shot prompting in a sandbox environment, the tool writes entire TypeScript visualizations from scratch without understanding the code themselves. Given the simplicity of the task, if the first prompt isn't sufficient, they'll make slight tweaks and try again.

尽管不精通 TypeScript，数据科学家们仍用 Claude Code 构建完整的 React 应用，来可视化强化学习（RL）模型的性能。在沙盒环境中一次提示（one-shot prompting）后，工具就能从零写出完整的 TypeScript 可视化，而他们自己并不需要看懂这些代码。鉴于任务本身不复杂，如果第一条提示词不够用，他们就稍作调整再试一次。

## 文档与知识管理（Documentation and knowledge management）

Technical documentation often sits scattered across wikis, code comments, and team members' heads. Claude Code consolidates this knowledge via MCP and CLAUDE.md files into accessible formats, making expertise available to everyone who needs it.

技术文档常常散落在 wiki、代码注释和团队成员的脑子里。Claude Code 通过 MCP 和 CLAUDE.md 文件把这些知识整合成便于获取的形式，让每个需要的人都能用到这些专业知识。

Inference team members without ML backgrounds depend on Claude to explain model-specific functions. What normally requires an hour of Google searching now takes 10-20 minutes-an 80% reduction in research time.

推理团队中没有机器学习（ML）背景的成员依靠 Claude 来解释模型相关的函数。过去需要一小时 Google 检索的问题，现在只需 10-20 分钟--研究时间减少了 80%。

The Security Engineering team has Claude ingest multiple documentation sources to create markdown runbooks and troubleshooting guides. These condensed documents become context for debugging real production issues, which is often more efficient than searching through full knowledge bases.

安全工程团队让 Claude 消化多个文档来源，生成 markdown 操作手册（runbook）和排障指南。这些精炼的文档成为调试真实生产问题的上下文，往往比翻查完整知识库更高效。

## 自动化与工作流优化（Automation and workflow optimization）

Agentic coding tools help teams build custom automation that would traditionally require dedicated developer resources or expensive software.

智能体编码工具帮助团队构建自定义自动化，而这些过去需要专职开发资源或昂贵的软件。

The Growth Marketing team built an agentic workflow that processes CSV files with hundreds of ads, identifies underperformers, and generates new variations within strict character limits. Using two specialized sub-agents, the system generates hundreds of new ads in minutes instead of hours.

增长营销团队构建了一个智能体工作流：处理包含数百条广告的 CSV 文件，识别表现不佳者，并在严格的字符限制内生成新变体。借助两个专用 sub-agent，该系统在几分钟（而非几小时）内就能生成数百条新广告。

They also developed a Figma plugin that identifies frames and programmatically generates up to 100 ad variations by swapping headlines and descriptions, reducing hours of copy-pasting to half a second per batch of ads.

他们还开发了一个 Figma 插件，能识别画板（frame）并通过替换标题和描述，以程序方式生成多达 100 个广告变体，把每批广告数小时的复制粘贴工作缩减到半秒。

In a particularly unique use case, the Legal team created prototype "phone tree" systems to help team members connect with the right lawyer at Anthropic, demonstrating how departments can build custom tools without traditional development resources.

在一个相当独特的用例中，法务团队创建了"电话树"（phone tree）系统原型，帮助团队成员找到 Anthropic 内部对口的律师，展示了各部门如何在没有传统开发资源的情况下构建自定义工具。

## 用 Claude Code 释放新的可能性（Unlocking new possibilities with Claude Code）

These stories reveal a pattern: Claude Code works best when you focus on the human workflows that it can augment. The most successful teams treat Claude Code as a thought partner rather than a code generator.

这些故事揭示了一个规律：当你专注于 Claude Code 能够增强的人类工作流时，它表现最好。最成功的团队把 Claude Code 当作思考伙伴（thought partner），而不是代码生成器。

They explore possibilities, prototype rapidly, and share discoveries across technical and non-technical users. This collaborative approach between humans and AI creates opportunities we're only beginning to understand.

他们探索可能性、快速做原型，并在技术与非技术用户之间分享发现。这种人机协作的方式，正在创造出我们刚刚开始理解的机会。

# 在企业中构建可信赖的 AI（Building trusted AI in the enterprise）

Anthropic's guide to starting, scaling, and succeeding based on real-world examples and best practices

Anthropic 基于真实案例与最佳实践打造的指南，助你启动、扩展并取得成功

![《Building trusted AI in the enterprise》指南配图](images/teamsuse-1.svg)

![《Building trusted AI in the enterprise》指南配图](images/teamsuse-2.svg)
