# agents/agent_router.py

import re
from typing import Dict, List, Tuple, Optional
import json
from utils import get_gemini_response

class AgentRouter:
    """
    Central router that determines which agent should handle incoming requests using Gemini LLM
    """

    def route_request(self, text: str, has_image: bool = False, context: Dict = None) -> str:
        """
        Route the request to the appropriate agent using Gemini LLM.

        Args:
            text: User input text
            has_image: Whether an image was uploaded
            context: Conversation context

        Returns:
            Agent identifier ('agent1' for issue detection, 'agent2' for tenancy, or 'router' for clarification)
        """

        if has_image:
            # If an image is present, it's highly likely an issue detection request
            return 'agent1'

        prompt = self._build_gemini_routing_prompt(text, context)

        try:
            gemini_response = get_gemini_response(prompt)
            # Assuming Gemini is instructed to return a single word: 'issue', 'tenancy', or 'general'
            routing_decision = gemini_response.strip().lower()

            if 'issue' in routing_decision:
                return 'agent1'  # Route to Issue Detection Agent
            elif 'tenancy' in routing_decision:
                return 'agent2'  # Route to Tenancy FAQ Agent
            else:
                return 'router'  # Needs clarification or general handling

        except Exception as e:
            print(f"Error calling Gemini API for routing: {e}")
            # Fallback to a simple keyword-based routing or default to router
            return self._fallback_route(text, has_image, context)

def _build_gemini_routing_prompt(self, text: str, context: Dict) -> str:
    """
    Build the prompt for the Gemini model to determine the correct agent.
    """
    prompt = f"Analyze the following user query and determine if it is related to property issues or tenancy law/rental guidance. \n"

    if context:
        prompt += f"Consider the following conversation context:\n{json.dumps(context)}\n\n"

    prompt += f"User query: {text}\n\n"
    prompt += "Respond with only one word: 'issue' if it is related to property issues, 'tenancy' if it is related to tenancy law or rental guidance, or 'general' if it is neither or unclear."

    return prompt

    def _fallback_route(self, text: str, has_image: bool, context: Dict) -> str:
        """
        Fallback routing mechanism if Gemini API call fails.
        """
        # This is a simplified version of the original keyword-based routing
        text_lower = text.lower()

        tenancy_keywords = ['landlord', 'tenant', 'rent', 'deposit', 'evict', 'lease', 'rights', 'law', 'legal']
        issue_keywords = ['damage', 'broken', 'crack', 'leak', 'mold', 'repair', 'fix', 'issue']

        tenancy_score = sum(1 for keyword in tenancy_keywords if keyword in text_lower)
        issue_score = sum(1 for keyword in issue_keywords if keyword in text_lower)

        if has_image or issue_score > tenancy_score:
            return 'agent1'
        elif tenancy_score > issue_score:
            return 'agent2'
        else:
            return 'router'

    def generate_clarification_response(self, text: str, context: Dict = None) -> Tuple[str, float]:
        """
        Generate a clarification response when routing is unclear.
        This can also be potentially enhanced by Gemini.
        """
        responses = [
            "I'm not sure if you need help with a property issue or a tenancy question. Can you please clarify?",
            "To assist you better, could you specify if your query is about a problem with a property or about rental/tenancy matters?",
            "Are you asking about a property issue or a question about tenancy laws? Please tell me more."
        ]
        return random.choice(responses), 1.0

    def analyze_conversation_flow(self, messages: List[Dict]) -> Dict:
        """
        Analyze conversation flow for insights.
        """
        agent_usage = {'agent1': 0, 'agent2': 0, 'router': 0}

        for msg in messages:
            if msg.get('type') == 'bot' and msg.get('agent'):
                agent_usage[msg['agent']] = agent_usage.get(msg['agent'], 0) + 1

        return {
            'agent_usage': agent_usage,
            'total_messages': len(messages),
            'dominant_agent': max(agent_usage, key=agent_usage.get) if messages else None,
            'conversation_type': self._determine_conversation_type(agent_usage) if messages else 'empty'
        }

    def _determine_conversation_type(self, agent_usage: Dict) -> str:
        """
        Determine the primary conversation type.
        """
        if agent_usage['agent1'] > agent_usage['agent2']:
            return 'issue_focused'
        elif agent_usage['agent2'] > agent_usage['agent1']:
            return 'tenancy_focused'
        else:
            return 'mixed'

    def get_routing_explanation(self, text: str, has_image: bool, chosen_agent: str) -> str:
        """
        Provide explanation for why a particular agent was chosen.
        This can also be potentially enhanced by Gemini.
        """
        explanations = {
            'agent1': "🔍 Routed to Issue Detection Agent",
            'agent2': "⚖️ Routed to Tenancy FAQ Agent",
            'router': "🏠 Handled by Main Assistant (needs clarification)"
        }

        base_explanation = explanations.get(chosen_agent, "Routed to an agent.")

        if chosen_agent == 'agent1' and has_image:
            return f"{base_explanation} due to image upload."
        elif chosen_agent == 'router':
             return f"{base_explanation}. Your query was unclear or didn't match specific keywords. Please provide more details."
        else:
             return f"{base_explanation} based on the analysis of your request."
