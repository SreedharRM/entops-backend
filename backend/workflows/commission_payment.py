import asyncio
from backend.core.comms import process_email
from backend.core.memory import fetch_policy
from backend.core.payments import process_payment
from backend.core.events import emit_event
from backend.core.approvals import require_approval, approve_task

async def commission_payment(task_id, email: dict, amount: float, recipient: str):
    try:
        await emit_event(task_id, "started", {"workflow": "commission_payment"})

        # Step 1 – Read invoice email
        await process_email(task_id, email["from"], email["subject"], email["body"])

        # Step 2 – Validate with finance policy
        policy = await fetch_policy(task_id, "contractor commission")

        # Step 3 – Require manager approval
        await require_approval(task_id, {"amount": amount, "recipient": recipient})
        return  # wait until /approve endpoint is called

        # Step 4 – Process payment (after approval)
        payment = await process_payment(task_id, amount, recipient)

        await emit_event(task_id, "completed", {"policy": policy, "payment": payment})
    except Exception as e:
        await emit_event(task_id, "failed", {"error": str(e)})
