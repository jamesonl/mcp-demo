import asyncio
import time

import streamlit as st
import httpx

from mcp_tasks import stateless_task, stateful_task, procedural_task

try:
    import openai
except ImportError:  # pragma: no cover - openai not installed
    openai = None


class DemoAgent:
    """Simple agent demonstrating local and remote tool usage."""
    def __init__(self, driver="o3"):
        self.driver = driver
        self.log = []
        self.tools = {}
        self.register_tool("stateless_task", stateless_task,
                           "Convert text to uppercase for quick transformations.")
        self.register_tool("stateful_task", stateful_task,
                           "Retrieve and manipulate stored objects by id.")
        self.register_tool("procedural_task", procedural_task,
                           "Run a short procedure defined by the detail argument.")

    def register_tool(self, name: str, func, description: str) -> None:
        """Register a tool callable with a description."""
        self.tools[name] = {"callable": func, "description": description}

    async def call_remote_tool(self, url: str, payload: dict) -> dict:
        """Call a remote tool hosted on the MCP server."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def stateless_task(self, text: str) -> str:
        """Use the stateless tool to transform ``text`` without side effects."""
        start = time.time()
        result = await self.tools["stateless_task"]["callable"](text)
        self.log.append(("stateless_task", time.time() - start))
        return result

    async def stateful_task(self, obj_id: str) -> dict:
        """Retrieve an object and mutate it when appropriate."""
        start = time.time()
        obj = await self.tools["stateful_task"]["callable"](obj_id)
        self.log.append(("stateful_task", time.time() - start))
        return obj

    async def procedural_task(self, detail: str) -> str:
        """Execute a structured step according to ``detail``."""
        start = time.time()
        result = await self.tools["procedural_task"]["callable"](detail)
        self.log.append((f"procedural_task({detail})", time.time() - start))
        return result

    async def run_tasks_in_parallel(self, tasks):
        """Run multiple tasks concurrently and record the total duration."""
        start = time.time()
        results = await asyncio.gather(*tasks)
        self.log.append(("parallel_tasks", time.time() - start))
        return results

    async def long_running_reasoning_task(self, prompt: str) -> str:
        """Delegate a complex reasoning step to a large model."""
        start = time.time()
        if openai is None:
            result = "openai package not available"
        else:
            resp = openai.chat.completions.create(
                model="o3-pro",
                messages=[{"role": "user", "content": prompt}],
            )
            result = resp.choices[0].message.content
        self.log.append(("long_running_reasoning_task", time.time() - start))
        return result


agent = DemoAgent()

st.set_page_config(layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

left, right = st.columns([0.6, 0.4])

with left:
    st.header("Chat")
    user_input = st.text_input("Say something")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        if user_input.startswith("remote:"):
            text = user_input[len("remote:"):].strip()
            resp = asyncio.run(
                agent.call_remote_tool("http://localhost:8000/stateless",
                                      {"text": text})
            )
            result = resp.get("result", "")
        else:
            result = asyncio.run(agent.stateless_task(user_input))
        st.session_state.messages.append(("assistant", result))

    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")

with right:
    st.header("Reasoning steps")
    for task, duration in agent.log:
        st.write(f"{task}: {duration:.2f}s")
