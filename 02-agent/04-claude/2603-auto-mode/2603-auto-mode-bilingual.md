# Claude Code 的 Auto 模式（中英对照）

> **原文标题：** Auto mode for Claude Code
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/auto-mode
> **发布日期：** 2026-03-24
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Auto mode lets Claude Code make permission decisions with built-in safeguards - fewer interruptions than default, less risk than skipping permissions.

Auto 模式让 Claude Code 自主做出权限决策，并内置安全防护——比默认模式打扰更少，比跳过权限检查风险更低。

Auto mode provides a safer long-running alternative to --dangerously-skip-permissions.

Auto 模式提供了一个比 `--dangerously-skip-permissions` 更安全的长时运行（long-running）替代方案。

Update: Auto mode is generally available in Claude Code for all users. (July 10, 2026)

更新：Auto 模式现已面向所有 Claude Code 用户正式发布（GA）。（2026 年 7 月 10 日）

Today, we're introducing auto mode, a new permissions mode in Claude Code where Claude makes permission decisions on your behalf, with safeguards monitoring actions before they run. It's available now as a research preview on the Team plan, and coming to the Enterprise plan and API users in the coming days.

今天，我们推出 auto 模式——Claude Code 中的一种全新权限模式，由 Claude 代你做出权限决策，并有安全防护在操作运行前加以监控。它现在以研究预览（research preview）形式在 Team 计划中提供，并将在未来几天内推送到 Enterprise 计划和 API 用户。

# 工作原理（How it works）

Claude Code's default permissions are purposefully conservative: every file write and bash command asks for approval. It's a safe default, but it means you can't kick off a large task and walk away, since Claude will request frequent human approvals along the way. While some developers choose to bypass permission checks with --dangerously-skip-permissions, skipping permissions can result in dangerous and destructive outcomes and should not be used outside of isolated environments.

Claude Code 的默认权限设置刻意保守：每一次文件写入和 bash 命令都要请求批准。这是一个安全的默认值，但也意味着你无法启动一个大型任务后就径直离开，因为 Claude 会在过程中频繁请求人工批准。虽然一些开发者选择用 `--dangerously-skip-permissions` 绕过权限检查，但跳过权限可能导致危险且具破坏性的后果，不应在隔离环境之外使用。

Auto mode is a middle path that lets you run longer tasks with fewer interruptions while introducing less risk than skipping all permissions. Before each tool call runs, a classifier reviews it to check for potentially destructive actions like mass deleting files, sensitive data exfiltration, or malicious code execution.

Auto 模式是一条中间路线：它让你能以更少的打扰运行更长的任务，同时相比跳过全部权限又引入更少的风险。每次工具调用运行之前，都会有一个分类器（classifier）对其进行审查，检查是否存在潜在破坏性操作，例如批量删除文件、敏感数据外泄或恶意代码执行。

Actions that the classifier deems as safe proceed automatically, and risky ones get blocked, redirecting Claude to take a different approach. If Claude insists on taking actions that are continually blocked, it will eventually trigger a permission prompt to the user.

被分类器判定为安全的操作会自动继续执行，而危险操作则会被拦截，并引导 Claude 改用其他方式。如果 Claude 坚持执行持续被拦截的操作，最终会触发一个面向用户的权限确认提示。

# 预期效果（What to expect）

Auto mode reduces risk compared to --dangerously-skip-permissions but doesn't eliminate it entirely, and we continue to recommend using it in isolated environments. The classifier may still allow some risky actions: for example, if user intent is ambiguous, or if Claude doesn't have enough context about your environment to know an action might create additional risk. It may also occasionally block benign actions. We'll continue to improve the experience over time.

与 `--dangerously-skip-permissions` 相比，auto 模式降低了风险，但并未完全消除，我们仍建议在隔离环境中使用它。分类器仍可能放行一些危险操作：例如，当用户意图含糊不清时，或当 Claude 缺乏关于你环境的足够上下文、无法判断某个操作可能带来额外风险时。它偶尔也可能拦截无害操作。我们会持续改进这一体验。

Auto mode may have a small impact on token consumption, cost, and latency for tool calls.

Auto 模式可能对 token 消耗、成本以及工具调用延迟产生轻微影响。

# 开始使用（Getting started）

Auto mode is available in Claude Code as a research preview for Claude Team users today, and will roll out to Enterprise and API users in the coming days. It works with both Claude Sonnet 4.6 and Opus 4.6.

Auto 模式今天起以研究预览形式面向 Claude Team 用户在 Claude Code 中提供，并将在未来几天内推广至 Enterprise 和 API 用户。它同时支持 Claude Sonnet 4.6 和 Opus 4.6。

- For admins: Auto mode will soon be available for all Claude Code users on Enterprise, Team, and Claude API plans. To disable it for the CLI and VS Code extension, set "disableAutoMode": "disable" in your managed settings. Auto mode is disabled by default on the Claude desktop app, and can be toggled on using Organization Settings -> Claude Code.
- For developers: Run `claude --enable-auto-mode` to enable auto mode, then cycle to it with Shift+Tab. On Desktop and in the VS Code extension, first toggle auto mode on in Settings -> Claude Code, then select it from the permission mode drop-down in a session.

- 面向管理员：Auto 模式即将面向 Enterprise、Team 和 Claude API 计划上的所有 Claude Code 用户开放。若要在 CLI 和 VS Code 扩展中禁用它，请在托管设置（managed settings）中设置 "disableAutoMode": "disable"。Auto 模式在 Claude 桌面应用中默认禁用，可通过 Organization Settings -> Claude Code 开启。
- 面向开发者：运行 `claude --enable-auto-mode` 启用 auto 模式，然后按 Shift+Tab 切换到它。在桌面端和 VS Code 扩展中，先在 Settings -> Claude Code 中开启 auto 模式，然后在会话的权限模式下拉菜单中选择它。

Explore the docs for more information.

欢迎查阅文档了解更多信息。
