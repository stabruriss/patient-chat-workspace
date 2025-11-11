"""
FastAPI Server for Healthcare Workflow Composer
Provides WebSocket support for real-time workflow generation and REST endpoints for condition/loop evaluation
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Dict, List, Any
import json
import asyncio
from datetime import datetime
import logging

# Import configuration and models
from backend.config.settings import settings
from backend.config.key_manager import key_manager
from backend.config.logging_config import setup_logging, get_agent_logger

# Initialize logging first
setup_logging()
logger = logging.getLogger(__name__)
agent_logger = get_agent_logger()
from backend.models.workflow_context import (
    WorkflowGenerationRequest,
    ConditionEvaluationRequest,
    LoopEvaluationRequest,
    WorkflowType
)

# Import agents
from backend.agents.workflow_generator import workflow_generator
from backend.agents.condition_evaluator import condition_evaluator
from backend.agents.loop_controller import loop_controller
from backend.agents.practice_insights import practice_insights_agent

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Workflow Composer API",
    description="AI-powered workflow generation and runtime evaluation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"[WebSocket] Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            print(f"[WebSocket] Client {client_id} disconnected")

    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)


manager = ConnectionManager()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Healthcare Workflow Composer API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "claude_api_configured": key_manager.is_configured(),
        "active_websocket_connections": len(manager.active_connections),
        "timestamp": datetime.now().isoformat()
    }


@app.websocket("/ws/workflow-chat")
async def workflow_chat_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time workflow generation chat.
    Frontend sends user messages, backend streams AI responses and generated blocks.
    """
    client_id = f"client-{id(websocket)}"
    await manager.connect(websocket, client_id)

    try:
        while True:
            # Receive message from frontend
            data = await websocket.receive_json()

            message_type = data.get("type")

            if message_type == "chat_message":
                # User sent a chat message
                user_message = data.get("message", "")
                workflow_type = data.get("workflow_type", "patient")
                existing_blocks = data.get("existing_blocks", [])

                # Validate workflow type
                if workflow_type not in ["patient", "practice"]:
                    await manager.send_message(client_id, {
                        "type": "error",
                        "error": "Invalid workflow_type. Must be 'patient' or 'practice'"
                    })
                    continue

                # Send acknowledgment
                await manager.send_message(client_id, {
                    "type": "processing_started",
                    "message": "Generating workflow..."
                })

                # Stream workflow generation
                try:
                    async for response in workflow_generator.generate_workflow_stream(
                        user_message=user_message,
                        workflow_type=workflow_type,
                        existing_blocks=existing_blocks
                    ):
                        await manager.send_message(client_id, response)

                except Exception as e:
                    await manager.send_message(client_id, {
                        "type": "error",
                        "error": f"Workflow generation error: {str(e)}"
                    })

            elif message_type == "reset_conversation":
                # Reset the conversation history
                workflow_generator.reset_conversation()
                await manager.send_message(client_id, {
                    "type": "conversation_reset",
                    "message": "Conversation history cleared"
                })

            elif message_type == "ping":
                # Heartbeat
                await manager.send_message(client_id, {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })

            else:
                await manager.send_message(client_id, {
                    "type": "error",
                    "error": f"Unknown message type: {message_type}"
                })

    except WebSocketDisconnect:
        manager.disconnect(client_id)
        print(f"[WebSocket] Client {client_id} disconnected")
    except Exception as e:
        print(f"[WebSocket] Error with client {client_id}: {str(e)}")
        manager.disconnect(client_id)


@app.post("/api/evaluate-condition")
async def evaluate_condition_endpoint(request: ConditionEvaluationRequest):
    """
    REST endpoint to evaluate a condition block at runtime.
    Used during workflow execution to make routing decisions.
    """
    try:
        result = await condition_evaluator.evaluate_condition(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/evaluate-loop")
async def evaluate_loop_endpoint(request: LoopEvaluationRequest):
    """
    REST endpoint to evaluate a loop decision at runtime.
    Determines whether to continue, break, or escalate the loop.
    """
    try:
        result = await loop_controller.evaluate_loop(request)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/parse-block-references")
async def parse_block_references(text: str):
    """
    Parse @@ block references from natural language text.
    Returns list of referenced block IDs.
    """
    import re
    pattern = r'@@([a-zA-Z0-9\-_]+)'
    matches = re.findall(pattern, text)

    return {
        "text": text,
        "referenced_blocks": matches,
        "count": len(matches)
    }


@app.get("/api/block-types")
async def get_block_types(workflow_type: str = "patient"):
    """
    Get available block types for a specific workflow type.
    Helps frontend understand what blocks can be created.
    """
    if workflow_type not in ["patient", "practice"]:
        raise HTTPException(status_code=400, detail="workflow_type must be 'patient' or 'practice'")

    block_types = {
        "patient": {
            "triggers": [
                "trigger-patient-profile",
                "trigger-order",
                "trigger-report",
                "trigger-encounter-note",
                "trigger-document",
                "trigger-calendar-event",
                "trigger-task",
                "trigger-internal-note"
            ],
            "actions": [
                "action-send-message",
                "action-send-email",
                "action-create-task",
                "action-update-patient",
                "action-generate-report"
            ],
            "logic": [
                "wait",
                "condition",
                "loop",
                "approval",
                "ai-touch"
            ]
        },
        "practice": {
            "triggers": [
                "trigger-scheduled",
                "trigger-threshold"
            ],
            "actions": [
                "action-send-message",
                "action-send-email",
                "action-create-task",
                "action-generate-report"
            ],
            "logic": [
                "wait",
                "condition",
                "loop",
                "approval",
                "ai-touch"
            ]
        }
    }

    return block_types.get(workflow_type, {})


@app.post("/api/practice-insights")
async def generate_practice_insights(request: Dict[str, Any]):
    """
    Generate AI-powered insights from practice operational data.

    Request body:
    {
        "practice_data": {
            "current_period": {...},
            "previous_period": {...},
            "period_comparison": {...},
            "top_services": [...],
            "peak_hours": [...],
            "provider_performance": [...]
        }
    }

    Returns:
    {
        "insights": [
            {
                "type": "positive|negative|neutral|warning",
                "title": "Insight title",
                "description": "Detailed description",
                "recommendation": "Optional recommendation"
            }
        ]
    }
    """
    try:
        practice_data = request.get("practice_data", {})

        if not practice_data:
            raise HTTPException(status_code=400, detail="practice_data is required")

        insights = await practice_insights_agent.generate_insights(practice_data)

        return {
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to generate practice insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/practice-ask")
async def ask_practice_question(request: Dict[str, Any]):
    """
    Answer a specific question about practice data.

    Request body:
    {
        "question": "What's our patient growth trend?",
        "practice_data": {
            "current_period": {...},
            "previous_period": {...},
            ...
        }
    }

    Returns:
    {
        "answer": "AI-generated answer",
        "question": "Original question",
        "timestamp": "ISO timestamp"
    }
    """
    try:
        question = request.get("question", "")
        practice_data = request.get("practice_data", {})

        if not question:
            raise HTTPException(status_code=400, detail="question is required")

        if not practice_data:
            raise HTTPException(status_code=400, detail="practice_data is required")

        answer = await practice_insights_agent.answer_question(question, practice_data)

        return {
            "answer": answer,
            "question": question,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Failed to answer practice question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    print(f"[ERROR] {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("Healthcare Workflow Composer API")
    print("=" * 60)
    print(f"Starting server on {settings.host}:{settings.port}")
    print(f"WebSocket endpoint: ws://{settings.host}:{settings.port}/ws/workflow-chat")
    print(f"Health check: http://{settings.host}:{settings.port}/api/health")
    print("=" * 60)

    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
