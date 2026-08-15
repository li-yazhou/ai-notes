---
type: overview
title: "NVIDIA GPU 产品线总览（按发布时间）"
created: 2026-08-15
updated: 2026-08-15
status: active
tags:
  - vendor/nvidia
  - hardware/gpu
  - topic/inference
---

# NVIDIA GPU 产品线总览（按发布时间）

> 范围：NVIDIA **数据中心 GPU**（重点，AI 训练 / 推理）、**GeForce 消费级**、**工作站 / 边缘设备**、**中国市场特供版**，按发布时间排序
> 信息来源：NVIDIA 官网产品页（2026-08 快照）、Wikipedia；标 ❓ 的为报道口径或待核实数字
> 关联：LLM 侧硬件选型背景，配合 [[01-deepseek-overview]]、[[03-kimi-overview]]、[[01-glm-overview]] 阅读

---

## 〇、一页时间线

| 时间         | 产品                                      | 架构 / 制程               | 一句话要点                                               |
| ---------- | --------------------------------------- | --------------------- | --------------------------------------------------- |
| 1999-10    | GeForce 256                             | 固定管线 / 220nm          | 首个被称作 "GPU" 的消费显卡（硬件 T&L）                           |
| 2006-11    | GeForce 8800 GTX                        | Tesla / 90nm          | 统一着色器架构；2007 年随 G80 发布 **CUDA**，GPU 通用计算起点          |
| 2016-04    | **Tesla P100**                          | Pascal / 台积电 16nm     | 首张 NVLink、首用 HBM2 的计算卡；DGX-1 开启 AI 一体机时代            |
| 2017-05    | **Tesla V100**                          | Volta / 台积电 12nm      | 首代 **Tensor Core**，FP16 Tensor 125 TFLOPS           |
| 2018-09    | Tesla T4 / RTX 2080                     | Turing / 12nm         | 推理专用低功耗卡；消费线首次加入 RT Core + Tensor Core（DLSS 起点）     |
| 2020-05    | **A100**                                | Ampere / 台积电 7nm      | MIG 切分 + 稀疏化加速，40GB→80GB HBM2e，AI 云算力标配三年           |
| 2022-03    | **H100**                                | Hopper / 台积电 4N       | **Transformer Engine + FP8**，生成式 AI 引擎，一度缺货 36–52 周 |
| 2023-05    | GH200                                   | Hopper + Grace        | 首个 Grace CPU 合封 superchip（GPU+CPU 统一内存）             |
| 2023-11    | **H200**                                | Hopper / 4N           | 显存升级 141GB HBM3e @ 4.8TB/s，算力同 H100，主打推理            |
| 2024-03    | **B200 / GB200**                        | Blackwell / 台积电 4NP   | 双 die 合封 2080 亿晶体管，FP4 + NVL72 机架级系统                |
| 2025-01    | **RTX 50 系列**                           | Blackwell / 4N        | 消费级 GDDR7 + DLSS 4 多帧生成，5090 32GB                   |
| 2025-03    | **B300 / GB300**（Blackwell Ultra）       | Blackwell Ultra / 4NP | 288GB HBM3e，FP4 +50%，主打 test-time scaling 推理        |
| 2025-10    | Rubin CPX ❓                             | Rubin / 3nm ❓         | 推理专用 GDDR7 版本（去 HBM 降本），2026 年中出货                   |
| 2025-12    | NVIDIA × Groq 交易                        | —                     | 200 亿美元收购 Groq 资产 + 推理技术非独占授权                       |
| 2026-01~03 | **Vera Rubin（VR200 / NVL72）**           | Rubin / 3nm ❓         | HBM4 + NVFP4 + NVLink 6 + 自研 Vera CPU，2026 H2 上市    |
| 2026-08    | NVIDIA Groq 3 LPX / Vera Rubin with LPX | —                     | GPU（HBM）+ LPU（SRAM）混合推理机架，面向万亿参数长上下文                |
| 2027 H2    | Rubin Ultra NVL576（路线图）                 | —                     | 单机柜 576 个 GPU die；2028 下一代代号 Futuname ❓             |

---

## 一、数据中心 GPU 详解（按时间）

### 1. Tesla P100（2016-04）—— Pascal，现代 AI 数据中心起点

- **规格**：台积电 16nm，153 亿晶体管，16GB HBM2 @ 720GB/s，FP16 19.5 TFLOPS，**NVLink 1**（160GB/s），300W
- **意义**：首张同时用上 HBM2 和 NVLink 的计算卡；配套 **DGX-1**（8×P100，$129,000）开创 "AI 超算一体机" 品类。同年消费级 GTX 1080 同架构。

### 2. Tesla V100（2017-05 发布）—— Volta，Tensor Core 元年

- **规格**：台积电 12FFN，211 亿晶体管，640 个 **Tensor Core**（首代），16GB（后 32GB）HBM2 @ 900GB/s，FP16 Tensor 125 TFLOPS，NVLink 2（300GB/s），300W
- **意义**：为混合精度矩阵乘法设计的专用单元成为此后所有架构的标配；2018 年 **NVSwitch** + DGX-2（16×V100-32GB）实现机内全互联。

### 3. Tesla T4（2018-09）—— Turing，首张"推理专用"卡

- **规格**：16GB GDDR6 @ 320GB/s，INT8 65 TOPS（稀疏 130），仅 70W，单槽半高
- **意义**：面向在线推理 / 视频转码的低功耗卡，长期占据云厂商推理实例；同年 RTX 2080 把 Tensor Core 带进消费线。

### 4. A100（2020-05 发布；80GB 版 2020-11）—— Ampere，AI 云算力标配

- **规格**：台积电 7nm，540 亿晶体管，40GB HBM2 @ 1.55TB/s → **80GB HBM2e @ 2.0TB/s**；FP16 Tensor 312 TFLOPS（稀疏 624）、TF32 156（稀疏 312）、FP64 9.7 TFLOPS；**NVLink 3** 600GB/s；400W SXM4
- **关键特性**：**MIG**（单卡切 7 个隔离实例，推理云卖点）、结构化稀疏 2× 加速
- **意义**：2020–2023 全球大模型训练事实标准（GPT-3 即 1 万张 V100 训练）；2022–2023 补充 A30/A10/A40/L4/L40S 覆盖推理与图形（L4：2023，24GB GDDR6，72W，GCP 推理主力）。

### 5. H100（2022-03 GTC 发布，2022 Q4 上市）—— Hopper，生成式 AI 引擎

- **规格**：台积电 4N（5nm 级），800 亿晶体管，132 SM；80GB **HBM3** @ 3.35TB/s；FP8/FP16 Tensor 1979 TFLOPS（稀疏 3958）；**NVLink 4** 900GB/s；700W SXM
- **关键特性**：**Transformer Engine**（FP8 动态量化）、线程块集群、DPX 指令
- **市场**：2023 年 AI 热潮下交货周期一度 36–52 周，单季卖出 50 万张，把 NVIDIA 市值推过 $2T
- **变体**：H100 NVL（2023-03，2×94GB=188GB，为 ChatGPT 类推理设计）；GH200（2023-05，Grace CPU + H100 合封，最高 141GB HBM3 + 480GB LPDDR5X）

### 6. H200（2023-11 发布，2024 Q2 上市）—— Hopper 显存升级版

- **规格**：**141GB HBM3e @ 4.8TB/s**（H100 的 1.4× 容量、1.4× 带宽），算力与 H100 相同
- **意义**：首次把"推理是显存带宽游戏"写进产品定义——Llama 2-70B 推理吞吐显著高于 H100；证实了 NVIDIA "一年一代" 新节奏（2023-10 投资者会议宣布数据中心从两年一代改为每年一代）。

### 7. B100 / B200 / GB200（2024-03-18 GTC 发布）—— Blackwell

- **B200 规格**：台积电 4NP，**双 die 合封 2080 亿晶体管**（NV-HBI 互联 10TB/s），**192GB HBM3e @ 8TB/s**，FP4 9 PFLOPS（稀疏 18），1000W，NVLink 5（1.8TB/s）
- **GB200 superchip**：1× Grace CPU + 2× B200（每 GPU 拉到 1200W，FP4 稀疏 10 PF）；Grace 72 核 Neoverse V2 + 480GB LPDDR5X，NVLink-C2C 互联
- **GB200 NVL72**：机架级产品——36 Grace + 72 Blackwell + 18 NVLink 交换器，**130TB/s 全互联 NVLink**，液冷，整机 FP4 推理 1440 PFLOPS（稀疏）/ FP8 训练 720 PFLOPS
- **波折**：2024-10 曝出掩膜级设计缺陷（联合台积电修复）；2024-11 Morgan Stanley 称 2025 年产能已全部售罄；B100 基本被跳过，直接 B200/GB200
- **意义**：计算单位从"卡"变成"机架"；FP4 + 第二代 Transformer Engine（MXFP4/MXFP6）把推理精度推入 4-bit 时代。

### 8. B300 / GB300（2025-03-18 GTC 发布）—— Blackwell Ultra

- **B300 规格**：**288GB HBM3e** @ 8TB/s（容量 1.5×，带宽不变），FP4 15 PFLOPS（稀疏 20，较 B200 +50%），约 1400W
- **GB300 NVL72**（官网数字）：72× Blackwell Ultra + 36× Grace；FP4 1440 PFLOPS（稀疏）/ 1080（稠密）、FP8/FP6 720 PFLOPS（稠密）；GPU 显存合计 20TB @ 576TB/s，另有 17TB LPDDR5X；NVLink 130TB/s；FP8 吞吐较 GB200 +50%，注意力层性能 2×
- **定位**：明确面向 **test-time scaling 推理**（DeepSeek-R1 类推理模型），官方口径 "为 AI 推理时代而生"；配套 Dynamo 开源推理框架；2025 H2 出货

### 9. Rubin CPX（2025-10 GTC DC 发布 ❓）—— 推理专用 GDDR7 版本

- 定位：把 Rubin 的计算能力配上 **GDDR7**（替代 HBM）以降低成本，专攻高吞吐推理；2026 年中出货
- ❓ 规格细节（128GB GDDR7、NVFP4 算力等）以官方新闻稿为准，待核实

### 10. Vera Rubin（2026-01 CES 首发亮相，2026-03 GTC 正式发布）—— 2026 旗舰

- **Rubin GPU**（官网"初步规格"）：**288GB HBM4 @ 22TB/s**（带宽约为 B300 的 2.75×）；**NVFP4 推理 50 PFLOPS（稠密）**/ 训练 35 PFLOPS，FP8/FP6 17.5 PFLOPS，FP16 4 PFLOPS，FP64 33 TFLOPS；**NVLink 6** 3.6TB/s；配套 ConnectX-9 SuperNIC（1.6Tb/s）+ BlueField-4 DPU
- **Vera CPU**：自研 **Olympus 核心**（Arm 兼容），每 CPU 88 核 + 1.5TB LPDDR5X，取代 Grace；NVLink-C2C 1.8TB/s
- **Vera Rubin NVL72**：72 Rubin GPU + 36 Vera CPU，机柜 NVFP4 推理 **3600 PFLOPS（稠密）**、HBM4 合计 20.7TB；第三代 MGX 机架、免线缆模块化托盘；官方口径：相比 Blackwell **训练用 1/4 的 GPU、推理每百万 token 成本 1/10**
- 上市节奏：2026 H2（截至 2026-08 官网标注 preliminary）

### 11. NVIDIA Groq 3 LPX / Vera Rubin with LPX（2026，官网已上线）

- **背景**：2025-12，NVIDIA 与 Groq 达成 **200 亿美元现金收购资产** + 推理技术非独占授权，Groq CEO 等高管加入 NVIDIA，Groq 品牌继续独立运营
- **产品**：**Vera Rubin with LPX** —— Rubin GPU（HBM 大容量）+ **Groq 3 LPU（SRAM 低延迟）**混合机架；每颗 LPU 加速器 500MB SRAM、SRAM 带宽 150TB/s、扩展互联 2.5TB/s
- **定位**：万亿参数模型 + 百万 token 上下文的极致低延迟推理；"GPU 管容量、LPU 管延迟" 的新品类

### 12. 后续路线图（GTC 2025 公布）

- **Rubin Ultra NVL576**：2027 H2，单机柜 576 个 GPU die
- **Futuname** ❓：2028 下一代（代号以 GPU 命名传统延续）

### 数据中心规格对比表

| 型号 | 发布 | 显存 / 带宽（每卡） | 代表算力（稠密） | NVLink | 功耗 |
| --- | --- | --- | --- | --- | --- |
| P100 | 2016-04 | 16GB HBM2 / 0.72TB/s | FP16 19.5 TF | 160GB/s（V1） | 300W |
| V100 | 2017-05 | 16/32GB HBM2 / 0.9TB/s | FP16 Tensor 125 TF | 300GB/s（V2） | 300W |
| T4 | 2018-09 | 16GB GDDR6 / 0.32TB/s | INT8 65 TOPS | —（PCIe） | 70W |
| A100 | 2020-05 | 40/80GB HBM2e / 2.0TB/s | FP16 312 TF | 600GB/s（V3） | 400W |
| H100 SXM | 2022-03 | 80GB HBM3 / 3.35TB/s | FP8 1979 TF | 900GB/s（V4） | 700W |
| H200 | 2023-11 | 141GB HBM3e / 4.8TB/s | FP8 1979 TF | 900GB/s（V4） | 700W |
| B200 | 2024-03 | 192GB HBM3e / 8TB/s | FP4 9 PF | 1.8TB/s（V5） | 1000W |
| B300 | 2025-03 | 288GB HBM3e / 8TB/s | FP4 15 PF | 1.8TB/s（V5） | ~1400W |
| Rubin | 2026 H2 | 288GB HBM4 / 22TB/s | NVFP4 50 PF | 3.6TB/s（V6） | ❓ |

> 注：算力口径各异（稀疏 / 稠密 / 训练 / 推理），表中尽量取稠密口径；Vera Rubin 为官网 preliminary 数字。

---

## 二、NVL 机架级系统对比

| 系统 | 发布 | 构成 | 机柜算力 | GPU 显存合计 |
| --- | --- | --- | --- | --- |
| DGX-2（NVSwitch 雏形） | 2018 | 16× V100-32GB | FP16 2 PF | 0.5TB HBM2 |
| GB200 NVL72 | 2024-03 | 36 Grace + 72 B200 | FP4 1440 PF（稀疏） | 13.8TB HBM3e |
| GB300 NVL72 | 2025-03 | 36 Grace + 72 B300 | FP4 1080 PF（稠密）/ FP8 720 PF | 20TB HBM3e（+17TB LPDDR5X） |
| Vera Rubin NVL72 | 2026 H2 | 36 Vera + 72 Rubin | NVFP4 推理 3600 PF（稠密） | 20.7TB HBM4（+54TB LPDDR5X） |
| Vera Rubin with LPX | 2026 | VR NVL72 + Groq 3 LPU 机架 | —（面向延迟敏感推理） | GPU HBM + LPU SRAM 混合 |
| Rubin Ultra NVL576 | 2027 H2（路线图） | 576 GPU die | ❓ | ❓ |

---

## 三、消费级 GeForce 时间线（简表）

| 时间 | 系列 | 架构 | 关键点 |
| --- | --- | --- | --- |
| 1999 | GeForce 256 | — | 首个 "GPU" 概念，硬件 T&L |
| 2001 | GeForce 3 | — | 首个可编程着色器（同款芯片进 Xbox） |
| 2006 | GeForce 8（G80） | Tesla | 统一着色器；2007 CUDA 发布，游戏卡变通用计算卡 |
| 2010 | GTX 480 | Fermi | 40nm "电热炉"，但 GPU 计算软件栈成型 |
| 2012 | GTX 680 / Titan | Kepler | 28nm，Titan 把数据中心规格带入消费线 |
| 2014 | GTX 980 | Maxwell | 能效比标杆 |
| 2016 | GTX 1080 | Pascal | 16nm，与 P100 同代 |
| 2018 | RTX 2080 | Turing | RT Core + Tensor Core + **DLSS 1.0** |
| 2020 | RTX 3080 / 3090 | Ampere | 三星 8nm，GDDR6X；疫情 + 挖矿大缺货 |
| 2022 | RTX 4090 | Ada Lovelace | 台积电 4N，24GB，DLSS 3 帧生成，AV1 编码，450W |
| 2025-01 | **RTX 50 系列** | Blackwell | **GDDR7**、DLSS 4 多帧生成（单帧生成 3 帧）、PCIe 5；5090 笔记本版 24GB（2025 春） |

### RTX 50 系列明细（2025-01-06 CES 发布）

| 型号 | CUDA 核心 | 显存 | 带宽 | 功耗 | 首发价 | 上市 |
| --- | --- | --- | --- | --- | --- | --- |
| RTX 5090 | 21,760 | 32GB GDDR7 512-bit | 1.79TB/s | 575W | $1,999 | 2025-01-30 |
| RTX 5080 | 10,752 | 16GB GDDR7 | 0.96TB/s | 360W | $999 | 2025-01-30 |
| RTX 5070 Ti | 8,960 | 16GB GDDR7 | 0.67TB/s | 300W | $749 | 2025-02 |
| RTX 5070 | 6,144 | 12GB GDDR7 | 0.67TB/s | 250W | $549 | 2025-03 |
| RTX 5060 Ti | 4,608 | 16GB / 8GB | 0.45TB/s | 180W | $429 / $379 | 2025 Q2 |
| RTX 5060 | 3,840 | 8GB | 0.45TB/s | 145W | $299 | 2025 Q2 |

> 本地跑 LLM 的实用位：5090（32GB，唯一消费级 30GB+）；性价比位：5060 Ti 16GB / 5070 Ti 16GB。

---

## 四、工作站 / 边缘 / 开发者设备

| 产品 | 时间 | 关键规格 | 定位 |
| --- | --- | --- | --- |
| RTX PRO 6000 Blackwell | 2025-03 GTC | 96GB GDDR7，工作站 / Server 版 | 单卡最大显存的工作站卡，本地推理热门（Mac Studio 之外） |
| DGX Spark（GB10，CES 时名 Project DIGITS） | 2025-01 发布 / 2025-10 上市 ❓ | 128GB 统一 LPDDR5X @ 273GB/s，FP4 ~1 PF（稀疏），$3,999 | 桌面 AI 开发机，Grace+Blackwell superchip |
| DGX Station（GB300） | 2025-03 GTC | GB300 superchip，约 0.8TB 统一内存 ❓ | 桌面级 AI 工作站顶配 |
| Jetson Orin | 2022 | 275 TOPS（INT8 稀疏） | 机器人 / 自动驾驶边缘计算 |
| Jetson Thor | 2025 | 2070 TFLOPS FP4（稀疏），Blackwell，开发套件 $3,499 | 人形机器人本体计算机 |

---

## 五、中国市场特供版（出口管制线）

| 型号 | 时间 | 与原版差异 | 状态 |
| --- | --- | --- | --- |
| A800 | 2022-10 | A100 互联带宽降为 400GB/s | 2023-10 新规后被禁 |
| H800 | 2023-03 | 算力保留，互联大幅阉割；DeepSeek-V3 用 2048 张训练 ❓口径 | 2023-10 被禁 |
| L20 / L2 | 2023-12 | L40 衍生，算力削减 | 合规销售 |
| H20 | 2024 | 96GB HBM3 @ 4.0TB/s，FP16 Tensor 约 148 TF（H100 的 ~15%），NVLink 保留 | 2024-12 被要求许可证；2025-04 NVIDIA 计提 $5.5B；2025-07 获准恢复销售（附 15% 收入分成安排 ❓） |
| H20E ❓ | 2025-09 报道 | 显存升至 141GB HBM3e | 报道口径 |
| B30A ❓ | 2025-08 报道 | Blackwell 中国版：大显存（288GB HBM3e）、算力受限 | 报道口径 |

> 背景：2022-10-07 美国出口新规（A100/H100 对华禁售）催生特供线；此后管制与许可反复，是国产算力（昇腾等）崛起的直接背景。

---

## 六、趋势速览

1. **一年一代**：2023-10 起数据中心从两年一代改为年度节奏（Hopper → Blackwell → Blackwell Ultra → Rubin → Rubin Ultra，节奏未断）
2. **显存是主战场**：16GB（P100）→ 80GB（A100）→ 141GB（H200）→ 192GB（B200）→ 288GB（B300/Rubin）；带宽 0.72 → 22TB/s（30×），HBM4 首次带宽翻倍以上
3. **精度持续下探**：FP16（V100）→ TF32/稀疏（A100）→ FP8（H100 Transformer Engine）→ FP4/MXFP4（Blackwell）→ **NVFP4**（Rubin）——推理成本每代数量级下降
4. **计算单位从卡到机架**：superchip（Grace/Vera + C2C）→ NVL72（NVLink 全互联 130→260TB/s）→ NVL576；网络（ConnectX / BlueField / Spectrum-X / Quantum-X）与 GPU 同代齐更
5. **推理专用化分流**：GB300 主打 test-time scaling；Rubin CPX 用 GDDR7 降本；LPX 引入 SRAM 型 LPU 攻低延迟——"推理不再是训练卡的副业"
6. **公司层面**：FY2026 Q4 营收 $68.1B 创纪录；2025-12 收购 Groq 资产（$20B）补齐推理版图；Blackwell 掩膜事件（2024-10）证明供给端仍是最大变量

---

## 参考链接

- [NVIDIA GB300 NVL72 官网](https://www.nvidia.com/en-us/data-center/gb300-nvl72/)
- [NVIDIA Vera Rubin NVL72 官网](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)
- [NVIDIA LPX（Groq 3 LPU）官网](https://www.nvidia.com/en-us/data-center/lpx/)
- Wikipedia: [Blackwell (microarchitecture)](https://en.wikipedia.org/wiki/Blackwell_(microarchitecture))、[Nvidia](https://en.wikipedia.org/wiki/Nvidia)、[List of Nvidia graphics processing units](https://en.wikipedia.org/wiki/List_of_Nvidia_graphics_processing_units)
- 注：检索工具当月限额受限，部分 2025–2026 数字来自官网 2026-08 快照与 Wikipedia，标 ❓ 者待后续核实
