# FastAPI File Chunking Service

This is a FastAPI-based service for uploading and downloading files in chunks with authentication and checksum verification.

## Features
- JWT authentication using OAuth2 Bearer tokens
- Chunked file upload with checksum validation
- File download in chunks with byte range support
- File status checking

## Installation

1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/fastapi-file-chunking.git
   cd fastapi-file-chunking
   ```

2. **Create a virtual environment and install dependencies**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the FastAPI application**
   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API docs**
   - Open `http://127.0.0.1:8000/docs` in your browser.

## Endpoints

| Method | Endpoint        | Description |
|--------|----------------|-------------|
| POST   | `/token`       | Get authentication token |
| POST   | `/upload`      | Upload a file chunk |
| GET    | `/download`    | Download a file chunk |
| GET    | `/status`      | Check file upload status |
