# from typing import Dict, Any
#
# from app.agents.base_agent import BaseAgent
#
# class PlanningAgent(BaseAgent):
#     def name(self) -> str:
#         return "understand_query"
#
#     def system_prompt(self) -> str:
#         return """It understand the user query and pass it to the appropriate agent"""
#
#     def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
#         query = state.get("user_message", "")
#         prompt = f"""
#                 Classify the intent of the user
#                 {query}
#                 Return only one of: create_report | view_stats | unknow
#         """
#         # llm_complete this will be a gemini call
#         intent = llm_complete(prompt).split()[0].lower() or "unknow"
#         state["intent"] = intent
