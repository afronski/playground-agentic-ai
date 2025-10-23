from fastmcp import FastMCP

mcp = FastMCP("Greet MCP Server")

@mcp.tool(description="Greeting service based on the provided name")
def greet(name: str) -> str:
  return f"Hello, {name}!"

if __name__ == "__main__":
  mcp.run(transport="http", port=8000)
