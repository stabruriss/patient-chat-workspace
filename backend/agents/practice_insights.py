"""
Practice Insights Agent
Generates AI-powered insights from practice operational data and answers questions about practice metrics
"""

from typing import Dict, Any, List, Optional
from claude_agent_sdk import query, ClaudeAgentOptions
import json
import os
from backend.config.key_manager import key_manager


class PracticeInsightsAgent:
    """Agent for generating practice insights and answering questions about practice data"""

    def __init__(self, user_api_key: Optional[str] = None):
        self.user_api_key = user_api_key

    async def generate_insights(self, practice_data: Dict[str, Any], user_api_key: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Generate AI insights from practice operational data

        Args:
            practice_data: Dictionary containing current/previous period metrics
            user_api_key: Optional user API key

        Returns:
            List of insights with type, title, description, and recommendation
        """

        api_key = key_manager.get_claude_api_key(user_api_key or self.user_api_key)
        if not api_key:
            return [
                {
                    "type": "neutral",
                    "title": "API Key Required",
                    "description": "Configure your Claude API key to enable AI insights.",
                    "recommendation": None
                }
            ]

        prompt = f"""You are a healthcare practice operations analyst. Analyze the following practice data and generate 3-5 actionable insights.

Practice Data:
{json.dumps(practice_data, indent=2)}

For each insight:
1. Compare current metrics to previous period (identify trends)
2. Highlight what's working well (positive trends)
3. Flag concerns or opportunities (negative trends or warnings)
4. Provide specific, actionable recommendations

Return insights as a JSON array with this format:
[
  {{
    "type": "positive|negative|neutral|warning",
    "title": "Brief insight title",
    "description": "2-3 sentence description with specific numbers",
    "recommendation": "Specific action to take (optional)"
  }}
]

Focus on:
- Revenue trends
- Patient growth and retention
- Operational efficiency (wait times, utilization)
- Service performance
- Areas needing attention

Return ONLY the JSON array, no additional text."""

        try:
            os.environ['ANTHROPIC_API_KEY'] = api_key

            response_text = ""
            async for message in query(prompt=prompt, options=ClaudeAgentOptions(model=key_manager.get_claude_model())):
                if hasattr(message, 'content') and message.content:
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            response_text += block.text

            # Remove markdown code blocks if present
            content = response_text.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            insights = json.loads(content)
            return insights

        except Exception as e:
            print(f"[ERROR] Failed to generate insights: {e}")
            # Return fallback insights
            return [
                {
                    "type": "neutral",
                    "title": "Practice Data Available",
                    "description": "Your practice metrics are being tracked. Enable AI insights for detailed analysis.",
                    "recommendation": None
                }
            ]

    async def answer_question(self, question: str, practice_data: Dict[str, Any], user_api_key: Optional[str] = None) -> str:
        """
        Answer a specific question about practice data

        Args:
            question: User's question
            practice_data: Dictionary containing practice metrics
            user_api_key: Optional user API key

        Returns:
            AI-generated answer
        """

        api_key = key_manager.get_claude_api_key(user_api_key or self.user_api_key)
        if not api_key:
            return "Please configure your Claude API key to use the AI assistant."

        prompt = f"""You are a healthcare practice operations analyst. Answer the following question based on the practice data provided.

Practice Data:
{json.dumps(practice_data, indent=2)}

Question: {question}

Provide a clear, concise answer with specific numbers from the data. If the question cannot be answered with the available data, politely explain what data would be needed.

Keep your answer to 2-4 sentences and be specific."""

        try:
            os.environ['ANTHROPIC_API_KEY'] = api_key

            response_text = ""
            async for message in query(prompt=prompt, options=ClaudeAgentOptions(model=key_manager.get_claude_model())):
                if hasattr(message, 'content') and message.content:
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            response_text += block.text

            return response_text.strip()

        except Exception as e:
            print(f"[ERROR] Failed to answer question: {e}")
            return "I'm having trouble analyzing the data right now. Please try again."


# Singleton instance
practice_insights_agent = PracticeInsightsAgent()
