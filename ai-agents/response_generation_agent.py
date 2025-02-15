from data_classes import *


class ResponseAgent:
    async def generate_response(self, ticket_analysis: TicketAnalysis, response_templates: Dict[str, str], context: Dict[str, Any]) -> ResponseSuggestion:
        
    