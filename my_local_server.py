# file: my_http_mcp_server.py

from fastapi import FastAPI
import uvicorn
from mcp.server.fastapi import FastAPIMCPServer

# Create a FastAPI app
app = FastAPI()

# Wrap it in an MCP server
server = FastAPIMCPServer("local-example", app=app)

# Define a simple MCP tool
@server.tool("say_hello", description="Greets the user")
async def say_hello(name: str) -> str:
    return f"Hello, {name}! This response came from your local MCP server."

if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn on localhost:8000
    uvicorn.run(app, host="127.0.0.1", port=8000)
