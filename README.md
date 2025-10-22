# `playground-agentic-ai`

## Local Development

Here you can find a list of the recommended prerequisites for this repository.

- Pre-installed tools:
  - [Finch](https://runfinch.com) or any other tool for local container development compatible with *Docker* APIs.
  - Most recent *AWS CLI* (`2.31.4` or higher).
  - Most recent *AWS SAM CLI* (`1.144.0` or higher).
  - Node.js in version `22.9.x` or higher.
  - Python in version `3.12.x` or higher.
  - Java in version `21.x` or higher.
- Configured profile in the installed *AWS CLI* with credentials for your *AWS IAM* user account of choice.

If you would like to start all the dependent services, run the following commands:

```shell
# After cloning it, inside the the repository root:

$ cd examples
$ finch vm start                                    # ... if `finch` did not start virtual machine yet.
$ finch compose up -d                               # ... or compatible ones like: `docker compose up -d`.
$ cd ../infrastructure
$ npm install
$ npm run package
```

## TODO

- [ ] Samples for Python SDK of Strands Agents: https://github.com/strands-agents/samples
- [ ] Tutorial #1: https://www.youtube.com/watch?v=TD2ihEBkdkY
- [ ] Tutorial #2: https://www.youtube.com/watch?v=N7FGbBq1mI4
- [ ] AWS MCP servers: https://awslabs.github.io/mcp
- [ ] Spring AI example for Amazon Bedrock Agent Core: https://github.com/jamesward/hello-spring-ai-agentcore
- [ ] Spring AI MCP example: https://github.com/jamesward/spring-ai-mcp-demo

## License

- [MIT](./LICENSE.md)

## Authors

- [Wojciech Gawroński (afronski)](https://github.com/afronski) (aka [AWS Maniac](https://awsmaniac.com))
