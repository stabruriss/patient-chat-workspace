"""
Condition Evaluator Agent
"""
from typing import Dict, Any, Optional
from claude_agent_sdk import query, ClaudeAgentOptions
from backend.config.key_manager import key_manager
from backend.models.workflow_context import ConditionEvaluationRequest, ConditionEvaluationResponse
import json
import os


class ConditionEvaluatorAgent:
    def __init__(self, user_api_key: Optional[str] = None):
        self.user_api_key = user_api_key

    async def evaluate_condition(self, request: ConditionEvaluationRequest, user_api_key: Optional[str] = None) -> ConditionEvaluationResponse:
        api_key = key_manager.get_claude_api_key(user_api_key or self.user_api_key)
        if not api_key:
            return ConditionEvaluationResponse(decision="escalate", reasoning="No API key", confidence=0.0)

        try:
            os.environ['ANTHROPIC_API_KEY'] = api_key
            
            prompt = f"""Evaluate: {request.condition_description}
Context: {json.dumps(request.workflow_context)}
Respond JSON: {{"decision": "true|false|escalate", "reasoning": "...", "confidence": 0.9}}"""

            response_text = ""
            async for message in query(prompt=prompt, options=ClaudeAgentOptions(model=key_manager.get_claude_model())):
                if hasattr(message, 'content') and message.content:
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            response_text += block.text

            decision_data = self._parse_decision(response_text)
            return ConditionEvaluationResponse(**decision_data)
        except Exception as e:
            return ConditionEvaluationResponse(decision="escalate", reasoning=str(e), confidence=0.0)

    def _parse_decision(self, text: str) -> Dict[str, Any]:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return {"decision": "escalate", "reasoning": "Parse failed", "confidence": 0.0}


condition_evaluator = ConditionEvaluatorAgent()
