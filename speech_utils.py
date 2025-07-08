import whisper
import pyttsx3
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import tempfile
import os
import threading
import time
from typing import Optional, Callable

class SpeechHandler:
    def __init__(self, model_size="base"):
        # Initialize speech recognition with Whisper
        self.model = whisper.load_model(model_size)
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Get available voices and set a good one
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer female voice for tutoring (usually index 1)
            voice_index = 1 if len(voices) > 1 else 0
            self.tts_engine.setProperty('voice', voices[voice_index].id)
        
        self.is_listening = False
        self.is_speaking = False
        self.audio_thread = None
        
    def speech_to_text(self, audio_data: np.ndarray, sample_rate: int) -> Optional[str]:
        """
        Convert speech to text using Whisper.
        
        Args:
            audio_data: NumPy array containing audio data
            sample_rate: Sample rate of the audio data
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            # Normalize audio data to be in the range [-1, 1]
            audio_data = audio_data.astype(np.float32) / np.iinfo(audio_data.dtype).max
            
            print("Processing speech with Whisper...")
            result = self.model.transcribe(audio_data, fp16=False)
            text = result['text']
            print(f"Transcribed: {text}")
            return text
            
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
    
    def text_to_speech(self, text: str, block: bool = True) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text: Text to convert to speech
            block: Whether to block until speech is complete
        """
        if not text.strip():
            return
            
        try:
            if block:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            else:
                # Non-blocking speech in a separate thread
                def speak():
                    self.is_speaking = True
                    self.tts_engine.say(text)
                    self.tts_engine.runAndWait()
                    self.is_speaking = False
                
                self.audio_thread = threading.Thread(target=speak)
                self.audio_thread.start()
                
        except Exception as e:
            print(f"Error in text-to-speech: {e}")
    
    def stop_speaking(self) -> None:
        """Stop any ongoing speech."""
        if self.is_speaking:
            self.tts_engine.stop()
            self.is_speaking = False
            if self.audio_thread and self.audio_thread.is_alive():
                self.audio_thread.join(timeout=1)

# Global speech handler instance
speech_handler = SpeechHandler()

def get_speech_handler() -> SpeechHandler:
    """Get the global speech handler instance."""
    return speech_handler
