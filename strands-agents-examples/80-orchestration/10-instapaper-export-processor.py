import logging
from strands import Agent
from strands.models import BedrockModel
from strands.multiagent import Swarm
from strands_tools import file_read, http_request

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# TODO: Each agent has its own file.
# TODO: Strands logs are in separate file.
# TODO: I think it should be a workflow, not swarm to make it more predictable.
# TODO: How to do fan-out here?

# Create a logger for our agent.
agentName = "10-instapaper-export-processor"
agentLogger = logging.getLogger(agentName)
agentLogger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)
agentLogger.addHandler(fileHandler)

# Sets the logging format and streams logs to a file.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Create a BedrockModel with a specific model ID and region.
small_model = BedrockModel(
  model_id="anthropic.claude-3-haiku-20240307-v1:0",
  region_name="eu-central-1",
  temperature=0.3
)

big_model = BedrockModel(
  model_id="anthropic.claude-3-5-sonnet-20240620-v1:0",
  region_name="eu-central-1",
  temperature=0.65
)

# Create specialized agents.
loader = Agent(
  name="loader",
  model=small_model,
  tools=[file_read],
  system_prompt="""
  You are a data loader. You treat each line of a CSV file as a separate entry to analyze further down the chain.
  CSV file uses one type of separator per line. First line in the file is always a header, so do not count it as
  an entry. You are not analysing content of those entries, you are allowed just to parse file and return the results.
  """
)

researcher = Agent(
  name="researcher",
  model=big_model,
  tools=[http_request],
  system_prompt="""
  You are a research specialist, that analyzes provided data. You specialise in software engineering, and you want to
  focus specifically in deeply analysing a single article according to the following criteria:
  - Article should be useful for senior software engineer, either as a reminder or something new to learn.
  - Article is not older than 3 years, or if it is - it is considered a state of the art.
  - Articles are not news-like or they are not aging easily, in terms of usefulness for senior software engineers.
  - My favourite articles are about databases, distributed systems, and cloud computing.
  """
)

thinker = Agent(
  name="thinker",
  model=big_model,
  system_prompt="""
  Your job is to find common patterns in the results provided by researching team. We are especially interested in
  finding creative and new connections between analysed articles and extracting insights that could be relevant for
  upskilling a senior software engineer or will be helpful in his daily job related to designing and implementing
  distributed systems in the public cloud.
  """
)

# Create a swarm with these agents, starting with the extractor.
swarm = Swarm(
  [loader, researcher, thinker],
  entry_point=loader,  # Start with the extractor
  max_handoffs=5,
  max_iterations=20,
  execution_timeout=900.0,  # 15 minutes
  node_timeout=300.0,       # 5 minutes per agent
  repetitive_handoff_detection_window=8,  # There must be >= 3 unique agents in the last 8 handoffs
  repetitive_handoff_min_unique_agents=3
)

# Execute the swarm on a task.
result = swarm(
  """
  File is stored in a local file system, under path: ./assets/instapaper-export.csv.
  For now do research on only first 3 entries, and based on that research - provide me
  a deep analysis with insights about those articles.
  """
)

print("*" * 100)
print("*" * 100)
print("*" * 100)

print(f"ℹ️ Status: {result.status}")

for node in result.node_history:
  print(f"ℹ️ Agent: {node.node_id}")

researchers_result = result.results["researcher"].result
print(f"ℹ️ Researchers: {researchers_result}")

print(f"ℹ️ Total iterations: {result.execution_count}")
print(f"ℹ️ Execution time: {result.execution_time}ms")
print(f"ℹ️ Token usage: {result.accumulated_usage}")
