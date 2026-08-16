# 用 Skills 构建智能体：让智能体胜任专业化工作（中英对照）

> **原文标题：** Building agents with Skills: Equipping agents for specialized work
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/building-agents-with-skills-equipping-agents-for-specialized-work
> **发布日期：** 2026-01-22
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Learn how Agent Skills package domain expertise for AI agents-turning capable generalists into knowledgeable specialists through organized files and workflows.

了解 Agent Skills 如何为 AI 智能体打包领域专业知识--通过组织良好的文件和工作流，把能力全面的多面手变成知识扎实的专家。

Skills package domain expertise in files agents can access and apply-turning general-purpose agents into knowledgeable specialists for real work.

Skills 把领域专业知识打包成智能体可以访问并应用的文件--把通用智能体变成能胜任实际工作、知识扎实的专家。

A lot has changed in the past year. MCP became the standard for agent connectivity with rapid adoption from industry leaders and the developer community. Claude Code launched as a general-purpose coding agent. And we launched the Claude Agent SDK, which now provides a production-ready agent out of the box.

过去一年发生了很多变化。MCP 成为智能体连接（connectivity）的标准，并迅速获得行业领袖和开发者社区的采纳。Claude Code 作为通用编程智能体发布。我们还发布了 Claude Agent SDK，如今它能开箱即用地提供一个可投入生产的智能体。

But as we've built and deployed these agents, we keep running into the same gap: agents have intelligence and capabilities, but not always the expertise to effectively tackle real work. This led us to create Agent Skills. Skills are organized collections of files that package domain expertise - workflows, best practices, scripts - in a format agents can access and apply. They turn a capable generalist into a knowledgeable specialist.

但在构建和部署这些智能体的过程中，我们不断遇到同一个缺口：智能体拥有智能和能力，却未必拥有有效应对实际工作所需的专业知识（expertise）。这促使我们创建了 Agent Skills。Skills 是组织良好的文件集合，以智能体可以访问并应用的格式打包领域专业知识--包括工作流、最佳实践和脚本。它们把能力全面的多面手变成知识扎实的专家。

In this post, we'll explain why we stopped building specialized agents and started building skills instead, and how this shift is changing how we think about extending agent capabilities.

在这篇文章中，我们将解释为什么我们不再构建专用智能体，转而构建 Skills，以及这一转变如何改变了我们对扩展智能体能力的思考方式。

# 新范式：代码即一切（The new paradigm: code is all you need）

We used to think agents in different domains would look very different. A coding agent, a research agent, one for finance, one for marketing-each seemed to need its own tools and scaffolding. The industry initially embraced this model of domain-specific agents. But as models improved in intelligence and agent capabilities progressed, we converged on a different approach.

我们曾经以为不同领域的智能体会长得截然不同：编程智能体、研究智能体、财务智能体、营销智能体--每一个似乎都需要自己的工具和脚手架（scaffolding）。业界最初也接受了这种领域专用智能体的模式。但随着模型智能水平的提升和智能体能力的进步，我们逐渐收敛到了另一种做法。

![示意图：各领域专用智能体收敛为同一种通用架构](images/skillsbuild-1.png)

We came to see code less as just a use case and more as an interface for agents to do almost any digital work. Claude Code is a coding agent, but also a general-purpose agent that happens to work through code.

我们逐渐认识到，代码不只是智能体的一个使用场景，更是智能体完成几乎任何数字化工作的接口。Claude Code 是一个编程智能体，同时也是恰好通过代码来工作的通用智能体。

![示意图：代码作为智能体完成各类数字工作的接口](images/skillsbuild-2.png)

Consider working with Claude Code to generate a financial report. It can call APIs for research, store data in the filesystem, analyze it with Python, and synthesize insights. All of that happens through code. The scaffolding becomes as simple as bash and a filesystem.

想象用 Claude Code 生成一份财务报告。它可以调用 API 做研究，把数据存入文件系统，用 Python 分析数据，并综合出洞见。这一切都通过代码完成。脚手架简化到只剩 bash 和一个文件系统。

But general capability isn't the same as expertise. When we started using Claude Code for real work, a gap emerged.

但通用能力不等于专业知识。当我们开始用 Claude Code 处理真实工作时，一个缺口显现出来。

# 缺失的一环：领域专业知识（The missing piece: domain expertise）

Who would you want filing your taxes: a math genius figuring it out from first principles, or an experienced tax professional who's filed thousands of returns? Most people would choose the tax professional. Not because they're smarter, but because they have the right expertise.

报税这件事，你会交给谁：一个从第一性原理开始推导的数学天才，还是一个填报过数千份申报表的资深税务师？大多数人会选税务师。不是因为他更聪明，而是因为他拥有正确的专业知识。

Agents today are like that math genius: brilliant at reasoning through novel situations, but often lacking the accumulated expertise of a seasoned professional. They can do amazing things with proper guidance. However, they're often missing important context, can't easily absorb your organization's expertise, and don't automatically learn from repeated tasks.

今天的智能体就像那个数学天才：面对陌生情境时推理能力出众，却往往缺少资深专业人士日积月累的专业知识。在恰当的指引下，它们能做出惊人的成果。但是，它们常常缺少重要的上下文，难以吸收你所在组织的专业知识，也不会从重复性任务中自动学习。

Skills bridge this gap by packaging domain expertise in a format that agents can progressively access and apply.

Skills 弥补了这个缺口：它把领域专业知识打包成智能体可以渐进访问和应用的格式。

# 什么是 Agent Skills？（What are Agent Skills?）

Skills package domain expertise and procedural knowledge for agents.

Skills 为智能体打包领域专业知识和程序性知识（procedural knowledge）。

```
anthropic_brand/
├── SKILL.md
├── docs.md
├── slide-decks.md
└── apply_template.py
```

The simplicity of skills is deliberate. Files are a universal primitive that works with what you already have. You can version them with Git, store them in Google Drive, and share them with your team. This simplicity also means skill creation isn't limited to engineers. Product managers, analysts, and domain experts are already building skills to codify their workflows.

Skills 的简单是刻意为之。文件是一种通用原语（primitive），与你已有的一切都能配合。你可以用 Git 对它们做版本管理，把它们存进 Google Drive，并与团队共享。这种简单也意味着创建 Skill 并不局限于工程师。产品经理、分析师和领域专家已经在构建 Skills，把他们的工作流沉淀成可复用的形式。

# 渐进式披露（Progressive disclosure）

Skills can contain extensive information. To protect the context window and make skills composable, they use progressive disclosure: at runtime, only the metadata (name and description from the YAML frontmatter) is shown to the model.

Skills 可以包含大量信息。为了保护上下文窗口（context window）并让 Skills 可组合，它们采用渐进式披露（progressive disclosure）：运行时，只有元数据（YAML frontmatter 中的 name 和 description）会展示给模型。

```
---
name: Anthropic Brand Style Guidelines
description: Anthropic's official brand colors and typography…
---
```

If Claude determines a skill is needed, it reads the full SKILL.md file. For additional detail, skills can include a references/ directory with supporting documentation loaded only on demand.

如果 Claude 判断需要某个 Skill，它会读取完整的 SKILL.md 文件。如需更多细节，Skills 还可以包含一个 references/ 目录，存放只在需要时才加载的支撑文档。

This three-tier approach means you can equip an agent with hundreds of skills without overwhelming its context window-metadata uses ~50 tokens, full SKILL.md files ~500 tokens, and reference files 2,000+ tokens and only when specifically needed.

这种三层结构意味着你可以为一个智能体配备数百个 Skills，也不会撑爆它的上下文窗口--元数据约占 50 个 token，完整 SKILL.md 约 500 个 token，参考文件 2,000+ 个 token 且只在确实需要时才加载。

# Skills 可以把脚本作为工具纳入（Skills can include scripts as tools）

Traditional tools have problems: some have poorly written instructions, the model can't always modify or extend them, and they often bloat the context window. Code, on the other hand, is self-documenting, modifiable, and doesn't need to be in context at all times.

传统工具存在一些问题：有的指令写得很差，模型不一定能修改或扩展它们，而且它们经常把上下文窗口撑得很大。相比之下，代码是自文档化（self-documenting）的、可修改的，也不需要始终驻留在上下文中。

Here's a real example: we kept seeing Claude write the same script to apply Anthropic styling to slides. So we asked Claude to save it as a tool for itself:

这是一个真实例子：我们一再看到 Claude 编写同样的脚本来为幻灯片应用 Anthropic 风格。于是我们让 Claude 把它保存为自己可用的工具：

```python
# anthropic/brand_styling/apply_template.py
import sys
from pptx import Presentation

if len(sys.argv) != 2:
    print("USAGE: apply_template.py <pptx>")
    sys.exit(1)

prs = Presentation(sys.argv[1])
for slide in prs.slides:
    ...
```

The corresponding documentation in slide-decks.md simply references this script:

slide-decks.md 中相应的文档只是简单地引用了这个脚本：

```markdown
## Anthropic Slide Decks

- Intro/outro slides
  - background color: `#141413`
  - foreground color: oat
- Section slides:
  - background color: `#da7857`
  - foreground color: `#141413`

Use the `./apply_template.py` script to update a pptx file in-place.
```

# Skills 生态系统（The skills ecosystem）

The skills ecosystem has emerged quickly, and so far we've seen three major types of skills being built:

Skills 生态系统发展得很快，到目前为止我们看到三类主要的 Skills：

## 基础技能（Foundational skills）

These provide core capabilities everyone needs: working with documents, spreadsheets, presentations, etc. They encode best practices for document generation and manipulation. You can see what this looks like in practice by exploring the foundational skills in our public repository.

这类 Skills 提供人人都需要的核心能力：处理文档、电子表格、演示文稿等。它们把文档生成与操作的最佳实践编码其中。你可以浏览我们公开仓库中的基础技能，了解它在实际中的样子。

## 伙伴技能（Partner skills）

As skills standardize how agents interact with specialized capabilities, companies are building skills to make their services agent-accessible. K-Dense, Browserbase, Notion, and many others are creating skills that integrate their services directly, extending Claude's capabilities in specific domains while maintaining the simplicity of the skills format.

随着 Skills 把智能体与专业能力的交互标准化，各公司正在构建 Skills，让自己的服务可以被智能体访问。K-Dense、Browserbase、Notion 以及其他许多公司都在创建直接集成其服务的 Skills，在保持 Skills 格式简单性的同时，扩展 Claude 在特定领域的能力。

## 企业技能（Enterprise skills）

Organizations build proprietary skills encoding their internal processes and domain expertise. Skills help capture the specific workflows, compliance requirements, and institutional knowledge that make an agent useful for enterprise work.

各组织构建专有 Skills，把内部流程和领域专业知识编码其中。Skills 帮助沉淀那些让智能体在企业工作中真正有用的特定工作流、合规要求和机构知识。

# 我们看到的趋势（Trends we see）

As skills adoption grows, several patterns are emerging that point to where this paradigm may be heading. These trends shape how we think about skill design and the tooling we're building to support skill developers.

随着 Skills 的普及，若干模式正在浮现，指向这一范式可能的发展方向。这些趋势影响着我们对 Skill 设计的思考，以及我们为支持 Skill 开发者而构建的工具。

## 复杂度不断提升（Increasing complexity）

Early skills were simple documentation references. Now we're seeing sophisticated multi-step workflows that coordinate data retrieval, complex calculations, and formatted output across multiple tools.

早期的 Skills 只是简单的文档参考。现在我们看到的则是复杂的多步骤工作流，能跨多个工具协调数据检索、复杂计算和格式化输出。

- Simple: "Status report writer" (~100 lines) - Templates and formatting
- Intermediate: "Financial model builder" (~800 lines) - Data retrieval, Excel modeling with Python
- Complex: "RNA sequencing pipeline" (2,500+ lines) - Coordinates HISAT2, StringTie, DESeq2 analysis

- 简单："状态报告撰写器"（约 100 行）--模板与格式化
- 中等："财务模型构建器"（约 800 行）--数据检索、用 Python 做 Excel 建模
- 复杂："RNA 测序流水线"（2,500+ 行）--协调 HISAT2、StringTie、DESeq2 分析

## Skills 与 MCP（Skills and MCP）

Skills and MCP servers work together naturally. A competitive analysis skill might coordinate web search, internal databases via MCP, Slack message history, and Notion pages to synthesize a comprehensive report.

Skills 与 MCP 服务器天然协同。一个竞争分析 Skill 可以协调网络搜索、通过 MCP 访问的内部数据库、Slack 消息历史和 Notion 页面，综合出一份完整的报告。

## 非开发者的采纳（Non-developer adoption）

Skill creation is expanding beyond engineers to product managers, analysts, and domain experts across disciplines. They can create and test their first skill in under 30 minutes using the skill-creator tool, which guides them through the process interactively. We're working to make skill creation even more accessible, with improved tooling and templates that let anyone capture and share expertise.

Skill 的创建正在从工程师扩展到各学科的产品经理、分析师和领域专家。借助 skill-creator 工具（以交互方式引导他们完成整个过程），他们可以在 30 分钟内创建并测试自己的第一个 Skill。我们正在努力让创建 Skill 更加容易上手，提供改进的工具和模板，让任何人都能沉淀和分享专业知识。

# 完整架构（The complete architecture）

Putting it all together, the emerging agent architecture looks like a combination of:

把这一切拼起来，正在成形的智能体架构看起来是以下几部分的组合：

- Agent loop: The core reasoning system that decides what to do next
- Agent runtime: Execution environment (code, filesystem)
- MCP servers: Connections to external tools and data sources
- Skills library: Domain expertise and procedural knowledge

- 智能体循环（agent loop）：决定下一步做什么的核心推理系统
- 智能体运行时（agent runtime）：执行环境（代码、文件系统）
- MCP 服务器：连接外部工具和数据源
- Skills 库：领域专业知识和程序性知识

![示意图：智能体完整架构--循环、运行时、MCP 服务器与 Skills 库](images/skillsbuild-3.png)

Each layer has a clear purpose: the loop reasons, the runtime executes, MCP connects, and skills guide. This separation makes the system comprehensible and allows each piece to evolve independently.

每一层都有清晰的职责：循环负责推理，运行时负责执行，MCP 负责连接，Skills 负责指引。这种分离让系统易于理解，也让每个部分可以独立演进。

Consider what happens when you add a single skill to this architecture. The frontend design skill transforms Claude's frontend capabilities instantly. It provides specialized guidance on typography, color theory, and animation, activating only when building web interfaces. Progressive disclosure means it loads only when relevant. Adding new capabilities is straightforward.

想一想在这个架构上添加一个 Skill 会发生什么。前端设计 Skill 能立即改变 Claude 的前端能力。它提供排版、色彩理论和动效方面的专业指引，只在构建 Web 界面时激活。渐进式披露意味着它只在相关时才加载。添加新能力变得非常直接。

# 将 Skills 部署到新的垂直领域（Deploying skills to new verticals）

This emerging pattern of general agents equipped with MCP servers and skills is already helping us deploy Claude to new verticals.

这种"通用智能体 + MCP 服务器 + Skills"的新模式，已经在帮助我们把 Claude 部署到新的垂直行业。

## 金融服务（Financial Services）

Just after launching skills, we enhanced Claude for the financial services sector with skills that make Claude more useful for finance professionals:

就在发布 Skills 之后，我们用一批 Skills 增强了 Claude 在金融服务领域的表现，让 Claude 对金融从业者更有用：

- DCF model builder: Constructs discounted cash flow models with proper WACC calculations and sensitivity analysis
- Comparable company analysis: Generates comps tables with relevant multiples and benchmarking
- Earnings analysis: Processes quarterly results and creates investment update reports
- Initiation coverage: Builds comprehensive research reports with financial models
- Due diligence: Structures M&A analysis with standardized frameworks
- Pitch materials: Creates client presentations following industry standards

- DCF 模型构建器：构建贴现现金流（DCF）模型，包含规范的 WACC 计算和敏感性分析
- 可比公司分析：生成包含相关倍数和基准对比的可比公司（comps）表格
- 财报分析：处理季度业绩并生成投资更新报告
- 首次覆盖报告：构建包含财务模型的综合研究报告
- 尽职调查：用标准化框架组织并购（M&A）分析
- 路演材料：按照行业标准创建客户演示文稿

## 医疗健康与生命科学（Healthcare & Life Sciences）

We've also enhanced our healthcare and life sciences offerings with skills that make Claude more useful for researchers, clinicians, and healthcare developers:

我们还用一批 Skills 增强了医疗健康与生命科学方面的产品，让 Claude 对研究人员、临床工作者和医疗开发者更有用：

- Bioinformatics bundles: Skills for scVI-tools and Nextflow deployments, essential for managing genomic pipelines and single-cell RNA sequencing
- Clinical trial protocol generation: Accelerates protocol development for clinical research
- Scientific problem selection: Helps researchers identify and frame impactful research questions
- FHIR development: Helps developers write more accurate code for health data interoperability, connecting healthcare systems faster with fewer errors
- Prior authorization review: Cuts administrative burden and accelerates patient access to needed care by cross-referencing coverage requirements, clinical guidelines, and patient records

- 生物信息学套件：用于 scVI-tools 和 Nextflow 部署的 Skills，对管理基因组流水线和单细胞 RNA 测序必不可少
- 临床试验方案生成：加速临床研究方案的开发
- 科研选题：帮助研究人员识别并构建有影响力的研究问题
- FHIR 开发：帮助开发者编写更准确的健康数据互操作代码，更快、更少出错地打通医疗系统
- 预授权审核：通过交叉核对承保要求、临床指南和患者病历，削减行政负担，加快患者获得所需诊疗

# 将 Agent Skills 标准化（Standardizing Agent Skills）

To enable this vision, we're publishing Agent Skills as an open standard. Like MCP, we believe skills should be portable across tools and platforms. The same skill should work whether you're using Claude or other AI platforms. We've been collaborating with members of the ecosystem on the standard, and we're excited to see early adoption.

为了实现这一愿景，我们将 Agent Skills 作为一个开放标准发布。和 MCP 一样，我们相信 Skills 应当可跨工具、跨平台移植。无论你使用的是 Claude 还是其他 AI 平台，同一个 Skill 都应当能用。我们一直在与生态成员协作制定该标准，也很高兴看到早期的采纳。

When someone starts using an AI agent for the first time, it should already know what you and your team care about because skills capture and transfer that expertise. As this ecosystem grows, a skill built by someone else in the community can make your agent more useful, reliable, and capable - regardless of which AI platform they're using.

当一个人第一次使用 AI 智能体时，它应该已经了解你和你的团队关注什么，因为 Skills 会捕获并传递这些专业知识。随着生态的发展，社区里其他人构建的 Skill 可以让你的智能体更有用、更可靠、更强大--无论对方用的是哪个 AI 平台。

# 开始使用（Getting started）

We're converging on an architecture for general agents, and skills provide a paradigm for shipping and sharing new capabilities. The real value emerges from the collective knowledge base we build together: capturing expertise, transferring it across teams, and making every agent more capable than the last.

我们正在收敛到一种通用智能体架构，而 Skills 提供了发布和分享新能力的范式。真正的价值来自我们共同构建的知识库：沉淀专业知识，跨团队传递，让每一个智能体都比上一个更强大。

Resources:

资源：

- Don't Build Agents, Build Skills Instead (YouTube Video)
- Skills documentation
- GitHub repository
- Skills cookbook
- Using skills in Claude
- Skills API quickstart
- Skills best practices documentation

- 《不要构建智能体，转而构建 Skills》（Don't Build Agents, Build Skills Instead，YouTube 视频）
- Skills 文档
- GitHub 仓库
- Skills 食谱（cookbook）
- 在 Claude 中使用 Skills
- Skills API 快速上手
- Skills 最佳实践文档

## 致谢（Acknowledgments）

Barry Zhang, Mahesh Murag, Keith Lazuka, Ryan Whitehead

Barry Zhang、Mahesh Murag、Keith Lazuka、Ryan Whitehead
