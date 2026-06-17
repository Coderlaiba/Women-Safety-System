import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import speech_recognition as sr
import io
import time
import threading

def run_async_voice_processor(system_coordinator):
    sample_rate = 16000
    duration = 3.5  # 3.5 Seconds snapshot scanning window
    SAFETY_KEYWORDS = ["help", "stop", "bachao", "emergency", "police", "save me"]
    recognizer = sr.Recognizer()

    while True:
        try:
            # Non-blocking async chunk tracking buffer allocations
            recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait() # Stream capture logic isolate ho chuka hai, main app safe rahegi

            byte_io = io.BytesIO()
            wav.write(byte_io, sample_rate, recording)
            byte_io.seek(0)

            with sr.AudioFile(byte_io) as source:
                audio_data = recognizer.record(source)

            try:
                spoken_text = recognizer.recognize_google(audio_data, language="en-IN").lower()
                print(f"🗣️ Detected Speech: '{spoken_text}'")

                matched_trigger = [word for word in SAFETY_KEYWORDS if word in spoken_text]
                if matched_trigger:
                    print(f"🚨 ALERT TRIGGER MATCHED! Detected Keyword: '{matched_trigger[0]}'")
                    
                    # Direct parallel background dispatch pipeline execute karein
                    trigger_worker = threading.Thread(
                        target=system_coordinator.route_incident_trigger,
                        args=("BACKGROUND_VOICE_MIC",)
                    )
                    trigger_worker.daemon = True
                    trigger_worker.start()
                    
                    time.sleep(6) # Cooldown window loops bypass logic
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass

        except Exception as hardware_error:
            # Silent fallback framework agar active drivers process change ho
            time.sleep(3)

def deploy_audio_pipeline_safely(system_coordinator, fetch_contacts_callback):
    """
    Main gateway framework function jo user app interface ko bina crash kiye 
    background thread pipeline fork kar deti hai.
    """
    print("🎤 [NATIVE AUDIO ENGINE] Starting async sounddevice interface channel...")
    background_mic_thread = threading.Thread(
        target=run_async_voice_processor, 
        args=(system_coordinator,)
    )
    background_mic_thread.daemon = True
    background_mic_thread.start()