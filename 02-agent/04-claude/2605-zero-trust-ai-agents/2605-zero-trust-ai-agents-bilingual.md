# 面向 AI 智能体的零信任（中英对照）

> **原文标题：** Zero Trust for AI agents
> **作者：** Anthropic（原文未署名）
> **原文链接：** https://claude.com/blog/zero-trust-for-ai-agents
> **发布日期：** 2026-05-27
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

A Zero Trust framework for deploying autonomous AI agents in the enterprise, covering current threats, a tiered architecture, an eight-phase implementation workflow, and agentic SOAR.

一个用于在企业中部署自主 AI 智能体的零信任（Zero Trust）框架，涵盖当前威胁、分层架构、八阶段实施工作流以及智能体化 SOAR。

We share a security framework for deploying autonomous AI agents in the enterprise, covering the new threat landscape, a tiered Zero Trust architecture, and defensive operations built for AI-accelerated attacks.

我们分享了一个用于在企业中部署自主 AI 智能体的安全框架，涵盖新的威胁态势、分层的零信任架构，以及为 AI 加速攻击打造的防御性运营。

Frontier AI models are compressing the timeline between vulnerability and exploit from months to hours. Defenders who adopt these tools find and fix bugs faster; attackers who adopt them, or who simply wait for defenders' patches and reverse-engineer them into exploits, move faster too. This is not a future concern: models can already find serious vulnerabilities that traditional tooling and human reviewers have missed for years.

前沿 AI 模型正在把从漏洞出现到漏洞利用（exploit）问世的时间线从数月压缩到数小时。采用这些工具的防御者能更快发现并修复 bug；采用这些工具的攻击者、或者干脆等待防御者的补丁再将其逆向为漏洞利用的攻击者，行动也更快了。这不是对未来的担忧：模型已经能够发现传统工具和人类评审者多年遗漏的严重漏洞。

This acceleration matters twice for any organization deploying agents. The infrastructure your agents run on is exposed to AI-accelerated offense like the rest of your estate, and the agents themselves introduce autonomy to interpret goals, select tools, and execute multi-step operations. Traditional access controls won't prevent agents from misusing legitimate permissions, and monitoring needs to account for attacks designed to succeed through persistence rather than exploitation.

对于任何部署智能体的组织，这种加速在两个层面都关系重大。你的智能体运行所在的基础设施像你其余的资产一样暴露在 AI 加速的攻击之下，而智能体本身也带来了自主性--解读目标、选择工具、执行多步操作。传统的访问控制无法阻止智能体滥用合法权限，而监控也需要顾及那些靠持久潜伏而非漏洞利用来得手的攻击。

Zero Trust—trust nothing, verify everything, and assume breach has already occurred—gives security leaders a proven foundation to address this. But the principles need new shape for agentic systems: identities that are cryptographically rooted, permissions scoped per task, memory protected against poisoning, and defensive operations that run at the speed of autonomous attackers.

零信任（Zero Trust）--不信任任何东西、验证一切、并假设入侵已经发生--为安全负责人应对这一局面提供了一个经过验证的基石。但这些原则需要为智能体系统赋予新的形态：以密码学为根的身份、按任务限定范围的权限、防御投毒（poisoning）的记忆，以及能以自主攻击者速度运转的防御性运营。

To help security and risk leaders build for this shift, we put together a practical framework for deploying autonomous AI agents in the enterprise.

为帮助安全与风险负责人为这一转变做好准备，我们编制了一套用于在企业中部署自主 AI 智能体的实用框架。

In this guide, we share:

在本指南中，我们分享：

- The security considerations unique to agentic systems, including tool access, autonomous decision-making, context persistence, and multi-agent coordination
- The current threat landscape for agents, including prompt injection, tool poisoning, identity and privilege abuse, memory poisoning, and supply chain attacks
- A three-tier Zero Trust framework (Foundation, Advanced, and Optimized) mapped to organizational maturity and risk tolerance
- An eight-phase implementation workflow covering identity, access scoping, sandboxing, input and output controls, and memory safeguards
- How to run agentic security operations (Agentic SOAR) fast enough to contend with AI-accelerated attackers
- Compliance alignment for regulated industries including healthcare, finance, and government

- 智能体系统特有的安全考量，包括工具访问、自主决策、上下文持久化以及多智能体协调
- 智能体当前面临的威胁态势，包括提示词注入（prompt injection）、工具投毒（tool poisoning）、身份与权限滥用、记忆投毒（memory poisoning）和供应链攻击（supply chain attack）
- 与组织成熟度和风险容忍度相映射的三层零信任框架（基础级 Foundation、进阶级 Advanced、优化级 Optimized）
- 覆盖身份、访问范围界定、沙箱（sandbox）化、输入与输出控制以及记忆防护的八阶段实施工作流
- 如何让智能体化安全运营（Agentic SOAR，安全编排、自动化与响应）快到足以与 AI 加速的攻击者抗衡
- 面向医疗、金融和政府等受监管行业的合规对齐

The organizations best positioned for this shift will be the ones whose fundamentals are strong enough that AI-assisted scanning finds fewer bugs in the first place, and whose agent deployments are architected for breach from day one.

在这场转变中占据最佳位置的组织，将是那些基本功足够扎实、以至于 AI 辅助扫描一开始就发现不了多少 bug 的组织，以及那些从第一天起就按"已被入侵"来设计智能体部署的组织。

Check it out, here.

在此查阅。

Get started with Claude Security today.

立即开始使用 Claude Security。
