---
type: paper
paper_id: arxiv-2307.13854
title: "WebArena: A Realistic Web Environment for Building Autonomous Agents"
arxiv: https://arxiv.org/abs/2307.13854
year: 2023
updated: 2026-06-28
status: summarized
primary_category: web-agent
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/web-agent
  - eval/agent-benchmark
  - env/web
  - year/2023
  - priority/p0
  - read/deep
---

# WebArena：面向真实网站任务的自主 Agent 评测环境

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2307.13854
> 项目：https://webarena.dev/
> 发表：2023 ｜ 作者：Shuyan Zhou, Frank F. Xu, Hao Zhu 等

---

## 一、一句话概括

**WebArena** 构建了一组可复现、功能完整的真实风格网站，并用 812 个长程网页任务评估语言 Agent 是否能通过网页交互完成现实互联网任务。

它的重要性在于：把 Web Agent 从简化网页或脚本环境推进到更接近真实互联网的功能性评测。

---

## 二、核心动机

很多早期 Web Agent 任务过于简化：

- 页面结构固定。
- 操作路径短。
- 任务目标明确且单一。
- 评测偏动作模仿，而不是真正完成任务。

WebArena 认为真实网页任务更像这样：

```text
理解用户目标
  ↓
跨页面导航
  ↓
搜索 / 筛选 / 填表 / 比较
  ↓
使用外部知识或工具
  ↓
完成可验证状态变化
```

---

## 三、环境设计

WebArena 包含四类功能完整的网站：

| 领域 | 例子 | 能力要求 |
|---|---|---|
| E-commerce | 商品浏览、搜索、购物 | 筛选、比较、表单操作 |
| Social Forum | 类 Reddit 社区 | 阅读帖子、发帖、互动 |
| Collaborative Software Development | 类 GitLab | issue、repo、项目管理 |
| Content Management | 后台管理 / CMS | 内容编辑、权限、配置 |

环境还提供地图、计算器、scratchpad、Wikipedia / 用户手册等外部资源，以模拟人类完成网页任务时的辅助工具。

---

## 四、任务与评测

WebArena 提供：

- 812 个长程任务。
- 241 个任务模板。
- 任务覆盖信息查找、配置修改、内容创建、购物决策、软件协作等。

评测关注的是 **functional correctness**，也就是任务最终是否真的完成，而不是动作轨迹是否和人工示范一致。

这点很关键：Agent 可以走不同路径，只要最终状态正确就算成功。

---

## 五、关键结果

论文中的结果显示，真实网页任务对当前 Agent 非常困难：

| 系统 | 端到端成功率 |
|---|---|
| 人类 | 78.24% |
| 最强 GPT-4 Agent | 14.41% |
| GPT-4 + CoT | 约 11.70% |
| GPT-3.5 | 约 5.05% |

失败模式包括：

- 被第一个相关信息吸引，过早下结论。
- 忽略细粒度页面状态。
- 忘记前一步操作结果。
- 反复执行无效动作直到步数耗尽。
- 把可完成任务误判为不可能。

---

## 六、为什么重要

WebArena 让 Web Agent 评测从“浏览器玩具任务”进入更严肃的阶段：

```text
真实网站结构
+ 长程任务
+ 可复现环境
+ 功能正确性评估
```

它直接影响了后续 WebVoyager、VisualWebArena、BrowserGym 等 Web Agent 评测方向。

---

## 七、局限

1. **仍不等于开放互联网**：网站虽真实风格，但仍是受控部署环境。
2. **视觉能力不是最核心设置**：原始 WebArena 更偏 DOM / 文本交互，后续 VisualWebArena 才进一步强调视觉网页理解。
3. **评测维护成本高**：网站、数据库、状态重置和任务检查都需要工程维护。
4. **成功率低带来分析困难**：当模型普遍失败时，很难细分能力边界。
5. **安全与权限问题未完全覆盖**：真实 Web Agent 部署还涉及登录、支付、隐私、越权等风险。

---

## 八、对 Agent 的启发

- Web Agent 必须有状态记忆，不能只看当前页面。
- 任务完成应以最终状态验证，而不是模仿固定轨迹。
- 网页任务需要检索、规划、执行、纠错一体化。
- 对浏览器 Agent 来说，错误恢复能力和步数预算非常关键。

---

## 参考 / 延伸阅读

- 论文：[WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)
- 项目：[WebArena](https://webarena.dev/)
- 相关：[[2308-AgentBench Evaluating LLMs as Agents]]

