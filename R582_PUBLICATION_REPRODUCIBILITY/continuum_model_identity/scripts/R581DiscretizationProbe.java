// Read-only R581 probe for mesh and time-solver configuration.
import com.comsol.model.*;
import com.comsol.model.util.*;
import java.lang.reflect.Method;

public class R581DiscretizationProbe {
  static final String MPH="E:\\zifb_final_9129_luck\\battery_comsol\\02_outputs_core\\R581_CANONICAL_CLOSURE_REBUILD\\inputs\\R581_probe_input_COPY.mph";
  static Object call(Object t,String n,Class<?>[] ty,Object... a){if(t==null)return null;try{return t.getClass().getMethod(n,ty).invoke(t,a);}catch(Throwable x){return null;}}
  static Object c0(Object t,String n){return call(t,n,new Class<?>[]{});}
  static Object c1(Object t,String n,String a){return call(t,n,new Class<?>[]{String.class},a);}
  static String[] tags(Object m){Object o=c0(m,"tags");return o instanceof String[]?(String[])o:new String[0];}
  static String clean(Object o){return o==null?"":String.valueOf(o).replace('\n',' ').replace('\r',' ').replace(',',';');}
  static boolean interesting(String p){String s=p.toLowerCase();return s.contains("time")||s.contains("step")||s.contains("tol")||s.contains("order")||s.contains("strict")||s.contains("output")||s.contains("control")||s.contains("size")||s.contains("elem")||s.contains("quality")||s.contains("hauto")||s.contains("hmax")||s.contains("hmin")||s.contains("hgrad");}
  static void dumpTree(Object manager,String prefix,int depth){
    if(manager==null||depth>5)return;
    for(String tag:tags(manager)){
      Object f=c1(manager,"get",tag);if(f==null)f=c1(manager,"feature",tag);
      Object type=c0(f,"getType");
      System.out.println(prefix+"NODE,"+tag+",type="+clean(type));
      Object props=c0(f,"properties");
      if(props instanceof String[])for(String p:(String[])props)if(interesting(p)){
        Object v=c1(f,"getString",p);if(v==null){Object a=c1(f,"getStringArray",p);if(a instanceof String[])v=String.join("|",(String[])a);}
        System.out.println(prefix+"PROP,"+tag+","+p+","+clean(v));
      }
      dumpTree(c0(f,"feature"),prefix+"  ",depth+1);
    }
  }
  public static void main(String[] args){
    try{
      ModelUtil.initStandalone(false);ModelUtil.showProgress(false);
      Model m=ModelUtil.load("r581disc",MPH);
      System.out.println("DISC_PROBE,LOADED,no_solve_no_save");
      Object mesh=m.component("comp1").mesh("mesh1");
      System.out.println("MESH,mesh1");
      dumpTree(c0(mesh,"feature"),"MESH_",0);
      Object stat=c0(mesh,"stat");
      if(stat!=null){
        for(Method method:stat.getClass().getMethods()){
          String n=method.getName();String l=n.toLowerCase();
          if(method.getParameterCount()==0&&(l.contains("elem")||l.contains("quality")||l.contains("vertex")||l.contains("point"))){
            try{System.out.println("MESH_STAT,"+n+","+clean(method.invoke(stat)));}catch(Throwable t){}
          }
        }
      }
      System.out.println("SOLUTION,sol5");
      dumpTree(c0(m.sol("sol5"),"feature"),"SOL_",0);
      System.out.println("STUDY,stdR522");
      dumpTree(c0(m.study("stdR522"),"feature"),"STUDY_",0);
      System.out.println("DISC_PROBE,OK,no_solve_no_save");
      ModelUtil.remove("r581disc");
    }catch(Throwable t){System.out.println("DISC_PROBE,FATAL,"+t.getClass().getName()+","+clean(t.getMessage()));t.printStackTrace(System.out);}
  }
}
