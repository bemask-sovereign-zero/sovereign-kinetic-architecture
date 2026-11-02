import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

st.set_page_config(
    page_title="S.K.A. // BOSCHETTO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ARCHITETTONICO: PULIZIA, ALTO CONTRASTO E PRATICITÀ ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

header[data-testid="stHeader"] {
    background: transparent !important;
}

button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] button {
    background-color: #0284c7 !important;
    color: #ffffff !important;
    border: 2px solid #38bdf8 !important;
    border-radius: 8px !important;
}

.stApp {
    background-color: #090d16 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

.block-container {
    padding-top: 2.0rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* INTESTAZIONE */
.top-bar {
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
    margin-bottom: 14px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
}
.brand-title {
    font-size: 1.2rem;
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
.brand-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #38bdf8;
    letter-spacing: 0.03em;
}

/* STRISCIA KPI TECNICA (5 INDICATORI CON PRESENZE HOTEL LIVE) */
.kpi-bar {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.kpi-box {
    background: #0f172a;
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

/* BANNER DISPACCI & ALLERTE */
.dispatch-bar {
    background: #0c192c;
    border: 1px solid #0284c7;
    border-left: 4px solid #38bdf8;
    color: #e0f2fe;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.80rem;
    margin-bottom: 12px;
}
.alert-bar-sos {
    background: #1e1b18;
    border: 1px solid #d97706;
    border-left: 4px solid #f59e0b;
    color: #fde68a;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin-bottom: 12px;
}
.alert-bar-crit {
    background: #231215;
    border: 1px solid #dc2626;
    border-left: 4px solid #ef4444;
    color: #fecaca;
    padding: 10px 14px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin-bottom: 12px;
}

/* BOTTONI SECONDARI: AZZURRO VIVO E TESTO BIANCO */
div.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%) !important;
    color: #ffffff !important;
    border: 1.5px solid #38bdf8 !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.84rem !important;
    padding: 10px 16px !important;
    box-shadow: 0 4px 12px rgba(2, 132, 199, 0.3) !important;
}
div.stButton > button[kind="secondary"] p {
    color: #ffffff !important;
    font-weight: 700 !important;
}
div.stButton > button[kind="secondary"]:hover {
    background: #0ea5e9 !important;
    border-color: #ffffff !important;
}

/* CARD NODI DELLA COSTELLAZIONE */
div.stButton > button[kind="primary"] {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-top: 2px solid #38bdf8 !important;
    border-radius: 6px !important;
    height: auto !important;
    min-height: 118px !important;
    width: 100% !important;
    padding: 15px 18px !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    margin-bottom: 6px !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #16243d !important;
    border-color: #38bdf8 !important;
}
div.stButton > button[kind="primary"] p {
    white-space: pre-line !important;
    line-height: 1.55 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    color: #cbd5e1 !important;
    margin: 0 !important;
    text-align: left !important;
}
div.stButton > button[kind="primary"] p::first-line {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}

/* MATRICE QUADRETTI HACCP */
.haccp-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; margin-bottom: 16px; }
.haccp-tile {
    width: 160px; min-height: 88px; border-radius: 4px; padding: 10px 12px;
    display: flex; flex-direction: column; justify-content: space-between;
    font-family: 'JetBrains Mono', monospace; color: #f8fafc;
}
.tile-purple { background: #1e1333; border: 1px solid #7e22ce; border-left: 4px solid #a855f7; }
.tile-green  { background: #092218; border: 1px solid #15803d; border-left: 4px solid #22c55e; }
.tile-yellow { background: #261c0b; border: 1px solid #b45309; border-left: 4px solid #eab308; }
.tile-red    { background: #2b1115; border: 1px solid #b91c1c; border-left: 4px solid #ef4444; }
.tile-title  { font-family: 'Inter', sans-serif; font-size: 0.74rem; font-weight: 600; color: #e2e8f0; }
.tile-val    { font-size: 1.05rem; font-weight: 700; margin: 4px 0; }
.tile-slots  { font-size: 0.65rem; color: #94a3b8; display: flex; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 4px; }

label, .stRadio label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #cbd5e1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}

@media (max-width: 768px) {
    .block-container {
        padding-top: 1.4rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .kpi-bar {
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    .haccp-tile {
        width: 48% !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- SONAR TATTICO ---
def play_tactical_sonar(mode="ping"):
    freq = 880 if mode == "ping" else 220
    wave = "sine" if mode == "ping" else "triangle"
    js_code = f"""
    <script>
    (function() {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator(); const gain = ctx.createGain();
        osc.type = '{wave}'; osc.frequency.setValueAtTime({freq}, ctx.currentTime);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
        osc.connect(gain); gain.connect(ctx.destination);
        osc.start(); osc.stop(ctx.currentTime + 0.3);
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)

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

# --- DNA STRUTTURALE & MEMORIA CONDIVISA ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N01", "code": "01", "name": "CASA MADRE", "subtitle": "Laboratorio Pasticceria & Direzione",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni & Sfogliatura", "Uffici Direzione"],
            "breakfast_profiles": [
                {"name": "Linea Lievitati Standard (B&B)", "active": True},
                {"name": "Pasticceria & Torte Credenza (HB/FB)", "active": True},
                {"name": "Linea Dedicata Gluten-Free / Senza Lattosio", "active": True}
            ],
            "fridges": [
                {"name": "Cella Basi +4°C", "kind": "POS"},
                {"name": "Cella Semifreddi -18°C", "kind": "NEG"},
                {"name": "Abbattitore Lab", "kind": "NEG"},
                {"name": "Vetrina Torte +4°C", "kind": "POS"}
            ]
        },
        {
            "id": "N02", "code": "02", "name": "CORPO ALBERGO", "subtitle": "Camere, Piani & Housekeeping",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria"],
            "breakfast_profiles": [
                {"name": "Room Service Camera", "active": True},
                {"name": "Early Breakfast Box", "active": False}
            ],
            "fridges": [{"name": "Frigo Office Piani", "kind": "POS"}]
        },
        {
            "id": "N03", "code": "03", "name": "RICEVIMENTO & HUB", "subtitle": "Imputazione Presenze, Dispacci & Magazzino",
            "sub_zones": ["Front Desk & Briefing", "Magazzino Centrale", "Baia Scarico Fornitori"],
            "breakfast_profiles": [],
            "fridges": [
                {"name": "Cella Latticini/Salumi", "kind": "POS"},
                {"name": "Cella Ortofrutta +6°C", "kind": "POS"},
                {"name": "Cella Scorte Bevande", "kind": "POS"}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "RISTORANTE & VERANDE", "subtitle": "Cucina Centrale, Sala Colazioni & 5 Verande",
            "sub_zones": ["Sala Colazioni", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare", "Cucina Centrale"],
            "breakfast_profiles": [
                {"name": "Tipo A: Buffet Continentale / B&B", "active": True},
                {"name": "Tipo B: International & Pensioni HB/FB", "active": True},
                {"name": "Tipo C: Corner Salute & Celiaci", "active": True}
            ],
            "fridges": [
                {"name": "Buffet Freddo Colazioni", "kind": "POS"},
                {"name": "Vetrina Yogurt/Salumi", "kind": "POS"},
                {"name": "Cella Carne +2°C", "kind": "POS"},
                {"name": "Cella Pesce 0°C", "kind": "POS"},
                {"name": "Congelatore Stoccaggio", "kind": "NEG"},
                {"name": "Abbattitore Cucina", "kind": "NEG"},
                {"name": "Frigo Linea Antipasti", "kind": "POS"},
                {"name": "Frigo Linea Primi/Sec.", "kind": "POS"}
            ]
        },
        {
            "id": "N05", "code": "05", "name": "CORPO BAR", "subtitle": "Caffetteria, Terrazza & Gelateria",
            "sub_zones": ["Banco Caffetteria", "Terrazza Aperitivi", "Cocktail Station"],
            "breakfast_profiles": [{"name": "Supporto Espresso & Cappuccini", "active": True}],
            "fridges": [
                {"name": "Banco Bar 1 (Latte)", "kind": "POS"},
                {"name": "Banco Bar 2 (Birre/Vini)", "kind": "POS"},
                {"name": "Vetrina Gelati -16°C", "kind": "NEG"},
                {"name": "Pozzetto Ghiaccio Bar", "kind": "NEG"}
            ]
        },
        {
            "id": "N06", "code": "06", "name": "SPIAGGIA & GAZEBO", "subtitle": "Stabilimento Balneare & Regia Eventi",
            "sub_zones": ["Gazebo Cerimonie", "Ombrelloni & Tende", "Chiosco Spiaggia"],
            "breakfast_profiles": [{"name": "Light Breakfast Tenda", "active": False}],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"},
                {"name": "Pozzetto Ghiaccio Gazebo", "kind": "NEG"}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "PARCHEGGIO & VIABILITÀ", "subtitle": "Controllo Accessi, Valet & Sposi",
            "sub_zones": ["Ingresso Principale", "Area Sosta Hotel", "Area Riservata Eventi"],
            "breakfast_profiles": [],
            "fridges": []
        }
    ]

    haccp_state = {}
    for n in nodes:
        for fr in n["fridges"]:
            key = f"{n['id']} || {fr['name']}"
            haccp_state[key] = {
                "node_id": n["id"], "fridge_name": fr["name"],
                "status": "PURPLE", "label": "ATTESA", "by": "-", "time": "--:--",
                "kind": fr["kind"], "slots": {"M": "-", "P": "-", "S": "-"}
            }

    haccp_state["N01 || Cella Basi +4°C"].update({"status": "GREEN", "label": "+3.6°C", "by": "Marco S.", "time": "07:30", "slots": {"M": "OK", "P": "-", "S": "-"}})
    haccp_state["N04 || Buffet Freddo Colazioni"].update({"status": "GREEN", "label": "+3.9°C", "by": "Jolly 01", "time": "07:15", "slots": {"M": "OK", "P": "-", "S": "-"}})
    haccp_state["N04 || Cella Pesce 0°C"].update({"status": "YELLOW", "label": "+6.2°C", "by": "Jolly 01", "time": "08:15", "slots": {"M": "WARN", "P": "-", "S": "-"}})

    return {
        "nodes": nodes,
        "haccp_state": haccp_state,
        # BRIEFING MATTUTINO IMPUTATO DAL RICEVIMENTO (100% AUTONOMO DAL GESTIONALE)
        "daily_briefing": {
            "updated_at": "07:30",
            "updated_by": "Ricevimento",
            "pax_colazioni": 112,
            "pax_hb": 38,
            "pax_fb": 14,
            "sala_colazioni": "Veranda 1 + Sala Interna",
            "note_cucina": "3 Celiaci (Cam. 104, 208) | 2 Senza Lattosio (Cam. 115)"
        },
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Giulia F.", "role": "Addetta Ricevimento", "index_cost": 95, "node_id": "N03", "sub_zone": "Front Desk & Briefing", "shift": "Mattina (07-15)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Maître Verande", "index_cost": 110, "node_id": "N04", "sub_zone": "Sala Colazioni", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node_id": "N05", "sub_zone": "Banco Caffetteria", "shift": "Mattina (07-15)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Regia Gazebo", "index_cost": 150, "node_id": "N06", "sub_zone": "Gazebo Cerimonie", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "08:10", "node_id": "N04", "from": "04. Ristorante (Sala Colazioni)", "item": "2 Vassoi Cornetti + Latte Senza Lattosio", "status": "In corso"}
        ],
        "events": [
            {"id": "EV1", "title": "Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "notes": "Aperitivo a buffet in spiaggia, 2 vegani tavolo sposi", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "notes": "Torta millefoglie da Pasticceria", "phase": "2. Aperitivo"},
            {"id": "EV3", "title": "Ristorante Pensioni & Carta", "zone": "Veranda 1 + Sala Interna", "pax": 85, "cake_time": "Continuo", "notes": "Servizio standard + Mezze Pensioni", "phase": "3. Servito"}
        ],
        "alarm_counter": 0
    }

store = get_shared_store()

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None
if "active_pin" not in st.session_state:
    st.session_state.active_pin = "9999"
if "last_sos_count" not in st.session_state:
    st.session_state.last_sos_count = len(store["sos_queue"])
if "last_alarm_counter" not in st.session_state:
    st.session_state.last_alarm_counter = store["alarm_counter"]

# --- INTESTAZIONE + BARRA DI COMANDO RAPIDA IN CIMA ---
bf = store["daily_briefing"]
st.markdown(f"""
<div class="top-bar">
    <div class="brand-title">SOVEREIGN KINETIC ARCHITECTURE <span>// BOSCHETTO PRO</span></div>
    <div class="brand-sub">PRESENZE OGGI ({bf['updated_at']}): {bf['pax_colazioni']} COLAZIONI · {bf['pax_hb']} HB · {bf['pax_fb']} FB</div>
</div>
""", unsafe_allow_html=True)

c_pin, c_btn, c_refresh, c_sonar = st.columns([1.3, 1.1, 1.1, 1.2])
with c_pin:
    new_pin = st.text_input("PIN ACCESSO", value=st.session_state.active_pin, label_visibility="collapsed", placeholder="PIN (9999 Dir. | 1003 Ricevimento | 1001 Staff)")
with c_btn:
    if st.button("CONFERMA PIN ↵", type="secondary", use_container_width=True) or (new_pin != st.session_state.active_pin):
        st.session_state.active_pin = new_pin.strip()
        st.session_state.selected_node_id = None
        play_tactical_sonar("ping")
        st.toast(f"Accesso confermato: PIN {st.session_state.active_pin}")
        st.rerun()
with c_refresh:
    if st.button("AGGIORNA LIVE ↻", type="secondary", use_container_width=True):
        st.toast("Plancia sincronizzata")
        st.rerun()
with c_sonar:
    sonar_active = st.toggle("SONAR AUDIO URGENZE", value=False)

pin_input = st.session_state.active_pin

if sonar_active:
    if len(store["sos_queue"]) > st.session_state.last_sos_count:
        play_tactical_sonar("ping")
    if store["alarm_counter"] > st.session_state.last_alarm_counter:
        play_tactical_sonar("alarm")

st.session_state.last_sos_count = len(store["sos_queue"])
st.session_state.last_alarm_counter = store["alarm_counter"]

# ==============================================================================
# VISTA 1: DIREZIONE (PIN 9999) + MASTER ARCHITECT (PIN 0000)
# ==============================================================================
if pin_input in ["9999", "0000"]:
    is_architect = (pin_input == "0000")

    if is_architect:
        st.info("MODALITÀ MASTER ARCHITECT ATTIVA (PIN 0000) — Modifica strutturale abilitata.")

    # DISPACCIO GIORNALIERO DAL RICEVIMENTO SEMPRE IN EVIDENZA
    st.markdown(
        f"<div class='dispatch-bar'>📋 <b>DISPACCIO RICEVIMENTO ({bf['updated_at']}):</b> "
        f"Colazioni: <b>{bf['pax_colazioni']} pax</b> ({bf['sala_colazioni']})  |  "
        f"Mezze Pensioni (HB): <b>{bf['pax_hb']}</b>  |  Complete (FB): <b>{bf['pax_fb']}</b>  |  "
        f"Allergie/Note: <b>{bf['note_cucina']}</b></div>",
        unsafe_allow_html=True
    )

    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='alert-bar-crit'>ALLARME CRITICO HACCP: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        st.markdown(f"<div class='alert-bar-sos'>LOGISTICA SOS ATTIVO ({len(store['sos_queue'])}) — {latest_sos['from']} [{latest_sos['time']}]: {latest_sos['item']}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA COSTELLAZIONE DEI NODI
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_ev = len(store["events"])
        tot_pts = sum(f["index_cost"] for f in store["figurine"])
        tot_pax = sum(e["pax"] for e in store["events"])

        st.markdown(f"""
        <div class="kpi-bar">
            <div class="kpi-box"><div class="kpi-lbl">Colazioni & Pensioni</div><div class="kpi-num">{bf['pax_colazioni']} COL · {bf['pax_hb']} HB</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Nodi Struttura</div><div class="kpi-num">07 REPARTI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Brigata Attiva</div><div class="kpi-num">{tot_fig} UNITA ({tot_pts} PT)</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Coda Logistica</div><div class="kpi-num">{tot_sos} SOS APERTI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Agenda Eventi</div><div class="kpi-num">{tot_ev} LIVE ({tot_pax} PAX)</div></div>
        </div>
        """, unsafe_allow_html=True)

        row1 = st.columns(4)
        row2 = st.columns(4)
        grid_cols = row1 + row2

        for idx, node in enumerate(store["nodes"]):
            nid = node["id"]
            n_staff = len([f for f in store["figurine"] if f["node_id"] == nid])
            n_sos = len([s for s in store["sos_queue"] if s["node_id"] == nid])
            n_fridges = [v for v in store["haccp_state"].values() if v["node_id"] == nid]

            n_ok = sum(1 for f in n_fridges if f["status"] == "GREEN")
            n_anom = sum(1 for f in n_fridges if f["status"] in ["YELLOW", "RED"])

            if not n_fridges:
                haccp_summary = "HACCP: N/A"
            elif n_anom > 0:
                haccp_summary = f"HACCP: {n_anom} ANOMALIA"
            else:
                haccp_summary = f"HACCP: {n_ok}/{len(n_fridges)} OK"

            sos_summary = f"SOS: {n_sos}" if n_sos > 0 else "LOGISTICA: OK"

            tile_label = (
                f"{node['code']} // {node['name']}\n"
                f"{node['subtitle']}\n"
                f"STAFF: {n_staff}   |   {haccp_summary}   |   {sos_summary}"
            )

            with grid_cols[idx]:
                if st.button(tile_label, key=f"tile_{nid}", type="primary", use_container_width=True):
                    st.session_state.selected_node_id = nid
                    st.rerun()

        with grid_cols[7]:
            hub_label = (
                f"08 // AGENDA EVENTI & BRIGATA\n"
                f"Crea Eventi, Gestisci Dipendenti & PIN\n"
                f"EVENTI: {tot_ev} ({tot_pax} PAX)   |   STAFF: {tot_fig}"
            )
            if st.button(hub_label, key="tile_HUB", type="primary", use_container_width=True):
                st.session_state.selected_node_id = "HUB_VAULT"
                st.rerun()

    # --------------------------------------------------------------------------
    # VISTA 08: AGENDA EVENTI, GESTIONE DIPENDENTI/PIN & CASSAFORTE
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "HUB_VAULT":
        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown("### 08 // AGENDA EVENTI, ANAGRAFICA BRIGATA & ARCHIVIO")

        tab_ev, tab_staff, tab_vault = st.tabs([
            "📅 1. AGENDA EVENTI & CERIMONIE",
            "👥 2. GESTIONE DIPENDENTI & PIN (AUTONOMIA)",
            "🔐 3. CHIUSURA & ARCHIVIO NOTTURNO"
        ])

        with tab_ev:
            st.markdown("##### EVENTI E SERVIZI ATTIVI OGGI")
            phase_options = [
                "1. Accoglienza / Rito",
                "2. Aperitivo",
                "3. Servito",
                "4. Alert Pasticceria: Fuori Torta!",
                "5. Open Bar & Musica"
            ]
            for idx, ev in enumerate(store["events"]):
                with st.expander(f"{ev['title']} — {ev['zone']} ({ev['pax']} pax | Torta: {ev['cake_time']})", expanded=True):
                    st.caption(f"Note Dispaccio: {ev.get('notes', '-')}")
                    c_e1, c_e2 = st.columns([3, 1])
                    cur_i = phase_options.index(ev["phase"]) if ev["phase"] in phase_options else 0
                    new_ph = c_e1.selectbox("Stato Avanzamento Live", phase_options, index=cur_i, key=f"ev_{ev['id']}")
                    if new_ph != ev["phase"]:
                        ev["phase"] = new_ph
                        st.rerun()
                    if c_e2.button("Elimina Evento", key=f"del_ev_{ev['id']}"):
                        store["events"].pop(idx)
                        st.rerun()

            st.divider()
            st.markdown("##### ➕ INSERISCI NUOVO EVENTO IN AGENDA")
            ce1, ce2, ce3, ce4 = st.columns(4)
            ne_title = ce1.text_input("Titolo Evento (es. Matrimonio Neri)")
            ne_zone = ce2.selectbox("Location / Veranda", ["Gazebo -> Veranda Circolare", "Veranda Grande", "Veranda 1", "Veranda 2", "Sala Interna", "Spiaggia & Chiosco"])
            ne_pax = ce3.number_input("Numero Ospiti (Pax)", min_value=1, value=60, step=5)
            ne_cake = ce4.text_input("Orario Uscita Torta", value="22:45")
            ne_notes = st.text_input("Note Operative per Cucina, Sala e Pasticceria (allergie, menu, allestimento)")
            if st.button("SALVA NUOVO EVENTO IN AGENDA", type="secondary"):
                if ne_title:
                    store["events"].append({
                        "id": f"EV{int(datetime.now().timestamp())}",
                        "title": ne_title, "zone": ne_zone, "pax": ne_pax,
                        "cake_time": ne_cake, "notes": ne_notes, "phase": "1. Accoglienza / Rito"
                    })
                    st.toast("Evento aggiunto in Agenda!")
                    st.rerun()

        with tab_staff:
            st.markdown("##### ➕ CREA NUOVO OPERATORE / ASSEGNA PIN")
            st.caption("La Direzione o il Ricevimento possono inserire qui in piena autonomia nuovi dipendenti o extra del weekend.")
            cs1, cs2, cs3 = st.columns(3)
            ns_nick = cs1.text_input("Nome / Nickname (es. Matteo B.)")
            ns_role = cs2.text_input("Mansione (es. Cameriere Veranda / Extra)")
            ns_pin = cs3.text_input("Assegna PIN a 4 cifre (es. 1007)")

            cs4, cs5, cs6 = st.columns(3)
            node_map = {f"{n['code']} - {n['name']}": n for n in store["nodes"]}
            ns_node_label = cs4.selectbox("Reparto di Destinazione", list(node_map.keys()))
            chosen_node = node_map[ns_node_label]
            ns_sub = cs5.selectbox("Sottozona", chosen_node["sub_zones"])
            ns_shift = cs6.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)"])

            if st.button("AGGIUNGI OPERATORE ALLA BRIGATA", type="secondary"):
                if ns_nick and ns_pin:
                    store["figurine"].append({
                        "pin": ns_pin.strip(), "nick": ns_nick.strip(), "role": ns_role.strip() or "Operatore",
                        "index_cost": 100, "node_id": chosen_node["id"], "sub_zone": ns_sub, "shift": ns_shift
                    })
                    st.toast(f"Operatore {ns_nick} (PIN {ns_pin}) attivato!")
                    st.rerun()

            st.divider()
            st.markdown("##### ELENCO COMPLETO BRIGATA E PIN ATTIVI")
            for idx_f, f in enumerate(store["figurine"]):
                cf1, cf2 = st.columns([4, 1])
                cf1.markdown(f"- **PIN `{f['pin']}`** — **{f['nick']}** ({f['role']})  |  Reparto: `{f['node_id']}` ({f['sub_zone']})  |  `{f['shift']}`")
                if cf2.button("Rimuovi", key=f"rm_fig_{f['pin']}_{idx_f}"):
                    store["figurine"].pop(idx_f)
                    st.rerun()

        with tab_vault:
            st.markdown("##### CHIUSURA GIORNATA & SCARICO REGISTRO")
            c_v1, c_v2 = st.columns(2)
            with c_v1:
                st.download_button(
                    "SCARICA VAULT CRIPTATO 03:00 AM (.JSON)",
                    data=json.dumps({"briefing": store["daily_briefing"], "haccp": store["haccp_state"], "staff": store["figurine"], "events": store["events"]}, indent=2),
                    file_name=f"SKA_BOSCHETTO_PRO_{datetime.now().strftime('%Y%m%d')}.json",
                    use_container_width=True
                )
            with c_v2:
                if st.button("RESET NUOVO GIRO HACCP (RIPORTA IN ATTESA)", type="secondary", use_container_width=True):
                    for k in store["haccp_state"]:
                        store["haccp_state"][k].update({"status": "PURPLE", "label": "ATTESA", "by": "-", "time": "--:--"})
                    st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 1: INTERNO DEL SINGOLO REPARTO (N01..N07)
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown(f"### {node['code']} // {node['name']} — {node['subtitle']}")
        st.divider()

        # SE SIAMO NEL NODO 03 (RICEVIMENTO), MOSTRA IL MODULO DI IMPUTAZIONE MATTUTINA!
        if nid == "N03":
            st.markdown("#### 📋 IMPUTAZIONE MATTUTINA PRESENZE, COLAZIONI & DISPACCI (RICEVIMENTO)")
            st.caption("Inserisci qui i numeri del giorno letti dal foglio arrivi/presenze. Si aggiorneranno istantaneamente per Cucina, Sala e Pasticceria.")
            b1, b2, b3, b4 = st.columns(4)
            new_col = b1.number_input("Colazioni Totali Oggi", min_value=0, value=bf["pax_colazioni"], step=1)
            new_hb = b2.number_input("Mezze Pensioni (HB)", min_value=0, value=bf["pax_hb"], step=1)
            new_fb = b3.number_input("Pensioni Complete (FB)", min_value=0, value=bf["pax_fb"], step=1)
            new_sala = b4.selectbox("Sala Colazioni Attiva", ["Veranda 1 + Sala Interna", "Solo Veranda 1", "Solo Sala Interna", "Veranda Grande", "Gazebo Spiaggia"])
            new_note = st.text_input("Segnalazioni Allergie / Celiaci / Intolleranze / Note Reparti:", value=bf["note_cucina"])

            if st.button("PUBBLICA DISPACCI DEL GIORNO A TUTTI I REPARTI", type="secondary", use_container_width=True):
                bf.update({
                    "updated_at": datetime.now().strftime("%H:%M"),
                    "updated_by": "Ricevimento / Direzione",
                    "pax_colazioni": new_col, "pax_hb": new_hb, "pax_fb": new_fb,
                    "sala_colazioni": new_sala, "note_cucina": new_note
                })
                st.toast("Dispaccio giornaliero pubblicato a tutti i reparti!")
                st.rerun()
            st.divider()

        col_haccp, col_ops = st.columns([1.6, 1.4])

        with col_haccp:
            st.markdown("##### MATRICE CONTROLLO TEMPERATURE HACCP (3 GIRI: M · P · S)")
            st.caption("VIOLA: In Attesa  |  VERDE: Conforme  |  GIALLO: Pre-Allarme  |  ROSSO: Critico/Guasto")
            node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
            if not node_fridges:
                st.caption("Nessuna unità frigorifera censita in questo reparto.")
            else:
                tiles_html = "<div class='haccp-grid'>"
                for st_data in node_fridges:
                    css_class = {"PURPLE": "tile-purple", "GREEN": "tile-green", "YELLOW": "tile-yellow", "RED": "tile-red"}[st_data["status"]]
                    slots = st_data["slots"]
                    tiles_html += (
                        f"<div class='haccp-tile {css_class}'>"
                        f"<div class='tile-title'>{st_data['fridge_name']}</div>"
                        f"<div class='tile-val'>{st_data['label']}</div>"
                        f"<div class='tile-slots'><span>M:{slots['M']}</span><span>P:{slots['P']}</span><span>S:{slots['S']}</span></div>"
                        f"<div class='tile-slots' style='border:none; padding-top:2px;'><span>{st_data['time']}</span><span>{st_data['by']}</span></div>"
                        f"</div>"
                    )
                tiles_html += "</div>"
                st.markdown(tiles_html, unsafe_allow_html=True)

            if is_architect:
                with st.expander("[ARCHITETTO] Aggiungi Unità Frigorifera"):
                    nf_name = st.text_input("Denominazione Unità")
                    nf_kind = st.selectbox("Regime Termico", ["POS (+2°C / +6°C)", "NEG (-18°C)"])
                    if st.button("Inserisci nel Reparto", type="secondary"):
                        if nf_name:
                            k_code = "POS" if "POS" in nf_kind else "NEG"
                            node["fridges"].append({"name": nf_name, "kind": k_code})
                            store["haccp_state"][f"{nid} || {nf_name}"] = {
                                "node_id": nid, "fridge_name": nf_name, "status": "PURPLE",
                                "label": "ATTESA", "by": "-", "time": "--:--",
                                "kind": k_code, "slots": {"M": "-", "P": "-", "S": "-"}
                            }
                            st.rerun()

        with col_ops:
            st.markdown("##### SOTTOZONE & LINEE COLAZIONE")
            st.pills("Sottozone Reparto:", node["sub_zones"], default=node["sub_zones"][0] if node["sub_zones"] else None)
            if node["breakfast_profiles"]:
                for idx_b, bp in enumerate(node["breakfast_profiles"]):
                    bp["active"] = st.checkbox(f"{bp['name']}", value=bp["active"], key=f"bf_{nid}_{idx_b}")

            st.divider()
            st.markdown("##### PERSONALE ASSEGNATO & LOGISTICA")
            for f in [f for f in store["figurine"] if f["node_id"] == nid]:
                st.markdown(f"- **{f['nick']}** ({f['role']}) — Zona: `{f['sub_zone']}` | Turno: `{f['shift']}` | PIN: `{f['pin']}`")

            with st.expander("Sposta Operatore in questo Reparto"):
                pick_fig = st.selectbox("Operatore", [f["nick"] for f in store["figurine"]])
                pick_sub = st.selectbox("Sottozona", node["sub_zones"])
                pick_sh = st.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)"])
                if st.button("Conferma Assegnazione", type="secondary"):
                    for f in store["figurine"]:
                        if f["nick"] == pick_fig:
                            f["node_id"] = nid
                            f["sub_zone"] = pick_sub
                            f["shift"] = pick_sh
                    st.rerun()

            node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]
            if node_sos:
                st.markdown("##### RICHIESTE SOS ATTIVE")
                for req in node_sos:
                    st.warning(f"{req['time']} — {req['item']}")
                if st.button("Segna Richieste SOS come Evase", type="secondary", use_container_width=True):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()

# ==============================================================================
# VISTA 2: TERMINALE OPERATORE & RICEVIMENTO (PIN 1001, 1003, 1004...)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error(f"PIN '{pin_input}' non riconosciuto. Inserisci 9999 (Direzione) o un PIN Operatore attivo.")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.success(f"OPERATORE ATTIVO: {user['nick']} ({user['role']}) — Reparto: {user_node['name']}")

        # OGNI OPERATORE VEDE SUBITO IN CIMA IL DISPACCIO DEL RICEVIMENTO E GLI EVENTI!
        st.markdown(
            f"<div class='dispatch-bar'>📋 <b>BRIEFING OGGI ({bf['updated_at']}):</b> "
            f"Colazioni: <b>{bf['pax_colazioni']} pax</b> ({bf['sala_colazioni']}) | "
            f"HB: <b>{bf['pax_hb']}</b> | FB: <b>{bf['pax_fb']}</b><br>"
            f"⚠️ <b>Note/Allergie:</b> {bf['note_cucina']}</div>",
            unsafe_allow_html=True
        )

        with st.expander("📅 Vedi Agenda Eventi & Orari Torte di Oggi", expanded=False):
            for ev in store["events"]:
                st.markdown(f"- **{ev['title']}** ({ev['zone']} · `{ev['pax']} pax`) — **{ev['phase']}** | Torta: `{ev['cake_time']}` | *{ev.get('notes', '')}*")

        # SE L'OPERATORE È DEL RICEVIMENTO (N03), PUÒ IMPUTARE I NUMERI DIRETTAMENTE DAL SUO PIN!
        if user["node_id"] == "N03":
            st.markdown("##### 📋 IMPUTAZIONE PRESENZE & DISPACCI MATTUTINI (FRONT DESK)")
            b1, b2, b3 = st.columns(3)
            u_col = b1.number_input("Colazioni Oggi", min_value=0, value=bf["pax_colazioni"])
            u_hb = b2.number_input("Mezze Pensioni (HB)", min_value=0, value=bf["pax_hb"])
            u_fb = b3.number_input("Pensioni Complete (FB)", min_value=0, value=bf["pax_fb"])
            u_sala = st.selectbox("Sala Colazioni", ["Veranda 1 + Sala Interna", "Solo Veranda 1", "Solo Sala Interna", "Veranda Grande"])
            u_note = st.text_input("Allergie / Celiaci / Note per Cucina e Pasticceria:", value=bf["note_cucina"])
            if st.button("AGGIORNA E INVIA A TUTTI I REPARTI", type="secondary", use_container_width=True):
                bf.update({
                    "updated_at": datetime.now().strftime("%H:%M"),
                    "updated_by": user["nick"],
                    "pax_colazioni": u_col, "pax_hb": u_hb, "pax_fb": u_fb,
                    "sala_colazioni": u_sala, "note_cucina": u_note
                })
                st.toast("Numeri del giorno inviati a tutti i reparti!")
                st.rerun()
            st.divider()

        st.markdown("##### 1. REGISTRAZIONE TEMPERATURA HACCP")
        round_sel = st.radio("Giro di Controllo:", ["M (Mattina)", "P (Pomeriggio)", "S (Sera)"], horizontal=True)
        round_code = round_sel[0]

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        if my_fridges:
            sel_key = st.selectbox("Seleziona Unità Frigorifera", my_fridges, format_func=lambda x: x.split(" || ")[1])
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura Rilevata (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("Segnala Anomalia Blocco / Guasto Meccanico")

            if st.button("FIRMA E REGISTRA LETTURA", type="secondary", use_container_width=True):
                status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                slot_txt = {"GREEN": "OK", "YELLOW": "WARN", "RED": "CRIT"}[status_color]
                fr_info["slots"][round_code] = slot_txt
                fr_info.update({"status": status_color, "label": label_text, "by": user["nick"], "time": datetime.now().strftime("%H:%M")})
                if status_color in ["RED", "YELLOW"]:
                    store["alarm_counter"] += 1
                st.toast(f"Temperatura {label_text} registrata!")
                st.success(f"Registrato ({round_code}): {label_text}")

        st.divider()
        st.markdown("##### 2. RICHIESTA URGENTE MAGAZZINO (SOS)")
        sos_item = st.text_input("Articolo / Fornitura richiesta:")
        if st.button("INVIA RICHIESTA AL MAGAZZINO", type="secondary", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']}. {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.toast("SOS inviato al Magazzino!")
                st.success("Richiesta trasmessa in Direzione e al Magazzino.")
