import asyncio
import os
import time
from typing import List

import streamlit as st
import httpx

from mcp_tasks import clean_text, update_ticket_status, deep_research

try:
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
except ImportError:  # pragma: no cover - openai not installed
    openai = None


class DemoAgent:
    """Agent that can chain multiple tools to satisfy a request."""

    def __init__(self, driver: str = "o3"):
        self.driver = driver
        self.log: List[tuple[str, float]] = []
        self.tools = {}
        self.register_tool(
            "clean_text", clean_text,
            "Strip private information such as SSNs from text.")
        self.register_tool(
            "update_ticket_status", update_ticket_status,
            "Modify the status of a ticket via the ticket system.")
        self.register_tool(
            "deep_research", deep_research,
            "Perform an in-depth research task using a long running model.")

    def register_tool(self, name: str, func, description: str) -> None:
        """Register a tool callable with a description."""
        self.tools[name] = {"callable": func, "description": description}

    async def call_remote_tool(self, url: str, payload: dict) -> dict:
        """Call a remote tool hosted on the MCP server."""
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def run_tool(self, name: str, *args, **kwargs):
        start = time.time()
        result = await self.tools[name]["callable"](*args, **kwargs)
        self.log.append((name, time.time() - start))
        return result

    async def runner(self, prompt: str) -> str:
        """Decide which tools to use and execute them sequentially."""
        # This is where an o3/o4-high model would plan which tools to run.
        # Without the OpenAI Agents SDK available, we fall back to heuristics.
        plan = []
        if "clean" in prompt:
            plan.append(("clean_text", {"text": prompt}))
        if "ticket" in prompt:
            plan.append(("update_ticket_status", {"ticket_id": "1", "status": "in_progress"}))
        if "research" in prompt:
            plan.append(("deep_research", {"query": prompt}))

        results = []
        for name, kwargs in plan:
            result = await self.run_tool(name, **kwargs)
            results.append(str(result))
        return "\n".join(results) if results else "No tools executed."


def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []


agent = DemoAgent()

st.set_page_config(layout="wide")
init_session_state()

left, right = st.columns([0.6, 0.4])

with left:
    st.header("Chat")
    user_input = st.text_input("Say something")
    if user_input:
        st.session_state.messages.append(("user", user_input))
        result = asyncio.run(agent.runner(user_input))
        st.session_state.messages.append(("assistant", result))

    for role, msg in st.session_state.messages:
        st.write(f"**{role}:** {msg}")

with right:
    st.header("Reasoning steps")
    for task, duration in agent.log:
        st.write(f"{task}: {duration:.2f}s")
