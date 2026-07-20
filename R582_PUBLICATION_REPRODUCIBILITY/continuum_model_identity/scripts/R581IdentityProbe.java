// R581 read-only identity probe. Loads only a verified copy; never solves or saves.
import com.comsol.model.*;
import com.comsol.model.util.*;
import java.lang.reflect.Method;
import java.util.Locale;

public class R581IdentityProbe {
  static final String MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_probe_input_COPY.mph";

  static Object call(Object target, String name, Class<?>[] types, Object... args) {
    if (target == null) return null;
    try { Method m = target.getClass().getMethod(name, types); return m.invoke(target, args); }
    catch (Throwable t) { return null; }
  }
  static Object c0(Object target, String name) { return call(target, name, new Class<?>[]{}); }
  static Object c1(Object target, String name, String a) { return call(target, name, new Class<?>[]{String.class}, a); }
  static Object c2(Object target, String name, String a, String b) { return call(target, name, new Class<?>[]{String.class,String.class}, a, b); }
  static Object c2a(Object target, String name, String a, String[] b) { return call(target, name, new Class<?>[]{String.class,String[].class}, a, b); }
  static String[] tags(Object manager) { Object o=c0(manager,"tags"); return o instanceof String[]?(String[])o:new String[0]; }
  static String clean(Object o) { return o==null?"":String.valueOf(o).replace('\n',' ').replace('\r',' ').replace(',',';'); }
  static String f(double x) { return Double.isFinite(x)?String.format(Locale.US,"%.12g",x):""; }

  static double[] eval(Model model, String dataset, String expr) {
    try {
      Object numerical = c0(c0(model,"result"),"numerical");
      String tag = "r581_" + Math.abs((dataset+expr+System.nanoTime()).hashCode());
      Object feature = c2(numerical,"create",tag,"EvalGlobal");
      c2(feature,"set","data",dataset);
      c2a(feature,"set","expr",new String[]{expr});
      Object raw = c0(feature,"getReal");
      if (!(raw instanceof double[][])) return null;
      double[][] values = (double[][])raw;
      return values.length==0?null:values[0];
    } catch(Throwable t) { return null; }
  }

  static void printEndpoint(Model model, String dataset, String label, String expr) {
    double[] values=eval(model,dataset,expr);
    if(values==null || values.length==0) {
      System.out.println("EVAL,"+dataset+","+label+",FAIL");
      return;
    }
    System.out.println("EVAL,"+dataset+","+label+",n="+values.length+",first="+f(values[0])+",last="+f(values[values.length-1]));
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      Model model=ModelUtil.load("r581probe",MPH);
      System.out.println("PROBE,LOADED,"+MPH);
      System.out.println("TAGS,studies,"+String.join("|",model.study().tags()));
      System.out.println("TAGS,solutions,"+String.join("|",model.sol().tags()));
      System.out.println("TAGS,meshes,"+String.join("|",model.component("comp1").mesh().tags()));

      Object datasetManager=c0(c0(model,"result"),"dataset");
      String[] datasets=tags(datasetManager);
      System.out.println("TAGS,datasets,"+String.join("|",datasets));
      for(String dataset:datasets) {
        Object feature=c1(datasetManager,"feature",dataset);
        if(feature==null) feature=model.result().dataset(dataset);
        System.out.println("DATASET,"+dataset+",type="+clean(c0(feature,"getType")));
        Object properties=c0(feature,"properties");
        if(properties instanceof String[]) {
          for(String property:(String[])properties) {
            Object value=c1(feature,"getString",property);
            if(value!=null) System.out.println("DSETPROP,"+dataset+","+property+","+clean(value));
          }
        }
        // Derived plot/helper datasets can trigger expensive interpolation.  The
        // identity audit only evaluates solution-backed datasets needed to map
        // historical and production branches.
        if(!(dataset.equals("dset1") || dataset.equals("dset4") ||
             dataset.equals("dset5") || dataset.equals("dset6"))) continue;
        printEndpoint(model,dataset,"Q_mAh_cm2","i_app*t/36000");
        printEndpoint(model,dataset,"V","tcd.phis0_ec1");
        printEndpoint(model,dataset,"S_direct","aveop1(cI2_surf_free/cI2_sat)");
        printEndpoint(model,dataset,"cI2_free","aveop1(cI2_surf_free)");
        printEndpoint(model,dataset,"cI2_total","aveop1(cI2_surf_tot)");
        printEndpoint(model,dataset,"beta","aveop1(beta_I2_surf_dyn)");
        printEndpoint(model,dataset,"cI_minus","aveop1(cI_m_surf_dyn)");
        printEndpoint(model,dataset,"eps_s","aveop1(eps_s_pos)");
        printEndpoint(model,dataset,"eps_s_reg","aveop1(eps_s_reg)");
        printEndpoint(model,dataset,"theta","aveop1(theta_eff_R520)");
        printEndpoint(model,dataset,"A_bare","aveop1(Av_bare_i2/av0_i2)");
        printEndpoint(model,dataset,"K_perm","aveop1(K_perm_rel_R520)");
      }

      Object variable=model.component("comp1").variable("varTry2I2");
      System.out.println("VARIABLE,cov_theta_surf,"+clean(c1(variable,"get","cov_theta_surf")));
      System.out.println("VARIABLE,theta_eff_R520,"+clean(c1(variable,"get","theta_eff_R520")));
      System.out.println("PARAM,i_app,"+clean(model.param().get("i_app")));
      System.out.println("PARAM,cI2_sat0,"+clean(model.param().get("cI2_sat0")));
      System.out.println("PARAM,gamma_I2_saltout,"+clean(model.param().get("gamma_I2_saltout")));
      System.out.println("PROBE,OK,no_solve_no_save");
      ModelUtil.remove("r581probe");
    } catch(Throwable t) {
      System.out.println("PROBE,FATAL,"+t.getClass().getName()+","+clean(t.getMessage()));
      t.printStackTrace(System.out);
    }
  }
}
