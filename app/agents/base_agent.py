from abc import ABC, abstractmethod
from typing import Dict, Any, List, Callable

from app.tools.base_tool import BaseTool


class BaseAgent(ABC):
    """All feature agent should inherit this class"""

    @abstractmethod
    def name(self) -> str:
        """Unique name of the agent (used as a node in the langgraph)"""
        pass

    @abstractmethod
    def system_prompt(self) -> str:
        """System prompt that help Agent routing"""
        pass

    @abstractmethod
    def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Main logic of the agent node""" # direct logic, or it can call a list of tools or MCP client
        pass

    def tools(self) -> List[Callable]: # Callable anything that I can execute as a function List[fetch_template_tool] List[0]()
        return []

    def pre_hook(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Optional pre-processing hook""" # Check if token usage is under limit, guardrails to reject the execution, custom event emitter
        pass

    def post_hook(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Optional post-processing hook""" # Token usage update, bulk upload of custom event to langgraph state, guardrails to reject the execution
        pass

    def on_error(self, state: Dict[str, Any], error: Exception) -> Dict[str, Any]:
        """Error handling hook"""
        state["error"] = str(error)
        return state


