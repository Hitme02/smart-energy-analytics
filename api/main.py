# api/main.py

from fastapi import FastAPI
from api.chatbot_interface import router as chatbot_router

app = FastAPI()
app.include_router(chatbot_router)

@app.get("/")
def root():
    return {"msg": "Smart Energy Analytics API is running!"}
