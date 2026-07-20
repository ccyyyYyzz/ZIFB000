// R581 true-mesh physical-dense closure solve. Run only after the mesh-only probe passes.
import com.comsol.model.*;
import com.comsol.model.util.*;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Locale;

public class R581TrueMeshPhysicalRun {
  static final String INPUT_MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_true_mesh_physical_input_COPY.mph";
  static final String OUTPUT_MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\outputs\\R581_true_mesh_physical_dense_SOLVED.mph";
  static final String CASE_ID = "matched_physical_dense_true_mesh";
  static final String DATASET_TAG = "dsetR581PhysMesh";
  static final long EXPECTED_INPUT_ELEMENTS = 1944L;
  static final String HMAX = "0.00067";
  static final String HMIN = "3e-6";
  static final String HGRAD = "1.2";
  static final int DIS1_NUMELEM = 36;
  static final int DIS2_NUMELEM = 36;
  static final int DIS3_NUMELEM = 72;
  static final String PRODUCTION_COV = "1-exp(-k_geo*N_i2_pos^(1/3)*eps_s_reg^(2/3))";
  static final String PRODUCTION_THETA = "cov_theta_surf";
  static final String PHYSICAL_DENSE = "1-exp(-35.4*eps_s_reg^0.6222)";

  static final String[][] SERIES = new String[][] {
    {"time_s", "t"},
    {"q_mAh_cm2", "i_app*t/36000"},
    {"voltage_V", "tcd.phis0_ec1"},
    {"S_direct", "aveop1(cI2_surf_free/cI2_sat)"},
    {"S_reconstructed", "aveop1(gamma_I2_saltout*cI2_surf_tot/(beta_I2_surf_dyn*cI2_sat0))"},
    {"cI2_surf_free_avg_mol_m3", "aveop1(cI2_surf_free)"},
    {"cI2_surf_tot_avg_mol_m3", "aveop1(cI2_surf_tot)"},
    {"beta_surf_avg", "aveop1(beta_I2_surf_dyn)"},
    {"cI_minus_surf_avg_mol_m3", "aveop1(cI_m_surf_dyn)"},
    {"eps_s_avg", "aveop1(eps_s_pos)"},
    {"eps_s_reg_avg", "aveop1(eps_s_reg)"},
    {"theta_avg", "aveop1(theta_eff_R520)"},
    {"A_bare_avg", "aveop1(Av_bare_i2/av0_i2)"},
    {"K_perm_rel_avg", "aveop1(K_perm_rel_R520)"},
    {"D_rel_avg", "aveop1(D_rel_R520)"},
    {"eps_l_eff_avg", "aveop1(eps_l_eff_R520)"},
    {"Rfilm_avg_ohm_m2", "aveop1(Rfilm_i2)"},
    {"R_precip_avg", "aveop1(R_precip_i2)"},
    {"R_diss_avg", "aveop1(R_diss_i2)"}
  };

  static Object call(Object target, String name, Class<?>[] types, Object... args) {
    if (target == null) return null;
    try { return target.getClass().getMethod(name, types).invoke(target, args); }
    catch (Throwable t) { return null; }
  }
  static Object c0(Object target, String name) { return call(target, name, new Class<?>[]{}); }
  static Object c1(Object target, String name, String a) { return call(target, name, new Class<?>[]{String.class}, a); }
  static Object c2(Object target, String name, String a, String b) { return call(target, name, new Class<?>[]{String.class, String.class}, a, b); }
  static Object c2a(Object target, String name, String a, String[] b) { return call(target, name, new Class<?>[]{String.class, String[].class}, a, b); }
  static String clean(Object value) { return value == null ? "" : String.valueOf(value).replace('\n', ' ').replace('\r', ' ').replace(',', ';'); }
  static String fmt(double value) { return Double.isFinite(value) ? String.format(Locale.US, "%.12g", value) : "NaN"; }
  static void require(boolean condition, String message) { if (!condition) throw new IllegalStateException(message); }
  static long asLong(Object value, String label) {
    if (value instanceof Number) return ((Number) value).longValue();
    try { return Long.parseLong(clean(value)); }
    catch (Throwable t) { throw new IllegalStateException("Could not parse " + label + " from " + clean(value)); }
  }
  static String property(Object feature, String name) {
    Object value = c1(feature, "getString", name);
    if (value == null) value = c1(feature, "get", name);
    return clean(value);
  }

  static String datasetSolution(Model model, String dataset) {
    Object manager = c0(c0(model, "result"), "dataset");
    Object feature = c1(manager, "feature", dataset);
    if (feature == null) feature = model.result().dataset(dataset);
    return clean(c1(feature, "getString", "solution"));
  }

  static void applyTrueMeshRefinement(Model model) {
    Object mesh = model.component("comp1").mesh("mesh1");
    Object size = model.component("comp1").mesh("mesh1").feature("size");
    Object dis1 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis1");
    Object dis2 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis2");
    Object dis3 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis3");
    require(mesh != null && size != null && dis1 != null && dis2 != null && dis3 != null,
            "Required mapped-mesh feature missing");
    long beforeElements = asLong(c0(c0(mesh, "stat"), "getNumElem"), "input element count");
    require(beforeElements == EXPECTED_INPUT_ELEMENTS,
            "Unexpected input element count: " + beforeElements + " != " + EXPECTED_INPUT_ELEMENTS);
    System.out.println(
      "TRUE_MESH_BEFORE,elements=" + beforeElements
      + ",hmax=" + property(size, "hmax")
      + ",hmin=" + property(size, "hmin")
      + ",hgrad=" + property(size, "hgrad")
      + ",dis1=" + property(dis1, "numelem")
      + ",dis2=" + property(dis2, "numelem")
      + ",dis3=" + property(dis3, "numelem")
    );

    model.component("comp1").mesh("mesh1").feature("size").set("custom", "on");
    model.component("comp1").mesh("mesh1").feature("size").set("hmax", HMAX);
    model.component("comp1").mesh("mesh1").feature("size").set("hmin", HMIN);
    model.component("comp1").mesh("mesh1").feature("size").set("hgrad", HGRAD);
    model.component("comp1").mesh("mesh1").feature("map1").feature("dis1").set("numelem", DIS1_NUMELEM);
    model.component("comp1").mesh("mesh1").feature("map1").feature("dis2").set("numelem", DIS2_NUMELEM);
    model.component("comp1").mesh("mesh1").feature("map1").feature("dis3").set("numelem", DIS3_NUMELEM);
    model.component("comp1").mesh("mesh1").run();

    long afterElements = asLong(c0(c0(mesh, "stat"), "getNumElem"), "refined element count");
    Object stat = c0(mesh, "stat");
    System.out.println(
      "TRUE_MESH_AFTER,elements=" + afterElements
      + ",vertices=" + clean(c0(stat, "getNumVertex"))
      + ",min_quality=" + clean(c0(stat, "getMinQuality"))
      + ",hmax=" + property(size, "hmax")
      + ",hmin=" + property(size, "hmin")
      + ",hgrad=" + property(size, "hgrad")
      + ",dis1=" + property(dis1, "numelem")
      + ",dis2=" + property(dis2, "numelem")
      + ",dis3=" + property(dis3, "numelem")
    );
    require(afterElements > beforeElements,
            "True mesh refinement failed to increase element count: " + afterElements);

    // Keep the same tightened temporal tolerance as the 1944-element refined
    // control. This makes their difference a mesh-only comparison.
    model.study("stdR522").feature("time").set("usertol", "on");
    model.study("stdR522").feature("time").set("rtol", "3e-4");
    model.sol("sol5").feature("t1").set("rtol", "3e-4");
    System.out.println(
      "TRUE_MESH_REFINEMENT,hmax=" + HMAX + ",hmin=" + HMIN + ",hgrad=" + HGRAD
      + ",distributions=36|36|72,rtol=3e-4,before_elements=" + beforeElements
      + ",after_elements=" + afterElements
    );
  }

  static double[][] evaluate(Model model, String dataset) {
    Object numerical = c0(c0(model, "result"), "numerical");
    Object feature = c2(numerical, "create", "gevR581Mesh", "EvalGlobal");
    require(feature != null, "Could not create EvalGlobal feature");
    c2(feature, "set", "data", dataset);
    String[] expressions = new String[SERIES.length];
    for (int i = 0; i < SERIES.length; i++) expressions[i] = SERIES[i][1];
    c2a(feature, "set", "expr", expressions);
    Object raw = c0(feature, "getReal");
    require(raw instanceof double[][], "EvalGlobal did not return double[][]");
    double[][] values = (double[][]) raw;
    require(values.length == SERIES.length, "Unexpected EvalGlobal expression count: " + values.length);
    int n = values[0].length;
    require(n > 1, "Empty/single-point trajectory");
    for (int i = 1; i < values.length; i++) require(values[i].length == n, "Mismatched trajectory length");
    return values;
  }

  static void printSeries(double[][] values) {
    StringBuilder header = new StringBuilder("CSV_HEADER,case_id");
    for (String[] item : SERIES) header.append(',').append(item[0]);
    System.out.println(header.toString());
    for (int row = 0; row < values[0].length; row++) {
      StringBuilder line = new StringBuilder("CSV_ROW,").append(CASE_ID);
      for (double[] value : values) line.append(',').append(fmt(value[row]));
      System.out.println(line.toString());
    }
  }

  public static void main(String[] args) throws Exception {
    ModelUtil.initStandalone(false);
    ModelUtil.showProgress(true);
    System.out.println("R581_TRUE_MESH_CASE_START," + CASE_ID);
    System.out.println("R581_INPUT," + INPUT_MPH);
    System.out.println("R581_OUTPUT," + OUTPUT_MPH);
    Model model = ModelUtil.load("r581_true_mesh_physical", INPUT_MPH);
    require(Arrays.asList(model.study().tags()).contains("stdR522"), "stdR522 missing");
    require(Arrays.asList(model.sol().tags()).contains("sol5"), "sol5 missing before solve");
    require(datasetSolution(model, "dset5").equals("sol5"), "dset5 does not map to sol5");

    ModelEntity variable = model.component("comp1").variable("varTry2I2");
    String covBefore = clean(c1(variable, "get", "cov_theta_surf"));
    String thetaBefore = clean(c1(variable, "get", "theta_eff_R520"));
    System.out.println("CLOSURE_BEFORE,cov_theta_surf," + covBefore);
    System.out.println("CLOSURE_BEFORE,theta_eff_R520," + thetaBefore);
    require(covBefore.equals(PRODUCTION_COV), "Unexpected production coverage expression");
    require(thetaBefore.equals(PRODUCTION_THETA), "Unexpected production theta expression");
    model.component("comp1").variable("varTry2I2").set("cov_theta_surf", PHYSICAL_DENSE);
    model.component("comp1").variable("varTry2I2").set("theta_eff_R520", PHYSICAL_DENSE);
    String covAfter = clean(c1(variable, "get", "cov_theta_surf"));
    String thetaAfter = clean(c1(variable, "get", "theta_eff_R520"));
    System.out.println("CLOSURE_AFTER,cov_theta_surf," + covAfter);
    System.out.println("CLOSURE_AFTER,theta_eff_R520," + thetaAfter);
    require(covAfter.equals(PHYSICAL_DENSE) && thetaAfter.equals(PHYSICAL_DENSE),
            "Physical-dense closure mutation failed");

    applyTrueMeshRefinement(model);
    long start = System.currentTimeMillis();
    System.out.println("SOLVE_START,stdR522");
    model.study("stdR522").run();
    long solveMs = System.currentTimeMillis() - start;
    System.out.println("SOLVE_DONE,stdR522,elapsed_ms=" + solveMs);
    require(datasetSolution(model, "dset5").equals("sol5"), "dset5 lost sol5 mapping after solve");
    require(!Arrays.asList(model.result().dataset().tags()).contains(DATASET_TAG), "Dataset tag already exists");
    model.result().dataset().create(DATASET_TAG, "Solution");
    model.result().dataset(DATASET_TAG).set("solution", "sol5");
    require(datasetSolution(model, DATASET_TAG).equals("sol5"), "New dataset does not map to sol5");
    model.save(OUTPUT_MPH);
    System.out.println("MODEL_SAVED," + OUTPUT_MPH);

    double[][] values = evaluate(model, DATASET_TAG);
    printSeries(values);
    double maxIdentity = 0.0;
    for (int i = 0; i < values[3].length; i++) maxIdentity = Math.max(maxIdentity, Math.abs(values[3][i] - values[4][i]));
    System.out.println("IDENTITY_MAX_ABS_S," + fmt(maxIdentity));
    System.out.println("R581_TRUE_MESH_CASE_OK," + CASE_ID + ",rows=" + values[0].length + ",solve_ms=" + solveMs);
    ModelUtil.remove("r581_true_mesh_physical");
  }
}
