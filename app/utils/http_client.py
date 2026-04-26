import logging
import os

import httpx


class HttpClient:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._client = httpx.AsyncClient()

    async def post(
        self,
        endpoint: str,
        payload: dict | None = None,
        content: bytes | None = None,
        timeout: float = 5.0,
        headers: dict = None
    ):
        headers = headers or {}

        try:
            response = await self._client.post(
                endpoint,
                json=payload if payload else None,
                content=content if content else None,
                timeout=timeout,
                headers=headers
            )

            response.raise_for_status()

            return {
                "content": response.content,
                "json": response.json() if "application/json" in response.headers.get("content-type", "") else None,
                "headers": dict(response.headers),
                "status_code": response.status_code
            }

        except httpx.RequestError as e:
            self._logger.error(f"Request failed: {str(e)}")
            return None

        except httpx.HTTPStatusError as e:
            self._logger.error(f"Bad response: {str(e.response.text)}")
            return {
                "content": e.response.content,
                "headers": dict(e.response.headers),
                "status_code": e.response.status_code
            }
        
    async def get(
        self,
        endpoint: str,
        params: dict | None = None,
        timeout: float = 5.0,
        headers: dict = None
    ):
        headers = headers or {}

        try:
            response = await self._client.get(
                endpoint,
                params=params,
                timeout=timeout,
                headers=headers
            )

            response.raise_for_status()

            return {
                "content": response.content,
                "json": response.json() if "application/json" in response.headers.get("content-type", "") else None,
                "headers": dict(response.headers),
                "status_code": response.status_code
            }

        except httpx.RequestError as e:
            self._logger.error(f"Request failed: {str(e)}")
            return None

        except httpx.HTTPStatusError as e:
            self._logger.error(f"Bad response: {str(e.response.text)}")
            return {
                "content": e.response.content,
                "headers": dict(e.response.headers),
                "status_code": e.response.status_code
            }

    async def close(self) -> None:
        await self._client.aclose()