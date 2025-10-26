from fastapi import FastAPI

from app.orchestrator import run_graph

app = FastAPI(title="Reporting Agent")

@app.on_event("startup")
def _setup():
    # init db step (create db or create some MCP client connect etc...)
    pass

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/chat")
def chat():
    out = run_graph("f9ca17eb-b4fe-4b29-b5b6-8283f87e1963", {
        "message": "I want to create a report for participate based on demographics",
    })

    return  {
        "reply": out["reply"],
        "candidate_templates": out["candidate_templates"]
    }