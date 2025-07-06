import streamlit as st
import requests
import re

API_URL = "http://localhost:8001/chat"

st.title("Math Tutor Chatbot Task")

if "step_idx" not in st.session_state:
    st.session_state.step_idx = 0
if "last_steps" not in st.session_state:
    st.session_state.last_steps = []
if "last_question" not in st.session_state:
    st.session_state.last_question = None
if "history" not in st.session_state:
    st.session_state.history = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "asked_indices" not in st.session_state:
    st.session_state.asked_indices = []
if "last_user_inputs" not in st.session_state:
    st.session_state.last_user_inputs = []
if "last_tutor_outputs" not in st.session_state:
    st.session_state.last_tutor_outputs = []

def send_message():
    user_input = st.session_state.input_text.strip()
    if not user_input:
        return
    payload = {
        "user_input": user_input,
        "step_idx": st.session_state.step_idx,
        "last_steps": st.session_state.last_steps,
        "last_question": st.session_state.last_question,
        "asked_indices": st.session_state.asked_indices,
        "last_user_inputs": st.session_state.last_user_inputs,
        "last_tutor_outputs": st.session_state.last_tutor_outputs
    }
    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()
        st.session_state.history.append(("You", user_input))
        tutor_response = data["response"]
        # Remove <think>...</think> blocks
        tutor_response = re.sub(r"<think>.*?</think>", "", tutor_response, flags=re.DOTALL)
        st.session_state.history.append(("Tutor", tutor_response))
        st.session_state.step_idx = data["step_idx"]
        st.session_state.last_steps = data["last_steps"]
        st.session_state.last_question = data["last_question"]
        st.session_state.asked_indices = data.get("asked_indices", [])
        # Update last 3 user inputs and tutor outputs
        st.session_state.last_user_inputs = (st.session_state.last_user_inputs + [user_input])[-3:]
        st.session_state.last_tutor_outputs = (st.session_state.last_tutor_outputs + [tutor_response])[-3:]
    except Exception as e:
        st.session_state.history.append(("System", f"Error: {e}"))
    st.session_state.input_text = ""  # Clear input box

# Display chat history at the top
for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")

# Input bar at the bottom
input_placeholder = st.empty()
input_placeholder.text_input("You:", key="input_text", on_change=send_message) 