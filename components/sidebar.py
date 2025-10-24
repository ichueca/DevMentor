from datetime import datetime
import streamlit as st
from utils import GeminiClient, OpenAIClient
from components import ChatInterface
from config import DEFAULT_SETTINGS

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
            ChatInterface.clear_chat()

        # Exportar chat a texto
        if st.session_state.get('messages'):
            st.markdown("### 📋 Exportar Chat a Markdown")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            filename = st.text_input(
                "Nombre del archivo:",
                value= f"devmentor_chat_{timestamp}",
                help="Sin extensión",
            )

            if st.button(
                "💾 Descargar Chat",
                use_container_width=True,
                ):
                export_text = ChatInterface.export_chat()

                if not filename.endswith(".md"):
                    filename = f"{filename}.md"
                
                st.download_button(
                    "💾 Confirmar Descarga",
                    data=export_text,
                    file_name=filename,
                    mime="text/markdown",
                    use_container_width=True
                )
        
        st.divider()
        with st.expander("🔧 Configuración Avanzada"):
            temperature = st.slider(
                "Creatividad (Temperatura)",
                min_value = 0.0,
                max_value = 2.0,
                value=DEFAULT_SETTINGS["temperature"],
                help="Cuanto más alto, más creativo"
            )

            max_tokens = st.slider(
                "Máximo de Tokens",
                min_value = 100,
                max_value = 20000,
                value = DEFAULT_SETTINGS["max_tokens"],
                step = 100,
                help = "Longitud de la respuesta"
            )

            #Guardamos los parámetros en session_state (accesible desde ChatInterface también)
            st.session_state.temperature = temperature
            st.session_state.max_tokens = max_tokens






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