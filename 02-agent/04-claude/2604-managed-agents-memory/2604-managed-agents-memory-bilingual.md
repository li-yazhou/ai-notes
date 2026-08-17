# Claude Managed Agents 的内置记忆（中英对照）

> **原文标题：** Built-in memory for Claude Managed Agents
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/claude-managed-agents-memory
> **发布日期：** 2026-04-23
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Memory for Claude Managed Agents is a built-in memory layer that lets agents learn across sessions, improve over time, and share what they've learned.

Claude Managed Agents 的 Memory（记忆）是一个内置记忆层，让智能体能够跨会话学习、随时间不断改进，并共享所学。

Memory on Claude Managed Agents is available today in public beta. Your agents can now learn from every session, using an intelligence-optimized memory layer that balances performance with flexibility. Because memories are stored as files, developers can export them, manage them via the API, and keep full control over what agents retain.

Claude Managed Agents 的 Memory 从今天起开放公测（public beta）。你的智能体现在可以从每一次会话中学习，依托一个在性能与灵活性之间取得平衡、针对智能水平优化的记忆层。由于记忆以文件形式存储，开发者可以导出它们、通过 API 管理它们，并完全掌控智能体记住的内容。

![Memory 功能示意图](images/mamem-1.png)

# Claude Managed Agents 中的记忆如何运作（How memory works in Claude Manged Agents）

Memory for Claude Managed Agents is a built-in, intelligence-optimized memory layer that lets agents learn from every session. Memory is optimized against internal benchmarks for long-running agents that improve across sessions and share what they've learned with each other.

Claude Managed Agents 的 Memory 是一个内置的、针对智能水平优化的记忆层，让智能体从每一次会话中学习。Memory 依据内部基准进行了优化，目标是让长时间运行的智能体能够跨会话改进，并彼此共享所学。

We've found that agents are most effective with memory when it builds on the tools they already use. Memory on Claude Managed Agents mounts directly onto a filesystem, so Claude can rely on the same bash and code execution capabilities that make it effective at agentic tasks. With filesystem-based memory, our latest models save more comprehensive, well-organized memories and are more discerning about what to remember for a given task.

我们发现，当记忆建立在智能体已有的工具之上时，效果最好。Claude Managed Agents 的 Memory 直接挂载（mount）到文件系统上，因此 Claude 可以依赖让它擅长智能体任务的同一套 bash 和代码执行能力。有了基于文件系统的记忆，我们最新的模型会保存更全面、更有条理的记忆，也更善于甄别特定任务该记住什么。

# 面向生产级智能体的可移植记忆（Portable memories for production-grade agents）

Memory is built for enterprise deployments, with scoped permissions, audit logs, and full programmatic control. Stores can be shared across multiple agents with different access scopes. For example, an org-wide store might be read-only, while per-user stores allow reads and writes. Multiple agents can work concurrently against the same store without overwriting each other.

Memory 为企业级部署而生，具备范围化权限（scoped permissions）、审计日志（audit log）和完整的程序化控制。记忆存储库（store）可以在多个智能体之间以不同的访问范围共享。例如，组织级存储库可以设为只读，而用户级存储库允许读写。多个智能体可以并发操作同一个存储库，而不会相互覆盖。

Memories are files that can be exported and independently managed via the API, giving developers full control. All changes are tracked with a detailed audit log, so you can tell which agent and session a memory came from. You can roll back to an earlier version or redact content from history. Updates also surface in the Claude Console as session events, so developers can trace what an agent learned and where it came from.

记忆是文件，可以导出并通过 API 独立管理，开发者因此拥有完全的控制权。所有变更都有详细的审计日志记录，你可以知道每条记忆来自哪个智能体、哪次会话。你可以回滚到较早版本，或从历史中抹除敏感内容（redact）。更新还会作为会话事件显示在 Claude Console 中，开发者可以追溯智能体学到了什么、来自哪里。

# 各团队正在构建什么（What teams are building）

Teams have been using memory to close feedback loops, speed up verification, and replace custom retrieval infrastructure:

各团队已经在用 Memory 闭合反馈回路、加速验证，并替换自建的检索基础设施：

- Netflix agents carry context across sessions, including insights that took multiple turns to uncover and corrections from a human mid-conversation, instead of manually updating prompts and skills.
- Rakuten's task-based long-running agents use memory to learn from every session and avoid repeating past mistakes, cutting first-pass errors by 97%, all within workspace-scoped, observable boundaries.
- Wisedocs built their document verification pipeline on Managed Agents, using cross-session memory to spot and remember recurring document issues, speeding up verification by 30%.‍
- Ando is building their workplace messaging platform on Managed Agents, capturing how each organization interacts instead of building memory infrastructure themselves.

- Netflix 的智能体跨会话携带上下文，包括需要多轮才能挖出的洞察，以及对话中途来自人类的纠正，而无需手动更新提示词和 Skills（技能）。
- Rakuten 的任务型长时运行智能体利用记忆从每次会话中学习，避免重蹈覆辙，将首轮错误率降低了 97%，且全部处于工作区范围限定、可观测的边界之内。
- Wisedocs 把文档验证流水线构建在 Managed Agents 之上，利用跨会话记忆发现并记住反复出现的文档问题，验证速度提升了 30%。‍
- Ando 正在基于 Managed Agents 构建其职场通讯平台，记录每个组织的互动方式，而不必自建记忆基础设施。

![公司 Logo](images/mamem-2.svg)

![公司 Logo](images/mamem-3.svg)

Memory in Claude Managed Agents lets us put continuous learning into production at scale. Our agents distill lessons from every session, delivering 97% fewer first-pass errors at 27% lower cost and 34% lower latency, so users spend less time nudging agents to fix mistakes the system has already learned to avoid. And because memory is workspace-scoped and observable, continuous learning stays under our control.

Claude Managed Agents 中的 Memory 让我们得以把持续学习大规模投入生产。我们的智能体从每次会话中提炼经验，首轮错误减少 97%，成本降低 27%，延迟降低 34%，用户不用再花时间催促智能体去修复系统早已学会避免的错误。而且由于记忆以工作区为范围且可观测，持续学习始终处于我们的掌控之中。

![公司 Logo](images/mamem-4.svg)

![公司 Logo](images/mamem-5.svg)

A lot of our work at Ando is making sense of fast-moving, messy conversations between teams and their agents. Memory lets us stop building memory infra and focus on the product itself.

我们在 Ando 的很多工作，是理清团队与其智能体之间那些快速变化、杂乱无章的对话。Memory 让我们不必再自建记忆基础设施，可以专注于产品本身。

![公司 Logo](images/mamem-6.svg)

![公司 Logo](images/mamem-7.svg)

A good memory API gets rid of many infrastructure headaches, especially when building across agents and sessions. In our document verification pipeline on Claude Managed Agents, we used cross-session memory to let our agents identify and remember common issues — including ones we didn't think about. It's sped verification up 30%.

一个好的记忆 API 能省去许多基础设施烦恼，尤其是在跨智能体、跨会话构建时。在 Claude Managed Agents 上的文档验证流水线中，我们利用跨会话记忆让智能体识别并记住常见问题--包括那些我们没想到的问题。它让验证速度提升了 30%。

# 开始使用（Getting started）

Memory on Managed Agents is now available in public beta on the Claude Platform. Visit the Claude Console or use our new CLI to deploy your first agent with memory. Explore the documentation to learn more.

Managed Agents 的 Memory 现已在 Claude 平台上开放公测。前往 Claude Console，或使用我们的新 CLI 部署你的第一个带记忆的智能体。查阅文档了解更多。
