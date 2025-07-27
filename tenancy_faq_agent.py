# agents/tenancy_faq_agent.py

import random
from typing import Dict, List, Tuple, Optional
import re
from utils import get_gemini_response

class TenancyFAQAgent:
    """
    Agent specialized in handling tenancy law questions and rental guidance
    """

    def process_request(self, text: str, location: Optional[str] = None, context: Dict = None) -> Tuple[str, float]:
        """
        Process tenancy-related questions using Gemini LLM

        Args:
            text: User question
            location: User's location for specific laws
            context: Conversation context

        Returns:
            Tuple of (response_text, confidence_score)
        """

        prompt = self._build_gemini_prompt(text, location, context)

        try:
            gemini_response = get_gemini_response(prompt)
            response_text, confidence = self._parse_gemini_response(gemini_response)
            return response_text, confidence
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Sorry, I couldn't process your request at the moment. Please try again later.", 0.0

    def _build_gemini_prompt(self, text: str, location: Optional[str], context: Dict) -> str:
        """
        Build the prompt for the Gemini model.
        """
        prompt = f"You are a helpful AI assistant specializing in tenancy law and rental guidance. Provide comprehensive and accurate information based on the user's query.

"""

        if location:
            prompt += f"Consider the laws and regulations specific to {location}.

"

        if context:
            prompt += f"Here is some recent conversation history for context:
{json.dumps(context)}

"

        prompt += f"User query: {text}

"
        prompt += "Please provide a detailed response covering the relevant legal aspects, tenant rights, landlord responsibilities, and recommended next steps. Format your response clearly with headings and bullet points."

        return prompt

    def _parse_gemini_response(self, response: str) -> Tuple[str, float]:
    
        # Basic parsing: assume the entire response is the text and assign a default confidence.
        # More sophisticated parsing would be needed for structured responses from Gemini.
        return response, 0.8

    def get_emergency_resources(self, location: Optional[str] = None) -> str:          

        """Get emergency tenant resources (can be potentially enhanced by Gemini later)"""
        response_parts = []
        response_parts.append("🚨 **Emergency Tenant Resources**
")

        response_parts.append("**Immediate Help:**")
        response_parts.append("• Contact local housing authority")
        response_parts.append("• Reach out to tenant rights organizations")
        response_parts.append("• Call 211 for local resource referrals")
        response_parts.append("• Contact legal aid societies for free legal help")
        response_parts.append("")

        if location:
            response_parts.append(f"**{location}-Specific Resources:**")
            response_parts.append("• Search '[your city] tenant rights organization'")
            response_parts.append("• Look up '[your state] housing authority'")
            response_parts.append("• Contact '[your area] legal aid'")
        else:
            response_parts.append("**How to Find Local Help:**")
            response_parts.append("• Search 'tenant rights [your city]'")
            response_parts.append("• Contact your city's housing department")
            response_parts.append("• Look up state tenant protection agencies")

        response_parts.append("")
        response_parts.append("**If facing illegal eviction or harassment:**")
        response_parts.append("• Document everything (photos, messages, recordings if legal)")
        response_parts.append("• File complaints with housing authorities")
        response_parts.append("• Seek immediate legal representation")
        response_parts.append("• Know that self-help evictions are illegal in most places")

        return "
".join(response_parts)

    def generate_document_template(self, document_type: str) -> str:
        """
        Generate template documents for common tenant needs (can be potentially enhanced by Gemini later)
        """

        templates = {
            'repair_request': """
**Repair Request Letter Template**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

I am writing to formally request repairs to my rental unit at [Property Address], Unit [Number].

**Issues requiring attention:**
• [Describe issue 1 in detail]
• [Describe issue 2 in detail]

These issues affect the habitability of the property and require prompt attention. Please arrange for repairs within a reasonable timeframe as required by law.

I am available to provide access to the unit. Please contact me at [Phone] or [Email] to schedule.

Thank you for your prompt attention to this matter.

Sincerely,
[Your Name]
[Date]

**Keep a copy for your records**
""",

            'notice_to_vacate': """
**Notice to Vacate Template**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

This letter serves as my formal [30/60] day notice to vacate the rental property located at [Property Address], Unit [Number].

**Move-out Details:**
• Last day of occupancy: [Date]
• Final rent payment through: [Date]
• Forwarding address: [New Address]

I request to schedule a pre-move-out inspection and will ensure the property is returned in good condition, normal wear and tear excepted.

Please return my security deposit of $[Amount] to my forwarding address within the timeframe required by law.

Thank you for your cooperation.

Sincerely,
[Your Name]
[Current Date]
""",

            'deposit_demand': """
**Security Deposit Return Demand Letter**

[Date]

[Landlord Name]
[Landlord Address]

Dear [Landlord Name],

I am writing to formally request the return of my security deposit for the property at [Property Address], which I vacated on [Move-out Date].

**Deposit Details:**
• Amount paid: $[Amount]
• Date paid: [Date]
• Days since move-out: [Number]

According to [State] law, security deposits must be returned within [timeframe] days. As this period has passed, I am requesting immediate return of my full deposit.

If deductions were made, please provide an itemized list with receipts as required by law. I believe I am entitled to the full amount as the property was left in good condition.

Please send the deposit to: [Forwarding Address]

I expect resolution within [timeframe] or I may pursue legal remedies available under state law.

Sincerely,
[Your Name]
[Date]
"""
        }

        return templates.get(document_type, "Template not found. Available templates: repair_request, notice_to_vacate, deposit_demand")

    def get_legal_resources_by_state(self, state: str) -> str:
        """
        Get legal resources specific to a state (can be potentially enhanced by Gemini later)
        """

        # This would be expanded with real resources in production
        state_resources = {
            'california': {
                'housing_authority': 'California Department of Housing and Community Development',
                'tenant_org': 'Tenants Together',
                'legal_aid': 'California Legal Aid',
                'hotline': '1-866-557-7368'
            },
            'new_york': {
                'housing_authority': 'New York State Division of Housing',
                'tenant_org': 'Met Council on Housing',
                'legal_aid': 'Legal Aid Society',
                'hotline': '311'
            },
            'texas': {
                'housing_authority': 'Texas Department of Housing',
                'tenant_org': 'Texas Tenants Union',
                'legal_aid': 'Texas Legal Aid',
                'hotline': '2-1-1'
            }
        }

        state_lower = state.lower()
        if state_lower in state_resources:
            resources = state_resources[state_lower]
            return f"""
**{state.title()} Tenant Resources:**

• **Housing Authority:** {resources['housing_authority']}
• **Tenant Organization:** {resources['tenant_org']}
• **Legal Aid:** {resources['legal_aid']}
• **Hotline:** {resources['hotline']}

**Additional Resources:**
• Search "[your city] tenant rights" for local organizations
• Contact your city hall for housing department information
• Check state bar association for lawyer referrals
"""
        else:
            return f"""
**General Resources for {state.title()}:**

• Contact your state housing authority
• Search "tenant rights {state}" online
• Call 2-1-1 for local resource referrals
• Contact state legal aid organizations
• Check with your city's housing department

**For specific {state.title()} laws:**
• Visit your state government website
• Contact state attorney general's office
• Look up "{state} landlord tenant law"
"""