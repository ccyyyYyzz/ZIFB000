# Local iodine-handling failure in porous carbon-felt electrodes drives solid-iodine blockage in zinc-iodine flow batteries

**Article type:** Research Paper

**Authors:** [Author names]

**Affiliations:** [Author affiliations]

**Corresponding author:** [Name and email]

## Abstract

Zinc-iodine flow batteries combine high aqueous iodine capacity with a distinctive failure risk: neutral iodine can leave the soluble redox pool and become a solid foulant in porous positive carbon felt. We formulate this transition as a local iodine-handling failure. The governing state is not total iodine inventory in the tank, but the fiber-scale balance between neutral iodine generation and local removal by complexation, diffusion, flow renewal, dissolution and accessible carbon surface. Molecular surface calculations provide bounded priors for iodine residence near graphitic and oxygenated motifs. A radial single-fiber model converts local precipitation into closures for surface accessibility, iodine-film attenuation, precipitation/dissolution and bare/covered current partition. Porous-electrode postprocessing then shows two routes to the same failure chain: capacity-oriented operation accumulates solid iodine inventory and surface-state loss, whereas rate-oriented operation first produces high free-I2 supersaturation. Spatial fields show broad iodine stress, implying that visible clumps and pressure symptoms arise from localization or pore-throat amplification rather than uniform mean porosity loss. The framework yields testable coordinates for iodine failure and clarifies which experiments are needed to make blockage predictable.

**Keywords:** zinc-iodine flow battery; iodine precipitation; carbon felt; local supersaturation; single-fiber model; COMSOL; porous electrode; flow blockage

## 1 Introduction

Redox flow batteries are attractive for long-duration storage because they separate power conversion from tank-scale energy capacity and allow aqueous, serviceable cell architectures [1-3]. Within this broad family, zinc-iodine chemistry is especially attractive because iodine-rich electrolytes can support high energy density while zinc remains inexpensive and abundant. High-energy zinc-polyiodide operation was demonstrated with ambipolar electrolyte chemistry [4]. Subsequent work showed that polyiodide and bromide complexation can unlock iodide capacity [5], that self-healing and single-flow architectures can extend cycle life [6,7], that iodine redox chemistry and modified carbon electrodes can improve practical operation [8,9], and that high-voltage or dendrite-suppressed Zn-I systems are possible with additional ion-management strategies [10]. Degradation studies further show that excessive charging can produce coupled chemical, electrochemical and transport failure in Zn-I cells [11]. In parallel, porous-electrode optimization, iodine-equilibrium measurements and redox-flow electrode modelling have clarified how electrode structure, compression, active area, transport length and electrolyte speciation affect flow-cell performance [12-18]. More recent complexation and ion-interception strategies continue to improve iodine utilization and cycle life [19,20].

These advances make the Zn-I system technologically compelling, but they also expose a distinctive failure problem. Iodine is not only a soluble redox carrier. During charge it passes through neutral I2, polyiodide and mixed-halide species; it can reside near carbon surfaces; it can cross a free-I2 saturation boundary; and it can form solid deposits that cover fibers, bridge pore throats or enter poorly renewed regions of the felt. Practical observations of dark solid iodine, clumps, flow obstruction, pressure rise and pump-line failure therefore point to a physical conversion of iodine from mobile redox inventory into a local solid/morphology state.

We therefore formulate iodine failure in a Zn-I flow battery as a local iodine-handling failure of the porous positive carbon felt. The tank can remain chemically buffered while the fiber-scale interface crosses a free-I2 supersaturation boundary. At that interface, current generates neutral iodine at a flux proportional to the local current density. Removal is supplied by complexation, diffusion, flow renewal, dissolution and the still-accessible carbon surface. When the source exceeds the local handling capacity, the relevant state variables are free-I2 supersaturation, cumulative supersaturation dose, solid iodine inventory, surface accessibility, film attenuation and localization.

This framing separates three effects that are often conflated. Global electrolyte composition determines the reservoir available to the cell, but it does not guarantee a low local free-I2 activity at a reacting fiber. A resistive surface layer, if present, is only one consequence of deposition; coverage, precipitation/dissolution and bare/covered current partition are separate links. Full-cell voltage is also a mixed observable, combining open-circuit potential, zinc-side polarization, membrane/electrolyte resistance, terminal concentration polarization and positive-electrode iodine loss. The mechanism must therefore follow iodine from molecular residence to fiber-scale precipitation, porous-electrode fields and morphology-scale blockage.

Carbon felt amplifies the importance of locality. Compression, permeability, tortuosity, wetting, active area and flow distribution determine where reaction occurs and how quickly species are renewed. In a Zn-I positive felt these structural variables also determine where neutral iodine first forms, how long it remains near carbon, where solid iodine can nucleate, and whether a small mean solid fraction becomes harmlessly distributed or dangerously localized. This is why a continuum field and a visible clump should not be treated as contradictory: they describe different levels of the same chain.

We build the mechanism with three connected modelling levels and one interpretation layer. First, molecular surface calculations test whether iodine residence near representative carbon motifs is chemically plausible. These calculations are used only as bounded surface priors, not as fitted macroscopic kinetic constants. Second, a standalone single-fiber model resolves radial transport, fast complexation, surface generation/consumption, precipitation/dissolution, coverage and local film attenuation. This model exports closures rather than replacing the porous-electrode model with a black-box voltage term. Third, COMSOL porous-electrode postprocessing maps the local state variables under capacity- and rate-oriented operation. Finally, mean-field versus localized-blockage analysis explains why hydraulic symptoms require morphology amplification beyond a uniform mean porosity loss.

The contribution is a mechanism framework rather than an optimization recipe, and it is written for the engineering question of how a porous positive electrode can fail even when the bulk electrolyte remains chemically competent. It identifies where each parameter family enters the iodine-failure chain: accessible carbon area changes the local source term, flow and diffusivity change removal, speciation and saturation move the free-I2 gate, precipitation and dissolution control solid inventory and recovery, compression and localization control hydraulic amplification, and ASR controls voltage loss without necessarily changing iodine phase stability. This chain provides a cleaner basis for experiments and design decisions than a single empirical failure threshold.

![Fig1_R67_local_iodine_failure_framework.png](figures/Fig1_R67_local_iodine_failure_framework.png)

**Figure 1. Local iodine-handling failure in porous positive carbon felt.** The reservoir can remain chemically buffered while the positive felt fails locally. Electrochemical current generates free iodine at fiber surfaces, and the balance among complexation, diffusion, flow renewal, dissolution and accessible carbon surface determines whether that iodine remains mobile or crosses a saturation boundary. Persistent supersaturation drives solid iodine inventory, closure-derived surface accessibility loss, film attenuation and morphology-scale clumping.

## 2 Results

### 2.1 Local iodine-handling coordinates define the failure state

The mechanism begins by choosing the correct state coordinate. In the reservoir, total iodine, iodide and supporting halide concentrations describe chemical storage capacity. At the positive carbon surface, the relevant quantity is the local source-removal balance. Charging generates neutral iodine at a fiber-scale flux J_gen = j_loc/(2F), where j_loc is the local interfacial current density and F is Faraday's constant. A compact removal scale is J_rem = k_m,eff beta_eff c_I2,sat,eff, where k_m,eff groups diffusion, pore-scale renewal and convective exchange, beta_eff expresses rapid buffering of free iodine into soluble complexes, and c_I2,sat,eff is the effective free-I2 saturation concentration at the local surface.

These quantities define the local iodine-handling number Da_I2 = J_gen/J_rem. The phase-forming species is free iodine rather than total dissolved iodine, so the saturation coordinate is S_I2 = c_I2,free,local/c_I2,sat,eff. Long-duration charging is captured by the cumulative supersaturation dose Omega_I2 = integral max(S_I2 - S_on, 0) dt. This coordinate set explains the iodine paradox: a formulation can contain a large total iodine inventory and still fail locally if the positive felt generates free iodine faster than it can be complexed, transported, dissolved or distributed over accessible surface. Conversely, a lower total iodine loading can remain stable if active area, flow renewal and local speciation keep S_I2 below the precipitation boundary.

**Table 1. Local iodine-handling variables used in the framework.**

| Quantity | Definition | Physical meaning |
|---|---|---|
| J_gen | j_loc/(2F) | Fiber-scale neutral-iodine source flux |
| J_rem | k_m,eff beta_eff c_I2,sat,eff | Local removal by transport, complexation and dissolution |
| Da_I2 | J_gen/J_rem | Instantaneous iodine-handling stress |
| S_I2 | c_I2,free,local/c_I2,sat,eff | Local free-I2 saturation coordinate |
| Omega_I2 | integral max(S_I2 - S_on, 0) dt | Cumulative supersaturation dose |
| eps_s | solid iodine volume fraction | Mean solid inventory in the continuum model |
| eps_s,local | eps_s,mean/f_local | Localized solid loading relevant to pore-throat obstruction |
| theta | 1 - exp(-a_theta h_I2^b_theta) | Closure-derived surface accessibility state |
| f_film | 1/(1 + g_eff R_film) | Covered-path kinetic attenuation factor |

Table 1 is used as a mechanism map rather than a fitting table. The source term, removal term, phase gate, cumulative dose, solid inventory, surface state and morphology amplification are treated as separate links, which prevents every late voltage rise, pressure symptom or cycle fade from being collapsed into a single generic iodine-film term.

### 2.2 Molecular surface calculations justify residence, not macroscopic rates

The first modelling level asks whether iodine has a plausible tendency to reside near carbon surfaces (Figure 2). Finite carbon motifs cannot represent a compressed, flowing carbon felt, but they can provide a bounded prior for local residence and nucleation tendency. In the final molecular prior set, neutral I2 on a basal graphitic motif has an adsorption energy of about -0.51 eV, or -49.6 kJ mol-1. Hydroxylated basal motifs are only modestly more iodine-philic than basal carbon, by about 0.039 eV, corresponding to a conservative site-preference factor of 1.5. Carbonyl-edge motifs are weaker still, about 0.016 eV relative to basal, and are retained only as a weak sensitivity prior.

The important conclusion from Figure 2 is not that one functional group uniquely controls the battery. The molecular result says something narrower and more useful: iodine residence near carbon is chemically plausible, modest surface heterogeneity can bias where iodine first resides, and patchy nucleation is therefore a reasonable physical assumption. It does not determine precipitation rates, film conductivity, surface area loss or pressure rise. Those quantities belong to the fiber, porous-electrode and morphology levels.

This restricted use of molecular information is deliberate. A finite motif calculation cannot set a full-cell failure threshold, but it can establish whether iodine residence near carbon is chemically plausible. The fiber and porous-electrode models then determine how this residence participates in precipitation and transport.

![SI_Fig_molecular_surface_evidence_R64.png](figures/SI_Fig_molecular_surface_evidence_R64.png)

**Figure 2. Molecular surface prior for iodine residence on carbon motifs.** Finite graphitic and oxygenated carbon motifs are used only to bound the plausibility and relative strength of local I2 residence. The molecular layer supports patchy residence and nucleation as chemically reasonable, but it is not used to fit full-cell voltage, precipitation rate constants, film conductivity or pore-blockage thresholds.

### 2.3 The single-fiber model turns surface deposition into portable closures

The second modelling level is the radial single-fiber model. It solves a local problem that the macroscopic model needs but cannot infer from voltage alone: how free-I2 transport, precipitation, dissolution, coverage and film attenuation evolve around a single carbon fiber.

Fast complexation is represented by beta_I2 = 1 + K_I2,I c_I- + K_I2,Br c_Br,support, with c_I2,free = c_I2,total/beta_I2. At the fiber surface, the electrochemical reaction I2 + 2e- <-> 2I- supplies or consumes iodine. The model then updates solid iodine thickness h_I2, surface coverage theta = 1 - exp(-a_theta h_I2^b_theta), local film resistance R_film = h_I2/sigma_I2, covered-path attenuation f_film = 1/(1 + g_eff R_film), and the current split j_total = j_bare + j_cov.

Figure 3 shows the resulting closure structure. The upper-left panel shows that coverage is a nonlinear accessibility state: small deposits can quickly change the usable fraction of a surface, while later deposits approach a plateau. The upper-right panel shows that local film attenuation can be represented as a compact algebraic factor, separating it from coverage. The lower-left panel shows why bare/covered parallel pathways are needed: current does not simply vanish when a surface becomes partly covered, but the accessible current pathway shifts. The lower-right panel shows the precipitation/dissolution boundary: precipitation responds to supersaturation, while dissolution requires both undersaturation and existing solid/covered state.

The closure scan contains 720 single-fiber rows and is summarized in Figure 3. For initially bare fibers, theta(h_I2) is described by a_theta = 4.04e+06 m^(-b) and b_theta = 1.018, with R^2 = 0.80. The film attenuation fit gives g_eff = 40.00 S m-2 with a numerical RMSE of 3.46 x 10^-9. The retained precipitation and dissolution coefficients are k_precip = 1.0 x 10^-6 m s-1 and k_diss = 2.0 x 10^-6 m s-1. The pathway prefactors are j0,bare = 15.0 A m-2 and j0,cov = 2.0 A m-2, and the current-split expression reproduces the scan with RMSE below 6.3 x 10^-10 in fractional current.

These values should be interpreted as closure parameters for a local mechanism model, not as universal material constants. The important advance is the separation of links. Precipitation/dissolution, surface accessibility, local film attenuation and current redistribution are exported as distinct quantities. This separation makes the later COMSOL interpretation readable: when a field shows rising theta, it means closure-derived accessibility loss; when it shows rising R_film, it means a local covered-path penalty; and when it shows a current split, it means the model has moved current from bare to covered surface rather than hidden the effect in one voltage residual.

![Fig2_single_fiber_closure_bridge_R64.png](figures/Fig2_single_fiber_closure_bridge_R64.png)

**Figure 3. Single-fiber bridge from local precipitation to porous-electrode closures.** The radial fiber calculation resolves free-I2 transport, fast complexation, electrochemical generation/consumption, precipitation/dissolution and local solid iodine thickness. Its outputs are converted into separate closures for theta(h_I2), R_film, film kinetic attenuation and bare/covered current split.

### 2.4 Time-resolved COMSOL states separate capacity and rate routes

The third modelling level asks how the closure variables behave in porous-electrode operation. Figure 4 is the central result because it shows state evolution, not just endpoints. The capacity-oriented route and rate-oriented route load the same iodine-failure chain in different order.

In the capacity-oriented route, the most important signature is delayed coupling among solid iodine inventory, coverage-derived accessibility loss, local film resistance and area-loss proxy. The free-I2 supersaturation proxy remains comparatively lower than in the rate case, but the solid inventory grows with charge progress. Once inventory has accumulated, theta and the area-loss proxy rise sharply. This pattern is the fingerprint of a cumulative-dose route: the system is not failing because the instantaneous source term is always extreme; it is failing because the integral of supersaturation exposure and solid persistence eventually changes the surface state.

In the rate-oriented route, the free-I2 supersaturation proxy is already high early in the charge. The red curve in the supersaturation panel is therefore the clearest sign of source-removal imbalance. It indicates that J_gen has exceeded J_rem before the same magnitude of mean solid inventory and closure-derived area loss develops. This is why high-rate operation can seed failure quickly even when the total charged capacity is lower: the local interface crosses the free-I2 gate first, and the solid/morphology consequences follow later.

The state ordering also defines the claim boundary. The rate route is a high-supersaturation route rather than a resolved single mesh hotspot. The capacity route is a closure-derived surface-state route rather than a direct measurement of surface coverage. Within those boundaries, the simulation establishes that capacity and rate load the iodine-failure chain in different order.

This ordering leads to testable predictions. If the rate route is correct, increasing flow renewal, improving current distribution or increasing accessible area should suppress early S_I2 more efficiently than merely increasing tank capacity. If the capacity route is correct, interrupted-charge dissolution, rest history, phase imaging and accessible-area recovery should strongly influence late solid inventory and surface-state loss. These route-specific predictions make the model falsifiable rather than merely descriptive.

![Fig3_R69_COMSOL_state_evolution.png](figures/Fig3_R69_COMSOL_state_evolution.png)

**Figure 4. Time-resolved state variables separate capacity and rate routes.** Capacity-oriented operation produces delayed growth of solid iodine inventory, closure-derived coverage, film proxy and area-loss proxy, indicating cumulative supersaturation dose and surface-state persistence. Rate-oriented operation produces early free-I2 supersaturation before comparable mean solid inventory develops, indicating an instantaneous generation/removal imbalance. The key result is the ordering of physical state variables across the two routes.

### 2.5 Spatial fields move the hydraulic question from mean field to morphology

The spatial COMSOL fields provide a second important constraint: the iodine-stress pattern is broad across the positive electrode rather than concentrated into one dominant resolved continuum point. This matters because visible clumps and pressure symptoms are localized phenomena. If the continuum model does not show a sharp hotspot, the correct conclusion is not that clumps are impossible. The correct conclusion is that clumps are produced by a morphology-amplification layer that the mean-field model does not fully resolve.

A uniform solid iodine volume fraction changes porosity and permeability only through a smooth mean-field pathway. For small eps_s,mean, a Kozeny-Carman-like permeability estimate may change only modestly. But if the same solid inventory localizes into a fraction f_local of the active pore space, the local solid fraction becomes

eps_s,local = eps_s,mean/f_local.    (11)

This relation is simple but powerful. A mean inventory of 0.1% is hydraulically mild if distributed everywhere, but it becomes a local 10% obstruction if concentrated into 1% of the pore space. In a fibrous felt, such localization can occur at stagnant pockets, fiber crossings, binder-like debris, compression-induced dead zones or pore throats with slow renewal. The pressure event is then a morphology consequence of local solid arrangement, not only a volume-average porosity loss.

Figure 5 therefore connects model-resolved fields to model-implied morphology. The COMSOL fields resolve broad iodine stress and axial/state gradients. They do not fully resolve nucleation heterogeneity, agglomeration, detachment, particle bridging or slurry-like motion. These processes define the next model layer required for quantitative pressure prediction.

![Fig4_COMSOL_axis_profile_fields_R64.png](figures/Fig4_COMSOL_axis_profile_fields_R64.png)

**Figure 5. Spatial iodine-state fields and morphology amplification.** Coordinate-aware COMSOL fields show broad positive-electrode iodine stress rather than a single resolved continuum hotspot. Visible clumps, pore-throat obstruction and pressure symptoms are therefore interpreted as morphology-amplified consequences of local solid iodine inventory.

### 2.6 Parameter effects must be argued by physical entry point

Parameter effects are most informative when organized by physical entry point. Each parameter family enters a different equation, produces a different tradeoff and points to a different experiment. Figure 6 therefore presents a mechanism matrix rather than an optimization chart.

#### 2.6.1 Accessible carbon area: source dilution and surface inventory distribution

Accessible carbon area acts first on J_gen. For a fixed stack current, increasing the effective active surface lowers j_loc and therefore lowers the local neutral-iodine source flux j_loc/(2F). It also distributes any solid iodine over more surface, delaying local coverage and preserving a larger bare-current fraction. Conversely, poor wetting, compression dead zones, partial felt utilization or blocked flow paths concentrate current into fewer active regions. The nominal current density can then look safe while the true local j_loc is high.

Accessible area is therefore more than a kinetic prefactor. It is a source-distribution variable. A decisive experiment would compare identical electrolyte and current at different controlled wetting/compression states, then measure whether the early S_I2 proxy, phase appearance or pressure onset shifts as predicted. If only voltage is measured, area effects may be confused with ASR or activation.

#### 2.6.2 Flow renewal and diffusivity: removal rather than chemistry

Flow renewal and effective diffusivity act on k_m,eff in J_rem. Their role is to remove newly generated iodine from the fiber-scale environment before free-I2 activity crosses the saturation boundary. This is physically different from changing iodide or bromide concentration. Flow and diffusivity do not primarily change how much iodine the tank can store; they change how quickly the interfacial region can shed the iodine it just produced.

This distinction predicts that rate-driven failure should be highly sensitive to flow renewal and local transport length. If early supersaturation is caused by generation-removal imbalance, increasing flow or improving pore connectivity should suppress the red high-S_I2 signature in Figure 4 more efficiently than it suppresses late cumulative inventory after long capacity loading. That is a falsifiable route-specific prediction.

#### 2.6.3 Speciation and saturation: moving the free-I2 gate

Speciation and free-I2 saturation act at the phase gate. Iodide and bromide complexation reduce c_I2,free at fixed total iodine, while c_I2,sat,eff determines where precipitation begins. This is the correct scientific place to discuss NH4Br or related additives. They are not the thesis of the paper; they are one way to move the free-I2 gate.

The tradeoff is subtle. Strong complexation can suppress free iodine and delay precipitation, but it cannot eliminate local source intensity, slow flow renewal, stagnant zones or nucleation heterogeneity. A formulation with excellent total iodine buffering can still fail if a carbon-felt region crosses S_I2 > 1. Conversely, a formulation with less total buffering might operate safely if local current density is low and renewal is high. For this reason, additive chemistry is treated here as one physical control of the free-I2 gate rather than as the central optimization target.

#### 2.6.4 Precipitation and dissolution: reversible buffer or persistent foulant

Precipitation and dissolution control the conversion between free iodine and solid inventory. Faster precipitation can reduce free-I2 activity by moving iodine into a solid reservoir, but it can also increase eps_s, coverage and blockage risk. Slower precipitation can keep more iodine in solution, which may reduce solid inventory but increase local free-I2 activity and reaction stress. Dissolution controls whether a solid deposit is reversible during rest or discharge.

The same parameter can therefore look beneficial or harmful depending on the observable. If the observable is free-I2 activity, precipitation can appear protective. If the observable is pressure or coverage, precipitation can appear damaging. The relevant question is therefore not whether precipitation is simply beneficial or harmful, but whether solid iodine remains reversible, distributed and dissolvable, or becomes localized and persistent.

#### 2.6.5 Compression, permeability and localization: the hydraulic amplification layer

Compression improves electronic contact and may increase apparent active area, but it reduces pore volume, modifies permeability and makes local obstruction more dangerous. This is the entry point for hydraulic failure. Uniform eps_s,mean alone is usually insufficient to explain abrupt pump symptoms; localization converts the same inventory into much larger eps_s,local. Compression lowers the tolerance for that localization by shrinking pore throats and increasing pressure sensitivity.

This is also where a future pore-network or precipitation-permeability model is required. The present model supports the physical route from supersaturation to solid inventory and from solid inventory to localization risk. It does not assign a numerical pressure cutoff.

#### 2.6.6 Conductivity, membrane resistance and ASR: voltage loss is not phase stability

Ohmic resistance, membrane resistance and electrolyte conductivity determine the voltage penalty for a given current. They are technologically important, but they are not the same as iodine phase stability. A low-ASR cell can still precipitate iodine if J_gen exceeds J_rem. A high-ASR cell can show poor voltage efficiency without solid iodine being the primary cause. Therefore voltage loss must be separated from iodine-handling failure in both modelling and interpretation.

This separation explains why archived full-cell curves are not used as microscopic proof. Voltage is an observable mixture. It can be consistent with the iodine mechanism, but it cannot by itself identify coverage, film or pore blockage without reference electrodes, pressure data, phase imaging or controlled perturbations.

![Fig5_R67_parameter_mechanism_matrix.png](figures/Fig5_R67_parameter_mechanism_matrix.png)

**Figure 6. Parameter-family mechanism map.** Parameter families are grouped by the link they control in the iodine-failure chain: local generation, transport renewal, free-I2 gate, phase conversion, localization/permeability or voltage loss. The map is a reasoning scaffold for interpreting interventions; a parameter is important because of where it enters the chain and what tradeoff it creates.

### 2.7 Mechanism synthesis: what the model explains and what remains open

The full mechanism can now be written in one chain. Local current generates free iodine. If local complexation, diffusion, flow renewal, dissolution and accessible area cannot remove it, free-I2 supersaturation appears. If the supersaturation is sustained, solid iodine inventory accumulates. Solid iodine changes the surface through closure-derived accessibility loss and film attenuation, and it changes the current distribution through bare/covered pathways. If the inventory remains broadly distributed, the hydraulic effect may remain mild. If it localizes, agglomerates or bridges pore throats, a modest mean solid fraction can create visible clumps and pressure symptoms.

This chain explains why capacity and rate routes are different but connected. Capacity loads the integral Omega_I2 and therefore drives solid inventory and surface-state persistence. Rate loads J_gen/J_rem and therefore drives early free-I2 supersaturation. A practical cell can experience either route or both. The same framework also explains why a post-failure cell is difficult to interpret: once flow obstruction, pressure rise, local dry-out or uncontrolled clumping occurs, voltage curves and EIS no longer isolate the initial onset mechanism.

The model-supported conclusions are therefore deliberately precise. The simulations establish a local iodine-handling chain, separate capacity and rate routes, provide portable single-fiber closures and show that continuum iodine stress must be interpreted with a morphology/localization layer. Quantitative validation of true surface coverage, local pressure threshold and clump hydrodynamics remains an experimental and modelling priority.

## 3 Discussion

### 3.1 Local iodine handling as the organizing principle

The main conclusion is that iodine failure in Zn-I flow batteries is governed by local iodine handling inside the positive carbon felt. This principle is more general than a particular salt, felt treatment or voltage trace. It says that iodine remains useful when free-I2 generation, buffering, transport renewal, dissolution and surface accessibility remain balanced. It becomes a failure source when that balance is lost locally.

This view explains why bulk chemistry can be simultaneously necessary and insufficient. Iodide, bromide and polyiodide equilibria determine the chemical ability of the electrolyte to store iodine. But the positive felt determines how the reaction sees that chemistry locally. A high-capacity electrolyte can still fail at a fiber interface; a lower-capacity electrolyte can be stable if local source-removal balance is maintained.

### 3.2 Why capacity and rate should be treated as two routes

Capacity and rate should not be collapsed into one empirical severity axis. Capacity-oriented operation emphasizes time-integrated exposure and solid persistence. The associated observables are Omega_I2, eps_s, theta, R_film and accessible-area loss. Rate-oriented operation emphasizes instantaneous source strength. The associated observables are J_gen/J_rem and early S_I2. This distinction suggests different mitigation strategies. Capacity problems require reversible deposition, dissolution and inventory management; rate problems require better renewal, lower local current density and improved current distribution.

### 3.3 What the molecular and single-fiber levels add

The molecular calculations add chemical plausibility: iodine can reside near carbon motifs, and modest surface heterogeneity can bias where iodine first accumulates. The single-fiber model adds closure structure: it translates local deposition into coverage, film attenuation, precipitation/dissolution and current split without fitting a full-cell voltage. These two levels are the reason the COMSOL variables have physical meaning. Without them, theta and R_film would be arbitrary internal variables. With them, they are explicitly defined, portable closure states whose limitations can be stated.

### 3.4 Why hydraulic failure is a morphology problem

Visible clumps and pressure rise are not explained by uniform mean solid iodine alone. The model identifies broad iodine stress and mean solid inventory, but pressure symptoms require localization, agglomeration or pore-throat bridging. This is not a contradiction; it is a hierarchy. Continuum simulation predicts where iodine stress and solid inventory become possible. Morphology determines how that inventory is arranged in the pore network. The next model generation should therefore couple precipitation to permeability and pore accessibility rather than only refine voltage fits.

### 3.5 Evidence boundary and future falsification

The framework is intentionally conservative about evidence. Visible iodine, clumps and pressure symptoms are qualitative physical anchors. COMSOL and the single-fiber model support a mechanistic chain. Direct phase imaging, pressure traces, interrupted-charge recovery, Raman or optical identification, Cdl/area tracking and reference-electrode measurements are needed to convert the chain into quantitative validation.

Several falsification tests are straightforward. If rate-driven failure is controlled by generation-removal imbalance, flow renewal and active-area distribution should shift early S_I2 and onset more strongly than they shift late capacity inventory. If capacity-driven failure is controlled by solid persistence, rest/dissolution protocols and interrupted-charge imaging should change eps_s and theta-derived accessibility more strongly than they change early supersaturation. If hydraulic symptoms are controlled by localization, pressure rise should correlate with visible or tomographic clump localization more strongly than with mean solid inventory alone.

### 3.6 Implications for design without making an optimization claim

The practical implication is a mechanism checklist rather than a finalized NH4Br recipe, best-felt claim or production operating map. A successful Zn-I positive electrode should spread current over accessible carbon area, renew the fiber-scale environment, buffer free iodine without hiding local supersaturation, keep solid iodine reversible and distributed, avoid pore-throat localization, and maintain voltage efficiency without conflating ohmic loss with phase failure. This checklist can compare additives, membranes, felts, compression states and flow fields after each intervention is assigned to the physical link it controls.

## 4 Materials and methods

### 4.1 Study design and evidence hierarchy

The study was designed as a mechanism-oriented modelling article. The central question was not whether a particular full-cell voltage trace could be fitted, but how iodine changes state from a soluble redox species to a solid, surface-covering and morphology-amplifying foulant in a porous positive carbon felt. Evidence was therefore organized by physical scale. Molecular calculations supplied bounded priors for iodine residence near carbon motifs. The single-fiber model supplied local precipitation, dissolution, coverage and film-attenuation closures. COMSOL porous-electrode fields supplied spatial and time-resolved state variables under capacity-oriented and rate-oriented operation. Mean-field versus localized-blockage analysis connected continuum solid inventory to the possibility of pore-throat obstruction. Archived full-cell voltage and EIS records were not used as microscopic proof of surface coverage, film growth or pressure blockage because those observables mix multiple cell-level processes.

### 4.2 Molecular surface calculations

Finite carbon motifs were used to test whether iodine residence near carbon is chemically plausible. A basal graphitic motif was used as the reference surface. Hydroxylated basal and carbonyl-edge motifs represented common oxygenated environments on carbon felt. Iodine adsorption energies were interpreted only as local residence priors and relative site-bias indicators. They were not converted into macroscopic precipitation rates, film conductivities or active-area loss parameters. This restriction is important because a finite molecular motif does not represent electrolyte renewal, pore-scale residence time, compression or agglomeration in a working felt.

### 4.3 Single-fiber iodine precipitation and coverage model

The single-fiber model represents one carbon fiber surrounded by a radial diffusion layer. The model solves for iodide and total molecular iodine in cylindrical coordinates with fast complexation written as c_I2,free = c_I2,total/beta_I2, where beta_I2 accounts for iodide and bromide-supported soluble iodine complexes. At the fiber surface, positive applied current corresponds to iodide oxidation and molecular iodine generation. The surface balance includes electrochemical I2/I- conversion, precipitation when local free iodine exceeds an effective saturation concentration, and dissolution when undersaturation occurs in the presence of deposited iodine.

The solid state is represented by a local iodine thickness h_I2, a closure-derived surface accessibility variable theta, and a local film resistance R_film = h_I2/sigma_I2. Bare and covered surface pathways operate in parallel. The covered pathway is attenuated by a local film kinetic factor, while the bare pathway is weighted by the remaining accessible fraction. The model returns time series of eta_I, j_bare, j_cov, theta, h_I2, R_film, c_I2,free at the surface, precipitation rate and dissolution rate. A parameter scan was then fitted to compact closure expressions: theta(h_I2), film kinetic attenuation, effective precipitation/dissolution coefficients and bare/covered current split. These closures are local constitutive relations, not direct measurements of microscopic coverage.

### 4.4 Porous-electrode COMSOL model and state extraction

The porous-electrode model contains the zinc negative side, ion-conducting membrane and positive carbon felt with iodine speciation, transport, reaction, precipitation/dissolution and closure-derived surface variables. The present manuscript analyzes existing solved fields and postprocessed variables; no new empirical voltage-fitting term was introduced in the postprocessing. Extracted positive-electrode quantities include free-I2 supersaturation proxy, solid iodine inventory, closure-derived theta, local film resistance, film kinetic factor, accessible-area proxy and spatial iodine-state profiles.

Two operating routes were compared. Capacity-oriented operation emphasizes cumulative charge and long exposure time, whereas rate-oriented operation emphasizes high interfacial generation flux. The comparison was made using normalized charge progress so that the relative ordering of S_I2, eps_s, theta, R_film and accessible-area loss could be compared across protocols. A capacity route was assigned when solid inventory and surface-state loss rose after cumulative exposure. A rate route was assigned when free-I2 supersaturation rose early, before comparable mean solid inventory developed.

### 4.5 Local iodine-handling coordinates

The mechanism is described by source, removal, phase and morphology coordinates. The local iodine source is J_gen = j_loc/(2F), where j_loc is the local interfacial current density. The local removal scale is J_rem = k_m,eff beta_eff c_I2,sat,eff, where k_m,eff groups diffusion and flow renewal, beta_eff expresses rapid soluble complexation and c_I2,sat,eff is the local free-I2 saturation scale. The local handling number is Da_I2 = J_gen/J_rem. The phase coordinate is S_I2 = c_I2,free,local/c_I2,sat,eff, and the cumulative exposure coordinate is Omega_I2 = integral max(S_I2 - S_on, 0) dt. Solid iodine accumulation is interpreted through d eps_s/dt = V_m,I2(R_precip - R_diss). These quantities are used as diagnostic coordinates rather than as a single fitted failure threshold.

### 4.6 Mean-field versus localized blockage analysis

Uniform solid iodine inventory was compared with localized obstruction using a simple amplification argument. The mean solid iodine volume fraction eps_s,mean changes the average porosity smoothly and may produce only a modest permeability reduction when it is small. If the same inventory is concentrated into a fraction f_local of the pore volume or active felt region, the local solid loading becomes eps_s,local = eps_s,mean/f_local. This scan was used to determine when an apparently small continuum inventory could become large enough locally to cover surfaces, bridge fiber crossings or obstruct pore throats. The calculation is a physical implication analysis; it does not fit f_local to any pressure trace and does not assign an absolute pressure threshold.

### 4.7 Parameter-family interpretation

Parameter effects were interpreted according to where they enter the iodine-failure chain. Accessible carbon area changes local source intensity and inventory distribution. Flow renewal and diffusivity change k_m,eff and therefore removal capacity. Iodide, bromide and iodine saturation move the free-I2 phase gate. Precipitation and dissolution control solid inventory and reversibility. Compression and localization control hydraulic amplification. Conductivity, membrane resistance and ASR control voltage loss but do not by themselves determine iodine phase stability. This grouping avoids ranking all parameters on one arbitrary lever axis and instead links each intervention to a falsifiable physical mechanism.

### 4.8 Reproducibility and limitations

The standalone single-fiber model, closure fitting scripts, COMSOL postprocessing scripts and figure-generation scripts are retained in the project repository. Original experimental archives and COMSOL model files were not modified. The principal limitations are that surface coverage is closure-derived rather than directly imaged, film attenuation is a local model variable rather than an independently measured film conductivity, pressure is not quantitatively predicted, and clump hydrodynamics are not resolved. These limitations define the next experimental tests: phase identification, pressure tracing during charge, interrupted-charge imaging or mass/Cdl measurements, reference-electrode separation of positive and negative polarization, and controlled flow-renewal perturbations.


## 5 Conclusions

This work identifies solid iodine failure in zinc-iodine flow batteries as a local iodine-handling failure of the porous positive carbon felt. The decisive state is the fiber-scale balance between free-I2 generation and local removal, not the total iodine inventory in the reservoir. Molecular surface calculations show that iodine residence near carbon motifs is chemically plausible. A radial single-fiber model converts local deposition into interpretable closures for surface accessibility, film attenuation, precipitation/dissolution and bare/covered current partition. COMSOL state evolution then separates two routes to the same failure chain: capacity-oriented operation loads cumulative solid inventory and surface-state persistence, whereas rate-oriented operation first raises the free-I2 supersaturation coordinate. Finally, the mean-field/localization analysis explains why visible clumps and pressure symptoms require morphology amplification beyond a uniform solid-volume-fraction argument.

The resulting framework is deliberately operational. It tells an experimentalist which variables must be measured to make iodine blockage predictable: local iodine supersaturation, cumulative supersaturation dose, solid iodine inventory, accessible surface state, flow renewal, localization and pressure response. It also tells a modeler where additional physics is needed: pore-scale nucleation heterogeneity, solid transport, permeability loss and coupled hydraulic instability. The contribution is therefore not an optimized additive recipe or a production operating map, but a physically ordered route from soluble iodine chemistry to solid iodine blockage in a working porous electrode.


## Data availability

Processed data tables and figure-generation scripts needed to reproduce the manuscript figures are available from the corresponding author upon reasonable request and should be deposited in a public repository before final publication. Original experimental archives and COMSOL model files are retained unchanged.

## Code availability

Python postprocessing scripts, the standalone single-fiber model, closure-fitting scripts and manuscript figure-generation scripts will be made available with the curated data package.

## Author contributions

[To be completed by the authors before submission.]

## Conflict of Interest

The authors declare that they have no conflict of interest. [Revise before submission if any financial or non-financial conflict exists.]

## Funding

[To be completed by the authors before submission. Include full fund names and grant numbers.]

## Acknowledgements

[To be completed by the authors before submission.]

## Ethical approval

This article does not contain any studies with human participants or animals performed by any of the authors.

## Informed consent

Not applicable.

## References

[1] Weber A Z, Mench M M, Meyers J P, et al. Redox flow batteries: a review. J Appl Electrochem, 2011, 41: 1137-1164. doi:10.1007/s10800-011-0348-2.
[2] Soloveichik G L. Flow batteries: current status and trends. Chem Rev, 2015, 115: 11533-11558. doi:10.1021/cr500720t.
[3] Noack J, Roznyatovskaya N, Herr T, et al. The chemistry of redox-flow batteries. Angew Chem Int Ed, 2015, 54: 9776-9809. doi:10.1002/anie.201410823.
[4] Li B, Nie Z, Vijayakumar M, et al. Ambipolar zinc-polyiodide electrolyte for a high-energy density aqueous redox flow battery. Nat Commun, 2015, 6: 6303. doi:10.1038/ncomms7303.
[5] Weng G M, Li Z, Cong G, et al. Unlocking the capacity of iodide for high-energy-density zinc/polyiodide and lithium/polyiodide redox flow batteries. Energy Environ Sci, 2017, 10: 735-741. doi:10.1039/C6EE03554J.
[6] Xie C, Zhang H, Xu W, et al. A long cycle life, self-healing zinc-iodine flow battery with high power density. Angew Chem Int Ed, 2018, 57: 11171-11176. doi:10.1002/anie.201803122.
[7] Xie C, Liu Y, Lu W, et al. Highly stable zinc-iodine single flow batteries with super high energy density for stationary energy storage. Energy Environ Sci, 2019, 12: 1834-1839. doi:10.1039/C8EE02825G.
[8] Ma J, Liu M, He Y, et al. Iodine redox chemistry in rechargeable batteries. Angew Chem Int Ed, 2021, 60: 12636-12647. doi:10.1002/anie.202009871.
[9] Williams A A, Emmett R K, Roberts M E. High power zinc iodine redox flow battery with iron-functionalized carbon electrodes. Phys Chem Chem Phys, 2023, 25: 16222-16226. doi:10.1039/D3CP02067C.
[10] Wang C, Gao G, Su Y, et al. High-voltage and dendrite-free zinc-iodine flow battery. Nat Commun, 2024, 15: 6234. doi:10.1038/s41467-024-50543-2.
[11] Richtr P, Graf D, Drnec M, et al. Understanding the degradation process in zinc-iodine hybrid flow batteries. J Mater Chem A, 2026, 14: 4529-4545. doi:10.1039/D5TA07792C.
[12] Berkowitz A, Caiado A A, Aravamuthan S R, et al. Optimization framework for redox flow battery electrodes with improved microstructural characteristics. Energy Adv, 2024, 3: 2220-2237. doi:10.1039/D4YA00248B.
[13] Palmer D A, Ramette R W, Mesmer R E. Triiodide ion formation equilibrium and activity coefficients in aqueous solution. J Solution Chem, 1984, 13: 673-683. doi:10.1007/BF00650374.
[14] Chakrabarti B K, Kalamaras E, Singh A K, et al. Modelling of redox flow battery electrode processes at a range of length scales: a review. Sustain Energy Fuels, 2020, 4: 5433-5468. doi:10.1039/D0SE00667J.
[15] Banerjee R, Bevilacqua N, Mohseninia A, et al. Carbon felt electrodes for redox flow battery: impact of compression on transport properties. J Energy Storage, 2019, 26: 100997. doi:10.1016/j.est.2019.100997.
[16] Emmel D, Hofmann J D, Arlt T, et al. Understanding the impact of compression on the active area of carbon felt electrodes for redox flow batteries. ACS Appl Energy Mater, 2020, 3: 4384-4393. doi:10.1021/acsaem.0c00075.
[17] Amini K, Shocron A N, Suss M E, et al. Pathways to high-power-density redox flow batteries. ACS Energy Lett, 2023, 8: 3526-3535. doi:10.1021/acsenergylett.3c01043.
[18] Wang P, Zhao Y, Ban Y, et al. A review of porous electrode structural parameters and optimization for redox flow batteries. J Energy Storage, 2024, 97: 112859. doi:10.1016/j.est.2024.112859.
[19] Lee J, Faheem A B, Jang W J, et al. Effective enhancement of energy density of zinc-polyiodide flow batteries by organic/penta-iodide complexation. ACS Appl Mater Interfaces, 2023, 15: 48122-48134. doi:10.1021/acsami.3c09426.
[20] Wei Z, Wang Y, Hong H, et al. Long-life aqueous zinc-iodine flow batteries enabled by selectively intercepting hydrated ions. Nat Commun, 2025, 16: 9301. doi:10.1038/s41467-025-64344-8.
