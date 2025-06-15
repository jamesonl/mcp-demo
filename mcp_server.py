from fastapi import FastAPI
from mcp_tasks import stateless_task, stateful_task, procedural_task

app = FastAPI()

@app.post('/stateless')
async def do_stateless(text: str):
    return {'result': await stateless_task(text)}

@app.post('/stateful')
async def do_stateful(obj_id: str):
    return await stateful_task(obj_id)

@app.post('/procedural')
async def do_procedural(detail: str):
    return {'result': await procedural_task(detail)}
