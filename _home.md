# Anthropic / Claude 双语文摘

本站收录 [li-yazhou/ai-notes](https://github.com/li-yazhou/ai-notes) 笔记库中 Anthropic 官方博客的中英对照翻译，共 56 篇：

- **Anthropic 工程博客**（engineering.antropic.com，24 篇）：Agent 工程、上下文工程、评测（evals）、工具与 harness 设计等工程方法类文章
- **Claude 产品博客**（claude.com/blog，32 篇）：Claude Code 使用方法、多智能体、Skills、hooks、工作流模式等产品实践类文章

## 阅读说明

- 排版为**英文原文在前、中文翻译紧随其后**，逐段对照；
- 术语保留英文原文并附中文释义（如：工作流（workflows））；
- 每篇开头的引用块保留原文元信息：作者、原文链接、发布日期；
- 每组第一篇「文章登记总表」是 Obsidian 登记表，含重要程度星级与未翻译篇目，站内链接（`[[...]]`）不可点击，仅作参考。

## 站点说明

- 由 [docsify](https://docsify.js.org) 驱动：直接渲染仓库中的 Markdown，无构建步骤，仓库推送后自动更新；
- 左侧为文档目录（当前文章自动展开二级标题），左侧顶部搜索框支持全文检索；
- 文中图片可点击放大。

## 文章导航

### Anthropic 工程博客（24 篇）

[文章登记总表（星级与未译篇目）](/02-agent/03-anthropic/anthropic-engineering.md)

| 发布时间 | 英文原文标题 | 中英文版本 |
| --- | --- | --- |
| 2024-09-19 | [Introducing Contextual Retrieval](https://www.anthropic.com/engineering/contextual-retrieval) | [上下文检索（Contextual Retrieval）介绍](/02-agent/03-anthropic/2409-contextual-retrieval/2409-contextual-retrieval-bilingual.md) |
| 2024-12-19 | [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents) | [构建有效的 Agent](/02-agent/03-anthropic/2412-building-effective-agents/2412-building-effective-agents-bilingual.md) |
| 2025-01-06 | [Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet](https://www.anthropic.com/engineering/swe-bench-sonnet) | [用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 基准](/02-agent/03-anthropic/2501-swe-bench-sonnet/2501-swe-bench-sonnet-bilingual.md) |
| 2025-03-20 | [The 'think' tool: Enabling Claude to stop and think in complex tool use situations](https://www.anthropic.com/engineering/claude-think-tool) | ["思考"（Think）工具：让 Claude 在复杂的工具使用场景中停下来思考](/02-agent/03-anthropic/2503-claude-think-tool/2503-claude-think-tool-bilingual.md) |
| 2025-06-13 | [How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | [我们如何构建多 Agent 研究系统](/02-agent/03-anthropic/2506-multi-agent-research-system/2506-multi-agent-research-system-bilingual.md) |
| 2025-06-26 | [Desktop Extensions: One-click MCP server installation for Claude Desktop](https://www.anthropic.com/engineering/desktop-extensions) | [桌面扩展：为 Claude Desktop 一键安装 MCP 服务器（Desktop Extensions: One-click MCP server installation for Claude Desktop）](/02-agent/03-anthropic/2506-desktop-extensions/2506-desktop-extensions-bilingual.md) |
| 2025-09-11 | [Writing effective tools for agents — with agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | [为 Agent 编写高效工具——与 Agent 协作（Writing effective tools for agents — with agents）](/02-agent/03-anthropic/2509-writing-tools-for-agents/2509-writing-tools-for-agents-bilingual.md) |
| 2025-09-17 | [A postmortem of three recent issues](https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues) | [三起近期问题的复盘（A postmortem of three recent issues）](/02-agent/03-anthropic/2509-postmortem-three-issues/2509-postmortem-three-issues-bilingual.md) |
| 2025-09-29 | [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | [面向 AI Agent 的有效上下文工程](/02-agent/03-anthropic/2509-effective-context-engineering/2509-effective-context-engineering-bilingual.md) |
| 2025-10-16 | [Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | [用 Agent Skills 为真实世界装备 Agent](/02-agent/03-anthropic/2510-agent-skills/2510-agent-skills-bilingual.md) |
| 2025-10-20 | [Beyond permission prompts: making Claude Code more secure and autonomous](https://www.anthropic.com/engineering/claude-code-sandboxing) | [超越权限提示：让 Claude Code 更安全、更自主](/02-agent/03-anthropic/2510-claude-code-sandboxing/2510-claude-code-sandboxing-bilingual.md) |
| 2025-11-04 | [Code execution with MCP: Building more efficient agents](https://www.anthropic.com/engineering/code-execution-with-mcp) | [MCP 代码执行：构建更高效的 Agent](/02-agent/03-anthropic/2511-code-execution-with-mcp/2511-code-execution-with-mcp-bilingual.md) |
| 2025-11-24 | [Introducing advanced tool use on the Claude Developer Platform](https://www.anthropic.com/engineering/advanced-tool-use) | [在 Claude 开发者平台上推出高级工具使用](/02-agent/03-anthropic/2511-advanced-tool-use/2511-advanced-tool-use-bilingual.md) |
| 2025-11-26 | [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | [长时运行 Agent 的高效 harness（运行框架）](/02-agent/03-anthropic/2511-effective-harnesses-for-long-running-agents/2511-effective-harnesses-for-long-running-agents-bilingual.md) |
| 2026-01-09 | [Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | [揭开 AI Agent 评测（Evals）的神秘面纱](/02-agent/03-anthropic/2601-demystifying-evals-for-ai-agents/2601-demystifying-evals-for-ai-agents-bilingual.md) |
| 2026-01-21 | [Designing AI-resistant technical evaluations](https://www.anthropic.com/engineering/AI-resistant-technical-evaluations) | [设计抗 AI 的技术评测](/02-agent/03-anthropic/2601-designing-ai-resistant-technical-evaluations/2601-designing-ai-resistant-technical-evaluations-bilingual.md) |
| 2026-02-05 | [Building a C compiler with a team of parallel Claudes](https://www.anthropic.com/engineering/building-c-compiler) | [用一队并行的 Claude 构建 C 编译器](/02-agent/03-anthropic/2602-building-c-compiler/2602-building-c-compiler-bilingual.md) |
| 2026-02-05 | [Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | [量化 Agent 编码评测中的基础设施噪声](/02-agent/03-anthropic/2602-quantifying-infrastructure-noise/2602-quantifying-infrastructure-noise-bilingual.md) |
| 2026-03-06 | [Eval awareness in Claude Opus 4.6's BrowseComp performance](https://www.anthropic.com/engineering/eval-awareness-browsecomp) | [Claude Opus 4.6 在 BrowseComp 表现中的评测意识（Eval Awareness）](/02-agent/03-anthropic/2603-eval-awareness-browsecomp/2603-eval-awareness-browsecomp-bilingual.md) |
| 2026-03-24 | [Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | [面向长时运行应用开发的 Harness 设计](/02-agent/03-anthropic/2603-harness-design-long-running-apps/2603-harness-design-long-running-apps-bilingual.md) |
| 2026-03-25 | [How we built Claude Code auto mode: a safer way to skip permissions](https://www.anthropic.com/engineering/claude-code-auto-mode) | [我们如何构建 Claude Code 自动模式：一种更安全的跳过权限审批的方式](/02-agent/03-anthropic/2603-claude-code-auto-mode/2603-claude-code-auto-mode-bilingual.md) |
| 2026-04-08 | [Scaling Managed Agents: Decoupling the brain from the hands](https://www.anthropic.com/engineering/managed-agents) | [扩展托管 Agent：将大脑与双手解耦](/02-agent/03-anthropic/2604-scaling-managed-agents/2604-scaling-managed-agents-bilingual.md) |
| 2026-04-23 | [An update on recent Claude Code quality reports](https://www.anthropic.com/engineering/april-23-postmortem) | [关于近期 Claude Code 质量问题报告的更新](/02-agent/03-anthropic/2604-april-23-postmortem/2604-april-23-postmortem-bilingual.md) |
| 2026-05-25 | [How we contain Claude across products](https://www.anthropic.com/engineering/how-we-contain-claude) | [我们如何在各个产品中收容 Claude](/02-agent/03-anthropic/2605-how-we-contain-claude/2605-how-we-contain-claude-bilingual.md) |

### Claude 产品博客（32 篇）

[文章登记总表（星级与未译篇目）](/02-agent/04-claude/claude-blog.md)

| 发布时间 | 英文原文标题 | 中英文版本 |
| --- | --- | --- |
| 2025-07-24 | [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code) | [Anthropic 各团队如何使用 Claude Code](/02-agent/04-claude/2507-how-anthropic-teams-use-claude-code/2507-how-anthropic-teams-use-claude-code-bilingual.md) |
| 2025-10-15 | [How to scale agentic coding across your engineering organization](https://claude.com/blog/scaling-agentic-coding) | [如何在工程组织中规模化推广 agentic coding](/02-agent/04-claude/2510-scaling-agentic-coding/2510-scaling-agentic-coding-bilingual.md) |
| 2025-11-25 | [Using CLAUDE.md files: Customizing Claude Code for your codebase](https://claude.com/blog/using-claude-md-files) | [使用 CLAUDE.md 文件：为你的代码库定制 Claude Code](/02-agent/04-claude/2511-using-claude-md-files/2511-using-claude-md-files-bilingual.md) |
| 2025-12-11 | [Claude Code power user customization: How to configure hooks](https://claude.com/blog/how-to-configure-hooks) | [Claude Code 高级用户自定义：如何配置 hooks](/02-agent/04-claude/2512-how-to-configure-hooks/2512-how-to-configure-hooks-bilingual.md) |
| 2026-01-22 | [Building agents with Skills: Equipping agents for specialized work](https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work) | [用 Skills 构建智能体：让智能体胜任专业化工作](/02-agent/04-claude/2601-building-agents-with-skills/2601-building-agents-with-skills-bilingual.md) |
| 2026-01-23 | [Building multi-agent systems: When and how to use them](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) | [构建多智能体系统：何时使用与如何使用](/02-agent/04-claude/2601-building-multi-agent-systems/2601-building-multi-agent-systems-bilingual.md) |
| 2026-03-05 | [Common workflow patterns for AI agents-and when to use them](https://claude.com/blog/common-workflow-patterns-for-ai-agents-and-when-to-use-them) | [常见的 AI 智能体工作流模式及其使用时机](/02-agent/04-claude/2603-common-workflow-patterns/2603-common-workflow-patterns-bilingual.md) |
| 2026-03-05 | [Skills explained: How Skills compares to prompts, Projects, MCP, and subagents](https://claude.com/blog/skills-explained) | [Skills 详解：Skills 与提示词、Projects、MCP 和 subagents 的对比](/02-agent/04-claude/2603-skills-explained/2603-skills-explained-bilingual.md) |
| 2026-03-24 | [Auto mode for Claude Code](https://claude.com/blog/auto-mode) | [Claude Code 的 Auto 模式](/02-agent/04-claude/2603-auto-mode/2603-auto-mode-bilingual.md) |
| 2026-04-02 | [Agent Harness Design: 3 Patterns for Harnessing Claude's Intelligence](https://claude.com/blog/harnessing-claudes-intelligence) | [Agent Harness 设计：驾驭 Claude 智能的三种模式](/02-agent/04-claude/2604-harnessing-claudes-intelligence/2604-harnessing-claudes-intelligence-bilingual.md) |
| 2026-04-07 | [How and when to use subagents in Claude Code](https://claude.com/blog/subagents-in-claude-code) | [如何以及何时在 Claude Code 中使用 subagents](/02-agent/04-claude/2604-subagents-in-claude-code/2604-subagents-in-claude-code-bilingual.md) |
| 2026-04-09 | [The advisor strategy: Give agents an intelligence boost](https://claude.com/blog/the-advisor-strategy) | [顾问策略：给智能体一次智力升级](/02-agent/04-claude/2604-the-advisor-strategy/2604-the-advisor-strategy-bilingual.md) |
| 2026-04-10 | [Multi-agent coordination patterns: Five approaches and when to use them](https://claude.com/blog/multi-agent-coordination-patterns) | [多智能体协调模式：五种方法及其适用场景](/02-agent/04-claude/2604-multi-agent-coordination-patterns/2604-multi-agent-coordination-patterns-bilingual.md) |
| 2026-04-10 | [Seeing like an agent: how we design tools in Claude Code](https://claude.com/blog/seeing-like-an-agent) | [像 Agent 一样看世界：我们如何在 Claude Code 中设计工具](/02-agent/04-claude/2604-seeing-like-an-agent/2604-seeing-like-an-agent-bilingual.md) |
| 2026-04-14 | [Redesigning Claude Code on desktop for parallel agents](https://claude.com/blog/claude-code-desktop-redesign) | [为并行 agent 重新设计桌面端 Claude Code](/02-agent/04-claude/2604-claude-code-desktop-redesign/2604-claude-code-desktop-redesign-bilingual.md) |
| 2026-04-15 | [Using Claude Code: session management and 1M context](https://claude.com/blog/using-claude-code-session-management-and-1m-context) | [Using Claude Code：会话管理与 1M 上下文](/02-agent/04-claude/2604-session-management-1m-context/2604-session-management-1m-context-bilingual.md) |
| 2026-04-22 | [Building agents that reach production systems with MCP](https://claude.com/blog/building-agents-that-reach-production-systems-with-mcp) | [构建可通过 MCP 触达生产系统的智能体](/02-agent/04-claude/2604-agents-reach-production-mcp/2604-agents-reach-production-mcp-bilingual.md) |
| 2026-04-28 | [Onboarding Claude Code like a new developer: Lessons from 17 years of development](https://claude.com/blog/onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development) | [像对待新开发者一样让 Claude Code 入职：来自 17 年开发的经验](/02-agent/04-claude/2604-onboarding-claude-code/2604-onboarding-claude-code-bilingual.md) |
| 2026-04-30 | [Lessons from building Claude Code: Prompt caching is everything](https://claude.com/blog/lessons-from-building-claude-code-prompt-caching-is-everything) | [构建 Claude Code 的经验：提示缓存就是一切](/02-agent/04-claude/2604-lessons-claude-code-prompt-caching/2604-lessons-claude-code-prompt-caching-bilingual.md) |
| 2026-05-13 | [Best practices for computer and browser use with Claude](https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude) | [Claude 计算机与浏览器使用最佳实践](/02-agent/04-claude/2605-computer-browser-use/2605-computer-browser-use-bilingual.md) |
| 2026-05-14 | [How Claude Code works in large codebases: Best practices and where to start](https://claude.com/blog/how-claude-code-works-in-large-codebases-best-practices-and-where-to-start) | [Claude Code 在大型代码库中如何运作：最佳实践与入手指南](/02-agent/04-claude/2605-claude-code-large-codebases/2605-claude-code-large-codebases-bilingual.md) |
| 2026-05-20 | [Using Claude Code: The unreasonable effectiveness of HTML](https://claude.com/blog/using-claude-code-the-unreasonable-effectiveness-of-html) | [Using Claude Code：HTML 出乎意料的有效性](/02-agent/04-claude/2605-unreasonable-effectiveness-html/2605-unreasonable-effectiveness-html-bilingual.md) |
| 2026-06-02 | [A harness for every task: dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) | [为每个任务打造 harness：Claude Code 中的动态工作流](/02-agent/04-claude/2606-dynamic-workflows-in-claude-code/2606-dynamic-workflows-in-claude-code-bilingual.md) |
| 2026-06-03 | [Running an AI-native engineering org](https://claude.com/blog/running-an-ai-native-engineering-org) | [运营一个 AI 原生的工程组织](/02-agent/04-claude/2606-ai-native-engineering-org/2606-ai-native-engineering-org-bilingual.md) |
| 2026-06-03 | [Lessons from building Claude Code: How we use skills](https://claude.com/blog/lessons-from-building-claude-code-how-we-use-skills) | [构建 Claude Code 的经验：我们如何使用 skills](/02-agent/04-claude/2606-lessons-claude-code-skills/2606-lessons-claude-code-skills-bilingual.md) |
| 2026-06-18 | [Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) | [驾驭 Claude Code：何时使用 CLAUDE.md、skills、hooks 与 subagents](/02-agent/04-claude/2606-steering-claude-code/2606-steering-claude-code-bilingual.md) |
| 2026-06-24 | [Building effective human-agent teams](https://claude.com/blog/building-effective-human-agent-teams) | [构建高效的人类-智能体团队](/02-agent/04-claude/2606-building-effective-human-agent-teams/2606-building-effective-human-agent-teams-bilingual.md) |
| 2026-06-30 | [Loop engineering: Getting started with loops](https://claude.com/blog/getting-started-with-loops) | [循环工程：循环入门](/02-agent/04-claude/2606-getting-started-with-loops/2606-getting-started-with-loops-bilingual.md) |
| 2026-07-16 | [How Anthropic runs large-scale code migrations with Claude Code](https://claude.com/blog/ai-code-migration) | [Anthropic 如何用 Claude Code 执行大规模代码迁移](/02-agent/04-claude/2607-ai-code-migration/2607-ai-code-migration-bilingual.md) |
| 2026-07-22 | [Building verification loops in Claude Code with skills](https://claude.com/blog/building-verification-loops-in-claude-code-with-skills) | [在 Claude Code 中用 Skills 构建验证循环](/02-agent/04-claude/2607-building-verification-loops/2607-building-verification-loops-bilingual.md) |
| 2026-07-24 | [The new rules of context engineering for Claude 5 generation models](https://claude.com/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models) | [面向 Claude 5 代模型的上下文工程新规则](/02-agent/04-claude/2607-new-rules-context-engineering/2607-new-rules-context-engineering-bilingual.md) |
| 2026-08-07 | [Running auto mode in production](https://claude.com/blog/auto-mode-in-production) | [在生产环境中运行 auto mode](/02-agent/04-claude/2608-auto-mode-in-production/2608-auto-mode-in-production-bilingual.md) |
