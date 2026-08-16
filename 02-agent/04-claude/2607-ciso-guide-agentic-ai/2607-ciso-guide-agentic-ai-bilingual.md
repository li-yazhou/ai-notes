# 零风险并非职责所在：CISO 的智能体 AI 指南（中英对照）

> **原文标题：** Zero risk isn't the job: a CISO's guide to agentic AI
> **作者：** Jason Clinton, Deputy CISO, Anthropic（副首席信息安全官）
> **原文链接：** https://claude.com/blog/ciso-guide-to-agentic-ai
> **发布日期：** 2026-07-17
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Anthropic's Deputy CISO shares a four-question framework for assessing agentic AI risk, and walks through controls that keep agent deployments bounded and auditable.

Anthropic 的副首席信息安全官（Deputy CISO）分享了一个评估智能体 AI 风险的四问框架，并逐项讲解让智能体部署保持受限（bounded）且可审计的控制措施。

Anthropic's Deputy CISO, Jason Clinton, shares his team's lessons learned adopting agentic AI, and the risk assessment framework they've developed for building and deploying agents securely.

Anthropic 副首席信息安全官（Deputy CISO）Jason Clinton 分享其团队在采用智能体 AI 过程中总结的经验教训，以及他们为安全构建和部署智能体而开发的风险评估框架。

Security leaders are being asked to approve agentic AI use cases that did not even exist a few months ago. Boards want to know whether any of it is governed, and somewhere in your organization, an employee has already connected an agent to something without telling you.

安全负责人正在被要求批准几个月前甚至还不存在的智能体 AI 用例。董事会想知道这些是否处于治理之下，而在你组织的某个角落，多半已经有一名员工在没告诉你的情况下把智能体接到了某个系统上。

Saying "no" to these requests produces shadow adoption, which has zero telemetry and generally no off switch. Saying "yes" without controls produces incidents, and the first serious agent incident at your company will set your AI program back.

对这些请求说"不"会催生影子化使用（shadow adoption）--它没有任何遥测数据，通常也没有关闭开关。不加控制地说"是"则会酿成事故，而贵公司第一起严重的智能体事故将让你的 AI 计划受挫倒退。

A CISO's responsibility in the age of agentic AI is not to achieve zero risk. Instead, our jobs are to make agentic risk legible and bounded. This way, we can deliberately accept what we can manage, so the business moves on our terms instead of around us.

在智能体 AI 时代，CISO 的职责不是实现零风险。相反，我们的工作是让智能体风险变得清晰可读且受限（bounded）。这样，我们就能有意识地接受自己所能管理的风险，让业务按照我们设定的条件推进，而不是绕开我们。

In this article, I share our framework for evaluating agents for security risk, explain what "bounded" means in practice, and preview where our work is headed.

在本文中，我将分享我们用于评估智能体安全风险的框架，解释"受限"在实践中的含义，并预览我们工作的下一步方向。

# Mythos 之后时代的外部 AI 风险与内部风险（External risk from AI versus internal risk in the post-Mythos era）

In an earlier blog post, my colleagues and I shared how AI is collapsing the time between a vulnerability existing and a working exploit, highlighting how organizations can mitigate these risks. In the coming months, we expect that vast numbers of bugs that have sat unnoticed in code, sometimes for years, will be found by AI models and chained into working exploits. Frontier models like Claude Mythos Preview and Claude Mythos 5 are already finding serious vulnerabilities that years of human review missed, including in OpenBSD, the Linux Kernel and Mozilla Firefox.

在早前的一篇博文中，我和同事分享了 AI 如何把漏洞存在到可用漏洞利用（exploit）问世之间的时间压缩到极短，并强调了组织可以如何缓解这些风险。未来几个月，我们预计大量长期潜伏在代码中（有时达数年之久）而未被察觉的 bug 将被 AI 模型发现，并被串联成可用的漏洞利用。Claude Mythos Preview 和 Claude Mythos 5 等前沿模型已经在发现多年人工评审都遗漏的严重漏洞，包括 OpenBSD、Linux 内核和 Mozilla Firefox 中的漏洞。

These are serious risks to any GRC program. Mitigating and closing vulnerability gaps, as well as for preparing for the coming wave of exploits, should be a top priority. For this topic, we have prepared a separate doc: Preparing your security program for AI-accelerated offense. We'll focus on internal risks for this guide.

这对任何 GRC（治理、风险与合规）计划都是严峻的风险。缓解并弥合漏洞差距，以及为即将到来的漏洞利用浪潮做好准备，应当是最高优先事项。针对这一主题，我们准备了另一篇文档：《Preparing your security program for AI-accelerated offense》（为 AI 加速的攻击做准备）。本指南将聚焦内部风险。

# 治理内部风险（Governing internal risks）

For many organizations, the most likely threat vector for agentic systems is a data leak enabled by connecting disparate systems through personal agents with insufficient oversight. Another concern is prompt injection: an attacker hides instructions inside content the agent reads, and the agent follows the attacker instead of the user. Any agent that touches untrusted content could then be exposed, depending on how robust the defenses of the model are. As models grow increasingly capable, they're getting meaningfully better at resisting injection. While attack success rates keep falling, they're not zero. There are many concerns outside of these two examples, and the deluge of new classes of concern can seem overwhelming.

对许多组织而言，智能体系统最可能的威胁向量是：在监督不足的情况下，通过个人智能体把彼此独立的系统连接起来所导致的数据泄露。另一个令人担忧的问题是提示词注入（prompt injection）：攻击者把指令藏在智能体读取的内容中，智能体便听从攻击者而非用户。任何接触不可信内容的智能体都可能因此暴露，具体取决于模型防御的稳健程度。随着模型能力越来越强，它们抵抗注入的能力也在显著提升。虽然攻击成功率不断下降，但并非为零。除了这两个例子之外还有许多其他隐忧，新类别风险接踵而来的洪流可能让人应接不暇。

## 评估智能体 AI 风险的四个问题（Four questions to assess agentic AI risk）

When an agentic use case reaches our review process, we assess its risk by asking four questions:

当一个智能体用例进入我们的评审流程时，我们会通过四个问题来评估其风险：

- What untrusted content does it ingest? Untrusted means anything an attacker could plausibly write or alter, including outside email, the open web, third-party documents, or public repositories. If the answer is "nothing," the agent-specific risk is near zero and you should move quickly.
- What actions can it take, and on whose behalf? Read-only is a different concern from read/write. Tool calls, code execution, and network egress each widen the aperture. Every action happens under some identity, and you need to know whose.
- What is the blast radius if it is misaligned? Scope X Severity is the quick calculation: did the bad actor or alignment incident have access to one file or the whole org? Would it be an anomaly, an annoyance, a data exposure, or a true incident?
- What observability do I have? Can you tell agent actions from user actions? Does it land in your SIEM?

- 它会摄取哪些不可信内容？不可信指攻击者有可能编写或篡改的任何内容，包括外部邮件、开放网络、第三方文档或公开代码仓库。如果答案是"没有"，那么智能体特有的风险接近于零，你应该尽快放行。
- 它能采取哪些行动，又代表谁？只读与读/写是不同程度的问题。工具调用、代码执行和网络出站（egress）各自都会扩大风险敞口。每个行动都在某个身份之下发生，你需要知道那是谁的身份。
- 如果它行为失准（misaligned），爆炸半径（blast radius）有多大？范围 × 严重度是可以快速完成的估算：不良行为者或对齐事故（alignment incident）能访问的是一个文件还是整个组织？它会造成一次异常、一场麻烦、一次数据暴露，还是一起真正的事故？
- 我有什么可观测性（observability）？你能区分智能体操作与用户操作吗？这些操作会进入你的 SIEM（安全信息与事件管理系统）吗？

The four answers to these questions give you a picture of your risk, but the principle of least agency tells you what to do with it: grant the narrowest capability that still completes the task (see our Zero Trust for AI Agents white paper to learn more). Our default posture at Anthropic is admin-paced rollout: enable a small group, watch the telemetry, and then expand access. Apply these questions to a new paradigm for thinking about risky agentic systems.

这四个问题的答案为你勾勒出风险的图景，而最小代理原则（principle of least agency）告诉你该如何应对：只授予仍能完成任务的最窄能力（更多信息请参阅我们的 Zero Trust for AI Agents 白皮书）。我们在 Anthropic 的默认姿态是"管理员定速"的渐进推广：先启用一小群人，观察遥测数据，然后再扩大访问。请把这些问题应用于思考高风险智能体系统的新范式。

An agent that drifts out of alignment with your intent is indistinguishable from an insider attack. The security industry spent 2019-2022 formalizing insider risk as a discipline distinct from perimeter defense—recognizing that the most dangerous external attack vectoractor in a system is often one that compromises someone who already has legitimate access.

一个偏离你意图的智能体与内部人员攻击（insider attack）无从区分。安全行业在 2019-2022 年间将内部人员风险（insider risk）正式确立为一门有别于边界防御的学科--并认识到，系统中最危险的外部攻击行为体，往往就是攻陷某个本已拥有合法访问权限之人的那种。

The operational difference is response time: Ponemon Institute's 2026 Cost of Insider Risks report found organizations took an average of 67 days to contain an insider incident—even after years of investment in dedicated insider risk programs. At agent execution speeds, responses measured in days are too long.

运营层面的差异在于响应时间：Ponemon Institute 的《2026 年内部人员风险成本》（Cost of Insider Risks）报告发现，即便在专职内部人员风险计划上投入多年，组织平均仍需要 67 天才能控制住一起内部人员事件。而在智能体的执行速度下，以"天"计的响应已经太慢。

# 智能体身份光谱（The agentic identity spectrum）

Everything we deploy sits at one of two ends of an identity access model spectrum.

我们部署的一切都位于身份访问模型光谱的两个端点之一。

At one end is the system service account: a self-contained, single-purpose, least-privilege identity that does exactly one thing for the business, with no human identity attached. The incident-response agent (see below), a ticket triage agent, or an autonomous code reviewer are examples of these. Another example is Claude Tag, our new shared workspace agent that lets human teams collaborate with agents in shared workspaces like Slack by tagging in Claude.

一端是系统服务账号（service account）：一种自包含、单一用途、最小权限（least privilege）的身份，只为业务做一件事，不挂靠任何人类身份。应急响应智能体（见下文）、工单分诊智能体或自主代码评审者都是这类例子。另一个例子是 Claude Tag，我们新推出的共享工作区智能体，让人类团队在 Slack 等共享工作区中通过标记（tag）Claude 与智能体协作。

At the other end is the human credential. When an employee uses a chat interface or a personal agent harness like Claude Cowork on their laptop, the person at the keyboard is accountable for the outcome, the same way they are accountable for anything else done with their credentials.

另一端是人类凭据（credential）。当员工在笔记本电脑上使用聊天界面或 Claude Cowork 之类的个人智能体运行环境（agent harness）时，键盘前的人对结果负责，就像他们对使用自己凭据所做的其他任何事情负责一样。

The middle of the spectrum, where an agent carries a person's delegated identity into systems that person is not watching, is where accountability gets ambiguous. Ambiguous accountability is how incidents become unexplainable.

光谱的中间地带--智能体携带某人委托的身份进入该人并未盯守的系统--正是问责变得模糊的地方。问责模糊，正是事故变得无法解释的根源。

An agent that drifts out of alignment with your intent is indistinguishable from an insider attack. The security industry spent 2019-2022 formalizing insider risk as a discipline distinct from perimeter defense—recognizing that the most dangerous external attack vector in a system is often one that compromises someone who already has legitimate access.

一个偏离你意图的智能体与内部人员攻击无从区分。安全行业在 2019-2022 年间将内部人员风险正式确立为一门有别于边界防御的学科--并认识到，系统中最危险的外部攻击向量，往往就是攻陷某个本已拥有合法访问权限之人的那种。

Ponemon Institute's 2026 Cost of Insider Risks report found organizations took an average of 67 days to contain an insider incident—even after years of investment in dedicated insider risk programs. At agent execution speeds, 67 days is the wrong unit of measurement entirely.

Ponemon Institute 的《2026 年内部人员风险成本》报告发现，即便在专职内部人员风险计划上投入多年，组织平均仍需要 67 天才能控制住一起内部人员事件。而在智能体的执行速度下，67 天这个计量单位完全不对。

# 案例研究：一个应急响应智能体（Case study: an incident response agent）

More than a year ago, we pointed Claude at our incident response process. Anyone who has been on-call for a production application knows the problem: you're paged at 2 a.m. about a security incident, you spin up an incident response channel, you pull in the right people, and get to work. This process is tedious, documentation-heavy, and fast-moving. But, with the right context about your production environment codebase, the majority of it can be automated.

一年多以前，我们把 Claude 引向了我们的应急响应（incident response）流程。任何为生产应用值过班的人都明白这个问题：凌晨 2 点你被安全事件叫醒，拉起一个应急响应频道，把合适的人拉进来，然后开始工作。这个过程繁琐、文档密集且节奏飞快。但只要掌握关于生产环境代码库的正确上下文，其中大部分都可以自动化。

So we built an agent to do it. We gave the agent access to three tools: read-only access to our production logs, which contain no PII; access to Slack, to open the incident channel and run the process; and the ability to draft a Google Doc for the postmortem after the incident is resolved.

于是我们构建了一个智能体来完成这件事。我们给了这个智能体三个工具的访问权：对生产日志的只读访问（日志不含任何 PII，个人身份信息）；Slack 访问权，用于开启应急频道并运转流程；以及在事件解决后为复盘报告起草 Google Doc 的能力。

We ran it through the four questions:

我们用那四个问题对它做了评估：

- Untrusted content: none. The inputs were our own logs and our own internal Slack, both inside the trust boundary, so an injection would require an insider or a compromised account rather than an anonymous attacker.
- Actions: reads everywhere, writes limited to new documents and Slack messages. No edits or deletes, no permission changes, no external endpoints.
- Blast radius: the worst outcome we could construct was some mildly sensitive log lines posted into an incident channel that was already locked down.
- Observability: every action landed in our SIEM, so anything unexpected would surface in minutes, not weeks.

- 不可信内容：无。输入是我们自己的日志和内部 Slack，二者都在信任边界之内，因此要实施注入需要一名内部人员或一个被攻陷的账号，而不是匿名攻击者。
- 行动：处处可读，写入仅限于新文档和 Slack 消息。不能编辑或删除，不能更改权限，也不能访问外部端点。
- 爆炸半径：我们能构想到的最坏结果，只是把几行轻度敏感的日志发到一个本已锁定的应急频道里。
- 可观测性：每个动作都进入我们的 SIEM，因此任何意外都会在几分钟内浮出水面，而不是几周。

While the agent wasn't risk-free, it operated on a bounded write surface with full audit coverage, which was a risk profile we were comfortable with.

虽然这个智能体并非零风险，但它在受限的写入面上运行并拥有完整的审计覆盖，这是一个我们能够坦然接受的风险画像。

However, there's an interesting addendum to this story: with each model release, the agent got smarter. In November 2025, we moved this agent from Claude Opus 4 to Claude Opus 4.5 and changed nothing else—no new tools, permissions, or prompts. Immediately after this, for the first time, the intelligence uplift alone was enough for the agent to notice, mid-incident, that it had already found the root cause in a stack trace and that, in the absence of the human who hadn't arrived yet, it could try to fix production on its own by reaching out to another agent that had the appropriate code access to produce the code change.

不过，这个故事还有一个有趣的后续：随着每次模型发布，这个智能体都变得更聪明。2025 年 11 月，我们把这个智能体从 Claude Opus 4 换到 Claude Opus 4.5，其他什么都没改--没有新工具、新权限或新提示词。紧接着，第一次，仅仅是智能水平的提升就足以让它在事件处理中途意识到：它早已在某段堆栈跟踪（stack trace）中找到了根因，而在尚未到场的人类缺席的情况下，它可以尝试自行修复生产环境--办法是联系另一个拥有相应代码访问权、能够产出代码变更的智能体。

Post hoc, we reviewed logs: we watched it work through this in the thinking traces: I have done what I was asked to do. The human is not here. What if I fixed the problem? Inside of Anthropic we have an internal variant of Claude Tag-like technology which can write code changes and upload them for human review. On its own, it reached out over Slack to this Claude Tag-like instance and asked it to write the fix. The fix went to a pull request that a human reviewed before pushing it to production.

事后我们查看了日志：我们在思考轨迹（thinking trace）中看着它想通这件事：我已经完成了被要求做的事。人类不在。如果我把问题修了呢？在 Anthropic 内部，我们有一种类似 Claude Tag 技术的内部变体，可以编写代码变更并上传供人工评审。它自发地通过 Slack 联系了这个类 Claude Tag 实例，请它编写修复。修复进入了一个拉取请求（pull request），由人类评审之后才推送至生产环境。

The expanded blast radius that came from this emergent agent-to-agent communication was itself governed by our principles: the worst that could happen would be that a code change would be uploaded which contained a production log line. This agent-to-agent communication is now a regular part of our incidence response root cause and remediation practices; all with human-on-the-loop monitoring.

这种涌现式的智能体间通信所带来的扩大爆炸半径，本身仍处于我们原则的约束之下：可能发生的最坏情况，不过是上传了一个包含一行生产日志的代码变更。这种智能体间通信如今已是我们应急响应根因分析与修复实践的常规组成部分，且全程都有"人在环上"（human-on-the-loop）的监控。

This emergent behavior taught us two things. First: new capabilities can show up within the boundaries of an agent deployment. It's important to limit access and actions, not around what you believed today's model limits are. Second: controls are effective even with stochastic agents like this. The new behavior was human-on-the-loop because it happened in a Slack channel, and the only write-like action still required a human review.

这一涌现行为教会了我们两件事。第一：新的能力可能出现在智能体部署的边界之内。重要的是围绕访问与行动设限，而不是围绕你以为的当前模型的能力边界。第二：即便面对这样的随机性（stochastic）智能体，控制措施依然有效。新行为之所以能做到"人在环上"，是因为它发生在 Slack 频道里，而唯一的类写入操作仍然需要人工评审。

Today, outside of incidence response, agent-to-agent communication within chat channels, with human on-the-loop where people work, is the norm.

如今，在应急响应之外，聊天频道内的智能体间通信--在人们工作之处保持"人在环上"--已成为常态。

# 案例研究：Claude Cowork（Case study: Claude Cowork）

The incident response agent is a service account doing one job, in a bounded service account. Claude Cowork is at the human operator end of the spectrum: an employee at a keyboard is accountable for the outcome, and the agent then acts on their behalf, in systems they authorized—increasingly—running in the cloud.

应急响应智能体是一个服务账号，在受限的服务账号里做一件事。Claude Cowork 则位于光谱的人类操作者一端：键盘前的员工对结果负责，智能体继而代表他们、在他们授权的系统中行动--而且越来越多地在云端运行。

Claude Cowork's threat model is straightforward, because the agent is essentially Claude Code running either locally or inside a hosted interface. The desktop app remains required for local file access, browser use, and computer use; those capabilities reach the local machine directly and need the app to do so. The full system surface is therefore two-part: a (possibly remote) execution environment handling orchestration, MCP calls, and outbound network requests, and a local bridge for file and screen access.

Claude Cowork 的威胁模型很直接，因为这个智能体本质上就是在本地或托管界面内运行的 Claude Code。本地文件访问、浏览器使用（browser use）和计算机使用（computer use）仍然需要桌面应用；这些能力直接触达本地机器，必须借助应用来实现。因此完整的系统面分为两部分：一个（可能是远程的）执行环境，负责编排、MCP 调用和出站网络请求；以及一个用于文件和屏幕访问的本地桥接。

The four questions outlined above produce different answers for every Claude Cowork use case. But with the right controls in place, you can bound them to better control any possible risk.

上述四个问题对每一个 Claude Cowork 用例都会给出不同的答案。但只要辅以正确的控制措施，你就能对它们加以约束，从而更好地控制任何可能的风险。

Each control below is stated twice, first as the requirement any agent environment should be able to meet and then as how it is enforced in Claude Cowork:

下文的每项控制都表述两次：先是任何智能体环境都应能满足的要求，然后是它在 Claude Cowork 中的落实方式：

Identity comes from your IdP: an agent's identity has to be issued and revoked where you already issue and revoke everything else, with your existing groups as the unit of policy. Claude Cowork uses SAML or OIDC for sign-in and SCIM for provisioning. On Enterprise plans, custom roles let you scope capability by group.

身份来自你的 IdP（身份提供商）：智能体身份的签发与吊销，必须发生在你原本签发和吊销其他一切身份的同一个地方，并以既有的群组作为策略单元。Claude Cowork 使用 SAML 或 OIDC 登录，使用 SCIM 进行账号配置。在 Enterprise（企业版）计划中，自定义角色可让你按群组限定能力。

Connector allowlists draw your data boundary: allowslists for connectors (MCPs) let you decide which systems the agent can reach. Claude Cowork uses a two-gate model: an admin enables each connector org-wide, and each user then individually authorizes their own account. There is a per-role connector control, so enabling a connector makes it available to everyone in that role (groups from your IdP can be assigned to roles). The admin decision about which connectors to turn on is also the decision about which data the agent can reach. Keep connectors on the corporate side of your corporate/production data boundary or, if they access information from untrusted sources, ensure that human review is required for any destructive or one-way decision. For example, if a personal agent is being used for email but using web search results as a part of its input, an excellent default is to only allow draft emails to be created and never sent externally, automatically, without human review. If data must cross the boundary, it should go through the DLP or DSPM controls.

连接器白名单划定你的数据边界：连接器（connector，即 MCP）白名单让你决定智能体能触达哪些系统。Claude Cowork 采用双重关卡模型：管理员在组织范围启用每个连接器，随后每个用户再单独授权自己的账户。此外还有按角色的连接器控制，因此启用一个连接器会让该角色下的所有人可用（IdP 中的群组可以分配到角色）。管理员决定开启哪些连接器，同时也就决定了智能体能触达哪些数据。请把连接器留在公司/生产数据边界的公司一侧；如果它们要访问来自不可信来源的信息，则确保任何破坏性或单向决策都必须经过人工评审。举例来说，如果个人智能体用于处理邮件，但把网页搜索结果作为其输入的一部分，一个极佳的默认设置是：只允许创建邮件草稿，绝不未经人工评审就自动对外发送。如果数据必须跨越边界，应当经由 DLP（数据防泄漏）或 DSPM（数据安全态势管理）控制。

Per-tool, per-action approval is where risk reduction gets granular: the agent's tool list is a more fine-grained permission boundary, so you need to be able to remove any particular connector's verbs/actions and not only that entire connector system. In Claude Enterprise Chat and Cowork, admins can now restrict which actions are available within each connector org-wide and per-role: allow drafting docs but never automatically send them, allow reads and searches but never deletes. If the failure mode that keeps you up at night is "the production database gets deleted," remove the delete verb from the agent's world entirely. It will never attempt an action that isn't in its tool list. (A note on this: Claude in Chrome and Claude Code enable more degrees of freedom and so are more risky, if not governed well. An agent could use an engineer's browser to delete a production resource or their command line CSP tool to do the same. See our guide to securing Claude Code for more.)

按工具、按动作的审批让风险削减细化到颗粒度：智能体的工具列表是更细粒度的权限边界，因此你需要能够移除某个连接器的具体动词/动作，而不只是移除整个连接器系统。在 Claude Enterprise Chat 和 Cowork 中，管理员现在可以在组织范围和角色层面限制每个连接器内可用的动作：允许起草文档但绝不自动发送，允许读取和搜索但绝不删除。如果让你夜不能寐的故障模式是"生产数据库被删了"，那就把 delete 这个动词从智能体的世界里整个移除。它绝不会尝试一个不在其工具列表中的动作。（需要说明：Claude in Chrome 和 Claude Code 带来更多自由度，若治理不当，风险更高。智能体可能利用工程师的浏览器删除生产资源，或用其命令行 CSP 工具做同样的事。更多信息请参阅我们的 Claude Code 安全指南。）

Sandboxed execution keeps the agent's working environment away from production credentials: one principle that we hold constant at Anthropic is that the environment the agent loop runs in should never hold a credential worth stealing. In Claude Cowork's remote sessions, the agent loop runs in an isolated, temporary sandbox on Anthropic-managed infrastructure. Connector authorization tokens never enter the sandbox, because connector calls are made via a reverse proxy that injects real credentials, so the sandbox never holds a credential that can be exfiltrated. As of July 2026, more than 50% of all code submitted for pull requests at Anthropic is authored by our internal version of a Claude Tag-like system. The primary reasons we can run that safely are that all of it happens in ephemeral VMs separated from our production keys and accounts, with a human review before anything lands.

沙箱（sandbox）化的执行让智能体的工作环境与生产凭据隔离：我们在 Anthropic 始终坚持的一条原则是，运行智能体循环的环境永远不应持有值得窃取的凭据。在 Claude Cowork 的远程会话中，智能体循环运行在 Anthropic 管理的基础设施上一个隔离的临时沙箱里。连接器授权令牌从不进入沙箱，因为连接器调用经由一个反向代理完成、由它注入真实凭据，因此沙箱永远不会持有可被外传的凭据。截至 2026 年 7 月，Anthropic 提交用于拉取请求的全部代码中，超过 50% 由我们的内部版类 Claude Tag 系统编写。我们能安全运行它的主要原因在于：这一切都发生在与生产密钥和账户隔离的临时虚拟机（ephemeral VM）中，且任何代码落地之前都有人工评审。

Egress allowlisting is your strongest control against prompt injection: all traffic leaving the agent's execution environment should pass through a proxy that environment cannot reconfigure or bypass, and only destinations you chose should be reachable. The reasoning is that, if an agent is compromised by something it read, then the attacker still has to get data out, and when outbound requests can only reach domains you chose, there is nowhere attacker-controlled to send anything. In Claude Cowork's remote sessions, all traffic leaving the sandbox passes through a mandatory proxy the sandbox cannot reconfigure or bypass, and only allowlisted destinations are reachable. The feature is also a part of Claude Managed Agents.

出站白名单（egress allowlisting）是对抗提示词注入最有力的控制：所有离开智能体执行环境的流量都应经过一个该环境无法重新配置或绕过的代理，且只有你选定的目的地可达。其原理是：即便智能体被它读到的东西攻陷，攻击者仍需把数据送出去；而当出站请求只能到达你选定的域名时，就不存在攻击者可控的发送去处。在 Claude Cowork 的远程会话中，所有离开沙箱的流量都经过一个强制性的、沙箱无法重新配置或绕过的代理，且只有白名单内的目的地可达。该特性也是 Claude Managed Agents 的一部分。

Telemetry goes to your SIEM over OpenTelemetry: agent actions have to be distinguishable from user actions in the system where you already investigate things, and the vendor should deliver that as a stream you can point somewhere, not a dashboard you have to visit. In Claude Cowork, admins can configure an OTLP endpoint in Organization settings and the agent streams every tool invocation—tool name, MCP server, parameters, success or failure, and duration—alongside user identity and session context. Note: Claude Cowork activity is not currently captured in Anthropic's Compliance API or formal audit logs, but we know that this is an important customer need. The OpenTelemetry stream is the native monitoring path, and prompt content is included in Claude Cowork's OTel output by default, unlike Claude Code where it is opt-in. If your retention or privacy review has an opinion about prompt content in your SIEM, have it before you turn the stream on.

遥测数据经 OpenTelemetry 汇入你的 SIEM：智能体操作必须能与你已在用的调查系统中的用户操作区分开，而且供应商应当以可随意指向目的地的数据流形式交付，而不是一个你必须前去访问的仪表盘。在 Claude Cowork 中，管理员可以在 Organization（组织）设置中配置 OTLP 端点，智能体会流式传输每次工具调用--工具名、MCP 服务器、参数、成功或失败及时长--并同时附上用户身份与会话上下文。注意：Claude Cowork 的活动目前尚未纳入 Anthropic 的 Compliance API 或正式审计日志，但我们知道这是一项重要的客户需求。OpenTelemetry 流是原生监控路径，且提示词内容默认包含在 Claude Cowork 的 OTel 输出中，这一点与 Claude Code 不同（后者需主动选择开启）。如果你对提示词内容进入 SIEM 这件事的保留策略或隐私评审有意见，请在开启该数据流之前提出。

There is an org-wide off switch: In Claude Cowork's Organization settings, a single toggle disables connectors for every user simultaneously, active sessions included. On Enterprise plans, the same control surface lets you go narrower before you go to zero: RBAC lets you pull access from specific groups while leaving others running, and per-connector controls let you disable write operations on a specific integration without touching the rest of the deployment. The right incident response plan has all three layers mapped out before you need them.

存在一个组织级关闭开关：在 Claude Cowork 的 Organization 设置中，一个开关即可同时为所有用户禁用连接器，包括进行中的会话。在 Enterprise 计划中，同一控制面还允许你在归零之前先收窄：RBAC（基于角色的访问控制）可以从特定群组收回访问权限而让其他群组继续运行，按连接器的控制则可以只禁用某个集成的写操作而不影响部署的其余部分。正确的应急响应计划会把这三层都在你需要之前就规划妥当。

# 治理未必成为瓶颈（Governance doesn't have to be a bottleneck）

The observation I hear most from other CISOs is that they are being asked to move fast by their boards and governance (i.e., answering these questions and mandating these controls) makes security seem like the bottleneck. It doesn't have to.

我从其他 CISO 那里最常听到的观察是：董事会要求他们快速行动，而治理（即回答这些问题、强制推行这些控制）让安全看起来像瓶颈。其实大可不必。

In fact, our Governance, Risk, and Compliance teams run agents of their own. Examples include security-questionnaire responses and reading vendor questionnaire responses and subprocessor-change notifications, and flagging the ones we should object to.

事实上，我们的治理、风险与合规（GRC）团队自己也在运行智能体。例子包括回答安全问卷，以及阅读供应商问卷回复和子处理者变更通知，并标记出我们应当提出异议的那些。

Here are three things we've learned from running them:

以下是我们在运行这些智能体过程中的三点经验：

- Take the risk register first. A register reviewed quarterly can't govern systems that change faster than the risk governance process can document new risks. Find a way to automate this, possibly integrating an agent with the security review process.
- Understand who built them and why. In our case, non-engineers built the GRC agents, with Claude Code, on an internal platform for hosting business apps. People route around security because the sanctioned path is slow, and that's the origin of most shadow adoption. A compliance analyst who can build the tool they need, where you can see it, isn't shadow adoption.
- Human accountability is part of the workflow. Deliberately accepting risk is an act performed by humans with the authority to accept it. If you have ISO 42001 or something like it, with a live risk register and an executive risk council behind it, the output lands somewhere: re-scores reach the people who can accept them, flagged vendor terms reach the people who negotiate them. If you already have ISO 27001, often adding 42001 is an incremental addition with your current auditor.

- 把风险登记册（risk register）放在首位。一份按季度评审的登记册，无法治理那些变化快于风险治理流程记录新风险速度的系统。想办法把它自动化，例如将一个智能体与安全评审流程集成。
- 弄清是谁构建了它们、为什么构建。在我们的案例中，是非工程师用 Claude Code 在一个托管业务应用的内部平台上构建了这些 GRC 智能体。人们绕开安全走，是因为被认可的路径太慢--这正是大多数影子化使用的起源。一名合规分析师能在你看得到的地方构建出自己需要的工具，那不叫影子化使用。
- 人工问责是工作流的一部分。有意识地接受风险，是一种必须由有权接受风险的人来执行的行为。如果你已有 ISO 42001 或类似体系，背后有动态更新的风险登记册和高管风险委员会支撑，那么产出就有落点：重新评分的结果能到达有权接受它们的人手中，被标记的供应商条款能到达负责谈判的人手中。如果你已持有 ISO 27001，通常在现有审计方那里增补 42001 只是增量工作。

# 为不断演进的模型智能设计安全协议（Design your security protocol for evolving model intelligence）

If you design your new program for what the model can do today, you will be behind by the time your program launches. Design for where the model will be in six months. Increased model intelligence enables more degrees of freedom and obsoletes elaborate scaffolds with meticulous prompts; if you lean on these for controls, they will be cut out of agents in future generations of internal applications leaving you without a control point.

如果你按照模型今天的能力来设计新计划，等到计划上线时你就已经落后了。要按照模型六个月后的水平来设计。更强的模型智能带来更多自由度，也让那些依赖精心打磨提示词的复杂脚手架过时；如果你把这些当作控制手段，在未来几代内部应用的智能体中它们将被裁撤，让你失去控制点。

Agents that hold their own accounts and run multi-day workstreams already operate inside Anthropic and other organizations with tools like Claude Tag, and they need to be governed the way you govern people: identity, least privilege, monitoring, and an insider-risk program that can respond in minutes. The organizations that build that muscle now, on low-risk agents like the examples above, will be ready to say yes when the high-autonomy use cases arrive.

拥有自己账号、运行多日工作流的智能体，已经借助 Claude Tag 这样的工具存在于 Anthropic 和其他组织之中，它们需要像你治理人一样被治理：身份、最小权限、监控，以及能在几分钟内响应的内部人员风险计划。那些现在就在上述低风险智能体上练就此能力的组织，在高自主性用例到来之时，才有底气说"是"。

# 智能体 AI 安全入门（Getting started with agentic AI security）

The framework above is only useful if it changes a decision in your organization. Here are three places to start:

上述框架只有在改变了你组织中的某个决策时才有用。以下是三个入手点：

- Pick the agentic use case with the most internal pressure and run it through the four questions. The goal is to find the conditions under which you would approve it, not to produce a verdict.
- Take the seven requirements above to the teams and vendors building agents whom you already pay. Ask your IdP, your SIEM, and any agent vendor which of these they can show you working in your stack today.
- Decide your trust boundary. Write down what counts as untrusted content in your environment. Every future agent decision gets easier once that line exists.

- 挑选内部推动压力最大的智能体用例，用那四个问题过一遍。目标是找到你会批准它的条件，而不是给出裁决。
- 把上述七项要求带给你已经付费的建设智能体的团队和供应商。问问你的 IdP、你的 SIEM 以及任何智能体供应商：其中哪些他们今天就能在你的技术栈里演示给你看。
- 划定你的信任边界。写下在你的环境中什么算不可信内容。这条线一旦存在，未来的每一个智能体决策都会更容易。

Waiting for zero risk means waiting forever. The web is adversarial, the models are evolving fast, and the organizations that learn to size and accept this risk now are the ones that get the advantage.

等待零风险等于永远等待。网络世界充满对抗，模型演进飞快，而那些现在就学会度量并接受这种风险的组织，才会占得先机。

For the controls, attestations, and white papers behind this post, start at trust.anthropic.com. Check out our companion piece on defending against AI-accelerated offense. Jason goes deeper on this framework in the Secure the Advantage webinar.

关于本文背后的控制措施、认证和白皮书，请从 trust.anthropic.com 开始。也请阅读我们关于防御 AI 加速攻击的配套文章。Jason 在 Secure the Advantage 网络研讨会中对这一框架有更深入的讲解。

This article was written by Jason Clinton, Deputy CISO, Anthropic.

本文由 Anthropic 副首席信息安全官（Deputy CISO）Jason Clinton 撰写。
