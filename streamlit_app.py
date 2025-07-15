import streamlit as st
import requests
import re
from voice_utils import voice_handler

API_URL = "http://localhost:8001/chat"

st.title("Math Tutor Chatbot with Voice Features")

# Initialize session state
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
if "is_listening" not in st.session_state:
    st.session_state.is_listening = False
if "voice_enabled" not in st.session_state:
    st.session_state.voice_enabled = True

# --- Synchronous voice input ---
def listen_for_speech_sync():
    st.info("Listening... Speak now!")
    text = voice_handler.listen_for_speech()
    if text:
        st.session_state.input_text = text
        st.success(f"Recognized: {text}")
        send_message()
    else:
        st.warning("Could not understand audio. Please try again.")

# --- Message sending logic ---
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
        tutor_response = re.sub(r"<think>.*?</think>", "", tutor_response, flags=re.DOTALL)
        st.session_state.history.append(("Tutor", tutor_response))
        st.session_state.step_idx = data["step_idx"]
        st.session_state.last_steps = data["last_steps"]
        st.session_state.last_question = data["last_question"]
        st.session_state.asked_indices = data.get("asked_indices", [])
        st.session_state.last_user_inputs = (st.session_state.last_user_inputs + [user_input])[-3:]
        st.session_state.last_tutor_outputs = (st.session_state.last_tutor_outputs + [tutor_response])[-3:]
        if st.session_state.voice_enabled:
            voice_handler.speak_text(tutor_response)
    except Exception as e:
        error_msg = f"Error: {e}"
        st.session_state.history.append(("System", error_msg))
        if st.session_state.voice_enabled:
            voice_handler.speak_text(error_msg)
    st.session_state.input_text = ""  # Clear input box

# --- UI Layout ---
st.subheader("🎤 Voice Controls")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎤 Start Voice Input", type="primary"):
        listen_for_speech_sync()

with col2:
    if st.button("🔇 Toggle Voice Output"):
        st.session_state.voice_enabled = not st.session_state.voice_enabled
        status = "Enabled" if st.session_state.voice_enabled else "Disabled"
        st.success(f"Voice output {status}")

with col3:
    if st.button("🗣️ Test Voice"):
        voice_handler.test_voice()

with st.expander("⚙️ Voice Settings"):
    col1, col2 = st.columns(2)
    with col1:
        speed = st.slider("Speech Speed", 50, 300, 150, help="Words per minute")
        if st.button("Apply Speed"):
            voice_handler.set_voice_speed(speed)
            st.success(f"Speed set to {speed} WPM")
    with col2:
        volume = st.slider("Volume", 0.0, 1.0, 0.9, 0.1, help="Volume level")
        if st.button("Apply Volume"):
            voice_handler.set_voice_volume(volume)
            st.success(f"Volume set to {volume}")

st.markdown("---")
if st.session_state.voice_enabled:
    st.success("🔊 Voice output is enabled")
else:
    st.warning("🔇 Voice output is disabled")

st.subheader("💬 Chat History")
for speaker, text in st.session_state.history:
    if speaker == "You":
        st.markdown(f"**👤 {speaker}:** {text}")
    elif speaker == "Tutor":
        st.markdown(f"**🤖 {speaker}:** {text}")
    else:
        st.markdown(f"**⚠️ {speaker}:** {text}")

st.markdown("---")
st.subheader("📝 Input")
input_placeholder = st.empty()
input_placeholder.text_input("Type your message:", key="input_text", on_change=send_message)

with st.expander("ℹ️ How to use voice features"):
    st.markdown("""
    ### Voice Input:
    1. Click the **🎤 Start Voice Input** button
    2. Speak your question clearly
    3. Wait for the text to appear in the input box
    4. The message will be sent automatically
    
    ### Voice Output:
    - The tutor's responses will be spoken aloud when enabled
    - Toggle voice output on/off with the button
    - Test voice output with the test button
    
    ### Tips:
    - Speak clearly and at a normal pace
    - Make sure your microphone is working
    - You can use both voice and text input interchangeably
    - Adjust speech speed and volume in the settings
    """) 