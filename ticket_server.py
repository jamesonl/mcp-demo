from fastapi import FastAPI

app = FastAPI()

# In-memory ticket store
TICKETS = {
    "1": {"id": "1", "status": "created"},
    "2": {"id": "2", "status": "scheduled"},
}

@app.get('/tickets/{ticket_id}')
async def get_ticket(ticket_id: str):
    return TICKETS.get(ticket_id, {"error": "not found"})

@app.post('/tickets/{ticket_id}')
async def update_ticket(ticket_id: str, status: str):
    ticket = TICKETS.setdefault(ticket_id, {"id": ticket_id})
    ticket['status'] = status
    return ticket
