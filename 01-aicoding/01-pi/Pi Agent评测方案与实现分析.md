# Pi Agent 评测方案与实现分析

资料范围：

- 本地仓库：`/Users/liyazhou/Repo/repo_ai/pi`（`main` branch）
- 远程仓库：`https://github.com/earendil-works/pi`
- 开发指引：`AGENTS.md`

## 结论先行

Pi 的评测体系是**以 FauxProvider 为核心驱动 + AgentSession 完整运行时验证 + per-issue regression 回归覆盖**的分层架构。它不像 hermes-agent 那样关注训练数据生产（batch_runner + trajectory），也不像 nanobot 那样用 MagicMock 做细粒度的单元 mock，而是通过**在真实 AgentSession 中注入可编程的 faux provider 响应序列**，让测试既具备 mock 的确定性，又覆盖完整的 agent 运行时流程（消息编排、事件派发、错误恢复、compaction、queue 管理）。

它的核心设计特点：

1. **FauxProvider 测试框架**：`registerFauxProvider()` 提供完整 provider 模拟——支持 thinking/text/toolCall 分块构造、streaming 事件序列控制、prompt caching 模拟、token 估算、abort 测试。相比 nanobot 的 `MagicMock(spec=LLMProvider)`，FauxProvider 是 **react 级别可编程的 mock LLM**。
2. **真实 AgentSession 集成测试**：suite 测试使用完整的 `AgentSession` 实例 + FauxProvider，而非 mock session 或 runner。测试覆盖了事件派发、compaction、queue、retry、branching、tree navigation 等完整 session 行为。
3. **Per-issue 回归测试**：17 个以 issue 编号命名的回归测试（1717-4167），确保每个已修复的 bug 有可复现的测试用例。
4. **凭据安全隔离**：`test.sh` 在运行测试前备份 `auth.json`、unset 40+ 个 API key 环境变量、设置 `PI_NO_LOCAL_LLM=1`，保证测试不会意外调用真实 API。
5. **npm run check 工程管道**：biome 格式检查 + pinned-deps 版本锁定 + ts-imports 相对路径检查 + shrinkwrap 完整性 + browser-smoke 验证。
6. **分析脚本工具链**：cost/stats/edit-tool-stats/session-context/session-transcripts 等脚本，用于离线分析 session 日志。

## 评测系统总览

```
pi/
├── test.sh                               # 凭据隔离测试入口
├── pi-test.sh                            # 本地运行入口（--no-env）
├── AGENTS.md                             # 开发规则
├── package.json                          # check/test 脚本
├── scripts/
│   ├── cost.ts                           # Token 成本分析
│   ├── stats.ts                          # 会话统计
│   ├── edit-tool-stats.mjs               # 编辑工具统计
│   ├── read-tool-stats.mjs               # 读取工具统计
│   ├── session-context-stats.mjs         # Session 上下文统计
│   ├── session-transcripts.ts            # Session 日志提取
│   ├── tool-stats.ts                     # 工具使用统计
│   ├── check-browser-smoke.mjs           # Browser 冒烟
│   ├── check-pinned-deps.mjs             # 依赖锁定校验
│   ├── check-ts-relative-imports.mjs     # TS 相对路径校验
│   └── generate-coding-agent-shrinkwrap.mjs
├── packages/
│   ├── agent/            # 10 个测试文件 (vitest --run)
│   ├── ai/               # 41 个测试文件 (vitest --run)
│   ├── coding-agent/     # 160 个测试文件 (vitest --run)
│   └── tui/              # 22 个测试文件 (node --test)
```

### 测试框架选型

| Package | 运行器 | 配置 |
|---|---|---|
| agent | vitest --run | -- |
| ai | vitest --run | -- |
| coding-agent | vitest --run | -- |
| tui | node --test | 无配置文件，直接 glob |

### 命令层级

```bash
# 标准测试入口（凭据隔离）
./test.sh

# 测试子包
npm run test -w packages/agent
npm run test -w packages/ai
npm run test -w packages/coding-agent
npm run test -w packages/tui

# 工程检查
npm run check    # biome + pinned-deps + ts-imports + shrinkwrap + browser-smoke

# 单个 suite 测试
cd packages/coding-agent
node ../../node_modules/vitest/dist/cli.js --run test/suite/agent-session-runtime.test.ts
```

## 1. FauxProvider 测试基础设施

FauxProvider 是 Pi 评测体系的核心，位于 `packages/ai/src/` 中，提供了完整的可编程 LLM provider 模拟。

### 核心接口

```typescript
// packages/ai/src/index.ts
export function registerFauxProvider(options?: {
  api?: string;
  provider?: string;
  models?: FauxModelDefinition[];
  tokenSize?: { min: number; max: number };
  tokensPerSecond?: number;
}): FauxProviderRegistration
```

返回值 `FauxProviderRegistration` 提供：

```typescript
interface FauxProviderRegistration {
  setResponses(responses: FauxResponseStep[]): void;   // 设置响应序列
  appendResponses(responses: FauxResponseStep[]): void; // 追加响应
  getPendingResponseCount(): number;                     // 剩余响应数
  getModel(modelId?: string): Model<string>;             // 获取模型
  models: Model<string>[];
  state: { callCount: number };
  unregister(): void;
}
```

### 响应构造器

FauxProvider 提供四种辅助构造器，支持细粒度控制 LLM 输出：

```typescript
fauxAssistantMessage("hello world")  // 纯文本消息
fauxAssistantMessage([
  fauxThinking("think"),             // 推理块
  fauxToolCall("echo", { text: "hi" }, { id: "tool-1" }), // 工具调用
  fauxText("done"),                  // 文本块
], { stopReason: "toolUse" })       // 停止原因
```

### 能力矩阵

| 能力 | 实现 | 测试覆盖 |
|---|---|---|
| 文本响应 | `fauxAssistantMessage(content)` | basic registration test |
| Thinking + ToolCall + Text 组合 | `fauxThinking` + `fauxToolCall` + `fauxText` | helper blocks test |
| 多模型注册 | `models: [{id, name, reasoning}]` | multi-model test |
| 响应队列消费 | `setResponses` → 顺序消费 → 耗尽 error | exhausted queue test |
| 替换/追加响应 | `setResponses` / `appendResponses` | replace/append test |
| 异步工厂函数 | `(context, options, state, model) => response` | async factory test |
| 工厂抛出异常 | `throw new Error("boom")` | factory throws test |
| Token 估算 | `ceil(text.length / 4)` | token estimation test |
| Prompt caching 模拟 | per `sessionId` cache read/write | caching simulation test |
| Streaming 事件序列 | thinking_start/delta/end → text_start/delta/end → toolcall_start/delta/end | streaming event order test |
| 多 tool call streaming | 2 个 tool call 的正确事件序列 | multi tool call test |
| Error 模拟 | `stopReason: "error"` + `errorMessage` | explicit error test |
| Aborted 模拟 | `stopReason: "aborted"` + `errorMessage` | explicit aborted test |
| AbortController | 在开始前/中途中止 stream | abort test |
| 自定义 token 速率 | `tokensPerSecond` 控制发送速度 | paced abort tests |
| Provider 注销 | `unregister()` 后调用抛异常 | unregister test |

### 与 MagicMock 的对比

| 维度 | Pi FauxProvider | Nanobot MagicMock(spec=LLMProvider) |
|---|---|---|
| 抽象层级 | 完整 provider 模拟（含 streaming/token 估算/cache） | Python 接口 mock |
| 响应队列 | 支持（预设多轮响应序列） | 无（每次调用即时设置） |
| Streaming | 完整 streaming 事件序列 + abort 控制 | 无 |
| Prompt cache | 有（per-session cache read/write） | 无 |
| Token 估算 | 内置（text-length / 4） | 外部 `estimate_prompt_tokens_chain` |
| 使用场景 | 集成测试（真实 AgentSession） | 单元测试（独立 AgentRunner） |

## 2. Agent 层测试（10 个文件）

`packages/agent/test/` 包含 10 个测试文件，覆盖 Agent 核心抽象层。

| 文件 | 测试重点 |
|---|---|
| `agent.test.ts` | Agent 核心行为（状态管理、消息转换、payload/response 回调） |
| `agent-loop.test.ts` | AgentLoop 循环控制 |
| `harness/agent-harness.test.ts` | Harness 测试框架（agent 层） |
| `harness/agent-harness-stream.test.ts` | Harness streaming |
| `harness/compaction.test.ts` | Context 压缩行为 |
| `harness/nodejs-env.test.ts` | Node.js 环境验证 |
| `harness/prompt-templates.test.ts` | Prompt 模板 |
| `harness/repo.test.ts` | Repo 上下文 |
| `harness/resource-formatting.test.ts` | 资源格式化 |
| `harness/session-uuid.test.ts` | Session UUID |
| `harness/session.test.ts` | Session 基础行为 |
| `harness/skills.test.ts` | Skills 管理 |
| `harness/storage.test.ts` | 存储层 |
| `harness/system-prompt.test.ts` | System prompt 构建 |
| `harness/truncate.test.ts` | 消息截断 |
| `e2e.test.ts` | 端到端测试 |

测试模式示例——Agent 回调验证：

```typescript
const agent = new Agent({
  initialState: { model, systemPrompt: "test", tools: [] },
  onPayload: async (payload) => payload,
});
agent.subscribe((event) => events.push(event));
agent.execute({ ... });
expect(events.filter((e) => e.type === "done")).toHaveLength(1);
```

## 3. AI Provider 测试（41 个文件）

`packages/ai/test/` 包含 41 个测试文件，覆盖 provider 适配、streaming、tokens、cache 等。

| 类别 | 文件 | 测试重点 |
|---|---|---|
| Provider 适配 | `anthropic-*.test.ts` (12 个) | Anthropic：thinking、cache、SSE parsing、tool name normalization、OAuth |
| | `bedrock-*.test.ts` (4 个) | AWS Bedrock：message conversion、endpoint、thinking payload |
| | `openai-*.test.ts` (8 个) | OpenAI：Codex、Responses、completions、cache、tool choice |
| | `google-*.test.ts` (3 个) | Google：thinking、vertex、shared tools |
| | `azure-openai-*.test.ts` (1 个) | Azure base URL |
| | `github-copilot-*.test.ts` (2 个) | GitHub Copilot |
| | `fireworks-models.test.ts` | Fireworks 模型列表 |
| | `together-models.test.ts` | Together AI 模型列表 |
| | `mistral-*.test.ts` (2 个) | Mistral reasoning/tool schema |
| | `openrouter-*.test.ts` (2 个) | OpenRouter cache/images |
| 框架功能 | `faux-provider.test.ts` | FauxProvider 自身测试（前文已述） |
| | `stream.test.ts` | Streaming 核心逻辑 |
| | `tokens.test.ts` | Token 计算 |
| | `total-tokens.test.ts` | 总 token 统计 |
| | `cache-retention.test.ts` | Cache 保持策略 |
| | `env-api-keys.test.ts` | API key 环境变量解析 |
| | `context-overflow.test.ts` / `overflow.test.ts` | 上下文溢出 |
| | `abort.test.ts` | Abort 机制 |
| | `lazy-module-load.test.ts` | 延迟加载 |
| 交叉适配 | `cross-provider-handoff.test.ts` | 跨 provider 切换 |
| | `transform-messages-*.test.ts` | 消息格式转换 |
| | `tool-call-id-normalization.test.ts` | Tool call ID 归一化 |
| | `tool-call-without-result.test.ts` | 无结果的 tool call |
| | `image-tool-result.test.ts` / `images.test.ts` | 图像处理 |
| | `validation.test.ts` | 参数校验 |
| | `interleaved-thinking.test.ts` | 交错 thinking |
| | `responseid.test.ts` | Response ID |
| | `xhigh.test.ts` / `supports-xhigh.test.ts` | XHigh 能力检测 |
| | `unicode-surrogate.test.ts` | Unicode 代理对 |
| | `empty.test.ts` | 空请求 |
| | `zen.test.ts` | Zen 模式 |
| | `node-http-proxy.test.ts` | HTTP 代理 |
| | `oauth-device-code.test.ts` | OAuth 设备码 |

### 测试模式——Provider 适配测试

```typescript
describe("Anthropic", () => {
  it("converts thinking blocks", async () => {
    // 使用真实 provider 实例 + mock HTTP
    const provider = new AnthropicProvider({ apiKey: "test" });
    // 验证消息格式转换
  });
});
```

### 测试模式——OpenAI 兼容 API

```typescript
describe("OpenAI completions", () => {
  it("handles tool choice", async () => {
    // 构造多种 tool_choice 参数
    // 验证序列化为正确格式
  });
});
```

## 4. Coding Agent 测试（160 个文件）

`packages/coding-agent/test/` 是 Pi 测试体系的核心，包含 160 个测试文件。按功能划分为：suite 测试、regression 测试、组件测试。

### 4.1 Suite 测试（真实 AgentSession 集成测试）

Suite 测试是 Pi 评测体系的最大亮点：**使用真实 AgentSession 实例 + FauxProvider**，而非 mock 或 stub。每个 suite 测试通过 `createHarness()` 创建一个完整的测试环境：

```typescript
// test/suite/harness.ts
const harness = await createHarness({
  models,           // Faux model 定义
  settings,         // 内存 SettingsManager
  systemPrompt,     // 自定义 system prompt
  tools,            // 自定义工具
  extensionFactories, // 扩展工厂
});

// 设置 FauxProvider 的响应序列
harness.setResponses([
  fauxAssistantMessage("Let me check..."),
  fauxAssistantMessage("Here's the result.", { stopReason: "endTurn" }),
]);

// 执行用户消息
await harness.session.submitMessage("list files");

// 断言事件序列
expect(harness.eventsOfType("done")).toHaveLength(1);
expect(getUserTexts(harness)).toContain("list files");

// 清理
harness.cleanup();
```

| 测试文件 | 行数 | 测试重点 |
|---|---|---|
| `suite/agent-session-runtime.test.ts` | 596 | Session 运行时：消息提交、事件类型、FauxProvider 交互、多轮对话 |
| `suite/agent-session-compaction.test.ts` | 407 | Context 压缩触发、压缩后消息恢复 |
| `suite/agent-session-queue.test.ts` | 422 | 消息队列：并发提交排队、FIFO 顺序 |
| `suite/agent-session-retry-events.test.ts` | 360 | 重试事件：provider 错误重试、事件通知 |
| `suite/agent-session-prompt.test.ts` | — | Prompt 模板集成 |
| `suite/agent-session-model-extension.test.ts` | — | 模型扩展 |
| `suite/agent-session-bash-persistence.test.ts` | — | Bash 持久化 |

#### Agent-Session Runtime 测试（核心）

`agent-session-runtime.test.ts`（596 行）验证 AgentSession 的核心行为：

```typescript
async () => {
  // 1. 真实会话启动
  const harness = await createHarness();
  harness.setResponses([fauxAssistantMessage("hello")]);
  
  // 2. 提交用户消息
  await harness.session.submitMessage("hi");
  
  // 3. 检查事件序列
  expect(harness.eventsOfType("user_message")).toHaveLength(1);
  expect(harness.eventsOfType("done")).toHaveLength(1);
  
  // 4. 检查会话消息
  expect(harness.session.messages.length).toBeGreaterThan(0);
};
```

关键验证维度：

- **事件完整性**：`user_message` → `model_provider_request` → `model_provider_response` → `assistant_message` → `done`
- **消息往返**：用户消息正确传递给 provider，provider 响应正确返回 session
- **多轮交互**：多个 `submitMessage` 调用的状态累积
- **FauxProvider 队列消费**：预设响应被按顺序消费

#### Agent-Session Compaction 测试

`agent-session-compaction.test.ts`（407 行）验证上下文压缩机制：

- 压缩触发条件：token 计数超过阈值
- 压缩后消息历史可正确恢复
- 压缩不影响后续交互的语义完整性

### 4.2 Regression 测试（17 个 per-issue 测试）

Pi 的一个独特实践是**每个已修复的 bug 对应一个独立的回归测试文件**，以 issue 编号命名：

```typescript
// test/suite/regressions/1717-2113-agent-session-event-settlement.test.ts
describe("regression: agent session event settlement (#1717/#2113)", () => {
  // 复现 issue 中报告的场景
  // 验证修复后的正确行为
});
```

完整回归测试列表：

| 文件 | Issue | 测试场景 |
|---|---|---|
| `1717-2113-agent-session-event-settlement.test.ts` | #1717 / #2113 | 事件结算时序 |
| `2023-queued-slash-command-followup.test.ts` | #2023 | 排队 slash 命令跟进 |
| `2753-reload-stale-resource-settings.test.ts` | #2753 | 过期资源设置重载 |
| `2781-skill-collision-precedence.test.ts` | #2781 | Skill 碰撞优先级 |
| `2791-fswatch-error-crash.test.ts` | #2791 | fswatch 错误崩溃 |
| `2835-tools-allowlist-filters-extension-tools.test.ts` | #2835 | 工具白名单过滤 |
| `2860-replaced-session-context.test.ts` | #2860 | 替换 session 上下文 |
| `3217-scoped-model-order.test.ts` | #3217 | 作用域模型顺序 |
| `3302-find-path-glob.test.ts` | #3302 | find 路径 glob |
| `3303-find-nested-gitignore.test.ts` | #3303 | 嵌套 .gitignore |
| `3317-network-connection-lost-retry.test.ts` | #3317 | 断网重试 |
| `3592-no-builtin-tools-keeps-extension-tools.test.ts` | #3592 | 无内置工具时保留扩展工具 |
| `3616-settings-inmemory-reload.test.ts` | #3616 | 内存设置重载 |
| `3686-session-name-event.test.ts` | #3686 | Session 命名事件 |
| `3688-tree-cancel-compacting.test.ts` | #3688 | 树结构取消压缩 |
| `3982-message-end-cost-override.test.ts` | #3982 | 消息结束成本覆盖 |
| `4167-thinking-toggle-pending-tool-render.test.ts` | #4167 | Thinking 切换时挂起工具渲染 |

这种 "one issue = one test file" 的策略让回归测试更易于追溯——看到测试文件名就能关联到具体的 bug 修复。

### 4.3 组件测试（~120 个文件）

剩余 120+ 个测试文件覆盖 coding-agent 的各个组件：

| 类别 | 文件 | 测试重点 |
|---|---|---|
| Tool & Execution | `tools.test.ts`、`tool-execution-component.test.ts`、`edit-tool-*.test.ts`、`file-mutation-queue.test.ts` | 工具注册、执行、编辑工具、文件变异队列 |
| Session & State | `agent-session-*.test.ts`（branching/concurrent/dynamic-provider/dynamic-tools/retry/stats/tree-navigation） | Session 分支、并发、动态 provider/工具、重试、统计、树导航 |
| Config & Settings | `config.test.ts`、`settings-manager.test.ts`、`settings-manager-bug.test.ts`、`model-registry.test.ts`、`model-resolver.test.ts` | 配置加载、设置管理、模型注册/解析 |
| Compaction | `compaction.test.ts`、`compaction-extensions.test.ts`、`compaction-serialization.test.ts`、`compaction-summary-reasoning.test.ts` | 上下文压缩、扩展、序列化 |
| UI Components | `footer-data-provider.test.ts`、`footer-width.test.ts`、`theme-*.test.ts`、`keybindings-migration.test.ts`、`tree-selector.test.ts`、`session-selector-*.test.ts` | Footer、主题、快捷键、选择器 |
| Extensions | `extensions-discovery.test.ts`、`extensions-input-event.test.ts`、`extensions-runner.test.ts`、`trigger-compact-extension.test.ts` | 扩展发现、事件、运行 |
| Interactive Mode | `interactive-mode-*.test.ts`（anthropic-warning、clone-command、compaction、import-command、status、suspend） | 交互模式 |
| SDK | `sdk-openrouter-attribution.test.ts`、`sdk-session-manager.test.ts`、`sdk-skills.test.ts` | SDK 集成 |
| RPC | `rpc.test.ts`、`rpc-client-clone.test.ts`、`rpc-jsonl.test.ts`、`rpc-prompt-response-semantics.test.ts` | RPC 协议 |
| Utility | `ansi-utils.test.ts`、`args.test.ts`、`assistant-message.test.ts`、`auth-storage.test.ts`、`bash-*.test.ts`、`clipboard-*.test.ts`、`git-*.test.ts`、`image-*.test.ts`、`path-utils.test.ts`、`paths.test.ts`、`print-mode.test.ts`、`prompt-templates.test.ts`、`resource-loader.test.ts`、`skills.test.ts`、`stdout-cleanliness.test.ts`、`syntax-highlight.test.ts`、`system-prompt.test.ts`、`truncate-to-width.test.ts`、`user-message.test.ts`、`version-check.test.ts` | 各类辅助工具 |

## 5. TUI 测试（22 个文件）

TUI 测试使用 `node --test` 而非 vitest，覆盖终端渲染组件。

| 文件 | 测试重点 |
|---|---|
| `autocomplete.test.ts` | 自动补全 |
| `editor.test.ts` | 编辑器 |
| `fuzzy.test.ts` | 模糊搜索 |
| `input.test.ts` | 输入处理 |
| `keybindings.test.ts` | 快捷键绑定 |
| `keys.test.ts` | 按键事件 |
| `markdown.test.ts` | Markdown 渲染 |
| `overlay-non-capturing.test.ts` | 非捕获覆盖层 |
| `overlay-options.test.ts` | 覆盖层选项 |
| `overlay-short-content.test.ts` | 短内容覆盖层 |
| `select-list.test.ts` | 选择列表 |
| `stdin-buffer.test.ts` | 标准输入缓冲区 |
| `terminal.test.ts` | 终端控制 |
| `terminal-image.test.ts` | 终端图像显示 |
| `truncate-to-width.test.ts` | 截断到宽度 |
| `truncated-text.test.ts` | 截断文本 |
| `tui-cell-size-input.test.ts` | 单元格尺寸输入 |
| `tui-overlay-style-leak.test.ts` | 覆盖层样式泄漏 |
| `tui-render.test.ts` | 渲染引擎 |
| `wrap-ansi.test.ts` | ANSI 换行 |
| `bug-regression-isimageline-startswith-bug.test.ts` | bug 回归 |
| `regression-regional-indicator-width.test.ts` | 地区指示符宽度回归 |

node --test 的使用说明 TUI 包的测试场景比较简单直接，不需要 vitest 的额外功能（如 mock/watch/coverage）。

## 6. 凭据隔离（test.sh）

`test.sh` 是 Pi 的标准测试入口，它的核心作用是**确保测试不会意外调用真实 LLM API**：

```bash
# 1. 备份 auth.json（用户认证凭据）
mv "$HOME/.pi/agent/auth.json" "$HOME/.pi/agent/auth.json.bak"

# 2. 设置环境变量跳过本地 LLM
export PI_NO_LOCAL_LLM=1

# 3. 逐行 unset 40+ 个 API key 环境变量
unset ANTHROPIC_API_KEY
unset OPENAI_API_KEY
unset GEMINI_API_KEY
unset DEEPSEEK_API_KEY
unset OPENROUTER_API_KEY
# ... 覆盖所有主流 provider + AWS 凭据

# 4. 运行测试
npm test

# 5. 恢复 auth.json（trap EXIT）
mv "$HOME/.pi/agent/auth.json.bak" "$HOME/.pi/agent/auth.json"
```

对比其他项目的凭据处理方式：

| 项目 | 凭据处理 |
|---|---|
| Pi | 备份 auth.json + unset 40+ env vars + PI_NO_LOCAL_LLM |
| Hermes | conftest.py 清除 _API_KEY/_TOKEN/_SECRET 变量 |
| Nanobot | 未发现专门的凭据隔离机制 |
| OpenClaw | 未发现专门的凭据隔离机制 |

Pi 的凭据隔离是最彻底的——不仅清除环境变量，还移除了文件系统的 auth.json，并设置了框架层面的屏蔽开关。

## 7. 工程检查管道（npm run check）

Pi 的 `npm run check` 是 CI gate，包含 5 个阶段：

```bash
npm run check  # 等价于：
# 1. biome check --write --error-on-warnings .  # 代码格式 + lint
# 2. node scripts/check-pinned-deps.mjs          # 依赖版本锁定
# 3. node scripts/check-ts-relative-imports.mjs  # 相对路径 import
# 4. node scripts/generate-coding-agent-shrinkwrap.mjs --check  # shrinkwrap 完整性
# 5. node scripts/check-browser-smoke.mjs         # 浏览器打包冒烟
```

`check.sh` 不运行测试（`AGENTS.md` 明确区分：`npm run check` ≠ `npm test`）。

## 8. 分析脚本

Pi 提供了一套分析脚本，用于离线分析用户 session 数据。这与测试不同——它们从 session 日志中提取统计信息，可用于评估 agent 在实际使用中的表现。

| 脚本 | 输入 | 输出 |
|---|---|---|
| `cost.ts` | Session 日志 | Token 成本明细 |
| `stats.ts` | Session 日志 | 会话统计（turn 数、工具调用频率等） |
| `edit-tool-stats.mjs` | Session 日志 | 编辑工具使用统计 |
| `read-tool-stats.mjs` | Session 日志 | 读取工具使用统计 |
| `session-context-stats.mjs` | Session 日志 | 上下文窗口利用率 |
| `session-transcripts.ts` | Session 日志 | 提取可读 transcript |
| `tool-stats.ts` | Session 日志 | 通用工具使用统计 |

这些脚本弥补了 Pi 没有独立 benchmark 管道的不足——通过分析真实使用数据而非预设场景来评估 agent 表现。

## 9. 评测体系总结

### 分层评测覆盖

| 层次 | Pi 实现 | 成熟度 |
|---|---|---|
| L0 工程 gate | biome + pinned-deps + ts-imports + shrinkwrap + browser-smoke | ⭐⭐⭐⭐⭐ |
| L1 组件行为 | Provider/tool/settings/session 组件测试 | ⭐⭐⭐⭐⭐ |
| L2 Agent loop | 真实 AgentSession + FauxProvider 集成测试 | ⭐⭐⭐⭐⭐ |
| L3 Scenario eval | 无独立 scenario 评测集 | ⭐⭐ |
| L4 Live eval | 无独立 lane（依赖 test.sh 确保不会调用真实 API） | ⭐ |
| L5 离线分析 | 7 个分析脚本（cost/stats/edit-tool/session-context） | ⭐⭐⭐ |

### 与 Nanobot 的关键差异

| 维度            | Pi                                | Nanobot                     |
| ------------- | --------------------------------- | --------------------------- |
| 开发语言          | TypeScript (monorepo)             | Python                      |
| 测试框架          | vitest + node --test              | pytest + asyncio            |
| Provider mock | FauxProvider（完整 LLM 模拟）           | MagicMock(spec=LLMProvider) |
| 测试层级          | 真实 AgentSession 集成测试              | AgentRunner 单元测试            |
| Regression 管理 | 17 个 per-issue 测试文件               | 无 per-issue 命名              |
| Streaming 测试  | 完整事件序列 + abort 控制                 | 有限 streaming filter 测试      |
| 凭据隔离          | auth.json 备份 + 40+ env vars unset | 未发现                         |
| 工程检查          | biome + 4 个自定义 check 脚本           | ruff + coverage             |
| 分析脚本          | 7 个 session 分析脚本                  | 无                           |
| E2E 测试        | 有限                                | API / Docker / WebUI        |
| 前端测试          | 无（CLI-only）                       | 20+ vitest WebUI            |

### 与 Hermes 的关键差异

| 维度            | Pi                               | Hermes                               |
| ------------- | -------------------------------- | ------------------------------------ |
| 核心设计意图        | Agent 行为正确性验证                    | 训练数据生产                               |
| Provider mock | FauxProvider 完整模拟                | 简单 mock                              |
| 批量数据生成        | 无                                | batch_runner + checkpoint            |
| 轨迹格式          | 无（使用 AgentSessionEvent）          | ShareGPT-like from/value             |
| 性能基准          | 无（分析脚本为离线分析）                     | Kanban 基准 + browser eval             |
| 测试隔离          | 标准 vitest（单进程）                   | per-file 子进程隔离                       |
| 凭据安全          | auth.json 备份 + 40+ env var unset | conftest.py 清除                       |
| 分布式评测         | 无                                | mini_swe_runner (local/docker/modal) |

### 主要缺口

1. **缺少批量评测能力**：没有类似 hermes-agent `batch_runner.py` 的并行评测引擎，也无法像 nanobot 那样通过 `pytest --workers` 并行。大规模评测需要自行编写脚本。
2. **无任务级 scenario 评测集**：没有预设的评测场景目录，无法衡量 task completion rate。
3. **无 Live eval lane**：test.sh 的设计就是防止调用真实 API，这使得 Pi 无法在实际模型上评测 agent 行为——所有测试都基于 FauxProvider。
4. **无性能基准**：没有启动时间、gateway 延迟、并发吞吐量的基准测试。
5. **无 LLM Judge 评测**：没有类似 nanobot `evaluate_response` 或 OpenClaw rubric 的 LLM 评判机制。
6. **无前端测试**：作为 CLI-only 项目，缺少类似 nanobot WebUI 的 20+ vitest 前端测试。
7. **无增量评测机制**：没有 checkpoint/resume 能力，每次从零执行。
8. **分析脚本与测试脱节**：分析脚本（cost/stats/edit-tool-stats 等）是独立的 Node.js 脚本，与正式的测试框架没有集成，无法在 CI 中自动触发。
