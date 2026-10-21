from smolagents import OpenAIModel, ToolCallingAgent, MCPClient
from mcp.client.streamable_http import streamable_http_client
import os
from dotenv import load_dotenv
from tools import github_metadata, github_repo_code, github_repo_files
load_dotenv()
server_parameters = {
    "url": "https://api.githubcopilot.com/mcp/x/repos/readonly",
    "transport": "streamable-http",
    "headers": {
        "Authorization": f"Bearer {os.environ['github_token']}"
    }
}
print(os.getenv("github_token") is not None)
model = OpenAIModel(
    model_id = "qwen3.5:4b-mlx",
    api_base="http://localhost:11434/v1",
    api_key = "ollama"
    )
with MCPClient(server_parameters) as github_tools: #passing server parameters through mcp client class to extract the tools needed
    agent = ToolCallingAgent(
        model = model, #use the model to reason and figure out with tools to use given what we have
        tools = github_tools, #we gave it the tools with the premise, inputs, and expected outputs of each function
        max_steps = 6 #no more than 6 steps until its terminated
        )
    result = agent.run(
        "Investigate the psf/requests repository. Identify the files responsible for making HTTP requests, explain their roles, and cite the relevant filenames. Do not modify the repository."
    )

print(result)