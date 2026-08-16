# 模型发布幕后：客户提前测试 Claude Opus 4.6 时发现了什么（中英对照）

> **原文标题：** Behind the model launch: What customers discovered testing Claude Opus 4.6 early
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/behind-model-launch-what-customers-discovered-testing-claude-opus-4-6-early
> **发布日期：** 2026-02-09
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Four customer teams tested Opus 4.6 before anyone else. See their testing approaches, technical breakthroughs, and the feedback that shaped the release.

四个客户团队先于所有其他人测试了 Opus 4.6。本文呈现他们的测试方法、技术突破，以及塑造了这次发布的反馈。

Inside the tight window between pre-production access and public launch, when customers race to test what a new Claude model can really do.

走进预生产（pre-production）访问与公开发布之间那段紧凑的窗口期--彼时客户们正争分夺秒地测试一款新 Claude 模型的真实能力。

Before a new Claude model goes live, a small group of customers gets access days before the rest of the world. They work with pre-production research models, test them against real workloads to figure out what the model is great at, where it breaks, and whether it's ready to ship to their own users the moment Anthropic launches it publicly. Their honest assessments — what works and what doesn't — directly shape the version of the model Anthropic ultimately ships.

在新的 Claude 模型上线之前，一小群客户会比世界其他地方早几天获得访问权限。他们拿到的是预生产阶段的研究模型，用真实工作负载来测试，弄清模型擅长什么、在哪里出问题，以及它是否已经准备好--能否在 Anthropic 公开发布的那一刻就交付给他们自己的用户。他们的坦诚评估--哪些可行、哪些不可行--直接塑造了 Anthropic 最终发布的模型版本。

The review window is tight. Teams clear their calendars, spin up war rooms, and start throwing their hardest problems at the model. Behind the scenes, it's late nights, many cups of coffee, and Slack channels lighting up at odd hours. What their customers eventually see is polished—but the process of getting there is a lot messier and a lot more fun.

评审窗口非常紧凑。各团队清空日程、拉起作战室（war room），开始把他们最难的问题砸向模型。幕后是深夜加班、一杯又一杯咖啡，以及在不同寻常的时段不断亮起的 Slack 频道。他们的用户最终看到的是打磨光洁的成品--但抵达那里的过程要混乱得多，也有趣得多。

For this piece, we wanted to pull the curtain on what this looks like. Harvey, bolt.new, Shopify, and Lovable all gave us a look inside at their early access period with Claude Opus 4.6: the approaches they took, the breakthroughs they found, and what they learned before anyone else.

在本文中，我们想揭开这一过程的真实面貌。Harvey、bolt.new、Shopify 和 Lovable 都向我们展示了他们获得 Claude Opus 4.6 早期访问（early access）权限期间的内幕：他们采用的方法、发现的突破，以及他们比任何人都更早了解到的东西。

# 为模型测试做准备（Getting ready for model testing）

How teams kick things off depends a lot on what they're building.

各团队如何启动测试，很大程度上取决于他们在构建什么。

bolt.new spun up a dedicated Slack channel and deliberately avoided sharing impressions early so they wouldn't bias each other.

bolt.new 开设了一个专门的 Slack 频道，并刻意避免过早分享个人印象，以免彼此形成偏见。

Harvey's research team brought in experienced lawyers to test the model on legal tasks while running it through BigLaw Bench, their benchmark for real-world legal work.

Harvey 的研究团队请来经验丰富的律师，在法律任务上测试模型，同时让它跑 BigLaw Bench--他们针对真实法律工作的基准测试。

Shopify's engineers started feeding the model into iterative planning loops they'd already built around Claude.

Shopify 的工程师们开始把模型接入他们围绕 Claude 已构建好的迭代规划循环（iterative planning loops）之中。

At Lovable, the team that manages models and evals kicked into gear immediately—running benchmarks while engineers booked time to do what they call "vibe checks," building apps with the new model to feel out where it's stronger. Alexandre Pesant, engineering lead at Lovable, said, "It's a bit like Christmas."

在 Lovable，负责模型与评估（evals）的团队立刻行动起来--一边跑基准测试，一边让工程师们预约时间做他们所谓的"氛围测试"（vibe checks）：用新模型构建应用，感受它在哪里更强。Lovable 的工程负责人 Alexandre Pesant 说："有点像过圣诞节。"

The approaches were different, but the instinct was the same: throw your hardest problems at the model first.

方法各不相同，但直觉如出一辙：先把最难的问题砸向模型。

# 当结果开始陆续出现（When the results start coming in）

Once testing is underway, teams are watching for two things: how the model scores on their benchmarks, and how it feels in practice. Both matter, and they don't always tell you the same thing.

测试一旦启动，各团队会关注两件事：模型在他们的基准测试中得分如何，以及实际用起来的感受如何。两者都重要，而且它们给出的答案并不总是一致。

Harvey's BigLaw Bench results came back at 90.2%—the first Anthropic model to break 90% on that benchmark, with 40% of tasks receiving perfect scores. But it was the qualitative reaction that stuck.

Harvey 的 BigLaw Bench 成绩是 90.2%--这是第一个在该基准上突破 90% 的 Anthropic 模型，40% 的任务拿到了满分。但真正让人印象深刻的，是定性层面的反响。

One of their internal lawyers ran a single query and came back saying the output felt "smart and analytical, like it's actually thinking." When your structured evals and your subject matter experts are both saying the same thing, that's a strong signal.

他们的一位内部律师只跑了一个查询，回来就说输出给人的感觉"聪明而富有分析性，就像它真的在思考"。当你的结构化评估（evals）和你的领域专家（subject matter experts）说出同样的话时，这就是一个强烈的信号。

bolt.new.new combined their automated eval platform—which tests build quality, bug fixing, codebase understanding, and design aesthetics—with hands-on stress testing. By the end of the first day, they had a shared doc full of deployed test apps and specific observations.

bolt.new.new 把他们的自动化评估平台--该平台测试构建质量、bug 修复、代码库理解和设计美学--与上手压力测试（stress testing）结合起来。第一天结束时，他们已经拿出了一份共享文档，里面满是已部署的测试应用和具体的观察记录。

One developer had a waterfall graph bug that had failed five-plus attempts with the previous model. Opus 4.6 diagnosed it on the first try, finding eight parallel HubSpot API searches firing simultaneously and additional queries bypassing rate-limit protection by using raw fetch instead of the project's rate-limited wrapper.

一位开发者有个瀑布图（waterfall graph）bug，用上一个模型尝试了五次以上都未能解决。Opus 4.6 第一次尝试就诊断出了问题：发现有八个并行的 HubSpot API 搜索同时触发，还有一些额外查询绕过了限流（rate-limit）保护--它们使用原生 fetch，而不是项目里带限流封装的 wrapper。

At Shopify, Paulo Arruda, a Staff Engineer, described a moment that flipped the usual dynamic: "I asked Opus 4.6 to move something from one page into another menu item — that's all I said. I didn't specify any details. It not only moved it but went above and beyond, creating a lot of details I didn't even know I wanted until I saw them. It anticipated my next ask and just did it. I found myself saying 'You're absolutely right' to the AI instead of the other way around, which had been the pattern before."

在 Shopify，Staff Engineer（资深工程师）Paulo Arruda 描述了一个颠覆往常互动模式的瞬间："我让 Opus 4.6 把某个东西从一个页面移到另一个菜单项里--我就说了这么一句，没有指定任何细节。它不仅完成了移动，还远超预期，创造出许多我自己直到看见才意识到原来想要的细节。它预判了我的下一个请求，然后直接做了。我发现自己在对 AI 说'你说得对'，而不是反过来--以前一直是反过来的那种模式。"

Ben Lafferty, a Staff Engineer on Shopify's Assistants team, pushed in a different direction. He had Opus 4.6 port a large library from TypeScript to Ruby for an internal prototype. "It created a shim to run against the existing test cases in the repo, then ported over almost the entire spec in one shot while validating against the original test set," he said. "Instruction following is significantly improved. This was one of the first early access periods where I haven't had substantial feedback to give."

Shopify Assistants 团队的 Staff Engineer（资深工程师）Ben Lafferty 则从另一个方向施压。他让 Opus 4.6 为一个内部原型把一个大型库从 TypeScript 迁移（port）到 Ruby。"它创建了一个 shim（垫片），用来跑仓库里现有的测试用例，然后一次性迁移了几乎整个 spec，同时对照原始测试集做了验证，"他说。"指令遵循（instruction following）有了显著提升。这是我经历的第一个几乎没有什么实质性反馈可提的早期访问期。"

At Lovable, the testing ran on two tracks.

在 Lovable，测试沿两条轨道进行。

The team ran design benchmarks and complex task evals to get the structured picture, but they also performed what they call "vibe checks"—engineers building apps with the new model to feel where it's stronger and where it breaks.

团队跑了设计基准和复杂任务评估（evals）来获得结构化的整体图景，但他们也做了所谓的"氛围测试"（vibe checks）--工程师用新模型构建应用，感受它哪里更强、哪里会出问题。

"It's always a bit of a race to discover the new rough edges," said Alexandre Pesant.

"发现新的粗糙边缘（rough edges）总有点像一场竞赛，"Alexandre Pesant 说。

His own stress test was a side project involving complicated subway mapping and itinerary logic, something he'd tried with previous models and hit a wall on. With Opus 4.6 and max effort turned up, the model pushed past the point where he expected it to stall.

他自己的压力测试是一个业余项目，涉及复杂的地铁线路映射与出行路线逻辑--他曾用之前的模型尝试过，并撞了墙。而在 Opus 4.6 加上最大努力程度（max effort）档位后，模型越过了他预期会停滞的那个点。

"I kind of know when things are not going to work or if we're hitting the limits," he said. "It went further than others." He also noticed a broader shift: with the model's ability to use the browser and test on its own inside Lovable, "you can feel a difference in autonomy."

"我大致能感觉到什么时候行不通、什么时候撞到了极限，"他说。"它比其他模型走得更远。"他还注意到一个更广泛的变化：凭借模型在 Lovable 内部自主使用浏览器并自行测试的能力，"你能感受到自主性（autonomy）上的差异。"

# 另一侧的体验（What it's like on the other side）

By the time early access wraps up, teams have a clear picture of what they're working with. Every team we talked to kept coming back to the same point: the relationship with the model is changing.

到早期访问收尾时，各团队对自己手里的模型已经有了清晰的认识。我们交谈过的每一个团队都反复回到同一个话题：人与模型的关系正在改变。

"Opus 4.6 diagnosed bugs on the first try that we'd failed to fix across five-plus attempts with previous models. The jump in reasoning depth is real," said Garrett Serviss, VP of Marketing at bolt.new.

"我们用之前的模型尝试五次以上都没修好的 bug，Opus 4.6 第一次尝试就诊断了出来。推理深度的跃升是真实存在的，"bolt.new 市场副总裁（VP of Marketing）Garrett Serviss 说。

"For me, Opus 4.6 is the first model from Anthropic that feels like a true collaborator in my day-to-day work," said Ben Lafferty at Shopify. "The time horizon of tasks that I can hand off to the model continues to grow."

"对我来说，Opus 4.6 是 Anthropic 第一个在我日常工作中感觉像真正协作者的模型，"Shopify 的 Ben Lafferty 说。"我能交给模型的任务时间跨度（time horizon）还在不断变长。"

"Claude Opus 4.6 is an uplift in design quality," said Fabian Hedin, co-founder of Lovable. "It's more autonomous, which is core to Lovable's values. People should be creating things that matter, not micromanaging AI."

"Claude Opus 4.6 带来了设计质量的提升，"Lovable 联合创始人 Fabian Hedin 说。"它更自主，而自主正是 Lovable 价值观的核心。人们应该去创造重要的东西，而不是对 AI 进行微观管理（micromanaging）。"

Of course not all of the feedback was glowing, and that's the point. Early testers directly inform what version of the model Anthropic ultimately ships. The whole process only works because teams are as candid about what's not working as they are about what is, and they know that candor actually goes somewhere.

当然，并非所有反馈都是溢美之词，而这恰恰是关键所在。早期测试者直接影响 Anthropic 最终发布哪个版本的模型。整个流程之所以成立，是因为各团队对"哪里不行"与对"哪里行"同样坦诚，而且他们知道这份坦诚真的会被倾听并落到实处。

"We get to shape the future of tools our engineering organization will use," said Paulo Arruda at Shopify. "We're not just passive testers — we're partners in development. When we identify issues or patterns, Anthropic listens and iterates."

"我们得以塑造工程组织未来将使用的工具，"Shopify 的 Paulo Arruda 说。"我们不只是被动的测试者--我们是开发伙伴。当我们发现问题或规律时，Anthropic 会倾听并迭代。"
