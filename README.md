# mcp-demo

This repository demonstrates a basic Streamlit chat agent using the OpenAI Agents SDK. The app showcases stateless, stateful, procedural and parallel task execution as well as long‑running reasoning steps.

The project highlights three key ideas:

1. **Sophisticated function calls** – reasoning models (``o3``/``o4-high``) can orchestrate local and remote tools.
2. **Extensibility** – new capabilities can be added via the MCP server with minimal changes to the agent.
3. **Asynchronous execution** – long running reasoning tasks illustrate the non‑blocking nature of the tools.

## Setup

1. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
2. Export your OpenAI API key
   ```bash
   export OPENAI_API_KEY=<your-key>
   ```

3. Make the helper script executable
   ```bash
   chmod +x start.sh
   ```

4. Start both the MCP server and the Streamlit app
   ```bash
   ./start.sh
   ```

The interface opens with the chat panel on the left and a list of reasoning steps on the right showing each task and the time it took.

The agent can import any additional asynchronous functions from `mcp_tasks.py` or
from your own modules. Each function includes a short description so the agent
knows when to use it.

To call a remote tool instead of a local one, prefix your chat message with
`remote:`. The agent will contact the MCP server and execute the appropriate
task.

## Example demo utterances

* **Stateless task** – `uppercase hello world`
* **Stateful task** – `fetch item 42`
* **Procedural task** – `run procedure sample step`
* **Parallel tasks** – `process A and B together`
* **Long running reasoning** – `reason about the meaning of life`
