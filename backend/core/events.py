import asyncio
from datetime import datetime
from backend.core.convex_client import convex

event_queue = asyncio.Queue()

async def emit_event(task_id: str, status: str, details: dict = None):
    event = {
        "task_id": task_id,
        "status": status,
        "details": details or {},
        "timestamp": datetime.utcnow().isoformat()
    }

    # Push to WebSocket
    await event_queue.put(event)

    # Persist to Convex
    try:
        # Add event to Convex
        await convex.mutation("events:addEvent", {
            "taskId": task_id,
            "status": status,
            "details": event["details"],
            "timestamp": event["timestamp"]
        })
        
        # Update task status in Convex
        await convex.mutation("tasks:updateTaskStatus", {
            "taskId": task_id,
            "status": status
        })
    except Exception as e:
        print(f"⚠️ Convex logging error: {e}")
