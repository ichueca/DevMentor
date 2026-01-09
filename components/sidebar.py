from datetime import datetime
import streamlit as st
from utils import GeminiClient, OpenAIClient, OllamaClient
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
            ["Ollama","Gemini","OpenAI"],
            help="Seleccione el proveedor de la IA a utilizar"
        )
        _display_connection_status(model_provider)

        st.divider
        conversations = st.session_state.storage.list_conversations()

        if conversations:
            conversation_options = [
                f"📄 {conv['name']} ({conv['message_count']})" for conv in conversations
            ]
            conversation_options.insert(0, "-- Seleccione --")
            default_index = 0
            if st.session_state.current_conversation_id:
                for i, conv in enumerate(conversations):
                    if conv['id'] == st.session_state.current_conversation_id:
                        default_index = i + 1
                        break

            selected_option = st.selectbox(
                "📁 Conversaciones guardadas",
                conversation_options,
                index=default_index,
                help="Seleccione una conversación para cargarla"
            )
            selected_index = conversation_options.index(selected_option)
            if selected_index != 0:
                selected_conv = conversations[selected_index - 1]
                # Si no es la conversación activa
                if st.session_state.current_conversation_id != selected_conv['id']:
                    # La cargamos
                    chat_interface = ChatInterface()
                    chat_interface.load_conversation(selected_conv['id'])
                    st.rerun()

                st.markdown("**Acciones:**")
                col1,col2 = st.columns(2)

                with col1:
                    if st.button("✏️ Renombrar", use_container_width=True):
                        st.session_state.rename_mode = selected_conv['id']
                with col2:
                    if st.button("🗑️ Eliminar", use_container_width=True):
                        if st.session_state.current_conversation_id == selected_conv['id']:
                            st.session_state.messages = []
                            st.session_state.current_conversation_id = None
                            st.session_state.current_conversation_name = "Nueva Conversación"
                        
                        st.session_state.storage.delete_conversation(selected_conv['id'])
                        st.success("✅ Conversación Eliminada!")
                        st.rerun()
                
                if st.button("➕ Nueva Conversación", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.current_conversation_id = None
                    st.session_state.current_conversation_name = "Nueva Conversación"
                    st.rerun()
                
                if 'rename_mode' in st.session_state and st.session_state.rename_mode:
                    conv_id = st.session_state.rename_mode
                    conv = st.session_state.storage.load_conversation(conv_id)
                    if conv:
                        st.markdown("**Renombrar Conversación**")
                        new_name = st.text_input(
                            "Nuevo Nombre:",
                            value=conv['name'],
                            key=f"rename_input_{conv_id}"
                        )

                        col1,col2 = st.columns(2)
                        with col1:
                            if st.button("✅ Guardar", use_container_width=True):
                                conv['name'] = new_name
                                st.session_state.storage.save_conversation(
                                    conversation_id = conv_id,
                                    name = new_name,
                                    messages = conv['messages']
                                )
                                st.session_state.rename_mode = None
                                st.success(f"✅ Conversación renombrada a {new_name}")
                                st.rerun()
                        
                        with col2:
                            if st.button("❌ Cancelar", use_container_width=True):
                                st.session_state.rename_mode = None
                                st.rerun()

        st.divider()

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

        st.divider()
        st.sidebar.markdown("### ⚙️ Optimización de Contexto")
        context_strategy = st.sidebar.selectbox(
            "Estrategia de Optimización",
            ["Ninguna","Ventana Deslizante", "Resumen Automático", "Selección Inteligente"],
            help="Seleccione el método de optimización del historial" 
        )
        st.session_state.context_strategy = context_strategy

        if 'context_stats' in st.session_state:
            st.sidebar.markdown("### 📶 Estadísticas de Optimización")
            stats = st.session_state.context_stats

            strategy_name = st.session_state.get("context_strategy","Ninguna")

            print(strategy_name)
            print(stats)

            if strategy_name == "Ventana Deslizante":
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    st.metric(
                        "Recientes Mantenidos",
                        stats.get('max_messages',0)
                    )
                with col2:
                    st.metric(
                        "Optimizaciones",
                        stats.get('optimization_counts',0)
                    )
                st.metric(
                    "Promedio Mantenido",
                    f"{stats.get('average_messages_kept',0):.1f}"
                )
            elif strategy_name == "Resumen Automático":
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    st.metric(
                        "Recientes Mantenidos",
                        stats.get('keep_recent',0)
                    )
                with col2:
                    st.metric(
                        "Umbral Resumen",
                        stats.get('summarize_threshold',0)
                    )
                st.metric(
                    "Optimizaciones",
                    f"{stats.get('optimizations',0)}"
                )
            elif strategy_name == "Selección Inteligente":
                col1, col2 = st.sidebar.columns(2)
                with col1:
                    st.metric(
                        "Máximo Seleccionado",
                        stats.get('max_selected',0)
                    )
                with col2:
                    st.metric(
                        "Optimizaciones",
                        f"{stats.get('optimizations',0)}"
                    )
                st.success("✅ Mensajes selecionados con éxito")
        st.divider()



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
        elif provider == "Ollama":
            client = OllamaClient()
            if client.api_key:
                st.success("✅ Ollama conectado")
                st.session_state.llm_client = client
            else:
                st.error("❌ OpenAI no configurado")
    except ValueError as e:
        st.error(f"❌ Error: {e}")
        st.info("💡Configura tu clave de API en el archivo .env")