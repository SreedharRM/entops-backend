# Empty payments.py file
from backend.core.events import emit_event

async def process_payment(task_id, amount: float, recipient: str):
    await emit_event(task_id, "in_progress", {"step": f"Paying {recipient}", "amount": amount})
    return {"status": "paid", "recipient": recipient, "amount": amount}
