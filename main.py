import os
from typing import Literal, Optional
from dotenv import load_dotenv
try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - handled at runtime
    OpenAI = None  # type: ignore[assignment]

from fastmcp import FastMCP

from prompt_structure import PromptStructure

mcp = FastMCP("My MCP Server")

load_dotenv()
def _get_openai_client() -> "OpenAI":
    """Instantiate an OpenAI client using the API key from the environment."""
    api_key = os.getenv("APIKEY")
    # print(api_key)
    if not api_key:
        raise RuntimeError("Environment variable APIKEY must be set with a valid OpenAI API key.")
    if OpenAI is None:
        raise RuntimeError("openai package is required but not installed. Install `openai` to enable GPT-5 interactions.")
    return OpenAI(api_key=api_key)


@mcp.tool()
def build_better_meta_prompt(name: str, prompt_instruction: str, tone: Literal["formal", "informal", "friendly", "professional", "humorous", "serious"] = "friendly") -> str:
    """Generate a structured greeting prompt and request a GPT-5 refinement suggestion."""
    prompt = PromptStructure(
        objective=prompt_instruction,
        tone=tone,
        refinement_notes=[
            "Start with this structure and adjust the context or tone based on the model's response.",
            "Keep iterating until the greeting matches the desired voice and clarity.",
        ],
    )
    structured_prompt = prompt.render()

    client = _get_openai_client()
    response = client.responses.create(
        model="gpt-5",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "You are an expert prompt engineer. "
                            "You rewrite prompt drafts for clarity, specificity, and tone alignment."
                        ),
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Rewrite the following prompt to maximize clarity, and propose any additional adjustments "
                            "to context or tone if they improve the result. Return the improved prompt text and a short rationale.\n\n"
                            f"{structured_prompt}"
                        ),
                    }
                ],
            },
        ],
    )
    refined_prompt: Optional[str] = getattr(response, "output_text", None)
    if not refined_prompt:
        refined_prompt = "\n".join(
            block.text if hasattr(block, "text") else str(block) for block in getattr(response, "output", [])
        )

    return (
        "Structured Prompt Draft:\n"
        f"{structured_prompt}\n\n"
        "GPT-5 Proposal:\n"
        f"{refined_prompt.strip()}"
    )

test = build_better_meta_prompt(name="Alice", prompt_instruction="Create a warm and engaging greeting message.", tone="friendly")
print(test)


if __name__ == "__main__":
    mcp.run()
