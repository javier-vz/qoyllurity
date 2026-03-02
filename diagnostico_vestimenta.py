#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de diagnóstico para verificar qué contexto se genera
para la query sobre vestimenta de ukukus
"""

import os
from dotenv import load_dotenv
from graphrag_v4_api import GraphRAG_v4_API
from config_graphrag import Config

load_dotenv()

# Configuración
TTL_PATH = "qoyllurity.ttl"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("❌ GROQ_API_KEY no configurada en .env")
    exit(1)

# Inicializar
print("🚀 Inicializando GraphRAG...")
rag = GraphRAG_v4_API(
    ttl_path=TTL_PATH,
    groq_api_key=GROQ_API_KEY,
    verbose=False
)

print(f"✅ Grafo cargado: {len(rag.entidades)} entidades\n")

# ============================================================================
# FASE 1: BÚSQUEDA
# ============================================================================

query = "vestimenta ukukus"
print("="*70)
print(f"BÚSQUEDA: '{query}'")
print("="*70)

resultados = rag.buscar_hibrido(query, top_k=10)

print(f"\n📊 Top 10 resultados:\n")
for i, (ent_id, score) in enumerate(resultados[:10], 1):
    ent = rag.entidades[ent_id]
    nombre = ent.get('labels', [ent_id])[0]
    tipos = ent.get('tipos', [])
    
    # Detectar si es clase o instancia
    es_clase = any('Class' in t for t in tipos)
    tipo_str = "CLASE" if es_clase else "INSTANCIA"
    
    print(f"{i:2d}. [{tipo_str:9s}] {nombre:30s} ({score:.3f})")
    
    # Verificar si tiene tieneParte
    relaciones = ent.get('relaciones', {})
    if 'tieneParte' in relaciones:
        partes = relaciones['tieneParte']
        print(f"    🔧 tieneParte: {len(partes)} partes")
        for parte_id in partes[:3]:
            parte = rag.entidades.get(parte_id, {})
            parte_nombre = parte.get('labels', [parte_id])[0]
            print(f"       - {parte_nombre}")
        if len(partes) > 3:
            print(f"       ... y {len(partes)-3} más")

# ============================================================================
# FASE 2: CONTEXTO
# ============================================================================

print("\n" + "="*70)
print("CONTEXTO GENERADO")
print("="*70)

entidades_ids = [ent_id for ent_id, _ in resultados[:Config.TOP_K_CONTEXTO]]
contexto = rag.construir_contexto(entidades_ids)

print(f"\n{contexto}\n")

print("="*70)
print(f"Contexto: {len(contexto)} caracteres")
print("="*70)

# ============================================================================
# FASE 3: VERIFICAR TRAJE ESPECÍFICAMENTE
# ============================================================================

print("\n" + "="*70)
print("VERIFICACIÓN: TrajeUkumari")
print("="*70)

# Buscar TrajeUkumari en el grafo
traje_id = None
for ent_id, ent in rag.entidades.items():
    labels = ent.get('labels', [])
    if 'Traje de Ukumari' in labels or 'TrajeUkumari' in labels:
        traje_id = ent_id
        break

if traje_id:
    print(f"✅ TrajeUkumari encontrado: {traje_id}")
    
    traje = rag.entidades[traje_id]
    
    # Mostrar info completa
    print(f"\nLabels: {traje.get('labels', [])}")
    print(f"Comments: {traje.get('comments', [])[:200]}...")
    
    # Mostrar partes
    relaciones = traje.get('relaciones', {})
    if 'tieneParte' in relaciones:
        print(f"\nPartes ({len(relaciones['tieneParte'])}):")
        for parte_id in relaciones['tieneParte']:
            parte = rag.entidades.get(parte_id, {})
            parte_nombre = parte.get('labels', [parte_id])[0]
            parte_comment = parte.get('comments', [''])[0][:60]
            
            # Material
            material = ""
            parte_rels = parte.get('relaciones', {})
            if 'hechoDeRitual' in parte_rels:
                material = f" | Material: {parte_rels['hechoDeRitual'][0]}"
            
            print(f"  • {parte_nombre}: {parte_comment}{material}")
    
    # Ver si está en los resultados de búsqueda
    ranking = next((i for i, (eid, _) in enumerate(resultados, 1) if eid == traje_id), None)
    if ranking:
        print(f"\n📍 Ranking en búsqueda: #{ranking}")
    else:
        print(f"\n⚠️  NO apareció en top 10 de búsqueda")
        
else:
    print("❌ TrajeUkumari NO encontrado en el grafo")

# ============================================================================
# FASE 4: RESPUESTA DEL LLM
# ============================================================================

print("\n" + "="*70)
print("RESPUESTA DEL LLM")
print("="*70)

respuesta = rag.responder("Háblame de la vestimenta de los ukukus", use_api=True, verbose=False)
print(f"\n{respuesta}\n")

print("="*70)
print("FIN DEL DIAGNÓSTICO")
print("="*70)
