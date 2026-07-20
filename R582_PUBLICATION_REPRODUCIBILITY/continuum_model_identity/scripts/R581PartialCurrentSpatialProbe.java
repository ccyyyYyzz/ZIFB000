// R581 read-only spatial partial-current probe on the authoritative dset5 -> sol5 branch.
// No solve, no model mutation, no model save; node rows are written only to stdout.
import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;
import java.lang.reflect.Method;
import java.util.Locale;

public class R581PartialCurrentSpatialProbe {
  static final String MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_probe_input_COPY.mph";
  static final String DATASET = "dset5";
  static final double[] Q_TARGET = {80.0, 96.0, 100.0, 108.0, 115.0, 120.0};
  static final String[] LABEL = {"q080", "q096", "q100", "q108", "q115", "q120"};
  static final String[][] FIELD = {
    {"x_m", "x"}, {"y_m", "y"}, {"eps_s_pos", "eps_s_pos"},
    {"theta_eff", "theta_eff_R520"},
    {"j_bare_A_m2", "tcd.pce2.per1.iloc*Av_bare_i2*W_cf"},
    {"j_native_solid_A_m2", "tcd.pce2.per_i2s_tafel.iloc*av0_i2*W_cf"},
    {"Av_bare_1_m", "Av_bare_i2"}, {"Il_mag_A_m2", "tcd.IlMag"}
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
  static String fmt(double x) { return Double.isFinite(x) ? String.format(Locale.US, "%.12g", x) : "NaN"; }

  static double[] evalGlobal(Model model, String expression) {
    Object numerical = c0(c0(model, "result"), "numerical");
    Object feature = c2(numerical, "create", "r581pc_global", "EvalGlobal");
    c2(feature, "set", "data", DATASET);
    c2a(feature, "set", "expr", new String[]{expression});
    Object raw = c0(feature, "getReal");
    if (!(raw instanceof double[][]) || ((double[][]) raw).length == 0) return new double[0];
    return ((double[][]) raw)[0];
  }

  static double[][] normalize(double[][] raw, int expressions) {
    if (raw == null || raw.length == 0) return new double[0][0];
    if (raw.length == expressions) return raw;
    if (raw[0] != null && raw[0].length == expressions) {
      double[][] out = new double[expressions][raw.length];
      for (int row = 0; row < raw.length; row++)
        for (int col = 0; col < expressions; col++) out[col][row] = raw[row][col];
      return out;
    }
    return raw;
  }

  static double[][] evalDomain(Model model, int solnum, String[] expressions) {
    Object numerical = c0(c0(model, "result"), "numerical");
    Object feature = c2(numerical, "create", "r581pc_" + solnum, "Eval");
    c2(feature, "set", "data", DATASET);
    c2a(feature, "set", "expr", expressions);
    c2(feature, "set", "solnum", String.valueOf(solnum));
    c2(feature, "set", "edim", "domain");
    Object selection = c0(feature, "selection");
    c1(selection, "named", "sel3");
    Object raw = c0(feature, "getReal");
    if (!(raw instanceof double[][])) return new double[0][0];
    return normalize((double[][]) raw, expressions.length);
  }

  static int nearest(double[] values, double target) {
    int best = 0; double distance = Double.POSITIVE_INFINITY;
    for (int i = 0; i < values.length; i++) {
      if (!Double.isFinite(values[i])) continue;
      double current = Math.abs(values[i] - target);
      if (current < distance) { distance = current; best = i; }
    }
    return best;
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      Model model = ModelUtil.load("r581partialcurrent", MPH);
      System.out.println("PROBE,LOADED," + MPH + ",dataset=" + DATASET);
      double[] time = evalGlobal(model, "t");
      if (time.length != 1081) throw new RuntimeException("Expected 1081 time points; got " + time.length);
      String[] expressions = new String[FIELD.length];
      for (int i = 0; i < FIELD.length; i++) expressions[i] = FIELD[i][1];

      for (int snapshot = 0; snapshot < LABEL.length; snapshot++) {
        int index = nearest(time, Q_TARGET[snapshot] * 90.0);
        int solnum = index + 1;
        double q = 400.0 * time[index] / 36000.0;
        double[][] data = evalDomain(model, solnum, expressions);
        int rows = data.length == 0 ? 0 : data[0].length;
        System.out.println("SECTION," + LABEL[snapshot] + ",time_s," + fmt(time[index]) + ",Q," + fmt(q) + ",nrows," + rows);
        if (rows == 0) throw new RuntimeException("No spatial rows for " + LABEL[snapshot]);
        StringBuilder header = new StringBuilder("SPATIAL_HEADER,time_label,Q_mAh_cm2");
        for (String[] field : FIELD) header.append(",").append(field[0]);
        System.out.println(header.toString());
        for (int row = 0; row < rows; row++) {
          StringBuilder record = new StringBuilder("SPATIAL_ROW,").append(LABEL[snapshot]).append(",").append(fmt(q));
          for (int col = 0; col < FIELD.length; col++) record.append(",").append(fmt(data[col][row]));
          System.out.println(record.toString());
        }
      }
      System.out.println("PROBE,OK,no_solve_no_save");
      ModelUtil.remove("r581partialcurrent");
    } catch (Throwable t) {
      System.out.println("PROBE,FATAL," + t.getClass().getName() + "," + String.valueOf(t.getMessage()).replace(',', ';'));
      t.printStackTrace(System.out);
      System.exit(2);
    }
  }
}
