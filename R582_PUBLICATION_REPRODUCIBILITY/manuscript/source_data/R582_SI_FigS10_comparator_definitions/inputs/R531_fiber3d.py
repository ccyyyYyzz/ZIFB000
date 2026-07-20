#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
R531 — 3D single-fiber iodine deposition + accessibility model (battery-calibrated, bounded).

A representative cylindrical UNIT CELL of the compressed graphite felt:
  carbon fiber radius r_f = 7.5 um  (gives specific area a_s = 4e4 m^-1 at porosity 0.85)
  electrolyte annulus out to r_out = r_f/sqrt(1-eps) = 19.36 um  ->  porosity exactly 0.85
  segment length L_z = 150 um, J40 = 40 mA cm^-2.

Three genuinely-3D ingredients:
  1. solid accumulation V_s(Q) = phi_ppt * generation (constant precipitation fraction; the rest of
     the oxidized iodine stays soluble/complexed and washes out). phi_ppt calibrated to COMSOL eps_s.
  2. 3D fiber-surface island nucleation + growth with TRUE geometric coalescence -> theta_geo(Q),
     deposit volume, connected-cluster count (resolved on the cylinder surface).
  3. 3D cylindrical finite-difference diffusion in the electrolyte annulus around the partially
     covered fiber -> diffusion-limited ACCESSIBILITY a(theta_geo); theta_eff = 1 - accessibility.

This PHYSICALLY DERIVES the accessibility-loss closure theta_eff(eps_s) that the R500/R523 COMSOL
model uses as an algebraic closure -> a direct multi-scale complement to COMSOL. COMSOL is not used.

Bounded mechanistic model. DFT energies are tabulated for reference only and do NOT enter this
model (R531 nucleation is uniform-random); DFT-weighted clustered nucleation is implemented in R532.
"""
import os, json
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.sparse.linalg as spla

np.random.seed(531)
OUTBASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB=os.path.join(OUTBASE,"tables"); FSD=os.path.join(OUTBASE,"figure_source_data")
LOG=os.path.join(OUTBASE,"logs")
for d in (TAB,FSD,LOG): os.makedirs(d,exist_ok=True)
PROOT=os.path.dirname(os.path.dirname(OUTBASE)); POUT=os.path.join(PROOT,"outputs")

# ---- battery-calibrated constants ----
F=96485.0; EPS=0.85; A_S=4.0e4
R_F=(1-EPS)*2/A_S                 # 7.5e-6 m
R_OUT=R_F/np.sqrt(1-EPS)          # 19.36e-6 m  -> porosity exactly EPS
L_Z=150e-6                        # m segment
CI2_SAT=1.33; VM_I2=5.15e-5; D_I2=0.5e-9
I_APP=400.0; L_ELEC=2.0e-3
J_GEN=I_APP/(2*F)/(A_S*L_ELEC)    # mol m^-2 s^-1 per TRUE surface area (2 e- per I2)
Q_END=120.0; T_END=Q_END/40.0*3600.0  # s
SHELL_VOL=np.pi*(R_OUT**2-R_F**2)*L_Z
SURF_AREA=2*np.pi*R_F*L_Z
DFT_ADS={"basal":-0.403,"C=O":-0.848,"C-OH":-0.998,"vacancy":-0.318}

log_lines=[]
def log(*a):
    s=" ".join(str(x) for x in a); print(s); log_lines.append(s)

def interp_cross(x,y,thr,rising=True):
    x=np.asarray(x,float); y=np.asarray(y,float)
    for i in range(1,len(x)):
        a,b=y[i-1],y[i]
        if (rising and a<thr<=b) or ((not rising) and a>thr>=b):
            return float(x[i-1]+(x[i]-x[i-1])*(thr-a)/(b-a)) if b!=a else float(x[i])
    return None

# ---------------- 3D surface morphology (true coalescence) ----------------
def nucleation_sites(n_n):
    """Uniform-random (Poisson) nucleation on the fibre surface. DFT-weighted CLUSTERED nucleation
    (C-OH-seeded) is implemented as a separate physical mode in the R532 refinement."""
    N=max(1,int(round(n_n*SURF_AREA)))
    th=np.random.rand(N)*2*np.pi; z=np.random.rand(N)*L_Z
    return th,z,N

def coverage_raster(th_s,z_s,a, Nth=64,Nz=64):
    """Boolean covered mask (Nth x Nz) for cap base radius a, via periodic cKDTree nearest-site
    geodesic distance on the unrolled cylinder (arc-length, z). Fast for many sites."""
    from scipy.spatial import cKDTree
    if a<=0 or len(th_s)==0:
        return np.zeros((Nth,Nz),bool), np.zeros((Nth,Nz))
    arc=2*np.pi*R_F
    sites=np.column_stack([(np.asarray(th_s)/(2*np.pi))*arc, np.asarray(z_s)%L_Z])
    tree=cKDTree(sites, boxsize=[arc, L_Z])
    th=(np.arange(Nth)+0.5)/Nth*2*np.pi; z=(np.arange(Nz)+0.5)/Nz*L_Z
    TH,ZZ=np.meshgrid(th,z,indexing="ij")
    pts=np.column_stack([(TH.ravel()/(2*np.pi))*arc, ZZ.ravel()])
    d,_=tree.query(pts,k=1); d=d.reshape(Nth,Nz)
    covered=d<a
    height=np.sqrt(np.maximum(a**2-d**2,0.0))
    return covered,height

def count_clusters(covered):
    """4-connected clusters on the cylinder surface, with azimuth (axis 0) periodic merge."""
    from scipy import ndimage
    lab,n=ndimage.label(covered)
    if n==0: return 0
    for j in range(covered.shape[1]):           # merge clusters wrapping theta=0 / theta=2pi
        if covered[0,j] and covered[-1,j] and lab[0,j]!=lab[-1,j]:
            lab[lab==lab[-1,j]]=lab[0,j]
    return len(np.unique(lab[lab>0]))

# ---------------- 3D cylindrical diffusion accessibility (vectorized) ----------------
_GRID={}
def _grid(Nr,Nth,Nz):
    key=(Nr,Nth,Nz)
    if key in _GRID: return _GRID[key]
    r=np.linspace(R_F,R_OUT,Nr); dr=r[1]-r[0]; dth=2*np.pi/Nth; dz=L_Z/Nz
    ii,jj,kk=np.meshgrid(np.arange(Nr),np.arange(Nth),np.arange(Nz),indexing="ij")
    n=((ii*Nth+jj)*Nz+kk)
    ri=r[ii]
    nrp=(((ii+1)*Nth+jj)*Nz+kk); nrm=(((ii-1)*Nth+jj)*Nz+kk)
    ntp=((ii*Nth+(jj+1)%Nth)*Nz+kk); ntm=((ii*Nth+(jj-1)%Nth)*Nz+kk)
    nzp=((ii*Nth+jj)*Nz+(kk+1)%Nz); nzm=((ii*Nth+jj)*Nz+(kk-1)%Nz)
    cp=(1.0/dr**2+1.0/(2*ri*dr)); cm=(1.0/dr**2-1.0/(2*ri*dr))
    cth=1.0/(ri**2*dth**2); cz=np.full_like(ri,1.0/dz**2)
    g=dict(Nr=Nr,Nth=Nth,Nz=Nz,r=r,dr=dr,dth=dth,dz=dz,Ntot=Nr*Nth*Nz,
        n=n.ravel(),ii=ii.ravel(),nrp=nrp.ravel(),nrm=nrm.ravel(),ntp=ntp.ravel(),ntm=ntm.ravel(),
        nzp=nzp.ravel(),nzm=nzm.ravel(),cp=cp.ravel(),cm=cm.ravel(),cth=cth.ravel(),cz=cz.ravel())
    _GRID[key]=g; return g

def _flux(cov, g):
    """cov = covered (blocked) inner-surface mask (Nth,Nz). Bare cells (~cov) react (c=0 Dirichlet);
    covered cells are no-flux; outer boundary c=1. Returns total diffusive flux onto the bare wall."""
    Nr,Nth,Nz=g["Nr"],g["Nth"],g["Nz"]; Ntot=g["Ntot"]
    n=g["n"]; ii=g["ii"]
    covflat=np.zeros(Ntot,bool)
    inner_idx=((0*Nth+np.arange(Nth)[:,None])*Nz+np.arange(Nz)[None,:]).ravel()
    covflat[inner_idx]=cov.ravel()
    outer=ii==(Nr-1); inner=ii==0
    react_inner=inner&(~covflat)             # BARE inner -> Dirichlet c=0 (fast reaction)
    Dirichlet=outer|react_inner
    IL=~Dirichlet                            # interior-like (incl covered-inner no-flux)
    R=[];C=[];V=[]; DS=[]; DV=[]
    def add(mask,col,coef):
        s=n[mask]; cv=coef[mask]; R.append(s);C.append(col[mask]);V.append(cv); DS.append(s); DV.append(-cv)
    A=IL&inner                               # covered-inner: no-flux mirror to i+1
    add(A,g["nrp"],np.full(Ntot,2.0/g["dr"]**2))
    B=IL&(ii>0)                              # i in 1..Nr-2: both radial neighbours
    add(B,g["nrp"],g["cp"]); add(B,g["nrm"],g["cm"])
    add(IL,g["ntp"],g["cth"]); add(IL,g["ntm"],g["cth"])
    add(IL,g["nzp"],g["cz"]);  add(IL,g["nzm"],g["cz"])
    diag=np.bincount(np.concatenate(DS),weights=np.concatenate(DV),minlength=Ntot)
    R.append(n[IL]);C.append(n[IL]);V.append(diag[IL])
    R.append(n[Dirichlet]);C.append(n[Dirichlet]);V.append(np.ones(Dirichlet.sum()))
    rows=np.concatenate(R);cols=np.concatenate(C);vals=np.concatenate(V)
    rhs=np.zeros(Ntot); rhs[outer]=1.0
    Amat=sp.csr_matrix((vals,(rows,cols)),shape=(Ntot,Ntot))
    c=spla.spsolve(Amat,rhs).reshape(Nr,Nth,Nz)
    dA=R_F*g["dth"]*g["dz"]
    bare=~cov
    flux=np.sum(D_I2*(c[1][bare]-0.0)/g["dr"]*dA)   # reactive flux on BARE cells (c=0 wall)
    return flux

def solve_accessibility(covered, Nr=8, Nth=36, Nz=36):
    """accessibility = reactive flux(partial coverage) / reactive flux(fully bare fibre)."""
    g=_grid(Nr,Nth,Nz)
    # downsample covered to (Nth,Nz) if needed
    if covered.shape!=(Nth,Nz):
        ci=(np.arange(Nth)*covered.shape[0]//Nth); cj=(np.arange(Nz)*covered.shape[1]//Nz)
        covered=covered[np.ix_(ci,cj)]
    key=("fbare",Nr,Nth,Nz)
    if key not in _GRID:
        _GRID[key]=_flux(np.zeros((Nth,Nz),bool), g)   # fully BARE fibre reference
    f_bare=_GRID[key]
    f_cov=_flux(covered.astype(bool), g)
    return f_cov/f_bare if f_bare>0 else np.nan

# ---------------- main: drive a case, snapshot 3D + accessibility ----------------
def run_case(phi_ppt, n_n, label, snapshots=(0.1,0.3,0.5,0.7,1.0)):
    """phi_ppt = fraction of generated I2 that precipitates as solid on the fibre (rest stays
    soluble/complexed by NH4Br/I- and is washed out). Calibrated so baseline phi~5e-3 gives the
    COMSOL endpoint eps_s~3.2e-3 at Q120 -> the model operates at the battery's real solid scale."""
    dVs_dt=phi_ppt*J_GEN*VM_I2                          # m3 m^-2 s^-1 solid growth per true area
    th_s,z_s,N=nucleation_sites(n_n)
    rows=[]
    for frac in snapshots:
        t=frac*T_END; Q=frac*Q_END
        vs_area=dVs_dt*t                                # m3 m^-2 (solid vol per true area)
        Vs_total=vs_area*SURF_AREA                      # m3 on the segment
        v_i=Vs_total/N if N>0 else 0.0
        a=(3*v_i/(2*np.pi))**(1/3) if v_i>0 else 0.0    # cap base radius
        covered,height=coverage_raster(th_s,z_s,a)
        theta_geo=covered.mean()
        eps_s=Vs_total/SHELL_VOL                         # solid volume fraction of unit cell
        ncl=count_clusters(covered) if theta_geo>0 else 0
        acc=solve_accessibility(covered) if theta_geo>0 else 1.0
        rows.append(dict(label=label,phi_ppt=phi_ppt,n_n_m2=n_n,Q_mAh_cm2=Q,
            vs_area_m3m2=vs_area, eps_s=eps_s,
            cap_radius_um=a*1e6, n_islands=N, n_clusters=ncl, theta_geo=theta_geo,
            accessibility=acc, theta_eff_transport=1-acc))
    return pd.DataFrame(rows),(th_s,z_s)

def comsol_theta_ref(eps_s, eps_s_ref=3.22e-3, theta_ref=0.99):
    """R523/R528 baseline endpoint (eps_s~3.2e-3 -> theta_eff~0.99): a saturating algebraic closure
    theta = 1-exp(-k*eps_s) calibrated to that single point, for side-by-side comparison only."""
    k=-np.log(1-theta_ref)/eps_s_ref
    return 1-np.exp(-k*np.asarray(eps_s))

if __name__=="__main__":
    log("R531 3D single-fiber model — start")
    log(f"geometry: r_f={R_F*1e6:.2f}um r_out={R_OUT*1e6:.2f}um L_z={L_Z*1e6:.0f}um eps={EPS} "
        f"a_s={A_S:.0e} j_gen={J_GEN:.3e} mol/m2/s")
    # representative cases at the battery's real solid scale (phi_ppt calibrated to COMSOL eps_s)
    cases=[(1e-3,1e13,"washable"),(5e-3,1e13,"baseline_comsol"),
           (5e-3,1e11,"baseline_lowNn"),(2e-2,1e14,"retained_highNn")]
    allc=[]; sites={}
    for phi,nn,lab in cases:
        df,sxy=run_case(phi,nn,lab); allc.append(df); sites[lab]=sxy
        end=df.iloc[-1]
        log(f"  {lab}: phi_ppt={phi:.1e} n_n={nn:.0e} -> end theta_geo={end.theta_geo:.3f} "
            f"eps_s={end.eps_s:.2e} accessibility={end.accessibility:.3f} clusters={end.n_clusters}")
    big=pd.concat(allc,ignore_index=True)
    big.to_csv(os.path.join(TAB,"R531_fiber3d_clock.csv"),index=False)
    big.to_csv(os.path.join(FSD,"R531_fiber3d_clock.csv"),index=False)

    # accessibility closure theta_eff(eps_s): pool all snapshots with deposit, compare to COMSOL ref
    clo=big[big.theta_geo>0][["eps_s","theta_geo","accessibility","theta_eff_transport","label"]].copy()
    clo["one_minus_theta_geo"]=1-clo["theta_geo"]
    clo["comsol_theta_ref"]=comsol_theta_ref(clo["eps_s"].values)
    clo=clo.sort_values("eps_s")
    clo.to_csv(os.path.join(TAB,"R531_fiber3d_accessibility_closure.csv"),index=False)
    clo.to_csv(os.path.join(FSD,"R531_fiber3d_accessibility_closure.csv"),index=False)
    log(f"  accessibility closure: {len(clo)} points; theta_eff_transport range "
        f"{clo.theta_eff_transport.min():.3f}..{clo.theta_eff_transport.max():.3f}")

    # save a morphology snapshot (height map) for the 3D render: baseline_comsol at Q~72 (frac 0.6)
    phi,nn,lab=5e-3,1e13,"baseline_comsol"
    th_s,z_s=sites[lab]
    dVs_dt=phi*J_GEN*VM_I2
    vs_area=dVs_dt*(0.6*T_END); Vs_total=vs_area*SURF_AREA; v_i=Vs_total/len(th_s)
    a=(3*v_i/(2*np.pi))**(1/3)
    cov,height=coverage_raster(th_s,z_s,a,Nth=96,Nz=96)
    np.savez(os.path.join(FSD,"R531_fiber3d_morphology.npz"),height=height,covered=cov,
             r_f=R_F,L_z=L_Z,a_um=a*1e6,theta_geo=cov.mean(),label=lab)
    log(f"  saved 3D morphology snapshot ({lab}, theta_geo={cov.mean():.3f}, cap a={a*1e6:.2f}um)")
    with open(os.path.join(LOG,"R531_fiber3d_log.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    log("R531 3D single-fiber model COMPLETE")
