// R581 read-only kinetics/physics-feature probe.
// Loads only the verified probe copy; never solves, mutates, or saves the model.
import com.comsol.model.*;
import com.comsol.model.util.*;
import java.lang.reflect.Array;
import java.lang.reflect.Method;
import java.util.Locale;

public class R581KineticsFeatureProbe {
  static final String MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_probe_input_COPY.mph";

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

  static Object c1(Object target, String name, String value) {
    return call(target, name, new Class<?>[]{String.class}, value);
  }

  static String[] tags(Object manager) {
    Object value = c0(manager, "tags");
    return value instanceof String[] ? (String[]) value : new String[0];
  }

  static String clean(Object value) {
    if (value == null) return "";
    if (value.getClass().isArray()) {
      int n = Array.getLength(value);
      StringBuilder out = new StringBuilder();
      for (int i = 0; i < n; i++) {
        if (i > 0) out.append("|");
        out.append(clean(Array.get(value, i)));
      }
      return out.toString();
    }
    return String.valueOf(value)
      .replace('\n', ' ')
      .replace('\r', ' ')
      .replace(',', ';');
  }

  static boolean relevant(String text) {
    String value = text.toLowerCase(Locale.ROOT);
    return value.contains("i0") || value.contains("exchange") ||
           value.contains("eeq") || value.contains("equilibrium") ||
           value.contains("alpha") || value.contains("butler") ||
           value.contains("overpotential") || value.contains("theta") ||
           value.contains("av_bare") || value.contains("i2") ||
           value.contains("iod") || value.contains("br");
  }

  static void printProperties(String path, Object feature) {
    Object label = c0(feature, "label");
    Object type = c0(feature, "getType");
    Object active = c0(feature, "isActive");
    System.out.println("FEATURE," + path + ",type=" + clean(type) + ",label=" + clean(label) + ",active=" + clean(active));
    Object props = c0(feature, "properties");
    if (!(props instanceof String[])) return;
    for (String prop : (String[]) props) {
      Object value = c1(feature, "get", prop);
      if (value == null || clean(value).isEmpty()) value = c1(feature, "getString", prop);
      String record = prop + "=" + clean(value);
      if (relevant(path) || relevant(clean(label)) || relevant(record)) {
        System.out.println("PROPERTY," + path + "," + prop + "," + clean(value));
      }
    }
  }

  static void walkFeature(String path, Object feature, int depth) {
    printProperties(path, feature);
    if (depth >= 4) return;
    Object childManager = c0(feature, "feature");
    for (String child : tags(childManager)) {
      Object childFeature = c1(childManager, "feature", child);
      if (childFeature == null) childFeature = c1(feature, "feature", child);
      walkFeature(path + "/" + child, childFeature, depth + 1);
    }
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      Model model = ModelUtil.load("r581kineticsprobe", MPH);
      System.out.println("PROBE,LOADED," + MPH);
      Object component = model.component("comp1");
      Object physicsManager = c0(component, "physics");
      String[] physicsTags = tags(physicsManager);
      System.out.println("TAGS,physics," + String.join("|", physicsTags));
      for (String physicsTag : physicsTags) {
        Object physics = c1(physicsManager, "physics", physicsTag);
        if (physics == null) physics = model.component("comp1").physics(physicsTag);
        printProperties("physics/" + physicsTag, physics);
        Object featureManager = c0(physics, "feature");
        for (String featureTag : tags(featureManager)) {
          Object feature = c1(featureManager, "feature", featureTag);
          if (feature == null) feature = c1(physics, "feature", featureTag);
          walkFeature("physics/" + physicsTag + "/" + featureTag, feature, 0);
        }
      }
      Object i2ode = model.component("comp1").physics("i2ode");
      Object dode = c1(c0(i2ode, "feature"), "feature", "dode1");
      if (dode == null) dode = c1(i2ode, "feature", "dode1");
      for (String prop : new String[]{"f", "da", "ea"}) {
        System.out.println("DODE_MATRIX," + prop + "," + clean(c1(dode, "getStringMatrix", prop)));
        System.out.println("DODE_ARRAY," + prop + "," + clean(c1(dode, "getStringArray", prop)));
      }
      Object fieldManager = c0(i2ode, "field");
      System.out.println("TAGS,i2ode_fields," + String.join("|", tags(fieldManager)));
      for (String fieldTag : tags(fieldManager)) {
        Object field = c1(fieldManager, "field", fieldTag);
        System.out.println("I2ODE_FIELD," + fieldTag + ",name=" + clean(c0(field, "fieldName")) + ",components=" + clean(c0(field, "component")));
      }
      System.out.println("PARAM,Eeq_ref_I," + clean(model.param().get("Eeq_ref_I")));
      System.out.println("PARAM,E0_I2_I," + clean(model.param().get("E0_I2_I")));
      System.out.println("PARAM,i0_ref_I," + clean(model.param().get("i0_ref_I")));
      System.out.println("PARAM,alpha_a_Br," + clean(model.param().get("alpha_a_Br")));
      System.out.println("PARAM,alpha_c_Br," + clean(model.param().get("alpha_c_Br")));
      System.out.println("PROBE,OK,no_solve_no_save");
      ModelUtil.remove("r581kineticsprobe");
    } catch (Throwable t) {
      System.out.println("PROBE,FATAL," + t.getClass().getName() + "," + clean(t.getMessage()));
      t.printStackTrace(System.out);
      System.exit(2);
    }
  }
}
