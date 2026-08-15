# Nanobot 评测方案与实现分析

资料范围：

- 本地仓库：`/Users/liyazhou/Repo/repo_ai/nanobot`（`nightly` / `main` branch）
- 远程仓库：`https://github.com/HKUDS/nanobot`
- 在线文档：<https://nanobot.wiki/docs/latest/getting-started/nanobot-overview>
- 开发指引：`AGENTS.md`、`CLAUDE.md`

## 结论先行

Nanobot 的评测体系是**以 asyncio + MagicMock 为核心的分层测试架构**，强调通过 mock provider 实现高频、确定性的 agent 行为验证。它没有像 hermes-agent 那样提供大规模批量数据生成管道（batch_runner），也没有像 OpenClaw 那样提供 QA Lab scenario 管理平台，而是在"单次 agent 执行的正确性"上做得很深——工具调用、错误恢复、hook 生命周期、持久化、goal 延续等维度都有专门的测试覆盖。

它的核心设计特点：

1. **AgentRunner 可测性设计**：`AgentRunner` 与 `AgentLoop` 分离，`AgentRunner.run()` 接收 `AgentRunSpec`、返回 `AgentRunResult`（含 `final_content`、`tools_used`、`tool_events`、`stop_reason`），天然可断言。
2. **分层测试策略**：230+ 测试文件、3951 个测试函数，按 agent/provider/channel/tool/session/cron/webui 分层组织。
3. **MagicMock provider 模式**：通过 `MagicMock(spec=LLMProvider)` 构造确定性 provider，无需真实模型即可验证多轮工具交互。
4. **Dream 双阶段记忆评估**：独有的 `evaluate_response` 模块用于后台任务通知决策，Consolidator 做 session 压缩总结的 LLM 评估。
5. **无独立 benchmark 脚本**：相比 hermes 的 batch_runner 和 OpenClaw 的 QA Lab，nanobot 没有大规模评测管线——评测集中在工程正确性和组件行为层。

## 评测系统总览

```
nanobot/
├── pyproject.toml              # pytest 配置：asyncio_mode=auto, testpaths=tests
├── tests/                      # 230+ 文件, 3951 个测试函数
│   ├── agent/                  # 66 个文件 — Agent loop/runner/memory/dream/hooks
│   ├── providers/              # 36 个文件 — 18+ provider 实现
│   ├── channels/               # 36 个文件 — 15+ channel 平台适配
│   ├── tools/                  # 26 个文件 — exec/file/web/MCP/tool registry
│   ├── utils/                  # 19 个文件 — 辅助工具
│   ├── cli/                    # 6 个文件 — CLI 命令
│   ├── config/                 # 5 个文件 — 配置 schema/加载
│   ├── session/                # 5 个文件 — session/consolidation/goal
│   ├── cron/                   # 4 个文件 — cron 服务/工具
│   ├── webui/                  # 4 个文件 — WebUI Python 接口
│   ├── security/               # 3 个文件 — 安全边界
│   ├── cli_apps/               # 3 个文件 — CLI 应用
│   ├── bus/                    # 1 个文件 — MessageBus
│   ├── command/                # 4 个文件 — 命令路由
│   ├── pairing/                # 1 个文件 — DM pairing
│   └── 根目录                  # 11 个文件 — API 测试/集成
├── webui/
│   └── src/tests/              # 20+ 个 vitest 测试文件
└── docs/                       # 无独立 eval 相关文档
```

## 1. 测试基础设施

### pytest 配置

`pyproject.toml` 中配置：

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
```

- **asyncio_mode = "auto"**：所有 `async def test_*` 自动由 pytest-asyncio 处理，无需手动 decorator
- **testpaths = ["tests"]**：默认只扫描 tests/ 目录

### CLI 入口

```bash
# 完整回归
pytest

# 单模块
pytest tests/agent/
pytest tests/providers/

# 单文件
pytest tests/agent/test_runner_core.py

# 单测试
pytest tests/agent/test_runner_core.py::test_runner_preserves_reasoning_fields_and_tool_results -v

# 代码风格检查
ruff check nanobot/

# 覆盖率
pytest --cov
```

coverage 配置：

```toml
[tool.coverage.run]
source = ["nanobot"]
omit = ["tests/*", "**/tests/*"]
```

### WebUI 测试

```bash
cd webui && bun run test     # vitest run
cd webui && bun run lint     # eslint, max-warnings=0
```

vitest 配置（`webui/vite.config.ts`）：

```ts
test: {
  environment: "happy-dom",
  globals: true,
  setupFiles: ["./src/tests/setup.ts"],
}
```

## 2. Agent 层测试（66 个文件）

这是 nanobot 测试体系的核心，覆盖 AgentRunner 和 AgentLoop 的所有行为维度。

### 测试架构

```python
# conftest.py：共享 fixture
def make_provider(default_model="test-model", **kwargs) -> MagicMock:
    """创建 spec-limited LLM provider mock"""
    mock_type = MagicMock(spec=LLMProvider) if spec else MagicMock()
    provider = mock_type
    provider.get_default_model.return_value = default_model
    provider.estimate_prompt_tokens.return_value = (10_000, "test")
    return provider

def make_loop(tmp_path, **kwargs) -> AgentLoop:
    """创建真实的 AgentLoop 实例（可 patch 依赖）"""
    bus = MessageBus()
    provider = kwargs.pop("provider", make_provider())
    return AgentLoop(bus=bus, provider=provider, workspace=tmp_path, ...)
```

关键设计：**使用 `MagicMock(spec=LLMProvider)` 而非 fake provider**。这样既保证了 mock 不会偏离接口（`spec` 参数），又不需要实现完整的 provider 抽象类。

### AgentRunner 测试

AgentRunner 是核心执行引擎，`run()` 接收 `AgentRunSpec`、返回 `AgentRunResult`。测试按维度分散在多个文件中：

| 文件 | 测试重点 |
|---|---|
| `test_runner_core.py` | 消息传递、迭代限制、超时、空响应处理、usage 累积 |
| `test_runner_tool_execution.py` | 工具批处理（read-only 并行、exclusive 串行）、并发执行 |
| `test_runner_hooks.py` | Hook 生命周期顺序（before_iteration → before_execute_tools → after_iteration → finalize_content） |
| `test_runner_errors.py` | 工具执行错误恢复、out-of-quota 检测、回复失败 |
| `test_runner_fallback.py` | provider 回退逻辑 |
| `test_runner_safety.py` | 安全边界（工具注入、权限控制） |
| `test_runner_persistence.py` | 大工具结果持久化、清理、文件管理 |
| `test_runner_reasoning.py` | reasoning_content、thinking_blocks 传递 |
| `test_runner_goal_continue.py` | `/goal` 延续机制：goal_active_predicate 控制循环延续 |
| `test_runner_progress_deltas.py` | 增量进度事件 |
| `test_runner_injections.py` | 消息注入（多轮 injection cycles） |
| `test_runner_governance.py` | 治理/管控行为 |

AgentRunResult 的结构使得断言非常直接：

```python
result = await runner.run(spec)
assert result.final_content == "done"
assert result.tools_used == ["list_dir"]
assert result.stop_reason == "completed"
assert result.tool_events == [
    {"name": "list_dir", "status": "ok", "detail": "tool result"}
]
```

Stop reason 枚举：`"completed"`、`"max_iterations"`、`"error"`、`"cancelled"`、`"empty_final_response"`、`"tool_error"`。

### AgentLoop 集成测试

AgentLoop 在 AgentRunner 之外增加了 session 管理、context 构建、streaming、subagent 等能力。集成测试覆盖：

| 文件                                     | 测试重点                                                   |
| -------------------------------------- | ------------------------------------------------------ |
| `test_loop_runner_integration.py`      | Runner 与 Loop 集成、max_iterations 消息稳定性、streaming filter |
| `test_loop_save_turn.py`               | turn 持久化                                               |
| `test_loop_tool_context.py`            | 工具调用上下文传递                                              |
| `test_loop_progress.py`                | 进度事件                                                   |
| `test_loop_goal_wall_timeout.py`       | goal 超时                                                |
| `test_loop_image_generation_media.py`  | 图像生成媒体处理                                               |
| `test_loop_cron_timezone.py`           | cron 时区                                                |
| `test_loop_consolidation_tokens.py`    | 上下文压缩 token 管理                                         |
| `test_loop_direct_websocket_status.py` | WebSocket 状态                                           |

### Dream 记忆系统测试

Dream 是 nanobot 的**两阶段内存合并系统**，也是 nanobot 独有的"评估"组件——它用 LLM 决定哪些历史需要压缩、哪些需要通知用户。

| 文件 | 测试重点 |
|---|---|
| `test_dream.py` | `build_dream_prompt()`：cursor 管理、长条目截断、批量顺序 |
| `test_dream_session.py` | session key 生成 + 裁剪（保留最近 N 个 dream session） |
| `test_dream_tools.py` | `dream_tool` 行为 |
| `test_memory_store.py` | MemoryStore 纯文件 I/O：read/write/append/cursor/原子写入 |
| `test_consolidator.py` | Consolidator 的 LLM 摘要调用 + 追加 HISTORY.md |
| `test_consolidation_ratio.py` | 压缩比例控制 |
| `test_consolidate_offset.py` | 偏移量管理 |
| `test_auto_compact.py` | 自动上下文压缩触发器 |

#### Evaluator 模块

`nanobot/utils/evaluator.py` 是后台任务（heartbeat/cron）的**后执行评估器**：执行完任务后，用一次轻量 LLM 调用来判断结果是否值得通知用户。

```python
async def evaluate_response(
    response: str,
    task_context: str,
    provider: LLMProvider,
    model: str,
    default_notify: bool = True,
) -> bool:
```

它通过 `evaluate_notification` 工具调用让 LLM 做二元决策（should_notify + reason）。测试覆盖：正常 true/false、provider 故障回退（fail open/closed）、无工具调用回退。

### 其他 agent 测试

| 文件 | 测试重点 |
|---|---|
| `test_context_builder.py` | 上下文构建 |
| `test_context_prompt_cache.py` | prompt cache 配置 |
| `test_cursor_recovery.py` | cursor 恢复 |
| `test_document_extraction_toggle.py` | 文档提取控制 |
| `test_git_store.py` | git 存储 |
| `test_hook_composite.py` | 复合 hook |
| `test_stop_preserves_context.py` | 停止时上下文保持 |
| `test_evaluator.py` | evaluate_response 单元测试（前文已述） |

## 3. Provider 测试（36 个文件）

Provider 测试验证各个 LLM provider 的行为正确性。nanobot 支持 18+ provider，测试覆盖其中大部分。

| 测试文件 | 测试重点 |
|---|---|
| `test_anthropic_thinking.py` | Anthropic 推理 token/thinking block 处理 |
| `test_anthropic_stream_idle.py` | Anthropic streaming 空闲超时 |
| `test_anthropic_tool_result.py` | tool result 格式转换 |
| `test_anthropic_merge_consecutive.py` | 用户消息合并（Anthropic 要求角色交替） |
| `test_anthropic_long_request_fallback.py` | 长请求回退 |
| `test_openai_responses.py` | OpenAI Responses API |
| `test_openai_codex_provider.py` | Codex provider |
| `test_openai_compat_timeout.py` | OpenAI 兼容超时配置 |
| `test_bedrock_provider.py` | AWS Bedrock provider |
| `test_azure_openai_provider.py` | Azure OpenAI |
| `test_github_copilot_routing.py` | GitHub Copilot 路由 |
| `test_minimax_anthropic_provider.py` | MiniMax Anthropic 兼容 |
| `test_mistral_provider.py` | Mistral provider |
| `test_novita_provider.py` | NovitaAI provider |
| `test_skywork_provider.py` | Skywork provider |
| `test_stepfun_reasoning.py` | StepFun 推理 |
| `test_xiaomi_mimo_thinking.py` | MiMo 推理 |
| `test_ant_ling_provider.py` | Ant Ling provider |
| `test_longcat_provider.py` | LongCat provider |
| `test_custom_provider.py` | 自定义 provider |
| `test_enforce_role_alternation.py` | 角色交替强制 |
| `test_extra_body_config.py` | extra_body 配置 |
| `test_image_generation.py` | 图像生成 provider |
| `test_transcription.py` | 语音转录 provider |
| `test_cached_tokens.py` | 缓存 token |
| `test_llm_response.py` | LLMResponse 数据类型 |
| `test_local_endpoint_detection.py` | 本地端点检测 |
| `test_provider_retry.py` | provider 重试逻辑 |
| `test_provider_retry_after_hints.py` | Retry-After 头处理 |
| `test_provider_sdk_retry_defaults.py` | SDK 默认重试 |
| `test_provider_error_metadata.py` | 错误元数据 |
| `test_providers_init.py` | 延迟导入（lazy import）验证 |
| `test_reasoning_content.py` | 推理内容格式 |
| `test_responses_circuit_breaker.py` | 熔断器 |
| `test_litellm_kwargs.py` | LiteLLM kwargs 传递 |
| `test_prompt_cache_markers.py` | prompt cache 标记 |

测试模式示例——Anthropic 推理 token 测试：

```python
async def test_reasoning_content_stored_in_response():
    """anthropic_reasoning tag → reasoning_content"""
    provider = AnthropicProvider(...)
    response = await provider.chat(messages=[{"role": "user", ...}])
    assert response.reasoning_content == "..."
```

## 4. 工具测试（26 个文件）

工具测试覆盖 nanobot 所有内置工具的安全、正确性和边界条件。

| 测试文件 | 测试重点 |
|---|---|
| `test_exec_security.py` | exec 工具内部 URL 阻止（169.254.169.254、localhost 等） |
| `test_exec_allow_patterns.py` | 命令允许模式 |
| `test_exec_env.py` | 执行环境变量 |
| `test_exec_platform.py` | 平台特定行为 |
| `test_exec_session_tools.py` | 会话工具 |
| `test_sandbox.py` | sandbox 环境 |
| `test_filesystem_tools.py` | 文件系统工具 |
| `test_apply_patch_tool.py` | patch 应用 |
| `test_edit_advanced.py` / `test_edit_enhancements.py` | 文件编辑 |
| `test_file_edit_coding_enhancements.py` | 编码增强编辑 |
| `test_read_enhancements.py` | 读取增强 |
| `test_search_tools.py` | 搜索工具 |
| `test_web_search_tool.py` | web 搜索 |
| `test_web_fetch_security.py` | web 获取安全 |
| `test_web_fetch_url_sanitization.py` | URL 消毒 |
| `test_image_generation_tool.py` | 图像生成工具 |
| `test_mcp_tool.py` / `test_mcp_probe.py` | MCP 工具 |
| `test_message_tool.py` / `test_message_tool_suppress.py` | 消息工具 |
| `test_tool_loader.py` | 工具加载器 |
| `test_tool_registry.py` | 工具注册表 |
| `test_tool_validation.py` | 工具参数校验 |
| `test_tool_descriptions.py` | 工具描述 |

exec 安全测试示例——检测内部 URL 阻断：

```python
def _fake_resolve_private(hostname, port, family=0, type_=0):
    return [(socket.AF_INET, socket.SOCK_STREAM, 0, "", ("169.254.169.254", 0))]

async def test_exec_blocks_curl_metadata():
    tool = ExecTool()
    with patch("nanobot.security.network.socket.getaddrinfo", _fake_resolve_private):
        result = await tool.execute(
            command='curl -s -H "Metadata-Flavor: Google" http://169.254.169.254/...'
        )
    assert "Error" in result
    assert "internal" in result.lower() or "private" in result.lower()
```

## 5. 通道测试（36 个文件）

通道测试验证各消息平台的适配器行为。nanobot 支持 15+ 通道，测试覆盖大部分。

关键测试文件包括：

| 文件 | 通道 | 测试重点 |
|---|---|---|
| `test_telegram_channel.py` | Telegram | 消息收发、inline buttons |
| `test_discord_channel.py` | Discord | 消息格式、slash 命令 |
| `test_slack_channel.py` | Slack | 消息适配 |
| `test_feishu_*.py` (5 个文件) | 飞书 | 话题路由、mention、表格分割、流式、表情 |
| `test_dingtalk_channel.py` | 钉钉 | 消息处理 |
| `test_whatsapp_channel.py` | WhatsApp | 消息格式 |
| `test_signal_channel.py` | Signal | 消息收发 |
| `test_qq_channel.py` / `test_qq_media.py` | QQ | 消息 + 媒体 |
| `test_napcat_channel.py` | NapCat | 消息处理 |
| `test_base_channel.py` | 基类 | 通道基类行为 |

## 6. Session/Cron 测试

### Session 测试（5 个文件）

| 文件 | 测试重点 |
|---|---|
| `test_goal_state.py` | goal 状态持久化 |
| `test_consolidated_offset_clamp.py` | 压缩偏移限制 |
| `test_turn_continuation.py` | turn 延续 |
| `test_session_fsync.py` | fsync 持久化 |

### Cron 测试（4 个文件）

| 文件 | 测试重点 |
|---|---|
| `test_cron_service.py` | 作业增删、时区校验、表达式解析、到期触发 |
| `test_cron_persistence.py` | 持久化、跨重启恢复 |
| `test_cron_tool_schema_contract.py` | 工具 schema 契约 |
| `test_cron_tool_list.py` | 工具列表 |

## 7. Security 测试（3 个文件）

| 文件 | 测试重点 |
|---|---|
| `test_file_access.py` | workspace 文件访问控制 |
| `test_network_access.py` | 网络访问白名单 |
| `test_path_traversal.py` | 路径穿越防护 |

## 8. WebUI 测试（20+ vitest 文件）

前端测试使用 **vitest + happy-dom + @testing-library/react**。

测试文件清单：

| 文件 | 测试重点 |
|---|---|
| `thread-composer.test.tsx` | 消息输入组件 |
| `thread-composer-attach.test.tsx` | 附件 |
| `thread-messages.test.tsx` | 消息渲染 |
| `message-bubble.test.tsx` | 气泡组件 |
| `thread-shell.test.tsx` | 线程外壳 |
| `thread-viewport.test.tsx` | 视口 |
| `session-search-dialog.test.tsx` | 搜索对话框 |
| `session-info-popover.test.tsx` | 会话信息 popover |
| `chat-list.test.tsx` | 聊天列表 |
| `settings-view.test.tsx` | 设置页面 |
| `app-layout.test.tsx` | 应用布局 |
| `agent-activity-cluster.test.tsx` | agent 活动集群 |
| `code-block.test.tsx` | 代码块渲染 |
| `markdown-text.test.tsx` / `markdown-text-renderer.test.tsx` | Markdown 渲染 |
| `i18n.test.tsx` | 国际化 |
| `useNanobotStream.test.tsx` | WebSocket 流 hook |
| `useDeferredTitleRefresh.test.tsx` | 标题刷新 hook |
| `main-randomuuid.test.tsx` | UUID 生成 |
| `provider-brand.test.ts` | provider 品牌标识 |

## 9. 集成测试

| 文件 | 测试重点 |
|---|---|
| `test_openai_api.py` | OpenAI 兼容 API `/v1/chat/completions` |
| `test_api_attachment.py` | API 附件处理 |
| `test_api_stream.py` | API streaming |
| `test_nanobot_facade.py` | Python SDK facade |
| `test_context_documents.py` | 上下文文档 |
| `test_document_parsing.py` | 文档解析（PDF/Word/Excel） |
| `test_build_status.py` | 构建状态检查 |
| `test_package_version.py` | 包版本一致性 |
| `test_tool_contextvars.py` | 工具 ContextVar 隔离 |
| `test_msteams.py` | MS Teams 通道 |
| `test_truncate_text_shadowing.py` | 文本截断阴影 |
| `test_docker.sh` | Docker 镜像构建 + onboard + status 验证 |

Docker 测试流程：

```bash
docker build -t nanobot-test .
docker run nanobot-test onboard          # 初始化配置
docker run nanobot-test status            # 验证状态输出
# 断言: "nanobot Status"、"Config:"、"Model:"、"OpenRouter API:" 等
```

## 10. Evaluator（后台任务评估）

nanobot 的 `evaluate_response` 是唯一一个直接与"评估"相关的模块。它为 heartbeat 和 cron 这类后台任务提供执行后评估——判断结果是否值得推送给用户。

### 机制

```python
_EVALUATE_TOOL = [{
    "type": "function",
    "function": {
        "name": "evaluate_notification",
        "parameters": {
            "should_notify": {"type": "boolean"},
            "reason": {"type": "string"},
        },
    },
}]

async def evaluate_response(response, task_context, provider, model, default_notify=True):
    """LLM judge：决定是否通知用户"""
```

- 使用 `temperature=0.0` 保证可复现性
- 工具调用方式获取结构化输出（should_notify + reason）
- Cron 场景 fail open（`default_notify=True`）
- Heartbeat 场景 fail closed（`default_notify=False`）
- Provider 故障时回退到 default

测试覆盖 6 种场景：true、false、provider 错误、无工具调用回退、fail open、fail closed。

## 11. Dream 双阶段记忆评估

Dream 是 nanobot 独有的记忆系统，涉及两个阶段的"评估"：

### 第一阶段：Compaction

Consolidator 使用 LLM 压缩 session 历史：

```
Session 消息列表 → (LLM 调用) → 结构化摘要 → 追加到 HISTORY.md
```

测试验证：LLM 调用次数、摘要长度限制、历史文件格式。

### 第二阶段：Dream

MemoryStore 的 `build_dream_prompt()` 决定哪些历史需要"入梦"：

```python
def build_dream_prompt(self, max_entries=20, max_entry_chars=500):
    """构建 Dream prompt，包含 soul + memory + 未处理的历史条目"""
```

- 基于 cursor 跟踪已入梦位置
- 每次最多 20 条、每条 500 字符
- 输出被 skill-creator 技能消费

## 12. AgentRunResult 结构（运行时评估契约）

AgentRunner.run() 返回的 `AgentRunResult` 是评估的核心数据结构：

```python
@dataclass
class AgentRunResult:
    final_content: str | None
    messages: list[dict]          # 完整消息历史（含 tool calls/results）
    tools_used: list[str]         # 本轮调用过的工具名列表
    stop_reason: str              # 终止原因枚举
    tool_events: list[dict]       # 工具事件序列 [{name, status, detail}]
    had_injections: bool          # 是否发生过消息注入
    ...
```

这个结构使测试可以对 agent 执行做细粒度断言：

- **工具使用覆盖**：`tools_used` 断言调用了哪些工具
- **事件序列**：`tool_events` 断言工具执行成功/失败顺序
- **终止原因**：`stop_reason` 断言是否超过迭代限制、出错或被取消
- **消息完整性**：messages 字段保留完整往返，可检查 reasoning 字段保留

## 13. 评测体系总结

### 分层评测覆盖

| 层次 | Nanobot 实现 | 成熟度 |
|---|---|---|
| L0 工程 gate | pytest + ruff + coverage | ⭐⭐⭐⭐⭐ |
| L1 组件行为 | Provider/channel/tool 独立测试 | ⭐⭐⭐⭐⭐ |
| L2 Agent loop | AgentRunner + AgentLoop 全面覆盖 | ⭐⭐⭐⭐⭐ |
| L3 Scenario eval | 无独立 scenario 评测集 | ⭐ |
| L4 Live eval | 无独立 lane | ⭐ |
| L5 Benchmark | 无基准测试 | ⭐⭐ |

### 与 Hermes 的关键差异

| 维度 | Nanobot | Hermes |
|---|---|---|
| 测试规模 | 230 文件 / 3951 函数 | 900+ 文件 / 17000 测试 |
| 执行框架 | pytest asyncio | per-file 子进程隔离 |
| Provider 测试 | MagicMock(spec=LLMProvider) | 类似 mock 但更分散 |
| 批量评测 | 无 | batch_runner + checkpoint |
| 工具分布控制 | 无 | toolset_distributions 概率采样 |
| 轨迹格式 | 无（AgentRunResult 作为执行摘要） | ShareGPT-like from/value |
| 后执行评估 | evaluate_response（通知决策） | 无对应模块 |
| 记忆评估 | Dream + Consolidator LLM 摘要 | 无（trajectory compressor 为训练） |
| WebUI 测试 | 20+ vitest 文件 | ~10 个 TUI/Kanban 测试 |
| Benchmark | 无 | Kanban 延迟 + browser eval |
| 通道测试 | 36 个文件全覆盖 | ~5 个平台测试 |

### 主要缺口

1. **缺少批量评测能力**：没有类似 hermes-agent `batch_runner.py` 的并行批量数据生成引擎。如果要跑大规模评测，需要自行写脚本驱动。
2. **无任务级 scenario 评测集**：没有预设的评测场景目录，无法衡量 task completion rate。
3. **无 Live eval lane**：没有专门的真实模型/真实凭据评测通道。
4. **无基准性能测试**：没有启动时间、gateway 延迟、并发吞吐量的基准和 baseline 比较。
5. **无 LLM Judge 评测**：evaluate_response 功能单一（只做二元通知决策），没有开放式的 LLM judge 框架。
6. **无轨迹数据输出**：AgentRunResult 只在运行时存在，没有持久化到结构化文件用于离线分析。
7. **无增量评测机制**：每次从头执行测试，没有 checkpoint/resume 能力。
