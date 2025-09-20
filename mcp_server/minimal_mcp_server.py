"""
Minimal Model Context Protocol (MCP) server
==========================================

This script demonstrates the smallest possible MCP server you can run locally
to expose a single tool. It uses the `fastmcp` package, which provides a
high‑level, Pythonic interface for building MCP servers and clients. According
to the FastMCP documentation, you can install the library with pip by
running `pip install fastmcp`【532126726416560†L25-L34】. The same docs show
that creating a server involves instantiating `FastMCP`, decorating your
functions with `@mcp.tool`, and calling `mcp.run()`【532126726416560†L141-L154】.

This example defines a single tool called `echo` that simply returns
whatever text you pass to it. Because MCP automatically generates schemas
from type hints and docstrings, the function signature and docstring
describe the tool for clients.

Usage
-----

1. Install the `fastmcp` package (Python 3.10+ is required):

   ```sh
   pip install fastmcp
   ```

2. Save this file as `minimal_mcp_server.py` and run it with Python:

   ```sh
   python minimal_mcp_server.py
   ```

   By default, `mcp.run()` will choose an available transport and port. To
   explicitly serve HTTP on port 8000, you can call `mcp.run(host="0.0.0.0",
   port=8000, transport="streamable-http")` instead【943578069623670†L109-L119】.

After starting the server, you can connect to it with an MCP client (like
ChatGPT Desktop, Claude Desktop or any other compatible client) by
configuring the client to point at `http://localhost:8000/mcp` (or the
address/port you choose). When the client lists available tools, you’ll
see the `echo` tool exposed.
"""

from fastmcp import FastMCP

# Create an MCP server instance with a human‑friendly name.  The name is
# surfaced to clients when they connect.  You can choose any string here.
mcp = FastMCP(name="Minimal Echo Server")

@mcp.tool
def echo(text: str) -> str:
    """Echo the input text back to the caller.

    Parameters
    ----------
    text: str
        The text you want the server to return.

    Returns
    -------
    str
        The same text you passed in.
    """
    return text

if __name__ == "__main__":
    # Start the MCP server.  Without arguments, this chooses sensible defaults
    # for transport and port.  To make the server accessible over HTTP on
    # localhost:8000, uncomment the line below and provide the host, port,
    # and transport explicitly.
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path="/mcp")
    mcp.run()
