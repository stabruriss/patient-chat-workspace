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
        self.cache_duration = 604800  # 1 week in seconds (7 * 24 * 60 * 60)

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

        # If no API key, return fallback insights immediately
        if not api_key:
            print("[INFO] No API key found, returning fallback insights")
            curr = practice_data.get('current_period', {})
            prev = practice_data.get('previous_period', {})
            comp = practice_data.get('period_comparison', {})

            rev_change = curr.get('total_revenue', 0) - prev.get('total_revenue', 0)
            pat_change = curr.get('total_patients', 0) - prev.get('total_patients', 0)

            return [
                {
                    "type": "positive" if comp.get('revenue_change', 0) > 0 else "negative",
                    "title": "Revenue",
                    "value": f"+{comp.get('revenue_change', 0):.1f}%",
                    "change": f"+${rev_change/1000:.1f}K",
                    "trend": "up" if comp.get('revenue_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('total_patients_change', 0) > 0 else "negative",
                    "title": "Patients",
                    "value": f"+{comp.get('total_patients_change', 0):.1f}%",
                    "change": f"+{pat_change}",
                    "trend": "up" if comp.get('total_patients_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('wait_time_change', 0) < 0 else "warning",
                    "title": "Wait Time",
                    "value": f"{comp.get('wait_time_change', 0):.1f}%",
                    "change": f"{curr.get('average_wait_time', 0)}min",
                    "trend": "down" if comp.get('wait_time_change', 0) < 0 else "up"
                },
                {
                    "type": "positive" if comp.get('engagement_change', 0) > 0 else "warning",
                    "title": "Engagement",
                    "value": f"{curr.get('patient_engagement', 0)}%",
                    "change": f"+{comp.get('engagement_change', 0):.1f}%",
                    "trend": "up" if comp.get('engagement_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('no_show_change', 0) < 0 else "warning",
                    "title": "No-Shows",
                    "value": f"{curr.get('no_show_rate', 0):.1f}%",
                    "change": f"{comp.get('no_show_change', 0):.1f}%",
                    "trend": "down" if comp.get('no_show_change', 0) < 0 else "up"
                },
                {
                    "type": "positive",
                    "title": "Completed",
                    "value": f"{curr.get('appointments_completed', 0)}",
                    "change": f"+{curr.get('appointments_completed', 0) - prev.get('appointments_completed', 0)}",
                    "trend": "up"
                },
                {
                    "type": "positive" if comp.get('new_patients_change', 0) > 0 else "warning",
                    "title": "New Patients",
                    "value": f"+{comp.get('new_patients_change', 0):.1f}%",
                    "change": f"{curr.get('new_patients', 0)}",
                    "trend": "up" if comp.get('new_patients_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('utilization_change', 0) > 0 else "warning",
                    "title": "Utilization",
                    "value": f"{curr.get('provider_utilization', 0)}%",
                    "change": f"+{comp.get('utilization_change', 0):.1f}%",
                    "trend": "up" if comp.get('utilization_change', 0) > 0 else "down"
                },
                {
                    "type": "positive",
                    "title": "Scheduled",
                    "value": f"{curr.get('appointments_scheduled', 0)}",
                    "change": f"+{curr.get('appointments_scheduled', 0) - prev.get('appointments_scheduled', 0)}",
                    "trend": "up"
                },
                {
                    "type": "warning",
                    "title": "Cancelled",
                    "value": f"{curr.get('appointments_cancelled', 0)}",
                    "change": f"+{curr.get('appointments_cancelled', 0) - prev.get('appointments_cancelled', 0)}",
                    "trend": "up"
                }
            ]

        prompt = f"""You are a healthcare practice operations analyst. Analyze the following practice data and generate exactly 10 diverse insights.

IMPORTANT: Be extremely concise. Each insight should have minimal text.

Practice Data:
{json.dumps(practice_data, indent=2)}

Return exactly 10 insights as a JSON array with this EXACT format:
[
  {{
    "type": "positive|negative|warning",
    "title": "Revenue" (1-2 words only),
    "value": "+8.9%" (the main metric - NEVER use "N/A"),
    "change": "+$7.3K" (use K for thousands, optional),
    "trend": "up" (up|down|stable)
  }}
]

Rules:
- EXACTLY 10 different insights covering different metrics
- NO descriptions - visual only
- value must ALWAYS be a real number (never "N/A" or null)
- Use K for thousands (e.g., "$7.3K" not "$7,270")
- Mix of: revenue, patients, appointments, wait time, utilization, engagement, services
- Use positive for improvements, negative for declines, warning for concerns
- trend must be: "up", "down", or "stable"

Return ONLY the JSON array, no additional text.
"""

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
            curr = practice_data.get('current_period', {})
            prev = practice_data.get('previous_period', {})
            comp = practice_data.get('period_comparison', {})

            rev_change = curr.get('total_revenue', 0) - prev.get('total_revenue', 0)
            pat_change = curr.get('total_patients', 0) - prev.get('total_patients', 0)

            return [
                {
                    "type": "positive" if comp.get('revenue_change', 0) > 0 else "negative",
                    "title": "Revenue",
                    "value": f"+{comp.get('revenue_change', 0):.1f}%",
                    "change": f"+${rev_change/1000:.1f}K",
                    "trend": "up" if comp.get('revenue_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('total_patients_change', 0) > 0 else "negative",
                    "title": "Patients",
                    "value": f"+{comp.get('total_patients_change', 0):.1f}%",
                    "change": f"+{pat_change}",
                    "trend": "up" if comp.get('total_patients_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('wait_time_change', 0) < 0 else "warning",
                    "title": "Wait Time",
                    "value": f"{comp.get('wait_time_change', 0):.1f}%",
                    "change": f"{curr.get('average_wait_time', 0)}min",
                    "trend": "down" if comp.get('wait_time_change', 0) < 0 else "up"
                },
                {
                    "type": "positive" if comp.get('engagement_change', 0) > 0 else "warning",
                    "title": "Engagement",
                    "value": f"{curr.get('patient_engagement', 0)}%",
                    "change": f"+{comp.get('engagement_change', 0):.1f}%",
                    "trend": "up" if comp.get('engagement_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('no_show_change', 0) < 0 else "warning",
                    "title": "No-Shows",
                    "value": f"{curr.get('no_show_rate', 0):.1f}%",
                    "change": f"{comp.get('no_show_change', 0):.1f}%",
                    "trend": "down" if comp.get('no_show_change', 0) < 0 else "up"
                },
                {
                    "type": "positive",
                    "title": "Completed",
                    "value": f"{curr.get('appointments_completed', 0)}",
                    "change": f"+{curr.get('appointments_completed', 0) - prev.get('appointments_completed', 0)}",
                    "trend": "up"
                },
                {
                    "type": "positive" if comp.get('new_patients_change', 0) > 0 else "warning",
                    "title": "New Patients",
                    "value": f"+{comp.get('new_patients_change', 0):.1f}%",
                    "change": f"{curr.get('new_patients', 0)}",
                    "trend": "up" if comp.get('new_patients_change', 0) > 0 else "down"
                },
                {
                    "type": "positive" if comp.get('utilization_change', 0) > 0 else "warning",
                    "title": "Utilization",
                    "value": f"{curr.get('provider_utilization', 0)}%",
                    "change": f"+{comp.get('utilization_change', 0):.1f}%",
                    "trend": "up" if comp.get('utilization_change', 0) > 0 else "down"
                },
                {
                    "type": "positive",
                    "title": "Scheduled",
                    "value": f"{curr.get('appointments_scheduled', 0)}",
                    "change": f"+{curr.get('appointments_scheduled', 0) - prev.get('appointments_scheduled', 0)}",
                    "trend": "up"
                },
                {
                    "type": "warning",
                    "title": "Cancelled",
                    "value": f"{curr.get('appointments_cancelled', 0)}",
                    "change": f"+{curr.get('appointments_cancelled', 0) - prev.get('appointments_cancelled', 0)}",
                    "trend": "up"
                }
            ]

    async def answer_question(self, question: str, practice_data: Dict[str, Any], user_api_key: Optional[str] = None) -> str:
        """
        Answer a specific question about practice data

        Args:
            question: User question
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
