# AI Agent记忆系统横向分析

最近连续看了几个 AI Agent 项目的记忆设计：`nanobot`、`OpenClaw`、`Hermes-Agent`，也顺手对照了 Codex 和 Claude Code 这类编程助手的项目记忆机制。

看下来有一个很清晰的趋势：Agent 的记忆不只是“保存聊天记录”。真正有价值的记忆系统，要解决的是三个问题：

1. 什么信息值得长期保存？
2. 旧上下文如何被压缩、召回和沉淀？
3. 自动记忆如何避免污染系统提示、泄漏隐私或误导未来行为？

这篇文章做一个横向梳理。

---

## 为什么 Agent 需要记忆

普通 LLM 的“记忆”主要来自上下文窗口。窗口内的内容可以参考，窗口外的内容就消失了。

Agent 不一样。Agent 要完成长期任务，就必须有跨会话连续性：

- 记住用户偏好
- 记住项目约定
- 记住已经做过的决策
- 记住某些失败经验
- 在新会话中召回旧上下文
- 在上下文压缩前保存重要信息

所以 Agent 的记忆系统一般会分成两类：

- **短期记忆**：当前会话、当前任务、当前上下文窗口
- **长期记忆**：跨会话保存的偏好、事实、决策和经验

不同项目的差异，主要在于“短期如何变长期”“长期如何被召回”“哪些内容允许自动写入”。

---

## nanobot：从历史压缩到 Dream 巩固

![[nanobot-memory.svg]]

`nanobot` 的记忆系统很有代表性。它不是把所有内容塞进一个大文件，而是分成多个层次：

- `session.messages`：当前会话的短期上下文
- `memory/history.jsonl`：压缩后的历史摘要
- `SOUL.md`：Agent 的长期语气和沟通风格
- `USER.md`：关于用户的稳定信息
- `memory/MEMORY.md`：项目事实、决策和长期上下文
- `GitStore`：记录长期记忆文件的版本变化

它的核心流程是两步。

第一步是 **Consolidator**。当上下文变长时，系统会把旧消息中相对安全的一段压缩成摘要，追加到 `memory/history.jsonl`。这个文件是机器友好的 JSONL，有 cursor，可以增量处理。

第二步是 **Dream**。Dream 会定期读取新的历史摘要，再结合现有的 `SOUL.md`、`USER.md` 和 `MEMORY.md`，对长期记忆做小范围、可解释的编辑。

这个设计的优点是：短期会话不会无限膨胀，长期记忆也不是简单堆积，而是经过“梦境式”的二次整理。

我觉得 nanobot 最值得借鉴的是这个分层：

- `history.jsonl` 负责“发生过什么”
- `MEMORY.md` 负责“现在仍然重要什么”
- `USER.md` 负责“用户是谁、偏好是什么”
- `SOUL.md` 负责“Agent 应该如何表达自己”

这让记忆不只是归档，而是逐渐形成可用的长期理解。

---

## OpenClaw：文件为真，索引加速，插件可替换

![[openclaw-memory.svg]]

`OpenClaw` 的记忆系统更工程化。

它的用户侧模型很清晰：

- `MEMORY.md`：长期稳定记忆，启动时会进入上下文
- `memory/YYYY-MM-DD.md` 或 `memory/*.md`：日常工作记忆、会话摘要、观察记录
- `DREAMS.md`：dreaming 巩固过程中的人类审阅面
- `memory_search` / `memory_get`：检索和读取记忆的工具

OpenClaw 的核心思路可以概括成一句话：

> 文件为真，索引加速，工具召回，后台巩固，插件可替换。

也就是说，长期可信内容仍然是 Markdown 文件，但检索不靠模型“硬读全文”，而是通过索引系统。

默认的 `memory-core` 后端使用 SQLite、FTS 和 embedding 做 hybrid search。没有 embedding provider 时，可以走关键词检索；有 embedding provider 时，可以结合向量相似度和关键词匹配。

它还支持不同 memory backend，例如 builtin、QMD、Honcho、LanceDB，以及 Memory Wiki 这类知识库层。

OpenClaw 另一个值得注意的点是 **action-sensitive memories**。有些记忆不是普通事实，而会影响未来行为，比如：

- 某个任务暂时不要继续
- 某个结论来自不可信来源
- 某个授权只在特定条件下有效
- 某个约束有过期时间

这类记忆不能只写“用户说了 X”，还要写清楚“什么时候能行动、什么时候不能行动、谁是来源、何时失效”。

这说明 OpenClaw 对记忆的理解已经不只是“信息保存”，而是“未来行为约束”。

---

## Hermes-Agent：显式记忆 + 外部 Memory Provider

![[hermes-memory.svg]]

`Hermes-Agent` 的记忆方案是双层结构：

第一层是内置显式记忆。它有本地 `MEMORY.md` 和 `USER.md`，用于保存高信任、人工精选的内容：

- 用户偏好
- 项目约定
- 工具使用经验
- 长期事实

这些内容会在会话开始时形成 frozen snapshot，注入系统提示。中途即使写入文件，也不会立刻改变当前系统提示，这样可以保护 prefix cache 的稳定性。

第二层是外部语义记忆 Provider。Hermes 定义了 `MemoryProvider` 接口，由 `MemoryManager` 统一管理。Provider 可以负责：

- 每轮前召回相关上下文
- 每轮后同步用户和助手内容
- 会话结束时抽取事实
- 压缩前保存信息
- 处理会话切换
- 提供额外工具

Hermes 的一个务实选择是：同时只允许一个外部 provider。这样牺牲了一些组合能力，但避免多个记忆后端同时暴露工具、同时召回内容，导致 schema 变胖、语义冲突和延迟上升。

更重要的是，Hermes 在安全边界上做得比较细：

- 内置记忆写入和加载时会扫描 prompt injection / exfiltration 风险
- 记忆注入使用 frozen snapshot
- 外部召回内容会包进 `<memory-context>`
- 流式输出有 scrubber，防止模型把内部记忆上下文泄漏到用户界面
- provider 失败通常是 best-effort，不阻塞主对话

这套设计说明，记忆系统一旦自动化，就必须认真处理“记忆污染”和“记忆泄漏”。

---

## Codex 与 Claude Code：项目记忆和自动 Memories

![[codex-claude-memory.svg]]

对编程助手来说，最常见的“记忆”不是复杂数据库，而是项目规则文件。

Claude Code 有 `CLAUDE.md`，Codex 对应的是 `AGENTS.md`。这类文件适合保存：

- 项目结构说明
- 测试命令
- 代码风格
- 开发约定
- 注意事项
- Agent 在当前仓库中应该遵守的规则

这类记忆最大的优点是稳定、可见、可版本管理。它不像自动记忆那样神秘，也不会因为某次对话误判而悄悄改变行为。

Codex 现在还有自动 Memories 机制，可以从历史线程中提炼偏好、工作流、技术栈和项目约定，保存到本地，再在未来线程中注入。它更像跨线程个人记忆。

所以可以这样理解：

- `AGENTS.md` / `CLAUDE.md`：显式项目记忆
- Codex Memories：自动跨线程记忆
- Chronicle：更主动、更权限敏感的上下文辅助记忆

对于工程项目，我仍然建议优先维护 `AGENTS.md` 这种显式规则文件。自动 Memories 更适合补充个人偏好和长期工作流，而不是承载关键项目约束。

---

## 横向对比

![[memory-systems-comparison.svg]]

| 项目 | 核心设计 | 适合保存 | 主要特点 |
|---|---|---|---|
| nanobot | `history.jsonl` + Dream + `SOUL.md` / `USER.md` / `MEMORY.md` | 历史摘要、用户画像、项目事实、Agent 风格 | 强调从会话历史中逐步沉淀长期记忆 |
| OpenClaw | `MEMORY.md` + `memory/*.md` + hybrid search + dreaming + 插件后端 | 长期事实、日常笔记、可检索上下文、行为约束 | 工程化程度高，文件为真，索引和插件增强召回 |
| Hermes-Agent | 本地显式记忆 + 外部 MemoryProvider | 高信任本地事实、外部语义记忆、跨会话召回 | 安全边界清晰，provider 生命周期完整 |
| Codex / Claude Code | `AGENTS.md` / `CLAUDE.md` + 自动 memories | 项目规则、开发约定、用户偏好 | 显式规则文件最稳定，自动记忆作为补充 |

---

## 我看到的设计原则

### 1. 文件仍然是最可信的长期记忆

无论是 `MEMORY.md`、`USER.md`、`AGENTS.md` 还是 `CLAUDE.md`，这些纯文本文件都有一个共同点：用户能直接查看、编辑、审计和版本管理。

这比完全隐藏在数据库里的自动记忆更可靠。

### 2. 历史不等于记忆

聊天历史只是原材料。真正的记忆需要压缩、去重、判断重要性，并转化成未来可用的事实或规则。

`nanobot` 的 `history.jsonl -> Dream -> MEMORY.md`，以及 OpenClaw 的 dreaming promotion，都是在解决这个问题。

### 3. 召回应该和注入分开

长期记忆可以很多，但每次注入上下文的内容必须少而准。

好的系统会把“存储”和“召回”分开：

- 存储层可以大
- 索引层负责找相关内容
- prompt 注入层只放当前任务需要的部分

OpenClaw 的 `memory_search` / `memory_get` 和 Hermes 的 `prefetch()` 都是这种思路。

### 4. 自动记忆必须可审计、可回滚

Agent 自动写长期记忆很强大，但也很危险。

如果一次误判把错误偏好、过期事实或恶意内容写进长期记忆，未来会不断放大影响。

所以比较成熟的设计都会提供：

- 写入日志
- 版本记录
- 人类审阅面
- restore / rollback
- threat pattern 扫描
- 对行动型记忆标注边界

### 5. 记忆不只是事实，也是行为约束

“用户喜欢 TypeScript”是普通事实。

“这个迁移计划还没批准，未来会话不要直接改实现”就是行为约束。

后者如果没有写清楚边界，Agent 很容易在未来做错事。

这也是为什么 OpenClaw 提到 action-sensitive memories 很重要。

---

## 一个实用建议

如果要给自己的 AI Coding Agent 或个人知识库设计记忆系统，可以从三层开始：

### 第一层：显式项目记忆

放在仓库根目录：

- `AGENTS.md`
- `MEMORY.md`
- `USER.md`

保存稳定规则、项目约定、用户偏好和长期事实。

### 第二层：日常工作记忆

放在 `memory/` 目录：

- 每日记录
- 会话摘要
- 临时观察
- 方案对比
- 失败经验

这层不必每次全量注入 prompt，但应该可以被搜索。

### 第三层：自动巩固

用 Dream / consolidation / summarization 定期做：

- 压缩历史
- 提炼长期事实
- 去重和清理陈旧内容
- 标注不确定信息
- 生成可审阅日志

这三层组合起来，就能兼顾透明性、连续性和自动化。

---

## 结语

Agent 记忆系统的目标，不是让模型“什么都记住”。

真正好的记忆系统，应该像一个可靠的工作笔记：

- 重要的留下
- 过期的淡出
- 不确定的标注来源
- 会影响行动的写清边界
- 用户始终可以查看、修改和回滚

从 `nanobot`、`OpenClaw`、`Hermes-Agent` 到 Codex / Claude Code，可以看到一个共同方向：长期记忆越来越倾向于“透明文件 + 可检索索引 + 可审计自动巩固”。

这可能也是 AI Agent 从一次性聊天工具走向长期工作伙伴时，最基础的一块能力。
