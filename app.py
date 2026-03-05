#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qoyllur Rit'i Explorer — v2.1
Dark mode · Mobile-first · GraphRAG v4.0
"""

import os
import streamlit as st

st.set_page_config(
    page_title="Qoyllur Rit'i Explorer",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.stApp { background: #0d1117 !important; font-family: 'Inter', sans-serif !important; }

.block-container {
    max-width: 700px !important;
    margin: 0 auto !important;
    padding: 0 1.25rem 4rem 1.25rem !important;
    background: transparent !important;
}

#MainMenu, footer, header { visibility: hidden !important; }
.stDeployButton { display: none !important; }

p, span, label, div, li { color: #e6edf3; }
h1,h2,h3,h4,h5,h6 { color: #e6edf3 !important; }
code { background: #21262d !important; color: #79c0ff !important; border-radius: 4px; padding: 0 4px; }

.app-header {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 0.8rem 1.25rem;
    margin: 0 -1.25rem 1.75rem -1.25rem;
    display: flex;
    align-items: center;
}
.app-header-title { font-size: 1.05rem; font-weight: 700; color: #e6edf3; margin: 0; }
.app-header-sub   { font-size: 0.72rem; color: #8b949e; margin-left: auto; }

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22 !important;
    border-radius: 8px !important;
    padding: 3px !important;
    border: 1px solid #30363d !important;
    gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #8b949e !important;
    border-radius: 6px !important;
    border: none !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    padding: 0.45rem 1.1rem !important;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #21262d !important;
    color: #e6edf3 !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* INPUTS */
.stTextInput > div > div > input {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-size: 0.9rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: #d4a017 !important;
    box-shadow: 0 0 0 2px rgba(212,160,23,.2) !important;
}
.stTextInput > div > div > input::placeholder { color: #8b949e !important; }
.stTextInput label { color: #8b949e !important; font-size: 0.8rem !important; }

/* SELECTBOX — trigger */
.stSelectbox > div > div {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
}
.stSelectbox label { color: #8b949e !important; font-size: 0.8rem !important; }
/* SELECTBOX — dropdown list (portal, fuera del árbol normal) */
[data-baseweb="popover"] { background: #21262d !important; }
[data-baseweb="menu"]    { background: #21262d !important; border: 1px solid #30363d !important; border-radius: 8px !important; }
[data-baseweb="menu"] ul { background: #21262d !important; padding: 4px !important; }
[data-baseweb="option"]  { background: #21262d !important; color: #e6edf3 !important; font-size: 0.88rem !important; border-radius: 6px !important; }
[data-baseweb="option"]:hover,
[data-baseweb="option"][aria-selected="true"] { background: #30363d !important; color: #e6edf3 !important; }
/* valor seleccionado visible en el trigger */
.stSelectbox [data-testid="stMarkdownContainer"] p { color: #e6edf3 !important; }
.stSelectbox > div > div > div { color: #e6edf3 !important; }

/* RADIO */
.stRadio > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 0.5rem 0.75rem !important;
    gap: 1.5rem !important;
}
.stRadio label { color: #adbac7 !important; font-size: 0.85rem !important; }

/* BOTONES */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    transition: all .15s !important;
}
.stButton > button[kind="primary"] {
    background: #d4a017 !important;
    color: #000 !important;
    width: 100% !important;
    padding: 0.6rem !important;
    box-shadow: 0 2px 8px rgba(212,160,23,.3) !important;
}
.stButton > button[kind="primary"]:hover { background: #b8891a !important; }
.stButton > button[kind="secondary"] {
    background: #21262d !important;
    color: #8b949e !important;
    border: 1px solid #30363d !important;
    width: 100% !important;
}

/* EXPANDER */
.streamlit-expanderHeader {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
    font-size: 0.83rem !important;
}
.streamlit-expanderContent {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-top: none !important;
}

/* INFO/ALERT */
.stAlert > div {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
}

/* METRICS */
[data-testid="metric-container"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 10px !important;
    padding: 0.85rem 1rem !important;
}
[data-testid="stMetricValue"] { color: #d4a017 !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 0.72rem !important; }

/* DIVIDER */
hr { border-color: #30363d !important; margin: 1rem 0 !important; }

/* CHAT */
.msg-user {
    background: rgba(31,111,235,.1);
    border: 1px solid rgba(56,139,253,.25);
    border-radius: 10px 10px 4px 10px;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0;
}
.msg-user .lbl { font-size:0.68rem; font-weight:700; color:#58a6ff; text-transform:uppercase; letter-spacing:.5px; margin-bottom:5px; }
.msg-user .txt { font-size:0.88rem; color:#e6edf3; }

.msg-bot {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 3px solid #d4a017;
    border-radius: 4px 10px 10px 10px;
    padding: 0.8rem 1rem;
    margin: 0.6rem 0;
}
.msg-bot .lbl { font-size:0.68rem; font-weight:700; color:#d4a017; text-transform:uppercase; letter-spacing:.5px; margin-bottom:5px; }
.msg-bot .txt { font-size:0.88rem; color:#adbac7; line-height:1.7; }

/* ABOUT */
.about-sec {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.85rem;
}
.about-sec h4 { font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:.5px; color:#d4a017; margin:0 0 0.6rem 0; }
.about-sec p  { font-size:0.84rem; line-height:1.72; color:#adbac7; margin:0; }
.about-sec p+p { margin-top:0.5rem; }

.chips { display:flex; flex-wrap:wrap; gap:0.3rem; margin-top:0.6rem; }
.chip  { font-size:0.67rem; padding:0.18rem 0.5rem; border-radius:4px; font-family:monospace; border:1px solid #30363d; background:rgba(255,255,255,.04); color:#adbac7; }
.chip.b{ background:rgba(56,139,253,.1); border-color:rgba(56,139,253,.3); color:#79c0ff; }
.chip.g{ background:rgba(212,160,23,.1);  border-color:rgba(212,160,23,.3);  color:#d4a017; }

/* FOOTER */
.tfooter { text-align:center; padding:1.5rem 0 0.5rem; border-top:1px solid #30363d; margin-top:2rem; }
.tfooter p { font-size:0.72rem; color:#8b949e; margin:0.2rem 0; }

.empty-state { text-align:center; padding:2.5rem 1rem; color:#8b949e; font-size:0.85rem; }
</style>
""", unsafe_allow_html=True)

# ── ESTADO ────────────────────────────────────────────────────────────────────
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

def agregar_mensaje(tipo, texto):
    st.session_state.mensajes.append({'tipo': tipo, 'texto': texto})

def limpiar_chat():
    st.session_state.mensajes = []

# ── PREGUNTAS ─────────────────────────────────────────────────────────────────
PREGUNTAS = [
    "¿Qué es Qoyllur Rit'i?",
    "¿Dónde está el santuario?",
    "Háblame de la vestimenta de los ukukus",
    "¿Qué es el Ausangate?",
    "¿Dónde está Sinakara?",
    "¿Dónde está el glaciar Colque Punku?",
    "¿Qué hacen los ukukus?",
    "¿Qué es la lomada?",
    "¿Cuánto dura la lomada?",
    "¿Qué naciones participan?",
    "¿Cuál es el recorrido de la peregrinación?",
]

# ── MOTOR ─────────────────────────────────────────────────────────────────────
@st.cache_resource
def cargar_motor(groq_key: str):
    from graphrag_v4_api import GraphRAG_v4_API
    return GraphRAG_v4_API(ttl_path="qoyllurity.ttl", groq_api_key=groq_key, verbose=False)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
    <div class="app-header-title">🏔 Qoyllur Rit'i</div>
    <div class="app-header-sub">GraphRAG Explorer</div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab_chat, tab_about = st.tabs(["💬  Consultas", "ℹ️  Acerca de"])

# ─────────────────────────────────────────────────────────────────────────────
with tab_chat:

    # API KEY
    groq_key = ""
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
    if not groq_key:
        groq_key = os.getenv("GROQ_API_KEY", "")
    if not groq_key:
        groq_key = st.text_input(
            "🔑 Groq API Key",
            placeholder="gsk_...",
            type="password",
            help="Obtén tu key gratis en console.groq.com"
        )
    if not groq_key:
        st.info("Ingresa tu Groq API key para activar el asistente.")
        st.stop()

    # MOTOR
    try:
        with st.spinner("Inicializando sistema..."):
            motor = cargar_motor(groq_key)
    except ImportError as e:
        st.error(f"Archivo faltante: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error al inicializar: {e}")
        st.stop()

    # MODO
    modo = st.radio(
        "modo", ["📋 Preguntas sugeridas", "✍️ Pregunta libre"],
        horizontal=True, label_visibility="collapsed"
    )

    pregunta = ""
    if modo == "📋 Preguntas sugeridas":
        pregunta = st.selectbox(
            "pregunta", options=[""] + PREGUNTAS,
            format_func=lambda x: "Selecciona una pregunta..." if x == "" else x,
            label_visibility="collapsed"
        )
    else:
        pregunta = st.text_input(
            "pregunta", placeholder="¿Dónde está el glaciar Colque Punku?",
            label_visibility="collapsed"
        )
        with st.expander("💡 Ver ejemplos"):
            for p in PREGUNTAS[:6]:
                st.markdown(f"- {p}")

    # BOTÓN
    if st.button("✨  Preguntar", type="primary", use_container_width=True):
        if pregunta:
            agregar_mensaje('user', pregunta)
            with st.spinner("Consultando grafo de conocimiento..."):
                try:
                    respuesta = motor.responder(pregunta, use_api=True, modo="hibrido", verbose=False)
                    agregar_mensaje('bot', respuesta)
                except Exception as e:
                    agregar_mensaje('bot', f"Error: {e}")
            st.rerun()

    # HISTORIAL
    if st.session_state.mensajes:
        st.markdown("---")
        for msg in reversed(st.session_state.mensajes):
            if msg['tipo'] == 'user':
                st.markdown(f'<div class="msg-user"><div class="lbl">Tú</div><div class="txt">{msg["texto"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-bot"><div class="lbl">Asistente</div><div class="txt">{msg["texto"]}</div></div>', unsafe_allow_html=True)
        st.markdown(" ")
        if st.button("🗑️  Limpiar historial", use_container_width=True):
            limpiar_chat()
            st.rerun()
    else:
        st.markdown('<div class="empty-state">Selecciona o escribe una pregunta para comenzar</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
with tab_about:
    st.markdown("""
<div class="about-sec">
<h4>🏔 La festividad</h4>
<p>El Señor de Qoyllur Rit'i es una peregrinación andina que sincretiza el catolicismo
colonial con tradiciones ancestrales en torno al Apu Ausangate, espíritu protector de
la montaña más alta del Cusco (6,384 msnm). La festividad reúne a múltiples
<em>naciones</em> —comunidades con identidad ritual propia— que participan con danzas,
vestimentas ceremoniales y rituales específicos.</p>
<p>Entre sus elementos centrales destacan la subida nocturna de los Ukumaris al glaciar
Colque Punku (5,200 msnm), la <em>Lomada</em> —caminata ritual de 24 horas— y las
procesiones de las distintas naciones peregrinas. Declarada Patrimonio Cultural
Inmaterial de la Humanidad por la UNESCO.</p>
</div>
<div class="about-sec">
<h4>🔬 El proyecto</h4>
<p>Esta aplicación forma parte de una investigación sobre <strong>grafos de conocimiento
para el patrimonio inmaterial peruano</strong>. La ontología fue construida a partir de
trabajo de campo etnográfico con la Nación Paucartambo en la edición 2025.</p>
<p>El sistema implementa un pipeline <strong>GraphRAG</strong>
(<em>Retrieval-Augmented Generation</em>) que combina búsqueda semántica sobre el grafo
RDF con generación de lenguaje natural, permitiendo consultas en lenguaje natural sobre
el conocimiento documentado.</p>
</div>
<div class="about-sec">
<h4>⚙️ Stack técnico</h4>
<div class="chips">
  <span class="chip g">GraphRAG v4.0</span>
  <span class="chip g">Knowledge Graph</span>
  <span class="chip g">Patrimonio Inmaterial</span>
  <span class="chip b">OWL 2</span>
  <span class="chip b">Turtle (.ttl)</span>
  <span class="chip b">RDF / RDFS</span>
  <span class="chip">Groq API</span>
  <span class="chip">llama-3.3-70b</span>
  <span class="chip">sentence-transformers</span>
  <span class="chip">rdflib</span>
  <span class="chip">Streamlit</span>
</div>
</div>
<div class="about-sec">
<h4>📐 Arquitectura</h4>
<p>La ontología modela eventos rituales, lugares sagrados, participantes, objetos
ceremoniales, danzas y vestimentas. La búsqueda híbrida combina embeddings semánticos
(<code>paraphrase-multilingual-MiniLM-L12-v2</code>) con BM25 léxico para recuperar
las entidades más relevantes. El contexto se entrega al LLM junto con un prompt que
prioriza precisión factual sobre interpretación libre.</p>
</div>
""", unsafe_allow_html=True)

    try:
        from rdflib import Graph as RDFGraph
        _g = RDFGraph()
        _g.parse("qoyllurity.ttl", format='turtle')
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Tripletas RDF", len(_g))
        with c2:
            st.metric("Entidades", len(set(s for s, _, _ in _g)))
        with c3:
            st.metric("Propiedades", len(set(p for _, p, _ in _g)))
    except Exception:
        pass

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="tfooter">
    <p>🏔️ <b>Qoyllur Rit'i Explorer</b> · GraphRAG v4.0</p>
    <p>Knowledge Graph + RAG · Datos de campo · Nación Paucartambo · 2025</p>
    <p style="color:#30363d;font-size:0.65rem;margin-top:0.3rem;">
        OWL 2 / Turtle · Groq llama-3.3-70b · paraphrase-multilingual-MiniLM-L12-v2
    </p>
</div>
""", unsafe_allow_html=True)
