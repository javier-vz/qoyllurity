#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🏔️ Qoyllur Rit'i Explorer - Elegante y Simple
===============================================
GraphRAG v4.0 API + Mapa Interactivo
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from pathlib import Path
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDFS, RDF
import os

# ============================================================================
# CONFIGURACIÓN
# ============================================================================
st.set_page_config(
    page_title="Qoyllur Rit'i Explorer", 
    page_icon="🏔️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Namespaces
GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
FESTIVIDAD = Namespace("http://example.org/festividades#")

# ============================================================================
# CSS ELEGANTE
# ============================================================================
st.markdown("""
<style>
    /* Fondo degradado */
    .main { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
    }
    
    /* Contenedor principal */
    .block-container {
        max-width: 1400px;
        padding: 2rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Títulos */
    h1 {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.5rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: #4a5568;
        font-weight: 600;
    }
    
    /* Tabs elegantes */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f7fafc;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        background: transparent;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(102, 126, 234, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
    }
    
    /* Botón principal */
    .stButton button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Card de respuesta */
    .respuesta-card {
        background: linear-gradient(135deg, #f6f8fb 0%, #ffffff 100%);
        border-left: 6px solid #667eea;
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Inputs */
    .stTextInput input, .stSelectbox select {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Métricas */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 600;
        color: #718096;
    }
    
    /* Radio buttons */
    .stRadio [role="radiogroup"] {
        gap: 1rem;
        background: #f7fafc;
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stRadio [role="radio"] {
        border-radius: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f7fafc;
        border-radius: 12px;
        font-weight: 600;
    }
    
    /* Mapa */
    iframe {
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* Info/Warning boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
    }
    
    /* Ocultar elementos */
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# PREGUNTAS
# ============================================================================
PREGUNTAS_DESTACADAS = [
    "¿Qué es Qoyllur Rit'i?",
    "¿Qué es el Ausangate?",
    "¿Qué es Sinakara?",
    "¿Dónde está el glaciar Colque Punku?",
    "¿Dónde está el santuario?",
    "¿Qué hacen los ukukus?",
    "¿Qué es la lomada?",
    "¿Quién realiza la lomada?",
    "¿Qué eventos hay el día 2?",
    "¿Cuál es el recorrido de la peregrinación?"
]

# ============================================================================
# CARGAR GRAPHRAG V4.0
# ============================================================================
@st.cache_resource
def cargar_motor():
    """Carga GraphRAG v4.0 API"""
    try:
        from graphrag_v4_api import GraphRAG_v4_API
        
        # Obtener API key (secrets de Streamlit Cloud o variable de entorno)
        groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
        
        if not groq_key:
            return None, "No se encontró GROQ_API_KEY"
        
        motor = GraphRAG_v4_API(
            ttl_path="qoyllurity.ttl",
            groq_api_key=groq_key,
            verbose=False
        )
        
        return motor, None
        
    except ImportError as e:
        return None, f"Falta archivo: {e}"
    except Exception as e:
        return None, f"Error: {e}"

# ============================================================================
# CARGAR LUGARES
# ============================================================================
@st.cache_resource
def cargar_lugares():
    """Extrae lugares del TTL"""
    ttl_path = "qoyllurity.ttl"
    
    if not Path(ttl_path).exists():
        return {}
    
    g = Graph()
    try:
        g.parse(ttl_path, format='turtle')
    except:
        return {}
    
    lugares = {}
    
    for s in g.subjects():
        lat = lon = nombre = descripcion = None
        tipos = []
        
        # Coordenadas
        for lat_val in g.objects(s, GEO.lat):
            try:
                lat = float(lat_val)
            except:
                pass
        
        for lon_val in g.objects(s, GEO.long):
            try:
                lon = float(lon_val)
            except:
                pass
        
        if lat and lon:
            # Nombre
            for label in g.objects(s, RDFS.label):
                if isinstance(label, Literal):
                    nombre = str(label)
                    break
            
            nombre = nombre or str(s).split('#')[-1].replace('_', ' ')
            
            # Descripción
            for comment in g.objects(s, RDFS.comment):
                if isinstance(comment, Literal):
                    descripcion = str(comment)
                    break
            
            # Tipos
            for tipo in g.objects(s, RDF.type):
                tipo_str = str(tipo).split('#')[-1]
                if tipo_str not in ['NamedIndividual']:
                    tipos.append(tipo_str)
            
            lugares[str(s).split('#')[-1]] = {
                "lat": lat,
                "lon": lon,
                "nombre": nombre,
                "descripcion": descripcion or "Sin descripción",
                "tipos": tipos
            }
    
    return lugares

# ============================================================================
# CREAR MAPA
# ============================================================================
def crear_mapa(lugares):
    """Crea mapa Folium elegante"""
    
    if not lugares:
        m = folium.Map(location=[-13.5, -71.2], zoom_start=10)
        return m
    
    # Centro del mapa
    lats = [l["lat"] for l in lugares.values()]
    lons = [l["lon"] for l in lugares.values()]
    centro = [sum(lats) / len(lats), sum(lons) / len(lons)]
    
    # Crear mapa
    m = folium.Map(
        location=centro,
        zoom_start=11,
        tiles='OpenStreetMap'
    )
    
    # Marcadores
    for lugar in lugares.values():
        # Color según tipo
        if 'Apu' in lugar['tipos']:
            color, icon = 'purple', 'mountain'
        elif 'Glaciar' in lugar['tipos']:
            color, icon = 'lightblue', 'snowflake'
        elif 'Santuario' in lugar['tipos'] or 'Iglesia' in lugar['tipos']:
            color, icon = 'red', 'church'
        elif 'LugarSagrado' in lugar['tipos']:
            color, icon = 'orange', 'star'
        else:
            color, icon = 'blue', 'map-marker'
        
        # Popup
        popup_html = f"""
        <div style="width: 280px; font-family: 'Segoe UI', sans-serif;">
            <h4 style="color: #2d3748; margin: 0 0 12px 0; font-size: 1.1rem;">
                {lugar['nombre']}
            </h4>
            <p style="color: #4a5568; font-size: 0.95rem; line-height: 1.6; margin: 0;">
                {lugar['descripcion'][:200]}{'...' if len(lugar['descripcion']) > 200 else ''}
            </p>
            <p style="color: #a0aec0; font-size: 0.85rem; margin-top: 12px; padding-top: 12px; border-top: 1px solid #e2e8f0;">
                📍 {lugar['lat']:.5f}, {lugar['lon']:.5f}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[lugar["lat"], lugar["lon"]],
            popup=folium.Popup(popup_html, max_width=320),
            tooltip=f"<b>{lugar['nombre']}</b>",
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
    
    return m

# ============================================================================
# MAIN
# ============================================================================
def main():
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0 2rem 0;">
        <h1>🏔️ Qoyllur Rit'i</h1>
        <p style="font-size: 1.3rem; color: #718096; font-weight: 500;">
            Explora la peregrinación andina sagrada
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2 = st.tabs(["🗺️ Mapa Interactivo", "💬 Pregunta a la IA"])
    
    # ========================================================================
    # TAB 1: MAPA
    # ========================================================================
    with tab1:
        lugares = cargar_lugares()
        
        if lugares:
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📍 Lugares", len(lugares))
            
            with col2:
                apus = sum(1 for l in lugares.values() if 'Apu' in l['tipos'])
                st.metric("⛰️ Apus", apus)
            
            with col3:
                sagrados = sum(1 for l in lugares.values() if 'LugarSagrado' in l['tipos'])
                st.metric("✨ Sagrados", sagrados)
            
            with col4:
                santuarios = sum(1 for l in lugares.values() if 'Santuario' in l['tipos'] or 'Iglesia' in l['tipos'])
                st.metric("⛪ Santuarios", santuarios)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Mapa
            mapa = crear_mapa(lugares)
            st_folium(mapa, width=None, height=650, returned_objects=[])
            
            st.info("💡 **Tip:** Haz clic en los marcadores del mapa para ver más información")
            
        else:
            st.warning("⚠️ No se encontraron lugares en el archivo TTL")
    
    # ========================================================================
    # TAB 2: PREGUNTAS IA
    # ========================================================================
    with tab2:
        motor, error = cargar_motor()
        
        if motor:
            st.markdown("## 💬 Hazle una pregunta sobre la festividad")
            
            # Modo
            modo = st.radio(
                "¿Cómo quieres preguntar?",
                ["📋 Seleccionar de la lista", "✍️ Escribir mi pregunta"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            pregunta = ""
            
            # UI según modo
            if modo == "📋 Seleccionar de la lista":
                col1, col2 = st.columns([5, 1])
                with col1:
                    pregunta = st.selectbox(
                        "Pregunta",
                        options=[""] + PREGUNTAS_DESTACADAS,
                        format_func=lambda x: "👆 Selecciona una pregunta..." if x == "" else x,
                        label_visibility="collapsed"
                    )
                with col2:
                    st.markdown("<div style='margin-top: 8px;'>", unsafe_allow_html=True)
                    btn = st.button("✨ Preguntar", type="primary")
                    st.markdown("</div>", unsafe_allow_html=True)
            
            else:
                col1, col2 = st.columns([5, 1])
                with col1:
                    pregunta = st.text_input(
                        "Tu pregunta",
                        placeholder="Ejemplo: ¿Dónde está el Ausangate?",
                        label_visibility="collapsed"
                    )
                with col2:
                    st.markdown("<div style='margin-top: 8px;'>", unsafe_allow_html=True)
                    btn = st.button("✨ Preguntar", type="primary")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                # Ejemplos
                with st.expander("💡 Ver ejemplos de preguntas"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("""
                        **📍 Sobre lugares:**
                        - ¿Qué es el Ausangate?
                        - ¿Dónde está Colque Punku?
                        - ¿Qué es Sinakara?
                        - ¿Dónde está el santuario?
                        """)
                    with col2:
                        st.markdown("""
                        **🎭 Sobre la festividad:**
                        - ¿Qué hacen los ukukus?
                        - ¿Quién realiza la lomada?
                        - ¿Qué eventos hay el día 2?
                        - ¿Cuál es el recorrido?
                        """)
            
            # Procesar
            if btn and pregunta:
                with st.spinner("🔍 Consultando el grafo de conocimiento..."):
                    try:
                        respuesta = motor.responder(
                            pregunta,
                            use_api=True,
                            modo="hibrido",
                            verbose=False
                        )
                        
                        # Mostrar respuesta
                        st.markdown(f"""
                        <div class="respuesta-card">
                            <div style="display: flex; align-items: start; gap: 1.5rem; margin-bottom: 1.5rem;">
                                <div style="font-size: 3rem; line-height: 1;">💬</div>
                                <div style="flex: 1;">
                                    <p style="color: #a0aec0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin: 0; font-weight: 600;">
                                        Pregunta
                                    </p>
                                    <h3 style="color: #2d3748; margin: 0.5rem 0 0 0; font-size: 1.4rem; line-height: 1.4;">
                                        {pregunta}
                                    </h3>
                                </div>
                            </div>
                            <div style="border-top: 2px solid #e2e8f0; padding-top: 1.5rem;">
                                <p style="color: #a0aec0; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px; margin: 0 0 1rem 0; font-weight: 600;">
                                    Respuesta
                                </p>
                                <p style="color: #2d3748; font-size: 1.15rem; line-height: 1.8; margin: 0;">
                                    {respuesta}
                                </p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"❌ Error al procesar: {e}")
            
            elif btn:
                st.warning("⚠️ Por favor escribe o selecciona una pregunta")
        
        else:
            st.error(f"""
            ⚠️ **Sistema de IA no disponible**
            
            **Error:** {error}
            
            **Necesitas:**
            1. Configurar `GROQ_API_KEY` en Streamlit Secrets
            2. Archivos: `graphrag_v4_api.py`, `config_graphrag.py`
            3. Archivo: `qoyllurity.ttl`
            """)
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0 1rem 0; border-top: 2px solid #e2e8f0;">
        <p style="color: #a0aec0; font-size: 0.95rem; margin: 0;">
            🏔️ <b>Qoyllur Rit'i Explorer</b> | Powered by GraphRAG v4.0 API + Groq
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
