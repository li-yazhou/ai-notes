# 让你的安全项目为 AI 加速的攻击做好准备（中英对照）

> **原文标题：** Preparing your security program for AI-accelerated offense
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/preparing-your-security-program-for-ai-accelerated-offense
> **发布日期：** 2026-04-10
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

We share our initial set of recommendations to shore up your defenses based on our own findings and security practices.

基于我们自己的发现与安全实践，我们分享第一批加固防御的建议。

AI is changing the speed at which vulnerabilities are found and exploited. We're publishing an initial set of recommendations to shore up your defenses based on our own findings and security practices.

AI 正在改变漏洞被发现和被利用的速度。基于我们自身的发现与安全实践，我们发布一批初步建议，帮助你加固防御。

Earlier this week, we announced Project Glasswing—our urgent attempt to put the strong cybersecurity capabilities of our newest frontier model, Claude Mythos Preview, to use for defensive purposes. In the announcement—and the accompanying technical blog post—we described how AI models are rapidly reducing the required resources, time, and skill required to find and exploit vulnerabilities in software.

本周早些时候，我们发布了 Project Glasswing--我们的一次紧急尝试，目的是把我们最新前沿模型 Claude Mythos Preview 的强大网络安全能力用于防御目的。在发布公告及配套技术博客中，我们描述了 AI 模型正在如何快速降低查找和利用软件漏洞所需的资源、时间和技能。

With an eye on the lightning-fast progress of AI, we also noted that it will not be long before models of similar capability levels are widely available. Within the next 24 months, vast numbers of bugs that sat unnoticed in code, possibly for years, will be found by AI models and chained into working exploits. Indeed, it is already the case that publicly available, sub-Mythos-level models can find serious vulnerabilities that traditional reviews have missed for long periods of time.

着眼于 AI 的闪电般进展，我们还指出：用不了多久，能力水平相近的模型就会广泛可得。未来 24 个月内，大量潜伏在代码中--可能多年未被发现--的 bug 将被 AI 模型找到，并被串接成可用的漏洞利用（exploit）。事实上，公开可用、能力低于 Mythos 水平的模型，已经能找到传统审查长期遗漏的严重漏洞。

Thankfully, this works both ways: although attackers can use AI to move faster, so can defenders who adopt AI tools to secure themselves. In this post, we offer security recommendations and practical tips based on what our security teams and researchers have observed and learned from using frontier AI models to secure real codebases and systems. We hope security teams and others will find this advice useful as we enter the age of AI-driven cybersecurity.

所幸，这件事是双向的：攻击者可以用 AI 提速，采用 AI 工具保护自己的防御者同样可以。在这篇文章中，我们基于安全团队和研究人员用前沿 AI 模型保护真实代码库与系统的观察和经验，给出安全建议和实用提示。在进入 AI 驱动的网络安全时代之际，希望安全团队和其他读者能觉得这些建议有用。

Many of the pieces of advice below are already part of the existing security consensus; we have prioritized them according to which controls we have seen hold and which we have seen degrade. If your organization reports against SOC 2 and ISO 27001, these will map directly onto controls you are already tracking.

下面的许多建议本就属于既有的安全共识；我们按照"哪些控制措施被验证仍然有效、哪些正在失效"对它们做了优先级排序。如果你的组织对照 SOC 2 和 ISO 27001 进行合规汇报，这些建议可以直接映射到你已经在跟踪的控制项上。

We'll update this guidance as we and our Project Glasswing partners continue our cybersecurity work.

随着我们和 Project Glasswing 合作伙伴持续推进网络安全工作，我们会不断更新这份指南。

# 现在该做什么（What to do now）

## 1. 关闭你的补丁缺口（1. Close your patch gap）

AI models are very effective at recognizing the signatures of known, already-patched vulnerabilities in unpatched systems. Reversing a patch into a working exploit is exactly the kind of mechanical analysis at which these models excel. This means that the window between a patch being published and an exploit becoming available is shrinking.

AI 模型非常擅长在未打补丁的系统中识别已知、已被修补漏洞的特征。把一个补丁逆向成可用的漏洞利用，恰恰是这类模型最擅长的机械分析。这意味着，从补丁发布到漏洞利用可用之间的窗口正在缩小。

- Patch everything on the CISA Known Exploited Vulnerabilities (KEV) catalog immediately. This catalog contains vulnerabilities that are confirmed to be under active exploitation. Anything on this list which is reachable from a network should be treated as an emergency.
- Use EPSS to prioritize the rest. Exploit Prediction Scoring System (EPSS) provides a daily-updated probability that a given Common Vulnerability and Exposure (CVE) will be exploited in the next 30 days. Patching the KEV list first and then everything above a chosen EPSS threshold will help you turn thousands of open CVEs into a manageable queue.
- Reduce time-to-patch on internet-exposed systems. We recommend patching internet-facing applications within 24 hours of an exploit becoming available, and within days for other vulnerabilities.
- Automate patch deployment and reboots where the risk of an automated update causing an outage is acceptable. Manual approval steps add delay, and delay is now the primary risk.

- 立即修补 CISA 已知被利用漏洞（KEV）目录中的所有条目。该目录收录已确认正处于活跃利用中的漏洞。这个列表中任何可从网络触达的条目，都应按紧急事件对待。
- 用 EPSS 为其余漏洞排定优先级。漏洞利用预测评分系统（EPSS）为每个通用漏洞披露（CVE）提供每日更新的"未来 30 天内会被利用"的概率。先修补 KEV 列表，再修补所有高于选定 EPSS 阈值的漏洞，能帮你把成千上万条未决 CVE 变成一个可管理的队列。
- 缩短暴露在互联网上的系统的补丁时延。我们建议：对面向互联网的应用，在漏洞利用出现后 24 小时内完成修补；对其他漏洞，在数天内完成。
- 在"自动化更新导致停机"的风险可接受的前提下，将补丁部署和重启自动化。人工审批步骤会带来延迟，而延迟如今正是首要风险。

Practical tip: Most cloud and OS vendors already ship patch automation; enabling it is often a simple configuration change. For container images and dependency manifests, several open-source scanners run as a single continuous integration step and annotate CVEs with data from the KEV catalogue and EPSS, so prioritization is built in.

实用提示：大多数云和操作系统厂商已内置补丁自动化，启用它往往只是一次简单的配置变更。对容器镜像和依赖清单，若干开源扫描器可以作为单个持续集成（CI）步骤运行，并用 KEV 目录和 EPSS 数据标注 CVE，优先级排序是现成的。

## 2. 为应对大得多的漏洞报告量做好准备（2. Prepare to handle a much higher volume of vulnerability reports）

Over approximately the next two years, the processes you use to receive, prioritize, and fix vulnerabilities (both in your own code and in the software you buy from vendors) will be under far more pressure than they are today. Your Vulnerability Management process should plan for many more patches, from vendors and upstream.

大致在未来两年里，你用来接收、排序和修复漏洞的流程（既包括你自己代码中的，也包括你从供应商处购买软件中的）将承受远超今天的压力。你的漏洞管理（Vulnerability Management）流程应为来自供应商和上游的多得多的补丁做好规划。

- Plan for an order-of-magnitude increase in finding volume. Aspects like intake, triage, and remediation tracking need to keep pace with the increasing numbers of vulnerabilities being exposed. If your security meetings are still built around a spreadsheet and a weekly meeting, it's unlikely that you'll keep up. It's worth considering some amount of automation—with, of course, humans in the loop, to assist with the sheer volume here.
- Check the security of your open-source dependencies. Most software supply chains are mostly open source. Most open-source projects have no service-level agreement or commitment to maintain a high level of security. OpenSSF Scorecard automatically scores every dependency on signals like branch protection, fuzzing coverage, signed releases, and maintainer activity. It runs in CI and helps to identify unmaintained packages.
- Apply the same expectations to your vendors. Your third-party risk management process should ask suppliers how they are themselves preparing for accelerated exploit timelines and whether they are scanning their own code.

- 为发现数量的数量级增长做规划。接收、分诊和修复跟踪等环节都要跟得上不断暴露的漏洞数量。如果你的安全会议还建立在一张电子表格加一次周会之上，你多半跟不上。值得考虑一定程度的自动化--当然要有人类在环（humans in the loop）--来应对这里的巨大数量。
- 检查开源依赖的安全性。大多数软件供应链的主体是开源软件，而大多数开源项目并没有服务水平协议（SLA），也没有维持高安全水平的承诺。OpenSSF Scorecard 基于分支保护、模糊测试（fuzzing）覆盖率、签名发布、维护者活跃度等信号为每个依赖自动评分。它可以在 CI 中运行，帮助识别无人维护的软件包。
- 对你的供应商提出同样要求。你的第三方风险管理流程应当询问供应商：他们自己如何为加速的漏洞利用时间线做准备，是否在扫描自己的代码。

Practical tip: Look into open source software and third-party services that evaluate the reachability of vulnerable code. Build automated processes that continuously deliver new software updates to your IT and production infrastructure, by doing regression testing on updates to gain confidence that you can deploy them quickly.

实用提示：可以考察评估脆弱代码可达性（reachability）的开源软件和第三方服务。构建能持续向你的 IT 和生产基础设施交付新软件更新的自动化流程，并通过对更新做回归测试（regression testing），建立"可以快速部署"的信心。

Above we mentioned automation of these processes. There are a number of important ways that AI can assist:

上面提到了这些流程的自动化。AI 可以在几个重要方面提供帮助：

- Speeding up triage. Triage is a bottleneck, because it requires expert review and classification. A frontier model can deduplicate findings against an existing backlog, use its knowledge of your assets to estimate exposure, and draft remediation tickets where the affected code paths are pre-identified.
- Check your dependencies for redundancy. Most large codebases accumulate multiple libraries doing the same job (several HTTP clients; several JSON parsers). This gives attackers more opportunity, all for no functional gain on your part. Pointing an LLM at a lockfile and asking which dependencies overlap (and what migration and consolidation would look like) is a one-hour exercise that often pays off.
- AI upgrade automation. Frontier models are increasingly capable of generating patches to include alongside vulnerability reports. When the report is clear and thorough, maybe even with a proof-of-concept, the model can directly test the patch to confirm that the exploit path is closed. It can also directly automate the process of accepting the upstream patch, validating that the upgrade doesn't break tests or internal systems.
- AI vendoring. Some small dependencies will score poorly on the OpenSSF Scorecard—perhaps because they're not actively maintained. You shouldn't continue to rely on these; instead, you should consider having an LLM write its own code to reimplement the functionality you actually use.

- 加速分诊。分诊是瓶颈，因为它需要专家审查和归类。前沿模型可以把发现与既有积压清单去重、利用对你资产的了解估算暴露面，并起草"受影响代码路径已被预先标出"的修复工单。
- 检查依赖的冗余。大多数大型代码库会积累多个做同一件事的库（好几个 HTTP 客户端、好几个 JSON 解析器）。这给攻击者更多机会，而你却得不到任何功能收益。让 LLM 读一遍 lockfile，问哪些依赖互相重叠（以及迁移与合并会是什么样子），这是一小时的功课，常常物有所值。
- AI 升级自动化。前沿模型越来越擅长生成可以随漏洞报告一并附上的补丁。当报告清晰完整、甚至带有概念验证（proof-of-concept）时，模型可以直接测试补丁、确认利用路径已被封堵。它还能直接自动化"接受上游补丁"的过程，验证升级不会破坏测试或内部系统。
- AI 内化（vendoring）。一些小型依赖在 OpenSSF Scorecard 上得分很差--也许因为它们已无人积极维护。你不应继续依赖它们；可以考虑让 LLM 自行编写代码，重新实现你实际用到的那部分功能。

## 3. 在 bug 上线之前找到它们（3. Find bugs before you ship them）

Prevention is always better than cure. You should assume that bugs that reach production will eventually be found, so your security testing needs to happen well before.

预防胜于补救。你应当假设进入生产的 bug 终会被发现，所以安全测试必须提前得多。

- Add static analysis and AI-assisted code review to your continuous integration pipeline, and block merges on high-confidence findings. If false positives make this impractical, you should keep the check, but address the tooling. The OWASP Application Security Verification Standard defines what "passing" a test looks like at three different levels of rigor.
- Add automated penetration testing to your continuous delivery pipeline. You can run the same scanning for staging that attackers will run against your production systems.
- Secure the build pipeline. An attacker who can inject code between commit and deployment does not need to find a vulnerability. The SLSA security framework provides a graded path: lower levels establish which commit produced which artifact, and higher levels make the build itself verifiable.
- Adopt Secure by Design practices. CISA's pledge commitments (multi-factor authentication by default; no default passwords; transparent vulnerability reporting) are a reasonable minimum bar.
- Prefer memory-safe languages for new code. A large share of severe vulnerabilities are memory-safety bugs that do not occur in Rust, Go, or managed runtimes. CISA, the NSA, and the NCSC have published useful roadmaps. Existing C/C++ code does not need to be rewritten, but new C/C++ code should require a justification. AI assisted rewrites are increasingly viable, as well.

- 在持续集成流水线中加入静态分析和 AI 辅助代码审查，并对高置信度的发现阻断合并。如果误报让这难以落地，你应当保留这道检查，而去解决工具问题。OWASP 应用安全验证标准（ASVS）定义了在三个不同严格级别下"通过"测试分别意味着什么。
- 在持续交付流水线中加入自动化渗透测试（penetration testing）。你可以对预发（staging）环境运行与攻击者将对你的生产系统运行的相同扫描。
- 加固构建流水线。能在提交与部署之间注入代码的攻击者根本不需要找漏洞。SLSA 安全框架提供了一条分级路径：较低级别确定哪个提交产出了哪个工件（artifact），较高级别让构建本身可验证。
- 采纳"安全设计（Secure by Design）"实践。CISA 的承诺（默认多因素认证、无默认密码、透明的漏洞报告）是一个合理的最低标准。
- 新代码优先使用内存安全（memory-safe）语言。大量严重漏洞属于内存安全 bug，而它们不会发生在 Rust、Go 或托管运行时中。CISA、NSA 和 NCSC 已发布了有用的路线图。既有的 C/C++ 代码不需要重写，但新的 C/C++ 代码应当要求给出理由。AI 辅助重写也越来越可行。

Practical tip: Static application security testing (SAST) tooling that runs as a CI action with OWASP Top 10 and language-specific rule sets is widely available, both open-source and built into code hosting platforms (CodeQL on GitHub being the most common starting point). To assess build provenance, OpenSSF publishes a reusable workflow that produces SLSA Level 3 attestations from GitHub Actions; adopting it is significantly less work than the SLSA spec suggests.

实用提示：以 CI 动作形式运行、带 OWASP Top 10 和语言专属规则集的静态应用安全测试（SAST）工具已广泛可得，既有开源的，也内置于代码托管平台（GitHub 上的 CodeQL 是最常见的起点）。评估构建溯源（provenance）方面，OpenSSF 发布了一个可复用工作流，能从 GitHub Actions 产出 SLSA 3 级证明（attestation）；采纳它的工作量远比 SLSA 规范暗示的要少。

As before, there are some clear opportunities for accelerating this work with AI:

与前面一样，用 AI 加速这项工作也有几个明确的机会：

- AI vulnerability scanning. The logic here is straightforward: you should scan your own code and systems with the same kind of model an attacker would use, before they do. This approach just requires an isolated agent, a verification step to filter noise, and a path into your existing triage process. You can do this with an LLM today. If you implement one thing from this section, implement this.
- Patch generation. When SAST or a scanner produces a finding, a frontier model can usually propose a patch for it. This does not remove the need for review, but it changes the developer's job from "understand the bug and write a fix" to "verify a proposed fix is correct." The latter is faster. The same approach applies to memory-safe migration: LLMs can port a self-contained C module to Rust with tests; a reviewer can validate the equivalence rather than writing the whole thing from scratch.

- AI 漏洞扫描。逻辑很直接：你应该在攻击者之前，用与攻击者同类的模型扫描你自己的代码和系统。这个做法只需要一个隔离的智能体（agent）、一个过滤噪声的验证步骤、以及一条接入你现有分诊流程的通道。今天用 LLM 就能做到。如果这一节你只落地一件事，就落地这一件。
- 补丁生成。当 SAST 或扫描器产出一条发现，前沿模型通常能为它提出补丁。这并不免除审查，但把开发者的工作从"理解 bug 并编写修复"变成"核实一个给出的修复是否正确"。后者更快。同样的思路适用于内存安全迁移：LLM 可以把一个自包含的 C 模块连同测试一起移植到 Rust；审查者验证等价性即可，而不必从零重写全部。

## 4. 找出你代码中已有的漏洞（4. Find the vulnerabilities already in your code）

Patching addresses known vulnerabilities in software you depend on. But your own codebase contains unknown ones. Most long-running production code has been reviewed by humans many times, but has never been examined by a frontier model, and that kind of analysis tends to surface new, previously-overlooked issues. Proactively scanning can identify vulnerabilities that are within the reach of modern LLMs before attackers discover them themselves.

修补解决的是你所用软件中的已知漏洞，但你自己的代码库里藏着未知的那些。大多数长期运行的生产代码被人类审查过很多次，却从未被前沿模型检视过，而这类分析往往能带出新的、此前被忽略的问题。主动扫描可以在攻击者自己发现之前，找出处于现代 LLM 能力范围之内的漏洞。

- Prioritize by exposure. Start with code that parses untrusted input, enforces an authentication or authorization decision, or is reachable from the internet. These are the paths where a finding is most likely to matter.
- Include legacy code. Code that predates current review practices, or whose original authors have moved on, often has the least recent scrutiny. That's where you have the most to gain from a fresh pass.
- Budget for remediation. A well-structured model scan of older code typically produces fewer findings than a SAST rollout, but a higher share of them are real. Plan engineering time to fix the bugs.

- 按暴露程度排优先级。从解析不可信输入、执行认证或授权判定、或可从互联网触达的代码开始。这些路径上的发现最有可能是要紧的。
- 把遗留代码包括进来。早于现行审查实践的代码，或原作者早已离开的代码，往往最近受到的审视最少。在那里，一次全新扫描的收益最大。
- 为修复做预算。对较老代码做一次结构良好的模型扫描，产出的发现通常比一次 SAST 推广要少，但其中真实的比例更高。要为修复这些 bug 规划工程时间。

Practical tip: Pick one internet-facing service with few current owners and scan its input handling and auth logic. Run the agent in isolation and add a verification step so you're acting on confirmed findings. One service done properly is a reasonable basis for estimating what a broader program will cost.

实用提示：挑一个当前少人认领的面向互联网的服务，扫描它的输入处理和认证逻辑。让智能体在隔离环境中运行，并加上一个验证步骤，确保你行动的依据是已确认的发现。认真做好一个服务，就是估算更大范围项目成本的合理基础。

## 5. 假设会被攻破来设计（5. Design for breach）

Attackers will try to get a foothold somewhere. You need to limit what they can reach from there.

攻击者总会想办法在某个地方取得立足点。你需要限制他们从那里能触达的范围。

Mitigations whose value comes from friction—making an attack tedious—rather than a hard barrier (extra pivot hops, rate limits, non-standard ports, SMS-based MFA) are much less effective against an adversary that can grind through those tedious steps. Our recommendations below favor controls that hold even when the attacker has unlimited patience: hardware-bound credentials, expiring tokens, and network paths that do not exist rather than paths that are merely inconvenient.

那些价值来自"摩擦"--让攻击变得繁琐--而非硬屏障的缓解措施（额外的跳板、速率限制、非标准端口、基于短信的多因素认证），面对一个能把繁琐步骤硬磨过去的对手，效果会大打折扣。下面我们的建议偏爱那些"即使攻击者有无限耐心也依然成立"的控制：硬件绑定的凭据、会过期的令牌、以及"根本不存在的网络路径"，而不是"只是不太方便的路径"。

- Adopt zero trust architecture. Authenticate and authorize every request between services as if it came from the internet. CISA's Zero Trust Maturity Model and the NCSC's zero trust principles both provide staged adoption paths.
- Tie access to verified hardware rather than credentials. Production systems and sensitive internal tools should only be reachable from managed employee devices with attested hardware identity, paired with phishing-resistant 2FA (FIDO2 or passkeys). Stolen credentials alone should never be sufficient to gain access. Even calls between production services should be rooted in hardware identity.
- Isolate services by identity. A compromised build server should not be able to query production databases. A compromised laptop should not be able to reach build infrastructure. Enforce this at the receiving end: every workload should carry its own cryptographic identity, and each service should accept connections only from the specific callers of its policy names. Network segmentation can still reduce blast radius and noise, but it is a backstop.
- Replace long-lived secrets with short-lived tokens. Static API keys, embedded credentials, and shared service-account passwords are among the first things an attacker with model-assisted code analysis will find. Use short-lived, narrowly-scoped tokens issued by an identity provider.

- 采用零信任（Zero Trust）架构。像每个请求都来自互联网那样，对服务间的每个请求做认证和授权。CISA 的零信任成熟度模型和 NCSC 的零信任原则都提供了分阶段的采纳路径。
- 把访问绑定到经过验证的硬件而非凭据。生产系统和敏感内部工具应当只能从具备硬件身份证明（attested hardware identity）的受管员工设备访问，并配合防钓鱼的第二因素（FIDO2 或 passkey）。仅仅窃取凭据永远不应足以获得访问。甚至生产服务之间的调用也应根植于硬件身份。
- 按身份隔离服务。一台被攻陷的构建服务器不应能查询生产数据库；一台被攻陷的笔记本不应能触达构建基础设施。在接收端强制执行这一点：每个工作负载都应携带自己的密码学身份，每个服务只接受其策略所指名的特定调用方。网络分段（segmentation）仍可减少波及范围（blast radius）和噪声，但它只是兜底。
- 用短时令牌取代长效秘密。静态 API 密钥、内嵌凭据和共享的服务账号密码，是拿着模型辅助代码分析的攻击者最先找到的东西之一。使用由身份提供商（identity provider）签发的短时、窄范围令牌。

Practical tip: Full zero-trust is a multi-year program, but an identity-aware access proxy puts device-verified, MFA-gated access in front of internal services without having to fundamentally change their architecture. Each major cloud provider offers a native option, and several open-source and commercial alternatives exist for on-premises or multi-cloud environments. For secrets, every major cloud has a managed secrets store; moving the single most widely-shared credential into one and rotating it is a useful forcing function for the rest.

实用提示：完整的零信任是多年的项目，但一个身份感知访问代理（identity-aware proxy）可以把"设备验证 + MFA 把关"的访问放到内部服务前面，而不必从根本上改变其架构。每个主要云厂商都有原生选项，本地或多云环境也有若干开源与商业替代。秘密管理方面，每家主要云都有托管秘密存储；把那一个被共享得最广的凭据迁进去并轮换掉，对其余凭据的治理是一个有用的倒逼机制。

## 6. 减少并盘点你的暴露面（6. Reduce and inventory what you expose）

This section is based on two important principles. First, you cannot defend systems you don't know about. Second, the smaller the exposed surface, the less there is to attack.

本节基于两条重要原则。第一，你无法防御你不知道的系统。第二，暴露面越小，可被攻击的就越少。

- Maintain a current inventory of every internet-facing host, service, and API endpoint in your systems. Attackers can run automated reconnaissance; your inventory should be at least as accurate. Include these systems in your pentests and red-teaming.
- Decommission unused systems. Legacy services with no clear owner are typically also unpatched.
- Minimize what each service exposes. Default-deny network ingress and limit API surface area to what is actually required.

- 维护一份最新的资产清单，覆盖你系统中每个面向互联网的主机、服务和 API 端点。攻击者可以跑自动化侦察；你的清单至少要一样准确。把这些系统纳入你的渗透测试和红队（red-teaming）演练。
- 下线闲置系统。没有明确负责人的遗留服务通常也没打补丁。
- 最小化每个服务的暴露。网络入口默认拒绝（default-deny），并把 API 面积限制在实际需要的范围。

Practical tip: Internet-wide scan indexes are publicly searchable; querying one for your own IP ranges and domains shows you what an attacker's reconnaissance sees. For cloud assets, native inventory tools (AWS Config, Azure Resource Graph, GCP Asset Inventory) already exist; the work is in querying them.

实用提示：全网扫描索引是公开可查的；拿你自己的 IP 段和域名去查一查，看到的就是攻击者侦察时看到的东西。云上资产方面，原生清点工具（AWS Config、Azure Resource Graph、GCP Asset Inventory）已经存在，功夫在于去查询它们。

AI can help directly here, too:

AI 在这里也能直接帮上忙：

- Pruning stale code and systems. Identifying unused code is tedious—but as noted above, AI models are good at tedious tasks. A model with read access to a codebase and traffic logs can list endpoints that have no callers and have not received traffic; from there, it can explain what removing each one would affect.
- Autonomous external red-teaming. Point an AI offensive agent at your own perimeter from the outside, with no credentials and no source access. Then, let it do what an attacker would: work out what is reachable, fingerprint it, and attempt to chain what it finds into a foothold. This kind of automated red-teaming can catch things source scanning doesn't see: forgotten hosts, exposed management interfaces, default credentials, and misconfigured storage. Run it on the same cadence as your inventory refresh.

- 清理陈旧代码和系统。识别无人使用的代码很枯燥--但正如上文所说，AI 模型擅长枯燥任务。一个对代码库和流量日志有读权限的模型，可以列出没有任何调用方、也没有流量的端点；并能进一步解释移除每一个会影响什么。
- 自主外部红队。从外部、不给凭据、不给源码访问，把一个 AI 攻击智能体指向你自己的边界。然后让它做攻击者会做的事：摸清什么可达、做指纹识别、尝试把手头发现串接成立足点。这种自动化红队能抓住源码扫描看不到的东西：被遗忘的主机、暴露的管理接口、默认凭据、配置错误的存储。按与你资产清单刷新相同的节奏运行它。

## 7. 缩短你的事件响应时间（7. Shorten your incident response time）

Exploits can appear within hours of a patch. Response processes that take days are too slow. Here are some ideas for how to reduce your incident response time:

漏洞利用可能在补丁发布后几小时内出现。以"天"计的响应流程太慢了。以下是一些缩短事件响应时间的思路：

- Put a model at the front of your alert queue. Every inbound alert should get an automated first-pass investigation before a human sees it. This kind of "triage agent" with read-only access to your Security Information and Event Management (SIEM) platform and a well-scoped set of query tools can direct your attention to the alerts that need human judgement most.
- Put instrument dwell time and coverage before anything else. These are the two metrics that AI automation has the greatest ability to move; both matter most when exploit windows shorten.
- Automate the bookkeeping around incidents. During an active incident, models should be taking notes, capturing artifacts, pursuing parallel investigation tracks, and drafting the postmortem and root-cause analysis. On the other hand, humans should be making the containment calls, disclosure calls, and customer-comms calls. Human decision speed during an incident should never be rate-limited on aspects that would be better handed to an AI, like evidence collection or write-ups.
- Let models drive the detection flywheel. Ingesting threat intelligence, generating candidate detections, hunting for matches, and tuning what fires are all now within reach of frontier models, who can run the process end-to-end.
- Run a tabletop for five simultaneous incidents. The standard exercise assumes one critical CVE with a working exploit hits on a Monday. Given the improved AI capabilities we're seeing, this might be unwise. To truly stress-test your responses, you should run the version where five incidents hit in the same week.
- Map detection coverage against MITRE ATT&CK. ATT&CK provides a standard vocabulary of attacker techniques that most detection tools already use. Knowing which techniques you can detect (and which you can't), is more useful than a general goal to "improve detection." You should prioritize coverage for lateral movement and credential access.
- Establish emergency change procedures in advance. A two-week change-approval cycle for production patches is itself a security risk. The same applies to emergency containment actions (like taking a service offline, rotating a credential, or blocking a network path). You should decide in advance who can authorize these and how fast.

- 在告警队列的最前端放一个模型。每条进入的告警，都应在人看到之前先获得一次自动化初查。这种"分诊智能体"配合对安全信息与事件管理（SIEM）平台的只读访问和一组范围明确的查询工具，能把你的注意力引向最需要人工判断的告警。
- 把"驻留时间（dwell time）与覆盖率"置于一切之前。这是 AI 自动化最有能力改善的两个指标；当利用窗口缩短时，它们也最要紧。
- 自动化事件周边的事务性工作。在一次活跃事件中，模型应当负责记笔记、留存工件、并行推进多条调查线、起草事后复盘（postmortem）与根因分析（root-cause analysis）。另一面，人类应当做遏制决策、披露决策和客户沟通决策。事件中人类的决策速度，绝不应被那些本可交给 AI 的环节--比如证据收集或书面报告--所限速。
- 让模型驱动检测飞轮。摄入威胁情报、生成候选检测规则、搜寻匹配、调优触发，如今都在前沿模型的能力范围之内，它们可以把这个流程端到端跑起来。
- 为"五起同时发生的事件"做桌面演练（tabletop）。标准演练假设一个有可用漏洞利用的严重 CVE 在周一爆发。鉴于我们看到的 AI 能力提升，这可能不够明智。要真正压力测试你的响应，应当演练五个事件在同一周爆发的版本。
- 用 MITRE ATT&CK 映射检测覆盖率。ATT&CK 提供了大多数检测工具已在使用的攻击技术标准词汇表。知道你能（和不能）检测哪些技术，比"改进检测"这种笼统目标有用得多。你应优先覆盖横向移动（lateral movement）和凭据获取（credential access）。
- 提前建立紧急变更程序。为生产补丁设两周的变更审批周期，这本身就是安全风险。紧急遏制动作（下线某服务、轮换某个凭据、封堵某条网络路径）同理。你应事先决定：谁有权批准、能多快。

Practical tip: Pick one noisy rule with a known-high false positive rate. Wire a frontier model into its alert stream with read-only access to the underlying data, and have it produce a structured disposition for every firing. Measure agreement against a human reviewer for two weeks. If the agreement rate is tolerable, expand to the next rule. It's not worth trying to automate the whole queue at once. Separately, Atomic Red Team is an open-source library of small, safe tests mapped to ATT&CK techniques; running a handful and checking which ones your existing logging actually detected is a one-afternoon exercise that produces a concrete coverage map.

实用提示：挑一条噪声大、已知误报率高的规则。把一个前沿模型接入它的告警流，给它底层数据的只读权限，让它为每次触发产出结构化的处置意见。用两周时间对照人工审查者度量一致率。如果一致率可接受，再扩展到下一条规则。不值得试图一口气自动化整个队列。另外，Atomic Red Team 是一个映射到 ATT&CK 技术的小型安全测试开源库；跑几个用例、看看现有日志实际检测到了哪些，是一个下午的功课，能产出一张具体的覆盖图。

Here are some ways AI can assist with response times:

以下是一些 AI 帮助缩短响应时间的方式：

- First-pass triage at 100% coverage. A well-scoped triage agent can investigate every alert (where humans might look only at those above a given severity threshold), and produce a structured disposition a human can accept, reject, or escalate. The mechanism that makes this work is giving your model a minimal tool set (query, think, report), letting it choose its own investigation strategy, and measuring the output against operational metrics.
- Incident scribe and parallel investigator. During an active incident, a model can take contemporaneous notes, timestamp artifacts as they are collected, pursue independent investigation tracks the responder has not gotten to yet, and draft the postmortem from the transcript once the incident closes. This is the least glamorous application of frontier models to security work—but it's probably the highest-impact one.
- Proactive hunting against your own environment. The same kind of agent that can find vulnerabilities in source code can hunt for misconfigurations and indicators of compromise across your telemetry. You can run it on the same cadence as your external attack-surface scan.

- 100% 覆盖的初查分诊。一个范围明确的分诊智能体可以调查每一条告警（人类可能只看高于某个严重度阈值的那些），并产出人可以接受、拒绝或升级的结构化处置意见。让这套机制成立的关键，是给模型一个极简工具集（查询、思考、报告），让它自行选择调查策略，并依照运营指标度量其产出。
- 事件记录员与并行调查员。在一次活跃事件中，模型可以同步记录笔记、在收集时给工件打时间戳、推进响应者还没来得及处理的独立调查线，并在事件关闭后根据记录起草复盘。这是前沿模型在安全工作上最不起眼的应用--但很可能是影响最大的一个。
- 针对自身环境的主动狩猎。能在源代码中找漏洞的同一类智能体，也能在你的遥测数据中搜寻错误配置和失陷指标（IOC，indicator of compromise）。可以按与外部攻击面扫描相同的节奏运行它。

# 向他人提交漏洞报告的建议（Advice for submitting vulnerability reports to others）

If you are scanning code—your own dependencies, open-source projects, or vendor products—and reporting findings upstream, the quality of those reports determines whether anyone acts on them. Open-source maintainers are already receiving large volumes of low-quality automated reports, and many have started ignoring anything that looks AI-generated. Adding to that volume without adding signal makes the problem worse for everyone, including you.

如果你在扫描代码--你自己的依赖、开源项目或供应商产品--并向上游报告发现，这些报告的质量决定了是否有人会据此行动。开源维护者已经在接收大量低质量的自动化报告，许多人已开始无视任何看起来像 AI 生成的东西。只增加数量而不增加信号（signal），会让问题对所有人（包括你自己）更糟。

A report should be sent only when a human has verified it and is willing to put their name on it. Concretely:

只有人工验证过、并且愿意署名的报告才应该发出。具体来说：

- State the bug and its impact in plain language. A maintainer should be able to understand what is wrong and why it matters from the first paragraph, without running anything.
- Walk through the code path. Show where the input enters, where it is mishandled, and where the consequence occurs. This is the part that distinguishes a real finding from a pattern match.
- Provide a working reproduction. A proof-of-concept the maintainer can run, or a test case that fails, is more credible than any amount of explanation.
- Include a proposed patch you would accept if you were the maintainer. A patch demonstrates that the reporter understands the codebase well enough to fix the problem in a way that fits the project's conventions.
- Disclose AI involvement upfront. If a model found the bug or drafted the report, say so in the first line. Maintainers will find out anyway; concealing it costs more credibility than disclosing it.
- Defer to the maintainer's judgment. If they decline the report, you should make peace with that. The goodwill from being easy to work with is worth more than winning an argument over one bug.

- 用平实的语言说明 bug 及其影响。维护者应当不用运行任何东西，就能从第一段看懂哪里错了、为什么重要。
- 走一遍代码路径。展示输入从哪里进入、在哪里被错误处理、后果在哪里发生。正是这一部分，把真发现和模式匹配区分开来。
- 提供可运行的复现。一个维护者能跑起来的概念验证，或一个会失败的测试用例，比任何数量的解释都更可信。
- 附上"如果你是维护者也会接受"的补丁提案。补丁表明报告者对代码库的理解，足以按项目惯例的方式修复问题。
- 在开头就说明 AI 参与。如果是模型找到了 bug 或起草了报告，第一行就讲明。维护者迟早会发现；隐瞒损失的信誉远大于坦白。
- 尊重维护者的判断。如果他们拒绝了报告，你应当坦然接受。与合作融洽带来的善意，比在某个 bug 上争赢更有价值。

Practical tip: A useful self-check before sending a vulnerability report is to close the editor and explain the bug from memory. If you cannot describe what goes wrong without referring back to the model output, you do not understand it well enough to report it.

实用提示：发送漏洞报告前，一个有用的自检是：关掉编辑器，凭记忆解释这个 bug。如果离开模型输出你就描述不清哪里会出错，说明你理解得还不足以报告它。

# 如果你没有安全团队（If you don't have a security team）

Most of the above advice assumes that your organization has a dedicated security function. If you are a small organization, a solo developer, or an open-source maintainer, the same risks apply but the actions are simpler:

上面大多数建议假设你的组织有专职的安全职能部门。如果你是小组织、独立开发者或开源维护者，风险相同，但行动更简单：

- Turn on automatic updates for your operating system, browser, and every application that offers it. This is the single most effective action available and requires no ongoing effort.
- Prefer managed services over self-hosting. Letting a provider with a security team run the database, authentication, and email shifts the patching burden to them. The cost of a managed service like this is almost always lower than the cost of one incident.
- Use passkeys or hardware security keys on every account that supports them. SMS codes can be intercepted and passwords get reused; a hardware key cannot be phished.
- Enable the free security tooling on your code host. GitHub's Dependabot, secret scanning, and CodeQL are free for public repositories and catch a meaningful share of what enterprise tools catch. Enabling them takes minutes.

- 为操作系统、浏览器和所有提供该选项的应用打开自动更新。这是可采取的单个最有效行动，且不需要持续投入。
- 优先使用托管服务而非自建。让拥有安全团队的厂商来运营数据库、认证和邮件，把打补丁的担子转移给他们。这类托管服务的成本几乎总是低于一次安全事件的成本。
- 在所有支持 passkey 或硬件安全密钥的账户上使用它们。短信验证码可能被拦截，密码会被重复使用；硬件密钥无法被钓鱼。
- 启用代码托管平台上的免费安全工具。GitHub 的 Dependabot、secret scanning 和 CodeQL 对公开仓库免费，能抓住企业级工具所能抓到的一大部分。启用只需几分钟。

If you maintain an open-source project, publish a SECURITY.md stating who to contact and what to expect when they're contacted. AI-assisted scanning means you will receive more vulnerability reports than before. Some will be valuable; some will be automated noise. A clear intake process helps you tell them apart, and signals to good-faith reporters that their effort will not be wasted.

如果你维护一个开源项目，请发布一份 SECURITY.md，写明该联系谁、联系之后可以期待什么。AI 辅助扫描意味着你将收到比以往更多的漏洞报告。有些会有价值，有些会是自动化噪声。清晰的接收流程能帮你分辨二者，也向善意报告者表明他们的努力不会被浪费。

| Topic | Reference |
| --- | --- |
| Patch prioritization | CISA KEV Catalog, FIRST EPSS, CISA BOD 22-01 |
| Baseline controls | ACSC Essential Eight, CISA CPGs, CIS Controls v8, NCSC 10 Steps |
| Secure development | NIST SSDF (SP 800-218), OWASP ASVS, OWASP SAMM, CISA Secure by Design |
| Memory safety | CISA/NSA Memory Safe Roadmaps |
| Supply chain & build integrity | SLSA, OpenSSF Scorecards, CISA SBOM resources, NIST SP 800-161 |
| Zero trust | CISA Zero Trust Maturity Model, NIST SP 800-207, NCSC Zero Trust Principles |
| Detection & response | MITRE ATT&CK, MITRE D3FEND |
| Program framework | NIST Cybersecurity Framework 2.0, NCSC Cyber Assessment Framework |

| 主题 | 参考资料 |
| --- | --- |
| 补丁优先级排序 | CISA KEV 目录、FIRST EPSS、CISA BOD 22-01 |
| 基线控制 | ACSC Essential Eight、CISA CPGs、CIS Controls v8、NCSC 10 Steps |
| 安全开发 | NIST SSDF (SP 800-218)、OWASP ASVS、OWASP SAMM、CISA Secure by Design |
| 内存安全 | CISA/NSA 内存安全路线图 |
| 供应链与构建完整性 | SLSA、OpenSSF Scorecards、CISA SBOM 资源、NIST SP 800-161 |
| 零信任 | CISA 零信任成熟度模型、NIST SP 800-207、NCSC 零信任原则 |
| 检测与响应 | MITRE ATT&CK、MITRE D3FEND |
| 安全项目框架 | NIST Cybersecurity Framework 2.0、NCSC Cyber Assessment Framework |

## 致谢（Acknowledgements）

This article was written by members of Anthropic's Security Engineering and Research teams, including Donny Greenberg, Jason Clinton, Michael Moore, Abel Ribbink, and Jackie Bow, with contributions from Jannet Park, Gabby Curtis, and Stuart Ritchie.

本文由 Anthropic 安全工程与安全研究团队的成员撰写，包括 Donny Greenberg、Jason Clinton、Michael Moore、Abel Ribbink 和 Jackie Bow，Jannet Park、Gabby Curtis 和 Stuart Ritchie 亦有贡献。
