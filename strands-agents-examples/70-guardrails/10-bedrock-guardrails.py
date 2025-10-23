import json
import logging
from strands import Agent
from strands.models import BedrockModel

# Create Strands SDK logger that logs to a file on a `DEBUG` level.
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
agentName = "10-bedrock-guardrails"

logger = logging.getLogger("strands")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)

logging.basicConfig(handlers=[fileHandler])

# Create a Bedrock model with guardrail configuration.
bedrock_model = BedrockModel(
  model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
  region_name="eu-west-1",

  guardrail_id="oi78mrq3s4rb",              # Your Bedrock guardrail ID
  guardrail_version="1",                    # Guardrail version
  guardrail_trace="enabled",                # Enable trace info for debugging
)

# Create an agent with the guardrail-protected model.
agent = Agent(
  system_prompt="You are a helpful assistant.",
  model=bedrock_model,
)

# Use the protected agent for conversations.
response = agent("I own 200k USD. Should I invest in crypto?")

# Handle potential guardrail interventions.
if response.stop_reason == "guardrail_intervened":
  print("\nContent was blocked by guardrails, conversation context overwritten!")

print(f"Conversation: {json.dumps(agent.messages, indent=4)}")
