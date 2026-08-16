# 如何在工程组织中规模化推广 agentic coding（中英对照）

> **原文标题：** How to scale agentic coding across your engineering organization
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/scaling-agentic-coding
> **发布日期：** 2025-10-15
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

As Agentic coding tools mature, technical leaders are wrestling with a practical challenge: moving beyond isolated experiments to organization-wide adoption.

随着 agentic coding（智能体化编码）工具走向成熟，技术负责人正在为一个现实难题费尽心思：如何从零散试验走向全组织采用。

See Claude Code in action-from concept to commit in one seamless workflow.

亲眼看看 Claude Code 的实际表现--在一个无缝工作流中从概念直达提交。（原文此句作为头图视频配注重复出现三次，此处合并呈现一次。）

![Claude Code 演示配图](images/scaling-1.svg)

# 如何在工程组织中规模化推广 agentic coding（How to scale agentic coding across your engineering organization）

The difference between successful and struggling implementations often comes down to execution. Teams that deploy agentic coding thoughtfully see meaningful improvements in development velocity and engineer satisfaction. Those that rush deployment without proper planning encounter resistance, inconsistent results, and difficulty demonstrating value.

成功与挣扎的实施之间，差别往往在于执行。深思熟虑地部署 agentic coding 的团队，会在开发速度和工程师满意度上看到实质提升；而未做妥善规划就仓促上线的团队，则会遭遇阻力、结果忽好忽坏，并且难以证明价值。

Working with engineering teams across different industries has surfaced common patterns. Successful adoption depends less on the specific tool and more on how you approach workflow changes, skill development, team dynamics, and success measurement.

与不同行业工程团队的合作让我们发现了一些共同模式。能否成功采用，与其说取决于具体工具，不如说取决于你如何处理工作流变更、技能培养、团队动力学和成功度量。

Let's dive in.

让我们深入探讨。

# 理解 agentic coding 的能力（Understanding agentic coding capabilities）

Agentic coding tools differ from basic code completion by understanding broader context and handling multi-step tasks. They can plan approaches and work through implementation details with less hand-holding than earlier AI coding assistants.

Agentic coding 工具与基础代码补全的不同之处在于：它们能理解更广的上下文并处理多步骤任务。相比早期的 AI 编码助手，它们能够自主规划方案、推敲实现细节，需要的搀扶少得多。

Common applications include:

常见应用包括：

Legacy system modernization: Development teams use these tools to help migrate older codebases to current platforms. Projects that might have taken years can move faster, though they still require careful oversight and testing to preserve business logic correctly.

遗留系统现代化：开发团队用这些工具帮助把老旧代码库迁移到当前平台。原本可能耗时数年的项目可以推进得更快，但仍需谨慎监督和测试，以确保业务逻辑被正确保留。

Faster onboarding: New engineers can query codebases directly to understand architecture, dependencies, and implementation patterns. This complements traditional documentation and reduces the time before new hires contribute meaningfully.

更快上手（onboarding）：新工程师可以直接查询代码库来理解架构、依赖和实现模式。这是对传统文档的补充，能缩短新人做出实质性贡献所需的时间。

Incident response assistance: SRE and DevOps teams build agents that help diagnose and address common operational issues. While human oversight remains important for complex problems, routine incidents can often be handled with less manual intervention.

事故响应辅助：SRE 和 DevOps 团队构建 agent 来帮助诊断和处理常见运维问题。复杂问题仍需人工监督，但常规事故往往可以在更少的人工干预下得到处理。

Broader technical participation: Product managers can explore codebase constraints when writing requirements, and designers can create working prototypes from mockups. This doesn't replace engineering work but enables more informed collaboration across functions.

更广泛的技术参与：产品经理可以在撰写需求时探索代码库的约束，设计师可以从设计稿创建可运行的原型。这并不能取代工程工作，但能让跨职能协作建立在更充分的信息之上。

These represent starting points rather than exhaustive possibilities for agentic coding applications.

这些只是 agentic coding 应用的起点，而非全部可能。

# 规划你的推广路径（Planning your expansion approach）

Effective rollouts balance speed with learning. Rather than deploying to everyone at once or creating lengthy pilot phases, successful organizations build expertise incrementally while maintaining momentum.

有效的推广要在速度与学习之间取得平衡。成功的组织不会一次性铺开给所有人，也不会设置冗长的试点阶段，而是在保持势头的同时逐步积累专业经验。

## 从超级用户开始（Start with super users）

Begin with a pilot group of 20-50 developers who already use AI-assisted tools. This group serves multiple purposes: validating the technology against your codebase, identifying useful workflows, and developing the internal expertise that will help broader adoption.

先从 20-50 名已经在使用 AI 辅助工具的开发者组成试点小组开始。这个小组可以发挥多重作用：在你的代码库上验证技术、识别有用的工作流，以及培养有助于更大范围推广的内部专业力量。

Give your pilot group time to experiment with common use cases. Direct experience helps identify which customizations provide value and how well the tool integrates with your existing systems. Have them document patterns they discover-both what works and what doesn't.

给试点小组时间去实验常见用例。亲身实践有助于判断哪些定制能带来价值、工具与现有系统的集成效果如何。让他们把发现的模式记录下来--包括有效的和无效的。

Practical pilot activities include:

实用的试点活动包括：

- Creating custom slash commands for common tasks like database migrations or feature scaffolding
- Building CLAUDE.md files that capture coding standards and project-specific context
- Identifying repetitive workflows worth automating (boilerplate generation, test creation, dependency updates)
- Setting up a dedicated channel for troubleshooting and knowledge sharing
- Developing wrapper scripts for third-party tool authentication

- 为数据库迁移、功能脚手架（scaffolding）等常见任务创建自定义斜杠命令
- 构建记录编码标准和项目特定上下文的 CLAUDE.md 文件
- 识别值得自动化的重复工作流（样板代码生成、测试创建、依赖更新）
- 建立用于故障排查和知识共享的专属频道
- 为第三方工具认证编写包装脚本（wrapper script）

The pilot phase should surface both opportunities and challenges before you expand access more broadly.

试点阶段应当在更大范围开放之前，把机会与挑战都暴露出来。

## 用一场 hackathon 正式启动（Launch with a hackathon）

Rather than a phased rollout where teams wait for access, consider uniting your organization with a kickoff event. Your pilot users can share techniques and prompts they've developed while everyone experiments together.

与其采用各团队排队等待访问权限的分阶段推广，不如考虑用一场启动活动把整个组织团结起来。试点用户可以分享他们摸索出的技巧和提示词，所有人一起动手实验。

This format helps demonstrate capabilities in a low-stakes environment. Engineers who are skeptical about AI assistance often change their perspective after hands-on experience. The collaborative atmosphere also surfaces creative applications your pilot group may not have considered.

这种形式有助于在低风险环境中展示能力。对 AI 辅助持怀疑态度的工程师，往往在亲手实践后转变看法。协作氛围还能催生试点小组未曾想到的创造性用法。

Keep the event accessible and energizing-food helps with both attendance and morale.

让活动轻松易参与、令人振奋--食物对出勤率和士气都很有帮助。

## 依靠内部专业力量扩张（Scale through internal expertise）

As more people use the tools, your pilot group transitions to an advisory role. They can run workshops, create educational content, and serve as resources when others encounter challenges.

随着更多人开始使用这些工具，试点小组可以转型为顾问角色。他们可以组织工作坊、制作教学内容，并在其他人遇到挑战时提供支持。

This approach tends to work better than external training programs because internal champions understand your specific environment and can provide relevant examples from actual projects. They speak your organization's language and know your particular pain points.

这种方式往往比外部培训更有效，因为内部倡导者（champion）了解你们的具体环境，能举出真实项目中的相关例子。他们说组织的语言，清楚你们特有的痛点。

# 高效使用 CLAUDE.md 文件（Using CLAUDE.md files effectively）

CLAUDE.md files document repository conventions, environment setup, and project-specific behaviors. Their value grows when shared systematically across teams.

CLAUDE.md 文件记录仓库约定、环境配置和项目特定行为。当它们在团队间系统化共享时，价值会成倍放大。

Create project-level files: Check a CLAUDE.md file into your repository root. This ensures everyone working on the project inherits the same configuration and context automatically.

创建项目级文件：把 CLAUDE.md 文件提交到仓库根目录。这能确保所有参与项目的人自动继承相同的配置和上下文。

Treat like documentation: Update CLAUDE.md files when architectural decisions change or new patterns emerge. Include these updates in pull requests alongside code changes.

像对待文档一样维护：当架构决策变更或新模式出现时，及时更新 CLAUDE.md 文件。把这些更新随代码变更一起放进 pull request。

Include in onboarding: Make reviewing the project's CLAUDE.md file part of your developer onboarding checklist. New team members should understand both the codebase and how to use Claude Code within that context.

纳入入职流程：把审阅项目的 CLAUDE.md 文件加入开发者入职清单。新成员既要理解代码库，也要理解在该环境下如何使用 Claude Code。

Consider branch variations: For projects with significantly different patterns across branches, maintain branch-specific CLAUDE.md content that reflects each context.

考虑分支差异：对于各分支模式差异显著的项目，可维护反映各自上下文的分支专属 CLAUDE.md 内容。

A typical project-level file might cover development environment requirements, testing and code standards, key architectural patterns, and current focus areas. This creates living documentation that keeps Claude Code aligned with your evolving practices.

一个典型的项目级文件可能涵盖开发环境要求、测试与代码标准、关键架构模式和当前重点领域。这就形成了"活文档"，让 Claude Code 始终与你不断演进的实践保持一致。

# 度量影响（Measuring impact）

Pilots need clear success criteria. "How do we measure ROI?" remains a central question for driving adoption beyond early enthusiasts.

试点需要明确的成功标准。"我们如何度量 ROI（投资回报率）？"始终是能否把采用推向早期尝鲜者之外的关键问题。

Beyond lines of code written-which captures activity but not necessarily value-teams track multiple indicators:

除了代码行数--它只反映活跃度，未必反映价值--团队还会跟踪多个指标：

Sprint throughput: Teams with established DevOps practices can correlate adoption timing with changes in feature delivery speed.

迭代吞吐量（sprint throughput）：已建立 DevOps 实践的团队可以把采用时间点与功能交付速度的变化关联起来。

Task completion time: Measure how long standard tasks take before and after implementation. This granular view shows where agentic coding provides the most value.

任务完成时间：度量标准任务在实施前后的耗时。这种细粒度视图能显示 agentic coding 在哪里提供最大价值。

Migration velocity: Track time required to modernize legacy systems. Faster migrations free engineering resources for other priorities.

迁移速度：跟踪遗留系统现代化所需的时间。更快的迁移能把工程资源释放给其他优先事项。

Developer satisfaction: Survey engineers about time spent on repetitive versus creative work. Job satisfaction matters for retention and productivity.

开发者满意度：调查工程师在重复性工作与创造性工作上的时间分配。工作满意度对人才留任和生产力都很重要。

Onboarding duration: Measure how quickly new hires reach meaningful productivity. Shorter ramps reduce training costs and improve team capacity sooner.

入职周期：度量新员工多快达到有意义的生产力。更短的上手曲线能降低培训成本，更早提升团队产能。

Cross-functional efficiency: Track how often other teams need dedicated engineering support for prototyping and testing. Reduced dependencies can indicate broader technical capability.

跨职能效率：跟踪其他团队需要专职工程支持来做原型和测试的频率。依赖减少可以反映出更广泛的技术能力。

Claude Code includes Activity Metrics that track lines of code accepted, suggestion acceptance rates, daily active users and sessions, organization-wide and per-user spending, and individual developer metrics.

Claude Code 内置 Activity Metrics（活动指标），可跟踪接受的代码行数、建议接受率、日活跃用户和会话数、组织级与个人级支出，以及个体开发者指标。

Sometimes the most persuasive measure is the simplest: concrete examples of tasks that now take a fraction of the previous time. When you can point to specific, meaningful efficiency gains, the value becomes self-evident.

有时最有说服力的度量恰恰是最简单的：那些如今只需原来一小段时间的具体任务实例。当你能指出具体而实在的效率提升时，价值不言自明。

# 常见采用挑战（Common adoption challenges）

Several predictable issues emerge during agentic coding rollouts. Addressing them proactively improves outcomes:

在推广 agentic coding 的过程中，几个可预见的问题会反复出现。主动应对可以改善结果：

## 合理界定任务范围（Scope tasks appropriately）

New users sometimes give agentic tools overly broad tasks without sufficient context, leading to frustrating results. Test-driven development provides helpful structure and clear success criteria.

新用户有时会给 agentic 工具布置过于宽泛的任务，又不提供足够的上下文，结果令人沮丧。测试驱动开发（test-driven development）提供了有益的结构和明确的成功标准。

Start by writing tests that define what success looks like: required functionality, edge cases, error handling. Then implement features incrementally-just enough code to make one test pass at a time. For authentication, you might begin with basic login validation, then add password hashing, then session management.

先编写定义"成功是什么样子"的测试：必需功能、边界情况、错误处理。然后渐进式地实现功能--每次只写刚好让一个测试通过的代码。以身份认证为例，可以从基本的登录校验开始，然后加入密码哈希，再到会话管理。

Run tests after each step and review the changes before proceeding. Claude Code can help analyze test results, but wait until current functionality works before expanding scope.

每一步之后都运行测试，并在继续之前审查变更。Claude Code 可以帮助分析测试结果，但要等当前功能跑通后再扩大范围。

Add new requirements gradually by writing tests first, then implementing to pass them. This prevents scope creep and maintains quality.

逐步加入新需求：先写测试，再实现使其通过。这能防止范围蔓延（scope creep），并保持质量。

Use focused commands like "write tests for user registration" followed by "implement the registration logic to pass these tests" rather than requesting everything at once.

使用聚焦的指令，比如先"为用户注册编写测试"，再"实现注册逻辑让这些测试通过"，而不是一次性索要全部。

## 提供充分的上下文（Provide adequate context）

Vague descriptions like "this isn't working" or "the button is too big" don't give the AI enough information to help effectively. Be specific:

像"这不好使"或"按钮太大了"这类模糊描述，无法给 AI 足够的信息来有效帮忙。请具体一点：

Share complete error information-full error messages, stack traces, and the specific action that triggered the issue. Copy terminal output or browser console errors directly into your session.

分享完整的错误信息--完整的报错消息、堆栈跟踪（stack trace）以及触发问题的具体操作。把终端输出或浏览器控制台错误直接复制到会话里。

Document your environment by including operating system, language versions, framework details, and relevant dependencies. The AI needs this context to provide accurate solutions.

写明你的环境，包括操作系统、语言版本、框架细节和相关依赖。AI 需要这些上下文才能给出准确的解决方案。

For UI issues, take screenshots and describe precisely what's wrong: "the login button extends 20 pixels beyond the container border on mobile screens" rather than "the button looks weird."

对于 UI 问题，截图并精确描述哪里不对："移动端屏幕上登录按钮超出容器边框 20 像素"，而不是"按钮看起来怪怪的"。

Specify expected versus actual behavior clearly: "Expected: API returns 200 status with user data. Actual: Returns 401 with 'invalid token' message."

清楚说明预期行为与实际行为："预期：API 返回 200 状态码和用户数据。实际：返回 401 和 'invalid token' 消息。"

Include relevant file contents-the specific code, configuration, or data related to your issue.

附上相关文件内容--与问题相关的具体代码、配置或数据。

## 培养高效的提示词习惯（Develop effective prompting habits）

Communicating clearly with AI tools takes practice. Many developers expect immediate mind-reading and get frustrated when results miss the mark.

与 AI 工具清晰沟通需要练习。许多开发者指望它一下子就能读心，结果不符预期便倍感挫败。

Consider if a colleague would understand your request. If not, anticipate what questions they'd have and provide that information upfront.

想一想同事能否看懂你的请求。如果不能，就预判他们会问什么，并提前把信息给足。

Structure requests with high-level goals first, then add implementation details. "Build a REST API for user management" followed by specific endpoints and requirements works better than mixing everything together.

组织请求时先说高层目标，再补充实现细节。"构建一个用户管理的 REST API"，随后列出具体端点和需求，比把所有内容混在一起效果更好。

Use specific technical language instead of vague terms. "Optimize the database query to reduce response time from 2 seconds to under 500ms" beats "make it faster."

用具体的技术语言代替模糊说法。"优化这条数据库查询，把响应时间从 2 秒降到 500 毫秒以内"胜过"让它快一点"。

Show what success looks like with concrete examples. "Follow this existing API pattern [paste code]" or "Use this coding style [share guide]" provides clearer direction than abstract requirements.

用具体示例展示成功的样子。"遵循这个既有的 API 模式[粘贴代码]"或"采用这种代码风格[分享指南]"比抽象需求提供了更清晰的方向。

Break complex work into sequential prompts: "Create the database schema," then "implement product catalog API," then "add shopping cart functionality." Each command should focus on one clear objective.

把复杂工作拆成顺序化的提示词："创建数据库 schema"，然后"实现商品目录 API"，再"添加购物车功能"。每条指令只聚焦一个明确目标。

Start simple and refine iteratively. "Create a basic user login form" followed by "add input validation" then "implement password strength requirements" tends to work better than specifying everything at once.

从简单开始，迭代打磨。"创建一个基础的用户登录表单"，接着"添加输入校验"，然后"实现密码强度要求"，往往比一次性把所有要求说完效果更好。

Give specific feedback on output. "The error handling is too generic-add specific validation for email format and password length" guides improvement better than "fix the validation."

对输出给出具体反馈。"错误处理太笼统了--为邮箱格式和密码长度添加专门校验"比"修一下校验"更能引导改进。

Reference previous work explicitly when building on earlier steps: "Using the authentication middleware from earlier, now add role-based permissions."

在先前步骤的基础上继续时，明确引用之前的工作："使用之前那个身份认证中间件，现在添加基于角色的权限。"

# 展望前路（Moving forward）

Agentic coding shifts software development from writing every line to guiding implementation. Organizations that see good results focus on building foundations rather than rushing deployment.

Agentic coding 把软件开发从逐行编写转变为引导实现。取得良好结果的组织，把重心放在打好基础上，而不是仓促上线。

Start with a focused pilot group. Develop internal expertise. Build the infrastructure that supports success. Then expand deliberately through events like hackathons and internal champions.

从一个聚焦的试点小组起步。培养内部专业力量。搭建支撑成功的基础设施。然后借助 hackathon 和内部倡导者稳步扩张。

The path from pilot to production requires patience and systematic planning. Organizations that invest in this foundation tend to see meaningful returns: faster development, higher engineer satisfaction, and capacity to tackle previously difficult projects.

从试点到生产的道路需要耐心和系统性规划。在这份基础上投入的组织，往往能获得可观的回报：更快的开发速度、更高的工程师满意度，以及攻克过去望而却步的项目的能力。
