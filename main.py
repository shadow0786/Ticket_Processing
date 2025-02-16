import unittest
from data_classes import *
from ai_agents.agent_orchestration import TicketProcessor
from tests.templates import *
import asyncio

## run main class to run everything
if __name__ == "__main__":
    # Run unit tests
    unittest.main(exit=False)
    
    # Optionally process and print sample ticket resolutions. This will show output , help in debugging and give us idea of our code accuracy.
    async def process_sample_tickets():
        processor = TicketProcessor()
        all_tickets = SAMPLE_TICKETS + EDGE_CASE_TICKETS + AMBIGUOUS_TICKETS
        for ticket in all_tickets:
            resolution = await processor.process_ticket(ticket, RESPONSE_TEMPLATES)
            print("Ticket ID:", resolution.ticket_id)
            print("Analysis:", resolution.analysis)
            print("Response:\n", resolution.response.response_text)
            print("-" * 50)
    
    asyncio.run(process_sample_tickets())