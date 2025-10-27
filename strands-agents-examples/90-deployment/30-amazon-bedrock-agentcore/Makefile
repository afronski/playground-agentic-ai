all: deploy-agentcore start-agentcore call-agentcore

run-local:
	python 10-weather-agent-api.py

ping-local:
	 curl http://localhost:8080/ping                                                                \
        -X "GET"

call-local:
	 curl http://localhost:8080/invocations                                                         \
        -X "POST"                                                                                 \
        -H "Content-Type: application/json"                                                       \
	      -d '{"prompt": "What is the weather for Łódź?"}'

deploy-agentcore:
	agentcore configure --entrypoint 10-weather-agent-api.py --name weather_agent --requirements-file ./requirements.txt

start-agentcore:
	agentcore launch

call-agentcore:
	agentcore invoke '{"prompt": "What is the weather for Łódź?"}'

undeploy-agentcore:
	agentcore destroy
