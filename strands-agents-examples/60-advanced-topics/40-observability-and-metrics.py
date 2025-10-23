import logging
from strands import Agent
from strands_tools import shell
from pprint import pprint

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Enables Strands `debug` log level and log it to a file.
agentName = "40-observability-and-metrics"
logging.getLogger("strands").setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))

# Sets the logging format and streams logs to a file.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Create an agent with the callback handler.
agent = Agent(tools=[shell])

agent("What operating system am I using?")
agent("What version of brew is installed?")
agent("How many brew packages do I have in the system?")
agent("How many asdf plugins do I have installed?")

# Print the agent usage details:
pprint(agent.event_loop_metrics.get_summary())
