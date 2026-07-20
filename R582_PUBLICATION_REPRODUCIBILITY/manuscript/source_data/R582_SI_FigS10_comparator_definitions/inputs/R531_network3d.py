#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
R531 — 3D pore-throat network blockage model (battery-calibrated graphite felt, bounded).

A 3D cubic pore network calibrated to the compressed felt: lattice spacing l=60 um, lognormal throat
radii (seed median ~15 um) rescaled so the network porosity = 0.85 (matching the felt). Hydraulic
conductance g_h ~ r^4/l (Poiseuille), ionic/diffusive g_i ~ r^2/l. Sparse Laplace solves
(scipy) under a through-plane pressure drop give relative permeability and ionic accessibility as
iodine deposits and shrinks throat radii under six allocation laws. 3D connectivity (percolation)
is tracked.

COMSOL LINK: the network derives K_perm(eps_s) and accessibility(eps_s) — the closures the R500/R523
COMSOL model uses as the continuum Kozeny-Carman law K=(el/el0)^3((1-el0)/(1-el))^2. We overlay the
two and mark the COMSOL baseline operating point (eps_s ~ 3.2e-3) to show why discrete clogging is
negligible at baseline (K~unity, as R528 found) yet can dominate under localized deposition / high
load. COMSOL is not used; no .mph touched. Bounded mechanistic model.
"""
import os
import numpy as np
import pandas as pd
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import scipy.sparse.csgraph as csg

np.random.seed(531)
OUTBASE=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB=os.path.join(OUTBASE,"tables"); FSD=os.path.join(OUTBASE,"figure_source_data"); LOG=os.path.join(OUTBASE,"logs")
for d in (TAB,FSD,LOG): os.makedirs(d,exist_ok=True)

EPS=0.85; L_THROAT=60e-6; R_MIN=5e-7
Q_PORE_FILL=176.9; EPS_S_COMSOL=3.22e-3   # R523/R528 baseline endpoint eps_s

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

def build_network(nx=15,ny=15,nz=15,r0_med=15e-6,sigma=0.45,target_eps=EPS):
    N=nx*ny*nz
    nid=np.arange(N).reshape(nx,ny,nz)
    e0=[];e1=[];axis=[]
    for ax,sh in enumerate([(1,0,0),(0,1,0),(0,0,1)]):
        a=nid[:nx-sh[0] or None,:ny-sh[1] or None,:nz-sh[2] or None]
        b=nid[sh[0]:,sh[1]:,sh[2]:]
        e0.append(a.ravel()); e1.append(b.ravel()); axis.append(np.full(a.size,ax))
    e0=np.concatenate(e0); e1=np.concatenate(e1); axis=np.concatenate(axis)
    r0=np.exp(np.log(r0_med)+sigma*np.random.randn(len(e0))); r0=np.clip(r0,2*R_MIN,None)
    tot_vol=(nx*L_THROAT)*(ny*L_THROAT)*(nz*L_THROAT)
    # auto-calibrate throat radii so network porosity == target_eps (lognormal inflates mean r^2)
    eps_raw=np.sum(np.pi*r0**2*L_THROAT)/tot_vol
    r0=r0*np.sqrt(target_eps/eps_raw)
    pore_vol=np.sum(np.pi*r0**2*L_THROAT); eps_net=pore_vol/tot_vol
    inlet=nid[0,:,:].ravel(); outlet=nid[nx-1,:,:].ravel()
    fixed=np.zeros(N,bool); fixed[inlet]=True; fixed[outlet]=True
    fval=np.zeros(N); fval[inlet]=1.0
    coords=np.array(np.unravel_index(np.arange(N),(nx,ny,nz))).T.astype(float)
    inset=np.zeros(N,bool); inset[inlet]=True
    edge_inlet_mask=inset[e0]^inset[e1]          # edges crossing the inlet face (precomputed once)
    xe=(coords[e0,0]+coords[e1,0])/2.0           # edge through-plane position (precomputed once)
    return dict(N=N,nx=nx,ny=ny,nz=nz,e0=e0,e1=e1,r0=r0,l=np.full(len(e0),L_THROAT),
                inlet=inlet,outlet=outlet,fixed=fixed,fval=fval,
                edge_inlet_mask=edge_inlet_mask,xe=xe,
                pore_vol=pore_vol,eps_net=eps_net,nid=nid)

def solve(net,r,kind="hydraulic"):
    N=net["N"]; e0=net["e0"]; e1=net["e1"]; l=net["l"]
    g=r**4/l if kind=="hydraulic" else r**2/l
    fixed=net["fixed"]; fval=net["fval"]; free=~fixed
    # symmetric conductance graph Laplacian: diag = +sum incident g, off-diag = -g (true SPD)
    rows=np.concatenate([e0,e1,e0,e1]); cols=np.concatenate([e0,e1,e1,e0])
    vals=np.concatenate([g,g,-g,-g])     # (e0,e0):+g (e1,e1):+g (e0,e1):-g (e1,e0):-g
    L=sp.csr_matrix((vals,(rows,cols)),shape=(N,N))
    # Dirichlet-reduced SPD system on the free nodes (fast): L_ff x_f = -L_fd x_d
    Lff=L[free][:,free].tocsc(); Lfd=L[free][:,fixed]
    b=-Lfd@fval[fixed]
    xf=spla.spsolve(Lff,b)
    phi=fval.copy(); phi[free]=xf
    flux_e=g*(phi[e0]-phi[e1])
    Qtot=np.sum(np.abs(flux_e[net["edge_inlet_mask"]]))  # total flux across inlet (precomputed mask)
    return Qtot,flux_e,phi

def allocate(net,V_total,law,base_flux):
    e0=net["e0"]; r0=net["r0"]; l=net["l"]; E=len(e0); xe=net["xe"]
    if law=="uniform": w=np.ones(E)
    elif law=="surface_area": w=2*np.pi*r0*l
    elif law=="small_throat": w=1.0/r0**2
    elif law=="current_path": w=np.abs(base_flux)+1e-30
    elif law=="collector_biased": w=np.exp(xe/(0.3*net["nx"]))
    elif law=="strong_site":
        strong=(np.random.rand(E)<0.25).astype(float); w=1.0+4.0*strong*np.random.rand(E)
    w=w/w.sum()
    return V_total*w

def connected_active_fraction(net,r):
    """Fraction of throats with r>r_min that lie on an inlet-outlet connected path (3D)."""
    open_e=r>1.5*R_MIN
    N=net["N"]; e0=net["e0"][open_e]; e1=net["e1"][open_e]
    adj=sp.csr_matrix((np.ones(len(e0)*2),(np.concatenate([e0,e1]),np.concatenate([e1,e0]))),shape=(N,N))
    ncomp,lab=csg.connected_components(adj,directed=False)
    inl=lab[list(net["inlet"])]; out=lab[list(net["outlet"])]
    spanning=set(inl)&set(out)
    onpath=np.isin(lab[e0],list(spanning))
    return onpath.mean() if len(e0)>0 else 0.0

def run():
    log("R531 3D pore-network model — start")
    net=build_network()
    log(f"  network {net['nx']}x{net['ny']}x{net['nz']}={net['N']} nodes, {len(net['e0'])} throats, "
        f"porosity~{net['eps_net']:.3f} (target {EPS})")
    Q0h,flux0,_=solve(net,net["r0"],"hydraulic"); Q0i,_,_=solve(net,net["r0"],"ionic")
    laws=["uniform","surface_area","small_throat","current_path","collector_biased","strong_site"]
    fracs=np.linspace(0,0.5,16)
    rows=[]; thr=[]
    for law in laws:
        Kh=[];Ki=[];act=[];ov=[]
        for f in fracs:
            Vs=allocate(net,f*net["pore_vol"],law,flux0)
            r_new=np.sqrt(np.maximum(net["r0"]**2 - Vs/(np.pi*net["l"]), R_MIN**2))
            qh,fl,_=solve(net,r_new,"hydraulic"); qi,_,_=solve(net,r_new,"ionic")
            Kh.append(qh/Q0h); Ki.append(qi/Q0i); act.append(connected_active_fraction(net,r_new))
            ov.append(np.corrcoef(Vs,np.abs(flux0))[0,1] if f>0 and np.std(Vs)>0 else np.nan)
            eps_s=f*net["eps_net"]   # solid volume fraction of total
            rows.append(dict(law=law,retained_pore_fraction=f,eps_s=eps_s,K_hydraulic_rel=qh/Q0h,
                K_ionic_rel=qi/Q0i,connected_active_frac=act[-1],overlap_deposit_current=ov[-1]))
        Kh=np.array(Kh)
        def crit(loss): return interp_cross(fracs,1-Kh,loss,rising=True)
        # K at the COMSOL baseline operating point eps_s ~ 3.22e-3 -> f = eps_s/eps_net
        f_comsol=EPS_S_COMSOL/net["eps_net"]
        K_at_comsol=float(np.interp(f_comsol,fracs,Kh))
        thr.append(dict(law=law,crit_frac_10pct=crit(0.1),crit_frac_50pct=crit(0.5),
            crit_frac_90pct=crit(0.9),K_hydraulic_at_comsol_eps_s=K_at_comsol,
            f_at_comsol=f_comsol,mean_overlap=float(np.nanmean(ov))))
    dfc=pd.DataFrame(rows); dfc.to_csv(os.path.join(FSD,"R531_network3d_curves.csv"),index=False)
    tdf=pd.DataFrame(thr); tdf.to_csv(os.path.join(TAB,"R531_network3d_thresholds.csv"),index=False)
    tdf.to_csv(os.path.join(FSD,"R531_network3d_thresholds.csv"),index=False)
    log("  critical retained pore-fraction (hydraulic) + K at COMSOL eps_s=3.2e-3:")
    for _,r in tdf.iterrows():
        log(f"    {r.law:16s}: 50%@{r.crit_frac_50pct}, K@comsol={r.K_hydraulic_at_comsol_eps_s:.4f}, overlap={r.mean_overlap:.2f}")

    # ---- network vs continuum Kozeny-Carman (the COMSOL closure) ----
    el0=EPS
    f_axis=np.linspace(0,0.5,60); eps_s_axis=f_axis*net["eps_net"]
    el=el0-eps_s_axis  # liquid fraction shrinks as solid grows
    KC=(el/el0)**3*((1-el0)/(1-el))**2
    uni=dfc[dfc.law=="uniform"].sort_values("retained_pore_fraction")
    cur=dfc[dfc.law=="current_path"].sort_values("retained_pore_fraction")
    comp=pd.DataFrame(dict(retained_pore_fraction=f_axis,eps_s=eps_s_axis,
        KozenyCarman_continuum=KC,
        network_uniform=np.interp(f_axis,uni.retained_pore_fraction,uni.K_hydraulic_rel),
        network_current_path=np.interp(f_axis,cur.retained_pore_fraction,cur.K_hydraulic_rel)))
    comp.to_csv(os.path.join(TAB,"R531_network3d_vs_kozeny.csv"),index=False)
    comp.to_csv(os.path.join(FSD,"R531_network3d_vs_kozeny.csv"),index=False)
    log(f"  COMSOL operating point f={EPS_S_COMSOL/net['eps_net']:.4f} (eps_s={EPS_S_COMSOL}): "
        f"network uniform K={np.interp(EPS_S_COMSOL/net['eps_net'],uni.retained_pore_fraction,uni.K_hydraulic_rel):.4f}, "
        f"current_path K={np.interp(EPS_S_COMSOL/net['eps_net'],cur.retained_pore_fraction,cur.K_hydraulic_rel):.4f}, "
        f"Kozeny-Carman K={np.interp(EPS_S_COMSOL,eps_s_axis,KC):.4f}")
    # save a node-pressure field slice for a 3D render
    Vs=allocate(net,0.3*net["pore_vol"],"current_path",flux0)
    r_new=np.sqrt(np.maximum(net["r0"]**2 - Vs/(np.pi*net["l"]),R_MIN**2))
    _,fl,phi=solve(net,r_new,"hydraulic")
    np.savez(os.path.join(FSD,"R531_network3d_field.npz"),phi=phi,nx=net["nx"],ny=net["ny"],nz=net["nz"],
             e0=net["e0"],e1=net["e1"],r0=net["r0"],r_new=r_new,flux=fl)
    with open(os.path.join(LOG,"R531_network3d_log.txt"),"w",encoding="utf-8") as f:
        f.write("\n".join(log_lines))
    log("R531 3D pore-network model COMPLETE")

if __name__=="__main__":
    run()
