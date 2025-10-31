from langgraph.checkpoint.memory import InMemorySaver
from langgraph_supervisor import create_supervisor
from app.agents.template_agent import create_template_agent
from app.agents.scheduling_agent import create_report_agent
from app.llm import get_llm

checkpointer = InMemorySaver() # This is checkpointer (we'll replace it with postgres sql saver)

def create_workflow():
    model = get_llm() # Gemini model

    template_agent = create_template_agent() # Agent 1 (Internally a graph with tools)
    report_agent = create_report_agent() # Agent 2 (Internally a graph with tools)


    supervisor_prompt = """
       You are a supervisor coordinating TemplateAgent and ReportAgent.

       - If user asks to find or use a report template, delegate to TemplateAgent.
       - If user asks to schedule or trigger a report, delegate to ReportAgent.
       - If both tasks are mentioned, first use TemplateAgent to fetch template_id,
         then provide it to ReportAgent to schedule the report.
       - Summarize final outcome clearly for the user.
       """
    # THis is graph
    workflow = create_supervisor(
        [template_agent, report_agent],
        model=model,
        prompt=supervisor_prompt,
    )

    return workflow.compile(checkpointer=checkpointer)
