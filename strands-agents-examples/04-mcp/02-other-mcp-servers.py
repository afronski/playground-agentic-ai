import logging
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient

# Enables Strands `debug` log level and log it to a file.
agentName = "02-other-mcp-servers"
logging.getLogger("strands").setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))

# Sets the logging format and streams logs to stderr.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Connect to an MCP server using `stdio` transport.
stdio_mcp_client = MCPClient(
  lambda: stdio_client(
    StdioServerParameters(
      command="npx",
      args=["-y", "chrome-devtools-mcp@latest"]
    )
  )
)

# Get the tools from the MCP server and create an agent with them.
with stdio_mcp_client:
  tools = stdio_mcp_client.list_tools_sync()
  agent = Agent(tools=tools)

  response = agent("""
  Open https://strandsagents.com website and perform a Lighthouse analysis.
  Be concise in the results, and highlight top 3 good things and top 3 bad things.
  """)
