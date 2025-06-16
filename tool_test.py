from typing import Callable, List, get_type_hints, Any
from pydantic import BaseModel, Field
from openai import OpenAI
import os
import dotenv
import inspect
import pprint

# Load environment variables
dotenv.load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === Type Conversion ===

def python_type_to_json_schema(py_type: Any) -> dict:
    """Map Python type annotations to JSON Schema types."""
    origin = getattr(py_type, '__origin__', py_type)

    if origin is str:
        return {"type": "string"}
    elif origin is int:
        return {"type": "integer"}
    elif origin is float:
        return {"type": "number"}
    elif origin is bool:
        return {"type": "boolean"}
    elif origin is dict:
        return {"type": "object"}
    elif origin is list:
        return {"type": "array"}
    else:
        raise ValueError(f"Unsupported parameter type: {py_type}")

# === Tool Functions ===

def turn_upper_case(text: str) -> str:
    """Turn the text to upper case."""
    return text.upper()

def turn_lower_case(text: str) -> str:
    """Turn the text to lower case."""
    return text.lower()

def turn_title_case(text: str) -> str:
    """Turn the text to title case."""
    return text.title()

def addition(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def subtraction(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b

def multiplication(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# === Tool Registration ===

def register_tool(functions: List[Callable]) -> dict:
    """Register tools based on function metadata."""
    tools = {}

    for func in functions:
        sig = inspect.signature(func)
        tool_name = func.__name__
        type_hints = get_type_hints(func)

        properties = {}
        required = []

        for name, param in sig.parameters.items():
            param_type = type_hints.get(name, str)
            properties[name] = python_type_to_json_schema(param_type)
            if param.default == inspect.Parameter.empty:
                required.append(name)

        tools[tool_name] = {
            "type": "function",
            "name": tool_name,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
                "additionalProperties": False,
            },
        }

    return tools

tool_definitions = register_tool([
    turn_lower_case,
    turn_upper_case,
    turn_title_case,
    addition,
    subtraction,
    multiplication
])

# === Output Schema ===

class ToolTask(BaseModel):
    name: str = Field(description="The name of the tool used", json_schema_extra={"example": "turn_upper_case"})
    chain_of_thought: str = Field(description="The chain of thought process used to arrive at the output", json_schema_extra={"example": "I need to turn the text to uppercase"})
    output: str = Field(description="The output from the tool", json_schema_extra={"example": "THE CHICKEN CROSSED THE ROAD"})

    class Config:
        extra = "ignore" # instead of forbid

class ToolTasks(BaseModel):
    tasks: List[ToolTask]
    final_output: str

    model_config = {
        "extra": "ignore"  # options: "ignore", "forbid", "allow"
    }

# === Example Output (for prompting) ===

example_output = """
{
  "tasks": [ {"name": "...", "output": "..."}, ... ],
  "final_output": "..."
}
"""
# === Tool Call ===

# print(list(tool_definitions.values()))


# === Inference Call ===

lower_response = client.responses.parse(
    model="o3-mini",
    input=[
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Respond with a JSON object matching this schema:\n"
                "{ \"tasks\": [{\"name\": \"string\", \"output\": \"string\"}], \"final_output\": \"string\" }"
            )
        },
        {
            "role": "user",
            "content": "capitalize, then lowercase the following phrase: 'the chicken crossed the road'"
        }
    ],
    reasoning={"effort": "medium"},
    parallel_tool_calls=False,
    tools=list(tool_definitions.values()),
    tool_choice="auto",
    text_format=ToolTasks
)

# === Output Handling ===

if lower_response.output_parsed is None:
    print("Raw text output:\n", lower_response.text)
    raise ValueError("No valid parsed output returned.")

tooltasks: ToolTasks = lower_response.output_parsed

print("Final:", tooltasks.final_output)
for t in tooltasks.tasks:
    print(f"- Tool: {t.name}, Output: {t.output}, Chain of Thought: {t.chain_of_thought}")