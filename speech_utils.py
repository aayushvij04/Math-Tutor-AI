import speech_recognition as sr
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
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
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
        
    def speech_to_text(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Convert speech to text using microphone input.
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for a single phrase
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            with sr.Microphone() as source:
                print("Listening... Speak now!")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
                
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                print(f"Transcribed: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
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
    
    def listen_continuously(self, callback: Callable[[str], None], stop_phrase: str = "stop listening") -> None:
        """
        Continuously listen for speech and call the callback function.
        
        Args:
            callback: Function to call with transcribed text
            stop_phrase: Phrase to say to stop listening
        """
        self.is_listening = True
        
        def listen_loop():
            while self.is_listening:
                text = self.speech_to_text(timeout=1, phrase_time_limit=5)
                if text:
                    text_lower = text.lower().strip()
                    if stop_phrase.lower() in text_lower:
                        self.is_listening = False
                        break
                    else:
                        callback(text)
                time.sleep(0.1)
        
        self.audio_thread = threading.Thread(target=listen_loop)
        self.audio_thread.start()
    
    def stop_listening(self) -> None:
        """Stop continuous listening."""
        self.is_listening = False
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join(timeout=1)

# Global speech handler instance
speech_handler = SpeechHandler()

def get_speech_handler() -> SpeechHandler:
    """Get the global speech handler instance."""
    return speech_handler 