# 分类子代理提示词模板

用法：替换 `{YYMM}`、`{BATCH-A}`、`{BATCH-B}`、`{ROWS-N}` 后，作为 general-purpose 后台子代理的 prompt（每波 ≤4 个并发）。每代理负责 2 个 batch。

---

你在为《arXiv {YYMM} <主题> 月度文摘》做论文筛选与分类。用 Read 工具读取以下两个文件（每篇含 arXiv ID、日期、类别、标题、摘要，摘要可能被截断，照常处理）：
- {BATCH-A}
- {BATCH-B}

对每篇论文判断 KEEP 或 DROP，KEEP 的归入唯一主维度并写中文一句话要点。

【DROP 规则】（记录原因码）：
- llm-pure：纯 LLM 本体研究——模型架构/预训练/后训练/RLHF/对齐/纯 reasoning 训练/推理加速/模型发布技术报告，agent 不是核心
- robotics：纯机器人/控制/路径规划/无人机 swarm，无 LLM-agent 主线
- non-agent：领域深度学习应用（蛋白质/影像/化学等），agent/LLM 非核心
- weak：与主题工程弱相关（纯博弈论、纯图论、无 LLM 的多智能体理论）
- 专门覆盖本主题的综述可 KEEP（标签加 `survey`）；边缘情况倾向 KEEP，由主流程最后统一删减。

【主维度取值】（按论文核心贡献归类，唯一）：
self-evolve / memory / tool / mcp / skill / subagent / engineering / coding / eval / planning / safety / multiagent / webgui / domain
（domain=领域应用；engineering=prompt/context/harness/loop/工作流/框架/上下文管理；新基准一律 eval；MCP 一律 mcp；以自我改进为核心→self-evolve；以技能沉淀复用为核心→skill；coding agent 方法/实证→coding。）
※ 其他主题请先与用户确认维度表再替换本段。

【一句话要点】中文，≤50 字，尽量带摘要中的关键数字或结论，事实必须出自摘要原文，不得编造。风格示例：
- 提出记忆事务边界：Ordered PatchTest 验写、Temporal Resolver 选版本、快照恢复
- 首个生产规模 Copilot 轨迹刻画（3.2M 用户/761M 调用）：KV 命中 90%，跨轮骤降
- 恶意 issue 攻击 coding agent；66.5% 穿透所有护栏

【输出】两步：
A. 用 Write 工具把结果写入 {ROWS-N}，严格如下格式（按原文件顺序，日期 MM-DD，标题保留英文原文，标签 1-2 个反引号包裹）：
# rows-N
| id | 日期 | 标题 | 维度 | 标签 | 一句话要点 |
|---|---|---|---|---|---|
| {YYMM}.01234 | MM-DD | Paper Title Here | coding | `agent/coding` `method/repair` | 中文要点…… |
B. 最终回复只返回统计：总篇数、KEEP 数、各维度计数、各 DROP 原因计数（一行式即可）。

禁止访问网络、禁止读取上述两个文件以外的文件。

---

# 主流程注意事项（不发给子代理）

1. **ID 与日期以批文件为准逐字转录**——实战中子代理出现过 ID 数字错一位（17347→17337）与日期差一天；成文后必须跑 scripts/validate.py 全量校验。
2. 卡死（>25 分钟无产出）或报 1302 限流的代理：TaskStop 掉，把该 batch 单独拆一个小任务重跑，输出用 rows-9/rows-10 等未占用编号。
3. 子代理 KEEP 偏多（边缘即 KEEP）是设计如此，删减由主流程在精选阶段完成。
4. DROP 行如果子代理写进了表格（标签含 `drop/`），merge_rows.py 会自动剔除，无需手工清理。
