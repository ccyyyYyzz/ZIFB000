// R581 matched-branch solver core.
// The two wrappers load independent verified MPH copies in independent COMSOL
// processes.  This class changes no model setting except the two explicitly
// declared accessibility expressions for the physical-island case.
import com.comsol.model.*;
import com.comsol.model.util.*;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Locale;

public class R581RefinedPhysicalRun {
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
    try { Method m = target.getClass().getMethod(name, types); return m.invoke(target, args); }
    catch (Throwable t) { return null; }
  }
  static Object c0(Object target, String name) { return call(target, name, new Class<?>[]{}); }
  static Object c1(Object target, String name, String a) { return call(target, name, new Class<?>[]{String.class}, a); }
  static Object c2(Object target, String name, String a, String b) { return call(target, name, new Class<?>[]{String.class,String.class}, a, b); }
  static Object c2a(Object target, String name, String a, String[] b) { return call(target, name, new Class<?>[]{String.class,String[].class}, a, b); }
  static String clean(Object o) { return o==null?"":String.valueOf(o).replace('\n',' ').replace('\r',' ').replace(',',';'); }
  static String fmt(double x) { return Double.isFinite(x)?String.format(Locale.US,"%.12g",x):"NaN"; }
  static String[] tags(Object manager) { Object o=c0(manager,"tags"); return o instanceof String[]?(String[])o:new String[0]; }

  static void require(boolean condition, String message) {
    if (!condition) throw new IllegalStateException(message);
  }

  static String datasetSolution(Model model, String dataset) {
    Object manager=c0(c0(model,"result"),"dataset");
    Object feature=c1(manager,"feature",dataset);
    if(feature==null) feature=model.result().dataset(dataset);
    Object solution=c1(feature,"getString","solution");
    return clean(solution);
  }

  static void printStudyInventory(Model model) {
    Object manager=c0(model.study("stdR522"),"feature");
    for(String tag:tags(manager)) {
      Object feature=c1(manager,"get",tag);
      Object tlist=c1(feature,"getString","tlist");
      System.out.println("STUDY_FEATURE,"+tag+",tlist="+clean(tlist));
    }
  }

  static void printParameterInventory(Model model) {
    String[] names;
    try { names=model.param().varnames(); }
    catch(Throwable t) { names=new String[0]; }
    Arrays.sort(names);
    for(String name:names) {
      String value="";
      String description="";
      try { value=clean(model.param().get(name)); } catch(Throwable t) {}
      try { description=clean(model.param().descr(name)); } catch(Throwable t) {}
      System.out.println("PARAMETER,"+name+","+value+","+description);
    }
  }

  static double[][] evaluate(Model model, String dataset) {
    Object numerical=c0(c0(model,"result"),"numerical");
    Object feature=c2(numerical,"create","gevR581","EvalGlobal");
    require(feature!=null,"Could not create EvalGlobal feature");
    c2(feature,"set","data",dataset);
    String[] expressions=new String[SERIES.length];
    for(int i=0;i<SERIES.length;i++) expressions[i]=SERIES[i][1];
    c2a(feature,"set","expr",expressions);
    Object raw=c0(feature,"getReal");
    require(raw instanceof double[][],"EvalGlobal did not return double[][]");
    double[][] values=(double[][])raw;
    require(values.length==SERIES.length,"Unexpected EvalGlobal expression count: "+values.length);
    int n=values[0].length;
    require(n>1,"Unexpected empty/single-point trajectory");
    for(int i=1;i<values.length;i++) require(values[i].length==n,"Mismatched trajectory length at expression "+i);
    return values;
  }

  static void printSeries(String caseId, double[][] values) {
    StringBuilder header=new StringBuilder("CSV_HEADER,case_id");
    for(String[] item:SERIES) header.append(',').append(item[0]);
    System.out.println(header.toString());
    int n=values[0].length;
    for(int row=0;row<n;row++) {
      StringBuilder line=new StringBuilder("CSV_ROW,").append(caseId);
      for(int col=0;col<values.length;col++) line.append(',').append(fmt(values[col][row]));
      System.out.println(line.toString());
    }
  }

  static void applyDiscretizationRefinement(Model model) {
    model.component("comp1").mesh("mesh1").feature("size").set("hauto",4);
    model.component("comp1").mesh("mesh1").run();
    model.study("stdR522").feature("time").set("usertol","on");
    model.study("stdR522").feature("time").set("rtol","3e-4");
    model.sol("sol5").feature("t1").set("rtol","3e-4");
    Object stat=c0(model.component("comp1").mesh("mesh1"),"stat");
    Object nElem=c0(stat,"getNumElem");
    Object nVertex=c0(stat,"getNumVertex");
    Object minQuality=c0(stat,"getMinQuality");
    System.out.println("DISCRETIZATION_REFINEMENT,hauto=4,rtol=3e-4,elements="+clean(nElem)+",vertices="+clean(nVertex)+",min_quality="+clean(minQuality));
  }

  public static void run(String caseId, String inputMph, String outputMph,
                         String datasetTag, boolean physicalDense) throws Exception {
    ModelUtil.initStandalone(false);
    ModelUtil.showProgress(true);
    String modelTag="r581_"+caseId;
    System.out.println("R581_CASE_START,"+caseId);
    System.out.println("R581_INPUT,"+inputMph);
    System.out.println("R581_OUTPUT,"+outputMph);
    Model model=ModelUtil.load(modelTag,inputMph);
    System.out.println("MODEL_TAGS,studies,"+String.join("|",model.study().tags()));
    System.out.println("MODEL_TAGS,solutions_before,"+String.join("|",model.sol().tags()));
    System.out.println("MODEL_TAGS,datasets_before,"+String.join("|",model.result().dataset().tags()));
    require(Arrays.asList(model.study().tags()).contains("stdR522"),"stdR522 missing");
    require(Arrays.asList(model.sol().tags()).contains("sol5"),"sol5 missing before solve");
    require(datasetSolution(model,"dset5").equals("sol5"),"dset5 does not map to sol5 before solve");

    printStudyInventory(model);
    printParameterInventory(model);

    ModelEntity variable=model.component("comp1").variable("varTry2I2");
    String covBefore=clean(c1(variable,"get","cov_theta_surf"));
    String thetaBefore=clean(c1(variable,"get","theta_eff_R520"));
    System.out.println("CLOSURE_BEFORE,cov_theta_surf,"+covBefore);
    System.out.println("CLOSURE_BEFORE,theta_eff_R520,"+thetaBefore);
    require(covBefore.equals(PRODUCTION_COV),"Unexpected production cov_theta_surf expression");
    require(thetaBefore.equals(PRODUCTION_THETA),"Unexpected production theta_eff_R520 expression");

    if(physicalDense) {
      model.component("comp1").variable("varTry2I2").set("cov_theta_surf",PHYSICAL_DENSE);
      model.component("comp1").variable("varTry2I2").set("theta_eff_R520",PHYSICAL_DENSE);
    }
    String covAfter=clean(c1(variable,"get","cov_theta_surf"));
    String thetaAfter=clean(c1(variable,"get","theta_eff_R520"));
    System.out.println("CLOSURE_AFTER,cov_theta_surf,"+covAfter);
    System.out.println("CLOSURE_AFTER,theta_eff_R520,"+thetaAfter);
    if(physicalDense) {
      require(covAfter.equals(PHYSICAL_DENSE) && thetaAfter.equals(PHYSICAL_DENSE),"Physical closure mutation failed");
    } else {
      require(covAfter.equals(PRODUCTION_COV) && thetaAfter.equals(PRODUCTION_THETA),"Control closure changed unexpectedly");
    }

    applyDiscretizationRefinement(model);

    long t0=System.currentTimeMillis();
    System.out.println("SOLVE_START,stdR522");
    model.study("stdR522").run();
    long solveMs=System.currentTimeMillis()-t0;
    System.out.println("SOLVE_DONE,stdR522,elapsed_ms="+solveMs);
    System.out.println("MODEL_TAGS,solutions_after,"+String.join("|",model.sol().tags()));
    require(Arrays.asList(model.sol().tags()).contains("sol5"),"sol5 missing after solve");
    require(datasetSolution(model,"dset5").equals("sol5"),"dset5 does not map to live sol5 after solve");

    require(!Arrays.asList(model.result().dataset().tags()).contains(datasetTag),"R581 dataset tag already exists");
    model.result().dataset().create(datasetTag,"Solution");
    model.result().dataset(datasetTag).set("solution","sol5");
    require(datasetSolution(model,datasetTag).equals("sol5"),"New R581 dataset does not map to sol5");
    System.out.println("DATASET_MAPPING,"+datasetTag+",sol5");

    // Save the solved model before adding numerical evaluation helpers.
    model.save(outputMph);
    System.out.println("MODEL_SAVED,"+outputMph);

    double[][] values=evaluate(model,datasetTag);
    printSeries(caseId,values);
    double maxIdentity=0.0;
    for(int i=0;i<values[3].length;i++) maxIdentity=Math.max(maxIdentity,Math.abs(values[3][i]-values[4][i]));
    System.out.println("IDENTITY_MAX_ABS_S,"+fmt(maxIdentity));
    System.out.println("R581_CASE_OK,"+caseId+",rows="+values[0].length+",solve_ms="+solveMs);
    ModelUtil.remove(modelTag);
  }

  public static void main(String[] args) throws Exception {
    // COMSOL's Java security policy blocks getenv/system-property dispatch.
    // This audited source is the independently frozen refined physical entry
    // point; its paired refined control source is R581RefinedControlRun.java.
    String mode="physical_dense";
    if(mode.equals("control")) {
      run(
        "matched_control_refined",
        "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_control_refined_input_COPY.mph",
        "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\outputs\\R581_matched_control_REFINED_SOLVED.mph",
        "dsetR581CtrlRef",
        false
      );
    } else if(mode.equals("physical_dense")) {
      run(
        "matched_physical_dense_refined",
        "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_physical_dense_refined_input_COPY.mph",
        "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\outputs\\R581_matched_physical_dense_REFINED_SOLVED.mph",
        "dsetR581PhysRef",
        true
      );
    } else {
      throw new IllegalArgumentException("Unsupported R581_CASE="+mode);
    }
  }
}
