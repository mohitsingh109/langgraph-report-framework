import uuid
from typing import Dict, Any, List
from langchain.tools import tool

from ..hitl import hitl_tool, YesNoOptions
from ..services.template_service_client import list_templates, add_template


@tool("fetch_template_tool", return_direct=False, parse_docstring=True)
def fetch_template_tool() -> List[Dict[str, Any]]:
    """
    Retrieves a list of all available report templates, including their names and unique IDs.

    This function provides the complete catalogue of reports that the system can generate,
    allowing the user or agent to select a template for further action (like describing or triggering).

    Args:
        # No arguments are required for this tool.

    Returns:
        A list of dictionaries, where each dictionary represents a report template.
        Each entry includes the 'id', 'name', and 'config' keys.
        Example: [{"id": "...", "name": "...", "config": {...}}, ...]
    """
    return list_templates()


@tool("fetch_data_point", parse_docstring=True)
def fetch_data_point(domain: str) -> dict:
    """Retrieves a list of available data points for a specified domain.

    This function fetches a predefined catalog of data fields that can be selected
    to construct a new report template.

    Args:
        domain (str): The functional area or category of the data requested
            (e.g., "Participant", "Grants", "HR Payroll", "Marketing").
            The domain is case-sensitive for lookup.

    Returns:
        dict: A dictionary where the key is the requested domain and the value
            is a list of dictionaries. Each inner dictionary represents an
            available data point with its 'field_name' and suggested 'type'.
            Returns {domain: []} if the domain is not found.

            Example of the return format:
            {
                "Grants": [
                    {"field_name": "grant_name", "type": "string"},
                    {"field_name": "grant_amount", "type": "currency"},
                    ...
                ]
            }
    """
    # Mock data structure mapping domains to their available data points
    MOCK_DATA_CATALOG = {
        # Split Participant and Grants into two separate domains
        "Participant": [
            {"field_name": "participant_id", "type": "integer"},
            {"field_name": "first_name", "type": "string"},
            {"field_name": "last_name", "type": "string"},
            {"field_name": "enrollment_date", "type": "date"},
            {"field_name": "demographic_code", "type": "string"}
        ],
        "Grants": [
            {"field_name": "grant_id", "type": "integer"},
            {"field_name": "grant_name", "type": "string"},
            {"field_name": "grant_amount", "type": "currency"},
            {"field_name": "submission_date", "type": "datetime"},
            {"field_name": "program_area", "type": "string"},
            {"field_name": "grant_status", "type": "string"}
        ],
        "HR Payroll": [
            {"field_name": "employee_id", "type": "integer"},
            {"field_name": "job_title", "type": "string"},
            {"field_name": "salary", "type": "currency"},
            {"field_name": "pay_period_start", "type": "date"}
        ],
        "Marketing": [
            {"field_name": "campaign_id", "type": "integer"},
            {"field_name": "channel", "type": "string"},
            {"field_name": "impression_count", "type": "integer"}
        ]
    }

    # Normalize the domain input for lookup (using strip but maintaining case)
    normalized_domain = domain.strip()

    # Retrieve data points for the given domain. Returns an empty list if not found.
    data_points = MOCK_DATA_CATALOG.get(normalized_domain, [])

    # Format the output as specified in the docstring
    return {normalized_domain: data_points}


@hitl_tool(
    message="Do you want to create a template?",
    conformation_type='yes_no',
    options=YesNoOptions("Create Template", 'Cancel it', 'Yes create the template', 'No cancel it')
)
@tool("create_template_tool", parse_docstring=True)
def create_template_tool(name: str, required_fields:dict, description: str) -> dict:
    """
    Creates a new template configuration.

    Args:
        name: The display name for the new template (e.g., "Demographics: Basic").
        required_fields: A dictionary defining the fields required by this template and their properties.
        description: A brief description of the template's purpose.

    Returns:
        A dictionary containing a message and the ID of the newly created template.
    """

    obj = {
        "id": str(uuid.uuid4()), # Cast uuid to string for JSON serialization
        "name": name,
        "config": {
            "category": "", # You might want to parameterize this
            "description": description,
            "required_fields": required_fields
        }
    }

    add_template(obj) # Assuming this function exists

    # Corrected: Use a colon (:) to create a dictionary
    return {"message": f"Successfully create template with id: {obj['id']}"}

@tool("describe_template_tool", return_direct=False, parse_docstring=True)
def describe_template_tool(template_id: str) -> Dict[str, Any]:
    """
    Fetches the detailed configuration for a specific report template, including all required input fields.

    The main purpose of this tool is to retrieve the necessary parameters (e.g., 'region', 'asset_types')
    that a user must supply to successfully generate a report using the given template ID.

    Args:
        template_id: The unique identifier (string, a UUID) of the report template
                     whose full configuration details are required.

    Returns:
        A dictionary containing the full template configuration, including the
        'required_fields' list within the 'config' key. Returns a simple error
        dictionary if the ID is not found.
        Example: {"id": "...", "name": "...", "config": {"required_fields": ["report_name", "schedule_time", "region"]}}
    """
    templates = list_templates()
    for t in templates:
        if t["id"] == template_id:
            return t
    return {"error": "template not found"}

@tool("find_template_by_name")
def find_template_by_name(name: str) -> dict:
    """Find template ID by name (case-insensitive)."""
    for t in list_templates():
        if name.lower() in t["name"].lower():
            return t
    return {"error": "No matching template"}