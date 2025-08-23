import os
from dotenv import load_dotenv
from convex import ConvexClient

# Load environment (prefer .env.local if present)
if os.path.exists('.env.local'):
    load_dotenv('.env.local', override=True)
else:
    load_dotenv(override=True)

CONVEX_URL = os.getenv("CONVEX_URL")
if not CONVEX_URL:
    raise SystemExit("CONVEX_URL not set. Put it in .env.local or .env")

client = ConvexClient(CONVEX_URL)

# One-shot fetch
print(client.query("tasks:get"))

# Live updates (Ctrl-C to exit)
for tasks in client.subscribe("tasks:get"):
    print(tasks)
