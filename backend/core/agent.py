# Empty agent.py file
import uuid
from backend.core.events import emit_event

class Agent:
    def __init__(self, name="AI Employee"):
        self.id = str(uuid.uuid4())
        self.name = name

    async def perform_task(self, task_id: str, task: dict):
        """Execute a task and emit events step by step."""
        await emit_event(task_id, "started", {"task": task})

        try:
            # Process different task types
            task_type = task.get("type")
            task_data = task.get("data", {})
            
            await emit_event(task_id, "in_progress", {"step": f"Processing {task_type}..."})
            
            if task_type == "sales_sequence_update":
                await self._handle_sales_sequence_update(task_id, task_data)
            else:
                await emit_event(task_id, "in_progress", {"step": "Generic task processing..."})
            
            await emit_event(task_id, "completed", {"result": f"Task {task_type} completed ✅"})
        except Exception as e:
            await emit_event(task_id, "failed", {"error": str(e)})

    async def _handle_sales_sequence_update(self, task_id: str, data: dict):
        """Handle sales sequence update task"""
        leads = data.get("leads", [])
        await emit_event(task_id, "in_progress", {"step": f"Processing {len(leads)} leads"})
        
        for i, lead in enumerate(leads):
            await emit_event(task_id, "in_progress", {
                "step": f"Processing lead {i+1}/{len(leads)}: {lead.get('name', 'Unknown')}"
            })
            # Simulate processing time
            import asyncio
            await asyncio.sleep(0.5)
        
        await emit_event(task_id, "in_progress", {"step": "Sales sequence update completed"})
