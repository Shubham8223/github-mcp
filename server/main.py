import os
import base64
from typing import Optional, List, Dict, Any
from fastmcp import FastMCP
from server.config.config import settings
from server.config.clients.github_httpx_client import GitHubClient

GITHUB_API_BASE = settings.GITHUB_API_BASE_URL

client = GitHubClient()

mcp = FastMCP("GitHub MCP Server")



@mcp.tool()
async def list_repositories(
    owner: str,
    repo_type: str = "all",
    sort: str = "updated",
    per_page: int = 30,
    page: int = 1
) -> List[Dict[str, Any]]:
    """List GitHub repositories for a user or organization."""
    user_url = f"{GITHUB_API_BASE}/users/{owner}"
    user_data = await client.get(user_url)
    repos_url = f"{GITHUB_API_BASE}/users/{owner}/repos" if user_data.get("type") != "Organization" else f"{GITHUB_API_BASE}/orgs/{owner}/repos"
    
    params = {
        "type": repo_type,
        "sort": sort,
        "per_page": per_page,
        "page": page
    }
    repos_data = await client.get(repos_url, params=params)
    
    return [{
        "name": repo["name"],
        "full_name": repo["full_name"],
        "description": repo.get("description", ""),
        "private": repo["private"],
        "html_url": repo["html_url"],
        "clone_url": repo["clone_url"],
        "ssh_url": repo["ssh_url"],
        "default_branch": repo["default_branch"],
        "language": repo.get("language"),
        "size": repo["size"],
        "stargazers_count": repo["stargazers_count"],
        "watchers_count": repo["watchers_count"],
        "forks_count": repo["forks_count"],
        "created_at": repo["created_at"],
        "updated_at": repo["updated_at"],
        "pushed_at": repo["pushed_at"]
    } for repo in repos_data]

@mcp.tool()
async def read_file_content(
    owner: str,
    repo: str,
    path: str,
    branch: str = "main"
) -> Dict[str, Any]:
    """Read file content from a GitHub repository."""
    contents_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": branch} if branch != "main" else None
    file_data = await client.get(contents_url, params=params)
    
    if file_data.get("type") != "file":
        raise Exception(f"Path '{path}' is not a file")
    
    content_encoded = file_data.get("content", "")
    try:
        content_decoded = base64.b64decode(content_encoded).decode('utf-8')
    except UnicodeDecodeError:
        content_decoded = f"[Binary file - base64 content]: {content_encoded}"
    
    return {
        "name": file_data["name"],
        "path": file_data["path"],
        "size": file_data["size"],
        "content": content_decoded,
        "encoding": file_data.get("encoding", "base64"),
        "sha": file_data["sha"],
        "html_url": file_data.get("html_url", ""),
        "download_url": file_data.get("download_url", "")
    }

@mcp.tool()
async def list_directory_contents(
    owner: str,
    repo: str,
    path: str = "",
    branch: str = "main"
) -> List[Dict[str, Any]]:
    """List contents of a directory in a GitHub repository."""
    contents_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": branch} if branch != "main" else None
    contents_data = await client.get(contents_url, params=params)
    
    if isinstance(contents_data, dict):
        contents_data = [contents_data]
    
    return [{
        "name": item["name"],
        "path": item["path"],
        "type": item["type"],
        "size": item.get("size", 0),
        "sha": item["sha"],
        "html_url": item.get("html_url", ""),
        "download_url": item.get("download_url", "")
    } for item in contents_data]

@mcp.tool()
async def list_all_files(
    owner: str,
    repo: str,
    branch: str = "main",
    file_extensions: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """List all files in a GitHub repository using Git Trees API."""
    branch_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/branches/{branch}"
    branch_data = await client.get(branch_url)
    tree_sha = branch_data["commit"]["sha"]
    
    tree_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/git/trees/{tree_sha}?recursive=1"
    tree_data = await client.get(tree_url)
    
    files = []
    for item in tree_data.get("tree", []):
        if item["type"] == "blob":
            file_path = item["path"]
            if file_extensions:
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext not in [ext.lower() for ext in file_extensions]:
                    continue
            files.append({
                "path": file_path,
                "name": os.path.basename(file_path),
                "type": "file",
                "size": item.get("size", 0),
                "sha": item["sha"],
                "url": item.get("url", ""),
                "directory": os.path.dirname(file_path) or "/"
            })
    
    return files

@mcp.resource("resource://github/docs")
def github_docs_resource() -> str:
    """Provides a link to the GitHub REST API documentation."""
    return "https://docs.github.com/en/rest"

@mcp.prompt()
def inspect_repository_prompt(owner: str, repo: str):
    """Generates a prompt to inspect a GitHub repository."""
    return f"Please inspect the repository '{owner}/{repo}' and provide an overview of its structure and contents."


if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        print(f"An error occurred while running the server: {str(e)}")
        raise e
