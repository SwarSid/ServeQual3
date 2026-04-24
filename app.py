import streamlit as st
import pandas as pd
import re
from collections import defaultdict

st.set_page_config(page_title="HCP Qual Insight Engine", layout="wide", page_icon="🔬")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Geist:wght@300;400;500;600&display=swap');
html,body,[data-testid="stAppViewContainer"]{background:#080c14!important;color:#c8d4e8;font-family:'Geist',sans-serif}
[data-testid="stHeader"]{background:transparent!important}
.block-container{padding:1.5rem 2rem!important;max-width:1600px!important}
.stTextInput>div>div>input{background:#0d1420!important;border:1px solid #1e2d47!important;border-radius:10px!important;color:#e2ecf8!important;font-size:15px!important;padding:12px 18px!important}
.card{background:#0d1420;border:1px solid #1a2640;border-radius:12px;padding:18px 22px;margin-bottom:14px}
.stat-num{font-family:'IBM Plex Mono',monospace;font-size:38px;font-weight:600;color:#e2ecf8;line-height:1}
.stat-lbl{font-size:10px;color:#4a6080;letter-spacing:1.5px;text-transform:uppercase;margin-top:4px}
.sec-lbl{font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#3b6ef7;font-weight:600;margin-bottom:12px;font-family:'IBM Plex Mono',monospace}
.fq-card{background:#0a1220;border:1px solid #1a2640;border-left:3px solid #3b6ef7;border-radius:0 12px 12px 0;padding:16px 20px;margin-bottom:12px}
.fq-card.comm{border-left-color:#f59e0b}
.fq-card.acad{border-left-color:#3b6ef7}
.fq-meta{font-family:'IBM Plex Mono',monospace;font-size:10px;color:#4a6080;margin-bottom:8px}
.fq-text{font-size:13px;color:#c8d4e8;line-height:1.9;font-style:italic}
.hl-ins{background:rgba(249,115,22,.25);border-radius:3px;padding:1px 4px;color:#fb923c;font-style:normal;font-weight:600}
.hl-pfs{background:rgba(59,130,246,.25);border-radius:3px;padding:1px 4px;color:#60a5fa;font-style:normal;font-weight:600}
.hl-os{background:rgba(139,92,246,.25);border-radius:3px;padding:1px 4px;color:#a78bfa;font-style:normal;font-weight:600}
.hl-saf{background:rgba(245,158,11,.25);border-radius:3px;padding:1px 4px;color:#fbbf24;font-style:normal;font-weight:600}
.hl-sz{background:rgba(239,68,68,.25);border-radius:3px;padding:1px 4px;color:#f87171;font-style:normal;font-weight:600}
.hl-qol{background:rgba(16,185,129,.25);border-radius:3px;padding:1px 4px;color:#34d399;font-style:normal;font-weight:600}
.hl-oral{background:rgba(132,204,22,.25);border-radius:3px;padding:1px 4px;color:#a3e635;font-style:normal;font-weight:600}
.hl-trial{background:rgba(251,191,36,.25);border-radius:3px;padding:1px 4px;color:#fcd34d;font-style:normal;font-weight:600}
.hl-nccn{background:rgba(167,139,250,.25);border-radius:3px;padding:1px 4px;color:#c4b5fd;font-style:normal;font-weight:600}
.hl-def{background:rgba(59,110,247,.2);border-radius:3px;padding:1px 4px;color:#93c5fd;font-style:normal;font-weight:600}
.tag{display:inline-block;padding:2px 8px;border-radius:99px;font-size:10px;font-weight:600;margin-right:4px;margin-top:2px}
.bar-row{display:flex;align-items:center;gap:10px;margin-bottom:9px}
.bar-lbl{font-size:11px;color:#8a9ab5;min-width:180px}
.bar-trk{flex:1;height:5px;background:#1a2640;border-radius:3px}
.bar-fill{height:5px;border-radius:3px}
.bar-cnt{font-family:'IBM Plex Mono',monospace;font-size:11px;color:#4a6080;min-width:60px;text-align:right}
.diff-pos{color:#10b981;font-weight:700}
.diff-neg{color:#ef4444;font-weight:700}
.seg-a{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.3);padding:2px 10px;border-radius:99px;font-size:11px;font-weight:600}
.seg-b{background:rgba(59,110,247,.15);color:#93c5fd;border:1px solid rgba(59,110,247,.3);padding:2px 10px;border-radius:99px;font-size:11px;font-weight:600}
.ibadge{display:inline-block;padding:3px 12px;border-radius:99px;font-size:10px;font-weight:600;letter-spacing:1px;text-transform:uppercase;background:rgba(59,110,247,.12);color:#3b6ef7;border:1px solid rgba(59,110,247,.25);margin-right:6px}
.tbadge{display:inline-block;padding:3px 12px;border-radius:99px;font-size:10px;background:rgba(16,185,129,.1);color:#34d399;border:1px solid rgba(16,185,129,.2);margin-right:6px}
[data-testid="stExpander"]{background:#0d1420!important;border:1px solid #1a2640!important;border-radius:10px!important}
.stButton>button{background:#0d1420!important;border:1px solid #1e2d47!important;color:#8a9ab5!important;border-radius:8px!important;font-size:11px!important;padding:5px 10px!important;width:100%!important;text-align:left!important;white-space:normal!important;height:auto!important}
.stButton>button:hover{border-color:#3b6ef7!important;color:#93c5fd!important}
.stSelectbox>div>div{background:#0d1420!important;border:1px solid #1e2d47!important;color:#c8d4e8!important;border-radius:8px!important}
hr{border:none;border-top:1px solid #1a2640;margin:20px 0}
</style>
""", unsafe_allow_html=True)

# ── THEMES ────────────────────────────────────────────────────────────────────
THEMES = {
    "PFS":                 ["progression free survival","progression-free","pfs","time to progression","time to next intervention","time to next treatment"],
    "OS":                  ["overall survival"," os ","lifespan","live longer","living longer","survivability"],
    "Safety/Tolerability": ["side effect","adverse event","toxicity","tolerab","tolerat","fatigue","nausea","hepato","liver function","myelosuppression","hematotoxicity","well tolerated"],
    "Seizures":            ["seizure","epilepsy","seizure control","seizure frequency","seizure reduction","seizure prophylaxis","anti-seizure"],
    "Quality of Life":     ["quality of life","qol","daily activities","activities of daily","functional","cognitive","cognition","brain fog","neurocognit"],
    "Efficacy":            ["efficacy","effective","response rate","tumor reduction","tumor shrinkage","disease control","proven benefit","superior efficacy"],
    "Oral Administration": ["oral","pill","tablet","once daily","easy to take","easy to administer","oral formulation","oral daily"],
    "Cost/Insurance":      ["reimburs","insurance","prior auth","formulary","coverage","copay","co-pay","cost","afford","appeal","denial","out of pocket","financial","free drug"],
    "Patient Assistance":  ["patient assistance","patient support","financial assistance","manufacturer assistance","copay program","compassionate use","patient program"],
    "NCCN/Guidelines":     ["nccn","guideline","standard of care","fda approved","fda approval","category 1","category 2","institutional","formulary"],
    "Indigo Trial":        ["indigo trial","indigo study","phase 3","phase three","clinical trial data","indigo","nejm","new england journal"],
    "Radiation Delay":     ["delay radiation","defer radiation","avoid radiation","delay radiotherapy","delay chemo","defer chemo","avoid chemo"],
    "Surgery/Resection":   ["resection","biopsy","subtotal resection","gross total resection","residual tumor","residual disease"],
    "Targeted Therapy":    ["targeted therapy","targeted","mechanism of action","isocitrate","targeted treatment","idh inhibitor","blood-brain barrier"],
    "IDH Mutation":        ["idh1","idh2","idh mutation","idh mutant","idh inhibitor","isocitrate dehydrogenase","idh status"],
    "Fertility":           ["fertilit","birth defect","pregnan","desire to have children","family planning"],
    "Performance Status":  ["ecog","performance status","kps","fit patient","younger patient","functional status"],
    "Rep Support":         ["representative","drug rep","pharma rep"," rep ","lunch","dinner","detail","rep support"],
}

TC = {
    "PFS":"#3b82f6","OS":"#8b5cf6","Safety/Tolerability":"#f59e0b",
    "Seizures":"#ef4444","Quality of Life":"#10b981","Efficacy":"#06b6d4",
    "Oral Administration":"#84cc16","Cost/Insurance":"#f97316",
    "Patient Assistance":"#ec4899","NCCN/Guidelines":"#a78bfa",
    "Indigo Trial":"#fbbf24","Radiation Delay":"#fb7185",
    "Surgery/Resection":"#94a3b8","Targeted Therapy":"#34d399",
    "IDH Mutation":"#22d3ee","Fertility":"#f472b6",
    "Performance Status":"#60a5fa","Rep Support":"#fcd34d",
}

HL_MAP = {
    "Cost/Insurance":"hl-ins","Patient Assistance":"hl-ins",
    "PFS":"hl-pfs","OS":"hl-os","Safety/Tolerability":"hl-saf","Seizures":"hl-sz",
    "Quality of Life":"hl-qol","Oral Administration":"hl-oral",
    "Indigo Trial":"hl-trial","NCCN/Guidelines":"hl-nccn",
}

DRIVER_MAP = {
    "Efficacy / PFS Data":     ["efficacy","effective","response","pfs","progression free","survival benefit","indigo","phase 3"],
    "Tolerability":            ["tolerab","tolerat","side effect","well tolerated","low toxicity","manageable","minimal side"],
    "Oral Convenience":        ["oral","pill","tablet","once daily","convenient","easy to take"],
    "Cost / Access":           ["cost","afford","insurance","reimburs","copay","access","patient assistance","denied"],
    "Targeted Mechanism":      ["targeted","idh","mechanism of action","targeted therapy","isocitrate","blood-brain"],
    "Delay Radiation/Chemo":   ["delay radiation","defer radiation","avoid radiation","delay chemo","defer chemo"],
    "Clinical Trial (Indigo)": ["indigo","phase 3","clinical trial","nejm","new england journal"],
    "NCCN / FDA":              ["nccn","guideline","standard of care","fda"],
    "Seizure Control":         ["seizure","epilepsy","seizure control","seizure frequency"],
    "Quality of Life":         ["quality of life","qol","daily activities","cognitive","neurocognit"],
    "Patient Selection":       ["grade 2","idh mutant","residual tumor","subtotal resection","mutation status","performance status"],
}

# ── EXCEL LOADER ──────────────────────────────────────────────────────────────
def load_excel(file):
    """
    Robust loader handling:
    1. Sagan_Drivers format — header at row 0: Target | Specialty | Setting | Text
    2. Sagan_Responses format — metadata rows at top, data starts at row 8+
    3. Generic qual format — auto-detect
    """
    import openpyxl

    # ── Step 1: scan with openpyxl to find the real header row ───────────────
    try:
        wb = openpyxl.load_workbook(file, read_only=True)
        ws = wb.active
        all_rows = list(ws.iter_rows(values_only=True))
        wb.close()
    except Exception as e:
        return None, f"Cannot open file: {e}"

    if not all_rows:
        return None, "File is empty."

    # Find first row with 3+ non-null values — that's our header/data start
    header_row = 0
    for i, row in enumerate(all_rows):
        non_null = [v for v in row if v is not None]
        if len(non_null) >= 3:
            header_row = i
            break

    # ── Step 2: read with pandas using correct header row ─────────────────────
    try:
        raw = pd.read_excel(file, header=header_row)
    except Exception as e:
        return None, f"Cannot read file: {e}"

    if raw.empty:
        return None, "No data found after header row."

    # Convert all to string for uniform processing
    raw = raw.astype(str).replace("nan", pd.NA).replace("None", pd.NA)

    # ── Step 3: identify text column (highest avg string length) ─────────────
    avg_lens = {}
    for c in raw.columns:
        lengths = raw[c].dropna().apply(lambda x: len(str(x)))
        avg_lens[c] = lengths.mean() if len(lengths) > 0 else 0

    if not avg_lens or max(avg_lens.values()) < 30:
        return None, "No verbatim text column found. Check your file has a column with interview responses."

    text_col = max(avg_lens, key=avg_lens.get)

    # ── Step 4: filter to real content rows ───────────────────────────────────
    mask = raw[text_col].apply(lambda x: isinstance(x, str) and len(x.strip()) > 80)
    data = raw[mask].reset_index(drop=True)

    if len(data) == 0:
        return None, f"No rows with text >80 chars in column '{text_col}'. Check your verbatim column."

    # ── Step 5: identify metadata columns ─────────────────────────────────────
    meta_cols = []
    for c in raw.columns:
        if c == text_col: continue
        col_data = data[c].dropna()
        if len(col_data) == 0: continue
        avg_len = col_data.apply(lambda x: len(str(x))).mean()
        n_unique = col_data.nunique()
        if avg_len < 60 and 1 < n_unique <= 30:
            meta_cols.append(c)

    def best_col(keywords, fallback="Unknown"):
        """Match by column values first, then column header name."""
        # Try matching keywords against column VALUES
        for c in meta_cols:
            vals = data[c].dropna().astype(str).str.upper().tolist()
            if any(any(kw.upper() in v for kw in keywords) for v in vals):
                return data[c].fillna(fallback).astype(str).str.strip()
        # Try matching keywords against COLUMN NAMES
        for c in meta_cols:
            col_name = str(c).upper()
            if any(kw.upper() in col_name for kw in keywords):
                return data[c].fillna(fallback).astype(str).str.strip()
        # Fallback: first available meta col
        if meta_cols:
            return data[meta_cols[0]].fillna(fallback).astype(str).str.strip()
        return pd.Series([fallback] * len(data))

    out = pd.DataFrame()
    out["id"]        = [f"R_{i+1:03d}" for i in range(len(data))]
    out["text"]      = data[text_col].astype(str)

    # Setting — look for Academic/Community in values OR "setting/practice" in header
    out["setting"]   = best_col(["COMMUNITY","ACADEMIC","PRIVATE","HOSPITAL","TEACHING",
                                  "SETTING","PRACTICE","SITE","INSTITUTION"])
    # Simplify setting values: extract Community/Academic/Private from long strings
    def simplify_setting(v):
        vu = str(v).upper()
        if "ACADEMIC" in vu: return "Academic"
        if "COMMUNITY" in vu: return "Community"
        if "PRIVATE" in vu: return "Private Practice"
        if "TEACHING" in vu: return "Teaching Hospital"
        return v
    out["setting"] = out["setting"].apply(simplify_setting)

    out["target"]    = best_col(["TL","TARGET","TIER","ON TL","OFF TL","CO-LOC",
                                  "COLOC","PRIORITY","LIST"])
    out["specialty"] = best_col(["ONCOL","ONCOLOGY","NEURO","HEMATOL","MEDONC",
                                  "HEMEONC","SPEC","DISCIPLINE","HCP TYPE","NEUROLOGY",
                                  "CLINICAL","MEDICAL"])
    # Simplify specialty values
    def simplify_specialty(v):
        vu = str(v).upper()
        if "NEURO-ONC" in vu or "NEURO ONC" in vu: return "Neuro-Onc"
        if "NEUROLOGY" in vu: return "Neurology"
        if "HEMATOL" in vu: return "HemeOnc"
        if "MEDICAL" in vu or "CLINICAL" in vu: return "MedOnc"
        return v
    out["specialty"] = out["specialty"].apply(simplify_specialty)

    # ── Step 6: extract doctor-only speech ────────────────────────────────────
    def doctor_text(t):
        # SPEAKER_B pattern
        lines = re.findall(r'SPEAKER_B:\s*(.+?)(?=SPEAKER_A:|SPEAKER_B:|$)', t, re.DOTALL)
        cleaned = [re.sub(r'\s+', ' ', l).strip() for l in lines if len(l.strip()) > 15]
        result = ' '.join(cleaned)
        if len(result) > 50: return result
        # Doctor: pattern
        lines2 = re.findall(r'Doctor:\s*(.+?)(?=AI Moderator:|Doctor:|$)', t, re.DOTALL)
        cleaned2 = [re.sub(r'\s+', ' ', l).strip() for l in lines2 if len(l.strip()) > 15]
        result2 = ' '.join(cleaned2)
        if len(result2) > 50: return result2
        return t  # fallback: full text

    out["text"]       = out["text"].apply(doctor_text)
    out["text_lower"] = out["text"].str.lower()

    return out, None

# ── FULL QUOTE HIGHLIGHT + RENDER ─────────────────────────────────────────────
def hl_text(text, focus=None):
    result = text
    order = (focus or []) + [t for t in THEMES if not focus or t not in focus]
    pairs = []
    for theme in order:
        css = HL_MAP.get(theme, "hl-def")
        for p in THEMES[theme]:
            pairs.append((p, css, len(p)))
    pairs.sort(key=lambda x: -x[2])
    for p, css, _ in pairs:
        result = re.sub(f'({re.escape(p)})', f'<span class="{css}">\\1</span>',
                        result, flags=re.IGNORECASE, count=3)
    return result

def quote_card(row, focus=None):
    is_c = str(row.get("setting","")).upper() in ["COMMUNITY","COMM"]
    css = "fq-card comm" if is_c else "fq-card acad"
    sbadge = f'<span class="seg-a">{row["setting"]}</span>' if is_c else f'<span class="seg-b">{row["setting"]}</span>'
    tags = "".join(f'<span class="tag" style="background:{TC.get(t,"#4a6080")}22;color:{TC.get(t,"#4a6080")};border:1px solid {TC.get(t,"#4a6080")}33">{t}</span>'
                   for t, pats in THEMES.items() if any(p in str(row.get("text_lower","")) for p in pats))
    h = hl_text(str(row.get("text","")), focus)
    st.markdown(f"""<div class="{css}">
        <div class="fq-meta">📎 <b style="color:#e2ecf8">{row["id"]}</b> &nbsp;{sbadge}&nbsp;
        <span>{row.get("specialty","")}</span> &nbsp; <span>{row.get("target","")}</span></div>
        <div class="fq-text">{h}</div>
        <div style="margin-top:10px;border-top:1px solid #1a2640;padding-top:6px">{tags}</div>
    </div>""", unsafe_allow_html=True)

# ── ANALYTICS ─────────────────────────────────────────────────────────────────
def mtch(tl, pats): return any(p in tl for p in pats)
def t_counts(df): return {t: int(df["text_lower"].apply(lambda x: mtch(x,p)).sum()) for t,p in THEMES.items()}
def d_counts(df): return {d: int(df["text_lower"].apply(lambda x: mtch(x,p)).sum()) for d,p in DRIVER_MAP.items()}

def bar_html(label, count, total, color="#3b6ef7"):
    pct = round(count/total*100) if total else 0
    st.markdown(f"""<div class="bar-row">
        <div class="bar-lbl">{label}</div>
        <div class="bar-trk"><div class="bar-fill" style="width:{pct}%;background:{color}"></div></div>
        <div class="bar-cnt">{count} <span style="color:#2a3a55">({pct}%)</span></div>
    </div>""", unsafe_allow_html=True)

# ── ENGINES ───────────────────────────────────────────────────────────────────
def co_occur(ta, tb, df):
    pa, pb = THEMES.get(ta,[ta.lower()]), THEMES.get(tb,[tb.lower()])
    T = len(df)
    both_rows = [row for _,row in df.iterrows() if any(p in row["text_lower"] for p in pa) and any(p in row["text_lower"] for p in pb)]
    nb = len(both_rows)
    oa = int(df["text_lower"].apply(lambda x: any(p in x for p in pa) and not any(p in x for p in pb)).sum())
    ob = int(df["text_lower"].apply(lambda x: any(p in x for p in pb) and not any(p in x for p in pa)).sum())
    return {"ta":ta,"tb":tb,"T":T,"oa":oa,"ob":ob,"nb":nb,"pct":round(nb/T*100) if T else 0,"rows":both_rows}

def cluster(anchor, df):
    pats = THEMES.get(anchor,[anchor.lower()])
    adf = df[df["text_lower"].apply(lambda x: any(p in x for p in pats))]
    n = len(adf)
    if n == 0: return {"anchor":anchor,"n":0,"T":len(df),"clusters":[],"avg":0,"verdict":"standalone","adf":adf}
    co = {}
    for t,tp in THEMES.items():
        if t==anchor: continue
        c = int(adf["text_lower"].apply(lambda x: any(p in x for p in tp)).sum())
        if c: co[t]=c
    avg = round(sum(len([t for t,tp in THEMES.items() if t!=anchor and any(p in row["text_lower"] for p in tp)]) for _,row in adf.iterrows())/n, 1)
    return {"anchor":anchor,"n":n,"T":len(df),"pct":round(n/len(df)*100),"clusters":sorted(co.items(),key=lambda x:-x[1]),"avg":avg,"verdict":"complex" if avg>=4 else "moderate" if avg>=2 else "standalone","adf":adf}

def complexity(anchor, df):
    pats = THEMES.get(anchor,[anchor.lower()])
    adf = df[df["text_lower"].apply(lambda x: any(p in x for p in pats))]
    n = len(adf)
    if n==0: return {"anchor":anchor,"n":0}
    solo,mod,comp=[],[],[]
    co=defaultdict(int)
    for _,row in adf.iterrows():
        others=[t for t,tp in THEMES.items() if t!=anchor and any(p in row["text_lower"] for p in tp)]
        for t in others: co[t]+=1
        rec=dict(row); rec["others"]=others; rec["n_other"]=len(others)
        if len(others)<=1: solo.append(rec)
        elif len(others)<=3: mod.append(rec)
        else: comp.append(rec)
    v="standalone" if len(solo)>len(comp)+len(mod) else "complex" if len(comp)>len(solo) else "mixed"
    return {"anchor":anchor,"n":n,"T":len(df),"solo":solo,"mod":mod,"comp":comp,
            "ns":len(solo),"nm":len(mod),"nc":len(comp),
            "pcts":round(len(solo)/n*100),"pctc":round(len(comp)/n*100),
            "top_co":dict(sorted(co.items(),key=lambda x:-x[1])[:8]),"verdict":v}

# ── INTENT / TOPICS ───────────────────────────────────────────────────────────
def topics(q):
    ql=q.lower()
    return list(dict.fromkeys([t for t,pats in THEMES.items() if any(p in ql for p in pats) or t.lower() in ql]))

def intent(q):
    ql=q.lower()
    tpcs=topics(q)
    if len(tpcs)>=2 and any(w in ql for w in ["hand in hand","together","alongside","linked","co-occur","also mention","both","went together"]): return "co_occur"
    if any(w in ql for w in ["what else","other drivers","other themes","tagged to","cluster","travel with","come with","associated with","what other","drivers tagged"]): return "cluster"
    if any(w in ql for w in ["standalone","straightforward","straight forward","only driver","simple driver","complex","entangled","on its own","by itself","always with","was it just","was it only","was pfs"]): return "complexity"
    rules = {
        "comparison":[r'(community|academic|neuro|medonc|heme|on tl|off tl|co-loc|segment|setting|specialty).*(vs|versus|compare|differ|more|less|between|than)|(vs|versus|compare|differ|difference|different).*(community|academic|setting|specialty|tier|segment|group)'],
        "frequency": [r'how many|how often|what (percentage|proportion|%)|how frequent|number of|count'],
        "driver":    [r'(top|main|key|primary|most common|biggest|major|most important).*(reason|driver|factor|barrier|concern)|(most tied|most associated|which driver|what drives|why do)'],
        "quotes":    [r'(quote|verbatim|exact words|what.*(say|said)|show me.*(quote|example)|give me.*(quote|full response|full quote|full transcript))'],
        "cost":      [r'(cost|afford|insurance|reimburs|copay|prior auth|formulary|coverage|financial|patient assist)'],
        "seizure":   [r'seizure'],
        "endpoint":  [r'(pfs|os|overall survival|progression free).*(prefer|meaningful|important|endpoint)|(pfs.*(vs|or|versus).*os)'],
        "radiation": [r'(delay|defer|avoid).*(radiation|chemo|radiotherapy|rt)'],
        "patient":   [r'(patient|eligib).*(character|profile|who|age|grade|mutation|resection)|ideal candidate|appropriate patient'],
        "barrier":   [r'(barrier|obstacle|challenge|concern|hesitat|reluctan).*(prescrib|adopt|use)|what stops|what prevents'],
    }
    sc=defaultdict(int)
    for i,pats in rules.items():
        for p in pats:
            if re.search(p,ql): sc[i]+=1
    return max(sc,key=sc.get) if sc else "content"

def is_comp(q):
    ql=q.lower()
    sw=["community","academic","neuro","medonc","med onc","hemeonc","heme","on tl","off tl","co-loc","tier","specialty","setting","segment","group"]
    cw=["vs","versus","compare","difference","different","more","less","between","than","how does","what changed","higher","lower"]
    return any(w in ql for w in sw) and any(w in ql for w in cw)

def detect_segs(q, df):
    ql=q.lower()
    for col in ["setting","target","specialty"]:
        vals=df[col].unique().tolist()
        hits=[v for v in vals if v.lower() in ql or v.lower().replace("-","").replace(" ","") in ql.replace("-","").replace(" ","")]
        if len(hits)>=2: return (col,hits[0]),(col,hits[1])
        if len(hits)==1:
            others=[v for v in vals if v!=hits[0]]
            if others: return (col,hits[0]),(col,others[0])
    s=df["setting"].unique().tolist()
    if len(s)>=2: return ("setting",s[0]),("setting",s[1])
    return None,None

# ── ANSWER ────────────────────────────────────────────────────────────────────
def answer(q, adf, fdf):
    T=len(fdf); itn=intent(q); tpcs=topics(q); comp=is_comp(q)
    qpats=[]
    for t in tpcs: qpats+=THEMES.get(t,[])
    if not qpats: qpats=[w for w in q.lower().split() if len(w)>4]
    res={"intent":itn,"topics":tpcs,"is_comp":comp,"n":len(adf),"T":T,"summary":"","chart":{},"rows":[],"comp":None,"co":None,"cl":None,"cx":None,"export":[]}

    if comp:
        sa,sb=detect_segs(q,fdf)
        if sa and sb:
            ca,va=sa; cb,vb=sb
            dfa=fdf[fdf[ca]==va]; dfb=fdf[fdf[cb]==vb]
            na,nb=len(dfa),len(dfb)
            tca,tcb=t_counts(dfa),t_counts(dfb)
            rows=[]
            for t in THEMES:
                a,b=tca.get(t,0),tcb.get(t,0)
                pa=round(a/na*100) if na else 0; pb=round(b/nb*100) if nb else 0
                rows.append({"Theme":t,f"{va}(n={na})":f"{a}({pa}%)",f"{vb}(n={nb})":f"{b}({pb}%)","D":f"+{pa-pb}%" if pa>pb else f"{pa-pb}%","_d":pa-pb,"_pa":pa,"_pb":pb,"_a":a,"_b":b})
            rows=([r for r in rows if r["Theme"] in tpcs] or rows) if tpcs else sorted(rows,key=lambda x:abs(x["_d"]),reverse=True)[:10]
            top=rows[0] if rows else {}
            if top:
                w=va if top["_d"]>0 else vb; l=vb if top["_d"]>0 else va
                res["summary"]=f"**{w}** mentions **{top['Theme']}** more than **{l}** by **{abs(top['_d'])}pp** ({top['_pa']}% vs {top['_pb']}%)."
            focus=qpats or THEMES.get(tpcs[0],[]) if tpcs else []
            res["comp"]={"rows":rows,"va":va,"vb":vb,"na":na,"nb":nb,"dfa":dfa,"dfb":dfb,"focus":focus}
            res["intent"]="comparison"; return res

    if itn=="co_occur" and len(tpcs)>=2:
        co=co_occur(tpcs[0],tpcs[1],fdf)
        res["summary"]=f"**{co['nb']} of {co['T']} respondents ({co['pct']}%)** mentioned both **{tpcs[0]}** and **{tpcs[1]}**."
        res["co"]=co; return res

    if itn=="cluster" and tpcs:
        cl=cluster(tpcs[0],fdf)
        res["summary"]=f"**{cl['n']} of {cl['T']} respondents ({cl.get('pct',0)}%)** mentioned **{tpcs[0]}**. Avg **{cl['avg']} other themes**. Complexity: **{cl['verdict']}**."
        res["cl"]=cl; return res

    if itn=="complexity" and tpcs:
        cx=complexity(tpcs[0],fdf)
        vl={"standalone":"🟢 Standalone","complex":"🔴 Complex / Entangled","mixed":"🟡 Mixed"}.get(cx.get("verdict","mixed"),"")
        res["summary"]=f"**{cx.get('n',0)} respondents** on **{tpcs[0]}**: **{cx.get('ns',0)} standalone** · **{cx.get('nc',0)} complex**. {vl}"
        res["cx"]=cx; return res

    mdf=adf[adf["text_lower"].apply(lambda x: any(p in x for p in qpats))] if qpats else adf
    nm=len(mdf); pct=round(nm/T*100) if T else 0; tstr=" + ".join(tpcs) if tpcs else "this topic"
    res["n"]=nm; res["rows"]=mdf.to_dict("records")
    res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r["target"],"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]

    if itn=="frequency":
        res["summary"]=f"**{nm} of {T} respondents ({pct}%)** mentioned {tstr}."
        res["chart"]={"Associated Themes":dict(sorted({t:v for t,v in t_counts(mdf).items() if v>0}.items(),key=lambda x:-x[1])[:10])}
    elif itn=="driver":
        dc=dict(sorted(d_counts(mdf).items(),key=lambda x:-x[1]))
        top=next(iter(dc.items()),("unknown",0))
        res["summary"]=f"Top driver for **{tstr}**: **{top[0]}** — cited by **{top[1]} respondents**."
        res["chart"]={"Driver Ranking":dc}
    elif itn=="cost":
        cdf=fdf[fdf["text_lower"].apply(lambda x: mtch(x,THEMES["Cost/Insurance"]))]
        cn=len(cdf)
        appr={"Prior Auth/Appeal":int(cdf["text_lower"].apply(lambda x: mtch(x,["prior auth","appeal","peer to peer"])).sum()),"Patient Assistance":int(cdf["text_lower"].apply(lambda x: mtch(x,["patient assistance","patient support","patient program"])).sum()),"Manufacturer Programs":int(cdf["text_lower"].apply(lambda x: mtch(x,["manufacturer","company","free drug"])).sum()),"Copay Support":int(cdf["text_lower"].apply(lambda x: mtch(x,["copay","co-pay"])).sum()),"Office/Pharmacist":int(cdf["text_lower"].apply(lambda x: mtch(x,["my office","pharmacist","staff"])).sum())}
        res["summary"]=f"**{cn} of {T} respondents ({round(cn/T*100) if T else 0}%)** discussed cost/insurance."
        res["chart"]={"Reimbursement Approaches":dict(sorted(appr.items(),key=lambda x:-x[1]))}
        res["rows"]=cdf.to_dict("records"); res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r.get("target",""),"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]
    elif itn=="seizure":
        sdf=fdf[fdf["text_lower"].apply(lambda x: mtch(x,THEMES["Seizures"]))]
        sn=len(sdf); pos=int(sdf["text_lower"].apply(lambda x: any(p in x for p in ["reduc","decreas","lower","control","fewer","less"])).sum()); neg=int(sdf["text_lower"].apply(lambda x: any(p in x for p in ["trigger","worsen","increase","risk","not primary"])).sum())
        res["summary"]=f"**{sn} of {T} respondents** discussed seizures. **{pos} benefit** · **{neg} concern**."
        res["chart"]={"Seizure Sentiment":{"Benefit":pos,"Concern":neg,"Neutral":max(0,sn-pos-neg)}}
        res["rows"]=sdf.to_dict("records"); res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r.get("target",""),"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]
    elif itn=="endpoint":
        pn=int(fdf["text_lower"].apply(lambda x: mtch(x,THEMES["PFS"])).sum()); on=int(fdf["text_lower"].apply(lambda x: mtch(x,THEMES["OS"])).sum()); bn=int(fdf["text_lower"].apply(lambda x: mtch(x,THEMES["PFS"]) and mtch(x,THEMES["OS"])).sum())
        res["summary"]=f"**PFS**: {pn} ({round(pn/T*100) if T else 0}%) · **OS**: {on} ({round(on/T*100) if T else 0}%) · **Both**: {bn}"
        res["chart"]={"Endpoint Split":{"PFS":pn,"OS":on,"Both":bn}}
        res["rows"]=fdf[fdf["text_lower"].apply(lambda x: mtch(x,THEMES["PFS"]))].to_dict("records")
        res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r.get("target",""),"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]
    elif itn=="radiation":
        rdf=fdf[fdf["text_lower"].apply(lambda x: mtch(x,THEMES["Radiation Delay"]))]; rn=len(rdf)
        why={"Cognitive Preservation":int(rdf["text_lower"].apply(lambda x: any(p in x for p in ["cognitive","neurocognit","brain fog","dementia"])).sum()),"Long-term Side Effects":int(rdf["text_lower"].apply(lambda x: "long term" in x or "long-term" in x).sum()),"Fertility":int(rdf["text_lower"].apply(lambda x: mtch(x,THEMES["Fertility"])).sum()),"Quality of Life":int(rdf["text_lower"].apply(lambda x: mtch(x,THEMES["Quality of Life"])).sum()),"Younger Patients":int(rdf["text_lower"].apply(lambda x: any(p in x for p in ["young","younger","less than 40"])).sum())}
        res["summary"]=f"**{rn} of {T} respondents** cited delaying radiation/chemo as a benefit."
        res["chart"]={"Why Delay Radiation":dict(sorted(why.items(),key=lambda x:-x[1]))}
        res["rows"]=rdf.to_dict("records"); res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r.get("target",""),"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]
    elif itn=="patient":
        ch={"IDH1/IDH2 Mutant":int(fdf["text_lower"].apply(lambda x: mtch(x,THEMES["IDH Mutation"])).sum()),"Grade 2 Disease":int(fdf["text_lower"].apply(lambda x: "grade 2" in x or "grade two" in x).sum()),"Residual/Recurring":int(fdf["text_lower"].apply(lambda x: any(p in x for p in ["residual tumor","residual disease","recurring"])).sum()),"Good Performance Status":int(fdf["text_lower"].apply(lambda x: any(p in x for p in ["performance status","ecog","kps"])).sum()),"Younger Patients":int(fdf["text_lower"].apply(lambda x: any(p in x for p in ["young","younger","less than 40"])).sum())}
        res["summary"]=f"Patient characteristics across {T} respondents:"
        res["chart"]={"Ideal Patient Profile":dict(sorted(ch.items(),key=lambda x:-x[1]))}
    elif itn=="barrier":
        bp=["concern","hesitant","not comfortable","challenge","issue","barrier","problem","limited","refused","denied"]
        bdf=mdf[mdf["text_lower"].apply(lambda x: any(p in x for p in bp))] if nm>0 else mdf
        res["summary"]=f"**{len(bdf)} respondents** expressed barriers around {tstr}."
        res["chart"]={"Barrier Drivers":dict(sorted(d_counts(bdf).items(),key=lambda x:-x[1])[:8])}
        res["rows"]=bdf.to_dict("records"); res["export"]=[{"ID":r["id"],"Setting":r["setting"],"Target":r.get("target",""),"Specialty":r["specialty"],"Full Response":r["text"]} for r in res["rows"]]
    else:
        res["summary"]=f"**{nm} of {T} respondents ({pct}%)** discussed {tstr}."
        res["chart"]={"Themes Found":dict(sorted({t:v for t,v in t_counts(mdf).items() if v>0}.items(),key=lambda x:-x[1])[:10])}
    return res

# ── QUESTION BANK ─────────────────────────────────────────────────────────────
QB = {
    "📊 Frequency": ["How many HCPs mentioned PFS?","How many discussed cost or insurance?","How often was quality of life mentioned?","How many cited the Indigo trial?","What percentage mentioned seizures?","How many brought up radiation delay?","How many discussed oral administration?","How many mentioned NCCN guidelines?","How many raised fertility concerns?","How often was performance status cited?"],
    "⚖️ Comparison": ["Community vs academic on PFS — what's the difference?","Do community doctors mention cost more than academic?","Academic vs community on radiation delay","Did academic HCPs cite Indigo trial more than community?","Community vs academic on seizures","On TL vs Off TL — what's different?","What do Neuro-Onc vs MedOnc say about PFS?","HemeOnc vs MedOnc on cost barriers","Community vs academic on quality of life","Community vs academic on patient assistance"],
    "🎯 Drivers": ["What is the top driver for prescribing?","What driver is most tied to PFS?","What are the main barriers to prescribing?","Why do doctors delay radiation?","What motivates HCPs to choose oral therapy?","What are the key clinical rationale drivers?","What are the main cost-related barriers?","What stops community doctors from prescribing?","What is the primary driver for insurance navigation?","What are the main reasons for non-prescribing?"],
    "🔗 Co-occurrence": ["Did doctors talk about PFS and performance status hand in hand?","Did PFS and quality of life go together?","Did cost and patient assistance come up together?","When seizures were mentioned, was quality of life also discussed?","Did oral administration and convenience go hand in hand?","Did Indigo trial and PFS get mentioned together?","When NCCN was mentioned, was insurance also discussed?","Did radiation delay and cognition come up together?","Did PFS and OS get mentioned alongside each other?","Did safety and tolerability go hand in hand?"],
    "🧩 Theme Clustering": ["What other drivers were tagged to PFS?","What themes cluster around cost?","What travels with quality of life discussions?","What other topics come up with seizure mentions?","What themes cluster around the Indigo trial?","What goes with oral administration mentions?","What other factors travel with radiation delay?","What themes come up alongside NCCN guidelines?","What clusters around efficacy discussions?","What other themes appear with OS mentions?"],
    "🎯 Driver Complexity": ["Was PFS a straightforward driver or always complex?","Was oral administration a standalone driver?","Was cost a simple or complex barrier?","Was quality of life mentioned standalone or bundled?","Was efficacy a simple or entangled driver?","Was seizure control a standalone concern?","Was radiation delay a straightforward benefit?","Was the Indigo trial cited alone or bundled?","Was NCCN a standalone factor or always with others?","Was tolerability a simple or complex driver?"],
    "💬 Full Responses": ["Show me full responses about cost and insurance","Give me full quotes about PFS","Show full responses from community HCPs about barriers","Show full transcripts about quality of life","Show full responses mentioning seizures","Give me full quotes about oral administration","Show full responses about radiation delay","Give me full quotes about patient assistance programs","Show full responses about the Indigo trial","Show full quotes about overall survival"],
    "💰 Cost & Access": ["How do HCPs navigate insurance denials?","What patient assistance programs are mentioned?","How do doctors handle prior authorization?","What approaches do HCPs use for reimbursement?","How do community HCPs handle cost barriers?","What is the role of the rep in cost navigation?"],
    "🏥 Patient Profile": ["What patient profile is ideal for prescribing?","Which patients are most appropriate candidates?","What tumor characteristics matter most?","Do younger patients get prescribed more?","What performance status is needed?","What are the key eligibility factors?"],
    "📋 Clinical Endpoints": ["Do HCPs prefer PFS or OS?","What clinical endpoint matters most?","How many mentioned PFS vs OS?","Is OS or PFS more discussed in academic settings?"],
}

# ── APP ───────────────────────────────────────────────────────────────────────
st.markdown("""<div style="margin-bottom:20px">
    <div style="font-family:'IBM Plex Mono',monospace;font-size:10px;color:#3b6ef7;letter-spacing:2px;margin-bottom:6px">HCP QUAL INSIGHT ENGINE · UPLOAD YOUR DATA TO BEGIN</div>
    <h1 style="font-size:30px;margin:0;color:#e2ecf8;font-weight:600">HCP Insight Engine</h1>
</div>""", unsafe_allow_html=True)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sec-lbl">📂 UPLOAD DATA</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#4a6080;margin-bottom:10px;line-height:1.6">Upload your qual Excel.<br><span style="color:#8a9ab5">Required:</span> verbatim/transcript column<br><span style="color:#8a9ab5">Optional:</span> Setting · Specialty · Target</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload Excel", type=["xlsx","xls"], label_visibility="collapsed")
    st.markdown("<hr>", unsafe_allow_html=True)

    if not uploaded:
        st.markdown('<div style="text-align:center;padding:20px;color:#4a6080;font-size:12px">Upload an Excel file above to begin. All analysis uses your data only.</div>', unsafe_allow_html=True)
        st.stop()

    full_df, err = load_excel(uploaded)
    if err or full_df is None:
        st.error(f"⚠️ {err}")
        st.markdown('<div style="font-size:11px;color:#4a6080;margin-top:8px">Tips:<br>· Needs verbatim text column (>100 chars)<br>· Metadata cols should have few unique values<br>· Re-save as .xlsx if issues persist</div>', unsafe_allow_html=True)
        st.stop()

    TOTAL = len(full_df)
    st.markdown(f'<div style="background:#0a1f14;border:1px solid #10b98133;border-radius:10px;padding:12px 16px;margin-bottom:14px"><div style="font-size:11px;font-weight:600;color:#34d399;margin-bottom:3px">✅ Data loaded</div><div style="font-size:11px;color:#4a6080">{TOTAL} respondents · {uploaded.name}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-lbl">SEGMENT FILTERS</div>', unsafe_allow_html=True)
    settings    = ["All"] + sorted(full_df["setting"].dropna().unique().tolist())
    specialties = ["All"] + sorted(full_df["specialty"].dropna().unique().tolist())
    targets     = ["All"] + sorted(full_df["target"].dropna().unique().tolist())
    fs  = st.selectbox("Practice Setting", settings)
    fsp = st.selectbox("Specialty",        specialties)
    ft  = st.selectbox("Target Type",      targets)
    fdf = full_df.copy()
    if fs  != "All": fdf = fdf[fdf["setting"]  ==fs]
    if fsp != "All": fdf = fdf[fdf["specialty"]==fsp]
    if ft  != "All": fdf = fdf[fdf["target"]   ==ft]
    fn=len(fdf); sc=fdf["setting"].value_counts().to_dict()
    sh=" · ".join(f'<span style="color:#8a9ab5">{k}:{v}</span>' for k,v in sc.items())
    st.markdown(f'<div class="card" style="text-align:center;margin-top:6px"><div class="stat-num">{fn}</div><div class="stat-lbl">in view</div><div style="font-size:11px;margin-top:6px">{sh}</div></div>', unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.markdown('<div class="sec-lbl">QUESTION BROWSER</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#4a6080;margin-bottom:8px">Click any question to run instantly</div>', unsafe_allow_html=True)
    for cat, qs in QB.items():
        with st.expander(cat, expanded=False):
            for q in qs:
                if st.button(q, key=f"qb_{q[:28]}"):
                    st.session_state["q"] = q
                    st.rerun()

# ── MAIN ──────────────────────────────────────────────────────────────────────
if "q" not in st.session_state: st.session_state["q"] = ""

# Search label + colour legend row
st.markdown("""
<div style="margin-bottom:8px">
    <div style="font-size:12px;color:#8a9ab5;margin-bottom:6px;font-weight:500">
        🔍 <b style="color:#e2ecf8">Ask a question</b>
        <span style="color:#4a6080;font-weight:400"> — type freely below, or pick from the sidebar browser</span>
    </div>
</div>""", unsafe_allow_html=True)

query = st.text_input(
    label="Ask a question about your data",
    label_visibility="collapsed",
    placeholder='e.g. "How many HCPs mentioned PFS?" · "Community vs academic on cost" · "Was PFS a standalone driver?"',
    value=st.session_state.get("q",""),
    key="main"
)

# Quick-type suggestion chips (clickable, distinct from sidebar browser)
st.markdown('<div style="font-size:10px;color:#4a6080;margin:8px 0 4px;letter-spacing:1px;text-transform:uppercase">Quick questions — click to run:</div>', unsafe_allow_html=True)
chip_cols = st.columns(4)
CHIPS = [
    "How many HCPs mentioned PFS?",
    "Community vs academic on PFS",
    "What other drivers were tagged to PFS?",
    "Was PFS a standalone driver?",
    "Did PFS and quality of life go together?",
    "How many discussed cost or insurance?",
    "Show full responses about cost and insurance",
    "What are the main barriers to prescribing?",
]
for i, chip in enumerate(CHIPS):
    if chip_cols[i % 4].button(chip, key=f"chip_{i}"):
        st.session_state["q"] = chip
        st.rerun()

# Colour legend
st.markdown("""<div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 4px;align-items:center">
    <span style="font-size:10px;color:#4a6080;margin-right:2px">Highlight key:</span>
    <span class="hl-ins" style="font-style:normal">insurance/cost</span>
    <span class="hl-pfs" style="font-style:normal">PFS</span>
    <span class="hl-os" style="font-style:normal">OS</span>
    <span class="hl-saf" style="font-style:normal">safety</span>
    <span class="hl-sz" style="font-style:normal">seizures</span>
    <span class="hl-qol" style="font-style:normal">quality of life</span>
    <span class="hl-oral" style="font-style:normal">oral</span>
    <span class="hl-trial" style="font-style:normal">trial data</span>
    <span class="hl-nccn" style="font-style:normal">NCCN/guidelines</span>
</div>""", unsafe_allow_html=True)

if query and query.strip():
    with st.spinner(""):
        r = answer(query, fdf, full_df)

    st.markdown("<hr>", unsafe_allow_html=True)
    bh = f'<span class="ibadge">{r["intent"]}</span>'
    for t in r["topics"]: bh += f'<span class="tbadge">{t}</span>'
    if fs != "All": bh += f'<span class="ibadge" style="color:#fbbf24;border-color:rgba(251,191,36,.3);background:rgba(251,191,36,.06)">{fs}</span>'
    st.markdown(bh+"<br><br>", unsafe_allow_html=True)

    st.markdown(f"""<div class="card">
        <div class="sec-lbl">INSIGHT SUMMARY</div>
        <div style="font-size:17px;color:#e2ecf8;line-height:1.75">{r["summary"]}</div>
        <div style="font-size:11px;color:#4a6080;margin-top:8px">All counts and quotes drawn directly from uploaded data ({TOTAL} respondents). No inference or generation.</div>
    </div>""", unsafe_allow_html=True)

    T=r["T"]

    # ── COMPARISON ────────────────────────────────────────────────────────
    if r["is_comp"] and r["comp"]:
        cp=r["comp"]; va,vb=cp["va"],cp["vb"]; na,nb=cp["na"],cp["nb"]
        st.markdown(f'<div style="display:flex;gap:12px;margin-bottom:16px;align-items:center"><span class="seg-a">🟡 {va} (n={na})</span><span style="color:#4a6080">vs</span><span class="seg-b">🔵 {vb} (n={nb})</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="card"><div class="sec-lbl">THEME COMPARISON</div>', unsafe_allow_html=True)
        for row in cp["rows"]:
            t=row["Theme"]; pa,pb,d=row["_pa"],row["_pb"],row["_d"]; color=TC.get(t,"#4a6080")
            dh=f'<span class="diff-pos">▲{d}pp</span>' if d>0 else (f'<span class="diff-neg">▼{abs(d)}pp</span>' if d<0 else '<span style="color:#4a6080">═</span>')
            st.markdown(f"""<div style="margin-bottom:12px">
                <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px"><span style="color:#e2ecf8;font-weight:500">{t}</span><span>{dh}</span></div>
                <div style="display:flex;gap:6px;align-items:center;margin-bottom:2px">
                    <span style="font-size:10px;color:#fbbf24;min-width:65px">{va}</span><div class="bar-trk" style="flex:1"><div class="bar-fill" style="width:{pa}%;background:#f59e0b"></div></div><span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#fbbf24;min-width:38px;text-align:right">{pa}%</span>
                </div>
                <div style="display:flex;gap:6px;align-items:center">
                    <span style="font-size:10px;color:#93c5fd;min-width:65px">{vb}</span><div class="bar-trk" style="flex:1"><div class="bar-fill" style="width:{pb}%;background:#3b6ef7"></div></div><span style="font-family:'IBM Plex Mono',monospace;font-size:11px;color:#93c5fd;min-width:38px;text-align:right">{pb}%</span>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        c1,c2=st.columns(2)
        for col,df_s,val,color in [(c1,cp["dfa"],va,"#fbbf24"),(c2,cp["dfb"],vb,"#93c5fd")]:
            with col:
                st.markdown(f'<div class="sec-lbl" style="color:{color}">{"🟡" if color=="#fbbf24" else "🔵"} {val} FULL RESPONSES</div>', unsafe_allow_html=True)
                f=cp.get("focus",[])
                filt=df_s[df_s["text_lower"].apply(lambda x: any(p in x for p in f) if f else True)]
                for _,row in filt.head(4).iterrows(): quote_card(row)
        exp=[{"Theme":row["Theme"],f"{va}(n={na})":row.get(f"{va}(n={na})",""),f"{vb}(n={nb})":row.get(f"{vb}(n={nb})",""),"Diff":row["D"]} for row in cp["rows"]]
        st.download_button("⬇ Download comparison CSV", pd.DataFrame(exp).to_csv(index=False).encode(),"comparison.csv","text/csv")

    # ── CO-OCCURRENCE ─────────────────────────────────────────────────────
    elif r["intent"]=="co_occur" and r.get("co"):
        co=r["co"]; ta,tb=co["ta"],co["tb"]; ca=TC.get(ta,"#3b6ef7"); cb=TC.get(tb,"#f59e0b")
        c1,c2,c3=st.columns(3)
        c1.markdown(f'<div class="card" style="text-align:center;border-left:3px solid {ca}"><div class="stat-num" style="color:{ca}">{co["oa"]}</div><div class="stat-lbl">{ta} only</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card" style="text-align:center;border:2px solid #10b981"><div class="stat-num" style="color:#10b981">{co["nb"]}</div><div class="stat-lbl">BOTH ({co["pct"]}%)</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card" style="text-align:center;border-left:3px solid {cb}"><div class="stat-num" style="color:{cb}">{co["ob"]}</div><div class="stat-lbl">{tb} only</div></div>', unsafe_allow_html=True)
        if co["rows"]:
            st.markdown(f'<div class="card"><div class="sec-lbl" style="color:#10b981">RESPONDENTS MENTIONING BOTH — FULL RESPONSES WITH ALL THEMES HIGHLIGHTED</div><div style="font-size:11px;color:#4a6080;margin-bottom:12px">Both <b style="color:{ca}">{ta}</b> and <b style="color:{cb}">{tb}</b> highlighted. Full text, no truncation.</div>', unsafe_allow_html=True)
            for row in co["rows"][:5]: quote_card(row, [ta,tb])
            st.markdown('</div>', unsafe_allow_html=True)
            rows=[{"ID":rec["id"],"Setting":rec["setting"],"Target":rec.get("target",""),"Specialty":rec["specialty"],"Full Response":rec["text"]} for rec in co["rows"]]
            st.download_button("⬇ Download co-occurrence CSV", pd.DataFrame(rows).to_csv(index=False).encode(),"co_occurrence.csv","text/csv")

    # ── CLUSTER ───────────────────────────────────────────────────────────
    elif r["intent"]=="cluster" and r.get("cl"):
        cl=r["cl"]; vc={"complex":"#ef4444","moderate":"#f59e0b","standalone":"#10b981"}.get(cl["verdict"],"#4a6080")
        c1,c2,c3=st.columns(3)
        c1.markdown(f'<div class="card" style="text-align:center"><div class="stat-num">{cl["n"]}</div><div class="stat-lbl">mentioned {cl["anchor"]}</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card" style="text-align:center"><div class="stat-num">{cl["avg"]}</div><div class="stat-lbl">avg other themes</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card" style="text-align:center"><div class="stat-num" style="color:{vc};font-size:22px">{cl["verdict"].upper()}</div><div class="stat-lbl">driver type</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="card"><div class="sec-lbl">THEMES THAT TRAVEL WITH {cl["anchor"].upper()} — FROM UPLOADED DATA ONLY</div>', unsafe_allow_html=True)
        for t,cnt in cl["clusters"]:
            color=TC.get(t,"#4a6080"); pct=round(cnt/cl["n"]*100) if cl["n"] else 0
            st.markdown(f'<div style="margin-bottom:6px"><div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:3px"><span style="color:#e2ecf8">{t}</span><span style="font-family:\'IBM Plex Mono\',monospace;color:{color}">{cnt} ({pct}% of group)</span></div><div class="bar-trk"><div class="bar-fill" style="width:{pct}%;background:{color}"></div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="sec-lbl" style="margin-top:14px">FULL RESPONSES FROM {cl["anchor"].upper()} GROUP</div>', unsafe_allow_html=True)
        for _,row in cl["adf"].head(5).iterrows(): quote_card(row,[cl["anchor"]])
        exp=[{"Theme":t,"Count":cnt,"% of group":f"{round(cnt/cl['n']*100) if cl['n'] else 0}%"} for t,cnt in cl["clusters"]]
        st.download_button("⬇ Download cluster CSV", pd.DataFrame(exp).to_csv(index=False).encode(),"cluster.csv","text/csv")

    # ── COMPLEXITY ────────────────────────────────────────────────────────
    elif r["intent"]=="complexity" and r.get("cx"):
        cx=r["cx"]; vc_map={"standalone":("#10b981","🟢 STANDALONE","Mentioned independently, not bundled with many other themes."),"complex":("#ef4444","🔴 COMPLEX / ENTANGLED","Almost always appeared alongside 4+ other themes."),"mixed":("#f59e0b","🟡 MIXED","Sometimes standalone, sometimes part of a broader cluster.")}
        vc,vt,vd=vc_map.get(cx.get("verdict","mixed"),("#4a6080","MIXED",""))
        st.markdown(f'<div class="card" style="border-left:4px solid {vc}"><div style="font-size:13px;font-weight:700;color:{vc};margin-bottom:6px">{vt}</div><div style="font-size:13px;color:#c8d4e8;line-height:1.6">{vd}</div><div style="font-size:11px;color:#4a6080;margin-top:8px">Based on {cx["n"]} respondents — from uploaded data only.</div></div>', unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        c1.markdown(f'<div class="card" style="text-align:center;border-left:3px solid #10b981"><div class="stat-num" style="color:#10b981">{cx["ns"]}</div><div class="stat-lbl">Standalone (0–1 others)</div></div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card" style="text-align:center;border-left:3px solid #f59e0b"><div class="stat-num" style="color:#f59e0b">{cx["nm"]}</div><div class="stat-lbl">Moderate (2–3 others)</div></div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="card" style="text-align:center;border-left:3px solid #ef4444"><div class="stat-num" style="color:#ef4444">{cx["nc"]}</div><div class="stat-lbl">Complex (4+ others)</div></div>', unsafe_allow_html=True)
        if cx.get("top_co"):
            st.markdown(f'<div class="card"><div class="sec-lbl">THEMES MOST MENTIONED ALONGSIDE {cx["anchor"].upper()}</div>', unsafe_allow_html=True)
            for t,cnt in cx["top_co"].items(): bar_html(t,cnt,cx["n"],TC.get(t,"#4a6080"))
            st.markdown('</div>', unsafe_allow_html=True)
        if cx["solo"]:
            st.markdown('<div class="sec-lbl" style="color:#10b981;margin-top:14px">🟢 STANDALONE — FULL RESPONSES</div>', unsafe_allow_html=True)
            for rec in cx["solo"][:3]: quote_card(rec,[cx["anchor"]])
        if cx["comp"]:
            st.markdown('<div class="sec-lbl" style="color:#ef4444;margin-top:14px">🔴 COMPLEX MENTIONS — FULL RESPONSES</div>', unsafe_allow_html=True)
            for rec in cx["comp"][:3]: quote_card(rec,[cx["anchor"]]+rec.get("others",[])[:4])
        rows=[]
        for cat,recs in [("standalone",cx["solo"]),("moderate",cx["mod"]),("complex",cx["comp"])]:
            for rec in recs: rows.append({"ID":rec["id"],"Setting":rec["setting"],"Specialty":rec["specialty"],"Type":cat,"N other themes":rec["n_other"],"Other themes":", ".join(rec.get("others",[])[:5]),"Full Response":rec["text"]})
        st.download_button("⬇ Download complexity CSV", pd.DataFrame(rows).to_csv(index=False).encode(),"complexity.csv","text/csv")

    # ── STANDARD ─────────────────────────────────────────────────────────
    else:
        l,ri=st.columns([1,1])
        with l:
            cc1,cc2=st.columns(2)
            cc1.markdown(f'<div class="card" style="text-align:center"><div class="stat-num">{r["n"]}</div><div class="stat-lbl">matched</div></div>', unsafe_allow_html=True)
            cc2.markdown(f'<div class="card" style="text-align:center"><div class="stat-num">{round(r["n"]/T*100) if T else 0}%</div><div class="stat-lbl">of total</div></div>', unsafe_allow_html=True)
            for title,data in r["chart"].items():
                if data:
                    st.markdown(f'<div class="card"><div class="sec-lbl">{title}</div>', unsafe_allow_html=True)
                    for lbl,cnt in list(data.items())[:12]: bar_html(lbl,int(cnt),T,TC.get(lbl,"#3b6ef7"))
                    st.markdown('</div>', unsafe_allow_html=True)
        with ri:
            n_rows=len(r["rows"])
            st.markdown(f'<div class="sec-lbl">FULL RESPONSES — ALL THEMES HIGHLIGHTED</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:11px;color:#4a6080;margin-bottom:12px">Showing {min(n_rows,6)} of {n_rows} matched respondents. Full text shown — keywords colour-coded above.</div>', unsafe_allow_html=True)
            if r["rows"]:
                for rec in r["rows"][:6]: quote_card(rec, r["topics"] if r["topics"] else None)
            else:
                st.markdown('<div style="color:#4a6080;font-size:13px">No matches. Try broader keywords.</div>', unsafe_allow_html=True)
        if r.get("export"):
            st.markdown("<hr>", unsafe_allow_html=True)
            dfe=pd.DataFrame(r["export"])
            preview_cols=[c for c in ["ID","Setting","Specialty","Target"] if c in dfe.columns]
            st.dataframe(dfe[preview_cols].head(20) if preview_cols else dfe.head(20),hide_index=True,use_container_width=True)
            st.download_button("⬇ Download full responses CSV", dfe.to_csv(index=False).encode(),f"responses_{query[:20].replace(' ','_')}.csv","text/csv")

else:
    # Landing
    st.markdown('<div style="text-align:center;margin-top:60px"><div style="font-size:48px;margin-bottom:16px">📂</div><div style="font-size:16px;color:#4a6080">Upload your Excel file in the sidebar to begin</div><div style="font-size:13px;color:#2a3a55;margin-top:8px">Then click any question from the sidebar browser or type your own</div></div>', unsafe_allow_html=True)
