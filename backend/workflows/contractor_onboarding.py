from backend.core.events import emit_event
import asyncio
from services.agentmail import sendmes
from backend.core.convex_client import convex

async def contractor_onboarding(task_id: str, contractor_info: dict = None, **kwargs):
    """Handle contractor onboarding workflow"""
    if not contractor_info:
        contractor_info = {}
    
    contractor_name = contractor_info.get("name", "Unknown")
    contractor_email = contractor_info.get("email", "")
    
    await emit_event(task_id, "started", {"workflow": "contractor_onboarding", "contractor": contractor_name})
    
    try:
        # Step 1: Create contractor profile
        await emit_event(task_id, "in_progress", {
            "step": f"Creating profile for {contractor_name}",
            "action": "profile_creation"
        })
        await asyncio.sleep(0.5)

            # Persist to Convex
        try:
            # Add event to Convex
            await convex.mutation("contractors:createContractor", {
            "contractorId": "4821",
            "name": "Alex Johnson",
            "jobTitle": "Software Engineer",
            "department": "IT – Application Development",
            "email": "alex.johnson@fakemail.com",
            "phone": "(555) 234-9876",
            "dateOfJoining": "2022-03-15T00:00:00.000Z",
            "location": "Austin, Texas",
            "manager": "Sarah Williams"
            })
        except Exception as e:
            print(f"⚠️ Convex logging error: {e}")
        
        # Step 2: Send welcome email
        await emit_event(task_id, "in_progress", {
            "step": f"Sending welcome email to {contractor_email}",
            "action": "welcome_email"
        })
        await asyncio.sleep(0.5)

        # Send the mail (awaitable now because of to_thread)
        response = await asyncio.to_thread(
            sendmes,
            inbox_id="your_inbox_id",
            to=contractor_email,
            cc=None,
            subject="Welcome to the Project!",
            text=f"Hi {contractor_email},\n\nWelcome aboard! We're excited to have you join us.",
            html=f"<p>Hi {contractor_email},</p><p><b>Welcome aboard!</b> We're excited to have you join us.</p>"
        )

        print("Mail sent:", response)
        
        # Step 3: Setup access permissions
        await emit_event(task_id, "in_progress", {
            "step": f"Setting up access permissions for {contractor_name}",
            "action": "permissions_setup"
        })
        await asyncio.sleep(0.5)
        
        # Step 4: Schedule orientation
        await emit_event(task_id, "in_progress", {
            "step": f"Scheduling orientation session for {contractor_name}",
            "action": "orientation_scheduled"
        })
        
        await emit_event(task_id, "completed", {
            "result": f"Contractor onboarding completed for {contractor_name}",
            "contractor": contractor_name
        })
        
    except Exception as e:
        await emit_event(task_id, "failed", {"error": str(e)})
