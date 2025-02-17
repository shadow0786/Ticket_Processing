from data_classes import *
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
# Ensure VADER lexicon is downloaded (run this once)
nltk.download('vader_lexicon')
from collections import defaultdict


class TicketAnalysisAgent:
    async def analyze_ticket(self, ticket_content: str, customer_info: Optional[dict] = None) -> TicketAnalysis:

        # Convert the ticket content to lowercase to make the search case-insensitive.
        # For extra in future could use advacned tokenisation and stemming with stop word removal for more in depth analysis
        content_lowercase = ticket_content.lower()

    # Determine the category of the ticket based on the presence of certain words . 
    # For extra work in future would like to tackle this part with advanced nlp and sentiment analysis using llms or sentiment packages to understand context.

        billing = ["billing" , "invoice" , "pro-rating" , "account" , "cost" , "money" , "payroll"]
        access = ["admin dashboard" , "access" , "login" , "403" , "authentication" , "security" , "admin" , "dashboard"]
        feature = ["feature" , "request" , "function" , "characteristic"]
        technical = ["crash" , "system" , "failed" , "technical error" , "not working" , "server" , "down" , "stuck"]

        category_keywords = {
        TicketCategory.BILLING: billing,
        TicketCategory.ACCESS: access,
        TicketCategory.FEATURE: feature,
        TicketCategory.TECHNICAL: technical,
    }
    # Algorithm to assign categories -
    # first count the occurrences of category keywords and then assign the category based on the highest count. 
    # In case of a tie, it selects the category whose word appears first.

    # Count occurrences of each category
        category_counts = defaultdict(int)
        first_occurrence = {}

        for category, keywords in category_keywords.items():
            for word in keywords: # iterate over words from each category
                count = content_lowercase.count(word)  # Count occurrences
                if count > 0:
                    category_counts[category] += count
                    index = content_lowercase.find(word) # store index of word in content
                    if category not in first_occurrence or index < first_occurrence[category]:
                        first_occurrence[category] = index  # Track first occurrence index

        # Get the category with max occurrences
        if category_counts:
            max_count = max(category_counts.values())  # Get highest count

            # Filter categories that have the max count
            equal_categories = [cat for cat, count in category_counts.items() if count == max_count]

            # incase of tie choose the category whose word appears first
            category = min(equal_categories, key=lambda cat: first_occurrence[cat])
        else:
            category = TicketCategory.TECHNICAL  # Default category if no keywords found


        # Determine priority based on urgency , business impact and customer role. Keep default Low Priority
        # I have done basic priority identification based on words present for each priority category. There is some overlap also .
        #  However for extra in future we would use advanced sentiment analysis and nlp packages along with LLM embedding to understand context.

        priority = Priority.LOW

        # Define urgency keywords. I have added some extra keywords from those mentioned in the document ! 
        urgency_keywords = ["asap", "urgent", "emergency" , "immediately" , "fast"]

        # Check if any urgency keywords are present in the ticket content.
        urgency_detection = any(keyword in content_lowercase for keyword in urgency_keywords)

        # high value customers
        customer_priority = ["director", "admin", "c-level", "ceo", "cto", "manager" , "financial" , "vp" , "cfo" , "md"]
        
        # check if the customer role indicates high-level like C-suite
        customer_is_high_level = False
        if customer_info:
            role = customer_info.get("role", "").lower()
            if any(keyword in role for keyword in customer_priority):
                customer_is_high_level = True
        
        # Check for business-impact keywords. Initial default impact set to low. 
        impact_words = ["payroll", "demo" , "impact on business" , "payment" , "system is down" , "business problem" , "emergency" , "revenue" , "invoice" , "system crash" , "bill"]
        business_impact_present = any(word in content_lowercase for word in impact_words)
        business_impact = "High" if business_impact_present else "Low"

        # Count how many priority factors are present
        score = 0
        if urgency_detection:
            score += 1
        if business_impact_present:
            score += 1
        if customer_is_high_level: ## give more importance to high level customers queries. A senior position customer is always atleast High Priority
            score += 2

        # Assign priority based on score:
        # if score is >= 3 : URGENT
        # - score is 2 : HIGH
        # - score is 1: MEDIUM 
        # - score is 0 : LOW

        if score >= 3:
            priority = Priority.URGENT
        elif score == 2:
            priority = Priority.HIGH
        elif score == 1:
            priority = Priority.MEDIUM
        else:
            priority = Priority.LOW 


        # Extract key sentences with keywords

        #split text on new line
        sentences = [s.strip() for s in ticket_content.split("\n") if s.strip()]
        key_points = []

        for sentence in sentences:

            #store sentences with urgent keywords
            if any(keyword in sentence.lower() for keyword in urgency_keywords):
                key_points.append(sentence)
            
            #store important sentences related to billing
            elif category == TicketCategory.BILLING and any(keyword in sentence.lower() for keyword in billing):
                key_points.append(sentence)

            #store important sentences related to access
            elif category == TicketCategory.ACCESS and any(keyword in sentence.lower() for keyword in access):
                key_points.append(sentence)
            
            #store important sentences related to features
            elif category == TicketCategory.FEATURE and any(keyword in sentence.lower() for keyword in feature):
                key_points.append(sentence)
            
            #store important sentences related to technical stuff
            elif category == TicketCategory.TECHNICAL and any(keyword in sentence.lower() for keyword in technical):
                key_points.append(sentence)


        if not key_points:
            key_points = sentences[:3]  # store first 3 sentences if no category defined 

        # Assign the correct support team
        support_expertise = {
            TicketCategory.ACCESS: ["System Administrator" , "Access Manager"],
            TicketCategory.BILLING: ["Billing accountant", "Account Manager" , "Financial Manager"],
            TicketCategory.TECHNICAL: ["Technical Support Engineer" , "Customer Support"],
            TicketCategory.FEATURE: ["Product Manager", "Developer" , "Project Manager"]
        }
        # determine support and if no category send to general support 
        required_expertise = support_expertise.get(category, ["General Support"])
        
        ## Advanced extra sentiment analysis using vader package to determine positive or negative sentiment of ticket data 
        # Initialize VADER SentimentIntensityAnalyzer
        sia = SentimentIntensityAnalyzer()
        
        # Get sentiment scores
        sentiment_scores = sia.polarity_scores(ticket_content)
        sentiment = (sentiment_scores["compound"] + 1) / 2  # Normalize to scale 0 to 1
        
        # Map category to suggested response type
        mapping_response = {
            TicketCategory.ACCESS: "access_issue",
            TicketCategory.BILLING: "billing_inquiry",
            TicketCategory.TECHNICAL: "technical_issue",
            TicketCategory.FEATURE: "feature_request"
        }
        #incase no category so general response
        suggested_response_type = mapping_response.get(category, "general_response")

        # Extra feature - Follow-up Prediction based on category and sentiment
        follow_up_prediction = ""
        if category == TicketCategory.BILLING:
            follow_up_prediction = "The client may ask for more information about invoices or payment methods."
        elif category == TicketCategory.ACCESS:
            follow_up_prediction = "The customer might request additional troubleshooting steps or more privileged access."
        elif category == TicketCategory.TECHNICAL:
            follow_up_prediction = "The customer might ask for further technical support ."
        elif category == TicketCategory.FEATURE:
            follow_up_prediction = "The customer might inquire about the product roadmap or feature release timeline."
        if sentiment < 0.4:
            follow_up_prediction += "The customer is stressed as their issue seems to be complicated and may need to be escalated to higher authorities."

        

        #returning all required values 
        return TicketAnalysis(
            category=category,
            priority=priority,
            key_points=key_points,
            required_expertise=required_expertise,
            sentiment=sentiment,
            urgency_indicators=urgency_detection,
            business_impact=business_impact,
            suggested_response_type=suggested_response_type ,
            follow_up_prediction=follow_up_prediction
        )

        

    





    
        
