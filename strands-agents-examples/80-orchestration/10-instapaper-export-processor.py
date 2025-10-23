import logging
from strands import Agent
from strands.models import BedrockModel
from strands.multiagent import Swarm
from strands_tools import file_read, http_request

# Create Strands SDK logger that logs to a file on a `DEBUG` level.
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
agentName = "10-instapaper-export-processor"

logger = logging.getLogger("strands")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)

logging.basicConfig(handlers=[fileHandler])

# Prepare `BedrockModel` objects with a specific model ID and region.
small_model = BedrockModel(
  model_id="eu.anthropic.claude-haiku-4-5-20251001-v1:0",
  region_name="eu-west-1",
  temperature=0.3
)

bigger_model = BedrockModel(
  model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
  region_name="eu-west-1",
  temperature=0.4
)

creative_model = BedrockModel(
  model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
  region_name="eu-west-1",
  temperature=0.75
)

# Create specialized agents.
loader = Agent(
  name="loader",
  model=small_model,
  tools=[file_read],
  system_prompt="""
  You are a data loader.

  You treat each line of a CSV file as a separate entry to analyze further down the chain. CSV file uses one type of
  separator per line. First line in the file is always a header, so do not count it as an entry.

  You are not analysing content of those entries, you are allowed just to parse file and return the results.
  """
)

researcher = Agent(
  name="researcher",
  model=bigger_model,
  tools=[http_request],
  system_prompt="""
  You are a research specialist, that analyzes provided data. You specialise in software engineering, and you want to
  focus specifically in deeply analysing a single article according to the following criteria:

  - Article should be useful for senior software engineer, either as a reminder or something new to learn.
  - Article is not older than 3 years, or if it is - it is considered a state of the art.
  - Articles are not news-like or they are not aging easily, in terms of usefulness for senior software engineers.
  - My favourite articles are about databases, distributed systems, and cloud computing.

  Always include a title, author, creation date, key takeaways as bullet points, and a summary of the article that
  is not longer than 500 words. You are not performing deep analysis, but rather a general research on an article.
  Deeper research and insights creation are handed-off to other agents further down the chain.
  """
)

thinker = Agent(
  name="thinker",
  model=creative_model,
  system_prompt="""
  Your job is to find common patterns in the results provided by researching team.

  We are especially interested in finding creative and new connections between analysed articles and extracting
  insights that could be relevant for upskilling a senior software engineer or will be helpful in his daily job
  related to designing and implementing distributed systems in the public cloud.

  Be concise and precise in your answers, do not include code, diagrams, focus only on creative insights based on
  the provided summaries.
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
  Do a research on first 3 articles, and result of that research should be deeply
  analysed by the thinker agent.
  """
)

print("\n")
print("-" * 120)
print("-" * 120)
print("-" * 120)

print(f"ℹ️ Status: {result.status}")

for node in result.node_history:
  print(f"ℹ️ Agent: {node.node_id}")
#
# researchers_result = result.results["researcher"].result
# print(f"ℹ️ Researchers: {researchers_result}")

print(f"ℹ️ Total iterations: {result.execution_count}")
print(f"ℹ️ Execution time: {result.execution_time}ms")
print(f"ℹ️ Token usage: {result.accumulated_usage}")
