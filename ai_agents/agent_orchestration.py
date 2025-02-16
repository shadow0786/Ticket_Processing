from data_classes import *
from .ticket_analysis_agent import TicketAnalysisAgent
from .response_generation_agent import ResponseAgent



class TicketProcessor:
    def __init__(self):
        self.analysis_agent = TicketAnalysisAgent()
        self.response_agent = ResponseAgent()
        self.context = {}  

    async def process_ticket(self, ticket: dict[str, any], response_templates: dict[str, str]) -> TicketResolution:
        
        try:
            # Update context with basic ticket data like customer name and subject from ticket. Also add default values
            self.context["subject"] = ticket.get("subject", "Unidentified")
            customer_name = ticket.get("customer_info", {}).get("name", "Customer_Name")
            self.context["name"] = customer_name
            
            # Analyze the ticket content and call the ticketanalysis class first. Also add default values just in case
            analysis = await self.analysis_agent.analyze_ticket(
                ticket_content=ticket.get("content", ""),
                customer_info=ticket.get("customer_info", {})
            )
            
            # Generate a response based on analysis and context by calling the responseAgent class 
            response = await self.response_agent.generate_response(
                ticket_analysis=analysis,
                response_templates=response_templates,
                context=self.context
            )
            
            # return resolved analysed ticket
            return TicketResolution(
                ticket_id=ticket.get("id", "Unknown"),
                analysis=analysis,
                response=response
            )
        
        except Exception as e:
            # Error handling here and return a resolution with an error message
            #dummy response text
            error_response = ResponseSuggestion(
                response_text="An error occurred while processing the ticket.",
                confidence_score=0.0,
                requires_approval=True,
                suggested_actions=["Review error logs", "Contact system administrator"]
            )

            # default analysis incase of error to keep the system running and still displaying a solution with response type
            default_analysis = TicketAnalysis(
                category=TicketCategory.TECHNICAL,
                priority=Priority.LOW,
                key_points=[],
                required_expertise=["Error Handling"],
                sentiment=0.0,
                urgency_indicators=[],
                business_impact="Low",
                suggested_response_type="general_response"
            )

            # default ticket resolution return type 
            return TicketResolution(
                ticket_id=ticket.get("id", "Unknown"),
                analysis=default_analysis,
                response=error_response
            )





        
