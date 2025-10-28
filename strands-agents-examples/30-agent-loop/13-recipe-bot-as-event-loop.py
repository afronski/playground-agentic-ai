import logging
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands import Agent, tool

# Enables Strands `debug` log level and log it to a file.
agentName = "13-recipe-bot-as-event-loop"
logging.getLogger("strands").setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))

# Sets the logging format and streams logs to a file.
logging.basicConfig(
  format="%(levelname)s | %(name)s | %(message)s",
  handlers=[fileHandler]
)

# Define a websearch tool via DuckDuckGo Search API.
@tool
def websearch(keywords: str, region: str = "us-en", max_results: int | None = None) -> str:
  """Search the web to get updated information.
  Args:
      keywords (str): The search query keywords.
      region (str): The search region: wt-wt, us-en, uk-en, ru-ru, etc..
      max_results (int | None): The maximum number of results to return.
  Returns:
      List of dictionaries with search results.
  """
  try:
    results = DDGS().text(keywords, region=region, max_results=max_results)
    return results if results else "No results found."
  except RatelimitException:
    return "RatelimitException: Please try again after a short delay."
  except DDGSException as d:
    return f"DuckDuckGoSearchException: {d}"
  except Exception as e:
    return f"Exception: {e}"

# Event loop callback with detailed logging.
def event_loop_tracker(**kwargs):
  if kwargs.get("init_event_loop", False):
    print("🔄 Event loop initialized")
  elif kwargs.get("start_event_loop", False):
    print("▶️ Event loop cycle starting")
  elif "message" in kwargs:
    print(f"📬 New message created: {kwargs['message']['role']}")
  elif kwargs.get("complete", False):
    print("✅ Cycle completed")
  elif kwargs.get("force_stop", False):
    print(f"🛑 Event loop force-stopped: {kwargs.get('force_stop_reason', 'unknown reason')}")

  if "current_tool_use" in kwargs and kwargs["current_tool_use"].get("name"):
    tool_name = kwargs["current_tool_use"]["name"]
    print(f"🔧 Using tool: {tool_name}")

  if "data" in kwargs:
    data_snippet = kwargs["data"][:20] + ("..." if len(kwargs["data"]) > 20 else "")
    print(f"📟 Text: {data_snippet}")

# Create a recipe assistant agent.
recipe_agent = Agent(
  system_prompt="""
    You are RecipeBot, a helpful cooking assistant.
    Help users find recipes based on ingredients and answer cooking questions.
    Use the websearch tool to find recipes when users mention ingredients or to look up cooking information.
    """,
  tools=[websearch],
  callback_handler=event_loop_tracker
)

if __name__ == "__main__":
  print("\n👨‍🍳 RecipeBot: Ask me about recipes or cooking! Type 'exit' to quit.\n")

  # Run the agent in a loop for interactive conversation.
  while True:
    user_input = input("\nYou > ")

    if user_input is None or user_input == "":
      print("You have to provide input to continue.")
      continue

    if user_input.lower() == "exit":
      print("Happy cooking! 🍽️")
      break

    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
