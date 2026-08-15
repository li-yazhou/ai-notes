# 用 Claude 3.5 Sonnet 刷新 SWE-bench Verified 基准（中英对照）

> **原文标题：** Raising the bar on SWE-bench Verified with Claude 3.5 Sonnet
> **作者：** Erik Schluntz（Anthropic 工程团队）
> **原文链接：** https://www.anthropic.com/engineering/swe-bench-sonnet
> **发布日期：** 2025-01-06
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

*Our latest model, the upgraded [Claude 3.5 Sonnet](https://www.anthropic.com/news/3-5-models-and-computer-use), achieved 49% on SWE-bench Verified, a software engineering evaluation, beating the previous state-of-the-art model's 45%. This post explains the "agent" we built around the model, and is intended to help developers get the best possible performance out of Claude 3.5 Sonnet.*

*我们最新的模型——升级版 [Claude 3.5 Sonnet](https://www.anthropic.com/news/3-5-models-and-computer-use)——在软件工程评测 SWE-bench Verified 上取得了 49% 的成绩，超过了此前最先进模型的 45%。这篇文章解释了我们在模型周围构建的"Agent"，旨在帮助开发者从 Claude 3.5 Sonnet 中榨出最佳性能。*

[SWE-bench](https://www.swebench.com/) is an AI evaluation benchmark that assesses a model's ability to complete real-world software engineering tasks. Specifically, it tests how the model can resolve GitHub issues from popular open-source Python repositories. For each task in the benchmark, the AI model is given a set up Python environment and the checkout (a local working copy) of the repository from just before the issue was resolved. The model then needs to understand, modify, and test the code before submitting its proposed solution.

[SWE-bench](https://www.swebench.com/) 是一个 AI 评测基准，评估模型完成真实世界软件工程任务的能力。具体来说，它测试模型如何解决热门开源 Python 仓库中的 GitHub issue。对于基准中的每个任务，AI 模型都会获得一个配置好的 Python 环境，以及该 issue 被解决前一刻的仓库检出（checkout，即本地工作副本）。随后，模型需要理解、修改并测试代码，然后提交它提出的解决方案。

Each solution is graded against the real unit tests from the pull request that closed the original GitHub issue. This tests whether the AI model was able to achieve the same functionality as the original human author of the PR.

每个解决方案都会对照关闭原始 GitHub issue 的那个 pull request 中的真实单元测试进行评分。这测试了 AI 模型是否能够实现与原 PR 人类作者相同的功能。

SWE-bench doesn't just evaluate the AI model in isolation, but rather an entire "agent" system. In this context, an "agent" refers to the combination of an AI model and the software scaffolding around it. This scaffolding is responsible for generating the prompts that go into the model, parsing the model's output to take action, and managing the interaction loop where the result of the model's previous action is incorporated into its next prompt. The performance of an agent on SWE-bench can vary significantly based on this scaffolding, even when using the same underlying AI model.

SWE-bench 不只是孤立地评测 AI 模型，而是评测整个"Agent"系统。在这个语境下，"Agent"指的是 AI 模型与它周围的软件脚手架（scaffolding）的组合。这个脚手架负责生成进入模型的提示词、解析模型输出以采取行动，并管理交互循环——在这个循环里，模型上一次动作的结果会被纳入它的下一个提示词。Agent 在 SWE-bench 上的表现会因这个脚手架的不同而显著变化，即使使用的是同一个底层 AI 模型。

There are many other benchmarks for the coding abilities of Large Language Models, but SWE-bench has gained in popularity for several reasons:

衡量大语言模型编码能力的基准还有很多，但 SWE-bench 之所以广受欢迎，有以下几个原因：

1. It uses real engineering tasks from actual projects, rather than competition- or interview-style questions;
2. 它使用来自真实项目的真实工程任务，而非竞赛或面试风格的问题；
3. It is not yet saturated—there's plenty of room for improvement. No model has yet crossed 50% completion on SWE-bench Verified (though the updated Claude 3.5 Sonnet is, at the time of writing, at 49%);
4. 它尚未饱和——还有很大的提升空间。还没有模型在 SWE-bench Verified 上突破 50% 的完成率（尽管在撰写本文时，更新版 Claude 3.5 Sonnet 已达到 49%）；
5. It measures an entire "agent", rather than a model in isolation. Open-source developers and startups have had great success in optimizing scaffoldings to greatly improve the performance around the same model.
6. 它测量的是整个"Agent"，而非孤立的模型。开源开发者和初创公司在优化脚手架方面取得了巨大成功，围绕同一个模型大幅提升了性能。

Note that the original SWE-bench dataset contains some tasks that are impossible to solve without additional context outside of the GitHub issue (for example, about specific error messages to return). [SWE-bench-Verified](https://openai.com/index/introducing-swe-bench-verified/) is a 500 problem subset of SWE-bench that has been reviewed by humans to make sure they are solvable, and thus provides the most clear measure of coding agents' performance. This is the benchmark to which we'll refer in this post.

请注意，原始 SWE-bench 数据集包含一些任务，如果缺少 GitHub issue 之外的额外上下文（例如关于要返回的特定错误消息）就无法解决。[SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/) 是 SWE-bench 的一个 500 题子集，经过人工审核以确保题目可解，因此提供了对编码 Agent 性能最清晰的度量。本文所指的就是这个基准。

# 达到最先进水平（Achieving state-of-the-art）

## 使用工具（Tool Using Agent）的 Agent

Our design philosophy when creating the agent scaffold optimized for updated Claude 3.5 Sonnet was to give as much control as possible to the language model itself, and keep the scaffolding minimal. The agent has a prompt, a Bash Tool for executing bash commands, and an Edit Tool, for viewing and editing files and directories. We continue to sample until the model decides that it is finished, or exceeds its 200k context length. This scaffold allows the model to use its own judgment of how to pursue the problem, rather than be hardcoded into a particular pattern or workflow.

在为更新版 Claude 3.5 Sonnet 优化创建 Agent 脚手架时，我们的设计理念是：把尽可能多的控制权交给语言模型本身，并让脚手架保持极简。这个 Agent 有一个提示词、一个用于执行 bash 命令的 Bash 工具，以及一个用于查看和编辑文件与目录的 Edit 工具。我们会持续采样，直到模型决定自己已完成，或者超出它的 20 万上下文长度。这个脚手架让模型能够用自己的判断来决定如何解决问题，而不是被硬编码进某种特定的模式或工作流。

The prompt outlines a suggested approach for the model, but it's not overly long or too detailed for this task. The model is free to choose how it moves from step to step, rather than having strict and discrete transitions. If you are not token-sensitive, it can help to explicitly encourage the model to produce a long response.

提示词为模型勾勒了一个建议的方法，但对这个任务来说，它并不过长或过细。模型可以自由选择如何在步骤之间推进，而不是有严格而离散的转换。如果你对令牌不敏感，明确鼓励模型产生一个较长的响应会有所帮助。

The following code shows the prompt from our agent scaffold:

下面的代码展示了我们 Agent 脚手架中的提示词：

```text
<uploaded_files>
{location}
</uploaded_files>
I've uploaded a python code repository in the directory {location} (not in /tmp/inputs). Consider the following PR description:

<pr_description>
{pr_description}
</pr_description>

Can you help me implement the necessary changes to the repository so that the requirements specified in the <pr_description> are met?
I've already taken care of all changes to any of the test files described in the <pr_description>. This means you DON'T have to modify the testing logic or any of the tests in any way!

Your task is to make the minimal changes to non-tests files in the {location} directory to ensure the <pr_description> is satisfied.

Follow these steps to resolve the issue:
1. As a first step, it might be a good idea to explore the repo to familiarize yourself with its structure.
2. Create a script to reproduce the error and execute it with `python <filename.py>` using the BashTool, to confirm the error
3. Edit the sourcecode of the repo to resolve the issue
4. Rerun your reproduce script and confirm that the error is fixed!
5. Think about edgecases and make sure your fix handles them as well

Your thinking should be thorough and so it's fine if it's very long.
```

The model's first tool executes Bash commands. The schema is simple, taking only the command to be run in the environment. However, the description of the tool carries more weight. It includes more detailed instructions for the model, including escaping inputs, lack of internet access, and how to run commands in the background.

模型的第一个工具执行 bash 命令。它的 schema 很简单，只接受要在环境中运行的命令。然而，这个工具的描述承担了更重的分量。它包含了对模型更详细的指示，包括转义输入、无互联网访问，以及如何在后台运行命令。

Next, we show the spec for the Bash Tool:

接下来，我们展示 Bash 工具的规格：

```json
{
   "name": "bash",
   "description": "Run commands in a bash shell\n
* When invoking this tool, the contents of the \"command\" parameter does NOT need to be XML-escaped.\n
* You don't have access to the internet via this tool.\n
* You do have access to a mirror of common linux and python packages via apt and pip.\n
* State is persistent across command calls and discussions with the user.\n
* To inspect a particular line range of a file, e.g. lines 10-25, try 'sed -n 10,25p /path/to/the/file'.\n
* Please avoid commands that may produce a very large amount of output.\n
* Please run long lived commands in the background, e.g. 'sleep 10 &' or start a server in the background.",
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "description": "The bash command to run."
           }
       },
       "required": ["command"]
   }
}
```

The model's second tool (the Edit Tool) is much more complex, and contains everything the model needs for viewing, creating, and editing files. Again, our tool description contains detailed information for the model about how to use the tool.

模型的第二个工具（Edit 工具）要复杂得多，包含了模型查看、创建和编辑文件所需的一切。同样，我们的工具描述包含了对模型如何使用该工具的详细信息。

We put a lot of effort into the descriptions and specs for these tools across a wide variety of agentic tasks. We tested them to uncover any ways that the model might misunderstand the spec, or the possible pitfalls of using the tools, then edited the descriptions to preempt these problems. We believe that much more attention should go into designing tool interfaces for models, in the same way that a large amount of attention goes into designing tool interfaces for humans.

我们为各种 Agent 任务在这些工具的描述和规格上投入了大量精力。我们测试它们，以揭示模型可能误解规格的任何方式，或使用工具时可能的陷阱，然后编辑描述以预先规避这些问题。我们认为，为模型设计工具接口应该得到多得多的关注，就像为人类设计工具接口得到了大量关注一样。

The following code shows the description for our Edit Tool:

下面的代码展示了我们 Edit 工具的描述：

```json
{
   "name": "str_replace_editor",
   "description": "Custom editing tool for viewing, creating and editing files\n
* State is persistent across command calls and discussions with the user\n
* If `path` is a file, `view` displays the result of applying `cat -n`. If `path` is a directory, `view` lists non-hidden files and directories up to 2 levels deep\n
* The `create` command cannot be used if the specified `path` already exists as a file\n
* If a `command` generates a long output, it will be truncated and marked with `<response clipped>` \n
* The `undo_edit` command will revert the last edit made to the file at `path`\n
\n
Notes for using the `str_replace` command:\n
* The `old_str` parameter should match EXACTLY one or more consecutive lines from the original file. Be mindful of whitespaces!\n
* If the `old_str` parameter is not unique in the file, the replacement will not be performed. Make sure to include enough context in `old_str` to make it unique\n
* The `new_str` parameter should contain the edited lines that should replace the `old_str`",
...
```

One way we improved performance was to "error-proof" our tools. For instance, sometimes models could mess up relative file paths after the agent had moved out of the root directory. To prevent this, we simply made the tool always require an absolute path.

我们提升性能的一种方式是给工具"做错误防护"（error-proof）。例如，在 Agent 离开根目录之后，模型有时会搞乱相对文件路径。为了防止这一点，我们简单地让工具始终要求绝对路径。

We experimented with several different strategies for specifying edits to existing files and had the highest reliability with string replacement, where the model specifies `old_str` to replace with `new_str` in the given file. The replacement will only occur if there is exactly one match of `old_str`. If there are more or fewer matches, the model is shown an appropriate error message for it to retry.

我们尝试了几种不同的策略来指定对现有文件的编辑，发现字符串替换（string replacement）的可靠性最高——模型在给定文件中指定要替换成 `new_str` 的 `old_str`。只有当 `old_str` 恰好匹配一处时，替换才会发生。如果匹配处多于或少于一处，模型会看到一条相应的错误消息，让它重试。

The spec for our Edit Tool is shown below:

我们 Edit 工具的规格如下：

```json
...
   "input_schema": {
       "type": "object",
       "properties": {
           "command": {
               "type": "string",
               "enum": ["view", "create", "str_replace", "insert", "undo_edit"],
               "description": "The commands to run. Allowed options are: `view`, `create`, `str_replace`, `insert`, `undo_edit`."
           },
           "file_text": {
               "description": "Required parameter of `create` command, with the content of the file to be created.",
               "type": "string"
           },
           "insert_line": {
               "description": "Required parameter of `insert` command. The `new_str` will be inserted AFTER the line `insert_line` of `path`.",
               "type": "integer"
           },
           "new_str": {
               "description": "Required parameter of `str_replace` command containing the new string. Required parameter of `insert` command containing the string to insert.",
               "type": "string"
           },
           "old_str": {
               "description": "Required parameter of `str_replace` command containing the string in `path` to replace.",
               "type": "string"
           },
           "path": {
               "description": "Absolute path to file or directory, e.g. `/repo/file.py` or `/repo`.",
               "type": "string"
           },
           "view_range": {
               "description": "Optional parameter of `view` command when `path` points to a file. If none is given, the full file is shown. If provided, the file will be shown in the indicated line number range, e.g. [11, 12] will show lines 11 and 12. Indexing at 1 to start. Setting `[start_line, -1]` shows all lines from `start_line` to the end of the file.",
               "items": {
                   "type": "integer"
               },
               "type": "array"
           }
       },
       "required": ["command", "path"]
   }
}
```

# 结果（Results）

In general, the upgraded Claude 3.5 Sonnet demonstrates higher reasoning, coding, and mathematical abilities than our prior models, and the [previous state-of-the-art](https://solverai.com/) model. It also demonstrates improved agentic capabilities: the tools and scaffolding help put those improved abilities to their best use.

总的来说，升级版 Claude 3.5 Sonnet 展现出比我们之前的模型和[此前的最高水平模型](https://solverai.com/)更强的推理、编码和数学能力。它还展现出更强的 Agent 能力：工具和脚手架帮助这些提升后的能力得到最充分的发挥。

| 模型（Model） | Claude 3.5 Sonnet（新版） | 此前最高水平（Previous SOTA） | Claude 3.5 Sonnet（旧版） | Claude 3 Opus |
| --- | --- | --- | --- | --- |
| SWE-bench Verified 分数 | 49% | 45% | 33% | 22% |

# Agent 行为示例（Examples of agent behavior）

For running the benchmark, we used the [SWE-Agent](https://swe-agent.com/) framework as a foundation for our agent code. In our logs below, we render the agent's text output, tool calls, and tool responses as THOUGHT, ACTION, and OBSERVATION, even though we don't constrain the model to a fixed ordering.

为了运行基准测试，我们以 [SWE-Agent](https://swe-agent.com/) 框架作为 Agent 代码的基础。在下面的日志中，我们把 Agent 的文本输出、工具调用和工具响应分别渲染为 THOUGHT（思考）、ACTION（动作）和 OBSERVATION（观察），尽管我们并没有把模型约束为固定的顺序。

The code blocks below will walk through a typical case of the Sonnet 3.5 solving a SWE-bench problem.

下面的代码块将逐步展示 Sonnet 3.5 解决一个 SWE-bench 问题的典型案例。

In this first block, you can see part of the initial prompt given to the model, with `{pr_description}` filled in with the real value from a SWE-bench task. Importantly, this task contains steps to reproduce the issue, which will give the model a valuable starting point to investigate.

在第一个代码块中，你可以看到给模型的初始提示词的一部分，其中 `{pr_description}` 已被填入一个 SWE-bench 任务的真实内容。重要的是，这个任务包含复现该 issue 的步骤，这将给模型一个宝贵的调查起点。

```text
<uploaded_files>
/repo
</uploaded_files>
I've uploaded a python code repository in the directory /repo (not in /tmp/inputs). Consider the following PR description:

<pr_description>
linear_model.RidgeClassifierCV's Parameter store_cv_values issue
#### Description
Parameter store_cv_values error on sklearn.linear_model.RidgeClassifierCV

#### Steps/Code to Reproduce
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, 
                                         store_cv_values = True).fit(x, y)

#### Expected Results
Expected to get the usual ridge regression model output, keeping the cross validation predictions as attribute.

#### Actual Results
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'

lm.RidgeClassifierCV actually has no parameter store_cv_values, even though some attributes depends on it.
```

The model responds and first uses the Edit Tool to view the repository structure. You can see the model's text output and tool call arguments under THOUGHT and ACTION, and part of the tool's output under OBSERVATION:

模型作出回应，首先用 Edit 工具查看仓库结构。你可以在 THOUGHT 和 ACTION 下看到模型的文本输出和工具调用参数，在 OBSERVATION 下看到工具的部分输出：

```text
THOUGHT:
I'll help you implement the changes to satisfy the PR description. Let's follow the steps you outlined.

1. First, let's explore the repo structure:
ACTION (str_replace_editor):
command:
view

path:
/repo

OBSERVATION:
Here's the files and directories up to 2 levels deep in /repo, excluding hidden items:
/repo
/repo/PULL_REQUEST_TEMPLATE.md
/repo/ISSUE_TEMPLATE.md
/repo/sklearn
/repo/sklearn/decomposition
/repo/sklearn/kernel_ridge.py
/repo/sklearn/model_selection
/repo/sklearn/covariance
/repo/sklearn/cluster
/repo/sklearn/base.py
/repo/sklearn/dummy.py
/repo/sklearn/naive_bayes.py
...
```

Now that the model has a better understanding of the repository structure, it uses the Edit Tool to create a new script that it will use to reproduce the issue and test its fix:

现在模型对仓库结构有了更好的理解，它用 Edit 工具创建一个新脚本，用来复现该 issue 并测试它的修复：

```text
THOUGHT:
Based on the repository structure, we'll need to modify the Ridge Classifier in the `sklearn/linear_model` directory.

Let's create a script to reproduce the error:
ACTION (str_replace_editor):
command:
create

path:
/repo/reproduce_error.py

file_text:
import numpy as np
from sklearn import linear_model as lm

#test database
n = 100
x = np.random.randn(n, 30)
y = np.random.normal(size = n)

rr = lm.RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, 
                         store_cv_values=True).fit(x, y)

OBSERVATION:
File created successfully at: /repo/reproduce_error.py
```

The model then uses the Bash Tool to execute the script it wrote, and successfully reproduces the issue from the task:

随后，模型用 Bash 工具执行它写的脚本，并成功复现了任务中的 issue：

```text
THOUGHT:
Let's verify that we can reproduce the error:
ACTION (bash):
command:
python3 /repo/reproduce_error.py

OBSERVATION:
Traceback (most recent call last):
  File "/repo/reproduce_error.py", line 10, in <module>
    store_cv_values=True).fit(x, y)
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
```

From here on, the model uses the Edit Tool to change the source code in the repository and reruns its script to verify whether the change has resolved the issue:

从这里开始，模型用 Edit 工具修改仓库中的源代码，并重新运行它的脚本，以验证这次改动是否解决了问题：

```text
THOUGHT:
The error is reproducible. Looking at the code, I can see that the issue is that while the `RidgeClassifierCV` class inherits from `_BaseRidgeCV`, it fails to pass the `store_cv_values` parameter from its constructor through to the base class constructor.

Let's fix this:
ACTION (str_replace_editor):
command:
str_replace

path:
/repo/sklearn/linear_model/ridge.py

old_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv)
        self.class_weight = class_weight

new_str:
    def __init__(self, alphas=(0.1, 1.0, 10.0), fit_intercept=True,
                 normalize=False, scoring=None, cv=None, class_weight=None,
                 store_cv_values=False):
        super(RidgeClassifierCV, self).__init__(
            alphas=alphas, fit_intercept=fit_intercept, normalize=normalize,
            scoring=scoring, cv=cv, store_cv_values=store_cv_values)
        self.class_weight = class_weight
```

In this particular example, the model worked for 12 steps before deciding that it was ready to submit. The task's tests then ran successfully, verifying that the model's solution addressed the problem. Some tasks took more than 100 turns before the model submitted its solution; in others, the model kept trying until it ran out of context.

在这个具体例子中，模型工作了 12 步才决定可以提交。随后，任务的测试成功运行，验证了模型的解决方案解决了问题。有些任务需要超过 100 轮，模型才提交它的解决方案；还有些任务，模型一直尝试到上下文耗尽为止。

From reviewing attempts from the updated Claude 3.5 Sonnet compared to older models, updated 3.5 Sonnet self-corrects more often. It also shows an ability to try several different solutions, rather than getting stuck making the same mistake over and over.

通过对比更新版 Claude 3.5 Sonnet 与旧模型的尝试，更新版 3.5 Sonnet 自我纠正的频率更高。它还展现出尝试几种不同解决方案的能力，而不是反复陷入同一个错误。

# 挑战（Challenges）

SWE-bench Verified is a powerful evaluation, but it's also more complex to run than simple, single-turn evals. These are some of the challenges that we faced in using it—challenges that other AI developers might also encounter.

SWE-bench Verified 是一个强大的评测，但它运行起来也比简单的单轮评测更复杂。以下是我们使用它时面临的一些挑战——其他 AI 开发者可能也会遇到。

1. **Duration and high token costs.** The examples above are from a case that was successfully completed in 12 steps. However, many successful runs took hundreds of turns for the model to resolve, and >100k tokens. The updated Claude 3.5 Sonnet is tenacious: it can often find its way around a problem given enough time, but that can be expensive;
2. **时长与高令牌成本。**上面的例子来自一个 12 步就成功完成的案例。然而，许多成功的运行需要模型解决数百轮，消耗超过 10 万令牌。更新版 Claude 3.5 Sonnet 很顽强：只要有足够的时间，它往往能找到解决问题的方法，但这可能很昂贵；
3. **Grading.** While inspecting failed tasks, we found cases where the model behaved correctly, but there were environment setup issues, or problems with install patches being applied twice. Resolving these systems issues is crucial for getting an accurate picture of an AI agent's performance.
4. **评分。**在检查失败的任务时，我们发现有些情况下模型的行为是正确的，但存在环境设置问题，或者安装补丁被应用了两次的问题。解决这些系统性问题，对于获得 AI Agent 性能的准确图景至关重要。
5. **Hidden tests.** Because the model cannot see the tests it's being graded against, it often "thinks" that it has succeeded when the task actually is a failure. Some of these failures are because the model solved the problem at the wrong level of abstraction (applying a bandaid instead of a deeper refactor). Other failures feel a little less fair: they solve the problem, but do not match the unit tests from the original task.
6. **隐藏测试。**由于模型看不到它被评分的测试，它常常"以为"自己成功了，而任务实际上是失败的。其中一些失败是因为模型在错误的抽象层级上解决了问题（贴了创可贴，而不是做更深入的代码重构）。另一些失败感觉没那么公平：它们解决了问题，但与原始任务中的单元测试不匹配。
7. **Multimodal.** Despite the updated Claude 3.5 Sonnet having excellent vision and multimodal capabilities, we did not implement a way for it to view files saved to the filesystem or referenced as URLs. This made debugging certain tasks (especially those from Matplotlib) especially difficult, and also prone to model hallucinations. There is definitely low-hanging fruit here for developers to improve upon—and SWE-bench has launched a new [evaluation focused on multi-modal tasks](https://www.swebench.com/multimodal.html). We look forward to seeing developers achieve higher scores on this eval with Claude in the near future.
8. **多模态。**尽管更新版 Claude 3.5 Sonnet 拥有出色的视觉和多模态能力，我们并没有实现让它查看保存到文件系统或通过 URL 引用的文件。这让调试某些任务（尤其是来自 Matplotlib 的任务）格外困难，而且容易引发模型的幻觉。这里肯定有开发者可以改进的"低垂果实"——SWE-bench 已经推出了一个新的[专注于多模态任务的评测](https://www.swebench.com/multimodal.html)。我们期待看到开发者们在不久的将来用 Claude 在这个评测上取得更高的分数。

The upgraded Claude 3.5 Sonnet achieved 49% on SWE-bench Verified, beating the previous state-of-the-art (45%), with a simple prompt and two general purpose tools. We feel confident that developers building with the new Claude 3.5 Sonnet will quickly find new, better ways to improve SWE-bench scores over what we've initially demonstrated here.

升级版 Claude 3.5 Sonnet 用一个简单的提示词和两个通用工具，在 SWE-bench Verified 上取得了 49% 的成绩，超过了此前的最高水平（45%）。我们相信，使用新版 Claude 3.5 Sonnet 进行构建的开发者，很快就会找到比我们在这里初步展示的更好、更新的方式来提升 SWE-bench 分数。

# 致谢（Acknowledgements）

Erik Schluntz optimized the SWE-bench agent and wrote this blog post. Simon Biggs, Dawn Drain, and Eric Christiansen helped implement the benchmark. Shauna Kravec, Dawn Drain, Felipe Rosso, Nova DasSarma, Ven Chandrasekaran, and many others contributed to training Claude 3.5 Sonnet to be excellent at agentic coding.

Erik Schluntz 优化了 SWE-bench Agent 并撰写了这篇博客。Simon Biggs、Dawn Drain 和 Eric Christiansen 帮助实现了该基准测试。Shauna Kravec、Dawn Drain、Felipe Rosso、Nova DasSarma、Ven Chandrasekaran 以及许多其他人共同贡献，把 Claude 3.5 Sonnet 训练成在 Agent 编码方面表现出色。
