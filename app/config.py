import os

UPLOAD_DIR = "uploads"
SECRET_KEY = "c7f9d32ef1c4e497945d0dfe93a6b7989c2c1cb3602b8b31ed7696960aabc158"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

os.makedirs(UPLOAD_DIR, exist_ok=True)
