# SecureTransfer

A secure message/file encryption web app with face authentication (DeepFace SFace), AES-256-GCM encryption, and a modern Bootstrap UI.

## Features
- Register/login with username, password, and face recognition (no dlib, SFace model)
- Encrypt/decrypt text or files with AES-256-GCM
- User-provided or random encryption key (never stored)
- Download/upload encrypted files
- Responsive, dark-themed UI with webcam capture, drag-and-drop, and toasts

## Requirements
- Python 3.9–3.12 (recommended)
- MongoDB (running locally or via Atlas)
- See `requirements.txt` for all Python dependencies (DeepFace, TensorFlow, tf-keras, etc.)

## Installation & Running

1. **Clone the repo:**
   ```sh
   git clone <repo-url>
   cd secureTransfer
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   > If you see errors about numpy, protobuf, or tensorflow/keras versions, try:
   > ```sh
   > pip install --upgrade pip
   > pip install --force-reinstall -r requirements.txt
   > ```
3. **Start MongoDB** (if not already running)
   - Local: `mongod` (default: `mongodb://localhost:27017/securetransfer`)
   - Or use MongoDB Atlas and set the `MONGO_URI` environment variable.
4. **Run the app:**
   ```sh
   python app.py
   ```
5. **Open in browser:**
   - Go to [http://localhost:5000](http://localhost:5000)

## Usage Guide
- **Register:**
  - Enter username, password, and capture/upload a face image.
- **Login:**
  - Enter username, password, and face image (must match registration).
- **Secure Transfer Panel:**
  - Choose Encrypt or Decrypt.
  - Select Text or File mode.
  - For encryption: enter text or upload a file, provide or generate a key, and download the encrypted result.
  - For decryption: upload the encrypted file or paste encrypted text, enter the key, and download/view the decrypted result.

## Security Notes
- Passwords hashed with bcrypt
- Face embeddings stored Base64-encoded in MongoDB
- AES-256-GCM with random 12-byte nonce per encryption
- No encryption keys stored on server
- CSRF protection enabled

## File Structure
- `app.py` - Flask entry point
- `models.py` - MongoDB models
- `auth.py` - Auth routes
- `transfer.py` - Encrypt/decrypt routes
- `static/` - CSS/JS
- `templates/` - HTML

---
MIT License
