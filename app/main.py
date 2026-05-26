from fastapi import FastAPI

from app.api.upload import router as upload_router
from app.api.ask import router as ask_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(ask_router)

@app.get("/")
def home():
    return {"message": "OmniMind AI Running"}