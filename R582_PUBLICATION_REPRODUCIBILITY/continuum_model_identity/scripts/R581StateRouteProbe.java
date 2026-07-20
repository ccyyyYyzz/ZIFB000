// R581 read-only state-route/current-ledger probe.
// Loads the verified solved copy, evaluates sol5 through dset5, writes only a CSV audit output,
// and never solves, mutates, or saves the model.
import com.comsol.model.*;
import com.comsol.model.util.*;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.lang.reflect.Method;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

public class R581StateRouteProbe {
  static final String MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_probe_input_COPY.mph";
  static final String OUT = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\outputs\\R581_state_route_probe.csv";
  static final String DATASET = "dset5";

  static Object call(Object target, String name, Class<?>[] types, Object... args) {
    if (target == null) return null;
    try {
      Method m = target.getClass().getMethod(name, types);
      return m.invoke(target, args);
    } catch (Throwable t) {
      return null;
    }
  }

  static Object c0(Object target, String name) {
    return call(target, name, new Class<?>[]{});
  }

  static Object c2(Object target, String name, String a, String b) {
    return call(target, name, new Class<?>[]{String.class, String.class}, a, b);
  }

  static Object c2a(Object target, String name, String a, String[] b) {
    return call(target, name, new Class<?>[]{String.class, String[].class}, a, b);
  }

  static String clean(Object value) {
    return value == null ? "" : String.valueOf(value).replace('\n', ' ').replace('\r', ' ').replace(',', ';');
  }

  static String fmt(double value) {
    return Double.isFinite(value) ? String.format(Locale.US, "%.12g", value) : "";
  }

  static double[] eval(Model model, String label, String expression) {
    Object numerical = c0(c0(model, "result"), "numerical");
    String tag = "r581route_" + Math.abs(label.hashCode());
    Object feature = c2(numerical, "create", tag, "EvalGlobal");
    c2(feature, "set", "data", DATASET);
    c2a(feature, "set", "expr", new String[]{expression});
    Object raw = c0(feature, "getReal");
    if (!(raw instanceof double[][]) || ((double[][]) raw).length == 0) {
      throw new RuntimeException("Evaluation failed for " + label + ": " + expression);
    }
    double[] values = ((double[][]) raw)[0];
    System.out.println("EVAL," + label + ",n=" + values.length + ",first=" + fmt(values[0]) + ",last=" + fmt(values[values.length - 1]) + ",expr=" + expression);
    return values;
  }

  static double[][] evalAll(Model model, String[] labels, String[] expressions) {
    Object numerical = c0(c0(model, "result"), "numerical");
    Object feature = c2(numerical, "create", "r581route_all", "EvalGlobal");
    c2(feature, "set", "data", DATASET);
    c2a(feature, "set", "expr", expressions);
    Object raw = c0(feature, "getReal");
    if (!(raw instanceof double[][])) throw new RuntimeException("Multi-expression evaluation failed");
    double[][] values = (double[][]) raw;
    if (values.length != expressions.length) {
      throw new RuntimeException("Expected " + expressions.length + " expression rows; got " + values.length);
    }
    for (int i = 0; i < values.length; i++) {
      if (values[i].length == 0) throw new RuntimeException("Empty result for " + labels[i]);
      System.out.println("EVAL," + labels[i] + ",n=" + values[i].length + ",first=" + fmt(values[i][0]) + ",last=" + fmt(values[i][values[i].length - 1]) + ",expr=" + expressions[i]);
    }
    return values;
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      Model model = ModelUtil.load("r581stateroute", MPH);
      System.out.println("PROBE,LOADED," + MPH);

      LinkedHashMap<String, String> expressions = new LinkedHashMap<String, String>();
      expressions.put("Q_mAh_cm2", "i_app*t/36000");
      expressions.put("voltage_V", "tcd.phis0_ec1");
      expressions.put("S_direct_avg", "aveop1(cI2_surf_free/cI2_sat)");
      expressions.put("eps_s_feedback_avg", "aveop1(eps_s_pos)");
      expressions.put("eps_s_tcd_native_raw_avg", "aveop1(tcd.epss)-(1-epsl_cf)");
      expressions.put("eps_s_ode_avg", "aveop1(eps_s_i2)");
      expressions.put("N_i2_ode_avg", "aveop1(N_i2)");
      expressions.put("R_precip_fraction_per_s_avg", "aveop1(R_precip_i2)");
      expressions.put("R_diss_fraction_per_s_avg", "aveop1(R_diss_i2)");
      expressions.put("i0_i2s_phase_A_m2_avg", "aveop1(i0_i2s_phase)");
      expressions.put("j_bare_geom_A_m2", "aveop1(tcd.pce2.per1.iloc*Av_bare_i2)*W_cf");
      expressions.put("j_i2s_geom_A_m2", "aveop1(tcd.pce2.per_i2s_tafel.iloc*av0_i2)*W_cf");
      expressions.put("j_positive_geom_A_m2", "aveop1(tcd.pce2.per1.iloc*Av_bare_i2+tcd.pce2.per_i2s_tafel.iloc*av0_i2)*W_cf");
      expressions.put("cI2_total_avg_mol_m3", "aveop1(cI2_tot)");
      expressions.put("cI2_tank_mol_m3", "cBr2_tank");

      String[] labels = expressions.keySet().toArray(new String[0]);
      String[] expressionArray = expressions.values().toArray(new String[0]);
      double[][] result = evalAll(model, labels, expressionArray);
      LinkedHashMap<String, double[]> columns = new LinkedHashMap<String, double[]>();
      int n = result[0].length;
      for (int i = 0; i < labels.length; i++) {
        if (result[i].length != n) throw new RuntimeException("Length mismatch for " + labels[i]);
        columns.put(labels[i], result[i]);
      }

      StringBuilder header = new StringBuilder("ROUTE_HEADER");
      for (String key : columns.keySet()) header.append(",").append(key);
      System.out.println(header.toString());
      boolean first = true;
      for (int row = 0; row < n; row++) {
        StringBuilder record = new StringBuilder("ROUTE_ROW");
        for (double[] values : columns.values()) {
          record.append(",").append(fmt(values[row]));
        }
        System.out.println(record.toString());
      }
      System.out.println("WRITE,stdout_route_rows," + n);
      System.out.println("PROBE,OK,no_solve_no_save");
      ModelUtil.remove("r581stateroute");
    } catch (Throwable t) {
      System.out.println("PROBE,FATAL," + t.getClass().getName() + "," + clean(t.getMessage()));
      t.printStackTrace(System.out);
      System.exit(2);
    }
  }
}
