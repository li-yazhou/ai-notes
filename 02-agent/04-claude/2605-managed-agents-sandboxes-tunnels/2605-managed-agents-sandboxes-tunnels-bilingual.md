# Claude Managed Agents 新功能：自托管沙箱与 MCP 隧道（中英对照）

> **原文标题：** New in Claude Managed Agents: self-hosted sandboxes and MCP tunnels
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/claude-managed-agents-updates
> **发布日期：** 2026-05-19
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Claude Managed Agents can now operate in a sandbox you control and connect to your private Model Context Protocol (MCP) servers

Claude Managed Agents 现在可以在你控制的沙箱（sandbox）中运行，并连接你的私有 Model Context Protocol（MCP，模型上下文协议）服务器

Starting today, Claude Managed Agents can operate in a sandbox you control and connect to your private Model Context Protocol (MCP) servers. Both the sandbox where an agent executes tools and the services it reaches run within the established boundaries of your enterprise, under your security and runtime controls.

从今天起，Claude Managed Agents 可以在你控制的沙箱中运行，并连接你的私有 Model Context Protocol（MCP）服务器。智能体执行工具所在的沙箱，以及它访问的服务，都在你企业既有边界之内运行，受你的安全与运行时管控。

The sandbox runs on your own infrastructure, or with managed providers like Cloudflare, Daytona, Modal, or Vercel to handle the compute and isolation for you.

沙箱可以运行在你自己的基础设施上，也可以交给 Cloudflare、Daytona、Modal 或 Vercel 等托管提供商，由它们代为处理计算与隔离。

On the Claude Platform, self-hosted sandboxes is available in public beta and MCP tunnels in research preview (request access).

在 Claude 平台上，self-hosted sandboxes（自托管沙箱）已开放公测，MCP tunnels（MCP 隧道）处于研究预览（research preview）阶段（需申请访问）。

# 自托管沙箱：让智能体执行留在你的边界之内（Self-hosted sandboxes: keep agent execution within your perimeter）

A self-hosted sandbox lets a Claude Managed Agent execute tools on infrastructure you control or with a managed sandbox provider. Code execution, sensitive files, packages, services, and data stay within your enterprise perimeter, under your security and runtime controls.

Self-hosted sandbox 让 Claude Managed Agent 在你控制的基础设施上，或在托管沙箱提供商处执行工具。代码执行、敏感文件、软件包、服务和数据都留在你的企业边界之内，受你的安全与运行时管控。

With self-hosted sandboxes, you keep sensitive files, packages, and services in your own infrastructure or with a managed sandbox provider. The agent loop that handles orchestration, context management, and error recovery stays on Anthropic's infrastructure, while tool execution moves to your own configured environment.

使用 self-hosted sandboxes，你可以把敏感文件、软件包和服务留在自己的基础设施或托管沙箱提供商那里。负责编排、上下文管理和错误恢复的智能体循环（agent loop）仍在 Anthropic 的基础设施上运行，而工具执行则转移到你自行配置的环境中。

Inside your perimeter, network policies, audit logging, and security tooling are already in place, and files and repositories don't leave. You also control the compute: resource sizing and the runtime image are set on your side, so agents running compute-heavy work such as long builds or image generation get the CPU, memory, and capacity the task needs.

在你自己的边界之内，网络策略、审计日志和安全工具一应俱全，文件和代码库不会外流。算力也由你掌控：资源规格和运行时镜像都由你这边设定，因此运行长时间构建或图像生成等计算密集型工作的智能体，可以获得任务所需的 CPU、内存和容量。

![自托管沙箱架构示意图](images/matunnel-1.png)

# 选择你的沙箱客户端（Choose your sandbox client）

Bring any sandbox client you want, or start with one of our supported providers:

可以使用任何你想用的沙箱客户端，也可以从我们支持的提供商中选择：

- Cloudflare runs sandboxes at scale using microVMs and lighter weight isolates. Outbound network requests are in your control with zero-trust secrets injection, customizable proxies to audit, reroute, or modify egress, and the ability to connect to internal services over Cloudflare's network. Amplitude is building Design Agent, an internal tool for on-brand production UI and marketing design, on Managed Agents and Cloudflare for tighter observability and control.
- Daytona sandboxes are full composable computers, long-running and stateful. The same primitive runs a quick burst or an agent that works for hours. The sandbox stays accessible while a session runs over SSH or an authenticated preview URL, or can be paused and restored with full state preserved. Clay's GTM engineering agent, Sculptor, builds, tests, and monitors workflows autonomously on Managed Agents and Daytona.
- Modal is a cloud platform built for AI workloads, where sandboxes share the same foundation as Modal's functions, storage, and networking primitives, giving you everything you need to build production AI systems. Modal's custom container runtime delivers sub-second startup on any image, scales to hundreds of thousands of concurrent sandboxes, and gives you CPU and GPU resources on demand.
- Vercel sandboxes combine VM security, VPC peering, and bring your own cloud with millisecond startup time. Managed Agents handles the model, tools, and session state, while the Vercel Sandbox firewall injects credentials at the network boundary so they never enter the sandbox. Rogo, an AI platform for institutional finance, is building an analyst agent on Managed Agents and Vercel Sandbox to handle their proprietary data securely.

- Cloudflare 使用 microVM（微虚拟机）和更轻量的 isolate（隔离实例）来大规模运行沙箱。出站网络请求尽在你掌握：零信任（zero-trust）密钥注入、可自定义的代理用于审计、重定向或修改出站流量（egress），还能通过 Cloudflare 网络连接内部服务。Amplitude 正在基于 Managed Agents 和 Cloudflare 构建 Design Agent--一个用于品牌一致的生产级 UI 和营销设计的内部工具，以获得更强的可观测性与控制力。
- Daytona 沙箱是完整的可组合计算机，可长时间运行并保有状态。同一套原语（primitive）既能跑一次短促的爆发式任务，也能支撑连续工作数小时的智能体。会话进行期间，沙箱可通过 SSH 或经过身份验证的预览 URL 保持可访问，也可以暂停并在完整保留状态后恢复。Clay 的 GTM 工程智能体 Sculptor 就在 Managed Agents 和 Daytona 上自主构建、测试和监控工作流。
- Modal 是专为 AI 工作负载打造的云平台，其沙箱与 Modal 的函数、存储和网络原语共享同一套基础，构建生产级 AI 系统所需的一切一应俱全。Modal 自研的容器运行时可在任意镜像上实现亚秒级启动，可扩展到数十万个并发沙箱，并按需提供 CPU 和 GPU 资源。
- Vercel 沙箱将虚拟机级安全、VPC 对等连接（VPC peering）与自带云（bring your own cloud）相结合，启动时间以毫秒计。Managed Agents 负责模型、工具和会话状态，而 Vercel Sandbox 防火墙在网络边界注入凭证，使其从不进入沙箱。机构金融 AI 平台 Rogo 正在基于 Managed Agents 和 Vercel Sandbox 构建分析师智能体，以安全地处理其专有数据。

# MCP 隧道：连接私有网络内的服务（MCP tunnels: Connect to services within your private network）

MCP tunnels connect Claude Managed Agents to Model Context Protocol (MCP) servers inside your private network without exposing them to the public internet. Internal databases, private APIs, knowledge bases, and ticketing systems become tools your agents can call. A lightweight gateway you deploy makes a single outbound connection, no inbound firewall rules, no public endpoints, and traffic encrypted end to end.

MCP tunnels 将 Claude Managed Agents 连接到你私有网络内的 Model Context Protocol（MCP）服务器，而无需将其暴露到公共互联网。内部数据库、私有 API、知识库和工单系统都变成智能体可调用的工具。你只需部署一个轻量网关，发起单一出站连接即可--无需入站防火墙规则，没有公开端点，流量全程端到端加密。

MCP tunnels is supported in Managed Agents and the Messages API. MCP tunnels is managed from workspace settings within the Claude Console by organization admins.

Managed Agents 和 Messages API 均支持 MCP tunnels。组织管理员可在 Claude Console 的工作区设置中管理 MCP tunnels。

![MCP tunnels 示意图](images/matunnel-2.png)

![公司 Logo](images/matunnel-3.svg)

![公司 Logo](images/matunnel-4.svg)

"When building Sculptor, Clay's GTM engineering agent for building and testing GTM workflows autonomously, we wanted to give it a more flexible and powerful way to take actions than just tools in a loop. Claude Managed Agents let us replicate the power of a local agent with the reliability, versioning, and background execution of a cloud agent. And running it with our sandboxes, like Daytona, gives us control over the filesystem, so we can mount external file stores and install packages on the fly."

"在构建 Sculptor（Clay 的 GTM 工程智能体，用于自主构建和测试 GTM 工作流）时，我们想给它一种比'循环里挂几个工具'更灵活、更强大的行动方式。Claude Managed Agents 让我们既能复刻本地智能体的能力，又拥有云端智能体的可靠性、版本管理和后台执行。再加上与 Daytona 等我们自己的沙箱一起运行，文件系统也尽在掌握，我们可以挂载外部文件存储，并随时安装软件包。"

![公司 Logo](images/matunnel-5.svg)

![公司 Logo](images/matunnel-6.svg)

"Claude Managed Agents handles the agent loop, Vercel's sandboxes give us an environment we can configure for our workloads. This gives us the option to leverage best-in-class infrastructure while we focus on what compounds for a financial AI platform: depth and breadth of tools and data, and a product surface built for how investors and bankers actually work."

"Claude Managed Agents 负责智能体循环，Vercel 的沙箱则给我们一个可按自身工作负载定制的环境。这让我们得以依托一流的基础设施，同时专注于对金融 AI 平台能产生复利效应的事情：工具与数据的深度和广度，以及一个真正贴合投资者和银行家实际工作方式的产品界面。"

![公司 Logo](images/matunnel-7.svg)

![公司 Logo](images/matunnel-8.svg)

"Our use cases require secure orchestration of internal tools across a complex product surface. Modal's sandbox gives us the security boundary our enterprise customers need, and combining it with Claude Managed Agents gives us a powerful harness without hand-rolling extra complexity. We had a working version up in under a week, raising reliability for our customers."

"我们的使用场景需要在复杂的产品界面上安全地编排内部工具。Modal 的沙箱提供了企业客户所需的安全边界，再与 Claude Managed Agents 相结合，我们就获得了一个强大的 harness，而无需亲手堆叠额外的复杂度。不到一周我们就跑通了可用版本，为客户提升了可靠性。"

![公司 Logo](images/matunnel-9.svg)

![公司 Logo](images/matunnel-10.svg)

"Claude Managed Agents and Cloudflare let us get the first useful version of our design agent running in two days on infrastructure we already know and trust."

"借助 Claude Managed Agents 和 Cloudflare，我们只花两天就在自己早已熟悉且信任的基础设施上，让设计智能体的第一个可用版本跑了起来。"

![公司 Logo](images/matunnel-11.svg)

![公司 Logo](images/matunnel-12.svg)

"As we scale agentic commerce for local businesses, we need a highly efficient path to production with full harness control, scale, and reliability. We're excited to evaluate Claude Managed Agents for this next step, building on our Al infrastructure with Modal!"

"随着我们把面向本地商家的智能体商务（agentic commerce）规模化，我们需要一条通往生产环境的高效路径，兼具完整的 harness 控制、可扩展性和可靠性。我们很高兴在这一步评估 Claude Managed Agents，在 Modal 上构建我们的 AI 基础设施！"

# 开始使用（Getting started）

Both self-hosted sandboxes and MCP tunnels work within the same core primitives supported by Managed Agents. Self-hosted sandboxes is available in public beta and MCP tunnels in research preview. To get started with MCP tunnels, request access.

Self-hosted sandboxes 和 MCP tunnels 都在 Managed Agents 支持的同一套核心原语之内运作。Self-hosted sandboxes 已开放公测，MCP tunnels 处于研究预览阶段。要开始使用 MCP tunnels，请申请访问。

Explore our docs to learn more, follow our cookbooks to set up your sandbox provider, or deploy your first agent in the Claude Console.

查阅我们的文档了解更多，参照我们的 cookbook（实操手册）设置你的沙箱提供商，或前往 Claude Console 部署你的第一个智能体。
