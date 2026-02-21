import streamlit as st
from chatbot import ConversationManager

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Chatbot")
st.caption("Built with Groq + Streamlit")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = ConversationManager()

chatbot = st.session_state.chatbot

st.sidebar.title("⚙ Settings")

persona = st.sidebar.selectbox(
    "Choose Persona",
    ["helpful", "teacher", "sassy"]
)

if st.sidebar.button("Apply Persona"):
    chatbot.set_persona(persona)
    st.sidebar.success(f"Persona set to {persona}")

if st.sidebar.button("Clear Chat"):
    chatbot.clear_history()
    st.rerun()

for message in chatbot.conversation_history:
    if message["role"] == "system":
        continue

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = chatbot.chat_completion(prompt)
            st.markdown(reply)

    st.rerun()