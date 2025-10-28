# `playground-agentic-ai`

## Local Development

Here you can find a list of the recommended prerequisites for this repository.

- Pre-installed tools:
  - [Finch](https://runfinch.com) or any other tool for local container development, that is compatible with *Docker* APIs.
  - Most recent *AWS CLI* (`2.31.4` or higher).
  - Most recent *AWS SAM CLI* (`1.145.2` or higher).
  - Node.js in version `22.20.x` or higher.
  - Python in version `3.12.x` or higher.
  - Java in version `21.x` or higher.
- Configured profile in the installed *AWS CLI* with credentials for your *AWS IAM* user account of choice.

If you would like to start all the dependent services, run the following commands:

```shell
# After cloning it, inside the the repository root:

$ finch vm start             # ... if `finch` did not start virtual machine yet.
```

## Remarks

- *Strands Agents* does not support [Elicitation](https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation) yet ([ticket is here](https://github.com/strands-agents/sdk-python/issues/789)).
  - Recommended way for now is to use `handoff_to_user` tool.

## Resources

- [Building Intelligent Agents with Strands: A Hands-On Guide](https://www.youtube.com/watch?v=TD2ihEBkdkY)
- [Deploy ANY AI Agent to Production in Minutes - Amazon Bedrock AgentCore Tutorial](https://www.youtube.com/watch?v=N7FGbBq1mI4)
- [AWS MCP Servers](https://awslabs.github.io/mcp)
- [AWS Workshop: Diving Deep into Amazon Bedrock AgentCore](https://catalog.us-east-1.prod.workshops.aws/workshops/015a2de4-9522-4532-b2eb-639280dc31d8/en-US)

## License

- [MIT](./LICENSE.md)

## Authors

- [Wojciech Gawroński (afronski)](https://github.com/afronski) (aka [AWS Maniac](https://awsmaniac.com))
