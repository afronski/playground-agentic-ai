import logging
from ddgs import DDGS
from ddgs.exceptions import DDGSException, RatelimitException
from strands import Agent, tool
from strands.models.ollama import OllamaModel

# Enables Strands `debug` log level and log it to a file.
agentName = "10-recipe-bot"
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

# Use Polish model via ollama (Bielik 11B v2.3).
ollama_model = OllamaModel(
  host="http://localhost:11434",
  model_id="SpeakLeash/bielik-11b-v2.3-instruct:Q8_0"
)

# Create a recipe assistant agent.
recipe_agent = Agent(
  system_prompt="""
    Jesteś pomocnym asystentem 'RecipeBot' do wyszukiwania przepisów kulinarnych.
    Pomagasz użytkownikom znajdować przepisy na podstawie składników lub nazwy potrawy, którą użytkownik podał.
    Po tym jak użytkownik poda składniki lub nazwę potrawy, to przygotuj przepis na podstawie podanych danych.
    """,
  model=ollama_model,
  # Unfortunately, Bielik at this time does not support tools calling via Ollama. :(
  # tools=[websearch],
)

if __name__ == "__main__":
  print("\n👨‍🍳 RecipeBot: Co chcesz ugotować dzisiaj? Wpisz 'exit' aby wyjść.\n")

  # Run the agent in a loop for interactive conversation.
  while True:
    user_input = input("\nYou > ")

    if user_input.lower() == "exit":
      print("Udanego Gotowania! 🍽️")
      break

    response = recipe_agent(user_input)
    print(f"\nRecipeBot > {response}")
