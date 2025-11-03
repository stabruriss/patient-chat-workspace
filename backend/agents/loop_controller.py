"""
Loop Controller Agent
"""
from typing import Dict, Any, Optional
from claude_agent_sdk import query, ClaudeAgentOptions
from backend.config.key_manager import key_manager
from backend.models.workflow_context import LoopEvaluationRequest, LoopEvaluationResponse
import json
import os


class LoopControllerAgent:
    def __init__(self, user_api_key: Optional[str] = None):
        self.user_api_key = user_api_key

    async def evaluate_loop(self, request: LoopEvaluationRequest, user_api_key: Optional[str] = None) -> LoopEvaluationResponse:
        api_key = key_manager.get_claude_api_key(user_api_key or self.user_api_key)
        if not api_key:
            return LoopEvaluationResponse(action="escalate", reasoning="No API key", confidence=0.0)

        try:
            os.environ['ANTHROPIC_API_KEY'] = api_key
            
            prompt = f"""Loop iteration {request.iteration_count}
Continue: {request.continue_rule}
Break: {request.break_rule}
Context: {json.dumps(request.workflow_context)}
Respond JSON: {{"action": "continue|break|escalate", "reasoning": "...", "confidence": 0.9}}"""

            response_text = ""
            async for message in query(prompt=prompt, options=ClaudeAgentOptions(model=key_manager.get_claude_model())):
                if hasattr(message, 'content') and message.content:
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            response_text += block.text

            action_data = self._parse_action(response_text)
            return LoopEvaluationResponse(**action_data)
        except Exception as e:
            return LoopEvaluationResponse(action="break", reasoning=str(e), confidence=0.0)

    def _parse_action(self, text: str) -> Dict[str, Any]:
        try:
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                return json.loads(text[start:end])
        except:
            pass
        return {"action": "break", "reasoning": "Parse failed", "confidence": 0.0}


loop_controller = LoopControllerAgent()
