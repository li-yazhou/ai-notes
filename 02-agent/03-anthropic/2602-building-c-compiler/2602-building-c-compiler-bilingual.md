# 用一队并行的 Claude 构建 C 编译器（中英对照）

> **原文标题：** Building a C compiler with a team of parallel Claudes
> **作者：** Nicholas Carlini（Anthropic Safeguards 团队）
> **原文链接：** https://www.anthropic.com/engineering/building-c-compiler
> **发布日期：** 2026-02-05
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

*Written by Nicholas Carlini, a researcher on our Safeguards team.*

本文作者为 Nicholas Carlini，我们 Safeguards（安全防护）团队的研究员。

I've been experimenting with a new approach to supervising language models that we're calling "agent teams."

我一直在实验一种监督语言模型的新方法，我们称之为"Agent 团队"（agent teams）。

With agent teams, multiple Claude instances work in parallel on a shared codebase without active human intervention. This approach dramatically expands the scope of what's achievable with LLM agents.

在 Agent 团队中，多个 Claude 实例在没有主动人工干预的情况下，并行地在同一个共享代码库上工作。这种方法极大地扩展了 LLM Agent 所能实现的范围。

To stress test it, I tasked 16 agents with writing a Rust-based C compiler, from scratch, capable of compiling the Linux kernel. Over nearly 2,000 Claude Code sessions and $20,000 in API costs, the agent team produced a 100,000-line compiler that can build Linux 6.9 on x86, ARM, and RISC-V.

为了对它做压力测试，我让 16 个 Agent 从零开始编写一个基于 Rust 的 C 编译器，要求它能够编译 Linux 内核。在近 2,000 次 Claude Code 会话、20,000 美元的 API 成本之后，这个 Agent 团队产出了一个 10 万行的编译器，能够在 x86、ARM 和 RISC-V 上构建 Linux 6.9。

[The compiler is an interesting artifact](https://github.com/anthropics/claudes-c-compiler) on its own, but I focus here on what I learned about designing harnesses for long-running autonomous agent teams: how to write tests that keep agents on track without human oversight, how to structure work so multiple agents can make progress in parallel, and where this approach hits its ceiling.

[这个编译器本身就是一个有趣的产物](https://github.com/anthropics/claudes-c-compiler)，但在这里我重点想讲的是，关于为长时运行的自主 Agent 团队设计 harness，我学到了什么：如何编写测试让 Agent 在无人监督的情况下保持正轨，如何组织工作让多个 Agent 能够并行推进，以及这种方法在什么地方触到天花板。

# 让 Claude 能够长时运行（Enabling long-running Claudes）

Existing agent scaffolds like Claude Code require an operator to be online and available to work jointly. If you ask for a solution to a long and complex problem, the model may solve part of it, but eventually it will stop and wait for continued input—a question, a status update, or a request for clarification.

像 Claude Code 这样的现有 Agent 脚手架（scaffold）要求操作者在线并随时可参与协同工作。如果你要求解决一个又长又复杂的问题，模型可能会解决其中一部分，但最终它会停下来等待持续输入——一个问题、一次状态更新，或者一个澄清请求。

To elicit sustained, autonomous progress, I built a harness that sticks Claude in a simple loop (if you've seen Ralph-loop, this should look familiar). When it finishes one task, it immediately picks up the next. *(Run this in a container, not your actual machine).*

为了引出持续、自主的进展，我构建了一个把 Claude 套进简单循环的 harness（如果你见过 Ralph-loop，这个看起来应该很眼熟）。每当它完成一个任务，就立刻接手下一个。*（请在容器里运行，而不是在你的真实机器上。）*

```bash
#!/bin/bash

while true; do
    COMMIT=$(git rev-parse --short=6 HEAD)
    LOGFILE="agent_logs/agent_${COMMIT}.log"

    claude --dangerously-skip-permissions \
           -p "$(cat AGENT_PROMPT.md)" \
           --model claude-opus-X-Y &> "$LOGFILE"
done
```

In the agent prompt, I tell Claude what problem to solve and ask it to approach the problem by breaking it into small pieces, tracking what it's working on, figuring out what to work on next, and to effectively keep going until it's perfect. (On this last point, Claude has no choice. The loop runs forever—although in one instance, I did see Claude `pkill -9 bash` on accident, thus killing itself and ending the loop. Whoops!).

在 Agent 提示词中，我告诉 Claude 要解决什么问题，并要求它通过把问题拆成小块来处理它，记录自己正在做什么、想清楚下一步做什么，并实际上一直坚持到完美为止。（关于最后一点，Claude 别无选择。这个循环会永远运行下去——尽管有一次，我确实看到 Claude 意外地 `pkill -9 bash`，从而杀死了自己、结束了循环。哎呀！）。

# 并行运行 Claude（Running Claude in parallel）

Running multiple instances in parallel can address two weaknesses of a single-agent harness:

并行运行多个实例可以弥补单 Agent harness 的两个弱点：

- One Claude Code session can only do one thing at a time. Especially as the scope of a project expands, debugging multiple issues in parallel is far more efficient.
- 一个 Claude Code 会话一次只能做一件事。尤其是随着项目范围扩大，并行调试多个问题要高效得多。

- Running multiple Claude agents allows for specialization. While a few agents are tasked to solve the actual problem at hand, other specialized agents can be invoked to (for example) maintain documentation, keep an eye on code quality, or solve specialized sub-tasks.
- 运行多个 Claude Agent 可以实现专业化分工。当少数几个 Agent 被派去解决眼前实际的问题时，其他专门的 Agent 可以被调用来（例如）维护文档、盯着代码质量，或者解决专门的子任务。

My implementation of parallel Claude is bare-bones. A new bare git repo is created, and for each agent, a Docker container is spun up with the repo mounted to `/upstream`. Each agent clones a local copy to `/workspace`, and when it's done, pushes from its own local container to upstream.

我的并行 Claude 实现非常简陋。我会创建一个新的裸 git 仓库（bare git repo），并为每个 Agent 启动一个 Docker 容器，把仓库挂载到 `/upstream`。每个 Agent 把本地副本克隆到 `/workspace`，完成后，从它自己的本地容器推送到 upstream。

To prevent two agents from trying to solve the same problem at the same time, the harness uses a simple synchronization algorithm:

为了防止两个 Agent 同时尝试解决同一个问题，harness 使用了一个简单的同步算法：

1. Claude takes a "lock" on a task by writing a text file to current_tasks/ (e.g., one agent might lock current_tasks/parse_if_statement.txt, while another locks current_tasks/codegen_function_definition.txt). If two agents try to claim the same task, git's synchronization forces the second agent to pick a different one.
2. Claude 通过向 current_tasks/ 写入一个文本文件来"锁定"（lock）某个任务（例如，一个 Agent 可能锁定 current_tasks/parse_if_statement.txt，而另一个锁定 current_tasks/codegen_function_definition.txt）。如果两个 Agent 试图认领同一个任务，git 的同步机制会迫使第二个 Agent 改选另一个。

3. Claude works on the task, then pulls from upstream, merges changes from other agents, pushes its changes, and removes the lock. Merge conflicts are frequent, but Claude is smart enough to figure that out.
4. Claude 处理该任务，然后从 upstream 拉取，合并其他 Agent 的变更，推送自己的变更，并移除锁。合并冲突很常见，但 Claude 足够聪明，能处理好。

5. The infinite agent-generation-loop spawns a new Claude Code session in a fresh container, and the cycle repeats.
6. 那个无限的 Agent 生成循环会在一个全新的容器中启动一个新的 Claude Code 会话，然后循环重复。

This is a very early research prototype. I haven't yet implemented any other method for communication between agents, nor do I enforce any process for managing high-level goals. I don't use an orchestration agent.

这是一个非常早期的研究原型。我还没有实现任何其他 Agent 之间的通信方式，也没有强制任何管理高层目标的流程。我不使用编排 Agent（orchestration agent）。

Instead, I leave it up to each Claude agent to decide how to act. In most cases, Claude picks up the "next most obvious" problem. When stuck on a bug, Claude will often maintain a running doc of failed approaches and remaining tasks. In the [git repository](https://github.com/anthropics/claudes-c-compiler) of the project, you can read through the history and watch it take out locks on various tasks.

相反，我把行动的决定权留给每个 Claude Agent 自己。在大多数情况下，Claude 会接手"下一个最显而易见的"问题。当被一个 bug 卡住时，Claude 往往会维护一份不断更新的文档，记录失败的方法和剩余的任务。在该项目的 [git 仓库](https://github.com/anthropics/claudes-c-compiler)里，你可以通读历史，看着它在各种任务上加锁。

# 与 Claude Agent 团队一起编程的经验（Lessons from programming with Claude agent teams）

The scaffolding runs Claude in a loop, but that loop is only useful if Claude can tell how to make progress. Most of my effort went into designing the environment around Claude—the tests, the environment, the feedback—so that it could orient itself without me. These are the approaches I've found most helpful when orchestrating multiple Claude instances.

脚手架让 Claude 在一个循环中运行，但只有当 Claude 能明白如何取得进展时，这个循环才有用。我的大部分精力都花在设计 Claude 周围的环境上——测试、环境、反馈——让它在没有我的情况下也能自我定位。以下是我在编排多个 Claude 实例时发现最有用的方法。

## 编写极高品质的测试（Write extremely high-quality tests）

Claude will work autonomously to solve whatever problem I give it. So it's important that the task verifier is nearly perfect, otherwise Claude will solve the wrong problem. Improving the testing harness required finding high-quality compiler test suites, writing verifiers and build scripts for open-source software packages, and watching for mistakes Claude was making, then designing new tests as I identified those failure modes.

Claude 会自主地解决我给它的任何问题。因此，任务验证器（verifier）必须近乎完美，否则 Claude 就会解决错误的问题。改进测试 harness 需要：找到高质量的编译器测试套件、为开源软件包编写验证器和构建脚本、留意 Claude 正在犯的错误，然后在我识别出这些失败模式时设计新的测试。

For example, near the end of the project, Claude started to frequently break existing functionality each time it implemented a new feature. To address this, I built a continuous integration pipeline and implemented stricter enforcement that allowed Claude to better test its work so that new commits can't break existing code.

例如，在项目接近尾声时，Claude 开始频繁地在实现每个新功能时破坏已有功能。为了解决这个问题，我构建了一条持续集成（CI）流水线，并实施了更严格的强制机制，让 Claude 能够更好地测试自己的工作，使新提交不会破坏已有代码。

## 站在 Claude 的立场上思考（Put yourself in Claude's shoes）

I had to constantly remind myself that I was writing this test harness for Claude and not for myself, which meant rethinking many of my assumptions about how tests should communicate results.

我必须不断提醒自己：我是为 Claude、而不是为我自己写这个测试 harness，这意味着要重新思考我关于"测试应该如何传达结果"的许多假设。

For example, each agent is dropped into a fresh container with no context and will spend significant time orienting itself, especially on large projects. Before we even reach the tests, to help Claude help itself, I included instructions to maintain extensive READMEs and progress files that should be updated frequently with the current status.

例如，每个 Agent 都会被丢进一个没有上下文的全新容器，并会花相当多的时间自我定位，尤其是在大型项目上。在还没到测试阶段之前，为了帮助 Claude 自助，我在指令中要求维护详尽的 README 和进度文件，并频繁更新当前状态。

I also kept in mind the fact that language models have inherent limitations, which, in this case, needed to be designed around. These include:

我还牢记一个事实：语言模型有固有的局限，而在这种情况下，这些局限需要在设计中绕过去。它们包括：

- **Context window pollution:** The test harness should not print thousands of useless bytes. At most, it should print a few lines of output and log all important information to a file so Claude can find it when needed. Logfiles should be easy to process automatically: if there are errors, Claude should write ERROR and put the reason on the same line so grep will find it. It helps to pre-compute aggregate summary statistics so Claude doesn't have to recompute them.
- **上下文窗口污染（Context window pollution）：**测试 harness 不应打印数千字节的无用内容。它最多应该打印几行输出，并把所有重要信息记入文件，以便 Claude 在需要时能找到。日志文件应该易于自动处理：如果有错误，Claude 应该写上 ERROR，并把原因放在同一行，这样 grep 就能找到它。预先计算聚合的汇总统计也很有帮助，这样 Claude 就不必重新计算它们。

- **Time blindness:** Claude can't tell time and, left alone, will happily spend hours running tests instead of making progress. The harness prints incremental progress infrequently (to avoid polluting context) and includes a default `--fast` option that runs a 1% or 10% random sample. This subsample is deterministic per-agent but random across VMs, so Claude still covers all files but each agent can perfectly identify regressions.
- **时间盲（Time blindness）：**Claude 无法感知时间，如果放任不管，它会乐呵呵地花几个小时跑测试，而不是取得进展。harness 不频繁地打印增量进度（以避免污染上下文），并带有一个默认的 `--fast` 选项，运行 1% 或 10% 的随机样本。这个子样本对每个 Agent 是确定性的，但在不同 VM 之间是随机的，所以 Claude 仍然能覆盖所有文件，而每个 Agent 都能完美地识别回归（regression）。

## 让并行变得容易（Make parallelism easy）

When there are many distinct failing tests, parallelization is trivial: each agent picks a different failing test to work on. After the test suite reached a 99% pass rate, each agent worked on getting a different small open-source project (e.g., SQlite, Redis, libjpeg, MQuickJS, Lua) to compile.

当有大量各不相同、各自失败的测试时，并行化是轻而易举的：每个 Agent 挑选一个不同的失败测试来处理。在测试套件达到 99% 的通过率之后，每个 Agent 负责让一个不同的小型开源项目（例如 SQlite、Redis、libjpeg、MQuickJS、Lua）能够编译。

But when agents started to compile the Linux kernel, they got stuck. Unlike a test suite with hundreds of independent tests, compiling the Linux kernel is one giant task. Every agent would hit the same bug, fix that bug, and then overwrite each other's changes. Having 16 agents running didn't help because each was stuck solving the same task.

但当 Agent 们开始编译 Linux 内核时，它们卡住了。与拥有数百个独立测试的测试套件不同，编译 Linux 内核是一个巨型任务。每个 Agent 都会撞上同一个 bug，修复那个 bug，然后覆盖彼此的更改。有 16 个 Agent 在跑也没用，因为每个都被困在解决同一个任务上。

The fix was to use [GCC](https://gcc.gnu.org/) as an online known-good compiler oracle to compare against. I wrote a new test harness that randomly compiled most of the kernel using GCC, and only the remaining files with Claude's C Compiler. If the kernel worked, then the problem wasn't in Claude's subset of the files. If it broke, then it could further refine by re-compiling some of these files with GCC. This let each agent work in parallel, fixing different bugs in different files, until Claude's compiler could eventually compile all files. (After this worked, it was still necessary to apply delta debugging techniques to find pairs of files that failed together but worked independently.)

解决办法是使用 [GCC](https://gcc.gnu.org/) 作为一个在线的"已知良好"编译器预言机（oracle）来对照。我编写了一个新的测试 harness，它随机地用 GCC 编译内核的大部分文件，只对剩余文件使用 Claude 的 C 编译器。如果内核正常工作，那么问题就不在 Claude 负责的那部分文件里。如果它坏了，就可以用 GCC 重新编译其中一些文件来进一步缩小范围。这让每个 Agent 都能并行工作，修复不同文件中的不同 bug，直到 Claude 的编译器最终能够编译所有文件。（在这奏效之后，仍然有必要运用增量调试（delta debugging）技术，找出那些"合在一起会失败、单独却能成功"的文件对。）

## 多种 Agent 角色（Multiple agent roles）

Parallelism also enables specialization. LLM-written code frequently re-implements existing functionality, so I tasked one agent with coalescing any duplicate code it found. I put another in charge of improving the performance of the compiler itself, and a third I made responsible for outputting efficient compiled code. I asked another agent to critique the design of the project from the perspective of a Rust developer, and make structural changes to the project to improve the overall code quality, and another to work on documentation.

并行还实现了专业化。LLM 编写的代码经常重复实现已有功能，所以我让一个 Agent 负责合并它发现的任何重复代码。我让另一个 Agent 负责提升编译器本身的性能，第三个负责产出高效的编译代码。我还让一个 Agent 从 Rust 开发者的角度对项目设计提出批评，并对项目做出结构性改动以提升整体代码质量，另有一个 Agent 负责文档。

# 对 Agent 团队的极限做压力测试（Stress testing the limits of agent teams）

This project was designed as a capability benchmark. I am interested in stress-testing the limits of what LLMs can just *barely* achieve today in order to help us prepare for what models will reliably achieve in the future.

这个项目被设计成一个能力基准测试（capability benchmark）。我感兴趣的是，对 LLM 今天*勉强*能够做到的事情的极限进行压力测试，以帮助我们为模型在未来将可靠做到的事情做好准备。

I've been using the C Compiler project as a benchmark across the entire Claude 4 model series. As I did with prior projects, I started by drafting what I wanted: a from-scratch optimizing compiler with no dependencies, GCC-compatible, able to compile the Linux kernel, and designed to support multiple backends. While I specified some aspects of the design (e.g., that it should have an SSA IR to enable multiple optimization passes) I did not go into any detail on how to do so.

我一直在把 C 编译器项目当作横跨整个 Claude 4 模型系列的基准测试。和之前项目一样，我从起草我想要的东西开始：一个从零开始、无依赖、兼容 GCC、能够编译 Linux 内核、并设计为支持多个后端的优化编译器。虽然我指定了设计的某些方面（例如，它应该有一个 SSA 中间表示以支持多个优化 pass），但我没有就如何实现给出任何细节。

Previous Opus 4 models were barely capable of producing a functional compiler. Opus 4.5 was the first to cross a threshold that allowed it to produce a functional compiler which could pass large test suites, but it was still incapable of compiling any real large projects. My goal with Opus 4.6 was to again test the limits.

此前的 Opus 4 模型几乎不具备产出可用编译器的能力。Opus 4.5 是第一个跨过某一门槛的模型，它能够产出一个能通过大型测试套件的可用编译器，但仍无法编译任何真实的大型项目。我用 Opus 4.6 的目标，是再次测试极限。

## 评估（Evaluation）

Over nearly 2,000 Claude Code sessions across two weeks, Opus 4.6 consumed 2 billion input tokens and generated 140 million output tokens, a total cost just under $20,000. Compared to even the most expensive Claude Max plans, this was an extremely expensive project. But that total is a fraction of what it would cost me to produce this myself—let alone an entire team.

在两周、近 2,000 次 Claude Code 会话中，Opus 4.6 消耗了 20 亿输入令牌，生成了 1.4 亿输出令牌，总成本略低于 20,000 美元。即便与最昂贵的 Claude Max 套餐相比，这也是一个极其昂贵的项目。但这一总额，只是我独自产出这一切所需成本的一小部分——更不用说一个完整团队了。

This was a clean-room implementation (Claude did not have internet access at any point during its development); it depends only on the Rust standard library. The 100,000-line compiler can build a bootable Linux 6.9 on x86, ARM, and RISC-V. It can also compile QEMU, FFmpeg, SQlite, postgres, redis, and has a 99% pass rate on most compiler test suites including the [GCC torture test suite](https://gcc.gnu.org/onlinedocs/gccint/Torture-Tests.html). It also passes the developer's ultimate litmus test: it can compile and run Doom.

这是一次净室（clean-room）实现（Claude 在开发过程中的任何时刻都无法访问互联网）；它只依赖 Rust 标准库。这个 10 万行的编译器能够在 x86、ARM 和 RISC-V 上构建可启动的 Linux 6.9。它还能编译 QEMU、FFmpeg、SQlite、postgres、redis，并且在包括 [GCC torture 测试套件](https://gcc.gnu.org/onlinedocs/gccint/Torture-Tests.html)在内的大多数编译器测试套件上有 99% 的通过率。它还通过了开发者的终极试金石测试：它能够编译并运行 Doom。

The compiler, however, is not without limitations. These include:

然而，这个编译器并非没有局限。它们包括：

- It lacks the 16-bit x86 compiler that is necessary to boot Linux out of real mode. For this, it calls out to GCC (the x86_32 and x86_64 compilers are its own).
- 它缺少从实模式（real mode）启动 Linux 所必需的 16 位 x86 编译器。为此，它需要调用 GCC（x86_32 和 x86_64 编译器是它自己的）。

- It does not have its own assembler and linker; these are the very last bits that Claude started automating and are still somewhat buggy. The demo video was produced with a GCC assembler and linker.
- 它没有自己的汇编器和链接器；这些是 Claude 最后开始自动化的部分，仍然有点 buggy。演示视频是用 GCC 的汇编器和链接器制作的。

- The compiler successfully builds many projects, but not all. It's not yet a drop-in replacement for a real compiler.
- 这个编译器能成功构建许多项目，但不是全部。它还不能成为真正编译器的即插即用替代品。

- The generated code is not very efficient. Even with all optimizations enabled, it outputs less efficient code than GCC with all optimizations *disabled.*
- 生成的代码效率不高。即使开启所有优化，它输出的代码也不如*关闭*所有优化的 GCC 高效。

- The Rust code quality is reasonable, but is nowhere near the quality of what an expert Rust programmer might produce.
- Rust 代码的质量还算合理，但远不及一位资深 Rust 程序员可能产出的质量。

The resulting compiler has nearly reached the limits of Opus's abilities. I tried (hard!) to fix several of the above limitations but wasn't fully successful. New features and bugfixes frequently broke existing functionality.

这个最终产出的编译器已经几乎触及 Opus 能力的极限。我非常（非常！）努力地想修复上述几个局限，但没有完全成功。新功能和 bug 修复经常破坏已有的功能。

As one particularly challenging example, Opus was unable to implement a 16-bit x86 code generator needed to boot into 16-bit real mode. While the compiler can output correct 16-bit x86 via the 66/67 opcode prefixes, the resulting compiled output is over 60kb, far exceeding the 32k code limit enforced by Linux. Instead, Claude simply cheats here and calls out to GCC for this phase (This is only the case for x86. For ARM or RISC-V, Claude's compiler can compile completely by itself.)

举一个特别有挑战性的例子：Opus 无法实现启动到 16 位实模式所需的 16 位 x86 代码生成器。虽然编译器可以通过 66/67 操作码前缀输出正确的 16 位 x86 代码，但编译后的输出超过 60kb，远远超出 Linux 强制执行的 32k 代码上限。于是，Claude 干脆在这里作弊，为这个阶段调用 GCC（这仅限于 x86。对于 ARM 或 RISC-V，Claude 的编译器完全可以独立完成编译）。

The [source code for the compiler is available](https://github.com/anthropics/claudes-c-compiler). Download it, read through the code, and try it on your favorite C projects. I've consistently found the best way to understand what language models can do is to push them to their limits, and then study where they start to break down. Over the coming days, I'll continue having Claude push new changes if you want to follow along with Claude's continued attempts at addressing these limitations.

[这个编译器的源代码是公开可用的](https://github.com/anthropics/claudes-c-compiler)。下载它，通读代码，并在你最喜欢的 C 项目上试一试。我始终发现，理解语言模型能做什么的最好方式，就是把它们推到极限，然后研究它们开始崩溃的地方。在接下来的日子里，我会继续让 Claude 推送新的改动——如果你想跟踪 Claude 持续尝试解决这些局限的过程。

# 展望未来（Looking forward）

Each generation of language models opens up new ways of working with them. Early models were useful for tab-completion in IDEs. Before long, models could complete a function body from its docstring. The launch of Claude Code brought agents into the mainstream and enabled developers to pair-program with Claude. But each of these products operates under the assumption that a user defines a task, an LLM runs for a few seconds or minutes and returns an answer, and then the user provides a follow-up.

每一代语言模型都会开启与其协作的新方式。早期的模型对 IDE 中的制表补全（tab-completion）有用。没过多久，模型就能根据 docstring 补全函数体。Claude Code 的发布把 Agent 带入了主流，让开发者能够与 Claude 结对编程。但这些产品都运行在一个假设之下：用户定义一个任务，LLM 运行几秒或几分钟并返回答案，然后用户再提供后续输入。

Agent teams show the possibility of implementing entire, complex projects autonomously. This allows us, as users of these tools, to become more ambitious with our goals.

Agent 团队展示了自主实现完整复杂项目的可能性。这让我们作为这些工具的用户，能够对自己的目标变得更加雄心勃勃。

We are still early, and fully autonomous development comes with real risks. When a human sits with Claude during development, they can ensure consistent quality and catch errors in real time. For autonomous systems, it is easy to see tests pass and assume the job is done, when this is rarely the case. I used to work in penetration testing, exploiting vulnerabilities in products produced by large companies, and the thought of programmers deploying software they've never personally verified is a real concern.

我们仍然处于早期阶段，而完全自主的开发伴随着真实的风险。当一个人在开发过程中与 Claude 并肩工作时，他们可以确保质量一致，并实时发现错误。对于自主系统，人们很容易看到测试通过就假定工作完成了，而现实很少如此。我以前从事渗透测试工作，利用大公司产品中的漏洞，想到程序员要部署他们从未亲自验证过的软件，这确实是一个令人担忧的问题。

So, while this experiment excites me, it also leaves me feeling uneasy. Building this compiler has been some of the most fun I've had recently, but I did not expect this to be anywhere near possible so early in 2026. The rapid progress in both language models and the scaffolds we use to interact with them opens the door to writing an enormous amount of new code. I expect the positive applications to outweigh the negative, but we're entering a new world which will require new strategies to navigate safely.

所以，虽然这个实验让我兴奋，它也让我感到不安。构建这个编译器是我最近最有乐趣的事之一，但我没想到 2026 年这么早就能接近这种可能。语言模型和我们用来与之交互的脚手架都在快速进步，这为编写海量新代码打开了大门。我预期积极的应用会超过消极的，但我们将进入一个需要新策略才能安全航行的新世界。

## 致谢（Acknowledgements）

Special thanks to Josef Bacik, Edwin Chen, Bernardo Meurer Costa, Jake Eaton, Dan Kelley, Felix Klock, Jannet Park, Steve Weis, and many other people across Anthropic for their assistance and contributions.

特别感谢 Josef Bacik、Edwin Chen、Bernardo Meurer Costa、Jake Eaton、Dan Kelley、Felix Klock、Jannet Park、Steve Weis，以及 Anthropic 内部许多其他人为本项目提供的协助与贡献。
