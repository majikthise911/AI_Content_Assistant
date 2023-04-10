import openai
import toml
import os
import streamlit as st
# from dotenv import load_dotenv # needed to load .env file on local machine. Comment out when running on streamlit cloud

def show_messages(text):
    messages_str = [
        f"{_['role']}: {_['content']}" for _ in st.session_state["messages"][1:]
    ]
    text.text_area("Messages", value=str("\n".join(messages_str)), height=400)

# load_dotenv() # needed to load .env file on local machine. Comment out when running on streamlit cloud

openai.api_key = os.environ.get("OPENAI_API_KEY")
BASE_PROMPT = [{"role": "system", "content": "You are a helpful assistant."}]

if "messages" not in st.session_state:
    st.session_state["messages"] = BASE_PROMPT

st.header("STREAMLIT GPT-3 CHATBOT")

text = st.empty()
show_messages(text)

prompt = st.text_input("Prompt", value="Enter your message here...")

if st.button("Send"):
    with st.spinner("Generating response..."):
        st.session_state["messages"] += [{"role": "user", "content": prompt}]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=st.session_state["messages"]
        )
        message_response = response["choices"][0]["message"]["content"]
        st.session_state["messages"] += [
            {"role": "system", "content": message_response}
        ]
        show_messages(text)

if st.button("Clear"):
    st.session_state["messages"] = BASE_PROMPT
    show_messages(text)