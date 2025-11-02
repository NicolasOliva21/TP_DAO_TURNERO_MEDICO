import httpx
from typing import Any, Dict, Optional, Tuple
from settings import settings

class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _auth_headers(self, token: Optional[str]) -> Dict[str, str]:
        return {"Authorization": f"Bearer {token}"} if token else {}

    async def post(self, path: str, json: Dict[str, Any], token: Optional[str] = None):
        async with httpx.AsyncClient(timeout=12.0) as client:
            r = await client.post(f"{self.base_url}{path}", json=json, headers=self._auth_headers(token))
            r.raise_for_status()
            return r.json()

    async def get(self, path: str, params: Optional[Dict[str, Any]] = None, token: Optional[str] = None):
        async with httpx.AsyncClient(timeout=12.0) as client:
            r = await client.get(f"{self.base_url}{path}", params=params or {}, headers=self._auth_headers(token))
            r.raise_for_status()
            return r.json()

    async def put(self, path: str, json: Dict[str, Any], token: Optional[str] = None):
        async with httpx.AsyncClient(timeout=12.0) as client:
            r = await client.put(f"{self.base_url}{path}", json=json, headers=self._auth_headers(token))
            r.raise_for_status()
            return r.json()

    async def patch(self, path: str, json: Dict[str, Any], token: Optional[str] = None):
        async with httpx.AsyncClient(timeout=12.0) as client:
            r = await client.patch(f"{self.base_url}{path}", json=json, headers=self._auth_headers(token))
            r.raise_for_status()
            return r.json()

    async def delete(self, path: str, token: Optional[str] = None):
        async with httpx.AsyncClient(timeout=12.0) as client:
            r = await client.delete(f"{self.base_url}{path}", headers=self._auth_headers(token))
            r.raise_for_status()
            return {"ok": True}

api = ApiClient(settings.API_BASE_URL)
