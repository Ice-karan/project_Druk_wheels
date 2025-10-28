from cryptography.fernet import Fernet
from django.conf import settings
import os

# Generate or load encryption key
def get_encryption_key():
    key = getattr(settings, 'ENCRYPTION_KEY', None)
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in settings")
    return key

cipher = Fernet(get_encryption_key())

def encrypt_message(content):
    return cipher.encrypt(content.encode()).decode()

def decrypt_message(encrypted_content):
    return cipher.decrypt(encrypted_content.encode()).decode()
