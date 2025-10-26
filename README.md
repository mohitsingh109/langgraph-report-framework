```commandline

"""State object for the reporting agent workflow"""
    messages: Annotated[List, operator.add]
    user_query: str
    available_templates: Optional[List[Dict]]
    selected_template: Optional[Dict]
    required_parameters: Optional[Dict]
    collected_parameters: Optional[Dict]
    validation_result: Optional[Dict]
    report_id: Optional[str]
    navigation_path: Optional[str]
    current_step: str
    user_confirmed: Optional[bool]
    error_message: Optional[str]
    
```

```text
"""Few Template json"""
"""
{
    "id": <uuid>,
    "name": "Hello Template",
    "config": {
        ...
    },
    ...
}
"""

"""
    Required field for specific template,
    Required field to schedule a report 
"""
```
# CMD to run the application
> uvicorn app.main:app --host 0.0.0.0 --port 8000
> 

```json
[
  "388a6a7b-1405-4fe2-b352-eb0fc6bde269",
  "f4d65171-986f-4ed5-b1a5-a0e1a4adf7db",
  "321f163b-e14e-46df-b0b4-593211f13c72"
]
```