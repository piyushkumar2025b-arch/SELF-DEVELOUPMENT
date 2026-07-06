"""
Global CSS styles injected into Streamlit
Dark theme with neon accents — cyber/terminal aesthetic
"""

CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Root Tokens ── */
:root {
  --bg-0: #0a0e1a;
  --bg-1: #0f1629;
  --bg-2: #151d35;
  --bg-3: #1c2444;
  --border: #1e2d52;
  --accent-p: #6366f1;   /* indigo */
  --accent-b: #3b82f6;   /* blue */
  --accent-g: #10b981;   /* green */
  --accent-y: #f59e0b;   /* amber */
  --accent-r: #ef4444;   /* red */
  --accent-pk: #ec4899;  /* pink */
  --text-1: #f1f5f9;
  --text-2: #94a3b8;
  --text-3: #475569;
  --mono: 'JetBrains Mono', monospace;
  --sans: 'Inter', sans-serif;
  --radius: 12px;
  --glow-p: 0 0 20px rgba(99,102,241,0.35);
  --glow-b: 0 0 20px rgba(59,130,246,0.35);
  --glow-g: 0 0 20px rgba(16,185,129,0.35);
}

/* ── Base Reset ── */
html, body, [class*="css"] {
  font-family: var(--sans) !important;
  background-color: var(--bg-0) !important;
  color: var(--text-1) !important;
}

/* ── Streamlit chrome ── */
.stApp { background: var(--bg-0) !important; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }
header[data-testid="stHeader"] { background: rgba(10,14,26,0.95) !important; backdrop-filter: blur(12px); border-bottom: 1px solid var(--border); }
.stSidebar { background: var(--bg-1) !important; border-right: 1px solid var(--border); }
.stSidebar .stMarkdown, .stSidebar p { color: var(--text-2) !important; }

/* ── Typography ── */
h1, h2, h3 { font-family: var(--sans) !important; font-weight: 800 !important; color: var(--text-1) !important; }
h1 { font-size: 2.2rem !important; }
h2 { font-size: 1.6rem !important; }
h3 { font-size: 1.2rem !important; }
code, pre, .stCode { font-family: var(--mono) !important; }

/* ── Cards ── */
.card {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}
.card:hover { border-color: var(--accent-p); box-shadow: var(--glow-p); transform: translateY(-1px); }
.card::before { content:''; position:absolute; top:0; left:0; right:0; height:2px; background: linear-gradient(90deg, var(--accent-p), var(--accent-b)); }

.card-blue::before { background: linear-gradient(90deg, var(--accent-b), var(--accent-g)); }
.card-green::before { background: linear-gradient(90deg, var(--accent-g), var(--accent-y)); }
.card-red::before { background: linear-gradient(90deg, var(--accent-r), var(--accent-pk)); }
.card-gold::before { background: linear-gradient(90deg, var(--accent-y), var(--accent-pk)); }

/* ── Glow Heading ── */
.glow-text {
  background: linear-gradient(135deg, var(--accent-p) 0%, var(--accent-b) 50%, var(--accent-g) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ── Difficulty badges ── */
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 100px;
  font-size: 0.72rem;
  font-weight: 600;
  font-family: var(--mono) !important;
  letter-spacing: 0.03em;
}
.badge-easy   { background: rgba(16,185,129,0.15); color: #10b981; border: 1px solid rgba(16,185,129,0.3); }
.badge-medium { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); }
.badge-hard   { background: rgba(239,68,68,0.15);  color: #ef4444; border: 1px solid rgba(239,68,68,0.3); }

/* ── Company tags ── */
.company-tag {
  display: inline-block;
  background: rgba(99,102,241,0.15);
  color: #818cf8;
  border: 1px solid rgba(99,102,241,0.3);
  padding: 1px 8px;
  border-radius: 6px;
  font-size: 0.7rem;
  font-weight: 500;
  margin: 2px;
}

/* ── Achievement Badges ── */
.achievement-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, var(--bg-3), var(--bg-2));
  border: 1px solid var(--border);
  border-radius: 100px;
  padding: 6px 14px;
  font-size: 0.8rem;
  font-weight: 600;
  margin: 4px;
  color: var(--text-1);
  transition: all 0.2s;
}
.achievement-badge:hover { border-color: var(--accent-y); box-shadow: 0 0 12px rgba(245,158,11,0.25); }

/* ── Pins ── */
.pin {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(99,102,241,0.12);
  border: 1px solid rgba(99,102,241,0.25);
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.78rem;
  font-weight: 600;
  margin: 4px;
  color: #a5b4fc;
  cursor: pointer;
  transition: all 0.2s;
}
.pin:hover { background: rgba(99,102,241,0.25); transform: scale(1.03); }
.pin-green { background: rgba(16,185,129,0.12); border-color: rgba(16,185,129,0.25); color: #6ee7b7; }
.pin-gold  { background: rgba(245,158,11,0.12); border-color: rgba(245,158,11,0.25); color: #fcd34d; }
.pin-red   { background: rgba(239,68,68,0.12);  border-color: rgba(239,68,68,0.25);  color: #fca5a5; }

/* ── Question Dropdown ── */
.q-item {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem 1.25rem;
  margin: 0.5rem 0;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}
.q-item:hover, .q-item.selected {
  border-color: var(--accent-p);
  background: var(--bg-3);
  box-shadow: var(--glow-p);
}
.q-item.selected { border-left: 3px solid var(--accent-p); }

/* ── Quote Box ── */
.quote-box {
  background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(59,130,246,0.08));
  border: 1px solid rgba(99,102,241,0.2);
  border-left: 4px solid var(--accent-p);
  border-radius: var(--radius);
  padding: 1.25rem 1.5rem;
  margin: 1rem 0;
}
.quote-text { font-style: italic; font-size: 1.15rem; color: var(--text-1); line-height: 1.6; }
.quote-author { font-size: 0.85rem; color: var(--accent-p); font-weight: 600; margin-top: 0.5rem; }

/* ── Stat Chip ── */
.stat-chip {
  background: var(--bg-3);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  text-align: center;
}
.stat-chip .num { font-size: 1.8rem; font-weight: 800; font-family: var(--mono) !important; }
.stat-chip .label { font-size: 0.72rem; color: var(--text-2); font-weight: 500; text-transform: uppercase; letter-spacing: 0.05em; margin-top: 2px; }

/* ── Buttons ── */
.stButton > button {
  background: linear-gradient(135deg, var(--accent-p), var(--accent-b)) !important;
  color: white !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  font-family: var(--sans) !important;
  transition: all 0.2s !important;
  box-shadow: 0 2px 10px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 20px rgba(99,102,241,0.4) !important; }

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-1) !important;
  font-family: var(--sans) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
  border-color: var(--accent-p) !important;
  box-shadow: 0 0 0 2px rgba(99,102,241,0.2) !important;
}

/* ── Progress bar ── */
.stProgress > div > div { background: linear-gradient(90deg, var(--accent-p), var(--accent-b)) !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { background: var(--bg-2) !important; border-radius: 10px !important; padding: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: var(--text-2) !important; border-radius: 8px !important; font-weight: 500 !important; }
.stTabs [aria-selected="true"] { background: var(--accent-p) !important; color: white !important; }

/* ── Metrics ── */
[data-testid="metric-container"] {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 10px !important;
  padding: 1rem !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
  background: var(--bg-2) !important;
  border: 1px solid var(--border) !important;
  border-radius: 8px !important;
  color: var(--text-1) !important;
  font-weight: 600 !important;
}
.streamlit-expanderContent {
  background: var(--bg-1) !important;
  border: 1px solid var(--border) !important;
  border-top: none !important;
  border-radius: 0 0 8px 8px !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Sidebar Nav ── */
.nav-link {
  display: block;
  padding: 0.6rem 1rem;
  border-radius: 8px;
  color: var(--text-2);
  font-weight: 500;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.15s;
  margin: 2px 0;
  text-decoration: none;
}
.nav-link:hover, .nav-link.active {
  background: rgba(99,102,241,0.15);
  color: var(--text-1);
}
.nav-link.active { border-left: 3px solid var(--accent-p); }

/* ── Heatmap ── */
.heatmap-cell {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: 2px;
  margin: 1px;
}

/* ── Link button ── */
.link-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 4px 12px;
  background: rgba(59,130,246,0.12);
  border: 1px solid rgba(59,130,246,0.25);
  border-radius: 6px;
  color: #60a5fa;
  font-size: 0.8rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.15s;
}
.link-btn:hover { background: rgba(59,130,246,0.25); text-decoration: none; }

/* ── Fitness ── */
.workout-card {
  background: var(--bg-2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 1rem;
  margin: 6px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* ── Toast-like notification ── */
.notification {
  background: linear-gradient(135deg, rgba(16,185,129,0.15), rgba(59,130,246,0.15));
  border: 1px solid rgba(16,185,129,0.3);
  border-radius: 10px;
  padding: 0.75rem 1rem;
  color: #6ee7b7;
  font-size: 0.875rem;
  font-weight: 500;
  margin: 0.5rem 0;
}

/* ── scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-p); }

/* ── Hide streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""

def inject_css():
    import streamlit as st
    st.markdown(CSS, unsafe_allow_html=True)

def card(content: str, variant: str = "") -> str:
    cls = f"card card-{variant}" if variant else "card"
    return f'<div class="{cls}">{content}</div>'

def badge(text: str, difficulty: str) -> str:
    return f'<span class="badge badge-{difficulty.lower()}">{text}</span>'

def stat_chip(num, label: str, color: str = "#6366f1") -> str:
    return f'''
<div class="stat-chip">
  <div class="num" style="color:{color}">{num}</div>
  <div class="label">{label}</div>
</div>'''

def quote_box(quote: str, author: str) -> str:
    return f'''
<div class="quote-box">
  <div class="quote-text">"{quote}"</div>
  <div class="quote-author">— {author}</div>
</div>'''

def pin(text: str, variant: str = "") -> str:
    cls = f"pin pin-{variant}" if variant else "pin"
    return f'<span class="{cls}">{text}</span>'

def achievement(icon: str, name: str) -> str:
    return f'<span class="achievement-badge">{icon} {name}</span>'
