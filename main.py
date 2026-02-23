import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx
import re
import numpy as np
from collections import Counter

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(page_title="CNMV Explorer — BQuant Finance", page_icon="🏛️", layout="wide", initial_sidebar_state="expanded")

PAL = ["#0FF0B3","#818CF8","#FFBE0B","#FB7185","#38BDF8","#A78BFA","#34D399","#F472B6","#FBBF24","#60A5FA"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600;700&display=swap');
:root{--bg:#030712;--bg2:#0a0f1a;--glass:rgba(10,15,26,0.7);--border:rgba(255,255,255,0.04);--teal:#0FF0B3;--indigo:#818CF8;--gold:#FFBE0B;--rose:#FB7185;--sky:#38BDF8;--t1:#F1F5F9;--t2:#94A3B8;--t3:#475569;--t4:#1E293B}
.stApp{background:var(--bg)!important;font-family:'Plus Jakarta Sans',sans-serif}
.stApp::before{content:'';position:fixed;inset:0;background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 512 512' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.7' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.018'/%3E%3C/svg%3E");pointer-events:none;z-index:0}
.stApp::after{content:'';position:fixed;top:-30%;right:-15%;width:60vw;height:60vw;background:conic-gradient(from 200deg at 50% 50%,rgba(15,240,179,0.06),rgba(129,140,248,0.04),rgba(56,189,248,0.03),transparent 60%);border-radius:50%;filter:blur(100px);pointer-events:none;z-index:0;animation:mspin 40s linear infinite}
@keyframes mspin{to{transform:rotate(360deg)}}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#050a14,#030712)!important;border-right:1px solid var(--border)}
section[data-testid="stSidebar"]>div{padding-top:0!important}
header[data-testid="stHeader"]{background:transparent!important}
.brand{text-align:center;padding:36px 20px 28px;border-bottom:1px solid var(--border);position:relative}
.brand::after{content:'';position:absolute;bottom:-1px;left:15%;right:15%;height:1px;background:linear-gradient(90deg,transparent,var(--teal),transparent)}
.brand-icon{font-size:2.6rem;margin-bottom:10px;filter:drop-shadow(0 0 24px rgba(15,240,179,0.4))}
.brand-name{font-family:'Outfit';font-size:1.5rem;font-weight:800;letter-spacing:-.5px;background:linear-gradient(135deg,#0FF0B3,#818CF8,#38BDF8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-size:300% 300%;animation:bshift 6s ease infinite}
@keyframes bshift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
.brand-sub{font-family:'IBM Plex Mono';font-size:.6rem;color:var(--t3);letter-spacing:4px;text-transform:uppercase;margin-top:6px}
section[data-testid="stSidebar"] .stRadio>div{gap:3px!important}
section[data-testid="stSidebar"] .stRadio label{font-family:'Plus Jakarta Sans'!important;font-size:.88rem!important;font-weight:500!important;color:#475569!important;padding:14px 20px!important;border-radius:12px!important;transition:all .25s!important;border:1px solid transparent!important;margin:0 10px!important}
section[data-testid="stSidebar"] .stRadio label:hover{color:#94A3B8!important;background:rgba(15,240,179,.03)!important;border-color:rgba(15,240,179,.08)!important}
::-webkit-scrollbar{width:4px;height:4px}::-webkit-scrollbar-track{background:transparent}::-webkit-scrollbar-thumb{background:rgba(255,255,255,.06);border-radius:10px}::-webkit-scrollbar-thumb:hover{background:var(--teal)}
.hero{margin-bottom:42px}
.hero-title{font-family:'Outfit';font-size:2.8rem;font-weight:900;letter-spacing:-2px;color:#F8FAFC;line-height:1.05;margin-bottom:12px}
.hero-title .em{background:linear-gradient(135deg,#0FF0B3,#38BDF8);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{color:#475569;font-size:1rem;line-height:1.7;max-width:680px}
.kpi-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;margin:30px 0 42px}
.kpi{position:relative;background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:26px 22px;backdrop-filter:blur(24px);overflow:hidden;transition:all .35s cubic-bezier(.4,0,.2,1)}
.kpi:hover{border-color:rgba(255,255,255,.08);transform:translateY(-3px);box-shadow:0 16px 40px rgba(0,0,0,.4)}
.kpi::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:var(--kpi-a,linear-gradient(90deg,#0FF0B3,#818CF8));opacity:.7}
.kpi::after{content:'';position:absolute;top:-30px;right:-30px;width:100px;height:100px;background:radial-gradient(circle,var(--kpi-g,rgba(15,240,179,.06)),transparent 70%);pointer-events:none}
.kpi-icon{font-size:1.4rem;margin-bottom:14px}.kpi-val{font-family:'Outfit';font-size:2.3rem;font-weight:800;letter-spacing:-1.5px;color:#F8FAFC;line-height:1;margin-bottom:8px}.kpi-lbl{font-family:'IBM Plex Mono';font-size:.62rem;color:var(--t3);text-transform:uppercase;letter-spacing:1.5px;font-weight:500}
.kpi.c1{--kpi-a:linear-gradient(90deg,#0FF0B3,#34D399);--kpi-g:rgba(15,240,179,.07)}.kpi.c2{--kpi-a:linear-gradient(90deg,#818CF8,#A78BFA);--kpi-g:rgba(129,140,248,.07)}.kpi.c3{--kpi-a:linear-gradient(90deg,#FFBE0B,#FBBF24);--kpi-g:rgba(255,190,11,.07)}.kpi.c4{--kpi-a:linear-gradient(90deg,#38BDF8,#60A5FA);--kpi-g:rgba(56,189,248,.07)}.kpi.c5{--kpi-a:linear-gradient(90deg,#FB7185,#F472B6);--kpi-g:rgba(251,113,133,.07)}
.sec{display:flex;align-items:center;gap:13px;margin:38px 0 20px;padding-bottom:13px;border-bottom:1px solid var(--border);position:relative}
.sec::after{content:'';position:absolute;bottom:-1px;left:0;width:50px;height:1px;background:linear-gradient(90deg,var(--teal),transparent)}
.sec-icon{width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:1rem;background:rgba(15,240,179,.07);border:1px solid rgba(15,240,179,.12)}
.sec-txt{font-family:'Outfit';font-size:1.15rem;font-weight:700;color:#F1F5F9;letter-spacing:-.3px}
.ibox{background:linear-gradient(135deg,rgba(15,240,179,.03),rgba(129,140,248,.02));border:1px solid rgba(15,240,179,.1);border-radius:13px;padding:16px 20px 16px 23px;color:#94A3B8;font-size:.86rem;line-height:1.7;margin:12px 0;position:relative}
.ibox::before{content:'';position:absolute;top:0;left:0;width:3px;height:100%;background:linear-gradient(180deg,#0FF0B3,#818CF8);border-radius:3px 0 0 3px}
.ibox b{color:#E2E8F0}
.gdiv{height:1px;background:linear-gradient(90deg,transparent,rgba(15,240,179,.12),rgba(129,140,248,.08),transparent);margin:24px 0}
.ecard{background:var(--glass);border:1px solid var(--border);border-radius:22px;padding:32px;backdrop-filter:blur(24px);position:relative;overflow:hidden}
.ecard::before{content:'';position:absolute;top:-40%;right:-15%;width:350px;height:350px;background:radial-gradient(circle,rgba(15,240,179,.035),transparent 60%);pointer-events:none}
.ename{font-family:'Outfit';font-size:1.45rem;font-weight:700;color:#F8FAFC;letter-spacing:-.5px;margin-bottom:8px}
.ebadge{display:inline-flex;align-items:center;gap:6px;padding:5px 16px;border-radius:100px;font-family:'IBM Plex Mono';font-size:.68rem;font-weight:600;letter-spacing:.8px;text-transform:uppercase}
.ebadge-s{background:rgba(15,240,179,.08);color:#0FF0B3;border:1px solid rgba(15,240,179,.18)}
.ebadge-e{background:rgba(129,140,248,.08);color:#A78BFA;border:1px solid rgba(129,140,248,.18)}
.ebadge-f{background:rgba(255,190,11,.08);color:#FFBE0B;border:1px solid rgba(255,190,11,.18)}
.erows{display:grid;grid-template-columns:1fr 1fr;margin-top:22px}
.erow{display:flex;justify-content:space-between;padding:13px 14px;border-bottom:1px solid rgba(255,255,255,.03)}.erow:last-child{border:none}
.erow-k{font-size:.8rem;color:var(--t3);font-weight:500}.erow-v{font-size:.82rem;color:#E2E8F0;font-weight:600;text-align:right;max-width:65%;word-break:break-word}
.tags{display:flex;flex-wrap:wrap;gap:7px;margin:10px 0}
.tag{padding:6px 16px;border-radius:100px;font-size:.72rem;font-weight:500;background:rgba(15,240,179,.05);color:#5EEAD4;border:1px solid rgba(15,240,179,.1);transition:all .2s}
.tag:hover{background:rgba(15,240,179,.1);border-color:rgba(15,240,179,.25);transform:translateY(-1px)}
.stTabs [data-baseweb="tab-list"]{gap:5px;background:rgba(10,15,26,.5);border-radius:14px;padding:4px;border:1px solid var(--border)}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:10px!important;border:1px solid transparent!important;color:#475569!important;padding:10px 22px!important;font-family:'Plus Jakarta Sans'!important;font-weight:500!important;font-size:.86rem!important;transition:all .2s!important}
.stTabs [data-baseweb="tab"]:hover{color:#94A3B8!important}
.stTabs [aria-selected="true"]{background:rgba(15,240,179,.06)!important;border-color:rgba(15,240,179,.12)!important;color:#E2E8F0!important;box-shadow:0 0 20px rgba(15,240,179,.04)!important}
.stTabs [data-baseweb="tab-highlight"]{background-color:transparent!important}
.stTabs [data-baseweb="tab-border"]{display:none!important}
.stDataFrame{border-radius:14px;overflow:hidden;border:1px solid var(--border)}
.stSelectbox label,.stMultiSelect label,.stTextInput label{font-family:'Plus Jakarta Sans'!important;font-size:.82rem!important;font-weight:600!important;color:#94A3B8!important}
.statbox{background:linear-gradient(135deg,rgba(15,240,179,.05),rgba(129,140,248,.03));border:1px solid rgba(15,240,179,.1);border-radius:18px;padding:28px;text-align:center}
.statbox .sv{font-family:'Outfit';font-size:3.5rem;font-weight:900;background:linear-gradient(135deg,#0FF0B3,#38BDF8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1}
.statbox .sl{font-size:.82rem;color:var(--t3);margin-top:10px;font-weight:500}
.nleg{display:flex;gap:22px;padding:13px 18px;background:rgba(10,15,26,.5);border-radius:11px;border:1px solid var(--border);margin:12px 0;flex-wrap:wrap}
.nleg-i{display:flex;align-items:center;gap:8px;font-size:.78rem;color:#94A3B8;font-weight:500}
.nleg-d{width:10px;height:10px;border-radius:50%;position:relative}.nleg-d::after{content:'';position:absolute;inset:-3px;border-radius:50%;background:inherit;opacity:.3;filter:blur(4px)}
div[data-testid="stExpander"]{background:rgba(10,15,26,.5)!important;border:1px solid var(--border)!important;border-radius:14px!important}
.foot{text-align:center;padding:40px 0 20px;margin-top:56px;border-top:1px solid var(--border);position:relative}
.foot::before{content:'';position:absolute;top:-1px;left:30%;right:30%;height:1px;background:linear-gradient(90deg,transparent,rgba(15,240,179,.25),transparent)}
.foot-b{font-family:'Outfit';font-weight:700;font-size:.9rem;background:linear-gradient(135deg,#0FF0B3,#818CF8);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:6px}
.foot-s{font-family:'IBM Plex Mono';font-size:.6rem;color:var(--t4);letter-spacing:1.2px}
/* GAUGE */
.gauge-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin:20px 0}
.gauge{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:24px;text-align:center;backdrop-filter:blur(24px);position:relative;overflow:hidden}
.gauge::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;opacity:.6}
.gauge-val{font-family:'Outfit';font-size:2.6rem;font-weight:900;line-height:1;margin-bottom:4px}
.gauge-lbl{font-family:'IBM Plex Mono';font-size:.6rem;color:var(--t3);text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px}
.gauge-bar{height:6px;background:rgba(255,255,255,.04);border-radius:3px;overflow:hidden;margin-top:10px}
.gauge-fill{height:100%;border-radius:3px;transition:width 1.5s cubic-bezier(.4,0,.2,1)}
.gauge.danger .gauge-val{color:#FB7185}.gauge.danger::before{background:linear-gradient(90deg,#FB7185,#F43F5E)}.gauge.danger .gauge-fill{background:linear-gradient(90deg,#F43F5E,#FB7185)}
.gauge.warn .gauge-val{color:#FFBE0B}.gauge.warn::before{background:linear-gradient(90deg,#FFBE0B,#F59E0B)}.gauge.warn .gauge-fill{background:linear-gradient(90deg,#F59E0B,#FFBE0B)}
.gauge.ok .gauge-val{color:#0FF0B3}.gauge.ok::before{background:linear-gradient(90deg,#0FF0B3,#34D399)}.gauge.ok .gauge-fill{background:linear-gradient(90deg,#34D399,#0FF0B3)}
/* PERSON CARD */
.pcard{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:24px;backdrop-filter:blur(24px);margin-bottom:14px;position:relative;overflow:hidden;transition:border-color .3s}
.pcard:hover{border-color:rgba(255,255,255,.08)}
.pcard::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#FFBE0B,#FB7185);opacity:.6}
.pcard-name{font-family:'Outfit';font-size:1.1rem;font-weight:700;color:#F8FAFC;margin-bottom:4px}
.pcard-sub{font-family:'IBM Plex Mono';font-size:.68rem;color:var(--t3);letter-spacing:1px;margin-bottom:12px}
.pcard-ent{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:.82rem;color:#94A3B8}
.pcard-ent:last-child{border:none}
.pcard-dot{width:7px;height:7px;border-radius:50%;flex-shrink:0}
</style>""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@st.cache_data
def load_entities():
    df = pd.read_csv("cnmv_entities_complete.csv", encoding="utf-8-sig")
    df["direccion_provincia"] = df["direccion_provincia"].str.strip().str.upper()
    cap = df["capital_social"].astype(str).str.replace(".","",regex=False).str.replace(",",".",regex=False).str.strip()
    df["cap_num"] = pd.to_numeric(cap, errors="coerce")
    df["fecha_dt"] = pd.to_datetime(df["fecha_registro"], format="%d/%m/%Y", errors="coerce")
    return df

@st.cache_data
def load_funds():
    df = pd.read_csv("all_entities_detailed.csv")
    df["fecha_dt"] = pd.to_datetime(df["fecha_registro"], format="%d/%m/%Y", errors="coerce")
    return df

def parse_svc(s):
    return [x.strip() for x in str(s).split(";") if x.strip()] if pd.notna(s) else []

def parse_people(s):
    if pd.isna(s): return []
    r = []
    for p in str(s).split(";"):
        p = p.strip()
        m = re.match(r"(.+?)\s*\((.+?)\)", p)
        if m: r.append({"Nombre":m.group(1).strip(),"Cargo":m.group(2).strip()})
        elif p: r.append({"Nombre":p,"Cargo":"N/D"})
    return r

def parse_socios(s):
    if pd.isna(s): return []
    r = []
    for p in str(s).split(";"):
        p = p.strip()
        m = re.match(r"(.+?):\s*([\d,]+)\s*%", p)
        if m: r.append({"Socio":m.group(1).strip(),"Pct":float(m.group(2).replace(",","."))})
        elif p: r.append({"Socio":p,"Pct":None})
    return r

@st.cache_data
def build_graph(_E):
    G = nx.Graph()
    people_map = {}  # person -> [(entity, cargo, tipo)]
    socios_map = {}  # socio -> [(entity, pct, tipo)]
    for _, r in _E.iterrows():
        ent = r["nombre"]; tipo = r["tipo_entidad"]
        G.add_node(ent, nt="entity", et=tipo, prov=str(r.get("direccion_provincia","")))
        for p in parse_people(r.get("administradores")):
            nm = p["Nombre"]
            if nm not in G: G.add_node(nm, nt="admin")
            G.add_edge(ent, nm, rel="admin", cargo=p["Cargo"])
            people_map.setdefault(nm, []).append((ent, p["Cargo"], tipo))
        for s in parse_socios(r.get("socios_principales")):
            nm = s["Socio"]
            if nm not in G: G.add_node(nm, nt="socio")
            G.add_edge(ent, nm, rel="socio", pct=s.get("Pct"))
            socios_map.setdefault(nm, []).append((ent, s.get("Pct"), tipo))
    cross = {k:v for k,v in people_map.items() if len(set(e[0] for e in v)) > 1}
    return G, people_map, socios_map, cross

E = load_entities()
F = load_funds()
G, people_map, socios_map, cross_people = build_graph(E)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def kpi_row(items):
    cards = "".join(f'<div class="kpi {c}"><div class="kpi-icon">{i}</div><div class="kpi-val">{v}</div><div class="kpi-lbl">{l}</div></div>' for v,l,i,c in items)
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

def sec(text, icon="📊"):
    st.markdown(f'<div class="sec"><div class="sec-icon">{icon}</div><span class="sec-txt">{text}</span></div>', unsafe_allow_html=True)

def ibox(html):
    st.markdown(f'<div class="ibox">{html}</div>', unsafe_allow_html=True)

def gdiv():
    st.markdown('<div class="gdiv"></div>', unsafe_allow_html=True)

def foot():
    st.markdown('<div class="foot"><div class="foot-b">CNMV Explorer</div><div class="foot-s">Datos públicos CNMV · Agosto 2025 · BQuant Finance</div></div>', unsafe_allow_html=True)

def sfig(fig, h=420):
    fig.update_layout(
        template=None,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8",family="Plus Jakarta Sans",size=12),
        xaxis=dict(gridcolor="rgba(255,255,255,0.025)",zerolinecolor="rgba(255,255,255,0.03)",showgrid=True,gridwidth=1,tickfont=dict(size=11)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.025)",zerolinecolor="rgba(255,255,255,0.03)",showgrid=True,gridwidth=1,tickfont=dict(size=11)),
        height=h,margin=dict(l=16,r=16,t=32,b=32),
        legend=dict(bgcolor="rgba(0,0,0,0)",font=dict(color="#94A3B8",size=11)),
        hoverlabel=dict(bgcolor="#0a0f1a",font_size=12,font_family="Plus Jakarta Sans",bordercolor="rgba(15,240,179,0.3)"))
    return fig

def ego_graph_fig(G, center_node, radius=2):
    """Build a plotly figure for the ego network of center_node."""
    try:
        ego = nx.ego_graph(G, center_node, radius=radius)
    except nx.NetworkXError:
        return None
    if len(ego.nodes()) < 2:
        return None

    # Layout: center node fixed, rest spread around
    pos = nx.spring_layout(ego, k=2.5, iterations=60, seed=42, center=[0,0])

    # Edges
    ex, ey = [], []
    edge_colors = []
    for u, v in ego.edges():
        x0, y0 = pos[u]; x1, y1 = pos[v]
        ex.extend([x0, x1, None]); ey.extend([y0, y1, None])

    edge_trace = go.Scatter(x=ex, y=ey, mode="lines",
        line=dict(width=0.6, color="rgba(148,163,184,0.12)"),
        hoverinfo="none", showlegend=False)

    # Nodes by type
    cfg = {
        "entity": ("#0FF0B3", "diamond", 20, "Entidades"),
        "socio":  ("#818CF8", "circle", 12, "Socios"),
        "admin":  ("#FFBE0B", "circle", 10, "Administradores"),
    }
    traces = [edge_trace]
    for nt, (clr, sym, base_sz, label) in cfg.items():
        nodes = [n for n, d in ego.nodes(data=True) if d.get("nt") == nt]
        if not nodes: continue
        x = [pos[n][0] for n in nodes]
        y = [pos[n][1] for n in nodes]
        sizes = []
        for n in nodes:
            sz = base_sz
            if n == center_node: sz = 32
            elif ego.degree(n) > 3: sz = base_sz + 6
            sizes.append(sz)
        hovers = []
        for n in nodes:
            nbs = [nb for nb in ego.neighbors(n)]
            deg = ego.degree(n)
            ed_info = []
            for nb in nbs[:8]:
                ed = ego.get_edge_data(n, nb)
                rel = ed.get("rel","") if ed else ""
                extra = ""
                if rel == "admin" and ed.get("cargo"): extra = f" ({ed['cargo']})"
                elif rel == "socio" and ed.get("pct"): extra = f" ({ed['pct']:.1f}%)"
                ed_info.append(f"{'→' if rel=='admin' else '◆'} {nb[:35]}{extra}")
            more = f"<br>...y {deg - 8} más" if deg > 8 else ""
            hovers.append(f"<b>{n}</b><br><span style='color:#475569'>{label}</span><br>Conexiones: {deg}<br><br>{'<br>'.join(ed_info)}{more}")

        marker_line = dict(width=2, color="#0FF0B3") if any(n == center_node for n in nodes) else dict(width=1, color="rgba(255,255,255,0.06)")
        traces.append(go.Scatter(x=x, y=y, mode="markers", name=label,
            marker=dict(size=sizes, color=clr, symbol=sym,
                line=marker_line, opacity=0.9),
            text=hovers, hoverinfo="text"))

    fig = go.Figure(data=traces)
    fig.update_layout(
        showlegend=True, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94A3B8", family="Plus Jakarta Sans"),
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False),
        height=600, margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(bgcolor="rgba(10,15,26,.85)", bordercolor="rgba(255,255,255,.04)",
            borderwidth=1, font=dict(size=11), x=.01, y=.99),
        hoverlabel=dict(bgcolor="#0a0f1a", font_size=11, font_family="Plus Jakarta Sans",
            bordercolor="rgba(15,240,179,.25)"))
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-icon">🏛️</div><div class="brand-name">CNMV Explorer</div><div class="brand-sub">BQuant Finance</div></div>', unsafe_allow_html=True)
    page = st.radio("n", ["🕸️  Red de Poder", "🔍  Buscador Universal", "📊  Concentración de Mercado"], label_visibility="collapsed")
    st.markdown("<br>"*3, unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;padding:16px;border-top:1px solid rgba(255,255,255,.04)"><div style="font-family:IBM Plex Mono;font-size:.58rem;color:#1E293B;letter-spacing:2px;text-transform:uppercase">Datos CNMV · Ago 2025</div></div>', unsafe_allow_html=True)


# ╔═══════════════════════════════════════════════════════════════╗
# ║  RED DE PODER (LANDING)                                       ║
# ╚═══════════════════════════════════════════════════════════════╝
if page == "🕸️  Red de Poder":
    st.markdown('<div class="hero"><div class="hero-title">Red de <span class="em">Poder</span> Financiero</div><div class="hero-sub">El mapa tridimensional de relaciones entre entidades, administradores y socios del ecosistema de valores español. Arrastra para rotar.</div></div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3D NETWORK — STARFIELD AESTHETIC
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    @st.cache_data
    def compute_3d_layout(_node_list, _edge_list):
        H = nx.Graph()
        for n, nt, et in _node_list:
            H.add_node(n, nt=nt, et=et)
        for u, v in _edge_list:
            H.add_edge(u, v)

        comps = sorted(nx.connected_components(H), key=len, reverse=True)
        pos = {}
        rng = np.random.RandomState(42)
        golden_angle = np.pi * (3 - np.sqrt(5))
        n_comps = len(comps)

        for idx, comp in enumerate(comps):
            sub = H.subgraph(comp)
            n_nodes = len(comp)
            comp_radius = max(0.6, np.sqrt(n_nodes) * 0.5)

            t = idx * 0.8
            spiral_r = 2.8 * np.sqrt(t + 1)
            phi = golden_angle * idx
            theta = np.arccos(1 - 2 * ((idx + 0.5) / max(n_comps, 1)))

            cx = spiral_r * np.sin(theta) * np.cos(phi)
            cy = spiral_r * np.sin(theta) * np.sin(phi)
            cz = spiral_r * np.cos(theta) * 0.65

            if n_nodes == 1:
                n = list(comp)[0]
                pos[n] = (cx + rng.uniform(-0.2, 0.2), cy + rng.uniform(-0.2, 0.2), cz + rng.uniform(-0.2, 0.2))
            else:
                local = nx.spring_layout(sub, k=1.4, iterations=40, seed=42, dim=3)
                for n, coords in local.items():
                    pos[n] = (
                        coords[0] * comp_radius + cx,
                        coords[1] * comp_radius + cy,
                        coords[2] * comp_radius * 0.5 + cz,
                    )
        return pos

    node_list = tuple((n, d.get("nt",""), d.get("et","")) for n, d in G.nodes(data=True))
    edge_list = tuple((u, v) for u, v in G.edges())
    pos3d = compute_3d_layout(node_list, edge_list)

    # Camera depth
    all_coords = np.array(list(pos3d.values()))
    scene_center = all_coords.mean(axis=0)
    scene_scale = np.abs(all_coords - scene_center).max()
    cam_world = np.array([0.5, 0.5, 0.3]) * scene_scale + scene_center
    node_dists = {n: np.linalg.norm(np.array(p) - cam_world) for n, p in pos3d.items()}
    d_min, d_max = min(node_dists.values()), max(node_dists.values())
    d_range = max(d_max - d_min, 1)

    def df(n):
        return (node_dists[n] - d_min) / d_range

    # ── Edges ──
    ex, ey, ez = [], [], []
    for u, v in G.edges():
        if u in pos3d and v in pos3d:
            x0, y0, z0 = pos3d[u]; x1, y1, z1 = pos3d[v]
            ex.extend([x0, x1, None]); ey.extend([y0, y1, None]); ez.extend([z0, z1, None])

    traces = [go.Scatter3d(x=ex, y=ey, z=ez, mode="lines",
        line=dict(width=1.0, color="rgba(80,200,180,0.045)"),
        hoverinfo="none", showlegend=False)]

    # ── Nodes — small crisp particles ──
    node_cfg = {
        "entity": {"near": (100, 255, 218), "far": (20, 80, 100), "sz": (4, 12), "a": (0.95, 0.2), "label": "🏛️ Entidades"},
        "admin":  {"near": (255, 220, 100), "far": (140, 80, 30), "sz": (2, 5),   "a": (0.85, 0.15), "label": "👤 Administradores"},
        "socio":  {"near": (180, 170, 255), "far": (60, 50, 120), "sz": (2, 5),   "a": (0.80, 0.15), "label": "💼 Socios"},
    }

    for nt, c in node_cfg.items():
        nodes = [n for n in G.nodes() if G.nodes[n].get("nt") == nt and n in pos3d]
        if not nodes: continue

        x = [pos3d[n][0] for n in nodes]
        y = [pos3d[n][1] for n in nodes]
        z = [pos3d[n][2] for n in nodes]

        degrees = [G.degree(n) for n in nodes]
        max_deg = max(degrees) if degrees else 1

        sizes, colors = [], []
        for n, d in zip(nodes, degrees):
            t = df(n)
            # Size: near=big, far=small, plus degree boost
            base = c["sz"][1] + (c["sz"][0] - c["sz"][1]) * t
            deg_boost = (d / max(max_deg, 1)) * (c["sz"][1] * 0.8) * (1 - t * 0.5)
            sizes.append(max(1.5, base + deg_boost))
            # Color: interpolate near→far with depth opacity
            nr, ng, nb = c["near"]; fr, fg, fb = c["far"]
            r = int(nr + (fr - nr) * t)
            g = int(ng + (fg - ng) * t)
            b = int(nb + (fb - nb) * t)
            a = c["a"][0] + (c["a"][1] - c["a"][0]) * t
            colors.append(f"rgba({r},{g},{b},{a:.2f})")

        hovers = []
        for n, deg in zip(nodes, degrees):
            nbs = list(G.neighbors(n))[:5]
            nb_lines = "<br>".join(f"· {nb[:35]}" for nb in nbs)
            if G.degree(n) > 5: nb_lines += f"<br>...+{G.degree(n)-5} más"
            hovers.append(f"<b>{n}</b><br>{c['label']}<br>Conexiones: {deg}<br><br>{nb_lines}")

        traces.append(go.Scatter3d(x=x, y=y, z=z, mode="markers", name=c["label"],
            marker=dict(size=sizes, color=colors, line=dict(width=0)),
            text=hovers, hoverinfo="text"))

    fig = go.Figure(data=traces)

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(visible=False, showbackground=False),
            yaxis=dict(visible=False, showbackground=False),
            zaxis=dict(visible=False, showbackground=False),
            camera=dict(eye=dict(x=0.5, y=0.5, z=0.3), center=dict(x=0,y=0,z=0), up=dict(x=0,y=0,z=1)),
            aspectmode="data",
        ),
        font=dict(color="#94A3B8", family="Plus Jakarta Sans"),
        height=850, margin=dict(l=0, r=0, t=0, b=0),
        showlegend=True,
        legend=dict(bgcolor="rgba(3,7,18,0.92)", bordercolor="rgba(100,255,218,.06)",
            borderwidth=1, font=dict(size=11, color="#94A3B8"), x=0.01, y=0.98, itemsizing="constant"),
        hoverlabel=dict(bgcolor="rgba(3,7,18,0.95)", font_size=11, font_family="Plus Jakarta Sans",
            bordercolor="rgba(100,255,218,0.2)"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "scrollZoom": True})

    # ── Legend + KPIs BELOW the graph ──
    st.markdown('<div class="nleg"><div class="nleg-i"><div class="nleg-d" style="background:#0FF0B3"></div> Entidades SAV/EAF</div><div class="nleg-i"><div class="nleg-d" style="background:#818CF8"></div> Socios / Accionistas</div><div class="nleg-i"><div class="nleg-d" style="background:#FFBE0B"></div> Administradores</div><div class="nleg-i" style="margin-left:auto;color:#475569;font-size:.7rem">Arrastra para rotar · Scroll para zoom</div></div>', unsafe_allow_html=True)

    kpi_row([
        (str(G.number_of_nodes()), "Nodos en la Red", "🔵", "c1"),
        (str(G.number_of_edges()), "Conexiones", "🔗", "c2"),
        (str(len(cross_people)), "Personas Multi-Entidad", "👥", "c3"),
        (str(len(E)), "Entidades Reguladas", "🏛️", "c4"),
    ])

    gdiv()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TABS BELOW THE GRAPH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    tab1, tab2 = st.tabs(["🏛️ Explorador por Entidad", "👥 Conexiones Cruzadas"])

    # ─── TAB 1: EGO NETWORK ───
    with tab1:
        sec("Explorador por Entidad", "🏛️")
        ibox("Selecciona una entidad para ver su <b>red de relaciones</b> a 1-2 grados de separación — administradores, socios, y sus conexiones con otras entidades.")

        c1, c2 = st.columns([2, 1])
        with c1:
            entities = sorted(E["nombre"].tolist())
            selected = st.selectbox("Selecciona una entidad", entities, index=entities.index("ALANTRA EQUITIES SOCIEDAD DE VALORES, S.A.") if "ALANTRA EQUITIES SOCIEDAD DE VALORES, S.A." in entities else 0)
        with c2:
            radius = st.select_slider("Profundidad de red", options=[1, 2, 3], value=2)

        if selected and selected in G:
            fig = ego_graph_fig(G, selected, radius=radius)
            if fig:
                ego = nx.ego_graph(G, selected, radius=radius)
                n_ent = sum(1 for _,d in ego.nodes(data=True) if d.get("nt")=="entity")
                n_ppl = sum(1 for _,d in ego.nodes(data=True) if d.get("nt") in ("admin","socio"))

                kpi_row([
                    (str(len(ego.nodes())), "Nodos en Red", "🔵", "c1"),
                    (str(len(ego.edges())), "Conexiones", "🔗", "c2"),
                    (str(n_ent), "Entidades Conectadas", "🏛️", "c4"),
                    (str(n_ppl), "Personas Relacionadas", "👤", "c3"),
                ])

                st.plotly_chart(fig, use_container_width=True)

                # Show the entity details inline
                gdiv()
                ent_row = E[E["nombre"] == selected].iloc[0]
                tipo = ent_row["tipo_entidad"]
                bc = "ebadge-s" if tipo == "SAV" else "ebadge-e"
                bl = "Sociedad de Valores" if tipo == "SAV" else "Empresa de Asesoramiento"
                bd = "🟢" if tipo == "SAV" else "🟣"

                dets = [("CIF", ent_row.get("id","—")), ("Nº Registro", ent_row.get("numero_registro","—")),
                        ("Fecha Registro", ent_row.get("fecha_registro","—")), ("Provincia", ent_row.get("direccion_provincia","—")),
                        ("Capital Social", f'{ent_row.get("capital_social","—")} €'), ("FOGAIN", ent_row.get("fogain","—")),
                        ("Auditor", ent_row.get("ultimo_auditor","—")), ("Email", ent_row.get("titular_email","—"))]
                rh = "".join(f'<div class="erow"><span class="erow-k">{k}</span><span class="erow-v">{v}</span></div>' for k,v in dets)
                st.markdown(f'<div class="ecard"><div class="ename">{selected}</div><span class="ebadge {bc}">{bd} {bl}</span><div class="erows">{rh}</div></div>', unsafe_allow_html=True)

                x1, x2 = st.columns(2)
                with x1:
                    sec("Administradores", "👥")
                    adm = parse_people(ent_row.get("administradores"))
                    if adm: st.dataframe(pd.DataFrame(adm), use_container_width=True, hide_index=True)
                with x2:
                    sec("Socios Principales", "🏢")
                    soc = parse_socios(ent_row.get("socios_principales"))
                    if soc: st.dataframe(pd.DataFrame(soc), use_container_width=True, hide_index=True)

                svcs = parse_svc(ent_row.get("servicios_inversion"))
                if svcs:
                    sec("Servicios Autorizados", "📋")
                    st.markdown(f'<div class="tags">{"".join(f"<span class=tag>{s}</span>" for s in svcs)}</div>', unsafe_allow_html=True)
            else:
                st.info("Esta entidad no tiene conexiones en la red.")

    # ─── TAB 2: CROSS CONNECTIONS ───
    with tab2:
        sec("Personas en Múltiples Entidades", "🔗")
        ibox(f'<b>{len(cross_people)} personas</b> ocupan cargos en más de una entidad regulada simultáneamente. Estas conexiones cruzadas revelan los centros de poder del ecosistema financiero español.')

        # Sort by unique entities
        cross_sorted = sorted(cross_people.items(), key=lambda x: len(set(e[0] for e in x[1])), reverse=True)

        for person, entries in cross_sorted[:20]:
            unique_ents = list(set(e[0] for e in entries))
            n_ents = len(unique_ents)
            cargos_by_ent = {}
            for ent, cargo, tipo in entries:
                cargos_by_ent.setdefault(ent, []).append(cargo)

            ent_html = ""
            for ent in unique_ents:
                tipo_row = E[E["nombre"]==ent]
                tipo_color = "#0FF0B3" if not tipo_row.empty and tipo_row.iloc[0]["tipo_entidad"]=="SAV" else "#818CF8"
                cargos = ", ".join(set(cargos_by_ent.get(ent,[])))
                ent_html += f'<div class="pcard-ent"><div class="pcard-dot" style="background:{tipo_color}"></div><span style="color:#E2E8F0;font-weight:600">{ent[:50]}</span><span style="margin-left:auto;color:#475569;font-size:.75rem">{cargos}</span></div>'

            st.markdown(f'<div class="pcard"><div class="pcard-name">{person}</div><div class="pcard-sub">{n_ents} ENTIDADES</div>{ent_html}</div>', unsafe_allow_html=True)

    foot()


# ╔═══════════════════════════════════════════════════════════════╗
# ║  BUSCADOR UNIVERSAL                                           ║
# ╚═══════════════════════════════════════════════════════════════╝
elif page == "🔍  Buscador Universal":
    st.markdown('<div class="hero"><div class="hero-title">Buscador <span class="em">Universal</span></div><div class="hero-sub">Un único buscador para todo el ecosistema — entidades, personas, fondos de capital riesgo. Escribe un nombre y descubre todas sus conexiones.</div></div>', unsafe_allow_html=True)

    query = st.text_input("🔍 Busca cualquier nombre — persona, entidad, fondo, ISIN...", placeholder="Ej: Alantra, Poblet, CACEIS, ES0...")

    if query and len(query) >= 2:
        q = query.upper().strip()

        # Search entities
        ent_matches = E[E["nombre"].str.upper().str.contains(q, na=False) | E["id"].astype(str).str.upper().str.contains(q, na=False)]
        # Search funds
        fund_matches = F[F["entity_name"].str.upper().str.contains(q, na=False) | F["isin"].astype(str).str.upper().str.contains(q, na=False) | F["gestora_nombre"].astype(str).str.upper().str.contains(q, na=False)]
        # Search people
        people_matches = {k:v for k,v in people_map.items() if q in k.upper()}
        socio_matches = {k:v for k,v in socios_map.items() if q in k.upper()}

        total = len(ent_matches) + fund_matches["entity_name"].nunique() + len(people_matches) + len(socio_matches)
        ibox(f'Encontrados <b>{total}</b> resultados para "<b>{query}</b>" — {len(ent_matches)} entidades, {fund_matches["entity_name"].nunique()} fondos CR, {len(people_matches)} administradores, {len(socio_matches)} socios')

        # ── ENTITIES ──
        if not ent_matches.empty:
            sec(f"Entidades Reguladas ({len(ent_matches)})", "🏛️")
            for _, ent in ent_matches.iterrows():
                tipo = ent["tipo_entidad"]
                bc = "ebadge-s" if tipo == "SAV" else "ebadge-e"
                bl = tipo
                bd = "🟢" if tipo == "SAV" else "🟣"
                dets = [("CIF",ent.get("id","—")),("Nº Registro",ent.get("numero_registro","—")),
                        ("Provincia",ent.get("direccion_provincia","—")),("Capital Social",f'{ent.get("capital_social","—")} €'),
                        ("Auditor",ent.get("ultimo_auditor","—")),("FOGAIN",ent.get("fogain","—"))]
                rh = "".join(f'<div class="erow"><span class="erow-k">{k}</span><span class="erow-v">{v}</span></div>' for k,v in dets)
                st.markdown(f'<div class="ecard"><div class="ename">{ent["nombre"]}</div><span class="ebadge {bc}">{bd} {bl}</span><div class="erows">{rh}</div></div>', unsafe_allow_html=True)

                with st.expander(f"📋 Ver administradores, socios y servicios"):
                    x1, x2 = st.columns(2)
                    with x1:
                        adm = parse_people(ent.get("administradores"))
                        if adm: st.dataframe(pd.DataFrame(adm), use_container_width=True, hide_index=True)
                        else: st.caption("Sin administradores")
                    with x2:
                        so = parse_socios(ent.get("socios_principales"))
                        if so: st.dataframe(pd.DataFrame(so), use_container_width=True, hide_index=True)
                        else: st.caption("Sin socios")
                    svcs = parse_svc(ent.get("servicios_inversion"))
                    if svcs:
                        st.markdown(f'<div class="tags">{"".join(f"<span class=tag>{s}</span>" for s in svcs)}</div>', unsafe_allow_html=True)

            gdiv()

        # ── PEOPLE ──
        if people_matches:
            sec(f"Administradores ({len(people_matches)})", "👤")
            for person, entries in sorted(people_matches.items()):
                unique_ents = list(set(e[0] for e in entries))
                multi = len(unique_ents) > 1
                cargos_by_ent = {}
                for ent, cargo, tipo in entries:
                    cargos_by_ent.setdefault(ent,[]).append(cargo)

                ent_html = ""
                for ent in unique_ents:
                    tipo_row = E[E["nombre"]==ent]
                    tc = "#0FF0B3" if not tipo_row.empty and tipo_row.iloc[0]["tipo_entidad"]=="SAV" else "#818CF8"
                    cargos = ", ".join(set(cargos_by_ent.get(ent,[])))
                    ent_html += f'<div class="pcard-ent"><div class="pcard-dot" style="background:{tc}"></div><span style="color:#E2E8F0;font-weight:600">{ent[:55]}</span><span style="margin-left:auto;color:#475569;font-size:.75rem">{cargos}</span></div>'

                badge = f' <span style="background:rgba(251,113,133,.08);color:#FB7185;padding:2px 10px;border-radius:100px;font-size:.65rem;font-weight:600;border:1px solid rgba(251,113,133,.15)">⚡ MULTI-ENTIDAD</span>' if multi else ""
                st.markdown(f'<div class="pcard"><div class="pcard-name">{person}{badge}</div><div class="pcard-sub">{len(unique_ents)} ENTIDAD{"ES" if len(unique_ents)>1 else ""}</div>{ent_html}</div>', unsafe_allow_html=True)
            gdiv()

        # ── SOCIOS ──
        if socio_matches:
            sec(f"Socios / Accionistas ({len(socio_matches)})", "💼")
            for socio, entries in sorted(socio_matches.items()):
                unique_ents = list(set(e[0] for e in entries))
                ent_html = ""
                for ent, pct, tipo in entries:
                    tc = "#0FF0B3" if tipo == "SAV" else "#818CF8"
                    pct_str = f"{pct:.1f}%" if pct else "—"
                    ent_html += f'<div class="pcard-ent"><div class="pcard-dot" style="background:{tc}"></div><span style="color:#E2E8F0;font-weight:600">{ent[:55]}</span><span style="margin-left:auto;color:#FFBE0B;font-weight:600;font-size:.82rem">{pct_str}</span></div>'
                st.markdown(f'<div class="pcard"><div class="pcard-name">{socio}</div><div class="pcard-sub">SOCIO EN {len(unique_ents)} ENTIDAD{"ES" if len(unique_ents)>1 else ""}</div>{ent_html}</div>', unsafe_allow_html=True)
            gdiv()

        # ── FUNDS ──
        if not fund_matches.empty:
            n_funds = fund_matches["entity_name"].nunique()
            sec(f"Capital Riesgo ({n_funds} fondos, {len(fund_matches)} registros)", "💰")
            st.dataframe(
                fund_matches[["entity_type","entity_name","gestora_nombre","depositaria_nombre","fecha_registro","denominacion","isin"]]
                .rename(columns={"entity_type":"Tipo","entity_name":"Fondo","gestora_nombre":"Gestora","depositaria_nombre":"Depositaria","fecha_registro":"Fecha","denominacion":"Clase","isin":"ISIN"})
                .reset_index(drop=True),
                use_container_width=True, height=400)

    elif query:
        st.caption("Escribe al menos 2 caracteres para buscar.")
    else:
        # ── DISCOVERY PANEL ──
        kpi_row([
            (str(len(E)), "Entidades SAV+EAF", "🏛️", "c1"),
            (f"{F['entity_name'].nunique():,}", "Fondos Capital Riesgo", "💰", "c3"),
            (str(len(people_map)), "Personas en la Red", "👤", "c2"),
            (str(len(socios_map)), "Socios / Accionistas", "💼", "c4"),
            (str(len(cross_people)), "Personas Multi-Entidad", "⚡", "c5"),
        ])

        # ── HIGHLIGHTED FINDINGS ──
        sec("🔥 Hallazgos Destacados", "⚡")
        ibox("Datos llamativos detectados automáticamente en el ecosistema — haz clic en las pestañas para explorar por categoría.")

        # Build highlights
        cross_sorted = sorted(cross_people.items(), key=lambda x: len(set(e[0] for e in x[1])), reverse=True)
        top_cross = cross_sorted[:3]

        dep_funds = F.drop_duplicates("entity_name").groupby("depositaria_nombre").size()
        dep_top = dep_funds.sort_values(ascending=False).head(3)
        dep_total = dep_funds.sum()

        gest_top = F.drop_duplicates("entity_name").groupby("gestora_nombre").size().nlargest(3)

        hl_html = '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:16px 0">'

        # Card 1 - Multi-entity people
        ppl_items = ""
        for name, entries in top_cross:
            n_ents = len(set(e[0] for e in entries))
            ppl_items += f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:.8rem"><span style="color:#E2E8F0">{name[:28]}</span><span style="color:#FFBE0B;font-weight:600">{n_ents} ent.</span></div>'
        hl_html += f'<div class="ecard" style="padding:22px"><div style="font-size:.65rem;color:#FB7185;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;font-weight:600">👥 Personas más conectadas</div><div style="font-size:.78rem;color:#475569;margin-bottom:14px">Administradores en múltiples entidades</div>{ppl_items}</div>'

        # Card 2 - Depositaria concentration
        dep_items = ""
        for name, count in dep_top.items():
            pct = count / dep_total * 100
            dep_items += f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:.8rem"><span style="color:#E2E8F0">{name[:28]}</span><span style="color:#0FF0B3;font-weight:600">{pct:.0f}%</span></div>'
        hl_html += f'<div class="ecard" style="padding:22px"><div style="font-size:.65rem;color:#0FF0B3;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;font-weight:600">🏦 Concentración Depositarias</div><div style="font-size:.78rem;color:#475569;margin-bottom:14px">Solo 8 depositarias custodian todo</div>{dep_items}</div>'

        # Card 3 - Top gestoras
        gest_items = ""
        for name, count in gest_top.items():
            gest_items += f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.03);font-size:.8rem"><span style="color:#E2E8F0">{name[:28]}</span><span style="color:#818CF8;font-weight:600">{count} fondos</span></div>'
        hl_html += f'<div class="ecard" style="padding:22px"><div style="font-size:.65rem;color:#818CF8;font-family:IBM Plex Mono;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:6px;font-weight:600">🏢 Mayores Gestoras CR</div><div style="font-size:.78rem;color:#475569;margin-bottom:14px">Las 3 gestoras con más fondos</div>{gest_items}</div>'
        hl_html += '</div>'
        st.markdown(hl_html, unsafe_allow_html=True)

        gdiv()

        # ── BROWSABLE DIRECTORIES ──
        sec("Directorio Completo", "📂")

        dtab1, dtab2, dtab3, dtab4 = st.tabs(["🏛️ Entidades SAV & EAF", "👤 Personas (A-Z)", "💰 Gestoras CR", "🏦 Fondos CR"])

        with dtab1:
            letter = st.select_slider("Filtrar por letra", options=["Todas"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), value="Todas", key="ent_letter")
            ent_dir = E[["nombre","tipo_entidad","numero_registro","direccion_provincia","ultimo_auditor"]].copy()
            ent_dir.columns = ["Entidad","Tipo","Nº Registro","Provincia","Auditor"]
            ent_dir = ent_dir.sort_values("Entidad")
            if letter != "Todas":
                ent_dir = ent_dir[ent_dir["Entidad"].str.upper().str.startswith(letter)]
            st.caption(f"{len(ent_dir)} entidades" + (f" que empiezan por '{letter}'" if letter != "Todas" else ""))
            st.dataframe(ent_dir.reset_index(drop=True), use_container_width=True, height=420)

        with dtab2:
            # Show people directory with their entity connections
            letter_p = st.select_slider("Filtrar por letra", options=["Todas"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), value="Todas", key="ppl_letter")
            ppl_rows = []
            for person, entries in sorted(people_map.items()):
                unique_ents = list(set(e[0] for e in entries))
                cargos = list(set(e[1] for e in entries if e[1] != "N/D"))
                ppl_rows.append({
                    "Persona": person,
                    "Nº Entidades": len(unique_ents),
                    "Entidades": " · ".join(e[:35] for e in unique_ents),
                    "Cargos": ", ".join(cargos[:3]) if cargos else "—",
                })
            ppl_df = pd.DataFrame(ppl_rows).sort_values("Persona")
            if letter_p != "Todas":
                ppl_df = ppl_df[ppl_df["Persona"].str.upper().str.startswith(letter_p)]
            # Highlight multi-entity
            multi_mask = ppl_df["Nº Entidades"] > 1
            st.caption(f"{len(ppl_df)} personas" + (f" que empiezan por '{letter_p}'" if letter_p != "Todas" else "") + f" · {multi_mask.sum()} en múltiples entidades")
            st.dataframe(ppl_df.reset_index(drop=True), use_container_width=True, height=420,
                column_config={"Nº Entidades": st.column_config.NumberColumn("Nº Ent.", width="small")})

        with dtab3:
            gest_df = F.drop_duplicates("entity_name").groupby("gestora_nombre").agg(
                Fondos=("entity_name","count"),
                Tipos=("entity_type", lambda x: ", ".join(sorted(x.unique())[:2])),
            ).sort_values("Fondos", ascending=False).reset_index()
            gest_df.columns = ["Gestora","Fondos","Tipos de Vehículo"]
            st.caption(f"{len(gest_df)} gestoras activas")
            st.dataframe(gest_df, use_container_width=True, height=420)

        with dtab4:
            letter_f = st.select_slider("Filtrar por letra", options=["Todas"] + list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"), value="Todas", key="fund_letter")
            fund_dir = F.drop_duplicates("entity_name")[["entity_type","entity_name","gestora_nombre","depositaria_nombre","fecha_registro"]].copy()
            fund_dir.columns = ["Tipo","Fondo","Gestora","Depositaria","Fecha Registro"]
            fund_dir = fund_dir.sort_values("Fondo")
            if letter_f != "Todas":
                fund_dir = fund_dir[fund_dir["Fondo"].str.upper().str.startswith(letter_f)]
            st.caption(f"{len(fund_dir)} fondos/sociedades" + (f" que empiezan por '{letter_f}'" if letter_f != "Todas" else ""))
            st.dataframe(fund_dir.reset_index(drop=True), use_container_width=True, height=420)

    foot()


# ╔═══════════════════════════════════════════════════════════════╗
# ║  CONCENTRACIÓN DE MERCADO                                     ║
# ╚═══════════════════════════════════════════════════════════════╝
elif page == "📊  Concentración de Mercado":
    st.markdown('<div class="hero"><div class="hero-title">Concentración de <span class="em">Mercado</span></div><div class="hero-sub">Análisis de riesgo sistémico — ¿cuánta concentración hay en depositarias, auditores y gestoras? Índices HHI y cuotas de mercado.</div></div>', unsafe_allow_html=True)

    # ── HHI CALCULATIONS ──
    def calc_hhi(series):
        total = series.sum()
        if total == 0: return 0, pd.Series()
        shares = series / total * 100
        hhi = (shares**2).sum()
        return hhi, shares

    # Depositarias (entities)
    dep_ent = E.dropna(subset=["num_servicios_inversion"]).copy()  # just use all entities
    # Actually use fund depositarias for CR
    dep_funds = F.drop_duplicates("entity_name").groupby("depositaria_nombre").size()
    hhi_dep, shares_dep = calc_hhi(dep_funds)

    # Auditores
    aud_counts = E.dropna(subset=["ultimo_auditor"])["ultimo_auditor"].value_counts()
    hhi_aud, shares_aud = calc_hhi(aud_counts)

    # Gestoras
    gest_counts = F.drop_duplicates("entity_name").groupby("gestora_nombre").size()
    hhi_gest, shares_gest = calc_hhi(gest_counts)

    # ── HHI GAUGES ──
    sec("Índices de Concentración HHI", "🎯")
    ibox("El <b>Índice Herfindahl-Hirschman (HHI)</b> mide la concentración de mercado. <b>&lt;1500</b> = competitivo, <b>1500-2500</b> = moderadamente concentrado, <b>&gt;2500</b> = altamente concentrado. Máximo teórico: 10.000 (monopolio).")

    def hhi_class(hhi):
        if hhi > 2500: return "danger"
        if hhi > 1500: return "warn"
        return "ok"

    def hhi_label(hhi):
        if hhi > 2500: return "ALTAMENTE CONCENTRADO"
        if hhi > 1500: return "MODERADAMENTE CONCENTRADO"
        return "MERCADO COMPETITIVO"

    gauges_html = f"""
    <div class="gauge-row">
        <div class="gauge {hhi_class(hhi_dep)}">
            <div class="gauge-val">{hhi_dep:,.0f}</div>
            <div class="gauge-lbl">{hhi_label(hhi_dep)}</div>
            <div style="font-size:.88rem;color:#E2E8F0;font-weight:600;margin-bottom:4px">Depositarias CR</div>
            <div style="font-size:.75rem;color:#475569">{len(dep_funds)} depositarias · {dep_funds.sum()} fondos</div>
            <div class="gauge-bar"><div class="gauge-fill" style="width:{min(100,hhi_dep/100)}%"></div></div>
        </div>
        <div class="gauge {hhi_class(hhi_aud)}">
            <div class="gauge-val">{hhi_aud:,.0f}</div>
            <div class="gauge-lbl">{hhi_label(hhi_aud)}</div>
            <div style="font-size:.88rem;color:#E2E8F0;font-weight:600;margin-bottom:4px">Auditores SAV/EAF</div>
            <div style="font-size:.75rem;color:#475569">{len(aud_counts)} firmas · {aud_counts.sum()} mandatos</div>
            <div class="gauge-bar"><div class="gauge-fill" style="width:{min(100,hhi_aud/100)}%"></div></div>
        </div>
        <div class="gauge {hhi_class(hhi_gest)}">
            <div class="gauge-val">{hhi_gest:,.0f}</div>
            <div class="gauge-lbl">{hhi_label(hhi_gest)}</div>
            <div style="font-size:.88rem;color:#E2E8F0;font-weight:600;margin-bottom:4px">Gestoras CR</div>
            <div style="font-size:.75rem;color:#475569">{len(gest_counts)} gestoras · {gest_counts.sum()} fondos</div>
            <div class="gauge-bar"><div class="gauge-fill" style="width:{min(100,hhi_gest/100)}%"></div></div>
        </div>
    </div>
    """
    st.markdown(gauges_html, unsafe_allow_html=True)

    gdiv()

    # ── DEPOSITARIAS ──
    sec("Depositarias de Capital Riesgo", "🏦")
    ibox(f'Solo <b>{len(dep_funds)} depositarias</b> custodian los activos de <b>{dep_funds.sum():,} fondos de capital riesgo</b>. El top 3 concentra el <b>{shares_dep.nlargest(3).sum():.1f}%</b> del mercado.')

    c1, c2 = st.columns([3, 2])
    with c1:
        sd = shares_dep.sort_values(ascending=True).reset_index()
        sd.columns = ["Depositaria", "Cuota"]
        fig = go.Figure(go.Bar(x=sd["Cuota"], y=sd["Depositaria"], orientation="h",
            marker=dict(color=sd["Cuota"], colorscale=[[0,"#FFBE0B"],[.6,"#F97316"],[1,"#FB7185"]], line_width=0, cornerradius=6),
            text=[f"{v:.1f}%" for v in sd["Cuota"]], textposition="outside",
            textfont=dict(color="#94A3B8", size=11, family="IBM Plex Mono"),
            hovertemplate="<b>%{y}</b><br>%{x:.1f}% cuota de mercado<extra></extra>"))
        sfig(fig, 360); st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = go.Figure(go.Pie(labels=shares_dep.index.tolist(), values=shares_dep.values,
            hole=.55, marker=dict(colors=PAL[:len(shares_dep)], line=dict(color="#030712", width=3)),
            textinfo="percent", textfont=dict(size=10, family="IBM Plex Mono", color="white"),
            hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"))
        sfig(fig, 360)
        fig.update_layout(legend=dict(font=dict(size=9)),
            annotations=[dict(text=f'<b>HHI</b><br><span style="font-size:1.4rem;color:#FB7185">{hhi_dep:,.0f}</span>',
                x=.5,y=.5,font=dict(size=11,color="#94A3B8",family="Outfit"),showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    gdiv()

    # ── AUDITORES ──
    sec("Firmas de Auditoría — SAV & EAF", "🔍")
    ibox(f'<b>{len(aud_counts)} firmas</b> de auditoría cubren todo el mercado de SAV y EAF. Las <b>Big Four</b> (KPMG, Deloitte, PwC, EY) concentran una proporción significativa.')

    c1, c2 = st.columns([3, 2])
    with c1:
        sa = shares_aud.head(12).sort_values(ascending=True).reset_index()
        sa.columns = ["Auditor","Cuota"]
        fig = go.Figure(go.Bar(x=sa["Cuota"],y=sa["Auditor"],orientation="h",
            marker=dict(color=sa["Cuota"],colorscale=[[0,"rgba(129,140,248,.35)"],[.5,"#818CF8"],[1,"#A78BFA"]],line_width=0,cornerradius=6),
            text=[f"{v:.1f}%" for v in sa["Cuota"]],textposition="outside",
            textfont=dict(color="#94A3B8",size=11,family="IBM Plex Mono"),
            hovertemplate="<b>%{y}</b><br>%{x:.1f}% cuota<extra></extra>"))
        sfig(fig,420); st.plotly_chart(fig,use_container_width=True)

    with c2:
        st.markdown("<br>",unsafe_allow_html=True)
        top4 = shares_aud.head(4)
        top4_names = top4.index.tolist()
        big4_share = top4.sum()
        st.markdown(f'<div class="statbox"><div class="sv">{big4_share:.0f}%</div><div class="sl">Cuota Big Four (Top 4 firmas)</div></div>',unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        for name, share in top4.items():
            count = aud_counts[name]
            st.markdown(f'<div class="ibox"><b>{name}</b> — {share:.1f}% ({count} entidades)</div>',unsafe_allow_html=True)

    gdiv()

    # ── GESTORAS ──
    sec("Top 25 Gestoras de Capital Riesgo", "🏢")
    ibox(f'El mercado de gestoras es <b>fragmentado</b> (HHI {hhi_gest:.0f}) con <b>{len(gest_counts)} gestoras</b> para {gest_counts.sum():,} fondos. Las 25 mayores gestionan el <b>{shares_gest.nlargest(25).sum():.1f}%</b>.')

    top25 = gest_counts.nlargest(25).sort_values(ascending=True).reset_index()
    top25.columns = ["Gestora","Fondos"]
    fig = go.Figure(go.Bar(x=top25["Fondos"],y=top25["Gestora"],orientation="h",
        marker=dict(color=top25["Fondos"],colorscale=[[0,"rgba(56,189,248,.3)"],[.5,"#38BDF8"],[1,"#60A5FA"]],line_width=0,cornerradius=5),
        hovertemplate="<b>%{y}</b><br>%{x} fondos<extra></extra>"))
    sfig(fig,640); st.plotly_chart(fig,use_container_width=True)

    gdiv()

    # ── GEOGRAPHIC ──
    sec("Concentración Geográfica", "📍")
    prov = E["direccion_provincia"].value_counts()
    hhi_geo, shares_geo = calc_hhi(prov)

    c1, c2 = st.columns([1, 2])
    with c1:
        gc = hhi_class(hhi_geo)
        st.markdown(f"""
        <div class="gauge {gc}" style="margin-top:10px">
            <div class="gauge-val">{hhi_geo:,.0f}</div>
            <div class="gauge-lbl">{hhi_label(hhi_geo)}</div>
            <div style="font-size:.88rem;color:#E2E8F0;font-weight:600;margin:8px 0 4px">Geográfico SAV/EAF</div>
            <div style="font-size:.75rem;color:#475569">{len(prov)} provincias</div>
            <div class="gauge-bar"><div class="gauge-fill" style="width:{min(100,hhi_geo/100)}%"></div></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        ibox(f'<b>Madrid</b> concentra el <b>{shares_geo.iloc[0]:.1f}%</b> de todas las entidades reguladas — una concentración geográfica extrema.')

    with c2:
        sp = shares_geo.head(10).sort_values(ascending=True).reset_index()
        sp.columns = ["Provincia","Cuota"]
        fig = go.Figure(go.Bar(x=sp["Cuota"],y=sp["Provincia"],orientation="h",
            marker=dict(color=[f"rgba(15,240,179,{.2+.8*i/len(sp)})" for i in range(len(sp))],line_width=0,cornerradius=6),
            text=[f"{v:.1f}%" for v in sp["Cuota"]],textposition="outside",
            textfont=dict(color="#94A3B8",size=11,family="IBM Plex Mono"),
            hovertemplate="<b>%{y}</b><br>%{x:.1f}%<extra></extra>"))
        sfig(fig,380); st.plotly_chart(fig,use_container_width=True)

    foot()
