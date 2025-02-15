from data_classes import *

class TicketAnalysisAgent:
    async def analyze_ticket(self, ticket_content: str, customer_info: Optional[dict] = None) -> TicketAnalysis:

        # Convert the ticket content to lowercase to make the search case-insensitive.
        content_lowercase = ticket_content.lower()

        # Define urgency keywords. I have added some extra keywords from those mentioned in the document ! 
        urgency_keywords = ["asap", "urgent", "emergency" , "immediately", "help"  , "crashed", "error",  "system down" ,"failed"]

        # Check if any urgency keywords are present in the ticket content.
        urgency_detection = []
        for word in urgency_keywords:
            if word in content_lowercase:
                urgency_detection.append(word)

    # Determine the category of the ticket based on the presence of certain words . 
    # For extra work in future would like to tackle this part with advanced nlp and sentiment analysis using llms or sentiment packages to understand context.

        billing = ["billing" , "invoice" , "pro-rating" , "account" , "cost" , "money"]
        access = ["admin dashboard" , "access" , "login" , "403" , "authentication" , "security" , "admin" , "dashboard"]
        feature = ["feature" , "request" , "function" , "characteristic"]
        technical = ["crash" , "system" , "failed" , "technical error" , "not working" , "server" , "down" , "stuck"]

    # If the ticket mentions billing-related terms, categorize it as BILLING.
        if any(word in content_lowercase for word in billing):
            category = TicketCategory.BILLING

        # If the ticket is about access issues or login problems, categorize it as ACCESS.
        elif any(word in content_lowercase for word in access):
            category = TicketCategory.ACCESS

        # If the ticket is about feature requests, categorize it as FEATURE.
        elif any(word in content_lowercase for word in feature):
            category = TicketCategory.FEATURE

        # If the ticket mentions errors, crashes, or system issues, categorize it as TECHNICAL.
        elif any(word in content_lowercase for word in technical):
            category = TicketCategory.TECHNICAL

        # If none of the above conditions are met, default to TECHNICAL.
        else:
            category = TicketCategory.TECHNICAL  # Default category

    





    
        
