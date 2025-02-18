# AI Ticket Processing System

This repository contains an AI-powered system designed to process customer support tickets by analyzing their content, determining the correct category and priority, and generating appropriate responses. The system is composed of several modular components and includes robust unit tests to ensure high accuracy and reliability.

## Project Structure

```plaintext
ai-ticket-processing/
├── README.md                 # Project documentation (this file)
├── requirements.txt          # Python dependencies (e.g., nltk, transformers)
├── main.py                   # Entry point: runs unit tests, processes sample tickets, and starts user input interface
├── data_classes.py           # Contains all data classes and enums
├── ai_agents/
│   ├── __init__.py           # Package initializer for ai_agents
│   ├── ticket_analysis_agent.py  # Contains TicketAnalysisAgent class for analyzing tickets
│   ├── response_generation_agent.py  # Contains ResponseAgent class for generating responses
│   └── agent_orchestration.py  # Contains TicketProcessor class to orchestrate agents
└── tests/
    ├── __init__.py           # Package initializer for tests
    ├── test_agent.py         # Unit tests for ticket analysis, response generation, and additional edge case tests
    ├── templates.py          # Response templates used for generating replies
```

## File & Class Descriptions

### `main.py`
- **Purpose:** Serves as the entry point for the application.
- **Functionality:**
  - Discovers and runs all unit tests before proceeding with ticket processing.
  - Processes sample tickets using the `TicketProcessor` if tests pass.
  - Provides clear console output for both testing and ticket processing results.

### `data_classes.py`
- **Purpose:** Contains all the data classes and enums used throughout the system.
- **Key Classes:**
  - **TicketAnalysis:** Holds analysis information such as category, priority, key points, required expertise, sentiment score, business impact, and follow-up prediction.
  - **ResponseSuggestion:** Contains the generated response details including response text, confidence score, and suggested actions.
  - **TicketResolution:** Aggregates the analysis and response for a given ticket.
  - **Enums:** Such as `TicketCategory` and `Priority` for classification and priority levels.

### `ai_agents/ticket_analysis_agent.py`
- **Class:** `TicketAnalysisAgent`
- **Purpose:** Analyzes ticket content to classify it into one of four categories (BILLING, ACCESS, FEATURE, TECHNICAL) and to assign a priority.
- **Key Algorithms:**
  - **Category Detection:**
    - Uses keyword matching where each category has an associated list of keywords.
    - Counts keyword occurrences and tracks the index of the first occurrence.
    - Resolves ties by selecting the category whose keyword appears first.
    - Defaults to TECHNICAL if no keywords are found.
  - **Priority Detection:**
    - Considers urgency keywords, business impact indicators, and high-level customer roles.
    - Uses a weighted scoring system:
      - **1 point** for urgency keywords.
      - **1 point** for business impact.
      - **2 points** for a high-level customer.
    - Priority is assigned as:
      - **Score ≥ 3:** URGENT
      - **Score = 2:** HIGH
      - **Score = 1:** MEDIUM
      - **Score = 0:** LOW

### `ai_agents/response_generation_agent.py`
- **Class:** `ResponseAgent`
- **Purpose:** Generates a personalized response based on the ticket analysis.
- **Key Features:**
  - Selects response templates based on the analyzed ticket category.
  - Fills in dynamic placeholders (e.g., customer name, feature, diagnosis) and converts list values into readable strings.
  - Computes a confidence score using factors such as key points, sentiment, and urgency, flagging responses that may require human approval.

### `ai_agents/agent_orchestration.py`
- **Class:** `TicketProcessor`
- **Purpose:** Orchestrates the overall workflow of ticket processing.
- **Functionality:**
  - Invokes `TicketAnalysisAgent` to analyze the ticket.
  - Invokes `ResponseAgent` to generate a response based on the analysis.
  - Handles errors gracefully and maintains context for each ticket.

### `tests/`
- **Purpose:** Contains robust unit tests to validate the functionality of the system.
- **Files:**
  - **`test_agent.py`:** Unit tests covering core functionality, edge cases, and algorithm correctness.
  - **`templates.py`:** Contains response templates used for testing and response generation.

## Algorithms & Approaches

### Category Detection
- **Keywords:** Each ticket category is associated with a set of keywords. For example:
  - **BILLING:** "billing", "invoice", "pro-rating", "account", "cost", "money", "payroll"
  - **ACCESS:** "admin dashboard", "access", "login", "403", "authentication", "security", "admin", "dashboard"
  - **FEATURE:** "feature", "request", "function", "characteristic"
  - **TECHNICAL:** "crash", "system", "failed", "technical error", "not working", "server", "down", "stuck"
- **Method:**
  - Counts occurrences of each category’s keywords in the ticket content.
  - Tracks the first occurrence index for each category.
  - In case of a tie, selects the category with the earliest occurring keyword.
  - Defaults to TECHNICAL if no keywords are found.

### Priority Detection
- **Factors Considered:**
  - **Urgency Keywords:** e.g., "asap", "urgent", "emergency" , "immediately" , "fast".
  - **Business Impact:** e.g., "payroll", "demo" , "impact on business" , "payment" , "system is down" , "business problem" , "emergency" , "revenue" , "invoice" , "system crash" , "bill".
  - **High-Level Customer:** e.g., "director", "admin", "c-level", "ceo", "cto", "manager" , "financial" , "vp" , "cfo" , "md".
- **Scoring System:**
  - **1 point** for urgency keywords.
  - **1 point** for business impact.
  - **2 points** for a high-level customer.
- **Priority Assignment:**
  - **Score ≥ 3:** URGENT
  - **Score = 2:** HIGH
  - **Score = 1:** MEDIUM
  - **Score = 0:** LOW

### Confidence Score Calculation (in Response Generation)
- **Components:**
  - **Key Points Factor:** More key points might indicate a complex ticket.
  - **Sentiment Factor:** Utilizes a sentiment score from libraries like VADER or transformer-based models.
  - **Urgency Factor:** Adjusts the score for urgent tickets.
- **Usage:** A lower combined confidence score flags the response as potentially requiring human approval.

## Running Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/ai-ticket-processing.git
   cd ai-ticket-processing
   ```

2. **Set Up the Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   > **Note:** This project uses libraries such as `nltk` (for VADER sentiment analysis) and optionally `transformers` if you opt for a transformer-based sentiment analyzer.

4. **Run Unit Tests:**

   - To run all tests, execute:

     ```bash
     python -m unittest discover
     ```

   - Alternatively, run `main.py` which will first execute all tests and then launch the interactive CLI if tests pass.

5. **Run the Application:**

   ```bash
   python main.py
   ```

## Robust Unit Testing

The project includes extensive unit tests to ensure every aspect of the ticket processing logic works correctly:

- **Test Coverage:**
  - Verifies correct ticket classification into categories based on keyword frequency and order.
  - Validates the priority detection using the weighted scoring system.
  - Tests edge cases such as ambiguous tickets or overlapping keyword triggers.
  - Confirms that business impact is correctly identified.
- **Test Files:**
  - **`test_agent.py`:** Covers core functionalities and edge cases.
  - **`templates.py`:** Provides response templates for testing and response generation.

This comprehensive testing suite ensures that any changes to the algorithms are promptly validated, keeping the system robust and reliable.

## Conclusion

This system demonstrates a modular and extensible design for processing customer support tickets. By leveraging keyword-based classification, a weighted scoring system for priority detection, and robust unit testing, the solution is both maintainable and scalable. 


