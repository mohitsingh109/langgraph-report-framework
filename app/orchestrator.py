""""
        START
          |
        ROUTING
     |             |
TEMPLATE AGENT   REPORT AGENT  DRY RUN TEMPLATE AGENT
        SUMMARIZE AGENT
        |
        END

"""

from typing import Dict, Any

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from app.agents.registry import init_agents, get_agent

checkpointer = InMemorySaver()

def build_graph():
    init_agents()
    g = StateGraph(dict)

    #g.add_node("routing_intent", lambda s: get_agent("routing_intent").execute(s))
    g.add_node("template_phase", lambda s: get_agent("template_phase").execute(s))
    #g.add_node("report_phase", lambda s: get_agent("report_phase").execute(s))

    g.add_edge(START, "template_phase")
    g.add_edge("template_phase", END)

    # We'll add token usage or custom event storage using hooks
    return g.compile(checkpointer = checkpointer)

graph = build_graph()

def run_graph(thread_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Payload may contain
        - message
        - selected_template_id
        - input_fields
    """
    # TODO: all this things we'll be extracted from user message
    state: Dict[str, Any] = {
        "thread_id": thread_id,
        "user_message": payload.get("message") or "",
        "selected_template_id": payload.get("selected_template_id") or "",
        "provided_inputs": payload.get("input_fields") or {}
    }
    config = {"configurable": {"thread_id": thread_id}}
    out = graph.invoke(state, config=config)

    return out