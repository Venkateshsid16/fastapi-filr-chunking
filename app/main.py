import asyncio
import os
import aiofiles
import hashlib
import jwt
from datetime import datetime, timedelta
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.config import UPLOAD_DIR, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils import create_access_token, verify_checksum

app = FastAPI()

# OAuth2 scheme for JWT authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

class FileStatus(BaseModel):
    filename: str
    status: str
    next_byte: int

@app.post("/token")
async def login():
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": "device_id"}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload")
async def upload_file_chunk(file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    try:
        header = await file.read(12)
        start_byte, end_byte, checksum = int.from_bytes(header[:4], 'big'), int.from_bytes(header[4:8], 'big'), int.from_bytes(header[8:], 'big')
        content = await file.read()

        if not verify_checksum(content, checksum):
            raise HTTPException(status_code=400, detail="Checksum validation failed")

        file_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(file_path, 'ab') as f:
            await f.seek(start_byte)
            await f.write(content)

        return {"message": "Chunk uploaded successfully", "next_byte": end_byte + 1}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
async def download_file_chunk(filename: str, range: str, token: str = Depends(oauth2_scheme)):
    try:
        start_byte, end_byte = map(int, range.replace("bytes=", "").split("-"))
        file_path = os.path.join(UPLOAD_DIR, filename)

        async def file_streamer():
            async with aiofiles.open(file_path, 'rb') as f:
                await f.seek(start_byte)
                chunk = await f.read(end_byte - start_byte + 1)
                yield chunk

        return StreamingResponse(file_streamer(), headers={"Content-Range": f"bytes {start_byte}-{end_byte}/{os.path.getsize(file_path)}"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/status")
async def check_file_status(filename: str, token: str = Depends(oauth2_scheme)):
    try:
        file_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(file_path):
            return {"filename": filename, "status": "pending", "next_byte": 0}

        file_size = os.path.getsize(file_path)
        return {"filename": filename, "status": "partially_received", "next_byte": file_size}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
