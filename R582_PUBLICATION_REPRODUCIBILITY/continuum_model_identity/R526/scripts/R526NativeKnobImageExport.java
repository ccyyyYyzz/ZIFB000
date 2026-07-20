import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

import java.io.File;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.Locale;

public class R526NativeKnobImageExport {
  static final String MPH = "outputs/R523_IMAGE_MESH_REPAIR/comsol/ZIFB_R523_NATIVE_FPF_COUPLED_REFINED_SOLVED.mph";
  static final String OUT = "C:/Users/CYZ\u7684computer/.comsol/v63/applications/files/user/R526_COMSOL_NATIVE_KNOB_EXPORT";
  // COMSOL batch Java is sandboxed to the COMSOL user-files tree. A companion
  // PowerShell watcher moves completed MPH files from this local staging folder
  // to E:/cyz000/solved_mph_archive/R526_COMSOL_NATIVE_KNOB_EXPORT.
  static final String ARCHIVE = OUT + "/solved_mph_local";
  static final String MANIFEST = OUT + "/R526_COMSOL_NATIVE_KNOB_IMAGE_MANIFEST.csv";
  static final String STATUS = OUT + "/R526_NATIVE_SOLVE_STATUS.csv";
  static final String MODEL_MANIFEST = OUT + "/R526_SOLVED_MPH_ARCHIVE_MANIFEST.csv";

  static final String[][] CASES = new String[][] {
    // case_id, family, knob, target_Q, i_app_A_m2, solve, rebuild_geom_mesh
    {"baseline_J40_Q120","baseline","J40 Q120", "120", "400", "false", "false"},
    {"rate_J20_Q40","current_density_fixed_Q","J20 Q40", "40", "200", "true", "false"},
    {"rate_J40_Q40","current_density_fixed_Q","J40 Q40", "40", "400", "false", "false"},
    {"rate_J80_Q40","current_density_fixed_Q","J80 Q40", "40", "800", "true", "false"},
    {"rate_J120_Q40","current_density_fixed_Q","J120 Q40", "40", "1200", "true", "false"},
    {"comp_L15_Q120","compression_true_branch","L=1.5mm eps=0.800", "120", "400", "true", "true"},
    {"comp_L25_Q120","compression_true_branch","L=2.5mm eps=0.880", "120", "400", "true", "true"},
    {"comp_L30_Q120","compression_true_branch","L=3.0mm eps=0.900", "120", "400", "true", "true"},
    {"br_2M_Q120","Br_support_isolated","cBr=2M", "120", "400", "true", "false"},
    {"br_3M_Q120","Br_support_isolated","cBr=3M", "120", "400", "true", "false"},
    {"br_5M_Q120","Br_support_isolated","cBr=5M", "120", "400", "true", "false"},
    {"activity_gamma2_Q120","activity_saltout","gamma=2", "120", "400", "true", "false"},
    {"activity_gamma4_Q120","activity_saltout","gamma=4", "120", "400", "true", "false"},
    {"flow_25_Q120","flow_rate","Q_flow=25 ml/min", "120", "400", "true", "false"},
    {"flow_100_Q120","flow_rate","Q_flow=100 ml/min", "120", "400", "true", "false"},
    {"sigmal_10_Q120","liquid_conductivity","sigmal=10 S/m", "120", "400", "true", "false"},
    {"sigmal_40_Q120","liquid_conductivity","sigmal=40 S/m", "120", "400", "true", "false"},
    {"D_half_Q120","diffusion_prior","D species 0.5x", "120", "400", "true", "false"},
    {"D_double_Q120","diffusion_prior","D species 2x", "120", "400", "true", "false"},
    {"Av_half_Q120","wet_area_Av","Av 0.5x", "120", "400", "true", "false"},
    {"Av_double_Q120","wet_area_Av","Av 2x", "120", "400", "true", "false"},
    {"sigmas_80_Q120","solid_conductivity","sigmas=80 S/m", "120", "400", "true", "false"},
    {"sigmas_320_Q120","solid_conductivity","sigmas=320 S/m", "120", "400", "true", "false"}
  };

  static final String[][] FIELDS = new String[][]{
    {"S_surf", "Free-I2 stress S", "cI2_surf_free/cI2_sat"},
    {"eps_s_pos", "Native I2(s) inventory", "eps_s_pos"},
    {"theta_eff", "Accessibility loss theta", "theta_eff_R520"},
    {"A_bare_frac", "Bare accessible area", "Av_bare_i2/av0_i2"},
    {"K_perm_rel", "Relative permeability K/K0", "K_perm_rel_R520"},
    {"u_native_mag", "Native Darcy/Brinkman speed", "u_native_mag_R522"},
    {"p_native", "Native pressure", "p_native_R522"}
  };

  static final String[][] BASELINE = new String[][]{
    {"i_app", "400[A/m^2]"},
    {"W_cf", "2[mm]"},
    {"epsl_cf", "0.85"},
    {"Av_cf", "4e4[1/m]"},
    {"K0_perm_R520", "1e-10[m^2]"},
    {"c0_NH4Br", "4[M]"},
    {"cBr_support", "4[M]"},
    {"gamma_I2_saltout", "3"},
    {"Q_flow", "50[ml/min]"},
    {"sigmal", "20[S/m]"},
    {"D_I2_free", "0.6e-9[m^2/s]"},
    {"D_I3_m", "0.5e-9[m^2/s]"},
    {"D_I2Br_m", "0.5e-9[m^2/s]"},
    {"D_I_m", "1.0e-9[m^2/s]"},
    {"D_Br_m", "1.0e-9[m^2/s]"},
    {"sigmas_cf", "160[S/m]"}
  };

  static Object call(Object target, String name, Class<?>[] types, Object... args) throws Exception {
    Method m = target.getClass().getMethod(name, types);
    return m.invoke(target, args);
  }
  static Object call0(Object target, String name) throws Exception { return call(target, name, new Class<?>[]{}); }
  static Object call1s(Object target, String name, String a) throws Exception { return call(target, name, new Class<?>[]{String.class}, a); }
  static Object call2s(Object target, String name, String a, String b) throws Exception { return call(target, name, new Class<?>[]{String.class, String.class}, a, b); }
  static Object call2arr(Object target, String name, String a, String[] b) throws Exception { return call(target, name, new Class<?>[]{String.class, String[].class}, a, b); }
  static void set(Object feat, String key, String value) throws Exception { call2s(feat, "set", key, value); }
  static String clean(Object o) { return o == null ? "" : String.valueOf(o).replace('\n',' ').replace('\r',' ').replace(',',';'); }
  static String safe(String s) { return s.replaceAll("[^A-Za-z0-9_\\-]+", "_"); }
  static String fmt(double x) { return (Double.isNaN(x) || Double.isInfinite(x)) ? "NaN" : String.format(Locale.US, "%.12g", x); }
  static String[] tags(Object manager) {
    try { Object o = call0(manager, "tags"); return o instanceof String[] ? (String[]) o : new String[0]; }
    catch (Throwable t) { return new String[0]; }
  }
  static String datasetTag(Model model) {
    try {
      Object dsm = call0(call0(model, "result"), "dataset");
      for (String d : tags(dsm)) if (d.equals("dset5")) return d;
      for (String d : tags(dsm)) if (d.equals("dset1")) return d;
      String[] all = tags(dsm);
      return all.length > 0 ? all[0] : "dset1";
    } catch(Throwable t) { return "dset1"; }
  }
  static void setParam(Model model, String name, String value) {
    try { model.param().set(name, value); System.out.println("PARAM_SET," + name + "," + value + ",OK"); }
    catch(Throwable t) { System.out.println("PARAM_SET," + name + "," + value + ",FAIL," + clean(t.getMessage())); }
  }
  static void setBaseline(Model model) {
    for (String[] p : BASELINE) setParam(model, p[0], p[1]);
  }
  static void applyCaseParams(Model model, String caseId) {
    if (caseId.equals("rate_J20_Q40")) setParam(model, "i_app", "200[A/m^2]");
    if (caseId.equals("rate_J80_Q40")) setParam(model, "i_app", "800[A/m^2]");
    if (caseId.equals("rate_J120_Q40")) setParam(model, "i_app", "1200[A/m^2]");

    if (caseId.equals("comp_L15_Q120")) {
      setParam(model, "W_cf", "1.5[mm]"); setParam(model, "epsl_cf", "0.8");
      setParam(model, "Av_cf", "5.333333333e4[1/m]"); setParam(model, "K0_perm_R520", "4.64734395e-11[m^2]");
    }
    if (caseId.equals("comp_L25_Q120")) {
      setParam(model, "W_cf", "2.5[mm]"); setParam(model, "epsl_cf", "0.88");
      setParam(model, "Av_cf", "3.2e4[1/m]"); setParam(model, "K0_perm_R520", "1.71111313e-10[m^2]");
    }
    if (caseId.equals("comp_L30_Q120")) {
      setParam(model, "W_cf", "3.0[mm]"); setParam(model, "epsl_cf", "0.9");
      setParam(model, "Av_cf", "2.666666667e4[1/m]"); setParam(model, "K0_perm_R520", "2.63021952e-10[m^2]");
    }
    if (caseId.equals("br_2M_Q120")) { setParam(model, "c0_NH4Br", "2[M]"); setParam(model, "cBr_support", "2[M]"); }
    if (caseId.equals("br_3M_Q120")) { setParam(model, "c0_NH4Br", "3[M]"); setParam(model, "cBr_support", "3[M]"); }
    if (caseId.equals("br_5M_Q120")) { setParam(model, "c0_NH4Br", "5[M]"); setParam(model, "cBr_support", "5[M]"); }
    if (caseId.equals("activity_gamma2_Q120")) setParam(model, "gamma_I2_saltout", "2");
    if (caseId.equals("activity_gamma4_Q120")) setParam(model, "gamma_I2_saltout", "4");
    if (caseId.equals("flow_25_Q120")) setParam(model, "Q_flow", "25[ml/min]");
    if (caseId.equals("flow_100_Q120")) setParam(model, "Q_flow", "100[ml/min]");
    if (caseId.equals("sigmal_10_Q120")) setParam(model, "sigmal", "10[S/m]");
    if (caseId.equals("sigmal_40_Q120")) setParam(model, "sigmal", "40[S/m]");
    if (caseId.equals("D_half_Q120")) {
      setParam(model, "D_I2_free", "0.3e-9[m^2/s]"); setParam(model, "D_I3_m", "0.25e-9[m^2/s]");
      setParam(model, "D_I2Br_m", "0.25e-9[m^2/s]"); setParam(model, "D_I_m", "0.5e-9[m^2/s]"); setParam(model, "D_Br_m", "0.5e-9[m^2/s]");
    }
    if (caseId.equals("D_double_Q120")) {
      setParam(model, "D_I2_free", "1.2e-9[m^2/s]"); setParam(model, "D_I3_m", "1.0e-9[m^2/s]");
      setParam(model, "D_I2Br_m", "1.0e-9[m^2/s]"); setParam(model, "D_I_m", "2.0e-9[m^2/s]"); setParam(model, "D_Br_m", "2.0e-9[m^2/s]");
    }
    if (caseId.equals("Av_half_Q120")) setParam(model, "Av_cf", "2e4[1/m]");
    if (caseId.equals("Av_double_Q120")) setParam(model, "Av_cf", "8e4[1/m]");
    if (caseId.equals("sigmas_80_Q120")) setParam(model, "sigmas_cf", "80[S/m]");
    if (caseId.equals("sigmas_320_Q120")) setParam(model, "sigmas_cf", "320[S/m]");
  }
  static void rebuildGeometryMesh(Model model, String caseId) {
    try { model.geom("geom1").run(); System.out.println("GEOM_RUN," + caseId + ",OK"); }
    catch(Throwable t) { System.out.println("GEOM_RUN," + caseId + ",FAIL," + clean(t.getMessage())); }
    try { model.mesh("mesh1").run(); System.out.println("MESH_RUN," + caseId + ",OK"); }
    catch(Throwable t) { System.out.println("MESH_RUN," + caseId + ",FAIL," + clean(t.getMessage())); }
  }
  static void setTimeList(Model model, double iapp, double qEnd) {
    double tend = qEnd * 36000.0 / iapp;
    String tlist = "range(0,10," + String.format(Locale.US, "%.0f", tend) + ")";
    setParam(model, "t_charge", String.format(Locale.US, "%.0f[s]", tend + 1000.0));
    try {
      model.study("stdR522").feature("time").set("tlist", tlist);
      System.out.println("TLIST_SET," + tlist + ",OK");
    } catch(Throwable t) {
      System.out.println("TLIST_SET," + tlist + ",FAIL," + clean(t.getMessage()));
    }
  }
  static double[] evalGlobal(Model model, String expr) {
    try {
      Object num = call0(call0(model, "result"), "numerical");
      Object gev = call2s(num, "create", "r526_gev_" + Math.abs((expr + System.nanoTime()).hashCode()), "EvalGlobal");
      call2s(gev, "set", "data", datasetTag(model));
      call2arr(gev, "set", "expr", new String[]{expr});
      Object real = call0(gev, "getReal");
      if (!(real instanceof double[][])) return new double[0];
      double[][] data = (double[][]) real;
      return data.length > 0 ? data[0] : new double[0];
    } catch(Throwable t) { return new double[0]; }
  }
  static int nearest(double[] a, double target) {
    int k = 0; double best = Double.POSITIVE_INFINITY;
    for (int i=0; i<a.length; i++) {
      double d = Math.abs(a[i] - target);
      if (d < best) { best = d; k = i; }
    }
    return k;
  }
  static void createPlot(Model model, String tag, String expr, String title, String solnum) throws Exception {
    Object result = call0(model, "result");
    try {
      Object pgOld = call1s(result, "get", tag);
      if (pgOld != null) call1s(result, "remove", tag);
    } catch(Throwable ignored) {}
    Object pg = call2s(result, "create", tag, "PlotGroup2D");
    set(pg, "data", datasetTag(model));
    try { set(pg, "solnum", solnum); } catch (Throwable ignored) {}
    try { set(pg, "titletype", "manual"); set(pg, "title", title); } catch (Throwable ignored) {}
    Object surf = call2s(call0(pg, "feature"), "create", "surf1", "Surface");
    set(surf, "expr", expr);
    try { set(surf, "descr", title); } catch (Throwable ignored) {}
    try { call1s(call0(surf, "selection"), "named", "sel3"); } catch (Throwable ignored) {}
    try { call0(pg, "run"); } catch (Throwable ignored) {}
  }
  static boolean exportPlot(Model model, String plotTag, String outPng) {
    String expTag = "img_" + plotTag;
    try {
      Object expMgr = call0(call0(model, "result"), "export");
      Object exp = null;
      try { exp = call2s(expMgr, "create", expTag, "Image2D"); } catch (Throwable ignored) {}
      if (exp == null) exp = call2s(expMgr, "create", expTag, "Image");
      set(exp, "plotgroup", plotTag);
      try { set(exp, "pngfilename", outPng); } catch (Throwable t) { set(exp, "filename", outPng); }
      try { set(exp, "imagetype", "png"); } catch (Throwable ignored) {}
      try { set(exp, "background", "white"); } catch (Throwable ignored) {}
      try { set(exp, "printunit", "px"); set(exp, "webunit", "px"); } catch (Throwable ignored) {}
      try { set(exp, "webwidth", "3000"); set(exp, "webheight", "2100"); } catch (Throwable ignored) {}
      try { set(exp, "width", "3000"); set(exp, "height", "2100"); } catch (Throwable ignored) {}
      call0(exp, "run");
      File f = new File(outPng);
      return f.exists() && f.length() > 1000;
    } catch (Throwable t) {
      System.out.println("EXPORT_FAIL," + plotTag + "," + clean(t.getMessage()));
      return false;
    }
  }
  static boolean solveCase(Model model, String caseId, boolean solve) {
    if (!solve) return true;
    try {
      model.study("stdR522").run();
      System.out.println("CASE_SOLVE," + caseId + ",OK");
      return true;
    } catch(Throwable t) {
      System.out.println("CASE_SOLVE," + caseId + ",FAIL," + t.getClass().getName() + ":" + clean(t.getMessage()));
      return false;
    }
  }
  static String saveSolvedModel(Model model, String caseId) {
    String dir = ARCHIVE + "/" + caseId;
    new File(dir).mkdirs();
    String path = dir + "/R526_" + safe(caseId) + "_solved.mph";
    try {
      model.save(path);
      System.out.println("MODEL_ARCHIVE," + caseId + ",PASS," + path);
      return path;
    } catch(Throwable t) {
      System.out.println("MODEL_ARCHIVE," + caseId + ",FAIL," + t.getClass().getName() + ":" + clean(t.getMessage()));
      return "SAVE_FAILED:" + clean(t.getMessage());
    }
  }
  public static void main(String[] args) {
    new File(OUT).mkdirs();
    new File(ARCHIVE).mkdirs();
    try (PrintWriter man = new PrintWriter(new FileWriter(MANIFEST));
         PrintWriter stat = new PrintWriter(new FileWriter(STATUS));
         PrintWriter mphMan = new PrintWriter(new FileWriter(MODEL_MANIFEST))) {
      man.println("case_id,family,knob,target_Q_mAh_cm2,i_app_A_m2,variable,label,expr,time_s,Q_mAh_cm2,solnum,png,status");
      stat.println("case_id,family,knob,target_Q_mAh_cm2,i_app_A_m2,status,detail,solved_mph_archive");
      mphMan.println("case_id,family,knob,target_Q_mAh_cm2,i_app_A_m2,solved_mph_archive,status");
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      int okImgs = 0; int totalImgs = 0;
      for (String[] c : CASES) {
        String caseId = c[0], family = c[1], knob = c[2];
        double qEnd = Double.parseDouble(c[3]);
        double iapp = Double.parseDouble(c[4]);
        boolean solve = Boolean.parseBoolean(c[5]);
        boolean geom = Boolean.parseBoolean(c[6]);
        System.out.println("CASE_START," + caseId + ",fresh_load");
        Model model = null;
        long t0 = System.currentTimeMillis();
        try {
          model = ModelUtil.load("r526_" + safe(caseId), MPH);
          setBaseline(model);
          setParam(model, "i_app", fmt(iapp) + "[A/m^2]");
          applyCaseParams(model, caseId);
          if (geom) rebuildGeometryMesh(model, caseId);
          setTimeList(model, iapp, qEnd);
          boolean solved = solveCase(model, caseId, solve);
          if (!solved) {
            stat.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + ",FAIL,solve_failed,NOT_SAVED");
            mphMan.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + ",NOT_SAVED,solve_failed");
            ModelUtil.remove("r526_" + safe(caseId));
            continue;
          }
          String archivePath = saveSolvedModel(model, caseId);
          String archiveStatus = archivePath.startsWith("SAVE_FAILED") ? "SAVE_FAILED" : "SAVED";
          mphMan.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + "," + archivePath + "," + archiveStatus);
          mphMan.flush();
          double[] t = evalGlobal(model, "t");
          double targetT = qEnd * 36000.0 / iapp;
          int idx = t.length > 0 ? nearest(t, targetT) : 0;
          int solnum = idx + 1;
          double time = t.length > idx ? t[idx] : targetT;
          double q = iapp * time / 36000.0;
          File caseDir = new File(OUT + "/" + caseId);
          caseDir.mkdirs();
          int caseOk = 0;
          for (String[] f : FIELDS) {
            totalImgs++;
            String plotTag = "r526_" + safe(caseId) + "_" + f[0];
            String png = OUT + "/" + caseId + "/" + plotTag + ".png";
            String title = caseId + " endpoint " + f[1] + " Q=" + fmt(q);
            try {
              createPlot(model, plotTag, f[2], title, String.valueOf(solnum));
              boolean exported = exportPlot(model, plotTag, png);
              if (exported) { okImgs++; caseOk++; }
              man.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + "," + f[0] + "," + f[1].replace(',', ';') + "," + f[2].replace(',', ';') + "," + fmt(time) + "," + fmt(q) + "," + solnum + "," + png + "," + (exported ? "EXPORTED" : "FAILED"));
              System.out.println("NATIVE_EXPORT," + caseId + "," + f[0] + "," + (exported ? "PASS" : "FAIL") + "," + png);
            } catch(Throwable tx) {
              man.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + "," + f[0] + "," + f[1].replace(',', ';') + "," + f[2].replace(',', ';') + "," + fmt(time) + "," + fmt(q) + "," + solnum + "," + png + ",FAILED:" + clean(tx.getMessage()));
              System.out.println("NATIVE_EXPORT," + caseId + "," + f[0] + ",FAIL," + clean(tx.getMessage()));
            }
          }
          long elapsed = System.currentTimeMillis() - t0;
          stat.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + "," + (caseOk == FIELDS.length ? "PASS" : "PARTIAL") + ",images_" + caseOk + "_of_" + FIELDS.length + "_elapsed_ms_" + elapsed + "," + archivePath);
          System.out.println("CASE_DONE," + caseId + "," + caseOk + "," + FIELDS.length + "," + elapsed);
          ModelUtil.remove("r526_" + safe(caseId));
        } catch(Throwable tcase) {
          stat.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + ",FAIL," + tcase.getClass().getName() + ":" + clean(tcase.getMessage()) + ",UNKNOWN");
          mphMan.println(caseId + "," + family + "," + knob.replace(',', ';') + "," + qEnd + "," + iapp + ",UNKNOWN,case_failed_before_archive");
          System.out.println("CASE_FAIL," + caseId + "," + tcase.getClass().getName() + ":" + clean(tcase.getMessage()));
          try { if (model != null) ModelUtil.remove("r526_" + safe(caseId)); } catch(Throwable ignored) {}
        }
      }
      System.out.println("R526_NATIVE_KNOB_IMAGE_EXPORT_DONE," + okImgs + "," + totalImgs + "," + OUT);
    } catch(Throwable t) {
      System.out.println("FATAL," + t.getClass().getName() + "," + clean(t.getMessage()));
      t.printStackTrace(System.out);
    }
  }
}
