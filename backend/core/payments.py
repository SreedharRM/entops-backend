# Empty payments.py file
from backend.core.events import emit_event
from services.agentmail import sendmes
import asyncio

async def process_payment(task_id, amount: float, recipient: str):
    response = await asyncio.to_thread(
            sendmes,
            inbox_id="your_inbox_id",
            to="contractor_email",
            cc=None,
            subject="Welcome to the Project!",

            html = f"""
            <p>Hi Finance Team,</p>
            This is to inform you that the payment of $2000 "
            (Transaction ID: 8908209312) has been successfully processed.</b></p>
            <p>Thank you.</p>
            """
    )

    print("Mail sent:", response)
    await emit_event(task_id, "in_progress", {"step": f"Paying {recipient}", "amount": amount})
    return {"status": "paid", "recipient": recipient, "amount": amount}
