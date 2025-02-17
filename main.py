import unittest
from data_classes import *
from ai_agents.agent_orchestration import TicketProcessor
from tests.templates import *
import asyncio
from tests import test_agent

def interactive_cli():
    ## creating an iterative ui where user can enter info like query , their job position , etc. and a sample ticket analysis 
    # along with a sample response would be generated to show how data is being processed , analysed and stored. 

    # take in customer details one by one
    print("Welcome to the Ticket Processing CLI.")
    print("Enter 'exit' at any prompt to quit.")
    ticket_processor = TicketProcessor()
    ticket_counter = 1
    while True:
        role = input("Enter customer role: ").strip()
        if role.lower() == 'exit':
            break

        content = input("Enter ticket content: ").strip()
        if content.lower() == 'exit':
            break

        subject = input("Enter ticket subject (or leave blank for default): ").strip()
        if subject.lower() == 'exit':
            break
        if not subject:
            subject = "Customer Query"

        customer_name = input("Enter customer name (or leave blank for 'Customer'): ").strip()
        if customer_name.lower() == 'exit':
            break
        if not customer_name:
            customer_name = "Customer"

        # Create the ticket dictionary.
        ticket = {
            "id": f"TKT-CLI-{ticket_counter}",
            "subject": subject,
            "content": content,
            "customer_info": {
                "role": role,
                "name": customer_name
            }
        }

        # Process the ticket asynchronously.
        resolution = asyncio.run(ticket_processor.process_ticket(ticket, RESPONSE_TEMPLATES))

        # Display Ticket Analysis before Response
        print("\nTicket Created:")
        print(f"Ticket ID: {resolution.ticket_id}")
        print("\n--- Ticket Analysis ---")
        print(f"Category: {resolution.analysis.category}")
        print(f"Priority: {resolution.analysis.priority}")
        print(f"Key Points: {', '.join(resolution.analysis.key_points) if resolution.analysis.key_points else 'None'}")
        print(f"Required Expertise: {', '.join(resolution.analysis.required_expertise) if resolution.analysis.required_expertise else 'None'}")
        print(f"Sentiment Score: {resolution.analysis.sentiment}")
        print(f"Business Impact: {resolution.analysis.business_impact}")
        print(f"Follow-up Prediction: {resolution.analysis.follow_up_prediction}")
        
        # show ticket response
        print("\n--- Ticket Response ---")
        print(resolution.response.response_text)
        print("-" * 50)
        ticket_counter += 1

    print("Exiting CLI. Goodbye!")

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

    interactive_cli()


