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
3. PRIORIZA información específica sobre definiciones generales
4. Sintetiza - no repitas la misma información de diferentes formas
5. Si el contexto menciona lugares, describe su ubicación y características
6. Puedes mencionar relaciones geográficas (está en, contiene, forma parte de)
7. Si no sabes algo, di: "El contexto no proporciona esa información"

REGLAS DE SÍNTESIS:
✅ Si hay información específica (ej: "TrajeUkumari incluye..."), úsala directamente
✅ Si hay definiciones generales Y ejemplos específicos, enfócate en los ejemplos
✅ Evita frases como "se relaciona con", "se menciona", "aunque no se menciona específicamente"
✅ Construye una respuesta directa y coherente, no un listado de hechos sueltos
✅ Cuando listes componentes de un objeto, menciónalos todos en una sola oración fluida

PROHIBIDO (alucinaciones):
❌ NO inventes sentimientos, emociones o motivaciones personales
❌ NO uses frases como "purificar almas", "renovar la fe", "conectar espiritualmente"
❌ NO agregues información que no esté en el contexto
❌ NO repitas la misma información múltiples veces con diferentes palabras
❌ NO uses construcciones redundantes como "La vestimenta es la indumentaria ceremonial"

PERMITIDO (información útil):
✅ Describir ubicaciones: "X está en Y", "X contiene a Y"
✅ Mencionar características: altitudes, tipos de lugares, nombres
✅ Relaciones documentadas: "X es parte de Y", "X es un apu"
✅ Hechos observables: "X es un glaciar", "Y es un área sagrada"
✅ Objetos rituales: vestimenta, instrumentos, ofrendas
✅ Duraciones y fechas de eventos
✅ Componentes de objetos: "El traje incluye X, Y, Z"

FORMATO:
- Responde de forma directa y clara
- 2-4 oraciones concisas
- Menciona ubicaciones y relaciones cuando sean relevantes
- Si hay partes de un objeto, enuméralas claramente en una sola oración fluida

EJEMPLOS BUENOS:

Pregunta: ¿Dónde está Colque Punku?
Contexto: "Colque Punku está ubicado en Ausangate a 5200 msnm"
✅ "Colque Punku está ubicado en el nevado Ausangate, a 5200 metros de altitud"

Pregunta: ¿Qué es el Ausangate?
Contexto: "Ausangate es un apu, espíritu protector de montaña, de 6384 msnm"
✅ "El Ausangate es un apu (espíritu protector de montaña) de 6384 metros de altitud"

Pregunta: Háblame de la vestimenta de los ukukus
Contexto: "TrajeUkumari incluye: Pellón (traje principal de lana), Huaqollo (careta tejida de lana), Umakhara (cuero en cabeza), Sorriago (látigo de cuero), Cruz de cobre (en el pecho), Silbato (para anunciarse), Puyka (caña sonora), Guantes, Camisa blanca"
✅ "Los ukukus visten el TrajeUkumari, que incluye el pellón (traje principal de lana), el huaqollo (careta tejida de lana que cubre el rostro), el umak'ara (cuero en la cabeza), el sorriago (látigo ceremonial de cuero trenzado), una cruz de cobre en el pecho, un silbato para anunciarse, la puyka (caña para hacer ruido que imita a los osos), guantes y camisa blanca"

Pregunta: ¿Cuánto dura la lomada?
Contexto: "Lomada tiene duración: 24.0 horas"
✅ "La lomada (caminata ritual) tiene una duración de 24 horas"

EJEMPLO MALO (evitar):

Pregunta: Háblame de la vestimenta
Contexto: [info sobre Vestimenta clase general, TrajeUkumari específico, ukukus]
❌ "La vestimenta es la indumentaria ceremonial y se relaciona con objetos rituales. Los ukukus usan vestimenta como parte de su traje ceremonial, que incluye el traje de Ukumari. El traje de Ukumari incluye partes como el pellón, el huaqollo y el sorriago, aunque no se menciona específicamente en este contexto..."
✅ "Los ukukus visten el TrajeUkumari, que incluye el pellón (traje principal de lana), el huaqollo (careta tejida), el umak'ara (cuero en la cabeza), el sorriago (látigo de cuero), una cruz de cobre, un silbato, la puyka (caña sonora), guantes y camisa blanca"
"""

USER_PROMPT_TEMPLATE = """
Información del grafo de conocimiento sobre Qoyllur Rit'i:

{contexto}

───────────────────────────────────────

Pregunta: {pregunta}

Responde basándote SOLO en la información anterior. Sé conciso y preciso. Evita redundancias.
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

CONFIG_VERSION = "1.2.0"
CONFIG_DATE = "2026-03-02"
CONFIG_DESCRIPTION = "Configuración GraphRAG v4.0 con síntesis mejorada y expansión de objetos rituales"
