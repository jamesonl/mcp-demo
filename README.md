# mcp-demo

This repository demonstrates a small Streamlit chat agent built with the OpenAI Agents SDK. The goal is to showcase how reasoning models such as `o3` and `o4-high` can chain together multiple tools, including remote MCP tasks, while tracking the timing of each step.

The demo highlights three ideas:

1. **Sophisticated function calls** – the agent can decide when to clean text, update a ticket, or launch a deep research task.
2. **Extensibility** – new tools can be exposed through the MCP server or via additional modules without modifying the agent logic.
3. **Asynchronous execution** – long running reasoning tasks run without blocking the chat interface.

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
4. Start the MCP server, ticket API and Streamlit app together
   ```bash
   ./start.sh
   ```

The interface opens with the chat panel on the left and reasoning steps on the right. Each step lists the tool name and the time it took to execute.

## Example demo utterances

* **Clean sensitive text** – `clean 123-45-6789 in this sentence`
* **Update a ticket** – `ticket 2 should be completed`
* **Perform deep research** – `research the history of open source`
