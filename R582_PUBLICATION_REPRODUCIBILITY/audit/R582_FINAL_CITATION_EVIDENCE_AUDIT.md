# R582 最终引文、证据与发布门禁审计

日期：2026-07-20  
审计模式：只读；未修改 `main_R582.tex`、`SI_R582.tex`、`refs.bib`、图件、实验原始文件或模型文件。  
机器可读明细：`manuscript/audit_R582/R582_FINAL_CITATION_EVIDENCE_AUDIT.csv`

## 结论

**科学内容与引文链：PASS。** 在冻结的 R582 科学源中，没有残留的缺失引用键、重复 BibTeX 键、重复 DOI、无 DOI 的已引期刊条目、引用占位符或实质性 claim-to-source 错配。此前发现的五个方法引用缺口、校准独立性表述、`R_theta`/`A_bare` 身份漂移、DFT 能量语义、COMSOL 流动设置、扫描范围与跨证据排名问题均已关闭。

**当前状态：SCIENTIFIC PACKAGE PASS；PUBLIC TAG + HUMAN METADATA PENDING。** 正文和 SI 已锁定目标 tag `r582-zifb-positive-electrode-reproducibility-v1` 的精确目录 URL，Data Availability 不再含 repository 占位符，并明确“不声称尚未签发的 DOI”。本地 R582-only 候选包与边界化 README 已建立且通过独立验证；尚未完成的是把批准的 commit/tag/release 真正发布并验证 URL，以及由作者本人提供作者、单位、CRediT、基金/致谢和披露元数据。

## 冻结快照

| 对象 | SHA-256 | 状态 |
|---|---|---|
| `manuscript/main_R582.tex` | `8AE9FF4F244E9D5AB2308D88E3B1E98BC5C9E946931F2CD7EF6A9CAA7D3E606D` | 当前权威科学/引用/发布源 |
| `manuscript/main_R582.pdf` | `5662806744E1B989808FDAD316F1C7C52433937048DDB129C4F291AB45CCCD1B` | 17 页；469,089 bytes；晚于 TeX；日志干净 |
| `manuscript/SI_R582.tex` | `8BDC18C71088398E0E9B1A55359FA3FDF688DE536B49C2C6C497EA34C47F6C1C` | 当前权威科学/引用/发布源 |
| `manuscript/SI_R582.pdf` | `67C3AB505395721303D691DE9EF75D2B82CD32FCA48C65C90D2DF343BC46B1DD` | 26 页；922,460 bytes；晚于 TeX；日志干净 |
| `manuscript/refs.bib` | `5CFD59B79994E43C90C0B1E5BFDB0002593C9343DA2E2526AC2BEB84C52B4D20` | 116 个唯一条目；无重复键/DOI |

编译日志搜索结果：正文与 SI 均无 undefined citation/reference、LaTeX/package warning、overfull/underfull box、missing character 或 oversized-float 警告。

## 引文完整性

| 指标 | 正文 | SI | 合并 |
|---|---:|---:|---:|
| citation-key occurrences | 45 | 25 | 70 |
| unique citation keys | 39 | 24 | 44 |
| missing BibTeX keys | 0 | 0 | 0 |

额外门禁：

- 116 个 BibTeX 键全部唯一；44 个已引条目全部有 DOI；全库无重复 DOI 组。
- 72 个未使用条目留在 `refs.bib`，但 `unsrtnat` 只输出实际引用项；这是可选清理项，不是引文失败。
- 修正 DOI 审计脚本的输入后，`CITATION_DOI_CROSSREF_AUDIT.json` 直接读取 `main_R582.tex`/`SI_R582.tex`；44 个当前已引键全部 PASS（WARN 0，FAIL 0）。
- 新增的五个严格方法键已单独核对 DOI、题名和年份：`Ehlert2021ALPB`、`Bussi2007VRescale`、`Bernetti2020CRescale`、`Essmann1995PME`、`Savitzky1964`。
- `Park2021` 已按出版方/KCI 记录核对；`Tichter2020` 已按 Refubium 官方记录核对。
- 未发现 `citation needed`、TODO/TBD citation 或空引用占位符。

## 外部文献对当前句子的支持

| 当前声明组 | 引用 | 判定 | 支持边界 |
|---|---|---|---|
| ZIFB 流动电池的发展背景 | `Li2015,Xie2018,Weng2017,Fan2024` | PASS | 四篇均承担 flow-battery 背景；不再把静态 Zn-I2 邻域论文混称 ZIFB 直接证据 |
| `I2/I-/I3-` 平衡及可溶聚碘表示 | `Palmer1984,Wen2025` | PASS | 当前句不再用 Palmer 支撑未测的络合速率 |
| 限域碳中固碘可保持可逆 | `SolidI2_NatCommun2020,Fitzek2023` | PASS | 明确保留 host-specific 边界；不外推到本 felt 形貌 |
| 致密碘膜与电荷转移阻力 | `Jang2021` | PASS | 当前表述为其他条件下的 film-associated interfacial resistance，不移植数值阈值 |
| 其他碘电池中的充/放电形貌变化 | `LiDualPlate2025` | PASS | 明确标注 different iodine cell，不作为本 felt 的形貌鉴定 |
| 多孔电极理论与 flow-cell 扩展 | `Newman1962,Tichter2020,Chakrabarti2020,AparicioMauricio2023` | PASS | 基础理论和流动电池扩展已拆层陈述 |
| 其他固体产物电极的建模/operando 邻域证据 | `LiS_ROM_JES2025,ZnO_EEM2024,Li2S_EcoMat2024` | PASS | 不再把实验论文统称为 models；仅支持面积/传输可受析出影响 |
| 碘化物络合系数的量级 | `Palmer1984` | PASS | `0.72 m3 mol-1 = 720 M-1` 是靠近 `698 +/- 10 M-1` 的条件先验，不称精确复现 |
| 溴化物络合系数与 I2Br- 先例 | `Lee2023,Park2021,Weng2017` | PASS | `0.0115 m3 mol-1 = 11.5 L mol-1` 靠近 Lee 的 12.2；Park/Weng 只承担形成先例，不承担该数值 |
| 稀水 I2 溶解度与 salting prior | `Ramette1965,Palmer1984` | PASS | `1.33 mol m-3` 是稀水参考；`gamma_salt=3` 是 2--4 跨盐先验，不称本电解液实测值 |
| CP2K/PBE/D3(BJ)/MOLOPT/GTH/counterpoise | `Kuhne2020CP2K,VandeVondele2005Quickstep,Perdew1996PBE,Grimme2010D3,Grimme2011D3BJ,VandeVondele2007MOLOPT,Goedecker1996GTH,Hartwigsen1998GTH,Krack2005GTHPBE,Boys1970Counterpoise` | PASS | 方法出处完整；论文仍把结果限定为有限干态计算而非溶液自由能/成核势垒 |
| GROMACS/SPC-E/离子参数/Packmol/ECC | `Abraham2015GROMACS,Berendsen1987SPCE,Joung2008Ions,Martinez2009Packmol,Leontyev2009ECC` | PASS | 标准方法引用不被用来验证项目特定 polyhalide analogue 参数 |
| GFN2-xTB 与 ALPB-water | `Bannwarth2019GFN2xTB,Ehlert2021ALPB` | PASS | 两个方法层引用已拆全；绝对 polyhalide 参数仍标高不确定性 |
| V-rescale、C-rescale、PME | `Bussi2007VRescale,Bernetti2020CRescale,Essmann1995PME` | PASS | SI 首次使用处均有原始方法引用 |
| Savitzky--Golay 导数 | `Savitzky1964` | PASS | 正文和 SI 均引用；窗口变化明确是 estimator sensitivity 而非置信区间 |
| 外部碘溶解动力学 | `Zhao2022` | PASS | 只作条件依赖的方向/尺度背景；不称本电解液的 sustainable-current ceiling |
| UV-vis / EIS 的可执行验证先例 | `ZnNC_AEL2025,WangNatCommun2025PSI,Jang2021` | PASS | 只提出 dissolved I3- 与界面阻抗的相关体系方案，不称已验证本模型内部状态 |

## 内部证据、软件与恒等式

| 审计对象 | 判定 | 直接证据与结论 |
|---|---|---|
| COMSOL 软件/物理接口 | PASS | `main_R582.tex:67` 给出 6.3.0.290、Tertiary Current Distribution/Nernst--Planck、Free and Porous Media Flow 及 porous-domain Darcian setting；构建脚本中的 `flowModelType="darcian"` 与其一致 |
| 规范分支身份 | PASS | `manuscript/notes/project_truth.md` 与 R581 closure manifest 锁定 `PB-R526-J40-Q120-DSET5-v1`、输入 MPH hash、`stdR522/sol5/dset5`；只在副本上重求 |
| 基线事件 | PASS | `Q_s=83.0202`、`Q_f,cal=99.5901 mAh cm-2` 与规范时序表一致；`Q_f,cal` 定义为 `<theta_cal>=0.5`，不是材料阈值 |
| 校准与实验 overlay | PASS | `main_R582.tex:58,133,143` 与 `SI_R582.tex:137-140` 已明确：导数 landmarks 未设置 Qs/Qf；Qf 来自预先存在的 voltage-calibrated branch；同一 full-cell record 另用于 S6 reduced fit，overlay 不是独立验证 |
| `R_theta` / native area 恒等式 | PASS | 正文 78--86 与 SI 348--361、927--930 一致：`R_theta=1-theta_cal`，`T_pore=sqrt(K/K0)`，`A_bare/A0=R_theta*T_pore`；Qf 只由 `<theta_cal>=0.5` 定义 |
| matched accessibility control | PASS | 7776-element、`rtol=3e-4` 对比给出 `Q_s=82.8903/82.8924`、终点 `1.7284/1.4402 V`、差值 `-288.156 mV`；只替换两个 accessibility expressions |
| DFT 数值语义 | PASS | 单 I2 数值已统一为 BSSE-corrected adsorption energies；两 I2 compact/separated 仍作为独立 electronic-energy diagnostic；图 5、SI Table、SI Fig. S7 文本同步 |
| CP2K 版本 | PASS | SI 指明 CP2K/Quickstep 2026.1；原始输出头部支持该版本 |
| MD 软件、轨迹和不确定性 | PASS | SI 指明 GROMACS 2026.0-conda_forge；每 SOC/电荷参数化仅一条 20 ns trajectory；四个 5 ns block 仅为 within-trajectory stability，不称 replicas/SEM |
| MD 拓扑本地完整性 | PASS-LOCAL | `MD/workspace_mirror/outputs/md_transport_soc_series/inputs/soc_series/` 含逐 case `topol.top`、ITP、MDP、分子文件及 hash manifest；需复制进最终公开 release |
| single-fibre 身份 | PASS | 主图 5c 与 SI S11 均标几何 `A/A0`；与 native `A_bare/A0=R_theta*T_pore` 和 reduced `R_theta` comparator 明确分离 |
| pore-network 身份 | PASS | `K/K0=0.981--0.992` 只承担当前载量下的 smooth bulk permeability bound；不排除局部 pore-throat blockage |
| 电流扫描范围 | PASS | 20/40 mA cm-2 为 Q=120 完整轨迹；80/120 为 Q=40 固定窗，80 仅报 `Q_s>40`，120 在 `8.391` 穿越；图/文未插值被删失点 |
| 灵敏度排名 | PASS | 主文只说 selected operating-variable comparison；SI 明示 `gamma_salt=2--4` 总 span 更大但属于 E-LIT/PRES prior，不跨不同证据类型做统一排名 |
| smooth-permeability voltage | PASS | 终点差 `+1.271 mV` 与窗口内最大绝对差 `5.214 mV` 分开报告 |
| NH4Cl -> NH4Br | PASS | 正文 60、SI 97--99 是唯一两个 active-TeX `NH4Cl` token；均声明 EXP-META-001、原始名称/字节/hash 不变；19 个 active figure PDF 中无 NH4Cl |
| 论文主角层级 | PASS | 标题、摘要、结论和全部主图以 ZIFB porous positive electrode 为核心；NH4Br 仅是 representative supporting electrolyte/ligand，没有优化或通用定律主张 |

## 图件与字体门禁

冻结稿引用 6 幅主图和 13 幅 SI 图。所有 19 幅 active PDF 以及正文/SI PDF 均通过 `check_font_consistency.py`：

- TeX Gyre Termes 正文字体存在；
- 无 Arial、Helvetica、DejaVu、Liberation、Calibri 等回退族；
- 无 Type 3 字体；
- 图 5c 显式为 geometric `A/A0`；
- SI Fig. S7 显式为 relative BSSE-corrected adsorption energy；
- SI Fig. S11 把 geometric `A/A0`、`R_theta` comparator 与 native `A_bare/A0` 分开；
- active figures 中没有 NH4Cl。

完整 21-PDF 机器可读记录已固化为 `R582_FINAL_FONT_GATE.json`（21 records，`failures=[]`；SHA-256 `0284E505C719A62AB0E0FE45A13A57E055D6E91F302EA236A82F9A5F775B6753`）。脚本同时强制 2 份活动文稿 PDF、19 幅活动图和 21 条总记录的非空计数；在原项目与公开包两种目录布局下均不得空集通过，且报告路径采用布局无关的相对路径。

`check_r582_language_and_format.py` 的 hard failures 为 0；摘要 187 词，主图 6 幅，关键词 7 个，含 TeX 前后文的近似正文词数为 5,324。

Data Availability 的最终变更页也已单独检查：正文第 13--14 页及 SI 第 24 页以 160 dpi 重渲染，无裁切、重叠、缺字或异常 URL 换行；PDF annotation 指向同一个精确 tagged-directory URL。

## 发布阶段剩余项（不是科学失败）

| ID | 严重度 | 位置/现状 | 投稿前动作 |
|---|---|---|---|
| REL-001 | PLANNED-FOR-TAG | `main_R582.tex:276` 与 `SI_R582.tex:974` 已嵌入精确目标 URL；repository 占位符为 0，且未虚构 DOI | 发布 tag 后从未登录环境打开该 URL，核对 commit/tree；若无真实 DOI，保留当前无 DOI 陈述 |
| REL-002 | PUBLICATION GATE | 本地根 README 已改为 R582 的有界结论，R582-only 候选目录已建立；远端尚无目标 tag/release | 审核 commit 后 push/merge，创建并发布 `r582-zifb-positive-electrode-reproducibility-v1`，确认 release/tag 可公开解析且不可变 |
| REL-003 | BLOCKER | `main_R582.tex:26-27,279,282` 为作者/单位、CRediT、基金致谢占位符 | 由作者核准后填写；这是 human-only metadata，不由模型推断 |
| REL-004 | LOCAL PASS / TAG PENDING | 本地候选包含 6+13 active figures、17 个 source/QA bundles、renderer/manifest 及 EXP-META-001；独立 verifier 通过 | 将刷新后的审计文件重建进候选后再次验证，再随批准 commit/tag 发布 |
| REL-005 | LOCAL PASS / TAG PENDING | 本地候选含 34 条采用的 single-I2 CP2K input/output/geometry identity records；无越权的溶液自由能或成核声称 | 发布后从 tag 清单复核记录数、版本与哈希 |
| REL-006 | LOCAL PASS / TAG PENDING | 本地候选含十个 SOC/charge cases 的精确 topology/ITP/MDP/protocol/metadata/log identities | 发布后从 clean download 重跑 manifest 与代表性分析检查 |
| REL-007 | LOCAL PASS / TAG PENDING | COMSOL 原始 `.mph` 未进入轻量仓储；输入 hash、6.3.0.290、study/solution/dataset、脚本/导出/访问边界已打包 | 发布后验证公开 access note 和哈希；原始 `.mph` 继续不可变且不移动 |
| REL-008 | CURRENT SNAPSHOT PASS | Data Availability 更新后 main/SI 已重编、重哈希，并重跑 citation/log/freshness/font/caption/hyperlink 门禁 | 若随后填写作者或披露元数据，必须再次重编与重锁；不得移动已发布的不可变 tag，必要时发布新版本 tag |

## 最终判定

在上述 frozen science snapshot 上：

- **引用键与 DOI 元数据：PASS**
- **句级文献支持：PASS**
- **内部数值与身份：PASS**
- **NH4Br 更正与主角层级：PASS**
- **`R_theta` / `A_bare` / DFT 语义：PASS**
- **字体与编译：PASS**
- **目标 tag URL 已写入且本地候选内容门禁：PASS / PLANNED-FOR-TAG**
- **远端不可变 tag/release：PENDING PUBLICATION**
- **作者与披露元数据：PENDING / HUMAN-ONLY SUBMISSION BLOCKER**

因此，本审计没有要求再次修改科学正文或图件。发布阶段只需冻结并验证已写入的 tag 身份；作者元数据只能由作者核准。任何后续 TeX 改动都必须触发机械复编、caption 同步、引用/字体/链接门禁与新哈希记录。
