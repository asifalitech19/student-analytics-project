"""
======================================================================
AI STUDENT ANALYTICS DASHBOARD
LOCAL AI CHATBOT API
======================================================================

Purpose:
    Expose the local Ollama-powered chatbot through FastAPI.

Endpoint:
    POST /api/chatbot/

The actual AI/RAG logic remains inside:
    app.rag.chatbot.chat_with_ai

No cloud AI API is used here.
======================================================================
"""

from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.rag.chatbot import chat_with_ai


# ======================================================================
# ROUTER
# ======================================================================

router = APIRouter(
    prefix="/api/chatbot",
    tags=["AI Chatbot"],
)


# ======================================================================
# REQUEST MODEL
# ======================================================================

class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User question"
    )

    conversation: Optional[
        List[ChatMessage]
    ] = None


# ======================================================================
# HEALTH
# ======================================================================

@router.get("/health")
def chatbot_health():
    """
    Basic chatbot API health check.
    """

    return {
        "status": "ready",
        "provider": "Ollama",
        "mode": "local",
    }


# ======================================================================
# CHAT
# ======================================================================

@router.post("/")
def chatbot(
    request: ChatRequest
):
    """
    Send a question to the local AI chatbot.
    """

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        # --------------------------------------------------------------
        # Convert Pydantic messages to plain dictionaries
        # --------------------------------------------------------------

        conversation = None

        if request.conversation:

            conversation = [
                {
                    "role":
                        message.role,

                    "content":
                        message.content,
                }

                for message
                in request.conversation
            ]

        # --------------------------------------------------------------
        # Local AI / RAG call
        # --------------------------------------------------------------

        result = chat_with_ai(

            question=question,

            conversation=conversation,
        )

        # --------------------------------------------------------------
        # Preserve existing chatbot response
        # --------------------------------------------------------------

        if isinstance(
            result,
            dict
        ):

            return {
                "success": True,
                **result,
            }

        # --------------------------------------------------------------
        # Fallback if chatbot returns plain text
        # --------------------------------------------------------------

        return {
            "success": True,
            "response": str(result),
        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:

        print(
            f"[CHATBOT ERROR] {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Local AI chatbot failed: "
                f"{str(error)}"
            ),
        )