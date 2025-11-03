"""
Workflow Generator Agent
Converts natural language descriptions into workflow block structures
Uses MCP tools to create blocks on the canvas
"""
from typing import List, Dict, Any, Optional, AsyncIterator
from claude_agent_sdk import query, ClaudeAgentOptions
from backend.config.settings import settings
from backend.config.key_manager import key_manager
from backend.config.logging_config import get_agent_logger
from backend.tools.workflow_canvas_tool import WorkflowCanvasTool, WORKFLOW_CANVAS_TOOL_DESCRIPTOR, WORKFLOW_CANVAS_BATCH_TOOL_DESCRIPTOR
import json
import os
import logging

logger = logging.getLogger(__name__)
agent_logger = get_agent_logger()


class WorkflowGeneratorAgent:
    """Agent that generates workflow blocks from natural language"""

    def __init__(self, user_api_key: Optional[str] = None):
        self.conversation_history: List[Dict[str, str]] = []
        self.user_api_key = user_api_key  # For BYOK (Bring Your Own Key)
        self.canvas_tool = WorkflowCanvasTool()
        logger.info("WorkflowGeneratorAgent initialized")

    async def generate_workflow_stream(
        self,
        user_message: str,
        workflow_type: str,
        existing_blocks: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncIterator[Dict[str, Any]]:
        """
        Generate workflow blocks from natural language, streaming responses.
        """
        logger.info(f"Starting workflow generation: type={workflow_type}")
        agent_logger.log_agent_call(
            agent_name="workflow_generator",
            prompt=user_message,
            options={"workflow_type": workflow_type, "existing_blocks_count": len(existing_blocks) if existing_blocks else 0}
        )

        # Get API key from key manager
        api_key = key_manager.get_claude_api_key(self.user_api_key)
        if not api_key:
            error_msg = "No Claude Agent SDK API key configured"
            logger.error(error_msg)
            agent_logger.log_error("api_key_missing", error_msg)
            yield {
                "type": "error",
                "error": error_msg,
                "done": True
            }
            return

        model = key_manager.get_claude_model()

        # Build prompts
        system_prompt = self._build_system_prompt(workflow_type, existing_blocks)
        full_prompt = self._build_prompt(user_message, workflow_type, existing_blocks)

        # Add to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Set API key in environment (Claude SDK reads from ANTHROPIC_API_KEY)
            os.environ['ANTHROPIC_API_KEY'] = api_key

            accumulated_text = ""
            workflow_json_buffer = ""
            in_workflow_json = False
            blocks_created = []

            logger.debug("Starting Claude Agent SDK query")

            async for message in query(
                prompt=full_prompt,
                options=ClaudeAgentOptions(
                    system_prompt=system_prompt,
                    model=model,
                    include_partial_messages=True
                )
            ):
                # Handle text content
                if hasattr(message, 'content') and message.content:
                    for block in message.content:
                        if hasattr(block, 'text') and block.text:
                            text = block.text
                            accumulated_text += text

                            # Check for WORKFLOW_JSON start
                            if 'WORKFLOW_JSON:' in text:
                                in_workflow_json = True
                                # Extract JSON part
                                workflow_json_buffer = text.split('WORKFLOW_JSON:', 1)[1]
                                # Send text before WORKFLOW_JSON to chat
                                pre_json = text.split('WORKFLOW_JSON:', 1)[0]
                                if pre_json.strip():
                                    yield {
                                        "type": "chat_message",
                                        "content": pre_json,
                                        "done": False
                                    }
                            elif in_workflow_json:
                                workflow_json_buffer += text
                            else:
                                # Regular chat message
                                yield {
                                    "type": "chat_message",
                                    "content": text,
                                    "done": False
                                }

                            # Try to parse complete JSON
                            if in_workflow_json and workflow_json_buffer.count('{') > 0:
                                try:
                                    # Try parsing the accumulated JSON
                                    workflow_def = json.loads(workflow_json_buffer.strip())

                                    logger.info(f"Detected WORKFLOW_JSON with {len(workflow_def.get('blocks', []))} blocks")

                                    # Send the complete workflow to frontend
                                    yield {
                                        "type": "workflow_created",
                                        "workflow": workflow_def,
                                        "done": False
                                    }

                                    blocks_created = workflow_def.get('blocks', [])

                                    agent_logger.log_tool_call(
                                        tool_name="create_workflow",
                                        parameters=workflow_def,
                                        result={"success": True, "blocks_count": len(blocks_created)}
                                    )

                                    logger.info(f"Workflow created with {len(blocks_created)} blocks")

                                    in_workflow_json = False
                                    workflow_json_buffer = ""

                                except json.JSONDecodeError:
                                    # Not complete yet, keep accumulating
                                    pass

                            logger.debug(f"Streaming text: {text[:100]}...")

            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": accumulated_text
            })

            logger.info(f"Generation complete. Blocks created: {len(blocks_created)}")
            agent_logger.log_agent_response(
                agent_name="workflow_generator",
                response=accumulated_text,
                token_count=None
            )

            yield {
                "type": "generation_complete",
                "blocks_created": len(blocks_created),
                "done": True
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error in workflow generation: {error_msg}", exc_info=True)
            agent_logger.log_error(
                error_type="generation_error",
                error_message=error_msg,
                context={"workflow_type": workflow_type, "user_message": user_message[:100]}
            )
            yield {
                "type": "error",
                "error": error_msg,
                "done": True
            }

    def _execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call from the agent"""
        logger.debug(f"Executing tool: {tool_name}")

        try:
            if tool_name == "create_workflow_block":
                return self.canvas_tool.create_block(
                    block_type=tool_input.get('block_type'),
                    config=tool_input.get('config', {}),
                    insert_after_id=tool_input.get('insert_after_id')
                )
            elif tool_name == "create_multiple_workflow_blocks":
                return self.canvas_tool.create_multiple_blocks(
                    blocks=tool_input.get('blocks', [])
                )
            else:
                error_msg = f"Unknown tool: {tool_name}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
        except Exception as e:
            error_msg = f"Tool execution error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"success": False, "error": error_msg}

    def _build_system_prompt(self, workflow_type: str, existing_blocks: Optional[List[Dict[str, Any]]]) -> str:
        """Build the system prompt for the workflow generator"""

        return f"""You are a healthcare workflow automation expert. Your ONLY job is to output valid WORKFLOW_JSON.

ABSOLUTE REQUIREMENTS - NO EXCEPTIONS:
1. ALWAYS output WORKFLOW_JSON when user requests a workflow
2. Format: WORKFLOW_JSON: {{"blocks": [...], "connections": [...]}}
3. Put brief 1-sentence explanation BEFORE the JSON, then output the complete JSON
4. DO NOT describe what you'll do - just output the JSON immediately

WORKFLOW TYPE: {workflow_type}

VALID BLOCK TYPES (use these exact type names):
- send-message
- appointment
- task
- document
- order
- note
- wait
- condition
- loop
- smart-review
- ai-touch

REQUIRED JSON STRUCTURE:
WORKFLOW_JSON: {{
  "blocks": [
    {{"id": "block_1", "type": "send-message", "config": {{"channel": "sms", "message": "text here"}}}},
    {{"id": "block_2", "type": "wait", "config": {{"waitType": "time", "duration": "24 hours"}}}},
    {{"id": "block_3", "type": "task", "config": {{"title": "Task name", "assignee": "nurse", "priority": "medium"}}}}
  ],
  "connections": [
    {{"from": "block_1", "to": "block_2"}},
    {{"from": "block_2", "to": "block_3"}}
  ]
}}

EXAMPLE USER REQUEST: "Create a patient intake workflow"

CORRECT RESPONSE:
"Patient intake workflow with registration, document collection, and appointment scheduling."

WORKFLOW_JSON: {{
  "blocks": [
    {{"id": "block_1", "type": "send-message", "config": {{"channel": "email", "message": "Welcome! Please complete your registration forms."}}}},
    {{"id": "block_2", "type": "document", "config": {{"documentType": "form", "title": "Patient Registration", "requireSignature": true}}}},
    {{"id": "block_3", "type": "appointment", "config": {{"type": "in-person", "duration": 30}}}}
  ],
  "connections": [
    {{"from": "block_1", "to": "block_2"}},
    {{"from": "block_2", "to": "block_3"}}
  ]
}}

CRITICAL: You MUST output WORKFLOW_JSON for EVERY workflow request. Do not just explain - output the actual JSON!"""

    def _build_prompt(self, user_message: str, workflow_type: str, existing_blocks: Optional[List[Dict[str, Any]]]) -> str:
        """Build the user prompt"""

        context = f"User wants a {workflow_type} workflow.\n\n"

        if existing_blocks and len(existing_blocks) > 0:
            context += f"Current workflow has {len(existing_blocks)} blocks.\n\n"
        else:
            context += "IMPORTANT: Output WORKFLOW_JSON with the complete workflow structure.\n\n"

        # Include recent conversation history for context
        if self.conversation_history:
            context += "Recent conversation:\n"
            for msg in self.conversation_history[-4:]:  # Last 2 exchanges
                role = msg['role'].capitalize()
                content = msg['content'][:200]
                context += f"{role}: {content}\n"
            context += "\n"

        return f"{context}User request: {user_message}\n\nRemember: Output WORKFLOW_JSON format immediately!"

    def reset_conversation(self):
        """Reset conversation history"""
        logger.info("Resetting conversation history")
        self.conversation_history = []
        self.canvas_tool.clear_blocks()


# Global instance
workflow_generator = WorkflowGeneratorAgent()
