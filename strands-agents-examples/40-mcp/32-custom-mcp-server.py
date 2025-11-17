from dataclasses import dataclass
from fastmcp import FastMCP, Context

mcp = FastMCP("Greet MCP Server")

@dataclass
class UserInfo:
  name: str

@mcp.tool(description="Greeting service based on the elicited name")
async def greet(ctx: Context) -> str:
  result = await ctx.elicit(
    message="What's your name?",
    response_type=UserInfo
  )

  if result.action == "accept":
    user = result.data
    return f"Hello {user.name}!"
  elif result.action == "decline":
    return "Name not provided"
  else:
    return "Operation cancelled"

if __name__ == "__main__":
  mcp.run(transport="http", port=8000)
