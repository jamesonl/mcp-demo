from fastapi import FastAPI
from mcp_tasks import clean_text, update_ticket_status, deep_research

app = FastAPI()

@app.post('/clean_text')
async def do_clean_text(text: str):
    return {'result': await clean_text(text)}

@app.post('/update_ticket')
async def do_update_ticket(ticket_id: str, status: str):
    return await update_ticket_status(ticket_id, status)

@app.post('/deep_research')
async def do_deep_research(query: str):
    return {'result': await deep_research(query)}
