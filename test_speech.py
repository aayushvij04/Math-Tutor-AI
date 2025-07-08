#!/usr/bin/env python3
"""
Simple test script for speech-to-text and text-to-speech functionality.
Run this to test if the speech features work on your system.
"""

import sys
import time

def test_speech_features():
    print("🎤 Testing Speech Features...")
    print("=" * 50)
    
    try:
        from speech_utils import get_speech_handler
        speech_handler = get_speech_handler()
        print("✅ Speech handler initialized successfully")
        
        # Test text-to-speech
        print("\n🔊 Testing Text-to-Speech...")
        test_text = "Hello! This is a test of the text to speech functionality."
        print(f"Speaking: '{test_text}'")
        speech_handler.text_to_speech(test_text)
        print("✅ Text-to-speech test completed")
        
        # Test speech-to-text
        print("\n🎤 Testing Speech-to-Text...")
        print("Please speak something when prompted (you have 5 seconds)...")
        time.sleep(2)
        
        text = speech_handler.speech_to_text(timeout=5, phrase_time_limit=5)
        if text:
            print(f"✅ Speech recognized: '{text}'")
        else:
            print("⚠️ No speech detected or recognition failed")
        
        print("\n🎉 Speech feature test completed!")
        print("\nTo use in the main app:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Run the Streamlit app: streamlit run streamlit_app.py")
        print("3. Use the speech controls in the sidebar")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install the required dependencies:")
        print("pip install SpeechRecognition pyttsx3 sounddevice scipy")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Please check your microphone and audio settings")

if __name__ == "__main__":
    test_speech_features() 