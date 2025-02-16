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
            
        
        # here we add template values using context or default values incase some fields are not available
        template_vals = {
            "name": context.get("name", "Customer_Name"),
            "feature": context.get("feature", "Ticket_Processing"),
            "diagnosis": context.get("diagnosis", "Unidentified Issue (Special Case)"),
            "resolution_steps": context.get("resolution_steps", "Hello , we are looking into your problem and would get back to you soon ! "),
            "priority_level": ticket_analysis.priority.name,
            "eta": context.get("eta", "As soon as Possible"),
            "billing_topic": context.get("billing_topic", "your billing queries"),
            "explanation": context.get("explanation", "We are reviewing your invoice details."),
            "next_steps": context.get("next_steps", "We will get in touch soon with more details")
        }

        # here we use try and except statements to handle errors in data entry and prevent whole system from crashing 
        try:
            response_text = template.format(**template_vals)
        except Exception as e:
            response_text = "Error formatting response template."
        
        # Dummy confidence score and determine if approval is required
        confidence_score = 0.9
        requires_approval = (ticket_analysis.priority == Priority.URGENT)
        
        # Map response type to suggested actions based on response type
        action_mapping = {
            "access_issue": ["Please Reset password", "Check user permissions with System Administrator"],
            "billing_inquiry": ["Please Verify Billing details", "Contact billing department"],
            "technical_issue": ["Contact Technical Support", "Check error logs"],
            "feature_request": ["Please forward requests to customer relations team"],
            "general_response": ["Follow up with customer"]
        }

        # let action value and default incase no other suitable option 
        suggested_actions = action_mapping.get(ticket_analysis.suggested_response_type, ["Review ticket/error details and please contact customer support"])

        #return response suggestion

        return ResponseSuggestion(
        response_text=response_text,
        confidence_score=confidence_score,
        requires_approval=requires_approval,
        suggested_actions=suggested_actions

        )