import streamlit as st
from utils import GeminiClient, OpenAIClient
from dotenv import load_dotenv

load_dotenv()

class ChatInterface:
    """ Gestiona la interfaz del chat """

    def __init__(self):
        self.initialize_session_state()
    
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
            st.markdown(prompt)

            # Añadir al historial
            self.add_message("user",prompt)

            # Generar respuesta
            if st.session_state.llm_client:

                    
                    with st.chat_message("assistant"):
                        with st.spinner("Pensando..."):
                            # Crear el contexto del prompt
                            context = self._create_context(prompt)
                            response = st.session_state.llm_client.generate_response(context)
                            st.write_stream(response)
                            self.add_message("assistant", response)
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
        for msg in st.session_state.messages:
            print(msg)
        print("-----------------------------")
        