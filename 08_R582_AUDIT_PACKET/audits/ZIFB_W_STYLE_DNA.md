# `ZIFB_W` 组内语言与视觉范式 DNA

> 版本：R582，2026-07-20  
> Zotero collection：`ZIFB_W` (`QI8BAEXB`)  
> 用途：本项目的写作、术语和图形风格语料。**不得把本库论文当作本项目科学主张的证据来源，除非该论文另行进入 `ZIFB` 科学证据库并完成引用核验。**  
> 项目硬约束：ZIFB 正极是主角；NH4Br 只是代表性支持电解质；Br− 只作为支持配体/络合参与者；无新增物理实验；旧实验文件中的 `NH4Cl/NH4CL` 标签实际均为 NH4Br，按 `EXP-META-001` 解释，原始文件名和字节不改。

## 0. 一页结论

这 25 篇组内论文最值得移植的不是若干套话，而是一个稳定的论证机器：**先把失效现象做实，再用最少的模型变量解释它，最后把机制翻译成可操作的器件判断。** 对本项目，叙事主语必须始终是 ZIFB 正极及其随面容量演化的空间状态；NH4Br 只能在方法、配方和边界条件中出现，不能占据标题、摘要首句、图标题或机制图视觉中心。

语言应采用“观察—比较—解释”的短链，而不是把模型、证据、机制和意义压进一个长句。组内语料的粗略句长中位数为 20 个英文词，四分位区间为 11–32 个词；本稿应把主结果句控制在约 15–25 词，并让每句只承担一个主要命题。

视觉上，最强的可迁移母版是：**变量按行、面容量按列的二维小倍图，统一计算域、色标和阅读方向；上方或左侧用一条全局曲线标出被截取的面容量节点。** 该母版直接来自组内近期论文的“变量 × 工况”空间矩阵，而不是来自装饰性机制卡通。Figure 3 应优先按此重构。

组内近期原创研究的 18 张主图共 119 个面板，面板数中位数为 6；但可读性来自固定比较语法，而不是面板数量。本稿主图建议保持 5–8 个视觉单元，并只设置一个面积占比 40–55% 的主视觉区域。完整的六个面容量切片、网格独立性、辅助变量和敏感性分析下沉 SI。

机制图应改为**扁平、证据挂钩、可反驳的因果图**：传统/残缺描述与完整模型并列，箭头上写动作，节点旁标出对应模型变量或证据面板。禁止把 NH4Br、Br−、I−、I2、Zn、孔隙、电流、传质、吸附等全部堆进一张“化学元素全家福”。

## 1. 核查范围与方法

- 通过 Zotero Desktop local API 核验 `QI8BAEXB`：25 个顶层条目，25 个 PDF 附件。
- Zotero 的 `/fulltext` endpoint 对 25 个附件均未建立索引；随后按 `file-url` 解析到 `ZhaoWu_writing_corpus/PDFs/`，逐篇提取全文。
- 实际读取 25 个 PDF，共 445 页；另外渲染并视觉核查 21 个代表性图页。
- 全文粗略频率统计在移除参考文献尾部后进行，仅用于识别写作习惯，不作为语言质量评分。
- Zotero item key（例如 `BEUYP2UN`）与 BibTeX key（例如 `Xu2024HighRateLongLifeZBFB`）是两套标识。本文两者并列，以便回溯。
- 已交叉核对 `ZHAOWU_STYLE_GUIDE.md` 和 25 张 `READING_CARDS`；本文新增的重点是 Zotero key、逐图证据、配色/版式规则以及对当前 ZIFB 正极论文的可执行约束。

## 2. `ZIFB_W` 完整论文清单

| # | Zotero item / PDF attachment | BibTeX key | 年份 | 作者 | 题名与期刊 | 在本次风格核查中的角色 |
|---:|---|---|---:|---|---|---|
| 1 | `BEUYP2UN` / `8X7SXZOV` | `Xu2024HighRateLongLifeZBFB` | 2024 | Z. Xu; J. Li; M. Wu | *A high-rate and long-life zinc-bromine flow battery*, JPS | 近期吴组系统优化、超密图组、仿真场图与性能收官母版 |
| 2 | `FJ56R3AK` / `CKUNJK19` | `Li2025ReactionKineticsMassTransferZBFB` | 2025 | J. Li; Z. Xu; M. Wu | *Reaction Kinetics and Mass Transfer Synergistically Enhanced Electrodes for High-Performance Zinc-Bromine Flow Batteries*, ACS AMI | 近期旗舰写法；诊断先行、理论/仿真/实验同图、红灰主对照 |
| 3 | `HVPF4KTQ` / `AU6GIS4P` | `Li2023HalogenAqueousFlowCells` | 2023 | J. Li; Z. Xu; M. Wu | *Halogen enabled aqueous flow cells for large-scale energy storage: Current status and perspectives*, JPS | 卤素体系术语与综述结构；仅作措辞语料 |
| 4 | `4XYE9GL4` / `BYZQCPWU` | `Li2026TemperatureDynamicsZBFB` | 2026 | J. Li; W. Liu; Y. Chen; M. Wu | *Temperature-dependent electrochemical dynamics in zinc-bromine flow batteries*, JES | 最新吴组机制叙事；温度×时间矩阵、三条机制腿与自限结论 |
| 5 | `SZRY2NZT` / `HWPWHP3O` | `Li2023ElectrolyteEngineeringZnAnodes` | 2023 | A. Li; J. Li; Y. He; M. Wu | *Toward stable and highly reversible zinc anodes for aqueous batteries via electrolyte engineering*, J. Energy Chem. | 锌负极机制与电解液工程术语；综述式分类框架 |
| 6 | `L9L9WMSH` / `4VS3DD30` | `Lin2021HighCapacityAllSolidStateLithium` | 2021 | Y. Lin et al. | *A High-Capacity, Long-Cycling All-Solid-State Lithium Battery Enabled by Integrated Cathode/Ultrathin Solid Electrolyte*, AEM | 旗舰摘要对偶、机制先于数字、性能对比插旗图 |
| 7 | `U2PZYYTG` / `P6YXNFZ2` | `Jian2021ReversibleZincAnode` | 2021 | Q. Jian et al. | *A Highly Reversible Zinc Anode for Rechargeable Aqueous Batteries*, ACS AMI | 原位/事后证据闭环与锌沉积措辞 |
| 8 | `UGPNEZKR` / `RPR7LQ50` | `Jian2020DendriteFreeZincAnode` | 2020 | Q. Jian et al. | *A dendrite-free zinc anode for rechargeable aqueous batteries*, JMCA | 极简引言、平行 counterfactual 机制图 |
| 9 | `HVRAQWCN` / `52D27NVG` | `Jian2020TrifunctionalElectrolyteZIFB` | 2021（online 2020） | Q. Jian; M. Wu; H. Jiang; Y. Lin; T. Zhao | *A trifunctional electrolyte for high-performance zinc-iodine flow batteries*, JPS | 唯一直接 ZIFB 机制/语言锚；双机制卡通结构。注意：只学写法，不继承“NH4Br 为主角”的选题框架 |
| 10 | `PX6HW3XG` / `CMNA4RS8` | `Wu2017HighPerformanceZBFB` | 2017 | M. Wu et al. | *High-performance zinc bromine flow battery via improved design of electrolyte and electrode*, JPS | 早期“部件优化→整机性能”工作马写法 |
| 11 | `P4V9AQ3S` / `O4L76LDO` | `Wu2018ImprovedElectrolyteZBFB` | 2018 | M. Wu et al. | *Improved electrolyte for zinc-bromine flow batteries*, JPS | 极简标题、配方对照、倍率/循环图 |
| 12 | `927FJYTB` / `K7ES2MMG` | `Wu2018CarbonizedTubularPolypyrrole` | 2018 | M. Wu et al. | *Carbonized tubular polypyrrole with a high activity for the Br2/Br− redox reaction in zinc-bromine flow batteries*, Electrochim. Acta | 材料→半电池→全电池标准链 |
| 13 | `QEVBUQNQ` / `GBV2QNRS` | `Wu2019MesoporousPomeloCarbon` | 2019 | M. Wu et al. | *Mesoporous carbon derived from pomelo peel as a high-performance electrode material for zinc-bromine flow batteries*, JPS | 四图式紧凑材料论文、固定颜色序列 |
| 14 | `X6W32SD8` / `KG1AHNTG` | `Xu2015FundamentalModelsFlowBatteries` | 2015 | Q. Xu; T. Zhao | *Fundamental models for flow batteries*, PECS | 建模合法性、假设披露、模型边界措辞 |
| 15 | `NBE6688T` / `DHZYXYXD` | `Esan2020ModelingSimulationFlowBatteries` | 2020 | O. Esan et al. | *Modeling and Simulation of Flow Batteries*, AEM | 现代模型分类与“假设缺陷→修正→验证”叙事 |
| 16 | `FPYNHZ2Q` / `EPSDHGSV` | `Xu2013FlowFieldDesignsVRFB` | 2013 | Q. Xu; T. Zhao; P. Leung | *Numerical investigations of flow field designs for vanadium redox flow batteries*, Applied Energy | 纯仿真验证先行、非单调最优、三构型公平比较 |
| 17 | `9YLYG999` / `9U97W3IF` | `Xu2014VRFBWithWithoutFlowFields` | 2014 | Q. Xu; T. Zhao; C. Zhang | *Performance of a vanadium redox flow battery with and without flow fields*, Electrochim. Acta | 二元可判定问题与模型/实验对照 |
| 18 | `QESIC6JA` / `99LJ7DMK` | `Zhou2015VRFBIonMobilityModel` | 2015 | X. Zhou et al. | *A vanadium redox flow battery model incorporating the effect of ion concentrations on ion mobility*, Applied Energy | 本项目最重要的纯仿真语言母版；输入性质→系统输出两层验证 |
| 19 | `YGPRYLP2` / `82L06PQR` | `Zhou2016CriticalTransportIssuesRFB` | 2017（online 2016） | X. Zhou et al. | *Critical transport issues for improving the performance of aqueous redox flow batteries*, JPS | 传质/离子输运词汇与综述判词 |
| 20 | `IFWYZSPU` / `XTQD1P6O` | `Xu2017LBMTransportFuelCellsFlowBatteries` | 2017 | A. Xu; W. Shyy; T. Zhao | *Lattice Boltzmann modeling of transport phenomena in fuel cells and flow batteries*, Acta Mech. Sin. | 多尺度输运建模表述与证据等级 |
| 21 | `IQQQ8M3G` / `DKQ3U8ZK` | `Wei2021ConvectionEnhancedFlowField` | 2021 | L. Wei et al. | *A convection-enhanced flow field for aqueous redox flow batteries*, IJHMT | 空间场小倍图、临界区/非敏感区 regime 图 |
| 22 | `P8FW5SEK` / `2Z1A11EE` | `Jiang2019HighPowerDensityLongCycleVRFB` | 2020（online 2019） | H. Jiang et al. | *A high power density and long cycle life vanadium redox flow battery*, Energy Storage Materials | 仿真场→实验兑现对偶图、长循环英雄面板、文献坐标 |
| 23 | `MYF7J4N9` / `MSWYMHQ9` | `Zeng2015ComparativeVanadiumIronChromiumRFB` | 2015 | Y. Zeng et al. | *A comparative study of all-vanadium and iron-chromium redox flow batteries for large-scale energy storage*, JPS | 对称比较、数字定罪与系统账本 |
| 24 | `4G3TB5J8` / `Z6F9DYMS` | `Zeng2016FlowFieldStructuredIronChromiumRFB` | 2016 | Y. Zeng et al. | *A high-performance flow-field structured iron-chromium redox flow battery*, JPS | 流场设计与性能翻译 |
| 25 | `LJJKI5X2` / `R5DW933W` | `Tan2016RuO2NiOLithiumAir` | 2016 | P. Tan et al. | *A nano-structured RuO2/NiO cathode enables the operation of non-aqueous lithium-air batteries in ambient air*, EES | 旗舰“一个能力跨越”叙事、观察×机制覆盖表 |

## 3. 代表性样本与选择依据

### 3.1 一级样本：直接决定本稿语言和图形

| Zotero key | 采用原因 | 最可迁移证据 |
|---|---|---|
| `HVRAQWCN` | 唯一直接 ZIFB 原创论文；提供 ZIFB、正/负极、支持电解质和面容量的组内叫法 | PDF p.2 Fig.1、p.5 Fig.5、p.7 Fig.7 |
| `BEUYP2UN` | 近期吴组工作马论文；图序与变量优化逻辑最成熟 | PDF p.2 Fig.1、p.5 Fig.3、p.6 Fig.4、p.8 Fig.6 |
| `FJ56R3AK` | 近期旗舰；诊断先行并将 DFT、相场、显微和整机结果组合成同一证据链 | PDF p.2 Fig.1、p.3 Fig.2、p.5 Figs.4–5、p.6 Fig.6 |
| `4XYE9GL4` | 最新吴组机制论文；把复杂机理拆成正极、负极和跨膜三条腿 | PDF p.3 Fig.1、p.4 Fig.2、p.6 Fig.3、p.7 Fig.4、p.8 Fig.5 |
| `QESIC6JA` | 纯仿真论文最接近本稿的信任结构 | printed p.162 Fig.2；p.163 Fig.3 |
| `IQQQ8M3G` | “物理量×构型”空间小倍图与 regime 概念图母版 | PDF p.8 Figs.6–7 |
| `P8FW5SEK` | 仿真场与实验性能按同一图组兑现；英雄长循环面板 | PDF pp.8–9 Figs.7–9、p.10 Fig.11、p.11 Fig.12 |

### 3.2 二级样本：补充词汇和结构

- `PX6HW3XG`, `P4V9AQ3S`, `927FJYTB`, `QEVBUQNQ`：ZBFB 传统“材料/电解液→动力学→整机”用词体系。
- `FPYNHZ2Q`, `9YLYG999`, `X6W32SD8`, `NBE6688T`, `IFWYZSPU`：模型验证、假设、输运和设计外推的证据等级。
- `L9L9WMSH`, `U2PZYYTG`, `UGPNEZKR`, `LJJKI5X2`：高影响力论文的摘要对偶、机制闭环和图组留白。
- 三篇综述只用于术语覆盖和段落组织，不用于模仿其长句密度。

## 4. 语言 DNA

### 4.1 文章级叙事骨架

组内原创论文反复采用以下五步：

1. 用一个可判定的器件失效现象开题，而不是先讲模型有多复杂。
2. 把失效拆成 2–3 个具名病因，并令后文图序与病因顺序同构。
3. 在 Results 的第一阶段取得“信任许可证”：实验基线、外部物性或系统输出验证。
4. 用 counterfactual 或控制变量对照定位责任变量。
5. 把机制压缩成一个工程判词或 regime 图，而不是列一串 future work。

对本稿的翻译应是：**正极可及性损失现象 → 溶解受限自由碘过饱和假设 → 输入/系统两层验证 → 完整模型与残缺模型对照 → 面容量—局部状态—可及性因果图 → 可操作的容量/运行窗口判断。**

### 4.2 标题

25 个标题中，绝大多数是零谓语的名词短语。纯仿真论文最稳妥的组内结构是：

- `A [battery] model incorporating [previously omitted physics]`
- `[Variable]-dependent [system-level behavior] in [battery]`
- `Numerical investigation of [one bounded design question]`

本稿标题不应出现 NH4Br；也不应堆叠“multiscale / multiphysics / unified / comprehensive / synergistic”等多重形容词。标题只承诺一个贡献类型：模型修正、机制识别或正极失效诊断。

### 4.3 摘要

推荐 7–8 句，固定槽位如下：

1. 一句给出 ZIFB 正极失效及其工程后果。
2. 一句指出现有解释无法同时解释哪些观测。
3. 一句说明本文建立何种模型；不得把软件名或求解细节塞入摘要。
4. 一句说明模型中的核心物理链，但只写 2–3 个动作。
5. 一句给输入物性或系统级验证结果。
6. 一句给完整模型与 counterfactual 的关键差值。
7. 一句给最重要的容量节点/端点结果及工况。
8. 一句给条件式设计含义。

组内摘要的数字从不裸报：数字必须同时带工况、比较基线和方向。对本稿，主数字应优先服务正极机制；NH4Br 浓度只在确有必要的工况括号中出现。

### 4.4 引言

建议 4 段：

- P1：从 ZIFB 的器件价值迅速落到正极容量/可及性问题。宏观能源背景不超过 2–3 句。
- P2：列出现有解释及各自能解释/不能解释的现象；用数字或互相冲突的观测定罪，不用形容词定罪。
- P3：说明为什么运行电极内的耦合变量不能仅凭现有实验逐一解耦，从问题性质推出建模必要性。不得写成“因为无法做实验”。
- P4：`Here, we develop...`；方案、机制、验证锚和最强数字依次出现。贡献用连续叙事，不用 `(1)–(4)` 列表。

### 4.5 Results and Discussion

每个结果段采用四拍，且按此顺序：

1. **问题/目的**：这一段要回答什么。
2. **观察**：直接报图中可见趋势或数字。
3. **比较**：与基线、counterfactual 或另一工况同句比较。
4. **解释**：用与证据等级匹配的动词给出归因，并用一句前挂后钩引向下一图。

推荐句法：

- 直接观察：`The accessible area decreased from ... to ... as the areal capacity increased.`
- 对照：`By contrast, the model without dissolution limitation did not reproduce ...`
- 模型能力：`The model reproduces / captures / resolves ...`
- 一步推断：`This trend indicates ...`
- 跨越模型边界：`The result suggests / may reflect / is consistent with ...`
- 控制变量归因：`Because all other inputs were held fixed, the difference is attributed to ...`

不要把“观察”和“机制解释”写在同一个带三层从句的句子中。若存在不利结果，应在相应段落立即处理，不应把所有 caveat 集中到结论或独立 limitations 段。

### 4.6 Discussion 的边界

组内多数原创论文将 Discussion 嵌入 Results。对本稿应保持：

- 模型内部的数学事实可以说满。
- 模型对独立观测的复现可用 `reproduces`, `captures`, `agrees with`。
- 从模型输出推断真实微观机制用 `indicates`, `suggests`, `is consistent with`。
- 未显式建模的吸附、晶体形貌、孔口排斥或相变路径只能写 `may`, `could`, `a possible explanation is`，且必须另挂文献。
- 不使用 `prove`；`confirm` 仅保留给多条独立证据同时命中的少数位置。

### 4.7 结论

结论建议一个段落、5–7 句：问题与方法各 1 句，验证 1 句，核心机制 1–2 句，关键数字 1–2 句，工程含义 1 句。不要重新讲背景，不要出现新机制，不要用展望清单收尾。

### 4.8 句法与节奏的定量指纹

全文粗略计数显示：

| 表达 | 总次数 | 覆盖论文数 | 使用建议 |
|---|---:|---:|---|
| `as shown in` | 153 | 25/25 | 可保留，但每段最多一次；优先让科学对象作主语 |
| `due to` | 268 | 25/25 | 只用于证据充分的直接归因，避免一段多次 |
| `as a result` | 73 | 22/25 | 用于跨句结果，不要当装饰性连接词 |
| `moreover` | 112 | 22/25 | 全文限量；能用逻辑关系替代时不用 |
| `in this work` | 43 | 15/25 | 引言末段和结论首句各一次足够 |
| `it is found that` | 38 | 18/25 | 属于组内旧式模板，本稿应大幅减少 |
| `is attributed to / is ascribed to` | 26 | 20/25（合计） | 只在对照或多证据支持下使用 |
| `indicating that / suggesting that` | 32 | 19/25（合计） | 与证据等级匹配，不要链式连用 |

应继承的是“比较—归因”的节奏，不是模板的重复。优先写 `The solid fraction increased...`，少写 `It can be clearly seen that...`。

### 4.9 常用词族

可保留的组内词族：

- 现象：`performance`, `rate capability`, `cycling stability`, `polarization`, `capacity loss`, `voltage gap`。
- 输运：`mass transport`, `ion transport`, `local concentration`, `current-density distribution`, `transport pathway`。
- 电极：`positive electrode`, `negative electrode`, `electrode/electrolyte interface`, `reactive surface area`, `electrochemically accessible area`。
- 比较：`by contrast`, `under otherwise identical conditions`, `in the same range`, `compared with`。
- 机制校准：`indicates`, `suggests`, `is consistent with`, `can be attributed to`, `a likely explanation is`。
- 结果：`achieves`, `delivers`, `maintains`, `reproduces`, `captures`；仿真结果不使用 `delivers` 描述自然系统。

### 4.10 不应照抄的语言表面

- `It is obvious/clearly seen/evident that`：删去，让数字和比较关系承担清晰度。
- `Remarkably / impressively / encouragingly`：每篇最多保留一个，且只用于真正的头条结果。
- `unlock`, `shed light on`, `pave the way`, `promising`：组内常见但已高度模板化；末句只择一，或完全不用。
- `complex interplay`, `holistic`, `multifaceted`, `comprehensive framework`, `orthogonal evidence`, `evidence legs`, `mechanistic landscape`：不对应具体变量时全部删除。
- `synergistic`：只有严格的非加和对照才可用。
- `prove / definitively establish`：不用于纯仿真机制结论。
- 连续三个以上名词作前置定语：拆成介词短语或两句。
- 连续 em dash、括号套括号和一口气列 4 个因果动作：拆句。

## 5. 本项目术语账本

| 概念 | 首选写法 | 可接受变体 | 禁用或慎用 | 执行理由 |
|---|---|---|---|---|
| 体系 | `zinc–iodine flow battery (ZIFB)` | 复数 `ZIFBs` | `zinc iodine battery`, `Zn–I system` | 与 `HVRAQWCN` 的组内命名一致 |
| 论文主角 | `ZIFB positive electrode` / `positive electrode of the ZIFB` | 后文可简化为 `positive electrode` | `NH4Br system`, `NH4Br mechanism` | 用户硬约束：正极是主角 |
| 支持盐 | `NH4Br as a representative supporting electrolyte` | `NH4Br-containing supporting electrolyte` | `active electrolyte`, `key active material`, `protagonist electrolyte` | NH4Br 只代表一类支持电解质 |
| Br− 角色 | `supporting ligand`, `complexing species`, `bromide-assisted complexation`（仅在有证据处） | `bromide ion` | `active positive species`, `catalyst` | 防止 Br− 抢走正极碘化学主线 |
| 历史标签 | `NH4Br`，并在方法/数据声明一次 `legacy files were mislabeled as NH4Cl (EXP-META-001)` | 表格脚注可写 `legacy label: NH4Cl; actual salt: NH4Br` | 把 NH4Cl 与 NH4Br 当两种实验配方比较 | 用户确认的元数据纠错，原始文件不改 |
| 电极命名 | `positive electrode`, `negative electrode` | 电化学上下文明确时可用 `iodine electrode`, `zinc electrode` | 同段混用 `cathode/anode` 与 `positive/negative` | 充放电方向下避免歧义；组内流电池论文惯例 |
| 核心物理 | `dissolution-limited iodine supersaturation` | 首次定义后 `dissolution-limited regime` | `iodine blocking mechanism`（过宽）, `precipitation catastrophe` | 给机制一个可引用、可检验的名字 |
| 碘相态 | 按模型实际变量写 `oxidized iodine state`, `free iodine`, `solid iodine fraction` | `iodine-rich solid phase`（若定义清楚） | `crystal morphology`, `film morphology`, `dendritic iodine` | 当前模型不支持形貌推断 |
| 失效量 | `loss of electrochemically accessible area` | `positive-electrode accessibility loss` | `electrode death`, `complete passivation` | 与 EIS/模型可观测量直接对应 |
| 面容量 | `areal capacity (mAh cm−2)` | `capacity per geometric area`（仅定义处） | `surface capacity`, `areal loading` | 与组内 ZIFB/ZBFB 文献一致 |
| 空间量 | `local concentration`, `local current density`, `solid volume fraction`, `accessible-area fraction` | 明确符号后可用 `c`, `j`, `εs`, `θ` | `distribution field` 不说明变量 | 图标题和正文必须能脱离符号阅读 |
| 模型 | `continuum model`, `coupled transport–reaction model` | `positive-electrode model` | `digital twin`, `AI model`, `holistic multiphysics platform` | 准确限定能力边界 |
| 验证 | `agreement with`, `reproduces`, `captures`, `is consistent with` | `validation against` 仅用于独立数据 | `verified by the same fitted data`, `proves` | 避免循环验证与过度声称 |
| 充放电图 | `charge–discharge voltage profiles` | `voltage–time profiles` | 同一图组交替用 `curves/profiles/traces` | 固定词汇，减少同义词噪声 |
| 效率 | 首次定义 `coulombic efficiency (CE)`, `voltage efficiency (VE)`, `energy efficiency (EE)` | 后文只用缩写 | `Coulomb efficiency` | 组内一致写法 |
| 工况 | `current density`, `flow rate`, `state of charge`, `areal capacity`, `temperature` | — | `operating parameter` 不具体化 | 每个数字必须带可复现实验/模拟条件 |

## 6. 视觉 DNA

### 6.1 应继承的结构，不应照抄的表面

应继承：

- 一个主图只回答一个问题。
- 同一比较对象在全文保持固定颜色、线型和命名。
- 图序等于论证序；只看图和 caption 即可复述文章主链。
- 空间图采用固定行列规则；时间序列采用固定帧位和方向。
- 机制图位于诊断之后或与关键证据呼应，不作为无证据的封面装饰。
- 长循环或最强性能用一个明显更宽的英雄面板，视觉上体现“久”或“强”。

不应照抄：

- 早期论文的 rainbow/jet 热图。
- 11–12 个同等大小、同等权重的小面板。
- 3D 电池块、光泽球、阴影、渐变和装饰性分子。
- 把解释句写进图内；图内只保留变量、动作、工况和极短判词。
- 每个空间切片重复一条色标和一套坐标标题。

### 6.2 面板密度与版式

近期三篇原创研究的面板数：

- `BEUYP2UN`：7 张主图，面板数 `11, 12, 11, 6, 8, 5, 8`。
- `FJ56R3AK`：6 张主图，面板数 `7, 1, 6, 5, 5, 5`。
- `4XYE9GL4`：5 张主图，面板数 `6, 7, 4, 9, 3`。

合计 18 张图，中位数 6。对本稿的执行规则：

- 普通主图 5–8 个视觉单元；超过 8 个必须证明存在统一的行列语法。
- 仅一个英雄面板，面积占整图约 40–55%；其余面板围绕它提供验证、对照或定量摘要。
- 图宽优先采用单栏或通栏的明确尺寸，不使用介于两者之间的任意宽度。
- 面板标签统一置于左上角外侧，黑色粗体；禁止漂移到图内数据区域。
- 行列间距固定；标题、轴标签和 colorbar 不得侵入相邻面板。

### 6.3 颜色体系

组内近期论文的可用语义是“灰色基线 + 彩色设计/工况 + 红色最佳结果”。本稿建议现代化为以下固定角色，而非逐图重新配色：

| 角色 | 建议颜色 | 用途 |
|---|---|---|
| 基线/残缺模型 | graphite `#4D4D4D` | control、旧模型、无溶解限制 |
| 完整模型/主结论 | vermilion `#D65345` | 主曲线、关键面容量、本文方案 |
| 次级工况 1 | blue `#3B6FB6` | 早期容量或低工况 |
| 次级工况 2 | teal `#2A9D8F` | 中间容量/中间工况 |
| 次级工况 3 | violet `#7A68A6` | 后期但非端点 |
| 碘正极语义色 | amber `#D8912B` | I2/iodine-rich state、正极边界 |
| 支持电解质/Br− | muted cyan `#67A9B7` | 仅作辅助图例或小图标，不作主强调 |

空间标量：

- 浓度或体积分数使用感知均匀的 sequential colormap，例如 `viridis`, `cividis`, `magma`。
- 正负偏差使用以 0 为中心的 diverging colormap。
- 同一变量跨所有面容量必须使用相同 `vmin/vmax`；若动态范围过大，主图用物理归一化量，原始范围放 SI。
- 不使用 jet/rainbow，不用红绿作为唯一差异通道。

### 6.4 线图、柱图和散点图

- 白色背景，无主网格；必要时只保留极浅灰水平辅助线。
- 轴线约 0.8–1.0 pt，数据线约 1.2–1.6 pt；主要曲线略粗于对照。
- 标记点用于实测/离散工况，实线用于模型/连续趋势；不要让每条曲线同时拥有复杂颜色、线型和 marker。
- 基线优先用灰/黑，完整模型用主红；中间容量采用蓝—青—紫的固定顺序。
- 可直接标注的曲线不再放大图例；图例不得遮挡数据。
- 关键差值直接标在图旁，但每个面板最多 1–2 个数字 callout。
- 双 y 轴只在 CE/EE 这类组内成熟惯例中使用；其他情况拆图。
- 误差条、样本量和统计定义只在确有重复数据时出现；模拟确定性曲线不得伪造误差条。

### 6.5 Figure 3：面容量 × 空间变量二维小倍图规范

这是本次核查对当前稿件最明确的图形处方。

**建议骨架**：

1. 顶部窄面板：全局电压、容量或可及性随面容量的曲线，用四条竖线标出所选快照。
2. 主体矩阵：列为面容量阶段，行为不同物理量。
3. 每一行仅一个共享 colorbar；每一列只在顶部写一次 `Q = ... mAh cm−2`，必要时同时给 `Q/Qf`。
4. 所有面板共享同一正极计算域、坐标方向、inlet/outlet 或 membrane/current-collector 标识。
5. 每个变量的色标在各面容量之间固定，读者才能直接看到空间演化。

**推荐列**：早期、膝前、膝点、终点四个物理节点；节点必须由全局曲线定义，而不是等间距随意抽样。若现有数据有六个容量切片，主图保留四个，六个全量矩阵放 SI。

**推荐行**：

- Row 1：oxidized/free-iodine state 或 saturation ratio。
- Row 2：solid iodine fraction / iodine-rich solid fraction。
- Row 3：accessible-area fraction 或 local current density；两者谁更接近主张就留主图，另一变量放 SI。

**禁止**：

- 把四个变量叠在同一彩色地图上。
- 每个切片使用独立自动色标。
- 只给“漂亮的终点场”而没有早期—膝点—终点演化。
- 用箭头/气泡在空间图上讲完整机制；机制解释应由相邻定量面板和正文完成。
- 把 NH4Br 浓度作为 Figure 3 的行或列主维度；本图必须服务正极空间演化。

**组内直接母版**：`BEUYP2UN`, PDF p.6 Fig.4（两个空间变量 × 三个流速）；`IQQQ8M3G`, PDF p.8 Fig.6（三个物理量 × 两种构型）；`4XYE9GL4`, PDF p.6 Fig.3（温度 × 时间图像矩阵）。

### 6.6 机制图语言

组内最有效的机制图有两类：

1. counterfactual 平行图：上/左为基线失效，下/右为完整机制；构图、尺度和视角完全一致，只改变责任变量。
2. 时间/状态序列：3–5 个阶段，显示同一对象从初始到失效的变化。

本稿机制图建议采用扁平 counterfactual：

- 左侧：无溶解限制或传统欧姆膜图景。
- 右侧：溶解受限过饱和 → 固相积累 → 可及性下降 → 电流重分布。
- 每条箭头只写一个动词：`accumulates`, `precipitates`, `occludes`, `redistributes`。
- 每个节点标出能被图或模型追踪的量；无法对应变量或证据的图标删除。
- 正极和碘用主色；NH4Br/Br− 用小尺寸、低饱和度辅助色，且不位于视觉中心。
- 不画未经模型支持的晶体形貌、微孔堵塞细节或排斥轨迹。
- 不使用 3D 透视、光泽球、拟物阴影和发光箭头。

证据依据：`HVRAQWCN`, PDF p.2 Fig.1 与 p.5 Fig.5 展示“开头承诺—中场兑现”的双卡通；`FJ56R3AK`, PDF p.3 Fig.2 展示两条完全平行的 PGF/CZGF 因果通道。应继承平行语法，舍弃旧式拟物外观。

### 6.7 Caption 规则

- Caption 只说明“图中是什么”，不写结果解释。
- 多面板按 `(a) ...; (b) ...; and (c) ...` 顺序逐项对应。
- 电流密度、面容量、温度、SOC、时间点、坐标切面和单位写全。
- 空间图必须说明时间/面容量节点、截面位置和归一化方式。
- 缩写只有在正文已定义后才直接使用。
- 图中省略的范围、截断、插值或归一化应在 caption 当场说明。
- Caption 与图例、轴标题、正文逐项巡检；组内旧文曾出现 caption 漏列实际曲线，本稿不得复制这种缺陷。

### 6.8 主文与 SI 的分工

主文只保留：

- 直接支撑中心主张的验证图。
- 一个空间演化英雄图。
- 一个 counterfactual 归因图。
- 一个设计/性能收官图。

SI 承担：

- 全部六个容量切片。
- 额外变量、不同截面、网格/容差/参数敏感性。
- 低价值重复曲线、完整拟合表和导出字段说明。
- 文献对比表、参数来源表、模型假设回收表。

## 7. 对当前稿件的可执行图组建议

| 图 | 单一职责 | 推荐结构 | ZIFB_W 母版 |
|---|---|---|---|
| Fig.1 | 让读者 10 秒内明白“正极何处、何时、为何失去可及性” | 极简正极剖面 + 一条容量演化主链；NH4Br 只在小型工况框中 | `HVRAQWCN` Fig.1 的定位功能；外观按现代扁平风格重画 |
| Fig.2 | 建立现象学和模型可信度 | 关键实验锚/历史数据 + 模型复现 + 明确残差 | `QESIC6JA` Figs.2–3；`FPYNHZ2Q` 验证先行 |
| Fig.3 | 展示正极空间状态随面容量演化 | 全局曲线 + 变量×容量二维矩阵 | `BEUYP2UN` Fig.4；`IQQQ8M3G` Fig.6；`4XYE9GL4` Fig.3 |
| Fig.4 | 证明溶解限制是必要条件 | 完整模型/无溶解限制/无固相项的固定颜色 counterfactual | `QESIC6JA` 双模型；`FJ56R3AK` Fig.1 诊断先行 |
| Fig.5 | 将机制压缩成设计判词 | 参数扫描 + regime map + 条件式工程结论 | `IQQQ8M3G` Fig.7 |
| 最终性能图 | 把容量、电压、效率或稳定性放回器件尺度 | 一个宽英雄面板 + 1–2 个摘要指标 | `FJ56R3AK` Fig.6；`P8FW5SEK` Figs.9–12 |

## 8. 逐项证据索引

| 结论 | Zotero item / 题名 | 页/图证据 |
|---|---|---|
| 机制图可采用“开头承诺、数据后兑现”的双图结构 | `HVRAQWCN`, *A trifunctional electrolyte for high-performance zinc-iodine flow batteries* | PDF p.2 Fig.1；p.5 Fig.5 |
| Caption 应包含完整电流密度、配方、面容量 | `HVRAQWCN` | PDF p.2 Fig.2；p.4 Fig.4；p.7 Fig.7 |
| 系统优化图序可按“一变量一图、扫描后循环盖章”推进 | `BEUYP2UN`, *A high-rate and long-life zinc-bromine flow battery* | PDF pp.2–9 Figs.1–7 |
| 空间场应采用变量×工况的固定矩阵 | `BEUYP2UN` | PDF p.6 Fig.4 |
| 最终性能应用宽长循环面板和明确关键数字 | `BEUYP2UN` | PDF p.8 Fig.6 |
| Results 可以从基线失效诊断开始，而非先介绍新材料/模型 | `FJ56R3AK`, *Reaction Kinetics and Mass Transfer Synergistically Enhanced Electrodes...* | PDF p.2 Fig.1 |
| 正/负功能线可采用镜像图组，保持相同视觉语法 | `FJ56R3AK` | PDF p.5 Figs.4–5 |
| 红色本文方案、灰色基线、宽长循环英雄面板 | `FJ56R3AK` | PDF p.6 Fig.6 |
| 图片小倍图最适合用“工况为行、时间为列” | `4XYE9GL4`, *Temperature-dependent electrochemical dynamics in ZBFBs* | PDF p.6 Fig.3 |
| 多条机制腿应拆到独立图中，最终用膜/自放电闭环 | `4XYE9GL4` | PDF p.7 Fig.4；p.8 Fig.5 |
| 模型验证应先验证被修正的输入物性，再验证系统输出 | `QESIC6JA`, *A VRFB model incorporating... ion mobility* | printed p.162 Fig.2；p.163 Fig.3 |
| 旧模型可放 inset 或固定灰色，不让其破坏主坐标 | `QESIC6JA` | printed p.162 Fig.2 |
| 纯仿真设计问题应在 Results 先给验证再外推 | `FPYNHZ2Q`, *Numerical investigations of flow field designs...* | Fig.3 后再进入 Figs.4–8 |
| 三个物理量共用行列结构，可形成“速度→浓度→电流”因果阅读 | `IQQQ8M3G`, *A convection-enhanced flow field...* | PDF p.8 Fig.6 |
| 数据扫描最终应蒸馏为临界/非敏感区 regime 图 | `IQQQ8M3G` | PDF p.8 Fig.7 |
| 仿真场和器件性能可在同一图中按上/下两层兑现 | `P8FW5SEK`, *A high power density and long cycle life VRFB* | PDF pp.8–9 Figs.7–8 |
| 标题中的“long cycle life”应由横向英雄面板直接兑现 | `P8FW5SEK` | PDF p.10 Fig.11 |
| 最高级主张需要文献坐标或表格作许可证 | `P8FW5SEK` | PDF p.11 Fig.12 |

## 9. 交付前验收清单

### 语言

- [ ] 标题没有 NH4Br，没有并列承诺两件以上贡献。
- [ ] 摘要 7–8 句；每个关键数字带工况和基线。
- [ ] 正极在摘要、引言末段、每个主图 caption 和结论中都是语法主语。
- [ ] `NH4Br` 只被称为代表性支持电解质；`Br−` 不被写成活性主角。
- [ ] `NH4Cl` 只在元数据纠错声明或 legacy label 中出现。
- [ ] 观察、比较、解释分句；没有超过 35 词的核心结果句。
- [ ] `It is found/seen that`、`remarkably`、`promising` 等模板词已做限量检查。
- [ ] 仿真没有使用 `prove`；自然机制的动词等级不高于证据等级。
- [ ] 同一对象全文使用同一术语，不靠同义词轮换制造“文采”。

### 图形

- [ ] 每张主图能用一句话说出唯一职责。
- [ ] Figure 3 采用面容量×空间变量矩阵，色标跨容量固定。
- [ ] 同一模型/工况在全文颜色、线型和名称一致。
- [ ] 主图存在一个明确英雄面板，其他面板从属于它。
- [ ] 没有 jet/rainbow、3D 拟物、光泽球、阴影或装饰性渐变。
- [ ] 机制图中每个节点都能回指模型变量或证据面板。
- [ ] NH4Br/Br− 在机制图中为次级低饱和度元素，不在视觉中心。
- [ ] 面板标签、坐标、单位、色标、膜侧/集流体侧方向可在缩至投稿尺寸后读清。
- [ ] Caption 写全工况，但不替正文解释结果。
- [ ] 六容量全量、辅助变量和敏感性图已移入 SI。

### 十秒测试

把正文遮住，仅展示每张图 10 秒，读者应能回答：

1. 这一图比较的对象是什么？
2. 横向/纵向/颜色分别编码什么？
3. 哪一个是基线，哪一个是完整模型？
4. 这一图只想让我相信哪一件事？

任一问题答不出，即判定该图仍需重构。

## 10. 使用边界

- `ZIFB_W` 是风格语料，不自动拥有科学证据权威。
- 组内早期论文存在语法错误、过密面板和旧式彩虹场图；应继承论证结构，不照抄语言瑕疵和视觉表面。
- 本文只提供风格和设计合同，不代表已核验当前稿件的每一条科学主张。
- 任何从组内句子借鉴的内容都应重写为本项目自己的表达；不得逐句拼贴。

