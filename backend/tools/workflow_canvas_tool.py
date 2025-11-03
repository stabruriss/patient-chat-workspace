"""
MCP Tool for creating workflow blocks on the canvas
Allows the AI agent to directly manipulate the workflow canvas
"""

import json
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class WorkflowCanvasTool:
    """Tool for AI agents to create and manipulate workflow blocks"""

    VALID_BLOCK_TYPES = [
        'send-message', 'appointment', 'task', 'document', 'order',
        'note', 'nested-workflow', 'wait', 'condition', 'loop',
        'smart-review', 'ai-touch'
    ]

    def __init__(self):
        self.blocks_created = []
        logger.info("WorkflowCanvasTool initialized")

    def create_block(self, block_type: str, config: Dict[str, Any], insert_after_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new workflow block

        Args:
            block_type: Type of block (e.g., 'send-message', 'condition', 'smart-review')
            config: Block configuration (varies by type)
            insert_after_id: Optional ID of block to insert after (null = append to end)

        Returns:
            Response with block creation details
        """
        logger.info(f"create_block called: type={block_type}, insert_after={insert_after_id}")
        logger.debug(f"Block config: {json.dumps(config, indent=2)}")

        if block_type not in self.VALID_BLOCK_TYPES:
            error_msg = f"Invalid block type: {block_type}. Valid types: {', '.join(self.VALID_BLOCK_TYPES)}"
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg
            }

        # Generate unique block ID
        block_id = f"block_{len(self.blocks_created) + 1}"

        block = {
            "id": block_id,
            "type": block_type,
            "config": config,
            "insertAfter": insert_after_id
        }

        self.blocks_created.append(block)

        logger.info(f"Block created successfully: {block_id}")

        return {
            "success": True,
            "block": block,
            "action": "create_block",
            "message": f"Created {block_type} block"
        }

    def create_multiple_blocks(self, blocks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Create multiple blocks at once

        Args:
            blocks: List of block definitions, each with {type, config, insertAfter?}

        Returns:
            Response with all created blocks
        """
        logger.info(f"create_multiple_blocks called with {len(blocks)} blocks")

        created_blocks = []
        errors = []

        for i, block_def in enumerate(blocks):
            try:
                result = self.create_block(
                    block_type=block_def.get('type'),
                    config=block_def.get('config', {}),
                    insert_after_id=block_def.get('insertAfter')
                )

                if result['success']:
                    created_blocks.append(result['block'])
                else:
                    errors.append(f"Block {i}: {result['error']}")

            except Exception as e:
                error_msg = f"Block {i}: {str(e)}"
                logger.error(error_msg, exc_info=True)
                errors.append(error_msg)

        logger.info(f"Created {len(created_blocks)} blocks, {len(errors)} errors")

        return {
            "success": len(errors) == 0,
            "blocks": created_blocks,
            "action": "create_multiple_blocks",
            "errors": errors if errors else None,
            "message": f"Created {len(created_blocks)} blocks" + (f" with {len(errors)} errors" if errors else "")
        }

    def get_block_schema(self, block_type: str) -> Dict[str, Any]:
        """
        Get the expected configuration schema for a block type

        Args:
            block_type: Type of block

        Returns:
            Schema definition for the block's config
        """
        schemas = {
            'send-message': {
                "channel": "string (sms|email|in-app)",
                "message": "string - message content",
                "template": "string? - optional template ID"
            },
            'appointment': {
                "type": "string (virtual|in-person)",
                "duration": "number - minutes",
                "provider": "string? - optional provider ID"
            },
            'task': {
                "title": "string - task title",
                "assignee": "string - role or person",
                "priority": "string (low|medium|high)",
                "dueInDays": "number? - optional days until due"
            },
            'document': {
                "documentType": "string (consent|form|educational)",
                "title": "string - document title",
                "requireSignature": "boolean"
            },
            'order': {
                "orderType": "string (lab|medication|imaging)",
                "details": "string - order details"
            },
            'note': {
                "content": "string - note content",
                "category": "string? - optional category"
            },
            'wait': {
                "waitType": "string (time|event|input)",
                "duration": "string - e.g., '24 hours', '2 days'",
                "event": "string? - optional event name for event-based wait"
            },
            'condition': {
                "conditionType": "string (ai-evaluation|simple)",
                "description": "string - what to check",
                "trueBranch": "array - blocks for true path",
                "falseBranch": "array - blocks for false path"
            },
            'loop': {
                "loopType": "string (ai-evaluation|count)",
                "description": "string - loop condition",
                "maxIterations": "number - max loop count",
                "blocks": "array - blocks to repeat"
            },
            'smart-review': {
                "reviewType": "string - what to review",
                "aiAnalysis": "boolean - use AI pre-analysis",
                "escalationTimeout": "number? - hours before escalation",
                "escalateTo": "string? - role to escalate to"
            },
            'ai-touch': {
                "analysisType": "string - what to analyze",
                "action": "string - what AI should do",
                "confidenceThreshold": "number? - 0-1, default 0.8"
            }
        }

        return schemas.get(block_type, {"error": f"Unknown block type: {block_type}"})

    def clear_blocks(self):
        """Clear all created blocks (for testing)"""
        logger.info(f"Clearing {len(self.blocks_created)} blocks")
        self.blocks_created = []


# Tool descriptor for Claude Agent SDK
WORKFLOW_CANVAS_TOOL_DESCRIPTOR = {
    "name": "create_workflow_block",
    "description": """Creates a visual workflow block on the canvas. Use this to build the workflow as you discuss it with the user.

    IMPORTANT: Always use this tool to create blocks as you explain them. Don't just describe - actually create them!

    Examples:
    - User says "send them a reminder": Create a send-message block
    - User says "if they don't respond": Create a condition block
    - User says "assign to nurse": Create a task block
    """,
    "input_schema": {
        "type": "object",
        "properties": {
            "block_type": {
                "type": "string",
                "enum": ['send-message', 'appointment', 'task', 'document', 'order', 'note', 'nested-workflow', 'wait', 'condition', 'loop', 'smart-review', 'ai-touch'],
                "description": "Type of workflow block to create"
            },
            "config": {
                "type": "object",
                "description": "Configuration for the block (varies by type - use get_block_schema to see options)"
            },
            "insert_after_id": {
                "type": "string",
                "description": "Optional: ID of existing block to insert after (omit to append to end)",
                "nullable": True
            }
        },
        "required": ["block_type", "config"]
    }
}

WORKFLOW_CANVAS_BATCH_TOOL_DESCRIPTOR = {
    "name": "create_multiple_workflow_blocks",
    "description": "Creates multiple workflow blocks at once. More efficient for building complete workflows.",
    "input_schema": {
        "type": "object",
        "properties": {
            "blocks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "type": {"type": "string"},
                        "config": {"type": "object"},
                        "insertAfter": {"type": "string", "nullable": True}
                    },
                    "required": ["type", "config"]
                },
                "description": "Array of block definitions to create"
            }
        },
        "required": ["blocks"]
    }
}
