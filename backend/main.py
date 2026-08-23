import sys
import os

# ---- YEH TEEN LINES ADD KI HAIN AZURE KE PATH MASLE KE LIYE ----
# Yeh Python ko batata hai ke "bhai, 'app' folder yahin backend ke andar rakha hai, usay dhoond lo"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# ----------------------------------------------------------------

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import home
from app.api import dashboard
from app.api import predict
from app.api import chatbot


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="AI Student Analytics Dashboard",
    version="1.0.0",
    description="ML + RAG + Analytics Dashboard using FastAPI and Ollama",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://happy-sand-0612d6410.azurestaticapps.net",
        "https://happy-sand-0612d6410.7.azurestaticapps.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROUTERS
# ============================================================

# Home / default routes
app.include_router(home.router)

# Dashboard analytics routes
app.include_router(dashboard.router)

# Machine Learning prediction routes
app.include_router(predict.router)

# AI Chatbot / RAG routes
app.include_router(chatbot.router)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():
    return {
        "message": "AI Student Analytics Dashboard API",
        "status": "running",
        "version": "1.0.0",
    }


# ============================================================
# ABOUT
# ============================================================

@app.get("/about")
def about():
    return {
        "name": "AI Student Analytics Dashboard",
        "version": "1.0.0",
        "description": "ML + RAG + Analytics Dashboard using FastAPI and Ollama",
        "features": [
            "Student Analytics",
            "CGPA Prediction",
            "AI Chatbot",
            "RAG",
            "Local Ollama AI",
        ],
    }