from backend.core.events import emit_event
from backend.core.convex_client import convex
import asyncio

async def require_approval(task_id, action: dict):
    # Store approval in Convex
    await convex.mutation("approvals:createApproval", {
        "taskId": task_id,
        "action": action,
        "status": "pending"
    })
    
    await emit_event(task_id, "pending_approval", {"action": action})
    return {"status": "waiting_for_approval"}

async def approve_task(task_id):
    # Call Convex mutation to approve task
    result = await convex.mutation("approvals:approveTask", {"taskId": task_id})
    
    if result.get("error"):
        return {"status": "not_found"}
    
    action = result.get("action", {})
    await emit_event(task_id, "approved", {"action": action})
    
    # Continue workflow after approval
    await continue_workflow_after_approval(task_id, action)
    
    return {"status": "approved", "action": action}

async def reject_task(task_id):
    # Call Convex mutation to reject task
    result = await convex.mutation("approvals:rejectTask", {"taskId": task_id})
    
    if result.get("error"):
        return {"status": "not_found"}
    
    action = result.get("action", {})
    await emit_event(task_id, "rejected", {"action": action})
    return {"status": "rejected"}

async def continue_workflow_after_approval(task_id, action):
    """Continue workflow execution after approval"""
    from backend.core.payments import process_payment
    from backend.core.memory import fetch_policy
    
    try:
        # Step 4 – Process payment (after approval)
        payment = await process_payment(task_id, action["amount"], action["recipient"])
        
        # Get policy for completion event
        policy = await fetch_policy(task_id, "contractor commission")
        
        await emit_event(task_id, "completed", {"policy": policy, "payment": payment})
    except Exception as e:
        await emit_event(task_id, "failed", {"error": str(e)})
