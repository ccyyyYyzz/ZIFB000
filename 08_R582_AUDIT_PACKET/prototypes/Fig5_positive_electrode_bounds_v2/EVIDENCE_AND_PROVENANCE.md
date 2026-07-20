# Evidence and provenance

## Main-text-safe numbers

### Panel a — periodic single-I2 placement prior

- Accepted PBE-D3(BJ) plus PBE counterpoise-corrected adsorption energies are
  -0.4026 eV per I2 (basal), -0.8482 eV (C=O), -0.9977 eV (C-OH) and
  -0.3185 eV (vacancy).
- Figure values are referenced to basal: C-OH -0.5951 eV, C=O -0.4456 eV,
  basal 0 and vacancy +0.0841 eV.
- Safe inference: the dry periodic calculation supports a relative site
  ordering in which the two oxygenated motifs are more favorable than basal.
- Excluded inference: no solution free energy, adsorption population,
  residence time, nucleation barrier, rate, island density N or calibrated
  accessibility follows from these values.

### Panel b — bulk carrier-mobility prior

All values below are in 10^-9 m2 s^-1 and are means across five long SOC boxes.

| Species | q = 0.8 ECC | q = 1.0 formal charges |
|---|---:|---:|
| I- | 1.222 +/- 0.030 | 0.708 +/- 0.021 |
| I3- | 0.752 +/- 0.067 | 0.533 +/- 0.032 |
| I2Br- | 0.724 +/- 0.088 | 0.518 +/- 0.042 |

- The 0.4247–0.6643 band is the composition-weighted carrier-proxy range across
  the five q = 1.0 SOC boxes. The plotted 0.50 line is the baseline continuum
  D_eff, which lies inside that low-end prior.
- The MD mixture is 1 M ZnI2 + 4 M NH4Br in water. NH4Br is a representative
  supporting electrolyte and I2Br- is one supporting-ligand-containing carrier;
  neither is the figure's protagonist.
- Error bars propagate the four-block within-trajectory stability values over
  the five SOC boxes. They are not independent-replicate SEM or experimental
  uncertainty.
- Safe inference: the calculations bound bulk mobility and charge-scaling
  sensitivity; the charged oxidized carriers are slower than iodide within each
  parameterization.
- Excluded inference: the values do not validate absolute polyhalide mobility,
  simulate transport through deposited iodine, prove phase equilibrium or
  replace a continuum production constant.

### Panel c — single-fibre accessibility comparators

- Sparse placement uses N = 10^11 m^-2; dense placement uses N = 10^14 m^-2.
- Sparse computed nodes retain A_bare/A0 = 0.890 at eps_s = 3.391 x 10^-3.
- Dense computed nodes give A_bare/A0 = 0.544 at eps_s = 1.356 x 10^-3 and
  0.293 at eps_s = 4.069 x 10^-3.
- The origin A_bare/A0 = 1 at eps_s = 0 is an exact zero-solid boundary; other
  lines only connect computed nodes and are not a fitted closure.
- Safe inference: assumed placement density strongly changes the physical
  accessible-area family over the baseline solid-loading range.
- Excluded inference: the curves are not observed morphology, measured
  coverage, a unique placement law or the voltage-calibrated continuum
  accessibility relation.

### Panel d — pore-network permeability comparator

- The exact frozen baseline endpoint is eps_s = 3.21926062394 x 10^-3.
- Linear interpolation of the six registered placement laws at that endpoint
  gives K/K0 = 0.981468–0.991827 (displayed as 0.981–0.992).
- The archived threshold table evaluates eps_s = 3.220 x 10^-3; the renderer
  reproduces that table first and then evaluates the plotted exact endpoint.
- Safe inference: smooth hydraulic permeability remains near unity within the
  analyzed loading range in this idealized 15^3 cubic network family.
- Excluded inference: the result is not measured pore closure, an imaged felt,
  a local blockage field or an electrical-potential result.

## Read-only upstream sources

The exact paths, SHA256 values and evidence roles are recorded in
`R582_Fig5_input_manifest.csv`. The renderer refuses to run if any upstream hash
changes. The seven sources are the accepted CP2K site table, MD carrier table and
range summary, single-fibre clock, pore-network curves and endpoint table, and
the frozen baseline endpoint summary.

## Transformations

1. Panel a subtracts the accepted basal energy from each accepted site energy.
2. Panel b selects I-, I3- and I2Br- from both charge-scaling variants without
   fitting; the shaded band is read from the registered carrier-proxy summary.
3. Panel c selects the sparse and dense computed families and adds only the
   exact zero-solid accessibility boundary.
4. Panel d uses linear interpolation, matching the original R531 endpoint
   procedure. The inset uses the unmodified full-range nodes.
5. No smoothing, extrapolation, synthetic uncertainty or generative artwork is
   used.

## Paper-level boundary

Figure 5 is a bounds/comparator figure for the ZIFB positive electrode. It is
not an independent validation figure and cannot identify deposit morphology.
The calibrated accessibility relation remains a separate continuum-model
object evaluated in Figure 4.

