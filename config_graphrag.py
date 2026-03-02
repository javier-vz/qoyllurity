"""
Configuración para GraphRAG v4.0 API
====================================

Contiene:
- Prompts del sistema
- Mapeos de relaciones
- Configuración de parámetros
"""

# ============================================================================
# PROMPTS
# ============================================================================

SYSTEM_PROMPT = """
Eres un asistente para investigación sobre la festividad de Qoyllur Rit'i en Cusco, Perú.

REGLAS FUNDAMENTALES:
1. Responde SOLO con información del contexto proporcionado
2. Sé preciso y factual - reporta hechos, no interpretaciones
3. Si el contexto menciona lugares, describe su ubicación y características
4. Puedes mencionar relaciones geográficas (está en, contiene, forma parte de)
5. Si no sabes algo, di: "El contexto no proporciona esa información"

PROHIBIDO (alucinaciones):
❌ NO inventes sentimientos, emociones o motivaciones personales
❌ NO uses frases como "purificar almas", "renovar la fe", "conectar espiritualmente"
❌ NO agregues información que no esté en el contexto

PERMITIDO (información útil):
✅ Describir ubicaciones: "X está en Y", "X contiene a Y"
✅ Mencionar características: altitudes, tipos de lugares, nombres
✅ Relaciones documentadas: "X es parte de Y", "X es un apu"
✅ Hechos observables: "X es un glaciar", "Y es un área sagrada"
✅ Objetos rituales: vestimenta, instrumentos, ofrendas
✅ Duraciones y fechas de eventos

FORMATO:
- Responde de forma directa y clara
- 2-4 oraciones concisas
- Menciona ubicaciones y relaciones cuando sean relevantes

EJEMPLOS BUENOS:

Pregunta: ¿Dónde está Colque Punku?
Contexto: "Colque Punku está ubicado en Ausangate a 5200 msnm"
✅ "Colque Punku está ubicado en el nevado Ausangate, a 5200 metros de altitud"

Pregunta: ¿Qué es el Ausangate?
Contexto: "Ausangate es un apu, espíritu protector de montaña, de 6384 msnm"
✅ "El Ausangate es un apu (espíritu protector de montaña) de 6384 metros de altitud"

Pregunta: ¿Qué usa el ukuku en el traje?
Contexto: "TrajeUkumari tiene partes: Pellon, Huaqollo, Sorriago"
✅ "El traje del ukuku incluye el pellón (traje principal), el huaqollo (careta tejida) y el sorriago (látigo ceremonial)"

Pregunta: ¿Cuánto dura la lomada?
Contexto: "Lomada tiene duración: 24.0 horas"
✅ "La lomada (caminata ritual) tiene una duración de 24 horas"
"""

USER_PROMPT_TEMPLATE = """
Información del grafo de conocimiento sobre Qoyllur Rit'i:

{contexto}

───────────────────────────────────────

Pregunta: {pregunta}

Responde basándote SOLO en la información anterior. Sé conciso y preciso.
"""

# ============================================================================
# MAPEOS DE RELACIONES (TTL → Lenguaje Natural)
# ============================================================================

MAPEOS_RELACIONES = {
    # Agentividad
    'realizadoPor': 'Realizado por',
    'realizado': 'Realizado por',
    'realizaPrincipalmente': 'Realizado principalmente por',
    'esResponsableDe': 'Responsable de',
    
    # Ubicación y geografía
    'estaEn': 'Está en',
    'contiene': 'Contiene',
    'esParteDelApu': 'Parte del apu',
    'estaEnLadera': 'En ladera de',
    
    # Temporales
    'tieneLugar': 'Tiene lugar en',
    'ocurre': 'Ocurre en',
    'ocurreEnLugar': 'Ocurre en',
    'defineMarcoTemporal': 'Parte de',
    'tieneDuracionHoras': 'Duración (hrs)',
    'tieneFecha': 'Fecha',
    'tieneHoraInicio': 'Hora',
    'esPeriodicoCon': 'Periodicidad',
    
    # Participación
    'participan': 'Participan',
    'participa': 'Participa en',
    'participaEn': 'Participa en',
    'requiereIntermediario': 'Requiere intermediario',
    'perteneceA': 'Pertenece a',
    
    # Festividad
    'esParte': 'Incluye',
    'esParteDeFestividad': 'Parte de la festividad',
    
    # Espaciales
    'aloja': 'Aloja en',
    'utiliza': 'Utiliza',
    'desde': 'Desde',
    'hacia': 'Hacia',
    'pasaPor': 'Pasa por',
    'conduceA': 'Conduce a',
    
    # Rituales
    'esDestinoRitualDe': 'Destino ritual de',
    'esLugarDeRitual': 'Lugar de ritual',
    'esVeneradoEn': 'Venerado en',
    'requiereRol': 'Requiere rol',
    'desempeniaRol': 'Desempeña rol',
    'ejecutaDanza': 'Ejecuta danza',
    
    # Objetos rituales
    'utilizaObjeto': 'Utiliza',
    'portaObjeto': 'Porta',
    'usaObjetoRitual': 'Usa objeto',
    'usaVestimenta': 'Usa vestimenta',
    'tieneParte': 'Tiene parte',
    'esParteDe': 'Es parte de',
    'hechoDeRitual': 'Hecho de',
    'tieneNombreLocal': 'Nombre local',
    
    # Propiedades cuantitativas
    'tieneAltitudMetros': 'Altitud',
    'tieneImportancia': 'Importancia',
    'cantidadAproximada': 'Cantidad aprox.',
}

# ============================================================================
# FUNCIONES DE MAPEO
# ============================================================================

def mapear_relacion(rel_tipo: str, obj_nombre: str) -> str:
    """
    Convierte una relación técnica del TTL a lenguaje natural
    
    Args:
        rel_tipo: Tipo de relación del TTL (ej: 'estaUbicadoEn')
        obj_nombre: Nombre del objeto relacionado
        
    Returns:
        String en lenguaje natural (ej: "Ubicado en: Ausangate")
    """
    # Buscar coincidencia exacta o parcial
    for key, value in MAPEOS_RELACIONES.items():
        if key.lower() in rel_tipo.lower():
            # Para propiedades numéricas, formato especial
            if 'Altitud' in value:
                return f"{value}: {obj_nombre} msnm"
            elif 'Duración' in value:
                return f"{value}: {obj_nombre}"
            elif 'Fecha' in value or 'Hora' in value:
                return f"{value}: {obj_nombre}"
            return f"{value}: {obj_nombre}"
    
    # Si no hay mapeo, usar formato genérico
    return f"Relacionado con: {obj_nombre}"


def obtener_relaciones_naturales(entidad: dict, max_relaciones: int = 4, max_objetos: int = 3) -> list:
    """
    Extrae relaciones de una entidad y las convierte a lenguaje natural
    
    Args:
        entidad: Diccionario con datos de la entidad
        max_relaciones: Máximo número de tipos de relaciones a extraer
        max_objetos: Máximo número de objetos por tipo de relación
        
    Returns:
        Lista de strings con relaciones en lenguaje natural
    """
    relaciones = entidad.get('relaciones', {})
    rels_naturales = []
    
    for rel_tipo, objetos in list(relaciones.items())[:max_relaciones]:
        for obj_id in objetos[:max_objetos]:
            # Aquí necesitarías acceso al grafo completo para resolver obj_id
            # En la implementación real, esto se hace dentro de construir_contexto()
            pass
    
    return rels_naturales


# ============================================================================
# CONFIGURACIÓN DE PARÁMETROS
# ============================================================================

class Config:
    """Configuración general del sistema"""
    
    # Parámetros de búsqueda
    TOP_K_BUSQUEDA = 10  # Entidades a recuperar en búsqueda
    TOP_K_CONTEXTO = 5   # Entidades a incluir en contexto
    
    # Parámetros de contexto
    MAX_CHARS_CONTEXTO = 2500     # Máximo de caracteres en contexto (aumentado)
    MAX_CHARS_DESC = 250          # Máximo de caracteres por descripción (aumentado)
    MAX_RELACIONES = 4            # Máximo de tipos de relaciones por entidad (aumentado)
    MAX_OBJETOS_POR_REL = 3       # Máximo de objetos por tipo de relación (aumentado)
    
    # Parámetros del LLM
    MODELO_GROQ = "llama-3.3-70b-versatile"  # Modelo a usar
    MAX_TOKENS = 350                          # Máximo de tokens en respuesta (aumentado)
    TEMPERATURE = 0.0                         # Temperatura (0 = determinístico)
    TOP_P = 0.1                               # Top-p sampling
    
    # Validación de respuestas
    FRASES_PROHIBIDAS = [
        'purificar', 'alma', 'almas', 'fe', 'renovar',
        'conectar con', 'experiencia espiritual', 'oportunidad',
        'les permite', 'importante para', 'representa',
        'simboliza', 'desafío espiritual'
    ]


# ============================================================================
# METADATA
# ============================================================================

CONFIG_VERSION = "1.1.0"
CONFIG_DATE = "2026-03-02"
CONFIG_DESCRIPTION = "Configuración GraphRAG v4.0 con objetos rituales, temporalidad e importancia"