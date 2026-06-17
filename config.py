import os
import re
from dotenv import load_dotenv

# Environment variables load karein (.env file se)
load_dotenv()

TWILIO_ACCOUNT_SID = "ACfccb0d8fea8b7b29ceaeb1cecf4d7a5b"
TWILIO_AUTH_TOKEN = "db19b663c0867db62ac2ea0ec32ff429"
TWILIO_NUMBER = "+19452313548"

# Requirement 1: Background voice trigger ke liye specific code words
CODE_WORDS = ["help", "bachao", "emergency", "police", "stop"]

# Requirement 4: Indian Numbers standard validation filtering format
def validate_indian_number(phone_number):
    cleaned = re.sub(r'\s+', '', phone_number) # Spaces remove karein
    # Check regular expression formatting for 10 structural indian mobile digits
    pattern = re.compile(r'^(?:\+91|91)?[6-9]\d{9}$')
    if pattern.match(cleaned):
        if not cleaned.startswith('+91'):
            if cleaned.startswith('91') and len(cleaned) == 12:
                return "+" + cleaned
            else:
                return "+91" + cleaned
        return cleaned
    return None