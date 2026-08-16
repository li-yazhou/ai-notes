# 为并行 agent 重新设计桌面端 Claude Code（中英对照）

> **原文标题：** Redesigning Claude Code on desktop for parallel agents
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/claude-code-desktop-redesign
> **发布日期：** 2026-04-14
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Today, we're releasing a redesign of the Claude Code desktop app, built to help you run more Claude Code tasks at once.

今天，我们发布 Claude Code 桌面应用的重新设计版，旨在帮助你同时运行更多 Claude Code 任务。

It includes a new sidebar for managing multiple sessions, a drag-and-drop layout for arranging your workspace, an integrated terminal and file editor, plus performance and quality-of-life improvements.

它包含一个用于管理多个会话的全新侧边栏、可自由拖放排布的工作区布局、集成终端与文件编辑器，以及性能和使用体验上的改进。

# 全新桌面体验（The new desktop experience）

For many developers, the shape of agentic work has changed. You're not typing one prompt and waiting. You're kicking off a refactor in one repo, a bug fix in another, and a test-writing pass in a third, checking on each as results come in, steering when something drifts, and reviewing diffs before you ship.

对许多开发者来说，agent 式工作的形态已经改变。你不再是输入一个提示词然后干等。你在一个代码仓库里启动一次重构，在另一个仓库里修一个 bug，又在第三个仓库里跑一轮测试编写；随着结果陆续产出逐一查看进展，在方向跑偏时加以纠正，并在发布前审查 diff。

The new app is built for how agentic coding actually feels now: many things in flight, and you in the orchestrator seat.

新应用正是为如今 agent 式编程的真实体感而构建：多线任务并行推进，而你坐在编排者（orchestrator）的位置上。

# 并行运行会话（Run sessions in parallel）

The new sidebar puts every active and recent session in one place. Kick off work across multiple repos and move between them as results arrive.

全新侧边栏把所有进行中和最近的会话集中在一处。跨多个代码仓库启动工作，并在结果到达时在它们之间切换。

You can filter by status, project, or environment, or group the sidebar by project to find and resume sessions faster. When a session's PR merges or closes, it archives itself so the sidebar stays focused on what's live.

你可以按状态、项目或环境进行筛选，也可以让侧边栏按项目分组，从而更快找到并恢复会话。当某个会话的 PR 合并或关闭后，它会自动归档，让侧边栏始终聚焦于进行中的内容。

When you need to ask a question mid-task, you can open a side chat (⌘ + ; or Ctrl + ;) to branch off a conversation. Side chats pull context from the main thread, but don't add anything back to the thread, to avoid misdirecting your tasks.

当你在任务中途需要提一个问题时，可以打开侧聊（side chat，⌘ + ; 或 Ctrl + ;）来分出一段对话。侧聊会从主线程拉取上下文，但不会向主线程回写任何内容，以免带偏你的任务。

# 在应用内完成审查与发布（Review and ship without leaving the app）

The redesign brings more commonly-used tools into the app, so you can review, tweak, and ship Claude's work without bouncing to your editor:

这次改版把更多常用工具带进了应用，让你无需在编辑器之间来回跳转，就能审查、微调并发布 Claude 的工作成果：

- Integrated terminal: Run tests or builds alongside your session.
- In-app file editor: Open files, make spot edits directly, and save changes.
- Faster diff viewer: Rebuilt for performance on large changesets.
- Expanded preview: Open HTML files or PDFs in-app, in addition to running local app servers in the preview pane.

- 集成终端：在会话旁边运行测试或构建。
- 应用内文件编辑器：打开文件、直接做局部修改并保存更改。
- 更快的 diff 查看器：为大型变更集（changeset）上的性能重新构建。
- 增强的预览：除在预览面板中运行本地应用服务器外，还可在应用内打开 HTML 文件或 PDF。

Every pane is drag-and-drop. Arrange the terminal, preview, diff viewer, and chat in whatever grid matches how you work.

每个面板都支持拖放。按照最贴合你工作方式的网格布局，随意排布终端、预览、diff 查看器和聊天。

# 适配你的技术栈（Fits your stack）

The desktop app now has parity with CLI plugins. If your org manages Claude Code plugins centrally, or you've installed your own locally, they work in the desktop app exactly the way they do in your terminal.

桌面应用现在与 CLI 插件功能对等。无论你的组织是集中管理 Claude Code 插件，还是你在本地自行安装，它们在桌面应用中的运行方式与在终端中完全一致。

You can still run sessions locally or in the cloud. SSH support now extends to Mac alongside Linux, so you can point sessions at remote machines from either platform.

你仍然可以在本地或云端运行会话。SSH 支持现在在 Linux 之外也覆盖了 Mac，因此在两个平台上你都可以把会话指向远程机器。

# 按你的工作方式自定义（Customize for how you work）

Three view modes-Verbose, Normal, and Summary-let you dial the interface from full transparency into Claude's tool calls to just the results. New keyboard shortcuts cover session switching, spawning, and navigation; press ⌘ + / (or Ctrl + /) to see the full list. A new usage button shows both your context window and session usage at a glance.

三种视图模式--Verbose（详尽）、Normal（标准）和 Summary（摘要）--让你在“完整透明地展示 Claude 的工具调用”与“只看结果”之间自由调节界面。新的键盘快捷键覆盖会话切换、创建（spawn）和导航；按 ⌘ + /（或 Ctrl + /）可查看完整列表。新的用量按钮可让你一眼看到上下文窗口和会话的使用情况。

Under the hood, the app has been rebuilt for reliability and speed, and now streams responses as Claude generates them.

在底层，应用为可靠性与速度进行了重构，现在会在 Claude 生成响应的同时进行流式输出。

# 开始使用（Getting started）

The redesigned desktop app is available now for all Claude Code users on Pro, Max, Team, and Enterprise plans, and via the Claude API.

重新设计后的桌面应用现已面向 Pro、Max、Team 和 Enterprise 计划的所有 Claude Code 用户开放，也可通过 Claude API 使用。

Download the app, or update and restart if you already have it. Explore the documentation to learn more.

下载应用即可；如果你已经安装，更新并重启即可。欢迎查阅文档了解更多。
