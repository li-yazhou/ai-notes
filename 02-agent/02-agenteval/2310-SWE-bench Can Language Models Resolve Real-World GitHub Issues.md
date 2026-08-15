---
type: paper
paper_id: arxiv-2310.06770
title: "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?"
arxiv: https://arxiv.org/abs/2310.06770
year: 2023
updated: 2026-06-28
status: summarized
primary_category: software-agent
priority: p0
read_type: deep
tags:
  - paper
  - paper/agent
  - paper/eval
  - agent/software-agent
  - eval/agent-benchmark
  - env/code
  - year/2023
  - priority/p0
  - read/deep
---

# SWE-bench：用真实 GitHub Issue 评测软件工程 Agent

> 更新时间：2026-06-28
> 论文地址：https://arxiv.org/abs/2310.06770
> 项目：https://www.swebench.com/
> 发表：2023 ｜ 作者：Carlos E. Jimenez, John Yang, Alexander Wettig 等

---

## 一、一句话概括

**SWE-bench** 从真实 GitHub issue 和对应 PR 中构造 2,294 个软件工程问题，要求模型在真实代码库中修改代码，并通过测试判断是否解决问题。

它的重要性在于：代码评测从“写一个函数”升级为“在真实仓库里修真实 bug / feature”。

---

## 二、为什么 HumanEval 不够

HumanEval / MBPP 这类代码生成任务通常是：

```text
给定函数签名和描述 → 写一个函数 → 跑隐藏测试
```

真实软件工程更复杂：

- 需要理解已有代码架构。
- 需要跨文件修改。
- 需要处理依赖和运行环境。
- 需要读 issue 描述，定位相关代码。
- 需要保证修复不破坏旧行为。

SWE-bench 试图评估模型是否能完成接近真实开发者的修复流程。

---

## 三、数据构造

SWE-bench 从 12 个流行 Python 仓库中抽取：

- GitHub issue。
- 对应解决该 issue 的 pull request。
- PR 中新增或修改的测试。
- 代码仓库在修复前的状态。

评测时给模型：

```text
仓库代码 + issue 描述
```

模型需要输出 patch。系统将 patch 应用到仓库，并运行测试判断是否解决问题。

---

## 四、任务难点

SWE-bench 难在它不是孤立编程题，而是软件维护任务：

- 需要从长上下文中定位相关函数 / 类 / 文件。
- 需要理解项目特定约定。
- 需要同时修改实现和边界条件。
- 需要与执行环境交互，观察测试失败。
- 需要避免过拟合单个测试。

这使它天然适合评估 Coding Agent、Repo Agent 和自动程序修复系统。

---

## 五、关键结果

论文早期评测显示，前沿模型在 SWE-bench 上成功率很低：

- Claude 2 在一种设置下解决约 1.96% 的 issues。
- 使用更强检索 / oracle 信息时，Claude 2 和 GPT-4 也只能解决少量问题。
- 作者还训练了 SWE-Llama，但只能解决相对简单的问题。

这些结果说明：会写函数的模型，距离能自主维护真实软件项目还有很大差距。

---

## 六、为什么重要

SWE-bench 后来成为软件工程 Agent 最重要的评测之一，因为它满足几个关键条件：

| 特点 | 意义 |
|---|---|
| 真实 GitHub issue | 任务来源真实，不是人工玩具题 |
| 真实仓库上下文 | 考察代码库理解，而非单函数生成 |
| 测试驱动验证 | 结果可自动评估 |
| 可持续扩展 | GitHub issue / PR 是持续数据源 |

后续 SWE-bench Verified、SWE-bench Multimodal、SWE-agent、OpenHands、Devin 类系统都围绕它展开。

---

## 七、局限

1. **测试通过不等于完全正确**：模型可能只满足测试，未必真正解决所有场景。
2. **环境复现成本高**：依赖安装、版本、系统环境都会影响评测。
3. **Issue 描述可能信息不足**：人类开发者常依赖隐性项目知识。
4. **检索是瓶颈**：模型失败常来自找不到相关代码，而不是不会改代码。
5. **容易被 benchmark 过拟合**：公开 issue 与补丁可能进入训练数据。

---

## 八、对 Agent 的启发

- Coding Agent 需要 repo-level 检索、编辑、执行、测试、回滚能力。
- 自动修复不能只依赖模型生成，必须接入真实执行反馈。
- 评测软件 Agent 时，要区分“定位能力”和“修改能力”。
- 好的 Coding Agent 应显式管理 patch、测试结果和失败诊断。

---

## 参考 / 延伸阅读

- 论文：[SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://arxiv.org/abs/2310.06770)
- 项目：[SWE-bench](https://www.swebench.com/)
- 相关：[[2308-AgentBench Evaluating LLMs as Agents]]

