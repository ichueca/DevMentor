import streamlit as st
from utils import GeminiClient, OpenAIClient, PromptType, PromptService
from dotenv import load_dotenv


load_dotenv()

class ChatInterface:
    """ Gestiona la interfaz del chat """

    def __init__(self):
        self.initialize_session_state()

        llm_client = st.session_state.get("llm_client")
        self.prompt_service = PromptService(llm_Client= llm_client)
    
    def initialize_session_state(self):
        """ Inicializar el estado de sesión """
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'llm_client' not in st.session_state:
            try:
                st.session_state.llm_client = GeminiClient()
            except ValueError:
                st.session_state.llm_client = None
    
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

                            detected_type = self.prompt_service.detect_prompt_type(prompt)
                            optimized_prompt = self.prompt_service.build_prompt(user_input=prompt, prompt_type=detected_type)

                            response = st.session_state.llm_client.generate_response(
                                #context,
                                optimized_prompt,
                                st.session_state.messages,
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