import logging
from pydantic import BaseModel
from strands import Agent

# Enables Strands `debug` log level.
logging.getLogger("strands").setLevel(logging.DEBUG)

# Create a logger for our agent.
agentName = "12-structured-output"
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

class PersonInfo(BaseModel):
  name: str
  years_of_experience: int
  occupation: str

with open("assets/CV.pdf", "rb") as fp:
  document_bytes = fp.read()

agent = Agent()

# noinspection PyTypeChecker
result = agent(
  [
    {"text": "Please process this application."},
    {
      "document": {
        "format": "pdf",
        "name": "application",
        "source": {
          "bytes": document_bytes,
        },
      },
    },
  ],
  structured_output_model=PersonInfo
)

result = result.structured_output

print(f"Name: {result.name}")
print(f"Years of Experience: {result.years_of_experience}")
print(f"Job: {result.occupation}")
