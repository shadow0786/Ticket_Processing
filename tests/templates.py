SAMPLE_TICKETS = [
    {
        "id": "TKT-001",
        "subject": "Cannot access admin dashboard",
        "content": """
Hi Support,
Since this morning I can't access the admin dashboard. I keep getting a 403 error.
I need this fixed ASAP as I need to process payroll today.
Thanks,
John Smith
Finance Director
""",
        "customer_info": {
            "role": "Admin",
            "plan": "Enterprise",
            "company_size": "250+",
            "name": "John Smith"
        }
    },
    {
        "id": "TKT-002",
        "subject": "Question about billing cycle",
        "content": """
Hello,
Our invoice shows billing from the 15th but we signed up on the 20th.
Can you explain how the pro-rating works?
Best regards,
Sarah Jones
""",
        "customer_info": {
            "role": "Billing Admin",
            "plan": "Professional",
            "company_size": "50-249",
            "name": "Sarah Jones"
        }
    }
]

EDGE_CASE_TICKETS = [
    {
        "id": "TKT-003",
        "subject": "URGENT: System down during demo",
        "content": """
System crashed during customer demo!!!
Call me ASAP: +1-555-0123
-Sent from my iPhone
""",
        "customer_info": {
            "role": "Sales Director",
            "plan": "Enterprise",
            "name": "Alex Brown"
        }
    }
]

AMBIGUOUS_TICKETS = [
    {
        "id": "TKT-004",
        "subject": "It's not working",
        "content": "Nothing works. Please help.",
        "customer_info": {
            "role": "User",
            "plan": "Basic",
            "name": "Chris Doe"
        }
    }
]

RESPONSE_TEMPLATES = {
    "access_issue": """
Hello {name},

I understand you're having trouble accessing {feature}. Let me help you resolve this.

{diagnosis}

{resolution_steps}

Priority Status: {priority_level}
Estimated Resolution: {eta}

Please let me know if you need any clarification.

Best regards,
Baguette Support
""",
    "billing_inquiry": """
Hi {name},

Thank you for your inquiry about {billing_topic}.

{explanation}

{next_steps}

If you have any questions, don't hesitate to ask.

Best regards,
Baguette Billing Team
""",
    "technical_issue": """
Hello {name},

We have received your technical issue report. Our technical team is reviewing the error details.

{diagnosis}

{resolution_steps}

Thanks for understanding and apologies for any inconvenience.

Priority: {priority_level}
ETA: {eta}

Best regards,
Technical Support Team
""",
    "feature_request": """
Hi {name},

Thank you for your feature request. We appreciate your feedback and are evaluating your suggestion.

{resolution_steps}

Best regards,
Product Team
""",
    "general_response": """
Hello {name},

Thank you for reaching out to us. We have received your request and will get back to you shortly.

Best regards,
Support Team
"""
}