import streamlit as st
import streamlit.components.v1 as components
import json
from datetime import datetime

st.set_page_config(page_title="S.K.A. // SOVEREIGN KINETIC ARCHITECTURE", layout="wide")

# --- CSS STELLARE: PIANO PRINCIPALE PULITO & QUADRETTI INTERNI ---
st.markdown("""
<style>
@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.85); }
    70% { box-shadow: 0 0 0 12px rgba(239, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
@keyframes pulse-amber {
    0% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(245, 158, 11, 0); }
    100% { box-shadow: 0 0 0 0 rgba(245, 158, 11, 0); }
}
.tactical-banner-sos {
    background: linear-gradient(90deg, #78350f 0%, #b45309 100%);
    color: #fef3c7; padding: 10px 18px; border-radius: 8px;
    border-left: 6px solid #fbbf24; font-weight: 700; margin-bottom: 12px;
    animation: pulse-amber 2s infinite;
}
.tactical-banner-danger {
    background: linear-gradient(90deg, #7f1d1d 0%, #dc2626 100%);
    color: #fef2f2; padding: 10px 18px; border-radius: 8px;
    border-left: 6px solid #f87171; font-weight: 700; margin-bottom: 12px;
    animation: pulse-red 1.5s infinite;
}
.architect-badge {
    background: linear-gradient(90deg, #311042 0%, #701a75 100%);
    color: #f5d0fe; padding: 8px 16px; border-radius: 8px;
    border-left: 5px solid #e879f9; font-weight: 700; margin-bottom: 12px;
}
.node-card {
    background: linear-gradient(145deg, #0f172a 0%, #1e293b 100%);
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
    color: #f8fafc;
    margin-bottom: 8px;
    min-height: 160px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
.node-card-alert { border: 2px solid #ef4444; animation: pulse-red 1.8s infinite; }
.node-card-warn  { border: 2px solid #f59e0b; }
.node-title  { font-size: 1.08rem; font-weight: 800; color: #38bdf8; letter-spacing: 0.3px; }
.node-sub    { font-size: 0.78rem; color: #94a3b8; margin-top: 2px; }
.node-badges { display: flex; gap: 8px; margin-top: 12px; font-size: 0.76rem; font-weight: 700; flex-wrap: wrap; }
.badge-pill  { background: rgba(255,255,255,0.08); padding: 4px 9px; border-radius: 6px; }

.haccp-grid  { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; margin-bottom: 14px; }
.haccp-tile  {
    width: 152px; height: 92px; border-radius: 8px; padding: 8px 10px;
    display: flex; flex-direction: column; justify-content: space-between;
    color: white; box-shadow: 0 2px 6px rgba(0,0,0,0.4);
}
.tile-purple { background: #581c87; border: 2px solid #a855f7; }
.tile-green  { background: #14532d; border: 2px solid #22c55e; }
.tile-yellow { background: #713f12; border: 2px solid #eab308; }
.tile-red    { background: #7f1d1d; border: 2px solid #ef4444; animation: pulse-red 1.5s infinite; }
.tile-title  { font-size: 0.72rem; font-weight: 700; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.tile-val    { font-size: 1.05rem; font-weight: 900; }
.tile-slots  { font-size: 0.66rem; font-weight: 700; background: rgba(0,0,0,0.3); padding: 2px 6px; border-radius: 4px; display: flex; justify-content: space-between; }
.tile-meta   { font-size: 0.62rem; opacity: 0.85; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
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

# --- DNA ARCHITETTURALE CERTIFICATO BEMASK (Sigillato a monte) ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N01", "code": "01", "name": "Casa Madre", "subtitle": "Lab Pasticceria & Uffici Direzione",
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
            "id": "N02", "code": "02", "name": "Corpo Albergo", "subtitle": "Camere, Piani & Housekeeping",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria & Carrelli"],
            "breakfast_profiles": [
                {"name": "Room Service / Vassoi Camera", "active": True},
                {"name": "Early Breakfast Box (Partenze Alba)", "active": False}
            ],
            "fridges": [{"name": "Frigo Office Piani", "kind": "POS"}]
        },
        {
            "id": "N03", "code": "03", "name": "Ricevimento & Magazzino", "subtitle": "Front Office & Stoccaggio Centrale",
            "sub_zones": ["Front Desk & Accoglienza", "Magazzino Centrale", "Baia Scarico Fornitori"],
            "breakfast_profiles": [],
            "fridges": [
                {"name": "Cella Latticini/Salumi", "kind": "POS"},
                {"name": "Cella Ortofrutta +6°C", "kind": "POS"},
                {"name": "Cella Scorte Bevande", "kind": "POS"}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "Ristorante & 5 Verande", "subtitle": "Cucina Centrale, Sala Colazioni & Sale",
            "sub_zones": ["Sala Colazioni (Mattina)", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare", "Cucina Centrale"],
            "breakfast_profiles": [
                {"name": "Tipo A: Buffet Continentale / B&B (Dolce & Caffetteria)", "active": True},
                {"name": "Tipo B: International & Pensioni HB/FB (Salato, Uova, Bacon)", "active": True},
                {"name": "Tipo C: Corner Salute, Celiaci (Gluten-Free) & Bimbi", "active": True}
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
            "id": "N05", "code": "05", "name": "Corpo Bar", "subtitle": "Caffetteria, Cocktail & Gelateria",
            "sub_zones": ["Banco Caffetteria Mattina", "Terrazza Aperitivi", "Postazione Cocktail Sera"],
            "breakfast_profiles": [
                {"name": "Supporto Espresso & Cappuccini Grandi Numeri", "active": True}
            ],
            "fridges": [
                {"name": "Banco Bar 1 (Latte)", "kind": "POS"},
                {"name": "Banco Bar 2 (Birre/Vini)", "kind": "POS"},
                {"name": "Vetrina Gelati -16°C", "kind": "NEG"},
                {"name": "Pozzetto Ghiaccio Bar", "kind": "NEG"}
            ]
        },
        {
            "id": "N06", "code": "06", "name": "Spiaggia & Gazebo", "subtitle": "Stabilimento Balneare & Regia Cerimonie",
            "sub_zones": ["Gazebo Rito & Taglio Torta", "Ombrelloni & Tende", "Chiosco/Point Spiaggia"],
            "breakfast_profiles": [
                {"name": "Light Breakfast / Frutta Fresca sotto Tenda", "active": False}
            ],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"},
                {"name": "Pozzetto Ghiaccio Gazebo", "kind": "NEG"}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "Parcheggio & Viabilità", "subtitle": "Controllo Accessi, Valet & Flussi Ospiti",
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

    # Demo pre-caricata
    haccp_state["N01 || Cella Basi +4°C"].update({"status": "GREEN", "label": "+3.6°C", "by": "Marco S.", "time": "07:30", "slots": {"M": "🟢", "P": "⚪", "S": "⚪"}})
    haccp_state["N04 || Buffet Freddo Colazioni"].update({"status": "GREEN", "label": "+3.9°C", "by": "Jolly 01", "time": "07:15", "slots": {"M": "🟢", "P": "⚪", "S": "⚪"}})
    haccp_state["N04 || Cella Pesce 0°C"].update({"status": "YELLOW", "label": "+6.2°C", "by": "Jolly 01", "time": "08:15", "slots": {"M": "🟡", "P": "⚪", "S": "⚪"}})

    return {
        "nodes": nodes,
        "haccp_state": haccp_state,
        "active_round": "M (Mattina 07-11)",
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Luca M.", "role": "Runner Magazzino", "index_cost": 85, "node_id": "N03", "sub_zone": "Magazzino Centrale", "shift": "Pranzo/Pom (12-20)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Maître / Resp. Verande", "index_cost": 110, "node_id": "N04", "sub_zone": "Sala Colazioni (Mattina)", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node_id": "N05", "sub_zone": "Banco Caffetteria Mattina", "shift": "Mattina (07-15)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Regia Gazebo", "index_cost": 150, "node_id": "N06", "sub_zone": "Gazebo Rito & Taglio Torta", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "08:10", "node_id": "N04", "from": "04. Ristorante (Sala Colazioni)", "item": "2 Vassoi Cornetti + Latte Senza Lattosio", "status": "In corso"}
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

# --- BARRA LATERALE ---
with st.sidebar:
    st.markdown("### 🏛️ S.K.A. // BOSCHETTO")
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

    st.divider()
    st.caption("🔒 *Architettura Certificata BEMASK — Struttura Nodi Sigillata*")

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
        st.markdown("<div class='architect-badge'>🛠️ MODALITÀ MASTER ARCHITECT BEMASK ATTIVA (PIN 0000) — I comandi di modifica strutturale dei Nodi e dei Frighi sono sbloccati.</div>", unsafe_allow_html=True)

    # BANNER VISIVI PULSANTI SEMPRE VISIBILI IN ALTO
    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='tactical-banner-danger'>🚨 ALLARME ROSSO HACCP: Anomalia critica rilevata su: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        st.markdown(f"<div class='tactical-banner-sos'>⚡ SOS MAGAZZINO ATTIVO ({len(store['sos_queue'])}) — Ultimo da {latest_sos['from']} ({latest_sos['time']}): \"{latest_sos['item']}\"</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA COSTELLAZIONE PRINCIPALE (SOLO I 7 QUADRATI PULITI)
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        st.markdown("## 🌌 SOVEREIGN KINETIC ARCHITECTURE // Costellazione Nodi")
        st.caption("Piano Principale ad Alta Purezza Visiva — Tocca un Quadrato per entrare nelle Sottozone, negli Assetti Colazione LAZERS e nei Quadretti HACCP del reparto.")

        k1, k2, k3, k4 = st.columns(4)
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_ev = len(store["events"])
        k1.metric("🏛️ Nodi Certificati", f"{len(store['nodes'])} Blocchi", "Struttura Sigillata")
        k2.metric("👥 Figurine in Campo", f"{tot_fig} Unità", f"{sum(f['index_cost'] for f in store['figurine'])} pt indice")
        k3.metric("🚨 Coda SOS Magazzino", f"{tot_sos} Aperti", "Tempo Reale")
        k4.metric("🥂 Regia Multi-Evento", f"{tot_ev} Attivi Oggi", f"{sum(e['pax'] for e in store['events'])} Pax Totali")

        st.write("")

        row1 = st.columns(4)
        row2 = st.columns(3)
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

            border_class = ""
            if n_red > 0: border_class = "node-card-alert"
            elif n_sos > 0 or n_yellow > 0: border_class = "node-card-warn"

            fridge_badge = f"❄️ 🟢{n_green} 🟣{n_purple} 🟡{n_yellow} 🔴{n_red}" if n_fridges else "❄️ Zero Frighi"
            sos_badge = f"🚨 {n_sos} SOS" if n_sos > 0 else "✔️ Logistica OK"

            with grid_cols[idx % len(grid_cols)]:
                st.markdown(f"""
                <div class="node-card {border_class}">
                    <div>
                        <div class="node-title">[{node['code']}] {node['name']}</div>
                        <div class="node-sub">{node['subtitle']}</div>
                        <div class="node-sub" style="margin-top:6px; color:#cbd5e1;">🧭 {len(node['sub_zones'])} Sottozone · 🥐 {active_bf} Linee Colazione</div>
                    </div>
                    <div class="node-badges">
                        <span class="badge-pill">👥 {n_staff} Figurine</span>
                        <span class="badge-pill">{fridge_badge}</span>
                        <span class="badge-pill">{sos_badge}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"🔍 Apri {node['code']}. {node['name']}", key=f"open_{nid}", use_container_width=True):
                    st.session_state.selected_node_id = nid
                    st.rerun()

        st.divider()
        with st.expander("🥂 Regia Parallela Multi-Evento & 🔐 Cassaforte Notturna 03:00 AM", expanded=False):
            cols_ev = st.columns(len(store["events"]))
            phase_options = [
                "1. Accoglienza / Rito",
                "2. Aperitivo",
                "3. Servito",
                "4. Alert Pasticceria: Fuori Torta!",
                "5. Open Bar & Musica"
            ]
            for idx, ev in enumerate(store["events"]):
                with cols_ev[idx]:
                    st.markdown(f"**{ev['title']}** (`{ev['pax']} pax`)")
                    st.caption(f"📍 {ev['zone']} | 🎂 Torta: `{ev['cake_time']}`")
                    cur_i = phase_options.index(ev["phase"]) if ev["phase"] in phase_options else 0
                    new_ph = st.selectbox("Fase Live", phase_options, index=cur_i, key=f"ev_{ev['id']}")
                    if new_ph != ev["phase"]:
                        ev["phase"] = new_ph
                        st.rerun()

            st.divider()
            c_v1, c_v2 = st.columns(2)
            with c_v1:
                st.download_button(
                    "📲 Scarica Vault Criptato 03:00 AM (JSON)",
                    data=json.dumps({"haccp": store["haccp_state"], "staff": store["figurine"], "events": store["events"]}, indent=2),
                    file_name=f"SKA_VAULT_{datetime.now().strftime('%Y%m%d')}.json",
                    use_container_width=True
                )
            with c_v2:
                if st.button("🟣 Prepara Nuovo Giro HACCP (Rimetti Quadretti in VIOLA)", use_container_width=True):
                    for k in store["haccp_state"]:
                        store["haccp_state"][k].update({"status": "PURPLE", "label": "In Attesa", "by": "-", "time": "--:--"})
                    st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 1: INTERNO DEL SINGOLO QUADRATO (SOTTOZONE, COLAZIONI, FRIGHI, STAFF)
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        c_back, c_title = st.columns([1, 4])
        with c_back:
            if st.button("⬅️ Torna ai 7 Quadrati", use_container_width=True):
                st.session_state.selected_node_id = None
                st.rerun()
        with c_title:
            st.markdown(f"## 📍 [{node['code']}] {node['name']} — *{node['subtitle']}*")

        st.divider()

        col_sub, col_bf = st.columns(2)
        with col_sub:
            st.markdown("#### 🧭 Sottozone Fisiche Certificate")
            st.pills("Sottozone attive in questo blocco:", node["sub_zones"], default=node["sub_zones"][0] if node["sub_zones"] else None)
            if is_architect:
                new_sub = st.text_input("🛠️ [Architetto] Aggiungi Nuova Sottozona:")
                if st.button("➕ Salva Sottozona nel DNA"):
                    if new_sub:
                        node["sub_zones"].append(new_sub)
                        st.rerun()

        with col_bf:
            st.markdown("#### 🥐 Moduli Colazione & Pensioni (Ponte LAZERS)")
            if node["breakfast_profiles"]:
                for idx_b, bp in enumerate(node["breakfast_profiles"]):
                    bp["active"] = st.checkbox(f"**{bp['name']}**", value=bp["active"], key=f"bf_{nid}_{idx_b}")
            else:
                st.caption("Nessuna linea colazione prevista in questo nodo logistico.")

        st.divider()

        col_haccp, col_ops = st.columns([1.6, 1.4])

        with col_haccp:
            st.markdown("#### 🔲 Quaderno Sinottico HACCP (3 Giri: M · P · S)")
            st.caption("🟣 In Attesa | 🟢 OK | 🟡 Incoerente / Pre-Allarme | 🔴 Guasto / Critico")
            node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
            if not node_fridges:
                st.caption("Nessuna unità frigorifera installata in questo nodo.")
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

            if is_architect:
                with st.expander("🛠️ [Architetto] Aggiungi Unità Freddo al Reparto"):
                    nf_name = st.text_input("Nome Unità (es. Frigo Vini Veranda)")
                    nf_kind = st.selectbox("Tipologia", ["POS (+2°C / +6°C)", "NEG (-18°C)"])
                    if st.button("➕ Inserisci Quadretto Frigo"):
                        if nf_name:
                            k_code = "POS" if "POS" in nf_kind else "NEG"
                            node["fridges"].append({"name": nf_name, "kind": k_code})
                            store["haccp_state"][f"{nid} || {nf_name}"] = {
                                "node_id": nid, "fridge_name": nf_name, "status": "PURPLE",
                                "label": "In Attesa", "by": "-", "time": "--:--",
                                "kind": k_code, "slots": {"M": "⚪", "P": "⚪", "S": "⚪"}
                            }
                            st.rerun()

        with col_ops:
            st.markdown("#### 👥 Figurine Operanti nel Blocco")
            node_staff = [f for f in store["figurine"] if f["node_id"] == nid]
            for f in node_staff:
                st.info(f"♟️ **{f['nick']}** (*{f['role']}*) — Sottozona: **{f['sub_zone']}** | `{f['shift']}` (PIN: `{f['pin']}`)")

            with st.expander("🔄 Sposta qui una Figurina o cambia Sottozona"):
                pick_fig = st.selectbox("Figurina", [f["nick"] for f in store["figurine"]])
                pick_sub = st.selectbox("Destinazione Sottozona", node["sub_zones"])
                pick_sh = st.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)"])
                if st.button("Assegna Figurina"):
                    for f in store["figurine"]:
                        if f["nick"] == pick_fig:
                            f["node_id"] = nid
                            f["sub_zone"] = pick_sub
                            f["shift"] = pick_sh
                    st.rerun()

            st.markdown("#### 🚨 SOS Magazzino del Reparto")
            node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]
            if not node_sos:
                st.caption("Nessuna richiesta urgente attiva.")
            for req in node_sos:
                st.warning(f"⏰ {req['time']} — **{req['item']}**")
            if node_sos and st.button("✔️ Segna SOS del Reparto come Evasi", use_container_width=True):
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
        st.title(f"👋 {user['nick']}")
        st.info(f"🏛️ **Blocco:** [{user_node['code']}] {user_node['name']}\n\n🧭 **Sottozona:** {user['sub_zone']} | ⏰ **Turno:** {user['shift']}")

        active_bfs = [b["name"] for b in user_node["breakfast_profiles"] if b["active"]]
        if active_bfs:
            with st.expander("🥐 Linee Colazione Attive nel tuo Reparto", expanded=True):
                for b_name in active_bfs:
                    st.markdown(f"- ✔️ **{b_name}**")

        st.subheader("1️⃣ Firma Quadretto Frigo (" + user_node["name"] + ")")
        round_sel = st.radio("Giro HACCP:", ["M (Mattina)", "P (Pomeriggio)", "S (Sera)"], horizontal=True)
        round_code = round_sel[0]

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        if my_fridges:
            sel_key = st.selectbox("Seleziona Unità Freddo", my_fridges, format_func=lambda x: x.split(" || ")[1])
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura Letta (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("🔴 Segnala Macchina GUASTA / Blocco Motore")

            if st.button("✔️ Firma e Colora Quadretto", use_container_width=True):
                status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                dot_icon = {"GREEN": "🟢", "YELLOW": "🟡", "RED": "🔴"}[status_color]
                fr_info["slots"][round_code] = dot_icon
                fr_info.update({"status": status_color, "label": label_text, "by": user["nick"], "time": datetime.now().strftime("%H:%M")})
                if status_color in ["RED", "YELLOW"]:
                    store["alarm_counter"] += 1
                st.success(f"Quadretto aggiornato ({round_code}): {label_text}")

        st.divider()
        st.subheader("2️⃣ SOS Magazzino Rapido")
        sos_item = st.text_input("Cosa serve urgente nella tua Sottozona?")
        if st.button("🚀 Invia SOS al Runner", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']}. {user_node['name']} ({user['sub_zone']})",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.success("Richiesta inviata in Direzione e al Magazzino!")
