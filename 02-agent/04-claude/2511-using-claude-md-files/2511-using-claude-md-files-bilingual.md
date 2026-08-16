# 使用 CLAUDE.md 文件：为你的代码库定制 Claude Code（中英对照）

> **原文标题：** Using CLAUDE.md files: Customizing Claude Code for your codebase
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/using-claude-md-files
> **发布日期：** 2025-11-25
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Learn how to use CLAUDE.md files to give Claude Code persistent context about your project structure, coding standards, and workflows.

了解如何使用 CLAUDE.md 文件，为 Claude Code 提供关于项目结构、编码标准和工作流的持久上下文。

A practical guide for using CLAUDE.md files to optimize your use of Claude Code.

一份实用指南：用 CLAUDE.md 文件优化你的 Claude Code 使用体验。

If you use AI coding agents, you face the same challenge: how do you give them enough context to understand your architecture, conventions, and workflows without repeating yourself?

如果你在用 AI 编码 agent（智能体），就会面对同一个挑战：如何在不反复重复自己的前提下，给它足够的上下文来理解你的架构、约定和工作流？

The problem compounds as your codebase grows. Complex module relationships, domain-specific patterns, and team conventions don't surface easily. You end up explaining the same architectural decisions, testing requirements, and code style preferences at the start of every conversation.

随着代码库增长，问题会不断放大。复杂的模块关系、领域特定模式和团队约定并不容易浮出水面。你不得不在每次对话开始时重新解释同样的架构决策、测试要求和代码风格偏好。

CLAUDE.md files solve this by giving Claude persistent context about your project. Think of it as a configuration file that Claude automatically incorporates into every conversation, ensuring it always knows your project structure, coding standards, and preferred workflows.

CLAUDE.md 文件通过为 Claude 提供关于项目的持久上下文来解决这一问题。可以把它看作一个配置文件，Claude 会自动将其纳入每次对话，确保它始终了解你的项目结构、编码标准和工作流偏好。

In this article, we walk through how to structure your CLAUDE.md, share best practices, and tips for using them to get the most out of Claude Code.

在本文中，我们将介绍如何组织 CLAUDE.md 的结构，分享最佳实践和使用技巧，帮你把 Claude Code 的效用发挥到极致。

# 什么是 CLAUDE.md 文件？（What is a CLAUDE.md file?）

CLAUDE.md is a special configuration file that lives in your repository and provides Claude with project-specific context. You can place it in your repository root to share with your team, in parent directories for monorepo setups, or in your home folder for universal application across all projects.

CLAUDE.md 是一个存放在你仓库中的特殊配置文件，为 Claude 提供项目特定上下文。你可以把它放在仓库根目录与团队共享，放在父目录以适配 monorepo 场景，或放在主目录（home folder）使其对所有项目通用。

Here's an example CLAUDE.md that you might have in your repository:

下面是一个你可能放在仓库里的 CLAUDE.md 示例：

````markdown
# Project Context

When working with this codebase, prioritize readability over cleverness. Ask clarifying questions before making architectural changes.

## About This Project

FastAPI REST API for user authentication and profiles. Uses SQLAlchemy for database operations and Pydantic for validation.

## Key Directories

- `app/models/` - database models
- `app/api/` - route handlers
- `app/core/` - configuration and utilities

## Standards

- Type hints required on all functions
- pytest for testing (fixtures in `tests/conftest.py`)
- PEP 8 with 100 character lines

## Common Commands

```bash
uvicorn app.main:app --reload  # dev server
pytest tests/ -v               # run tests
```

## Notes

All routes use `/api/v1` prefix. JWT tokens expire after 24 hours.
````

A well-configured CLAUDE.md transforms how Claude works with your specific project. The file serves multiple purposes: providing architectural context, establishing workflows, and connecting Claude to your development tools. Each addition should solve a real problem you have encountered, not theoretical concerns about what Claude might need.

一个配置得当的 CLAUDE.md 会改变 Claude 处理你特定项目的方式。这个文件有多种用途：提供架构上下文、建立工作流、把 Claude 连接到你的开发工具。每一次添加都应该解决你实际遇到过的问题，而不是"Claude 可能需要什么"的理论担忧。

This file can document common bash commands, core utilities, code style guidelines, testing instructions, repository conventions, developer environment setup, and project-specific warnings. There is no required format. The recommendation is to keep this file concise and human-readable, treating it like documentation that both humans and Claude need to understand quickly.

这个文件可以记录常用 bash 命令、核心工具、代码风格指南、测试说明、仓库约定、开发环境配置以及项目特定的警告。它没有强制格式。建议保持文件简洁、易读，把它当作人和 Claude 都需要快速理解的文档。

Your CLAUDE.md file becomes part of Claude's system prompt. Every conversation starts with this context already loaded, eliminating the need to explain basic project information repeatedly.

你的 CLAUDE.md 文件会成为 Claude 系统提示词（system prompt）的一部分。每次对话一开始就已加载这些上下文，无需再反复解释基本项目信息。

# 用 /init 快速上手（Getting started with /init）

Creating a CLAUDE.md from scratch can feel daunting, especially in an unfamiliar codebase.

从零创建 CLAUDE.md 可能令人生畏，尤其是在不熟悉的代码库里。

The /init command automates this process by analyzing your project and generating a starter configuration.

/init 命令会分析你的项目并生成一份初始配置，把这个过程自动化。

Run /init in any Claude Code session:

在任意 Claude Code 会话中运行 /init：

```bash
cd your-project
claude
/init
```

Claude examines your codebase-reading package files, existing documentation, configuration files, and code structure-then generates a CLAUDE.md tailored to your project. The generated file typically includes build commands, test instructions, key directories, and coding conventions it detected.

Claude 会检视你的代码库--读取包文件、既有文档、配置文件和代码结构--然后生成一份为你的项目量身定制的 CLAUDE.md。生成的文件通常包含它检测到的构建命令、测试说明、关键目录和编码约定。

Think of /init as a starting point, not a finished product. The generated CLAUDE.md captures obvious patterns but may miss nuances specific to your workflow. Review what Claude produces and refine it based on your team's actual practices.

把 /init 当作起点，而不是成品。生成的 CLAUDE.md 能捕捉显见的模式，但可能遗漏你工作流的特殊细节。审查 Claude 的产出，并根据团队的实际做法加以完善。

You can also use /init on existing projects that already have a CLAUDE.md. Claude will review the current file and suggest improvements based on what it learns from exploring your codebase.

你也可以在已有 CLAUDE.md 的项目上运行 /init。Claude 会审查当前文件，并根据它探索代码库的所得提出改进建议。

After running /init, consider these next steps:

运行 /init 之后，可以考虑以下后续步骤：

- Review the generated content for accuracy
- Add workflow instructions Claude couldn't infer (branch naming conventions, deployment processes, code review requirements)
- Remove generic guidance that doesn't apply to your project
- Commit the file to version control so your team benefits

- 检查生成内容的准确性
- 补充 Claude 无法推断的工作流指令（分支命名约定、部署流程、代码评审要求）
- 删掉不适用于你项目的通用指导
- 把文件提交到版本控制，让团队受益

The /init command works well for getting oriented quickly, but the real value comes from iterating on the generated file over time. As you work with Claude Code, use the # key to add instructions you find yourself repeating-these additions accumulate into a CLAUDE.md that genuinely reflects how your team works.

/init 命令很适合快速上手，但真正的价值来自随时间推移对生成文件的持续迭代。使用 Claude Code 时，用 # 键把你发现自己在反复重复的指令记下来--这些累积起来，就会成为一份真正反映团队工作方式的 CLAUDE.md。

# 如何组织 CLAUDE.md 的结构（How to structure your CLAUDE.md）

The following sections show you how to structure content for maximum impact: navigating complex architectures, tracking progress on multi-step tasks, integrating custom tools, and preventing rework through consistent workflows.

接下来的几节展示如何组织内容以获得最大效果：浏览复杂架构、跟踪多步骤任务的进度、集成自定义工具，以及通过一致的工作流避免返工。

## 给 Claude 一张地图（Give Claude a map）

Explaining your project architecture, key libraries, and coding styles becomes tedious when you do it for every new task. You need Claude to maintain consistent context about your codebase structure without manual reinforcement.

每来一个新任务就要解释一遍项目架构、关键库和代码风格，很快就会令人厌倦。你需要 Claude 在无需人工强化的情况下，对代码库结构保持一致的认知。

Add a project summary and high-level directory structure to your CLAUDE.md. This gives Claude immediate orientation when navigating your codebase.

在 CLAUDE.md 中加入项目摘要和高层目录结构。这能让 Claude 在浏览代码库时立刻获得方向感。

A simple tree output showing key directories helps Claude understand where different components live:

一个展示关键目录的简单 tree 输出，就能帮 Claude 理解各个组件的位置：

```
main.py
├── logs
│   ├── application.log
├── modules
│   ├── cli.py
│   ├── logging_utils.py
│   ├── media_handler.py
│   ├── player.py
```

Include information about your main dependencies, architectural patterns, and any non-standard organizational choices. If you use domain-driven design, microservices, or specific frameworks, document that. Claude uses this map to make better decisions about where to find code and where to make changes.

写入你的主要依赖、架构模式以及任何非标准的组织方式。如果你使用领域驱动设计（domain-driven design）、微服务或特定框架，都记下来。Claude 会借助这张地图更好地决定去哪里找代码、在哪里做修改。

## 把 Claude 接入你的工具（Connect Claude to your tools）

Claude inherits your complete environment but needs guidance on which custom tools and scripts to use. Your team likely has specialized utilities for deployment, testing, or code generation that Claude should know about.

Claude 会继承你的完整环境，但需要有人指引它该使用哪些自定义工具和脚本。你的团队很可能有用于部署、测试或代码生成的专用工具，Claude 应当知道它们。

Document your custom tools in CLAUDE.md with usage examples. Include tool names, basic usage patterns, and when to invoke them. If your tool provides help documentation through a --help flag, mention that so Claude knows to check it. For complex tools, add examples of common invocations your team uses regularly.

在 CLAUDE.md 中记录你的自定义工具并附上用法示例。写明工具名称、基本用法模式和调用时机。如果你的工具通过 --help 参数提供帮助文档，也要提一下，好让 Claude 知道去查阅。对于复杂工具，补充团队常用的调用示例。

Claude functions as an MCP (Model Context Protocol) client, connecting to MCP servers that extend its capabilities. Configure these through project settings, global configuration, or checked-in .mcp.json files. The --mcp-debug flag helps troubleshoot connection issues when tools don't appear as expected.

Claude 可以充当 MCP（Model Context Protocol，模型上下文协议）客户端，连接扩展其能力的 MCP 服务器。你可以通过项目设置、全局配置或提交到版本库的 .mcp.json 文件来配置它们。当工具没有如期出现时，--mcp-debug 参数有助于排查连接问题。

For example, if you have a Slack MCP server configured for your organization and you need Claude to understand how to use it, include something like this in CLAUDE.md:

例如，如果你的组织配置了 Slack MCP 服务器，而你需要 Claude 理解如何使用它，可以在 CLAUDE.md 中写上类似这样的内容：

```markdown
### Slack MCP

- Posts to #dev-notifications channel only
- Use for deployment notifications and build failures
- Do not use for individual PR updates (those go through GitHub webhooks)
- Rate limited to 10 messages per hour
```

Learn more about MCP fundamentals and best practices.

了解更多 MCP 基础知识与最佳实践。

For more information on setting permissions for Claude Code, see settings.json documentation at code.claude.com.

关于为 Claude Code 设置权限的更多信息，请参阅 code.claude.com 上的 settings.json 文档。

## 定义标准工作流（Define standard workflows）

Having Claude jump straight into code changes without planning creates rework. Claude might implement a solution that misses requirements, choose the wrong architectural approach, or make changes that break existing functionality.

让 Claude 不做规划就直接改代码，会带来返工。Claude 可能实现出一个偏离需求的方案、选错架构思路，或做出破坏既有功能的修改。

You need Claude to think before acting. Define standard workflows in your CLAUDE.md that Claude should follow for different types of tasks. A solid default workflow addresses four questions before making changes:

你需要 Claude 先思考再行动。在 CLAUDE.md 中定义 Claude 处理不同类型任务时应遵循的标准工作流。一个稳妥的默认工作流会在动手修改前回答四个问题：

- Is this a question about current state that requires investigation first?
- Does this need a detailed plan before implementation?
- What additional information is missing?
- How will effectiveness be tested?

- 这是关于当前状态的问题，需要先调查吗？
- 实现之前是否需要详细计划？
- 还缺少哪些额外信息？
- 效果将如何验证？

Specific workflows might include explore-plan-code-commit for features, test-driven development for algorithmic work, or visual iteration for UI changes. Document your testing requirements, commit message format, and any approval steps. When Claude knows your workflow upfront, it structures work to match your team's actual process rather than guessing.

具体的工作流可以包括：功能开发采用 explore-plan-code-commit（探索-计划-编码-提交），算法类工作采用测试驱动开发（test-driven development），UI 修改采用视觉迭代。把你的测试要求、提交信息格式和审批环节都写清楚。当 Claude 预先知晓你的工作流，它就会按照团队的实际流程组织工作，而不是靠猜。

An example workflow instruction might be:

一条工作流指令的示例：

```
1) Before modifying code in the following locations: X, Y, Z
   - Consider how it might affect A, B, C
   - Construct an implementation plan
   - Develop a test plan that will validate the following functions...
```

# 使用 Claude Code 的更多技巧（Additional tips for working with Claude Code）

Beyond configuring your CLAUDE.md file, three additional techniques improve how you work with Claude Code.

除了配置 CLAUDE.md 文件，还有三项技巧可以改善你使用 Claude Code 的体验。

## 保持上下文新鲜（Keep context fresh）

Working with Claude Code over time accumulates irrelevant context. File contents from earlier tasks, command outputs that no longer matter, and tangential conversations fill Claude's context window. As the signal-to-noise ratio drops, Claude struggles to maintain focus on the current task.

长时间使用 Claude Code 会积累无关上下文。早期任务的文件内容、已无意义的命令输出、偏离主题的对话，都会塞满 Claude 的上下文窗口。随着信噪比下降，Claude 难以专注于当前任务。

Use /clear between distinct tasks to reset the context window. This removes accumulated history while preserving your CLAUDE.md configuration and Claude's ability to address new problems with fresh context. Think of it as closing one work session and opening another.

在不同任务之间使用 /clear 重置上下文窗口。它会清除累积的历史，同时保留你的 CLAUDE.md 配置，让 Claude 能以全新上下文处理新问题。可以把它想象成结束一个工作时段、开启另一个。

When you finish debugging authentication and switch to implementing a new API endpoint, clear the context. The authentication details no longer matter and distract from the new work.

当你调试完身份认证、转而实现新的 API 端点时，就清空上下文。认证细节已无关紧要，只会干扰新工作。

## 在不同阶段使用 subagent（Use subagents for distinct phases）

Long conversations accumulate context that interferes with new tasks. You've debugged a complex authentication flow, and now you need a security review of that same code. The debugging details color Claude's security analysis, potentially causing it to overlook issues or focus on already-resolved concerns.

漫长的对话积累的上下文会干扰新任务。你刚调试完一个复杂的认证流程，现在需要对同一段代码做安全审查。调试的细节会给 Claude 的安全分析蒙上色彩，可能让它忽视问题，或纠结于早已解决的疑点。

Tell Claude to use a subagent for distinct phases of work. Subagents maintain isolated context, preventing information from earlier tasks from interfering with new analysis. After implementing a payment processor, instruct Claude to "use a sub-agent to perform a security review of that code" rather than continuing in the same conversation.

让 Claude 在不同的工作阶段使用 subagent。subagent 维护隔离的上下文，防止早期任务的信息干扰新分析。实现完支付处理器后，指示 Claude"使用 subagent 对该代码执行安全审查"，而不是在同一对话中继续。

Subagents work best for multistep workflows where each phase requires different perspectives. Implementation needs architectural context and feature requirements; security review needs fresh eyes focused solely on vulnerabilities. Context separation keeps both analyses sharp.

subagent 最适合每个阶段需要不同视角的多步骤工作流。实现阶段需要架构上下文和功能需求；安全审查需要只盯着漏洞的全新眼光。上下文分离能让两边的分析都保持敏锐。

## 创建自定义命令（Create custom commands）

Repetitive prompts waste time. You find yourself typing "review this code for security issues" or "analyze this for performance problems" over and over. Each time you need to remember the exact phrasing that gets good results.

重复的提示词浪费时间。你会发现自己一遍遍输入"审查这段代码的安全问题"或"分析这里的性能问题"。每次都得回忆起能带来好效果的确切措辞。

Custom slash commands store these as markdown files in your .claude/commands/ directory. Create a file named performance-optimization.mm with your preferred performance optimization prompt, and it becomes available as /performance-optimization in any conversation. Commands support arguments through $ARGUMENTS or numbered placeholders like $1 and $2, letting you pass specific files or parameters.

自定义斜杠命令（slash command）以 markdown 文件的形式存放在 .claude/commands/ 目录中。创建一个名为 performance-optimization.mm 的文件，写入你偏好的性能优化提示词，它就会在任何对话中变成可用的 /performance-optimization 命令。命令通过 $ARGUMENTS 或 $1、$2 这类编号占位符支持参数，让你可以传入具体文件或参数。

For example, performance-optimization.md might look like this:

例如，performance-optimization.md 可能像这样：

````markdown
# Performance Optimization

Analyze the provided code for performance bottlenecks and optimization opportunities. Conduct a thorough review covering:

## Areas to Analyze

### Database & Data Access

- N+1 query problems and missing eager loading
- Lack of database indexes on frequently queried columns
- Inefficient joins or subqueries
- Missing pagination on large result sets
- Absence of query result caching
- Connection pooling issues

### Algorithm Efficiency

- Time complexity issues (O(n²) or worse when better exists)
- Nested loops that could be optimized
- Redundant calculations or repeated work
- Inefficient data structure choices
- Missing memoization or dynamic programming opportunities

### Memory Management

- Memory leaks or retained references
- Loading entire datasets when streaming is possible
- Excessive object instantiation in loops
- Large data structures kept in memory unnecessarily
- Missing garbage collection opportunities

### Async & Concurrency

- Blocking I/O operations that should be async
- Sequential operations that could run in parallel
- Missing Promise.all() or concurrent execution patterns
- Synchronous file operations
- Unoptimized worker thread usage

### Network & I/O

- Excessive API calls (missing request batching)
- No response caching strategy
- Large payloads without compression
- Missing CDN usage for static assets
- Lack of connection reuse

### Frontend Performance

- Render-blocking JavaScript or CSS
- Missing code splitting or lazy loading
- Unoptimized images or assets
- Excessive DOM manipulations or reflows
- Missing virtualization for long lists
- No debouncing/throttling on expensive operations

### Caching

- Missing HTTP caching headers
- No application-level caching layer
- Absence of memoization for pure functions
- Static assets without cache busting

## Output Format

For each issue identified:

1. **Issue**: Describe the performance problem
2. **Location**: Specify file/function/line numbers
3. **Impact**: Rate severity (Critical/High/Medium/Low) and explain expected performance degradation
4. **Current Complexity**: Include time/space complexity where applicable
5. **Recommendation**: Provide specific optimization strategy
6. **Code Example**: Show optimized version when possible
7. **Expected Improvement**: Quantify performance gains if measurable

If code is well-optimized:

- Confirm optimization status
- List performance best practices properly implemented
- Note any minor improvements possible

**Code to review:**

```
$ARGUMENTS
```
````

You don't need to write custom command files manually. Ask Claude to create them for you:

你不必手动编写自定义命令文件，可以让 Claude 帮你创建：

```
Create a custom slash command called /performance-optimization that analyzes code for database query issues, algorithm efficiency, memory management, and caching opportunities.
```

Claude will write the markdown file to .claude/commands/performance-optimization.md, and the command will be available immediately.

Claude 会把 markdown 文件写入 .claude/commands/performance-optimization.md，命令随即立即可用。

# 从简单开始，稳步扩展（Start simple, expand deliberately）

It's tempting to create a comprehensive CLAUDE.md right away. Resist that urge.

一上来就写一份面面俱到的 CLAUDE.md 很有诱惑力。请克制这种冲动。

CLAUDE.md is added to Claude Code's context every time, so from a context engineering and prompt engineering standpoint, keep it concise. One option: break up information into separate markdown files and reference them inside the CLAUDE.md file.

CLAUDE.md 每次都会加入 Claude Code 的上下文，所以从上下文工程（context engineering）和提示词工程（prompt engineering）的角度看，务必保持精简。一种做法是：把信息拆分到多个 markdown 文件中，再在 CLAUDE.md 文件里引用它们。

Don't include sensitive information, API keys, credentials, database connection strings, or detailed security vulnerability information-especially if you commit to version control. Since CLAUDE.md becomes part of Claude's system prompt, treat it as documentation that could be shared publicly.

不要包含敏感信息、API 密钥、凭据、数据库连接字符串或详细的安全漏洞信息--尤其是当你要提交到版本控制时。由于 CLAUDE.md 会成为 Claude 系统提示词的一部分，请把它当作可能被公开共享的文档来对待。

# 让 CLAUDE.md 为你所用（Make CLAUDE.md work for you）

CLAUDE.md files turn Claude Code from a general-purpose assistant into a tool configured specifically for your codebase. Start simple with basic project structure and build documentation, then expand based on actual friction points in your workflow.

CLAUDE.md 文件能让 Claude Code 从通用助手变成为你的代码库专门配置的工具。从基本的项目结构和构建文档起步，再根据工作流中的实际摩擦点逐步扩展。

The most effective CLAUDE.md files solve real problems: they document the commands you type repeatedly, capture the architectural context that takes ten minutes to explain, and establish workflows that prevent rework. Your file should reflect how your team actually develops software-not theoretical best practices that sound good but don't match reality.

最有效的 CLAUDE.md 解决的是真实问题：它们记录你反复敲打的命令、沉淀需要十分钟才能讲清的架构背景、建立防止返工的工作流。你的文件应当反映团队实际开发软件的方式--而不是那些听起来美好却与现实脱节的理论最佳实践。

Treat customization as an ongoing practice rather than a one-time setup task. Projects change, teams learn better patterns, and new tools enter your workflow. A well-maintained CLAUDE.md evolves with your codebase, continuously reducing the friction of working with AI assistance on complex software.

把定制当作一项持续实践，而非一次性设置任务。项目会变化，团队会学到更好的模式，新工具会进入工作流。维护良好的 CLAUDE.md 会随代码库一起演进，持续降低在复杂软件上借助 AI 协作的摩擦。

Get started with Claude Code today.

今天就上手 Claude Code 吧。
