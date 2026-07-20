# R582 逐句引文支持审计（claim-to-source）

> **历史整改快照，不是当前投稿状态。** 本文件审计的是早期
> `R582_MAIN_TEXT_DRAFT.md`，其中的 PARTIAL/FAIL 行是推动后续修订的输入。
> 当前权威源为 `main_R582.tex`/`SI_R582.tex`；这些问题已在
> `R582_FINAL_CITATION_EVIDENCE_AUDIT.md` 中逐项关闭。机器可读 CSV 保留
> 原判定以保存整改轨迹，不得把它解释为当前 canonical manuscript 的 open findings。

日期：2026-07-20  
审计对象：`manuscript/audit_R582/R582_MAIN_TEXT_DRAFT.md`  
机器可读明细：`manuscript/audit_R582/R582_SENTENCE_CITATION_AUDIT.csv`  
范围：正文所有含 `\citep{...}` 的句子，以及与 COMSOL、物种平衡、溶解度、DFT、MD 可复现性直接相关的无引文方法句。  
操作边界：只读核查；未修改正文、`refs.bib`、原始 PDF、实验文件或模型文件。

## 结论先行

本轮将 10 个含引文段落拆成 28 个最小可核声明：

| 结论 | 数量 | 含义 |
|---|---:|---|
| FULL | 20 | 引用原文直接支持当前声明；仍须保留已写明的体系边界 |
| PARTIAL | 3 | 证据方向正确，但句子把不同证据类型或未证实的修饰词混在一起 |
| FAIL | 3 | 关键方法参数或软件 provenance 在首次使用处没有可核引用 |
| CONTEXT-RISK | 2 | 引用本身存在，但体系、架构或参数化范围容易被读成可直接外推 |

**正式投稿前必须修改 7 处。** 其余引文句可保留或仅做收紧。当前最实质的问题不是 DOI 或 BibTeX，而是：

1. 把静态 Zn-I2 电池综述/高载量工作并入“ZIFB studies”；
2. 用 Palmer 平衡热力学支撑“rapidly”这一动力学副词；
3. 把基础多孔电极理论与流动电池实现写成同一层证据；
4. 把 ZnO、Li2S 的实验工作统称为“models”；
5. COMSOL 6.3 缺软件版本/build/module citation；
6. `K_I`、`K_Br` 和“rapidly interconverting”在方法首次使用处无来源；
7. `c_sat^eff` 的稀水溶解度与跨盐 salting prior 未在 R582 主文方法中恢复其来源和不可转移限定。

## 判定规则

- **FULL**：原文的实验、方程、图表或方法定义直接支持最小声明。
- **PARTIAL**：来源只支持句子的一部分，或句子把模型、实验、综述混称。
- **FAIL**：未找到支持，或所引来源不承担该声明。
- **CONTEXT-RISK**：来源支持其自身体系，但当前写法会诱导跨宿主、跨电解液或跨电池架构外推。

DOI、题名或摘要只用于定位，不能替代结果页/图表。未能定位的内容按 FAIL 处理，不从文件名或旧锚表反推。

## 必须修改的 7 处

### 1. Introduction L17：ZIFB 与静态 Zn-I2 电池混引

原句引用集：`Li2015,Xie2018,Weng2017,Wen2025,Fan2024,Huang2025,WuLoading2025`  
判定：**CONTEXT-RISK**

- `Li2015`、`Xie2018`、`Weng2017` 和 `Fan2024` 是流动电池直接证据。
- `Wen2025`、`Huang2025` 是更广义/主要静态 Zn-I2 综述；`WuLoading2025` 是高载量静态干电极工作。
- 因此不能把七篇整体称作“Recent ZIFB studies”。

安全措辞：

> Over the past decade, zinc-polyiodide flow batteries have combined high-energy iodide chemistry with electrolyte, membrane and cell-design strategies for improved power and cycling performance \citep{Li2015,Xie2018,Weng2017,Fan2024}.

若需要保留 `WuLoading2025`，应另起一句，明确它是**静态 Zn-I2 高载量架构的邻域证据**，不能用来证明本流动毡电极的工作状态。

### 2. Introduction L19：Palmer 不支持“rapidly”

判定：平衡/主物种 **FULL**；动力学副词 **PARTIAL**。

- Palmer 1984 p.673 Eq.1 直接定义 `I2(aq)+I-(aq)<=>I3-(aq)`；pp.677-679 Tables III-IV 给出 25 C 的 `K=698+/-10`。
- Palmer 是平衡常数、活度系数和温度/离子强度研究，**没有测定络合速率**。
- Wen 2025 p.4 综述写到该反应有利且快，但这只是二手动力学表述；本句不需要该副词。

安全措辞：

> In excess iodide, aqueous I2 is partitioned by the I2 + I- <=> I3- equilibrium; I3- is commonly treated as the dominant soluble polyiodide \citep{Palmer1984,Wen2025}.

### 3. Introduction L21：基础理论与 flow-cell 扩展必须拆开

判定：**PARTIAL**。

- `Newman1962` 支持多孔电极电流分布理论。
- `Tichter2020` 是宏观多孔电极循环伏安理论，不是流动电池实现。
- `Chakrabarti2020` 系统综述流动电池多尺度模型。
- `AparicioMauricio2023` 直接建立三维流动电池 tertiary-current model，并求解浓度、速度、固/液相电势及电流分布。

安全措辞：

> Porous-electrode theory resolves coupled current and species transport \citep{Newman1962,Tichter2020}; flow-battery extensions calculate concentration, current and potential distributions across porous cells \citep{Chakrabarti2020,AparicioMauricio2023}.

### 4. Introduction L21：不能把实验论文统称为 models

判定：**PARTIAL**。

- `LiS_ROM_JES2025` 是 reduced-order model；其 Eq.13 明确把孔隙率变化映射到反应面积。
- `ZnO_EEM2024` 是原位光学/Raman 实验，显示 ZnO 析出膜先出现，随后约 255 mV 发生钝化。
- `Li2S_EcoMat2024` 是形貌控制和电化学实验，2D film 与 3D particle 对应不同钝化行为。

安全措辞：

> Studies of other solid-product electrodes, including reduced-order modeling and operando characterization, show how precipitation can alter reaction area and transport \citep{LiS_ROM_JES2025,ZnO_EEM2024,Li2S_EcoMat2024}.

### 5. Methods L39：COMSOL provenance 缺失

判定：**FAIL**。

R582 写了“COMSOL Multiphysics 6.3 solves ...”，但 `refs.bib` 没有 COMSOL 条目，正文也没有 exact build、使用模块或 vendor citation。`Newman1962`/`AparicioMauricio2023` 等理论论文不能代替软件 provenance。

最低安全补充：

> COMSOL Multiphysics 6.3 [exact build; named Electrochemistry/CFD modules], COMSOL AB, Stockholm, Sweden, was used to solve ...

并在 SI/数据包保留：软件 build、模块、study/solver/dataset 名称、输入副本 hash、导出 hash。若期刊不要求 BibTeX 软件引用，完整 vendor citation 仍不可省略。

### 6. Methods L39-L50：`K_I`、`K_Br` 与“rapidly interconverting”无首次使用引用

判定：**FAIL**。

- Palmer 1984 只支持 `I2/I-/I3-` 平衡和活度；它不能支持 `K_Br`。
- Park 2021 直接估计 `I2Br-` stability constant 和 `I2/I3-/I2Br-` fractional diagrams。
- Weng 2017 p.1 直接说明 Br- 稳定 iodine、形成 `I2Br-`，但不是本项目 4 M NH4Br 的原位参数测量。
- 当前句把“局部平衡的模型降阶”写成已实证的共同快速动力学。

安全措辞：

> The dissolved oxidized species were treated as a locally equilibrated lumped pool. The I2/I-/I3- partition follows Palmer et al., whereas I2Br- formation is represented by a conditional bromide-complexation prior \citep{Palmer1984,Park2021,Weng2017}.

SI 参数表必须列出 `K_I=0.72 m3 mol-1`、`K_Br=0.0115 m3 mol-1`、各自来源、单位换算、角色为 conditional prior，而不是本电解液测量。Br- 仍应保持 supporting ligand 的定位。

### 7. Methods L48：`c_sat^eff` 的来源与跨盐边界被省略

判定：**FAIL**。

旧 SI 已有正确且谨慎的分类：

- `c_sat=1.33 mol m-3`：Ramette 1965 的稀水 intrinsic reference；
- `gamma_salt=3`：Palmer 1984 的 ionic-strength/salting 行为所约束的 **bounded cross-salt prior**；
- `c_sat^eff≈0.44 mol m-3`：模型内派生值，**不是** 1 M ZnI2 + 4 M NH4Br 的实测表观溶解度。

R582 主文只写“includes the specified salting correction”，会把最弱约束输入写成既定物性。必须在首次使用处恢复 `Ramette1965` 与 `Palmer1984`，并明确 cross-salt、not-present-electrolyte-data 和 sensitivity range。

## 可直接保留的外部科学证据句

### 宿主依赖与形貌边界

1. **纳米孔碳中保留固体碘仍可逆** — **FULL**。  
   `SolidI2_NatCommun2020` pp.4-6, Figs.2g,3c-d,4a-c：约 30% 孔占据仍保持高倍率、近 100% CE 和数百循环无明显性能退化。`Fitzek2023` pp.6-9, Figs.2-4 进一步支持稳定循环阶段的可逆结构/光谱变化。

2. **致密 I2 膜显著提高 Rct** — **FULL**。  
   `Jang2021` p.6385 abstract、pp.6388-6391, Figs.3-6：多孔膜转为致密膜后，Rct 从低于 16.5 增至 147.4 ohm cm2；在实际 flow cell >400 mA cm-2 时伴随 >300 mV 的过电位跃升。建议把“dense iodine deposits”收紧为“dense iodine film”。

3. **充电成膜、放电后残余颗粒** — **FULL**。  
   `LiDualPlate2025` pp.3163-3164, Fig.3a-b/S12：210 s 充电后黄色 iodine film 覆盖石墨毡碳纤维；420 s 放电后仍见少量 I2 颗粒。当前“in a different iodine cell”限定必须保留；其 G4/I- dual-plating chemistry 不可外推到本电解液。

4. **两种宿主的对照结论** — **FULL**。  
   Results L146 用 `SolidI2_NatCommun2020` 对照 `Jang2021` 是合格的 host-specific identifiability 论证。紧随其后的“不把两者形貌转移到本 felt”一句不能删。

### 溶解动力学与可测量性

5. **Zhao 2022 的条件性溶解/电流尺度** — **FULL**。  
   pp.14090-14096, Figs.2-5：UV-vis particle-dissolution model 与 chronoamperometry 共同给出 dissolution rate；7.5 vol% ACN 使速率常数约增一数量级，并改变稳定充电电流范围。当前后句已经说明浓度、方法和 half-cycle 不同，方向正确。建议把“iodine clearance”改成更可核的“iodine dissolution kinetics”。不得把其 80-140 mA cm-2 当成本项目上限。

6. **UV-vis 定量 I3-** — **FULL，但仅限相关体系**。  
   `ZnNC_AEL2025`（实际书目信息为 ACS Energy Lett. 2026）p.1735, Fig.2c-f/S10：I-/I3- adsorption capacity 与 dissolved I3- tracking。`WangNatCommun2025PSI` pp.5-6, Fig.3a/S11-S12：I3- 吸光度-浓度标定与 in-situ UV-vis/Raman。安全表述应点名“dissolved I3-”，不能泛化为本 felt 内的 local free-I2 或 accessible area 测量。

7. **EIS 跟踪 iodine-film-associated Rct** — **FULL**。  
   `Jang2021` 的 EIS/chronoamperometry 直接支持。应保留“Jang-system boundary”，不能把 147.4 ohm cm2 或 400 mA cm-2 数字转移成本项目阈值。

## DFT/MD 方法引用审计

### DFT：全部方法引用匹配

| 方法声明 | 引用 | 判定 | 必须保留的边界/复现项 |
|---|---|---|---|
| CP2K/Quickstep | `Kuhne2020CP2K,VandeVondele2005Quickstep` | FULL | 补 actual CP2K version/build |
| PBE | `Perdew1996PBE` | FULL | 无 |
| D3(BJ) | `Grimme2010D3,Grimme2011D3BJ` | FULL | 两篇分别承担 D3 与 BJ damping |
| DZVP-MOLOPT-SR-GTH | `VandeVondele2007MOLOPT` | FULL | SI 给 basis-set file 与逐元素 alias |
| GTH pseudopotentials | `Goedecker1996GTH,Hartwigsen1998GTH,Krack2005GTHPBE` | FULL | SI 给逐元素 `GTH-PBE-q*` 名称 |
| counterpoise | `Boys1970Counterpoise` | FULL | 保留“single-point correction”，勿写成优化全程校正 |

这些引用只证明方法/软件出处，不证明本项目的 150 Ry/30 Ry cutoff、Gamma sampling、有限 slab 或所得 site ordering 已收敛。当前“not solution free energies or nucleation barriers”限定正确，必须保留。

### MD：标准方法引用匹配；项目特定 analogue 不获外部验证

| 方法声明 | 引用 | 判定 | 必须保留的边界/复现项 |
|---|---|---|---|
| GROMACS | `Abraham2015GROMACS` | FULL | 补 actual version/build |
| SPC/E | `Berendsen1987SPCE` | FULL | 无 |
| Joung-Cheatham monovalent halides | `Joung2008Ions` | FULL | 点名 SPC/E 行、Br-/I- 参数 |
| Packmol | `Martinez2009Packmol` | FULL | 无 |
| electronic-continuum charge scaling | `Leontyev2009ECC` | FULL | 给 scaling factor；不得写成已验证参数 |
| project-specific I3-/I2Br- analogues | 无外部验证 | CONTEXT-RISK | 释放 topology/parameters；保持“mobility prior”措辞 |

`Abraham2015GROMACS` 等标准引用不能为 I3-/I2Br- analogue force fields 或扩散率数值背书。当前“one trajectory”“four contiguous blocks are not independent-replica SE”“mobility prior”三层限定均应保留。

## Palmer、Br- 与溶解度：投稿时的精确分工

| 来源 | 可承担的声明 | 不能承担的声明 |
|---|---|---|
| `Palmer1984` | I2+I-<=>I3-；K=698+/-10 at 25 C；NaClO4 ionic-strength/activity behavior | complexation rate；K_Br；4 M NH4Br 中实测 solubility |
| `Park2021` | I2Br- stability constant/fractional diagrams；高 Br- 条件下 soluble I2Br- formation | 本项目 4 M NH4Br 的直接参数测量 |
| `Weng2017` | Br- 作为 iodine complexing ligand 形成 I2Br- 的 flow-battery precedent | 本项目的 K_Br 数值或局部平衡速率 |
| `Ramette1965` | dilute-water intrinsic I2 solubility reference | concentrated mixed-salt apparent solubility |

这套分工同时保护用户的核心叙事：**ZIFB 正极是主角；NH4Br/Br- 只是代表性 supporting electrolyte/ligand，不是论文主角。**

## 逐句保留清单

下列原句或最小声明可保持科学含义不变：

- L19：充电时 I- 氧化为 I2（`Wen2025`）。
- L19：I2/I-/I3- 平衡与 I3- 主要可溶聚碘表示（去掉“rapidly”后）。
- L19：纳米孔宿主可保留固体碘并保持可逆（必须保留 host qualifier）。
- L19：致密 I2 film 与 Rct 大幅增加（建议把 deposits 改成 film）。
- L19：另一个 iodine cell 中充电膜/放电残粒（必须保留 different-cell qualifier）。
- L70：CP2K/Quickstep、PBE、D3(BJ)、MOLOPT、GTH、counterpoise 方法出处。
- L72：GROMACS、SPC/E、Joung-Cheatham、Packmol、MDEC/ECC 方法出处。
- L146：confined reversible host 与 dense-film high-resistance system 的对照及不可转移限定。
- L160：Zhao 2022 的 condition-specific dissolution statement。
- L162：related systems 中 UV-vis 定量 dissolved I3- 的可执行先例。
- L162：Jang 2021 的 iodine-film-associated EIS/Rct 先例。

## 证据完整性与误命名防线

- 未使用 `round2/ChemRev_Bazant2022.pdf` 作为 Bazant 证据；该文件实为 Bui et al. 多孔电极综述。
- 未使用 `round2/Davies1952.pdf` 作为 Davies & Gwynne 1952；该文件实为 Katzin & Gebert, JACS 1955, 77, 5814。
- Jang 结论来自已补抓的一手 `round12/Jang_ACSAMI2021_IodineFilm_ChargeTransferResistance.pdf`，不是 Vanek 二手转引。
- `ZnNC_AEL2025` 是 citation key，不是年份权威；`refs.bib` 的正式元数据为 ACS Energy Letters 2026, 11, 1732-1740。
- Zotero 本地 API 用于条目/附件定位；题名、摘要和库条目未被当作结果证据。
- Li2015 与 Xie2018 本地未发现对应正文 PDF；只用官方 publisher page 的摘要验证其 broad introductory claim，不用其摘要承担形貌、参数或阈值声明。

## 最低通过门槛

正文冻结前应满足：

1. 七个 `MUST_CHANGE` 全部落实；
2. R582 SI 恢复 `K_I/K_Br/c_sat/gamma_salt` 的数值、单位、来源、角色和 sensitivity；
3. COMSOL/CP2K/GROMACS 写明 actual version/build，并在数据包给可复现输入身份；
4. 任一 host-specific 文献句后不出现 present-felt morphology inference；
5. `Zhao2022` 不被转换为本体系 current ceiling；
6. UV-vis 先例只称 dissolved I3- / related-system protocol，不称 local free-I2 validation；
7. 最终 TeX 再跑一次句级 citation diff，确认修稿没有让引文跨句漂移。

## 主要核查锚

- `R576_anchor_table.md`
- `literature_pdfs/round2/Palmer1984.pdf`
- `literature_pdfs/round2/SolidI2_NatCommun2020.pdf`
- `literature_pdfs/Fitzek2023.pdf`
- `literature_pdfs/round12/Jang_ACSAMI2021_IodineFilm_ChargeTransferResistance.pdf`
- `literature_pdfs/round3/Li_EES2025_DualPlatingHalogenComplexation.pdf`
- `literature_pdfs/round2/ZnO_EEM2024.pdf`
- `literature_pdfs/round2/Li2S_EcoMat2024.pdf`
- `literature_pdfs/round2/LiS_ROM_JES2025.pdf`
- `literature_pdfs/round2/ZnNC_AEL2025.pdf`
- `literature_pdfs/round3/Wang_NatCommun2025_PolysulfideIodideRFB.pdf`
- `electrochemical/03_final_interpretation_packages/ZIFB_ECHEM_R03_EXISTING_DATA_ONLY_INTERPRETATION/input_copies/d2ta03195g.pdf`

完整逐行判定、页码/图表、短摘、建议措辞和证据路径见同目录 CSV。
