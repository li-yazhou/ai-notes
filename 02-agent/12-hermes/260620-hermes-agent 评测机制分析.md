# Hermes-Agent 评测机制分析

> 分析对象：[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent)
> 分析日期：2026-06-20
> 本地路径：`/Users/liyazhou/Repo/repo_ai/hermes-agent`

## 核心结论

**Hermes-Agent 仓库本身不包含传统意义上的"模型质量评测"框架**（没有 SWE-bench 评分器、没有 LLM-as-judge、没有 pass rate 计算、没有 ground-truth 比对）。

这在社区里也是个公开的痛点——GitHub issue [#23137](https://github.com/NousResearch/hermes-agent/issues/23137) 直接追问作者"为什么没有 SWE-bench 分数"，至今 open、无人回复。

仓库里所谓的"评测"实际分四种性质不同的东西：

1. **轨迹/数据生成管线**（最接近"评测"的部分，但目的是产出 SFT 训练数据）
2. **性能/延迟基准**（内部内核，非 agent 能力）
3. **实时功能测试**（A/B 特性验证）
4. **第三方评测工具的 Skill 封装**（教 agent 怎么评测别人）

---

## 一、轨迹/数据生成管线（最接近"评测"的部分）

这是仓库里最成体系的一套，但它的**目的是产出 SFT 训练数据，而不是给 Hermes 打分**。

| 文件 | 行数 | 作用 |
|---|---|---|
| `batch_runner.py` | ~1321 | 并行批处理 JSONL prompt → 完整 agent session → ShareGPT 格式轨迹 + 工具使用统计 |
| `mini_swe_runner.py` | ~731 | 跑 SWE 风格任务的轻量 runner，输出 Hermes 轨迹格式 |
| `trajectory_compressor.py` | ~1579 | 把超长轨迹压缩到目标 token 预算（保头尾、LLM 摘要中间） |
| `scripts/sample_and_compress.py` | ~409 | 从 HuggingFace 下数据集采样+压缩 |
| `toolset_distributions.py` | ~364 | 定义工具集分布（如 `browser_tasks`）用于采样 |
| `datagen-config-examples/` | — | 示例配置 + 样例 prompt |

### 关键设计点（值得借鉴的部分）

**1. 沙箱化执行环境**——`mini_swe_runner.py` 通过 `create_environment()` 支持三种后端：

```
local → docker → modal（云）
```

每个 prompt 独立隔离，文件系统在 task 内持久。这是做任何严肃 agent 评测的基础设施。

**2. 完成判定是"自我报告"而非客观验证**——`mini_swe_runner.py` 让模型自己 `echo` 一个哨兵字符串 `MINI_SWE_AGENT_FINAL_OUTPUT` 来宣告完成。**没有跑测试套件、没有 diff 比对**。这是它和真正的 SWE-bench 评测的本质区别。

**3. 批处理输出格式**（`batch-processing.md` 文档）：

```
data/<run_name>/
├── trajectories.jsonl   # 合并的最终输出
├── batch_N.jsonl        # 分批结果
├── checkpoint.json      # 断点续跑
└── statistics.json      # 工具使用统计
```

每条轨迹记录 `conversations`（ShareGPT 格式）+ `tool_stats`（每个工具的调用次数、成功/失败数）+ `completed` 标志。

**4. 自动质量过滤**——丢弃零推理的样本、丢弃幻觉工具名的样本。这是为训练数据质量服务的，不是评测指标。

**5. 内容寻址的断点续跑**——resume 时按 prompt 文本内容匹配已完成项，而非按索引，即使数据集顺序变了也能恢复。

### 真实用途的证据

`scripts/sample_and_compress.py:30-36` 写死了要采样的 HuggingFace 数据集：

```
NousResearch/swe-terminus-agent-glm-kimi-minimax
NousResearch/hermes-agent-megascience-sft1
NousResearch/Hermes-Agent-Thinking-GLM-4.7-SFT2
NousResearch/Hermes-Agent-Thinking-GLM-4.7-SFT1
NousResearch/terminal-tasks-glm-hermes-agent
```

`README.md:29` 明说："Batch trajectory generation, trajectory compression for **training the next generation of tool-calling models**."

所以这条管线是**数据工厂**，评测只是 `batch-processing.md` 里顺带提到的"也可以这么用"的一个用法（见文档第 207-218 行的 "Model Evaluation" 小节，但它也只是跑一遍看模型怎么用工具，没有打分）。

---

## 二、性能/延迟基准（内部内核，非 agent 能力）

这些测的是 Hermes 自己内部组件快不快，不是 agent 聪不聪明。

- `tests/stress/test_benchmarks.py`（221 行）——Kanban 内核在 100/1k/10k 任务规模下的 `dispatch_once`、`recompute_ready` 等延迟，输出 JSON 做回归对比。文档明说"不是 pass/fail 测试"。
- `scripts/benchmark_browser_eval.py`（138 行）——A/B 对比两条浏览器 eval 代码路径的延迟（跑 `1+1` N 次计时）。
- `apps/desktop/scripts/eval.mjs`（21 行）——调用 Chrome DevTools `Runtime.evaluate` 的调试小工具。

---

## 三、实时功能测试（A/B 特性验证）

这是仓库里**唯一带有"期望结果断言"的东西**，但只针对单个特性，不是整体能力评测。

- `scripts/tool_search_livetest.py`（~600 行）——为 Tool Search 特性建的 live harness：起真实 `AIAgent`、注册约 20 个假 MCP 工具、跑 5 个场景（`obvious_single`、`vague_paraphrased`、`multi_tool_chain` 等），每个场景分别在 tool_search 开/关下跑，记录完整 transcript + 工具调用序列，含 `expected_underlying_tools` 断言。
- `scripts/analyze_livetest.py`——读 `out/_summary.json` 生成开/关对比报告。

---

## 四、第三方评测工具的 Skill 封装（教 agent 怎么评测别人）

`skills/mlops/evaluation/` 下的 lm-evaluation-harness、weights-and-biases 等 skill，是**让 Hermes 去用 EleutherAI 的评测工具**，不是用来评测 Hermes 自己的。

---

## 五、CI 工作流（`.github/workflows/`，19 个）

**没有任何一个跑 agent 质量评测**。`tests.yml`、`docker-publish.yml` 甚至显式把 `OPENROUTER_API_KEY=""` / `OPENAI_API_KEY=""` 置空，确保不触发真实 API 调用。其余全是 lint / typecheck / 安全审计 / 发布。

---

## 总结：Hermes 的"评测哲学"

把上面的发现拼起来，Hermes-Agent 对评测的态度可以概括为三点：

**1. 重数据生成，轻质量评测。** 仓库投入大量工程做轨迹生成（沙箱、并行、断点续跑、压缩、质量过滤），但没有一套给 Hermes 自己打分的 harness。评测被外移到了"下游"——生成的数据喂给 SFT，SFT 后的模型再由外部 benchmark 评测。

**2. 重功能回归，轻能力评分。** 唯一带断言的 live test（tool_search_livetest）是**特性级 A/B 回归**，验证"加了 tool search 后模型还能选对工具"，而非"这个模型整体有多强"。

**3. 完成判定依赖 agent 自报告。** `mini_swe_runner.py` 靠模型 echo 哨兵字符串判定完成，不跑测试套件。这意味着即便有人拿它跑 SWE-bench 题目，也只能得到"轨迹"，拿不到"通过率"——还需要自己接一套 SWE-bench 的 grading harness（FAIL_TO_PASS / PASS_TO_PASS 测试验证）才行，而这恰恰是仓库缺失的部分。

### 可借鉴/可复用的基础设施

如果要做"给 Hermes 接一套真正的能力评测"，缺口很明确：需要一个 `create_environment()` 之后追加 test-suite 执行 + FAIL_TO_PASS 比对 + pass@k 统计的 grading 层。**现有的沙箱和批处理基础设施可以复用，缺的只是"判定"这一环。**

可复用的部分：

| 组件 | 文件 | 复用价值 |
|---|---|---|
| 沙箱执行环境（local/docker/modal） | `tools/environments/` | 评测容器复用 |
| 并行批处理 + 断点续跑 | `batch_runner.py` | 批量跑题 |
| 轨迹格式（ShareGPT） | `_convert_to_hermes_format()` | 标准化输出 |
| 工具使用统计 | `statistics.json` | 附加分析维度 |
| 质量过滤 | `batch_runner.py` | 清洗评测样本 |

需自建的部分：

- **Grading 层**：跑题目的测试套件，比对 FAIL_TO_PASS / PASS_TO_PASS
- **评分聚合**：pass@1 / pass@k / 分领域通过率
- **LLM-as-judge**（可选）：对开放性任务做主观评分

---

## 参考链接

- [hermes-agent 仓库](https://github.com/NousResearch/hermes-agent)
- [issue #23137：请增加 SWE benchmark](https://github.com/NousResearch/hermes-agent/issues/23137)
- [SWE-bench 官方](https://github.com/swe-bench/SWE-bench)
- [SWE-bench Verified 排行榜](https://swebench.com/verified.html)
