from typing import Literal

from fastmcp import FastMCP

from prompt_structure import PromptStructure

mcp = FastMCP("My MCP Server")


@mcp.tool
def build_better_prompt(name: str, tone: Literal["formal", "informal", "friendly", "professional", "humorous", "serious"] = "friendly") -> str:
    """Provide a structured prompt that follows recommended prompt engineering practices."""
    prompt = PromptStructure(
        objective="Generate a concise greeting for the provided person.",
        context=f"The person's name is {name}. Respond with a single sentence that greets them directly.",
        tone=tone,
        refinement_notes=[
            "Start with this structure and adjust the context or tone based on the model's response.",
            "Keep iterating until the greeting matches the desired voice and clarity.",
        ],
    )
    return prompt.render()


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
