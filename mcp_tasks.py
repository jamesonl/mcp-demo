import asyncio

async def stateless_task(text: str) -> str:
    """Convert text to uppercase. Use for quick, stateless transformations."""
    await asyncio.sleep(0)
    return text.upper()

async def stateful_task(obj_id: str) -> dict:
    """Retrieve and modify an object using ``obj_id`` when its value is 'example'."""
    await asyncio.sleep(0)
    obj = {"id": obj_id, "value": "example"}
    if obj["value"] == "example":
        obj["value"] = obj["value"].upper()
    return obj

async def procedural_task(detail: str) -> str:
    """Run a small procedure described by ``detail``."""
    await asyncio.sleep(0.1)
    return f"completed: {detail}"
