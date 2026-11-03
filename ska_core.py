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

# --- CSS ARCHITETTONICO CON COLONNA VERTICALE DESTRA E GRIGLIA SIMMETRICA ---
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
    padding-top: 1.4rem !important;
    padding-bottom: 2rem !important;
    max-width: 1460px !important;
}

.top-bar {
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
    margin-bottom: 12px;
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

/* GRANDE RETTANGOLO VERTICALE DI RIEPILOGO A DESTRA */
.right-tower {
    background: linear-gradient(180deg, #0d1524 0%, #09101d 100%);
    border: 1.5px solid #1e3a5f;
    border-top: 3px solid #38bdf8;
    border-radius: 8px;
    padding: 18px 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
}
.tower-header {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e293b;
    padding-bottom: 10px;
    margin-bottom: 14px;
}
.tower-item {
    background: #070c15;
    border: 1px solid #1e293b;
    border-left: 3px solid #38bdf8;
    border-radius: 6px;
    padding: 12px 14px;
    margin-bottom: 12px;
}
.tower-lbl {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #94a3b8;
    text-transform: uppercase;
}
.tower-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-top: 3px;
}
.tower-sub {
    font-family: 'Inter', sans-serif;
    font-size: 0.72rem;
    color: #64748b;
    margin-top: 3px;
}
.tower-legend {
    margin-top: 14px;
    padding-top: 12px;
    border-top: 1px solid #1e293b;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.70rem;
    color: #cbd5e1;
    line-height: 1.8;
}

/* BANNER ALLERTE CRITICHE E SOS */
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

/* GRANDI QUADRATI TOUCH: ALTEZZA IDENTICA BLOCCATA A 154px */
div.stButton > button[kind="primary"] {
    background: linear-gradient(160deg, #0d1524 0%, #111c30 100%) !important;
    border: 1.5px solid #1e3a5f !important;
    border-top: 2.5px solid #38bdf8 !important;
    border-radius: 8px !important;
    height: 154px !important;
    min-height: 154px !important;
    max-height: 154px !important;
    width: 100% !important;
    padding: 12px 15px !important;
    text-align: left !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: space-between !important;
    align-items: stretch !important;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.45) !important;
    margin-bottom: 6px !important;
    cursor: pointer !important;
    user-select: none !important;
    overflow: hidden !important;
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
    .haccp-tile { width: 48% !important; }
}
</style>
""", unsafe_allow_html=True)

# --- MOTORE AUDIO TATTICO COMPATIBILE CON ANDROID / iOS / DESKTOP ---
def bind_global_tactile_audio(enabled=True):
    en_flag = "true" if enabled else "false"
    js = f"""
    <script>
    (function() {{
        const parentWin = window.parent;
        const doc = parentWin.document;
        parentWin.__skaAudioEnabled = {en_flag};

        parentWin.__ensureMobileAudioUnlocked = function() {{
            if (!parentWin.__skaAudioCtx) {{
                const AudioCtx = parentWin.AudioContext || parentWin.webkitAudioContext;
                if (AudioCtx) {{
                    parentWin.__skaAudioCtx = new AudioCtx();
                }}
            }}
            const ctx = parentWin.__skaAudioCtx;
            if (ctx && ctx.state === 'suspended') {{
                ctx.resume();
            }}
            return ctx;
        }};

        parentWin.__playSkaSound = function(kind) {{
            if (!parentWin.__skaAudioEnabled) return;
            try {{
                const ctx = parentWin.__ensureMobileAudioUnlocked();
                if (!ctx) return;

                if (parentWin.navigator && parentWin.navigator.vibrate) {{
                    parentWin.navigator.vibrate(kind === 'node' ? 20 : 12);
                }}

                const now = ctx.currentTime;
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);

                if (kind === 'node') {{
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(440, now);
                    osc.frequency.exponentialRampToValueAtTime(880, now + 0.065);
                    gain.gain.setValueAtTime(0.35, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.085);
                    osc.start(now);
                    osc.stop(now + 0.085);
                }} else if (kind === 'action') {{
                    osc.type = 'triangle';
                    osc.frequency.setValueAtTime(587.33, now);
                    osc.frequency.setValueAtTime(880.0, now + 0.05);
                    gain.gain.setValueAtTime(0.35, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
                    osc.start(now);
                    osc.stop(now + 0.14);
                }} else {{
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(1100, now);
                    osc.frequency.exponentialRampToValueAtTime(520, now + 0.035);
                    gain.gain.setValueAtTime(0.28, now);
                    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.045);
                    osc.start(now);
                    osc.stop(now + 0.045);
                }}
            }} catch(e) {{}}
        }};

        if (!parentWin.__skaAudioEngineReady) {{
            parentWin.__skaAudioEngineReady = true;

            ['touchstart', 'touchend', 'click'].forEach(function(evtName) {{
                doc.addEventListener(evtName, function() {{
                    parentWin.__ensureMobileAudioUnlocked();
                }}, {{ passive: true, capture: true }});
            }});

            doc.addEventListener('click', function(ev) {{
                const btnPrimary = ev.target.closest('button[kind="primary"]');
                const btnSecondary = ev.target.closest('button[kind="secondary"]');
                const anyInteractive = ev.target.closest('button, [role="tab"], [data-baseweb="select"], input[type="checkbox"], [data-testid="stExpander"] summary');

                if (btnPrimary) {{
                    parentWin.sessionStorage.setItem('__skaPendingSound', 'node');
                    parentWin.__playSkaSound('node');
                }} else if (btnSecondary) {{
                    parentWin.sessionStorage.setItem('__skaPendingSound', 'action');
                    parentWin.__playSkaSound('action');
                }} else if (anyInteractive) {{
                    parentWin.__playSkaSound('tick');
                }}
            }}, true);
        }}

        const pending = parentWin.sessionStorage.getItem('__skaPendingSound');
        if (pending) {{
            parentWin.sessionStorage.removeItem('__skaPendingSound');
            setTimeout(function() {{
                parentWin.__playSkaSound(pending);
            }}, 40);
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

# --- MOTORE GRAFICO CON GEOMETRIA IDENTICA PER TUTTI I 10 QUADRATI ---
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
                    if (rawText.includes(c.marker)) {{
                        let sqHtml = '';
                        if (c.squares.length === 0) {{
                            for (let i=0; i<3; i++) {{
                                sqHtml += `<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:#0f172a;border:1.5px solid #334155;"></span>`;
                            }}
                        }} else {{
                            c.squares.forEach(col => {{
                                sqHtml += `<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:${{col.bg}};border:1.5px solid ${{col.border}};box-shadow:0 0 5px ${{col.bg}}66;"></span>`;
                            }});
                        }}
                        let dotsHtml = '';
                        const totDots = Math.max(c.staff_count, 4);
                        for (let i=0; i<totDots; i++) {{
                            if (i < c.staff_count) {{
                                dotsHtml += `<span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:#0ea5e9;border:1.5px solid #7dd3fc;box-shadow:0 0 6px #0ea5e988;"></span>`;
                            }} else {{
                                dotsHtml += `<span style="display:inline-block;width:11px;height:11px;border-radius:50%;background:#0f172a;border:1.5px solid #1e293b;"></span>`;
                            }}
                        }}
                        btn.innerHTML = `
                        <div style="width:100%;height:126px;display:flex;flex-direction:column;justify-content:space-between;text-align:left;pointer-events:none;">
                            <div>
                                <div style="font-family:'Inter',sans-serif;font-size:0.92rem;font-weight:700;color:#ffffff;letter-spacing:0.03em;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${{c.title}}</div>
                                <div style="font-family:'Inter',sans-serif;font-size:0.72rem;color:#94a3b8;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">${{c.subtitle}}</div>
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 10px;background:#070c15;border:1px solid #1e293b;border-radius:6px;min-height:38px;">
                                <div style="display:flex;flex-wrap:wrap;gap:4px;max-width:65%;">${{sqHtml}}</div>
                                <div style="display:flex;flex-wrap:wrap;gap:4px;justify-content:flex-end;max-width:35%;">${{dotsHtml}}</div>
                            </div>
                            <div style="display:flex;justify-content:space-between;align-items:center;font-family:'JetBrains Mono',monospace;font-size:0.69rem;color:#cbd5e1;border-top:1px solid #1e293b;padding-top:5px;">
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
        setTimeout(paintTouchMatrix, 100);
        setTimeout(paintTouchMatrix, 350);
    }})();
    </script>
    """
    components.html(js, height=0, width=0)

# --- NUOVA ARCHITETTURA UFFICIALE A 10 BLOCCHI (00 -> 09) ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N00", "code": "00", "name": "DIREZIONE", "subtitle": "Ufficio Direzionale & Slot Strategico",
            "sub_zones": ["Ufficio Direzione", "Amministrazione", "Controllo Gestione"],
            "fridges": []
        },
        {
            "id": "N01", "code": "01", "name": "PASTICCERIA", "subtitle": "Laboratorio Pasticceria & Forni",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni & Sfogliatura"],
            "fridges": [
                {"name": "Cella Basi +4°C", "kind": "POS"},
                {"name": "Cella Semifreddi -18°C", "kind": "NEG"},
                {"name": "Abbattitore Lab", "kind": "NEG"},
                {"name": "Vetrina Torte +4°C", "kind": "POS"}
            ]
        },
        {
            "id": "N02", "code": "02", "name": "CAMERE", "subtitle": "Piani, Camere & Housekeeping",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria"],
            "fridges": [
                {"name": "Frigo Office Piano 1", "kind": "POS"},
                {"name": "Frigo Office Piano 2", "kind": "POS"}
            ]
        },
        {
            "id": "N03", "code": "03", "name": "RECEPTION", "subtitle": "Front Office, Accoglienza & Hub",
            "sub_zones": ["Front Desk", "Magazzino Centrale", "Scarico Fornitori"],
            "fridges": [
                {"name": "Cella Latticini/Salumi", "kind": "POS"},
                {"name": "Cella Ortofrutta +6°C", "kind": "POS"},
                {"name": "Cella Scorte Bevande", "kind": "POS"}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "SALA COLAZIONI", "subtitle": "Buffet Mattutino & Caffetteria Sala",
            "sub_zones": ["Buffet Centrale", "Sala Colazioni Interna", "Veranda Colazioni"],
            "fridges": [
                {"name": "Buffet Freddo Colazioni", "kind": "POS"},
                {"name": "Vetrina Yogurt & Latte", "kind": "POS"},
                {"name": "Vetrina Salumi & Formaggi", "kind": "POS"}
            ]
        },
        {
            "id": "N05", "code": "05", "name": "RISTORANTE", "subtitle": "Cucina Centrale & 5 Verande",
            "sub_zones": ["Cucina Centrale", "Sala Interna", "Veranda 1", "Veranda 2", "Veranda Grande", "Veranda Circolare"],
            "fridges": [
                {"name": "Cella Carne +2°C", "kind": "POS"},
                {"name": "Cella Pesce 0°C", "kind": "POS"},
                {"name": "Congelatore Stoccaggio", "kind": "NEG"},
                {"name": "Abbattitore Cucina", "kind": "NEG"},
                {"name": "Frigo Linea Antipasti", "kind": "POS"},
                {"name": "Frigo Linea Primi/Sec.", "kind": "POS"}
            ]
        },
        {
            "id": "N06", "code": "06", "name": "BAR", "subtitle": "Terrazza Bar, Caffetteria & Gelateria",
            "sub_zones": ["Banco Caffetteria", "Terrazza Bar", "Cocktail Station"],
            "fridges": [
                {"name": "Banco Bar 1 (Latte)", "kind": "POS"},
                {"name": "Banco Bar 2 (Birre/Vini)", "kind": "POS"},
                {"name": "Vetrina Gelati -16°C", "kind": "NEG"},
                {"name": "Pozzetto Ghiaccio Bar", "kind": "NEG"}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "SPIAGGIA", "subtitle": "Stabilimento Balneare & Gazebo",
            "sub_zones": ["Gazebo Cerimonie", "Ombrelloni & Tende", "Chiosco Spiaggia"],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"}
            ]
        },
        {
            "id": "N08", "code": "08", "name": "PARCHEGGIO", "subtitle": "Viabilità, Accessi & Area Sposi",
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
        {"date": today_d, "time": "06:45", "window": "MATTINA", "node": "01 - PASTICCERIA", "fridge": "Cella Basi +4°C", "temp": "+3.6°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:46", "window": "MATTINA", "node": "01 - PASTICCERIA", "fridge": "Cella Semifreddi -18°C", "temp": "-19.5°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:50", "window": "MATTINA", "node": "04 - SALA COLAZIONI", "fridge": "Buffet Freddo Colazioni", "temp": "+3.9°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:51", "window": "MATTINA", "node": "04 - SALA COLAZIONI", "fridge": "Vetrina Yogurt & Latte", "temp": "+4.1°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:52", "window": "MATTINA", "node": "05 - RISTORANTE", "fridge": "Cella Carne +2°C", "temp": "+2.4°C", "outcome": "CONFORME", "operator": "Matteo B.", "pin_sig": "PIN #1005 (Verificato)"},
        {"date": today_d, "time": "06:55", "window": "MATTINA", "node": "05 - RISTORANTE", "fridge": "Cella Pesce 0°C", "temp": "+6.2°C", "outcome": "PRE-ALLARME", "operator": "Matteo B.", "pin_sig": "PIN #1005 (Verificato)"}
    ]

    return {
        "schema_v": "v10_00_09",
        "nodes": nodes,
        "hub_meta": {
            "code": "09",
            "name": "REGIA",
            "subtitle": "Configurazione, Staff, Eventi & Stampa ASL"
        },
        "haccp_state": haccp_state,
        "haccp_logs": haccp_logs,
        "figurine": [
            {"pin": "1000", "nick": "Direzione", "role": "Coordinamento", "index_cost": 150, "node_id": "N00", "sub_zone": "Ufficio Direzione", "shift": "Giornaliero"},
            {"pin": "1001", "nick": "Marco S.", "role": "Chef Pasticcere", "index_cost": 120, "node_id": "N01", "sub_zone": "Laboratorio Pasticceria", "shift": "Mattina (07-15)"},
            {"pin": "1002", "nick": "Elena R.", "role": "Governante Piani", "index_cost": 100, "node_id": "N02", "sub_zone": "Piano 1", "shift": "Mattina (07-15)"},
            {"pin": "1003", "nick": "Giulia F.", "role": "Receptionist", "index_cost": 95, "node_id": "N03", "sub_zone": "Front Desk", "shift": "Mattina (07-15)"},
            {"pin": "1004", "nick": "Jolly 01", "role": "Responsabile Colazioni", "index_cost": 110, "node_id": "N04", "sub_zone": "Buffet Centrale", "shift": "Mattina (07-15)"},
            {"pin": "1005", "nick": "Matteo B.", "role": "Maître Ristorante", "index_cost": 115, "node_id": "N05", "sub_zone": "Veranda 1", "shift": "Pranzo/Sera"},
            {"pin": "1006", "nick": "Extra A", "role": "Barman Terrazza", "index_cost": 90, "node_id": "N06", "sub_zone": "Terrazza Bar", "shift": "Mattina (07-15)"},
            {"pin": "1007", "nick": "Bagnino / Regia", "role": "Presidio Spiaggia", "index_cost": 100, "node_id": "N07", "sub_zone": "Gazebo Cerimonie", "shift": "Giornaliero"}
        ],
        "sos_queue": [],
        "events": [
            {"id": "EV1", "title": "Matrimonio Rossi-Bianchi", "zone": "Gazebo -> Veranda Circolare", "pax": 130, "cake_time": "22:30", "phase": "1. Accoglienza / Rito"},
            {"id": "EV2", "title": "50° Anniversario", "zone": "Veranda Grande", "pax": 55, "cake_time": "23:00", "phase": "2. Aperitivo"}
        ]
    }

store = get_shared_store()

# Allineamento automatico se il server aveva in memoria la vecchia mappa a 8 blocchi
if store.get("schema_v") != "v10_00_09":
    st.cache_resource.clear()
    st.rerun()

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None
if "active_pin" not in st.session_state:
    st.session_state.active_pin = "9999"

now_it = get_italy_now()
now_str = now_it.strftime("%H:%M")
today_str = now_it.strftime("%d/%m/%Y")
win_name = get_current_window_info(now_it)

unchecked_list = [v for v in store["haccp_state"].values() if v["status"] == "PURPLE"]
total_fridges = len(store["haccp_state"])
checked_fridges = total_fridges - len(unchecked_list)

# --- INTESTAZIONE PULITA ---
st.markdown(f"""
<div class="top-bar">
    <div class="brand-title">SOVEREIGN KINETIC ARCHITECTURE <span>// BOSCHETTO PRO</span></div>
    <div class="brand-clock">🕒 ORA SISTEMA: {now_str}  |  FASCIA ATTIVA: {win_name}</div>
</div>
""", unsafe_allow_html=True)

c_pin, c_btn, c_dir, c_sonar = st.columns([1.3, 1.1, 1.1, 1.2])
with c_pin:
    new_pin = st.text_input("PIN ACCESSO", value=st.session_state.active_pin, label_visibility="collapsed", placeholder="PIN (9999 Dir. | 1001..1007 Staff)")
with c_btn:
    if st.button("CONFERMA PIN ↵", type="secondary", use_container_width=True) or (new_pin != st.session_state.active_pin):
        st.session_state.active_pin = new_pin.strip()
        st.session_state.selected_node_id = None
        st.rerun()
with c_dir:
    if st.button("PLANCIA 9999 🏛️", type="secondary", use_container_width=True):
        st.session_state.active_pin = "9999"
        st.session_state.selected_node_id = None
        st.rerun()
with c_sonar:
    sonar_active = st.toggle("🔊 AUDIO TASTI & SONAR", value=True)

bind_global_tactile_audio(sonar_active)

pin_input = st.session_state.active_pin

# ==============================================================================
# VISTA 1: DIREZIONE (PIN 9999) — 10 BLOCCHI AL CENTRO + RETTANGOLO VERTICALE A DESTRA
# ==============================================================================
if pin_input in ["9999", "0000"]:
    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='alert-bar-crit'>🚨 ALLARME ROSSO GUASTO/TEMPERATURA: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        c_s1, c_s2 = st.columns([4.5, 1])
        with c_s1:
            st.markdown(f"<div class='alert-bar-sos'>📦 RICHIESTA MAGAZZINO ({len(store['sos_queue'])}) — {latest_sos['from']} [ore {latest_sos['time']}]: {latest_sos['item']}</div>", unsafe_allow_html=True)
        with c_s2:
            if st.button("✖ Chiudi SOS", type="secondary", use_container_width=True):
                store["sos_queue"].clear()
                st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 0: GRIGLIA CENTRALE (00..09) + RETTANGOLO VERTICALE A DESTRA
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_logs = len(store["haccp_logs"])

        col_center, col_right = st.columns([3.1, 1.15], gap="medium")

        with col_center:
            r1 = st.columns(3)
            r2 = st.columns(3)
            r3 = st.columns(3)
            r4 = st.columns(3)
            grid_slots = r1 + r2 + r3 + r4

            color_palette = {
                "GREEN":  {"bg": "#10b981", "border": "#34d399"},
                "PURPLE": {"bg": "#6b21a8", "border": "#a855f7"},
                "YELLOW": {"bg": "#eab308", "border": "#fde047"},
                "RED":    {"bg": "#ef4444", "border": "#fca5a5"}
            }

            cards_payload = []

            for idx, node in enumerate(store["nodes"]):
                nid = node["id"]
                n_staff = len([f for f in store["figurine"] if f["node_id"] == nid])
                n_fridges = [v for v in store["haccp_state"].values() if v["node_id"] == nid]

                squares = [color_palette[f["status"]] for f in n_fridges]
                n_ok = sum(1 for f in n_fridges if f["status"] == "GREEN")
                n_anom = sum(1 for f in n_fridges if f["status"] in ["YELLOW", "RED"])

                if not n_fridges:
                    haccp_txt = "SLOT ATTIVO"
                    st_col = "#94a3b8"
                elif n_anom > 0:
                    haccp_txt = f"{n_anom} ANOMALIA"
                    st_col = "#fbbf24"
                elif n_ok < len(n_fridges):
                    haccp_txt = f"{n_ok}/{len(n_fridges)}"
                    st_col = "#c084fc"
                else:
                    haccp_txt = f"{n_ok}/{len(n_fridges)} OK"
                    st_col = "#34d399"

                marker = f"{node['code']} - {node['name']}"
                cards_payload.append({
                    "marker": marker,
                    "title": marker,
                    "subtitle": node["subtitle"],
                    "squares": squares,
                    "staff_count": n_staff,
                    "haccp_txt": haccp_txt,
                    "status_color": st_col
                })

                with grid_slots[idx]:
                    if st.button(f"{marker}\n{node['subtitle']}", key=f"tile_{nid}", type="primary", use_container_width=True):
                        st.session_state.selected_node_id = nid
                        st.rerun()

            # Blocco 09 - REGIA
            hm = store["hub_meta"]
            marker_09 = f"{hm['code']} - {hm['name']}"
            cards_payload.append({
                "marker": marker_09,
                "title": marker_09,
                "subtitle": hm["subtitle"],
                "squares": [{"bg": "#0284c7", "border": "#38bdf8"} for _ in range(4)],
                "staff_count": tot_fig,
                "haccp_txt": f"{tot_logs} FIRME",
                "status_color": "#38bdf8"
            })
            with grid_slots[9]:
                if st.button(f"{marker_09}\n{hm['subtitle']}", key="tile_HUB", type="primary", use_container_width=True):
                    st.session_state.selected_node_id = "HUB_VAULT"
                    st.rerun()

            inject_matrix_into_touch_cards(cards_payload)

        # GRANDE RETTANGOLO VERTICALE DI CONTROLLO A DESTRA
        with col_right:
            sos_txt = f"{tot_sos} APERTI" if tot_sos > 0 else "0 NESSUNA URGENZA"
            st.markdown(f"""
            <div class="right-tower">
                <div class="tower-header">QUADRO SINOTTICO LIVE</div>
                <div class="tower-item">
                    <div class="tower-lbl">CONTROLLI HACCP ({win_name.split()[0]})</div>
                    <div class="tower-val">{checked_fridges}/{total_fridges}</div>
                    <div class="tower-sub">Unità frigorifere certificate in fascia</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">PRESIDIO STAFF (PALLINI BLU)</div>
                    <div class="tower-val">{tot_fig} UNITÀ ATTIVE</div>
                    <div class="tower-sub">1 Pallino Blu = 1 Operatore in turno nel reparto</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">RICHIESTE MAGAZZINO (SOS)</div>
                    <div class="tower-val">{sos_txt}</div>
                    <div class="tower-sub">Segnalazioni di rifornimento dai reparti</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">REGIA & STAMPA ASL</div>
                    <div class="tower-val">{tot_logs} FIRME</div>
                    <div class="tower-sub">Letture timbrate con ora e PIN nel registro</div>
                </div>
                <div class="tower-legend">
                    <b>LEGENDA MATRICE NEI BLOCCHI:</b><br>
                    🟩 <b>Verde:</b> Temperatura conforme<br>
                    🟪 <b>Viola:</b> In attesa di lettura<br>
                    🟨 <b>Giallo:</b> Pre-allarme termico<br>
                    🟥 <b>Rosso:</b> Fuori soglia / Guasto<br>
                    🔵 <b>Pallino Blu:</b> Operatore presente
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # VISTA 09: REGIA (TITOLI DINAMICI, STAMPA REGISTRO ASL, FRIGO, STAFF, EVENTI)
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "HUB_VAULT":
        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        hm = store["hub_meta"]
        st.markdown(f"### {hm['code']} - {hm['name']} — {hm['subtitle']}")

        tab_titles, tab_print, tab_fr, tab_staff, tab_ev = st.tabs([
            "✏️ 1. PERSONALIZZA TITOLI (00-09)",
            "🖨️ 2. STAMPA REGISTRO ASL",
            "❄️ 3. CONFIGURA UNITÀ FRIGO",
            "👥 4. GESTIONE DIPENDENTI & PIN",
            "🥂 5. AGENDA EVENTI"
        ])

        with tab_titles:
            st.markdown("##### ✏️ MODIFICA IN TEMPO REALE I TITOLI E I SOTTOTITOLI DEI BLOCCHI (00 — 09)")
            for idx_n, nd in enumerate(store["nodes"]):
                ct1, ct2, ct3 = st.columns([0.6, 1.8, 2.6])
                nd["code"] = ct1.text_input("Cod.", value=nd["code"], key=f"ed_c_{nd['id']}")
                nd["name"] = ct2.text_input(f"Titolo {nd['code']}", value=nd["name"], key=f"ed_n_{nd['id']}")
                nd["subtitle"] = ct3.text_input(f"Sottotitolo {nd['code']}", value=nd["subtitle"], key=f"ed_s_{nd['id']}")
                if nd.get("sub_zones") is not None:
                    sz_str = st.text_input(f"Sottozone di {nd['name']} (separate da virgola)", value=", ".join(nd["sub_zones"]), key=f"ed_sz_{nd['id']}")
                    nd["sub_zones"] = [s.strip() for s in sz_str.split(",") if s.strip()]
                st.divider()

            ch1, ch2, ch3 = st.columns([0.6, 1.8, 2.6])
            hm["code"] = ch1.text_input("Cod. 09", value=hm["code"], key="ed_hc")
            hm["name"] = ch2.text_input("Titolo 09", value=hm["name"], key="ed_hn")
            hm["subtitle"] = ch3.text_input("Sottotitolo 09", value=hm["subtitle"], key="ed_hs")

            if st.button("💾 SALVA TUTTI I NUOVI TITOLI E TORNA ALLA PLANCIA", type="secondary", use_container_width=True):
                st.session_state.selected_node_id = None
                st.toast("Titoli aggiornati!")
                st.rerun()

        with tab_print:
            st.markdown("##### 📋 REGISTRO CRONOLOGICO FIRME E ORARI HACCP")
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
                <thead><tr><th>Data</th><th>Ora Sistema</th><th>Fascia</th><th>Reparto</th><th>Unità Frigo</th><th>Temp.</th><th>Esito</th><th>Firmatario</th><th>Certificazione PIN</th></tr></thead>
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
                        store["haccp_state"][k].update({"status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--"})
                    st.rerun()

        with tab_fr:
            st.markdown("##### ➕ AGGIUNGI O RIMUOVI UNITÀ FRIGO IN AUTONOMIA")
            cf1, cf2, cf3 = st.columns(3)
            node_map = {f"{n['code']} - {n['name']}": n for n in store["nodes"]}
            fr_node_lbl = cf1.selectbox("Scegli Reparto", list(node_map.keys()))
            target_node = node_map[fr_node_lbl]
            fr_new_name = cf2.text_input("Nome Unità Frigo (es. Frigo Vini Veranda 2)")
            fr_new_kind = cf3.selectbox("Tipo Temperatura", ["POS (+0°C / +5°C)", "NEG (-18°C / -22°C)"])

            if st.button("AGGIUNGI UNITÀ FRIGO AL REPARTO", type="secondary"):
                if fr_new_name:
                    k_code = "POS" if "POS" in fr_new_kind else "NEG"
                    target_node["fridges"].append({"name": fr_new_name.strip(), "kind": k_code})
                    store["haccp_state"][f"{target_node['id']} || {fr_new_name.strip()}"] = {
                        "node_id": target_node["id"], "node_name": target_node["name"],
                        "fridge_name": fr_new_name.strip(),
                        "status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--",
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
            ns_nick = cs1.text_input("Nome e Cognome / Nickname (es. Luca M.)")
            ns_role = cs2.text_input("Mansione (es. Chef de Rang)")
            ns_pin = cs3.text_input("PIN Personale a 4 cifre (es. 1008)")

            cs4, cs5, cs6 = st.columns(3)
            ns_node_label = cs4.selectbox("Reparto", list(node_map.keys()), key="staff_node_sel")
            chosen_node = node_map[ns_node_label]
            ns_sub = cs5.selectbox("Sottozona", chosen_node["sub_zones"] if chosen_node["sub_zones"] else ["Generale"])
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
    # LIVELLO 1: INTERNO DEL SINGOLO REPARTO (00..08)
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown(f"### {node['code']} - {node['name']} — {node['subtitle']}")

        with st.expander("✏️ Rinomina questo Blocco o le sue Sottozone al volo"):
            rn1, rn2 = st.columns(2)
            new_n_name = rn1.text_input("Titolo Blocco", value=node["name"])
            new_n_sub = rn2.text_input("Sottotitolo", value=node["subtitle"])
            new_n_zones = st.text_input("Sottozone (separate da virgola)", value=", ".join(node["sub_zones"]))
            if st.button("Salva Titolo Blocco", type="secondary"):
                node["name"] = new_n_name.strip()
                node["subtitle"] = new_n_sub.strip()
                node["sub_zones"] = [s.strip() for s in new_n_zones.split(",") if s.strip()]
                st.rerun()

        st.divider()

        col_haccp, col_ops = st.columns([1.6, 1.4])

        with col_haccp:
            st.markdown(f"##### UNITÀ FRIGO — FASCIA {win_name} (Ora Sistema: {now_str})")
            st.caption("VIOLA: In Attesa  |  VERDE: Regolare  |  GIALLO: Pre-Allarme  |  ROSSO: Guasto")
            node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
            if not node_fridges:
                st.info("Slot strategico libero da unità frigorifere. Puoi aggiungere unità o sottozone in qualsiasi momento.")
            else:
                tiles_html = "<div class='haccp-grid'>"
                for st_data in node_fridges:
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
                pick_sub = st.selectbox("Sottozona", node["sub_zones"] if node["sub_zones"] else ["Generale"])
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
                st.markdown("##### RICHIESTE MAGAZZINO")
                for req in node_sos:
                    st.warning(f"Ore {req['time']} — {req['item']}")
                if st.button("Segna SOS come Evasi", type="secondary", use_container_width=True):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()

# ==============================================================================
# VISTA 2: TERMINALE OPERATORE TOUCH (PIN 1001..1007)
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
            st.info(f"📋 Unità Frigo in attesa di firma: {', '.join(my_unchecked)}")
        elif my_fridges:
            st.success("✔️ Tutte le unità frigo del tuo reparto sono state firmate!")

        if my_fridges:
            st.markdown(f"##### 1. RILEVAZIONE E FIRMA ELETTRONICA TEMPERATURA (Orario Certificato: {now_str})")
            sel_key = st.selectbox("Seleziona Unità Frigo", my_fridges, format_func=lambda x: f"{x.split(' || ')[1]}  [{store['haccp_state'][x]['label']} - ore {store['haccp_state'][x]['time']}]")
            fr_info = store["haccp_state"][sel_key]
            default_t = 3.0 if fr_info["kind"] == "POS" else -19.0
            temp_val = st.slider("Temperatura Letta sul Display (°C)", -28.0, 15.0, default_t, 0.5)
            is_broken = st.checkbox("Segnala Anomalia / Unità Frigo GUASTA")
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
                        "node": f"{user_node['code']} - {user_node['name']}",
                        "fridge": fr_info["fridge_name"],
                        "temp": label_text,
                        "outcome": outcome_map[status_color],
                        "operator": user["nick"],
                        "pin_sig": f"PIN #{user['pin']} (Verificato)"
                    })
                    st.toast(f"Firmato da {user['nick']} alle {now_str}: {label_text}")
                    st.rerun()

        st.divider()
        st.markdown("##### 2. RICHIESTA URGENTE MAGAZZINO (SOS)")
        sos_item = st.text_input("Articolo / Rifornimento richiesto:")
        if st.button(f"INVIA RICHIESTA MAGAZZINO (ORE {now_str})", type="secondary", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": now_str,
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']} - {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.toast("Richiesta inviata!")
                st.rerun()
