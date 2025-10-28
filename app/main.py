from fastapi import FastAPI

from app.orchestrator import run_graph
from app.schemas import ChatResponse, ChatRequest

app = FastAPI(title="Reporting Agent")

@app.on_event("startup")
def _setup():
    # init db step (create db or create some MCP client connect etc...)
    pass

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chat", response_model=ChatResponse) # this is the respone payload we need to return in the post request (it's a fast api stuff)
def chat(req: ChatRequest):
    out = run_graph(req.conversation_id, req.message)

    return ChatResponse(
        conversation_id = req.conversation_id, # conversation_id == thread_id
        status="ok",
        reply=out.get("reply"),
        data = out
    )