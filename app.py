from components import ChatInterface, create_sidebar

import streamlit as st

st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide",
)

create_sidebar()

st.title("DevMentor AI")

chat = ChatInterface()

chat.display_messages()

chat.handle_user_input()

chat.display_chat_stats()
