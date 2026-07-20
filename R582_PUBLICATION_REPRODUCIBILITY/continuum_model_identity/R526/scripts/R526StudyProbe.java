import com.comsol.model.Model;
import com.comsol.model.util.ModelUtil;

public class R526StudyProbe {
  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      ModelUtil.showProgress(false);
      Model model = ModelUtil.load("probe", "outputs/R523_IMAGE_MESH_REPAIR/comsol/ZIFB_R523_NATIVE_FPF_COUPLED_REFINED_SOLVED.mph");
      System.out.println("STUDY_TAGS," + String.join("|", model.study().tags()));
      String st = "stdR522";
      System.out.println("FEATURE_TAGS," + st + "," + String.join("|", model.study(st).feature().tags()));
      for (String tag : model.study(st).feature().tags()) {
        try {
          System.out.println("FEATURE," + tag + ",type," + model.study(st).feature(tag).getType());
        } catch (Throwable t) {
          System.out.println("FEATURE," + tag + ",type_fail," + t.getMessage());
        }
        for (String key : new String[]{"tlist","tunit","tout","useinitsol","solnum","notsolmethod"}) {
          try {
            System.out.println("PROP," + tag + "," + key + "," + model.study(st).feature(tag).getString(key));
          } catch (Throwable ignored) {}
        }
      }
      ModelUtil.remove("probe");
    } catch (Throwable t) {
      System.out.println("PROBE_FAIL," + t.getClass().getName() + ":" + t.getMessage());
      t.printStackTrace(System.out);
    }
  }
}
