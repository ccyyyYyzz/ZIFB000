// R581 mesh-only build probe. This class never runs a study or saves over an input.
import com.comsol.model.*;
import com.comsol.model.util.*;

import java.lang.reflect.Method;

public class R581TrueMeshBuildProbe {
  static final String INPUT_MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_true_mesh_probe_input_COPY.mph";
  static final String OUTPUT_MPH = "E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\outputs\\R581_true_mesh_probe_MESHED_ONLY.mph";
  static final long EXPECTED_INPUT_ELEMENTS = 1944L;
  static final String HMAX = "0.00067";
  static final String HMIN = "3e-6";
  static final String HGRAD = "1.2";
  static final int DIS1_NUMELEM = 36;
  static final int DIS2_NUMELEM = 36;
  static final int DIS3_NUMELEM = 72;

  static Object call(Object target, String name, Class<?>[] types, Object... args) {
    if (target == null) return null;
    try {
      Method method = target.getClass().getMethod(name, types);
      return method.invoke(target, args);
    } catch (Throwable t) {
      return null;
    }
  }

  static Object c0(Object target, String name) {
    return call(target, name, new Class<?>[]{});
  }

  static Object c1(Object target, String name, String arg) {
    return call(target, name, new Class<?>[]{String.class}, arg);
  }

  static String clean(Object value) {
    return value == null ? "" : String.valueOf(value).replace('\n', ' ').replace('\r', ' ').replace(',', ';');
  }

  static long asLong(Object value, String label) {
    if (value instanceof Number) return ((Number) value).longValue();
    try {
      return Long.parseLong(clean(value));
    } catch (Throwable t) {
      throw new IllegalStateException("Could not parse " + label + " from " + clean(value));
    }
  }

  static String property(Object feature, String name) {
    Object value = c1(feature, "getString", name);
    if (value == null) value = c1(feature, "get", name);
    return clean(value);
  }

  static void require(boolean condition, String message) {
    if (!condition) throw new IllegalStateException(message);
  }

  static void printMeshState(String phase, Object mesh, Object size, Object dis1, Object dis2, Object dis3) {
    Object stat = c0(mesh, "stat");
    System.out.println(
      "TRUE_MESH_STATE," + phase
      + ",elements=" + clean(c0(stat, "getNumElem"))
      + ",vertices=" + clean(c0(stat, "getNumVertex"))
      + ",min_quality=" + clean(c0(stat, "getMinQuality"))
      + ",mean_quality=" + clean(c0(stat, "getMeanQuality"))
    );
    System.out.println(
      "TRUE_MESH_SIZE," + phase
      + ",custom=" + property(size, "custom")
      + ",hmax=" + property(size, "hmax")
      + ",hmin=" + property(size, "hmin")
      + ",hgrad=" + property(size, "hgrad")
      + ",hauto=" + property(size, "hauto")
    );
    System.out.println(
      "TRUE_MESH_DISTRIBUTIONS," + phase
      + ",dis1=" + property(dis1, "numelem")
      + ",dis2=" + property(dis2, "numelem")
      + ",dis3=" + property(dis3, "numelem")
    );
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(true);
      System.out.println("TRUE_MESH_PROBE_START,mesh_only_no_study_run");
      System.out.println("TRUE_MESH_INPUT," + INPUT_MPH);
      System.out.println("TRUE_MESH_OUTPUT," + OUTPUT_MPH);
      Model model = ModelUtil.load("r581_true_mesh_probe", INPUT_MPH);
      Object mesh = model.component("comp1").mesh("mesh1");
      Object size = model.component("comp1").mesh("mesh1").feature("size");
      Object map1 = model.component("comp1").mesh("mesh1").feature("map1");
      Object dis1 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis1");
      Object dis2 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis2");
      Object dis3 = model.component("comp1").mesh("mesh1").feature("map1").feature("dis3");
      require(mesh != null && size != null && map1 != null && dis1 != null && dis2 != null && dis3 != null,
              "Required mesh feature missing");

      long beforeElements = asLong(c0(c0(mesh, "stat"), "getNumElem"), "input element count");
      require(beforeElements == EXPECTED_INPUT_ELEMENTS,
              "Unexpected input element count: " + beforeElements + " != " + EXPECTED_INPUT_ELEMENTS);
      printMeshState("before", mesh, size, dis1, dis2, dis3);

      // The default size is made explicitly custom. The mapped mesh has explicit
      // edge distributions, so their counts must also be refined; changing only
      // hauto/hmax leaves this model at 1944 elements.
      model.component("comp1").mesh("mesh1").feature("size").set("custom", "on");
      model.component("comp1").mesh("mesh1").feature("size").set("hmax", HMAX);
      model.component("comp1").mesh("mesh1").feature("size").set("hmin", HMIN);
      model.component("comp1").mesh("mesh1").feature("size").set("hgrad", HGRAD);
      model.component("comp1").mesh("mesh1").feature("map1").feature("dis1").set("numelem", DIS1_NUMELEM);
      model.component("comp1").mesh("mesh1").feature("map1").feature("dis2").set("numelem", DIS2_NUMELEM);
      model.component("comp1").mesh("mesh1").feature("map1").feature("dis3").set("numelem", DIS3_NUMELEM);
      model.component("comp1").mesh("mesh1").run();

      long afterElements = asLong(c0(c0(mesh, "stat"), "getNumElem"), "refined element count");
      printMeshState("after", mesh, size, dis1, dis2, dis3);
      require(afterElements != beforeElements,
              "True-mesh probe failed: element count remained " + afterElements);
      require(afterElements > beforeElements,
              "True-mesh probe failed: refined element count did not increase");

      model.save(OUTPUT_MPH);
      System.out.println("TRUE_MESH_MESHED_MODEL_SAVED," + OUTPUT_MPH);
      System.out.println(
        "TRUE_MESH_PROBE_OK,before_elements=" + beforeElements
        + ",after_elements=" + afterElements
        + ",ratio=" + ((double) afterElements / (double) beforeElements)
        + ",no_study_run=true"
      );
      ModelUtil.remove("r581_true_mesh_probe");
    } catch (Throwable t) {
      System.out.println("TRUE_MESH_PROBE_FATAL," + t.getClass().getName() + "," + clean(t.getMessage()));
      t.printStackTrace(System.out);
    }
  }
}
