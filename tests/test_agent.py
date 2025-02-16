import unittest
from ai_agents.ticket_analysis_agent import TicketAnalysisAgent
from data_classes import *
from ai_agents.response_generation_agent import ResponseAgent
from ai_agents.agent_orchestration import TicketProcessor
from tests.templates import *


## test class to initialise and conduct the test
## I used the default test cases provided to me and have also created my own 10 test cases to check how robust the code and algorithm is. 

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

    ##### 10 additional tests with different scenarios to test the algorithm for business impact , ticket category and priority level. 
    
    async def test_error_handling(self):
        processor = TicketProcessor()
        # Ticket with missing content should trigger error handling
        ticket = {"id": "TKT-007", "subject": "Empty ticket", "customer_info": {"role": "User", "name": "Jane Doe"}}
        # checking edge case here
        resolution = await processor.process_ticket(ticket, RESPONSE_TEMPLATES)
        self.assertEqual(resolution.ticket_id, "TKT-007")
        self.assertIn("error", resolution.response.response_text.lower())

    async def test_billing_ticket_with_invoice(self):
        # Ticket with billing keywords and invoice => High business impact
        agent = TicketAnalysisAgent()
        content = "I have an issue with my invoice and need help with my billing."
        customer_info = {"role": "Customer"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.BILLING)
        self.assertEqual(analysis.priority, Priority.URGENT)
        self.assertEqual(analysis.business_impact, "High")

    async def test_access_ticket_without_urgency(self):
        # Ticket about login issues with no urgency keywords
        agent = TicketAnalysisAgent()
        content = "I cannot login to my account."
        customer_info = {"role": "User"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.ACCESS)
        self.assertEqual(analysis.priority, Priority.LOW)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_technical_ticket_with_error(self):
        # Ticket describing an error and system crashes (urgency detected)
        agent = TicketAnalysisAgent()
        content = "We are experiencing an error with the system crashing frequently."
        customer_info = {"role": "Technician"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.TECHNICAL)
        self.assertEqual(analysis.priority, Priority.HIGH)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_feature_request_ticket(self):
        # Ticket that clearly requests a new feature
        agent = TicketAnalysisAgent()
        content = "I would like to request a new feature that allows for better reporting."
        customer_info = {"role": "User"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.FEATURE)
        self.assertEqual(analysis.priority, Priority.LOW)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_access_ticket_with_urgency(self):
        # Access issue with explicit urgency words ("ASAP", "can't access")
        agent = TicketAnalysisAgent()
        content = "I can't access the admin dashboard, please fix this ASAP."
        customer_info = {"role": "User"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.ACCESS)
        self.assertEqual(analysis.priority, Priority.HIGH)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_billing_ticket_with_payroll(self):
        # Billing ticket where invoice and payroll are mentioned, triggering urgent priority
        agent = TicketAnalysisAgent()
        content = "My invoice is incorrect and I need it corrected before payroll processing."
        customer_info = {"role": "Customer"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.BILLING)
        self.assertEqual(analysis.priority, Priority.URGENT)
        self.assertEqual(analysis.business_impact, "High")

    async def test_technical_ticket_system_down_with_director(self):
        # Technical issue with system down and a high-level customer role should be urgent
        agent = TicketAnalysisAgent()
        content = "The system is down and I'm getting a 500 error."
        customer_info = {"role": "Director"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.TECHNICAL)
        self.assertEqual(analysis.priority, Priority.URGENT)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_ambiguous_ticket(self):
        # A vague ticket with no clear keywords, so it defaults to technical and low impact
        agent = TicketAnalysisAgent()
        content = "Nothing works at all. I'm confused and need help."
        customer_info = {"role": "User"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.TECHNICAL)
        self.assertEqual(analysis.priority, Priority.LOW)
        self.assertEqual(analysis.business_impact, "Low")

    async def test_mixed_category_ticket(self):
        # Ticket with both billing and technical terms; billing check comes first so it should be billing.
        agent = TicketAnalysisAgent()
        content = "I received an error on my invoice generation process."
        customer_info = {"role": "Customer"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.BILLING)
        self.assertEqual(analysis.priority, Priority.URGENT)
        self.assertEqual(analysis.business_impact, "High")

    async def test_urgent_ambiguous_ticket(self):
        # Ticket with urgent language but no clear category words should default to technical with high priority.
        agent = TicketAnalysisAgent()
        content = "URGENT: Something went wrong, please address immediately!"
        customer_info = {"role": "User"}
        analysis = await agent.analyze_ticket(content, customer_info)
        self.assertEqual(analysis.category, TicketCategory.TECHNICAL)
        self.assertEqual(analysis.priority, Priority.HIGH)
        self.assertEqual(analysis.business_impact, "Low")

