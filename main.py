import unittest
from data_classes import *
from ai_agents.agent_orchestration import TicketProcessor
from tests.templates import *
import asyncio
from tests import test_agent

## run main class to run everything
if __name__ == "__main__":
    
    print("\nRunning Unit Tests...\n")
    
    # Discover and run tests from all test files in the 'tests' folder
    test_loader = unittest.defaultTestLoader
    test_suite = test_loader.discover('tests')  # Ensure tests folder exists
    test_runner = unittest.TextTestRunner()
    test_results = test_runner.run(test_suite)

    # If tests fail, prevent ticket processing from running
    if not test_results.wasSuccessful():
        print("\n❌ Tests failed! Fix the errors before processing tickets.")
    else:
        print("\n✅ All tests passed! Proceeding with ticket processing...\n")

    
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