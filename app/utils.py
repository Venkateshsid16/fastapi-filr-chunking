import jwt
import hashlib
from datetime import datetime, timedelta
from app.config import SECRET_KEY, ALGORITHM

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=30))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_checksum(content: bytes, expected_checksum: int) -> bool:
    return sum(content) % 256 == expected_checksum
