import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="SOVEREIGN KINETIC ARCHITECTURE", layout="wide")

# --- MEMORIA CONDIVISA LIVE (Sincronizza il tuo PC e il telefono di Alessandro) ---
@st.cache_resource
def get_shared_store():
    return {
        "nodes": [
            {"id": "N01", "name": "01. Casa Madre (Lab Pasticceria & Uffici)", "type": "PRODUZIONE_FREDDO", "fridges": ["Cella Positiva +4°C", "Cella Negativa -18°C", "Abbattitore"]},
            {"id": "N02", "name": "02. Corpo Albergo (Camere & Piani)", "type": "HOTEL_CORE", "fridges": []},
            {"id": "N03", "name": "03. Ricevimento & Magazzino Centrale", "type": "LOGISTICA_HUB", "fridges": ["Cella Scorte Bevande"]},
            {"id": "N04", "name": "04. Ristorante (Cucina + 5 Sale/Verande)", "type": "SALA_F&B", "sub_areas": ["Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare", "Cucina Centrale"], "fridges": ["Cella Carne +2°C", "Cella Pesce 0°C", "Frigo Linea 1"]},
            {"id": "N05", "name": "05. Corpo Bar", "type": "PRODUZIONE_FREDDO", "fridges": ["Banco Bar 1", "Vetrina Gelati/Dolci"]},
            {"id": "N06", "name": "06. Spiaggia & Gazebo Eventi", "type": "BALNEARE_EVENTI", "fridges": ["Frigo Champagne Gazebo"]},
            {"id": "N07", "name": "07. Parcheggio & Viabilità", "type": "PRESIDIO", "fridges": []}
        ],
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node": "01. Casa Madre (Lab Pasticceria & Uffici)", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante", "index_cost": 100, "node": "02. Corpo Albergo (Camere & Piani)", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Luca M.", "role": "Runner Magazzino", "index_cost": 85, "node": "03. Ricevimento & Magazzino Centrale", "shift": "Pranzo/Pom (12-20)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Resp. Veranda Circolare", "index_cost": 110, "node": "04. Ristorante (Cucina + 5 Sale/Verande)", "shift": "Cena/Sera (18-02)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node": "05. Corpo Bar", "shift": "Cena/Sera (18-02)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Esterno Matrimonio", "index_cost": 150, "node": "06. Spiaggia & Gazebo Eventi", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "12:15", "from": "Veranda Circolare", "item": "6x Franciacorta + 4 Casse Acqua", "status": "In corso"}
        ],
        "haccp_logs": [
            {"time": "07:30", "node": "01. Casa Madre", "fridge": "Cella Positiva +4°C", "temp": "+3.8°C", "by": "Marco S."}
        ],
        "event_phase": "1. Rito Civile (Gazebo)"
    }

store = get_shared_store()

# --- BARRA LATERALE: LOGIN PIN & PONTI MODULI ---
with st.sidebar:
    st.markdown("### 🏛️ SOVEREIGN KINETIC ARCHITECTURE")
    pin_input = st.text_input("Inserisci PIN Operativo", value="9999", help="9999 = Direzione | 1001 = Vista Dipendente")
    if st.button("🔄 Aggiorna Vista Live"):
        st.rerun()
    
    st.divider()
    st.caption("🔌 **PONTI ECOSISTEMA BEMASK**")
    hook_sz = st.toggle("Link: Sovereign Zero (Hotel)", value=True)
    hook_fb = st.toggle("Link: Modulo F&B (Lars Engine)", value=True)
    if hook_sz:
        st.info("Sovereign Zero: 18 Partenze | 24 Fermate")
    if hook_fb:
        st.info("F&B Engine: 145 Coperti Prenotati")

# ==============================================================================
# VISTA 1: DIREZIONE & ARCHITETTO (PIN MASTER 9999)
# ==============================================================================
if pin_input == "9999":
    st.title("⚡ SOVEREIGN KINETIC ARCHITECTURE // Command Center")
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌬️ Meteo Follonica (18:00)", "Maestrale 9 kt", "Verande OK")
    c2.metric("👥 Figurine Attive", str(len(store["figurine"])), "Max 99.000")
    tot_index = sum(f["index_cost"] for f in store["figurine"])
    c3.metric("📊 Indice Carico Giornaliero", f"{tot_index} pt", "Zero-Trace Mode")
    c4.metric("💍 Regia Evento Gazebo", store["event_phase"])

    tab_grid, tab_ops, tab_arch, tab_vault = st.tabs([
        "♟️ 1. Scacchiera Cinetica (7 Nodi)",
        "🚨 2. SOS Magazzino, HACCP & Eventi",
        "🏗️ 3. Costruttore Architetto",
        "🔐 4. Cassaforte 03:00 AM (Zero-Trace)"
    ])

    with tab_grid:
        st.subheader("Assegnazione Tattica Figurine sui Nodi Fisici")
        col_form, col_board = st.columns([1, 2])
        
        with col_form:
            st.markdown("**Sposta o Aggiungi Figurina**")
            nick_list = [f["nick"] for f in store["figurine"]] + ["+ Nuova Figurina Rapida"]
            sel_fig = st.selectbox("Seleziona Figurina", nick_list)
            node_names = [n["name"] for n in store["nodes"]]
            target_node = st.selectbox("Destinazione Nodo", node_names)
            target_shift = st.selectbox("Fascia Oraria", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)", "Notte (22-06)"])
            
            if sel_fig == "+ Nuova Figurina Rapida":
                new_nick = st.text_input("Nickname / Sigla (es. Extra B)")
                new_role = st.text_input("Ruolo (es. Sala / Runner)")
                new_idx = st.number_input("Indice Carico (Punti)", value=90)
                if st.button("Inserisci in Scacchiera"):
                    if new_nick:
                        store["figurine"].append({
                            "pin": str(1000 + len(store["figurine"]) + 1),
                            "nick": new_nick, "role": new_role, "index_cost": new_idx,
                            "node": target_node, "shift": target_shift
                        })
                        st.rerun()
            else:
                if st.button("Sposta Figurina"):
                    for f in store["figurine"]:
                        if f["nick"] == sel_fig:
                            f["node"] = target_node
                            f["shift"] = target_shift
                    st.rerun()

        with col_board:
            for node in store["nodes"]:
                with st.expander(f"📍 {node['name']} ({node['type']})", expanded=True):
                    assigned = [f for f in store["figurine"] if f["node"] == node["name"]]
                    if assigned:
                        for a in assigned:
                            st.markdown(f"- **{a['nick']}** (*{a['role']}*) — `{a['shift']}` | Indice: {a['index_cost']} pt | PIN: `{a['pin']}`")
                    else:
                        st.caption("Nessuna figurina assegnata in questo momento.")

    with tab_ops:
        col_sos, col_haccp, col_ev = st.columns(3)
        with col_sos:
            st.markdown("📦 **Coda SOS Magazzino -> Reparti**")
            for req in store["sos_queue"]:
                st.warning(f"⏰ {req['time']} | **Da:** {req['from']}\n\n**Richiesta:** {req['item']} ({req['status']})")
            if st.button("Segna SOS come Evasi"):
                store["sos_queue"].clear()
                st.rerun()

        with col_haccp:
            st.markdown("❄️ **Registro Ufficiale Temperature HACCP**")
            for log in store["haccp_logs"]:
                st.success(f"✔️ {log['time']} - **{log['node']}** ({log['fridge']}): **{log['temp']}** [Firma: {log['by']}]")

        with col_ev:
            st.markdown("🥂 **Sincronia Evento (Gazebo -> Cucina -> Pasticceria)**")
            store["event_phase"] = st.radio(
                "Cambia Fase Live:",
                ["1. Rito Civile (Gazebo)", "2. Aperitivo in Spiaggia", "3. Servito nelle Verande", "4. Alert Pasticceria: Fuori Torta!"]
            )
            st.checkbox("Fascia Tricolore & Regia Audio Pronta", value=True)
            st.checkbox("Permesso SIAE Verificato", value=True)

    with tab_arch:
        st.subheader("🏗️ Configuratore Nodi Aziendali (Modello Lego)")
        c_add1, c_add2, c_add3 = st.columns(3)
        new_node_name = c_add1.text_input("Nome Nuovo Blocco (es. 08. Rooftop Piscina)")
        new_node_type = c_add2.selectbox("Famiglia Mattone", ["SALA_F&B", "HOTEL_CORE", "PRODUZIONE_FREDDO", "LOGISTICA_HUB", "BALNEARE_EVENTI", "PRESIDIO"])
        new_fridges = c_add3.text_input("Frighi HACCP (separati da virgola)", value="Frigo Bar 1, Cella +4°C")
        if st.button("➕ Aggiungi Blocco alla Struttura"):
            if new_node_name:
                store["nodes"].append({
                    "id": f"N0{len(store['nodes'])+1}",
                    "name": new_node_name,
                    "type": new_node_type,
                    "fridges": [x.strip() for x in new_fridges.split(",") if x.strip()]
                })
                st.success(f"Blocco {new_node_name} creato!")
                st.rerun()

    with tab_vault:
        st.subheader("🔐 Protocollo Zero-Trace & Backup Criptato Notturno")
        st.write("Alle **03:00 AM** il sistema invia il pacchetto storico privato al dispositivo di Alessandro e azzera i turni sull'app aziendale, lasciando intatto solo il registro legale HACCP.")
        
        vault_payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "total_index_points": tot_index,
            "staff_snapshot": store["figurine"],
            "warehouse_movements": store["sos_queue"]
        }
        st.download_button(
            "📲 Simula Scarico Pacchetto Criptato (Vault Alessandro)",
            data=json.dumps(vault_payload, indent=2),
            file_name=f"SKA_VAULT_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )
        if st.button("🧹 Esegui Pulizia Lavagna Giornaliera (Reset Turni, Mantieni HACCP)"):
            for f in store["figurine"]:
                f["shift"] = "Da Assegnare"
            store["sos_queue"].clear()
            st.success("Lavagna operativa azzerata! Nessuno storico turni presente sul server pubblico.")
            st.rerun()

# ==============================================================================
# VISTA 2: MOBILE DIPENDENTE (Inserendo es. PIN 1001, 1002...)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error("PIN non riconosciuto. Prova '9999' per Direzione o '1001' per Vista Dipendente.")
    else:
        st.title(f"👋 Ciao, {user['nick']}")
        st.info(f"📍 **Il tuo Nodo oggi:** {user['node']}\n\n⏰ **Turno:** {user['shift']} | **Fase Evento:** {store['event_phase']}")
        
        st.subheader("1️⃣ Richiesta Rapida SOS Magazzino")
        sos_item = st.text_input("Cosa serve urgente dal Magazzino Centrale?")
        if st.button("🚀 Invia SOS al Runner"):
            if sos_item:
                store["sos_queue"].append({
                    "time": datetime.now().strftime("%H:%M"),
                    "from": user["node"],
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.success("Richiesta inviata al Magazzino!")

        st.subheader("2️⃣ Registrazione Rapida Temperatura Frighi (HACCP)")
        all_fridges = [f"{n['name']} -> {fr}" for n in store["nodes"] for fr in n.get("fridges", [])]
        sel_fridge = st.selectbox("Seleziona Cella / Frigo", all_fridges)
        temp_val = st.slider("Temperatura Rilevata (°C)", min_value=-25.0, max_value=15.0, value=4.0, step=0.5)
        if st.button("✔️ Firma e Registra HACCP"):
            store["haccp_logs"].append({
                "time": datetime.now().strftime("%H:%M"),
                "node": sel_fridge.split(" -> ")[0],
                "fridge": sel_fridge.split(" -> ")[1],
                "temp": f"{temp_val:+.1f}°C",
                "by": user["nick"]
            })
            st.success("Temperatura registrata correttamente nel registro ufficiale!")