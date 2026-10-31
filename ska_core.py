import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

st.set_page_config(
    page_title="S.K.A. // BOSCHETTO PRO",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS ARCHITETTONICO MINIMALISTA (ZERO EMOJI, ZERO TAGLI) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');

/* Nasconde l'header bianco di Streamlit che copriva il banner */
header[data-testid="stHeader"] {
    background: transparent !important;
}

.stApp {
    background-color: #090d16 !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}

.block-container {
    padding-top: 2.8rem !important;
    padding-bottom: 2rem !important;
    max-width: 1400px !important;
}

/* INTESTAZIONE PULITA */
.top-bar {
    border-bottom: 1px solid #1e293b;
    padding-bottom: 12px;
    margin-bottom: 18px;
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
}
.brand-title {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    color: #f8fafc;
    text-transform: uppercase;
}
.brand-title span {
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 500;
}
.brand-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #64748b;
    letter-spacing: 0.05em;
}

/* STRISCIA KPI TECNICA */
.kpi-bar {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.kpi-box {
    background: #0f172a;
    border: 1px solid #1e293b;
    border-left: 3px solid #38bdf8;
    border-radius: 4px;
    padding: 10px 14px;
}
.kpi-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.kpi-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f8fafc;
    margin-top: 2px;
}

/* BANNER ALLERTE SOBRI E LEGGIBILI */
.alert-bar-sos {
    background: #1e1b18;
    border: 1px solid #d97706;
    border-left: 4px solid #f59e0b;
    color: #fde68a;
    padding: 10px 16px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin-bottom: 16px;
}
.alert-bar-crit {
    background: #231215;
    border: 1px solid #dc2626;
    border-left: 4px solid #ef4444;
    color: #fecaca;
    padding: 10px 16px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    margin-bottom: 16px;
}

/* CARD NODI: NESSUNA ALTEZZA BLOCCATA CHE TAGLIA IL TESTO, STILE ARCHITETTONICO */
div.stButton > button[kind="primary"] {
    background: #0f172a !important;
    border: 1px solid #1e293b !important;
    border-top: 2px solid #334155 !important;
    border-radius: 6px !important;
    height: auto !important;
    min-height: 118px !important;
    width: 100% !important;
    padding: 16px 18px !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: flex-start !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25) !important;
    transition: all 0.15s ease !important;
    margin-bottom: 6px !important;
}
div.stButton > button[kind="primary"]:hover {
    background: #131f38 !important;
    border-color: #38bdf8 !important;
    border-top: 2px solid #38bdf8 !important;
}
div.stButton > button[kind="primary"] p {
    white-space: pre-line !important;
    line-height: 1.55 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.80rem !important;
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
    letter-spacing: 0.02em !important;
}

/* MATRICE QUADRETTI HACCP INTERNA */
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

/* RESPONSIVE SMARTPHONE: 1 COLONNA LARGA E PULITA, MAI TESTO MOZZATO */
@media (max-width: 768px) {
    .block-container {
        padding-top: 2.4rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
    }
    .kpi-bar {
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
    }
    div.stButton > button[kind="primary"] {
        min-height: 92px !important;
        padding: 12px 14px !important;
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

# --- DNA STRUTTURALE ---
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
            "id": "N03", "code": "03", "name": "RICEVIMENTO & HUB", "subtitle": "Front Office & Magazzino Centrale",
            "sub_zones": ["Front Desk", "Magazzino Centrale", "Baia Scarico Fornitori"],
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
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Luca M.", "role": "Runner Magazzino", "index_cost": 85, "node_id": "N03", "sub_zone": "Magazzino Centrale", "shift": "Pranzo/Pom (12-20)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Maître Verande", "index_cost": 110, "node_id": "N04", "sub_zone": "Sala Colazioni", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node_id": "N05", "sub_zone": "Banco Caffetteria", "shift": "Mattina (07-15)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Regia Gazebo", "index_cost": 150, "node_id": "N06", "sub_zone": "Gazebo Cerimonie", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "08:10", "node_id": "N04", "from": "04. Ristorante (Sala Colazioni)", "item": "2 Vassoi Cornetti + Latte Senza Lattosio", "status": "In corso"}
        ],
        "events": [
            {"id": "EV1", "title": "Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "phase": "2. Aperitivo"},
            {"id": "EV3", "title": "Ristorante Pensioni & Carta", "zone": "Veranda 1 + Sala Interna", "pax": 85, "cake_time": "Continuo", "phase": "3. Servito"}
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

# --- BARRA LATERALE ---
with st.sidebar:
    st.markdown("### S.K.A. // BOSCHETTO PRO")
    pin_input = st.text_input("PIN Operativo", value="9999", help="9999 = Direzione | 1001 = Dipendente | 0000 = Architetto")
    if st.button("Aggiorna Stato Live", use_container_width=True):
        st.rerun()

    st.divider()
    st.caption("SONAR TATTICO")
    sonar_active = st.toggle("Attiva Sonar Urgenze", value=False)
    if sonar_active:
        c_s1, c_s2 = st.columns(2)
        if c_s1.button("Test Ping"): play_tactical_sonar("ping")
        if c_s2.button("Test Allarme"): play_tactical_sonar("alarm")

    st.divider()
    st.caption("PONTI ECOSISTEMA BEMASK")
    hook_sz = st.toggle("Sovereign Zero (Hotel)", value=True)
    hook_lz = st.toggle("LAZERS (F&B Engine)", value=True)
    if hook_sz:
        st.caption("Sovereign Zero: 112 Pax in Casa")
    if hook_lz:
        st.caption("LAZERS: 3 Linee Colazione | 38 HB | 3 Celiaci")

# --- CONTROLLO SONAR AUTOMATICO ---
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

    # INTESTAZIONE SOBRIA E PROFESSIONALE
    st.markdown("""
    <div class="top-bar">
        <div class="brand-title">SOVEREIGN KINETIC ARCHITECTURE <span>// BOSCHETTO PRO</span></div>
        <div class="brand-sub">BEMASK COMMAND SYSTEM · ZERO-TRACE PROTOCOL</div>
    </div>
    """, unsafe_allow_html=True)

    if is_architect:
        st.info("MODALITÀ MASTER ARCHITECT ATTIVA (PIN 0000) — Modifica strutturale abilitata.")

    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='alert-bar-crit'>ALLARME CRITICO HACCP: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        st.markdown(f"<div class='alert-bar-sos'>LOGISTICA SOS ATTIVO ({len(store['sos_queue'])}) — {latest_sos['from']} [{latest_sos['time']}]: {latest_sos['item']}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA GRIGLIA DEI NODI (PULIZIA ASSOLUTA, ZERO EMOJI)
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_ev = len(store["events"])
        tot_pts = sum(f["index_cost"] for f in store["figurine"])
        tot_pax = sum(e["pax"] for e in store["events"])

        st.markdown(f"""
        <div class="kpi-bar">
            <div class="kpi-box"><div class="kpi-lbl">Nodi Struttura</div><div class="kpi-num">07 ATTIVI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Forza Lavoro</div><div class="kpi-num">{tot_fig} UNITA ({tot_pts} PT)</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Coda Logistica</div><div class="kpi-num">{tot_sos} SOS APERTI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Regia Eventi</div><div class="kpi-num">{tot_ev} LIVE ({tot_pax} PAX)</div></div>
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
            n_wait = sum(1 for f in n_fridges if f["status"] == "PURPLE")
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
                f"08 // REGIA EVENTI & VAULT\n"
                f"Sincronia Cerimonie & Backup 03:00 AM\n"
                f"EVENTI: {tot_ev} ({tot_pax} PAX)   |   ZERO-TRACE"
            )
            if st.button(hub_label, key="tile_HUB", type="primary", use_container_width=True):
                st.session_state.selected_node_id = "HUB_VAULT"
                st.rerun()

    # --------------------------------------------------------------------------
    # VISTA 08: REGIA MULTI-EVENTO & CASSAFORTE 03:00 AM
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "HUB_VAULT":
        if st.button("← TORNA ALLA PLANCIA PRINCIPALE"):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown("### 08 // REGIA MULTI-EVENTO & CASSAFORTE 03:00 AM")
        st.divider()

        phase_options = [
            "1. Accoglienza / Rito",
            "2. Aperitivo",
            "3. Servito",
            "4. Alert Pasticceria: Fuori Torta!",
            "5. Open Bar & Musica"
        ]
        cols_ev = st.columns(len(store["events"]))
        for idx, ev in enumerate(store["events"]):
            with cols_ev[idx]:
                st.markdown(f"**{ev['title']}**")
                st.caption(f"Zona: {ev['zone']}  |  Ospiti: {ev['pax']} pax  |  Torta: {ev['cake_time']}")
                cur_i = phase_options.index(ev["phase"]) if ev["phase"] in phase_options else 0
                new_ph = st.selectbox("Stato Avanzamento", phase_options, index=cur_i, key=f"ev_{ev['id']}")
                if new_ph != ev["phase"]:
                    ev["phase"] = new_ph
                    st.rerun()

        st.divider()
        c_v1, c_v2 = st.columns(2)
        with c_v1:
            st.download_button(
                "SCARICA VAULT CRIPTATO 03:00 AM (.JSON)",
                data=json.dumps({"haccp": store["haccp_state"], "staff": store["figurine"], "events": store["events"]}, indent=2),
                file_name=f"SKA_BOSCHETTO_PRO_{datetime.now().strftime('%Y%m%d')}.json",
                use_container_width=True
            )
        with c_v2:
            if st.button("RESET NUOVO GIRO HACCP (RIPORTA IN ATTESA)", use_container_width=True):
                for k in store["haccp_state"]:
                    store["haccp_state"][k].update({"status": "PURPLE", "label": "ATTESA", "by": "-", "time": "--:--"})
                st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 1: INTERNO DEL SINGOLO REPARTO (N01..N07)
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        if st.button("← TORNA ALLA PLANCIA PRINCIPALE"):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown(f"### {node['code']} // {node['name']} — {node['subtitle']}")
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
                    if st.button("Inserisci nel Reparto"):
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
            st.markdown("##### SOTTOZONE & LINEE COLAZIONE (LAZERS)")
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
                if st.button("Conferma Assegnazione"):
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
                if st.button("Segna Richieste SOS come Evase", use_container_width=True):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()

# ==============================================================================
# VISTA 2: TERMINALE OPERATORE (PIN 1001, 1002...)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error("PIN non riconosciuto. Inserire 9999 (Direzione) o 1001 (Operatore).")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.markdown(f"### OPERATORE: {user['nick']} // [{user_node['code']}] {user_node['name']}")
        st.caption(f"SOTTOZONA: {user['sub_zone']}   |   TURNO: {user['shift']}")
        st.divider()

        st.markdown("##### 1. REGISTRAZIONE TEMPERATURA HACCP")
        round_sel = st.radio("Giro di Controllo:", ["M (Mattina)", "P (Pomeriggio)", "S (Sera)"], horizontal=True)
        round_code = round_sel[0]

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        if my_fridges:
            sel_key = st.selectbox("Seleziona Unità", my_fridges, format_func=lambda x: x.split(" || ")[1])
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura Rilevata (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("Segnala Anomalia Blocco / Guasto Meccanico")

            if st.button("FIRMA E REGISTRA LETTURA", use_container_width=True):
                status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                slot_txt = {"GREEN": "OK", "YELLOW": "WARN", "RED": "CRIT"}[status_color]
                fr_info["slots"][round_code] = slot_txt
                fr_info.update({"status": status_color, "label": label_text, "by": user["nick"], "time": datetime.now().strftime("%H:%M")})
                if status_color in ["RED", "YELLOW"]:
                    store["alarm_counter"] += 1
                st.success(f"Registrato ({round_code}): {label_text}")

        st.divider()
        st.markdown("##### 2. RICHIESTA URGENTE MAGAZZINO (SOS)")
        sos_item = st.text_input("Articolo / Fornitura richiesta:")
        if st.button("INVIA RICHIESTA AL MAGAZZINO", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']}. {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.success("Richiesta trasmessa.")
                
