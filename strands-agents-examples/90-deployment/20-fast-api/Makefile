all: build-image run-container

run-local:
	fastapi dev 10-weather-agent-api.py

build-image:
	finch build -t strands-agents-examples/fastapi-image .

run-container:
	finch run --rm                                                                            \
            -it                                                                             \
					  -p 8000:8000                                                                    \
						--env-file .env                                                                 \
						strands-agents-examples/fastapi-image

non-streaming-call:
	 curl http://localhost:8000/weather                                                       \
        -X "POST"                                                                           \
        -H "Content-Type: application/json"                                                 \
	      -d '{"prompt": "What is the weather for Łódź?"}'

streaming-call:
	 curl http://localhost:8000/weather-streaming                                             \
        -X "POST"                                                                           \
        -H "Content-Type: application/json"                                                 \
	      -d '{"prompt": "What is the weather for Łódź?"}'
