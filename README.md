AI-Powered Customer Support Ticket Processing System

This repository contains an AI-powered system designed to process customer support tickets by analyzing their content, determining the correct category and priority, and generating appropriate responses. The system is composed of several modular components and robust unit tests to ensure high accuracy and reliability.


ai-ticket-processing/
├── README.md                 # Project documentation (this file)
├── requirements.txt          # Python dependencies (e.g., nltk, transformers)
├── main.py                   # Entry point: runs unit tests and processes sample tickets and starts interface for user input
├── data_classes.py           # Contains all the data classes and enums
├── ai_agents/
│   ├── __init__.py           # Package initializer for ai_agents
│   ├── ticket_analysis_agent.py  # Contains TicketAnalysisAgent class for analyzing tickets
│   ├── response_generation_agent.py         # Contains ResponseAgent class for generating responses
│   └── agent_orchestration.py       # Contains TicketProcessor class to orchestrate agents
└── tests/
    ├── __init__.py           # Package initializer for tests
    ├── test_agent.py        # Unit tests for ticket analysis and response and additional tests covering edge cases and algorithm
    ├── templates.py          # Response Templates


File & Class Descriptions

main.py - 

Purpose: Serves as the entry point for the application.
Functionality:
Discovers and runs all unit tests before proceeding with ticket processing.
Processes sample tickets using the TicketProcessor if tests pass.
Provides clear console output for both testing and ticket processing results.

ai_agents/ticket_analysis_agent.py - 

Class: TicketAnalysisAgent
Purpose: Analyzes ticket content to classify the ticket into one of four categories (BILLING, ACCESS, FEATURE, TECHNICAL) and to assign a priority.
Key Algorithms:
Category Detection:
Uses a keyword matching approach where each category has an associated list of keywords.
Counts keyword occurrences and tracks the index of the first occurrence.
Resolves ties by selecting the category whose keyword appears first.
Defaults to TECHNICAL if no keywords are found.
Priority Detection:
Checks for urgency keywords, business impact indicators, and high-level customer roles.
Uses a weighted scoring system:
1 point for urgency keywords.
1 point for business impact.
2 points for a high-level customer.
Priority is assigned as follows:
Score ≥ 3: URGENT
Score = 2: HIGH
Score = 1: MEDIUM
Score = 0: LOW

ai_agents/response_agent.py-

Class: ResponseAgent
Purpose: Generates a personalized response based on ticket analysis.
Key Features:
Selects response templates based on the analyzed ticket category.
Fills in dynamic placeholders (e.g., customer name, feature, diagnosis) and ensures lists (e.g., required expertise) are converted into readable strings.
Computes a confidence score using several factors (e.g., number of key points, sentiment analysis, urgency) and flags responses that may require human approval.

ai_agents/ticket_processor.py-

Class: TicketProcessor
Purpose: Orchestrates the overall workflow:
Calls the TicketAnalysisAgent to analyze the ticket.
Uses the ResponseAgent to generate a response based on the analysis.
Handles errors gracefully and maintains context for each ticket.

tests/ - 

Purpose: Contains robust unit tests to validate the behavior of the agents.
Files:

test_agents.py: Tests for basic functionality of ticket analysis and response generation. Includes around 10 test cases covering edge cases such as ambiguous tickets, multiple category triggers, and different priority scenarios. These tests ensure that the algorithms for determining category, priority, and business impact are working as expected.


Algorithms & Approaches

Category Detection Algorithm - 
Keywords: Each ticket category is associated with a set of keywords. For example:
BILLING: "billing", "invoice", "pro-rating", "account", "cost", "money", "payroll"
ACCESS: "admin dashboard", "access", "login", "403", "authentication", "security", "admin", "dashboard"
FEATURE: "feature", "request", "function", "characteristic"
TECHNICAL: "crash", "system", "failed", "technical error", "not working", "server", "down", "stuck"
Counting & Tie-Breaking:
Counts occurrences of keywords in the ticket content.
Tracks the first occurrence index for each category.
In case of a tie, the category whose keyword appears first is selected.
Defaults to TECHNICAL if no keywords are found.

Priority Detection Algorithm - 
Factors Considered:
Urgency Keywords: e.g., "ASAP", "urgent", "failed".
Business Impact: e.g., "payroll", "demo", "revenue".
High-Level Customer: e.g., roles like "CEO", "C-level", "Director".
Weighted Scoring:
1 point for urgency keywords.
1 point for business impact.
2 points for a high-level customer (weighted more heavily).
Priority Assignment:
Score ≥ 3: URGENT
Score = 2: HIGH
Score = 1: MEDIUM
Score = 0: LOW
Confidence Score Calculation (in Response Generation)

Components:
Key Points Factor: More key points may indicate a complex ticket.
Sentiment Factor: Uses the sentiment score (improved using VADER or transformer-based models).
Urgency Factor: Adjusts confidence for urgent tickets.
Usage: The combined score flags responses that may require human approval if the confidence is below a threshold.

Running Instructions

Clone the Repository:

git clone https://github.com/yourusername/ai-ticket-processing.git
cd ai-ticket-processing

Install Dependencies:

pip install -r requirements.txt

Note: This project uses libraries such as nltk (for VADER sentiment analysis) and optionally transformers if you opt for a transformer-based sentiment analyzer.


Run the Application:
python main.py


Robust Unit Testing
The project includes extensive unit tests to ensure that every aspect of the ticket processing logic works correctly:

Test Coverage:
Tests verify that tickets are correctly classified into categories based on keyword frequency and order.
Priority determination is validated using the weighted scoring system.
Edge cases, such as ambiguous tickets or mixed keyword triggers, are thoroughly tested.
Business impact detection is also validated.
Test Files:
test_agents.py: Covers the core functionality.
test_additional_cases.py: Includes around 10 test cases focusing on edge cases and algorithm nuances.
This robust testing suite ensures that modifications to the algorithms are quickly validated, keeping the system robust and reliable.

Conclusion
This system demonstrates a modular and extensible design for processing customer support tickets. By leveraging keyword-based classification, a weighted scoring system for priority detection, and robust unit testing, the solution is both maintainable and scalable. Contributions and further enhancements are welcome!
