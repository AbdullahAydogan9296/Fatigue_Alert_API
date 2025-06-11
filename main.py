from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Fatigue Alert API is running!"}