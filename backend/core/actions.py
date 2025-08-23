# Empty actions.py file
from backend.core.events import emit_event
import asyncio

async def browser_login_and_fill_form(task_id, site: str, data: dict):
    await emit_event(task_id, "in_progress", {"step": f"Logging into {site}"})
    await asyncio.sleep(1)
    await emit_event(task_id, "in_progress", {"step": f"Filling form with data {data}"})
    return {"status": "form submitted"}
