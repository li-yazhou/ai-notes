# 将 MCP 2026-07-28 带入 Claude（中英对照）

> **原文标题：** Bringing MCP 2026-07-28 to Claude
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/bringing-mcp-2026-07-28-to-claude
> **发布日期：** 2026-07-28
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

The MCP 2026-07-28 spec is live, moving the Model Context Protocol to a stateless core with standardized extensions and hardened auth. Support is rolling out across Claude products soon. See what's new and how MCP is advancing in Claude.

MCP 2026-07-28 规范现已正式发布：Model Context Protocol（模型上下文协议）迁移到无状态内核，并带来标准化扩展与更坚固的身份验证。相关支持即将在 Claude 各产品中陆续推出。一起来看看本次更新有哪些新内容，以及 MCP 在 Claude 中的最新进展。

The fifth spec release of the Model Context Protocol, MCP 2026-07-28, is live today. The latest spec moves MCP to a stateless core, while hardening authorization and graduating official extensions. Support is being rolled out across Claude products.

Model Context Protocol（MCP，模型上下文协议）的第五个规范版本 MCP 2026-07-28 于今日正式发布。最新规范将 MCP 迁移到无状态内核（stateless core），同时强化了授权机制，并将官方扩展正式转正。相关支持正在 Claude 各产品中陆续推出。

# MCP 的新变化（What's new in MCP）

MCP recently surpassed 400M monthly SDK downloads, a 4x increase this year, and has become the industry standard for connecting AI agents to applications. MCP 2026-07-28 is one of the most significant spec releases to date:Stateless core. MCP moves from a bidirectional stateful protocol to a request/response model. Servers can now deploy on serverless and edge infrastructure. This simplifies the experience of building MCP servers for Claude and scaling their usage as they grow in adoption.

MCP 的月度 SDK 下载量近期突破了 4 亿次，较今年年初增长了 4 倍，它已成为连接 AI 智能体（agent）与应用的行业标准。MCP 2026-07-28 是迄今为止最重要的规范版本之一：无状态内核（Stateless core）。MCP 从双向有状态协议转向请求/响应模型。服务器如今可以部署在 serverless（无服务器）与边缘基础设施上。这简化了为 Claude 构建 MCP 服务器的体验，也便于随着采用规模的增长而扩展其用量。

Standardized extensions. MCP Apps and Tasks now ship under a versioned extensions framework, giving developers a formal path to add capabilities like interactive UIs and long-running work without changing the core protocol.Auth hardening. Authorization now aligns with production OAuth 2.0 and OIDC deployments, so MCP servers connect to enterprise identity systems like Entra or Okta without workarounds.

标准化扩展（Standardized extensions）。MCP Apps 与 Tasks 现在以带版本管理的扩展框架（extensions framework）发布，为开发者提供了一条正式途径，无需改动核心协议即可添加交互式 UI、长时间运行任务等能力。身份验证强化（Auth hardening）。授权机制现在与生产级 OAuth 2.0 和 OIDC 部署保持一致，MCP 服务器无需各种变通手段即可接入 Entra、Okta 等企业身份系统。

Companies across the ecosystem have been building on the new spec alongside the MCP community since beta:

自 beta 阶段以来，生态系统中的众多公司一直在与 MCP 社区一起基于新规范进行构建：

![Figma 公司 Logo](images/mcpnew-1.svg)

![Figma 公司 Logo](images/mcpnew-2.svg)

“More builders are using our MCP server to bring generated outputs into Figma's canvas, where they can explore, riff and refine them with their team into products that stand out. As that usage grows, our stateless architecture can scale with it, and with MCP Apps, Tasks, and Enterprise-Managed Auth, we can do even more to keep design and code together in one, connected flow.”

"越来越多的构建者在使用我们的 MCP 服务器，把生成式产出带入 Figma 的画布，在那里与团队一起探索、演绎、打磨，最终做出出类拔萃的产品。随着用量增长，我们的无状态架构可以随之扩展；再加上 MCP Apps、Tasks 和 Enterprise-Managed Auth（企业托管身份验证），我们还能做得更多，让设计与代码保持在同一个互联的工作流中。"

![Intuit 公司 Logo](images/mcpnew-3.svg)

![Intuit 公司 Logo](images/mcpnew-4.svg)

"MCP is the industry standard for connecting AI agents to tools and data, and Intuit is proud to support the new MCP 2026-07-28 spec. The stateless protocol core and extensions framework, including MCP Apps and Tasks, let our technologists and customers build and connect agentic experiences at enterprise scale, and allow Intuit to continue delivering trusted financial intelligence experiences to its 100 million consumers and businesses, wherever they choose to work."

"MCP 是连接 AI 智能体与工具和数据的行业标准，Intuit 很自豪能支持新的 MCP 2026-07-28 规范。无状态协议内核与扩展框架（包括 MCP Apps 和 Tasks）让我们的技术团队和客户能够在企业级规模上构建并连接智能体体验，也让 Intuit 得以继续为其 1 亿消费者和企业客户交付可信赖的财务智能体验，无论他们选择在哪里工作。"

![Netlify 公司 Logo](images/mcpnew-5.svg)

![Netlify 公司 Logo](images/mcpnew-6.svg)

"The stateless core in the 2026-07-28 spec makes MCP a first-class HTTP workload with no session management to work around. Our customers wanted MCPs on Netlify to be as simple as the rest of the platform and this new spec unlocks this at its core. Building MCP Apps into the new extensions framework is a huge step forward for scalability, accessibility, and capability across the whole ecosystem."

"2026-07-28 规范中的无状态内核让 MCP 成为一等公民（first-class）的 HTTP 工作负载，再也不需要绞尽脑汁绕开会话管理。我们的客户希望 Netlify 上的 MCP 能和平台的其他部分一样简单，而新规范从核心层面解锁了这一点。把 MCP Apps 纳入新的扩展框架，对整个生态的可扩展性、可及性和能力来说都是巨大的一步。"

![PostHog 公司 Logo](images/mcpnew-7.svg)

![PostHog 公司 Logo](images/mcpnew-8.svg)

"Moving MCP to a stateless protocol makes it easier to scale our own service and makes it easier for us to add analytics for our customers' MCP servers. This helps us show people how their MCP tools are being used and what tools are missing that their users would want to use. It's great to see this protocol growing in this direction."

"把 MCP 迁移到无状态协议，让我们自己的服务更容易扩展，也让我们更容易为客户的 MCP 服务器增加分析能力。这有助于我们向用户展示他们的 MCP 工具是如何被使用的，以及还缺少哪些用户想用而未提供的工具。很高兴看到协议朝着这个方向发展。"

![合作伙伴公司 Logo](images/mcpnew-9.svg)

![合作伙伴公司 Logo](images/mcpnew-10.png)

"Anthropic pairs frontier models with a developer experience that keeps raising the bar. The stateless core in the open MCP 2026-07-28 spec reduces the complexity we manage, so we can ship more features to our customers, faster and at scale."

"Anthropic 将前沿模型与不断拔高标准的开发者体验结合在一起。开放的 MCP 2026-07-28 规范中的无状态内核降低了我们需要管理的复杂度，使我们能够更快、更大规模地向客户交付更多功能。"

![Zoom 公司 Logo](images/mcpnew-11.svg)

![Zoom 公司 Logo](images/mcpnew-12.svg)

"At Zoom, we believe organizational context is what enables AI to deliver meaningful work, which is why we've built MCP servers that securely bring Zoom meeting intelligence into AI platforms like Claude. The new MCP spec makes it far easier to deploy and scale MCP servers on standard HTTP infrastructure — so users get Zoom's meeting intelligence faster and more reliably, right inside the AI workflows they depend on every day."

"在 Zoom，我们相信组织上下文（organizational context）正是让 AI 交付有价值工作的关键，因此我们构建了 MCP 服务器，把 Zoom 会议智能安全地引入 Claude 等 AI 平台。新的 MCP 规范让在标准 HTTP 基础设施上部署和扩展 MCP 服务器容易得多--用户因此能在他们每天依赖的 AI 工作流中，更快、更可靠地获得 Zoom 的会议智能。"

See the MCP 2026-07-28 release announcement for full details on the new spec.

关于新规范的完整细节，请参阅 MCP 2026-07-28 发布公告。

# MCP 在 Claude 中的演进（Advancing MCP in Claude）

Claude now lists over 950 MCP servers in the connectors directory, used by millions of people every day. This year we shipped support for new protocol extensions alongside features that make MCP easier to build on and deploy:MCP Apps let servers render interactive UI directly in the conversation. Users can see what a connector is doing and work with it inline, without switching tabs.Enterprise-managed auth lets admins provision MCP connectors for their whole organization through their identity provider. Admins authorize a connector once, users inherit access through their existing IdP groups, and it's connected on first login: zero-touch setup for the end user.

Claude 的连接器目录（connectors directory）目前已收录超过 950 个 MCP 服务器，每天有数百万人在使用。今年我们既发布了新协议扩展的支持，也推出了让 MCP 更易构建、更易部署的功能：MCP Apps 让服务器直接在对话中渲染交互式 UI。用户可以看到连接器正在做什么，并内联地与之协作，无需切换标签页。企业托管身份验证（Enterprise-managed auth）让管理员可以通过组织的身份提供商（identity provider）为整个组织配置 MCP 连接器。管理员只需对连接器授权一次，用户即可通过现有的 IdP 分组继承访问权限，并在首次登录时自动完成连接：对最终用户而言是零接触（zero-touch）设置。

Observability for developers building connectors gives published connectors in our directory a dashboard showing how they perform across Claude product surfaces. Developers can use it to track adoption, diagnose errors and latency, and break down usage by product.

面向连接器开发者的可观测性（Observability）功能，为发布到我们目录中的连接器提供了一个仪表盘，展示其在 Claude 各产品界面上的表现。开发者可以用它跟踪采用情况、诊断错误与延迟，并按产品细分用量。

MCP tunnels (research preview) connect Claude to MCP servers inside a private network without exposing them to the public internet. Teams can bring internal tools to Claude with no inbound firewall rules, no public endpoints, and no IP allowlisting on the origin.The stateless core, standardized extensions, and hardened auth in 2026-07-28 will help developers bring more applications to Claude, with a lower-friction, more consistent end-user experience. We'll continue investing in MCP as an open standard alongside the community, and in the Claude features that make MCP more accessible and effective in production.

MCP 隧道（tunnels，研究预览版）可以让 Claude 连接到私有网络内的 MCP 服务器，而无需将其暴露到公共互联网。团队无需入站防火墙规则、无需公共端点、也无需在源站做 IP 白名单，即可把内部工具接入 Claude。2026-07-28 中的无状态内核、标准化扩展与强化后的身份验证，将帮助开发者以更低摩擦、更一致的最终用户体验把更多应用接入 Claude。我们将继续与社区一起投资 MCP 这一开放标准，并持续完善让 MCP 在生产环境中更易用、更有效的 Claude 功能。

# 开始使用（Getting started）

Explore the spec and SDKs to get started. Support is rolling out across Claude products soon. If you're planning to submit your MCP server to Claude's connectors directory, you can learn more here.

阅读规范与各 SDK 即可开始上手。相关支持即将在 Claude 各产品中陆续推出。如果你计划把自己的 MCP 服务器提交到 Claude 的连接器目录，可以在此了解更多。
