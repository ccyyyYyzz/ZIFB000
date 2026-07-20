import com.comsol.model.*;
import com.comsol.model.util.*;
import java.lang.reflect.*;

public class R520BuildBlockageFeedbackNative {
  static final String INPUT = "outputs/R520_BLOCKAGE_FEEDBACK_NATIVE/comsol/ZIFB_R520_BLOCKAGE_FEEDBACK_NATIVE_BASECOPY.mph";
  static final String OUTPUT = "outputs/R520_BLOCKAGE_FEEDBACK_NATIVE/comsol/ZIFB_R520_BLOCKAGE_FEEDBACK_NATIVE.mph";

  static String clean(String s) {
    if (s == null) return "";
    return s.replace('\n',' ').replace('\r',' ').replace(',',';');
  }

  static void setTry(Object node, String prop, String value) {
    try {
      node.getClass().getMethod("set", String.class, String.class).invoke(node, prop, value);
      System.out.println("SET," + prop + "," + value + ",OK");
    } catch (Throwable t) {
      System.out.println("SET," + prop + "," + value + ",FAIL," + clean(t.getMessage()));
    }
  }

  static void setArrTry(Object node, String prop, String[] value) {
    try {
      node.getClass().getMethod("set", String.class, String[].class).invoke(node, prop, (Object)value);
      System.out.println("SETARR," + prop + "," + String.join("|", value) + ",OK");
    } catch (Throwable t) {
      System.out.println("SETARR," + prop + "," + String.join("|", value) + ",FAIL," + clean(t.getMessage()));
    }
  }

  static void setVarTry(Object varNode, String name, String expr, String descr) {
    try {
      varNode.getClass().getMethod("set", String.class, String.class).invoke(varNode, name, expr);
      System.out.println("VARSET," + name + "," + expr + ",OK");
      try {
        varNode.getClass().getMethod("descr", String.class, String.class).invoke(varNode, name, descr);
      } catch (Throwable ignored) {}
    } catch (Throwable t) {
      System.out.println("VARSET," + name + "," + expr + ",FAIL," + clean(t.getMessage()));
    }
  }

  static String getVar(Object varNode, String name) {
    try {
      return clean(String.valueOf(varNode.getClass().getMethod("get", String.class).invoke(varNode, name)));
    } catch (Throwable t) {
      return "";
    }
  }

  public static void main(String[] args) {
    try {
      ModelUtil.initStandalone(false);
      Model m = ModelUtil.load("r520", INPUT);
      System.out.println("LOAD," + INPUT + ",OK");
      m.label("ZIFB_R520_BLOCKAGE_FEEDBACK_NATIVE.mph");
      m.description("R520 native positive I2(s)-accessibility/blockage feedback branch. Built from R500 final native full-cell scaffold. Negative electrode and membrane remain scaffold. Native COMSOL I2s/eps_s_pos is the only solid iodine inventory. Added transparent porosity, transport, pore-throat and optional film-contact feedback switches; no capacity/current gates.");

      // Preserve old parameter values as audit aliases, then lock requested measured values.
      m.param().set("sigmal_R500_old", "60[S/m]", "R500 old liquid conductivity parameter retained for branch audit");
      m.param().set("V_res_R500_old", "29.25[cm^3]", "R500 old reservoir volume retained for branch audit");
      m.param().set("sigmal", "20[S/m]", "R520 measured 1 M ZnI2 + 4 M NH4Br conductivity: 0.20 S/cm = 20 S/m");
      m.param().set("V_res", "25[cm^3]", "R520 actual wetted reservoir/tank inventory volume used for positive iodine bookkeeping");

      // R520 feedback parameters: dimensioned, switchable, bounded.
      m.param().set("R520_porosity_on", "1", "R520 switch: 1 couples native I2(s) volume to positive-electrode liquid porosity; 0 reproduces R500 porosity baseline");
      m.param().set("R520_transport_on", "1", "R520 switch: 1 couples D and kappa_l to eps_l_eff; 0 keeps transport coefficients at R500 baseline");
      m.param().set("R520_porethroat_on", "1", "R520 switch: 1 multiplies accessible area by a pore-throat transmissibility factor; 0 keeps R500 theta-only area");
      m.param().set("R520_film_on", "0", "R520 switch: optional dense-I2 contact/film resistance sensitivity; default 0 so film is not the main mechanism");
      m.param().set("R520_theta_area_on", "1", "R520 switch: 1 applies native-I2(s)-derived surface coverage to soluble iodine reaction area; 0 keeps the full bare area for no-feedback ablation");
      m.param().set("D_eps_exp_R520", "1.5", "R520 bounded Bruggeman-like exponent for D_eff vs eps_l_eff");
      m.param().set("kappa_eps_exp_R520", "1.5", "R520 bounded Bruggeman-like exponent for ionic conductivity vs eps_l_eff");
      m.param().set("R520_area_perm_exp", "0.5", "R520 exponent mapping permeability loss to accessible-area transmissibility");
      m.param().set("chi_throat_R520", "1", "R520 throat-film shape factor h = chi_throat*delta_eff");
      m.param().set("kappa_I2_eff_R520", "1e-7[S/m]", "R520 bounded effective conductivity of iodine-rich covered contact path; sensitivity only");
      m.param().set("mu_electrolyte_R520", "2.2e-3[Pa*s]", "R520 electrolyte viscosity for frozen Darcy pressure estimate");
      m.param().set("K0_perm_R520", "1e-10[m^2]", "R520 nominal carbon-felt permeability scale for frozen Darcy estimate; not a fitted pressure threshold");

      Object varI2 = m.component("comp1").variable("varI2");
      setVarTry(varI2, "cOeq", "cBr2", "R520 paper-facing alias: total oxidized iodine-equivalent concentration. Internal COMSOL variable cBr2 is legacy naming.");
      setVarTry(varI2, "cI2_tot_R520", "cOeq", "R520 paper-facing alias for transported total oxidized iodine; no new species inventory.");

      Object varTry = m.component("comp1").variable("varTry2I2");
      System.out.println("OLD,epsl_try2_eff," + getVar(varTry, "epsl_try2_eff"));
      System.out.println("OLD,D_try2_eff," + getVar(varTry, "D_try2_eff"));
      System.out.println("OLD,sigmal_try2_eff," + getVar(varTry, "sigmal_try2_eff"));
      System.out.println("OLD,Av_bare_i2," + getVar(varTry, "Av_bare_i2"));
      System.out.println("OLD,Rfilm_i2," + getVar(varTry, "Rfilm_i2"));

      // Raw and effective porosity: no hidden clipping in the central expression. Non-negativity is audited post-solve.
      setVarTry(varTry, "eps_l_raw_R520", "epsl_cf-eps_s_pos", "R520 raw liquid porosity after native deposited I2(s); no clipping.");
      setVarTry(varTry, "eps_l_eff_R520", "epsl_cf-R520_porosity_on*eps_s_pos", "R520 liquid porosity used by positive porous electrode. Switch off gives R500 baseline epsl_cf.");
      setVarTry(varTry, "K_perm_rel_R520", "(eps_l_eff_R520/epsl_cf)^3*((1-epsl_cf)/(1-eps_l_eff_R520))^2", "R520 Kozeny-Carman-like permeability ratio from native I2(s) porosity loss.");
      setVarTry(varTry, "D_rel_R520", "(eps_l_eff_R520/epsl_cf)^(D_eps_exp_R520*R520_transport_on)", "R520 effective diffusivity ratio. Switch off exponent is zero.");
      setVarTry(varTry, "kappa_l_rel_R520", "(eps_l_eff_R520/epsl_cf)^(kappa_eps_exp_R520*R520_transport_on)", "R520 liquid conductivity ratio. Switch off exponent is zero.");
      setVarTry(varTry, "theta_eff_R520", "cov_theta_surf", "R520 effective surface coverage; central branch inherits R500 native-solid coverage until island-family sensitivity is applied in postprocess.");
      setVarTry(varTry, "delta_eff_R520", "eps_s_pos/(av0_i2*max(theta_eff_R520,1e-6))", "R520 effective iodine-rich layer thickness from native I2(s) inventory and coverage.");
      setVarTry(varTry, "h_throat_R520", "chi_throat_R520*delta_eff_R520", "R520 equivalent throat intrusion thickness.");
      setVarTry(varTry, "T_pore_R520", "(1-R520_porethroat_on)+R520_porethroat_on*K_perm_rel_R520^R520_area_perm_exp", "R520 pore-throat transmissibility multiplier for accessible area.");
      setVarTry(varTry, "RfA_R520", "R520_film_on*delta_eff_R520/kappa_I2_eff_R520", "R520 optional dense-iodine contact/film ASR. Default off.");
      setVarTry(varTry, "DeltaP_frozen_R520", "mu_electrolyte_R520*U*W_cf/(K0_perm_R520*K_perm_rel_R520)", "R520 frozen Darcy pressure-drop diagnostic, not a solved hydraulic pressure field.");

      // Overwrite R500 transparent variables with R520 physically explicit forms.
      setVarTry(varTry, "epsl_try2_eff", "eps_l_eff_R520", "R520 positive-electrode liquid porosity passed to COMSOL pce2; no clipping; audited for non-negativity.");
      setVarTry(varTry, "D_try2_eff", "D_Br2*D_rel_R520", "R520 D_eff for transported oxidized iodine-equivalent in pce2.");
      setVarTry(varTry, "sigmal_try2_eff", "sigmal*kappa_l_rel_R520", "R520 liquid conductivity in pce2 using measured sigmal and porosity feedback.");
      setVarTry(varTry, "Av_bare_i2", "av0_i2*(1-R520_theta_area_on*theta_eff_R520)*T_pore_R520", "R520 positive soluble iodine reaction area: native-I2(s) surface coverage and pore-throat accessibility with separate switches.");
      setVarTry(varTry, "Av_cov_i2", "av0_i2*(R520_theta_area_on*theta_eff_R520)", "R520 covered positive area. Zero in the no-feedback ablation; diagnostic if covered branch is inactive.");
      setVarTry(varTry, "Rfilm_i2", "delta_eff_R520/kappa_I2_eff_R520", "R520 physical dense-I2 contact-path ASR per covered area, used only if R520_film_on is enabled.");
      setVarTry(varTry, "Rfilm_area_i2", "RfA_R520*theta_eff_R520", "R520 optional surface film/contact resistance passed to COMSOL SurfaceResistance when enabled.");

      // Ensure pce2 is coupled to the R520 variables. These properties already existed in R500 and are updated here for clarity.
      Object pce2 = m.component("comp1").physics("tcd").feature("pce2");
      setTry(pce2, "epsl", "epsl_try2_eff");
      setTry(pce2, "D_cBr2", "D_try2_eff");
      setTry(pce2, "sigmal_mat", "userdef");
      setTry(pce2, "sigmal", "sigmal_try2_eff");
      setTry(pce2, "FilmResistanceType", "SurfaceResistance");
      setTry(pce2, "Rfilm", "Rfilm_area_i2");

      // Study: keep one J40 solve. Branch/ablation runs are created by changing the switch parameters in copied mph files.
      try {
        Object param = m.study("std1").feature("param");
        setArrTry(param, "pname", new String[]{"i_app", "t_charge", "k_diss_new"});
        setArrTry(param, "plistarr", new String[]{"400[A/m^2]", "20000[s]", "0.01[1/s]"});
        setArrTry(param, "punit", new String[]{"A/m^2", "s", "1/s"});
      } catch (Throwable t) {
        System.out.println("STUDY_PARAM_UPDATE_FAIL," + clean(t.getMessage()));
      }

      m.save(OUTPUT);
      System.out.println("SAVE," + OUTPUT + ",OK");
      ModelUtil.remove("r520");
    } catch (Throwable t) {
      System.out.println("FATAL," + t.getClass().getName() + "," + clean(t.getMessage()));
      t.printStackTrace(System.out);
    }
  }
}
