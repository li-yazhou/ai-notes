# Claude Code 高级用户自定义：如何配置 hooks（中英对照）

> **原文标题：** Claude Code power user customization: How to configure hooks
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/how-to-configure-hooks
> **发布日期：** 2025-12-11
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Learn how to configure Claude Code hooks to automate repetitive tasks, enforce project rules, and inject dynamic context into your coding sessions.

了解如何配置 Claude Code hooks（钩子），以自动化重复任务、强制执行项目规则，并向你的编码会话注入动态上下文。

Even a smooth Claude Code workflow accumulates friction points over time. Every time Claude writes a file, Prettier needs to run manually. Every time it runs npm test, the same permission prompt appears. Every session starts with pasting the same boilerplate project context into the first message.

再顺畅的 Claude Code 工作流也会随时间积累摩擦点。每次 Claude 写入文件后，都需要手动运行 Prettier；每次它运行 npm test，都会弹出同样的权限提示；每个会话都从往第一条消息里粘贴同样的项目背景模板开始。

The good news? Hooks eliminate these friction points. They act as triggers you can configure to fire before or after certain actions, allowing you to inject custom logic, scripts, and commands directly into Claude's operations.

好消息是：hooks 可以消除这些摩擦点。它们相当于你可以配置的触发器，在特定动作之前或之后触发，让你能够把自定义逻辑、脚本和命令直接注入 Claude 的操作中。

This article covers advanced configuration for developers already familiar with Claude Code basics. By the end of this article, you'll understand the eight hook types, when to use each one, how to configure them, and how to debug them when things go wrong.

本文面向已熟悉 Claude Code 基础用法的开发者，讲解高级配置。读完本文，你将了解八种 hook 类型、各自的使用时机、如何配置，以及出问题时如何调试。

Let's dive in.

让我们开始吧。

# 什么是 hook？（What is a hook?）

A hook is a custom shell command that you create to execute automatically when a targeted event occurs in your Claude Code session, such as when Claude is about to write a file or when you submit a prompt. You can designate hooks for a huge range of things: intercepting actions before they execute, injecting agent context, automating approvals, or blocking operations before they happen.

Hook（钩子）是你创建的自定义 shell 命令，当 Claude Code 会话中发生目标事件时自动执行，例如 Claude 即将写入文件时，或你提交提示词（prompt）时。你可以为各种用途指定 hook：在动作执行前拦截、注入 agent 上下文、自动批准操作，或在操作发生前将其阻止。

Hooks are configured in your settings files using a JSON structure with event names, matchers (to filter which tools trigger the hook), and the commands to run. They execute in your local environment with your user permissions, receiving information about the triggering event via stdin and communicating back through exit codes and stdout. This gives you precise control over Claude Code behavior without modifying the tool itself.

Hook 在你的设置文件中配置，采用 JSON 结构，包含事件名称、matcher（匹配器，用于筛选哪些工具触发该 hook）以及要运行的命令。它们在你的本地环境中以你的用户权限执行，通过 stdin 接收关于触发事件的信息，并通过退出码（exit code）和 stdout 进行回传。这让你无需修改工具本身，就能精确控制 Claude Code 的行为。

# 为什么在 Claude Code 中使用 hooks？（Why use hooks in Claude Code?）

Hooks solve three categories of problems.

Hooks 解决三类问题。

First, they eliminate repetitive manual steps. Instead of running your formatter after every file change, a PostToolUse hook handles it automatically. Instead of approving npm test for the hundredth time, a PermissionRequest hook auto-approves it.

第一，它们消除重复的手动步骤。不必在每次文件更改后手动运行格式化工具，PostToolUse hook 会自动处理；不必第一百次批准 npm test，PermissionRequest hook 会自动放行。

Second, hooks enforce project-specific rules automatically. You can block dangerous commands before they execute, validate file paths before writes, or ensure naming conventions are followed. These guardrails run every time, not only when you remember to check.

第二，hooks 会自动强制执行项目特定规则。你可以在危险命令执行前拦截它、在写入前校验文件路径，或确保遵守命名约定。这些护栏每次都会生效，而不只是在你记得检查的时候。

Third, hooks inject dynamic context without manual effort. A SessionStart hook can feed Claude your current git status and TODO list. A UserPromptSubmit hook can append your sprint priorities to every request. Claude stays informed without you repeating yourself.

第三，hooks 无需人工介入即可注入动态上下文。SessionStart hook 可以把当前的 git 状态和 TODO 列表喂给 Claude；UserPromptSubmit hook 可以把迭代（sprint）优先级附加到每个请求上。你不必反复交代，Claude 也能保持知情。

# Claude Code 的 hook 类型及使用时机（Claude Code hook types and when to use them）

Claude Code provides eight hook events that cover the full lifecycle of a session, from startup through tool execution to completion. Each fires at a specific moment, giving you precise control over when your automation runs. Choosing the right hook depends on what you want to accomplish.

Claude Code 提供八种 hook 事件，覆盖会话的完整生命周期——从启动、工具执行到结束。每种事件都在特定时刻触发，让你能精确控制自动化何时运行。选择哪个 hook 取决于你想达成什么目标。

Hooks at a glance

Hooks 一览

| Hook | When it fires | Common uses |
| --- | --- | --- |
| PreToolUse | Before a tool executes | Block dangerous commands, validate file paths, auto-approve safe operations |
| PermissionRequest | Before a permission dialog appears | Auto-approve test commands, block access to sensitive files |
| PostToolUse | After a tool completes | Run formatters, trigger linters, log file changes |
| PreCompact | Before context compaction | Back up transcripts, preserve important decisions |
| SessionStart | When a session begins or resumes | Inject git status, load TODO lists, set environment context |
| Stop | When Claude finishes responding | Verify task completion, run tests, generate summaries |
| SubagentStop | When a subagent completes | Validate subagent output, trigger follow-up actions |
| UserPromptSubmit | When you submit a prompt | Inject sprint context, validate requests, add dynamic context |

| Hook | 触发时机 | 常见用途 |
| --- | --- | --- |
| PreToolUse | 工具执行之前 | 拦截危险命令、校验文件路径、自动批准安全操作 |
| PermissionRequest | 权限对话框弹出之前 | 自动批准测试命令、阻止访问敏感文件 |
| PostToolUse | 工具完成之后 | 运行格式化工具、触发 linter、记录文件变更日志 |
| PreCompact | 上下文压缩（compaction）之前 | 备份会话记录、保留重要决策 |
| SessionStart | 会话开始或恢复时 | 注入 git 状态、加载 TODO 列表、设置环境上下文 |
| Stop | Claude 完成响应时 | 验证任务完成情况、运行测试、生成摘要 |
| SubagentStop | subagent（子代理）完成时 | 校验 subagent 输出、触发后续动作 |
| UserPromptSubmit | 你提交提示词时 | 注入迭代上下文、校验请求、添加动态上下文 |

## 工具使用前（PreToolUse）

This is the most commonly used hook, firing after Claude chooses a tool to use but before the tool actually executes. Your script can inspect the planned action and approve it, block it, request user confirmation, or modify the parameters, using a matcher to filter which tools trigger this hook.

这是最常用的 hook，在 Claude 选定要使用的工具之后、工具实际执行之前触发。你的脚本可以审查计划中的动作，批准、拦截、请求用户确认或修改参数，并使用 matcher 筛选哪些工具触发此 hook。

This PreToolUse hook example evaluates file writes before they execute. Claude reviews the planned action against the specified criteria and can approve, block, or flag concerns based on the prompt logic.

这个 PreToolUse hook 示例会在文件写入执行前对其进行评估。Claude 会依据指定标准审查计划中的动作，并可基于提示词逻辑批准、拦截或标记疑虑。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate-file-path.sh"
          }
        ]
      }
    ]
  }
}
```

When to use PreToolUse:

何时使用 PreToolUse：

- Blocking dangerous Bash commands like rm -rf or force pushes
- Auto-approving safe, repetitive operations to reduce prompt fatigue
- Validating file paths before writes to prevent accidental overwrites
- Modifying tool inputs to inject project-specific defaults

- 拦截危险 Bash 命令，如 rm -rf 或强制推送（force push）
- 自动批准安全且重复的操作，减少审批提示带来的疲劳
- 写入前校验文件路径，防止意外覆盖
- 修改工具输入以注入项目特定默认值

## 权限请求（PermissionRequest）

This hook fires when Claude would normally show a permission dialog. This hook intercepts the moment before you would see a confirmation prompt, letting your script decide whether to allow, deny, or still ask the user.

此 hook 在 Claude 通常会弹出权限对话框时触发。它拦截在你看到确认提示之前的那个时刻，让脚本决定是允许、拒绝，还是仍然询问用户。

```json
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "Bash(npm test*)",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/validate-test-command.sh"
          }
        ]
      }
    ]
  }
}
```

This example auto-approves any Bash command starting with npm test. The matcher pattern can include arguments for finer control.

此示例会自动批准任何以 npm test 开头的 Bash 命令。matcher 模式可以包含参数以实现更精细的控制。

When to use PermissionRequest:

何时使用 PermissionRequest：

- Auto-approving test commands you run dozens of times per session
- Blocking write access to production configuration files
- Allowing read operations on specific directories without prompts
- Denying any command that matches a dangerous pattern

- 自动批准每个会话要运行几十次的测试命令
- 阻止对生产环境配置文件的写入
- 允许对特定目录的读取操作无需提示
- 拒绝任何匹配危险模式的命令

## 工具使用后（PostToolUse）

Fires immediately after a tool completes successfully. Your script receives information about what happened, including the tool output, using matchers to filter which tools trigger it.

在工具成功完成后立即触发。你的脚本会收到关于所发生情况的信息（包括工具输出），并使用 matcher 筛选哪些工具触发它。

This example of PostToolUse runs Prettier on any file Claude writes or edits. The pipe syntax in the matcher means it triggers for both Write and Edit tools.

这个 PostToolUse 示例会对 Claude 写入或编辑的任何文件运行 Prettier。matcher 中的管道语法意味着它对 Write 和 Edit 两个工具都会触发。

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

When to use PostToolUse:

何时使用 PostToolUse：

- Running Prettier, Black, or gofmt after every file write to enforce formatting
- Logging all file modifications to an audit trail
- Triggering linters and showing warnings after code changes
- Sending notifications when certain operations complete

- 每次文件写入后运行 Prettier、Black 或 gofmt 以强制格式化
- 将所有文件修改记入审计日志
- 代码变更后触发 linter 并显示警告
- 特定操作完成时发送通知

## 压缩前（PreCompact）

Fires before Claude compacts the conversation context to free up space. Compaction summarizes older parts of the conversation, which means some details get lost. This hook gives you a chance to preserve information before that happens.

在 Claude 压缩（compact）对话上下文以释放空间之前触发。压缩会对对话中较旧的部分做摘要，这意味着部分细节会丢失。此 hook 让你有机会在那之前保存信息。

This PreCompact example backs up the transcript before automatic compaction. The matcher can be "auto" or "manual" so you can distinguish between automatic compaction and user-triggered compaction events.

这个 PreCompact 示例会在自动压缩前备份会话记录（transcript）。matcher 可以设为 "auto" 或 "manual"，便于区分自动压缩与用户触发的压缩事件。

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/backup-transcript.sh"
          }
        ]
      }
    ]
  }
}
```

When to use PreCompact:

何时使用 PreCompact：

- Backing up the full transcript to a file before summarization
- Extracting and saving important decisions or code snippets
- Logging session milestones for later review

- 在摘要化之前把完整会话记录备份到文件
- 提取并保存重要决策或代码片段
- 记录会话里程碑以便日后回顾

## 会话启动（SessionStart）

Fires when Claude Code starts a new session or resumes an existing one. Whatever your script outputs gets added to the conversation context, so Claude starts with that information already loaded.

在 Claude Code 启动新会话或恢复现有会话时触发。脚本输出的任何内容都会加入对话上下文，因此 Claude 一开始就已加载这些信息。

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "git status --short && echo '---' && cat TODO.md"
          }
        ]
      }
    ]
  }
}
```

Every session starts with Claude knowing your current git status and TODO list. Stdout automatically becomes context.

每个会话开始时，Claude 都知道你当前的 git 状态和 TODO 列表。stdout 会自动成为上下文。

When to use SessionStart:

何时使用 SessionStart：

- Feeding Claude your current git branch and recent commits
- Loading the contents of your TODO list or sprint backlog
- Injecting environment-specific configuration details

- 把当前 git 分支和最近的提交喂给 Claude
- 加载 TODO 列表或迭代待办（sprint backlog）的内容
- 注入环境特定的配置细节

## 停止（Stop）

Fires when Claude finishes responding and would normally wait for your next input. Your script can inspect what Claude produced and decide whether the task is truly complete.

在 Claude 完成响应、通常会等待你下一次输入时触发。你的脚本可以检查 Claude 产出的内容，判断任务是否真正完成。

The script can return JSON with "continue": true to make Claude continue working, which is useful for multi-step workflows:

脚本可以返回包含 "continue": true 的 JSON 让 Claude 继续工作，这在多步骤工作流中很有用：

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Review whether the task is complete. If all requirements are met, respond with 'complete'. If work remains, respond with 'continue' and specify what still needs to be done."
          }
        ]
      }
    ]
  }
}
```

When to use Stop:

何时使用 Stop：

- Forcing Claude to continue until all items in a checklist are done
- Verifying that tests pass before considering a task complete
- Triggering summary generation at the end of a session
- Checking that generated code compiles before stopping

- 强制 Claude 继续工作，直到清单中所有事项完成
- 在认定任务完成前验证测试通过
- 在会话结束时触发生成摘要
- 停止前检查生成的代码可以编译

## 子代理停止（SubagentStop）

This hook fires whenever a subagent created via the Task tool finishes. Works the same way as Stop, but triggers specifically when a subagent completes its action (rather than the main agent). The configuration of SubagentStop mirrors the Stop hook structure:

每当通过 Task 工具创建的 subagent（子代理）完成时，此 hook 就会触发。它与 Stop 的工作方式相同，但专门在 subagent（而非主 agent）完成动作时触发。SubagentStop 的配置与 Stop hook 结构一致：

```json
{
  "hooks": {
    "SubagentStop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate the subagent's output. Verify the task was completed correctly and the results meet quality standards. If the output is satisfactory, respond with 'accept'. If issues exist, respond with 'reject' and explain what needs to be fixed."
          }
        ]
      }
    ]
  }
}
```

When to use SubagentStop:

何时使用 SubagentStop：

- Validating that subagent output meets quality criteria
- Triggering follow-up actions based on subagent results
- Logging subagent activity for debugging or auditing

- 校验 subagent 输出是否符合质量标准
- 基于 subagent 结果触发后续动作
- 记录 subagent 活动用于调试或审计

## 用户提示提交（UserPromptSubmit）

Fires when you submit a prompt, before Claude processes it. Whatever your script outputs via stdout gets added to Claude's context along with your prompt, which makes UserPromptSubmit useful for dynamically injecting information that Claude should consider.

在你提交提示词时、Claude 处理它之前触发。脚本通过 stdout 输出的任何内容都会随你的提示词一起加入 Claude 的上下文，这使得 UserPromptSubmit 非常适合动态注入 Claude 应当考虑的信息。

In this example, every time you submit a prompt, Claude receives the contents of your sprint context file. This keeps Claude informed about current priorities without you needing to restate them.

在这个示例中，每次你提交提示词，Claude 都会收到你的迭代上下文文件的内容。这样你无需重复说明，Claude 也能随时了解当前优先级。

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat ./current-sprint-context.md"
          }
        ]
      }
    ]
  }
}
```

When to use UserPromptSubmit:

何时使用 UserPromptSubmit：

- Injecting current sprint context or project priorities with every prompt
- Validating prompts before they reach Claude
- Blocking certain types of requests based on content
- Adding dynamic context like recent error logs or test results

- 随每个提示词注入当前迭代上下文或项目优先级
- 在提示词到达 Claude 之前先校验
- 根据内容拦截某些类型的请求
- 添加动态上下文，如最近的错误日志或测试结果

# 配置与文件位置（Configuration and file locations）

Hooks live in JSON settings files at three levels. Project-level hooks go in .claude/settings.json within your repository, making them shareable with your team. User-level hooks go in ~/.claude/settings.json and apply across all your projects. Local project hooks go in .claude/settings.local.json for personal configuration you don't want to commit.

Hooks 存在于三个层级的 JSON 设置文件中。项目级（project-level）hooks 放在仓库内的 .claude/settings.json，可与团队共享；用户级（user-level）hooks 放在 ~/.claude/settings.json，适用于你的所有项目；本地项目（local）hooks 放在 .claude/settings.local.json，用于你不想提交到版本库的个人配置。

Project-level settings take precedence over user-level settings. There are also enterprise-managed policy settings available for organizational control. For complete details, see the Claude Code settings information.

项目级设置优先于用户级设置。此外还有企业管理的策略设置，可供组织统一管控。完整细节请参阅 Claude Code 设置文档。

Pro tip: This is the same file where you can set granular permissions for Claude actions, at the project, user, or local levels. For example, you can explicitly allow Claude to read all files in a directory so that you don't have to approve it every time, or block any modification of sensitive files.

小贴士：你也可以在同一个文件中，在项目、用户或本地层级为 Claude 的操作设置细粒度权限。例如，你可以明确允许 Claude 读取某个目录下的所有文件，免得每次都要批准；或者阻止对敏感文件的任何修改。

# Matcher（匹配器）语法（Matcher syntax）

Matchers are how you filter which tools can trigger your hook. They only apply to PreToolUse, PostToolUse, and PermissionRequest hooks.

Matcher 用于筛选哪些工具可以触发你的 hook。它们只适用于 PreToolUse、PostToolUse 和 PermissionRequest 这三种 hook。

Simple string matching works exactly as you'd expect: "Write" matches only the Write tool.

简单字符串匹配的行为完全如你所料："Write" 只匹配 Write 工具。

For example:

例如：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "your-command-here"
          }
        ]
      }
    ]
  }
}
```

The pipe syntax lets you match multiple tools: "Write|Edit" triggers for either, whereas wildcards match everything: "*" or an empty string matches all tools.

管道语法可以匹配多个工具："Write|Edit" 对两者都触发；而通配符匹配一切："*" 或空字符串匹配所有工具。

Note: Matchers are case sensitive, so "bash" won't be matched to the Bash tool.

注意：matcher 区分大小写，因此 "bash" 不会匹配到 Bash 工具。

For finer control, argument patterns like "Bash(npm test*)" can match specific command arguments. MCP tool patterns follow the format "mcp__memory__.*" for Model Context Protocol tools.

如需更精细的控制，参数模式（如 "Bash(npm test*)"）可以匹配特定的命令参数。MCP 工具模式采用 "mcp__memory__.*" 这样的格式，用于模型上下文协议（Model Context Protocol）工具。

# 输入、输出与结构化响应（Input, output, and structured responses）

## hooks 接收什么（What hooks receive）

All hooks receive JSON via stdin containing session information and event-specific data. Common fields include: session_id, transcript_path, cwd, permission_mode, and hook_event_name.

所有 hook 都会通过 stdin 接收 JSON，其中包含会话信息和事件特定数据。常见字段包括：session_id、transcript_path、cwd、permission_mode 和 hook_event_name。

Additionally, tool-related hooks also receive tool_name and tool_input. This data lets your scripts make informed decisions about how to respond.

此外，与工具相关的 hook 还会接收 tool_name 和 tool_input。这些数据让你的脚本能就如何响应做出有依据的决策。

## hooks 如何响应（How hooks respond）

Exit codes determine the basic outcome. Exit code 0 means success, and stdout either gets processed for JSON or added to context. Exit code 2 means a blocking error: stderr becomes the error message and the action gets prevented.

退出码决定基本结果。退出码 0 表示成功，stdout 要么被当作 JSON 解析处理，要么被加入上下文。退出码 2 表示阻断性错误：stderr 成为错误信息，动作被阻止。

Other exit codes indicate non-blocking errors, with stderr shown in verbose mode.

其他退出码表示非阻断性错误，stderr 会在详细（verbose）模式下显示。

Beyond exit codes, hooks can return structured JSON for more control. Fields include: decision (approve, block, allow, or deny), reason (explanation shown to Claude), continue (for Stop hooks to force continuation), and updatedInput (to modify tool parameters before execution).

除退出码外，hook 还可以返回结构化 JSON 以获得更多控制。字段包括：decision（决定：approve、block、allow 或 deny）、reason（原因，向 Claude 展示的解释）、continue（供 Stop hook 强制继续）和 updatedInput（在执行前修改工具参数）。

# 环境与执行（Environment and execution）

Hooks have access to environment variables, including: CLAUDE_PROJECT_DIR for the project root path, CLAUDE_CODE_REMOTE which is true for web environments, and CLAUDE_ENV_FILE for SessionStart hooks to persist variables. Standard environment variables from your shell are also accessible.

Hooks 可以访问环境变量，包括：CLAUDE_PROJECT_DIR（项目根路径）、CLAUDE_CODE_REMOTE（在 Web 环境下为 true）和 CLAUDE_ENV_FILE（供 SessionStart hook 持久化变量）。shell 中的标准环境变量同样可以访问。

Also of note: Hooks have a 60-second default timeout, configurable per hook. When multiple hooks match an event, they run in parallel. Identical commands are automatically deduplicated.

另需注意：hooks 默认超时为 60 秒，可按 hook 单独配置。当多个 hook 匹配同一事件时，它们并行运行。相同的命令会被自动去重。

# 安全性考量（Security considerations）

Hooks execute arbitrary shell commands with your user permissions. Claude Code includes a safeguard: direct edits to hook configuration files require review in the /hooks menu before taking effect. This prevents malicious code from silently adding hooks to your configuration.

Hooks 会以你的用户权限执行任意 shell 命令。Claude Code 内置了一道防线：对 hook 配置文件的直接修改必须先在 /hooks 菜单中审核才能生效。这可以防止恶意代码悄悄向你的配置中添加 hook。

However, if you configure and approve hooks, they will execute at your permission levels.

不过，一旦你配置并批准了 hooks，它们就会以你的权限级别执行。

Pro tip: Before you run any commands in an environment, consider the risks. If you're going to run commands with hooks, consider good practices like: validating and sanitizing inputs from stdin, quoting shell variables to prevent injection, using absolute paths for scripts, and avoiding processing sensitive files like .env or credentials.

小贴士：在任何环境中运行命令之前，都要先考虑风险。如果你打算用 hooks 运行命令，请遵循良好实践，例如：校验并清理来自 stdin 的输入、为 shell 变量加引号以防注入、为脚本使用绝对路径，以及避免处理 .env 或凭据等敏感文件。

# 调试与测试（Debugging and testing）

Claude Code logs everything to transcript files, which provides visibility into tool calls and responses without any setup. Every hook receives a transcript_path field pointing to a JSONL file containing the full session history. You can use a SessionStart hook to log where each transcript lives:

Claude Code 会把所有内容记录到 transcript（会话记录）文件中，无需任何配置即可查看工具调用与响应。每个 hook 都会收到一个 transcript_path 字段，指向包含完整会话历史的 JSONL 文件。你可以用 SessionStart hook 记录每个 transcript 的位置：

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '\"Session: \" + .transcript_path' >> ~/.claude/sessions.log"
          }
        ]
      }
    ]
  }
}
```

Then tail that transcript to watch Claude work in real time: `tail -f /path/to/transcript.jsonl | jq .`

然后 tail 那个 transcript，实时观察 Claude 工作：`tail -f /path/to/transcript.jsonl | jq .`

## hook 专项调试（Hook-specific debugging）

For hook-specific debugging, add logging to your hook scripts. The transcript files will show what Claude did, but not why your hook took the action to approve or block something.

针对 hook 的专项调试，可以在 hook 脚本中添加日志。transcript 文件会显示 Claude 做了什么，但不会显示你的 hook 为何批准或拦截了某个操作。

With a little extra effort you can add a small bash script that will wrap your tools and log the additional information. For example, log-wrapper.sh:

只需多花一点力气，你就可以添加一个小的 bash 脚本，包装你的工具并记录额外信息。例如 log-wrapper.sh：

```bash
#!/bin/bash

LOG=~/.claude/hooks.log

INPUT=$(cat)

TOOL=$(echo "$INPUT" | jq -r '.tool_name // "n/a"')
EVENT=$(echo "$INPUT" | jq -r '.hook_event_name // "n/a"')

echo "=== $(date) | $EVENT | $TOOL ===" >> "$LOG"
echo "$INPUT" | "$1"
CODE=$?
echo "Exit: $CODE" >> "$LOG"
exit $CODE
```

This small wrapper script captures stdin into a variable, logs the timestamp and tool name, then pipes the input to your actual tool.

这个小型包装脚本会把 stdin 捕获到变量中，记录时间戳和工具名，然后把输入通过管道传给你真正的工具。

Once you have log-wrapper.sh written, you would then prepend it to the tool call in the hook:

写好 log-wrapper.sh 之后，在 hook 中把它加到工具调用的前面：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "log-wrapper.sh your-tool-command.py"
          }
        ]
      }
    ]
  }
}
```

Pro tip: For more debugging tips, check out the Claude Code debugging documentation.

小贴士：更多调试技巧请查阅 Claude Code 调试文档。

# 构建你自己的 hooks（Building your own hooks）

Start with one simple hook that solves an actual friction point in your workflow. The PostToolUse formatter hook is a good first choice since the feedback is immediate and visible. Once that works, expand based on what you learn.

从一个能解决你工作流中实际摩擦点的简单 hook 开始。PostToolUse 格式化 hook 是不错的首选，因为其反馈即时且可见。等它跑通后，再根据所学逐步扩展。

For complete reference documentation including all available fields and advanced patterns, see the official hooks documentation.

包含所有可用字段和高级模式的完整参考文档，请参阅官方 hooks 文档。

Hooks let you shape Claude Code to match your workflow rather than adapting your workflow to the tool. When you invest in configuring hooks, it pays off every session.

Hooks 让你把 Claude Code 塑造成贴合自己工作流的形态，而不是让工作流去迁就工具。在配置 hooks 上投入的精力，每个会话都会有回报。

Start using hooks to customize your Claude Code workflows today.

今天就动手用 hooks 定制你的 Claude Code 工作流吧。
