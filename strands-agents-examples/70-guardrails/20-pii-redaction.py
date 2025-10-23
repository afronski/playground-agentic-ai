import logging
from strands import Agent
from llm_guard.vault import Vault
from llm_guard.input_scanners import Anonymize
from llm_guard.input_scanners.anonymize_helpers import BERT_LARGE_NER_CONF
from langfuse import Langfuse, observe

# Create Strands SDK logger that logs to a file on a `DEBUG` level.
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
agentName = "20-pii-redaction"

logger = logging.getLogger("strands")
logger.setLevel(logging.DEBUG)

fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)

logging.basicConfig(handlers=[fileHandler])

vault = Vault()

def create_anonymize_scanner():
  return Anonymize(vault, recognizer_conf=BERT_LARGE_NER_CONF, language="en")

def masking_function(data, **kwargs):
  if isinstance(data, str):
    scanner = create_anonymize_scanner()
    sanitized_data, _, _ = scanner.scan(data)
    return sanitized_data
  elif isinstance(data, dict):
    return {k: masking_function(v) for k, v in data.items()}
  elif isinstance(data, list):
    return [masking_function(item) for item in data]
  return data

# noinspection PyTypeChecker
langfuse = Langfuse(mask=masking_function)

class CustomerSupportAgent:
  def __init__(self):
    self.agent = Agent(
      system_prompt="You are a helpful customer service agent. Respond professionally to customer inquiries."
    )

  @observe
  def process_sanitized_message(self, sanitized_payload):
    sanitized_content = sanitized_payload.get("prompt", "empty input")

    conversation = f"Customer: {sanitized_content}"
    print(f"⬅️️ {conversation}")

    response = self.agent(conversation)
    return response


def process():
  support_agent = CustomerSupportAgent()
  scanner = create_anonymize_scanner()

  raw_payload = {
    "prompt": """
      Hi, I'm Jonny Test. My phone number is 123-456-7890 and my email is john@example.com.
      I need help with my order #123456789.
      """
  }

  sanitized_prompt, _, _ = scanner.scan(raw_payload["prompt"])
  sanitized_payload = {"prompt": sanitized_prompt}

  response = support_agent.process_sanitized_message(sanitized_payload)

  print(f"\n➡️ Response: {response}")
  langfuse.flush()

if __name__ == "__main__":
  process()
