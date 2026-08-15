# OpenClaw Agent 评测方案与实现分析

资料范围：

- 本地仓库：`/Users/liyazhou/Repo/repo_ai/openclaw`
- 远程仓库：`https://github.com/openclaw/openclaw.git`
- 在线文档：
  - <https://docs.openclaw.ai/help/testing>
  - <https://docs.openclaw.ai/concepts/qa-e2e-automation>
  - <https://docs.openclaw.ai/channels/qa-channel>
  - <https://docs.openclaw.ai/concepts/qa-matrix>
- 通用 Agent eval 参考：
  - <https://developers.openai.com/api/docs/guides/evaluation-best-practices>
  - <https://developers.openai.com/api/docs/guides/agent-evals>
  - <https://www.swebench.com/verified.html>
  - <https://arxiv.org/abs/2406.12045>

## 结论先行

OpenClaw 的评测体系不是单一测试套件，而是一个分层 QA/eval 平台：

1. 常规工程 gate：unit、e2e、coverage、contract、lint、build。
2. Docker/release e2e：安装、升级、插件、onboard、Open WebUI、MCP、发布包路径。
3. live model/provider eval：真实模型、真实凭据、真实 gateway、真实插件工具。
4. QA Lab scenario eval：repo-backed markdown scenarios、synthetic `qa-channel`、mock/live provider modes。
5. live transport lanes：Matrix、Telegram、Discord、Slack 等真实通道。
6. parity/reporting：candidate vs baseline、runtime pair、tool-call 证据、fake success、token efficiency。
7. observability/security eval：OTel、Prometheus、secret redaction、credential broker、sandbox/approval。

它的核心特点是：**确定性断言优先，真实模型/真实通道放到专门 lane，scenario 用人可读 Markdown 管理，运行结果用 JSON summary 和 Markdown report 留痕。**

这比“跑一批 prompt 看回答好不好”成熟得多，更接近生产级 Agent eval。

## 这篇文档的阅读路线

如果只是想快速理解 OpenClaw 的评测体系，建议按这个顺序读：

1. 先看“命令分层”，建立整体地图。
2. 再看“QA Lab 架构”和“Scenario 设计”，理解它为什么不是普通单测。
3. 然后看“Suite Summary 与报告”“Agentic Parity”，理解结果如何被机器消费和对比。
4. 最后看“可复用设计模式”和“潜在改进点”，判断怎么迁移到其他 Agent 项目。

如果你要真正复用这套方案，最重要的是三件事：

- 用 deterministic provider 固定模型行为。
- 用 transport adapter 把 Agent 放进接近真实产品的交互环境。
- 用 JSON summary 固化每次运行的 scenario、provider、model、runtime、artifact 和指标。

## 命令分层

在线测试文档把 OpenClaw 的测试分成 Vitest suites、Docker runners、live suites 和 QA-specific runners。结合本地 `package.json`，可以整理为：

| 层级 | 入口 | 作用 |
|---|---|---|
| 本地快速回归 | `pnpm test`、`pnpm test:unit`、`pnpm test:unit:fast` | 常规代码行为、unit、gateway、runtime、plugin/channel 单元回归 |
| 类型/构建/静态检查 | `pnpm build`、`pnpm lint`、`pnpm check:*` | TS build、oxlint、边界规则、依赖和文档检查 |
| 覆盖率 | `pnpm test:coverage` | unit coverage |
| E2E | `pnpm test:e2e` | gateway e2e + UI e2e |
| Live | `pnpm test:live`、`pnpm test:live:*` | 真实 provider/model、gateway、media、Codex harness 等 |
| Docker E2E | `pnpm test:docker:*` | 安装、升级、release journey、插件生命周期、OpenAI tools、Open WebUI、MCP 等 |
| QA Lab | `pnpm openclaw qa suite`、`pnpm qa:e2e` | repo-backed scenarios，synthetic channel，mock/live provider |
| QA UI | `pnpm qa:lab:up`、`pnpm qa:lab:ui` | 两栏 QA 操作站点：Gateway dashboard + QA Lab transcript |
| QA coverage | `pnpm openclaw qa coverage` | scenario coverage inventory 和搜索 |
| Observability | `pnpm qa:otel:smoke`、`pnpm qa:prometheus:smoke` | trace/metrics/logs 形状、敏感内容不泄漏 |
| 性能 | `pnpm test:startup:bench`、`pnpm test:startup:gateway`、`pnpm test:restart:gateway` | CLI/gateway 启动和重启性能 |

在线文档还明确说：大多数日常开发跑 `pnpm build && pnpm check && pnpm check:test-types && pnpm test`，需要更强信心时跑 coverage/e2e，真实 provider/model 问题才进入 live suite。

### 常见工作流

按使用场景可以进一步压缩成四条路径：

| 目标 | 推荐命令 | 说明 |
|---|---|---|
| 本地改代码后的基础信心 | `pnpm test` | 常规回归，不碰真实模型和外部通道 |
| 改 gateway/plugin/channel 共享契约 | `pnpm test:contracts`、`pnpm test:e2e` | 验证接口形状和端到端 wiring |
| 改 Agent 行为或 QA scenario | `pnpm openclaw qa suite --provider-mode mock-openai --scenario <id>` | 确定性、可复现，适合开发迭代 |
| 验证真实 provider/channel | `pnpm test:live` 或 `pnpm openclaw qa <telegram|discord|slack|matrix>` | 需要凭据，适合 nightly/release/manual |

一个较实用的迭代顺序是：

```bash
pnpm openclaw qa coverage --match approval
pnpm openclaw qa suite --provider-mode mock-openai --scenario approval-turn-tool-followthrough
pnpm openclaw qa coverage --tools --summary .artifacts/qa-e2e/<run>/qa-suite-summary.json
```

第一步找最小场景，第二步跑确定性 scenario，第三步把运行 summary 叠加到 tool coverage 上检查工具证据。

## QA Lab 架构

本地核心目录：

```text
extensions/qa-lab/
  src/
    suite.ts
    suite-summary.ts
    scenario-catalog.ts
    scenario-flow-runner.ts
    scenario-runtime-api.ts
    suite-runtime-flow.ts
    suite-runtime-agent.ts
    suite-runtime-gateway.ts
    qa-transport-registry.ts
    coverage-report.ts
    tool-coverage-report.ts
    agentic-parity-report.ts
    runtime-parity.ts
    token-efficiency-report.ts
    providers/
qa/
  README.md
  scenarios/
```

在线 QA overview 对组件的描述也和本地代码一致：

- `extensions/qa-channel`：synthetic message channel，模拟 DM、channel、thread、reaction、edit、delete。
- `extensions/qa-lab`：debugger UI 和 QA bus，用来观察 transcript、注入 inbound messages、导出 Markdown report。
- `extensions/qa-matrix`：live transport adapter，真实 Matrix lane。
- `qa/`：repo-backed kickoff task 和 baseline scenarios。
- Mantis：用于真实 transports、browser screenshots、VM state、PR evidence 的 before/after live verification。

### 运行链路

`qa suite` 大致链路：

1. 读取 `qa/scenarios/index.md` 和 `qa/scenarios/**/*.md`。
2. 从 Markdown fence 中解析 `qa-pack`、`qa-scenario`、`qa-flow`。
3. 用 `zod` 校验 scenario metadata 和 flow schema。
4. 根据 CLI 参数选择 scenario、provider mode、transport、model、concurrency。
5. 启动 QA Lab server、provider server、gateway child。
6. 创建 transport adapter，默认 synthetic `qa-channel`，也可走 live transport。
7. 对每个 scenario 构造 flow API。
8. 执行 flow steps：发消息、等待 gateway、等待 outbound、检查 state、断言 tool call 或 message。
9. 生成 Markdown report 和 `qa-suite-summary.json`。
10. 如果有 runtime pair 或 parity 参数，再做 parity/token efficiency report。

`suite.ts` 里可以看到这些关键模块：

- `startQaGatewayChild`
- `startQaProviderServer`
- `createQaTransportAdapter`
- `readQaBootstrapScenarioCatalog`
- `runScenarioFlow`
- `createQaSuiteScenarioFlowApi`
- `waitForGatewayHealthy`
- `waitForTransportReady`
- `captureRuntimeParityCell`

这说明 QA Lab 并不是 mock 几个函数，而是启动真实 gateway lane，在可控 provider/transport 下跑完整 Agent loop。

### 源码索引

读源码时可以按下面的索引定位：

| 关注点 | 本地文件 | 作用 |
|---|---|---|
| CLI 命令分发 | `extensions/qa-lab/src/cli.runtime.ts` | `qa suite`、`qa coverage`、`qa parity-report`、`qa jsonl-replay` 等命令入口 |
| Suite 主流程 | `extensions/qa-lab/src/suite.ts` | 启动 lab/provider/gateway、选择 scenario、运行 flow、写报告 |
| 运行规划 | `extensions/qa-lab/src/suite-planning.ts` | scenario 选择、并发、输出目录、插件收集、gateway config patch |
| Scenario 读取 | `extensions/qa-lab/src/scenario-catalog.ts` | 解析 Markdown fenced YAML、schema 校验、scenario pack 缓存 |
| Flow DSL | `extensions/qa-lab/src/scenario-flow-runner.ts` | 执行 `call/set/assert/if/forEach/try` |
| Flow API | `extensions/qa-lab/src/suite-runtime-flow.ts` | 给 YAML flow 暴露 `runAgentPrompt`、`waitForCondition` 等能力 |
| Transport registry | `extensions/qa-lab/src/qa-transport-registry.ts` | 选择 synthetic 或 live transport adapter |
| Provider modes | `extensions/qa-lab/src/providers/index.ts` | `mock-openai`、`aimock`、`live-frontier` |
| Summary schema | `extensions/qa-lab/src/suite-summary.ts` | `qa-suite-summary.json` 类型和失败计数读取 |
| Coverage | `extensions/qa-lab/src/coverage-report.ts`、`tool-coverage-report.ts` | scenario coverage 和运行时 tool coverage |
| Parity | `extensions/qa-lab/src/agentic-parity-report.ts`、`runtime-parity.ts` | candidate/baseline 和 runtime-pair 对比 |
| Observability | `scripts/qa-otel-smoke.ts`、`qa/scenarios/runtime/otel-trace-smoke.md` | OTel/Prometheus 诊断信号评测 |

## Scenario 设计

一个 scenario 是 Markdown 文件，包含两段 fenced YAML：

```yaml
qa-scenario:
  id: approval-turn-tool-followthrough
  title: Approval turn tool followthrough
  surface: harness
  coverage:
    primary:
      - runtime.approvals
    secondary:
      - tools.followthrough
  objective: ...
  successCriteria:
    - ...
  docsRefs:
    - ...
  codeRefs:
    - ...
  execution:
    kind: flow
    config:
      ...
```

```yaml
qa-flow:
  steps:
    - name: turns short approval into a real file read
      actions:
        - call: waitForGatewayHealthy
        - call: reset
        - call: runAgentPrompt
        - set: beforeApprovalCursor
        - call: waitForCondition
```

本地 `scenario-catalog.ts` 对 scenario 字段做了明确 schema：

- `id`
- `title`
- `surface`
- `category`
- `runtimeParityTier`
- `coverage.primary`
- `coverage.secondary`
- `surfaces`
- `risk`
- `capabilities`
- `lane`
- `objective`
- `successCriteria`
- `plugins`
- `gatewayConfigPatch`
- `gatewayRuntime`
- `docsRefs`
- `codeRefs`
- `execution`

这套设计的优点：

- Markdown 对人友好，适合评测任务长期维护。
- YAML 对机器友好，适合自动执行。
- `objective` 和 `successCriteria` 把“为什么测”写清楚。
- `coverage` 能把 scenario 映射到能力矩阵。
- `docsRefs`、`codeRefs` 能让失败回溯到相关文档和实现。
- `risk`、`runtimeParityTier` 能做 lane 分级。

## Flow Runner DSL

`scenario-flow-runner.ts` 实现了一个轻量 DSL。支持动作：

| 动作 | 作用 |
|---|---|
| `call` | 调用 flow API 中的函数，例如 `runAgentPrompt`、`waitForOutboundMessage` |
| `set` | 将表达式结果保存到变量 |
| `assert` | 执行表达式断言 |
| `throw` | 主动抛错 |
| `if` | 条件分支 |
| `forEach` | 遍历 |
| `try/catch/finally` | 容错和清理 |
| `detailsExpr` | 生成 step details，写入 report |

DSL 的表达式通过 `AsyncFunction` 运行，并把 `api`、`vars`、scenario config、transport state 放进上下文。

这有两个直接收益：

- scenario 作者不用写 TypeScript 测试文件，只要写 YAML flow。
- flow 仍能调用真实 runtime API，断言真实 state，而不是只检查最终文本。

风险也很明确：

- 表达式执行能力很强，必须只信任仓库内 scenario。
- 复杂 YAML flow 可读性会下降，需要保持 scenario 粒度小。
- 断言太依赖文本关键词时会脆弱，应该尽量用 state/tool-call evidence。

### Scenario 作者 checklist

新增或修改 scenario 时，建议按这个 checklist 检查：

- `id` 使用稳定、短小、可搜索的 kebab-case。
- `objective` 明确说明要防哪类回归，而不是只描述操作步骤。
- `successCriteria` 至少包含一个可机器断言的结果。
- `coverage.primary` 必填，且用行为维度命名，例如 `runtime.approvals`，不要直接复制 scenario 标题。
- 如果只是顺带覆盖某能力，放到 `coverage.secondary`。
- `docsRefs` 和 `codeRefs` 指向真实维护入口，方便失败后定位 owner。
- 需要插件时写 `plugins`，不要在 flow 里隐式假设插件已启用。
- 需要修改 gateway 配置时用 `gatewayConfigPatch`，这样 suite planner 可以决定是否隔离 worker。
- live-only 行为用 `runtimeParityTier: live-only` 或 provider requirement，不要污染默认 mock lane。
- flow 断言优先检查 state、tool call、artifact、message metadata，其次才检查最终文本关键词。
- `detailsExpr` 返回失败排查有价值的内容，例如实际 outbound text、tool payload、状态快照摘要。

## 一个典型 scenario：approval followthrough

文件：

`qa/scenarios/runtime/approval-turn-tool-followthrough.md`

目标：验证用户短确认 “ok do it” 后，Agent 是否真的继续执行工具调用，而不是只输出假进度。

流程：

1. 等 gateway healthy。
2. reset transport state。
3. 第一轮 prompt：要求 Agent 先别用工具，只说准备读哪个文件。
4. 记录当前 message cursor。
5. 第二轮 prompt：`ok do it. read QA_KICKOFF_TASK.md now...`
6. 等待 outbound message。
7. 检查回复包含 `qa`、`mission`、`testing`、`repo`、`worked`、`failed`、`blocked`、`chat flows` 等关键词。
8. 将 outbound text 写入 step details。

它测的是 Agent 产品里非常实际的失败模式：

- approval turn 后没有继续执行；
- 只说“我会去做”，但没有工具调用；
- 最终回答引用了占位进度，而非真实文件读取结果。

这个例子体现了 OpenClaw QA 的基本风格：**不是评估回答文采，而是评估多轮状态机和工具 follow-through。**

## Provider Modes

`extensions/qa-lab/src/providers/index.ts` 注册了三种 provider mode：

| Provider mode | 用途 |
|---|---|
| `mock-openai` | 默认确定性 provider，scenario-aware，适合 CI 和 release transport checks |
| `aimock` | AIMock-backed provider server，用于实验性 fixture 和 protocol-mock coverage |
| `live-frontier` | 真实 frontier model/provider，用于 live eval |

默认：

- `DEFAULT_QA_PROVIDER_MODE = "mock-openai"`
- `DEFAULT_QA_LIVE_PROVIDER_MODE = "live-frontier"`

这个分层很重要：

- PR/CI 需要确定性，优先 `mock-openai`。
- 协议兼容性和 fixture 覆盖可以用 `aimock`。
- 模型能力和真实 provider 兼容必须用 `live-frontier`，但要进入 nightly/manual/release lane。

这符合通用 Agent eval 最佳实践：先把环境和期望行为固定住，再用 live lane 观察真实模型变化。

## Transport 设计

OpenClaw 评测的一个核心难点是它不是纯 CLI Agent，而是 multi-channel gateway。单纯调用 API 无法证明 Slack/Discord/Telegram/Matrix 行为正确。

因此它分两类 transport：

### Synthetic transport：qa-channel

`qa-channel` 是合成消息通道，能模拟：

- DM
- channel
- thread
- reaction
- edit
- delete
- outbound reply
- channel state

它适合跑 repo-backed scenarios，因为可控、稳定、CI 友好。

### Live transport lanes

在线 QA overview 提到：

- Matrix：disposable Tuwunel homeserver，临时 driver/SUT/observer users。
- Telegram、Discord、Slack：真实私有 channel，两 bot 结构。
- Mantis：真实 transport、browser screenshots、VM/VNC、before/after bug verification。

这些 lane 用来证明 unit test 和 synthetic channel 不能证明的行为：

- mention gating
- allowlist/block
- top-level reply
- threaded reply
- restart replay dedupe
- media handling
- approval metadata delivery
- E2EE bootstrap/recovery
- native command registration

这里的架构判断很务实：**synthetic channel 覆盖产品行为，live transport 覆盖真实平台差异。**

## Coverage Inventory

`coverage-report.ts` 负责把 scenario metadata 汇总为 coverage inventory。

它统计：

- scenario count
- coverage id count
- primary coverage id count
- secondary coverage id count
- missing coverage
- overlapping coverage
- by theme
- by surface
- scenario packs
- live transport lane summaries

`pnpm openclaw qa coverage --match <query>` 可以搜索：

- scenario id
- title
- surface
- coverage id
- docs refs
- code refs
- plugins
- provider requirements

这解决了一个实际问题：代码改动后，开发者不一定知道该跑哪个 QA scenario。coverage search 可以从文件路径、能力名、插件名倒查最小 scenario 集合。

## Suite Summary 与报告

`suite-summary.ts` 定义了 `qa-suite-summary.json` 的核心结构：

```ts
type QaSuiteSummaryJson = {
  scenarios: Array<{
    name: string;
    status: "pass" | "fail";
    steps: unknown[];
    details?: string;
    runtimeParity?: RuntimeParityResult;
  }>;
  counts: {
    total: number;
    passed: number;
    failed: number;
  };
  metrics?: {
    wallMs: number;
    gatewayProcessCpuMs?: number | null;
    gatewayCpuCoreRatio?: number | null;
    gatewayProcessRssStartBytes?: number | null;
    gatewayProcessRssEndBytes?: number | null;
    gatewayProcessRssPeakBytes?: number | null;
    gatewayHeapSnapshots?: Array<...>;
  };
  run: {
    startedAt: string;
    finishedAt: string;
    providerMode: QaProviderMode;
    primaryModel: string;
    primaryProvider: string | null;
    alternateModel: string;
    fastMode: boolean;
    concurrency: number;
    scenarioIds: string[] | null;
    runtimePair?: [RuntimeId, RuntimeId] | null;
  };
};
```

这个 summary 设计很关键，因为它把评测结果从“日志”升级成“可比较数据”：

- 能统计 pass/fail。
- 能比较不同 provider/model。
- 能定位是否 fast mode、并发数、scenario list 不一致。
- 能做 CPU/RSS/heap 回归分析。
- 能给 parity report 和 token efficiency report 作为输入。

Markdown report 由 `report.ts` / plugin-sdk `qa-runtime` 渲染，适合人工阅读；JSON summary 适合 CI 和后处理。

### Artifact 落点

默认输出目录由 `suite-planning.ts` 决定：

```text
.artifacts/qa-e2e/suite-<timestamp>/
  qa-suite-report.md
  qa-suite-summary.json
  scenarios/
    <scenario-id>/
      qa-suite-report.md
      qa-suite-summary.json
  artifacts/
    gateway-runtime/
    gateway-heap-snapshots/
```

实际是否出现 `scenarios/<id>/`、heap snapshot、gateway runtime copy，取决于并发隔离、失败路径和运行参数。CLI 会打印：

```text
QA suite report: <path>
QA suite summary: <path>
```

Parity 相关命令会生成：

```text
qa-agentic-parity-report.md
qa-agentic-parity-summary.json
qa-runtime-parity-report.md
qa-runtime-parity-summary.json
qa-runtime-token-efficiency-report.md
qa-runtime-token-efficiency-summary.json
```

这部分值得在文档里单独写出来，因为 artifact 路径决定了后续 dashboard、CI artifact 上传、PR comment 和失败排查怎么接。

## Agentic Parity

`agentic-parity-report.ts` 是 OpenClaw 评测体系里最有价值的部分之一。

它把两个 `qa-suite-summary.json` 做 candidate/baseline 对比，并计算：

- total scenarios
- passed scenarios
- failed scenarios
- completion rate
- unintended stop count/rate
- valid tool call count/rate
- fake success count
- scenario coverage mismatch
- required parity scenario missing/fail

它还针对 Agent 常见假阳性做了文本模式检测：

- `incomplete turn`
- `timed out`
- `stopped`
- `blocked`
- `abandoned`
- `failed to`
- `could not`
- `unable to`
- `error occurred`

但它没有天真地把“没有工具证据”直接算 fake success，因为 passing scenario 的 details 往往是模型最终话术，不包含底层工具证据。代码注释明确说明：工具证据应该由每个 scenario 的 `/debug/requests` 或 flow assertions 来保证。

这是一个很成熟的评测判断：**全局 parity report 不应该替代 scenario 内部的确定性工具断言。**

## Runtime Parity 与 Token Efficiency

OpenClaw 不只比较不同模型，也比较不同 runtime。`runtime-parity.ts` 和 `agentic-parity-report.ts` 支持 runtime pair，例如 Codex vs OpenClaw runtime。

Runtime parity report 关注：

- 每个 scenario 两边状态：pass/fail/missing。
- drift 类型。
- 两边 tool calls。
- 两边 token usage。
- 是否缺少 live assistant-message usage。

这类评测适合回答：

- 新 runtime 是否行为等价？
- 是否只是最终回答相似，但工具调用路径变差？
- 是否 token 成本显著变高？
- 是否某些 scenario 只在某 runtime 缺失？

## Observability Eval

在线 QA overview 明确列出 observability smokes：

- `pnpm qa:otel:smoke`
- `pnpm qa:otel:collector-smoke`
- `pnpm qa:prometheus:smoke`
- `pnpm qa:observability:smoke`
- `pnpm qa:observability:collector-smoke`

这些不是普通“服务能启动”测试，而是检查诊断信号质量：

- 是否导出关键 trace spans：`openclaw.run`、`openclaw.harness.run`、model-call span、context assembled、message delivery。
- 成功 turn 不应导出 `StreamAbandoned`。
- raw diagnostic IDs 和 `openclaw.content.*` 不应进入 trace。
- prompt sentinel、response sentinel、QA session key 不应出现在 raw OTLP payload。
- Prometheus 未认证 scrape 应拒绝，认证 scrape 应包含关键 metric families，但不泄漏 prompt/response/token/local path。

这说明 OpenClaw 把 observability 也当成产品契约来评测，而不只是后端埋点。

## Docker 与 Release Lanes

OpenClaw 的 Docker E2E 覆盖大量真实用户旅程：

- 安装脚本 smoke/e2e。
- npm package onboard。
- channel agent onboard。
- plugin lifecycle。
- plugin update。
- package upgrade survivor。
- Open WebUI。
- OpenAI chat tools/image/web search。
- MCP channels。
- bundled plugin install/uninstall。
- session runtime context。
- QR import。
- release user journey。

这些 lane 的价值是验证“源代码测试通过”之外的东西：

- 打包产物是否包含正确文件；
- dist/plugin-sdk subpath 是否可用；
- on-demand dependency 是否能安装；
- 用户升级后配置/插件/会话是否保留；
- Docker 镜像里真实 CLI 路径是否正常；
- 不同 auth/profile mount 策略是否正确。

对 Agent 产品来说，这些 release lanes 往往比单测更接近真实事故来源。

## 与通用 Agent Eval 方法的对应

OpenAI Agent eval 文档强调 agent eval 不只看最终 output，还要评估工具选择、参数精度、handoff、trajectory 等。OpenClaw 的实现基本对应：

| 通用 Agent eval 问题 | OpenClaw 实现 |
|---|---|
| 任务是否完成 | scenario pass/fail、success criteria、state assertions |
| 工具是否选对 | flow assertions、debug requests、tool coverage |
| 参数是否正确 | tool call payload extraction、scenario-specific assertions |
| 是否假装完成 | fake success patterns + scenario 内工具证据 |
| 是否中途停止 | unintended stop patterns、timeout、failure details |
| 多轮是否持续 | approval followthrough、thread follow-up、restart recovery |
| 上下文/记忆是否正确 | memory recall、thread memory isolation、session memory ranking |
| 不同 runtime 是否等价 | runtime parity |
| 真实平台是否工作 | Matrix/Telegram/Discord/Slack live lanes |
| 成本是否可控 | token efficiency、usage metrics |
| 发布包是否可用 | Docker/package acceptance/release lanes |

它也和 SWE-bench / tau-bench 的方向一致：

- SWE-bench 用真实 issue + tests 判断 coding agent patch 是否有效。
- tau-bench 用模拟用户和工具 API 交互，最终检查环境状态。
- OpenClaw 用 channel-shaped scenarios、tool/runtime state、gateway artifacts 判断 Agent 行为是否正确。

三者共同点是：**最终文本不是唯一真相，环境状态和执行轨迹才是主要证据。**

## 可复用设计模式

如果要把 OpenClaw 的方案迁移到其他 Agent 项目，可以抽象成：

```text
eval/
  scenarios/
    *.md              # 人可读任务 + YAML metadata + YAML flow
  runner/
    scenario-catalog  # 读取和校验 scenario
    flow-runner       # 执行 DSL
    provider-server   # mock/live provider adapter
    transport         # CLI/API/channel adapter
    report            # markdown + JSON
    parity            # candidate/baseline comparison
```

关键工程原则：

1. Scenario 必须写清 objective 和 success criteria。
2. 所有 scenario 都要有 coverage id。
3. 默认 provider 必须确定性。
4. live provider 必须隔离到 nightly/manual/release lane。
5. 结果必须同时输出 Markdown 和 JSON。
6. 评测必须保存 transcript/tool calls/artifacts。
7. LLM judge 只能补充开放式质量判断，不能替代状态断言。
8. 真实 channel 必须有独立 live transport lane。
9. 评测报告要能做 candidate/baseline 对比。
10. 性能、token、CPU/RSS 要和功能结果放在同一个 summary 里。

## 潜在改进点

OpenClaw 已经很完整，但还有一些可以继续强化的地方：

- Scenario DSL 文档化：把 `call/set/assert/if/forEach/try` 的语法和最佳实践写成 authoring guide。
- Report schema 固化：给 `qa-suite-summary.json` 加 JSON Schema，方便外部 dashboard 消费。
- Artifact index：每次 run 输出统一 `index.json`，链接 summary、markdown、transcript、gateway logs、heap snapshots、screenshots。
- Flake tracking：记录 scenario 最近 N 次 pass/fail，区分功能失败和环境 flaky。
- Cost budget：对 live-frontier lane 增加 per-scenario cost/token budget。
- Dataset versioning：scenario pack 加版本号和变更记录，避免 candidate/baseline 使用不同 scenario set。
- Judge calibration：如果加入 LLM judge，应保留 rubric、few-shot、judge model、temperature、原始判分 JSON。
- Failure taxonomy：把失败分成 timeout、transport、provider、tool assertion、final answer、artifact missing、infra setup。

## 当前分析的边界

这篇文章主要基于本地源码和 OpenClaw 官方 docs。它没有做三件事：

- 没有实际运行 `qa suite`，所以没有采样真实 artifact 内容和失败日志。
- 没有拉取远程 GitHub 最新分支逐 commit 对比；远程仓库 URL 已确认，但内容分析以本地 checkout 为准。
- 没有分析 GitHub Actions workflow 的完整调度图，只引用了在线文档里对 nightly/release/manual lane 的说明。

如果要把这篇文章继续升级成“可执行 runbook”，下一步应该补：

1. 实跑一个 mock scenario，贴出真实 `qa-suite-summary.json` 的关键字段。
2. 实跑 `qa coverage --json`，生成 coverage inventory 示例。
3. 实跑一次 candidate/baseline parity，用真实报告解释每个指标。
4. 画一张 QA Lab 运行时序图：CLI -> Lab server -> provider server -> gateway child -> transport -> report。

## 我对 OpenClaw 评测体系的判断

OpenClaw 的评测方案已经具备“Agent 产品级 QA 平台”的形态：

- 它不是只验证函数，而是验证 Agent 在 gateway/channel/runtime 环境中的行为。
- 它不是只依赖真实模型，而是通过 mock provider 建立确定性回归，再用 live-frontier 做真实性补充。
- 它不是只看最终回答，而是保留 scenario steps、tool-call evidence、runtime parity、CPU/RSS/token 等运行证据。
- 它不是只服务开发本地，而是覆盖 CI、nightly、release、manual operator、Mantis bug proof。

最值得学习的是它的分层思路：

**unit/e2e 保证代码正确，QA Lab 保证 Agent 行为正确，live transport 保证真实平台正确，parity/reporting 保证变更可比较。**

对其他 Agent 项目来说，最小可复制版本不是整套 Docker/Matrix/Mantis，而是：

1. Markdown scenario catalog。
2. YAML flow DSL。
3. deterministic mock provider。
4. transport adapter。
5. JSON summary + Markdown report。
6. candidate/baseline parity report。

做到这六点，就能从“测试命令列表”升级到真正的 Agent eval 体系。
