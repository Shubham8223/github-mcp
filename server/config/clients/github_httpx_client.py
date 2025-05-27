import httpx
from server.config.config import Settings

class GitHubClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"token {Settings.GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "GitHub-MCP-Server/1.0"
            },
            timeout=10.0
        )

    async def get(self, url: str, params: dict = None) -> dict:
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise Exception(f"GitHub API request failed: {e}")
