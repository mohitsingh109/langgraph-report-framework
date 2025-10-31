from typing import List

from langchain.agents import create_agent
from langchain_core.tools import BaseTool

from app.agents.base_agent import BaseAgent
from app.llm import get_llm
from app.tools.report_tools import trigger_report_tool, collect_required_fields_tool, generate_report_url_tool


class SchedulingAgent(BaseAgent):
    def name(self) -> str:
        return "scheduling_agent"

    def system_prompt(self) -> str:
        return """
            You are a Scheduling Agent
            You help the user trigger a report, ask for required fields if needed,
            and return a dashboard url to track it
        """

    def tools(self) -> List[BaseTool]:
        return [
            collect_required_fields_tool,
            trigger_report_tool,
            generate_report_url_tool
        ]

def create_report_agent():
    model = get_llm()
    return create_agent(
        model=model,
        tools=[collect_required_fields_tool, trigger_report_tool, generate_report_url_tool],
        name="report_agent",
        system_prompt="""
            "You are ReportAgent. You schedule reports based on user input. "
            "Use the provided template_id and details like name or schedule time."
        """
    )