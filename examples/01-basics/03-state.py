import logging
from pprint import pprint
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from strands.types.content import Message, ContentBlock

# Enables Strands debug log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Sets the logging format and streams logs to stderr.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[logging.StreamHandler()]
)

# Create a conversation manager with a custom window size.
# By default, SlidingWindowConversationManager is used even if not specified.
conversation_manager = SlidingWindowConversationManager(
  window_size=10,  # Maximum number of message pairs to keep.
)

# Create an agent with initial messages.
agent = Agent(
  messages=[
    Message(role="user", content=[ContentBlock(text="Hello, my name is Strands!")]),
    Message(role="user", content=[ContentBlock(text="Hi there! How can I help you today?")]),
  ],
  conversation_manager=conversation_manager
)

# Continue the conversation
agent("What's my name?")

print("\n➡️  Messages exchanged so far:")
pprint(agent.messages)
