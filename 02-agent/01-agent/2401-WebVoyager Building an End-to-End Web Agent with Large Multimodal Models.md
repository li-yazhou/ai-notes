---
type: paper
paper_id: arxiv-2401.13919
title: "WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models"
arxiv: https://arxiv.org/abs/2401.13919
year: 2024
updated: 2026-06-28
status: summarized
primary_category: web-agent
priority: p1
read_type: skim
tags:
  - paper
  - paper/agent
  - agent/web-agent
  - agent/multimodal
  - env/web
  - year/2024
  - priority/p1
  - read/skim
---

# WebVoyager：基于多模态大模型的端到端 Web Agent

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2401.13919
> 项目：https://github.com/MinorJerry/WebVoyager
> 发表：2024 ｜ 作者：Hongliang He, Wenlin Yao, Kaixin Ma 等

---

## 一、一句话概括

**WebVoyager** 构建了一个由大多模态模型驱动的端到端 Web Agent，能在真实网站上根据用户指令进行浏览、观察和操作，并提出相应真实网站任务 benchmark。

它的重要性在于：从文本/DOM Web Agent 迈向截图视觉输入和真实网站操作。

---

## 二、核心动机

早期 Web Agent 常受两类限制：

- 只处理文本或 DOM，忽视网页视觉信息。
- 在简化模拟环境或静态网页快照中评测，离真实网站较远。

WebVoyager 试图让 Agent 直接在真实网站中工作，并使用视觉能力理解页面。

---

## 三、系统设计

WebVoyager 的基本循环是：

```text
用户任务
  ↓
观察网页截图/状态
  ↓
多模态模型推理下一步
  ↓
执行点击、输入、滚动等动作
  ↓
继续观察直到完成
```

论文还用 GPT-4V 的多模态理解能力设计自动评估协议，用于评估开放式 Web Agent 任务是否完成。

---

## 四、关键结果

WebVoyager 在论文构建的 15 个热门网站真实任务 benchmark 上达到 59.1% 任务成功率，显著超过 GPT-4 All Tools 和 text-only WebVoyager 设置。

自动评价指标与人类判断达到 85.3% 一致，说明多模态 judge 可用于辅助 Web Agent 评测。

---

## 五、与 WebArena / VisualWebArena 的关系

| 维度 | WebVoyager | WebArena | VisualWebArena |
|---|---|---|---|
| 环境 | 真实网站 | 自托管真实风格网站 | 视觉强化的自托管网站 |
| 输入 | 多模态截图为主 | 文本/DOM 为主 | 图文多模态 |
| 重点 | 端到端真实网页操作 | 可复现功能正确性 | 视觉 grounding |

---

## 六、局限与启发

局限：

- 真实网站随时间变化，复现性较难。
- 自动评价依赖强多模态模型，可能有 judge 偏差。
- 真实网站操作涉及登录、隐私、支付等安全边界。

启发：

- 浏览器 Agent 需要视觉理解，不能只依赖 HTML。
- Web Agent 评测要同时关注真实环境能力和可复现性。

---

## 参考 / 延伸阅读

- 论文：[WebVoyager: Building an End-to-End Web Agent with Large Multimodal Models](https://arxiv.org/abs/2401.13919)
- 项目：[WebVoyager](https://github.com/MinorJerry/WebVoyager)
- 相关：[[2401-VisualWebArena Evaluating Multimodal Agents on Realistic Visual Web Tasks]]

