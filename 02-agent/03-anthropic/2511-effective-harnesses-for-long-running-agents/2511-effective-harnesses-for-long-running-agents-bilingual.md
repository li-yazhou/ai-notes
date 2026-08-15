# 长时运行 Agent 的高效 harness（运行框架）（中英对照）

> **原文标题：** Effective harnesses for long-running agents
> **作者：** Justin Young（Anthropic 工程团队）
> **原文链接：** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
> **发布日期：** 2025-11-26
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

As AI agents become more capable, developers are increasingly asking them to take on complex tasks requiring work that spans hours, or even days. However, getting agents to make consistent progress across multiple context windows remains an open problem.

随着 AI Agent 的能力越来越强，开发者越来越多地要求它们承担需要持续数小时甚至数天的复杂任务。然而，让 Agent 在多个上下文窗口（context window）之间保持持续推进，仍然是一个悬而未决的问题。

The core challenge of long-running agents is that they must work in discrete sessions, and each new session begins with no memory of what came before. Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift. Because context windows are limited, and because most complex projects cannot be completed within a single window, agents need a way to bridge the gap between coding sessions.

长时运行 Agent 的核心挑战在于，它们必须在离散的会话（session）中工作，而每个新会话开始时，都没有对之前所发生事情的记忆。想象一个由轮班工程师参与的软件项目，每位新来的工程师都不记得上一个班次发生了什么。由于上下文窗口是有限的，而且大多数复杂项目无法在单个窗口内完成，Agent 需要一种方法来弥合编码会话之间的鸿沟。

We developed a two-fold solution to enable the [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) to work effectively across many context windows: an **initializer agent** that sets up the environment on the first run, and a **coding agent** that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session. You can find code examples in the accompanying [quickstart.](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)

为了让 [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) 能够在多个上下文窗口中高效工作，我们开发了一个两部分的解决方案：一个**初始化 Agent**（initializer agent），负责在首次运行时搭建环境；以及一个**编码 Agent**（coding agent），负责在每个会话中取得增量进展，同时为下一个会话留下清晰的产物（artifact）。你可以在随附的 [quickstart（快速入门）](https://github.com/anthropics/claude-quickstarts/tree/main/autonomous-coding)中找到代码示例。

# 长时运行 Agent 的问题（The long-running agent problem）

The Claude Agent SDK is a powerful, general-purpose agent harness adept at coding, as well as other tasks that require the model to use tools to gather context, plan, and execute. It has context management capabilities such as compaction, which enables an agent to work on a task without exhausting the context window. Theoretically, given this setup, it should be possible for an agent to continue to do useful work for an arbitrarily long time.

Claude Agent SDK 是一个强大、通用的 Agent 运行框架（harness），擅长编码，以及需要模型使用工具来收集上下文、规划和执行的其他任务。它具备上下文管理能力，例如压缩（compaction），这使 Agent 能够在不会耗尽上下文窗口的情况下处理任务。理论上，有了这样的设置，Agent 应该可以无限期地继续做有用的工作。

However, compaction isn't sufficient. Out of the box, even a frontier coding model like Opus 4.5 running on the Claude Agent SDK in a loop across multiple context windows will fall short of building a production-quality web app if it's only given a high-level prompt, such as "build a clone of [claude.ai](http://claude.ai/redirect/website.v1.d7825df1-f933-46b7-ad28-2d134bbad322)."

然而，仅有压缩（compaction）是不够的。开箱即用的情况下，即使是 Opus 4.5 这样的前沿编码模型，在 Claude Agent SDK 上跨多个上下文窗口循环运行，如果只给一个高层级的提示词，例如"构建一个 [claude.ai](http://claude.ai/redirect/website.v1.d7825df1-f933-46b7-ad28-2d134bbad322) 的克隆版"，也无法构建出一个达到生产质量的 Web 应用。

Claude's failures manifested in two patterns. First, the agent tended to try to do too much at once—essentially to attempt to one-shot the app. Often, this led to the model running out of context in the middle of its implementation, leaving the next session to start with a feature half-implemented and undocumented. The agent would then have to guess at what had happened, and spend substantial time trying to get the basic app working again. This happens even with compaction, which doesn't always pass perfectly clear instructions to the next agent.

Claude 的失败表现为两种模式。首先，Agent 往往试图一次做太多事——本质上是想一次性（one-shot）完成整个应用。这常常导致模型在实现中途耗尽上下文，让下一个会话从一个实现了一半、且没有文档记录的功能开始。Agent 随后不得不猜测之前发生了什么，并花费大量时间让基础应用重新工作起来。即使有压缩（compaction）也会出现这种情况，因为它并不总能向下一个 Agent 传递完全清晰的指令。

A second failure mode would often occur later in a project. After some features had already been built, a later agent instance would look around, see that progress had been made, and declare the job done.

第二种失败模式通常出现在项目后期。在已经构建了一些功能之后，后一个 Agent 实例会四处查看，发现已经取得了进展，然后就宣布工作完成了。

This decomposes the problem into two parts. First, we need to set up an initial environment that lays the foundation for *all* the features that a given prompt requires, which sets up the agent to work step-by-step and feature-by-feature. Second, we should prompt each agent to make incremental progress towards its goal while also leaving the environment in a clean state at the end of a session. By "clean state" we mean the kind of code that would be appropriate for merging to a main branch: there are no major bugs, the code is orderly and well-documented, and in general, a developer could easily begin work on a new feature without first having to clean up an unrelated mess.

这把问题分解为两个部分。首先，我们需要搭建一个初始环境，为给定提示词所要求的*所有*功能奠定基础，让 Agent 能够一步一步、一个功能一个功能地工作。其次，我们应该提示每个 Agent 朝着目标取得增量进展，同时在会话结束时让环境保持干净状态（clean state）。所谓"干净状态"，我们指的是适合合并到 main 分支的那种代码：没有重大 bug，代码有序且文档齐全，总体而言，开发者可以轻松地开始一个新功能的工作，而无需先清理一些不相干的烂摊子。

When experimenting internally, we addressed these problems using a two-part solution:

在内部实验时，我们用由两部分组成的解决方案来处理这些问题：

1. Initializer agent: The very first agent session uses a specialized prompt that asks the model to set up the initial environment: an `init.sh` script, a claude-progress.txt file that keeps a log of what agents have done, and an initial git commit that shows what files were added.
2. 初始化 Agent（Initializer agent）：第一个 Agent 会话使用一个专门的提示词，要求模型搭建初始环境：一个 `init.sh` 脚本、一个记录 Agent 已做工作的 claude-progress.txt 文件，以及一个显示添加了哪些文件的初始 git 提交。
3. Coding agent: Every subsequent session asks the model to make incremental progress, then leave structured updates.1
4. 编码 Agent（Coding agent）：此后的每个会话都要求模型取得增量进展，然后留下结构化的更新记录。1

The key insight here was finding a way for agents to quickly understand the state of work when starting with a fresh context window, which is accomplished with the claude-progress.txt file alongside the git history. Inspiration for these practices came from knowing what effective software engineers do every day.

这里的关键洞察，是找到一种方法让 Agent 在从一个全新的上下文窗口开始时，能快速理解工作的状态——这通过 claude-progress.txt 文件配合 git 历史记录来实现。这些做法的灵感，来自对高效软件工程师日常工作方式的了解。

# 环境管理（Environment management）

In the updated [Claude 4 prompting guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#multi-context-window-workflows), we shared some best practices for multi-context window workflows, including a harness structure that uses "a different prompt for the very first context window." This "different prompt" requests that the initializer agent set up the environment with all the necessary context that future coding agents will need to work effectively. Here, we provide a deeper dive on some of the key components of such an environment.

在更新后的 [Claude 4 提示词指南](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices#multi-context-window-workflows)中，我们分享了一些多上下文窗口工作流的最佳实践，包括一种使用"为第一个上下文窗口准备的不同提示词"的 harness 结构。这个"不同的提示词"要求初始化 Agent 搭建一个环境，其中包含未来编码 Agent 高效工作所需的全部必要上下文。在这里，我们对这类环境的一些关键组成部分做更深入的剖析。

## 功能清单（Feature list）

To address the problem of the agent one-shotting an app or prematurely considering the project complete, we prompted the initializer agent to write a comprehensive file of feature requirements expanding on the user's initial prompt. In the [claude.ai](http://claude.ai/redirect/website.v1.d7825df1-f933-46b7-ad28-2d134bbad322) clone example, this meant over 200 features, such as "a user can open a new chat, type in a query, press enter, and see an AI response." These features were all initially marked as "failing" so that later coding agents would have a clear outline of what full functionality looked like.

为了解决 Agent 一次性（one-shot）完成应用或过早认为项目已完成的问题，我们提示初始化 Agent 编写一份详尽的功能需求文件，对用户的初始提示词进行扩展。在 [claude.ai](http://claude.ai/redirect/website.v1.d7825df1-f933-46b7-ad28-2d134bbad322) 克隆版这个例子中，这意味着 200 多个功能，例如"用户可以打开一个新的聊天，输入查询，按回车，然后看到 AI 的回应"。所有这些功能最初都被标记为"失败"（failing），以便后续的编码 Agent 对完整功能是什么样有一个清晰的轮廓。下面是一个功能项的 JSON 示例：

```json
{
    "category": "functional",
    "description": "New chat button creates a fresh conversation",
    "steps": [
      "Navigate to main interface",
      "Click the 'New Chat' button",
      "Verify a new conversation is created",
      "Check that chat area shows welcome state",
      "Verify conversation appears in sidebar"
    ],
    "passes": false
  }
```

We prompt coding agents to edit this file only by changing the status of a passes field, and we use strongly-worded instructions like "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality." After some experimentation, we landed on using JSON for this, as the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files.

我们提示编码 Agent 只能通过更改 passes 字段的状态来编辑这个文件，并使用措辞强硬的指令，例如"删除或编辑测试是不可接受的，因为这可能导致功能缺失或出现 bug"。经过一些实验后，我们决定为此使用 JSON，因为与 Markdown 文件相比，模型不太可能不当地修改或覆盖 JSON 文件。

## 增量进展（Incremental progress）

Given this initial environment scaffolding, the next iteration of the coding agent was then asked to work on only one feature at a time. This incremental approach turned out to be critical to addressing the agent's tendency to do too much at once.

有了这个初始环境的脚手架（scaffolding）之后，下一版的编码 Agent 被要求一次只处理一个功能。事实证明，这种增量方法对于解决 Agent 一次做太多事的倾向至关重要。

Once working incrementally, it's still essential that the model leaves the environment in a clean state after making a code change. In our experiments, we found that the best way to elicit this behavior was to ask the model to commit its progress to git with descriptive commit messages and to write summaries of its progress in a progress file. This allowed the model to use git to revert bad code changes and recover working states of the code base.

在增量工作的情况下，模型在做出代码更改后让环境保持干净状态仍然至关重要。在我们的实验中，我们发现引出这种行为的最佳方式，是要求模型用描述性的提交信息把进展提交到 git，并在一个进度文件中写下进展摘要。这让模型能够用 git 回退糟糕的代码更改，并恢复代码库可工作的状态。

These approaches also increased efficiency, as they eliminated the need for an agent to have to guess at what had happened and spend its time trying to get the basic app working again.

这些方法还提高了效率，因为它们消除了 Agent 猜测之前发生了什么、并把时间花在让基础应用重新工作上的需要。

## 测试（Testing）

One final major failure mode that we observed was Claude's tendency to mark a feature as complete without proper testing. Absent explicit prompting, Claude tended to make code changes, and even do testing with unit tests or `curl` commands against a development server, but would fail recognize that the feature didn't work end-to-end.

我们观察到的最后一个主要失败模式，是 Claude 倾向于在没有适当测试的情况下就把功能标记为完成。在没有明确提示的情况下，Claude 倾向于做出代码更改，甚至用单元测试或针对开发服务器的 `curl` 命令进行测试，但无法识别该功能并没有端到端地工作。

In the case of building a web app, Claude mostly did well at verifying features end-to-end once explicitly prompted to use browser automation tools and do all testing as a human user would.

在构建 Web 应用的情况下，一旦明确提示 Claude 使用浏览器自动化工具、并像人类用户那样进行所有测试，它在端到端验证功能方面大多表现良好。

![Claude 在测试 claude.ai 克隆版时，通过 Puppeteer MCP 服务器截取的屏幕截图](images/harness-1.gif)

> Screenshots taken by Claude through the Puppeteer MCP server as it tested the claude.ai clone.
> Claude 在测试 claude.ai 克隆版时，通过 Puppeteer MCP 服务器截取的屏幕截图。

Providing Claude with these kinds of testing tools dramatically improved performance, as the agent was able to identify and fix bugs that weren't obvious from the code alone.

为 Claude 提供这类测试工具极大地改善了性能，因为 Agent 能够识别并修复仅从代码中看不出来的 bug。

Some issues remain, like limitations to Claude's vision and to browser automation tools making it difficult to identify every kind of bug. For example, Claude can't see browser-native alert modals through the Puppeteer MCP, and features relying on these modals tended to be buggier as a result.

一些问题仍然存在，例如 Claude 视觉能力和浏览器自动化工具的局限，使其难以识别每一种 bug。例如，Claude 无法通过 Puppeteer MCP 看到浏览器原生的 alert 弹窗，因此依赖这些弹窗的功能往往 bug 更多。

# 快速进入状态（Getting up to speed）

With all of the above in place, every coding agent is prompted to run through a series of steps to get its bearings, some quite basic but still helpful:

在上述一切就绪之后，每个编码 Agent 都被提示要经历一系列步骤来找到方向（get its bearings），其中一些相当基础但仍有帮助：

1. *Run `pwd` to see the directory you're working in. You'll only be able to edit files in this directory.*
2. *运行 `pwd`，查看你所在的目录。你只能编辑这个目录中的文件。*
3. *Read the git logs and progress files to get up to speed on what was recently worked on.*
4. *阅读 git 日志和进度文件，快速了解最近做了什么工作。*
5. *Read the features list file and choose the highest-priority feature that's not yet done to work on.*
6. *阅读功能清单文件，选择一个尚未完成、优先级最高的功能开始处理。*

This approach saves Claude some tokens in every session since it doesn't have to figure out how to test the code. It also helps to ask the initializer agent to write an init.sh script that can run the development server, and then run through a basic end-to-end test before implementing a new feature.

这种方法在每个会话中都为 Claude 节省了一些 token，因为它不必自己琢磨如何测试代码。让初始化 Agent 编写一个能够运行开发服务器的 init.sh 脚本，然后在实现新功能之前先跑一遍基本的端到端测试，也很有帮助。

In the case of the claude.ai clone, this meant that the agent always started the local development server and used the Puppeteer MCP to start a new chat, send a message, and receive a response. This ensured that Claude could quickly identify if the app had been left in a broken state, and immediately fix any existing bugs. If the agent had instead started implementing a new feature, it would likely make the problem worse.

在 claude.ai 克隆版这个例子中，这意味着 Agent 总是先启动本地开发服务器，并使用 Puppeteer MCP 开启一个新的聊天、发送一条消息、接收一个回应。这确保了 Claude 能够快速识别应用是否处于损坏状态，并立即修复任何现有 bug。如果 Agent 转而直接开始实现新功能，它很可能会让问题变得更糟。

Given all this, a typical session starts off with the following assistant messages:

考虑到所有这些，一个典型的会话会以以下助手消息开始：

```text
[Assistant] I'll start by getting my bearings and understanding the current state of the project.
[Tool Use] <bash - pwd>
[Tool Use] <read - claude-progress.txt>
[Tool Use] <read - feature_list.json>
[Assistant] Let me check the git log to see recent work.
[Tool Use] <bash - git log --oneline -20>
[Assistant] Now let me check if there's an init.sh script to restart the servers.
<Starts the development server>
[Assistant] Excellent! Now let me navigate to the application and verify that some fundamental features are still working.
<Tests basic functionality>
[Assistant] Based on my verification testing, I can see that the fundamental functionality is working well. The core chat features, theme switching, conversation loading, and error handling are all functioning correctly. Now let me review the tests.json file more comprehensively to understand what needs to be implemented next.
<Starts work on a new feature>
```

# Agent 失败模式与解决方案（Agent failure modes and solutions）

| **Problem**（问题） | **Initializer Agent Behavior**（初始化 Agent 行为） | **Coding Agent Behavior**（编码 Agent 行为） |
| --- | --- | --- |
| Claude declares victory on the entire project too early. | Set up a feature list file: based on the input spec, set up a structured JSON file with a list of end-to-end feature descriptions. | Read the feature list file at the beginning of a session. Choose a single feature to start working on. |
| Claude leaves the environment in a state with bugs or undocumented progress. | An initial git repo and progress notes file is written. | Start the session by reading the progress notes file and git commit logs, and run a basic test on the development server to catch any undocumented bugs. End the session by writing a git commit and progress update. |
| Claude marks features as done prematurely. | Set up a feature list file. | Self-verify all features. Only mark features as "passing" after careful testing. |
| Claude has to spend time figuring out how to run the app. | Write an `init.sh` script that can run the development server. | Start the session by reading `init.sh`. |

# 未来工作（Future work）

This research demonstrates one possible set of solutions in a long-running agent harness to enable the model to make incremental progress across many context windows. However, there remain open questions.

这项研究展示了在长时运行 Agent 的 harness（运行框架）中，让模型能够在多个上下文窗口中取得增量进展的一组可行解决方案。然而，仍有一些悬而未决的问题。

Most notably, it's still unclear whether a single, general-purpose coding agent performs best across contexts, or if better performance can be achieved through a multi-agent architecture. It seems reasonable that specialized agents like a testing agent, a quality assurance agent, or a code cleanup agent, could do an even better job at sub-tasks across the software development lifecycle.

最值得注意的是，目前仍不清楚是单个通用的编码 Agent 在各上下文中表现最好，还是通过多 Agent（multi-agent）架构能获得更好的性能。我们有理由认为，像测试 Agent、质量保证（QA）Agent 或代码清理 Agent 这样的专门 Agent，在软件开发生命周期的子任务上可以做得更好。

Additionally, this demo is optimized for full-stack web app development. A future direction is to generalize these findings to other fields. It's likely that some or all of these lessons can be applied to the types of long-running agentic tasks required in, for example, scientific research or financial modeling.

此外，这个演示是针对全栈 Web 应用开发优化的。未来的一个方向是把这些发现推广到其他领域。这些经验中的一部分甚至全部，很可能可以应用到例如科学研究或金融建模所需的这类长时运行 Agent 任务上。

## 致谢（Acknowledgements）

Written by Justin Young. Special thanks to David Hershey, Prithvi Rajasakeran, Jeremy Hadfield, Naia Bouscal, Michael Tingley, Jesse Mu, Jake Eaton, Marius Buleandara, Maggie Vo, Pedram Navid, Nadine Yasser, and Alex Notov for their contributions.

本文由 Justin Young 撰写。特别感谢 David Hershey、Prithvi Rajasakeran、Jeremy Hadfield、Naia Bouscal、Michael Tingley、Jesse Mu、Jake Eaton、Marius Buleandara、Maggie Vo、Pedram Navid、Nadine Yasser 和 Alex Notov 的贡献。

This work reflects the collective efforts of several teams across Anthropic who made it possible for Claude to safely do long-horizon autonomous software engineering, especially the code RL & Claude Code teams. Interested candidates who would like to contribute are welcome to apply at [anthropic.com/careers](http://anthropic.com/careers).

这项工作反映了 Anthropic 多个团队的集体努力，他们让 Claude 能够安全地从事长时间跨度的自主软件工程，尤其是 code RL（代码强化学习）团队和 Claude Code 团队。有兴趣贡献力量、希望加入的候选人，欢迎在 [anthropic.com/careers](http://anthropic.com/careers) 申请。

## 脚注（Footnotes）

1. We refer to these as separate agents in this context only because they have different initial user prompts. The system prompt, set of tools, and overall agent harness was otherwise identical.

1. 我们在这里把它们称为独立的 Agent，仅仅是因为它们有不同的初始用户提示词。除此之外，系统提示词（system prompt）、工具集和整体 Agent harness 是完全相同的。
