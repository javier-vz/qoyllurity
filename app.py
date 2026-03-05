#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qoyllur Rit'i Explorer — v2.0
Dark mode · Mobile-first · GraphRAG v4.0
"""

import os
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Qoyllur Rit'i Explorer",
    page_icon="🏔️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# CSS — Dark mode consistente con el grafo HTML
# ============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* ── BASE ── */
html, body, [data-testid="stAppViewContainer"] {
    background: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

[data-testid="stAppViewBlockContainer"] {
    max-width: 680px;
    padding: 0 1rem 5rem 1rem;
}

/* ocultar chrome de streamlit */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── HEADER ── */
.app-header {
    position: sticky;
    top: 0;
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 0.75rem 0;
    margin: 0 -1rem 1.5rem -1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.app-header h1 {
    font-size: 1rem !important;
    font-weight: 700 !important;
    color: #e6edf3 !important;
    margin: 0 !important;
    padding: 0 !important;
    display: flex;
    align-items: center;
    gap: 7px;
}
.app-header .accent { color: #d4a017; }
.app-header .subtitle {
    font-size: 0.72rem;
    color: #8b949e;
    margin-left: auto;
    white-space: nowrap;
}

/* ── TABS ── */
[data-testid="stTabs"] > div:first-child {
    background: #161b22;
    border-radius: 8px;
    padding: 3px;
    border: 1px solid #30363d;
    gap: 2px;
}
[data-testid="stTabs"] button {
    background: transparent !important;
    color: #8b949e !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    padding: 0.4rem 1rem !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background: #21262d !important;
    color: #e6edf3 !important;
}
[data-testid="stTabs"] [data-testid="stMarkdownContainer"] { display: none; }

/* ── INPUTS ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div > div {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #e6edf3 !important;
    font-size: 0.9rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #d4a017 !important;
    box-shadow: 0 0 0 3px rgba(212,160,23,.15) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #8b949e !important; }

/* ── SELECTBOX ── */
[data-testid="stSelectbox"] > div > div {
    background: #21262d !important;
}
[data-testid="stSelectbox"] svg { fill: #8b949e !important; }

/* ── RADIO ── */
[data-testid="stRadio"] > div {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.4rem 0.6rem;
    gap: 0.5rem;
}
[data-testid="stRadio"] label {
    color: #8b949e !important;
    font-size: 0.83rem !important;
}
[data-testid="stRadio"] label[data-baseweb="radio"] span:first-child {
    border-color: #30363d !important;
    background: #21262d !important;
}
[data-testid="stRadio"] [aria-checked="true"] label { color: #e6edf3 !important; }

/* ── BOTÓN PRINCIPAL ── */
[data-testid="stButton"] > button[kind="primary"] {
    background: #d4a017 !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    padding: 0.55rem 1.5rem !important;
    width: 100% !important;
    box-shadow: 0 2px 8px rgba(212,160,23,.3) !important;
}
[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #b8891a !important;
    box-shadow: 0 4px 12px rgba(212,160,23,.4) !important;
}

/* ── BOTÓN SECUNDARIO ── */
[data-testid="stButton"] > button[kind="secondary"] {
    background: #21262d !important;
    color: #8b949e !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    font-size: 0.82rem !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
}
[data-testid="stExpander"] summary {
    color: #8b949e !important;
    font-size: 0.82rem !important;
}

/* ── ALERTAS ── */
[data-testid="stAlert"] {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
}
[data-testid="stAlert"][data-baseweb="notification"] {
    border-color: #388bfd !important;
}

/* ── SPINNER ── */
[data-testid="stSpinner"] > div {
    color: #d4a017 !important;
}

/* ── DIVIDER ── */
hr {
    border-color: #30363d !important;
    margin: 1rem 0 !important;
}

/* ── CHAT MESSAGES ── */
.msg-user {
    background: #1f6feb22;
    border: 1px solid #388bfd44;
    border-radius: 10px 10px 4px 10px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #e6edf3;
}
.msg-user .label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #388bfd;
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 4px;
}
.msg-bot {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 3px solid #d4a017;
    border-radius: 4px 10px 10px 10px;
    padding: 0.75rem 1rem;
    margin: 0.5rem 0;
    font-size: 0.88rem;
    color: #adbac7;
    line-height: 1.65;
}
.msg-bot .label {
    font-size: 0.7rem;
    font-weight: 600;
    color: #d4a017;
    text-transform: uppercase;
    letter-spacing: .5px;
    margin-bottom: 4px;
}

/* ── ABOUT SECTIONS ── */
.about-section {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 0.85rem;
}
.about-section h3 {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: .5px;
    color: #d4a017 !important;
    margin: 0 0 0.6rem 0 !important;
}
.about-section p {
    font-size: 0.84rem;
    line-height: 1.7;
    color: #adbac7;
    margin: 0;
}
.about-section p + p { margin-top: 0.5rem; }

/* ── TECH CHIPS ── */
.chips { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
.chip {
    font-size: 0.67rem;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    font-family: monospace;
    border: 1px solid #30363d;
    background: rgba(255,255,255,.04);
    color: #adbac7;
}
.chip.blue {
    background: rgba(56,139,253,.1);
    border-color: rgba(56,139,253,.3);
    color: #79c0ff;
}
.chip.gold {
    background: rgba(212,160,23,.1);
    border-color: rgba(212,160,23,.3);
    color: #d4a017;
}

/* ── FOOTER ── */
.tech-footer {
    margin-top: 2.5rem;
    padding-top: 1rem;
    border-top: 1px solid #30363d;
    text-align: center;
}
.tech-footer p {
    font-size: 0.72rem;
    color: #8b949e;
    margin: 0.2rem 0;
}
.tech-footer b { color: #adbac7; }

/* ── MÉTRICAS ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.75rem 1rem;
}
[data-testid="stMetricValue"] {
    color: #d4a017 !important;
    font-size: 1.4rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.72rem !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# ESTADO
# ============================================================================
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []
if 'motor_cargado' not in st.session_state:
    st.session_state.motor_cargado = False

def agregar_mensaje(tipo, texto):
    st.session_state.mensajes.append({'tipo': tipo, 'texto': texto})

def limpiar_chat():
    st.session_state.mensajes = []

# ============================================================================
# PREGUNTAS SUGERIDAS
# ============================================================================
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
    "¿Qué es Colque Punku?",
    "¿Cuál es el recorrido de la peregrinación?",
]

# ============================================================================
# CARGAR MOTOR — cacheable por key
# ============================================================================
@st.cache_resource
def cargar_motor(groq_key: str):
    from graphrag_v4_api import GraphRAG_v4_API
    motor = GraphRAG_v4_API(
        ttl_path="qoyllurity.ttl",
        groq_api_key=groq_key,
        verbose=False
    )
    return motor

# ============================================================================
# HEADER
# ============================================================================
st.markdown("""
<div class="app-header">
    <h1>
        <span class="accent">🏔</span> Qoyllur Rit'i
    </h1>
    <span class="subtitle">GraphRAG Explorer</span>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# TABS
# ============================================================================
tab_chat, tab_about = st.tabs(["💬  Consultas", "ℹ️  Acerca de"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — CHAT
# ─────────────────────────────────────────────────────────────────────────────
with tab_chat:

    # ── API KEY ──────────────────────────────────────────────────────────────
    groq_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
    if not groq_key:
        groq_key = os.getenv("GROQ_API_KEY", "")

    if not groq_key:
        groq_key = st.text_input(
            "Groq API Key",
            placeholder="gsk_...",
            type="password",
            help="Ingresa tu Groq API key para activar el sistema"
        )
        if not groq_key:
            st.info("🔑 Ingresa tu Groq API key para comenzar. Puedes obtenerla en console.groq.com")
            st.stop()

    # ── CARGAR MOTOR ─────────────────────────────────────────────────────────
    with st.spinner("Cargando sistema..."):
        try:
            motor = cargar_motor(groq_key)
        except ImportError as e:
            st.error(f"Falta archivo: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Error al inicializar: {e}")
            st.stop()

    # ── MODO DE ENTRADA ──────────────────────────────────────────────────────
    modo = st.radio(
        "modo",
        ["📋 Preguntas sugeridas", "✍️ Pregunta libre"],
        horizontal=True,
        label_visibility="collapsed"
    )

    pregunta = ""

    if modo == "📋 Preguntas sugeridas":
        pregunta = st.selectbox(
            "pregunta",
            options=[""] + PREGUNTAS,
            format_func=lambda x: "Selecciona una pregunta..." if x == "" else x,
            label_visibility="collapsed"
        )
    else:
        pregunta = st.text_input(
            "pregunta",
            placeholder="¿Dónde está el glaciar Colque Punku?",
            label_visibility="collapsed"
        )
        with st.expander("💡 Ejemplos de preguntas"):
            st.markdown("""
- ¿Qué es el Ausangate?
- ¿Dónde está Sinakara?
- ¿Qué hacen los ukukus?
- ¿Cuál es el recorrido de la peregrinación?
- ¿Cuánto dura la lomada?
            """)

    # ── BOTÓN ────────────────────────────────────────────────────────────────
    if st.button("✨ Preguntar", type="primary"):
        if pregunta:
            agregar_mensaje('user', pregunta)
            with st.spinner("Consultando grafo de conocimiento..."):
                try:
                    respuesta = motor.responder(
                        pregunta,
                        use_api=True,
                        modo="hibrido",
                        verbose=False
                    )
                    agregar_mensaje('bot', respuesta)
                except Exception as e:
                    agregar_mensaje('bot', f"❌ Error: {e}")
            st.rerun()

    # ── HISTORIAL ────────────────────────────────────────────────────────────
    if st.session_state.mensajes:
        st.markdown("---")

        # mostrar en orden inverso (más reciente arriba)
        for msg in reversed(st.session_state.mensajes):
            if msg['tipo'] == 'user':
                st.markdown(f"""
<div class="msg-user">
  <div class="label">Tú</div>
  {msg['texto']}
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div class="msg-bot">
  <div class="label">Asistente</div>
  {msg['texto']}
</div>""", unsafe_allow_html=True)

        st.markdown("")
        if st.button("🗑️ Limpiar historial", type="secondary"):
            limpiar_chat()
            st.rerun()

    else:
        st.markdown("""
<div style="text-align:center;padding:2rem 0;color:#8b949e;font-size:0.85rem;">
    Selecciona o escribe una pregunta para comenzar
</div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — ACERCA DE
# ─────────────────────────────────────────────────────────────────────────────
with tab_about:

    st.markdown("""
<div class="about-section">
<h3>🏔 La festividad</h3>
<p>El Señor de Qoyllur Rit'i es una peregrinación andina que sincretiza el catolicismo
colonial con tradiciones ancestrales en torno al Apu Ausangate, espíritu protector de
la montaña más alta del Cusco (6,384 msnm). La festividad reúne a múltiples
<em>naciones</em> —comunidades con identidad ritual propia— que participan con danzas,
vestimentas ceremoniales y rituales específicos.</p>
<p>Entre sus elementos centrales destacan la subida nocturna de los Ukumaris al glaciar
Colque Punku (5,200 msnm), la <em>Lomada</em> —caminata ritual de 24 horas con hitos
sagrados en la ruta— y las procesiones de las distintas naciones peregrinas.
Declarada Patrimonio Cultural Inmaterial de la Humanidad por la UNESCO.</p>
</div>

<div class="about-section">
<h3>🔬 El proyecto</h3>
<p>Esta aplicación forma parte de una investigación sobre <strong>grafos de conocimiento
para el patrimonio inmaterial peruano</strong>. La ontología fue construida a partir de
trabajo de campo etnográfico con la Nación Paucartambo durante la edición 2025.</p>
<p>El sistema implementa un pipeline <strong>GraphRAG</strong>
(<em>Retrieval-Augmented Generation</em>) que combina búsqueda semántica sobre el grafo
RDF con generación de lenguaje natural mediante un LLM, permitiendo consultas en
lenguaje natural sobre el conocimiento documentado.</p>
</div>

<div class="about-section">
<h3>⚙️ Stack técnico</h3>
<div class="chips">
  <span class="chip gold">GraphRAG v4.0</span>
  <span class="chip gold">Knowledge Graph</span>
  <span class="chip gold">Patrimonio Inmaterial</span>
  <span class="chip blue">OWL 2</span>
  <span class="chip blue">Turtle (.ttl)</span>
  <span class="chip blue">RDF / RDFS</span>
  <span class="chip blue">geo:lat/long</span>
  <span class="chip">Groq API</span>
  <span class="chip">llama-3.3-70b</span>
  <span class="chip">sentence-transformers</span>
  <span class="chip">rdflib</span>
  <span class="chip">Streamlit</span>
</div>
</div>

<div class="about-section">
<h3>📐 Arquitectura</h3>
<p>La ontología modela eventos rituales, lugares sagrados, participantes, objetos
ceremoniales, danzas y vestimentas en OWL/RDF. La búsqueda híbrida combina
embeddings semánticos (<code>paraphrase-multilingual-MiniLM-L12-v2</code>) con
BM25 léxico para recuperar las entidades más relevantes a cada consulta.
El contexto recuperado se entrega al LLM junto con un prompt de sistema
que prioriza precisión factual sobre interpretación.</p>
</div>
""", unsafe_allow_html=True)

    # ── MÉTRICAS ─────────────────────────────────────────────────────────────
    try:
        from rdflib import Graph as RDFGraph
        g = RDFGraph()
        g.parse("qoyllurity.ttl", format='turtle')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Tripletas RDF", len(g))
        with col2:
            sujetos = set(s for s, _, _ in g)
            st.metric("Entidades", len(sujetos))
        with col3:
            props = set(p for _, p, _ in g)
            st.metric("Propiedades", len(props))
    except Exception:
        pass

# ============================================================================
# FOOTER TÉCNICO
# ============================================================================
st.markdown("""
<div class="tech-footer">
    <p>🏔️ <b>Qoyllur Rit'i Explorer</b> · GraphRAG v4.0</p>
    <p>Knowledge Graph + RAG · Datos de campo · Nación Paucartambo · 2025</p>
    <p style="color:#30363d;font-size:0.65rem;margin-top:0.4rem;">
        OWL 2 / Turtle ontology · Groq llama-3.3-70b · paraphrase-multilingual-MiniLM-L12-v2
    </p>
</div>
""", unsafe_allow_html=True)
