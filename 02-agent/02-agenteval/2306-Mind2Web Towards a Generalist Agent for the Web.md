---
type: paper
paper_id: arxiv-2306.06070
title: "Mind2Web: Towards a Generalist Agent for the Web"
arxiv: https://arxiv.org/abs/2306.06070
year: 2023
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
  - env/web
  - year/2023
  - priority/p1
  - read/skim
---

# Mind2Web：面向通用 Web Agent 的真实网页任务数据集

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2306.06070
> 项目：https://osu-nlp-group.github.io/Mind2Web
> 发表：2023 ｜ 作者：Xiang Deng, Yu Gu, Boyuan Zheng 等

---

## 一、一句话概括

**Mind2Web** 收集 137 个真实网站、31 个领域、2,000+ 个开放网页任务及人工动作序列，用于训练和评估能泛化到任意网站的 Web Agent。

它的重要性在于：Web Agent 从模拟网页走向真实网站多样性。

---

## 二、核心动机

早期 Web Agent 数据集常见问题：

- 网站数量少。
- 任务模式固定。
- 多为模拟环境。
- 难以评估跨网站泛化。

Mind2Web 提供真实网站上的用户任务和动作轨迹，强调 generalist web agent。

---

## 三、数据特点

Mind2Web 包含：

- 2,000+ open-ended tasks。
- 137 个真实网站。
- 31 个领域。
- 众包标注的 action sequences。
- 多种用户交互模式。

由于真实网页 HTML 很长，论文也探索先用小模型过滤候选元素，再让 LLM 决策。

---

## 四、与 WebArena 的关系

| 维度 | Mind2Web | WebArena |
|---|---|---|
| 网站 | 真实线上网站 | 自托管可复现网站 |
| 数据 | 人工动作轨迹 | 功能正确性任务 |
| 重点 | 泛化和动作预测 | 可复现端到端执行 |

两者互补：Mind2Web 更广，WebArena 更可控。

---

## 五、局限与启发

局限：

- 真实网页会变化，复现和长期维护难。
- 动作轨迹不代表唯一正确路径。
- HTML 过长导致上下文和候选筛选成为瓶颈。

启发：

- Web Agent 需要候选元素过滤，不能把整页无脑塞给 LLM。
- 泛化评测要按网站/领域划分 train-test，避免记忆具体页面。

---

## 参考 / 延伸阅读

- 论文：[Mind2Web: Towards a Generalist Agent for the Web](https://arxiv.org/abs/2306.06070)
- 项目：[Mind2Web](https://osu-nlp-group.github.io/Mind2Web)
- 相关：[[2307-WebArena A Realistic Web Environment for Building Autonomous Agents]]

