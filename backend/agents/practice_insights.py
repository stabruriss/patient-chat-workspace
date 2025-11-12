"""
Practice Insights Agent
Generates AI-powered insights from practice operational data and answers questions about practice metrics
"""

from typing import Dict, Any, List, Optional
from claude_agent_sdk import query, ClaudeAgentOptions
import json
import os
import hashlib
import time
from backend.config.key_manager import key_manager


class PracticeInsightsAgent:
    """Agent for generating practice insights and answering questions about practice data"""

    def __init__(self, user_api_key: Optional[str] = None):
        self.user_api_key = user_api_key
        self.cache = {}  # Simple in-memory cache: {data_hash: (insights, timestamp)}
        self.cache_duration = 3600  # 1 hour in seconds

    def _get_data_hash(self, practice_data: Dict[str, Any]) -> str:
        """Generate hash of practice data for caching"""
        data_str = json.dumps(practice_data, sort_keys=True)
        return hashlib.md5(data_str.encode()).hexdigest()

    def _is_cache_valid(self, timestamp: float) -> bool:
        """Check if cached data is still valid"""
        return (time.time() - timestamp) < self.cache_duration

    async def generate_insights(self, practice_data: Dict[str, Any], user_api_key: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Generate AI insights from practice operational data (with caching)

        Args:
            practice_data: Dictionary containing current/previous period metrics
            user_api_key: Optional user API key

        Returns:
            List of insights with type, title, value, change, description
        """

        # Check cache first
        data_hash = self._get_data_hash(practice_data)
        if data_hash in self.cache:
            cached_insights, timestamp = self.cache[data_hash]
            if self._is_cache_valid(timestamp):
                print(f"[CACHE HIT] Returning cached insights")
                return cached_insights

        api_key = key_manager.get_claude_api_key(user_api_key or self.user_api_key)
        if not api_key:
            return [
                {
                    "type": "neutral",
                    "title": "API Key Required",
                    "value": None,
                    "change": None,
                    "description": "Configure your Claude API key"
                }
            ]

        prompt = f"""You are a healthcare practice operations analyst. Analyze the following practice data and generate exactly 3 concise insights.

IMPORTANT: Be extremely concise. Each insight should be ONE SHORT SENTENCE only.

Practice Data:
{json.dumps(practice_data, indent=2)}

Return exactly 3 insights as a JSON array with this EXACT format:
[
  {{
    "type": "positive|negative|warning",
    "title": "Revenue Growth" (2-3 words max),
    "value": "+8.9%" (the key number),
    "change": "+$7,270" (optional, the actual change),
    "description": "One SHORT sentence only, max 10 words"
  }}
]

Rules:
- EXACTLY 3 insights
- Each description must be ONE sentence, max 10 words
- Include specific numbers in value/change
- Focus on: revenue, patient growth, operational efficiency
- Use positive for good trends, negative for bad trends, warning for concerns

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

            # Cache the insights
            self.cache[data_hash] = (insights, time.time())
            print(f"[CACHE SET] Cached insights for {data_hash}")

            return insights

        except Exception as e:
            print(f"[ERROR] Failed to generate insights: {e}")
            # Return fallback insights based on actual data
            return [
                {
                    "type": "positive",
                    "title": "Revenue Growth",
                    "value": f"+{practice_data.get('period_comparison', {}).get('revenue_change', 0):.1f}%",
                    "change": f"+${practice_data.get('current_period', {}).get('total_revenue', 0) - practice_data.get('previous_period', {}).get('total_revenue', 0):,.0f}",
                    "description": "Revenue increased compared to last period"
                },
                {
                    "type": "positive",
                    "title": "Patient Growth",
                    "value": f"+{practice_data.get('period_comparison', {}).get('total_patients_change', 0):.1f}%",
                    "change": f"+{practice_data.get('current_period', {}).get('total_patients', 0) - practice_data.get('previous_period', {}).get('total_patients', 0)} patients",
                    "description": "Patient base growing steadily"
                },
                {
                    "type": "positive",
                    "title": "Wait Time",
                    "value": f"{practice_data.get('period_comparison', {}).get('wait_time_change', 0):.1f}%",
                    "change": f"{practice_data.get('current_period', {}).get('average_wait_time', 0) - practice_data.get('previous_period', {}).get('average_wait_time', 0)} min",
                    "description": "Average wait time improved"
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
