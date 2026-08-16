# Claude 计算机与浏览器使用最佳实践（中英对照）

> **原文标题：** Best practices for computer and browser use with Claude
> **作者：** Lucas Gonzalez and Luca Weihs
> **原文链接：** https://claude.com/blog/best-practices-for-computer-and-browser-use-with-claude
> **发布日期：** 2026-05-13
> **翻译模型：** GLM-5.3
> 排版：每段英文原文在前，中文翻译紧随其后。术语保留英文原文并附中文释义。

---

Practical guidance for developers building computer and browser use integrations with the Claude model family.

为正在基于 Claude 模型家族构建计算机使用（computer use）与浏览器使用（browser use）集成的开发者提供的实用指南。

Claude's latest models represent a significant step forward in computer and browser use capabilities. Because of these features, LLMs are now able to power increasingly complex agentic systems that power real work, like building software applications and automating workflows across multiple, disparate technologies.

Claude 的最新模型在计算机使用与浏览器使用能力上迈出了重要一步。凭借这些特性，LLM 如今能够驱动日益复杂的 agentic 系统去完成真实工作，例如构建软件应用，以及跨多种迥异技术实现工作流自动化。

In this blog post, we share best practices for using Claude with computer and browser use, ranging from simple configuration changes to more advanced integration patterns. We hope this piece helps as you start integrating Claude's computer and browser use capabilities into your product. We are also releasing a new demo implementation which encapsulates some of these best practices and provides additional tools useful for developing on top of Claude's computer use capabilities.

在这篇博文中，我们分享将 Claude 用于计算机使用与浏览器使用的最佳实践，从简单的配置更改到更高级的集成模式。希望这篇文章能为你把 Claude 的计算机使用与浏览器使用能力集成到产品中提供帮助。我们还在同时发布一个新的演示实现（demo implementation），它封装了其中一些最佳实践，并提供了在 Claude 计算机使用能力之上进行开发时有用的附加工具。

Note that these recommendations apply to the Claude 4.6 family (Opus 4.6, Sonnet 4.6, Haiku 4.5) and Claude Opus 4.7 unless otherwise noted. Where guidance differs between the 4.6 family and Opus 4.7, we call it out inline. Our findings are based on internal experimentation and may be updated in the future as new models and techniques emerge.

请注意，除非另有说明，这些建议适用于 Claude 4.6 家族（Opus 4.6、Sonnet 4.6、Haiku 4.5）和 Claude Opus 4.7。当 4.6 家族与 Opus 4.7 的指导有所不同时，我们会在文中就地指出。我们的结论基于内部实验，未来随着新模型和新技术的出现可能会更新。

# 入门：分辨率与缩放（Getting started: resolution and scaling）

Click accuracy is the foundation of any computer use integration. If clicks don't land where they should, nothing downstream works: forms don't get filled, buttons don't get pressed, and workflows fail. The single highest impact optimization is also one of the simplest: pre downscale your screenshots before sending them to the API.

点击准确性是任何计算机使用集成的基石。如果点击没有落在该落的地方，下游一切都无从谈起：表单填不了、按钮按不了、工作流全线失败。影响最大的单项优化同时也是最简单的优化之一：在把截图发送给 API 之前预先降采样（downscale）。

# 确保缩放正确（Ensure proper scaling）

When you send a screenshot to Claude's Computer Use API, the model sees it and returns click coordinates in the display_width_px / display_height_px coordinate space you specified. But there's an important constraint: the API has internal processing limits on image size. Images that exceed these limits get downscaled before the model sees them, which means the model is clicking based on a degraded version of the image while your harness expects coordinates aligned to the original resolution.

当你向 Claude 的 Computer Use API 发送截图时，模型会查看它并在你指定的 display_width_px / display_height_px 坐标空间中返回点击坐标。但有一个重要约束：API 对图像尺寸有内部处理上限。超过这些上限的图像会在模型看到之前被降采样，这意味着模型是根据一个降质版的图像在点击，而你的 harness 却期望坐标对齐到原始分辨率。

For our Claude 4.6 model family, the API's limits are:

对于 Claude 4.6 模型家族，API 的限制为：

- Max long edge: 1568 pixels
- Max total pixels: 1.15 megapixels
- Images exceeding either limit get internally downscaled

- 最长边上限：1568 像素
- 总像素上限：115 万像素（1.15 megapixels）
- 超出任一上限的图像会被内部降采样

Our Opus 4.7 model supports higher resolution. The limits are:

我们的 Opus 4.7 模型支持更高的分辨率，其限制为：

- Max long edge: 2576 pixels
- Max total pixels: 3.75 megapixels
- Images exceeding either limit get internally downscaled

- 最长边上限：2576 像素
- 总像素上限：375 万像素（3.75 megapixels）
- 超出任一上限的图像会被内部降采样

When the coordinate space and the model's perceived image don't match, the model's predicted clicks land on a display scale different from the image it's actually seeing. This is the primary cause of click inaccuracy at high resolutions. The fix is straightforward: always downscale your screenshots to fit within these limits before sending them to the API. We consistently observe significant accuracy degradation when images exceed the limits, and this single change is worth more than almost any other optimization.

当坐标空间与模型实际感知的图像不一致时，模型预测的点击会落在一个与它实际看到的图像不同的显示尺度上。这就是高分辨率下点击不准确的主要原因。修复方法很简单：在把截图发送给 API 之前，始终先将其降采样到限制以内。我们持续观察到图像超限会导致显著的准确性下降，而仅这一项改动就比几乎任何其他优化都更有价值。

# 推荐分辨率（Recommended resolutions）

Start with 1280x720. This is a safe, practical default for most use cases. It uses about 80% of the pixel budget, stays well within both the long edge and total pixel limits, and is a standard resolution that models have seen during training. It works well for both modern web UIs and legacy desktop applications.

从 1280x720 开始。对大多数用例来说，这是一个安全、实用的默认值。它用掉约 80% 的像素预算，稳妥地落在最长边和总像素两项限制之内，而且是模型在训练中见过的标准分辨率。无论现代 Web UI 还是老式桌面应用，它都表现良好。

If you are using Opus 4.7, we recommend starting with 1080p, as this brings a meaningful quality lift over 720p and provides a good balance between token use and performance.

如果你使用的是 Opus 4.7，我们建议从 1080p 开始，因为相比 720p 它能带来实质性的质量提升，并在 token 用量与性能之间提供良好的平衡。

For developers who want to maximize the visual information the model receives, we also recommend a "max API fit" approach: computing the optimal resolution per-image based on the source's native aspect ratio:

对于希望最大化模型接收到的视觉信息的开发者，我们还推荐一种“最大适配 API（max API fit）”方法：根据源图像的原生宽高比逐图计算最优分辨率：

```python
import math

# 1568 for 4.6 family, 2576 for Opus 4.7
MAX_LONG_EDGE = 1568
# 1.15MP for 4.6 family, 3.75MP for Opus 4.7
MAX_PIXELS = 1_150_000


def compute_max_api_fit(native_w, native_h):
    """Compute the largest resolution that fits API limits while preserving aspect ratio."""
    aspect = native_w / native_h

    # Compute max dimensions from pixel budget
    h_from_pixels = math.sqrt(MAX_PIXELS / aspect)
    w_from_pixels = h_from_pixels * aspect

    # Apply long edge constraint
    if native_w >= native_h:
        w = min(w_from_pixels, MAX_LONG_EDGE)
        h = w / aspect
    else:
        h = min(h_from_pixels, MAX_LONG_EDGE)
        w = h * aspect

    # Never upscale beyond native
    w = min(w, native_w)
    h = min(h, native_h)

    return int(w), int(h)
```

This approach is slightly more complex but avoids aspect ratio distortion and uses the full pixel budget available for each image. The accuracy improvement over a fixed 1280x720 is modest, but it's a straightforward implementation that avoids the distortion that occurs when forcing a 16:9 source into a 4:3 display resolution.

这种方法稍显复杂，但能避免宽高比失真，并充分利用每张图像可用的像素预算。相比固定的 1280x720，其准确性提升有限，但实现起来直截了当，也避免了把 16:9 源图像强行塞进 4:3 显示分辨率时产生的失真。

Resolutions to avoid:

应避免的分辨率：

- Native resolution (unscaled): Unless your source images happen to be below the resolution limits, sending native resolution screenshots is the most common cause of poor click accuracy.
- Very low resolutions (below 960x540): With low resolution images, too much detail is lost for the model to accurately identify small UI elements.
- If on MacOS: A common issue for browser use is that the screenshots on MacOS are often captured with a device pixel ratio of 2, which means that you can end up with images that are 2x the resolution of the screen coordinates.
- If you are on the 4.6 family, avoid 1920x1080 and above: These exceed the pixel limit and will be silently downscaled. On Opus 4.7 the ceiling is higher (3.75 MP), so 1080p and 1440p is within budget; still avoid native 4K without downscaling.

- 原生分辨率（未缩放）：除非你的源图像恰好低于分辨率限制，否则发送原生分辨率截图是点击准确性差的最常见原因。
- 极低分辨率（低于 960x540）：低分辨率图像会丢失过多细节，模型无法准确识别小型 UI 元素。
- 如果在 MacOS 上：浏览器使用的一个常见问题是，MacOS 截图常以设备像素比（device pixel ratio）2 捕获，这意味着你最终得到的图像分辨率可能是屏幕坐标分辨率的 2 倍。
- 如果使用 4.6 家族，避免 1920x1080 及以上：这些超出像素上限，会被静默降采样。Opus 4.7 的上限更高（3.75 MP），1080p 和 1440p 都在预算之内；但仍要避免不做降采样的原生 4K。

# 坐标缩放（Coordinate scaling）

When you resize a screenshot before sending it, the model returns click coordinates in the display resolution you specified. You must scale these back to your actual screen resolution before executing the click:

当你在发送前调整了截图尺寸，模型会以你指定的显示分辨率返回点击坐标。在执行点击之前，你必须把这些坐标换算回实际的屏幕分辨率：

```python
# Your screen is screen_w x screen_h
# You sent a screenshot resized to display_w x display_h
scale_x = screen_w / display_w
scale_y = screen_h / display_h

screen_x = int(api_returned_x * scale_x)
screen_y = int(api_returned_y * scale_y)
```

This is straightforward but critical, because if you forget to scale or display_width_px / display_height_px don't match the actual dimensions of the image you sent, every click will be consistently offset

这一步简单却至关重要：如果你忘了换算，或者 display_width_px / display_height_px 与你实际发送图像的尺寸不符，每一次点击都会朝着同一方向持续偏移。

# messages 数组中的内容顺序（Content ordering in the messages array）

When constructing your messages content array, place the text instruction before the image, as depicted in the code snippet below. This lets the model know what it's looking for as it processes the screenshot, which improves click accuracy.

在构造 messages 内容数组时，把文本指令放在图像之前，如下方代码片段所示。这样模型在处理截图时就知道自己要找什么，从而提升点击准确性。

```python
# RECOMMENDED - text instruction first, then screenshot:
content = [
    {"type": "text", "text": "Click on the Submit button"},
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}},
]

# NOT RECOMMENDED - image first, then text:
content = [
    {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": screenshot_b64}},
    {"type": "text", "text": "Click on the Submit button"},
]
```

# 诊断点击问题（Diagnosing click issues）

If clicks are missing their targets, it often boils down to one of the causes, below:

如果点击总是偏离目标，原因往往可以归结为以下几种之一：

| Symptom | Likely causes | Try this |
| --- | --- | --- |
| Clicks consistently offset in one direction | - display_width_px / display_height_px don't match the actual image dimensions sent<br>- Screenshot exceeds API limits and is being silently downscaled<br>- Content ordering is image-first instead of text-first | - Ensure display dimensions exactly match your resized screenshot, not your native resolution<br>- Pre-downscale to 1280x720 or use compute_max_api_fit<br>- Move text instruction before the image in the content array |
| Clicks land in roughly the right area but miss the target | - Target is very small (checkbox, icon, toggle)<br>- Source image was very high resolution (4K+) and detail was lost during downscaling<br>- Aspect ratio distortion from forcing a non-native aspect ratio | - Enable enable_zoom: True for dense UIs<br>- Capture at a lower DPI or crop to the relevant screen region before downscaling<br>- Preserve the source aspect ratio when resizing |
| Model clicks the wrong element entirely | - Ambiguous instruction ("click Submit" when multiple submit-like buttons exist)<br>- Visually similar elements near the target<br>- UI is too complex for a single instruction | - Use more specific prompts with positional context ("click the blue Submit button in the bottom-right of the form")<br>- Break complex interactions into smaller steps<br>- Provide additional context about the page layout |
| Accuracy is poor across the board | - Screenshots are being sent above API limits<br>- Source images are from very high-resolution displays (4K+) with extreme compression ratios<br>- Resolution is too low, losing critical detail | - Pre-downscale all screenshots to fit within limits<br>- For 4K+ sources on the 4.6 family, Sonnet is more robust to heavy downscaling than Opus 4.6. On Opus 4.7 this gap largely closes, use the 4.7 pixel budget (up to 3.75 MP) so less downscaling is needed in the first place.<br>- Try 1280x720 as a baseline; if too lossy, use compute_max_api_fit |

| 症状 | 可能原因 | 试试这些 |
| --- | --- | --- |
| 点击始终朝同一方向偏移 | - display_width_px / display_height_px 与实际发送的图像尺寸不符<br>- 截图超过 API 上限，正被静默降采样<br>- 内容顺序是图像在前而非文本在前 | - 确保显示尺寸与你缩放后的截图完全一致，而不是原生分辨率<br>- 预先降采样到 1280x720，或使用 compute_max_api_fit<br>- 把文本指令移到内容数组中图像之前 |
| 点击落点大致正确但偏离目标 | - 目标非常小（复选框、图标、开关）<br>- 源图像分辨率非常高（4K+），降采样时细节丢失<br>- 强制使用非原生宽高比导致的宽高比失真 | - 对密集 UI 启用 enable_zoom: True<br>- 以较低的 DPI 捕获，或先裁剪到相关屏幕区域再降采样<br>- 缩放时保持源图像宽高比 |
| 模型完全点错了元素 | - 指令含糊（存在多个类似“提交”按钮时却说“点击提交”）<br>- 目标附近存在视觉上相似的元素<br>- UI 过于复杂，单条指令不足以描述 | - 使用更具体、带位置上下文的提示词（“点击表单右下角的蓝色 Submit 按钮”）<br>- 把复杂交互拆分成更小的步骤<br>- 提供关于页面布局的额外上下文 |
| 准确性整体很差 | - 发送的截图超过 API 上限<br>- 源图像来自超高分辨率显示器（4K+），压缩比极大<br>- 分辨率过低，丢失关键细节 | - 把所有截图预先降采样到限制以内<br>- 对 4.6 家族的 4K+ 源图像，Sonnet 比 Opus 4.6 更耐受重度降采样。在 Opus 4.7 上这一差距已基本消除，请使用 4.7 的像素预算（最高 3.75 MP），从一开始就减少降采样。<br>- 以 1280x720 为基线尝试；如果损失过大，改用 compute_max_api_fit |

# 点击任务的模型选择（Model selection for clicking tasks）

Based on our internal testing, Claude Sonnet 4.6 tends to be more mechanically precise at clicking (better spatial accuracy, fewer near misses) while Claude Opus 4.6 brings stronger reasoning. Sonnet 4.6 is also more robust when source images require heavy downscaling.

根据我们的内部测试，Claude Sonnet 4.6 在点击上往往机械精度更高（空间准确性更好、擦边失误更少），而 Claude Opus 4.6 带来更强的推理能力。当源图像需要重度降采样时，Sonnet 4.6 也更稳健。

Opus 4.7 narrows this gap: Through testing, we have found its clicking precision is roughly on par with Sonnet 4.6, and its higher resolution budget reduces the amount of downscaling needed in the first place, making it a strong choice when you want Opus-level reasoning paired with strong click accuracy.

Opus 4.7 缩小了这一差距：通过测试，我们发现它的点击精度与 Sonnet 4.6 大致相当，而其更高的分辨率预算从一开始就减少了所需的降采样量。因此，当你既想要 Opus 级别的推理、又想要出色的点击准确性时，它是一个有力的选择。

For most tasks, we recommend starting with Sonnet 4.6, which provides the best balance of clicking accuracy, reasoning, and cost. Choose Opus 4.7 when you want stronger reasoning, particularly if using high-resolution source images. Haiku 4.5 remains an excellent option when latency is the priority. Advanced workflows may still benefit from an orchestrator + sub-agent pattern where a reasoning model handles planning and decision-making while Sonnet or Haiku executes the mechanical clicking steps.

对大多数任务，我们建议从 Sonnet 4.6 开始，它在点击准确性、推理和成本之间提供了最佳平衡。当你需要更强推理时选择 Opus 4.7，尤其是在使用高分辨率源图像的情况下。当延迟优先时，Haiku 4.5 仍然是绝佳选项。高级工作流仍可受益于“编排者 + 子代理（orchestrator + sub-agent）”模式：由推理模型负责规划与决策，而 Sonnet 或 Haiku 执行机械性的点击步骤。

# 处理小目标（Handling small targets）

Click accuracy degrades as targets get smaller. Large and medium UI elements (buttons, input fields, and standard menu items) are reliable across all resolutions within the safe zone. The challenge is with small and tiny targets, like checkboxes, system tray icons, dropdown arrows, small toggle switches, and tree view expand/collapse buttons.

目标越小，点击准确性越差。大中型 UI 元素（按钮、输入框和标准菜单项）在安全区内的所有分辨率下都可靠。真正的挑战在于小微型目标，比如复选框、系统托盘图标、下拉箭头、小型开关，以及树状视图的展开/折叠按钮。

If your application involves clicking small targets frequently, consider these strategies:

如果你的应用需要频繁点击小目标，可以考虑以下策略：

Use zoom for dense UIs. Claude 4.6 and 4.7 models support a zoom capability that lets the model inspect specific screen regions at higher resolution before clicking. Enable it in your tool configuration:

对密集 UI 使用缩放（zoom）。Claude 4.6 与 4.7 模型支持一种缩放能力，让模型能在点击前以更高分辨率查看特定屏幕区域。在工具配置中启用它：

```
{
  "type": "computer_20251124",
  "name": "computer",
  "display_width_px": 1280,
  "display_height_px": 720,
  "enable_zoom": True
}
```

Make targets larger. If you control the UI being automated, increasing the size of click targets (even modestly) has a disproportionate impact on reliability. This might mean using a lower system DPI, zooming in the browser, or adjusting UI scaling settings.

把目标做大。如果被自动化的 UI 由你掌控，增大点击目标的尺寸（哪怕只是适度增大）对可靠性的影响会不成比例地大。这可能意味着使用更低的系统 DPI、在浏览器中放大页面，或调整 UI 缩放设置。

Use keyboard alternatives for tiny targets. For very small elements, such as system tray icons or tiny checkboxes), keyboard shortcuts or tab-based navigation can be more reliable than clicking. If your workflow allows it, prompting the model to use keyboard interactions for specific steps can improve success rates.

对微型目标使用键盘替代方案。对于非常小的元素（如系统托盘图标或微型复选框），键盘快捷键或基于 Tab 的导航可能比点击更可靠。如果你的工作流允许，引导模型在特定步骤使用键盘交互可以提高成功率。

Consider source image resolution. Screenshots from 4K+ displays that get compressed down to 720p lose significant detail (for example, a 16px checkbox at 3840x2160 native becomes roughly 5px at 1280x720 display resolution, which makes the target much smaller and therefore more difficult to hit). If you're working with very high-resolution displays, consider using Opus 4.7, which has a higher resolution limit than previous models. If using 4.6 models, consider capturing at a lower DPI, using display scaling to enlarge UI elements, or focusing the screenshot on the relevant portion of the screen rather than the full display. Because these models represent more information with less pixels, we've observed that performance degrades as source image scale increases, meaning more compression is needed.

留意源图像分辨率。来自 4K+ 显示器、再被压缩到 720p 的截图会损失大量细节（例如，原生 3840x2160 下 16px 的复选框，在 1280x720 显示分辨率下只剩约 5px，目标变得更小、因此更难命中）。如果你在处理超高分辨率显示器，考虑使用 Opus 4.7，它的分辨率上限高于之前的模型。如果使用 4.6 模型，可以考虑以较低的 DPI 捕获、利用显示缩放放大 UI 元素，或者让截图只聚焦屏幕的相关区域而非整个画面。由于这些模型要用更少的像素表示更多信息，我们观察到性能会随源图像尺寸增大而下降--也就是说，所需的压缩更重。

# 我们测试过但未见成效的方法（Approaches we tested that didn't help）

We experimented on internal evaluations with several popular optimization techniques and did not find consistent uplift from these approaches, though results may vary depending on the specific situation:

我们在内部评估中试验了几种流行的优化技术，没有发现这些方法带来一致的提升，不过具体效果可能因场景而异：

- Breaking the image into smaller tiles: Splitting a screenshot into quadrants or regions and sending them separately did not improve click accuracy.
- Overlaying a grid pattern with coordinates: Adding a visual coordinate grid to screenshots to help the model localize targets did not produce reliable gains.
- Resize algorithm choice: PIL LANCZOS, sips, and other common resize algorithms produced identical results. Use whatever is convenient for your stack.

- 把图像切成小块（tiling）：将截图拆成象限或区域分别发送，并未提升点击准确性。
- 叠加带坐标的网格：在截图上叠加可视化坐标网格以帮助模型定位目标，没有产生可靠的收益。
- 缩放算法的选择：PIL LANCZOS、sips 及其他常见缩放算法的结果完全相同。用你的技术栈里顺手的那种即可。

# 检查失败（Inspecting failures）

If the model acts unpredictably after trying the fixes above, log the full transcripts and overlay the predicted clicks on the source screenshots to understand what the model is actually seeing and deciding.

如果尝试上述修复后模型仍表现异常，请记录完整的交互记录（transcript），并把预测的点击位置叠加到源截图上，弄清模型到底看到了什么、做出了什么决定。

Some failures aren't about click accuracy at all. For example, certain dropdown menus may invoke system-level UI that the browser viewport doesn't capture-the model appears to be failing the task, but it simply can't see the menu it needs to interact with. In cases like these, the model should rely on alternative methods such as JavaScript execution, keyboard navigation, or direct document object model (DOM) manipulation rather than clicking.

有些失败根本与点击准确性无关。例如，某些下拉菜单可能会调出浏览器视口捕获不到的系统级 UI--模型看起来是在任务上失败了，其实它只是看不到自己需要交互的那个菜单。遇到这类情况，模型应当改用替代方法，例如执行 JavaScript、键盘导航，或直接操作文档对象模型（document object model，DOM），而不是点击。

# 快速参考（Quick reference）

How to scale and prepare an image for computer use

如何为计算机使用缩放并准备图像

```python
import math
from PIL import Image
import base64
import io

# 1568 for 4.6 family, 2576 for Opus 4.7
MAX_LONG_EDGE = 1568
# 1.15MP for 4.6 family, 3.75MP for Opus 4.7
MAX_PIXELS = 1_150_000


def prepare_screenshot(screenshot: Image.Image, native_w: int, native_h: int) -> tuple[str, int, int]:
    """Resize a screenshot to fit API limits and return base64 + display dimensions."""
    # Option A: Fixed 720p (simple, reliable)
    display_w, display_h = 1280, 720
    # Option B: Max API fit (maximizes fidelity)
    # display_w, display_h = compute_max_api_fit(native_w, native_h)

    resized = screenshot.resize((display_w, display_h), Image.LANCZOS)
    buffer = io.BytesIO()
    resized.save(buffer, format="PNG")
    b64 = base64.standard_b64encode(buffer.getvalue()).decode()

    return b64, display_w, display_h


def scale_coordinates(api_x: int, api_y: int, display_w: int, display_h: int,
                      screen_w: int, screen_h: int) -> tuple[int, int]:
    """Scale API-returned coordinates back to native screen space."""
    screen_x = int(api_x * (screen_w / display_w))
    screen_y = int(api_y * (screen_h / display_h))
    return screen_x, screen_y


def compute_max_api_fit(native_w: int, native_h: int) -> tuple[int, int]:
    """Compute the largest resolution that fits API limits while preserving aspect ratio."""
    aspect = native_w / native_h
    h_from_pixels = math.sqrt(MAX_PIXELS / aspect)
    w_from_pixels = h_from_pixels * aspect
    if native_w >= native_h:
        w = min(w_from_pixels, MAX_LONG_EDGE)
        h = w / aspect
    else:
        h = min(h_from_pixels, MAX_LONG_EDGE)
        w = h * aspect
    w = min(w, native_w)
    h = min(h, native_h)
    return int(w), int(h)
```

Usage:

用法：

```python
import anthropic
from PIL import Image

client = anthropic.Anthropic()

# Capture screenshot (your method here)
screenshot = Image.open("screenshot.png")
native_w, native_h = screenshot.size

# Prepare for API
b64, display_w, display_h = prepare_screenshot(screenshot, native_w, native_h)

# Send to Claude - text before image
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Click on the Submit button"},
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": b64}},
        ]
    }],
    tools=[{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": display_w,
        "display_height_px": display_h,
    }],
)

# Scale coordinates back for execution
api_x, api_y = extract_click_coords(response)  # your parsing logic
screen_x, screen_y = scale_coordinates(api_x, api_y, display_w, display_h, native_w, native_h)
```

# 为计算机使用调优思考力度（Tuning thinking effort for computer use）

Claude's latest models support adaptive thinking, a setting which lets Claude decide how much to reason through intermediate steps before acting. Instead of manually setting a thinking token budget, adaptive thinking lets Claude dynamically determine when and how much to use extended thinking based on the complexity of each request. For computer use, this means Claude can think through what it's seeing on screen, plan multi-step interactions, and self-correct before committing to a click or keystroke.

Claude 的最新模型支持自适应思考（adaptive thinking），这一设置让 Claude 自行决定在行动之前对中间步骤推理到什么程度。无需手动设置思考 token 预算，自适应思考让 Claude 根据每个请求的复杂度，动态决定何时以及以多大程度使用扩展思考（extended thinking）。对计算机使用而言，这意味着 Claude 可以想清楚屏幕上看到的内容、规划多步交互，并在落下一个点击或按键之前自我纠正。

With adaptive thinking, Claude's thinking depth is controlled via the thinking parameter with an effort level: low, medium, high,xhigh (with Opus 4.7),and max. More thinking means more reasoning per action, but also more output tokens, higher latency, and higher cost.

在自适应思考下，Claude 的思考深度通过 thinking 参数和一个力度（effort）级别来控制：low、medium、high、xhigh（随 Opus 4.7 提供）以及 max。思考越多意味着每个动作的推理越多，但也意味着更多输出 token、更高延迟和更高成本。

The natural question: depending on the model, how much thinking is optimal for computer use?

一个自然的问题：视模型而定，多少思考量对计算机使用才是最优的？

# Claude Opus 4.7

We tested each thinking effort level across a suite of end to end UI automation tasks spanning desktop applications, browsers, and multi-application workflows.

我们在一套端到端 UI 自动化任务上测试了每个思考力度级别，任务涵盖桌面应用、浏览器以及跨应用工作流。

![Opus 4.7 在不同思考力度下的性能对比](images/compuse-1.png)

Opus 4.7 outperforms the 4.6 family. On the OSWorld Verified benchmark, we find that Opus outperforms all 4.6 family models at equivalent token usage and effort settings. Opus 4.7 on low effort scores similarly to Sonnet 4.6 on max, while using ~1/10th the tokens per task. For difficult tasks, Opus 4.7 is the obvious choice.

Opus 4.7 优于 4.6 家族。在 OSWorld Verified 基准上，我们发现 Opus 在同等 token 用量和力度设置下超过了所有 4.6 家族模型。Opus 4.7 以 low 力度得分与 Sonnet 4.6 以 max 力度相当，而每任务的 token 用量仅约 1/10。对于困难任务，Opus 4.7 是显而易见的选择。

Setting effort to high achieves close to the highest task success rate while using roughly half the output tokens of max. Compared to Opus 4.6, low, medium and high all use approximately the same amount of tokens while improving score on OSWorld. During our internal testing, Max effort used more tokens and provided the best score. The table below outlines our recommendations for when to use each thinking effort level.

把力度设为 high 能取得接近最高的任务成功率，同时输出 token 大约只有 max 的一半。与 Opus 4.6 相比，low、medium 和 high 的 token 用量都大致相同，却在 OSWorld 上的得分更高。在内部测试中，Max 力度使用了更多 token 并取得了最好成绩。下表概述了我们对何时使用各思考力度级别的建议。

## 思考力度级别建议（Recommendations for effort levels）

| Scenario | Thinking effort | Why |
| --- | --- | --- |
| Default for most use cases | high | Opus 4.7 is best for difficult tasks. Using high will give the model enough reasoning to plan over complex multi-step interactions without significantly increasing token usage. |
| High-throughput / cost-sensitive | low | Lower token usage while providing quality between Opus 4.6's high and max effort settings. |
| Simple, well-defined workflows / fastest | Suggest trying Sonnet 4.6 | Use if low latency is the highest priority. Adequate for short, predictable tasks where the UI is consistent and the workflow is known. |
| Complex, one-shot tasks | max | Use when tasks are highly challenging and you need to get it right on the first attempt. |

| 场景 | 思考力度 | 原因 |
| --- | --- | --- |
| 大多数用例的默认选择 | high | Opus 4.7 最适合困难任务。使用 high 能给模型足够的推理能力来规划复杂的多步交互，又不会显著增加 token 用量。 |
| 高吞吐 / 成本敏感 | low | token 用量更低，同时提供介于 Opus 4.6 的 high 与 max 力度之间的质量。 |
| 简单、定义明确的工作流 / 最快 | 建议尝试 Sonnet 4.6 | 若低延迟是最高优先级则使用。适合 UI 稳定、流程已知的短小可预测任务。 |
| 复杂的一次性任务 | max | 当任务极具挑战且必须一次做对时使用。 |

# Claude 4.6 模型（Claude 4.6 models）

We tested each thinking effort level across a suite of end to end UI automation tasks spanning desktop applications, browsers, and multi-application workflows.

我们在一套端到端 UI 自动化任务上测试了每个思考力度级别，任务涵盖桌面应用、浏览器以及跨应用工作流。

![Claude 4.6 模型在不同思考力度下的性能对比](images/compuse-2.png)

Two patterns stand out:

有两个规律非常突出：

‍Medium effort is the sweet spot. Setting effort to medium achieves close to the highest task success rate while using roughly half the output tokens of high. Beyond medium, performance somewhat plateaus. Notably, when tasks are retried, medium and high converge to the same success rate. This means high effort may help the model get a difficult task right on the first try, but given multiple attempts, medium may get there just as reliably at lower cost.

Medium 力度是最佳平衡点（sweet spot）。把力度设为 medium 能取得接近最高的任务成功率，而输出 token 大约只有 high 的一半。超过 medium 之后，性能会略有停滞。值得注意的是，当任务可以重试时，medium 和 high 会收敛到相同的成功率。也就是说，high 力度或许能帮助模型第一次就做对困难任务，但如果允许多次尝试，medium 能以更低的成本同样可靠地达成。

A little thinking goes a long way. low effort is a surprisingly strong option. It actually uses fewer total output tokens than disabling thinking entirely (the model makes fewer mistakes and needs fewer retry cycles), while matching or slightly exceeding no-thinking accuracy. This makes it the best option for cost-sensitive, high-throughput workloads. The table below outlines our effort recommendations.

少量思考作用巨大。low 力度是一个出人意料强的选项。它的实际总输出 token 比完全关闭思考更少（模型犯的错更少，需要的重试轮次也更少），同时准确性持平或略高于不思考。这使它成为成本敏感、高吞吐工作负载的最佳选择。下表概述了我们的力度建议。

## 思考力度级别建议（Recommendations for effort levels）

| Scenario | Thinking effort | Why |
| --- | --- | --- |
| Default for most use cases | medium | Best accuracy-to-cost ratio. Gives the model enough reasoning to plan multi-step interactions without overthinking. With retries, matches high performance at half the token cost. |
| High-throughput / cost-sensitive | low | More accurate than no thinking, but with lower token usage due to fewer errors and retries. |
| Simple, well-defined workflows / fastest | Thinking disabled | Use if low latency is the highest priority. Adequate for short, predictable tasks where the UI is consistent and the workflow is known. |
| Complex, one-shot tasks | high | Use when tasks are challenging and you need to get it right on the first attempt. If your system supports retries, medium may achieve the same eventual success rate. |

| 场景 | 思考力度 | 原因 |
| --- | --- | --- |
| 大多数用例的默认选择 | medium | 准确性与成本之比最佳。给模型足够的推理来规划多步交互，又不会过度思考。配合重试时，能以一半的 token 成本达到与 high 相当的性能。 |
| 高吞吐 / 成本敏感 | low | 比不思考更准确，且因错误和重试更少，token 用量反而更低。 |
| 简单、定义明确的工作流 / 最快 | 关闭思考 | 若低延迟是最高优先级则使用。适合 UI 稳定、流程已知的短小可预测任务。 |
| 复杂的一次性任务 | high | 当任务有挑战且必须一次做对时使用。如果你的系统支持重试，medium 可能达到相同的最终成功率。 |

We don't recommend max effort for computer use. In our testing, it provides no accuracy benefit over high while further increasing output token cost. UI tasks are primarily perceptual rather than deeply logical, and the additional reasoning budget goes unused or leads to overthinking. Keep in mind that this advice will change as models evolve.

我们不推荐在计算机使用中使用 max 力度。在我们的测试中，相比 high 它没有带来准确性收益，却进一步推高了输出 token 成本。UI 任务主要是感知型而非深度逻辑型，额外的推理预算要么用不上，要么导致过度思考。请记住，随着模型演进，这条建议也会改变。

# 将力度设为 medium 的配置示例（Example configuration of medium setting effort level）

```python
import anthropic

client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    betas=["computer-use-2025-11-24"],
    thinking={"type": "adaptive"},
    output_config={"effort": "medium"},
    messages=[...],
    tools=[
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 720,
        }
    ],
)
```

# 为什么更多思考并不总有帮助（Why more thinking doesn't always help）

UI automation tasks are fundamentally different from coding or math problems. Most computer use actions are perceptual and mechanical: identifying the right element, clicking in the right place, rather than deeply logical. Thinking helps most when the model needs to:

UI 自动化任务与编程或数学问题有本质区别。大多数计算机使用动作是感知性和机械性的：识别正确的元素、点击正确的位置，而不是深度逻辑推理。思考在模型需要以下操作时帮助最大：

- Plan a multi-step sequence before starting (e.g., "I need to open Settings, navigate to Privacy, then disable tracking")
- Recover from an unexpected UI state (e.g., a dialog appeared that wasn't anticipated)
- Cross-reference information between what's on screen and the task instructions
- Complete challenging projects on professional software

- 在开始前规划多步序列（例如“我需要打开设置，进入隐私，然后关闭跟踪”）
- 从意外的 UI 状态中恢复（例如出现了一个预料之外的对话框）
- 在屏幕上的内容与任务指令之间交叉核对信息
- 在专业软件上完成有挑战性的项目

# 提升安全性：利用提示注入分类器（Improving safety: leveraging prompt injection classifiers）

This section covers prompt injection protection, which is offered by default and for free if you use our official computer use tool header. However, if you are interested in enabling this on custom computer or browser use tools, please fill out our Prompt Injection Classifiers Interest Form.

本节介绍提示注入（prompt injection）防护：如果你使用我们的官方计算机使用工具类型（tool header），该防护默认免费提供。如果你有兴趣在自定义的计算机或浏览器使用工具上启用该防护，请填写我们的 Prompt Injection Classifiers Interest Form（提示注入分类器意向表单）。

Computer use agents interact with untrusted content by design. Every screenshot, webpage, or application UI that Claude processes could contain adversarial instructions, including hidden text, manipulated images, deceptive UI elements, or social engineering attempts that try to hijack the agent's behavior. This attack surface is fundamentally different from a typical API integration where you control the inputs. With computer use, the inputs to the model are the open internet and whatever software the agent is navigating.

计算机使用 agent 天生就要与不可信内容打交道。Claude 处理的每一张截图、每一个网页或应用 UI 都可能包含对抗性指令，包括隐藏文本、被篡改的图像、欺骗性 UI 元素，或试图劫持 agent 行为的社会工程攻击。这个攻击面与由你掌控输入的典型 API 集成有本质不同。在计算机使用中，模型的输入是开放的互联网以及 agent 正在操作的任何软件。

As computer use agents become more capable and more widely deployed, prompt injection becomes a correspondingly more serious risk. An agent that can click, type, and navigate can be manipulated into taking real-world actions such as filling out forms, downloading files, or navigating to malicious URLs. Building robust defenses against these attacks is essential for any production deployment.

随着计算机使用 agent 能力越来越强、部署越来越广，提示注入也相应成为更严重的风险。一个能点击、输入、导航的 agent 可能被操纵去执行现实世界的动作，比如填写表单、下载文件或访问恶意 URL。对任何生产部署而言，针对这类攻击构建稳健的防御都至关重要。

# 我们如何进行提示注入防御（How we approach prompt injection defense）

We've written in detail about our approach to prompt injection defenses for browser and computer use. Our defense strategy operates at multiple layers:

我们已经撰文详细介绍了针对浏览器与计算机使用的提示注入防御方法。我们的防御策略在多个层面运作：

Training-time robustness. We use reinforcement learning to build prompt injection resistance directly into Claude's capabilities. During training, Claude is exposed to injected content embedded in simulated web pages and application UIs, and rewarded when it correctly identifies and refuses to follow malicious instructions. This means Claude's first line of defense is the model itself as it has learned to distinguish between legitimate user instructions and adversarial content encountered during task execution.

训练时鲁棒性。我们利用强化学习（reinforcement learning）把提示注入抗性直接构建进 Claude 的能力中。训练期间，Claude 会接触到嵌入在模拟网页和应用 UI 中的注入内容，并在正确识别、拒绝执行恶意指令时获得奖励。这意味着 Claude 的第一道防线就是模型本身，因为它已经学会区分合法的用户指令与任务执行中遇到的对抗性内容。

Real-time classifiers. We run probes that scan content entering Claude's context window and flag potential prompt injection attempts. These probes detect adversarial commands across multiple modalities such as text hidden in page content, instructions embedded in images, and deceptive UI elements designed to trick the agent and then adjust Claude's behavior when they identify an attack.

实时分类器。我们运行探针来扫描进入 Claude 上下文窗口的内容，并标记潜在的提示注入尝试。这些探针能检测多种模态的对抗性命令，例如隐藏在页面内容中的文本、嵌在图像中的指令、以及为诱骗 agent 而设计的欺骗性 UI 元素，并在识别到攻击时调整 Claude 的行为。

Continuous red teaming. Our security researchers continuously probe these defenses, and we participate in external adversarial evaluations to benchmark robustness against evolving attack techniques.

持续红队测试。我们的安全研究人员会持续探测这些防御，我们还参与外部对抗性评估，以对照不断演进的攻击技术检验鲁棒性。

We've continued to invest heavily in all three layers since our initial computer use research preview. Each new model generation incorporates stronger training-time defenses and more capable classifiers, and we've expanded the range of attack techniques our red team evaluates against.

自最初的计算机使用研究预览以来，我们持续在这三个层面大力投入。每一代新模型都融入了更强的训练时防御和更强大的分类器，我们也扩展了红队评估所覆盖的攻击技术范围。

# 使用 Claude 内置分类器（Using Claude's built-in classifiers）

When you use Claude's official computer use tool via the API, prompt injection classifiers run automatically on every request. These classifiers operate in parallel with the main model inference, adding approximately zero additional latency and no additional cost to your requests.

当你通过 API 使用 Claude 的官方计算机使用工具时，提示注入分类器会在每个请求上自动运行。这些分类器与主模型推理并行运作，为请求增加的延迟约等于零，也不产生额外成本。

There is nothing you need to configure to enable this protection. It's on by default when you use the official computer_20251124 tool type. The classifiers evaluate screenshots and other content for signs of prompt injection and influence Claude's responses accordingly.

启用这项保护无需任何配置。使用官方 computer_20251124 工具类型时它默认开启。分类器会评估截图及其他内容是否存在提示注入迹象，并据此影响 Claude 的响应。

```
# Classifiers run automatically when using the official CU tool - no extra config needed
tools = [
    {
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1280,
        "display_height_px": 720,
    }
]
```

# 如果你没有使用官方计算机使用工具（If you're not using the official computer use tool）

Many developers build computer use integrations using custom tool definitions rather than the official computer_20251124 tool type, for example, defining their own screenshot and click tools. If this describes your setup, the built-in classifiers described above don't currently run on your requests.

许多开发者构建计算机使用集成时使用自定义工具定义而非官方 computer_20251124 工具类型，例如定义自己的截图和点击工具。如果你的配置正是如此，上述内置分类器目前不会在你的请求上运行。

We're actively exploring how to extend prompt injection protection to these custom implementations. If you're building a computer use or browser use integration without the official tool type and are interested in prompt injection classifiers, fill out this interest form and we'll follow up as this capability becomes available.

我们正在积极探索如何把提示注入防护扩展到这些自定义实现。如果你正在构建不使用官方工具类型的计算机使用或浏览器使用集成，并且对提示注入分类器感兴趣，请填写这份意向表单，我们会在该能力可用时与你联系。

# 无论是否使用分类器都适用的最佳实践（Best practices regardless of classifier use）

Classifiers are one layer of defense, not a complete solution. We recommend the following practices for any computer use deployment:

分类器只是一层防御，不是完整的解决方案。我们建议任何计算机使用部署都遵循以下实践：

Implement human-in-the-loop for high-stakes actions. Have the agent pause and request user confirmation before performing irreversible actions such as submitting forms, making purchases, sending messages, or modifying data. This is the single most effective mitigation against prompt injection regardless of classifier performance.

对高风险操作实现人在回路（human-in-the-loop）。让 agent 在执行不可逆操作（如提交表单、购买商品、发送消息或修改数据）之前暂停并请求用户确认。无论分类器表现如何，这都是对提示注入最有效的单项缓解措施。

Scope the agent's permissions. Limit what the agent can do. If your workflow doesn't require file downloads, don't give the agent access to download files. If it doesn't need to send emails, don't give it access to an email client. Reducing the blast radius of a successful injection is as important as preventing the injection itself.

限定 agent 的权限。限制 agent 能做的事。如果你的工作流不需要下载文件，就不要给 agent 下载文件的权限；如果它不需要发邮件，就不要给它邮件客户端的访问权。缩小一次成功注入的波及范围（blast radius）与阻止注入本身同样重要。

Monitor and log agent actions. Log the full sequence of actions the agent takes, including screenshots at each step. This allows you to detect anomalous behavior, audit what happens when something goes wrong, and build a feedback loop to improve your system's robustness over time.

监控并记录 agent 的操作。完整记录 agent 执行的动作序列，包括每一步的截图。这让你能够检测异常行为、在出问题时审计当时发生了什么，并建立一个反馈回路来持续提升系统的鲁棒性。

Treat all web content as untrusted. Design your agent's system prompt to clearly distinguish between the user's instructions and content encountered during task execution. Remind the model that text found on web pages, in emails, or in application UIs is not from the user and should not be treated as instructions.

把所有网页内容视为不可信。在 agent 的 system prompt 设计中明确区分用户指令与任务执行中遇到的内容。提醒模型：网页、邮件或应用 UI 中的文字并非来自用户，不应被当作指令。

# 计算机使用的上下文管理（Context management for computer use）

When building computer use agents, screenshots accumulate fast. Every action generates a new image, and each image consumes roughly 1,000–1,800 tokens depending on resolution. After accounting for the system prompt, tool definitions, and text content, a 200k context window can fill up in well under 100 screenshots.

构建计算机使用 agent 时，截图会迅速累积。每个动作都会生成一张新图像，而每张图像视分辨率大约消耗 1,000–1,800 个 token。算上 system prompt、工具定义和文本内容之后，一个 200k 的上下文窗口用不到 100 张截图就会被填满。

Managing this context well has two goals: 1) keeping total tokens bounded and 2) keeping prompt caching effective so you don't repeatedly pay full price for the same prefix. We've found that effective context management has more impact on long-running-agent cost and latency than almost any other optimization. This section covers three layers that compose cleanly: placing cache breakpoints, pruning old screenshots without breaking the cache, and summarizing history when pruning isn't enough.

管理好这些上下文有两个目标：1) 让总 token 量保持有界；2) 让提示缓存持续生效，避免为同一前缀反复支付全价。我们发现，有效的上下文管理对长时运行 agent 的成本和延迟的影响几乎超过任何其他优化。本节介绍三个可以干净组合的层面：设置缓存断点、在不破坏缓存的前提下修剪旧截图，以及在修剪不够用时对历史做摘要。

# 设置缓存断点（Placing cache breakpoints）

Prompt caching only helps if breakpoints land on content that will recur across turns. The API supports four cache breakpoints total. Putting all four on a stable prefix (system prompt, tool definitions) wastes them as that prefix is already hit once and never invalidates, so one breakpoint is enough. The other three are better spent on recent history, where invalidation risk is highest and savings compound over long sessions.

提示缓存只有在断点落在会跨轮复现的内容上时才有用。API 总共支持四个缓存断点。把它们全部放在稳定前缀（system prompt、工具定义）上是一种浪费，因为该前缀命中一次后就不会再失效，一个断点足矣。另外三个断点更适合花在最近的历史上--那里失效风险最高，而在长会话中节省的收益会不断复利累积。

We recommend:

我们的建议：

- One breakpoint on the system prompt or trailing tool definitions. This prefix rarely changes within a session.
- Up to three additional breakpoints on the most recent tool results, advancing each turn and clearing the previous iteration's breakpoints so you don't overrun the four-breakpoint limit.

- 在 system prompt 或末尾的工具定义上放一个断点。这个前缀在一个会话内很少变化。
- 在最近的工具结果上最多再放三个断点，每轮前移并清除上一轮的断点，以免超出四个断点的上限。

Spreading breakpoints across recent positions gives you graceful degradation. If your most recent breakpoint is invalidated, e.g. by an image prune, a compaction, or a tool-definition change, an earlier breakpoint can still hit, and you keep paying 10% of the full input cost instead of 100%.

把断点分散在较近的多个位置能带来优雅降级。如果你最近的断点失效了（例如因为图像修剪、压缩或工具定义变更），更早的断点仍然可以命中，你继续支付的是全额输入成本的 10%，而不是 100%。

Example of cache control and setting breakpoints:

缓存控制与设置断点的示例：

```python
def set_trailing_cache_control(messages, max_breakpoints=3):
    """Place up to `max_breakpoints` ephemeral cache_control markers on the most
    recent tool_result blocks, after clearing any existing markers."""
    for msg in messages:
        for block in msg.get("content", []):
            if isinstance(block, dict):
                block.pop("cache_control", None)

    placed = 0
    for msg in reversed(messages):
        for block in reversed(msg.get("content", [])):
            if placed >= max_breakpoints:
                return
            if isinstance(block, dict) and block.get("type") == "tool_result":
                block["cache_control"] = {"type": "ephemeral"}
                placed += 1
```

# 方法一：滚动缓冲（缓存感知）（Approach 1: Rolling buffer (cache-aware)）

The simplest way to keep token counts bounded is to keep only the N most recent screenshots and drop the rest. Before each API call, walk the message array and replace older image blocks with a short placeholder (e.g., a text block saying "[Image omitted]").

让 token 数量保持有界，最简单的方法是只保留最近 N 张截图并丢弃其余部分。每次 API 调用前，遍历消息数组，把较旧的图像块替换为一个简短的占位符（例如一个写着 "[Image omitted]" 的文本块）。

The naive version of this pattern is dropping screenshots one at a time as they age out, which changes the prefix on every turn and invalidates the prompt cache continuously. This is how rolling buffers got their reputation for breaking caching. The fix is to prune in batches so the prefix stays byte-identical for several turns at a time, then invalidates once, then stays stable again.

这个模式的朴素版本是让截图随时间一张一张地淘汰，这会每轮都改变前缀、持续使提示缓存失效。滚动缓冲（rolling buffer）“缓存杀手”的名声就是这么来的。修复方法是分批修剪，让前缀一次在多轮内保持字节级不变，然后失效一次，随后再次保持稳定。

A concrete pattern that we have tested is to:

我们测试过的一个具体模式是：

- Keep the most recent keep_n screenshots in full resolution.
- Once the total screenshot count exceeds keep_n + interval, replace the oldest interval screenshots with placeholders in a single pass.
- Between pruning events, the message array is byte-identical across turns, so your cache breakpoints keep hitting.

- 以全分辨率保留最近的 keep_n 张截图。
- 一旦截图总数超过 keep_n + interval，就一次性把最旧的 interval 张截图替换为占位符。
- 在两次修剪事件之间，消息数组跨轮保持字节级一致，因此缓存断点持续命中。

Reasonable defaults to start with: keep_n = 3, interval = 25. These are tunable, and a higher interval means fewer prune events (better cache efficiency) but a larger tail of full-resolution screenshots in context (more tokens). Measure cache hit rate and total input tokens on a representative trajectory and adjust.

合理的起始默认值：keep_n = 3，interval = 25。这些参数可调：interval 越高，修剪事件越少（缓存效率更好），但上下文中全分辨率截图的尾部越长（token 更多）。请在一条有代表性的轨迹上测量缓存命中率和总输入 token，再据此调整。

Example of pruning previous screenshots while keeping cache breakpoints:

在保留缓存断点的同时修剪先前截图的示例：

```python
def prune_old_screenshots(messages, keep_n=3, interval=25):
    """Replace older screenshots with text placeholders in batches.
    Only prunes when the total count exceeds keep_n + interval, so the
    message prefix stays byte-stable for `interval` turns between prunes."""
    image_positions = [
        (msg_idx, block_idx)
        for msg_idx, msg in enumerate(messages)
        for block_idx, block in enumerate(msg.get("content", []))
        if isinstance(block, dict) and block.get("type") == "image"
    ]
    if len(image_positions) <= keep_n + interval:
        return messages

    to_prune = image_positions[:-keep_n][-interval:]
    for msg_idx, block_idx in to_prune:
        messages[msg_idx]["content"][block_idx] = {
            "type": "text",
            "text": "[Image omitted]",
        }

    return messages
```

Rolling buffers still have one real limitation: anything outside the buffer is gone. The original instructions, what the agent already tried, and where it is in the task all disappear with the pruned screenshots. For short tasks (under ~50 actions), that's fine. For anything longer, combine this with compaction.

滚动缓冲仍有一个真实的局限：缓冲区之外的任何东西都会消失。最初的指令、agent 已经尝试过什么、任务进行到哪一步，都随被修剪的截图一起消失。对于短任务（约 50 个动作以内），这没问题。更长的任务则要把它与压缩（compaction）结合使用。

# 方法二：基于 LLM 的压缩（Approach 2: LLM-based compaction）

Instead of silently dropping old images, summarize the full conversation before discarding it. The summary preserves what happened, what the user asked for, what's been completed, and where to resume. A few recent screenshots are kept alongside it so the agent can see what it's currently looking at.

与其悄无声息地丢弃旧图像，不如在丢弃之前对完整对话做摘要。摘要保留了发生过什么、用户要求了什么、完成了什么、以及从哪里继续。旁边再保留几张最近的截图，让 agent 能看到自己当前正在看的内容。

Compaction and the cache-aware rolling buffer are complementary. Use the rolling buffer turn-to-turn to keep token growth manageable; use compaction occasionally to reclaim the rest of the window without losing earlier context. Each compaction event is a cache invalidation by design, so you want it to happen rarely, not every few turns.

压缩与缓存感知的滚动缓冲是互补的。逐轮使用滚动缓冲，让 token 增长保持可控；偶尔使用压缩，在不丢失先前上下文的情况下回收窗口的其余部分。每次压缩事件在设计上就是一次缓存失效，所以你希望它很少发生，而不是每隔几轮就来一次。

## 摘要提示词（The summarization prompt）

This example prompt provides a scaffold where each section targets a specific failure mode. The prompt must capture everything the agent needs to continue the task without re-reading the original conversation, as depicted in the example below:

这个示例提示词提供了一个骨架，其中每一节都针对一种特定的失败模式。该提示词必须囊括 agent 继续任务所需的一切信息，使其无需重读原始对话，如下例所示：

```python
COMPACT_PROMPT = """Your task is to create a detailed summary of this conversation that will REPLACE the conversation history. The agent will continue working with only this summary and a few recent screenshots as context.

CRITICAL: Preserve ALL user instructions verbatim. User instructions are the most critical element. If they are lost, the agent will deviate from the task.

Before providing your summary, analyze the conversation in tags:

1. Extract every user instruction, requirement, and constraint
2. Identify if this is a repeatable workflow (e.g., processing N items)
3. Chronologically trace what actions were taken and what happened

Your summary MUST include these sections:

1. USER INSTRUCTIONS:
- Complete initial task definition (verbatim when possible)
- ALL specific requirements and criteria
- Every "DO NOT", "ALWAYS", "MUST" instruction
- Any corrections or feedback that changed the approach

2. TASK TEMPLATE (if this is a repeatable workflow):
- The pattern being repeated
- Decision criteria for each iteration
- Standard workflow steps
- Example of one completed iteration

3. CONSTRAINTS AND RULES:
- All user-specified rules and restrictions
- Edge cases and exceptions discovered

4. ACTIONS TAKEN:
- Pages visited and elements interacted with
- Forms filled and buttons clicked

5. ERRORS AND FIXES:
- What went wrong and how it was resolved
- Approaches that failed (so they aren't retried)

6. PROGRESS TRACKING:
- Items completed vs. remaining
- Current position in the workflow

7. CURRENT STATE:
- Current application, URL and domain (optional)
- Important page state (logged in, form progress, etc.)

8. NEXT STEP:
- Exactly what should be done next to continue
"""
```

In the prompt above, User Instructions prevents task drift: without them, the agent deviates after compaction. Task Template captures the repeatable pattern so the agent can continue iterating after compaction without re-deriving the workflow from scratch. Constraints and Rules preserves restrictions and edge cases set before or discovered during the task, so the agent doesn't violate existing rules it knew to abide by. Actions Taken helps track past progress. Errors and Fixes prevents retrying failed approaches ("I already tried clicking Submit; it doesn't work until the Terms checkbox is checked"). Progress Tracking prevents restarts and skipped items. Current State & Next Step gives an unambiguous entry point to resume.

在上面的提示词中，User Instructions 防止任务漂移：没有它们，agent 在压缩后就会偏离任务。Task Template 捕获可重复的模式，让 agent 在压缩后无需从头重新推导工作流即可继续迭代。Constraints and Rules 保留任务前设定或任务中发现的限制与边界情况，让 agent 不会违反它本已知晓要遵守的既有规则。Actions Taken 帮助追踪过往进度。Errors and Fixes 防止重试已经失败的做法（“我已经试过点击提交了；不勾选条款复选框它是不会生效的”）。Progress Tracking 防止从头重来和遗漏条目。Current State 与 Next Step 给出一个无歧义的恢复切入点。

## 服务端压缩（beta）（Server-side compaction (beta)）

The simplest way to use this prompt is to let the API handle compaction via server-side compaction (beta). Pass your custom summarization prompt as the instructions parameter in context_management, and the API automatically summarizes when input tokens exceed a trigger threshold. The instructions parameter completely replaces the default summarization prompt, so the sections above are what the model will follow. Set pause_after_compaction to attach the most recent messages (including screenshots) across compaction events.

使用这个提示词最简单的方式，是让 API 通过服务端压缩（beta）来处理压缩。把你自定义的摘要提示词作为 context_management 中的 instructions 参数传入，当输入 token 超过触发阈值时 API 会自动进行摘要。instructions 参数会完全替换默认的摘要提示词，因此模型遵循的就是上面这些小节。设置 pause_after_compaction 可以在压缩事件之间附上最近的消息（包括截图）。

Examples of using autocompaction tool:

使用自动压缩（autocompaction）工具的示例：

```python
# Minimal - turn on autocompaction with API defaults
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    betas=["compact-2026-01-12", "computer-use-2025-11-24"],
    context_management={"edits": [{"type": "compact_20260112"}]},
    messages=[...],
    tools=[...],
)

# Customized - set your own trigger threshold and summarization prompt
response = client.beta.messages.create(
    model="claude-opus-4-7",
    max_tokens=16000,
    betas=["compact-2026-01-12", "computer-use-2025-11-24"],
    context_management={
        "edits": [
            {
                "type": "compact_20260112",
                "trigger": {"type": "input_tokens", "value": 150_000},
                "instructions": COMPACT_PROMPT,
            }
        ]
    },
    messages=[...],
    tools=[...],
)
```

## 在客户端截断以与服务端保持一致（Truncate client-side to match the server）

When the API runs a server-side compaction, it replaces pre-compaction content on its side, but your local messages array still holds the full history. If you keep sending the full history on every subsequent turn, you'll pay for tokens the server no longer needs, plus your rolling-buffer pruner will operate on a different message slice than the server actually sees, which can break the cache-stable prefix you carefully maintained above.

当 API 执行服务端压缩时，它会在自己那一侧替换掉压缩前的内容，但你本地的消息数组仍保存着完整历史。如果你在后续每一轮都继续发送完整历史，你就要为服务端不再需要的 token 买单，而且你的滚动缓冲修剪器操作的消息切片会与服务端实际看到的不同，这可能破坏你前面精心维护的缓存稳定前缀。

The fix is to mirror the server's truncation on the client, as depicted by the code snippet below. When the response reports that compaction occurred, drop everything before the compaction marker from your local messages array before the next turn. This keeps client and server views aligned and lets the rolling buffer keep working correctly.

解决办法是在客户端镜像服务端的截断操作，如下方代码片段所示。当响应报告发生了压缩时，在下一轮之前把本地消息数组中压缩标记之前的所有内容删掉。这能让客户端与服务端的视图保持一致，让滚动缓冲继续正常工作。

```python
def truncate_to_last_compaction(messages, response):
    """If the server compacted on this turn, drop pre-compaction messages locally
    so the next turn's cache prefix matches what the server sees."""
    context_mgmt = getattr(response, "context_management", None)
    if not context_mgmt or not context_mgmt.get("applied_edits"):
        return messages

    compaction = next(
        (e for e in context_mgmt["applied_edits"] if e["type"] == "compact"),
        None,
    )
    if compaction is None:
        return messages

    keep_from = compaction["message_index_after_compaction"]
    return messages[keep_from:]
```

# 客户端压缩（Client-side compaction）

If you're using a model that doesn't support server-side compaction, or you want full control, implement compaction client-side with the same prompt. After each API call, check the total input token count from the response usage field. When that crosses a threshold (e.g., 90% of the context window), send the conversation to a summarizer model with COMPACT_PROMPT as the system prompt. Replace the message history with the summary plus a few recent screenshots, then continue the agent loop.

如果你使用的模型不支持服务端压缩，或者你想要完全掌控，可以在客户端用同样的提示词实现压缩。每次 API 调用后，从响应的 usage 字段检查总输入 token 数。当它越过某个阈值（例如上下文窗口的 90%）时，把对话发给一个摘要模型，并以 COMPACT_PROMPT 作为 system prompt。用摘要加上几张最近的截图替换消息历史，然后继续 agent 循环。

# 整合起来（Putting it together）

A good default for a long-running computer use agent looks like this:

一个长时运行的计算机使用 agent 的良好默认配置如下：

- One cache breakpoint on the stable prefix, three on trailing tool results, cleared and re-placed each turn.
- Cache-aware rolling buffer with keep_n = 3 and interval = 25, replacing older screenshots with placeholders in batches.
- Server-side compaction triggered around 150k input tokens with a custom prompt, plus a client-side truncation pass to keep the two views aligned.

- 稳定前缀上放一个缓存断点，末尾工具结果上放三个，每轮清除并重新放置。
- 缓存感知的滚动缓冲，keep_n = 3、interval = 25，分批用占位符替换较旧的截图。
- 输入 token 达到约 150k 时触发的服务端压缩（使用自定义提示词），外加一次客户端截断，以保持两个视图一致。

With these three layers in place, a typical long-horizon CU session will hit the prompt cache on the vast majority of turns, keep total input tokens bounded well below the context window, and preserve enough history through compaction events that the agent doesn't lose track of the task.

有了这三层，一次典型的长时程计算机使用（CU）会话将在绝大多数轮次命中提示缓存，让总输入 token 稳定控制在远低于上下文窗口的水平，并通过压缩事件保留足够的历史，使 agent 不会迷失任务。

# 改进计算机与浏览器使用的实验性设置（Experimental settings for improving computer and browser use）

The patterns below are techniques we've been testing in our implementations that show promise but aren't yet blanket recommendations. Each trades off complexity or cost for a potential lift on specific kinds of workloads. We include them here so you can try them on your workflow, but expect the guidance in this section to evolve quickly.

下面的模式是我们在自己的实现中持续测试、已显现潜力但尚未成为普适推荐的技术。每一项都以复杂性或成本为代价，换取在特定类型工作负载上的潜在提升。我们把它们写在这里供你在自己的工作流上尝试，但请预期本节的指导会快速演进。

# 批量工具（Batch tools）

In the updated reference implementation we expose two tools alongside the standard computer and browser tools: computer_batch and browser_batch. Each accepts a list of sub-actions and executes them in a single tool call. For example, instead of separate click, type, and press key turns, the model can emit one computer_batch call containing all three actions.

在更新后的参考实现中，我们在标准 computer 与 browser 工具之外提供了两个工具：computer_batch 和 browser_batch。每个工具都接受一个子动作列表，并在一次工具调用中执行它们。例如，模型不再用单独的轮次分别点击、输入、按键，而是可以发出一次包含全部三个动作的 computer_batch 调用。

The appeal is efficiency: a workflow with N mechanical actions is a single round trip instead of N round trips, which on long-horizon tasks meaningfully reduces wall-clock time and output token spend. The risk is compounding error, if action 2 depends on visual state that action 1 changed, and action 1 misses, the rest of the batch operates on stale assumptions and the agent can drift without ever seeing a screenshot of the actual state.

它的吸引力在于效率：一个包含 N 个机械动作的工作流只需一次往返（round trip），而不是 N 次，这在长时程任务上能显著缩短实际耗时并减少输出 token 开销。风险则是误差复合：如果动作 2 依赖于动作 1 改变后的视觉状态，而动作 1 没有命中，批处理的其余动作就会在过时的假设上执行，agent 可能在从未看到实际状态截图的情况下越走越偏。

We recommend batch tools when the sub-actions are self-contained and don't depend on each other's visual outcomes (filling multiple fields in a form, chaining keyboard shortcuts, scrolling and clicking a known target). We'd avoid them in exploratory navigation, error-recovery sequences, or any workflow where "if action 1 fails I need to re-plan" is a real state.

当子动作彼此独立、不依赖彼此的视觉结果时（在表单中填写多个字段、串联键盘快捷键、滚动后点击一个已知目标），我们推荐使用批量工具。在探索式导航、错误恢复序列，或任何“一旦动作 1 失败我就得重新规划”是真实状态的工作流中，我们则不建议使用。

Because batch tools are your own custom definitions, they stack cleanly with the standard computer or browser tools. Keep both available and let the model choose.

由于批量工具是你自己的自定义定义，它们可以与标准 computer 或 browser 工具干净地叠加。两者都保持可用，让模型自己选。

# advisor 工具（beta）（The advisor tool (beta)）

The advisor tool pairs an executor model with a higher-intelligence advisor model that the executor can consult mid-generation for strategic guidance. The executor runs the loop and when it hits something that needs deeper reasoning, it calls the advisor, receives a plan or course correction, and continues. This happens server-side inside a single request, no extra round trips on your side.

advisor 工具把一个执行器（executor）模型与一个更高智能的顾问（advisor）模型配对，执行器可以在生成过程中向顾问请教战略性指导。执行器负责跑循环，当遇到需要更深层推理的环节时，它调用顾问、收到一份计划或路线修正，然后继续。这一切都在服务端的单次请求内完成，你这一侧没有额外往返。

For computer use specifically, this pattern is most useful on long-horizon tasks where most turns are mechanical clicking but occasional planning moments (choosing which tab to open, recovering from an unexpected modal, deciding whether to abandon a strategy) benefit from Opus-level reasoning. You get close to advisor-solo quality while the bulk of token generation happens at executor rates.

具体到计算机使用，这个模式在长时程任务上最有用：大多数轮次是机械性点击，但偶发的规划时刻（选择打开哪个标签页、从意外的模态框中恢复、决定是否放弃某个策略）能从 Opus 级推理中受益。你能在按执行器费率生成绝大部分 token 的同时，获得接近顾问单独出马的质量。

Example of enabling the advisor tool:

启用 advisor 工具的示例：

```python
response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=16000,
    betas=["advisor-tool-2026-03-01", "computer-use-2025-11-24"],
    tools=[
        {
            "type": "advisor_20260301",
            "name": "advisor",
            "model": "claude-opus-4-7",
        },
        {
            "type": "computer_20251124",
            "name": "computer",
            "display_width_px": 1280,
            "display_height_px": 720,
        },
    ],
    messages=[...],
)
```

Useful controls for the advisor tool include:

advisor 工具的有用控制项包括：

- max_uses: cap advisor calls per request. Helpful when you want to bound the worst-case cost.
- Conversation-wide cap in your harness: the advisor bills at Opus 4.7 rates for each consult, so on very long sessions you may want to stop offering the advisor after some number of uses.
- Advisor-side caching: on multi-call conversations, caching the advisor's prefix pays off after roughly three consults. In the reference implementation we default to 5-minute ephemeral caching.

- max_uses：限制每请求的顾问调用次数。当你想框定最坏情况成本时很有用。
- 在 harness 中设置会话级上限：顾问每次咨询都按 Opus 4.7 费率计费，因此在很长的会话中，你可能希望在若干次使用后不再向模型提供顾问。
- 顾问侧缓存：在多调用会话中，缓存顾问的前缀大约三次咨询后就开始划算。参考实现中我们默认使用 5 分钟的临时（ephemeral）缓存。

Two non-obvious things worth knowing: the advisor runs without tools and without context management, so it can't click or browse on your behalf, it only returns text advice. And because the executor model doesn't always remember the advisor exists on long-horizon tasks, see the reminder nudges section below.

有两件不那么显眼的事值得了解：advisor 运行时不带工具、也没有上下文管理，所以它不能替你点击或浏览，只会返回文本建议。另外，由于执行器模型在长时程任务上并不总能记得 advisor 的存在，请参阅下文的提醒助推（reminder nudges）一节。

# 清理孤立的 advisor 块（Cleaning up orphaned advisor blocks）

When the advisor tool fires, the executor emits a server_tool_use block with name: "advisor" followed by an advisor_tool_result block in the returned content. These blocks live in your messages array alongside everything else.

当 advisor 工具触发时，执行器会发出一个 name 为 "advisor" 的 server_tool_use 块，随后在返回内容中出现一个 advisor_tool_result 块。这些块和其他内容一起留在你的消息数组里。

If you later drop the advisor tool from your tools array - because you hit a conversation-wide cap, changed config, or switched models - those prior server_tool_use / advisor_tool_result blocks become orphaned. The API will return a 400 on the next request because the referenced tool is no longer declared.

如果你之后从 tools 数组中移除了 advisor 工具--因为触及会话级上限、更改配置或切换模型--那些先前的 server_tool_use / advisor_tool_result 块就成了孤立块。API 会在下一次请求返回 400，因为被引用的工具已不再声明。

The fix is a simple pre-send pass: whenever the advisor is disabled for a turn, walk the message history and strip any content blocks of type server_tool_use (with name == "advisor") and advisor_tool_result.

修复方法是一个简单的发送前遍历：只要某轮禁用了 advisor，就遍历消息历史，剥离所有类型为 server_tool_use（且 name == "advisor"）以及 advisor_tool_result 的内容块。

Example of removing stale advisor blocks:

移除过期 advisor 块的示例：

```python
def strip_orphaned_advisor_blocks(messages):
    """Remove advisor server_tool_use / tool_result blocks from history.
    Call this before any request that doesn't include the advisor tool."""
    for msg in messages:
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        msg["content"] = [
            block
            for block in content
            if not (
                isinstance(block, dict)
                and (
                    (block.get("type") == "server_tool_use" and block.get("name") == "advisor")
                    or block.get("type") == "advisor_tool_result"
                )
            )
        ]
    return messages
```

# 周期性提醒助推（Periodic reminder nudges）

On long sessions, the executor model can forget which tools are available or which ones it should prefer. Two short reminder patterns have helped in our testing:

在长会话中，执行器模型可能忘记哪些工具可用，或应该优先用哪些。在我们的测试中，两种简短的提醒模式很有帮助：

Batch reminder. If you expose computer_batch or browser_batch alongside the standard tools and observe the model chaining single-action calls when a batch would be appropriate, append a short system-level nudge after the next tool result: "Remember you can use computer_batch to combine sequential actions in a single tool call when they don't depend on intermediate screenshots." The goal is to pull the model back toward batching without dictating exactly when.

批量提醒。如果你在标准工具之外提供了 computer_batch 或 browser_batch，却观察到模型在适合批处理时仍连续发起单动作调用，可以在下一个工具结果之后追加一条简短的系统级提示：“记住，当连续动作不依赖中间截图时，你可以使用 computer_batch 将它们合并到一次工具调用中。”目标是把模型拉回到批处理方向，而不硬性规定具体时机。

Advisor reminder. The advisor tool is easy for the executor to forget exists, especially if it hasn't been called in many turns. On sessions longer than ~20 turns without an advisor call, append a brief reminder that the advisor is available for planning or course-correction moments. In the reference implementation we use a 20-turn cadence and append a one-line hint.

advisor 提醒。执行器很容易忘记 advisor 工具的存在，尤其是在很多轮都没调用过它的情况下。当会话超过约 20 轮仍未调用 advisor 时，追加一条简短提醒，说明 advisor 可用于规划或路线修正时刻。在参考实现中，我们以 20 轮为节奏追加一行提示。

Both nudges are light-touch context injections, not system-prompt rewrites. They cost a few tens of input tokens per append. If your system prompt is already long or your cache breakpoints are precisely placed, weigh whether the lift is worth the added invalidation risk.

两种助推都是轻量的上下文注入，而非对 system prompt 的重写。每次追加只消耗几十个输入 token。如果你的 system prompt 已经很长，或缓存断点放置得很精确，请权衡收益是否值得额外的失效风险。

# 参考实现中的调试模式（Debugging patterns in the reference implementation）

When something misbehaves and you're not sure whether the problem is your harness, your screenshots, or the model, three side utilities in the reference implementation are worth reaching for before you start adding logging:

当某个环节表现异常、而你不确定问题出在 harness、截图还是模型时，在开始添加日志之前，参考实现中的三个辅助工具值得一试：

- Trajectory viewer (streamlit run viewer/app.py). Loads a recorded trajectory and lets you step through the agent's turns with screenshots, thinking, tool calls, and usage per step. Best for answering "what did the model actually see, and what did it decide?" after a failed run.
- Tool debug panel (uvicorn debug.server:app --reload). A small web UI that lets you exercise each tool individually: take a screenshot, capture click coordinates, type, scroll, zoom. Useful for confirming that your capture pipeline and coordinate scaling are actually producing what you expect.
- Localization playground (uvicorn localize.server:app --reload --port 8001). Upload any image and ask the model to point at a target. Renders the predicted coordinates back on your image at both display and native resolution. This is the fastest way to diagnose whether a click miss is a resize bug, a coordinate-scaling bug, or a genuine model error. This is especially useful when a customer reports bad clicks and you want to reproduce the failure in isolation.

- 轨迹查看器（streamlit run viewer/app.py）。加载一条已录制的轨迹，让你逐步查看 agent 的各轮，包含每步的截图、思考、工具调用和用量。最适合在失败运行之后回答“模型到底看到了什么，做了什么决定？”。
- 工具调试面板（uvicorn debug.server:app --reload）。一个小型 Web UI，让你逐个试用每个工具：截图、捕获点击坐标、输入、滚动、缩放。可用于确认你的捕获管线和坐标缩放确实产出了你预期的结果。
- 定位演练场（uvicorn localize.server:app --reload --port 8001）。上传任意图像并让模型指向某个目标。它会把预测坐标以显示分辨率和原生分辨率两种形式渲染回你的图像上。这是诊断一次点击失手究竟是缩放尺寸 bug、坐标换算 bug 还是真正的模型错误的最快方法。当客户报告点击不准、而你想单独复现该故障时尤其有用。

None of these are required to build a working integration; they're debugging aids for when the default feedback loop (log, re-run, squint at transcripts) isn't fast enough.

这些都不是构建可用集成的必需品；它们是当默认反馈回路（记日志、重跑、眯着眼睛盯记录）不够快时的调试辅助。

# 提升可靠性：教 Claude（Improving reliability: teaching Claude）

Instead of iterating on text prompts until Claude gets a workflow right, you can show it the correct behavior directly. Record yourself performing the task, capturing screenshots, actions, and optionally voice narration at each step, then replay that demonstration as context when Claude executes the same workflow. The recording becomes a reusable specification Claude can follow, adapting to differences in the live UI state.

与其反复迭代文字提示词直到 Claude 把某个工作流做对，不如直接把正确行为演示给它看。录制你自己执行任务的过程，在每一步捕获截图、动作以及可选的语音解说，然后在 Claude 执行同一工作流时，把这段演示作为上下文回放给它。这份录制就成了一份可复用的规范，Claude 可以遵循它并适应实际 UI 状态的差异。

We use this pattern internally in Claude in Chrome (where we call it "Teach Mode") and are sharing it here because the underlying approach is broadly useful for anyone building computer use or browser use products. It helps in two ways: improving reliability on workflows Claude can mostly handle but occasionally gets wrong, and unlocking entirely new workflows that Claude can't complete from a text prompt alone. The core idea (capture a demonstration, feed it back as context) is straightforward to implement and adapts well to both browser and desktop environments.

我们在 Claude in Chrome 内部使用了这一模式（我们称之为“Teach Mode”），在此分享是因为这一底层方法对任何构建计算机使用或浏览器使用产品的人都有广泛用处。它在两方面有帮助：提升 Claude 大体掌握但偶尔出错的工作流的可靠性；解锁仅凭文字提示词 Claude 无法完成的全新工作流。核心思路（捕获一次演示，再作为上下文喂回去）实现起来直截了当，且能很好地适配浏览器与桌面两种环境。

## 核心理念：演示，而非描述（The core concept: show, don't tell）

Traditional prompt engineering asks users to describe what they want in words, then iterate when the AI misunderstands. This pattern inverts that: users demonstrate the task while the system records their actions, screenshots, and (optionally) voice narration. During playback, Claude receives the full demonstration as context and follows the same sequence of steps, adapting to any differences in the current UI state.

传统的提示词工程要求用户用语言描述想要什么，然后在 AI 误解时反复迭代。这个模式正好反过来：用户演示任务，系统记录他们的动作、截图以及（可选的）语音解说。回放时，Claude 收到完整演示作为上下文，遵循相同的步骤序列，并适应当前 UI 状态的任何差异。

The key insight is that playback isn't strict replay. Claude uses the demonstration as a guide while reasoning about the live environment. If a button has moved or a menu has been reorganized, Claude can find the equivalent element in the current UI rather than blindly clicking at recorded coordinates.

关键的洞察在于：回放不等于严格重放。Claude 把演示当作指引，同时对实时环境进行推理。如果按钮挪了位置或菜单被重新组织，Claude 能在当前 UI 中找到等价元素，而不是盲目地按录制的坐标点击。

## 数据模型（The data model）

The fundamental unit is a "workflow step", a single action captured during recording. Each step bundles what was done, where it happened, and what the screen looked like:

基本单位是“工作流步骤（workflow step）”，即录制过程中捕获的单个动作。每个步骤把做了什么、发生在哪里、以及当时屏幕是什么样打包在一起：

```python
from dataclasses import dataclass, field
from typing import Literal, Optional


@dataclass
class WorkflowStep:
    action: Literal["click", "type", "navigate", "scroll", "select"]
    description: str  # Human-readable, e.g. "Click the Submit button"
    timestamp: float
    selector: Optional[str] = None  # CSS selector or XPath
    coordinates: Optional[dict] = None  # {"x": int, "y": int}
    url: Optional[str] = None
    screenshot: Optional[str] = None  # Base64-encoded screenshot
    viewport_dimensions: Optional[dict] = None  # {"width": int, "height": int}
    speech_transcript: Optional[str] = None  # Voice narration, if captured
    value: Optional[str] = None  # For type actions


@dataclass
class SavedWorkflow:
    id: str
    name: str  # e.g. "Submit expense report"
    steps: list[WorkflowStep] = field(default_factory=list)
    description: Optional[str] = None  # AI-generated summary of the workflow
    start_url: Optional[str] = None
    created_at: float = 0.0
    usage_count: int = 0
```

Capturing both selectors and coordinates is intentional: selectors are more robust to layout changes, but coordinates provide a visual fallback Claude can use when selectors break. Viewport dimensions are stored so coordinates can be scaled when the playback environment differs from the recording environment.

同时捕获选择器（selector）和坐标是有意为之：选择器对布局变化更稳健，但当选择器失效时，坐标提供了 Claude 可以使用的视觉后备。存储视口（viewport）尺寸，是为了在回放环境与录制环境不一致时能够换算坐标。

## 录制：捕获什么（Recording: what to capture）

At minimum, capture click events, keyboard input, navigation changes, and a screenshot at each action. For each click, generate a human-readable description (from aria-labels, text content, or via a quick Claude call) and annotate the screenshot with a visual marker at the click position:

至少要捕获点击事件、键盘输入、导航变更，以及每个动作时的截图。对每次点击，生成一段人类可读的描述（来自 aria-label、文本内容，或通过一次快速的 Claude 调用），并在截图的点击位置上标注一个可视化标记：

```python
def on_click(event):
    step = WorkflowStep(
        action="click",
        selector=generate_selector(event.target),
        coordinates={"x": event.client_x, "y": event.client_y},
        url=current_url(),
        description=generate_description(event.target),
        timestamp=now(),
        viewport_dimensions=get_viewport_size(),
    )

    # Annotate screenshot with a circle at the click position
    screenshot = capture_screenshot()
    step.screenshot = annotate_with_circle(screenshot, event.client_x, event.client_y)

    workflow_steps.append(step)
```

The annotation (a colored circle at the click location) serves two purposes: it helps users verify the recording captured the right element, and during playback it shows Claude exactly where the action occurred. Your playback prompt should clarify that these markers are recording artifacts, not part of the live UI.

这个标注（点击位置的一个彩色圆圈）有两个作用：帮助用户确认录制捕获的是正确的元素；在回放时向 Claude 精确展示动作发生的位置。你的回放提示词应当说明，这些标记是录制产物，不属于实际 UI 的一部分。

## 回放：构造提示词（Playback: constructing the prompt）

This is the most important piece. When a user triggers a saved workflow, you construct a message to Claude containing three things: the user's intent, a context block explaining the demonstration format, and the recorded screenshots.

这是最关键的一环。当用户触发一个已保存的工作流时，你要构造一条发给 Claude 的消息，其中包含三样东西：用户的意图、一段解释演示格式的上下文块，以及录制的截图。

The context block tells Claude how to interpret annotated screenshots and how to adapt when the live UI differs:

这个上下文块告诉 Claude 如何解读带标注的截图，以及当实际 UI 与之不同时如何应变：

```python
def generate_playback_context(steps: list[WorkflowStep]) -> str:
    steps_description = "\n".join(
        f"Step {i+1}: {step.description}"
        for i, step in enumerate(steps)
    )

    return f"""<demonstration_context>
The user has recorded a demonstration showing how to perform this task.

RECORDED STEPS:
{steps_description}

ABOUT THE SCREENSHOTS:
- Each screenshot shows the screen state when an action was taken
- BLUE CIRCLES mark where the user clicked - these are recording annotations
- The blue highlighting is NOT part of the actual interface
- Your own screenshots will NOT have these markers

HOW TO USE THIS DEMONSTRATION:
1. Review all steps and screenshots to understand the complete workflow
2. Take your own screenshot to see the CURRENT page state
3. The blue highlights show which element to interact with - find it in your current view
4. Follow the same sequence of actions, adapting to any differences
5. If the UI has changed significantly, use judgment to find equivalent elements
</demonstration_context>"""
```

Then assemble the full message with the user's prompt, the context block, and each step's screenshot as an image:

然后把用户提示词、上下文块，以及每一步的截图（作为图像）组装成完整消息：

```python
import anthropic

client = anthropic.Anthropic()

content = [
    {"type": "text", "text": user_prompt},
    {"type": "text", "text": generate_playback_context(workflow.steps)},
]

for i, step in enumerate(workflow.steps):
    if step.screenshot:
        content.append({"type": "text", "text": f"[Step {i+1}: {step.description}]"})
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": step.screenshot},
        })

response = client.beta.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=4096,
    betas=["computer-use-2025-11-24"],
    messages=[{"role": "user", "content": content}],
    tools=[{
        "type": "computer_20251124",
        "name": "computer",
        "display_width_px": 1280,
        "display_height_px": 720,
    }],
)
```

## 回放模式（Playback modes）

Not every workflow needs the same level of adherence to the recorded demonstration. Some workflows are too long, consuming a significant amount of input tokens which ultimately degrades latency and increases cost. Consider supporting a strictness parameter that you include in the context prompt:

并非每个工作流都需要对录制演示保持同样的遵循程度。有些工作流太长，会消耗大量输入 token，最终拖累延迟并推高成本。可以考虑支持一个严格度（strictness）参数，并将其纳入上下文提示词：

Strict: follow steps exactly; stop and report if the UI has changed too much. Good for compliance-sensitive workflows where the exact sequence matters.

严格（Strict）：完全按步骤执行；若 UI 变化过大则停下来报告。适合对合规敏感、精确顺序至关重要的工作流。

Adaptive: use the demonstration as a guide but adapt to UI changes. This is the best default for most use cases - it handles minor layout shifts, updated button labels, and reorganized menus gracefully.

自适应（Adaptive）：以演示为指引，但适应 UI 变化。这是大多数用例的最佳默认--它能优雅处理轻微布局偏移、按钮文案更新和菜单重组。

‍Goal-oriented: focus on the end result; treat the recorded steps as hints rather than instructions. Useful when the UI changes frequently but the goal stays the same. Use a model to summarize the recorded demonstration, using strategies similar to the one described in the next section, then pass that summary to the CU model.

目标导向（Goal-oriented）：聚焦最终结果；把录制的步骤当作提示而非指令。适用于 UI 频繁变化但目标不变的场景。用一个模型对录制演示做摘要（策略与下一节所述类似），然后把该摘要传给计算机使用（CU）模型。

## 示例：端到端报销工作流（Example: end-to-end expense report workflow）

Here's what a saved workflow looks like in practice. The workflow captures five steps: navigating to the expense form, selecting an expense type, choosing "Travel" from the dropdown, entering an amount, and clicking Submit.

下面是一个已保存工作流在实践中的样子。该工作流捕获五个步骤：导航到报销表单、选择报销类型、在下拉菜单中选择“Travel（差旅）”、输入金额，以及点击提交。

```python
expense_workflow = SavedWorkflow(
    id="wf_abc123",
    name="Submit Expense Report",
    start_url="https://expenses.company.com/new",
    steps=[
        WorkflowStep(
            action="navigate",
            url="https://expenses.company.com/new",
            description="Navigate to new expense form",
            timestamp=1700000000,
        ),
        WorkflowStep(
            action="click",
            selector="#expense-type-dropdown",
            coordinates={"x": 400, "y": 200},
            description="Click on expense type dropdown",
            timestamp=1700000001,
        ),
        WorkflowStep(
            action="click",
            selector="[data-value='travel']",
            coordinates={"x": 400, "y": 280},
            description='Select "Travel" expense type',
            timestamp=1700000002,
        ),
        WorkflowStep(
            action="type",
            selector="#amount-input",
            value="150.00",
            description="Enter expense amount",
            timestamp=1700000003,
        ),
        WorkflowStep(
            action="click",
            selector="#submit-expense-btn",
            coordinates={"x": 1150, "y": 420},
            description="Click the Submit button",
            speech_transcript="Now I'll click submit to send the report for approval",
            timestamp=1700000004,
        ),
    ],
)
```

When a user later says "Submit my expense report for the team lunch ($85.50)", the playback service constructs a prompt with the demonstration context, all five annotated screenshots, and the specific values from the new request. Claude sees exactly where to click, what sequence to follow, and adapts the amounts and descriptions to match the current task. If your workflow is too long for this approach to be practical due to input token count, then consider first compacting the workflow before using it as an example. See the following section for tips on managing context.

当用户随后说“帮我提交团队午餐的报销（85.50 美元）”时，回放服务会构造一个提示词，其中包含演示上下文、全部五张带标注的截图，以及新请求中的具体数值。Claude 能准确看到该点哪里、按什么顺序执行，并调整金额和描述以匹配当前任务。如果由于输入 token 数量导致工作流太长、这种方式不够实际，可以考虑先把工作流压缩，再将其用作示例。关于管理上下文的技巧，请参阅下一节。

# 计算机与浏览器使用入门（Getting started with computer and browser use）

These practices reflect our current best understanding of what makes computer use integrations reliable in production. They apply to the Claude 4.6 model family and Opus 4.7, and will be updated as new models and techniques emerge.

这些实践反映了我们目前对“什么让计算机使用集成在生产环境中可靠”的最佳理解。它们适用于 Claude 4.6 模型家族和 Opus 4.7，并将随着新模型和新技术的出现而更新。

As your integration matures, the patterns that matter most will depend on your specific environment, target applications, and reliability requirements.‍

随着你的集成日趋成熟，最重要的模式将取决于你的具体环境、目标应用和可靠性要求。

Get started with the computer use documentation, check out our new demo implementation of these best practices, or revisit the original computer use research post for background on how these capabilities were built and where they're headed.

可以从计算机使用文档入手，查看我们对这些最佳实践的全新演示实现，或回顾最初的计算机使用研究文章，了解这些能力是如何构建的以及它们的发展方向。

Acknowledgements: This article & corresponding demo were written by Lucas Gonzalez and Luca Weihs. The authors would like to thank Molly Vorwerck, Javier Rando, Maya Nielan, Gabe Mulley, and Brigit Brown for their contributions.

致谢：本文及相应演示由 Lucas Gonzalez 和 Luca Weihs 撰写。作者感谢 Molly Vorwerck、Javier Rando、Maya Nielan、Gabe Mulley 和 Brigit Brown 的贡献。
