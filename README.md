# HCP Insight Engine

Zero-cost, no-API qual research tool. Upload any Excel with verbatim transcripts and ask natural language questions — with every answer traceable to source.

---

## Deploy to Streamlit Cloud (free, ~5 min)

1. Create a GitHub repo and upload **`app.py`** and **`requirements.txt`**
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo → `app.py` → Deploy

---

## How to use

**No upload needed** — Voranigo default data (60 HCPs) loads automatically.

**To use your own data:** Sidebar → Upload Excel. Needs:
- One column with verbatim / transcript text (long strings)
- Optional: columns named like `Practice Setting`, `Specialty`, `Target Type`

The app auto-detects your columns by name and content.

---

## What it can answer

| Type | Example |
|---|---|
| Frequency | "How many community HCPs mentioned PFS?" |
| Segment comparison | "Community vs academic on PFS — what's the difference?" |
| Driver | "What driver is most tied to PFS?" |
| Quotes | "Show me quotes about radiation delay" |
| Barriers | "What stops doctors from prescribing?" |
| Cost/Access | "How do HCPs navigate insurance denials?" |
| Patient profile | "What patient characteristics are cited most?" |
| Endpoints | "Do HCPs prefer PFS or OS?" |
| Specialty split | "Neuro-Onc vs MedOnc on seizures" |
| Target tier | "On TL vs Off TL — what's different?" |

---

## What makes this different from ChatGPT

| | This tool | ChatGPT |
|---|---|---|
| Uses only your data | ✅ | ❌ |
| Traceable to respondent ID | ✅ | ❌ |
| Verbatim quote per answer | ✅ | ❌ |
| Segment comparison | ✅ | ❌ |
| Downloadable evidence CSV | ✅ | ❌ |
| Zero API cost | ✅ | ❌ |
| No hallucination | ✅ | ❌ |

---

No API keys. No backend. Runs entirely in the browser.
