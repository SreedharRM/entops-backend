# Empty memory.py file
from backend.core.events import emit_event

async def fetch_policy(task_id, topic: str):
    await emit_event(task_id, "in_progress", {"step": f"Fetching policy for {topic}"})
    # Simulated policy fetch
    return {"policy": f"Policy for {topic}: Contractors must be paid within 30 days."}
