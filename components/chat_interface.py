import streamlit as st
from utils import GeminiClient, OpenAIClient, PromptType, PromptService
from dotenv import load_dotenv
from utils import SummaryStrategy, SlidingWindowStrategy, SmartSelectionStrategy
from utils.api_client import OllamaClient


load_dotenv()

class ChatInterface:
    """ Gestiona la interfaz del chat """

    def __init__(self, analysis_llm_client=None):
        self.initialize_session_state()
        self.analysis_llm_client = analysis_llm_client
        llm_client = st.session_state.get("llm_client")
        self.prompt_service = PromptService(llm_Client= llm_client, enable_guardrails=True, analysis_llm_client=analysis_llm_client)
    
    def initialize_session_state(self):
        """ Inicializar el estado de sesión """
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'llm_client' not in st.session_state:
            try:
                st.session_state.llm_client = GeminiClient()
            except ValueError:
                st.session_state.llm_client = None
        
        if 'prompt_mode' not in st.session_state:
            st.session_state.prompt_mode = 'auto'
        
        if 'selected_prompt_type' not in st.session_state:
            st.session_state.selected_prompt_type = 'general'
        
        if 'show_prompt_info' not in st.session_state:
            st.session_state.show_prompt_info = True
        
        if 'context_strategy' not in st.session_state:
            st.session_state.context_strategy = "Ninguna"
        
        if 'context_stats' not in st.session_state:
            st.context_stats = None
        
    
    def handle_user_input(self):
        """ Maneja la entrada del usuario y genera una respuesta """
        if prompt := st.chat_input("Escribe tu consulta sobre desarrollo..."):
            # Mostramos el mensaje del usuario
            #st.markdown(prompt)
            with st.chat_message("user"):
                st.markdown(prompt)

            # Añadir al historial
            self.add_message("user",prompt)

            temperature = st.session_state.temperature
            max_tokens = st.session_state.max_tokens

            # Generar respuesta
            if st.session_state.llm_client:
                    with st.chat_message("assistant"):
                        st.caption(f"Usando: temperature={temperature} - max_tokens={max_tokens}")
                        with st.spinner("Pensando..."):
                            # Crear el contexto del prompt
                            #context = self._create_context(prompt)

                            if st.session_state.prompt_mode == 'auto':
                                detected_type = self.prompt_service.detect_prompt_type(prompt)
                            else:
                                detected_type = PromptType(st.session_state.selected_prompt_type)

                            print(f"Tipo de prompt usado : {detected_type}")

                            optimized_prompt,error = self.prompt_service.build_prompt(user_input=prompt, prompt_type=detected_type)

                            if error:
                                st.error(f"❌ {error}")
                                self.add_message("assistant",error)
                                return

                            """
                            response = st.session_state.llm_client.generate_response(
                                #context,
                                optimized_prompt,
                                st.session_state.messages,
                                temperature=temperature,
                                max_tokens=max_tokens,
                            )
                            """
                            strategy_name = st.session_state.get("context_strategy","Ninguna")
                            optimized_messages = self._optimize_messages(
                                messages= st.session_state.messages,
                                strategy_name= strategy_name,
                                new_query=prompt
                            )

                            response = st.session_state.llm_client.generate_response(
                                optimized_prompt,
                                optimized_messages,
                                temperature=temperature,
                                max_tokens=max_tokens,
                            )


                            #st.write_stream(response)
                            full_response = ""
                            response_widget = st.empty()
                            for chunk in response:
                                if chunk:
                                    full_response += chunk
                                    response_widget.markdown(full_response)
                            self.add_message("assistant", full_response)
            else:
                with st.chat_message("assistant"):
                    error_msg="❌ No se pudo conectar con el servidor de IA. Verifica la configuración"
                    st.error(error_msg)
                    self.add_message("assistant", error_msg)
    
    def get_prompt_info(self, prompt_type: PromptType) -> dict:
        """ Retorna información sobre el tipo de prompt empleado"""
        info = {
            PromptType.GENERAL: {
                'name':'General',
                'description':'Consultas generales sobre desarrollo',
                'icon':'💬'
            },
            PromptType.CODE_REVIEW: {
                'name':'Revisión de Código',
                'description':'Análisis y mejora del código',
                'icon':'🔍'
            },
            PromptType.EXPLANATION: {
                'name':'Explicación',
                'description':'Aclaraciones sobre conceptos técnicos',
                'icon':'📓'
            },
            PromptType.DEBUGGING: {
                'name':'Depuración',
                'description':'Resolución de problemas y errores',
                'icon':'🐛'
            },
            PromptType.BEST_PRACTICES:{
                'name':'Mejores Prácticas',
                'description':'Recomendaciones y estándares',
                'icon':'⭐'
            },
            PromptType.ARCHITECTURE:{
                'name':'Arquitectura',
                'description':'Diseño de sistemas y patrones',
                'icon':'🏗️'
            },
            PromptType.LEARNING:{
                'name':'Aprendizaje',
                'description':'Guías y roadmaps de aprendizaje',
                'icon':'🧑‍🎓'
            }
            
        }
        return info.get(prompt_type, PromptType.GENERAL)


    def display_prompt_controls(self):
        """ Muestra controles del sistema de prompts en el sidebar """
        st.sidebar.markdown("### 🎯 Sistema de Prompts")

        st.session_state.prompt_mode = st.sidebar.radio(
            "Modo de Detección",
            ['auto','manual'],
            format_func=lambda x: {
                'auto': '🤖 Automático',
                'manual': '🙍‍♂️ Manual'
            }[x],
            help="Automático: detecta el tipo de consulta\nManual: selecciona manualmente"
        )

        if st.session_state.prompt_mode == 'manual':
            prompt_types = {}
            for prompt_type in PromptType:
                info = self.get_prompt_info(prompt_type)
                prompt_types[prompt_type.value] = f"{info['icon']} {info['name']}"
            
            st.session_state.selected_prompt_type = st.sidebar.selectbox(
                "Tipo de Consulta",
                list(prompt_types.keys()),
                format_func=lambda x: prompt_types[x],
                help="Selecciona el tipo más apropiado para tu consulta"
            )

    def _create_context(self, user_prompt:str) -> str:
        """
        Crea el contexto para el prompt

        Args:
            user_prompt: La pregunta del usuario

        Returns:
            prompt completo con el contexto
        """

        context= f"""
        Eres DevMentor AI, un asistente especializado en desarrollo de software-
        Tu objetivo es ayudar a desarrolladores con sus preguntas técnicas proporcionando:

        1. Explicaciones claras y precisas
        2. Ejemplos de código cuando sea apropiado
        3. Mejores prácticas de desarrollo
        4. Soluciones paso a paso

        Pregunta del usuario: {user_prompt}

        Responde de manera útil y educativa
"""
        return context
    
    def add_message(self, role:str, msg:str):
        """ Añade el mensaje al historial """
        st.session_state.messages.append({
            "role":role,
            "message":msg
        })


    def display_messages(self):
        """ Muestra todos los mensajes del chat """
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["message"])

    
    def display_chat_stats(self):
        """ Muestra estadísticas en la barra de estado """
        st.sidebar.markdown("### 📊 Estadísticas del chat")
        st.sidebar.metric("Mensajes Totales", len(st.session_state.messages))

        if st.session_state.messages:
            user_messages = len([m for m in st.session_state.messages if m['role'] == "user"])
            st.sidebar.metric("Preguntas Realizadas", user_messages)

    def _optimize_messages(self, messages, strategy_name, new_query):
        """ Optimiza los mensajes en base a la estrategia """
        if strategy_name == "Ninguna":
            return messages
        
        elif strategy_name == "Ventana Deslizante":
            strategy = SlidingWindowStrategy(max_messages=5)
        elif strategy_name == "Resumen Automático":
            strategy = SummaryStrategy(llm_client=OllamaClient(),keep_recent=3,summarize_thresold=7)
        else:
            strategy = SmartSelectionStrategy(OllamaClient(),max_selected=3)

        optimized = strategy.optimize(messages, new_query)
        st.session_state.context_stats = strategy.get_stats()
        return optimized

    @staticmethod
    def export_chat():
        """

        Exporta el historial del chat como texto
        
        Returns:
            El historial ddel chat formateado

        """

        if not st.session_state.messages:
            return "No hay mensajes para exportar"
        
        export_text = "# Historial de Chat - DdevMentor AI\n\n"

        for i, message in enumerate(st.session_state.messages):
            role = "👤 Usuario" if message["role"] == "user" else "🤖 DevMentor"
            export_text += f"## Mensaje {i} - {role}\n\n"
            export_text += f"{message['message']}\n\n"
            export_text += f"---\n\n"
        
        return export_text
    
    @staticmethod
    def clear_chat():
        st.session_state.messages = []
        st.rerun()