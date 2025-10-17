from components import ChatInterface
import streamlit as st

st.set_page_config(
    page_title="DevMentor AI",
    page_icon="🤖",
    layout="wide",
)

st.title("DevMentor AI")

chat = ChatInterface()

chat.handle_user_input()
