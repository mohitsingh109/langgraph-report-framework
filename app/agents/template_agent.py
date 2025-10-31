from typing import Dict, Any, List

from app.agents.base_agent import BaseAgent
from ..llm import get_llm
from ..tools.template_tool import fetch_template_tool, describe_template_tool, find_template_by_name, create_template_tool, fetch_data_point
from langchain.agents import create_agent


class TemplateAgent(BaseAgent):
    def name(self) -> str:
        return "template_agent"

    def system_prompt(self) -> str:
        return """
            "You are Template Agent"
            "You help user find and select the best template for selecting template"
            You can:
            "-- User 'fetch_template_tool' to get list of template"
            "-- User 'describe_template_tool' to describe a selected template."
        """

    def tools(self):
        return [fetch_template_tool, describe_template_tool]


def create_template_agent():
    model = get_llm()
    # you can build your own graph as well
    return create_agent( # it's a reactive agent
        model=model,
        tools=[fetch_template_tool, find_template_by_name, describe_template_tool, create_template_tool, fetch_data_point],
        name="template_agent",
        system_prompt="""
            "You are TemplateAgent. Your job is to help find the correct template "
            "for a report or create a new template if it's not available. Always call the right tool to find template ID by name."
            
            """
    )