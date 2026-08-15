# Hermes Agent 评测方案与实现分析

资料范围：

- 本地仓库：`/Users/liyazhou/.hermes/hermes-agent`（`main` branch）
- 远程仓库：`https://github.com/NousResearch/hermes-agent`
- DeepWiki 文档：<https://deepwiki.com/NousResearch/hermes-agent/9.1-batch-runner>
- 在线文档：<https://hermes-agent.nousresearch.com/docs/>

## 结论先行

Hermes Agent 的评测体系不是单一测试框架，而是一套以**轨迹（trajectory）生成和评估为核心**的分层系统。它没有像 OpenClaw 那样预设 QA Lab scenario 集，而是提供了一个**开放式的数据生成管道**——通过 `batch_runner.py` 并行驱动 agent 执行大量 prompt、收集结构化轨迹、统计工具调用和推理覆盖，再通过 `trajectory_compressor.py` 压缩轨迹用于训练。这套系统的主要设计目的是**训练数据生产**，但同时具备以下评测能力：

1. **数据生成驱动评测**：`batch_runner.py` 以 JSONL 为输入、JSONL 为输出，生成包含工具统计和推理指标的轨迹报告。
2. **最小化 SWE 评测**：`mini_swe_runner.py` 提供 SWE-bench 风格的 agent 评测，支持 local/docker/modal 环境。
3. **浏览器性能评测**：`scripts/benchmark_browser_eval.py` 量化浏览器工具的执行效率。
4. **标准 pytest 回归**：~900 文件、~17000 测试，采用 per-file 子进程隔离。
5. **Kanban 内核压力/性能评测**：多进程争用、随机操作序列、基准测试。
6. **自动质量过滤**：无推理轨迹丢弃、幻觉工具名过滤。

Hermes 评测的核心特点是：**以训练数据生产为主线，轨迹格式为中心，工具使用统计为副产品，并行 checkpoint 容错为工程保障。**

## 评测系统总览

```
hermes-agent/
├── batch_runner.py               # 核心：批量数据生成/评测引擎（并行、checkpoint、统计）
├── mini_swe_runner.py            # SWE-bench 风格 agent 评测（local/docker/modal）
├── trajectory_compressor.py      # 轨迹后处理压缩（训练数据准备）
├── toolset_distributions.py      # 工具集概率分布（评测变量控制）
├── run_agent.py                  # AIAgent 类：含 trajectory 保存、conversation loop
├── scripts/
│   ├── run_tests.sh              # 标准 pytest 回归入口
│   ├── run_tests_parallel.py     # per-file 并行测试运行器
│   └── benchmark_browser_eval.py # 浏览器 eval 性能对比
├── tests/
│   ├── (900+ 文件, ~17000 测试)   # 按模块组织：agent/ CLI/ gateway/ 等
│   ├── integration/              # 集成测试（batch_runner / checkpoint / web工具等）
│   ├── stress/                   # 压力/性能测试（Kanban 基准、并发、fuzzing）
│   └── e2e/                      # 端到端测试（Discord/平台命令）
├── datagen-config-examples/      # 数据生成配置示例
│   ├── run_browser_tasks.sh      # 浏览器任务数据生成
│   └── web_research.yaml         # Web 研究任务配置
└── website/docs/                 # 文档站含 batch-processing 页
```

## 1. 标准 pytest 回归（工程质量）

Hermes 的常规工程质量测试通过 `pytest` 实现，规模在四个项目中最大。

### 命令层级

| 入口 | 作用 | 覆盖范围 |
|---|---|---|
| `scripts/run_tests.sh` | 标准回归入口 | ~900 文件, ~17000 测试 |
| `scripts/run_tests.sh tests/agent/` | 模块子集 | agent loop/CLI/gateway 等 |
| `scripts/run_tests.sh tests/foo.py` | 单文件 | 指定文件 |
| `HERMES_TEST_WORKERS=8 scripts/run_tests.sh` | 控制并行度 | 自定义线程数 |
| `pytest tests/stress/test_benchmarks.py` | Kanban 基准 | 性能基线 |
| `pytest tests/stress/test_concurrency.py` | 并发正确性 | Kanban 内核并发 |

### 架构特点：per-file 子进程隔离

`scripts/run_tests_parallel.py` 的架构：

- 不使用 pytest-xdist（xdist 的持久 worker 跨文件累积状态）
- 每个测试文件启动独立 `python -m pytest <file>` 子进程
- 默认跳过 `integration/` 和 `e2e/`（需要外部服务）
- 默认并行度 = `os.cpu_count()`
- 单文件超时默认 600 秒

这样做的好处是**彻底杜绝跨文件 module-level 状态泄漏**，但代价是每个文件的启动开销约 250ms。对于 900+ 文件的规模，总启动时间约 3.5 分钟。

### conftest.py 常态化约束

`tests/conftest.py` 确保每个测试在常态化环境中运行：

- 所有 `_API_KEY`、`_TOKEN`、`_SECRET` 等凭据环境变量被清除
- `HERMES_HOME` 指向 per-test 临时目录
- `TZ=UTC`、`LANG=C.UTF-8`、`PYTHONHASHSEED=0` 固定

### 测试分类

| 类别 | 目录 | 内容 |
|---|---|---|
| 单元测试 | `tests/agent/`、`tests/cli/`、`tests/providers/` | Agent loop、工具调用、provider 适配 |
| 集成测试 | `tests/integration/` | batch_runner、checkpoint、Modal/Docker 终端、web 工具 |
| 压力测试 | `tests/stress/` | Kanban 基准、多进程并发、fuzzing、异常场景 |
| E2E 测试 | `tests/e2e/` | Discord adapter、平台命令 |
| 模块专项 | `tests/run_agent/` | ~90 个测试文件覆盖 AIAgent 各维度行为 |

### conftest.py 文件隔离策略

从 `AGENTS.md` 可以看到：

> Tests run via `scripts/run_tests_parallel.py`, which spawns a fresh `python -m pytest <file>` subprocess per test file. Cross-file state leakage (module-level dicts, ContextVars, caches) is impossible: each file gets a clean Python interpreter.

这解决了 OpenClaw 等项目中常见的跨文件状态泄漏问题，但代价是**无法使用 xdist 的共享 worker 来加速**。

## 2. Batch Runner（核心数据生成/评测引擎）

`batch_runner.py`（1321 行）是 Hermes 评测体系的核心组件。它虽然名为"batch runner"，但实际上承担了**大规模 agent 行为数据采集和质量评估**的双重角色。

### 数据流

```
JSONL 数据集 (prompt 列表)
  → 分批 (batch_size=N)
  → 并行 multiprocessing.Pool (num_workers=M)
    → 每个 prompt 启动独立 AIAgent 实例
      → run_conversation() 执行
      → 提取工具统计/推理覆盖
      → 转换轨迹格式
    → 写入 batch_N.jsonl
  → 合并为 trajectories.jsonl
  → 输出 statistics.json
```

### 核心能力

#### 1) 并行架构

```python
with Pool(processes=self.num_workers) as pool:
    for result in pool.imap_unordered(_process_batch_worker, tasks):
        # 增量 checkpoint 更新
```

每个 worker 进程内，prompt 串行执行但共享一个进程池。支持**增量 checkpoint**：每完成一个 batch 立即保存，宕机后可通过 `--resume` 恢复。

#### 2) Checkpoint 容错

两种恢复机制：

- **基于索引**：记录已完成 prompt 的 index
- **基于内容**：扫描已有 batch_*.jsonl 文件，按 prompt 文本去重

```python
def _scan_completed_prompts_by_content(self) -> set:
    """Scan all batch files and extract completed prompts by actual prompt text."""
    # 遍历 batch 文件，提取每个 entry 的 human 消息内容
```

这种方式允许 dataset 顺序变化后仍能正确恢复。

#### 3) 工具使用统计

`_extract_tool_stats()` 从消息历史中提取每个工具的调用次数、成功/失败次数：

```python
# 判定成功的逻辑：
# - 解析 tool response 的 JSON
# - 检查 error 字段是否为 null
# - 检查 success 字段
# - 特殊处理 terminal tool 的包裹格式
# - 不将非零 exit code 视为失败（模型可以自纠正）
```

统计结果归一化到所有已知工具（从 `TOOL_TO_TOOLSET_MAP` 自动推导），保证 HuggingFace dataset schema 一致。

#### 4) 推理覆盖度追踪

`_extract_reasoning_stats()` 统计每个 prompt 中 assistant turn 的推理覆盖度：

- `<REASONING_SCRATCHPAD>` XML tag
- 原生 thinking tokens（`reasoning` field）

**零推理样本过滤**：如果整个 prompt 执行过程中没有一次 assistant turn 包含推理，该样本被丢弃。这保证了训练数据质量。

#### 5) 最终输出质量过滤

在合并 `trajectories.jsonl` 时，自动过滤：

- **幻觉工具名**：如果 `tool_stats` 中包含不在 `VALID_TOOLS` 集中的工具名（模型幻觉），过滤
- **无效 JSON**：JSON 解析失败的行

### 评测用例

Batch runner 本身不限定数据集内容——使用者提供 JSONL，runner 执行并采集指标。常见用途：

```bash
# 模型评测
python batch_runner.py \
    --dataset_file=data/eval_suite.jsonl \
    --batch_size=10 --run_name=eval_gpt4 \
    --model=openai/gpt-4o --num_workers=4 --max_turns=10

# 训练数据生成（含工具集随机采样）
python batch_runner.py \
    --dataset_file=data/coding_prompts.jsonl \
    --distribution=development --max_turns=15
```

### 统计输出示例

```
📈 Tool Usage Statistics:
-------------------------------------------------------------------------
Tool Name                  Count      Success    Failure    Success Rate
-------------------------------------------------------------------------
terminal                   284        276        8          97.2%
web_search                 156        149        7          95.5%
read_file                  92         92         0          100.0%

🧠 Reasoning Coverage:
-------------------------------------------------------------------------
Total assistant turns:     1,247
With reasoning:            1,183 (94.9%)
Without reasoning:         64    (5.1%)
🚫 Samples discarded (zero reasoning): 12
```

## 3. Toolset Distributions（评测变量控制）

`toolset_distributions.py`（364 行）定义了**评测/数据生成中工具集的随机采样分布**。每个 prompt 独立采样，保证评测数据的多样性。

### 工作机制

每个 distribution 是一个 `{toolset_name: probability_percentage}` 字典。采样时每个 toolset 独立按照概率决定是否启用，且**保证至少一个 toolset 被选中**。

### 主要分布

| 分布名 | 意图 | 高概率工具 |
|---|---|---|
| `default` | 全部工具、全概率 | web/vision/image_gen/terminal/file/moa/browser 各 100% |
| `balanced` | 等概率随机 | 所有工具 50% |
| `research` | 网页研究 | web 90%, browser 70%, vision 50% |
| `development` | 编码任务 | terminal 80%, file 80%, moa 60% |
| `browser_use` | 浏览器自动化 | browser 100%, web 80% |
| `science` | 科学研究 | web 94%, terminal 94%, file 94% |
| `image_gen` | 图像生成 | image_gen 90%, vision 90% |
| `safe` | 安全模式（无 terminal） | web/browser/vision/image_gen/moa |
| `browser_tasks` | 浏览器任务数据生成 | browser 97%, terminal 15% |
| `terminal_tasks` | 终端任务数据生成 | terminal 97%, file 97%, web 97% |
| `mixed_tasks` | 混合任务 | browser 92%, terminal 92%, file 92% |

这种设计比固定工具集更灵活——通过调整概率控制评测难度分布，同时避免过拟合到单一工具组合。

## 4. Agent 级轨迹特征（run_agent.py）

`AIAgent` 类内置了轨迹采集能力，这是 batch runner 的单次执行基础。

### 轨迹保存

```python
class AIAgent:
    def _convert_to_trajectory_format(self, messages, user_query, completed):
        """Forwarder → agent.agent_runtime_helpers.convert_to_trajectory_format"""
    
    def _save_trajectory(self, messages, user_query, completed):
        """保存成功→trajectory_samples.jsonl, 失败→failed_trajectories.jsonl"""
```

### 轨迹格式（ShareGPT-like）

```json
{"conversations": [
    {"from": "system", "value": "You are a function calling AI model..."},
    {"from": "human", "value": "Write a function..."},
    {"from": "gpt", "value": "<think>...</think>\n<tool_call>{\"name\": \"terminal\", ...}</tool_call>"},
    {"from": "tool", "value": "<tool_response>...</tool_response>"},
    {"from": "gpt", "value": "Here's the completed function..."}
]}
```

关键设计决策：

- **不保存 system prompt 中的 ephemeral 内容**（如 `skip_context_files=True` 跳过 SOUL.md）
- **不保存多模态图像 base64**（`_trajectory_normalize_msg` 替换为 text_summary）
- **推理转 `<think>` tag**：`<REASONING_SCRATCHPAD>` → `<think>`，原生 reasoning field 也转为 `<think>` 嵌入
- **强制每个 gpt turn 有 `<think>` 块**：保证训练格式一致性
- **不对工具参数执行 JSON 验证**：runtime 已保证，trajectory 转换只做 try-catch

### CLI 脚本入口

```bash
# 单次运行+轨迹保存
python run_agent.py --save_trajectories --query="..."

# 单次运行+保存 inspect 用样本
python run_agent.py --save_sample --query="..."
```

## 5. Mini-SWE Runner（SWE-bench 风格评测）

`mini_swe_runner.py`（735 行）是专门为 SWE-bench 类任务设计的评测 runner。它**独立于 batch_runner**，但输出兼容的轨迹格式。

### 架构

```
MiniSWERunner
├── 终端环境: LocalEnvironment / DockerEnvironment / ModalEnvironment
├── Agent loop: 纯 OpenAI Chat Completions 循环
└── 输出: Hermes 格式轨迹（from/value pairs + <tool_call>/<tool_response> XML）
```

### 核心差异

相比 `batch_runner`，`mini_swe_runner`：

- **不使用 Hermes 的 AIAgent 类**，而是直接用 `openai.OpenAI` client
- 只暴露一个 `terminal` 工具（而非完整工具集）
- 使用 `MINI_SWE_AGENT_FINAL_OUTPUT` 信号标记任务完成
- 支持 per-task container image

### 使用场景

```bash
# 单任务
python mini_swe_runner.py --task "Create hello.py" --env local

# Docker 环境
python mini_swe_runner.py --task "Install numpy" --env docker --image python:3.11-slim

# 批处理
python mini_swe_runner.py --prompts_file tasks.jsonl --output_file results.jsonl
```

它对温度做了特殊处理：某些模型（如 Kimi）由服务端控制温度，client 不能传 `temperature` 参数，`_effective_temperature_for_model()` 负责处理这种差异。

## 6. Trajectory Compressor（轨迹压缩管道）

`trajectory_compressor.py`（1508 行）不是评测工具，但它是批量数据生成的**后处理阶段**，直接影响评测产物的可用性。

### 压缩策略

```
1. 保护开头: system/human/gpt-首轮/tool-首轮
2. 保护末尾: 最后 N 轮（最终行动和结论）
3. 仅压缩中间: 从第 2 个 tool response 开始
4. 按需压缩: 只压缩到目标 token 数以下
5. 替换为摘要: 压缩区域替换为一条 human summary message
6. 保留剩余工具调用: 模型可继续工作
```

### 用途

用于将长轨迹（如 30+ 轮的复杂任务）压缩到目标 token 预算内。压缩后的轨迹仍然保持 `from/value` 格式，可正常用于训练或下游评估。

## 7. 浏览器 Eval Benchmark

`scripts/benchmark_browser_eval.py` 是一个轻量的浏览器工具执行效率基准。

### 评测内容

对比两种路径的性能：

- **subprocess eval**：每次评估启动新 CDP session
- **supervisor-WS eval**：通过 supervisor 的持久 CDP WebSocket 复用

### 实现

```python
# 启动 headless Chrome
chrome_proc, profile, cdp_url = _start_chrome(port)

# supervisor 路径
supervisor = SUPERVISOR_REGISTRY.get_or_start(task_id="bench-eval", cdp_url=cdp_url)
result = supervisor.evaluate_runtime("1 + 1")

# subprocess 路径
result = subprocess_evaluate(cdp_url, "1 + 1")
```

默认 50 次迭代，输出对比表格。这个 benchmark 的诞生背景是 PR #23226，通过改用 supervisor 的持久连接实现了 **180x 性能提升**。

## 8. Kanban 内核压力/性能评测

Kanban 是 Hermes 的多 agent 板调度系统，`tests/stress/` 目录下有专门的基准和压力测试。

### 基准测试（test_benchmarks.py）

测量 Kanban 内核各操作在批量下的延迟：

| 操作 | 规模 | 输出指标 |
|---|---|---|
| `dispatch_once` | 100 / 1000 / 10000 tasks | min/median/max latency (ms) |
| `recompute_ready` | 同上（含 parent graph） | min/median/max latency (ms) |
| `build_worker_context` | 1 / 10 / 50 parent deps | min/median/max latency (ms) |
| `list_tasks` | 同上 | 查询延迟 |
| `board_stats` | 同上 | 统计查询延迟 |

输出同时打印表格并保存 JSON，支持后续 CI regression diff。

### 并发测试（test_concurrency.py）

多进程争用测试：5 个 worker 进程在 100 个 task 上争抢 claim，验证：

- 无 task 被两个 worker 同时 claim
- 无 task 被完成两次
- 每个 claim 产生且只产生一个 run row
- 零 SQLite locking error 逃逸 retry 层

### 属性 fuzzing（test_property_fuzzing.py）

生成 500 条随机操作序列（每条 20-100 ops），在小 task graph 上按序执行，每一步检查完备不变式集（I1-I9），覆盖 corner case。

## 9. 数据生成配置示例

`datagen-config-examples/` 提供了实际的数据生成评测用例参考：

```bash
# browser 任务数据生成
bash datagen-config-examples/run_browser_tasks.sh

# 内部调用
python batch_runner.py \
  --dataset_file="datagen-config-examples/example_browser_tasks.jsonl" \
  --distribution="browser_tasks" \
  --model="anthropic/claude-sonnet-4" \
  --ephemeral_system_prompt="..." \
  --max_turns=30
```

数据生成时使用的 ephemeral system prompt 不写入轨迹（`--ephemeral_system_prompt`），防止数据污染。

## 10. 评测体系总结

### 分层评测覆盖

| 层次 | Hermes 实现 | 成熟度 |
|---|---|---|
| L0 工程 gate | pytest per-file 隔离、~17000 测试 | ⭐⭐⭐⭐⭐ |
| L1 组件行为 | provider/tool/session/CLI 单元测试 | ⭐⭐⭐⭐⭐ |
| L2 Agent loop | agent loop mock 测试 + trajectory 格式测试 | ⭐⭐⭐⭐ |
| L3 Scenario eval | batch_runner 开放式数据生成（无预设 scenario 集） | ⭐⭐⭐ |
| L4 Live eval | 无独立 lane（依赖外部集成测试） | ⭐⭐ |
| L5 Benchmark | Kanban 延迟基准、browser eval benchmark | ⭐⭐⭐ |

### 与 OpenClaw 的关键差异

| 维度 | Hermes | OpenClaw |
|---|---|---|
| 核心设计意图 | 训练数据生产管道 | Agent 行为验证平台 |
| Scenario 管理 | 无预设 scenario 集 | Markdown 文件 + qa-channel |
| 确定性断言 | 工具调用/推理统计 | 状态/工具/文件/DB 断言 |
| LLM Judge | 无 | 有（结构化 rubric） |
| Checkpoint | multiprocessing + JSON | 无（非批量设计） |
| 轨迹格式 | ShareGPT-like from/value | 无独立轨迹格式 |
| 性能基线 | Kanban 基准 + browser eval | 启动/重启延迟 |
| 测试隔离 | per-file 子进程 | 标准 vitest（单进程） |

### 主要缺口

1. **缺少情景化评测集**：batch_runner 只是框架，没有内置的任务级评测集（scenario catalog）。用户需要自己准备 JSONL 数据集。
2. **无 LLM Judge 评测**：没有像 OpenClaw 那样用 LLM 作为 judge 来评估开放式任务质量。
3. **无统一评测报告**：statistics.json 只是工具使用的聚合统计，缺乏逐任务的成功率/失败原因分析。
4. **无 Live eval lane**：没有专门的真实模型/真实凭据评测通道。测试框架清除了所有凭据 env var，运行前需要手动注入。
5. **无跨版本 baseline 比较**：Kanban 基准虽然有 JSON 输出，但没有建立 CI baseline diff 机制。
6. **无增量评测**：每次 batch run 从头开始，不支持"只评测新增/修改场景"的增量模式。
7. **无任务级 DAG 管理**：Kanban 的多 agent 协调系统本身没有纳入评测范围。
