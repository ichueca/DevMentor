"""
Servicio que detecta automáticamente el tipo de prompt
y permite utilizar un tamplate espacializado
"""
from typing import Dict, Any, Optional
from enum import Enum

from utils.prompt_guardrails import PromptGuardrails


class PromptType(Enum):
    """Tipos de prompts disponibles"""
    GENERAL = "general"
    CODE_REVIEW = "code_review"
    EXPLANATION = "explanation"
    DEBUGGING = "debugging"
    BEST_PRACTICES = "best_practices"
    ARCHITECTURE = "architecture"
    LEARNING = "learning"


class PromptService:
    """ Servicio para la gestión de prompts"""

    def __init__(self, llm_Client=None, enable_guardrails: bool = True, analysis_llm_client=None):
        """
        Inicializa el servicio de prompts

        Args:   
            llm_client: Cliente LLM para clasificación de prompts 
        """
        self.templates = self._load_templates()
        self.llm_client = llm_Client
        self.analysis_llm_client = analysis_llm_client

        self.enable_guardrails = enable_guardrails
        if enable_guardrails:
            self.guardrails = PromptGuardrails()

    def _get_classification_prompt(self, user_input:str) -> str:
        """
        Crea el prompt para que el LLM clasefique la consulta del usuario

        Args:
            user_input: la consulta del usuario a clasificar

        Returns:
            Prompt optimizaco para clasificación
        """

        return f"""Eres un clasificador de consultas para DevMentor AI.

        Tu tarea es analizar la consulta del usuario y determinar a qué categoría pertenece.

        **Categorías disponibles:**

        1. **general** - Consultas generales sobre desarrollo de software
        2. **code_review** - Solicitudes de revisión, análisis o mejora de código
        3. **explanation** - Preguntas sobre conceptos, definiciones o funcionamiento
        4. **debbuging** - Problemas, errores o bugs que necesitan solución
        5. **best_practices** - Consultas sobre mejores prácticas, estándares o convenciones
        6. **architecture** - Diseño de sistemas, patrones arquitectónicos, estructuras...
        7. **learning** - Solicitudes de guías de aprendizaje, roadmaps o tutoriales

        **Consulta del usuario**
        {user_input}

        **Categoría:**"""
    
    def detect_prompt_type(self, user_input: str) -> PromptType:
        """
        Detecta automáticamente el tipo de prompt

        Args:
            user_input: Prompt del usuario

        Returns:
            Tipo de prompt detectado
        """

        if not self.llm_client:
            return PromptType.GENERAL
        
        try:
            # Cogemos el prompt de clasificación
            classification_prompt = self._get_classification_prompt(user_input)

            # Consultar al LLM
            response_generator = self.llm_client.generate_response(classification_prompt,{})

            response = ""
            for chunk in response_generator:
                if chunk:
                    response += chunk

            detected_category = response.strip().lower()

            for prompt_type in PromptType:
                if prompt_type.value == detected_category:
                    return prompt_type
            
            return PromptType.GENERAL

        except Exception as e:
            print(f"⚠️ Error eb clasificación LLM : {e}")
            return PromptType.GENERAL
    

    def _load_templates(self) -> Dict[PromptType, str]:
        """
        Carga los templates de prompts especializados.

        Cada template define el ROL y las INSTRUCCIONES para el LLM.
        NO usamos variables - el LLM entiende el contexto del mensaje completo.
        """
        return {
            PromptType.GENERAL: """
    Eres DevMentor AI, un asistente experto en desarrollo de software.

    Proporciona respuestas claras, precisas y útiles sobre desarrollo de software.
    Adapta tu nivel de detalle según el contexto de la pregunta.
    """,

            PromptType.CODE_REVIEW: """
    Eres un experto revisor de código con años de experiencia.

    Analiza el código proporcionado por el usuario y proporciona:
    1. **Análisis de calidad**: Evalúa la legibilidad, estructura y organización
    2. **Problemas potenciales**: Identifica bugs, errores lógicos o malas prácticas
    3. **Sugerencias de mejora**: Proporciona alternativas concretas y mejores soluciones
    4. **Mejores prácticas**: Recomienda patrones y estándares aplicables

    Sé específico, constructivo y proporciona ejemplos cuando sea posible.
    """,

            PromptType.EXPLANATION: """
    Eres un profesor experto en ciencias de la computación.

    Explica el concepto solicitado de forma clara y didáctica:
    1. **Definición**: ¿Qué es y para qué sirve?
    2. **Cómo funciona**: Explica el mecanismo interno de forma comprensible
    3. **Ejemplo práctico**: Muestra un caso de uso real con código
    4. **Cuándo usarlo**: Situaciones apropiadas y cuándo evitarlo

    Adapta el nivel de detalle al contexto de la pregunta.
    """,

            PromptType.DEBUGGING: """
    Eres un experto en debugging y resolución de problemas de código.

    Ayuda a resolver el problema siguiendo estos pasos:
    1. **Análisis del problema**: Identifica la causa raíz del error
    2. **Diagnóstico**: Explica por qué ocurre el error
    3. **Solución**: Proporciona el código corregido
    4. **Prevención**: Explica cómo evitar este problema en el futuro

    Sé metódico y proporciona explicaciones claras de cada paso.
    """,

            PromptType.BEST_PRACTICES: """
    Eres un arquitecto de software senior especializado en mejores prácticas.

    Proporciona recomendaciones sobre mejores prácticas:
    1. **Estándares de la industria**: Qué se considera buena práctica y por qué
    2. **Justificación**: Beneficios concretos de seguir estas prácticas
    3. **Ejemplos concretos**: Código que demuestra la práctica correcta vs incorrecta
    4. **Errores comunes**: Qué evitar y por qué

    Enfócate en prácticas probadas y ampliamente aceptadas.
    """,

            PromptType.ARCHITECTURE: """
    Eres un arquitecto de software con experiencia en diseño de sistemas escalables.

    Ayuda con el diseño arquitectónico:
    1. **Análisis de requisitos**: Identifica necesidades clave y restricciones
    2. **Propuesta arquitectónica**: Sugiere patrones y estructura general
    3. **Componentes principales**: Define módulos, servicios y sus responsabilidades
    4. **Consideraciones técnicas**: Escalabilidad, mantenibilidad, seguridad

    Proporciona diagramas conceptuales cuando sea apropiado (usando texto/ASCII).
    """,

            PromptType.LEARNING: """
    Eres un mentor de desarrollo de software especializado en guiar el aprendizaje.

    Crea una guía de aprendizaje estructurada:
    1. **Roadmap**: Pasos ordenados y progresivos para dominar el tema
    2. **Recursos**: Documentación oficial, tutoriales, cursos recomendados
    3. **Práctica**: Proyectos y ejercicios concretos para reforzar el aprendizaje
    4. **Hitos**: Cómo medir el progreso y saber cuándo avanzar

    Adapta la profundidad y complejidad al nivel de experiencia del usuario.
    """
        }
    
    def build_prompt(self, user_input: str, prompt_type:PromptType = None, skip_validation: bool = False) -> tuple:
        """
        Construye un prompt optimizado con validación de seguridad en dos capas

        Capa 1: Regex 
        Capa 2: LLM de análisis

        Args:
            user_input: El prompt del usuario
            prompt_type: El tipo de prompt (si es None lo detectamos automáticamente)

        Returns:
            El prompt optimizado listo para enviar al modelo
        """
        
        # Capa 1 (Regex)
        if self.enable_guardrails and not skip_validation:
            is_valid, error_msg = self.guardrails.validate_input(user_input)
            if not is_valid:
                print("Detectado ataque con Regex")
                return None, self.guardrails.get_safe_error_message()
        # Capa 2 (analizando con LLM)
        if self.enable_guardrails and self.analysis_llm_client and not skip_validation:
            is_attack, confidence = self.guardrails.detect_attack_with_llm(
                user_input,
                self.analysis_llm_client
            )
            if is_attack and confidence in ["ALTO","MEDIO"]:
                print("Detectado ataque con LLM")
                return None, self.guardrails.get_safe_error_message()

        if prompt_type is None:
            prompt_type = self.detect_prompt_type(user_input)

        # Obtenemos el template asociado al PromptType 
        template = self.templates.get(prompt_type, self.templates[PromptType.GENERAL])

        final_prompt = F"""{template}

{user_input}"""
        
        return final_prompt, None