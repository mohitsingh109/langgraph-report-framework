from typing import Dict, Any, List
from langchain.tools import tool
from ..services.template_service_client import list_templates


@tool("fetch_template", return_direct=False)
def fetch_template_tool() -> List[Dict[str, Any]]:
    """Fetch template from Template Service"""
    return list_templates()


