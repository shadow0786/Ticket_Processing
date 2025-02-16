import unittest
from ai_agents.ticket_analysis_agent import TicketAnalysisAgent
from data_classes import *
from ai_agents.response_generation_agent import ResponseAgent
from ai_agents.agent_orchestration import TicketProcessor
from .templates import *


## test class to initialise and conduct the test

class TestTicketProcessing(unittest.IsolatedAsyncioTestCase):
    async def test_priority_assignment(self):

        agent = TicketAnalysisAgent()
        # Ticket with urgency keywords and high role should be URGENT

        ticket_content = "Hello I am not able to access the dashboard. Need this fixed very fast because of bill processing."
        customer_info = {"role": "Finance Director"}

        # anaylse ticket with ticketAnalyser
        analysis = await agent.analyze_ticket(ticket_content, customer_info)

        #check the ticket category and priority are correct
        self.assertEqual(analysis.priority, Priority.URGENT)
        self.assertEqual(analysis.category, TicketCategory.ACCESS)
    
    async def test_response_generation(self):
        # sample expected ticket generation
        analysis = TicketAnalysis(
            category=TicketCategory.ACCESS,
            priority=Priority.URGENT,
            key_points=["Can't access the dashboard"],
            required_expertise=["System Administrator"],
            sentiment=0.8,
            urgency_indicators=["asap"],
            business_impact="High",
            suggested_response_type="access_issue"
        )

        #sample expected response
        response_agent = ResponseAgent()
        context = {
            "name": "Yazan A",
            "feature": "admin dashboard",
            "diagnosis": "idk I think there is some permission problem here.",
            "resolution_steps": "Please try resetting your password.",
            "eta": "1.5 hours"
        }

        #checking if we received the expected response 
        response = await response_agent.generate_response(analysis, RESPONSE_TEMPLATES, context)
        self.assertIn("Yazan A", response.response_text)
        self.assertIn("admin dashboard", response.response_text)
    
    async def test_error_handling(self):
        processor = TicketProcessor()
        # Ticket with missing content should trigger error handling
        ticket = {"id": "TKT-007", "subject": "Empty ticket", "customer_info": {"role": "User", "name": "Jane Doe"}}
        # checking edge case here
        resolution = await processor.process_ticket(ticket, RESPONSE_TEMPLATES)
        self.assertEqual(resolution.ticket_id, "TKT-007")
        self.assertIn("error", resolution.response.response_text.lower())