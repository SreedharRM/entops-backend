import asyncio
import json
import os
import sys
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv

# Allow loading from .env.local if present
if os.path.exists('.env.local'):
    load_dotenv('.env.local', override=True)
else:
    load_dotenv(override=True)

# Use our existing Convex HTTP client
from backend.core.convex_client import ConvexClient


def fmt(ts_ms: int) -> str:
    try:
        return datetime.fromtimestamp(ts_ms / 1000).isoformat()
    except Exception:
        return str(ts_ms)


async def print_task(convex: ConvexClient, task_id: str):
    res = await convex.query("tasks:getTask", {"taskId": task_id})
    print("Task:", json.dumps(res, indent=2, default=str))


async def print_events(convex: ConvexClient, task_id: str):
    res = await convex.query("events:getEvents", {"taskId": task_id})
    events = res.get("events", [])
    print(f"Events ({len(events)}):")
    for e in events:
        ts = e.get("timestamp")
        print(f"- {fmt(ts)} | {e.get('status')} | details={json.dumps(e.get('details'), default=str)}")


async def poll_updates(convex: ConvexClient, task_id: str, interval: float = 2.0, rounds: int = 10):
    print(f"\nPolling updates for task {task_id} every {interval}s (rounds={rounds})...")
    prev_status: Optional[str] = None
    prev_events_count = -1
    for i in range(rounds):
        task = await convex.query("tasks:getTask", {"taskId": task_id})
        status = (task or {}).get("status")
        if status != prev_status:
            print(f"[{i}] Status: {status}")
            prev_status = status
        ev = await convex.query("events:getEvents", {"taskId": task_id})
        events = ev.get("events", [])
        if len(events) != prev_events_count:
            print(f"[{i}] Events count: {len(events)}")
            prev_events_count = len(events)
        await asyncio.sleep(interval)


async def main():
    convex_url = os.getenv("CONVEX_URL")
    if not convex_url:
        print("ERROR: CONVEX_URL is not set. Put it in .env.local or your environment.")
        sys.exit(1)

    convex = ConvexClient(convex_url)

    # task_id from argv, otherwise print a hint and exit
    if len(sys.argv) < 2:
        print("Usage: python scripts/test_convex.py <task_id>")
        print("Tip: create a task via POST /task first, then pass its task_id here.")
        sys.exit(2)

    task_id = sys.argv[1]

    await print_task(convex, task_id)
    await print_events(convex, task_id)
    await poll_updates(convex, task_id)

    await convex.close()


if __name__ == "__main__":
    asyncio.run(main())
