# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.api.predict import router as predict_router

# from app.api.chatbot import router as chatbot_router    
# # ===============================
# # Import Routers
# # ===============================

# from app.api.home import router as home_router
# from app.api.dashboard import router as dashboard_router

# # Future Routers (uncomment when created)
# # from app.api.prediction import router as prediction_router
# # from app.api.chatbot import router as chatbot_router

# # ===============================
# # FastAPI App
# # ===============================

# app = FastAPI(
#     title="AI Student Analytics Dashboard",
#     version="1.0.0",
#     description="ML + RAG + Analytics Dashboard using FastAPI and Ollama"
# )

# # ===============================
# # CORS
# # ===============================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ===============================
# # Include Routers
# # ===============================

# app.include_router(home_router)
# app.include_router(dashboard_router)
# app.include_router(predict_router)

# # Future APIs
# # app.include_router(prediction_router)
# # app.include_router(chatbot_router)

# # ===============================
# # Root Endpoint
# # ===============================

# @app.get("/")
# def root():
#     return {
#         "message": "Welcome to AI Student Analytics Dashboard 🚀",
#         "status": "API Running Successfully"
#     }









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