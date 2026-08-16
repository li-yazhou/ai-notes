# 在前沿工作：Rakuten 如何用 Claude Fable 5 让代理隔夜干活（中英对照）

> **原文标题：** Working at the frontier: How Rakuten builds agents overnight with Claude Fable 5
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/working-at-the-frontier-rakuten
> **发布日期：** 2026-07-20
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Why Rakuten thinks Claude Fable 5 is a step change in model intelligence, transforming how long-running work is done.

为什么 Rakuten 认为 Claude Fable 5 是模型智能（model intelligence）的一次阶跃式变化（step change），正在变革长时间运行工作的完成方式。

Yusuke Kaji, General Manager of AI for Business at Rakuten, has been testing Claude models since Sep 2024. Here's why he thinks Claude Fable 5 is a step change for long-running enterprise agents.

Rakuten 商业 AI 总经理（General Manager of AI for Business）Yusuke Kaji 自 2024 年 9 月起一直在测试 Claude 模型。以下是他认为 Claude Fable 5 对企业级长时间运行代理而言是一次阶跃式变化的原因。

As General Manager of AI for Business at Rakuten, Yusuke Kaji’s job is to “find the seeds of transformative innovation and scale them across the company.”

作为 Rakuten 商业 AI 总经理，Yusuke Kaji 的职责是"找到变革性创新的种子，并将其推广到全公司"。

One of those seeds was Claude.

其中一颗种子，就是 Claude。

Since March 2025, Rakuten has used Claude to speed up software development with Claude Code, stand up agents across its business functions, and power AI features for millions of customers. According to Kaji, Rakuten chose to partner with Anthropic for its enterprise focus, leadership, and product taste.

自 2025 年 3 月以来，Rakuten 一直在使用 Claude：借助 Claude Code 加速软件开发，在各业务职能部门部署代理，并为数以百万计的客户提供 AI 功能。据 Kaji 介绍，Rakuten 选择与 Anthropic 合作，看中的是其企业级定位、领导力与产品品味（product taste）。

Across nearly a dozen model launches, he's watched the work he can hand to an agent keep growing: first using Claude Code to ship production software, then building custom Claude Managed Agents for teams across the company. He likens testing out new models with embarking on a “new quest.”

历经近十几次模型发布，他能交给代理的工作一直在增长：起初是用 Claude Code 发布生产级软件，随后是为全公司各团队构建定制的 Claude Managed Agents。他把测试新模型比作开启一场"新任务"（new quest）。

“The way a good leader prepares stretch goals for their people, we prepare stretch tasks for a new Claude,” he adds. “Maybe Claude is nudging us to stretch, too."

"就像优秀的领导者为下属制定挑战性目标（stretch goals）一样，我们也会为新的 Claude 准备挑战性任务，"他补充道。"或许 Claude 也在推动我们自我拉伸。"

When he tested Claude Fable 5, he knew something felt different. The model could run on its own for far longer than its predecessors, and for the first time, checking its own work and completing nuanced tasks overnight while Kaji slept.

当他测试 Claude Fable 5 时，他察觉到某种不同。这个模型能够自主运行的时间远超其前身，并且首次可以在 Kaji 睡觉的夜里检查自己的工作、完成精细微妙的任务。

That extra autonomy is what lets Rakuten hand its agents bigger, longer-running jobs, and transform the way they work.

正是这种额外的自主性，让 Rakuten 敢于把更大、运行时间更长的任务交给代理，并改变他们的工作方式。

## 构建 AI 原生的劳动力队伍（Building an AI-native workforce）

Rakuten is remaking itself around AI, a project it calls AI-nization – their company-wide effort to infuse AI into everything we do for customers, business partners, and employees.. When Claude Managed Agents arrived, Rakuten deployed agents across product, sales, marketing, and finance inside a week, plugged into Slack, Microsoft Teams, and the company's own task system.

Rakuten 正围绕 AI 重塑自身，这一项目被称为 AI-nization（AI 化）--一项全公司范围的行动，旨在把 AI 融入他们为客户、商业伙伴和员工所做的一切。当 Claude Managed Agents 推出后，Rakuten 在一周之内就在产品、销售、营销和财务部门部署了代理，接入 Slack、Microsoft Teams 以及公司自有的任务系统。

For Kaji and his team, the constraint about building agents used to be who could write code; now, it's who understands the business problem.

对 Kaji 和他的团队来说，构建代理的约束条件过去是"谁会写代码"，如今则是"谁理解业务问题"。

"The modern corporation is designed to minimize the cost of communication," he says. "I believe agents like Claude Code can shine when we work with them to minimize the cost of new innovation as well, like a quick transition from idea to production." Give a capable person agents that hold context and taste, and "it allows the hidden talent to unlock their potential and scale their potential 100 times more."

"现代公司的设计初衷是最小化沟通成本，"他说。"我相信，当我们与 Claude Code 这样的代理携手最小化新创新的成本时--比如从想法到生产的快速跨越--它们大有用武之地。"给一个能干的人配上拥有上下文和品味的代理，"这能让隐藏的人才释放潜力，把他们的能力放大 100 倍。"

But running agents in every function around the clock surfaces a new constraint: human judgment. While Rakuten's agents close issues roughly 10x faster across every domain, the number of tasks the organization takes on keeps rising. Adding more agents doesn't add judgment. So the faster the agents run, the more the organization's progress depends on a person closing the loop.

但在每个职能中全天候运行代理，也暴露出一个新的约束：人类判断力。虽然 Rakuten 的代理在所有领域关闭问题的速度都大约快了 10 倍，但组织承接的任务数量仍在持续攀升。增加代理并不能增加判断力。因此，代理跑得越快，组织进展就越是依赖人来收尾拍板。

## 驱动可无人值守运行数小时的代理（Powering agents that run for hours, unattended）

For most builders, the hardest part of building long-running agents is setting them up to succeed with minimal oversight. Connecting it to the right tools and context is one thing, but in Kaji’s experience, there were always limits to how long an agent could go without needing a human in the loop to validate its work.

对大多数构建者来说，构建长时间运行代理最难的部分，是让代理在最少监督下也能成功完成任务。把它连接到合适的工具和上下文是一回事，但在 Kaji 的经验里，代理在需要人介入验证其工作之前能坚持多久，始终存在上限。

Before Claude Fable 5, setting an agent loose on a multi-hour task without human oversight was always a gamble. "If they choose the right path in the first step, everything is fine," Kaji says. "But if they choose the wrong direction in the first pass, the agent spends significant time to fix the path, or even fails to reach the destination." On a job meant to run five hours or a full day, one early wrong assumption could burn the entire run, and the only way to catch it was a person checking in.

在 Claude Fable 5 之前，让代理在无人监督下执行长达数小时的任务，始终是一场赌博。"如果它第一步就走对路径，一切都没问题，"Kaji 说。"但如果第一轮就走错方向，代理就要花大量时间去纠正路径，甚至根本到不了终点。"在一个本要运行五小时或一整天的任务上，一个早期的错误假设就可能烧掉整次运行，而唯一的发现方式就是有人中途查看。

The failure mode was a lack of self-verification. Any model can take a wrong first step. The problem with earlier models was that they didn't check their own work as they went, so an early wrong turn went unnoticed. It compounded over the run and produced a suboptimal result hours later.

这种失败模式源于缺乏自我验证（self-verification）。任何模型都可能迈错第一步。早期模型的问题在于，它们不会在工作过程中随时检查自己的产出，因此早期走错的那一步无人察觉，随着运行不断累积放大，数小时后只能得到次优的结果。

According to Kaji, Claude Fable 5 changes the calculus for days-long agentic runs because it checks its own work as it goes, far more often than any prior model.

据 Kaji 所说，Claude Fable 5 改变了持续数日的代理式运行的得失盘算，因为它在工作过程中检查自身产出的频率，远超以往任何模型。

"We tested Fable, and we love its capability for self-reflection and self-verification," Kaji says. "Compared with previous models, it understands its mistake before I point it out at 2 a.m. or 3 a.m.—so that I can sleep."

"我们测试了 Fable，我们喜欢它的自我反思与自我验证能力，"Kaji 说。"与之前的模型相比，它会在凌晨两三点我指出问题之前，就先意识到自己的错误--这样我才能睡得着。"

## Claude Fable 5 的过人之处（What sets Claude Fable 5 apart）

Kaji’s team cite three behaviors that distinguish Claude Fable 5 from its predecessors, and signal a step-change in frontier intelligence:

Kaji 的团队列举了三种将 Claude Fable 5 与其前代模型区分开来的行为，它们预示着前沿智能（frontier intelligence）的一次阶跃式变化：

- It re-checks its own assumptions. When the state of the task changes midway, Fable 5 notices and corrects a wrong assumption before acting on it, rather than committing to a bad path and discovering it hours later.
- It returns to first principles at each step. It re-validates against the original intent without being told, the course-correction Kaji used to have to make himself when a run started down the wrong path..
- It matches the team's taste. Even with minimal guidance, its judgment on ambiguous calls lines up with theirs. Kaji has a name for this, a term he coined: taste alignment. "Taste alignment is smoother with Fable than any previous model from your company, or any other model we’ve used."

- 它会复查自己的假设。当任务状态中途发生变化时，Fable 5 会察觉并在行动之前纠正错误假设，而不是一头扎上糟糕的路径，数小时后才发现。
- 它在每一步都回到第一性原理（first principles）。无需提醒，它就会对照最初的意图重新校验--这种航向修正，过去一旦运行偏离方向，Kaji 常常得亲自动手完成。
- 它与团队的品味相契合。即便指引极少，它在模糊判断上的取舍也与团队一致。Kaji 为此起了个名字，一个他自创的术语：taste alignment（品味对齐）。"Fable 的品味对齐，比贵公司以往任何模型、以及我们用过的任何其他模型都要顺畅。"

Most importantly, longer autonomy changes the unit of work Kaji can delegate.

最重要的是，更长的自主运行时间改变了 Kaji 能够委派的工作单元。

“Before Fable, we had to break work into well-defined chunks for the agent to execute," he says. Now he can hand over a whole task and run several at once.

"在 Fable 之前，我们必须把工作拆解成定义明确的块，供代理执行，"他说。而现在，他可以把一整项任务整体交出去，并同时运行多项任务。

Claude Fable 5 changes what happens in between. It reflects at each step, catches a bad early assumption, and finds its own way back to first principles — re-navigating to the right outcome without anyone steering it. Because the model self-corrects mid-run, sign-off becomes feasible for the first time, and the unit of work Kaji delegates shifts from the task to the decision. The agents also carry memory between runs: "Our agents with memory remember what went wrong in past sessions and avoid repeating those mistakes."

Claude Fable 5 改变了这中间的过程。它在每一步反思，捕捉早期的不良假设，并自己找到回到第一性原理的路径--无需任何人掌舵，重新导航到正确的结果。由于模型能在运行中途自我修正，签字确认（sign-off）首次变得可行，Kaji 委派的工作单元也从"任务"转变为"决策"。这些代理还能在多次运行之间携带记忆："我们带记忆能力的代理记得过去会话中哪里出了问题，并避免重蹈覆辙。"

As a result, the absolute number of tasks keeps climbing, but the ones that truly need a human stay at a focusable level. Not having to jump in and steer mid-run is, he says, is the biggest productivity win of all—it lets his team spend its time on the decisions only people should make, and keeps an AI-native organization accelerating instead of stalling on human course-correction.

其结果是，任务的绝对数量持续攀升，但真正需要人来处理的任务，始终保持在可以专注应对的水平。他说，不必在运行中途介入把舵，本身就是最大的生产力红利--这让他的团队把时间花在只有人才能做的决策上，也让一个 AI 原生组织持续加速，而不是卡在等待人类修正航向上。

### 平衡成本与效率（Balancing cost and efficiency）

Frontier capability comes at a frontier price, and Kaji is direct that cost decides how widely he can deploy.

前沿能力自有前沿的价格，Kaji 坦言，成本决定了他能部署多广。

"As a large enterprise, we want to balance intelligence and cost," he says. His team measures task completion ratio alongside cost per task, then sends Fable 5 the work where the extra capability changes the outcome and lets smaller models keep the rest.

"作为一家大型企业，我们希望在智能与成本之间取得平衡，"他说。他的团队在衡量任务完成率的同时也衡量单任务成本，然后把那些额外能力能改变结果的工作交给 Fable 5，其余的留给较小的模型。

For Kaji, two things make the math work in Fable 5's favor: it gets more done with fewer tokens and fewer wrong turns, and it needs less hand-holding.

在 Kaji 看来，有两点让 Fable 5 的这笔账算得过来：它用更少的 token、更少的弯路完成更多工作；而且它需要的手把手指导也更少。

## 接下来（What's next）

The frontier Kaji is testing now isn't individual speed. It's getting agents to coordinate people. Claude Code has sped up his own work and his colleagues', but the hard part of any organization is the alignment between people, matching one person's context and taste to another's. He's exploring agents that "coordinate or organize, more like a manager," holding the nuance that usually gets lost between team members.

Kaji 如今正在测试的前沿，不是个人速度，而是让代理来协调人。Claude Code 已经加快了他自己和同事们的工作，但任何组织最难的部分都是人与人之间的对齐（alignment）--把一个人的上下文和品味与另一个人的相匹配。他正在探索那些"更像管理者一样去协调或组织"的代理，让通常在团队成员之间流失的细微信息得以保留。

"We do not see AI agents as future colleagues or competitors. They are systems around us." And he holds Anthropic to its own advice, that you should build for the model coming in three or six months rather than the one in front of you.

"我们不把 AI 代理视为未来的同事或竞争者。它们是围绕在我们身边的系统。"而且，他拿 Anthropic 自己的建议来要求 Anthropic：你应该为三到六个月后的模型做构建，而不是眼前这一个。

"I think we as a society still haven't found the model–task fit yet for Claude Fable 5," he says, "but it already stands out as a model that crossed the line and came over to our world.

"我认为，整个社会尚未为 Claude Fable 5 找到模型-任务契合点（model–task fit），"他说，"但它已经脱颖而出，成为一个越过了界线、来到我们世界的模型。

Get started with Claude Fable 5.

开始使用 Claude Fable 5。
