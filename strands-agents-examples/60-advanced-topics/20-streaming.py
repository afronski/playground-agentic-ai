import logging
from fastapi import FastAPI
from fastapi.responses import Response,StreamingResponse
from pydantic import BaseModel
from strands import Agent
from strands_tools import calculator, http_request

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Create a logger for our agent.
agentName = "20-streaming"
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

app = FastAPI()

class PromptRequest(BaseModel):
  prompt: str

@app.post("/streaming")
async def stream_response(request: PromptRequest):
  async def generate():
    agent = Agent(
      tools=[calculator, http_request],
      callback_handler=None
    )

    try:
      async for event in agent.stream_async(request.prompt):
        if "data" in event:
          yield event["data"]
    except Exception as e:
      yield f"Error: {str(e)}"

  return StreamingResponse(
    generate(),
    media_type="text/plain"
  )

@app.post("/non-streaming")
def stream_response(request: PromptRequest):
  agent = Agent(
    tools=[calculator, http_request],
    callback_handler=None
  )

  result = agent(request.prompt)

  return Response(
    str(result),
    media_type="text/plain",
  )
