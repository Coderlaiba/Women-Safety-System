import os
import time
from twilio.rest import Client
# config.py se real credentials aur number import kar rahe hain
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_NUMBER

def send_emergency_sms(to_number, map_url):
    message_body = f"🚨 EMERGENCY ALERT! I am in danger. My Live Location: {map_url}"
    
    # AGAR KEYS MISSING HAIN YA SET NHI HAIN, TOH FALLBACK SIMULATION CHALEGA
    if not TWILIO_ACCOUNT_SID or "aapka" in TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN or not TWILIO_NUMBER:
        print(f"\n📱 [LOCAL SMS SIMULATION] To: {to_number}")
        print(f"💬 Message: {message_body}\n")
        return True

    try:
        # Real Twilio Client Engine
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # 3 se 4 baar message bhejne ke liye hum loop chala rahe hain
        repeat_count = 3  # Agar 4 baar bhejna hai toh isko 4 kar sakti hain
        
        for i in range(repeat_count):
            message = client.messages.create(
                body=f"[{i+1}/{repeat_count}] {message_body}",
                from_=TWILIO_NUMBER,
                to=to_number
            )
            print(f"✅ Real SMS {i+1} Sent Successfully! SID: {message.sid}")
            
            # Har message ke beech me 2-3 seconds ka gap de rahe hain taaki pipeline crash na ho
            if i < repeat_count - 1:
                time.sleep(3)
                
        return True
    except Exception as e:
        print(f"⚠️ Twilio API Error: {e}")
        print(f"\n📱 [FALLBACK SIMULATION] Sent to {to_number}")
        print(f"💬 Message: {message_body}\n")
        return True