import uuid
from datetime import datetime
from backend.core.agent import Agent
from backend.core.events import emit_event

# Import workflow functions from package
from backend.workflows.sales_sequence_update import sales_sequence_update
from backend.workflows.contractor_onboarding import contractor_onboarding
from backend.workflows.commission_payment import commission_payment

class Orchestrator:
    def __init__(self):
        self.agent = Agent()
        self.tasks = {}
        # Map task types to workflow functions
        self.workflow_map = {
            "sales_sequence_update": sales_sequence_update,
            "contractor_onboarding": contractor_onboarding,
            "commission_payment": commission_payment,
        }

    async def assign_task(self, task: dict, task_id: str = None) -> str:
        """Assign a task and return task ID"""
        if not task_id:
            task_id = str(uuid.uuid4())
            
        self.tasks[task_id] = {
            "id": task_id,
            "status": "assigned",
            "task": task,
            "created_at": datetime.now()
        }
        
        await emit_event(task_id, "received", {"task_type": task.get("type")})
        
        # Route task to appropriate workflow
        await self._route_task(task_id, task)
        
        return task_id

    async def _route_task(self, task_id: str, task: dict):
        task_type = task.get("type")
        data = task.get("data", {})

        # Route task to the right workflow
        workflow_fn = self.workflow_map.get(task_type)
        if not workflow_fn:
            await emit_event(task_id, "failed", {"error": f"Unknown task type: {task_type}"})
            return

        # Run the workflow
        try:
            await workflow_fn(task_id, **data)
        except Exception as e:
            await emit_event(task_id, "failed", {"error": str(e)})

        return task_id
