# Claude Tag 中的智能体身份：面向自主、团队级 AI 的新型访问模型（中英对照）

> **原文标题：** Agent identity in Claude Tag: a new access model for autonomous, team-wide AI
> **作者：** Noah Zweben, a member of technical staff on the Claude Code team（Claude Code 团队技术成员）
> **原文链接：** https://claude.com/blog/agent-identity-access-model
> **发布日期：** 2026-06-24
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

How Claude Tag's agent identity access model works, and best practices for configuring it in your team's workspace.

Claude Tag 的智能体身份（agent identity）访问模型如何运作，以及在你团队的工作区中配置它的最佳实践。

For an AI agent to do its best work on a human-agent team, it needs access to the same tools, documents, and context humans have.

要让 AI 智能体在人机协作团队中发挥最佳水平，它需要访问与人类相同的工具、文档和上下文。

In a "single player" AI experience (where one person chats with one assistant), that's straightforward: you connect your own accounts and the agent acts on your behalf. But in a "multiplayer" AI experience like Claude Tag, Claude sits in a shared channel alongside many people at once, and it draws on the tools and context that belong to the workspace, rather than any one individual.

在"单人"（single player）AI 体验中（一个人与一个助手对话），这很简单：你连接自己的账户，智能体代表你行事。但在 Claude Tag 这样的"多人"（multiplayer）AI 体验中，Claude 同时与许多人一起身处共享频道，它调用的是属于工作区而非任何个人的工具和上下文。

To make multiplayer experiences work, Claude needs its own accounts for those tools, set up by an admin and tied to the workspace. We call this access model agent identity.

要让多人体验成立，Claude 需要在这些工具上拥有自己的账户，由管理员设置并与工作区绑定。我们称这种访问模型为智能体身份（agent identity）。

In this post, we explain how agent identity works, how it moves permissions from per-user to per-channel, and how to scope it well in your own workspace.

在这篇文章中，我们将解释智能体身份如何运作、它如何把权限从按用户（per-user）转变为按频道（per-channel），以及如何在你自己的工作区中恰当地限定它的范围。

# 为什么"代表用户行事"会失效（Why "act as the user" breaks down）

When you use AI as a personal assistant, you can connect platforms like Google Drive, GitHub, and your calendar, and let the model use your access permissions to read and write in them.

当你把 AI 用作个人助手时，你可以连接 Google Drive、GitHub 和日历等平台，让模型使用你的访问权限在其中读写。

This model doesn't work for Claude Tag for two reasons:

这个模型对 Claude Tag 不适用，原因有二：

- Increasing agent autonomy. The length of a task that an AI agent can reliably complete on its own has been doubling roughly every four months. Agents now schedule their own tasks for later and respond to events long after the person who asked has logged off. While users set up routines that trigger them to act given certain situations, the agent works largely autonomously.
- Multiplayer teams. Claude Tag places Claude in shared spaces where teams are already working—e.g., a channel where three engineers and a PM are debugging together. But when more than one person is steering, whose permissions apply? There's no single choice of person that'd be right all of the time. This gives admins the ability to define what an agent can do in Slack independent from the humans involved, and a distinct tracking of what is done in Slack.

- 智能体自主性不断提升。AI 智能体能够独立可靠完成的任务时长，大约每四个月翻一番。智能体现在会自行安排稍后执行的任务，并在提出请求的人早已下线很久之后响应事件。虽然由用户设置例程（routine）、在特定情境下触发它们行动，但智能体的工作在很大程度上是自主的。
- 多人协作团队。Claude Tag 把 Claude 放进团队本就在协作的共享空间--例如三个工程师和一名产品经理（PM）一起排查问题的频道。但当不止一个人在主导时，该适用谁的权限？不存在任何一个在任何时候都正确的人选。这让管理员能够独立于相关的人类，定义智能体在 Slack 中能做什么，并对 Slack 中发生的行为进行独立的追踪。

## Claude 以自身身份行事（Claude acts as itself）

In a channel where Claude Tag is active, Claude isn't acting on behalf of a single user. It has its own account in each system it touches: it posts in Slack as the Claude app, opens pull requests as the Claude GitHub App, and queries your warehouse under a service account provisioned by an admin.

在启用了 Claude Tag 的频道中，Claude 并不代表某个单一用户行事。它在每个接触的系统里都有自己的账户：它以 Claude 应用的身份在 Slack 发帖，以 Claude GitHub App 的身份开启拉取请求（pull request），并在管理员配置的服务账号（service account）下查询你的数据仓库。

And because there are no personal user credentials in play, a shared channel can never become a side door into someone's private documents.

而且由于没有个人用户凭据参与其中，共享频道永远不会成为通往某人私人文档的后门。

## 继承权限（Inheriting permissions）

In the agent identity model, admins define an identity—the baseline set of connections and skills Claude holds everywhere—at the workspace level, and every channel inherits it by default. Then, where it makes sense, they can override it at the channel level, such as by granting the engineering channel access to GitHub and the data warehouse, or confining a CRM connection to a single private channel.

在智能体身份模型中，管理员在工作区层面定义一个身份--即 Claude 处处持有的连接与技能的基线集合--每个频道默认继承它。然后，在合理之处，他们可以在频道层面进行覆盖，例如授予工程频道访问 GitHub 和数据仓库的权限，或者把某个 CRM 连接限定在单一私有频道内。

In addition to credentials, admins also define:

除凭据外，管理员还要定义：

- Repository access: which repos Claude can read and write to.
- Connectors: the tools and API keys that Claude uses to do its job. Across an organization, different API keys can connect to the same service at different permission levels (e.g., Claude might be given read-only warehouse access in a general channel, and write access in the data team's private one).
- Skills and plugins: folders of instructions, scripts, and resources Claude loads dynamically to improve performance on specialized tasks.
- Standing instructions: custom instructions and context for each channel.

- 仓库访问：Claude 可以读写哪些代码仓库。
- 连接器（connector）：Claude 用来完成工作的工具和 API 密钥。在组织内，不同的 API 密钥可以以不同的权限级别连接同一服务（例如，Claude 在通用频道可能只有数据仓库的只读权限，而在数据团队的私有频道则有写权限）。
- 技能与插件（skills and plugins）：由指令、脚本和资源组成的文件夹，Claude 会动态加载以提升在专门任务上的表现。
- 常驻指令（standing instructions）：为每个频道定制的指令和上下文。

Because this model works around distinct Claude identities, revoking the identity ends Claude's access everywhere that the identity was used. This takes much less effort to manage than auditing individual agent actions across dozens of user accounts.

由于这个模型围绕独立的 Claude 身份运作，吊销该身份即可一并终止 Claude 在所有使用过该身份之处的访问。相比在几十个用户账户之间审计单个智能体的操作，这种管理方式的工作量要小得多。

# 智能体身份模型如何运作（How the agent identity model works）

Agent identity replaces the question "what can this user do?" with "what can this agent do in this compartment?" That's a departure from per-user Access Control Lists: it means that a channel member without direct access to the repo can ask Claude to read that repo, if the channel's profile grants Claude that permission.

智能体身份把"这个用户能做什么？"的问题替换为"这个智能体在这个隔间（compartment）里能做什么？"这是对按用户访问控制列表（ACL）的一种背离：这意味着，如果频道的配置文件授予了 Claude 相应权限，那么即使某位频道成员本身没有该仓库的直接访问权，也可以让 Claude 去读取该仓库。

This is unusual, but we think it is a necessary step toward an access model that works for autonomous, multiplayer agents. Below, we sketch out how to think about setting those boundaries.

这很不寻常，但我们认为，这是迈向适用于自主、多人协作智能体的访问模型的必经一步。下面我们勾勒出如何思考这些边界的设定。

## 身份边界如何运作（How identity boundaries work）

Claude Tag creates a distinct identity for each private channel; public channels in a workspace share a workspace-level identity. Claude's identity in a legal channel can't reach code that wasn't granted there, and its identity in an engineering channel can't read legal documents that weren't granted there. Memory and access respect those boundaries: what Claude learns in a private channel never appears in the wider workspace.

Claude Tag 为每个私有频道创建独立身份；工作区中的公共频道则共享一个工作区级身份。Claude 在法务频道中的身份无法触达未在该处授权的代码，它在工程频道中的身份也无法读取未在该处授权的法务文档。记忆与访问都尊重这些边界：Claude 在私有频道中学到的东西绝不会出现在更广泛的工作区里。

The identity belongs to the channel, so anyone in it can tag Claude by default, and admins can scope each channel's profile to the least-privileged member. On Enterprise plans, role-based access control lets admins go further and decide which members can invoke Claude at all, so a channel governs both what the agent can reach and who can ask.

身份属于频道，因此默认情况下频道里的任何人都可以标记（tag）Claude，而管理员可以将每个频道的配置文件限定到权限最小的成员级别。在 Enterprise（企业版）计划中，基于角色的访问控制（RBAC）让管理员更进一步，决定哪些成员根本可以调用 Claude，这样一个频道就同时管住了智能体能触达什么、以及谁可以发起请求。

## 对工具和上下文的宽泛默认访问（Broad default access to tools and context）

![按访问面划分集成范围的示意图：宽泛、低风险的集成以共享智能体身份在工作区和私有频道运行，个人或团队专用工具则留在私聊（DM）中以用户身份运行](images/identity-1.jpg)

> How teams scope Claude's tool access in Claude Tag: broad, low-risk integrations run in shared channels under an agent identity, while personal or team-specific tools stay in DMs and run as the user.
> 团队如何在 Claude Tag 中限定 Claude 的工具访问范围：宽泛、低风险的集成以智能体身份在共享频道中运行，而个人或团队专用的工具则留在私聊（DM）中以用户身份运行。

Running Claude Tag inside Anthropic, we found that its value compounds with tool and context access. Each connected system makes every other one more useful, because Claude can combine context across them—pulling a thread from Slack, a doc from Drive, a ticket from a tracker, and a query from a warehouse into one answer that no single tool could provide.

在 Anthropic 内部运行 Claude Tag 的过程中，我们发现它的价值随工具和上下文访问的增多而复利式增长。每接入一个系统，都会让其他所有系统更有用，因为 Claude 能把跨系统的上下文组合起来--从 Slack 拉出一条讨论线索、从 Drive 取出一份文档、从任务跟踪器调出一张工单、从数据仓库跑出一次查询，汇成一个任何单一工具都无法给出的答案。

The teams that get the most out of Claude are the ones that grant it generous access from the start, and pare access back depending on their organization's admin preferences. Agent identity gives admins broad enough scope for Claude to do useful cross-system work, with boundaries firm enough that the access never travels somewhere it wasn't granted. Our advice is to start with a baseline profile in a few channels, read the audit trail, and then extend access where the work justifies it, one deliberate grant at a time.

从 Claude 获益最多的团队，正是那些从一开始就给予它宽泛访问权限、再根据组织的管理偏好收回部分权限的团队。智能体身份给管理员的管控范围足够宽泛，让 Claude 能做有用的跨系统工作；边界又足够坚实，访问权限绝不会跑到未被授权的地方。我们的建议是：先在几个频道中从基线配置文件起步，阅读审计轨迹，然后在工作确有需要之处扩展访问，一次一个审慎的授权。

For organizations that require even more granularity, admins can disable Claude Tag in specific channels. Admins can also apply role-based access controls (RBAC) to limit access to Claude Tag to specific users.

对于需要更细粒度的组织，管理员可以在特定频道中禁用 Claude Tag。管理员还可以应用基于角色的访问控制（RBAC），把 Claude Tag 的使用权限限定给特定用户。

## 私信（Direct messages）

With Claude Tag, direct messages work differently than in shared channels. DMs run on users' individual claude.ai accounts—their connectors, credentials, and name on the result. This makes DMs the right place to work with Claude on tasks and with tools that should never live in a channel, like email drafts or software only you have a license for.

在 Claude Tag 中，私信的工作方式与共享频道不同。私信运行在用户个人的 claude.ai 账户之上--用的是用户自己的连接器、凭据，结果上也署用户的名。这使得私信成为与 Claude 一起处理那些绝不该出现在频道中的任务和工具的合适场所，比如邮件草稿，或只有你持有许可证的软件。

## 安全与审计（Security and audit）

When an admin adds a connection to a channel's profile, the credential is stored independently and mapped to that channel's identity, then injected at the network boundary at request time. Outbound traffic to any host an admin hasn't allowed is blocked outright. On the audit side, every routine, memory write, and network call made with agent credentials is recorded, and because Claude acts under its own service accounts, those actions also land in each connected system's own logs.

当管理员向频道的配置文件添加连接时，凭据会被独立存储并映射到该频道的身份，然后在请求时于网络边界注入。发往管理员未允许的任何主机的出站流量都会被直接阻断。在审计方面，使用智能体凭据进行的每一次例程、记忆写入和网络调用都会被记录；而且由于 Claude 以自己的服务账号行事，这些操作也会落入每个已连接系统自身的日志。

# 下一步（What's next）

Agent identity is the foundation of Claude Tag's access model. In the future, we plan to strengthen our Claude Tag's security offerings to include just-in-time credential grants—so that a user can approve a single sensitive action in the moment without permanently widening the agent's scope—and an identity-aware overlay for organizations with more complex clearance structures. This will add user-level checks on top of an agent's scope, so Claude only acts when both the channel's profile and the requesting user's own permissions allow it.

智能体身份是 Claude Tag 访问模型的基石。未来，我们计划强化 Claude Tag 的安全能力，包括即时凭据授权（just-in-time credential grant）--让用户可以在当下批准单次敏感操作，而无需永久性扩大智能体的权限范围--以及面向权限层级更复杂的组织的身份感知叠加层（identity-aware overlay）。这将在智能体的权限范围之上叠加用户级校验，使 Claude 只在频道配置文件与发起请求用户自身的权限同时允许时才行动。

The shift from single player to multiplayer AI in products like Claude Tag makes long-running, team-based work possible. Agent identity ensures that Claude's access to tools is broad enough to be useful, but scoped enough to be secure at enterprise scale.

Claude Tag 等产品中 AI 从单人到多人的转变，使长期运行、以团队为单位的工作成为可能。智能体身份确保 Claude 对工具的访问宽泛到足够有用，又受到足够限定、在企业规模下依然安全。

Learn more about Claude Tag.

了解更多关于 Claude Tag 的信息。

This article was written by Noah Zweben, a member of technical staff on the Claude Code team.

本文由 Claude Code 团队的技术成员（member of technical staff）Noah Zweben 撰写。
