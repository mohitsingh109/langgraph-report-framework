from typing import Optional, Dict, Any, Callable

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool
from langgraph.types import interrupt
from langchain_core.tools import tool as create_tool
from langgraph.prebuilt.interrupt import HumanInterruptConfig, HumanInterrupt

# UI response for HITL
"""
{
    "type": "yes_no",
    "yes_text": "Yes",
    "no_text": "No",
    "yes_description":...
}
"""
class YesNoOptions:
    def __init__(
            self,
            yes_text: str = "Yes",
            no_text: str = "No",
            yes_description: Optional[str] = None,
            no_description: Optional[str] = None,
    ):
        self.yes_text = yes_text
        self.no_text = no_text
        self.yes_description = yes_description
        self.no_description = no_description


    def to_dict(self) -> Dict[str, Any]:
        result = {
            "type": "yes_no",
            "yes_text": self.yes_text,
            "no_text": self.no_text
        }

        if self.yes_description:
            result['yes_description'] = self.yes_description

        if self.no_description:
            result['no_description'] = self.no_description

        return result

# class CustomOptions:

# class ToolEditOption

# decorator

def hitl_tool(
    message: str,
    conformation_type: str = 'yes_no',
    options: Optional[YesNoOptions] = None
):
    def decorator(func: Callable) -> Callable:
        # this will going to help us to take decision later
        """
        this is how the options will looks like
        {
            "type": "yes_no",
            "yes_text": "Yes",
            "no_text": "No",
            "yes_description":...
        }
        """
        # create_template_tool we added a property name _hitl_config
        func._hitl_config = {
            "message": message,
            "interrupt_config": {
                "conformation_type": conformation_type,
                "options": options.to_dict()
            }
        }

        return func

    return decorator

def get_hitl_config(tool):
    if hasattr(tool, '_hitl_config'):
        return tool._hitl_config

    return None

def add_human_in_the_loop(
        tool: Callable | BaseTool,
        *,
        interrupt_config: HumanInterruptConfig, # information of what type of hitl we are going to trigger
        description: str = None
):
    interrupt_description = description or f"Please review the {tool.name} tool call"

    @create_tool(tool.name, description=interrupt_description, args_schema=tool.args_schema)
    async def call_tool_with_interrupt(config: RunnableConfig, **tool_input):

        enhanced_interrupt_config = interrupt_config.copy()
        # enhanced_interrupt_config we'll use this later when we want to add the feature of edit the tool argument

        request: HumanInterrupt = {
            "action_request": {"action": tool.name, "args": tool_input},
            "config": enhanced_interrupt_config,
            "description": interrupt_description
        }

        # graph will stop here
        response = interrupt([request])[0]

        # if user select yes then response["type"] will be accepted otherwise reject
        if response["type"] == "accept":
            tool_response = await tool.invoke(tool_input, config)
        else:
            # we'll either send the default message or user feedback
            tool_response = "User denied the execution"

        return tool_response

    return call_tool_with_interrupt


def wrap_tool_with_hitl(tools: list[BaseTool]) -> list[BaseTool]:

    wrapped_tools = []
    hitl_wrapped_tool = 0

    for tool in tools:
        hitl_config = get_hitl_config(tool)
        if hitl_config:
            wrapped_tool = add_human_in_the_loop(
                tool,
                interrupt_config=hitl_config['interrupt_config'],
                description=hitl_config['message']
            )
            wrapped_tools.append(wrapped_tool)
            hitl_wrapped_tool += 1
        else:
            wrapped_tools.append(tool)

    return wrapped_tools
