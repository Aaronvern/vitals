
---

# FormFit Backend


---

## Prerequisites

### Hardware
- Computer with at least 4GB RAM and a decent CPU (for OpenCV and Wolfram).
- Internet connection (for Appwrite Cloud and Aptos testnet).

### Software

- **Wolfram Engine**: Free version for Wolfram Language
  - Download: [wolfram.com/engine/](https://www.wolfram.com/engine/)
  - Requires a Wolfram ID

### Accounts
- **Appwrite Cloud**: For database storage
  - Sign up: [appwrite.io](https://appwrite.io/)
---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<yourusername>/formfit-backend.git
cd formfit-backend
```
- Replace `<yourusername>` with the repo owner’s GitHub username.

### 2. Set Up Python Environment
1. **Create Virtual Environment**:
   ```bash
   python3 -m venv venv  # Windows: python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
2. **Install Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
   - If `requirements.txt` is missing, create it with:
     ```text
    fastapi==0.95.1
    uvicorn==0.21.1
    opencv-python==4.7.0.72
    mediapipe==0.10.21
    numpy==1.26.4
    requests==2.28.2
    aptos-sdk==0.10.0
    python-jose[cryptography]==3.3.0
    python-multipart==0.0.6
    wolframclient==1.4.0
    appwrite==2.0.2
    pydantic==1.10.21
    starlette==0.26.1
    cryptography==44.0.1
     ```
     Then run `pip install -r requirements.txt`.

### 3. Install Wolfram Engine
1. **Download and Install**:
   - Get it from [wolfram.com/engine/](https://www.wolfram.com/engine/).
   - Follow OS-specific instructions (e.g., `brew install wolfram-engine` on macOS with Homebrew).
2. **Activate**:
   ```bash
   wolframscript
   # Sign in with a Wolfram ID; exit with Ctrl+D
   ```
3. **Verify**:
   ```bash
   python -c "from wolframclient.evaluation import WolframLanguageSession; session = WolframLanguageSession(); print(session.evaluate(2 + 3)); session.terminate()"
   # Should output: 5
   ```

### 4. Install Aptos CLI
```bash
npm install -g @aptos-labs/aptos-cli
aptos --version  # Verify installation
```

---

## Configuration

### Appwrite Setup
1. **Access Appwrite Cloud**:
   - Use Aaron’s `formfit` project credentials (ask for Project ID, API Key, Database ID, and Collection IDs).
   - Or create a new project at [appwrite.io](https://appwrite.io/).
2. **Collections** (should already exist in Aaron’s setup):
   - `users`: `username` (string), `password` (string), `wallet_address` (string).
   - `workouts`: `user_id` (string), `date` (string), `reps` (integer, 1–10,000), `form_score` (integer, 1–10,000), `calories` (integer).
   - `rewards`: `user_id` (string), `reps_achieved` (integer), `tokens` (integer), `tx_hash` (string).

### Environment Variables
1. **Create `.env`**:
   ```bash
   touch .env
   ```
2. **Edit `.env`**:
   ```bash
   echo "APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1" >> .env
   echo "APPWRITE_PROJECT_ID=<AARON_PROJECT_ID>" >> .env
   echo "APPWRITE_API_KEY=<AARON_API_KEY>" >> .env
   echo "APPWRITE_DATABASE_ID=<AARON_DATABASE_ID>" >> .env
   echo "SECRET_KEY=hackathon-secret" >> .env
   echo "USERS_COLLECTION_ID=<AARON_USERS_ID>" >> .env
   echo "WORKOUTS_COLLECTION_ID=<AARON_WORKOUTS_ID>" >> .env
   echo "REWARDS_COLLECTION_ID=<AARON_REWARDS_ID>" >> .env
   ```
   - Replace placeholders with Aaron’s values (ask him for exact IDs and keys).

---

## Running the App

1. **Start the Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   - Access at `http://localhost:8000`.
   - Verify: Open `http://localhost:8000` in a browser; expect `{"message": "FormFit Backend"}`.

---

## Testing the API

### 1. Register a User
```bash
curl -X POST "http://localhost:8000/register" -H "Content-Type: application/json" -d '{"username": "test_user", "password": "test123", "wallet_address": "0x789"}'
```
- Expected: `{"access_token": "...", "token_type": "bearer"}`
- Copy the `access_token`.

### 2. Login
```bash
curl -X POST "http://localhost:8000/token" -H "Content-Type: application/json" -d '{"username": "test_user", "password": "test123"}'
```
- Expected: `{"access_token": "...", "token_type": "bearer"}`
- Use this token or the one from registration.

### 3. Analyze Video
- **Prepare**: Record a short (5–10 sec) squat video, save as `sample_video.mp4` in `backend/`.
- Command:
  ```bash
  curl -X POST "http://localhost:8000/analyze_video" -H "Authorization: Bearer <token>" -F "file=@sample_video.mp4"
  ```
- Expected: `{"user_id": "...", "reps": 1, "form_feedback": "...", "calories": 10}`

### 4. Wolfram Analyze
```bash
curl -X GET "http://localhost:8000/wolfram_analyze" -H "Authorization: Bearer <token>"
```
- Expected: `{"insights": "1 total reps, 10 avg calories, 100% avg form accuracy"}` (after one workout).

### 5. Mint Tokens
```bash
curl -X POST "http://localhost:8000/mint_tokens" -H "Authorization: Bearer <token>" -H "Content-Type: application/json" -d '{"reps": 10}'
```
- Expected: `{"status": "success", "tokens": 100, "tx": "mock_tx_hash"}`

---

## Troubleshooting

### General
- **Command Fails**: Ensure `venv` is active (`source venv/bin/activate`) and retry.
- **Missing `.env`**: Contact Aaron for exact values.

### OpenCV
- **Error**: `(-215:Assertion failed) !_filename.empty()`
- **Fix**: Verify `sample_video.mp4` exists and is valid:
  ```bash
  file sample_video.mp4  # Should show "ISO Media, MP4"
  ```

### Wolfram
- **Error**: 500 with Wolfram traceback
- **Fix**: Check Wolfram Engine:
  ```bash
  wolframscript  # Sign in if needed; exit with Ctrl+D
  ```

### Appwrite
- **Error**: 400/500 with Appwrite message
- **Fix**: Confirm `.env` matches Appwrite dashboard; check collection schemas.

---
