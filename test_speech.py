import requests
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import io

API_URL = "http://localhost:8001"

def record_audio(duration=5, fs=44100):
    """Record audio from the microphone."""
    print("Recording for 5 seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
    sd.wait()
    print("Recording finished.")
    return recording, fs

def test_speech_to_text(audio_data, sample_rate):
    """Test the speech-to-text endpoint."""
    wav_io = io.BytesIO()
    wav.write(wav_io, sample_rate, audio_data)
    wav_io.seek(0)
    files = {'file': ('audio.wav', wav_io, 'audio/wav')}
    
    try:
        response = requests.post(f"{API_URL}/speech-to-text", files=files)
        response.raise_for_status()
        transcribed_text = response.json().get("text")
        print(f"Transcribed text: {transcribed_text}")
        return transcribed_text
    except requests.exceptions.RequestException as e:
        print(f"Error in speech-to-text test: {e}")
        return None

def test_text_to_speech(text):
    """Test the text-to-speech endpoint."""
    if not text:
        return
        
    payload = {"text": text}
    
    try:
        response = requests.post(f"{API_URL}/text-to-speech", json=payload)
        response.raise_for_status()
        
        # In a real application, you would handle the audio stream.
        # For this test, we just confirm the request was successful.
        if response.status_code == 200:
            print("Text-to-speech request successful.")
        else:
            print(f"Text-to-speech request failed with status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error in text-to-speech test: {e}")

if __name__ == "__main__":
    # Record audio
    audio_data, sample_rate = record_audio()
    
    # Test speech-to-text
    transcribed_text = test_speech_to_text(audio_data, sample_rate)
    
    # Test text-to-speech
    if transcribed_text:
        test_text_to_speech(transcribed_text)
