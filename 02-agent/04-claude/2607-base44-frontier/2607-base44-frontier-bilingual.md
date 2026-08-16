# 在前沿工作：Base44 为什么把他们最具挑战性的工程工作托付给 Claude Fable 5（中英对照）

> **原文标题：** Working at the frontier: Why Base44 trusts Claude Fable 5 with their most challenging engineering work
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/working-at-the-frontier-why-base44-trusts-claude-fable-5-with-their-most-challenging-engineering-work
> **发布日期：** 2026-07-15
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Why Base44 trusts Anthropic's Claude Fable 5 with its most complex product and engineering tasks.

Base44 为什么把其最复杂的产品与工程任务托付给 Anthropic 的 Claude Fable 5。

Yoav Orlev, Head of Product at Base44, joined the vibe coding platform as its first employee and has seen his team build on every Claude model since Sonnet 4. Here's why he thinks Claude Fable 5 is the first model that reasons about software the way a senior engineer would, and what that frees the rest of his team to build.

Yoav Orlev 是 Base44 的产品负责人（Head of Product），作为这家 vibe coding（氛围编程）平台的第一号员工加入，并见证了团队基于从 Sonnet 4 以来的每一代 Claude 模型进行构建。本文讲述他为什么认为 Claude Fable 5 是第一个能像资深工程师那样对软件进行推理的模型，以及这为团队其他人解放出了怎样的构建空间。

Base44 is a vibe-coding platform that allows anyone, regardless of technical ability, to build full stack applications and websites. Its customers range from small businesses with no developers to companies using it to build full SaaS products.

Base44 是一个 vibe-coding（氛围编程）平台，任何人无论技术能力如何，都能用它构建全栈应用和网站。它的客户既包括没有任何开发者的小企业，也包括用它构建完整 SaaS 产品的公司。

Yoav Orlev, who joined Base44 as its first employee and now runs product, says one of the most satisfying parts of his work is seeing what small businesses can do with the platform for which they otherwise lacked the time, budget, or knowhow, whether that's building a digital storefront or a shift-management application for restaurant staff. His team's mission is to keep widening their product's capabilities while keeping it usable for everyone.

Yoav Orlev 作为第一名员工加入 Base44，如今负责产品。他说，工作中最令人满足的部分之一，是看到小企业用这个平台做出他们原本没有时间、预算或技术知识去做的东西--无论是一家数字店面，还是给餐厅员工用的排班管理应用。他团队的使命是不断拓宽产品能力，同时让它对每个人都保持易用。

The Base44 product and engineering teams have always moved quickly, especially when shipping small or medium-scope features. But any changes to the platform's core that touch multiple interdependent parts could only be entrusted to the most senior engineers.

Base44 的产品与工程团队一直动作很快，尤其是在交付中小范围的功能时。但任何触及平台核心、牵动多个相互依赖部分的改动，只能交给最资深的工程师。

One such bottleneck was Base44's system prompt and its hundreds of permutations, which vary by whether someone is on their first app or their fifth, a free user or a subscriber, and by the category and features of the app being built. Another was changing the native mobile infrastructure, which only engineers with mobile expertise could do.

其中一个瓶颈是 Base44 的系统提示词（system prompt）及其数百种排列组合--这些变体取决于用户是在做第一个应用还是第五个、是免费用户还是订阅者，以及所构建应用的类别和功能。另一个瓶颈是原生移动基础设施的改动，这只有具备移动端专业知识的工程师才能胜任。

Earlier Claude models, which have powered Base44's app generation engine since it launched in early 2025, couldn't be trusted with that work, Orlev suggests. When a model got stuck on an error, for example, it would keep working the spot in front of it instead of recognizing the fix probably already existed elsewhere in the code and searching for it.

Orlev 认为，自 2025 年初上线以来一直驱动 Base44 应用生成引擎的早期 Claude 模型，还不足以把这类工作托付给它们。举例来说，当模型在某个错误上卡住时，它会一直死磕眼前那一处，而不是意识到修复方法很可能已经存在于代码的其他地方并主动去找。

"The decision on what to do next is a crucial one and most of the time [earlier] models would take, I would say, a naive approach," he says.

"下一步该做什么是个关键决策，而大多数时候，我可以这么说，（早期的）模型会采取一种天真（naive）的做法，"他说。

Claude Fable 5 was the first model the team tested that could reason as if it had an understanding of how software is built, Orlev says.

Orlev 说，Claude Fable 5 是团队测试过的第一个能够表现得像是真正理解软件构建方式那样进行推理的模型。

# 将最复杂的产品与工程工作托付给 Fable 5（Trusting Fable 5 with the most complex product and engineering jobs）

Base44 runs each new Claude model through evals across different app types, measuring latency, cost, and build errors. The team also runs tests like building a Minecraft clone to see how a model handles game physics and mechanics.

Base44 会让每一代新的 Claude 模型跑过覆盖不同应用类型的 evals（评估），度量延迟、成本和构建错误。团队还会做诸如构建一个《我的世界》（Minecraft）克隆版的测试，观察模型如何处理游戏物理和机制。

With Claude Fable 5, two things stood out: it finished tasks in far fewer turns, and it built more complete apps from the first prompt, including the edge cases that earlier models skipped.

在 Claude Fable 5 身上，有两点尤为突出：它用少得多的轮次（turns）就完成了任务，而且从第一条提示词开始就能构建出更完整的应用，连早期模型会跳过的边界情况（edge cases）也一并覆盖。

So the team pointed it at a task they had previously reserved only for the most senior engineers: rebuilding the Base44 system prompt. After about an hour of back-and-forth questions, Claude Fable 5 ran on its own for four hours and returned 90% to 95% of what they needed. Using its A/B testing infrastructure, the team was then able to measure and ship these changes that afternoon. And while Claude Fable 5 worked, it even flagged a gap in Base44's own evals: the team wasn't testing for cache hits, even though a prompt change can break the cache, and at the scale of millions of users that drives up cost. The model raised a blind spot and corrected it.

于是团队让它去做一项此前只保留给最资深工程师的任务：重构 Base44 的系统提示词。在大约一个小时的反问式来回沟通之后，Claude Fable 5 自主运行了四个小时，交回了他们所需内容的 90% 到 95%。借助 A/B 测试基础设施，团队当天下午就完成了这些改动的度量与上线。而在 Claude Fable 5 工作期间，它甚至指出了 Base44 自身评估体系的一个缺口：团队没有测试缓存命中（cache hits），尽管提示词的改动可能破坏缓存，而在数百万用户的规模下这会推高成本。模型发现了一个盲点，并补上了它。

When Claude Fable 5 got stuck on a change to the harness behind Base44's in-app agent, it reasoned that the same problem had probably been solved elsewhere in the codebase, went to investigate that part, and came back with the fix. "This reasoning of 'this probably has been solved somewhere else, so I should go there to investigate' is something we haven't seen so often in other models," Orlev says.

当 Claude Fable 5 在 Base44 应用内智能体背后的 harness（执行框架）的一处改动上卡住时，它推理出同样的问题很可能已经在代码库的其他地方被解决过，于是前去调查那部分代码，并带着修复方案回来了。"这种'这个问题多半在别处已经被解决过，所以我该去那里调查'的推理，我们在其他模型上并不常见，"Orlev 说。

Orlev compares working with Claude Fable 5 to working with a senior engineer. While a junior engineer needs every step specified and constant checking, you only need to brief a senior one on the goal and the why.

Orlev 把与 Claude Fable 5 的协作比作与资深工程师共事。初级工程师需要你把每一步都写清楚并不断检查，而资深工程师只需要你交代目标和背后的缘由。

This type of work extends beyond the engineering team, too. When a product manager wanted to bring native mobile app building inside Base44, he pointed Claude Fable 5 at the job and after roughly two and a half hours had a working environment that was about 90% of what the team needed to move to production.

这类工作也超出了工程团队的范畴。当一位产品经理想把原生移动应用构建能力引入 Base44 时，他把这项工作交给了 Claude Fable 5，大约两个半小时后，就得到了一个可运行的环境，达到了团队推进到生产环境所需的大约 90%。

Before Claude Fable 5, this type of work had to wait for Base44's top three engineers or a specialist to free up. Now, the model executes tasks while Orlev's team reviews, tests, and approves the code before shipping it.

在 Claude Fable 5 出现之前，这类工作只能等 Base44 最顶尖的三位工程师或某位专家腾出手来。现在，模型负责执行任务，由 Orlev 的团队在上线前评审、测试并批准代码。

![Claude Fable 5 让 Base44 的产品、工程与设计团队有信心构建平台中更具雄心的部分](images/base44-1.jpeg)

> Claude Fable 5 gives Base44's product, engineering, and design teams confidence to build more ambitious parts of their Sugeragents platform.
> Claude Fable 5 让 Base44 的产品、工程与设计团队有信心去构建其 Sugeragents 平台中更具雄心的部分。

# 下一步（What's next）

As Claude model capabilities advance, so do the Base44 team's goals for the platform. The team aims to turn Base44 from a tool that builds apps into one that also helps people manage and grow what they've built. Base44 Superagents, now public, run workflows around those apps.

随着 Claude 模型能力的提升，Base44 团队对这个平台的目标也在水涨船高。团队的目标是把 Base44 从一个构建应用的工具，变成一个还能帮助人们管理和壮大其构建成果的工具。目前已公开的 Base44 Superagents 就可以围绕这些应用运行工作流。

Knowing that they can trust Fable 5 with complex tasks, Orlev now encourages product managers and designers to build in parts of the platform they were previously not willing to touch for fear of breaking anything.

知道自己可以放心把复杂任务交给 Fable 5 之后，Orlev 现在鼓励产品经理和设计师去构建平台中那些他们此前因担心搞坏东西而不敢触碰的部分。

"Fable has given us the confidence to make bolder moves with the business," Orlev says. "It's bringing the product to a whole new area and possibilities that before that we were, I would say, scared to do."

"Fable 给了我们更大胆推进业务的信心，"Orlev 说，"它正把产品带入一个全新的领域，带来我们以前--可以说--不敢去尝试的可能性。"

Get started with Claude Fable 5.

开始使用 Claude Fable 5。
