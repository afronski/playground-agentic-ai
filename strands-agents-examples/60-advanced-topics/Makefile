all: streaming-server

streaming-server:
	fastapi dev 20-streaming.py

non-streaming-call:
	 curl http://localhost:8000/non-streaming                                                       \
        -X "POST"                                                                                 \
        -H "Content-Type: application/json"                                                       \
	      -d '{"prompt": "Write me a bedtime story about a cat that is 4000 characters long."}'

streaming-call:
	 curl http://localhost:8000/streaming                                                           \
        -X "POST"                                                                                 \
        -H "Content-Type: application/json"                                                       \
	      -d '{"prompt": "Write me a bedtime story about a cat that is 4000 characters long."}'
