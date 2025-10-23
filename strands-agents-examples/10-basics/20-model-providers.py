import logging
from strands import Agent
from strands.models import BedrockModel

# Enables Strands debug log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[logging.StreamHandler()]
)

# Create a BedrockModel with a specific model ID and region.
bedrock_model = BedrockModel(
  model_id="openai.gpt-oss-120b-1:0",
  region_name="eu-central-1",
  temperature=0.3,
)

agent = Agent(model=bedrock_model)

print(f"⚙️ Detailed model provider configuration: {agent.model.config}")

agent("Hello! Who are you?")
