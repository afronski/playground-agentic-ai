import logging
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools.http_request import http_request

# Enables Strands `debug` log level and log it to a specific file.
agentName = "10-weather-agent-api"

strandsLogger = logging.getLogger("strands")
strandsLogger.setLevel(logging.DEBUG)

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
fileHandler = logging.FileHandler("{0}/{1}.log".format("logs", agentName))
fileHandler.setFormatter(logFormatter)

strandsLogger.handlers.clear()
strandsLogger.addHandler(fileHandler)

app = BedrockAgentCoreApp()

class WeatherAgent(Agent):
  __WEATHER_SYSTEM_PROMPT = """You are a weather assistant with HTTP capabilities. You can:

  1. Make HTTP requests to the OpenMeteo API
  2. Process and display weather forecast data
  3. Provide weather information for locations all around the world, with emphasis on Poland

  When retrieving weather information:
  1. First get the coordinates or grid information using https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
  2. Then use the returned forecast URL to get the actual forecast

  When displaying responses:
  - Format weather data in a human-readable way
  - Highlight important information like temperature, precipitation, and alerts
  - Handle errors appropriately
  - Don't ask follow-up questions

  Always explain the weather conditions clearly and provide context for the forecast.

  At the point where tools are done being invoked and a summary can be presented to the user,
  invoke the ready_to_summarize tool and then continue with the summary.
  """

  is_summarizing = False

  @tool
  def ready_to_summarize(self):
    self.is_summarizing = True
    return "Ok - continue providing the summary!"

  def __init__(self):
    model = BedrockModel(
      model_id="arn:aws:bedrock:eu-west-1:641421169031:inference-profile/eu.amazon.nova-pro-v1:0",
      region_name="eu-west-1",
      temperature=0.3
    )

    super().__init__(
      system_prompt=self.__WEATHER_SYSTEM_PROMPT,
      model=model,
      tools=[http_request, self.ready_to_summarize],
      callback_handler=None
    )

agent = WeatherAgent()

@app.entrypoint
async def agent_invocation(payload):
  user_message = payload.get(
    "prompt", "No prompt found in input, please guide customer to create a json payload with prompt key"
  )
  response = agent(user_message)
  return str(response)

if __name__ == "__main__":
  app.run()
