---
type: paper
paper_id: arxiv-2403.07718
title: "WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?"
arxiv: https://arxiv.org/abs/2403.07718
year: 2024
updated: 2026-06-28
status: summarized
primary_category: web-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/web-agent
  - eval/agent-benchmark
  - env/business
  - env/web
  - year/2024
  - priority/p1
  - read/skim
---

# WorkArena：评测 Web Agent 完成企业知识工作任务的能力

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2403.07718
> 发表：2024 ｜ 作者：ServiceNow Research 等

---

## 一、一句话概括

**WorkArena** 基于 ServiceNow 企业软件平台构建 33 个知识工作任务，用于评测 Web Agent 在企业应用中执行真实办公流程的能力，并提出 BrowserGym 环境。

它把 Web Agent 评测从通用网页操作推进到企业软件和知识工作自动化。

---

## 二、核心动机

真实知识工作并不只是搜索网页，而是操作企业系统：

- 创建和更新工单。
- 查询记录。
- 修改状态。
- 跨页面完成流程。
- 遵守业务规则。

WorkArena 关注的正是“日常办公软件里的可执行任务”。

---

## 三、评测环境

WorkArena 包含：

- 33 个基于 ServiceNow 的任务。
- 远程托管 benchmark。
- BrowserGym 环境，用于设计和评估 Web Agent。
- 多模态观察和丰富动作空间。

它比普通网页任务更接近企业内 Agent 的落地场景。

---

## 四、关键发现

论文发现当前 Web Agent 在 WorkArena 上已有一定潜力，但距离完整自动化仍有明显差距。同时，闭源模型和开源模型之间存在显著性能差异。

这说明企业软件 Agent 的瓶颈不仅是网页导航，也包括流程理解、业务状态管理和可靠执行。

---

## 五、局限与启发

局限：

- 任务数量较少。
- 基于特定企业平台，泛化到其他 SaaS 仍需验证。
- 真实企业操作还涉及权限、审计和合规。

启发：

- 企业 Agent 评测要覆盖业务流程，而不是只测信息查找。
- BrowserGym 这类统一环境对 Web Agent 研究很关键。

---

## 参考 / 延伸阅读

- 论文：[WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks?](https://arxiv.org/abs/2403.07718)
- 相关：[[2307-WebArena A Realistic Web Environment for Building Autonomous Agents]]

