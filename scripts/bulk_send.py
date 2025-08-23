#!/usr/bin/env python3
import os
import sys
import json
import asyncio
import httpx

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1:8000")
DATA_FILE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), '..', 'sampleData.jsonl')

async def send_line(client: httpx.AsyncClient, payload: dict):
    r = await client.post(f"{BASE_URL}/task", json={
        "type": "todo_import",
        "data": payload
    })
    r.raise_for_status()
    return r.json()

async def main():
    print(f"Using BASE_URL={BASE_URL}")
    print(f"Reading data from {DATA_FILE}")
    created = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        with open(DATA_FILE, 'r') as f:
            for i, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception as e:
                    print(f"Skipping line {i}: invalid JSON: {e}")
                    continue
                try:
                    resp = await send_line(client, obj)
                    created.append(resp.get('task_id'))
                    print(f"[{i}] created task_id={resp.get('task_id')} status={resp.get('status')}")
                except httpx.HTTPError as e:
                    print(f"[{i}] HTTP error: {e}")
    print("\nSummary:")
    print(json.dumps({"count": len([x for x in created if x]), "task_ids": created}, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
