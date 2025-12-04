from components import ChatInterface, create_sidebar

import streamlit as st

from utils import OllamaClient

st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide",
)

create_sidebar()

st.title("DevMentor AI")

chat = ChatInterface(analysis_llm_client=OllamaClient())

chat.display_messages()

chat.handle_user_input()

chat.display_chat_stats()

chat.display_prompt_controls()
