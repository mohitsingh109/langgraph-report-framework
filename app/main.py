from fastapi import FastAPI
from langchain_core.runnables import RunnableConfig

from app.orchestrator import run_graph
from app.schemas import ChatResponse, ChatRequest
from app.supervisor_app import create_workflow

app = FastAPI(title="Reporting Agent")
workflow = create_workflow() # this is object supervisor agent
@app.on_event("startup")
def _setup():
    # init db step (create db or create some MCP client connect etc...)
    pass

@app.get("/health")
def health():
    return {"ok": True}

# UI will hit this endpoint with user message..
# Sync...
@app.post("/chat", response_model=ChatResponse) # this is the respone payload we need to return in the post request (it's a fast api stuff)
def chat(req: ChatRequest):
    config = RunnableConfig(configurable={"thread_id": req.conversation_id}) # this will help graph to remember your history
    result = workflow.invoke({
        "messages": [{"role": "user", "content": req.message}]
    }, config)

    # return ChatResponse(
    #     conversation_id = req.conversation_id, # conversation_id == thread_id
    #     status="ok",
    #     reply=out.get("reply"),
    #     data = out
    # )
    return ChatResponse(conversation_id=req.conversation_id, reply=result["messages"][-1].text)
