import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

st.set_page_config(
    page_title="S.K.A. // BOSCHETTO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS RESPONSIVE: DESKTOP (4x2) + SMARTPHONE COMPACT (2x4) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@500;700&family=Plus+Jakarta+Sans:wght@400;600;700&family=Space+Grotesk:wght@600;700&display=swap');

/* TEMA SCURO NATIVO AERONAUTICO */
.stApp {
    background-color: #060b16 !important;
    color: #f1f5f9 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.block-container {
    padding-top: 1.8rem !important;
    padding-bottom: 1.5rem !important;
    max-width: 1440px !important;
}

/* HEADER ULTRA-COMPATTO */
.ska-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 8px;
    margin-bottom: 10px;
}
.ska-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f8fafc;
    letter-spacing: -0.02em;
}
.ska-title span {
    color: #38bdf8;
}
.ska-sub {
    font-size: 0.78rem;
    color: #94a3b8;
}

/* BARRA KPI IN UNA SOLA RIGA SOTTILE (ZERO SCORRIMENTO SU TELEFONO) */
.kpi-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 8px;
    margin-bottom: 12px;
}
.kpi-pill {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 8px;
    padding: 6px 10px;
    display: flex;
    flex-direction: column;
}
.kpi-label { font-size: 0.65rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.04em; }
.kpi-val { font-family: 'Space Grotesk', sans-serif; font-size: 0.98rem; font-weight: 700; color: #38bdf8; }

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.85); }
    70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
@keyframes pulse-amber {
    0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
    70% { box-shadow: 0 0 0 8px rgba(245, 158, 11, 0); }
    100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}

.tactical-banner-sos {
    background: linear-gradient(90deg, #78350f 0%, #b45309 100%);
    color: #fef3c7; padding: 8px 14px; border-radius: 8px;
    border-left: 5px solid #fbbf24; font-weight: 600; font-size: 0.82rem;
    margin-bottom: 10px; animation: pulse-amber 2s infinite;
}
.tactical-banner-danger {
    background: linear-gradient(90deg, #7f1d1d 0%, #dc2626 100%);
    color: #fef2f2; padding: 8px 14px; border-radius: 8px;
    border-left: 5px solid #f87171; font-weight: 600; font-size: 0.82rem;
    margin-bottom: 10px; animation: pulse-red 1.5s infinite;
}
.architect-badge {
    background: linear-gradient(90deg, #311042 0%, #701a75 100%);
    color: #f5d0fe; padding: 8px 14px; border-radius: 8px;
    border-left: 4px solid #e879f9; font-weight: 600; font-size: 0.8rem; margin-bottom: 10px;
}

/* QUADRATI COSTELLAZIONE (DESKTOP) */
div.stButton > button[kind="primary"] {
    background: linear-gradient(155deg, #0d1526 0%, #16243d 100%) !important;
    border: 1px solid #38bdf840 !important;
    border-radius: 12px !important;
    height: 148px !important;
    min-height: 148px !important;
    max-height: 148px !important;
    width: 100% !important;
    padding: 14px 16px !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.16s ease-in-out !important;
    color: #f8fafc !important;
}
div.stButton > button[kind="primary"]:hover {
    border: 1.5px solid #38bdf8 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 22px rgba(56, 189, 248, 0.22) !important;
}
div.stButton > button[kind="primary"] p {
    white-space: pre-line !important;
    line-height: 1.38 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    margin: 0 !important;
}

/* QUADRETTI INTERNI HACCP */
.haccp-grid { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; margin-bottom: 12px; }
.haccp-tile {
    width: 142px; height: 86px; border-radius: 8px; padding: 7px 9px;
    display: flex; flex-direction: column; justify-content: space-between;
    color: white; box-shadow: 0 3px 8px rgba(0,0,0,0.4);
}
.tile-purple { background: #4c1d95; border: 1.5px solid #a855f7; }
.tile-green  { background: #064e3b; border: 1.5px solid #10b981; }
.tile-yellow { background: #713f12; border: 1.5px solid #eab308; }
.tile-red    { background: #7f1d1d; border: 1.5px solid #ef4444; animation: pulse-red 1.5s infinite; }
.tile-title  { font-size: 0.70rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tile-val    { font-family: 'JetBrains Mono', monospace; font-size: 0.98rem; font-weight: 700; }
.tile-slots  { font-family: 'JetBrains Mono', monospace; font-size: 0.62rem; font-weight: 700; background: rgba(0,0,0,0.35); padding: 2px 5px; border-radius: 4px; display: flex; justify-content: space-between; }
.tile-meta   { font-size: 0.60rem; opacity: 0.85; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* ==========================================================================
   OTTIMIZZAZIONE CHIRURGICA SMARTPHONE (Affianca 2 Quadrati per riga!)
   ========================================================================== */
@media (max-width: 768px) {
    .block-container {
        padding-top: 1.2rem !important;
        padding-left: 0.6rem !important;
        padding-right: 0.6rem !important;
    }
    .ska-title { font-size: 1.02rem !important; }
    .ska-sub { font-size: 0.68rem !important; }
    .kpi-strip {
        grid-template-columns: repeat(2, 1fr);
        gap: 6px;
    }
    .kpi-pill { padding: 5px 8px; }
    .kpi-val { font-size: 0.85rem; }

    /* Forza le colonne di Streamlit a stare a 2 a 2 affiancate su telefono */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 8px !important;
    }
    div[data-testid="column"] {
        width: 100% !important;
        min-width: 0 !important;
    }
    div.stButton > button[kind="primary"] {
        height: 116px !important;
        min-height: 116px !important;
        max-height: 116px !important;
        padding: 9px 10px !important;
        border-radius: 10px !important;
    }
    div.stButton > button[kind="primary"] p {
        font-size: 0.72rem !important;
        line-height: 1.26 !important;
    }
    .haccp-tile {
        width: 47% !important;
        height: 80px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# --- SINTETIZZATORE SONAR TATTICO ---
def play_tactical_sonar(mode="ping"):
    if mode == "ping":
        js_code = """
        <script>
        (function() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator(); const gain = ctx.createGain();
            osc.type = 'sine'; osc.frequency.setValueAtTime(880, ctx.currentTime);
            gain.gain.setValueAtTime(0.25, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + 0.35);
        })();
        </script>
        """
    else:
        js_code = """
        <script>
        (function() {
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            [0, 0.22].forEach(offset => {
                const osc = ctx.createOscillator(); const gain = ctx.createGain();
                osc.type = 'triangle'; osc.frequency.setValueAtTime(220, ctx.currentTime + offset);
                gain.gain.setValueAtTime(0.35, ctx.currentTime + offset);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + offset + 0.16);
                osc.connect(gain); gain.connect(ctx.destination);
                osc.start(ctx.currentTime + offset); osc.stop(ctx.currentTime + offset + 0.16);
            });
        })();
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

# --- DNA ARCHITETTURALE CERTIFICATO BEMASK ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N01", "code": "01", "name": "CASA MADRE", "subtitle": "Pasticceria & Direzione",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni & Sfogliatura", "Uffici Direzione"],
            "breakfast_profiles": [
                {"name": "Linea Lievitati Standard (B&B)", "active": True},
                {"name": "Pasticceria Secca & Torte Credenza (HB/FB)", "active": True},
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
            "id": "N02", "code": "02", "name": "CORPO ALBERGO", "subtitle": "Camere & Housekeeping",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria & Carrelli"],
            "breakfast_profiles": [
                {"name": "Room Service / Vassoi Camera", "active": True},
                {"name": "Early Breakfast Box (Partenze Alba)", "active": False}
            ],
            "fridges": [{"name": "Frigo Office Piani", "kind": "POS"}]
        },
        {
            "id": "N03", "code": "03", "name": "RICEVIMENTO & HUB", "subtitle": "Front Office & Magazzino",
            "sub_zones": ["Front Desk & Accoglienza", "Magazzino Centrale", "Baia Scarico Fornitori"],
            "breakfast_profiles": [],
            "fridges": [
                {"name": "Cella Latticini/Salumi", "kind": "POS"},
                {"name": "Cella Ortofrutta +6°C", "kind": "POS"},
                {"name": "Cella Scorte Bevande", "kind": "POS"}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "RISTORANTE & SALE", "subtitle": "Cucina, Colazioni & 5 Verande",
            "sub_zones": ["Sala Colazioni (Mattina)", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare", "Cucina Centrale"],
            "breakfast_profiles": [
                {"name": "Tipo A: Buffet Continentale / B&B", "active": True},
                {"name": "Tipo B: International & Pensioni HB/FB", "active": True},
                {"name": "Tipo C: Corner Salute, Celiaci & Bimbi", "active": True}
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
            "id": "N05", "code": "05", "name": "CORPO BAR", "subtitle": "Caffetteria & Gelateria",
            "sub_zones": ["Banco Caffetteria Mattina", "Terrazza Aperitivi", "Postazione Cocktail Sera"],
            "breakfast_profiles": [
                {"name": "Supporto Espresso & Cappuccini", "active": True}
            ],
            "fridges": [
                {"name": "Banco Bar 1 (Latte)", "kind": "POS"},
                {"name": "Banco Bar 2 (Birre/Vini)", "kind": "POS"},
                {"name": "Vetrina Gelati -16°C", "kind": "NEG"},
                {"name": "Pozzetto Ghiaccio Bar", "kind": "NEG"}
            ]
        },
        {
            "id": "N06", "code": "06", "name": "SPIAGGIA & GAZEBO", "subtitle": "Stabilimento & Cerimonie",
            "sub_zones": ["Gazebo Rito & Taglio Torta", "Ombrelloni & Tende", "Chiosco/Point Spiaggia"],
            "breakfast_profiles": [
                {"name": "Light Breakfast sotto Tenda", "active": False}
            ],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"},
                {"name": "Pozzetto Ghiaccio Gazebo", "kind": "NEG"}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "PARCHEGGIO & FLUSSI", "subtitle": "Accessi, Valet & Sposi",
            "sub_zones": ["Ingresso Principale", "Area Sosta Ospiti Hotel", "Area Riservata Fornitori/Sposi"],
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
                "status": "PURPLE", "label": "In Attesa", "by": "-", "time": "--:--",
                "kind": fr["kind"], "slots": {"M": "⚪", "P": "⚪", "S": "⚪"}
            }

    haccp_state["N01 || Cella Basi +4°C"].update({"status": "GREEN", "label": "+3.6°C", "by": "Marco S.", "time": "07:30", "slots": {"M": "🟢", "P": "⚪", "S": "⚪"}})
    haccp_state["N04 || Buffet Freddo Colazioni"].update({"status": "GREEN", "label": "+3.9°C", "by": "Jolly 01", "time": "07:15", "slots": {"M": "🟢", "P": "⚪", "S": "⚪"}})
    haccp_state["N04 || Cella Pesce 0°C"].update({"status": "YELLOW", "label": "+6.2°C", "by": "Jolly 01", "time": "08:15", "slots": {"M": "🟡", "P": "⚪", "S": "⚪"}})

    return {
        "nodes": nodes,
        "haccp_state": haccp_state,
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Luca M.", "role": "Runner Magazzino", "index_cost": 85, "node_id": "N03", "sub_zone": "Magazzino Centrale", "shift": "Pranzo/Pom (12-20)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Maître / Resp. Verande", "index_cost": 110, "node_id": "N04", "sub_zone": "Sala Colazioni (Mattina)", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node_id": "N05", "sub_zone": "Banco Caffetteria Mattina", "shift": "Mattina (07-15)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Regia Gazebo", "index_cost": 150, "node_id": "N06", "sub_zone": "Gazebo Rito & Taglio Torta", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "08:10", "node_id": "N04", "from": "04. Ristorante", "item": "2 Vassoi Cornetti + Latte S.L.", "status": "In corso"}
        ],
        "events": [
            {"id": "EV1", "title": "💍 Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "🥂 50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "phase": "2. Aperitivo"},
            {"id": "EV3", "title": "🍽️ Ristorante Pensioni & Carta", "zone": "Veranda 1 + Sala Interna", "pax": 85, "cake_time": "Continuo", "phase": "3. Servito"}
        ],
        "alarm_counter": 0
    }

store = get_shared_store()

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None
if "last_sos_count" not in st.session_state:
    st.session_state.last_sos_count = len(store["sos_queue"])
if "last_alarm_counter" not in st.session_state:
    st.session_state.last_alarm_counter = store["alarm_counter"]

# --- BARRA LATERALE (CHIUSA DI DEFAULT SU TELEFONO) ---
with st.sidebar:
    st.markdown("### 🏛️ S.K.A. // BOSCHETTO PRO")
    pin_input = st.text_input("PIN Operativo", value="9999", help="9999 = Direzione | 1001 = Dipendente")
    if st.button("🔄 Aggiorna Stato Live", use_container_width=True):
        st.rerun()

    st.divider()
    st.caption("🔊 **SONAR TATTICO**")
    sonar_active = st.toggle("Attiva Sonar Urgenze", value=False)
    if sonar_active:
        c_s1, c_s2 = st.columns(2)
        if c_s1.button("🔔 Ping"): play_tactical_sonar("ping")
        if c_s2.button("⚠️ Allarme"): play_tactical_sonar("alarm")

    st.divider()
    st.caption("🔌 **PONTI ECOSISTEMA BEMASK**")
    hook_sz = st.toggle("Link: Sovereign Zero (Hotel)", value=True)
    hook_lz = st.toggle("Link: LAZERS (F&B Engine)", value=True)
    if hook_sz:
        st.caption("🏨 **Sovereign Zero:** 112 Pax in Casa")
    if hook_lz:
        st.caption("🎯 **LAZERS:** 3 Linee Colazione | 38 HB | 3 Celiaci")

# --- CONTROLLO SONAR AUTOMATICO ---
if sonar_active:
    if len(store["sos_queue"]) > st.session_state.last_sos_count:
        play_tactical_sonar("ping")
    if store["alarm_counter"] > st.session_state.last_alarm_counter:
        play_tactical_sonar("alarm")

st.session_state.last_sos_count = len(store["sos_queue"])
st.session_state.last_alarm_counter = store["alarm_counter"]

# ==============================================================================
# VISTA 1: DIREZIONE (PIN 9999) + MODALITÀ SEGRETA ARCHITETTO BEMASK (PIN 0000)
# ==============================================================================
if pin_input in ["9999", "0000"]:
    is_architect = (pin_input == "0000")

    if is_architect:
        st.markdown("<div class='architect-badge'>🛠️ MODALITÀ MASTER ARCHITECT BEMASK (PIN 0000)</div>", unsafe_allow_html=True)

    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='tactical-banner-danger'>🚨 ALLARME HACCP: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        st.markdown(f"<div class='tactical-banner-sos'>⚡ SOS ({len(store['sos_queue'])}) — {latest_sos['from']} ({latest_sos['time']}): \"{latest_sos['item']}\"</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA COSTELLAZIONE PRINCIPALE (COMPATTA SU MOBILE 2x4, AMPIA SU PC 4x2)
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_ev = len(store["events"])
        tot_pts = sum(f["index_cost"] for f in store["figurine"])
        tot_pax = sum(e["pax"] for e in store["events"])

        st.markdown(f"""
        <div class="ska-header">
            <div>
                <div class="ska-title">🌌 S.K.A. // <span>BOSCHETTO PRO</span></div>
                <div class="ska-sub">Sovereign Kinetic Architecture — Tocca un quadrato per aprire il reparto</div>
            </div>
        </div>
        <div class="kpi-strip">
            <div class="kpi-pill"><span class="kpi-label">🏛️ Nodi</span><span class="kpi-val">7 Blocchi</span></div>
            <div class="kpi-pill"><span class="kpi-label">👥 Brigata</span><span class="kpi-val">{tot_fig} Unità ({tot_pts}pt)</span></div>
            <div class="kpi-pill"><span class="kpi-label">🚨 SOS Hub</span><span class="kpi-val">{tot_sos} Attivi</span></div>
            <div class="kpi-pill"><span class="kpi-label">🥂 Eventi</span><span class="kpi-val">{tot_ev} Live ({tot_pax}p)</span></div>
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
            active_bf = sum(1 for b in node["breakfast_profiles"] if b["active"])

            n_green = sum(1 for f in n_fridges if f["status"] == "GREEN")
            n_purple = sum(1 for f in n_fridges if f["status"] == "PURPLE")
            n_yellow = sum(1 for f in n_fridges if f["status"] == "YELLOW")
            n_red = sum(1 for f in n_fridges if f["status"] == "RED")

            fridge_txt = f"🟢{n_green} 🟣{n_purple} 🟡{n_yellow} 🔴{n_red}" if n_fridges else "❄️ —"
            sos_txt = f"🚨{n_sos}" if n_sos > 0 else "✔️OK"

            tile_label = (
                f"[{node['code']}] {node['name']}\n"
                f"{node['subtitle']}\n"
                f"🧭 {len(node['sub_zones'])} Zone · 🥐 {active_bf} Colaz.\n"
                f"👥{n_staff} · {fridge_txt} · {sos_txt}"
            )

            with grid_cols[idx]:
                if st.button(tile_label, key=f"tile_{nid}", type="primary", use_container_width=True):
                    st.session_state.selected_node_id = nid
                    st.rerun()

        with grid_cols[7]:
            hub_label = (
                f"[08] EVENTI & VAULT\n"
                f"Regia & Cassaforte 03 AM\n"
                f"🥂 {tot_ev} Eventi ({tot_pax} Pax)\n"
                f"🔐 Zero-Trace Attivo"
            )
            if st.button(hub_label, key="tile_HUB", type="primary", use_container_width=True):
                st.session_state.selected_node_id = "HUB_VAULT"
                st.rerun()

    # --------------------------------------------------------------------------
    # VISTA 8° QUADRATO: REGIA MULTI-EVENTO & CASSAFORTE 03:00 AM
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "HUB_VAULT":
        if st.button("⬅️ Torna alla Costellazione"):
            st.session_state.selected_node_id = None
            st.rerun()
        st.markdown("### 🥂 [08] REGIA MULTI-EVENTO & CASSAFORTE 03:00 AM")

        phase_options = [
            "1. Accoglienza / Rito",
            "2. Aperitivo",
            "3. Servito",
            "4. Alert Pasticceria: Fuori Torta!",
            "5. Open Bar & Musica"
        ]
        for ev in store["events"]:
            with st.expander(f"{ev['title']} — {ev['zone']} ({ev['pax']} pax | 🎂 {ev['cake_time']})", expanded=True):
                cur_i = phase_options.index(ev["phase"]) if ev["phase"] in phase_options else 0
                new_ph = st.selectbox("Fase Live", phase_options, index=cur_i, key=f"ev_{ev['id']}")
                if new_ph != ev["phase"]:
                    ev["phase"] = new_ph
                    st.rerun()

        st.divider()
        st.download_button(
            "📲 Scarica Vault Criptato 03:00 AM (JSON)",
            data=json.dumps({"haccp": store["haccp_state"], "staff": store["figurine"], "events": store["events"]}, indent=2),
            file_name=f"SKA_BOSCHETTO_PRO_{datetime.now().strftime('%Y%m%d')}.json",
            use_container_width=True
        )
        if st.button("🟣 Prepara Nuovo Giro HACCP (Rimetti Quadretti in VIOLA)", use_container_width=True):
            for k in store["haccp_state"]:
                store["haccp_state"][k].update({"status": "PURPLE", "label": "In Attesa", "by": "-", "time": "--:--"})
            st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 1: INTERNO DEL SINGOLO QUADRATO (N01..N07)
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        if st.button("⬅️ Torna alla Costellazione"):
            st.session_state.selected_node_id = None
            st.rerun()
        st.markdown(f"### 📍 [{node['code']}] {node['name']} — *{node['subtitle']}*")

        st.markdown("##### 🔲 Quaderno Sinottico HACCP (3 Giri: M · P · S)")
        node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
        if not node_fridges:
            st.caption("Nessuna unità frigorifera in questo nodo.")
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
                    f"<div class='tile-meta'>{st_data['time']} · {st_data['by']}</div>"
                    f"</div>"
                )
            tiles_html += "</div>"
            st.markdown(tiles_html, unsafe_allow_html=True)

        with st.expander("🧭 Sottozone & 🥐 Assetti Colazione LAZERS", expanded=True):
            st.pills("Sottozone del blocco:", node["sub_zones"], default=node["sub_zones"][0] if node["sub_zones"] else None)
            for idx_b, bp in enumerate(node["breakfast_profiles"]):
                bp["active"] = st.checkbox(f"{bp['name']}", value=bp["active"], key=f"bf_{nid}_{idx_b}")

        with st.expander("👥 Figurine & 🚨 SOS del Reparto", expanded=True):
            for f in [f for f in store["figurine"] if f["node_id"] == nid]:
                st.info(f"♟️ **{f['nick']}** (*{f['role']}*) — {f['sub_zone']} | `{f['shift']}` (PIN `{f['pin']}`)")
            node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]
            for req in node_sos:
                st.warning(f"⏰ {req['time']} — **{req['item']}**")
            if node_sos and st.button("✔️ Segna SOS Evasi", use_container_width=True):
                store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                st.rerun()

# ==============================================================================
# VISTA 2: MOBILE DIPENDENTE (PIN 1001, 1002...)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error("PIN non riconosciuto. Usa '9999' per Direzione o '1001' / '1004' per Dipendenti.")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.markdown(f"### 👋 {user['nick']} — [{user_node['code']}] {user_node['name']}")
        st.caption(f"🧭 **Sottozona:** {user['sub_zone']} | ⏰ **Turno:** {user['shift']}")

        st.markdown("##### 1️⃣ Firma Quadretto Frigo")
        round_sel = st.radio("Giro HACCP:", ["M (Mattina)", "P (Pomeriggio)", "S (Sera)"], horizontal=True)
        round_code = round_sel[0]

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        if my_fridges:
            sel_key = st.selectbox("Unità Freddo", my_fridges, format_func=lambda x: x.split(" || ")[1])
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("🔴 Segnala Macchina GUASTA")

            if st.button("✔️ Firma e Colora Quadretto", use_container_width=True):
                status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                dot_icon = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}[status_color]
                fr_info["slots"][round_code] = dot_icon
                fr_info.update({"status": status_color, "label": label_text, "by": user["nick"], "time": datetime.now().strftime("%H:%M")})
                if status_color in ["RED", "YELLOW"]:
                    store["alarm_counter"] += 1
                st.success(f"Registrato ({round_code}): {label_text}")

        st.divider()
        st.markdown("##### 2️⃣ SOS Magazzino Rapido")
        sos_item = st.text_input("Cosa serve urgente?")
        if st.button("🚀 Invia SOS al Runner", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']}. {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.success("Richiesta inviata!")
