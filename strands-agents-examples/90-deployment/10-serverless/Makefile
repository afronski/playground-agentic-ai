all: build-lambda deploy-lambda run-lambda

build-lambda:
	cd 10-weather-agent-api && sam build --use-container

deploy-lambda:
	cd 10-weather-agent-api && sam deploy

run-local:
	cd 10-weather-agent-api && sam local invoke WeatherAgentFunction -e ./events/prompt.json

run-lambda:
	aws lambda invoke --function-name WeatherAgentFunction 				\
    --region eu-west-1  																				\
    --cli-binary-format raw-in-base64-out 											\
    --payload file://./10-weather-agent-api/events/prompt.json 	\
    /dev/stdout                                                 \
  | jq -r '.'
