"""
Custom MCP tools for workflow manipulation
These tools allow the agent to create and modify workflow blocks
"""
from typing import Dict, Any, List, Optional
from claude_agent_sdk import tool, create_sdk_mcp_server
import json


# In-memory storage for demo (replace with database in production)
workflow_store: Dict[str, List[Dict[str, Any]]] = {}


@tool
async def create_workflow_block(
    block_type: str,
    config: Dict[str, Any],
    description: str = ""
) -> Dict[str, Any]:
    """
    Create a new workflow block with the specified type and configuration.

    Args:
        block_type: Type of block (e.g., "trigger-report", "action-send-message", "condition", "loop")
        config: Configuration object for the block (varies by type)
        description: Human-readable description of what this block does

    Returns:
        Dictionary containing the created block with generated ID
    """
    import uuid

    block_id = f"block-{uuid.uuid4().hex[:8]}"

    block = {
        "id": block_id,
        "type": block_type,
        "data": config,
        "description": description,
        "configured": True,
        "parentIds": [],
        "childIds": []
    }

    # Add special properties based on block type
    if block_type == "condition":
        block["supportsMultipleInputs"] = True
        block["children"] = {"paths": []}
    elif block_type == "loop":
        block["children"] = {"items": []}
        block["data"]["enclosedBlocks"] = []

    return {
        "success": True,
        "block": block,
        "message": f"Created {block_type} block with ID {block_id}"
    }


@tool
async def connect_blocks(
    source_block_id: str,
    target_block_id: str,
    condition_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a connection between two workflow blocks.

    Args:
        source_block_id: ID of the source/parent block
        target_block_id: ID of the target/child block
        condition_path: For condition blocks, specify the path label (optional)

    Returns:
        Success status and connection details
    """
    return {
        "success": True,
        "connection": {
            "from": source_block_id,
            "to": target_block_id,
            "path": condition_path
        },
        "message": f"Connected {source_block_id} to {target_block_id}"
    }


@tool
async def get_workflow_blocks(workflow_id: str) -> Dict[str, Any]:
    """
    Retrieve all blocks for a specific workflow.

    Args:
        workflow_id: The workflow identifier

    Returns:
        List of workflow blocks
    """
    blocks = workflow_store.get(workflow_id, [])
    return {
        "success": True,
        "workflow_id": workflow_id,
        "blocks": blocks,
        "count": len(blocks)
    }


@tool
async def update_workflow_block(
    block_id: str,
    updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update configuration of an existing workflow block.

    Args:
        block_id: ID of the block to update
        updates: Dictionary of fields to update

    Returns:
        Success status and updated block
    """
    return {
        "success": True,
        "block_id": block_id,
        "updates": updates,
        "message": f"Updated block {block_id}"
    }


@tool
async def validate_workflow_structure(
    blocks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Validate that a workflow structure is valid and complete.

    Args:
        blocks: List of workflow blocks to validate

    Returns:
        Validation results with any errors or warnings
    """
    errors = []
    warnings = []

    # Check for at least one trigger block
    trigger_blocks = [b for b in blocks if b.get("type", "").startswith("trigger-")]
    if not trigger_blocks:
        errors.append("Workflow must have at least one trigger block")

    # Check for orphaned blocks (no connections)
    if len(blocks) > 1:
        connected_blocks = set()
        for block in blocks:
            if block.get("parentIds"):
                connected_blocks.update(block["parentIds"])
            if block.get("childIds"):
                connected_blocks.update(block["childIds"])

        for block in blocks:
            if block["id"] not in connected_blocks and not block.get("type", "").startswith("trigger-"):
                warnings.append(f"Block {block['id']} ({block.get('type')}) is not connected to any other blocks")

    # Check condition blocks have paths configured
    for block in blocks:
        if block.get("type") == "condition" and not block.get("data", {}).get("prompt"):
            errors.append(f"Condition block {block['id']} is missing condition description")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "block_count": len(blocks),
        "trigger_count": len(trigger_blocks)
    }


@tool
async def suggest_next_blocks(
    current_block_type: str,
    workflow_context: str
) -> Dict[str, Any]:
    """
    Suggest appropriate next block types based on the current workflow context.

    Args:
        current_block_type: Type of the most recent block
        workflow_context: Description of what the workflow is trying to accomplish

    Returns:
        List of suggested block types with explanations
    """
    # Healthcare-specific suggestions
    suggestions = []

    if current_block_type.startswith("trigger-"):
        suggestions = [
            {"type": "condition", "reason": "Check conditions before taking action"},
            {"type": "action-send-message", "reason": "Notify patient or provider"},
            {"type": "action-create-task", "reason": "Create follow-up task"}
        ]
    elif current_block_type.startswith("action-"):
        suggestions = [
            {"type": "wait", "reason": "Wait for a response or time period"},
            {"type": "action-send-message", "reason": "Send another message"},
            {"type": "approval", "reason": "Require human review before continuing"}
        ]
    elif current_block_type == "condition":
        suggestions = [
            {"type": "action-send-message", "reason": "Take action based on condition"},
            {"type": "condition", "reason": "Add another conditional check"},
            {"type": "approval", "reason": "Route to human review"}
        ]
    else:
        suggestions = [
            {"type": "action-send-message", "reason": "Generic next action"},
            {"type": "condition", "reason": "Add conditional logic"}
        ]

    return {
        "suggestions": suggestions,
        "current_block": current_block_type
    }


# Create the MCP server for workflow tools
workflow_mcp_server = create_sdk_mcp_server(
    "workflow-tools",
    [
        create_workflow_block,
        connect_blocks,
        get_workflow_blocks,
        update_workflow_block,
        validate_workflow_structure,
        suggest_next_blocks
    ]
)
