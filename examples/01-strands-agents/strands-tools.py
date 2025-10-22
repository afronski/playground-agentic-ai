import logging
from strands import Agent
from strands_tools import shell

# Enables Strands debug log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Create a logger for our agent.
agentName = "strands-tools"
agentLogger = logging.getLogger(agentName)
agentLogger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)
agentLogger.addHandler(fileHandler)

# Define a simple callback handler that logs instead of printing.
tool_use_ids = []
def callback_handler(**kwargs):
  if "data" in kwargs:
    # Log the streamed data chunks.
    agentLogger.info(kwargs["data"])
  elif "current_tool_use" in kwargs:
    tool = kwargs["current_tool_use"]
    if tool["toolUseId"] not in tool_use_ids:
      # Log the tool use.
      agentLogger.info(f"\n[Using tool: {tool.get('name')}]")
      tool_use_ids.append(tool["toolUseId"])

# Create an agent with the callback handler.
agent = Agent(
  tools=[shell],
  callback_handler=callback_handler
)

result = agent("What operating system am I using?")

print(result.message)
