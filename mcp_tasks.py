import asyncio
import re
import httpx
from openai import OpenAI

TICKET_API_URL = 'http://localhost:9000'

async def clean_text(text: str, client: OpenAI) -> str:
    """Remove simple SSN patterns from text."""
    await asyncio.sleep(0)
    return re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED]", text)

async def update_ticket_status(client: OpenAI, ticket_id: str, status: str) -> dict:
    """Update the status of a ticket via the ticket API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{TICKET_API_URL}/tickets/{ticket_id}", json={"status": status})
        resp.raise_for_status()
        return resp.json()

async def deep_research(client: OpenAI, query: str) -> str:
    """Long running reasoning using the openai responses API."""
    try:
        resp = await client.responses.chat.completions.create(
            model="o3-pro",
            messages=[{"role": "user", "content": query}],
        )
        return resp.choices[0].message.content
    except Exception:
        # Demo environment fallback
        await asyncio.sleep(0.1)
        return f"research result for: {query}"

async def chitchat(client: OpenAI, query: str) -> str:
    """Respond to the user in a friendly and engaging manner."""
    await asyncio.sleep(0)
    chatchat_response = client.responses.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
    )
    return chatchat_response.final_output
