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
iframe{border:none!important;background:#030712!important;display:block!important}
.stHtml,.stHtml>div,.element-container:has(iframe),.stElementContainer:has(iframe){background:#030712!important;padding:0!important;border:none!important;border-radius:0!important;overflow:hidden!important}
div[data-testid="stHtmlFrame"],div[data-testid="stComponentFrame"]{background:#030712!important;border:none!important;padding:0!important}
.stHtml iframe,.stElementContainer iframe{border:0!important;outline:none!important;background:#030712!important}
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
def build_graph(_E, _F):
    G = nx.Graph()
    people_map = {}  # person -> [(entity, cargo, tipo)]
    socios_map = {}  # socio -> [(entity, pct, tipo)]

    # ── Phase 1: SAV / EAF entities + admins + socios ──
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

    # ── Phase 2: Capital Riesgo — gestoras + depositarias (no individual funds) ──
    uf = _F.drop_duplicates("entity_name")
    gest_dep_funds = {}  # (gestora, depositaria) → count
    gest_fund_count = {}  # gestora → total funds

    for _, r in uf.iterrows():
        gest = r.get("gestora_nombre")
        dep = r.get("depositaria_nombre")
        if pd.notna(gest) and str(gest).strip():
            gest = str(gest).strip()
            gest_fund_count[gest] = gest_fund_count.get(gest, 0) + 1
            if pd.notna(dep) and str(dep).strip():
                dep = str(dep).strip()
                key = (gest, dep)
                gest_dep_funds[key] = gest_dep_funds.get(key, 0) + 1

    # Add gestoras
    for gest, n_funds in gest_fund_count.items():
        if gest not in G:
            G.add_node(gest, nt="gestora", n_funds=n_funds)

    # Add depositarias
    dep_names = set()
    for (gest, dep), count in gest_dep_funds.items():
        dep_names.add(dep)
    for dep in dep_names:
        if dep not in G:
            G.add_node(dep, nt="depositaria")
        elif G.nodes[dep].get("nt") == "socio":
            G.nodes[dep]["nt"] = "depositaria"
            G.nodes[dep]["bridge"] = True

    # Connect gestora → depositaria directly
    for (gest, dep), count in gest_dep_funds.items():
        G.add_edge(gest, dep, rel="deposito", n_funds=count)

    cross = {k:v for k,v in people_map.items() if len(set(e[0] for e in v)) > 1}
    return G, people_map, socios_map, cross

E = load_entities()
F = load_funds()
G, people_map, socios_map, cross_people = build_graph(E, F)

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
    st.markdown('<div class="hero"><div class="hero-title">Red de <span class="em">Poder</span> Financiero</div><div class="hero-sub">El mapa tridimensional de relaciones entre entidades, gestoras, depositarias, administradores y socios del ecosistema financiero español. Arrastra para rotar.</div></div>', unsafe_allow_html=True)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3D NETWORK — THREE.JS WEBGL + BLOOM
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    import json as _json
    import streamlit.components.v1 as _stc

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
            # Scale radius with component size
            comp_radius = max(0.6, np.sqrt(n_nodes) * 0.45)

            t = idx * 0.8
            spiral_r = 3.0 * np.sqrt(t + 1)
            phi = golden_angle * idx
            theta = np.arccos(1 - 2 * ((idx + 0.5) / max(n_comps, 1)))

            cx = spiral_r * np.sin(theta) * np.cos(phi)
            cy = spiral_r * np.sin(theta) * np.sin(phi)
            cz = spiral_r * np.cos(theta) * 0.5

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

    # ── Serialize for Three.js ──
    nodes_js = [{"n": n[:55], "x": round(float(pos3d[n][0]),3), "y": round(float(pos3d[n][1]),3),
                 "z": round(float(pos3d[n][2]),3), "t": G.nodes[n].get("nt",""), "d": G.degree(n),
                 "nf": G.nodes[n].get("n_funds",0)}
                for n in G.nodes() if n in pos3d]
    edges_js = [{"a": [round(float(c),3) for c in pos3d[u]], "b": [round(float(c),3) for c in pos3d[v]],
                 "ta": G.nodes[u].get("nt",""), "tb": G.nodes[v].get("nt","")}
                for u, v in G.edges() if u in pos3d and v in pos3d]
    top30 = sorted(pos3d.keys(), key=lambda n: G.degree(n), reverse=True)[:30]
    core = [round(float(c),3) for c in np.array([pos3d[n] for n in top30]).mean(axis=0)]
    graph_json = _json.dumps({"nodes": nodes_js, "edges": edges_js, "core": core})

    # ── Three.js HTML ──
    threejs_html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body,html{background:#030712;overflow:hidden;font-family:system-ui,-apple-system,sans-serif;width:100%;height:100%}
canvas{display:block}
#tip{position:absolute;background:rgba(6,10,23,0.92);border:1px solid rgba(100,255,218,0.12);
  border-radius:12px;padding:14px 18px;color:#E2E8F0;font-size:12px;pointer-events:none;
  display:none;max-width:320px;z-index:100;backdrop-filter:blur(16px);
  box-shadow:0 4px 24px rgba(0,0,0,0.4),0 0 40px rgba(100,255,218,0.03)}
.tn{font-weight:700;font-size:13px;margin-bottom:4px;color:#F8FAFC}
.tt{font-size:9.5px;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:5px;opacity:0.7}
.tt-e{color:#64FFDA}.tt-a{color:#FFA726}.tt-s{color:#B388FF}.tt-g{color:#FF6B9D}.tt-d{color:#E0F7FA}
.td{color:#94A3B8;font-size:11px}
#ld{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);color:#1E293B;
  font-size:11px;letter-spacing:4px;text-transform:uppercase;z-index:200}
.sp{width:20px;height:20px;border:2px solid #0a1628;border-top-color:#64FFDA;
  border-radius:50%;animation:r .7s linear infinite;margin:0 auto 8px}
@keyframes r{to{transform:rotate(360deg)}}
#leg{position:absolute;bottom:20px;left:20px;display:flex;gap:18px;align-items:center;z-index:50}
.li{display:flex;align-items:center;gap:6px;font-size:11px;color:#64748B;letter-spacing:0.3px}
.ld{width:7px;height:7px;border-radius:50%}
#hint{position:absolute;bottom:20px;right:20px;color:#334155;font-size:10px;letter-spacing:0.5px;z-index:50}
.fade-t{position:absolute;top:0;left:0;right:0;height:80px;background:linear-gradient(to bottom,#030712 0%,transparent 100%);pointer-events:none;z-index:5}
.fade-b{position:absolute;bottom:0;left:0;right:0;height:80px;background:linear-gradient(to top,#030712 0%,transparent 100%);pointer-events:none;z-index:5}
.fade-l{position:absolute;top:0;left:0;bottom:0;width:40px;background:linear-gradient(to right,#030712 0%,transparent 100%);pointer-events:none;z-index:5}
.fade-r{position:absolute;top:0;right:0;bottom:0;width:40px;background:linear-gradient(to left,#030712 0%,transparent 100%);pointer-events:none;z-index:5}
</style></head><body>
<div class="fade-t"></div><div class="fade-b"></div><div class="fade-l"></div><div class="fade-r"></div>
<div id="tip"></div>
<div id="ld"><div class="sp"></div>Cargando red</div>
<div id="leg">
  <div class="li"><div class="ld" style="background:#E0F7FA;box-shadow:0 0 8px #E0F7FA88"></div>Depositarias</div>
  <div class="li"><div class="ld" style="background:#00FFD0;box-shadow:0 0 6px #00FFD066"></div>SAV/EAF</div>
  <div class="li"><div class="ld" style="background:#FF6B9D;box-shadow:0 0 6px #FF6B9D66"></div>Gestoras CR</div>
  <div class="li"><div class="ld" style="background:#B388FF;box-shadow:0 0 6px #B388FF66"></div>Socios</div>
  <div class="li"><div class="ld" style="background:#FFA726;box-shadow:0 0 6px #FFA72666"></div>Admins</div>
</div>
<div id="hint">Arrastra para rotar &middot; Scroll para zoom</div>

<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.160.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.160.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {EffectComposer} from 'three/addons/postprocessing/EffectComposer.js';
import {RenderPass} from 'three/addons/postprocessing/RenderPass.js';
import {UnrealBloomPass} from 'three/addons/postprocessing/UnrealBloomPass.js';
import {OutputPass} from 'three/addons/postprocessing/OutputPass.js';

const D = "__GRAPH_DATA__";
let W=window.innerWidth, H=window.innerHeight;

const scene=new THREE.Scene();
scene.background=new THREE.Color(0x030712);
scene.fog=new THREE.FogExp2(0x030712, 0.005);

const camera=new THREE.PerspectiveCamera(60, W/H, 0.1, 400);
camera.position.set(D.core[0]+20, D.core[1]+20, D.core[2]+14);

const renderer=new THREE.WebGLRenderer({antialias:true, alpha:false});
renderer.setSize(W,H);
renderer.setPixelRatio(Math.min(window.devicePixelRatio,2));
renderer.toneMapping=THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure=1.15;
document.body.appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0x0d1f3c, 0.5));
const keyLight=new THREE.PointLight(0x64FFDA, 0.45, 160);
keyLight.position.copy(camera.position); scene.add(keyLight);
const fillLight=new THREE.PointLight(0xB388FF, 0.2, 120);
fillLight.position.set(D.core[0]-15, D.core[1]+15, D.core[2]+8); scene.add(fillLight);
const rimLight=new THREE.PointLight(0xFFA726, 0.12, 100);
rimLight.position.set(D.core[0]+10, D.core[1]-20, D.core[2]-5); scene.add(rimLight);

const ctrl=new OrbitControls(camera, renderer.domElement);
ctrl.target.set(D.core[0], D.core[1], D.core[2]);
ctrl.enableDamping=true; ctrl.dampingFactor=0.05;
ctrl.autoRotate=true; ctrl.autoRotateSpeed=0.2;
ctrl.maxDistance=160; ctrl.minDistance=3; ctrl.update();

const composer=new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(W,H), 1.0, 0.6, 0.25));
composer.addPass(new OutputPass());

const eP=new Float32Array(D.edges.length*6);
const eC=new Float32Array(D.edges.length*6);
for(let i=0;i<D.edges.length;i++){
  const e=D.edges[i];
  eP[i*6]=e.a[0]; eP[i*6+1]=e.a[1]; eP[i*6+2]=e.a[2];
  eP[i*6+3]=e.b[0]; eP[i*6+4]=e.b[1]; eP[i*6+5]=e.b[2];
  const c=new THREE.Color(0x0a2e2e);
  eC[i*6]=c.r; eC[i*6+1]=c.g; eC[i*6+2]=c.b;
  eC[i*6+3]=c.r; eC[i*6+4]=c.g; eC[i*6+5]=c.b;
}
const eGeo=new THREE.BufferGeometry();
eGeo.setAttribute('position', new THREE.BufferAttribute(eP,3));
eGeo.setAttribute('color', new THREE.BufferAttribute(eC,3));
scene.add(new THREE.LineSegments(eGeo,
  new THREE.LineBasicMaterial({vertexColors:true, transparent:true, opacity:0.55})));

const sGeo=new THREE.IcosahedronGeometry(1,3);
const types={
  depositaria:{color:0xE0F7FA,emissive:0xE0F7FA,eI:0.7,sMin:0.25,sMax:0.55,label:'Depositaria',cls:'tt-d'},
  entity:{color:0x00FFD0, emissive:0x00FFD0, eI:0.4, sMin:0.10, sMax:0.38, label:'Entidad SAV/EAF', cls:'tt-e'},
  gestora:{color:0xFF6B9D,emissive:0xFF6B9D,eI:0.35,sMin:0.06,sMax:0.22,label:'Gestora',cls:'tt-g'},
  admin: {color:0xFFA726, emissive:0xFFA726, eI:0.28, sMin:0.04, sMax:0.13, label:'Administrador', cls:'tt-a'},
  socio: {color:0xB388FF, emissive:0xB388FF, eI:0.28, sMin:0.04, sMax:0.13, label:'Socio', cls:'tt-s'}
};
const mM={}, nM={}, dm=new THREE.Object3D();

for(const[type,cfg] of Object.entries(types)){
  const nodes=D.nodes.filter(n=>n.t===type);
  if(!nodes.length)continue;
  nM[type]=nodes;
  const mat=new THREE.MeshStandardMaterial({
    color:cfg.color, emissive:cfg.emissive, emissiveIntensity:cfg.eI,
    roughness:0.25, metalness:0.15
  });
  const mesh=new THREE.InstancedMesh(sGeo, mat, nodes.length);
  const mx=Math.max(...nodes.map(n=>n.d),1);
  for(let i=0;i<nodes.length;i++){
    const n=nodes[i], s=cfg.sMin+(n.d/mx)*(cfg.sMax-cfg.sMin);
    dm.position.set(n.x,n.y,n.z);
    dm.scale.setScalar(s);
    dm.updateMatrix();
    mesh.setMatrixAt(i,dm.matrix);
  }
  mesh.instanceMatrix.needsUpdate=true;
  scene.add(mesh); mM[type]=mesh;
}

const dN=3000, dPos=new Float32Array(dN*3), dCol=new Float32Array(dN*3);
for(let i=0;i<dN;i++){
  dPos[i*3]=(Math.random()-0.5)*180;
  dPos[i*3+1]=(Math.random()-0.5)*180;
  dPos[i*3+2]=(Math.random()-0.5)*180;
  const b=0.015+Math.random()*0.035;
  const hue=Math.random();
  if(hue<0.5){dCol[i*3]=b*0.4;dCol[i*3+1]=b;dCol[i*3+2]=b*0.85}
  else if(hue<0.8){dCol[i*3]=b*0.6;dCol[i*3+1]=b*0.55;dCol[i*3+2]=b}
  else{dCol[i*3]=b;dCol[i*3+1]=b*0.7;dCol[i*3+2]=b*0.3}
}
const dGeo=new THREE.BufferGeometry();
dGeo.setAttribute('position',new THREE.BufferAttribute(dPos,3));
dGeo.setAttribute('color',new THREE.BufferAttribute(dCol,3));
scene.add(new THREE.Points(dGeo,
  new THREE.PointsMaterial({size:0.1,vertexColors:true,transparent:true,opacity:0.5,sizeAttenuation:true})));

const ringGeo=new THREE.RingGeometry(15, 15.06, 128);
const ringMat=new THREE.MeshBasicMaterial({color:0x0a2a2a, transparent:true, opacity:0.15, side:THREE.DoubleSide});
const ring=new THREE.Mesh(ringGeo, ringMat);
ring.position.set(D.core[0], D.core[1], D.core[2]-2);
ring.rotation.x=Math.PI/2;
scene.add(ring);
const ring2Geo=new THREE.RingGeometry(30, 30.04, 128);
const ring2=new THREE.Mesh(ring2Geo, ringMat.clone());
ring2.material.opacity=0.08;
ring2.position.set(D.core[0], D.core[1], D.core[2]-2);
ring2.rotation.x=Math.PI/2;
scene.add(ring2);

const tip=document.getElementById('tip');
const rc=new THREE.Raycaster();
const msv=new THREE.Vector2();
let mx2=0,my2=0;
renderer.domElement.addEventListener('mousemove',e=>{
  const rect=renderer.domElement.getBoundingClientRect();
  msv.x=((e.clientX-rect.left)/rect.width)*2-1;
  msv.y=-((e.clientY-rect.top)/rect.height)*2+1;
  mx2=e.clientX; my2=e.clientY;
});

function hov(){
  rc.setFromCamera(msv,camera);
  let hit=false;
  for(const[type,mesh] of Object.entries(mM)){
    const its=rc.intersectObject(mesh);
    if(its.length){
      const nd=nM[type][its[0].instanceId];
      tip.innerHTML='<div class="tn">'+nd.n+'</div><div class="tt '+types[type].cls+'">'+types[type].label+'</div><div class="td">'+nd.d+' conexiones</div>';
      tip.style.display='block';
      tip.style.left=Math.min(mx2+16,W-330)+'px';
      tip.style.top=Math.max(my2-60,8)+'px';
      hit=true; renderer.domElement.style.cursor='pointer'; break;
    }
  }
  if(!hit){tip.style.display='none'; renderer.domElement.style.cursor='grab';}
}

document.getElementById('ld').style.display='none';

let t=0;
function animate(){
  requestAnimationFrame(animate);
  t+=0.012;
  ctrl.update();
  keyLight.position.copy(camera.position);

  // Breathing glow on all node types
  for(const[type,mesh] of Object.entries(mM)){
    const base=types[type].eI;
    const speed=type==='depositaria'?1.8:type==='entity'?1.2:0.8;
    const amp=type==='depositaria'?0.15:0.06;
    mesh.material.emissiveIntensity=base+Math.sin(t*speed)*amp;
  }

  // Swirling dust particles
  const dp=dGeo.attributes.position.array;
  for(let i=0;i<dN;i++){
    const phase=i*0.37;
    dp[i*3]+=Math.sin(t*0.4+phase)*0.004;
    dp[i*3+1]+=Math.cos(t*0.3+phase)*0.005;
    dp[i*3+2]+=Math.sin(t*0.5+phase*0.7)*0.003;
  }
  dGeo.attributes.position.needsUpdate=true;

  // Orbiting fill light
  fillLight.position.x=D.core[0]+Math.cos(t*0.15)*20;
  fillLight.position.z=D.core[2]+Math.sin(t*0.15)*15;

  hov();
  composer.render();
}
animate();

window.addEventListener('resize',()=>{
  W=window.innerWidth; H=window.innerHeight;
  camera.aspect=W/H; camera.updateProjectionMatrix();
  renderer.setSize(W,H); composer.setSize(W,H);
});
</script></body></html>'''.replace('"__GRAPH_DATA__"', graph_json)



    _stc.html(threejs_html, height=850)

    # Legend is now inside Three.js canvas

    n_gest = sum(1 for n in G.nodes() if G.nodes[n].get("nt") == "gestora")
    n_dep = sum(1 for n in G.nodes() if G.nodes[n].get("nt") == "depositaria")
    kpi_row([
        (f"{G.number_of_nodes():,}", "Nodos en la Red", "🔵", "c1"),
        (f"{G.number_of_edges():,}", "Conexiones", "🔗", "c2"),
        (f"{len(E)} + {n_gest}", "SAV/EAF + Gestoras", "🏛️", "c3"),
        (f"{n_gest}", "Gestoras Capital Riesgo", "📊", "c4"),
    ])

    gdiv()

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # TABS BELOW THE GRAPH
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    tab1, tab2, tab3 = st.tabs(["🏛️ Explorador por Entidad", "👥 Conexiones Cruzadas", "💰 Capital Riesgo"])

    # ─── TAB 1: EGO NETWORK — now includes gestoras + depositarias ───
    with tab1:
        sec("Explorador de Red", "🏛️")
        ibox("Selecciona cualquier nodo del ecosistema — entidad SAV/EAF, gestora o depositaria — para ver su <b>red de relaciones</b> a 1-2 grados de separación.")

        # Build explorable list: entities + gestoras + depositarias
        ent_list = sorted(E["nombre"].tolist())
        gest_list = sorted([n for n in G.nodes() if G.nodes[n].get("nt") == "gestora"])
        dep_list = sorted([n for n in G.nodes() if G.nodes[n].get("nt") == "depositaria"])

        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            all_explorable = dep_list + ent_list + gest_list
            labels = {n: f"⬡ {n}" for n in dep_list}
            labels.update({n: f"● {n}" for n in ent_list})
            labels.update({n: f"◆ {n}" for n in gest_list})
            selected = st.selectbox("Selecciona un nodo", all_explorable,
                format_func=lambda x: labels.get(x, x),
                index=all_explorable.index("ALANTRA EQUITIES SOCIEDAD DE VALORES, S.A.") if "ALANTRA EQUITIES SOCIEDAD DE VALORES, S.A." in all_explorable else 0)
        with c2:
            radius = st.select_slider("Profundidad", options=[1, 2, 3], value=2)
        with c3:
            node_type = G.nodes[selected].get("nt", "") if selected in G else ""
            type_labels = {"entity": "SAV/EAF", "gestora": "Gestora", "depositaria": "Depositaria"}
            st.markdown(f'<div style="padding:8px 0;"><span class="ebadge ebadge-s" style="font-size:.75rem">{type_labels.get(node_type, node_type)}</span></div>', unsafe_allow_html=True)

        if selected and selected in G:
            fig = ego_graph_fig(G, selected, radius=radius)
            if fig:
                ego = nx.ego_graph(G, selected, radius=radius)
                n_ent = sum(1 for _,d in ego.nodes(data=True) if d.get("nt")=="entity")
                n_ppl = sum(1 for _,d in ego.nodes(data=True) if d.get("nt") in ("admin","socio"))
                n_gest = sum(1 for _,d in ego.nodes(data=True) if d.get("nt")=="gestora")
                n_dep = sum(1 for _,d in ego.nodes(data=True) if d.get("nt")=="depositaria")

                kpi_row([
                    (str(len(ego.nodes())), "Nodos en Red", "🔵", "c1"),
                    (str(n_ent), "Entidades", "🏛️", "c4"),
                    (str(n_gest), "Gestoras", "📊", "c2"),
                    (str(n_ppl), "Personas", "👤", "c3"),
                ])

                st.plotly_chart(fig, use_container_width=True)

                gdiv()

                # ── Detail card depends on node type ──
                if node_type == "entity":
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

                elif node_type == "gestora":
                    gest_funds = F[F["gestora_nombre"] == selected].drop_duplicates("entity_name")
                    n_f = len(gest_funds)
                    deps_used = gest_funds["depositaria_nombre"].dropna().unique()
                    types_managed = gest_funds["entity_type"].value_counts()

                    dets = [("Fondos gestionados", str(n_f)),
                            ("Depositarias utilizadas", ", ".join(str(d)[:40] for d in deps_used) if len(deps_used) else "—"),
                            ("Tipos de fondo", ", ".join(f"{t} ({c})" for t,c in types_managed.items()))]
                    rh = "".join(f'<div class="erow"><span class="erow-k">{k}</span><span class="erow-v">{v}</span></div>' for k,v in dets)
                    st.markdown(f'<div class="ecard"><div class="ename">{selected[:60]}</div><span class="ebadge ebadge-s">◆ Gestora de Capital Riesgo</span><div class="erows">{rh}</div></div>', unsafe_allow_html=True)

                    if n_f > 0:
                        sec("Fondos Gestionados", "💰")
                        fund_df = gest_funds[["entity_name","entity_type","depositaria_nombre","fecha_registro"]].copy()
                        fund_df.columns = ["Fondo","Tipo","Depositaria","Fecha Registro"]
                        st.dataframe(fund_df, use_container_width=True, hide_index=True, height=min(400, 35*n_f+38))

                elif node_type == "depositaria":
                    dep_funds = F[F["depositaria_nombre"] == selected].drop_duplicates("entity_name")
                    n_f = len(dep_funds)
                    gest_connected = dep_funds["gestora_nombre"].dropna().nunique()

                    dets = [("Fondos en custodia", str(n_f)),
                            ("Gestoras conectadas", str(gest_connected)),
                            ("Tipos de fondo", ", ".join(f"{t} ({c})" for t,c in dep_funds["entity_type"].value_counts().head(5).items()))]
                    rh = "".join(f'<div class="erow"><span class="erow-k">{k}</span><span class="erow-v">{v}</span></div>' for k,v in dets)
                    st.markdown(f'<div class="ecard"><div class="ename">{selected[:60]}</div><span class="ebadge ebadge-e">⬡ Depositaria</span><div class="erows">{rh}</div></div>', unsafe_allow_html=True)

                    # Is this a bridge entity?
                    if G.nodes[selected].get("bridge"):
                        ibox(f'<b>Nodo puente:</b> {selected[:40]} es socio de entidades SAV/EAF y depositaria de fondos de capital riesgo. Conecta ambos ecosistemas.')

                    sec("Top Gestoras por Fondos en Custodia", "📊")
                    gest_rank = dep_funds.groupby("gestora_nombre").size().sort_values(ascending=False).head(15).reset_index()
                    gest_rank.columns = ["Gestora", "Fondos"]
                    st.dataframe(gest_rank, use_container_width=True, hide_index=True)

            else:
                st.info("Este nodo no tiene conexiones en la red.")

    # ─── TAB 2: CROSS CONNECTIONS + BRIDGES ───
    with tab2:
        sec("Personas en Múltiples Entidades", "🔗")
        ibox(f'<b>{len(cross_people)} personas</b> ocupan cargos en más de una entidad regulada simultáneamente. Estas conexiones cruzadas revelan los centros de poder del ecosistema financiero español.')

        # ── Bridge entities highlight ──
        bridge_nodes = [n for n in G.nodes() if G.nodes[n].get("bridge")]
        if bridge_nodes:
            sec("Nodos Puente", "🌉")
            ibox("Estas entidades conectan el mundo SAV/EAF con el capital riesgo — aparecen como socios en el primer ecosistema y como depositarias en el segundo.")
            for bn in bridge_nodes:
                neighbors = list(G.neighbors(bn))
                n_ent = sum(1 for nb in neighbors if G.nodes[nb].get("nt") == "entity")
                n_gest = sum(1 for nb in neighbors if G.nodes[nb].get("nt") == "gestora")
                n_fund_dep = len(F[F["depositaria_nombre"] == bn].drop_duplicates("entity_name"))
                st.markdown(f'<div class="pcard"><div class="pcard-name">{bn}</div><div class="pcard-sub">NODO PUENTE</div>'
                    f'<div class="pcard-ent"><div class="pcard-dot" style="background:#0FF0B3"></div><span style="color:#E2E8F0">Socio de <b>{n_ent}</b> entidad(es) SAV/EAF</span></div>'
                    f'<div class="pcard-ent"><div class="pcard-dot" style="background:#FF6B9D"></div><span style="color:#E2E8F0">Depositaria de <b>{n_fund_dep}</b> fondos de capital riesgo</span></div>'
                    f'</div>', unsafe_allow_html=True)
            gdiv()

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

    # ─── TAB 3: CAPITAL RIESGO OVERVIEW ───
    with tab3:
        sec("Ecosistema Capital Riesgo", "💰")
        ibox(f'Visión completa del capital riesgo registrado en CNMV: <b>{F["entity_name"].nunique():,} fondos</b> gestionados por <b>{F["gestora_nombre"].nunique()} gestoras</b> y custodiados por <b>{F["depositaria_nombre"].dropna().nunique()} depositarias</b>.')

        c1, c2 = st.columns(2)
        with c1:
            sec("Top 15 Gestoras por Fondos", "📊")
            gest_top = F.drop_duplicates("entity_name").groupby("gestora_nombre").agg(
                Fondos=("entity_name","count"),
                Depositarias=("depositaria_nombre","nunique"),
                Tipos=("entity_type","nunique")
            ).sort_values("Fondos", ascending=False).head(15).reset_index()
            gest_top.columns = ["Gestora", "Fondos", "Depositarias", "Tipos"]
            st.dataframe(gest_top, use_container_width=True, hide_index=True)

        with c2:
            sec("Depositarias — Concentración", "🏦")
            dep_top = F.drop_duplicates("entity_name").groupby("depositaria_nombre").agg(
                Fondos=("entity_name","count"),
                Gestoras=("gestora_nombre","nunique")
            ).sort_values("Fondos", ascending=False).reset_index()
            dep_top.columns = ["Depositaria", "Fondos", "Gestoras"]
            st.dataframe(dep_top, use_container_width=True, hide_index=True)

        gdiv()
        sec("Distribución por Tipo de Fondo", "📋")
        type_counts = F.drop_duplicates("entity_name")["entity_type"].value_counts().reset_index()
        type_counts.columns = ["Tipo de Fondo", "Cantidad"]
        st.dataframe(type_counts, use_container_width=True, hide_index=True)

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
