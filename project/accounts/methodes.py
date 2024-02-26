from django.utils import timezone
from datetime import timedelta
import random

def generate_code():
    code_verivecation = random.randint(1000,9999)
    return code_verivecation

def get_expiration_time():
    return timezone.now() + timedelta(minutes=10)