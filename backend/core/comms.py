# Empty comms.py file
from backend.core.events import emit_event

async def process_email(task_id, sender: str, subject: str, body: str):
    await emit_event(task_id, "in_progress", {"step": "Reading email", "from": sender, "subject": subject})
    return {"action": "processed", "content": body}
