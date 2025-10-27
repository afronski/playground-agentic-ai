import logging
import os
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request
from typing import Dict, Any
from pythonjsonlogger.json import JsonFormatter
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import correlation_paths

# Enables structured logging for Powertools on a `debug` level.
logger = Logger(service="APP")
logger.setLevel(os.getenv("POWERTOOLS_LOG_LEVEL", "DEBUG"))

# ... and the same for Strands Agents logging.
strandsLogger = logging.getLogger("strands")
strandsLogger.setLevel(logging.DEBUG)
strandsLogHandler = logging.StreamHandler()
strandsLogFormatter = JsonFormatter(fmt="%(asctime)s %(levelname)s %(name)s %(message)s")
strandsLogHandler.setFormatter(strandsLogFormatter)
strandsLogger.handlers.clear()
strandsLogger.addHandler(strandsLogHandler)

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
      model_id="eu.anthropic.claude-sonnet-4-5-20250929-v1:0",
      region_name="eu-west-1",
      temperature=0.3
    )

    super().__init__(
      system_prompt=self.__WEATHER_SYSTEM_PROMPT,
      model=model,
      tools=[http_request, self.ready_to_summarize]
    )

@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST, log_event=True)
def handler(event: Dict[str, Any], _context) -> str:
  weather_agent = WeatherAgent()

  response = weather_agent(event.get('prompt'))
  return str(response)
