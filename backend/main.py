from fastapi import FastAPI, UploadFile, File, Depends
from auth import get_current_user, login, register, LoginRequest, RegisterRequest
from video_analysis import analyze_video
from wolfram_analysis import wolfram_analyze
from aptos_rewards import mint_tokens

app = FastAPI()

# Endpoints
@app.get("/")
async def root():
    return {"message": "FormFit Backend"}

@app.post("/token")
async def token(request: LoginRequest):
    return login(request)

@app.post("/register")
async def register_user(request: RegisterRequest):
    return register(request)

@app.post("/analyze_video")
async def video_analysis(file: UploadFile = File(...), user: dict = Depends(get_current_user)):
    return await analyze_video(file, user)

@app.get("/wolfram_analyze")
async def get_wolfram_analysis(user: dict = Depends(get_current_user)):
    return wolfram_analyze(user)

@app.post("/mint_tokens")
async def mint_user_tokens(reps: int, user: dict = Depends(get_current_user)):
    return mint_tokens(reps, user)