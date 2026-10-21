# GitHub Repository Investigator

A Python prototype for exploring GitHub repositories with an AI agent. It connects a `smolagents` tool calling agent to GitHub's read only repository MCP endpoint and uses a locally served, OpenAI compatible model to answer questions about code.

The current example asks the agent to investigate `psf/requests`, identify the files involved in making HTTP requests, explain their roles, and cite filenames. The repository also includes custom GitHub REST API tools for reading repository metadata, listing files, and fetching file contents.

## What I built

- Configured a `ToolCallingAgent` with a local model served at `http://localhost:11434/v1`.
- Connected the agent to GitHub's read only repository MCP tools using a token from `.env`.
- Wrote reusable `smolagents` tools in `tools.py` for repository metadata, directory listings, and source files.
- Added a concrete code investigation prompt in `main.py` with a six step agent limit.

## Run locally

1. Create a Python virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Copy `.env.example` to `.env` and replace the placeholder with a GitHub token that can read the repositories you want to inspect. The `.env` file is ignored by Git.

3. Start an OpenAI compatible local model server at `http://localhost:11434/v1` and make the model named `qwen3.5:4b-mlx` available. If your local model has a different name or endpoint, update the `OpenAIModel` configuration in `main.py`.

4. Run the example:

   ```bash
   python main.py
   ```

The repository and investigation question are currently specified in `main.py`. Edit the prompt there to investigate another project. `tools.py` defines standalone REST API tools; the example agent currently uses the tools supplied by the MCP connection.

## Files

| File | Purpose |
| --- | --- |
| `main.py` | Loads configuration, connects to GitHub MCP, creates the agent, and runs the example investigation. |
| `tools.py` | Defines GitHub REST API helpers and `smolagents` tool wrappers. |
| `requirements.txt` | Lists Python packages needed by the project. |

This is an exploratory prototype with a fixed example prompt and local model configuration, rather than a general purpose command line application.
