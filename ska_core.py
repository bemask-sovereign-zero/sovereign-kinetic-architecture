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

# --- CSS ARCHITETTONICO + MENU A 5 RIGHE CLICCABILI ---
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

/* BANNER ALLERTE */
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

/* BOTTONI SECONDARI E RIGHE CLICCABILI DEI 5 SOTTOMENU */
div.stButton > button[kind="secondary"] {
    background: linear-gradient(90deg, #0f1d33 0%, #152744 100%) !important;
    color: #ffffff !important;
    border: 1.5px solid #38bdf8 !important;
    border-left: 5px solid #38bdf8 !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.83rem !important;
    padding: 11px 16px !important;
    min-height: 46px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    transition: transform 0.08s ease, background 0.15s ease !important;
}
div.stButton > button[kind="secondary"] p { color: #ffffff !important; font-weight: 700 !important; }
div.stButton > button[kind="secondary"]:hover {
    background: linear-gradient(90deg, #0284c7 0%, #0369a1 100%) !important;
    border-color: #ffffff !important;
}
div.stButton > button[kind="secondary"]:active { transform: scale(0.98) !important; }

/* GRANDI QUADRATI TOUCH DELLA COSTELLAZIONE (ALTEZZA FISSA 154px) */
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

/* QUADRETTI FRIGO INTERNI AL REPARTO */
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

.submenu-box {
    background: #0d1524;
    border: 1px solid #1e3a5f;
    border-top: 3px solid #38bdf8;
    border-radius: 8px;
    padding: 18px;
    margin-top: 10px;
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

# --- MOTORE GRAFICO PER I QUADRATI DELLA COSTELLAZIONE ---
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
                            for (let i=0; i<5; i++) {{
                                sqHtml += `<span style="display:inline-block;width:14px;height:14px;border-radius:3px;background:#0f172a;border:1.5px solid #334155;" title="5 Sottomenu Operativi"></span>`;
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
                                <span>STATO: <b style="color:${{c.status_color}};">${{c.haccp_txt}}</b></span>
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

# --- ARCHITETTURA ESPANDIBILE CON 5 SOTTOMENU IN OGNI BLOCCO ---
@st.cache_resource
def get_shared_store():
    nodes = [
        {
            "id": "N00", "code": "00", "name": "DIREZIONE", "subtitle": "Cabina Regia, Espansione Slot & Stampa ASL",
            "sub_zones": ["Ufficio Direzione", "Amministrazione", "Controllo Gestione"],
            "fridges": [],
            "tasks": [
                {"title": "Verifica Quadro Sinottico HACCP", "done": True},
                {"title": "Controllo Presidio Turni Reparti", "done": True},
                {"title": "Revisione Eventi & Cerimonie in Agenda", "done": False}
            ]
        },
        {
            "id": "N01", "code": "01", "name": "PASTICCERIA", "subtitle": "Laboratorio Pasticceria & Forni",
            "sub_zones": ["Laboratorio Pasticceria", "Zona Forni & Sfogliatura"],
            "fridges": [
                {"name": "Cella Basi +4°C", "kind": "POS"},
                {"name": "Cella Semifreddi -18°C", "kind": "NEG"},
                {"name": "Abbattitore Lab", "kind": "NEG"},
                {"name": "Vetrina Torte +4°C", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Sfogliatura e Cottura Lievitati Mattina", "done": True},
                {"title": "Preparazione Linea Senza Glutine / Lattosio", "done": True},
                {"title": "Allestimento Torte Cerimonia / Credenza", "done": False}
            ]
        },
        {
            "id": "N02", "code": "02", "name": "CAMERE", "subtitle": "Piani, Camere & Housekeeping",
            "sub_zones": ["Piano 1", "Piano 2", "Office Biancheria"],
            "fridges": [
                {"name": "Frigo Office Piano 1", "kind": "POS"},
                {"name": "Frigo Office Piano 2", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Priorità Camere in Partenza (Check-out)", "done": True},
                {"title": "Riassetto Camere Fermate", "done": False},
                {"title": "Controllo Dotazioni Office & Biancheria", "done": False}
            ]
        },
        {
            "id": "N03", "code": "03", "name": "RECEPTION", "subtitle": "Front Office, Accoglienza & Hub",
            "sub_zones": ["Front Desk", "Accoglienza Ospiti", "Back Office"],
            "fridges": [],
            "tasks": [
                {"title": "Invio Schedine Alloggiati / ISTAT", "done": True},
                {"title": "Verifica Arrivi del Giorno e Assegnazione", "done": True},
                {"title": "Chiusura Cassa e Passaggio Consegne", "done": False}
            ]
        },
        {
            "id": "N04", "code": "04", "name": "SALA COLAZIONI", "subtitle": "Buffet Mattutino & Caffetteria Sala",
            "sub_zones": ["Buffet Centrale", "Sala Colazioni Interna", "Veranda Colazioni"],
            "fridges": [
                {"name": "Buffet Freddo Colazioni", "kind": "POS"},
                {"name": "Vetrina Yogurt & Latte", "kind": "POS"},
                {"name": "Vetrina Salumi & Formaggi", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Allestimento Buffet Dolce/Salato ore 07:00", "done": True},
                {"title": "Presidio Macchine Caffè e Rimpiazzo Vassoi", "done": True},
                {"title": "Sanificazione Buffet Fine Servizio", "done": False}
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
            ],
            "tasks": [
                {"title": "Controllo Mise en Place Verande", "done": True},
                {"title": "Verifica Stoccaggio Celle Carne/Pesce", "done": True},
                {"title": "Briefing Menu Giorno & Eventi Serali", "done": False}
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
            ],
            "tasks": [
                {"title": "Apertura Banco Caffetteria e Taratura Macina", "done": True},
                {"title": "Rifornimento Frigo Bibite e Linea Aperitivo", "done": False},
                {"title": "Pulizia Terrazza e Chiusura Serale", "done": False}
            ]
        },
        {
            "id": "N07", "code": "07", "name": "SPIAGGIA", "subtitle": "Stabilimento Balneare & Gazebo",
            "sub_zones": ["Gazebo Cerimonie", "Ombrelloni & Tende", "Chiosco Spiaggia"],
            "fridges": [
                {"name": "Frigo Champagne Gazebo", "kind": "POS"},
                {"name": "Banco Bar Spiaggia", "kind": "POS"}
            ],
            "tasks": [
                {"title": "Apertura Ombrelloni e Controllo Tende", "done": True},
                {"title": "Allestimento Gazebo per Aperitivo/Evento", "done": False}
            ]
        },
        {
            "id": "N08", "code": "08", "name": "PARCHEGGIO", "subtitle": "Viabilità, Accessi & Area Sposi",
            "sub_zones": ["Ingresso Principale", "Area Sosta Hotel", "Area Riservata Eventi"],
            "fridges": [],
            "tasks": [
                {"title": "Verifica Sbarra Accessi e Posti Riservati", "done": True},
                {"title": "Presidio Viabilità Arrivo Ospiti Evento", "done": False}
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
        {"date": today_d, "time": "06:45", "window": "MATTINA", "node": "01 - PASTICCERIA", "fridge": "Cella Basi +4°C", "temp": "+3.6°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:46", "window": "MATTINA", "node": "01 - PASTICCERIA", "fridge": "Cella Semifreddi -18°C", "temp": "-19.5°C", "outcome": "CONFORME", "operator": "Marco S.", "pin_sig": "PIN #1001 (Verificato)"},
        {"date": today_d, "time": "06:50", "window": "MATTINA", "node": "04 - SALA COLAZIONI", "fridge": "Buffet Freddo Colazioni", "temp": "+3.9°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "06:51", "window": "MATTINA", "node": "04 - SALA COLAZIONI", "fridge": "Vetrina Yogurt & Latte", "temp": "+4.1°C", "outcome": "CONFORME", "operator": "Jolly 01", "pin_sig": "PIN #1004 (Verificato)"},
        {"date": today_d, "time": "05 - RISTORANTE", "window": "MATTINA", "node": "05 - RISTORANTE", "fridge": "Cella Carne +2°C", "temp": "+2.4°C", "outcome": "CONFORME", "operator": "Matteo B.", "pin_sig": "PIN #1005 (Verificato)"},
        {"date": today_d, "time": "06:55", "window": "MATTINA", "node": "05 - RISTORANTE", "fridge": "Cella Pesce 0°C", "temp": "+6.2°C", "outcome": "PRE-ALLARME", "operator": "Matteo B.", "pin_sig": "PIN #1005 (Verificato)"}
    ]

    return {
        "schema_v": "v11_5rows_expandable",
        "nodes": nodes,
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

if store.get("schema_v") != "v11_5rows_expandable":
    st.cache_resource.clear()
    st.rerun()

if "selected_node_id" not in st.session_state:
    st.session_state.selected_node_id = None
if "active_submenu" not in st.session_state:
    st.session_state.active_submenu = 1
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
# VISTA 1: DIREZIONE (PIN 9999) — GRIGLIA ESPANDIBILE + RETTANGOLO DESTRO
# ==============================================================================
if pin_input in ["9999", "0000"]:
    red_tiles = [v["fridge_name"] for v in store["haccp_state"].values() if v["status"] == "RED"]
    if red_tiles:
        st.markdown(f"<div class='alert-bar-crit'>🚨 ALLARME ROSSO GUASTO/TEMPERATURA: {', '.join(red_tiles)}</div>", unsafe_allow_html=True)

    if store["sos_queue"]:
        latest_sos = store["sos_queue"][-1]
        c_s1, c_s2 = st.columns([4.5, 1])
        with c_s1:
            st.markdown(f"<div class='alert-bar-sos'>📦 SEGNALAZIONE REPARTO ({len(store['sos_queue'])}) — {latest_sos['from']} [ore {latest_sos['time']}]: {latest_sos['item']}</div>", unsafe_allow_html=True)
        with c_s2:
            if st.button("✖ Chiudi Avviso", type="secondary", use_container_width=True):
                store["sos_queue"].clear()
                st.rerun()

    # --------------------------------------------------------------------------
    # LIVELLO 0: LA COSTELLAZIONE ESPANDIBILE + TORRE SINOTTICA A DESTRA
    # --------------------------------------------------------------------------
    if st.session_state.selected_node_id is None:
        tot_fig = len(store["figurine"])
        tot_sos = len(store["sos_queue"])
        tot_logs = len(store["haccp_logs"])
        tot_nodes = len(store["nodes"])

        col_center, col_right = st.columns([3.1, 1.15], gap="medium")

        with col_center:
            color_palette = {
                "GREEN":  {"bg": "#10b981", "border": "#34d399"},
                "PURPLE": {"bg": "#6b21a8", "border": "#a855f7"},
                "YELLOW": {"bg": "#eab308", "border": "#fde047"},
                "RED":    {"bg": "#ef4444", "border": "#fca5a5"}
            }

            cards_payload = []
            # Griglia dinamica a righe di 3 colonne (supporta espansione infinita fino a X blocchi!)
            num_rows = (tot_nodes + 2) // 3
            grid_slots = []
            for _ in range(num_rows):
                grid_slots.extend(st.columns(3))

            for idx, node in enumerate(store["nodes"]):
                nid = node["id"]
                n_staff = len([f for f in store["figurine"] if f["node_id"] == nid])
                n_fridges = [v for v in store["haccp_state"].values() if v["node_id"] == nid]

                if nid == "N00":
                    # Il blocco 00 - DIREZIONE ha 5 quadratini Ciano che rappresentano le 5 Righe di Regia
                    squares = [{"bg": "#0284c7", "border": "#38bdf8"} for _ in range(5)]
                    haccp_txt = "5 MENU REGIA"
                    st_col = "#38bdf8"
                else:
                    squares = [color_palette[f["status"]] for f in n_fridges]
                    n_ok = sum(1 for f in n_fridges if f["status"] == "GREEN")
                    n_anom = sum(1 for f in n_fridges if f["status"] in ["YELLOW", "RED"])

                    if not n_fridges:
                        haccp_txt = "5 SOTTOMENU"
                        st_col = "#94a3b8"
                    elif n_anom > 0:
                        haccp_txt = f"{n_anom} ANOMALIA"
                        st_col = "#fbbf24"
                    elif n_ok < len(n_fridges):
                        haccp_txt = f"HACCP {n_ok}/{len(n_fridges)}"
                        st_col = "#c084fc"
                    else:
                        haccp_txt = f"HACCP {n_ok}/{len(n_fridges)} OK"
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
                        st.session_state.active_submenu = 1
                        st.rerun()

            inject_matrix_into_touch_cards(cards_payload)

            # BARRA RAPIDA DI ESPANSIONE SLOT DIRETTAMENTE SOTTO LA GRIGLIA
            with st.expander(f"➕ ESPANDI ARCHITETTURA: AGGIUNGI NUOVO SLOT REPARTO (Attuali: {tot_nodes} Slot attivi — Espandibile fino a X)"):
                ex1, ex2, ex3 = st.columns([1, 2, 2.5])
                next_code = f"{tot_nodes:02d}"
                new_sl_code = ex1.text_input("Codice Slot", value=next_code)
                new_sl_name = ex2.text_input("Nome Nuovo Reparto (es. PISCINA / SPA / CANTINA)")
                new_sl_sub = ex3.text_input("Sottotitolo Funzione", value="Reparto Operativo & Controllo")
                if st.button("🚀 CREA NUOVO SLOT NELLA COSTELLAZIONE", type="secondary", use_container_width=True):
                    if new_sl_name:
                        new_id = f"N{int(datetime.now().timestamp())}"
                        store["nodes"].append({
                            "id": new_id,
                            "code": new_sl_code.strip(),
                            "name": new_sl_name.strip().upper(),
                            "subtitle": new_sl_sub.strip(),
                            "sub_zones": ["Zona Principale", "Postazione 1"],
                            "fridges": [],
                            "tasks": [{"title": "Controllo Apertura Reparto", "done": False}]
                        })
                        st.toast(f"Slot {new_sl_code} - {new_sl_name} creato con 5 sottomenu!")
                        st.rerun()

        # GRANDE RETTANGOLO VERTICALE DI CONTROLLO A DESTRA
        with col_right:
            sos_txt = f"{tot_sos} APERTI" if tot_sos > 0 else "0 NESSUNA URGENZA"
            st.markdown(f"""
            <div class="right-tower">
                <div class="tower-header">QUADRO SINOTTICO LIVE</div>
                <div class="tower-item">
                    <div class="tower-lbl">CONTROLLI HACCP ({win_name.split()[0]})</div>
                    <div class="tower-val">{checked_fridges}/{total_fridges}</div>
                    <div class="tower-sub">Unità certificate con ora e PIN</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">PRESIDIO STAFF (PALLINI BLU)</div>
                    <div class="tower-val">{tot_fig} UNITÀ ATTIVE</div>
                    <div class="tower-sub">1 Pallino Blu = 1 Operatore in turno</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">SEGNALAZIONI & MAGAZZINO</div>
                    <div class="tower-val">{sos_txt}</div>
                    <div class="tower-sub">Richieste o manutenzioni dai reparti</div>
                </div>
                <div class="tower-item">
                    <div class="tower-lbl">SLOT ATTIVI & STAMPA ASL</div>
                    <div class="tower-val">{tot_nodes} SLOT · {tot_logs} FIRME</div>
                    <div class="tower-sub">Architettura modulare espandibile</div>
                </div>
                <div class="tower-legend">
                    <b>COME LEGGERE I QUADRATI:</b><br>
                    🟩 <b>Verde:</b> Unità conforme<br>
                    🟪 <b>Viola:</b> In attesa di firma<br>
                    🟨 <b>Giallo:</b> Pre-allarme termico<br>
                    🟥 <b>Rosso:</b> Fuori soglia / Guasto<br>
                    🟦 <b>Grigio/Blu:</b> 5 Sottomenu attivi<br>
                    🔵 <b>Pallino Blu:</b> 1 Operatore presente
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 1 — SLOT 00 - DIREZIONE: LE 5 RIGHE CLICCABILI DI COMANDO GENERALE
    # --------------------------------------------------------------------------
    elif st.session_state.selected_node_id == "N00":
        node00 = next(n for n in store["nodes"] if n["id"] == "N00")
        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown(f"### {node00['code']} - {node00['name']} — {node00['subtitle']}")
        st.caption("Tocca una delle 5 righe operative qui sotto per aprire il relativo sottomenu direzionale:")

        # LE 5 RIGHE CLICCABILI DELLO SLOT 00 - DIREZIONE
        dir_rows = [
            (1, f"➕ RIGA 1 // ESPANDI ARCHITETTURA O RIMUOVI SLOT REPARTO (Attuali: {len(store['nodes'])} Slot)"),
            (2, "✏️ RIGA 2 // RINOMINA VELOCE TITOLI E SOTTOTITOLI DI TUTTI I BLOCCHI"),
            (3, f"👥 RIGA 3 // ANAGRAFICA GENERALE BRIGATA & ASSEGNAZIONE PIN ({len(store['figurine'])} Operatori)"),
            (4, f"🥂 RIGA 4 // AGENDA EVENTI, MATRIMONI & CERIMONIE LIVE ({len(store['events'])} Eventi)"),
            (5, f"🖨️ RIGA 5 // REGISTRO UFFICIALE ASL & SCARICO STAMPA ({len(store['haccp_logs'])} Firme Certificate)")
        ]

        for r_idx, r_label in dir_rows:
            prefix = "🟢 [APERTO] " if st.session_state.active_submenu == r_idx else "▸ "
            if st.button(f"{prefix}{r_label}", key=f"dir_row_{r_idx}", type="secondary", use_container_width=True):
                st.session_state.active_submenu = r_idx
                st.rerun()

        st.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

        # SOTTOMENU DIREZIONE 1: ESPANSIONE E RIMOZIONE SLOT
        if st.session_state.active_submenu == 1:
            st.markdown("#### ➕ SOTTOMENU 1: ESPANSIONE DINAMICA DEGLI SLOT STRUTTURA")
            st.caption("Puoi espandere la costellazione fino a X reparti (es. Piscina, Spa, Cantina, Lavanderia, Manutenzione).")
            ex1, ex2, ex3 = st.columns([1, 2, 2.5])
            next_code = f"{len(store['nodes']):02d}"
            ns_code = ex1.text_input("Codice", value=next_code, key="d1_c")
            ns_name = ex2.text_input("Nome Nuovo Slot (es. PISCINA & SPA)", key="d1_n")
            ns_sub = ex3.text_input("Sottotitolo", value="Controllo Reparto & Presidio", key="d1_s")
            if st.button("AGGIUNGI NUOVO SLOT ALLA PLANCIA", type="secondary"):
                if ns_name:
                    store["nodes"].append({
                        "id": f"N{int(datetime.now().timestamp())}",
                        "code": ns_code.strip(),
                        "name": ns_name.strip().upper(),
                        "subtitle": ns_sub.strip(),
                        "sub_zones": ["Zona 1", "Zona 2"],
                        "fridges": [],
                        "tasks": [{"title": "Verifica Apertura", "done": False}]
                    })
                    st.rerun()

            st.divider()
            st.markdown("##### ELENCO SLOT ATTIVI (Rimuovi slot aggiuntivi)")
            for idx_n, nd in enumerate(store["nodes"]):
                c1, c2 = st.columns([4, 1])
                c1.markdown(f"- **{nd['code']} - {nd['name']}** (*{nd['subtitle']}*)")
                if nd["id"] != "N00":
                    if c2.button("Elimina Slot", key=f"del_slot_{nd['id']}"):
                        store["nodes"].pop(idx_n)
                        st.rerun()

        # SOTTOMENU DIREZIONE 2: RINOMINA TUTTI I BLOCCHI
        elif st.session_state.active_submenu == 2:
            st.markdown("#### ✏️ SOTTOMENU 2: PERSONALIZZA I NOMI DI TUTTI GLI SLOT")
            for idx_n, nd in enumerate(store["nodes"]):
                ct1, ct2, ct3 = st.columns([0.7, 1.8, 2.5])
                nd["code"] = ct1.text_input("Cod.", value=nd["code"], key=f"rn_c_{nd['id']}")
                nd["name"] = ct2.text_input(f"Titolo {nd['code']}", value=nd["name"], key=f"rn_n_{nd['id']}")
                nd["subtitle"] = ct3.text_input(f"Sottotitolo {nd['code']}", value=nd["subtitle"], key=f"rn_s_{nd['id']}")
            if st.button("💾 CONFERMA E SALVA TUTTI I NOMI", type="secondary", use_container_width=True):
                st.toast("Nomi salvati!")
                st.rerun()

        # SOTTOMENU DIREZIONE 3: ANAGRAFICA STAFF & PIN
        elif st.session_state.active_submenu == 3:
            st.markdown("#### 👥 SOTTOMENU 3: GESTIONE GENERALE BRIGATA E PIN PERSONALI")
            cs1, cs2, cs3 = st.columns(3)
            ns_nick = cs1.text_input("Nome e Cognome / Nickname (es. Luca M.)")
            ns_role = cs2.text_input("Mansione (es. Chef de Rang)")
            ns_pin = cs3.text_input("PIN Personale a 4 cifre (es. 1008)")

            cs4, cs5, cs6 = st.columns(3)
            node_map = {f"{n['code']} - {n['name']}": n for n in store["nodes"]}
            ns_node_label = cs4.selectbox("Reparto Assegnato", list(node_map.keys()))
            chosen_node = node_map[ns_node_label]
            ns_sub = cs5.selectbox("Sottozona", chosen_node["sub_zones"] if chosen_node["sub_zones"] else ["Generale"])
            ns_shift = cs6.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)", "Giornaliero"])

            if st.button("ATTIVA OPERATORE E GENERA PALLINO BLU", type="secondary"):
                if ns_nick and ns_pin:
                    store["figurine"].append({
                        "pin": ns_pin.strip(), "nick": ns_nick.strip(), "role": ns_role.strip() or "Operatore",
                        "index_cost": 100, "node_id": chosen_node["id"], "sub_zone": ns_sub, "shift": ns_shift
                    })
                    st.rerun()

            st.divider()
            for idx_f, f in enumerate(store["figurine"]):
                cf1, cf2 = st.columns([4, 1])
                cf1.markdown(f"- 🔵 **PIN `{f['pin']}`** — **{f['nick']}** ({f['role']})  |  Slot: `{f['node_id']}` ({f['sub_zone']})")
                if cf2.button("Rimuovi", key=f"rm_fig_{f['pin']}_{idx_f}"):
                    store["figurine"].pop(idx_f)
                    st.rerun()

        # SOTTOMENU DIREZIONE 4: AGENDA EVENTI
        elif st.session_state.active_submenu == 4:
            st.markdown("#### 🥂 SOTTOMENU 4: AGENDA EVENTI & CERIMONIE LIVE")
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
            if st.button("AGGIUNGI EVENTO IN AGENDA", type="secondary"):
                if ne_title:
                    store["events"].append({"id": f"EV{int(datetime.now().timestamp())}", "title": ne_title, "zone": ne_zone, "pax": ne_pax, "cake_time": ne_cake, "phase": "1. Accoglienza / Rito"})
                    st.rerun()

        # SOTTOMENU DIREZIONE 5: STAMPA REGISTRO ASL
        elif st.session_state.active_submenu == 5:
            st.markdown("#### 🖨️ SOTTOMENU 5: REGISTRO UFFICIALE ASL (ORARI E FIRME ELETTRONICHE)")
            rows_html = ""
            for log in reversed(store["haccp_logs"]):
                rows_html += (
                    f"<tr>"
                    f"<td>{log['date']}</td><td><b>{log['time']}</b></td><td>{log['window']}</td>"
                    f"<td>{log['node']}</td><td>{log['fridge']}</td><td><b>{log['temp']}</b></td>"
                    f"<td>{log['outcome']}</td><td><b>{log['operator']}</b></td><td>{log['pin_sig']}</td>"
                    f"</tr>"
                )
            st.markdown(f"""
            <table class="log-table">
                <thead>
                    <tr>
                        <th>DATA</th><th>ORA ESATTA</th><th>FASCIA</th><th>REPARTO</th>
                        <th>UNITÀ FRIGO</th><th>TEMP.</th><th>ESITO</th><th>OPERATORE</th><th>FIRMA ELETTRONICA</th>
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
                <div><b>Sistema Digitale:</b> S.K.A. // Boschetto Pro</div>
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
                st.download_button("🖨️ SCARICA MODULO STAMPA ASL (.HTML)", data=printable_html, file_name=f"REGISTRO_ASL_{now_it.strftime('%Y%m%d')}.html", mime="text/html", use_container_width=True)
            with cp2:
                st.download_button("📊 SCARICA FOGLIO EXCEL (.CSV)", data=csv_buffer.getvalue(), file_name=f"REGISTRO_HACCP_{now_it.strftime('%Y%m%d')}.csv", mime="text/csv", use_container_width=True)
            with cp3:
                if st.button("🔄 INIZIA NUOVO GIRO (RIPORTA IN ATTESA)", type="secondary", use_container_width=True):
                    for k in store["haccp_state"]:
                        store["haccp_state"][k].update({"status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--"})
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIVELLO 1 — INTERNO DI QUALSIASI REPARTO (01..N): LE 5 RIGHE CLICCABILI
    # --------------------------------------------------------------------------
    else:
        nid = st.session_state.selected_node_id
        node = next(n for n in store["nodes"] if n["id"] == nid)

        if st.button("⬅ TORNA ALLA COSTELLAZIONE PRINCIPALE", type="secondary", use_container_width=True):
            st.session_state.selected_node_id = None
            st.rerun()

        st.markdown(f"### {node['code']} - {node['name']} — {node['subtitle']}")
        st.caption("Seleziona una delle 5 righe qui sotto per aprire il relativo sottomenu del reparto:")

        node_fridges = [v for k, v in store["haccp_state"].items() if v["node_id"] == nid]
        node_staff = [f for f in store["figurine"] if f["node_id"] == nid]
        node_tasks = node.get("tasks", [])
        node_sos = [s for s in store["sos_queue"] if s["node_id"] == nid]

        # LE 5 RIGHE CLICCABILI IDENTICHE E PULITE DENTRO OGNI QUADRATO
        dept_rows = [
            (1, f"❄️ RIGA 1 // CONTROLLO UNITÀ FRIGO & STORICO HACCP ({len(node_fridges)} Unità censite)"),
            (2, f"🔵 RIGA 2 // PRESIDIO STAFF & TURNI IN QUESTO REPARTO ({len(node_staff)} Pallini Blu attivi)"),
            (3, f"📋 RIGA 3 // CHECKLIST OPERATIVA & MANSIONI DI REPARTO ({sum(1 for t in node_tasks if t['done'])}/{len(node_tasks)} Completate)"),
            (4, f"📦 RIGA 4 // SEGNALAZIONE GUASTI & RICHIESTE MAGAZZINO ({len(node_sos)} Avvisi aperti)"),
            (5, f"⚙️ RIGA 5 // CONFIGURA QUESTO SLOT (Rinomina {node['name']}, Sottozone e Unità Frigo)")
        ]

        for r_idx, r_label in dept_rows:
            prefix = "🟢 [APERTO] " if st.session_state.active_submenu == r_idx else "▸ "
            if st.button(f"{prefix}{r_label}", key=f"dept_row_{nid}_{r_idx}", type="secondary", use_container_width=True):
                st.session_state.active_submenu = r_idx
                st.rerun()

        st.markdown("<div class='submenu-box'>", unsafe_allow_html=True)

        # SOTTOMENU REPARTO 1: UNITÀ FRIGO & FIRMA RAPIDA
        if st.session_state.active_submenu == 1:
            st.markdown(f"#### ❄️ SOTTOMENU 1: STATO UNITÀ FRIGO — {node['name']}")
            if not node_fridges:
                st.info("Nessuna unità frigorifera richiesta in questo reparto. Se serve aggiungerne una, apri la Riga 5 qui sopra.")
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
                st.markdown("##### ✍️ REGISTRAZIONE TEMPERATURA DIRETTA DA QUESTO REPARTO")
                my_keys = [k for k, v in store["haccp_state"].items() if v["node_id"] == nid]
                c_f1, c_f2, c_f3 = st.columns([2, 2, 1.5])
                sel_k = c_f1.selectbox("Seleziona Unità", my_keys, format_func=lambda x: x.split(" || ")[1])
                fr_obj = store["haccp_state"][sel_k]
                def_t = 3.0 if fr_obj["kind"] == "POS" else -19.0
                t_val = c_f2.slider("Temperatura (°C)", -28.0, 15.0, def_t, 0.5)
                signer = c_f3.selectbox("Firmatario", [f["nick"] for f in node_staff] if node_staff else ["Direzione"])
                is_brk = st.checkbox("Segnala Guasto Blocco Motore")
                if st.button(f"TIMBRA TEMPERATURA ORE {now_str}", type="secondary"):
                    st_col, lbl_t = evaluate_fridge_status(fr_obj["kind"], t_val, is_brk)
                    out_map = {"GREEN": "CONFORME", "YELLOW": "PRE-ALLARME", "RED": "CRITICO/GUASTO"}
                    fr_obj.update({"status": st_col, "label": lbl_t, "by": signer, "pin": "9999", "time": now_str})
                    store["haccp_logs"].append({
                        "date": today_str, "time": now_str, "window": win_name.split()[0],
                        "node": f"{node['code']} - {node['name']}", "fridge": fr_obj["fridge_name"],
                        "temp": lbl_t, "outcome": out_map[st_col], "operator": signer, "pin_sig": "Confermato in Plancia"
                    })
                    st.rerun()

        # SOTTOMENU REPARTO 2: PRESIDIO STAFF (PALLINI BLU)
        elif st.session_state.active_submenu == 2:
            st.markdown(f"#### 🔵 SOTTOMENU 2: OPERATORI ASSEGNATI A {node['name']} (PALLINI BLU)")
            st.caption("Ogni operatore elencato qui sotto accende un Pallino Blu sul quadrato del reparto nella schermata principale.")
            if not node_staff:
                st.warning("Nessun operatore attualmente assegnato a questo reparto.")
            for f in node_staff:
                st.markdown(f"- 🔵 **{f['nick']}** ({f['role']}) — Sottozona: `{f['sub_zone']}` | Turno: `{f['shift']}` | PIN Personale: `{f['pin']}`")

            st.divider()
            st.markdown("##### ➕ SPOSTA O ASSEGNA UN OPERATORE IN QUESTO REPARTO")
            c_p1, c_p2, c_p3 = st.columns(3)
            pick_fig = c_p1.selectbox("Scegli Operatore", [f["nick"] for f in store["figurine"]])
            pick_sub = c_p2.selectbox("Assegna a Sottozona", node["sub_zones"] if node["sub_zones"] else ["Generale"])
            pick_sh = c_p3.selectbox("Turno", ["Mattina (07-15)", "Pranzo/Pom (12-20)", "Cena/Sera (18-02)", "Giornaliero"])
            if st.button("CONFERMA ASSEGNAZIONE AL REPARTO", type="secondary"):
                for f in store["figurine"]:
                    if f["nick"] == pick_fig:
                        f["node_id"] = nid
                        f["sub_zone"] = pick_sub
                        f["shift"] = pick_sh
                st.rerun()

        # SOTTOMENU REPARTO 3: CHECKLIST & MANSIONI
        elif st.session_state.active_submenu == 3:
            st.markdown(f"#### 📋 SOTTOMENU 3: CHECKLIST OPERATIVA DI {node['name']}")
            for idx_t, t in enumerate(node_tasks):
                t["done"] = st.checkbox(t["title"], value=t["done"], key=f"tk_{nid}_{idx_t}")

            st.divider()
            new_tk = st.text_input("Aggiungi nuova mansione/controllo per questo reparto:")
            if st.button("➕ AGGIUNGI ALLA CHECKLIST", type="secondary"):
                if new_tk:
                    node.setdefault("tasks", []).append({"title": new_tk.strip(), "done": False})
                    st.rerun()

        # SOTTOMENU REPARTO 4: GUASTI & RICHIESTE MAGAZZINO
        elif st.session_state.active_submenu == 4:
            st.markdown(f"#### 📦 SOTTOMENU 4: SEGNALAZIONI, MANUTENZIONI E MAGAZZINO — {node['name']}")
            if node_sos:
                for req in node_sos:
                    st.warning(f"Ore {req['time']} — {req['item']}")
                if st.button("✔️ Segna tutte le segnalazioni di questo reparto come risolte", type="secondary"):
                    store["sos_queue"] = [s for s in store["sos_queue"] if s["node_id"] != nid]
                    st.rerun()
                st.divider()

            new_req = st.text_input("Nuova richiesta materiale o segnalazione guasto in questo reparto:")
            if st.button(f"INVIA SEGNALAZIONE DAL REPARTO (ORE {now_str})", type="secondary"):
                if new_req:
                    store["sos_queue"].append({
                        "time": now_str, "node_id": nid,
                        "from": f"{node['code']} - {node['name']}",
                        "item": new_req.strip(), "status": "Aperto"
                    })
                    st.rerun()

        # SOTTOMENU REPARTO 5: CONFIGURA QUESTO SLOT (NOME, SOTTOZONE, UNITÀ FRIGO)
        elif st.session_state.active_submenu == 5:
            st.markdown(f"#### ⚙️ SOTTOMENU 5: CONFIGURAZIONE AUTONOMA DELLO SLOT {node['code']} - {node['name']}")
            rn1, rn2 = st.columns(2)
            new_n_name = rn1.text_input("Modifica Titolo Blocco", value=node["name"])
            new_n_sub = rn2.text_input("Modifica Sottotitolo", value=node["subtitle"])
            new_n_zones = st.text_input("Modifica Sottozone (separate da virgola)", value=", ".join(node["sub_zones"]))
            if st.button("💾 SALVA NOME E SOTTOZONE", type="secondary"):
                node["name"] = new_n_name.strip().upper()
                node["subtitle"] = new_n_sub.strip()
                node["sub_zones"] = [s.strip() for s in new_n_zones.split(",") if s.strip()]
                st.rerun()

            st.divider()
            st.markdown("##### ❄️ AGGIUNGI O RIMUOVI UNITÀ FRIGO IN QUESTO REPARTO (QUADRATINI VIOLA/VERDI)")
            cf1, cf2 = st.columns(2)
            fr_new_name = cf1.text_input("Nome Nuova Unità Frigo (es. Frigo Bevande 2)")
            fr_new_kind = cf2.selectbox("Regime Termico", ["POS (+0°C / +5°C)", "NEG (-18°C / -22°C)"])
            if st.button("➕ AGGIUNGI UNITÀ FRIGO A QUESTO SLOT", type="secondary"):
                if fr_new_name:
                    k_code = "POS" if "POS" in fr_new_kind else "NEG"
                    node["fridges"].append({"name": fr_new_name.strip(), "kind": k_code})
                    store["haccp_state"][f"{nid} || {fr_new_name.strip()}"] = {
                        "node_id": nid, "node_name": node["name"], "fridge_name": fr_new_name.strip(),
                        "status": "PURPLE", "label": "ATTESA", "by": "-", "pin": "-", "time": "--:--",
                        "kind": k_code
                    }
                    st.rerun()

            for idx_fr, fr_item in enumerate(node["fridges"]):
                c_l, c_b = st.columns([4, 1])
                c_l.markdown(f"- **{fr_item['name']}** (`{fr_item['kind']}`)")
                if c_b.button("Rimuovi Unità", key=f"del_fr_{nid}_{idx_fr}"):
                    removed = node["fridges"].pop(idx_fr)
                    store["haccp_state"].pop(f"{nid} || {removed['name']}", None)
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# ==============================================================================
# VISTA 2: TERMINALE OPERATORE TOUCH (PIN 1001..1007)
# ==============================================================================
else:
    user = next((f for f in store["figurine"] if f["pin"] == pin_input), None)
    if not user:
        st.error(f"PIN '{pin_input}' non riconosciuto. Tocca 'PLANCIA 9999' in alto per tornare in Direzione.")
    else:
        user_node = next(n for n in store["nodes"] if n["id"] == user["node_id"])
        st.success(f"OPERATORE IDENTIFICATO: {user['nick']} ({user['role']})  |  REPARTO: {user_node['code']} - {user_node['name']}  |  ORA: {now_str}")

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
        st.markdown("##### 2. CHECKLIST DI REPARTO")
        for idx_t, t in enumerate(user_node.get("tasks", [])):
            t["done"] = st.checkbox(t["title"], value=t["done"], key=f"op_tk_{idx_t}")

        st.divider()
        st.markdown("##### 3. SEGNALAZIONE GUASTO O RICHIESTA MAGAZZINO")
        sos_item = st.text_input("Articolo mancante o segnalazione tecnica:")
        if st.button(f"INVIA SEGNALAZIONE (ORE {now_str})", type="secondary", use_container_width=True):
            if sos_item:
                store["sos_queue"].append({
                    "time": now_str,
                    "node_id": user["node_id"],
                    "from": f"{user_node['code']} - {user_node['name']}",
                    "item": sos_item,
                    "status": "Richiesto"
                })
                st.toast("Segnalazione inviata!")
                st.rerun()
