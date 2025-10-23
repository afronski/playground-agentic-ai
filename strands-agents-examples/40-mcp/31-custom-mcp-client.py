import logging
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient

# Enables Strands `debug` log level and log it to a file.
agentName = "31-custom-mcp-client"
logging.getLogger("strands").setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))

# Sets the logging format and streams logs to a file.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Connect to an MCP server using streamable HTTP transport.
streamable_http_mcp_client = MCPClient(
  lambda: streamablehttp_client("http://localhost:8000/mcp")
)

# Get the tools from the MCP server and create an agent with them.
with streamable_http_mcp_client:
  tools = streamable_http_mcp_client.list_tools_sync()
  agent = Agent(tools=tools)

  print(agent.tool.greet(name="Strands"))
