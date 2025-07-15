import speech_recognition as sr
import pyttsx3

class VoiceHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.speech_rate = 150
        self.speech_volume = 0.9
        self.speech_voice = None
        self._init_voice_settings()

    def _init_voice_settings(self):
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if "female" in voice.name.lower() or "zira" in voice.name.lower():
                        self.speech_voice = voice.id
                        break
                else:
                    self.speech_voice = voices[0].id
            temp_engine.stop()
        except Exception as e:
            print(f"Voice initialization error: {e}")

    def speak_text(self, text):
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', self.speech_rate)
            engine.setProperty('volume', self.speech_volume)
            if self.speech_voice:
                engine.setProperty('voice', self.speech_voice)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
            del engine
        except Exception as e:
            print(f"Speech error: {e}")

    def listen_for_speech(self, timeout=5, phrase_time_limit=10):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening... Speak now!")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = self.recognizer.recognize_google(audio)
            print(f"Recognized: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

    def test_voice(self):
        test_text = "Hello! I'm your math tutor. How can I help you today?"
        return self.speak_text(test_text)

    def get_available_voices(self):
        try:
            temp_engine = pyttsx3.init()
            voices = temp_engine.getProperty('voices')
            temp_engine.stop()
            return [voice.name for voice in voices]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []

    def set_voice_speed(self, speed):
        self.speech_rate = speed

    def set_voice_volume(self, volume):
        self.speech_volume = volume

voice_handler = VoiceHandler() 