import streamlit as st
import requests
import re
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io

API_URL = "http://localhost:8001"

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

def send_message(user_input=None):
    if user_input is None:
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
        response = requests.post(f"{API_URL}/chat", json=payload)
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
        play_audio(tutor_response)
    except Exception as e:
        st.session_state.history.append(("System", f"Error: {e}"))
    st.session_state.input_text = ""  # Clear input box

def record_audio():
    fs = 44100  # Sample rate
    seconds = 5  # Duration of recording
    st.info("Recording for 5 seconds...")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()  # Wait until recording is finished
    st.info("Recording finished.")
    return recording, fs

def play_audio(text):
    try:
        response = requests.post(f"{API_URL}/text-to-speech", json={"text": text})
        # This is a simplified example. In a real application, you would
        # receive the audio data and play it. For now, we'll just log it.
        st.write("Audio response generated.")
    except Exception as e:
        st.error(f"Error playing audio: {e}")

# Display chat history at the top
for speaker, text in st.session_state.history:
    st.markdown(f"**{speaker}:** {text}")

# Input bar at the bottom
col1, col2 = st.columns([4, 1])
with col1:
    st.text_input("You:", key="input_text", on_change=send_message)
with col2:
    if st.button("🎤"):
        audio_data, sample_rate = record_audio()
        wav_io = io.BytesIO()
        wav.write(wav_io, sample_rate, audio_data)
        wav_io.seek(0)
        files = {'file': ('audio.wav', wav_io, 'audio/wav')}
        try:
            response = requests.post(f"{API_URL}/speech-to-text", files=files)
            transcribed_text = response.json().get("text", "")
            st.session_state.input_text = transcribed_text
            send_message(user_input=transcribed_text)
        except Exception as e:
            st.error(f"Error transcribing audio: {e}")
