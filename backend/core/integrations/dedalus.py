import os
import asyncio
from typing import Any, AsyncGenerator, Dict, Optional, Union

from dotenv import load_dotenv
from slack_sdk.web.async_client import AsyncWebClient
from dedalus_labs import AsyncDedalus, DedalusRunner
from dedalus_labs.utils.streaming import stream_async
from mcp.server import MCPServer, action

# ---------------------------------------------------------------------------
# Load environment variables from .env.local
# ---------------------------------------------------------------------------
load_dotenv(".env.local")

DEDALUS_API_KEY = os.getenv("DEDALUS_API_KEY")
SLACK_TOKEN = os.getenv("SLACK_BOT_TOKEN")
DEDALUS_API_URL = os.getenv("DEDALUS_API_URL", "https://api.dedaluslabs.ai/mcp")

print(f"[dedalus.py] Loaded. API_KEY_SET={bool(DEDALUS_API_KEY)} SLACK_TOKEN_SET={bool(SLACK_TOKEN)}")

if not SLACK_TOKEN:
    raise RuntimeError("SLACK_BOT_TOKEN not set in .env.local")

slack = AsyncWebClient(token=SLACK_TOKEN)

# ---------------------------------------------------------------------------
# 1) Slack MCP Server
# ---------------------------------------------------------------------------
server = MCPServer("slack")

@action("send_message")
async def send_message(channel: str, text: str):
    """
    Send a message to a Slack channel.
    Args:
        channel (str): Channel name or ID (e.g. "#general")
        text (str): Message text
    """
    resp = await slack.chat_postMessage(channel=channel, text=text)
    return {"ok": resp["ok"], "ts": resp.get("ts")}

@action("list_channels")
async def list_channels():
    """
    List all public Slack channels.
    """
    resp = await slack.conversations_list()
    return resp["channels"]

# ---------------------------------------------------------------------------
# 2) Dedalus SDK Client Wrapper
# ---------------------------------------------------------------------------
class DedalusClient:
    """Thin wrapper around Dedalus AsyncDedalus + DedalusRunner."""

    def __init__(self):
        self._client = AsyncDedalus()
        self._runner = DedalusRunner(self._client)

    async def run(
        self,
        input_text: str,
        *,
        model: str = "openai/gpt-4o-mini",
        mcp_servers: Optional[list[str]] = None,
        stream: bool = False,
    ) -> Union[Dict[str, Any], AsyncGenerator[str, None]]:
        mcp_servers = mcp_servers or []

        if not stream:
            result = await self._runner.run(
                input=input_text,
                model=model,
                mcp_servers=mcp_servers,
                stream=False,
            )
            return {"final_output": getattr(result, "final_output", None), "raw": result}

        async def _gen() -> AsyncGenerator[str, None]:
            async for chunk in stream_async(
                self._runner.run(
                    input=input_text,
                    model=model,
                    mcp_servers=mcp_servers,
                    stream=True,
                )
            ):
                yield chunk if isinstance(chunk, str) else str(chunk)

        return _gen()

# ---------------------------------------------------------------------------
# 3) Example usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    async def _main():
        # Start Slack MCP server (so Dedalus can talk to it)
        asyncio.create_task(server.serve())

        # Run a Dedalus request that uses Slack MCP
        client = DedalusClient()
        result = await client.run(
            input="Send a message to #general saying 'Hello from AI Employee OS 🚀'",
            model="openai/gpt-4o-mini",
            mcp_servers=["slack"],  # 👈 our custom Slack MCP
            stream=False,
        )
        print("Slack MCP final_output:", result.get("final_output"))

    asyncio.run(_main())
