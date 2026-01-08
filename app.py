from components import ChatInterface, create_sidebar

import streamlit as st

from utils import OllamaClient

st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide",
)

chat = ChatInterface(analysis_llm_client=OllamaClient())

create_sidebar()

st.title("DevMentor AI")

chat.display_messages()

chat.handle_user_input()

chat.display_chat_stats()

chat.display_prompt_controls()
