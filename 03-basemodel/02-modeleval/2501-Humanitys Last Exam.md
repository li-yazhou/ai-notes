---
type: paper
paper_id: arxiv-2501.14249
title: "Humanity's Last Exam"
arxiv: https://arxiv.org/abs/2501.14249
year: 2025
updated: 2026-06-28
status: summarized
primary_category: model-benchmark
priority: p0
read_type: deep
tags:
  - paper
  - paper/eval
  - eval/model-benchmark
  - eval/knowledge
  - eval/frontier
  - year/2025
  - priority/p0
  - read/deep
---

# Humanity's Last Exam：面向前沿知识的高难闭卷式评测

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2501.14249
> 项目：https://lastexam.ai/
> 发表：2025 ｜ 作者：Long Phan, Alice Gatti, Ziwen Han 等

---

## 一、一句话概括

**Humanity's Last Exam（HLE）** 是一个面向前沿人类知识的多模态高难 benchmark，包含约 2,500 道跨学科题目，要求答案明确、可验证、难以通过简单互联网检索获得。

它的重要性在于：当 MMLU 等传统知识评测被前沿模型刷到 90% 以上时，HLE 试图重新拉开能力差距。

---

## 二、核心动机

LLM 评测面临一个持续问题：旧 benchmark 会被快速饱和。

当模型在 MMLU 等流行 benchmark 上超过 90% 后，这些数据集很难继续区分前沿模型能力。HLE 的目标是构建一个更接近人类专家知识边界的闭端评测。

---

## 三、数据集设计

HLE 的题目特点：

- 覆盖数学、人文、自然科学等多个学科。
- 由全球领域专家贡献和审核。
- 包含选择题和短答案题。
- 支持自动评分。
- 部分题目包含图像，是多模态 benchmark。
- 每题有明确、无歧义、容易验证的正确答案。
- 题目不能被简单搜索或数据库检索快速解决。

它不是开放式写作评测，而是 closed-ended academic benchmark。

---

## 四、质量控制

HLE 对题目质量控制非常严格：

1. 题目需要先让前沿模型难以答对。
2. 经过多阶段审核和专家反馈。
3. 要求答案明确、可验证、非主观。
4. 保留私有测试集，以减少公开题目过拟合和刷榜。

这种设计是为了解决 benchmark 污染和难度不足的问题。

---

## 五、关键结果

论文报告中，前沿模型在 HLE 上表现仍然很低：

- 多个 state-of-the-art LLM 准确率低于 10%。
- 模型校准也很差，经常以高置信度给出错误答案。
- RMS calibration error 在实验中很高，显示模型不知道自己不知道。

这说明：即便模型在很多标准考试型 benchmark 上高分，距离专家级闭端学术能力仍有明显差距。

---

## 六、与 Agent 评测的关系

HLE 本身不是 Agent benchmark，因为它主要评估闭端学术问题能力，而不是交互行动能力。

但它对 Agent 发展仍然重要：

- 通用 Agent 需要强知识和推理底座。
- Deep Research 类 Agent 需要处理高难、不可简单搜索的问题。
- 校准能力会影响 Agent 是否敢于行动、何时请求帮助、何时继续验证。
- 私有集和高难题设计对评测抗污染有借鉴意义。

---

## 七、局限

1. **不是交互式任务**：不评估工具使用、长期规划、环境行动。
2. **闭端题目有边界**：真实科研和工作常是开放式、过程型任务。
3. **专家题可能偏知识密度**：不一定代表一般用户任务。
4. **自动评分仍有挑战**：短答案题需要处理等价表达。
5. **难度会被模型进步追赶**：高难 benchmark 也需要持续更新。

---

## 八、为什么重要

HLE 代表了一类新的评测压力：

```text
高难度
+ 专家构造
+ 多学科
+ 多模态
+ 抗简单检索
+ 私有测试集
```

它提醒我们：评测不仅要覆盖真实任务，也要维持足够难度，否则很快无法衡量前沿模型。

---

## 九、对 Agent 的启发

- Agent 需要知道何时“不确定”，不能用高置信错误驱动行动。
- Deep Research 型系统应区分可搜索问题和需要专家推理的问题。
- Benchmark 应考虑私有集与动态更新，降低训练污染。
- 通用智能评测需要同时覆盖知识边界和行动能力边界。

---

## 参考 / 延伸阅读

- 论文：[Humanity's Last Exam](https://arxiv.org/abs/2501.14249)
- 项目：[lastexam.ai](https://lastexam.ai/)
- 相关：[[2311-GAIA a benchmark for General AI Assistants]]
- 相关：[[2503-Survey on Evaluation of LLM-based Agents]]

