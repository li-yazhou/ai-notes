# 在 Claude Code 中用 Skills 构建验证循环（中英对照）

> **原文标题：** Building verification loops in Claude Code with skills
> **作者：** Delba de Oliveira（Claude Code 团队）
> **原文链接：** https://claude.com/blog/building-verification-loops-in-claude-code-with-skills
> **发布日期：** 2026-07-22
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

How Anthropic builds verification loops in Claude Code: turn your manual checks into skills so Claude tests, fixes, and verifies its own work.

Anthropic 如何在 Claude Code 中构建验证循环（verification loop）：把你的人工检查变成 skills，让 Claude 测试、修复并验证自己的工作。

How to turn your manual checks into skills, so Claude closes its own feedback loop.

如何把你的人工检查变成 skills，让 Claude 自行闭合它的反馈循环。

Most agentic coding sessions follow a loop: you ask for a change, Claude gathers context, takes action, verifies the results, and if needed, loops back to gather additional context.

大多数智能体编程会话都遵循一个循环：你请求一项变更，Claude 收集上下文、采取行动、验证结果，如有需要，再回过头去收集更多上下文。

Verification is how agents check their work before responding. Claude already does some of this from observing the deterministic signals in your codebase, including type checkers, linters, tests, and runtime errors. Whatever Claude can't infer becomes the steps you take to manually check a feature.

验证（verification）是智能体在给出答复前检查自己工作的方式。Claude 已经会通过观察你代码库中的确定性信号来做一部分验证，包括类型检查器、linter、测试和运行时错误。而 Claude 无法自行推断的部分，就成了你人工检查一个功能时要执行的步骤。

These manual steps, however, can be transformed into verification loops. In Claude Code, a verification loop is an iterative process where Claude checks and attempts to fix the work.

不过，这些人工步骤可以被改造成验证循环（verification loop）。在 Claude Code 中，验证循环是一个迭代过程：Claude 检查工作成果，并尝试修复问题。

![智能体循环示意图：1. 收集上下文，2. 采取行动，3. 验证结果](images/verifloop-1.png)

> The agentic loop: 1. gathering context, 2. taking action, 3. verifying results.
> 智能体循环（agentic loop）：1. 收集上下文；2. 采取行动；3. 验证结果。

In this article, we cover the most common types of verification loops and show you what we use inside Anthropic. Then we'll show how to encode the manual checks you already do as skills, so Claude can close its own feedback loop and you can work on something else while it iterates.

在本文中，我们将介绍最常见的验证循环类型，并展示我们在 Anthropic 内部的用法。然后，我们会演示如何把你已经在做的人工检查编码成 skills，让 Claude 自己闭合反馈循环，而你可以在它迭代时去忙别的。

New to agent loops? Start with getting started with loops.

刚接触智能体循环？可以从《loops 入门》开始。

# 什么是验证循环？（What is a verification loop?）

A verification loop is a repeating cycle where an AI agent checks its own work - running tests, linters, or custom checks - and fixes what fails before moving on. In Claude Code, verification loops can be packaged as skills, so every session applies the same checks automatically instead of relying on a human to remember them.

验证循环是一个不断重复的周期：AI 智能体检查自己的工作--运行测试、linter 或自定义检查--并在继续之前修复失败的部分。在 Claude Code 中，验证循环可以打包成 skills，这样每个会话都会自动应用相同的检查，而不必依赖人来记住它们。

# 内置验证循环（Built-in verification loops）

Before diving into designing custom verification loops, it can be helpful to understand the built-in support Claude has for a number of different verification loops. Common features and approaches include:

在深入设计自定义验证循环之前，先了解 Claude 对多种验证循环的内置支持会很有帮助。常见的功能和做法包括：

- /verify skill: builds, runs, and observes the changes in your application.
- Toolchain: Claude aims to catch and act on error codes and warnings from any tool you provide such as a linter. A good practice is to list your exact build and test commands in CLAUDE.md so Claude doesn't have to infer them.
- Code Review (research preview): A managed multi-agent service that runs an automated review pass on PRs in the repos you enable. You can manually fix the finding and push, or close the loop by commenting @claude on the finding (if you've already set up and configured GitHub Actions, below).
- GitHub Actions: Define a job that invokes Claude with a verification skill, and the same checks you run locally fire on every push or PR.
- Spec validation: A skill that helps verify each change against a markdown spec in the repo and looks to fix violations.
- Rubrics in Claude Managed Agents (beta): A managed agentic service that allows you to verify outcomes against a rubric using a separate grader agent. Failures loop back for rework automatically.

- /verify 技能：构建、运行并观察你应用中的变更。
- 工具链（Toolchain）：Claude 会努力捕获并根据你提供的任何工具（如 linter）的错误码和警告采取行动。一个好做法是把确切的构建和测试命令写进 CLAUDE.md，这样 Claude 就不必去猜。
- 代码审查（Code Review，研究预览版）：一项托管的多智能体服务，会对你启用仓库中的 PR 运行自动化审查。你可以手动修复发现的问题并推送，也可以在发现项下评论 @claude 来闭环（如果你已经按下文设置并配置了 GitHub Actions）。
- GitHub Actions：定义一个调用 Claude 并附带验证技能的作业，你在本地运行的同样检查就会在每次 push 或 PR 时触发。
- 规格校验（Spec validation）：一个帮助依据仓库中的 markdown 规格文档校验每次变更、并着手修复违规之处的技能。
- Claude Managed Agents 中的评分标准（Rubrics，beta）：一项托管智能体服务，允许你使用单独的评分智能体（grader agent）按评分标准验证结果。失败的项会自动回流返工。

# 编写验证循环（Writing verification loops）

When you have an existing project and you find yourself making the same small corrections every time Claude implements a new feature for you, it's time to turn those steps into your own custom verification loop. The first step is to write down everything that you find yourself doing every time

当你已经有了一个项目，却发现每次让 Claude 实现新功能时自己都在做同样的小修小补，那就是时候把这些步骤变成你自己的自定义验证循环了。第一步是把你发现自己每次都在做的事情全部写下来

The same goes if you're starting a new project and need to figure out how the project should behave. Write the best-practices version in plain English, the way you'd hand it to a new teammate on day one.

如果你是在启动一个新项目、需要确定项目应有的行为方式，同样的方法也适用。用平实的语言写下最佳实践版本，就像第一天交接给一位新同事那样。

If you're struggling to articulate the verification check itself, ask Claude for best practices first and edit from there. Your version probably differs on a few specific points, and those differences are exactly what you want to capture.

如果你难以把验证检查本身表述清楚，可以先让 Claude 给出最佳实践，再在其基础上编辑。你的版本多半会在几个具体点上有所不同，而这些差异恰恰是你想捕捉的东西。

Pro tip: The check doesn't have to be qualitative to belong here. "Reject any migration that drops a column without a backfill step" is a deterministic rule no generic linter will catch but a project-specific one will. Anything you keep having to enforce by hand as a manual check qualifies for capture as a loop.

专业提示：检查并不一定要是定性主观的才配写在这里。"拒绝任何在没有回填（backfill）步骤的情况下删除列的迁移"是一条确定性规则，通用 linter 抓不到它，但项目专属的检查可以。任何你不得不一直靠人工执行的手动检查，都值得被收录为一个循环。

# 把它做成 skill（Make it a skill）

The most common way to encode repetitive steps into a verification loop is to write it as a skill, and the fastest way to create a skill is to install the skill-creator plugin and let Claude interview you:

把重复步骤编码成验证循环，最常见的做法是把它写成一个 skill；而创建 skill 最快的方式，是安装 skill-creator 插件，让 Claude 来采访你：

Example:

示例：

```
/skill-creator Create a skill for verifying frontend changes end-to-end. Interview me about my workflow.
```

You can also hand-write a skill by dropping a markdown file in .claude/skills/ inside your project. The simplest possible verification skill is a few lines of frontmatter plus a body:

你也可以手写 skill：在项目的 .claude/skills/ 目录下放一个 markdown 文件即可。最简单的验证 skill 就是几行 frontmatter 加上一段正文：

```markdown
# .claude/skills/verify-log-hygiene/SKILL.md

---
name: verify-log-hygiene
description: Check that error logs include the request ID and never include the request body. Use when the diff touches error handling or logging.
allowed-tools: [Read, Edit, Grep]
---

Read the error-handling paths in the current diff. For each log call on an error path, confirm it includes the request ID and does not pass the request body, headers, or any user-supplied payload. Report each violation with file:line, then fix it: add the request ID where it's missing and strip the payload from the log call.
```

The full schema and the philosophy behind it are in our complete guide to building skills.

完整的 schema 及其背后的设计哲学，见我们的《技能构建完整指南》。

# 让检查与运行位置相匹配（Match the check to where it runs）

The next thing to determine will be how the verification loop kicks off: standalone, embedded, chained, or tied to PR.

接下来要确定的是验证循环如何启动：独立运行（standalone）、内嵌（embedded）、链式（chained），还是绑定 PR。

## 独立运行（Standalone）

You invoke it deliberately, after the artifact exists. A standalone skill earns its place for cross-cutting checks that don't apply every time: a pre-commit security scan, a pre-PR accessibility audit, license-header verification across a repo. Anything you want available across many workflows but don't want firing on every code change.

由你有意调用，在产出物（artifact）已经存在之后。独立运行的 skill 适合那些并非每次都适用的横切检查：提交前的安全扫描、PR 前的无障碍审计、整个仓库范围的许可证头校验。即那些你希望在很多工作流中都能用到、但不想在每次代码变更时都触发的东西。

The cost is that each invocation is still a turn you have to remember to take. The signal that you've outgrown standalone is when you're running it after every change. At that point, the procedure has earned a permanent home: embed it or chain it.

代价在于，每次调用仍然需要你记得去执行这一轮。当你发现自己在每次变更后都要跑一遍它时，就是已经超出"独立运行"适用范围的信号。到那时，这套流程值得拥有一个常驻的家：把它内嵌或链式化。

## 内嵌（Embedded）

Fires automatically as part of the producing skill. The check belongs to one specific workflow, and the workflow now runs it without you asking.

作为产出该成果的技能的一部分自动触发。这项检查专属于某个具体工作流，而该工作流现在会在你无需开口的情况下运行它。

The simplest version is a one-line append to the producing skill's body:

最简单的版本是在产出性技能的正文末尾追加一行：

```markdown
# .claude/skills/scaffold-component/SKILL.md

---
name: scaffold-component
description: Scaffold a new React component under src/components/, including the component file, its co-located test, and an index export. Use when the user asks to create a new component.
allowed-tools: [Read, Write, Edit, Bash, Glob]
---

# Scaffold a new React component

Given a component name (PascalCase), create the following under `src/components/<Name>/`:

1. `<Name>.tsx`: function component with a typed props interface and a default export.
2. `<Name>.test.tsx`: React Testing Library test that renders the component and asserts it mounts without throwing.
3. `index.ts`: re-export the default and any named exports.

Follow the patterns in `src/components/Button/` as the reference.
Match the import alias style (`@/components/...`) used throughout the codebase.

# code continues...

After creating the component file, run eslint on it and address any errors before reporting completion.
```

Verify the embed works by invoking the skill on a fresh task and confirming the new step runs as part of the output. If it doesn't, the skill's description or earlier instructions aren't pulling the appended check in.

验证内嵌是否生效的方法：在一个新任务上调用该技能，确认新增步骤会作为输出的一部分运行。如果没有，说明技能的 description 或先前的指令没有把追加的检查拉进来。

Embedded only works on skills you can edit: ones you wrote yourself, or ones installed at a project level where the SKILL.md file is under your control. Built-in skills and plugin-managed skills (the kind that get overwritten on update) are off-limits for this pattern; for those, chain instead.

内嵌只适用于你能编辑的技能：你自己写的，或安装在项目级、SKILL.md 文件由你掌控的。内置技能和插件管理的技能（更新时会被覆盖的那种）不能用这个模式；对它们，请改用链式。

Skip embedded for checks that span workflows; those want standalone, so you can invoke them from any context.

跨工作流的检查不要用内嵌；它们需要的是独立运行，这样你才能在任何上下文中调用它们。

## 链式（Chained）

One skill calls another at its end, and several verified handoffs run end-to-end.

一个技能在结束时调用另一个技能，多个经过验证的接力一路端到端运行。

Members of Anthropic's Claude Code team use this pattern in their day-to-day: /code-review hunts for bugs, /simplify cleans up the diff, a /verify skill confirms end-to-end behavior, and a custom /design skill checks against guidelines in a DESIGN.md file if the change touched UI.

Anthropic Claude Code 团队的成员日常就在使用这个模式：/code-review 查找 bug，/simplify 清理 diff，一个 /verify 技能确认端到端行为，如果变更涉及 UI，还有一个自定义的 /design 技能对照 DESIGN.md 文件中的规范进行检查。

Chaining is also how you add verification to a skill you can't modify: build a custom wrapper skill that invokes the original, then invokes your verification skill, as depicted below:

链式也是你为无法修改的技能添加验证的方式：构建一个自定义的包装技能，先调用原技能，再调用你的验证技能，如下图所示：

```markdown
# .claude/skills/safe-refactor/SKILL.md

Run /simplify on the current diff first. When /simplify finishes, invoke /verify-no-public-api-changes.
```

What started as a habit ("I always run /verify after /simplify") becomes a contract ("/simplify always runs /verify when it finishes"). The chain runs the whole dev cycle on its own. You only step in when something escalates back to you.

起初只是一种习惯（"我总是在 /simplify 之后运行 /verify"），如今变成了一份契约（"/simplify 结束时总是运行 /verify"）。这条链会自己跑完整个开发循环，只有当有事项升级回到你这里时，你才需要出手。

You can skip chaining when the steps are independent enough that you sometimes want to run one without the others; chaining trades flexibility for automation. Chained verification loops can increase token spend, so it's best to test these loops before deploying them broadly.

当各步骤足够独立、你有时只想单独运行其中之一时，可以不用链式；链式是用灵活性换自动化。链式验证循环可能增加 token 开销，因此最好先测试这些循环，再大规模部署。

## 在每个 PR 上（On every PR）

Once the chain is solid for your own changes, the same procedure can run on every PR. A teammate's change passes the same gates yours did, whether they remembered to invoke the chain or not. The infrastructure is the same kind of thing as the chain you already wrote, one step further along: the same skills, the same rubrics, the same standards, applied without depending on the author's diligence.

一旦这条链对你自己的变更已经足够稳固，同样的流程就可以在每个 PR 上运行。队友的变更会通过与你的变更相同的关卡，无论他们是否记得调用这条链。这套基础设施与你已写好的链是同一类东西，只是再往前走了一步：同样的技能、同样的评分标准、同样的质量标准，只是不再依赖作者的自觉。

This is where verification stops being personal infrastructure and becomes team infrastructure. The check you wrote down to save yourself two minutes a week is now saving everyone two minutes a week, on every change. Hold off on PR-wide gates while the chain is still in flux; every adjustment becomes a team-visible event.

到这一步，验证就不再是个人的基础设施，而成为团队的基础设施。你为了每周给自己省两分钟而写下的检查，如今在每一次变更中为所有人省下两分钟。在链条本身还在频繁调整时，先不要上全 PR 范围的关卡；每一次调整都会成为全团队可见的事件。

Once you have the process down, you're ready to expand your loop engineering. The verification loop creation process is consistent, no matter what you're automating or in what environment:

一旦掌握了这套流程，你就可以扩展你的循环工程（loop engineering）了。验证循环的创建过程是一致的，无论你要自动化什么、在什么环境中：

- Pick the manual follow-up you did most often this week.
- Try out the built-in /verify skill first and see if it helps your process.
- Write the procedure in plain English, the way you'd hand it to a new teammate on day one.
- Hand it to skill-creator, or drop the markdown file in .claude/skills/ yourself.
- Invoke it on a new task and confirm the check runs as part of the output, iterate if needed.
- Experiment with skill chaining to create an end-to-end verification flow.

- 选出你本周做得最频繁的那项人工跟进。
- 先试用内置的 /verify 技能，看看它能否帮到你的流程。
- 用平实的语言写下这套流程，就像第一天交接给新同事那样。
- 交给 skill-creator，或者自己把 markdown 文件放进 .claude/skills/。
- 在新任务上调用它，确认检查会作为输出的一部分运行，必要时迭代改进。
- 尝试技能链式组合，打造端到端的验证流程。

The more you can encode for Claude to follow, the more often Claude's response will land closer to what you want on the very first try. The corrections you no longer have to fiddle with now free up your attention for the individual and exclusive work that no skill can write down for you.

你能为 Claude 编码下来供其遵循的越多，Claude 的回答在第一次尝试时就贴近你期望的次数就越多。那些你不必再摆弄的修正工作，把你的注意力解放出来，投入到任何 skill 都无法替你写下的、专属于你的工作中去。

Get started with verification loops in Claude Code.

立即在 Claude Code 中开始使用验证循环。

This article was written by Delba de Oliveira, a member of the Claude Code team.

本文由 Claude Code 团队成员 Delba de Oliveira 撰写。
