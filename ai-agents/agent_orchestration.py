from data_classes import *


class TicketProcessor:
    def __init__(self):
        self.analysis_agent = TicketAnalysisAgent()
        self.response_agent = ResponseAgent()
        self.context = {}  

    async def process_ticket(self, ticket: SupportTicket,) -> TicketResolution:

        
