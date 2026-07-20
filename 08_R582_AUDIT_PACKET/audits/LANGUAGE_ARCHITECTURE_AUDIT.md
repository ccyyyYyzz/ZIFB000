# R582 全文语言与论证架构狠批

## 审计范围与判定轴

- 文件：E:\zifb_final_9129_luck\manuscript\main.tex（1393 行）与 E:\zifb_final_9129_luck\manuscript\SI.tex（1160 行）
- 模式：只读审计；未修改 main.tex 或 SI.tex
- 论文类型：研究论文
- 章节范围：标题、摘要、引言、理论/模型、结果、讨论、结论、方法、SI
- 语言：英文
- 期刊轴：期刊中性；最终词汇、句法、标题习惯和图注风格必须再由 Zotero 的 ZIFB_W 组内论文校准
- 科学边界：ZIFB 正极是主角；NH4Br 只是一种代表性支持电解质；所有旧 NH4Cl/NH4CL 实验标签均按 EXP-META-001 解释为 NH4Br；不新增实际实验

## 一句话总评

这不是一篇“缺少信息”的稿子，而是一份把模型审计底稿、证据免责书、复现清单和科学论文挤在同一条叙事线上形成的稿子。科学内核可以成立，但当前版本要求读者先学会作者自造的整套审计语言，才能找到真正的结果。技术熟练的审稿人能够重建逻辑，但必须像核查员一样工作；这在投稿层面等同于不可读。

当前最大问题不是语法，而是贡献类型写错了。本文真正贡献不是“发现了真实沉积形貌”或“验证了一个普适失效阈值”，而是：

> 一个条件化的 ZIFB 正极模型把游离 I2 过饱和、固态 I2 库存和可接近面积损失分开，并显示预测电压与固体库存轨迹对“库存到可接近性”的闭包形式高度敏感，而平滑体相渗透率损失在所考察窗口内很小。

主文应围绕这句话展开。现在的主文却围绕“为什么每一句都不能被误读”展开。

## 最高优先级问题

| 级别 | 问题 | 直接后果 | 必须采取的动作 |
|---|---|---|---|
| P0 | 审计语言压过科学叙事 | 读者记住 registered、production、closure、marker，却记不住现象 | 把分支 ID、哈希、求解器对象、复现闸门、反复免责移到 Methods/SI 的单独 reproducibility note |
| P0 | 主文与 SI 的功能倒置 | 主文在第 160–679 行先读十余页理论、方程和实现，结果到第 681 行才出现 | 主文只保留最小模型框架；详细守恒方程、参数身份和实现映射全部下沉 |
| P0 | 核心结论被五套隐喻包围 | scaffold、chain、clock、map、node、branch、window、boundary、rail 同时存在 | 只保留 “model”, “state”, “marker”, “operating map” 四个基本词 |
| P0 | Results 不是结果驱动，而是边界驱动 | 每个观察后立即跟一串 “not / rather than / conditional” | 每段先给观察和 1–2 个数字，必要边界只在段末出现一次 |
| P1 | Discussion 几乎没有真正讨论 | 五个小节中两个专讲负极和支持电解质，另两个重复 scope | 重写为“物理含义—设计含义—边界与可证伪测试”三段或三小节 |
| P1 | ZIFB 正极主角漂移 | 引言先讲负极/穿梭；讨论专设负极和 NH4Br 小节；主结果插入 NH4Br 组成序列 | 负极压缩成一个范围边界；NH4Br 组成结果移 SI，主文只留一句条件说明 |
| P1 | 术语和符号发生实质碰撞 | theta_eff、theta_cal、theta_island；Q 同时表示容量和流量；“native” 指代不清 | 建立并执行术语账本，见下文 |
| P1 | 图文层级错误 | 核心二维场图留在 SI，主文放更难解码的 x–Q 热图；图注承担方法和免责 | 把不同面容量下的 2D 场小倍图提升到主文；图注只解释图，不写审计报告 |
| P2 | 句子和段落严重超载 | 主文 66 个文本块中 31 个超过约 150 词；17 个超过约 250 词 | 一段一任务，通常 100–180 词；一句一个主命题，通常 10–30 词 |

## 定量语言信号

以下词频来自 TeX 源码，足以说明稿件的语言重心。它们不是“错误词”，问题是密度和重复功能。

| 信号 | main.tex | SI.tex | 诊断 |
|---|---:|---:|---|
| registered | 54 | 24 | 复现身份词进入科学叙事过多 |
| production | 90 | 28 | 被用成几乎所有对象的前缀，迫使读者不断解码 |
| closure | 67 | 48 | 必要术语，但远超读者可承受密度 |
| marker | 75 | 36 | marker / threshold / event / coordinate / landmark 相互竞争 |
| calibrated | 47 | 30 | 校准边界重要，但目前每段重复声明 |
| not | 153 | 127 | 整体语气由否定句驱动 |
| does not | 35 | 22 | 同一证据边界被反复重述 |
| rather than | 30 | 9 | 典型的“先预防误解再说结果”句法 |
| declared | 8 | 4 | 审计/合规口吻，不像研究叙事 |
| trajectory | 29 | 15 | 经常替代更直接的 “simulation” 或 “as charge increased” |
| coordinate | 21 | 3 | 把普通模型读数抽象化 |
| NH4Br | 21 | 20 | 支持电解质在主文中的存在感仍偏高 |
| TeX 三连字符 em dash | 20 | 14 | 与当前目标风格不符，也助长多重插入语 |

粗略 PDF 文本筛查（含图注和表格，因此只作为可读性警报，不作为精确语法统计）得到：

- 主文约 623 个可识别句段，平均约 28 词；172 个超过 30 词，93 个超过 40 词。
- SI 约 327 个可识别句段，平均约 35 词；111 个超过 30 词，66 个超过 40 词。
- 主文最长的普通文本块包括：Methods 约 764 词；“Production state markers...”约 598 词；“State variables...”约 575 词；理论节开头约 442 词。

这说明问题不是几句偶发长句，而是整篇按“一个段落装完一个审计主题”的方式写成。

## 必要边界与多余防御必须分开

不能把所有 caveat 一刀切。本文有几条会改变证据解释的真实边界，必须保留；问题是它们目前被散落复述，和大量预防假想误解的免责句混在一起。

| 类型 | 内容 | 最合适的位置与频率 |
|---|---|---|
| 必要方法边界 | theta_cal 是电压校准的模型变量，不是独立测得的可接近面积 | Abstract 一次，首次核心结果一次，Discussion limitation 一次 |
| 必要解释边界 | 电压不能单独识别沉积形貌 | closure-sensitivity 结果末句一次，Discussion 展开一次 |
| 必要数据边界 | composition、compression、rate 多为每条件一个物理电池，不能做总体推断 | SI experimental scope 统一声明一次，各表列 n_cell |
| 必要可比性边界 | 文献 i*=2Fk 与本体系条件、半周期和观测量不同 | 首次引入 i* 时一次，后文只称 literature scale |
| 必要模型范围 | 负极形貌、穿梭和循环重置未求解 | Introduction 范围一句，Discussion limitation 一段 |
| 必要先验边界 | DFT 是电子能排序，MD 是力场限定移动性先验 | 各方法首次结果末句一次，详细条件在 SI |
| 必要数据治理 | 旧 NH4Cl/NH4CL 标签实际为 NH4Br | Data provenance 集中说明；科学正文不反复提 |
| 多余防御 | 每次提 NH4Br 都说 “not the protagonist” | 删除；正面写 “The model uses ... as the supporting electrolyte.” |
| 多余防御 | 每次提模型标记都说 “not a physical threshold / landmark / reserve” | 定义时一次，后文稳定称 model marker |
| 多余防御 | 每次提孔网都枚举所有未排除形貌 | 结果末尾一句概括，详细范围放 limitation table |
| 多余防御 | 每个图注都声明 “not an image / not validation / not morphology” | 同一类图首次出现时一次；其余由图题和术语维持边界 |
| 多余防御 | branch、mesh、rtol、hash 用来在 Results 中证明可信 | 移 Methods/SI；结果可信度由一句 convergence reference 支撑 |

防御句的重写原则不是“删掉限制”，而是把限制改成正面范围。例如：

- 不写 “The model does not resolve the negative electrode.”  
  写 “The analysis focuses on the positive electrode; negative-electrode morphology is treated as an external full-cell boundary.”
- 不写 “These data do not validate the model thresholds.”  
  写 “These single-cell data provide descriptive full-cell context.”
- 不写 “NH4Br is not the protagonist.”  
  写 “The baseline model uses NH4Br as the supporting electrolyte.”
- 不写 “The calculation does not identify a real morphology.”  
  写 “The matched calculation quantifies sensitivity to two accessibility relations; morphology identification requires an independent spatial measurement.”

## 核心主张—证据地图

| 主张 | 当前证据 | 状态 | 正确措辞边界 |
|---|---|---|---|
| 平均游离 I2 饱和先于校准的 50% 可接近性损失 | 基线 COMSOL 分支，Qs=83.0，Qf,cal=99.6 mAh cm−2 | 在基线模型内充分支持 | “the baseline simulation predicts...”，不是物理阈值或实验事件 |
| 可接近性闭包改变耦合库存和电压轨迹 | 匹配真网格两分支，仅改变可接近性表达式；端点差 288.156 mV | 充分支持“模型形式敏感性” | 不得升级为真实沉积形貌证据 |
| 平滑体相渗透率损失不是该窗口内的主要电压驱动 | 孔网 K 接近 1；闭包注入后电压约变 1.3 mV | 在所测试平滑闭包内支持 | 不能排除局部孔喉、壳层或离散堵塞 |
| 氧化碘载体传输是模型饱和标记的主要敏感性来源 | 七点 D_eff 求解扫描；delta/D_eff 解析关系 | 在测试参数范围内支持排序 | 绝对幅度依赖未经本体系独立测量的 D_eff、delta、gamma_salt |
| 固态库存与功能损失不是同一状态 | 模型状态定义、闭包对比、外部类比 | 作为模型结论充分；作为真实电极机制仅部分支持 | 写成 “must be distinguished in the model”，不能写成已实验证实的两阶段机制 |
| NH4Br 浓度提高容量 | 每条件多为单电池，组成系列描述性重建 | 只支持协议限定的描述关联 | 移到 SI；不能成为主文机制或配方优化结论 |
| 更快传输/更高溶解度是设计方向 | 条件化敏感性分析和文献外部尺度 | 模型导出的假设 | 用 “the model prioritizes testing...” 而不是器件设计定律 |

最强证据是闭包匹配对比，因为改变对象单一、数值收敛检查明确。最弱的部分是把校准 theta 的变化写成“failure / collapse / blocking”，以及把单电池描述性数据带回主文为机制背书。

## 当前主文的 reverse outline

### 标题、摘要与引言

| 行号 | 当前段落任务 | 实际问题 | 处理 |
|---|---|---|---|
| 35–36 | 标题 | 准确但像项目说明书；“model coupling...”没有给出最有价值的发现 | 改成发现导向或问题导向标题 |
| 47–69 | 摘要 | 同时塞入背景、三状态、两个事件、渗透率、两组匹配解、三个端点数、288 mV、实验边界和 NH4Br 免责声明 | 重写为 5 个动作：问题、方法、两项主结果、意义；保留至多 3–4 个数字 |
| 75–81 | 领域重要性 | 基本可用，但 “low-cost, safe, abundant, high-potential, high theoretical capacity” 是宣传式形容词串 | 用高面容量下正极行为这一具体问题开场 |
| 83–95 | 全电池失效通道巡礼 | 先讲负极和穿梭，正极主线到段落后半才出现 | 压缩为两句范围背景，立即聚焦正极 |
| 97–117 | 正极知识缺口 | 一段混入固体不等于失效、四组文献、九倍阻抗、溶解尺度、Newman 理论和本文缺口 | 拆成“已知现象”和“缺少的状态关系”两段 |
| 119–122 | 声明 NH4Br 不是主角 | 语言本身反而把 NH4Br 推到聚光灯下；“protagonist”不应出现在论文 | 移至引言末尾的一小句或 Methods 条件句 |
| 124–137 | 本文做什么 | 逐项列 DFT、MD、纤维、孔网、COMSOL、文献尺度及所有免责 | 只写研究问题、模型层级和三项贡献；证据角色放图或 Methods |
| 156–158 | 固体产物类比 | 被 Fig. 1 插断后成为孤儿段 | 并回知识缺口段，或删除 |

引言目前回答“我们如何避免过度解释”，却没有用足够锋利的一句话回答“为什么现在必须研究 ZIFB 正极中固态库存到可接近性损失的映射”。

### 理论与模型（当前行 160–679）

| 行号 | 当前任务 | 主要问题 | 处理 |
|---|---|---|---|
| 160–193 | 理论节总览 | 442 词；state chain、state clock、boundary、picture、scaffold 同时出现；是路线图而非科学论证 | 压成约 150 词，只定义 S、eps_s、theta 和两个模型事件 |
| 195–234 | 主符号表 | 表注长达一个小段，含重复字母解释和模型身份 | 主文只留 8–10 个核心符号；完整表移 SI |
| 236–284 | 状态变量与简化 | 575 词；物种、迁移、边界层、参数端点、两个反应路径、未解析对象全部在一段 | 移至 Methods/SI；主文留一张模型框图和最小质量平衡 |
| 286–309 | 多尺度证据角色 | 信息必要，但四次重复“X does not...” | 用四行 evidence-role 表或简图，一次性限定 |
| 322–347 | 游离 I2 平衡 | 核心方程有价值；方程后又有 250 词解释每一项和免责 | 主文保留方程、物理解释和一个边界句；内部变量说明移 SI |
| 349–386 | 无量纲应力 | “load-bearing coordinate of the whole framework”属于自我宣布重要；随后反复解释同一 gamma/beta 约定 | 直接定义 S 和 Pi_gen；把约定与基准数值放 Methods |
| 388–420 | J–Q 边界 | 逻辑可保留，但在结果出现前给出过多投影和外部尺度规则 | 先给预测问题；边界构造可放 Methods，J–Q 图在 Results |
| 422–477 | 两个事件及累积律 | 598 词；事件定义、物理比较、文献类比、解析沉积律、面积闭包混在一起 | 拆成“事件定义”短段；累积律和基底换算移 Methods |
| 479–509 | 外部溶解尺度与支持电解质 | 属于范围/方法，不是主理论链 | 移 SI 或 Discussion 边界 |
| 511–565 | 连续体实现与几何 | 重复前文，图注也重复；解释模型电压不是实验拟合 | 主文保留一段“what is solved”；详细实现下沉 |
| 567–666 | 守恒方程、BV、Tafel、ODE、反馈 | 这是 Methods；在结果前形成约 100 行技术墙 | 整体移 Methods/SI |
| 668–679 | 假设边界与 evidence map | 又一次总结“什么不是”，与 Fig. 2 和前文重复 | 删除；在 Methods 放一次证据层级表 |

结构性结论：当前“Model framework”不是一个主文章节，而是完整的理论附录。若目标是让读者看懂正极结果，主文应最多保留 2–3 个核心方程和一个状态图。

### Results

| 行号 | 当前任务 | 主要问题 | 处理 |
|---|---|---|---|
| 681–692 | Results 路线图 | 用八个分号列出后续章节，完全是目录复述 | 删除；直接以第一项观察开头 |
| 694–702 | “What model does and does not predict” | 是审计声明，不是结果；四次证据标签后仍未出现数据 | 移 Discussion 的 limitation 末段或删除 |
| 704–738 | 基线状态演化 | 核心结果埋在 branch ID、非物理阈值声明、外部卤素类比和代数一致性检查之间 | 第一段只写 Qs、Qf,cal、空间位置和含义；类比与一致性检查移后 |
| 740–776 | 事件表和 x–Q 图 | 表、图和正文重复同一组标记；图注承担解码和免责 | 选一个主表达；优先使用不同 Q 下的 2D 场小倍图 |
| 778–796 | 节点相关性和电流分区 | 大量 Spearman/Pearson、无权重点采样限定，最终明确不用于形貌推断 | 整段移 SI；主文只保留端点电流分区这一句，如确有论证价值 |
| 798–815 | 闭包“adds information” | 标题是方法论陈述；段末转去三篇外部高倍率文献 | 改成“Accessibility feedback separates solid inventory from voltage response”并只讲本研究数据 |
| 831–860 | DFT/MD 先验 | 基本清楚，但精确能量、cluster 诊断、力场边界和全部排除项过多 | 主文讲排序和移动性趋势；精确设置与 caveat 放 SI |
| 876–918 | 纤维闭包和匹配真网格 | 这是强结果，但被求解器对象、网格身份和三套 epsilon 阈值压住 | 先写 288 mV 与 half-accessibility 未到；复现细节移 Methods |
| 920–951 | 孔网与传输通道 | 同一段同时给 K、30–100 倍负载、1.8 倍位置效应、三篇类比、D 与 mu 分离 | 拆成“平滑 K 很小”和“位置仍可能重要”两段；类比进 Discussion |
| 965–998 | transport/formulation envelope | 427 词连续报数；读者无法比较各变量 | 用排序图或 2D sensitivity map，正文只给前两位和关键范围 |
| 1000–1034 | J–Q operating map 与文献 dissolution rail | 图中把有 Q 坐标的模型边界与无 Q 坐标的外部标尺放在一起，正文花大量篇幅防止误读 | 分图；主图只保留模型求解点和明确插值，外部尺度移 SI |
| 1036–1055 | 文献锚与 NH4Br 组成 | 从模型结果跳到外部溶解和单电池组成数据，主线断裂 | 外部尺度进 Discussion；组成数据进 SI |
| 1057–1102 | 替代失效通道 | Results 与 Discussion 完全混写；含“what this rules out”及三类外部机制 | 本研究的 K 注入结果留 Results；外部通道与解释移 Discussion |
| 1104–1158 | 三节点和旋钮排序 | 与 965–998 高度重复；clean negative control、node、lever 等抽象词过密 | 合并成一个结果小节、一张图或表 |
| 1160–1172 | flow–delta 分析图 | 解析 Sherwood 场景是次要敏感性，不应占一个主图 | 移 SI |
| 1174–1188 | 设计含义 | 是 Discussion 内容；“something to protect”像演讲稿 | 移 Discussion，改成可检验的模型推论 |

Results 的正确写法应是“发生了什么”，而不是“这个结果属于哪一证据类别，以及它不能被解释成什么”。证据等级可以在第一次出现时标注一次，不应成为每段的句法骨架。

### Discussion、Conclusion 与末尾章节

| 行号 | 当前任务 | 主要问题 | 处理 |
|---|---|---|---|
| 1192–1203 | 两电极两区间 | 主要重复 scope，没有解释为什么闭包变化几乎不动 Qs 却大幅改变电压 | 用这一反差开 Discussion：饱和是上游传输状态，可接近性是下游反馈 |
| 1205–1214 | 负极范围 | 独立小节把主角移到负极，且 CDR 仅为情景估算 | 压成 limitation 中 2–3 句；图移 SI |
| 1216–1227 | 支持电解质范围 | 与引言、理论、结果、结论重复“NH4Br 不是主角” | 只在 Methods 条件与 limitation 各出现一次 |
| 1229–1259 | 可证伪预测 | 是 Discussion 最有价值部分，但四项过长且夹带方法类比 | 保留 2–3 个最强测试，每项一到两句 |
| 1261–1272 | Scope and bounds | 再次总结所有“不做什么” | 与 limitation 合并，最多一段 |
| 1274–1287 | 结论 | 科学边界比前文清楚，但仍像审计摘要；“traceable accounting”没有学术吸引力 | 三部分收束：贡献、最强证据、带边界的意义 |
| 1289–1356 | Methods | 764 词单块，六种方法只靠粗体词分隔；句子超载 | 真正分成小节；参数身份表和模型哈希放 SI |
| 1358–1367 | Data/code availability | 仍用 “will be deposited”，不是可提交状态；元数据更正写得过细 | 投稿前替换真实 URL/DOI；EXP-META-001 细节放数据说明 |
| 1369–1380 | 作者、致谢、利益冲突 | 仍是内部占位文本 | 投稿前必须由作者元数据替换，不能留在候选稿 |
| 1382–1388 | AI 声明 | 内容透明，但需按目标期刊模板决定是否保留及长度 | 校准期刊要求；避免把“assistance drafting”写成核心科学论证由 AI 起草 |

## 建议的新主文架构

这是一篇研究论文，不应按“理论手册 → 实现说明 → 审计报告 → 结果”排序。建议如下：

1. **Introduction**
   - P1：高面容量 ZIFB 正极的具体问题。
   - P2：已知的碘络合、固态 I2 和面积损失现象。
   - P3：关键缺口是固态库存与功能可接近性之间的状态关系。
   - P4：本文如何用连续体模型、分子/介观先验和闭包对比回答该问题。

2. **Results**
   - 2.1 **Saturation precedes predicted accessibility loss in the positive electrode**
   - 2.2 **Accessibility feedback controls the coupled voltage and solid-inventory response**
   - 2.3 **Molecular and mesoscale calculations bound transport and deposit accessibility**
   - 2.4 **Transport shifts the modeled positive-electrode operating map**

3. **Discussion**
   - 上游饱和与下游可接近性为什么解耦。
   - 为什么电压不能反演形貌，以及哪些测量能区分闭包。
   - 对正极设计的条件化含义和模型边界。

4. **Methods**
   - Continuum model
   - Accessibility variants and matched comparison
   - Molecular calculations
   - Mesoscale calculations
   - Existing experimental datasets and metadata correction
   - Numerical convergence and reproducibility

5. **SI**
   - 全部守恒方程、边界条件、参数表、分支 ID/哈希、完整扫描、描述性实验序列、负极情景、额外二维场和收敛证据。

如果目标期刊要求 Results 与 Discussion 合并，也应保持每个结果块的顺序为：问题 → 观察 → 量化 → 一句解释 → 一句边界。不能恢复现在的“先写所有边界再给结果”。

## Figure–text 同步问题

这是语言审计，但当前图文结构直接造成不可读。

| 主图 | 当前文本功能 | 问题 | 建议 |
|---|---|---|---|
| Fig. 1 conceptual progression | 五个状态和两个事件 | 图注约一整段，连续使用 registered / marker / production / not morphology；示意图变成定义墙 | 只保留三状态：dissolved → retained solid → reduced accessibility；两个 Q 标记直接画在单一横轴上 |
| Fig. 2 provenance | 解释各尺度证据身份 | 是审计图，不是结果图；与正文四次重复 | 简化后放 Methods 或 SI；主文不应花一个整图说明“每个工具不能做什么” |
| Fig. 3 geometry | 同时画连续体几何、反应路径、纤维和孔网 | 一个图承担三种尺度，图注又解释坐标、化学、输出和免责；用户需要很久才能建立空间方向 | 拆分。主文几何只保留电极、流向、collector/separator；纤维和孔网放 Methods/SI |
| Fig. 4 x–Q evolution | 展示 S、eps_s、theta 随 Q 和 x 演化 | 横轴 Q、纵轴 x=3–5 mm 不直观；核心二维空间信息反而在 SI Fig. spatial | 按用户建议，提升 Q=80/100/120 mAh cm−2 的 2D 小倍图；列为面容量，行为 S、eps_s、theta，统一空间方向与色条策略 |
| Fig. 5 matched closure | 核心闭包敏感性 | 最强结果，但图注被网格数、rtol、branch identity 淹没 | 标题直接给发现；复现条件移 Methods。正文只报 Qs 基本不变、theta/voltage 显著分叉 |
| Fig. 6 molecular priors | DFT 位点、cluster、MD 扩散同图 | 三种证据问题不同；图注主要告诉读者这些不是什么 | 主文只保留与上层模型直接相连的两个结论；cluster 诊断和完整电子结构进 SI |
| Fig. 7 mesoscale | 可接近性、K、位置效应 | 三个结论竞争；“physical”容易让读者误以为是真实形貌 | 改称 geometric model variants；每面板标题写结论，不用 “physical bound” 统称 |
| Fig. 8 J–Q map | 模型边界加文献 dissolution rail | 右侧 rail 没有 Q 坐标，虚线又含外推和单锚投影，视觉上必然诱导错误比较 | 主图只画已求解点与明确的模型插值/不确定区；文献 dissolution scale 单独进 SI 图或表 |
| Fig. 9 flow–delta | 解析 Sherwood 情景 | 次要且非求解主结果，占用主图预算 | 移 SI |

正文第 731–738 行已经承认真正的二维场在 Supplementary Fig. spatial，而主文只给 y 平均的 x–Q 图。这是明显的证据层级放反。对读者最直观的问题是“在 80、100、120 mAh cm−2 时，电极哪里先达到饱和、哪里积累固体、哪里失去可接近性？”主图应直接回答这一问题。

### 建议的 2D 图对应正文句法

不要在正文逐面板报数。可使用：

> As charge increased from 80 to 120 mAh cm−2, supersaturation remained a smooth through-plane gradient, whereas solid iodine and accessibility loss became concentrated near the separator-facing side of the positive electrode (Fig. X). The spatial separation shows that average saturation, local deposition and loss of accessible area are distinct model states.

图注只需定义行、列、坐标方向、共同色标和两条 Q 标记。关于“不是沉积图像”“不识别形貌”的边界写一次即可。

## Results 与 Discussion 混写的典型位置

| 位置 | 当前写法 | 为什么错位 | 目标位置 |
|---|---|---|---|
| 807–815 | 用三篇外部电池文献解释 inventory–current decoupling | 本研究观察尚未讲完就转解释和外推 | Discussion |
| 920–937 | 孔网结果后串联 ZnMn、ZnBr、TEMPO 类比 | 文献类比不是本研究结果 | Discussion |
| 939–951 | 从闭包进入 supporting-electrolyte quantitative route | 已变成设计解释 | Discussion |
| 1025–1044 | 外部 dissolution 值和机制语境 | 是跨研究解释/边界 | Discussion 或 SI |
| 1057–1102 | “rules out / does not exclude”及三类外部 failure channel | 是机制竞争和 scope | Discussion |
| 1174–1188 | “Design implication” | 明确属于 Discussion | Discussion |
| 1192–1227 | Discussion 两小节主要重复 scope | 没有解释核心结果 | 重写，不是简单搬移 |

## 术语账本

最终具体词形须用 ZIFB_W 语料校准；在校准前，以下是本稿内部的推荐单一用法。

| Canonical term | 首次定义 | 当前变体/冲突 | 决定 |
|---|---|---|---|
| ZIFB positive electrode | zinc–iodine flow-battery (ZIFB) positive electrode | positive carbon-felt electrode; positive iodine electrode; iodine positive electrode; catholyte electrode | 首次全称，之后统一 “positive electrode”；只在需说明基材时写 carbon felt |
| representative NH4Br supporting electrolyte | 1 M ZnI2 + 4 M NH4Br supporting electrolyte | formulation context; supporting bromide; representative electrolyte; protagonist | 只作为条件；禁用 protagonist |
| free I2 concentration | free molecular I2 available for precipitation | free monomer; precipitable monomer; free iodine; neutral intermediate | 正文统一 free I2；“monomer”仅在严格物种说明中使用 |
| supersaturation, S | S = c_free I2 / c_sat,eff | super-saturation; stress; free-I2 stress; saturation coordinate | 拼写统一 supersaturation；普通结果句用 S，不反复叫 stress/coordinate |
| average saturation marker, Qs | capacity at average S=1 | averaged-saturation marker; saturation-marker coordinate; registered crossing; landmark | 统一 average saturation marker；不要写 threshold，除非明确是模型定义 |
| solid-I2 volume fraction, eps_s | retained I2(s) volume per total electrode volume | native solid; native deposited species; retained solid; deposited inventory; solid inventory | 第一次定义后统一 solid-I2 volume fraction 或 solid inventory；禁用含混的 native |
| calibrated accessibility loss, theta_cal | voltage-calibrated model variable | functional accessibility; effective accessibility; calibrated response; production accessibility state; blocking | 统一 theta_cal；描述时写 predicted/calibrated accessibility loss，不写实物 blocking |
| island-model accessibility loss, theta_island | output of the dense isolated-island geometric model | physical-island relation; physical dense case; physical closure; dense shadow | 统一 island-model variant；“physical”改为 geometric，避免把理想化模型当真实形貌 |
| accessible carbon fraction, A_bare | A_bare = 1 − theta in active closure | surviving area; accessible area; bare area; functional accessibility | 保留已有 A_bare，不另造 A_acc；正文用 accessible-area fraction |
| baseline simulation | voltage-calibrated baseline continuum model | production branch; registered production branch; canonical branch; control | 科学叙事统一 baseline simulation；PB-R526...只在复现说明出现 |
| island-model variant | matched continuum solve using theta_island | physical-dense case; coupled dense-island solve; physical branch | 统一一种名称 |
| operating map | model outputs in the J–Q plane | operating boundary; window; envelope; state map | 图叫 operating map；具体线叫 saturation marker line 或 accessibility marker line |
| dissolution-derived current scale, i* | i*=2Fk from literature flux | clearance scale; current ceiling; rail; external kinetic scale | 统一 dissolution-derived current scale；一次说明不是本体系 ceiling |
| model-form sensitivity | change caused by replacing one closure in matched solves | causal model-closure sensitivity; closure sensitivity; model sensitivity | 用 controlled model-form sensitivity；避免 causal 引发真实机制误读 |
| descriptive full-cell data | existing one-cell or low-n composition/rate/thickness observations | validation; stress test; context; consistency evidence | 统一 descriptive context；不与模型标记放同一验证句 |

### 必须修复的符号碰撞

1. **theta_eff 与 theta_cal/theta_island**  
   SI 仍多次用 theta_eff 表示活动闭包，但主文已要求区分 theta_cal 与 theta_island。theta_eff 会重新抹掉这一区分。除纯占位通式外，应显式写当前分支变量。

2. **Q 同时表示面容量和流量**  
   主文把 Q 定义为 mAh cm−2；SI Table continuuminputs 又用 Q 表示流量。流量必须统一为 dot V 或 Q_flow，不能让核心横轴符号复用。

3. **eps_s,cal,traj* 的分支身份**  
   主文给 canonical production trajectory 的 1.18572×10−4，后文/ SI 又给 true-mesh control 约 1.1898×10−4 或 1.190×10−4。数值差异小，但同一符号被用于不同分支。要么只保留一种权威值，要么用下标明确 canonical 与 true-mesh。

4. **内部变量 cBr2**  
   该 COMSOL 名称实际表示 lumped oxidized-iodine pool，不是 Br2。只在复现表中出现，并明确为 legacy/internal variable name；不要进入主叙事。

5. **marker / threshold / event / coordinate / landmark**  
   模型定义统一用 marker；实验读数用 landmark；只有物理模型真正定义临界值时才用 threshold。不要为词汇多样性轮换。

## 禁用词与限用表达

### 从科学叙事中禁用

- protagonist
- load-bearing result / load-bearing coordinate / load-bearing conclusion
- state clock
- state chain
- evidence map（若已有 Fig. provenance，可在图名中一次使用）
- clean negative control
- what the model does and does not predict
- carried forward with explicit evidence labels
- declared midpoint / declared scenario（改为 defined 或 specified）
- fresh matched true-mesh solve（写 matched 7776-element simulations；“fresh”没有科学信息）
- traceable accounting
- branch-specific output（除 Methods/SI）
- production magnitude / production state（改 baseline-model output）
- physical comparator（改 geometric model variant 或 literature comparison）

### 严格限用

- registered：仅复现说明、分支表、数据清单。
- production：仅当确实区分 production run 与测试 run；普通结果统一 baseline。
- closure：每段最多一到两次，不作为多个名词的连续前缀。
- conditional：在首次声明模型适用范围和结论边界时使用，不在每句重复。
- not / does not / rather than：每段最多一个关键边界；能用肯定句就用肯定句。
- framework / scaffold：选一个，推荐 model。不能交替。
- trajectory：仅指完整随 Q 演化曲线；单个结果用 simulation/result。
- response / relation / coordinate：优先替换为具体动词和对象。
- central / principal / key / dominant：必须由图或数字直接支持，不能用来自我宣布。

### 常见替换

| 当前表达 | 推荐表达 |
|---|---|
| “the load-bearing production-model result is...” | “In the baseline simulation, average saturation occurred at...” |
| “closure-conditioned state-clock output” | “model-predicted interval” |
| “the model carries...” | “the model includes / calculates / assumes...” |
| “kept separate” | 直接定义两个对象，不再元叙事地说它们被分开 |
| “does not identify morphology”反复出现 | 在 Abstract、核心 closure 结果和 Discussion limitation 各说一次即可 |
| “rather than a universal ceiling”反复出现 | 首次定义 i* 后一次说明，后文直接称 literature scale |
| “within the registered production parameterization” | “in the baseline model” |
| “the present evidence supports only the following statement” | 直接写受限主张 |

## 代表性 before → after

这些 after 只使用稿件现有证据，不新增数据或机制。最终节奏和高频动词需再按 ZIFB_W 校准。

### 1. 标题

**Before**

> A zinc–iodine flow-battery positive-electrode model coupling solid-iodine deposition and accessibility loss

**After A（最稳妥）**

> Separating iodine saturation, deposition and accessibility loss in zinc–iodine flow-battery positive electrodes

**After B（发现导向）**

> Accessibility feedback separates iodine saturation from voltage rise in a zinc–iodine flow-battery positive-electrode model

**After C（方法导向）**

> A multiscale model of iodine deposition and accessibility loss in zinc–iodine flow-battery positive electrodes

首选 A。B 更有钩子，但 “voltage rise” 必须确保与最终图和表述完全一致。

### 2. 摘要开头

**Before（49–52）**

> In zinc–iodine flow batteries (ZIFBs), the positive carbon-felt electrode couples soluble-iodine speciation, native-iodine deposition and progressive loss of electrochemically accessible area. We develop a calibrated multiscale positive-electrode scaffold that distinguishes free-I2 saturation, retained solid-iodine inventory and functional accessibility.

**After**

> In zinc–iodine flow batteries, oxidized iodine can remain dissolved, deposit as I2(s), or reduce the accessible area of the porous positive electrode. These states are often treated as a single limitation. We developed a multiscale positive-electrode model that resolves them separately.

变化：用具体动词替代 “couples / scaffold / distinguishes”；第二句直接给知识缺口。

### 3. 建议的完整摘要草案

> Zinc–iodine flow batteries store charge by oxidizing iodide in a porous carbon positive electrode, where dissolved iodine, solid I2 and loss of accessible area evolve together. We developed a multiscale positive-electrode model that resolves these states separately. At 40 mA cm−2, the baseline simulation reached average free-I2 saturation at 83.0 mAh cm−2 and 50% calibrated accessibility loss at 99.6 mAh cm−2. Replacing the calibrated accessibility relation with a dense isolated-island model barely shifted the saturation marker, but lowered the predicted end-of-charge voltage by 288 mV and prevented 50% accessibility loss within 120 mAh cm−2. Pore-network calculations retained more than 95% relative permeability across this window, indicating that the simulated voltage rise is more sensitive to the accessibility relation than to smooth bulk clogging. The model therefore separates iodine saturation from electrode deactivation and identifies oxidized-iodine transport and deposit accessibility as the main uncertainties controlling the modeled positive-electrode operating range.

注意：若最终主图不能清楚支持 “more than 95%” 或 “voltage rise”，应删去相应句子，不可由摘要替图补证。

### 4. 引言定位

**Before（75–81）**

> Zinc–iodine flow batteries (ZIFBs) are an attractive chemistry for low-cost, safe aqueous grid storage: they pair an abundant, high-potential iodide/iodine catholyte with a zinc anode, decouple power from energy, and reach high theoretical capacity...

**After**

> High areal loading in zinc–iodine flow batteries places the porous positive electrode under a coupled chemical and transport burden. During charge, oxidized iodine must remain soluble or accessible while it accumulates inside the carbon felt.

变化：删掉泛化宣传语，第一句就把读者带到本文问题。

### 5. 知识缺口

**Before（108–117，节选）**

> The unresolved modeling question is therefore not only the appearance of iodine but the state relation by which retained inventory becomes associated with loss of electrochemically accessible area... an auditable, conditional electrode-resolved scaffold...

**After**

> Existing studies show that solid iodine can either remain electrochemically available or form resistive deposits, depending on the host and morphology. What remains unresolved is how solid-I2 inventory should be related to accessible reaction area in a porous ZIFB positive electrode.

变化：把 100 多词的防御式 gap 压成一个已知和一个未知。

### 6. 理论主线

**Before（162–178，节选）**

> The positive-electrode scaffold follows one state chain... The production interval ... is therefore a closure-conditioned state-clock output...

**After**

> The model separates three states: free-I2 supersaturation, solid-I2 inventory and accessibility loss. Average saturation defines Qs, whereas the calibrated condition theta_cal=0.5 defines Qf,cal. Their separation is a model output that depends on the accessibility relation.

变化：保留全部科学含义，删除 chain、clock、registered、production 等认知税。

### 7. 第一项结果

**Before（706–721）**

> The load-bearing production-model result is the separation between the saturation marker... These are events on the registered PB-R526... trajectory and are not physical-island thresholds or experimental landmarks...

**After**

> In the baseline simulation, the positive-electrode average reached S=1 at 83.0 mAh cm−2 and theta_cal=0.5 at 99.6 mAh cm−2 (Fig. X). The resulting 16.6 mAh cm−2 interval separates average free-I2 saturation from the midpoint of the calibrated accessibility response. These values are model markers, not experimental thresholds.

变化：结果先行；分支 ID 移 Methods；边界只说一次。

### 8. 闭包敏感性

**Before（891–913，节选）**

> We then performed a fresh matched true-mesh continuum comparison from byte-identical copies of the canonical input... Both branches use the same study... live solution... mesh... rtol... The dense-island terminal voltage is 288.156 mV lower...

**After**

> Changing only the accessibility relation had little effect on average saturation but strongly altered the later charge response (Fig. X). Qs differed by 0.002 mAh cm−2 between the matched simulations, whereas the island-model variant did not reach theta=0.5 by 120 mAh cm−2 and ended 288 mV below the baseline voltage. Accessibility feedback also reduced the predicted solid-I2 inventory. Numerical settings and convergence tests are reported in Methods and Supplementary Table X.

变化：把最强证据从复现细节后面移到第一句。

### 9. 介观渗透率结果

**Before（920–937，节选）**

> A pore-throat network ... tests whether deposited I2 throttles transport by clogging. For every one of the six deposit-placement laws swept... This rules out only that continuum-permeability channel...

**After**

> Across six deposit-placement rules, the pore-network models retained 98–99% of their initial permeability at the simulated solid loading. Smooth bulk clogging therefore contributed little within the modeled window. This result does not exclude local pore-throat or shell-like blockage, which the network representation does not resolve.

变化：一个观察、一个含义、一个边界。

### 10. 参数敏感性

**Before（965–998）**

> 427 词连续列出 csat、phi_ppt、D_eff、delta、viscosity、ranking 和 caveat。

**After**

> The saturation marker was most sensitive to oxidized-iodine transport. Across the seven solved diffusivity cases, Qs increased from 45 to 106 mAh cm−2 as D_eff/D0 rose from 0.5 to 2.0 (Fig. X). Solubility was the second-largest source of variation, whereas smooth permeability changes were negligible within the baseline loading range. Because D_eff and the salting correction were not independently measured in the present electrolyte, these sweeps support a sensitivity ranking rather than absolute design limits.

### 11. Discussion 开头

**Before（1192–1203）**

> The solved contribution is confined to the ZIFB positive electrode... Within the solved regime we keep four objects separate...

**After**

> The matched simulations reveal an upstream–downstream separation in the positive electrode. Average free-I2 saturation changed little when the accessibility relation was replaced, whereas the subsequent solid inventory and voltage diverged strongly. Saturation is therefore controlled mainly by the imposed transport and speciation state, while the late voltage response depends on how deposited iodine is mapped onto accessible reaction area.

这才是 Discussion 应解释的核心反差。

### 12. 设计含义

**Before（1185–1188）**

> Fast oxidized-iodine transport is therefore something to protect, not to trade away for other electrolyte properties...

**After**

> Within the tested parameter range, the model prioritizes maintaining oxidized-iodine transport over changing smooth hydraulic permeability. This prediction should be tested with electrolyte-specific diffusivity and speciation measurements before it is used as a formulation rule.

变化：删除口号，保留可证伪的条件化推论。

### 13. 结论

**Before（1275–1287，节选）**

> We developed an auditable state model... The principal contribution is therefore a traceable positive-electrode accounting with explicit falsification tests for each link. NH4Br is only...

**After**

> We developed a ZIFB positive-electrode model that separates free-I2 saturation, solid-I2 inventory and accessibility loss. In matched simulations, the saturation marker remained nearly unchanged when the accessibility relation was replaced, but the later solid inventory and voltage differed substantially. The result identifies deposit accessibility, rather than smooth bulk permeability loss, as the main unresolved link between iodine accumulation and the modeled late-charge response. This conclusion is conditional on the calibrated baseline model and does not identify the deposit morphology.

### 14. 图注

**Before（Fig. 3 caption，523–535）**

> 一个图注同时解释 2D 几何、反应、符号不是沉积图像、输出字段、y 平均、单纤维、孔网和校准关系。

**After**

> **Positive-electrode model domain and boundary conditions.** Electrolyte flows along y through a 2-mm carbon felt, while electronic and ionic current enter from the collector and separator-facing boundaries, respectively. The model calculates free-I2 supersaturation, solid-I2 volume fraction and accessibility loss across this domain.

纤维和孔网模型应在另一图或 SI 中定义。

## SI 语言与架构审计

SI 可以技术化，但不应成为第二份主文或内部审计日志。

### 可保留的 SI 功能

- 完整控制方程、边界条件、初值和参数表。
- baseline 与 island-model variant 的模型身份、哈希、study/solution/dataset 对应。
- DFT、MD、单纤维和孔网的完整方法与收敛/限制。
- 完整参数扫描。
- 描述性组成、厚度、倍率和 dV/dQ 数据及纳入规则。
- EXP-META-001 的原始标签保留与规范化说明。

### SI 的主要问题

1. **重复主文的边界声明**  
   SI 中 not 出现 127 次，does not 出现 22 次。技术补充应给事实和限制表，不应每段重新辩护。

2. **复现身份散落在叙事中**  
   PB-R526、SHA、stdR522、sol5、dset5 应集中成一个 “Computational provenance” 表。正文只引用该表。

3. **参数扫描仍写成数字瀑布**  
   919–1025 的每个 knob 段落把十几个端点塞进长句。应改成统一表：range、Qs、Qf、eps_s,end、theta_end、V_end、evidence class。正文每个 knob 只写一句趋势。

4. **超范围水力外推语言不专业**  
   203–210 写到压力约 8 bar、“mechanically ruptures tubing and seals in practice”和“fully-destabilised hydraulic runaway”。这不是本研究已验证结果，也没有在此处给直接证据。建议删除器材破裂叙述；若保留数学外推，只写 “outside the calibrated range and not interpreted physically”。

5. **“causal model-closure sensitivity”措辞过强**  
   Table matchedclosures 的受控替换确实隔离了模型输入变化，但 “causal” 容易被理解为真实沉积机制因果。统一为 controlled model-form sensitivity。

6. **描述性实验章节过多解释同一个低 n 边界**  
   Composition、compression、rate、G4 每节都反复说 n_cell=1、not validation。可以在 Experimental data scope 开头统一声明一次，各表只给该数据集特有的限制。

7. **NH4Br/NH4Cl 更正应集中**  
   EXP-META-001 在 SI data provenance 中详细说明一次，在相关图注加一句脚注即可。不要在多个科学段落重新解释。

8. **Limitations 表与主文重复**  
   SI Table bounds 有价值，但主文、SI 正文和多个图注已逐条重复。把它作为唯一的详细边界台账，其他位置引用即可。

### SI reverse outline

| SI 部分 | 当前作用 | 重构建议 |
|---|---|---|
| S1 governing equations | 方程、状态、几何、流动、边界 | 保留；拆出一页 Computational provenance；删除主文式路线图 |
| S2 molecular priors | DFT/MD 表与图 | 保留；把“不是...”集中到每方法末尾一句 |
| S3 mesoscale closures | 阈值、匹配求解、MD protocol 混排 | 分成 geometric closure 与 matched continuum comparison；MD protocol 移回 S2 |
| Voltage degeneracy | 三张图 | 保留；标题和图注直接写模型结论，减少 morphology 枚举 |
| Experimental provenance | 格式、温度、metadata correction | 保留，作为所有后续实验节的共同前言 |
| G4 / compression / composition / rate | 描述性数据审计 | 合并为 Existing full-cell datasets，下设四小节；统一统计边界 |
| Key parameters | 两大参数表和 provenance 缺口 | 保留；增加 “measured / literature / fitted / prescribed / numerical” 五类图例 |
| Native-solid constants | 详细 ODE 和参数 | 保留；明确 eps_s 与 auxiliary state，不重复 2972 倍多次 |
| Per-knob scans | 数字瀑布 | 表格化并配统一 small multiples |
| Transport accounting | 通道边界表 | 保留，可能取代主文多处解释 |
| Negative-electrode estimate | 场景图 | 保留在 SI，但标题不要称 sanity check；写 illustrative estimate |
| Limitations and scope | 总边界台账 | 保留为唯一详细边界源；主文只摘要 |
| 2D field maps | 核心空间证据却放在最后 | 重绘后提升主文；SI 保留完整变量和更多 Q |

## “不像人写的”具体来自哪里

1. **每个名词都被加了身份前缀**  
   “registered production-state event”, “production accessibility relation”, “physical dense-island coupled solve”, “closure-conditioned operating boundary”。人类作者通常在第一次定义后直接称 Qs、theta_cal、baseline model。

2. **主语不是物理对象，而是文档管理对象**  
   大量句子以 “The framework”, “The map”, “The branch”, “The relation”, “This distinction”, “These scales” 开头。应让 positive electrode、free I2、solid iodine、accessibility、current 或 simulation 成为主语。

3. **一句话同时完成观察、解释、免责和文献定位**  
   这使句子不可自然朗读。每句只做一个主命题。

4. **反复给读者下解释禁令**  
   “not morphology”, “not threshold”, “not validation”, “not ceiling”, “not a second species”都有必要，但现在像法律条款。定义一次，随后用稳定术语自动维持边界。

5. **混用工程隐喻**  
   scaffold、chain、clock、map、nodes、branches、envelope、window、rail 让论文像在不断换白板。选一套最少词汇。

6. **过度精确的内部身份进入结果**  
   0.002、0.0938 mV 等数值适合收敛表，不适合主叙事。正文报告能改变科学判断的精度，数值审计放 SI。

7. **段尾总是最长、最弱**  
   许多段落最后一句列出所有仍然可能的机制，导致读者结束一段时不知道作者到底得到了什么。

## 可执行重写规则

1. 每个主图只允许一个主张；每个 Results 小节只回答一个问题。
2. 每段通常 100–180 词；超过 200 词必须拆分。
3. 每句 10–30 词；超过 20 词检查是否有两个以上主命题。
4. Results 每段只保留 1–2 个最能支持局部主张的硬数字。
5. 复现 ID、哈希、study、solution、dataset、rtol 和 mesh 数统一进 Methods/SI 表。
6. 同一科学边界在 Abstract、首次结果、Discussion limitation 各说一次即可。
7. NH4Br 在主文只承担三处功能：实验/模型条件、一次支持电解质范围说明、Methods 配方。组成扫描移 SI。
8. 负极在主文只承担一个范围边界段，不单设 Discussion 小节。
9. 不使用 em dash；用句号拆分。
10. 不为词汇多样性更换术语；术语一致性高于文采。
11. 不把 calibrated theta 写成 observed blockage/collapse。
12. 不把 geometric island model 称为真实的 physical morphology。
13. 先完成 ZIFB_W 风格 DNA，再做全稿微观措辞；否则会得到另一版流畅但仍不像组内论文的通用 AI 英文。

## 推荐的重写顺序

1. 锁定一条中心主张和 4 个 Results 问题。
2. 重排主图，优先解决 2D 场图、closure sensitivity 和 J–Q 图。
3. 按新图写 Results；不要从旧段落逐句润色。
4. 从 Results 反推 Introduction 和 Discussion。
5. 重写 Title、Abstract、Conclusion。
6. 将所有方程、身份、审计和完整扫描迁移到 Methods/SI。
7. 用术语账本做全局替换和人工复核。
8. 用 ZIFB_W 语料校准高频动词、段落长度、标题句型、图注句法和 hedging。
9. 最后才做语法、冠词、时态、连字符、单位和引用格式。

## 最终判定

- **科学内核**：可形成一篇有明确价值的条件化 ZIFB 正极建模论文。
- **当前语言可投稿性**：不通过。
- **当前论证架构可投稿性**：不通过。
- **最致命问题**：主文把“可审计”误写成“持续自我辩护”，导致真正的闭包敏感性结果失去冲击力。
- **最值得保留并放大的结果**：Qs 对闭包替换几乎不变，而后续 theta、solid inventory 和 voltage 强烈分叉；这清楚揭示了上游饱和与下游可接近性反馈的不同角色。
- **下一步**：不是 polish 现有句子，而是按上述新架构重写 Results，并让新图决定段落。只有在图和论证稳定后，才进入 ZIFB_W 风格的逐句校准。
