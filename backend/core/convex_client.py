import asyncio
from typing import Dict, Any, Optional
from convex import ConvexClient as SyncConvexClient
from backend.config.settings import settings


class ConvexClient:
    """Async wrapper around the official synchronous Convex Python client."""

    def __init__(self, convex_url: Optional[str] = None):
        self.convex_url = convex_url or settings.CONVEX_URL
        # Note: Python Convex client currently doesn't use API key; URL identifies deployment
        self._client = SyncConvexClient(self.convex_url)

    async def mutation(self, function_name: str, args: Dict[str, Any] | None = None) -> Dict[str, Any]:
        args = args or {}
        return await asyncio.to_thread(self._client.mutation, function_name, args)

    async def query(self, function_name: str, args: Dict[str, Any] | None = None) -> Dict[str, Any]:
        args = args or {}
        return await asyncio.to_thread(self._client.query, function_name, args)

    async def close(self):
        # No-op for sync client
        return None


# Global Convex client instance
convex = ConvexClient()
