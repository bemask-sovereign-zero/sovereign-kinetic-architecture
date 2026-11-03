import streamlit as st
import json
import csv
import io
from datetime import datetime, timezone, timedelta

st.set_page_config(
    page_title="S.K.A. // BOSCHETTO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- OROLOGIO DI SISTEMA (FUSO ORARIO ITALIA) ---
def get_italy_now():
    return datetime.now(timezone(timedelta(hours=1)))

def get_current_window_info(now_dt):
    h = now_dt.hour
    if 6 <= h < 14:
        return "MATTINA (06:00-14:00)"
    elif 14 <= h < 19:
        return "POMERIGGIO (14:00-19:00)"
    else:
        return "SERA (19:00-03:00)"

# --- CSS PURO NATIVO (ZERO BLOCCHI JAVASCRIPT, CARICAMENTO ISTANTANEO) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

header[data-testid="stHeader"] { background: transparent !important; }

.stApp {
    background-color: #05080e !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    -webkit-tap-highlight-color: transparent;
}

.block-container {
    padding-top: 1.1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1380px !important;
}

div[data-testid="stVerticalBlock"] > div {
    gap: 0.25rem !important;
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
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: #f8fafc;
    text-transform: uppercase;
}
.brand-title span {
    color: #10b981;
    font-family: 'JetBrains Mono', monospace;
}
.brand-clock {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #10b981;
    background: #09121e;
    border: 1px solid #10b98155;
    padding: 4px 12px;
    border-radius: 3px;
}

/* LIVELLO 1: QUADRATI GEOMETRICI STILE EXCEL (216px FISSI, NOME PURO IN ALTO A SINISTRA) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(145deg, #071914 0%, #0b1422 100%) !important;
    border: 1px solid #1e293b !important;
    border-left: 5px solid #10b981 !important;
    border-top: 2px solid #10b98188 !important;
    border-radius: 4px !important;
    height: 216px !important;
    min-height: 216px !important;
    max-height: 216px !important;
    width: 100% !important;
    padding: 22px 22px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: flex-start !important;
    align-items: flex-start !important;
    text-align: left !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5) !important;
    margin: 0 !important;
    transition: transform 0.08s ease, border-color 0.15s ease, filter 0.15s ease !important;
}
div.stButton > button[kind="primary"]:hover {
    filter: brightness(1.25) !important;
    border-color: #34d399 !important;
}
div.stButton > button[kind="primary"]:active {
    transform: scale(0.98) !important;
}
div.stButton > button[kind="primary"] p {
    font-family: 'Inter', sans-serif !important;
    font-size: 1.24rem !important;
    font-weight: 800 !important;
    color: #ffffff !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    text-align: left !important;
    margin: 0 !important;
    padding-bottom: 10px !important;
    border-bottom: 2px solid rgba(255, 255, 255, 0.12) !important;
    width: 100% !important;
}

/* CODIFICA CROMATICA NATIVA CSS PER AREE (ZERO JAVASCRIPT) */
div[class*="st-key-sq_AMBER_"] button[kind="primary"] {
    background: linear-gradient(145deg, #1c1406 0%, #0d1320 100%) !important;
    border-left: 5px solid #f59e0b !important;
    border-top: 2px solid #f59e0b88 !important;
}
div[class*="st-key-sq_EMERALD_"] button[kind="primary"] {
    background: linear-gradient(145deg, #061c15 0%, #0b1422 100%) !important;
    border-left: 5px solid #10b981 !important;
    border-top: 2px solid #10b98188 !important;
}
div[class*="st-key-sq_CYAN_"] button[kind="primary"] {
    background: linear-gradient(145deg, #07192b 0%, #0d1627 100%) !important;
    border-left: 5px solid #38bdf8 !important;
    border-top: 2px solid #38bdf888 !important;
}
div[class*="st-key-sq_PURPLE_"] button[kind="primary"] {
    background: linear-gradient(145deg, #170d29 0%, #0c1424 100%) !important;
    border-left: 5px solid #a855f7 !important;
    border-top: 2px solid #a855f788 !important;
}

/* LIVELLO 2: LE 5 RIGHE CHE OCCUPANO ESATTAMENTE LO STESSO QUADRATO (216px TOTALI) */
div.stButton > button[kind="secondary"] {
    background: #0b1523 !important;
    color: #e2e8f0 !important;
    border: 1px solid #1e3a5f !important;
    border-left: 4px solid #10b981 !important;
    border-radius: 3px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 600 !important;
    font-size: 0.76rem !important;
    padding: 0px 12px !important;
    height: 32px !important;
    min-height: 32px !important;
    max-height: 32px !important;
    margin: 0 !important;
    text-align: left !important;
    justify-content: flex-start !important;
}
div.stButton > button[kind="secondary"] p {
    color: #f8fafc !important;
    font-weight: 600 !important;
    font-size: 0.75rem !important;
    text-align: left !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: #064e3b !important;
    border-color: #34d399 !important;
}

/* RETTANGOLO VERTICALE DI RIEPILOGO A DESTRA */
.right-tower {
    background: linear-gradient(180deg, #0b1320 0%, #070d17 100%);
    border: 1px solid #1e293b;
    border-top: 3px solid #10b981;
    border-radius: 4px;
    padding: 18px 16px;
    min-height: 664px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.tower-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    color: #10b981;
    letter-spacing: 0.08em;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
    margin-bottom: 12px;
}
.tower-item {
    background: #060a11;
    border: 1px solid #1e293b;
    border-left: 3.5px solid #38bdf8;
    border-radius: 3px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.tower-item-emerald {
    background: #06110e;
    border: 1px solid #064e3b;
    border-left: 3.5px solid #10b981;
    border-radius: 3px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.tower-item-amber {
    background: #141007;
    border: 1px solid #78350f;
    border-left: 3.5px solid #f59e0b;
    border-radius: 3px;
    padding: 12px 14px;
    margin-bottom: 10px;
}
.tower-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.64rem;
    color: #94a3b8;
    text-transform: uppercase;
}
.tower-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.28rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 3px;
}
.tower-sub {
    font-size: 0.68rem;
    color: #64748b;
    margin-top: 2px;
    font-family: 'JetBrains Mono', monospace;
}

/* QUADRETTI FRIGO INTERNI AL SOTTOMENU */
.haccp-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px; margin-bottom: 16px; }
.haccp-tile {
    width: 175px; min-height: 92px; border-radius: 4px; padding: 10px 12px;
    display: flex; flex-direction: column; justify-content: space-between;
    font-family: 'JetBrains Mono', monospace; color: #f8fafc;
}
.tile-purple  { background: #1e1333; border: 1px solid #9333ea; border-left: 4px solid #a855f7; }
.tile-green   { background: #062419; border: 1px solid #10b981; border-left: 4px solid #34d399; }
.tile-yellow  { background: #261c0b; border: 1px solid #d97706; border-left: 4px solid #eab308; }
.tile-red     { background: #2b1115; border: 1px solid #dc2626; border-left: 4px solid #ef4444; }
.tile-title   { font-family: 'Inter', sans-serif; font-size: 0.76rem; font-weight: 600; color: #e2e8f0; }
.tile-val     { font-size: 1.05rem; font-weight: 700; margin: 4px 0; }
.tile-meta    { font-size: 0.65rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 4px; display: flex; justify-content: space-between; }

/* TABELLA REGISTRO STAMPA UFFICIALE */
.log-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    margin-top: 10px;
}
.log-table th {
    background: #0f243c;
    color: #10b981;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #1e293b;
}
.log-table td {
    padding: 7px 10px;
    border: 1px solid #1e293b;
    color: #e2e8f0;
}

@media (max-width: 768px) {
    .block-container { padding-top: 0.8rem !important; padding-left: 0.5rem !important; padding-right: 0.5rem !important; }
    div.stButton > button[kind="primary"] { height: 165px !important; min-height: 165px !important; max-height: 165px !important; }
    .haccp-tile { width: 48% !important; }
}
</style>
""", unsafe_allow_html=True)

# --- MOTORE AUDIO TATTICO TRAMITE NUOVO COMANDO NATIVO st.html (ZERO DEPRECAZIONI) ---
def bind_global_tactile_audio(enabled=True):
    if not enabled:
        return
    js_html = """
    <script>
    (function() {
        const w = window.parent || window;
        const d = w.document;
        if (w.__skaSoundBound) return;
        w.__skaSoundBound = true;

        function playTone(freq1, freq2, dur) {
            try {
                const AudioCtx = w.AudioContext || w.webkitAudioContext;
                if (!AudioCtx) return;
                if (!w.__skaCtx) w.__skaCtx = new AudioCtx();
                const ctx = w.__skaCtx;
                if (ctx.state === 'suspended') ctx.resume();
                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = 'triangle';
                osc.frequency.setValueAtTime(freq1, now);
                osc.frequency.exponentialRampToValueAtTime(freq2, now + dur);
                gain.gain.setValueAtTime(0.25, now);
                gain.gain.exponentialRampToValueAtTime(0.001, now + dur + 0.02);
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start(now);
                osc.stop(now + dur + 0.02);
            } catch(e) {}
        }

        d.addEventListener('click', function(ev) {
            const btnP = ev.target.closest('button[kind="primary"]');
            const btnS = ev.target.closest('button');
            if (btnP) playTone(440, 880, 0.06);
            else if (btnS) playTone(660, 990, 0.04);
        }, true);
    })();
    </script>
    """
    try:
        st.html(js_html, unsafe_allow_javascript=True)
    except Exception:
        pass

def evaluate_fridge_status(fridge_type, temp_val, is_broken=False):
    if is_broken:
        return "RED", "GUASTO"
    if fridge_type == "NEG":
        if -26.0 <= temp_val <= -16.0: return "GREEN", f"{temp_val:+.1f}°C"
        elif -16.0 < temp_val <= -12.0 or temp_val < -26.0: return "YELLOW", f"{temp_val:+.1f}°C"
        else: return "RED", f"{temp_val:+.1f}°C"
    else:
        if -1.0 <= temp_val <= 5.5: return "GREEN", f"{temp_val:+.1f}°C"
        elif 5.5 < temp_val <= 8.0 or temp_val < -1.0: return "YELLOW", f"{temp_val:+.1f}°C"
        else: return "RED", f"{temp_val:+.1f}°C"

# --- ARCHITETTURA CON PALETTE CROMATICA PER AREE ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N00", "name": "DIREZIONE", "theme": "AMBER",
            "sub_zones": ["Ufficio Direzione", "Amministrazione"],
            "fridges": [],
            "tasks": [{"title": "Verifica Quadro Sinottico", "done": True}]
        },
        {
            "id": "N01", "name": "PASTICCERIA", "theme": "EMERALD",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni"],
            "fridges": [
                {"name": "Cella Basi +4°C", "kind": "POS"},
                {"name": "Cella Semifreddi -18°C", "kind": "NEG"},
                {"name": "Abbattitore Lab", "kind": "NEG"},
                {"name": "Vetrina Torte +4°C", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Cottura Lievitati Mattina", "done": True},
                {"title": "Linea Senza Glutine / Lattosio", "done": True},
                {"title": "Torte Cerimonia / Credenza", "done": False}
            ]
        },
        {
            "id": "N02", "name": "CAMERE", "theme": "CYAN",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria"],
            "fridges": [
                {"name": "Frigo Office Piano 1", "kind": "POS"},
                {"name": "Frigo Office Piano 2", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Priorità Camere in Partenza", "done": True},
                {"title": "Riassetto Camere Fermate", "done": False}
            ]
        },
        {
            "id": "N03", "name": "RECEPTION", "theme": "CYAN",
            "sub_zones": ["Front Desk", "Accoglienza Ospiti"],
            "fridges": [],
            "tasks": [
                {"title": "Invio Schedine Alloggiati / ISTAT", "done": True},
                {"title": "Controllo Arrivi del Giorno", "done": True}
            ]
        },
        {
            "id": "N04", "name": "SALA COLAZIONI", "theme": "EMERALD",
            "sub_zones": ["Buffet Centrale", "Sala Colazioni", "Veranda Colazioni"],
            "fridges": [
                {"name": "Buffet Freddo Colazioni", "kind": "POS"},
                {"name": "Vetrina Yogurt & Latte", "kind": "POS"},
                {"name": "Vetrina Salumi & Formaggi", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Allestimento Buffet ore 07:00", "done": True},
                {"title": "Sanificazione Fine Servizio", "done": False}
            ]
        },
        {
            "id": "N05", "name": "RISTORANTE", "theme": "EMERALD",
            "sub_zones": ["Cucina Centrale", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare"],
            "fridges": [
                {"name": "Cella Carne +2°C", "kind": "POS"},
                {"name": "Cella Pesce 0°C", "kind": "POS"},
                {"name": "Congelatore Stoccaggio", "kind": "NEG"},
                {"name": "Abbattitore Cucina", "kind": "NEG"},
                {"name": "Frigo Linea Antipasti", "kind": "POS"},
                {"name": "Frigo Linea Primi/Sec.", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Mise en Place Verande", "done": True},
                {"title": "Controllo Stoccaggio Celle", "done": True}
            ]
        },
        {
            "id": "N06", "name": "BAR", "theme": "EMERALD",
            "sub_zones": ["Banco Caffetteria", "Terrazza Bar", "Cocktail Station"],
            "fridges": [
                {"name": "Banco Bar 1 (Latte)", "kind": "POS"},
                {"name": "Banco Bar 2 (Birre/Vini)", "kind": "POS"},
                {"name": "Vetrina Gelati -16°C", "kind": "NEG"},
                {"name": "Pozzetto Ghiaccio Bar", "kind": "NEG"}
            ],
            "tasks": [
                {"title": "Apertura Banco Caffetteria", "done": True},
                {"title": "Rifornimento Linea Aperitivo", "done": False}
            ]
        },
        {
            "id": "N07", "name": "SPIAGGIA", "theme": "PURPLE",
            "sub_zones": ["Gazebo Cerimonie", "Ombrelloni & Tende", "Chiosco Spiaggia"],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Apertura Ombrelloni e Tende", "done": True},
                {"title": "Allestimento Gazebo Evento", "done": False}
            ]
        },
        {
            "id": "N08", "name": "PARCHEGGIO", "theme": "PURPLE",
            "sub_zones": ["Ingresso Principale", "Area Sosta Hotel", "Area Sposi"],
            "fridges": [],
            "tasks": [
                {"title": "Controllo Sbarra e Posti Riservati", "done": True}
            ]
        }
    ]

    haccp_state = {}
    for n in nodes:
        for fr in n["fridges"]:
            key = f"{n['id']} || {fr['name']}"
            haccp_state[key] = {
                "node_id": n["id"], "node_name": n["name"], "fridge_name": fr["name"],
                "status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--",
                "kind": fr["kind"]
            }

    haccp_state["N01 || Cella Basi +4°C"].update({"status": "GREEN", "label": "+3.6°C", "by": "Marco S.", "pin": "1001", "time": "06:45"})
    haccp_state["N01 || Cella Semifreddi -18°C"].update({"status": "GREEN", "label": "-19.5°C", "by": "Marco S.", "pin": "1001", "time": "06:46"})
    haccp_state["N04 || Buffet Freddo Colazioni"].update({"status": "GREEN", "label": "+3.9°C", "by": "Jolly 01", "pin": "1004", "time": "06:50"})
    haccp_state["N04 || Vetrina Yogurt & Latte"].update({"status": "GREEN", "label": "+4.1°C", "by": "Jolly 01", "pin": "1004", "time": "06:51"})
    haccp_state["N05 || Cella Carne +2°C"].update({"status": "GREEN", "label": "+2.4°C", "by": "Matteo B.", "pin": "1005", "time": "06:52"})
    haccp_state["N05 || Cella Pesce 0°C"].update({"status": "YELLOW", "label": "+6.2°C", "by": "Matteo B.", "pin": "1005", "time": "06:55"})

    today_d = datetime.now(timezone(timedelta(hours=1))).strftime("%d/%m/%Y")
    haccp_logs = [
        {"date": today_d, "time": "06:45", "window": "MATTINA", "node": "PASTICCERIA", "fridge": "Cella Basi +4°C", "temp": "+3.6°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001"},
        {"date": today_d, "time": "06:46", "window": "MATTINA", "node": "PASTICCERIA", "fridge": "Cella Semifreddi -18°C", "temp": "-19.5°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001"},
        {"date": today_d, "time": "06:50", "window": "MATTINA", "node": "SALA COLAZIONI", "fridge": "Buffet Freddo Colazioni", "temp": "+3.9°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004"},
        {"date": today_d, "time": "06:51", "window": "MATTINA", "node": "SALA COLAZIONI", "fridge": "Vetrina Yogurt & Latte", "temp": "+4.1°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004"},
        {"date": today_d, "time": "06:52", "window": "MATTINA", "node": "RISTORANTE", "fridge": "Cella Carne +2°C", "temp": "+2.4°C", "outcome": "CONFORME", "operator": "Matteo B.", "pin_sig": "PIN #1005"},
        {"date": today_d, "time": "06:55", "window": "MATTINA", "node": "RISTORANTE", "fridge": "Cella Pesce 0°C", "temp": "+6.2°C", "outcome": "PRE-ALLARME", "operator": "Matteo B.", "pin_sig": "PIN #1005"}
    ]

    return {
        "schema_v": "v15_native_fast_css",
        "nodes": nodes,
        "haccp_state": haccp_state,
        "haccp_logs": haccp_logs,
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante Piani", "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Giulia F.", "role": "Receptionist", "node_id": "N03", "sub_zone": "Front Desk", "shift": "Mattina (07-15)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Resp. Colazioni", "node_id": "N04", "sub_zone": "Buffet Centrale", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Matteo B.", "role": "Maître Ristorante", "node_id": "N05", "sub_zone": "Veranda 1", "shift": "Pranzo/Sera"},
            {"pin": "1006", "nick": "Extra A", "role": "Barman Terrazza", "node_id": "N06", "sub_zone": "Terrazza Bar", "shift": "Mattina (07-15)"},
            {"pin": "1007", "nick": "Bagnino", "role": "Presidio Spiaggia", "node_id": "N07", "sub_zone": "Gazebo Cerimonie", "shift": "Giornaliero"}
        ],
        "sos_queue": [],
        "events": [
            {"id": "EV1", "title": "Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "phase": "2. Aperitivo"}
        ]
    }

store = get_shared_store()

if store.get("schema_v") != "v15_native_fast_css":
    st.cache_resource.clear()
    st.rerun()

if "expanded_node_id" not in st.session_state:
    st.session_state.expanded_node_id = None
if "opened_submenu_node" not in st.session_state:
    st.session_state.opened_submenu_node = None
if "opened_submenu_row" not in st.session_state:
    st.session_state.opened_submenu_row = None
if "active_pin" not in st.session_state:
    st.session_state.active_pin = "9999"

now_it = get_italy_now()
now_str = now_it.strftime("%H:%M")
today_str = now_it.strftime("%d/%m/%Y")
win_name = get_current_window_info(now_it)

unchecked_list = [v for v in store["haccp_state"].values() if v["status"] == "PURPLE"]
total_fridges = len(store["haccp_state"])
checked_fridges = total_fridges - len(unchecked_list)

# --- INTESTAZIONE ---
st.markdown(f"""
<div class="top-bar">
    <div class="brand-title">SOVEREIGN KINETIC ARCHITECTURE <span>// BOSCHETTO PRO</span></div>
    <div class="brand-clock">{now_str}  |  {win_name}</div>
</div>
""", unsafe_allow_html=True)

c_pin, c_btn, c_dir, c_sonar = st.columns([1.3, 1.1, 1.1, 1.2])
with c_pin:
    new_pin = st.text_input("PIN ACCESSO", value=st.session_state.active_pin, label_visibility="collapsed", placeholder="PIN (9999 Dir. | 1001..1007 Staff)")
with c_btn:
    if st.button("CONFERMA PIN ↵", type="secondary", use_container_width=True) or (new_pin != st.session_state.active_pin):
        st.session_state.active_pin = new_pin.strip()
        st.session_state.expanded_node_id = None
        st.session_state.opened_submenu_node = None
        st.rerun()
with c_dir:
    if st.button("PIANTA PRINCIPALE", type="secondary", use_container_width=True):
        st.session_state.active_pin = "9999"
        st.session_state.expanded_node_id = None
        st.session_state.opened_submenu_node = None
        st.rerun()
with c_sonar:
    sonar_active = st.toggle("AUDIO TASTI", value=True)

bind_global_tactile_audio(sonar_active)

pin_input = st.session_state.active_pin

# ==============================================================================
# VISTA DIREZIONE (PIN 9999)
# ==============================================================================
if pin_input in ["9999", "0000"]:

    # --------------------------------------------------------------------------
    # PIANTA PRINCIPALE: QUADRATI PURI CON CODIFICA COLORE NATIVA + COLONNA DESTRA
    # --------------------------------------------------------------------------
    if st.session_state.opened_submenu_node is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_logs = len(store["haccp_logs"])
        tot_nodes = len(store["nodes"])

        col_center, col_right = st.columns([3.0, 1.15], gap="small")

        with col_center:
            num_rows = (tot_nodes + 2) // 3
            for r_idx in range(num_rows):
                row_cols = st.columns(3, gap="small")
                for c_idx in range(3):
                    idx = r_idx * 3 + c_idx
                    if idx < tot_nodes:
                        node = store["nodes"][idx]
                        nid = node["id"]
                        theme = node.get("theme", "EMERALD")
                        with row_cols[c_idx]:
                            if st.session_state.expanded_node_id == nid:
                                if nid == "N00":
                                    five_rows = [
                                        (1, "1. Espandi Architettura"),
                                        (2, "2. Rinomina"),
                                        (3, "3. Anagrafica"),
                                        (4, "4. Agenda Eventi"),
                                        (5, "5. Registro Ufficiale")
                                    ]
                                else:
                                    five_rows = [
                                        (1, "1. Unità Frigo & HACCP"),
                                        (2, "2. Presidio Staff"),
                                        (3, "3. Checklist Reparto"),
                                        (4, "4. Segnalazioni & Guasti"),
                                        (5, "5. Configura Slot")
                                    ]

                                for r_num, r_txt in five_rows:
                                    if st.button(r_txt, key=f"r5_{nid}_{r_num}", type="secondary", use_container_width=True):
                                        st.session_state.opened_submenu_node = nid
                                        st.session_state.opened_submenu_row = r_num
                                        st.rerun()

                                if st.button(f"✖ {node['name']}", key=f"close_{nid}", type="secondary", use_container_width=True):
                                    st.session_state.expanded_node_id = None
                                    st.rerun()
                            else:
                                # SOLO IL NOME PURO DEL QUADRATO (NESSUN PALLINO VERDE O SCRITTA SOTTO)
                                if st.button(node["name"], key=f"sq_{theme}_{nid}", type="primary", use_container_width=True):
                                    st.session_state.expanded_node_id = nid
                                    st.rerun()

        # RETTANGOLO VERTICALE DI RIEPILOGO A DESTRA
        with col_right:
            sos_txt = f"{tot_sos} APERTI" if tot_sos > 0 else "0 ATTIVI"
            st.markdown(f"""
            <div class="right-tower">
                <div>
                    <div class="tower-header">QUADRO SINOTTICO</div>
                    <div class="tower-item-emerald">
                        <div class="tower-lbl">CONTROLLI HACCP ({win_name.split()[0]})</div>
                        <div class="tower-val">{checked_fridges}/{total_fridges}</div>
                        <div class="tower-sub">Unità certificate</div>
                    </div>
                    <div class="tower-item">
                        <div class="tower-lbl">PRESIDIO STAFF</div>
                        <div class="tower-val">{tot_fig} UNITÀ</div>
                        <div class="tower-sub">Operatori in turno</div>
                    </div>
                    <div class="tower-item-amber">
                        <div class="tower-lbl">SEGNALAZIONI</div>
                        <div class="tower-val">{sos_txt}</div>
                        <div class="tower-sub">Richieste dai reparti</div>
                    </div>
                    <div class="tower-item-emerald">
                        <div class="tower-lbl">REGISTRO ASL</div>
                        <div class="tower-val">{tot_logs} FIRME</div>
                        <div class="tower-sub">Pronte per stampa</div>
                    </div>
                </div>
                <div style="font-family:'JetBrains Mono',monospace;font-size:0.66rem;color:#94a3b8;border-top:1px solid #1e293b;padding-top:10px;line-height:1.7;">
                    <span style="color:#f59e0b;">■</span> DIREZIONE<br>
                    <span style="color:#10b981;">■</span> FOOD & BEVERAGE<br>
                    <span style="color:#38bdf8;">■</span> ACCOGLIENZA & CAMERE<br>
                    <span style="color:#a855f7;">■</span> ESTERNI & SPIAGGIA
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 3: IL SOTTOMENU APERTO
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.opened_submenu_node
        r_num = st.session_state.opened_submenu_row
        node = next(n for n in store["nodes"] if n["id"] == nid)

        c_back1, c_back2 = st.columns([1.5, 1.5])
        with c_back1:
            if st.button(f"⬅ TORNA ALLE 5 RIGHE DI {node['name']}", type="secondary", use_container_width=True):
                st.session_state.opened_submenu_node = None
                st.rerun()
        with c_back2:
            if st.button("TORNA ALLA PIANTA PRINCIPALE", type="secondary", use_container_width=True):
                st.session_state.opened_submenu_node = None
                st.session_state.expanded_node_id = None
                st.rerun()

        st.divider()

        if nid == "N00":
            if r_num == 1:
                st.markdown("### DIREZIONE // 1. ESPANDI ARCHITETTURA")
                c_n1, c_n2 = st.columns([2, 1])
                ns_name = c_n1.text_input("Nome Nuovo Quadrato (es. PISCINA / SPA / CANTINA)")
                ns_col = c_n2.selectbox("Colore Area", ["Verde Smeraldo (F&B)", "Blu Ciano (Camere/Ospiti)", "Viola Indaco (Esterni)", "Oro Ambra (Direzione)"])
                col_map = {
                    "Verde Smeraldo (F&B)": "EMERALD",
                    "Blu Ciano (Camere/Ospiti)": "CYAN",
                    "Viola Indaco (Esterni)": "PURPLE",
                    "Oro Ambra (Direzione)": "AMBER"
                }
                if st.button("➕ CREA NUOVO QUADRATO NELLA GRIGLIA", type="secondary"):
                    if ns_name:
                        store["nodes"].append({
                            "id": f"N{int(datetime.now().timestamp())}",
                            "name": ns_name.strip().upper(),
                            "theme": col_map[ns_col],
                            "sub_zones": ["Zona 1"],
                            "fridges": [],
                            "tasks": [{"title": "Controllo Apertura", "done": False}]
                        })
                        st.rerun()

                st.divider()
                st.markdown("##### Reparti Attivi nella Pianta Principale")
                for idx_n, nd in enumerate(store["nodes"]):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"- **`{nd['name']}`**")
                    if nd["id"] != "N00":
                        if c2.button("Rimuovi", key=f"del_sq_{nd['id']}"):
                            store["nodes"].pop(idx_n)
                            st.rerun()

            elif r_num == 2:
                st.markdown("### DIREZIONE // 2. RINOMINA REPARTI")
                for idx_n, nd in enumerate(store["nodes"]):
                    nd["name"] = st.text_input(f"Nome Quadrato {idx_n+1}", value=nd["name"], key=f"rn_{nd['id']}")
                if st.button("💾 SALVA NOMI", type="secondary", use_container_width=True):
                    st.rerun()

            elif r_num == 3:
                st.markdown("### DIREZIONE // 3. ANAGRAFICA & PIN")
                cs1, cs2, cs3 = st.columns(3)
                ns_nick = cs1.text_input("Nome Operatore (es. Luca M.)")
                ns_role = cs2.text_input("Mansione (es. Cameriere)")
                ns_pin = cs3.text_input("PIN a 4 cifre (es. 1008)")

                cs4, cs5 = st.columns(2)
                node_map = {n["name"]: n for n in store["nodes"]}
                ns_node_label = cs4.selectbox("Assegna al Reparto", list(node_map.keys()))
                chosen_node = node_map[ns_node_label]
                ns_shift = cs5.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)", "Giornaliero"])

                if st.button("➕ ATTIVA OPERATORE", type="secondary"):
                    if ns_nick and ns_pin:
                        store["figurine"].append({
                            "pin": ns_pin.strip(), "nick": ns_nick.strip(),
                            "role": ns_role.strip() or "Staff",
                            "node_id": chosen_node["id"],
                            "sub_zone": chosen_node["sub_zones"][0] if chosen_node["sub_zones"] else "Generale",
                            "shift": ns_shift
                        })
                        st.rerun()

                st.divider()
                for idx_f, f in enumerate(store["figurine"]):
                    cf1, cf2 = st.columns([4, 1])
                    cf1.markdown(f"- **PIN `{f['pin']}`** — **{f['nick']}** ({f['role']})")
                    if cf2.button("Rimuovi", key=f"rm_f_{f['pin']}_{idx_f}"):
                        store["figurine"].pop(idx_f)
                        st.rerun()

            elif r_num == 4:
                st.markdown("### DIREZIONE // 4. AGENDA EVENTI")
                phase_options = ["1. Accoglienza / Rito", "2. Aperitivo", "3. Servito", "4. Fuori Torta!", "5. Open Bar & Musica"]
                for idx, ev in enumerate(store["events"]):
                    with st.expander(f"{ev['title']} — {ev['zone']} ({ev['pax']} pax | Torta: {ev['cake_time']})", expanded=True):
                        c_e1, c_e2 = st.columns([3, 1])
                        cur_i = phase_options.index(ev["phase"]) if ev["phase"] in phase_options else 0
                        new_ph = c_e1.selectbox("Fase Live", phase_options, index=cur_i, key=f"ev_{ev['id']}")
                        if new_ph != ev["phase"]:
                            ev["phase"] = new_ph
                            st.rerun()
                        if c_e2.button("Elimina", key=f"del_ev_{ev['id']}"):
                            store["events"].pop(idx)
                            st.rerun()

                st.divider()
                ce1, ce2, ce3, ce4 = st.columns(4)
                ne_title = ce1.text_input("Nuovo Evento")
                ne_zone = ce2.selectbox("Location", ["Gazebo -> Veranda Circolare", "Veranda Grande", "Veranda 1", "Sala Interna"])
                ne_pax = ce3.number_input("Ospiti (Pax)", min_value=1, value=60, step=5)
                ne_cake = ce4.text_input("Orario Torta", value="22:45")
                if st.button("➕ AGGIUNGI IN AGENDA", type="secondary"):
                    if ne_title:
                        store["events"].append({"id": f"EV{int(datetime.now().timestamp())}", "title": ne_title, "zone": ne_zone, "pax": ne_pax, "cake_time": ne_cake, "phase": "1. Accoglienza / Rito"})
                        st.rerun()

            elif r_num == 5:
                st.markdown("### DIREZIONE // 5. REGISTRO UFFICIALE ASL")
                rows_html = ""
                for log in reversed(store["haccp_logs"]):
                    rows_html += (
                        f"<tr><td>{log['date']}</td><td><b>{log['time']}</b></td><td>{log['window']}</td>"
                        f"<td>{log['node']}</td><td>{log['fridge']}</td><td><b>{log['temp']}</b></td>"
                        f"<td>{log['outcome']}</td><td><b>{log['operator']}</b></td><td>{log['pin_sig']}</td></tr>"
                    )
                st.markdown(f"""
                <table class="log-table">
                    <thead><tr><th>DATA</th><th>ORA</th><th>FASCIA</th><th>REPARTO</th><th>UNITÀ FRIGO</th><th>TEMP.</th><th>ESITO</th><th>OPERATORE</th><th>FIRMA</th></tr></thead>
                    <tbody>{rows_html}</tbody>
                </table>
                """, unsafe_allow_html=True)

                st.divider()
                printable_html = f"""
                <html><head><meta charset="utf-8"><title>Registro HACCP</title>
                <style>body{{font-family:Arial,sans-serif;padding:20px;}} table{{width:100%;border-collapse:collapse;margin-top:15px;font-size:12px;}} th,td{{border:1px solid #000;padding:6px;text-align:left;}}</style>
                </head><body><h2>REGISTRO UFFICIALE AUTOCONTROLLO HACCP — BOSCHETTO PRO</h2>
                <div>Data Stampa: {today_str} ore {now_str}</div>
                <table><thead><tr><th>Data</th><th>Ora</th><th>Fascia</th><th>Reparto</th><th>Unità Frigo</th><th>Temp.</th><th>Esito</th><th>Firmatario</th><th>PIN</th></tr></thead>
                <tbody>{rows_html}</tbody></table></body></html>
                """
                csv_buffer = io.StringIO()
                writer = csv.DictWriter(csv_buffer, fieldnames=["date", "time", "window", "node", "fridge", "temp", "outcome", "operator", "pin_sig"])
                writer.writeheader()
                writer.writerows(store["haccp_logs"])

                cp1, cp2, cp3 = st.columns(3)
                with cp1:
                    st.download_button("🖨️ SCARICA STAMPA ASL (.HTML)", data=printable_html, file_name=f"REGISTRO_ASL_{now_it.strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
                with cp2:
                    st.download_button("📊 SCARICA EXCEL (.CSV)", data=csv_buffer.getvalue(), file_name=f"REGISTRO_HACCP_{now_it.strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
                with cp3:
                    if st.button("🔄 NUOVO GIRO (RESET ATTESA)", type="secondary", use_container_width=True):
                        for k in store["haccp_state"]:
                            store["haccp_state"][k].update({"status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--"})
                        st.rerun()

        else:
            node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
            node_staff = [f for f in store["figurine"] if f["node_id"] == nid]

            if r_num == 1:
                st.markdown(f"### {node['name']} // 1. UNITÀ FRIGO & HACCP")
                if not node_fridges:
                    st.info("Nessuna unità frigorifera in questo reparto. Puoi aggiungerla dalla Riga 5 (Configura Slot).")
                else:
                    tiles_html = "<div class='haccp-grid'>"
                    for st_data in node_fridges:
                        css_class = {"PURPLE": "tile-purple", "GREEN": "tile-green", "YELLOW": "tile-yellow", "RED": "tile-red"}[st_data["status"]]
                        tiles_html += (
                            f"<div class='haccp-tile {css_class}'>"
                            f"<div class='tile-title'>{st_data['fridge_name']}</div>"
                            f"<div class='tile-val'>{st_data['label']}</div>"
                            f"<div class='tile-meta'><span>🕒 {st_data['time']}</span><span>✍️ {st_data['by']}</span></div>"
                            f"</div>"
                        )
                    tiles_html += "</div>"
                    st.markdown(tiles_html, unsafe_allow_html=True)

                    st.divider()
                    my_keys = [k for k, v in store["haccp_state"].items() if v["node_id"] == nid]
                    c_f1, c_f2, c_f3 = st.columns([2, 2, 1.5])
                    sel_k = c_f1.selectbox("Unità Frigo", my_keys, format_func=lambda x: x.split(" || ")[1])
                    fr_obj = store["haccp_state"][sel_k]
                    def_t = 3.0 if fr_obj["kind"] == "POS" else -19.0
                    t_val = c_f2.slider("Temperatura (°C)", -28.0, 15.0, def_t, 0.5)
                    signer = c_f3.selectbox("Firmatario", [f["nick"] for f in node_staff] if node_staff else ["Direzione"])
                    is_brk = st.checkbox("Segnala Guasto")
                    if st.button(f"✍️ FIRMA E TIMBRA ORE {now_str}", type="secondary"):
                        st_col, lbl_t = evaluate_fridge_status(fr_obj["kind"], t_val, is_brk)
                        out_map = {"GREEN": "CONFORME", "YELLOW": "PRE-ALLARME", "RED": "CRITICO/GUASTO"}
                        fr_obj.update({"status": st_col, "label": lbl_t, "by": signer, "pin": "9999", "time": now_str})
                        store["haccp_logs"].append({
                            "date": today_str, "time": now_str, "window": win_name.split()[0],
                            "node": node["name"], "fridge": fr_obj["fridge_name"],
                            "temp": lbl_t, "outcome": out_map[st_col], "operator": signer, "pin_sig": "Plancia"
                        })
                        st.rerun()

            elif r_num == 2:
                st.markdown(f"### {node['name']} // 2. PRESIDIO STAFF")
                for f in node_staff:
                    st.markdown(f"- **{f['nick']}** ({f['role']}) — Turno: `{f['shift']}` | PIN: `{f['pin']}`")
                st.divider()
                pick_fig = st.selectbox("Sposta qui un Operatore", [f["nick"] for f in store["figurine"]])
                if st.button("Conferma Assegnazione", type="secondary"):
                    for f in store["figurine"]:
                        if f["nick"] == pick_fig:
                            f["node_id"] = nid
                    st.rerun()

            elif r_num == 3:
                st.markdown(f"### {node['name']} // 3. CHECKLIST REPARTO")
                for idx_t, t in enumerate(node.get("tasks", [])):
                    t["done"] = st.checkbox(t["title"], value=t["done"], key=f"tk_{nid}_{idx_t}")
                st.divider()
                new_tk = st.text_input("Nuova voce checklist:")
                if st.button("➕ Aggiungi Voce", type="secondary"):
                    if new_tk:
                        node.setdefault("tasks", []).append({"title": new_tk.strip(), "done": False})
                        st.rerun()

            elif r_num == 4:
                st.markdown(f"### {node['name']} // 4. SEGNALAZIONI & GUASTI")
                node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]
                for req in node_sos:
                    st.warning(f"Ore {req['time']} — {req['item']}")
                if node_sos and st.button("✔️ Segna come risolte", type="secondary"):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()
                new_req = st.text_input("Nuova segnalazione o richiesta:")
                if st.button("Invia Segnalazione", type="secondary"):
                    if new_req:
                        store["sos_queue"].append({"time": now_str, "node_id": nid, "from": node["name"], "item": new_req.strip(), "status": "Aperto"})
                        st.rerun()

            elif r_num == 5:
                st.markdown(f"### {node['name']} // 5. CONFIGURA SLOT")
                new_n_name = st.text_input("Rinomina questo Reparto", value=node["name"])
                if st.button("💾 Salva Nome", type="secondary"):
                    node["name"] = new_n_name.strip().upper()
                    st.rerun()
                st.divider()
                cf1, cf2 = st.columns(2)
                fr_new_name = cf1.text_input("Aggiungi Unità Frigo")
                fr_new_kind = cf2.selectbox("Regime", ["POS (+0°C / +5°C)", "NEG (-18°C / -22°C)"])
                if st.button("➕ Aggiungi Unità Frigo", type="secondary"):
                    if fr_new_name:
                        k_code = "POS" if "POS" in fr_new_kind else "NEG"
                        node["fridges"].append({"name": fr_new_name.strip(), "kind": k_code})
                        store["haccp_state"][f"{nid} || {fr_new_name.strip()}"] = {
                            "node_id": nid, "node_name": node["name"], "fridge_name": fr_new_name.strip(),
                            "status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--", "kind": k_code
                        }
                        st.rerun()

# ==============================================================================
# VISTA OPERATORE (PIN 1001..1007)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error("PIN non riconosciuto. Tocca 'PIANTA PRINCIPALE' per tornare in Direzione.")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.success(f"OPERATORE: {user['nick']} ({user['role']})  |  REPARTO: {user_node['name']}  |  ORA: {now_str}")

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        if my_fridges:
            sel_key = st.selectbox("Seleziona Unità Frigo", my_fridges, format_func=lambda x: f"{x.split(' || ')[1]} [{store['haccp_state'][x]['label']}]")
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("Unità Frigo GUASTA")
            if st.button(f"✍️ FIRMA E TIMBRA ORE {now_str}", type="secondary", use_container_width=True):
                status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                outcome_map = {"GREEN": "CONFORME", "YELLOW": "PRE-ALLARME", "RED": "CRITICO/GUASTO"}
                fr_info.update({"status": status_color, "label": label_text, "by": user["nick"], "pin": user["pin"], "time": now_str})
                store["haccp_logs"].append({
                    "date": today_str, "time": now_str, "window": win_name.split()[0],
                    "node": user_node["name"], "fridge": fr_info["fridge_name"],
                    "temp": label_text, "outcome": outcome_map[status_color], "operator": user["nick"], "pin_sig": f"PIN #{user['pin']}"
                })
                st.rerun()
