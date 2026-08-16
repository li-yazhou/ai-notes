# 循环工程：循环入门（中英对照）

> **原文标题：** Loop engineering: Getting started with loops
> **作者：** Delba de Oliveira、Michael Segner
> **原文链接：** https://claude.com/blog/getting-started-with-loops
> **发布日期：** 2026-06-30
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Loop engineering with Anthropic's Claude Code: design turn-based, goal, time, and proactive agent loops that run to a stop condition.

用 Anthropic 的 Claude Code 做循环工程（loop engineering）：设计基于回合（turn-based）、目标（goal）、时间（time）和主动（proactive）的智能体循环，让它们一直运行到满足停止条件。

Learn how the Claude Code team defines agentic loops, with practical guidance on progressing from turn-based to goal-based, time-based, and proactive loops-and when to use each.

了解 Claude Code 团队如何定义智能体循环（agentic loop），并获得从回合制循环进阶到基于目标、基于时间和主动式循环的实用指南--以及各自适用的时机。

# 循环入门（Getting started with loops）

There's a lot of talk right now about loop engineering or "designing loops" instead of prompting your coding agent. If you spend some time on X trying to pin down what a loop actually is, you'll come across multiple different answers.

眼下有很多关于循环工程（loop engineering）、即用"设计循环"取代直接给你的编码智能体写提示词的讨论。如果你在 X 上花点时间想弄清楚循环到底是什么，会看到五花八门的答案。

On the Claude Code team, we define loops as agents repeating cycles of work until a stop condition is met. We categorize a few different types of loops based on:

在 Claude Code 团队，我们把循环定义为：智能体重复执行工作周期，直到满足停止条件。我们基于以下几点把循环划分为几种不同类型：

- How they are triggered
- How they are stopped
- What Claude Code primitive is used
- What type of task is most appropriate for each.

- 如何触发
- 如何停止
- 使用哪种 Claude Code 原语（primitive）
- 每种循环最适合什么类型的任务。

We'll cover the main loop types, when to use each, and how to maintain code quality while managing token usage. Not all tasks require complex loops; start with the simplest solution and use these patterns selectively.

本文将介绍主要的循环类型、各自的使用时机，以及如何在管理 token 用量的同时保持代码质量。并非所有任务都需要复杂的循环；从最简单的方案开始，有选择地使用这些模式。

# 回合制循环（Turn-based loops）

![回合制循环示意图](images/loops-1.png)

- Triggered by: A user prompt.
- Stop criteria: Claude judges it has completed the task or needs additional context.
- Best used for: Shorter tasks that are not part of a regular process or schedule.
- Managed usage by: Write specific prompts and improve verification using skills to reduce the number of turns.‍

- 触发方式：用户提示词。
- 停止标准：Claude 判断任务已完成，或需要补充上下文。
- 最适用于：不属于常规流程或日程的较短任务。
- 用量管理方式：编写具体的提示词，并借助 skills 改进验证，以减少回合数。

Every prompt you send starts a manual loop with you directing each turn. Claude gathers context, takes action, checks its work, repeats if needed, and responds. We call this the agentic loop.

你发送的每一条提示词都会启动一个由你主导每一回合的手动循环：Claude 收集上下文、采取行动、检查自己的工作、必要时重复，然后做出响应。我们称之为智能体循环（agentic loop）。

For example, ask Claude to create a like button. It reads your code, makes the edit, runs the tests, and hands back something it believes works. You then manually check the work, and write the next prompt.

例如，让 Claude 创建一个点赞按钮。它会阅读你的代码、完成修改、运行测试，然后交回一个它认为可用的结果。接着你手动检查这份工作，再写下一条提示词。

You can improve the verification step by encoding your manual steps as a SKILL.md so Claude can check more of its own work, end-to-end. (For choosing between skills, hooks, and subagents for this kind of automation, see our guide to steering Claude Code.)

你可以通过把手动的验证步骤编写成 SKILL.md 来改进验证环节，让 Claude 能够端到端地检查更多自己的工作。（关于在这类自动化中如何在 skills、hooks 和 subagents 之间做选择，请参阅我们的 Claude Code 引导指南。）

This should include tools or connectors to allow Claude to see, measure or interact with the result. The more quantitative the checks are, the easier it is for Claude to self-verify.

其中应包含让 Claude 能够查看、度量或与结果交互的工具或连接器。检查越是定量化，Claude 就越容易自我验证。

For example, in your SKILL.md file you may specify:

例如，你可以在 SKILL.md 文件中写明：

```
---
name: verify-frontend-change
description: Verify any UI change end-to-end before declaring it done.
---

# Verifying frontend changes

Never report a UI change as complete based on a successful edit alone. Verify it the way a human reviewer would:

1. Start the dev server and open the edited page in the browser.
2. Interact with the change directly. For a new control (button, input, toggle): click it, confirm the expected state change, and screenshot before/after.
3. Check the browser console: zero new errors or warnings.
4. Use the Chrome Devtools MCP, run a performance trace and audit Core Web Vitals.

If any step fails, fix the issue and rerun from step 1 - do not hand back partially verified work.
```

# 基于目标的循环（Goal-based loop (/goal)）

![基于目标的循环示意图](images/loops-2.png)

- Triggered by: A manual prompt in real-time.
- Stop criteria: Goal achieved OR maximum number of turns reached.
- Best used for: Tasks that have verifiable exit criteria.
- Managed usage by: Setting a specific completion criteria and explicit turn caps, "stop after 5 tries."

- 触发方式：实时手动提示。
- 停止标准：目标达成，或达到最大回合数。
- 最适用于：具有可验证退出标准的任务。
- 用量管理方式：设定明确的完成标准和显式的回合上限，如"最多尝试 5 次后停止"。

Sometimes, a single turn is not enough, especially for more complex tasks. Agents do better when they can iterate. You can extend how long Claude keeps iterating by defining what done looks like with /goal.

有时一个回合并不够，尤其是对于更复杂的任务。智能体在能够迭代时表现更好。你可以用 /goal 定义"完成"是什么样子，从而延长 Claude 持续迭代的时间。

When you define the success criteria, Claude doesn't have to make a determination on what is "good enough" and end the loop early. Each time Claude tries to stop, an evaluator model checks your condition and sends it back to work until the goal is met or a number of turns you define is reached.

由你来定义成功标准后，Claude 就不必自行判断什么算"足够好"而提前结束循环。每当 Claude 想要停下时，评估器模型（evaluator model）会检查你设定的条件，把它送回去继续工作，直到目标达成或达到你定义的回合数。

This is why deterministic criteria, such as number of tests passed or clearing a certain score threshold, are so effective.

这就是为什么确定性标准--比如通过的测试数量、或超过某个分数阈值--如此有效。

For example:

例如：

```
/goal get the homepage Lighthouse score to 90 or above, stop after 5 tries.
```

# 基于时间的循环（Time-based loop (/loop and /schedule)）

- Triggered by: A specified time interval.
- Stop criteria: You cancel it, or the work completes (the PR merges, the queue is empty).
- Best used for: For recurring work, or interfacing with external environments / systems.
- Managed usage by: Set longer intervals or react based on events rather than time.

- 触发方式：指定的时间间隔。
- 停止标准：你手动取消，或工作完成（PR 合并了、队列清空了）。
- 最适用于：重复性工作，或与外部环境/系统交互。
- 用量管理方式：设置更长的间隔，或基于事件而非时间来响应。

Some agentic work is recurring: the task stays the same and only the inputs change. For example, summarizing Slack messages every morning. Other work depends on external systems, and a simple way to interface with one is to check it on an interval and react to what changed. For example, a PR which may receive code reviews or fail CI.

有些智能体工作是重复性的：任务不变，只有输入在变，比如每天早晨汇总 Slack 消息。另一些工作则依赖外部系统，与外部系统交互的一种简单方式就是按间隔检查它并对变化做出反应，比如一个可能收到代码评审或 CI 失败的 PR。

For these, you can trigger when Claude runs with `/loop` which re-runs a prompt on an interval. For example:

对于这类工作，你可以用 `/loop` 控制 Claude 何时运行，它会按固定间隔重新执行一条提示词。例如：

```
/loop 5m check my PR, address review comments, and fix failing CI
```

`/loop` runs on your computer, so if you turn it off, it stops. You can move the loop to the cloud by creating a routine with `/schedule`.

`/loop` 在你的电脑上运行，所以关机它就停了。你可以用 `/schedule` 创建例程（routine），把循环迁移到云端。

# 主动式循环（Proactive loops）

![主动式循环示意图](images/loops-3.png)

- Triggered by: An event or schedule, with no human in real time.
- Stop criteria: Each task exits when its goal is met. The routine itself runs until you turn it off.
- Best used for: Recurring streams of well-defined work: bug reports, issue triage, migrations, dependency upgrades, etc.
- Managed usage by: Routing routines to smaller, faster models and using the most capable model for judgment calls.

- 触发方式：事件或日程，无需真人实时参与。
- 停止标准：每个任务在达成目标后退出；例程本身一直运行，直到你关掉它。
- 最适用于：持续流入且定义清晰的工作流：缺陷报告、issue 分诊、迁移、依赖升级等。
- 用量管理方式：把例程路由到更小更快的模型，把最强的模型留给需要判断力的决策。

The primitives above, along with other Claude Code features like auto mode and dynamic workflows (research preview) can be composed into a loop for long-running work.

上述原语，连同 Claude Code 的其他特性--如 auto mode 和 dynamic workflows（research preview，研究预览）--可以组合成一个处理长期运行工作的循环。

For example, to handle incoming feedback, you can use:

例如，要处理源源不断到来的反馈，你可以使用：

- `/schedule` (research preview) to run a routine that checks for new reports
- `/goal` to define what done looks and skills to document how to verify it
- Dynamic workflows to orchestrate agents that triage each report, fix it, and review the fix
- Auto mode so the routine runs without stopping to ask for permission

- `/schedule`（research preview）：运行一个检查新报告的例程
- `/goal`：定义"完成"的样子，并用 skills 记录如何验证
- Dynamic workflows：编排智能体对每份报告进行分诊、修复并评审修复结果
- Auto mode：让例程无需停下来请求权限即可持续运行

Putting it together, a prompt could look like this:

把它们组合起来，一条提示词可以是这样的：

```
/schedule every hour: check #project-feedback for bug reports. /goal: don't stop until every report found this run is triaged, actioned, and responded to. When fixing a bug, use a workflow to explore three solutions in parallel worktrees and have a judge adversarially review them.
```

# 保持代码质量（Maintaining code quality）

The quality of a loop's output depends on the system around it. When designing the system:

循环产出的质量取决于围绕它的系统。设计这个系统时：

- Keep the codebase itself clean: Claude follows patterns and conventions that already exist in your codebase.
- Give Claude a way to verify its own work: Encode what good looks like for you and your team with skills.
- Make docs easy to reach: Frameworks and libraries docs have up-to-date best practices.
- Use a second agent for code reviews: A reviewer with fresh context is less biased and not influenced by the main agent's reasoning. You can use the built-in `/code-review` skill or Code Review for Github. Loops that write code need loops that check it - see how Anthropic secures an AI-native SDLC.

- 保持代码库本身整洁：Claude 会遵循你代码库中已有的模式和约定。
- 给 Claude 一种验证自身工作的手段：用 skills 把你和团队眼中"什么算好"编码下来。
- 让文档触手可及：框架和库的文档里有最新的最佳实践。
- 用第二个智能体做代码评审：拥有全新上下文的评审者偏见更少，也不受主智能体推理的影响。你可以使用内置的 `/code-review` skill 或 Code Review for Github。写代码的循环需要检查代码的循环--看看 Anthropic 如何保障 AI 原生 SDLC 的安全。

When an individual result doesn't meet the standard, don't stop at fixing the individual issue, try to encode it to improve the system for all future iterations.

当某次结果不达标时，不要止步于修复这一个问题，试着把它编码进系统，让未来的所有迭代都受益。

# 管理 token 用量（Managing token usage）

To manage token usage, loops should have clear boundaries:

为了管理 token 用量，循环应当有清晰的边界：

- Choose the right primitive and model for the job: Smaller tasks don't need multiple agents or loops. Some tasks can use cheaper and faster models.
- Define clear success and stop criteria: Be specific about what done looks like so Claude can arrive at the solution sooner (but not too soon).
- Pilot before a large run: Dynamic workflows can spawn hundreds of agents. Gauge usage on a smaller slice of the work first.
- Use scripts for deterministic work: Running a script is cheaper than reasoning through the steps. For example, a PDF skill can ship a form-filling script that Claude runs each time, instead of re-deriving the code.
- Don't run routines more often that you need to: Match the interval to how often the thing you're watching changes
- Review usage: The `/usage` command breaks down recent usage by skills, subagents, and MCPs, `/goal` with no arguments shows number of turns and token usage so far, `/workflows` shows each agent's token usage and you can stop an agent at any time.

- 为任务选择合适的原语和模型：小任务不需要多个智能体或循环；有些任务可以用更便宜、更快的模型。
- 定义清晰的成功与停止标准：把"完成"具体化，让 Claude 更快抵达解决方案（但也不能太快）。
- 大规模运行前先试点：Dynamic workflows 可能生成数百个智能体。先在一小片工作上估摸用量。
- 用脚本处理确定性工作：运行脚本比一步步推理便宜。例如，PDF skill 可以内置一个表单填写脚本，让 Claude 每次直接运行，而不是重新推导代码。
- 不要让例程跑得比需要的更频繁：让间隔与你所监控对象的变化频率相匹配
- 审查用量：`/usage` 命令按 skills、subagents 和 MCPs 细分近期用量；不带参数的 `/goal` 显示目前的回合数和 token 用量；`/workflows` 显示每个智能体的 token 用量，并且你随时可以停掉某个智能体。

Your model and effort level choices are among the biggest levers on what a loop costs.

模型与努力程度（effort level）的选择是决定循环成本的最大杠杆之二。

# 开始上手（Getting started）

To summarize:

总结如下：

| Loop | You hand off | Use it when | Reach for |
| --- | --- | --- | --- |
| Turn-based | The check | You're exploring or deciding | Custom verification skills |
| Goal-based | The stop condition | You know what done looks like | /goal |
| Time-based | The trigger | The work happens outside your project on a schedule | /loop, /schedule |
| Proactive | The prompt | The work is recurring and well-defined | All of the above, and dynamic workflows |

| 循环类型 | 你交出的部分 | 适用场景 | 使用的工具 |
| --- | --- | --- | --- |
| 回合制（Turn-based） | 检查验证 | 你在探索或做决策 | 定制验证 skills |
| 基于目标（Goal-based） | 停止条件 | 你知道"完成"是什么样子 | /goal |
| 基于时间（Time-based） | 触发时机 | 工作按日程在你的项目之外发生 | /loop、/schedule |
| 主动式（Proactive） | 提示词 | 工作重复且定义清晰 | 以上全部，以及 dynamic workflows |

To get started with loops, look at the work you already do. Pick one task where you're the bottleneck and ask which piece you could hand off: can you write the verification check? Is the goal clear enough? Does the work arrive on a schedule?

要开始使用循环，先审视你已经在做的工作。挑一件你自己是瓶颈的任务，问问哪一部分可以交出去：你能写出验证检查吗？目标足够清晰吗？这项工作会按日程到来吗？

Once you have an idea, run the loop, observe the results like where it stalls or over-reaches, and don't be afraid to iterate on it.

有了想法之后，运行循环，观察结果--比如它在哪里卡住或用力过猛--并且不要害怕对它进行迭代。

For more information, read the Claude Code docs on running agents in parallel, as well as the loop, schedule, goal, and dynamic workflows pages. To make your checks repeatable across sessions, see building verification loops in Claude Code with skills.

更多信息请阅读 Claude Code 文档中关于并行运行智能体的部分，以及 loop、schedule、goal 和 dynamic workflows 页面。想让你的检查跨会话可复用，请参阅"用 skills 在 Claude Code 中构建验证循环"一文。

This article was written by Delba de Oliveira and Michael Segner

本文由 Delba de Oliveira 和 Michael Segner 撰写。
