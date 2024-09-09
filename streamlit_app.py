import streamlit as st
import requests

API_URL = "http://localhost:8001/ask"


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Interactive Generative AI Chatbot")

question = st.text_input("Ask a question:")

if st.button("Get Answer") and question:
    chat_history = st.session_state.chat_history[-1] if st.session_state.chat_history != [] else []
    body = {"question": question, "history": chat_history}
    response = requests.post(API_URL, json=body)

    if response.status_code == 200:
        answer = response.json().get("answer")
        st.session_state.chat_history.append([
            {"role": "user", "parts": question},
            {"role": "model", "parts": answer},
        ])
    else:
        st.write("Error: Bot is not doing well!")
else:
    st.write("Please enter a question.")


if st.session_state.chat_history:
    st.write("**Chat History**")
    for chat in st.session_state.chat_history:
        st.write(f"**{chat[0]["role"]}**: {chat[0]["parts"]}")
        st.write(f"**{chat[1]["role"]}**: {chat[1]["parts"]}")


