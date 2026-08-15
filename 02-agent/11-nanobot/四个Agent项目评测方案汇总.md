# Agent评测方案汇总

范围：`/Users/liyazhou/Repo/repo_ai` 下的 `nanobot`、`openclaw`、`pi`、`hermes-agent`。

目标：把各项目当前已有的测试/评测资产放到同一张图里，区分“工程质量测试”“端到端行为验证”“真实模型/真实通道评测”“性能/压力评测”和“缺口”。

## 总览矩阵

| Project | 项目定位 | 当前评测成熟度 | 主要入口 | 覆盖重点 | 主要缺口 |
|---|---|---:|---|---|---|
| `openclaw` | 多通道 AI gateway、插件/扩展运行时、CLI/desktop/web 周边 | 高 | `pnpm test`、`pnpm test:e2e`、`pnpm test:live`、`pnpm test:docker:*`、`pnpm qa:e2e`、`pnpm openclaw qa suite` | unit/e2e/live/docker/QA scenario/perf/observability/security | 已有体系很强，后续重点是把 QA scenario 的指标、判分和报告沉淀成稳定 dashboard |
| `hermes-agent` | 自改进个人 Agent，CLI/gateway/skills/memory/MCP/ACP/terminal backend | 中高 | `scripts/run_tests.sh`、`pytest tests/stress`、`scripts/benchmark_browser_eval.py`、`ui-tui npm test` | Python 单测/集成、ACP、agent loop、providers、CLI、stress、browser eval benchmark | 缺少类似 `openclaw/qa/scenarios` 的统一任务级 agent eval pack；web 前端没有独立 test 脚本 |
| `nanobot` | 轻量 personal AI agent，WebUI、channel、memory、MCP、automation | 中高 | `pytest`、`pytest --cov`、`cd webui && bun run test`、`bun run lint` | agent loop、providers、channels、security、cron、MCP、WebUI unit | 缺少任务级/多轮 agent eval、真实通道 live eval、桌面端自动化测试 |
| `pi` | Agent harness monorepo：coding-agent、agent core、LLM API、TUI | 中高 | `npm run test`、`npm run check`、`./test.sh`、包级 `vitest` / `node --test`、`npm run release:local` | provider API 兼容（41 文件）、agent session 运行时（6 suite 文件）、160 coding-agent 组件测试、17 per-issue regression、22 TUI 测试、FauxProvider 测试框架、凭据隔离、7 个分析脚本 | 缺少独立 QA/eval scenario 层；Suite 测试基于 FauxProvider（非真实模型）；无性能基准 |

## 统一评测维度建议

建议四个项目都用下面的维度描述评测，而不是只列测试命令：

| 维度 | 说明 | 最适合的项目 |
|---|---|---|
| 工程正确性 | 单元测试、类型检查、lint、包边界、依赖安全 | 全部 |
| Agent loop 正确性 | 多轮上下文、工具调用、恢复、压缩、stop/retry、subagent | `nanobot`、`hermes-agent`、`pi`、`openclaw` |
| Provider/model 兼容 | OpenAI/Anthropic/Gemini/OpenRouter/Bedrock 等请求格式、stream、tool call、reasoning | 全部 |
| Channel/gateway 行为 | Telegram/Slack/Discord/Feishu/WhatsApp/WebSocket/gateway routing | `openclaw`、`hermes-agent`、`nanobot` |
| 任务级 eval | 用固定 scenario 衡量任务完成率、工具使用质量、恢复能力、是否撒谎 | `openclaw` 已有，其他项目建议补 |
| Live eval | 真实模型、真实凭据、真实外部服务，隔离在手动或 nightly lane | `openclaw`、`hermes-agent`、`nanobot`、`pi` |
| 性能/压力 | 启动时间、gateway restart、browser eval latency、并发、长上下文、soak | `openclaw`、`hermes-agent`、`pi` |
| 安全/权限 | secret redaction、workspace sandbox、approval、network/file boundary、dependency pin | 全部 |

## Agent 测评技术方案

Agent 测评不要只看最终回答。对这四个项目来说，更有效的技术方案是“分层评测”：

| 层级 | 评测对象 | 推荐判分方式 | 适用场景 |
|---|---|---|---|
| L0 工程 gate | 代码、类型、lint、依赖、包边界 | 确定性 pass/fail | PR 必跑 |
| L1 组件行为 | provider adapter、tool schema、stream parser、session state | mock/faux provider + 状态断言 | 高频回归 |
| L2 Agent loop | 多轮、工具调用、stop/retry、压缩、memory、subagent | trajectory/trace 断言 | Agent 核心能力 |
| L3 Scenario eval | 固定任务、固定环境、固定成功标准 | DSL/脚本 runner + 结构化结果 | nightly/release |
| L4 Live eval | 真实模型、真实凭据、真实通道、真实外部服务 | report + 人工复核/LLM judge | release/manual |
| L5 Benchmark | 启动、延迟、并发、成本、稳定性 | JSON baseline diff | 性能预算 |

这和 OpenAI eval best practices 的思路一致：先定义目标、收集数据、定义指标、运行比较、持续评测；同时要避免只靠“感觉可用”、泛泛指标或不贴近生产流量的数据集。OpenAI 文档也明确把 agent eval 关注点拆成 functional correctness、tool selection、tool argument precision、handoff accuracy 等维度。

### 推荐架构

```text
eval/
  scenarios/
    approval-turn-tool-followthrough.md
    memory-recall.md
    tool-argument-precision.md
  fixtures/
    mock-provider.jsonl
    workspace-template/
  runner/
    scenario-loader.ts
    flow-runner.ts
    transport.ts
    judges.ts
  reports/
    report-schema.json
    latest.json
    latest.md
  baselines/
    startup.json
    tool-call-latency.json
```

核心模块：

- Scenario catalog：从 Markdown/YAML/JSONL 读取任务元数据、风险级别、coverage、成功标准。
- Environment harness：创建临时 workspace、mock provider、fake tools、测试 gateway、真实或模拟 channel。
- Agent transport：把 prompt 发给 CLI、WebSocket、gateway、API 或 live channel。
- Trace capture：记录 messages、tool calls、tool args、tool outputs、files changed、stdout/stderr、token/cost、latency。
- Deterministic checker：用代码检查状态、工具调用、文件系统、数据库、HTTP response。
- LLM judge：只用于开放式质量判断，输入应包含 rubric 和 evidence，输出结构化 JSON。
- Report writer：输出 machine-readable JSON 和 human-readable Markdown。
- Baseline comparator：对成功率、延迟、成本、tool-call 数量做差异比较。

### 指标设计

建议 report schema 至少包含：

```json
{
  "project": "openclaw",
  "run_id": "2026-06-07T04:00:00Z",
  "lane": "nightly",
  "provider_mode": "mock-openai",
  "model": "gpt-5.5",
  "scenario": {
    "id": "approval-turn-tool-followthrough",
    "title": "Approval turn tool followthrough",
    "risk": "high",
    "coverage": ["runtime.approvals", "tools.followthrough"]
  },
  "status": "pass",
  "metrics": {
    "duration_ms": 42132,
    "turns": 2,
    "tool_calls": 1,
    "tokens_input": 1200,
    "tokens_output": 240,
    "cost_estimate": 0.01
  },
  "checks": [
    {"name": "read QA_KICKOFF_TASK.md", "status": "pass"}
  ],
  "artifacts": {
    "transcript": ".artifacts/eval/transcript.jsonl",
    "workspace": ".artifacts/eval/workspace"
  }
}
```

关键指标可以分成几类：

- 任务完成率：scenario pass rate、pass@k、连续多次运行稳定性。
- 工具行为：expected tools、actual tools、参数正确率、无效调用率、重复调用率。
- 轨迹质量：是否中途停止、是否假装完成、是否在 approval 后继续执行、是否按顺序调用工具。
- 状态结果：文件是否修改正确、数据库最终状态是否等于目标状态、HTTP/API 是否返回预期。
- 记忆/上下文：是否召回正确偏好、是否跨 thread 污染、是否压缩后丢关键事实。
- 成本性能：turn 数、tool-call 数、token、latency、启动时间、重试次数。
- 安全边界：secret redaction、approval、workspace scope、network allowlist、shell sandbox。

### 判分策略

优先级建议：

1. 能用确定性检查就不用 LLM judge：文件 diff、DB state、tool call、HTTP response、stdout 都应该直接断言。
2. LLM judge 只评开放式输出：例如总结质量、风格一致性、是否解释清楚，但必须给 rubric 和 evidence。
3. 对 tool-use agent，要保存 trajectory：只保存最终回答会漏掉“没调用工具但编造结果”的问题。
4. 对真实模型要做多次运行：`pass@1` 看单次能力，`pass@k` 或多 run 方差看可靠性。
5. 对 coding agent，要用项目原生测试验证最终 patch，不只看模型解释。

这个思路也能对应到公开 benchmark：SWE-bench Verified 用真实 GitHub issue + 测试补丁评估 coding agent；tau-bench 用模拟用户和工具 API 交互，最后比较数据库终态；LangSmith 类平台强调捕获完整 trajectory，包括步骤、工具调用和推理链路。

## nanobot

### 当前评测入口

- Python 主测试：`/Users/liyazhou/Repo/repo_ai/nanobot/pyproject.toml`
  - `dev` extra 包含 `pytest`、`pytest-asyncio`、`pytest-cov`、`ruff`
  - `[tool.pytest.ini_options]`：`asyncio_mode = "auto"`，`testpaths = ["tests"]`
  - `[tool.coverage.run]`：`source = ["nanobot"]`
- WebUI：`/Users/liyazhou/Repo/repo_ai/nanobot/webui/package.json`
  - `bun run test` -> `vitest run`
  - `bun run lint`
  - `bun run build`
- Desktop：`/Users/liyazhou/Repo/repo_ai/nanobot/desktop/package.json`
  - 有 build/dev/package 脚本，没有看到独立 test 脚本。

### 当前覆盖

`tests/` 覆盖面比较广，主要包括：

- Agent loop：auto compact、runner、goal continue、tool execution、fallback、reasoning、stop、task cancel、subagent、session persistence。
- Memory/session：dream、memory store、session manager、atomic write、goal state、context builder。
- MCP/tool/CLI apps：MCP connection、transient retry、tool loader、CLI apps service/tool。
- Providers：Anthropic、OpenAI Responses、OpenAI Codex、Bedrock、Mistral、MiniMax、StepFun、image generation、transcription、retry/cache 等。
- Channels：Telegram、Slack、Discord、Feishu、DingTalk、QQ、Matrix、Signal、WeCom、Weixin、WhatsApp、WebSocket。
- Security：network、workspace policy、workspace sandbox。
- Cron/config/API/document parsing：cron persistence、config migration、OpenAI-compatible API、attachments、document parsing。

### 判断

`nanobot` 的工程测试覆盖已经比较实用，尤其是 agent runtime、channels、providers、security 这些高风险面。它目前更像“功能/回归测试体系”，不是完整“评测体系”。

### 建议补齐

- 增加 `eval/scenarios/` 或 `qa/scenarios/`：覆盖多轮任务、工具链、记忆召回、channel thread、长任务恢复、workspace edit 等任务级行为。
- 定义统一指标：`pass/fail`、任务完成率、工具调用成功率、重试次数、最终回答质量、是否泄漏 secret、是否虚构进度。
- 增加 live lane：用少量真实模型和真实 channel 做 nightly/manual eval，避免每次 PR 都跑。
- Desktop 端补最小 smoke：启动、加载 packaged WebUI、engine 准备、基础设置页可打开。

### 可借鉴的实现细节

`nanobot` 已经有一个小型 LLM-as-judge 实现：`nanobot/utils/evaluator.py`。它用于后台任务完成后判断是否通知用户：

- 输入：`response`、`task_context`、provider、model。
- 方式：向模型发一个低温度请求，并提供 `evaluate_notification` function tool。
- 输出：工具参数里的 `should_notify: boolean`。
- 失败策略：异常或无工具调用时返回 `default_notify`，cron 可以 fail-open，heartbeat 可以 fail-closed。

这说明 `nanobot` 已经具备“结构化 judge”的雏形。后续可以把它扩展成通用 judge：

- `evaluate_task_completion(scenario, transcript, artifacts) -> score`
- `evaluate_response_quality(rubric, final_answer, evidence) -> score`
- `evaluate_safety(transcript, tool_calls) -> pass/fail`

但核心任务完成仍应优先用确定性检查，例如文件是否存在、WebSocket 是否收到消息、channel reply 是否进入正确 thread。

## openclaw

### 当前评测入口

- 根测试脚本：`/Users/liyazhou/Repo/repo_ai/openclaw/package.json`
  - `pnpm test` -> `node scripts/test-projects.mjs`
  - `pnpm test:unit`、`pnpm test:unit:fast`
  - `pnpm test:e2e` -> gateway e2e + UI e2e
  - `pnpm test:live`
  - `pnpm test:docker:all` 和大量 `test:docker:*`
  - `pnpm test:coverage`
  - `pnpm test:startup:bench`、`pnpm test:startup:gateway`、`pnpm test:restart:gateway`
  - `pnpm qa:e2e`、`pnpm qa:otel:smoke`、`pnpm qa:observability:smoke`
- QA 资产：`/Users/liyazhou/Repo/repo_ai/openclaw/qa/README.md`
  - `qa suite`：可执行 frontier subset / regression loop
  - `qa manual`：personality/style probe
  - `qa coverage`：scenario coverage inventory
- QA scenarios：`/Users/liyazhou/Repo/repo_ai/openclaw/qa/scenarios/`
  - agents、channels、config、jsonl replay、media、memory、models、personal、plugins、runtime、scheduling、security、ui、workspace 等。

### 当前覆盖

`openclaw` 是四个项目里最接近完整评测平台的：

- Unit/gateway/contracts：core gateway、client、protocol、plugin/channel contracts。
- E2E：CLI launcher、gateway multi、UI e2e、openshell、install/onboard/release journey。
- Docker e2e：插件生命周期、OpenAI chat tools/image/web search、upgrade survivor、skill install、gateway network、release upgrade、published install 等。
- Live eval：Codex harness、CLI backend、gateway models、media image/music/video、ACP bind。
- QA Lab：大量 markdown scenario 和 JSONL replay，用于可执行 frontier subset、manual personality/style probe、coverage inventory。
- Performance：CLI startup、gateway startup/restart、test hotspot/group/import profiling、perf budget。
- Observability/security：OTel/Prometheus smoke、secret scanning、dependency vulnerability gate、sandbox/approval/credential broker payload validation。

### 判断

`openclaw` 可作为其他三个项目的参考基准。它已经把“测试”“QA scenario”“live lane”“性能预算”“docker 用户旅程”分层得比较清楚。

### 建议补齐

- 把 `qa suite` 的输出固化成机器可读报告：scenario、provider mode、结果、耗时、失败原因、transcript/artifact 链接。
- 给 QA scenario 增加稳定分级：PR gate、nightly、manual/live、release candidate。
- 为 `qa manual` 增加 rubric：persona/style 不宜只靠人工感觉，应至少有结构化 checklist。
- 汇总 perf baseline：startup/gateway/restart/changed-test bench 的历史趋势可以和 release checklist 绑定。

### 实现细节

`openclaw` 的 QA Lab 是四个项目里最接近完整 agent eval harness 的实现。

关键代码：

- `extensions/qa-lab/src/scenario-catalog.ts`
- `extensions/qa-lab/src/scenario-flow-runner.ts`
- `extensions/qa-lab/src/report.ts`
- `extensions/qa-lab/src/agentic-parity-report.ts`
- `scripts/qa-e2e.ts`
- `scripts/qa-coverage-report.ts`

它的设计有几个亮点：

- Scenario 用 Markdown 承载，人可读；用 fenced YAML 承载机器可执行配置。
- `qa-scenario` 定义 id、title、surface、coverage、objective、successCriteria、docsRefs、codeRefs、execution config。
- `qa-flow` 定义步骤和动作，flow runner 支持 `call`、`set`、`assert`、`throw`、`if`、`forEach`、`try/catch/finally`。
- scenario catalog 用 `zod` 校验 schema，包括 coverage id、risk、runtime parity tier、flow step 等。
- runner 会把每个 step 转成可执行函数，失败时立刻返回 scenario fail，并保留 step details。
- report writer 输出 Markdown，包括 started/finished、duration、passed/failed、checks、scenarios、timeline、notes。
- coverage report 支持 JSON 输出，也支持把 runtime `qa-suite-summary.json` 叠加到 tool coverage 上。

一个典型 scenario 是 `qa/scenarios/runtime/approval-turn-tool-followthrough.md`：

- 第一轮让 Agent “先别用工具，只说准备读哪个文件”。
- 第二轮发短确认：`ok do it`。
- flow 断言 Agent 后续真的读文件并返回与 QA mission 相关的回复。

这个 scenario 测的是 Agent 产品里很常见的故障：用户批准后，Agent 只输出“我会继续”之类的假进度，而没有实际调用工具。

`agentic-parity-report.ts` 进一步做了候选/基线对比：

- completion rate
- unintended stop rate
- valid tool call rate
- fake success count
- runtime parity drift
- candidate/baseline scenario coverage mismatch

这套设计可以直接作为另外三个项目的 eval 模板。

## pi

### 当前评测入口

- 根目录：`/Users/liyazhou/Repo/repo_ai/pi/package.json`
  - `npm run test` -> `npm run test --workspaces --if-present`
  - `npm run check` -> `biome check`、pinned deps、TS imports、shrinkwrap、`tsgo --noEmit`、browser smoke
  - `npm run build`
  - `npm run release:local`
  - `profile:tui`、`profile:rpc`
- **凭据隔离入口**：`./test.sh`
  - 备份 `~/.pi/agent/auth.json`，测试结束后恢复
  - unset 40+ 个 API key 环境变量（覆盖所有主流 provider + AWS 凭据）
  - 设置 `PI_NO_LOCAL_LLM=1`
  - 然后执行 `npm test`
- 包级测试（233 个测试文件）：
  - `packages/agent/package.json`：`vitest --run`（10 文件）
  - `packages/ai/package.json`：`vitest --run`（41 文件）
  - `packages/coding-agent/package.json`：`vitest --run`（160 文件）
  - `packages/tui/package.json`：`node --test test/*.test.ts`（22 文件）
- 分析脚本（离线 session 评估）：
  - `scripts/cost.ts`、`stats.ts`、`tool-stats.ts`、`edit-tool-stats.mjs`、`read-tool-stats.mjs`、`session-context-stats.mjs`、`session-transcripts.ts`

### 当前覆盖

- **FauxProvider 框架**（`packages/ai/src/providers/faux.ts`）：完整可编程 LLM provider 模拟，支持 thinking/text/toolCall 分块构造、streaming 事件序列控制、prompt caching 模拟、token 估算、AbortController。自身有 20+ 测试覆盖 20 种场景。
- **Suite 测试**（6 文件）：`coding-agent/test/suite/` 使用真实 `AgentSession` + FauxProvider，覆盖运行时（596 行）、compaction（407 行）、queue（422 行）、retry-events（360 行）、prompt、model-extension、bash-persistence。
- **17 个 per-issue 回归测试**：以 issue 编号命名（1717-4167），每个对应一个已修复 bug，放在 `test/suite/regressions/`。
- `packages/ai/test/`：41 文件，覆盖 Anthropic（12 文件）、OpenAI（8 文件）、Bedrock（4 文件）、Google（3 文件）、Mistral/Fireworks/Together/OpenRouter 等 provider 适配 + stream/token/cache/abort/validation。
- `packages/agent/test/`：10 文件，覆盖 agent loop、tool calling、harness 框架、compaction、session、skills。
- `packages/coding-agent/test/`：160 文件，除 suite 测试外，覆盖工具执行、编辑工具、session 状态、config/settings、交互模式、compaction、扩展系统、RPC、SDK、CLI、git、image 处理等。
- `packages/tui/test/`：22 文件，覆盖 input/editor/autocomplete/markdown/keybindings/select-list/overlay/render/regression。
- Supply-chain/release：pinned direct deps、shrinkwrap generation、browser smoke、local release isolated install。

### 判断

Pi 的评测体系是四个项目中最”工程导向”的：FauxProvider 的 LLM 模拟能力远超简单 mock，suite 测试直接在真实 AgentSession 中验证行为，17 个 per-issue 回归测试确保修复不再复发，test.sh 的凭据隔离最为彻底。但它缺少 task-level eval scenario 和真实模型的 live eval lane，分析脚本也未与 CI 集成。

### 建议补齐

- 在 `packages/coding-agent/` 下增加 `eval/` 目录，用 FauxProvider + 固定 coding task 做可复现的任务级评测。
- 增加 live eval lane（可选 real provider），与 FauxProvider 测试分离。
- 把 `scripts/` 下的分析脚本与 CI 集成，自动分析 session 日志生成统计报告。
- 增加性能基准测试（启动时间、命令响应延迟）。

### 实现细节

Pi 的评测核心是 **FauxProvider + suite harness**。

关键代码：

- `packages/ai/src/providers/faux.ts` — FauxProvider 完整实现
- `packages/ai/test/faux-provider.test.ts` — 20 个测试验证 FauxProvider 全部能力
- `packages/coding-agent/test/suite/harness.ts` — Suite 测试 harness（`createHarness()`）
- `packages/coding-agent/test/suite/agent-session-runtime.test.ts` — 运行时测试（596 行）
- `packages/coding-agent/test/suite/agent-session-compaction.test.ts` — 压缩测试（407 行）
- `packages/coding-agent/test/suite/agent-session-queue.test.ts` — 队列测试（422 行）
- `packages/coding-agent/test/suite/regressions/` — 17 个 per-issue 回归测试

#### FauxProvider 架构

```typescript
const faux = registerFauxProvider({
  models: [{ id: “faux-model”, name: “Faux Model”, reasoning: false }],
});
faux.setResponses([
  fauxAssistantMessage(“Let me think...”),
  fauxAssistantMessage([fauxToolCall(“read_file”, { path: “foo.txt” })], { stopReason: “toolUse” }),
  fauxAssistantMessage(“Here's the content”),
]);
```

FauxProvider 支持的能力：

| 能力 | 实现 |
|---|---|
| 文本/thinking/toolCall 构造 | `fauxText()` / `fauxThinking()` / `fauxToolCall()` |
| Streaming 事件序列 | `start → thinking_start/delta/end → text_start/delta/end → toolcall_start/delta/end → done` |
| Prompt caching 模拟 | per-sessionId cache read/write |
| Token 估算 | `ceil(text.length / 4)` |
| AbortController | 支持在开始前/中途中止 stream |
| 自定义速率 | `tokensPerSecond` 控制模拟发送速度 |
| 响应队列 | `setResponses` / `appendResponses`，耗尽后返回 error |
| 异步工厂 | `(context, options, state, model) => response` |

相比 nanobot 的 `MagicMock(spec=LLMProvider)`，FauxProvider 提供了**完整的 LLM 行为模拟**（含 streaming、cache、abort、token 估算），使得 suite 测试可以在不依赖真实 API 的情况下覆盖完整的 agent 运行时路径。

#### Suite Harness 使用模式

```typescript
const harness = await createHarness({ tools, settings });
harness.setResponses([fauxAssistantMessage(“done”)]);
await harness.session.submitMessage(“list files”);

expect(harness.eventsOfType(“done”)).toHaveLength(1);
expect(getUserTexts(harness)).toContain(“list files”);

harness.cleanup();
```

这种模式的优势是测试运行在**完整的 AgentSession 实例**之上，而非 mock/stub——事件派发、消息编排、状态管理、tool execution 都经过真实代码路径，但又通过 FauxProvider 避免了真实 API 调用。

## hermes-agent

### 当前评测入口

- Python 主测试：`/Users/liyazhou/Repo/repo_ai/hermes-agent/scripts/run_tests.sh`
  - 每个 test file 独立 subprocess 执行，避免模块级状态污染。
  - 固定 `TZ=UTC`、`LANG=C.UTF-8`、`PYTHONHASHSEED=0`。
  - 清空环境变量，避免凭据泄漏到测试。
  - 支持 `scripts/run_tests.sh tests/agent/`、单文件、`--` 透传 pytest 参数。
- Stress：`/Users/liyazhou/Repo/repo_ai/hermes-agent/tests/stress/README.md`
  - 不由 `scripts/run_tests.sh` 默认执行。
  - 手动运行 `python -m pytest tests/stress/ -v -s`。
- Browser eval benchmark：`/Users/liyazhou/Repo/repo_ai/hermes-agent/scripts/benchmark_browser_eval.py`
  - 对比 supervisor WebSocket Runtime.evaluate 和 agent-browser subprocess eval 的 latency。
- TUI：`/Users/liyazhou/Repo/repo_ai/hermes-agent/ui-tui/package.json`
  - `npm test` -> `vitest run`
  - `type-check`、`lint`、`build`
- Web：`/Users/liyazhou/Repo/repo_ai/hermes-agent/web/package.json`
  - 有 `build`、`lint`、`dev`、`preview`，未看到 test 脚本。

### 当前覆盖

- Python tests 覆盖：ACP、ACP adapter、agent providers、LSP、CLI、transport、skills、memory、compression、prompt/cache、file safety、credential pool、image/vision/TTS/transcription、gateway/platform 相关行为。
- Stress 覆盖：
  - concurrency：多 worker claim/complete/block/unblock/archive，不变量检查。
  - subprocess e2e：真实 Python subprocess worker、heartbeat、dead PID 检测。
  - property fuzzing：随机操作序列和不变量检查。
  - atypical scenarios：unicode、RTL、1MB 字符串、SQL injection、cycle、clock skew、特殊 `HERMES_HOME`、dashboard REST 异常 JSON 等。
  - benchmarks：100/1k/10k tasks 下 dispatch、recompute_ready、list_tasks、build_worker_context 等延迟，并保存 JSON。
- Browser eval benchmark 覆盖：浏览器 supervisor path 性能，不是 pytest gate，适合 PR 描述或性能回归确认。

### 判断

`hermes-agent` 的测试 runner 很重视隔离性和确定性，这是它的优势。stress suite 也比较成熟。但它的“eval”资产更分散：有 benchmark、有 stress、有大量行为测试，但缺少一个统一的 agent scenario 目录来表达“任务级完成质量”。

### 建议补齐

- 增加 `eval/scenarios/`：覆盖 skills self-improvement、memory recall、cron、gateway thread continuity、terminal backend、subagent、MCP/ACP、多模型 fallback。
- 为 batch trajectory generation 建一个回归子集：固定任务、固定 seed/mock tools、输出 transcript JSONL 和评分。
- Web 前端补 `test` 脚本或至少 smoke test：dashboard route、terminal pane、QR/setup、session UI。
- Stress benchmark 的 JSON 输出建议纳入基线比较，形成 `stress:bench:check`。

### 实现细节

`hermes-agent` 的评测实现重点是“隔离性”和“压力/性能”。

关键代码：

- `scripts/run_tests.sh`
- `scripts/run_tests_parallel.py`
- `tests/stress/README.md`
- `tests/stress/test_benchmarks.py`
- `scripts/benchmark_browser_eval.py`

`scripts/run_tests.sh` 做了几个工程上很重要的选择：

- 不直接跑裸 `pytest`，而是走 canonical runner。
- 每个 test file 都在新的 `python -m pytest <file>` subprocess 里执行。
- 不用 pytest-xdist 的持久 worker，避免跨文件模块级状态泄漏。
- 固定 `TZ=UTC`、`LANG=C.UTF-8`、`PYTHONHASHSEED=0`。
- 用 `env -i` 清空环境，避免真实凭据泄漏进测试。
- 默认跳过 e2e/integration/docker，把它们交给专门 lane。

`tests/stress` 则覆盖长跑和极端情况：

- 多 worker 并发 claim/complete，检查无 double-claim、无 orphan run。
- reclaimer 抢占长任务，验证 CAS guard。
- subprocess e2e，检查真实 worker heartbeat 和 dead PID。
- property fuzzing，随机操作序列后检查不变量。
- atypical scenarios，覆盖 unicode、RTL、SQL injection、clock skew、特殊 home path、异常 JSON。
- benchmark，输出 dispatch/list/recompute/build context 等延迟 JSON。

`scripts/benchmark_browser_eval.py` 是一个很典型的局部性能评测：

- 启动 headless Chrome + CDP。
- 对比 supervisor WebSocket `Runtime.evaluate` 和 agent-browser subprocess eval。
- 输出 mean、median、min、max 和 speedup。

这类 micro-benchmark 不应该混进 PR quick gate，但适合性能 PR、架构改造和 release 前确认。

## 推荐的统一落地结构

如果要让四个项目后续能横向比较，可以逐步补成下面结构：

```text
<project>/
  docs/evaluation.md
  eval/
    scenarios/
      *.md
    runner.*
    report-schema.json
    baselines/
```

`docs/evaluation.md` 建议固定包含：

- 项目评测目标
- 本地 quick gate
- CI gate
- live/manual gate
- release gate
- scenario 列表和分级
- 环境变量/凭据要求
- 输出报告格式
- 当前 known gaps

## 优先级建议

1. 先把 `openclaw` 的 QA scenario/reporting 作为模板，不急着重写。
2. 给 `nanobot` 和 `hermes-agent` 各补一个最小 `eval/scenarios/`，先覆盖 8-12 个高价值多轮任务。
3. 给 `pi` 把 coding-agent 的固定任务评测抽出来，和 provider live eval 分离。
4. 建一个统一 report schema，至少包含：`project`、`scenario`、`lane`、`provider`、`model`、`status`、`duration_ms`、`cost_estimate`、`failure_reason`、`artifact_path`。
5. 每个项目保留三层命令：`quick`、`full`、`live/nightly`，避免所有评测都混进 PR gate。

## 参考资料

- OpenAI Evaluation best practices：<https://developers.openai.com/api/docs/guides/evaluation-best-practices>
- OpenAI Agent evals：<https://developers.openai.com/api/docs/guides/agent-evals>
- OpenAI Evals GitHub：<https://github.com/openai/evals>
- LangSmith Evaluation：<https://www.langchain.com/langsmith/evaluation>
- DeepEval Tool Correctness：<https://deepeval.com/docs/metrics-tool-correctness>
- SWE-bench Verified：<https://www.swebench.com/verified.html>
- tau-bench paper：<https://arxiv.org/abs/2406.12045>
