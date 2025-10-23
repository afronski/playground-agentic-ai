import logging
import os
from mcp import StdioServerParameters, stdio_client
from strands import Agent
from strands.tools.mcp import MCPClient

# Enables Strands `debug` log level and log it to a file.
agentName = "10-aws-mcp-servers"
logging.getLogger("strands").setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))

# Sets the logging format and streams logs to stderr.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Connect to an MCP server using `stdio` transport.
# noinspection PyTypeChecker
stdio_mcp_client = MCPClient(
  lambda: stdio_client(
    StdioServerParameters(
      command="uvx",
      args=["awslabs.aws-pricing-mcp-server@latest"],
      env={
        "AWS_PROFILE": os.environ.get("AWS_PROFILE", "default")
      }
    )
  )
)

# Get the tools from the MCP server and create an agent with them.
with stdio_mcp_client:
  tools = stdio_mcp_client.list_tools_sync()
  agent = Agent(tools=tools)

  response = agent("""
  Calculate the cost of monthly usage 24/7 for 2 machines with two GPUs each in Frankfurt region.
  Be concise and print specific family and instance types alongside the cost.
  """)
