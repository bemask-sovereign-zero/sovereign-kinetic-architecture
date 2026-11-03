import streamlit as st
import streamlit.components.v1 as components
import json
import csv
import io
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="S.K.A. // BOSCHETTO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- OROLOGIO DI SISTEMA (FUSO ORARIO ITALIA) E MOTORE REMIND AUTOMATICO ---
def get_italy_now():
    return datetime.now(timezone(timedelta(hours=1)))

def get_current_window_info(now_dt):
    h = now_dt.hour
    m = now_dt.minute
    cur_mins = h * 60 + m
    if 6 <= h < 14:
        overdue = cur_mins >= (9 * 60 + 30)
        return "MATTINA (06:00-14:00)", "09:30", overdue
    elif 14 <= h < 19:
        overdue = cur_mins >= (16 * 60)
        return "POMERIGGIO (14:00-19:00)", "16:00", overdue
    else:
        overdue = (h >= 21) or (h < 6)
        return "SERA (19:00-03:00)", "21:00", overdue

# --- CSS ARCHITETTONICO + TOUCH PANEL CON RETINO LED E PALLINI BLU ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

header[data-testid="stHeader"] { background: transparent !important; }

button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] button {
    background-color: #0284c7 !important;
    color: #ffffff !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 8px !important;
}

.stApp {
    background-color: #070b12 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    -webkit-tap-highlight-color: transparent;
}

.block-container {
    padding-top: 1.6rem !important;
    padding-bottom: 2rem !important;
    max-width: 1420px !important;
}

.top-bar {
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}
.brand-title {
    font-size: 1.22rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #f8fafc;
    text-transform: uppercase;
}
.brand-title span {
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}
.brand-clock {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    color: #38bdf8;
    background: #0d1524;
    border: 1px solid #1e293b;
    padding: 5px 12px;
    border-radius: 4px;
}

.kpi-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.kpi-box {
    background: #0d1524;
    border: 1px solid #1e293b;
    border-left: 3px solid #38bdf8;
    border-radius: 4px;
    padding: 9px 12px;
}
.kpi-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #94a3b8;
    text-transform: uppercase;
}
.kpi-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.0rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 2px;
}

/* BANNER ALLERTE E REMIND */
.alert-bar-remind {
    background: #23190f;
    border: 1px solid #f59e0b;
    border-left: 5px solid #fbbf24;
    color: #fef3c7;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    margin-bottom: 10px;
}
.alert-bar-sos {
    background: #131d31;
    border: 1px solid #0284c7;
    border-left: 5px solid #38bdf8;
    color: #e0f2fe;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    margin-bottom: 10px;
}
.alert-bar-crit {
    background: #2b1115;
    border: 1px solid #dc2626;
    border-left: 5px solid #ef4444;
    color: #fecaca;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    margin-bottom: 10px;
}

/* BOTTONI SECONDARI DI AZIONE RAPIDA */
div.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    border: 1.5px solid #38bdf8 !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    padding: 10px 16px !important;
    min-height: 44px !important;
    transition: transform 0.08s ease !important;
}
div.stButton > button[kind="secondary"] p { color: #ffffff !important; font-weight: 700 !important; }
div.stButton > button[kind="secondary"]:hover { background: #0ea5e9 !important; border-color: #ffffff !important; }
div.stButton > button[kind="secondary"]:active { transform: scale(0.97) !important; }

/* GRANDI QUADRATI TOUCH DELLA COSTELLAZIONE */
div.stButton > button[kind="primary"] {
    background: linear-gradient(160deg, #0d1524 0%, #111c30 100%) !important;
    border: 1.5px solid #1e3a5f !important;
    border-top: 2.5px solid #38bdf8 !important;
    border-radius: 8px !important;
    height: auto !important;
    min-height: 158px !important;
    width: 100% !important;
    padding: 14px 16px !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: stretch !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45) !important;
    margin-bottom: 8px !important;
    cursor: pointer !important;
    user-select: none !important;
    transition: transform 0.10s ease, border-color 0.15s ease, box-shadow 0.15s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(160deg, #132038 0%, #172a4a 100%) !important;
    border
