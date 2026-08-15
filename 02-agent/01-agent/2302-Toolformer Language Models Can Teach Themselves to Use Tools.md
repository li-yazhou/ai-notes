---
type: paper
paper_id: arxiv-2302.04761
title: "Toolformer: Language Models Can Teach Themselves to Use Tools"
arxiv: https://arxiv.org/abs/2302.04761
year: 2023
updated: 2026-06-28
status: summarized
primary_category: tool-use
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - agent/tool-use
  - method/tool-calling
  - method/self-supervised
  - year/2023
  - priority/p0
  - read/deep
---

# Toolformer：语言模型如何自监督学会调用工具

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2302.04761
> 发表：2023 ｜ 作者：Timo Schick 等（Meta AI）

---

## 一、一句话概括

**Toolformer** 提出一种自监督方法，让语言模型学会在生成文本时自主决定：**何时调用工具、调用哪个工具、传什么参数、如何利用返回结果继续生成**。

它的重要性在于：工具调用不再只是人工写 prompt 或规则路由，而可以被模型通过少量 API 示例和自监督过滤机制“学出来”。

---

## 二、研究动机

大语言模型有几个天然短板：

- 精确计算不稳。
- 实时信息缺失。
- 事实检索容易幻觉。
- 多语言转换、日期推理等任务依赖外部系统更可靠。

MRKL 强调“系统应当调用专家模块”，ReAct 强调“边想边行动”。Toolformer 则进一步问：**模型能不能自己学会在文本中插入 API 调用？**

---

## 三、核心方法

Toolformer 的训练流程可以概括为四步：

```text
原始文本语料
  ↓
用少量人工示例提示模型生成候选 API 调用
  ↓
执行 API，拿到返回结果
  ↓
只保留能降低后续 token loss 的调用
  ↓
用带 API 调用的新语料微调模型
```

关键不是“有没有工具”，而是过滤标准：如果某个 API 调用及其返回结果能显著降低模型预测后续文本的损失，就认为这个调用对语言建模有帮助，保留下来。

论文使用统一的线性化格式：

```text
<API> ToolName(input) → result </API>
```

这样工具调用就能被当作普通 token 序列学习。

---

## 四、接入的工具

论文测试了五类工具：

| 工具 | 解决的问题 |
|---|---|
| Calculator | 精确算术 |
| Question Answering API | 事实问答 |
| Wikipedia Search | 外部知识检索 |
| Machine Translation | 机器翻译 |
| Calendar | 日期和时间相关问题 |

这些工具都满足一个条件：输入和输出都可以表示为文本，因此容易嵌入语言模型生成过程。

---

## 五、实验与结果

Toolformer 使用 GPT-J 作为基础模型，在 CCNet 子集上生成带 API 调用的训练数据。评测覆盖：

- LAMA / T-REx：事实补全。
- 数学任务：计算器调用明显提升。
- WebQuestions、Natural Questions、TriviaQA：QA / Wikipedia 工具提升检索问答。
- MLQA：机器翻译工具用于跨语言问答。
- TEMP LAMA / DATESET：日期相关任务。

典型结果：

- LAMA 子集上，Toolformer 明显强于禁用工具的版本。
- 数学任务上，调用计算器后性能大幅提升。
- QA 任务中，模型大量使用 Wikipedia Search，并优于同规模基线。
- 微调后即使禁用工具，也有一定提升，说明 API 结果也提供了训练信号。

---

## 六、局限

1. **单步工具调用为主**：不能自然处理“先搜索，再计算，再查询”的多工具链。
2. **交互性弱**：不像 ReAct 那样根据环境反馈连续修正。
3. **调用敏感**：是否调用 API 对阈值、prompt 和模型规模敏感。
4. **工具接口质量决定上限**：如果 API 返回差，模型也会被误导。
5. **安全未充分展开**：真实产品中的 API 权限、注入攻击、成本控制不是本文重点。

---

## 七、为什么重要

Toolformer 把工具调用从“手写规则/人工 prompt”推进到“模型可学习的行为”。它启发了后来的：

- function calling 微调数据构造；
- tool-use benchmark；
- API 调用轨迹学习；
- Agent 中的工具选择器和参数生成器。

如果说 MRKL 是系统架构，ReAct 是推理-行动循环，那么 Toolformer 关注的是：**工具调用能力本身如何训练出来。**

---

## 八、对 Agent 的启发

- 工具调用轨迹可以自动挖掘，不一定全靠人工标注。
- 判断调用是否有价值，可以用“是否改善任务损失/验证结果”作为过滤信号。
- Agent 训练数据应记录完整的 `tool_name(input) -> output`，而不是只存最终答案。
- 长链工具调用仍需要 ReAct / planner / verifier 类机制补足。

---

## 参考 / 延伸阅读

- 论文：[Toolformer: Language Models Can Teach Themselves to Use Tools](https://arxiv.org/abs/2302.04761)
- 相关：[[2205-MRKL Systems]]
- 相关：[[2210-ReAct Synergizing Reasoning and Acting in Language Models]]
