from backend.core.events import emit_event
import asyncio

async def sales_sequence_update(task_id: str, leads: list = None, lead_list: list = None, **kwargs):
    """Handle sales sequence update workflow"""
    # Handle both 'leads' and 'lead_list' parameter names
    if leads is None:
        leads = lead_list or []
    if not leads:
        leads = []
    
    await emit_event(task_id, "started", {"workflow": "sales_sequence_update", "lead_count": len(leads)})
    
    try:
        # Process each lead
        for i, lead in enumerate(leads):
            lead_name = lead.get("name", "Unknown")
            lead_email = lead.get("email", "")
            
            await emit_event(task_id, "in_progress", {
                "step": f"Processing lead {i+1}/{len(leads)}",
                "lead_name": lead_name,
                "lead_email": lead_email
            })
            
            # Simulate lead processing
            await asyncio.sleep(0.5)
            
            # Update CRM (simulated)
            await emit_event(task_id, "in_progress", {
                "step": f"Updated CRM for {lead_name}",
                "action": "crm_update"
            })
            
            # Send follow-up email (simulated)
            await emit_event(task_id, "in_progress", {
                "step": f"Sent follow-up email to {lead_email}",
                "action": "email_sent"
            })
        
        await emit_event(task_id, "completed", {
            "result": f"Sales sequence updated for {len(leads)} leads",
            "leads_processed": len(leads)
        })
        
    except Exception as e:
        await emit_event(task_id, "failed", {"error": str(e)})
