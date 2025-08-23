from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from backend.core.orchestrator import Orchestrator
from backend.core.events import event_queue
from backend.core.approvals import approve_task, reject_task
from backend.core.convex_client import convex
import uvicorn
import json
from typing import List
from datetime import datetime
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(title="EntOps", description="Enterprise Operations API", version="1.0.0")

# ✅ Disable/Allow CORS (open to all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allow all origins (frontend domains)
    allow_credentials=True,
    allow_methods=["*"],       # Allow all HTTP methods
    allow_headers=["*"],       # Allow all headers
)

# Global orchestrator instance
orchestrator = Orchestrator()

# Pydantic models for request validation
class TaskRequest(BaseModel):
    type: str
    data: dict

@app.get("/")
async def root():
    return {"message": "EntOps API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/task")
async def create_task(task: TaskRequest):
    """Assign a new task to the AI Employee."""
    result = await convex.mutation("tasks:createTask", {
        "type": task.type,
        "data": task.data,
        "status": "assigned"
    })
    
    task_id = result.get("taskId")
    if task_id:
        await orchestrator.assign_task({"type": task.type, "data": task.data}, task_id)
    
    return {"task_id": task_id, "status": "assigned"}

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a specific task."""
    result = await convex.query("tasks:getTask", {"taskId": task_id})
    return result

@app.get("/tasks/{task_id}/logs")
async def get_task_logs(task_id: str):
    """Get all logs for a specific task."""
    result = await convex.query("events:getEvents", {"taskId": task_id})
    return result.get("events", [])

@app.get("/tasks/{task_id}/approvals")
async def get_task_approvals(task_id: str):
    """Get all approvals for a specific task."""
    result = await convex.query("approvals:getByTask", {"taskId": task_id})
    return result.get("approvals", [])

@app.post("/tasks/{task_id}/approve")
async def approve(task_id: str):
    """Approve a pending task."""
    return await approve_task(task_id)

@app.post("/tasks/{task_id}/reject")
async def reject(task_id: str):
    """Reject a pending task."""
    return await reject_task(task_id)

# WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/tasks")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        import asyncio
        async def send_events():
            while True:
                try:
                    event = await asyncio.wait_for(event_queue.get(), timeout=1.0)
                    await manager.send_personal_message(json.dumps(event), websocket)
                except asyncio.TimeoutError:
                    continue
                except Exception:
                    break
        
        event_task = asyncio.create_task(send_events())
        
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            response = {
                "type": "message",
                "data": message,
                "timestamp": str(datetime.now())
            }
            await manager.send_personal_message(json.dumps(response), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        if 'event_task' in locals():
            event_task.cancel()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
