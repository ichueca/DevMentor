import streamlit as st
from utils import GeminiClient, OpenAIClient

def create_sidebar():
    """ Crea y configura el sidebar de la aplicación """

    with st.sidebar:
        st.title("🚀 DevMentor AI")
        st.markdown("*Tu asistente de desarrollo*")
        st.divider()

        st.markdown("### ⚙️ Configuración")

        # Seleccionar el modelo
        model_provider = st.selectbox(
            "Proveedor de IA:",
            ["Gemini","OpenAI"],
            help="Seleccione el proveedor de la IA a utilizar"
        )
        _display_connection_status(model_provider)

        st.divider

        st.markdown("### 💬 Controles del Chat")

        if st.button("🗑️ Limpiar Chat", use_container_width=True):
            from components import ChatInterface
            chat = ChatInterface()
            chat.clear_chat()


def _display_connection_status(provider:str):
    """
    Muestra el estado de Conexión con el proveedor de IA

    Args:
        provider: El proveedor seleccionado ('Gemini' u 'OpenAI')
    """
    try:
        if provider == "Gemini":
            client = GeminiClient()
            if client.api_key:
                st.success("✅ Gemini conectado")
                st.session_state.llm_client = client
            else:
                st.error("❌ Gemini no configurado")
        elif provider == "OpenAI":
            client = OpenAIClient()
            if client.api_key:
                st.success("✅ OpenAI conectado")
                st.session_state.llm_client = client
            else:
                st.error("❌ OpenAI no configurado")
    except ValueError as e:
        st.error(f"❌ Error: {e}")
        st.info("💡Configura tu clave de API en el archivo .env")