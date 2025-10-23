import logging
import uuid
import boto3
from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.models import BedrockModel
from strands.session.s3_session_manager import S3SessionManager

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Create a logger for our agent.
agentName = "30-agent-with-persistent-memory"
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

# Custom system prompt for technical conversations.
custom_system_prompt = """
You are summarizing a technical conversation. Create a concise bullet-point summary that:
- Focuses on code changes, architectural decisions, and technical solutions
- Preserves specific function names, file paths, and configuration details
- Omits conversational elements and focuses on actionable information
- Uses technical terminology appropriate for software development

Format as bullet points without conversational language.
"""

# Create a cheaper, faster model for summarization tasks.
summarization_model = BedrockModel(
  model_id="anthropic.claude-3-haiku-20240307-v1:0",  # More cost-effective for summarization
  max_tokens=1000,
  region_name="eu-west-1",
  temperature=0.3,
)
custom_summarization_agent = Agent(
  system_prompt=custom_system_prompt,
  model=summarization_model
)

# Create a summarizing conversation manager with our custom system prompt and summarization agent.
conversation_manager = SummarizingConversationManager(
  summary_ratio=0.4,
  preserve_recent_messages=8,
  summarization_agent=custom_summarization_agent
)

# Create a session manager that stores data in S3 based on the user's session ID.
boto_session = boto3.Session(region_name="eu-west-1")

session_manager = S3SessionManager(
  session_id=uuid.uuid4().hex,   # ... or use sessions ID about AWS Lambda: `3c23593321cf4c68a6ddd4197f4c0b13`
  bucket="wg-playground-agentic-ai",
  prefix="production",
  boto_session=boto_session
)

agent = Agent(
  session_manager=session_manager,
  conversation_manager=conversation_manager
)

agent("Explain to me how to create a new AWS Lambda function.")
