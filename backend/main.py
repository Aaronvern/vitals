from fastapi import FastAPI
from routes import auth
# workouts

app = FastAPI()

app.include_router(auth.router, prefix="/auth")
#app.include_router(workouts.router, prefix="/workouts")

@app.get("/")
async def root():
    return {"message": "FormFit Backend"}
