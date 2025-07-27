# agents/issue_detection_agent.py

import base64
import json
import random
from typing import Dict, List, Tuple, Optional
import re
from utils import get_gemini_response, get_gemini_response_with_image

class IssueDetectionAgent:
    """
    Agent specialized in detecting and analyzing property issues from images and descriptions using Gemini LLM
    """

    def process_request(self, text: str, image_data: Optional[bytes] = None, context: Dict = None) -> Tuple[str, float]:
        """
        Process user request for issue detection and analysis using Gemini LLM.

        Args:
            text: User description of the issue
            image_data: Optional image data for visual analysis
            context: Conversation context

        Returns:
            Tuple of (response_text, confidence_score)
        """

        try:
            if image_data:
                prompt = self._build_gemini_prompt_with_image(text, context)
                gemini_response = get_gemini_response_with_image(prompt, image_data)
            else:
                prompt = self._build_gemini_prompt_from_text(text, context)
                gemini_response = get_gemini_response(prompt)

            response_text, confidence = self._parse_gemini_response(gemini_response)
            return response_text, confidence

        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return "Sorry, I couldn't process your request at the moment. Please try again later.", 0.0

    def _build_gemini_prompt_from_text(self, text: str, context: Dict) -> str:
        """
        Build the prompt for the Gemini model based on text description.
        """
        prompt = f"You are an AI assistant specialized in identifying potential property issues based on text descriptions. Analyze the following description and provide a brief assessment of the likely issue, its possible severity, and initial recommendations.

User description: {text}

"

        if context:
            prompt += f"Here is some recent conversation history for context:
{json.dumps(context)}

"

        prompt += "Please provide a concise response. Indicate the confidence level of your assessment."

        return prompt

    def _build_gemini_prompt_with_image(self, text: str, context: Dict) -> str:
        """
        Build the prompt for the Gemini model when an image is provided.
        """
        prompt = f"You are an AI assistant specialized in identifying and analyzing property issues from images. Examine the provided image and the user's description to identify any potential issues. Describe the issue(s) you observe, assess their severity, and suggest initial recommendations for addressing them.

User description: {text}

"

        if context:
            prompt += f"Here is some recent conversation history for context:
{json.dumps(context)}

"

        prompt += "Please provide a detailed analysis based on the image and description. Indicate the confidence level of your assessment."

        return prompt

    def _parse_gemini_response(self, response: str) -> Tuple[str, float]:
        """
        Parse the Gemini API response to extract the response text and confidence score.

        Args:
            response: The raw response string from the Gemini API.

        Returns:
            A tuple containing the parsed response text and a confidence score.
        """
        # Basic parsing: assume the entire response is the text and assign a default confidence.
        # More sophisticated parsing would be needed for structured responses from Gemini.
        return response, 0.7

    # The following methods from the original class are kept as they might still be useful,
    # or can be enhanced by Gemini in the future:

    def get_follow_up_questions(self, issue_type: str, severity: str) -> List[str]:
        """
        Get relevant follow-up questions for an issue.
        """
        # This method can be potentially enhanced by Gemini to generate more dynamic questions.
        questions_db = {
            'water_damage': [
                "Is the water damage still actively spreading?",
                "Can you locate the source of the water?",
                "Is there a musty odor in the area?",
                "How long has this damage been present?"
            ],
            'structural_damage': [
                "Are the cracks getting larger over time?",
                "Do doors or windows stick in this area?",
                "Is the crack wider than a coin?",
                "Are there multiple cracks in the same area?"
            ],
            'mold_growth': [
                "What color is the growth you're seeing?",
                "Is there a musty smell in the room?",
                "Is the area frequently damp or humid?",
                "How large is the affected area?"
            ],
            'electrical_issues': [
                "Are circuit breakers tripping frequently?",
                "Do you smell burning or see sparks?",
                "Are outlets warm to the touch?",
                "Do lights flicker when appliances turn on?"
            ],
            'plumbing_issues': [
                "Is water pressure affected throughout the house?",
                "Can you hear water running when all taps are off?",
                "Is the issue getting worse over time?",
                "Are multiple fixtures affected?"
            ],
            'cosmetic_damage': [
                "Is the damage affecting the underlying material?",
                "How large is the affected area?",
                "Is the damage spreading or stable?",
                "Do you know what caused the damage?"
            ]
        }

        base_questions = questions_db.get(issue_type, [
            "Can you describe the issue in more detail?",
            "When did you first notice this problem?",
            "Has the issue changed or worsened recently?"
        ])

        if severity == 'severe':
            base_questions.extend([
                "Do you need emergency professional assistance?",
                "Is the issue affecting other areas of the property?",
                "Are there any safety concerns for occupants?"
            ])

        return base_questions[:5]  # Limit to 5 questions

    def estimate_repair_timeline(self, issue_type: str, severity: str) -> str:
        """
        Estimate repair timeline based on issue type and severity.
        """
        # This method can be potentially enhanced by Gemini to provide more accurate estimates.
        timelines = {
            'water_damage': {
                'minor': '1-2 days',
                'moderate': '3-7 days',
                'severe': '1-3 weeks'
            },
            'structural_damage': {
                'minor': '1 day',
                'moderate': '1-2 weeks',
                'severe': '2-8 weeks'
            },
            'mold_growth': {
                'minor': '1-3 days',
                'moderate': '1-2 weeks',
                'severe': '2-4 weeks'
            },
            'electrical_issues': {
                'minor': '2-4 hours',
                'moderate': '1-2 days',
                'severe': '3-7 days'
            },
            'plumbing_issues': {
                'minor': '1-4 hours',
                'moderate': '1-2 days',
                'severe': '2-5 days'
            },
            'cosmetic_damage': {
                'minor': '2-6 hours',
                'moderate': '1-3 days',
                'severe': '1-2 weeks'
            }
        }

        return timelines.get(issue_type, {}).get(severity, 'Timeline varies - consult professional')
