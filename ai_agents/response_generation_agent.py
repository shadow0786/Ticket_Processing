from data_classes import *

class ResponseAgent:
    async def generate_response(self, ticket_analysis: TicketAnalysis, response_templates: dict[str, str], context: dict[str, any]) -> ResponseSuggestion:
       
        # Select template based on the suggested response type from analysis
        template_key = ticket_analysis.suggested_response_type


        template = response_templates.get(template_key)

        # if response type is general then use this - 
        if not template:
            # Use a generic fallback template
            template = ("Hello {name},\n\nThank you for contacting support. "
                        "We are looking into your issue and would get to you as soon as possible.\n\nBest regards,\nSupport Team")
            
        
        # Base confidence starts high 0.95 and is adjusted by several factors like rore key points may indicate a more complex ticket.
        # So we can assume that if there are many key points, our confidence might be lower.
        key_points_count = len(ticket_analysis.key_points)
        key_points_factor = max(0.7, 1.0 - (key_points_count * 0.05))  # Reduce confidence by 5% per key point, but not below 0.7

        # We also take into account the the sentiment score (assumed to be 0 to 1),
        # where a higher positive sentiment suggests more calm and easier resolution.
        sentiment_factor = ticket_analysis.sentiment

        # Urgent tickets might be more challenging to resolve quickly.
        urgency_factor = 0.88 if ticket_analysis.priority == Priority.URGENT else 1.0

        # Combine factors into a final confidence score
        base_confidence = 0.95
        confidence_score = base_confidence * key_points_factor * sentiment_factor * urgency_factor

        # Determine if approval is required: if the confidence score is below a threshold flag it for approval.
        # In our case I chose 0.80 to be on safe side 
        requires_approval = confidence_score < 0.80

        
        # Map response type to suggested actions based on response type
        action_mapping = {
            "access_issue": ["please reset your password and check user permissions with system administrator while the support team looks into the issue from their end."],
            "billing_inquiry": ["please verify billing details and contact billing department. We would also discuss this query with the Billing Manager and get back to you. "],
            "technical_issue": ["contact technical support and note down the error logs. The support team is already looking into problem and will get back to you with a solution soon."],
            "feature_request": ["please forward all product feature requests to customer relations team and they would review it."],
            "general_response": ["we are looking into the problem and would get back to you soon."]
        }

        # let action value and default incase no other suitable option 
        suggested_actions = action_mapping.get(ticket_analysis.suggested_response_type, ["Review ticket/error details and please contact customer support"])

        #return response suggestion

        # here we add template values using context or default values incase some fields are not available
        template_vals = {
            "name": context.get("name", "Customer_Name"),
            "feature": context.get("feature","the admin dashboard or admin functions") ,
            "diagnosis": context.get("diagnosis","We are forwarding the error and diagnosis report to " + ticket_analysis.required_expertise[0]),
            "resolution_steps": context.get("resolution_steps" , "For the next steps, " + suggested_actions[0]),
            "priority_level": ticket_analysis.priority.name,
            "eta": context.get("eta", "As Soon As Possible"),
            "billing_topic": context.get("billing_topic" , "billing and payments"),
            "explanation": context.get("explanation" ,"We are reviewing your invoice and payment records."),
            "next_steps": context.get("next_steps" , "For the next steps, please verify billing details and contact billing department. We would also discuss this query with the Billing and Account Managers and get back to you soon.")
        }

        # here we use try and except statements to handle errors in data entry and prevent whole system from crashing 
        try:
            response_text = template.format(**template_vals)
        except Exception as e:
            response_text = "Error formatting response template."

        return ResponseSuggestion(
        response_text=response_text,
        confidence_score=confidence_score,
        requires_approval=requires_approval,
        suggested_actions=suggested_actions

        )