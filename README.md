# GitHub MCP

A tool-powered GitHub integration built with FastMCP for reading repositories, files, and directory contents via GitHub's API.

---

## 🛠 Installation

### ✅ Prerequisites

- Python 3.12+
- [`uv`](https://github.com/charliermarsh/uv) (a modern Python package manager)
- Docker _(optional — each service has its own Dockerfile)_

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd github-mcp
```

### 2. Configure Environment

```bash
cp .env.template .env
# Open .env and add your GitHub token and other required configs
```

### 3. Install Dependencies

```bash
uv sync
```

---

## 🚀 Running the Application

```bash
uv run -m server.main
```

The MCP server will start on:  
📍 http://localhost:8000/mcp

---

## ⚙️ Configuration Files

server has its own `.env.template`:

- `github-mcp/.env.template` → Copy to `.env` and edit with your configuration.

---

## Testing with MCP Inspector

### 1. Start Your Server with HTTP Transport

Ensure your server is running with the `streamable-http` transport:

```bash
uv run -m server.main
```

This will start your server at `http://localhost:8000/mcp`.

### 2. Launch MCP Inspector

Use the MCP Inspector to connect to your running server:

```bash
npx @modelcontextprotocol/inspector uv run -m server.main
```

This command will open the MCP Inspector interface in your browser.

### 3. Connect to Your Server

In the MCP Inspector interface:

- Select the appropriate transport (e.g., `streamable-http`)
- Enter the server URL: `http://localhost:8000/mcp`
- Click the **Connect** button

### 4. Test Tools and Resources

Once connected, you can:

- Navigate to the **Tools** tab to test available tools
- Use the **Resources** tab to inspect available resources
- Utilize the **Prompts** tab to test defined prompts

This interactive interface allows you to validate your server’s functionality and debug any issues.

---
