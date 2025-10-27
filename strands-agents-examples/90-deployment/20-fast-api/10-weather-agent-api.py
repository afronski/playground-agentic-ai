import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import PlainTextResponse, StreamingResponse
from strands import Agent, tool
from strands_tools import http_request

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Create a logger for our agent.
agentName = "10-weather-agent-api"
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

app = FastAPI(title="Weather API")

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
    super().__init__(
      system_prompt=self.__WEATHER_SYSTEM_PROMPT,
      tools=[http_request, self.ready_to_summarize],
      callback_handler=None
    )

class PromptRequest(BaseModel):
  prompt: str

@app.post('/weather')
async def get_weather(request: PromptRequest):
  prompt = request.prompt

  if not prompt:
    raise HTTPException(status_code=400, detail="No prompt provided")

  try:
    weather_agent = WeatherAgent()
    response = weather_agent(prompt)
    content = str(response)
    return PlainTextResponse(content=content)
  except Exception as exception:
    raise HTTPException(status_code=500, detail=str(exception))

async def run_weather_agent_and_stream_response(prompt: str):
  weather_agent = WeatherAgent()

  async for item in weather_agent.stream_async(prompt):
    if not weather_agent.is_summarizing:
      continue

    if "data" in item:
      yield item['data']

@app.post('/weather-streaming')
async def get_weather_streaming(request: PromptRequest):
  prompt = request.prompt

  if not prompt:
    raise HTTPException(status_code=400, detail="No prompt provided")

  try:
    return StreamingResponse(
      run_weather_agent_and_stream_response(prompt),
      media_type="text/plain"
    )
  except Exception as exception:
    raise HTTPException(status_code=500, detail=str(exception))
