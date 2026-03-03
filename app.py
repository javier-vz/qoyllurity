#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qoyllur Rit'i Explorer
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
from pathlib import Path
from rdflib import Graph, Literal, Namespace
from rdflib.namespace import RDFS, RDF
import os

st.set_page_config(
    page_title="Qoyllur Rit'i Explorer", 
    page_icon="🏔️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

GEO = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
FESTIVIDAD = Namespace("http://example.org/festividades#")

# ============================================================================
# CSS
# ============================================================================
st.markdown("""
<style>
    .main { 
        background: linear-gradient(135deg, #1a1f2e 0%, #2c5f8d 100%);
        padding: 1rem;
    }
    
    .block-container {
        max-width: 100%;
        padding: 1.5rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    h1 {
        color: #2c5f8d;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-align: center;
    }
    
    h2 {
        color: #2d3748;
        font-weight: 700;
        font-size: 1.3rem;
        margin-top: 0;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #2c5f8d;
        font-weight: 600;
        font-size: 1.1rem;
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
        color: #1a1f2e;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.5rem;
        font-weight: 700;
        font-size: 1rem;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
        width: 100%;
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(212, 175, 55, 0.6);
    }
    
    .stTextInput input, .stSelectbox select {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.6rem 1rem;
        font-size: 0.95rem;
    }
    
    .stTextInput input:focus {
        border-color: #2c5f8d;
        box-shadow: 0 0 0 3px rgba(44, 95, 141, 0.1);
    }
    
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2c5f8d;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.75rem;
        font-weight: 600;
        color: #718096;
    }
    
    .stRadio [role="radiogroup"] {
        gap: 0.75rem;
        background: #f7fafc;
        padding: 0.5rem;
        border-radius: 8px;
    }
    
    iframe {
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    .stAlert {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SISTEMA DE MENSAJES
# ============================================================================
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = []

def agregar_mensaje(tipo, texto):
    st.session_state.mensajes.append({'tipo': tipo, 'texto': texto})

def limpiar_chat():
    st.session_state.mensajes = []

# ============================================================================
# PREGUNTAS
# ============================================================================
PREGUNTAS_DESTACADAS = [
    "¿Qué es Qoyllur Rit'i?",
    "¿Dónde está el santuario?",
    "Háblame de la vestimenta de los ukukus",
    "¿Qué es el Ausangate?",
    "¿Dónde está Sinakara?",
    "¿Dónde está el glaciar Colque Punku?",
    "¿Qué hacen los ukukus?",
    "¿Qué es la lomada?",
    "¿Cuánto dura la lomada?",
]

# ============================================================================
# CARGAR GRAPHRAG
# ============================================================================
@st.cache_resource
def cargar_motor():
    try:
        from graphrag_v4_api import GraphRAG_v4_API
        
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
            for label in g.objects(s, RDFS.label):
                if isinstance(label, Literal):
                    nombre = str(label)
                    break
            
            nombre = nombre or str(s).split('#')[-1].replace('_', ' ')
            
            for comment in g.objects(s, RDFS.comment):
                if isinstance(comment, Literal):
                    descripcion = str(comment)
                    break
            
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
    if not lugares:
        m = folium.Map(location=[-13.5, -71.2], zoom_start=10)
        return m
    
    lats = [l["lat"] for l in lugares.values()]
    lons = [l["lon"] for l in lugares.values()]
    centro = [sum(lats) / len(lats), sum(lons) / len(lons)]
    
    m = folium.Map(location=centro, zoom_start=11, tiles='OpenStreetMap')
    
    for lugar in lugares.values():
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
        
        popup_html = f"""
        <div style="width: 220px;">
            <h4 style="color: #2c5f8d; margin: 0 0 8px 0;">{lugar['nombre']}</h4>
            <p style="color: #4a5568; font-size: 0.85rem; line-height: 1.5; margin: 0;">
                {lugar['descripcion'][:150]}{'...' if len(lugar['descripcion']) > 150 else ''}
            </p>
        </div>
        """
        
        folium.Marker(
            location=[lugar["lat"], lugar["lon"]],
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"<b>{lugar['nombre']}</b>",
            icon=folium.Icon(color=color, icon=icon, prefix='fa')
        ).add_to(m)
    
    return m

# ============================================================================
# MAIN
# ============================================================================
def main():
    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1.5rem 0;">
        <h1>🏔️ Qoyllur Rit'i</h1>
        <p style="font-size: 1.1rem; color: #718096; font-weight: 500; margin: 0;">
            Explora la peregrinación andina sagrada
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # 50/50 CHAT Y MAPA
    col_chat, col_mapa = st.columns([1, 1], gap="large")
    
    with col_chat:
        st.markdown("## 💬 Consultas")
        
        motor, error = cargar_motor()
        
        if motor:
            modo = st.radio(
                "Modo",
                ["📋 Seleccionar de la lista", "✍️ Escribir mi pregunta"],
                horizontal=True,
                label_visibility="collapsed"
            )
            
            pregunta = ""
            
            if modo == "📋 Seleccionar de la lista":
                pregunta = st.selectbox(
                    "Pregunta",
                    options=[""] + PREGUNTAS_DESTACADAS,
                    format_func=lambda x: "👆 Selecciona una pregunta..." if x == "" else x,
                    label_visibility="collapsed"
                )
            else:
                pregunta = st.text_input(
                    "Tu pregunta",
                    placeholder="Ejemplo: ¿Dónde está el Ausangate?",
                    label_visibility="collapsed"
                )
                
                with st.expander("💡 Ver ejemplos de preguntas"):
                    st.markdown("""
                    - ¿Qué es el Ausangate?
                    - ¿Dónde está Colque Punku?
                    - ¿Qué hacen los ukukus?
                    - ¿Cuál es el recorrido de la peregrinación?
                    """)
            
            btn = st.button("✨ Preguntar", type="primary")
            
            if btn and pregunta:
                agregar_mensaje('user', pregunta)
                
                with st.spinner("🔍 Consultando..."):
                    try:
                        respuesta = motor.responder(pregunta, use_api=True, modo="hibrido", verbose=False)
                        agregar_mensaje('bot', respuesta)
                    except Exception as e:
                        agregar_mensaje('bot', f"❌ Error: {e}")
                
                st.rerun()
            
            if st.session_state.mensajes:
                st.markdown("---")
                st.markdown("### 📜 Historial")
                
                for msg in st.session_state.mensajes:
                    if msg['tipo'] == 'user':
                        st.markdown(f"""
                        <div style="background: #2c5f8d; color: white; padding: 0.75rem 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <strong>Tú:</strong> {msg['texto']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background: #f0f4f8; padding: 0.75rem 1rem; border-radius: 8px; margin: 0.5rem 0; border-left: 3px solid #d4af37;">
                            <strong style="color: #2c5f8d;">Asistente:</strong><br>
                            <p style="margin: 0.5rem 0 0 0; color: #2d3748;">{msg['texto']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                if st.button("🗑️ Limpiar"):
                    limpiar_chat()
                    st.rerun()
            else:
                st.info("💡 Selecciona o escribe una pregunta")
        
        else:
            st.error(f"⚠️ Sistema no disponible: {error}")
    
    with col_mapa:
        st.markdown("### 📍 Mapa de Lugares")
        
        lugares = cargar_lugares()
        
        if lugares:
            m1, m2 = st.columns(2)
            
            with m1:
                st.metric("Lugares", len(lugares))
            
            with m2:
                apus = sum(1 for l in lugares.values() if 'Apu' in l['tipos'])
                st.metric("Apus", apus)
            
            mapa = crear_mapa(lugares)
            st_folium(mapa, width=None, height=550, returned_objects=[])
            
            st.caption("💡 Click en marcadores para más info")
        else:
            st.warning("⚠️ Sin lugares en TTL")

if __name__ == "__main__":
    main()