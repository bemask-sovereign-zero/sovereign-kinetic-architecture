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
    border-color: #38bdf8 !important;
    box-shadow: 0 0 18px rgba(56, 189, 248, 0.28) !important;
}
div.stButton > button[kind="primary"]:active {
    transform: scale(0.97) !important;
    background: #1e3a5f !important;
}

/* QUADRETTI FRIGO INTERNI AL REPARTO (LIVELLO 1) */
.haccp-grid { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; margin-bottom: 16px; }
.haccp-tile {
    width: 175px; min-height: 94px; border-radius: 6px; padding: 10px 12px;
    display: flex; flex-direction: column; justify-content: space-between;
    font-family: 'JetBrains Mono', monospace; color: #f8fafc;
}
.tile-purple  { background: #1e1333; border: 1.5px solid #9333ea; border-left: 5px solid #a855f7; }
.tile-overdue { background: #2b1708; border: 1.5px solid #f59e0b; border-left: 5px solid #fbbf24; }
.tile-green   { background: #092218; border: 1.5px solid #16a34a; border-left: 5px solid #22c55e; }
.tile-yellow  { background: #261c0b; border: 1.5px solid #d97706; border-left: 5px solid #eab308; }
.tile-red     { background: #2b1115; border: 1.5px solid #dc2626; border-left: 5px solid #ef4444; }
.tile-title   { font-family: 'Inter', sans-serif; font-size: 0.76rem; font-weight: 600; color: #e2e8f0; }
.tile-val     { font-size: 1.05rem; font-weight: 700; margin: 4px 0; }
.tile-meta    { font-size: 0.66rem; color: #cbd5e1; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 4px; display: flex; justify-content: space-between; }

/* TABELLA REGISTRO STAMPA UFFICIALE */
.log-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.76rem;
    margin-top: 10px;
}
.log-table th {
    background: #16243d;
    color: #38bdf8;
    text-align: left;
    padding: 8px 10px;
    border: 1px solid #1e293b;
}
.log-table td {
    padding: 7px 10px;
    border: 1px solid #1e293b;
    color: #e2e8f0;
}

label, .stRadio label, .stSelectbox label, .stTextInput label, .stNumberInput label {
    color: #cbd5e1 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.78rem !important;
}

@media (max-width: 768px) {
    .block-container { padding-top: 1.2rem !important; padding-left: 0.7rem !important; padding-right: 0.7rem !important; }
    .kpi-bar { grid-template-columns: repeat(2, 1fr); gap: 8px; }
    .haccp-tile { width: 48% !important; }
}
</style>
""", unsafe_allow_html=True)

# --- SONAR TATTICO E SINTETIZZATORE AUDIO AD OGNI TOCCO ---
def play_tactical_sonar(mode="ping"):
    freq = 880 if mode == "ping" else 220
    wave = "sine" if mode == "ping" else "triangle"
    js_code = f"""
    <script>
    (function() {{
        try {{
            const ctx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = ctx.createOscillator(); const gain = ctx.createGain();
            osc.type = '{wave}'; osc.frequency.setValueAtTime({freq}, ctx.currentTime);
            gain.gain.setValueAtTime(0.18, ctx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.25);
            osc.connect(gain); gain.connect(ctx.destination);
            osc.start(); osc.stop(ctx.currentTime + 0.25);
        }} catch(e) {{}}
    }})();
    </script>
    """
    components.html(js_code, height=0, width=0)

def bind_global_tactile_audio(enabled=True):
    en_flag = "true" if enabled else "false"
    js = f"""
    <script>
    (function() {{
        const parentWin = window.parent;
        const doc = parentWin.document;
        parentWin.__skaAudioEnabled = {en_flag};

        if (!parentWin.__skaAudioEngineReady) {{
            parentWin.__skaAudioEngineReady = true;

            parentWin.__playSkaSound = function(kind) {{
                if (!parentWin.__skaAudioEnabled) return;
                try {{
                    if (!parentWin.__skaAudioCtx) {{
                        parentWin.__skaAudioCtx = new (parentWin.AudioContext || parentWin.webkitAudioContext)();
                    }}
                    const ctx = parentWin.__skaAudioCtx;
                    if (ctx.state === 'suspended') {{
                        ctx.resume();
                    }}
                    const now = ctx.currentTime;
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.connect(gain);
                    gain.connect(ctx.destination);

                    if (kind === 'node') {{
                        // Tocco sui grandi quadrati: switch tattico da console (340Hz -> 680Hz)
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(340, now);
                        osc.frequency.exponentialRampToValueAtTime(680, now + 0.045);
                        gain.gain.setValueAtTime(0.18, now);
                        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.055);
                        osc.start(now);
                        osc.stop(now + 0.055);
                    }} else if (kind === 'action') {{
                        // Tocco sui bottoni azzurri di conferma/firma: doppio impulso cristallino (587Hz -> 880Hz)
                        osc.type = 'triangle';
                        osc.frequency.setValueAtTime(587.33, now);
                        osc.frequency.setValueAtTime(880.0, now + 0.04);
                        gain.gain.setValueAtTime(0.16, now);
                        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.11);
                        osc.start(now);
                        osc.stop(now + 0.11);
                    }} else {{
                        // Tocco su schede, checkbox, menu: micro-click ad alta precisione (1200Hz)
                        osc.type = 'sine';
                        osc.frequency.setValueAtTime(1200, now);
                        osc.frequency.exponentialRampToValueAtTime(450, now + 0.02);
                        gain.gain.setValueAtTime(0.10, now);
                        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.025);
                        osc.start(now);
                        osc.stop(now + 0.025);
                    }}
                }} catch(e) {{}}
            }};

            // Intercetta in tempo reale qualsiasi pressione su bottoni, quadrati, tab e controlli
            doc.addEventListener('pointerdown', function(ev) {{
                const btnPrimary = ev.target.closest('button[kind="primary"]');
                const btnSecondary = ev.target.closest('button[kind="secondary"]');
                const anyInteractive = ev.target.closest('button, [role="tab"], [data-baseweb="select"], input[type="checkbox"], [data-testid="stExpander"] summary');

                if (btnPrimary) {{
                    parentWin.__playSkaSound('node');
                }} else if (btnSecondary) {{
                    parentWin.__playSkaSound('action');
                }} else if (anyInteractive) {{
                    parentWin.__playSkaSound('tick');
                }}
            }}, true);
        }}
    }})();
    </script>
    """
    components.html(js, height=0, width=0)

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

# --- MOTORE GRAFICO CHE INIETTA IL RETINO DI QUADRATINI E I PALLINI BLU NEI PULSANTI TOUCH ---
def inject_matrix_into_touch_cards(cards_payload):
    payload_json = json.dumps(cards_payload)
    js = f"""
    <script>
    (function() {{
        const cards = {payload_json};
        function paintTouchMatrix() {{
            const doc = window.parent.document;
            const buttons = doc.querySelectorAll('button[kind="primary"]');
            buttons.forEach(btn => {{
                const rawText = btn.innerText || "";
                cards.forEach(c => {{
                    if (rawText.includes(c.marker) && !btn.dataset.matrixPainted) {{
                        btn.dataset.matrixPainted = "true";
                        let sqHtml = '';
                        if (c.squares.length === 0) {{
                            for (let i=0; i<4; i++) {{
                                sqHtml += `<span style="display:inline-block;width:15px;height:15px;border-radius:3px;background:#0f172a;border:1.5px solid #334155;"></span>`;
                            }}
                        }} else {{
                            c.squares.forEach(col => {{
                                sqHtml += `<span style="display:inline-block;width:15px;height:15px;border-radius:3px;background:${{col.bg}};border:1.5px solid ${{col.border}};box-shadow:0 0 5px ${{col.bg}}66;"></span>`;
                            }});
                        }}
                        let dotsHtml = '';
                        const totDots = Math.max(c.staff_count, 5);
                        for (let i=0; i<totDots; i++) {{
                            if (i < c.staff_count) {{
                                dotsHtml += `<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#0ea5e9;border:1.5px solid #7dd3fc;box-shadow:0 0 6px #0ea5e988;"></span>`;
                            }} else {{
                                dotsHtml += `<span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#0f172a;border:1.5px solid #1e293b;"></span>`;
                            }}
                        }}
                        btn.innerHTML = `
                        <div style="width:100%;display:flex;flex-direction:column;justify-content:space-between;min-height:126px;text-align:left;pointer-events:none;">
                            <div>
                                <div style="font-family:'Inter',sans-serif;font-size:0.96rem;font-weight:700;color:#ffffff;letter-spacing:0.03em;">${{c.title}}</div>
                                <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#94a3b8;margin-top:2px;">${{c.subtitle}}</div>
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;margin:12px 0;padding:9px 11px;background:#070c15;border:1px solid #1e293b;border-radius:6px;">
                                <div style="display:flex;flex-wrap:wrap;gap:5px;max-width:65%;">${{sqHtml}}</div>
                                <div style="display:flex;flex-wrap:wrap;gap:5px;justify-content:flex-end;max-width:35%;">${{dotsHtml}}</div>
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:0.71rem;color:#cbd5e1;border-top:1px solid #1e293b;padding-top:6px;">
                                <span>STAFF: <b style="color:#38bdf8;">${{c.staff_count}}</b></span>
                                <span>HACCP: <b style="color:${{c.status_color}};">${{c.haccp_txt}}</b></span>
                            </div>
                        </div>
                        `;
                    }}
                }});
            }});
        }}
        paintTouchMatrix();
        setTimeout(paintTouchMatrix, 120);
        setTimeout(paintTouchMatrix, 400);
    }})();
    </script>
    """
    components.html(js, height=0, width=0)

# --- DNA STRUTTURALE E REGISTRO FIRME ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N01", "code": "01", "name": "CASA MADRE", "subtitle": "Laboratorio Pasticceria & Direzione",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni & Sfogliatura", "Uffici Direzione"],
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
            "fridges": [
                {"name": "Frigo Office Piano 1", "kind": "POS"},
                {"name": "Frigo Office Piano 2", "kind": "POS"}
            ]
        },
        {
            "id": "N03", "code": "03", "name": "RICEVIMENTO & HUB", "subtitle": "Front Office & Magazzino Centrale",
            "sub_zones": ["Front Desk", "Magazzino Centrale", "Baia Scarico Fornitori"],
            "fridges": [
                {"name": "Cella Latticini/Salumi", "kind": "POS"},
                {"name": "Cella Ortofrutta +6°C", "kind": "POS"},
                {"name": "Cella Scorte Bevande", "kind": "POS"}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "RISTORANTE & SALE", "subtitle": "Cucina Centrale, Sala Colazioni & 5 Verande",
            "sub_zones": ["Sala Colazioni", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare", "Cucina Centrale"],
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
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"},
                {"name": "Pozzetto Ghiaccio Gazebo", "kind": "NEG"}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "PARCHEGGIO & FLUSSI", "subtitle": "Controllo Accessi, Valet & Sposi",
            "sub_zones": ["Ingresso Principale", "Area Sosta Hotel", "Area Riservata Eventi"],
            "fridges": []
        }
    ]

    haccp_state = {}
    for n in nodes:
        for fr in n["fridges"]:
            key = f"{n['id']} || {fr['name']}"
            haccp_state[key] = {
                "node_id": n["id"], "node_name": n["name"], "fridge_name": fr["name"],
                "status": "PURPLE", "label": "DA CONTROLLARE", "by": "-", "pin": "-", "time": "--:--",
                "kind": fr["kind"]
            }

    haccp_state["N01 || Cella Basi +4°C"].update({"status": "GREEN", "label": "+3.6°C", "by": "Marco S.", "pin": "1001", "time": "06:45"})
    haccp_state["N01 || Cella Semifreddi -18°C"].update({"status": "GREEN", "label": "-19.5°C", "by": "Marco S.", "pin": "1001", "time": "06:46"})
    haccp_state["N04 || Buffet Freddo Colazioni"].update({"status": "GREEN", "label": "+3.9°C", "by": "Jolly 01", "pin": "1004", "time": "06:50"})
    haccp_state["N04 || Vetrina Yogurt/Salumi"].update({"status": "GREEN", "label": "+4.1°C", "by": "Jolly 01", "pin": "1004", "time": "06:51"})
    haccp_state["N04 || Cella Carne +2°C"].update({"status": "GREEN", "label": "+2.4°C", "by": "Jolly 01", "pin": "1004", "time": "06:52"})
    haccp_state["N04 || Cella Pesce 0°C"].update({"status": "YELLOW", "label": "+6.2°C", "by": "Jolly 01", "pin": "1004", "time": "06:55"})

    today_d = datetime.now(timezone(timedelta(hours=1))).strftime("%d/%m/%Y")
    haccp_logs = [
        {"date": today_d, "time": "06:45", "window": "MATTINA", "node": "01 // CASA MADRE", "fridge": "Cella Basi +4°C", "temp": "+3.6°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:46", "window": "MATTINA", "node": "01 // CASA MADRE", "fridge": "Cella Semifreddi -18°C", "temp": "-19.5°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:50", "window": "MATTINA", "node": "04 // RISTORANTE & SALE", "fridge": "Buffet Freddo Colazioni", "temp": "+3.9°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:51", "window": "MATTINA", "node": "04 // RISTORANTE & SALE", "fridge": "Vetrina Yogurt/Salumi", "temp": "+4.1°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:52", "window": "MATTINA", "node": "04 // RISTORANTE & SALE", "fridge": "Cella Carne +2°C", "temp": "+2.4°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:55", "window": "MATTINA", "node": "04 // RISTORANTE & SALE", "fridge": "Cella Pesce 0°C", "temp": "+6.2°C", "outcome": "PRE-ALLARME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"}
    ]

    return {
        "nodes": nodes,
        "haccp_state": haccp_state,
        "haccp_logs": haccp_logs,
        "force_remind_demo": False,
        "figurine": [
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante Piani", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Giulia F.", "role": "Ricevimento / Magazzino", "index_cost": 95, "node_id": "N03", "sub_zone": "Front Desk", "shift": "Mattina (07-15)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Maître Verande", "index_cost": 110, "node_id": "N04", "sub_zone": "Sala Colazioni", "shift": "Mattina (07-15)"},
            {"pin": "1007", "nick": "Matteo B.", "role": "Chef de Rang", "index_cost": 95, "node_id": "N04", "sub_zone": "Veranda 1", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Extra A", "role": "Barman", "index_cost": 90, "node_id": "N05", "sub_zone": "Banco Caffetteria", "shift": "Mattina (07-15)"},
            {"pin": "1006", "nick": "DJ / Evento", "role": "Regia Gazebo", "index_cost": 150, "node_id": "N06", "sub_zone": "Gazebo Cerimonie", "shift": "Cena/Sera (18-02)"}
        ],
        "sos_queue": [
            {"time": "06:52", "node_id": "N04", "from": "04. Ristorante (Sala Colazioni)", "item": "2 Vassoi Cornetti + Latte Senza Lattosio", "status": "In corso"}
        ],
        "events": [
            {"id": "EV1", "title": "Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "phase": "2. Aperitivo"}
        ],
        "alarm_counter": 0
    }

store = get_shared_store()

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None
if "active_pin" not in st.session_state:
    st.session_state.active_pin = "9999"

now_it = get_italy_now()
now_str = now_it.strftime("%H:%M")
today_str = now_it.strftime("%d/%m/%Y")
win_name, deadline_str, is_naturally_overdue = get_current_window_info(now_it)
is_overdue = is_naturally_overdue or store["force_remind_demo"]

unchecked_list = [v for v in store["haccp_state"].values() if v["status"] == "PURPLE"]
total_fridges = len(store["haccp_state"])
checked_fridges = total_fridges - len(unchecked_list)

# --- INTESTAZIONE CON OROLOGIO LIVE ---
st.markdown(f"""
<div class="top-bar">
    <div class="brand-title">SOVEREIGN KINETIC ARCHITECTURE <span>// BOSCHETTO PRO</span></div>
    <div class="brand-clock">🕒 ORA SISTEMA: {now_str}  |  FASCIA: {win_name} (LIMITE: {deadline_str})</div>
</div>
""", unsafe_allow_html=True)

c_pin, c_btn, c_dir, c_sim, c_sonar = st.columns([1.1, 1.0, 1.0, 1.3, 1.0])
with c_pin:
    new_pin = st.text_input("PIN ACCESSO", value=st.session_state.active_pin, label_visibility="collapsed", placeholder="PIN (9999 Dir. | 1001 Staff)")
with c_btn:
    if st.button("CONFERMA PIN ↵", type="secondary", use_container_width=True) or (new_pin != st.session_state.active_pin):
        st.session_state.active_pin = new_pin.strip()
        st.session_state.selected_node_id = None
        play_tactical_sonar("ping")
        st.rerun()
with c_dir:
    if st.button("PLANCIA 9999 🏛️", type="secondary", use_container_width=True):
        st.session_state.active_pin = "9999"
        st.session_state.selected_node_id = None
        play_tactical_sonar("ping")
        st.rerun()
with c_sim:
    store["force_remind_demo"] = st.toggle("⏰ SIMULA SCADENZA FRIGHI", value=store["force_remind_demo"])
with c_sonar:
    # ATTIVO DI DEFAULT: SUONA AD OGNI PRESSIONE SUI TASTI E SUI BLOCCHI!
    sonar_active = st.toggle("🔊 AUDIO TASTI & SONAR", value=True)

# Attiva il sintetizzatore globale su tutti i tasti della pagina
bind_global_tactile_audio(sonar_active)

pin_input = st.session_state.active_pin

# ==============================================================================
# VISTA 1: DIREZIONE (PIN 9999) — PLANCIA TOUCH CON RETINO QUADRATINI E PALLINI BLU
# ==============================================================================
if pin_input in ["9999", "0000"]:
    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='alert-bar-crit'>🚨 ALLARME ROSSO GUASTO/TEMPERATURA: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if unchecked_list and is_overdue:
        missing_nodes = sorted(list(set(v["node_id"] for v in unchecked_list)))
        st.markdown(
            f"<div class='alert-bar-remind'>⏰ <b>REMIND CONTROLLO FRIGHI SCADUTO (Limite ore {deadline_str} superato):</b> "
            f"Ci sono ancora <b>{len(unchecked_list)} frigoriferi non controllati</b> nei reparti: {', '.join(missing_nodes)}.</div>",
            unsafe_allow_html=True
        )

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        st.markdown(f"<div class='alert-bar-sos'>📦 SOS MAGAZZINO ({len(store['sos_queue'])}) — {latest_sos['from']} [ore {latest_sos['time']}]: {latest_sos['item']}</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA COSTELLAZIONE TOUCH CON RETINO GRAFICO INTERNO
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_ev = len(store["events"])

        st.markdown(f"""
        <div class="kpi-bar">
            <div class="kpi-box"><div class="kpi-lbl">Controlli HACCP ({win_name.split()[0]})</div><div class="kpi-num">{checked_fridges}/{total_fridges} FIRMATI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Presidio Staff (Pallini Blu)</div><div class="kpi-num">{tot_fig} UNITA ATTIVE</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Richieste Magazzino</div><div class="kpi-num">{tot_sos} SOS APERTI</div></div>
            <div class="kpi-box"><div class="kpi-lbl">Regia Eventi & Stampa</div><div class="kpi-num">{len(store['haccp_logs'])} FIRME REGISTRATE</div></div>
        </div>
        """, unsafe_allow_html=True)

        row1 = st.columns(4)
        row2 = st.columns(4)
        grid_cols = row1 + row2

        color_palette = {
            "GREEN":   {"bg": "#10b981", "border": "#34d399"},
            "PURPLE":  {"bg": "#6b21a8", "border": "#a855f7"},
            "OVERDUE": {"bg": "#ea580c", "border": "#fbbf24"},
            "YELLOW":  {"bg": "#eab308", "border": "#fde047"},
            "RED":     {"bg": "#ef4444", "border": "#fca5a5"}
        }

        cards_payload = []

        for idx, node in enumerate(store["nodes"]):
            nid = node["id"]
            n_staff = len([f for f in store["figurine"] if f["node_id"] == nid])
            n_fridges = [v for v in store["haccp_state"].values() if v["node_id"] == nid]

            squares = []
            for f in n_fridges:
                if f["status"] == "PURPLE" and is_overdue:
                    squares.append(color_palette["OVERDUE"])
                else:
                    squares.append(color_palette[f["status"]])

            n_unchecked = sum(1 for f in n_fridges if f["status"] == "PURPLE")
            n_anom = sum(1 for f in n_fridges if f["status"] in ["YELLOW", "RED"])

            if not n_fridges:
                haccp_txt = "NO FRIGHI"
                st_col = "#94a3b8"
            elif n_anom > 0:
                haccp_txt = f"{n_anom} ANOMALIA"
                st_col = "#fbbf24"
            elif n_unchecked > 0 and is_overdue:
                haccp_txt = f"REMIND ({n_unchecked})"
                st_col = "#fb923c"
            elif n_unchecked > 0:
                haccp_txt = f"{len(n_fridges)-n_unchecked}/{len(n_fridges)} ATTIVO"
                st_col = "#c084fc"
            else:
                haccp_txt = "100% OK"
                st_col = "#34d399"

            marker = f"{node['code']} // {node['name']}"
            cards_payload.append({
                "marker": marker,
                "title": marker,
                "subtitle": node["subtitle"],
                "squares": squares,
                "staff_count": n_staff,
                "haccp_txt": haccp_txt,
                "status_color": st_col
            })

            with grid_cols[idx]:
                if st.button(f"{marker}\n{node['subtitle']}", key=f"tile_{nid}", type="primary", use_container_width=True):
                    st.session_state.selected_node_id = nid
                    st.rerun()

        marker_08 = "08 // REGIA, IMPOSTAZIONI & STAMPA"
        cards_payload.append({
            "marker": marker_08,
            "title": marker_08,
            "subtitle": "Frigoriferi, Staff, Eventi & Stampa Registro ASL",
            "squares": [{"bg": "#0284c7", "border": "#38bdf8"} for _ in range(4)],
            "staff_count": tot_fig,
            "haccp_txt": f"{len(store['haccp_logs'])} FIRME",
            "status_color": "#38bdf8"
        })
        with grid_cols[7]:
            if st.button(f"{marker_08}\nConfigurazione & Stampe", key="tile_HUB", type="primary", use_container_width=True):
                st.session_state.selected_node_id = "HUB_VAULT"
                st.rerun()

        inject_matrix_into_touch_cards(cards_payload)

    # --------------------------------------------------------------------------
    # VISTA 08: IMPOSTAZIONI STRUTTURA + STAMPA REGISTRO UFFICIALE ASL
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "HUB_VAULT":
        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown("### 08 // IMPOSTAZIONI STRUTTURA, EVENTI & STAMPA REGISTRO UFFICIALE ASL")

        tab_print, tab_fr, tab_staff, tab_ev = st.tabs([
            "🖨️ 1. STAMPA REGISTRO ASL (ORARI E FIRME)",
            "❄️ 2. CONFIGURA FRIGORIFERI",
            "👥 3. GESTIONE DIPENDENTI & PIN",
            "🥂 4. AGENDA EVENTI"
        ])

        with tab_print:
            st.markdown("##### 📋 REGISTRO CRONOLOGICO FIRME E ORARI HACCP (VALIDAZIONE TRAMITE PIN PERSONALE)")
            st.caption("Ogni lettura registrata dagli operatori viene timbrata con l'ora esatta di sistema e la firma elettronica associata al PIN individuale.")

            rows_html = ""
            for log in reversed(store["haccp_logs"]):
                rows_html += (
                    f"<tr>"
                    f"<td>{log['date']}</td>"
                    f"<td><b>{log['time']}</b></td>"
                    f"<td>{log['window']}</td>"
                    f"<td>{log['node']}</td>"
                    f"<td>{log['fridge']}</td>"
                    f"<td><b>{log['temp']}</b></td>"
                    f"<td>{log['outcome']}</td>"
                    f"<td><b>{log['operator']}</b></td>"
                    f"<td>{log['pin_sig']}</td>"
                    f"</tr>"
                )
            st.markdown(f"""
            <table class="log-table">
                <thead>
                    <tr>
                        <th>DATA</th><th>ORA ESATTA</th><th>FASCIA</th><th>REPARTO</th>
                        <th>UNITÀ FRIGORIFERA</th><th>TEMP.</th><th>ESITO</th><th>OPERATORE</th><th>FIRMA ELETTRONICA</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
            """, unsafe_allow_html=True)

            st.divider()
            printable_html = f"""
            <html><head><meta charset="utf-8"><title>Registro HACCP - Boschetto Pro</title>
            <style>
                body {{ font-family: Arial, sans-serif; color: #000; padding: 25px; }}
                h2 {{ margin-bottom: 4px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 12px; }}
                th, td {{ border: 1px solid #000; padding: 6px 8px; text-align: left; }}
                th {{ background: #eee; }}
                .sig-box {{ margin-top: 35px; display: flex; justify-content: space-between; font-size: 13px; }}
            </style></head><body>
            <h2>REGISTRO UFFICIALE AUTOCONTROLLO TEMPERATURE HACCP</h2>
            <div><b>Struttura:</b> BOSCHETTO PRO  |  <b>Data Emissione:</b> {today_str} ore {now_str}</div>
            <table>
                <thead><tr><th>Data</th><th>Ora Sistema</th><th>Fascia</th><th>Reparto</th><th>Frigorifero</th><th>Temp.</th><th>Esito</th><th>Firmatario</th><th>Certificazione PIN</th></tr></thead>
                <tbody>{rows_html}</tbody>
            </table>
            <div class="sig-box">
                <div><b>Sistema Digitale:</b> S.K.A. // Boschetto Pro (Orario Certificato)</div>
                <div><b>Timbro e Firma Responsabile HACCP:</b> _______________________________</div>
            </div>
            </body></html>
            """

            csv_buffer = io.StringIO()
            writer = csv.DictWriter(csv_buffer, fieldnames=["date", "time", "window", "node", "fridge", "temp", "outcome", "operator", "pin_sig"])
            writer.writeheader()
            writer.writerows(store["haccp_logs"])

            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                st.download_button(
                    "🖨️ SCARICA MODULO PRONTO STAMPA ASL (.HTML)",
                    data=printable_html,
                    file_name=f"REGISTRO_STAMPA_HACCP_{now_it.strftime('%Y%m%d')}.html",
                    mime="text/html",
                    use_container_width=True
                )
            with cp2:
                st.download_button(
                    "📊 SCARICA FOGLIO EXCEL / CSV (.CSV)",
                    data=csv_buffer.getvalue(),
                    file_name=f"REGISTRO_HACCP_{now_it.strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with cp3:
                if st.button("🔄 INIZIA NUOVO GIRO (RIPORTA QUADRETTI IN VIOLA)", type="secondary", use_container_width=True):
                    for k in store["haccp_state"]:
                        store["haccp_state"][k].update({"status": "PURPLE", "label": "DA CONTROLLARE", "by": "-", "pin": "-", "time": "--:--"})
                    st.rerun()

        with tab_fr:
            st.markdown("##### ➕ AGGIUNGI O RIMUOVI FRIGORIFERI IN AUTONOMIA")
            cf1, cf2, cf3 = st.columns(3)
            node_map = {f"{n['code']} - {n['name']}": n for n in store["nodes"]}
            fr_node_lbl = cf1.selectbox("Scegli Reparto", list(node_map.keys()))
            target_node = node_map[fr_node_lbl]
            fr_new_name = cf2.text_input("Nome Frigorifero (es. Frigo Vini Veranda 2)")
            fr_new_kind = cf3.selectbox("Tipo Temperatura", ["POS (+0°C / +5°C)", "NEG (-18°C / -22°C)"])

            if st.button("AGGIUNGI FRIGORIFERO AL REPARTO", type="secondary"):
                if fr_new_name:
                    k_code = "POS" if "POS" in fr_new_kind else "NEG"
                    target_node["fridges"].append({"name": fr_new_name.strip(), "kind": k_code})
                    store["haccp_state"][f"{target_node['id']} || {fr_new_name.strip()}"] = {
                        "node_id": target_node["id"], "node_name": target_node["name"],
                        "fridge_name": fr_new_name.strip(),
                        "status": "PURPLE", "label": "DA CONTROLLARE", "by": "-", "pin": "-", "time": "--:--",
                        "kind": k_code
                    }
                    st.rerun()

            st.divider()
            for idx_fr, fr_item in enumerate(target_node["fridges"]):
                c_l, c_b = st.columns([4, 1])
                c_l.markdown(f"- **{fr_item['name']}** (`{fr_item['kind']}`)")
                if c_b.button("Elimina", key=f"del_fr_{target_node['id']}_{idx_fr}"):
                    removed = target_node["fridges"].pop(idx_fr)
                    store["haccp_state"].pop(f"{target_node['id']} || {removed['name']}", None)
                    st.rerun()

        with tab_staff:
            st.markdown("##### ➕ CREA NUOVO DIPENDENTE E ASSEGNA PIN PERSONALE DI FIRMA")
            cs1, cs2, cs3 = st.columns(3)
            ns_nick = cs1.text_input("Nome e Cognome / Nickname (es. Matteo B.)")
            ns_role = cs2.text_input("Mansione (es. Chef de Rang)")
            ns_pin = cs3.text_input("PIN Personale a 4 cifre (es. 1008)")

            cs4, cs5, cs6 = st.columns(3)
            ns_node_label = cs4.selectbox("Reparto", list(node_map.keys()), key="staff_node_sel")
            chosen_node = node_map[ns_node_label]
            ns_sub = cs5.selectbox("Sottozona", chosen_node["sub_zones"])
            ns_shift = cs6.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)"])

            if st.button("ATTIVA DIPENDENTE E ABILITA FIRMA PIN", type="secondary"):
                if ns_nick and ns_pin:
                    store["figurine"].append({
                        "pin": ns_pin.strip(), "nick": ns_nick.strip(), "role": ns_role.strip() or "Operatore",
                        "index_cost": 100, "node_id": chosen_node["id"], "sub_zone": ns_sub, "shift": ns_shift
                    })
                    st.rerun()

            st.divider()
            for idx_f, f in enumerate(store["figurine"]):
                cf1, cf2 = st.columns([4, 1])
                cf1.markdown(f"- **PIN `{f['pin']}`** — **{f['nick']}** ({f['role']})  |  Reparto: `{f['node_id']}` ({f['sub_zone']})")
                if cf2.button("Rimuovi", key=f"rm_fig_{f['pin']}_{idx_f}"):
                    store["figurine"].pop(idx_f)
                    st.rerun()

        with tab_ev:
            phase_options = ["1. Accoglienza / Rito", "2. Aperitivo", "3. Servito", "4. Alert Pasticceria: Fuori Torta!", "5. Open Bar & Musica"]
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
            ne_title = ce1.text_input("Nuovo Evento (es. Matrimonio Neri)")
            ne_zone = ce2.selectbox("Location", ["Gazebo -> Veranda Circolare", "Veranda Grande", "Veranda 1", "Veranda 2", "Sala Interna"])
            ne_pax = ce3.number_input("Ospiti (Pax)", min_value=1, value=60, step=5)
            ne_cake = ce4.text_input("Orario Torta", value="22:45")
            if st.button("AGGIUNGI EVENTO", type="secondary"):
                if ne_title:
                    store["events"].append({"id": f"EV{int(datetime.now().timestamp())}", "title": ne_title, "zone": ne_zone, "pax": ne_pax, "cake_time": ne_cake, "phase": "1. Accoglienza / Rito"})
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

        col_haccp, col_ops = st.columns([1.6, 1.4])

        with col_haccp:
            st.markdown(f"##### DETTAGLIO FRIGORIFERI — FASCIA {win_name} (Ora Sistema: {now_str})")
            st.caption("VIOLA: Da Controllare  |  ARANCIO: In Ritardo (Remind!)  |  VERDE: Regolare  |  GIALLO: Pre-Allarme  |  ROSSO: Guasto")
            node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
            if not node_fridges:
                st.caption("Nessuna unità frigorifera in questo reparto.")
            else:
                tiles_html = "<div class='haccp-grid'>"
                for st_data in node_fridges:
                    if st_data["status"] == "PURPLE" and is_overdue:
                        css_class = "tile-overdue"
                        val_txt = "⏰ IN RITARDO!"
                    else:
                        css_class = {"PURPLE": "tile-purple", "GREEN": "tile-green", "YELLOW": "tile-yellow", "RED": "tile-red"}[st_data["status"]]
                        val_txt = st_data["label"]

                    tiles_html += (
                        f"<div class='haccp-tile {css_class}'>"
                        f"<div class='tile-title'>{st_data['fridge_name']}</div>"
                        f"<div class='tile-val'>{val_txt}</div>"
                        f"<div class='tile-meta'><span>🕒 {st_data['time']}</span><span>✍️ {st_data['by']}</span></div>"
                        f"</div>"
                    )
                tiles_html += "</div>"
                st.markdown(tiles_html, unsafe_allow_html=True)

        with col_ops:
            st.markdown("##### PRESIDIO STAFF NEL REPARTO (PALLINI BLU)")
            for f in [f for f in store["figurine"] if f["node_id"] == nid]:
                st.markdown(f"- 🔵 **{f['nick']}** ({f['role']}) — Zona: `{f['sub_zone']}` | Turno: `{f['shift']}` | Firma: `PIN #{f['pin']}`")

            with st.expander("Sposta Operatore in questo Reparto"):
                pick_fig = st.selectbox("Operatore", [f["nick"] for f in store["figurine"]])
                pick_sub = st.selectbox("Sottozona", node["sub_zones"])
                pick_sh = st.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)"])
                if st.button("Conferma Spostamento", type="secondary"):
                    for f in store["figurine"]:
                        if f["nick"] == pick_fig:
                            f["node_id"] = nid
                            f["sub_zone"] = pick_sub
                            f["shift"] = pick_sh
                    st.rerun()

            node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]
            if node_sos:
                st.divider()
                st.markdown("##### RICHIESTE SOS MAGAZZINO")
                for req in node_sos:
                    st.warning(f"Ore {req['time']} — {req['item']}")
                if st.button("Segna SOS come Evasi", type="secondary", use_container_width=True):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()

# ==============================================================================
# VISTA 2: TERMINALE OPERATORE TOUCH (PIN 1001, 1004...) CON FIRMA CERTIFICATA
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error(f"PIN '{pin_input}' non riconosciuto. Tocca 'PLANCIA 9999' in alto per tornare in Direzione.")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.success(f"OPERATORE IDENTIFICATO: {user['nick']} ({user['role']})  |  FIRMA ELETTRONICA: PIN #{user['pin']}  |  ORA: {now_str}")

        my_fridges = [k for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"]]
        my_unchecked = [v["fridge_name"] for k, v in store["haccp_state"].items() if v["node_id"] == user["node_id"] and v["status"] == "PURPLE"]

        if my_unchecked:
            if is_overdue:
                st.markdown(
                    f"<div class='alert-bar-remind'>⏰ <b>REMIND URGENTE PER {user['nick'].upper()} — CONTROLLO FRIGHI IN RITARDO!</b><br>"
                    f"Unità da firmare subito: <b>{', '.join(my_unchecked)}</b></div>",
                    unsafe_allow_html=True
                )
            else:
                st.info(f"📋 Frigoriferi da controllare entro le ore {deadline_str}: {', '.join(my_unchecked)}")
        elif my_fridges:
            st.success("✔️ Tutti i frigoriferi del tuo reparto sono stati firmati in questa fascia oraria!")

        if my_fridges:
            st.markdown(f"##### 1. RILEVAZIONE E FIRMA ELETTRONICA TEMPERATURA (Orario Certificato: {now_str})")
            sel_key = st.selectbox("Seleziona Unità Frigorifera", my_fridges, format_func=lambda x: f"{x.split(' || ')[1]}  [{store['haccp_state'][x]['label']} - ore {store['haccp_state'][x]['time']}]")
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura Letta sul Display (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("Segnala Anomalia / Frigorifero GUASTO")
            confirm_check = st.checkbox(f"✔️ Dichiaro di aver verificato visivamente il display (Firma Elettronica: {user['nick']} - PIN #{user['pin']})", value=True)

            if st.button(f"✍️ APPLICA FIRMA E TIMBRA ORE {now_str}", type="secondary", use_container_width=True):
                if not confirm_check:
                    st.warning("Spunta la casella di conferma visiva prima di applicare la firma.")
                else:
                    status_color, label_text = evaluate_fridge_status(fr_info["kind"], temp_val, is_broken)
                    outcome_map = {"GREEN": "CONFORME", "YELLOW": "PRE-ALLARME", "RED": "CRITICO/GUASTO"}
                    fr_info.update({
                        "status": status_color,
                        "label": label_text,
                        "by": user["nick"],
                        "pin": user["pin"],
                        "time": now_str
                    })
                    store["haccp_logs"].append({
                        "date": today_str,
                        "time": now_str,
                        "window": win_name.split()[0],
                        "node": f"{user_node['code']} // {user_node['name']}",
                        "fridge": fr_info["fridge_name"],
                        "temp": label_text,
                        "outcome": outcome_map[status_color],
                        "operator": user["nick"],
                        "pin_sig": f"PIN #{user['pin']} (Verificato)"
                    })
                    if status_color in ["RED", "YELLOW"]:
                        store["alarm_counter"] += 1
                    play_tactical_sonar("ping")
                    st.toast(f"Firmato da {user['nick']} alle {now_str}: {label_text}")
                    st.rerun()

        st.divider()
        st.markdown("##### 2. RICHIESTA URGENTE MAGAZZINO (SOS)")
        sos_item = st.text_input("Cosa manca nel reparto?")
        if st.button(f"INVIA SOS MAGAZZINO (ORE {now_str})", type="secondary", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": now_str,
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']}. {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                play_tactical_sonar("ping")
                st.toast("SOS inviato!")
                st.rerun()
