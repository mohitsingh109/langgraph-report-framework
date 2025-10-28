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

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.constants import START, END
from langgraph.graph import StateGraph

from app.agents.registry import init_agents, get_agent

checkpointer = InMemorySaver() # For the current session

def build_graph():
    init_agents()
    g = StateGraph(dict)

    g.add_node("routing_agent", lambda s: get_agent("routing_agent").execute(s))
    g.add_node("template_agent", lambda s: get_agent("template_agent").execute(s))
    g.add_node("scheduling_agent", lambda s: get_agent("scheduling_agent").execute(s))

    g.add_edge(START, "routing_agent")
    g.add_conditional_edges(
        "routing_agent",
        lambda s: s.get("next_agent"),
        {
            "template_agent": "template_agent",   # State key to node name
            "scheduling_agent": "scheduling_agent"
        }
    )
    g.add_edge("template_agent", END)
    g.add_edge("scheduling_agent", END)

    # We'll add token usage or custom event storage using hooks
    return g.compile(checkpointer = checkpointer) # this checkpointer is storing all over state in (InMemory)

graph = build_graph()

def run_graph(thread_id: str, user_message: str) -> Dict[str, Any]:
    """
    Payload may contain
        - message
        - selected_template_id
        - input_fields
    """
    # TODO: all this things we'll be extracted from user message
    # V1 Code
    # state: Dict[str, Any] = {
    #     "thread_id": thread_id,
    #     "user_message": payload.get("message") or "",
    #     "selected_template_id": payload.get("selected_template_id") or "",
    #     "provided_inputs": payload.get("input_fields") or {}
    # }

    state = {
        "thread_id": thread_id,
        "user_message": user_message
    }
    #config = {"configurable": {"thread_id": thread_id}} # THis is required if you are using checkpointer
    config = RunnableConfig(configurable={"thread_id": thread_id})
    out = graph.invoke(state, config=config)
    states = list(graph.get_state_history(config))

    # for state in states:
    #     print(state.next)
    #     print(state.values)
    #     print(state.config["configurable"]["checkpoint_id"])
    #     print()
    return out