"""
Custom MCP tools for workflow execution and runtime evaluation
These tools handle condition and loop evaluation during workflow execution
"""
from typing import Dict, Any, List, Optional
from claude_agent_sdk import tool, create_sdk_mcp_server
import re


@tool
async def parse_block_references(
    text: str
) -> Dict[str, Any]:
    """
    Parse @@ block references from natural language text.
    Returns list of referenced block IDs.

    Args:
        text: Natural language text containing @@block-id references

    Returns:
        List of parsed block IDs
    """
    # Pattern matches @@block-name or @@block-id-123
    pattern = r'@@([a-zA-Z0-9\-_]+)'
    matches = re.findall(pattern, text)

    return {
        "success": True,
        "text": text,
        "referenced_blocks": matches,
        "count": len(matches)
    }


@tool
async def evaluate_condition(
    condition_description: str,
    workflow_context: Dict[str, Any],
    referenced_blocks_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Evaluate a natural language condition against workflow context.
    This is the core decision-making tool for condition blocks.

    Args:
        condition_description: Natural language description of the condition
        workflow_context: Current workflow instance context
        referenced_blocks_data: Output data from referenced blocks (@@syntax)

    Returns:
        Decision (true/false/escalate) with reasoning
    """
    # This is a placeholder that will be enhanced by the agent
    # The agent will use its reasoning to evaluate the condition

    return {
        "tool": "evaluate_condition",
        "condition": condition_description,
        "context": workflow_context,
        "references": referenced_blocks_data,
        "note": "This tool provides context. Agent will make the actual decision."
    }


@tool
async def decide_loop_action(
    continue_rule: str,
    break_rule: str,
    escalation_rule: Optional[str],
    workflow_context: Dict[str, Any],
    iteration_count: int,
    referenced_blocks_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Decide whether to continue, break, or escalate a loop based on natural language rules.
    This is the core decision-making tool for loop blocks.

    Args:
        continue_rule: Natural language rule for when to continue
        break_rule: Natural language rule for when to break
        escalation_rule: Optional rule for when to escalate to human
        workflow_context: Current workflow instance context
        iteration_count: Current loop iteration number
        referenced_blocks_data: Output data from referenced blocks

    Returns:
        Action (continue/break/escalate) with reasoning
    """
    # This is a placeholder that will be enhanced by the agent
    # The agent will use its reasoning to make the loop decision

    return {
        "tool": "decide_loop_action",
        "continue_rule": continue_rule,
        "break_rule": break_rule,
        "escalation_rule": escalation_rule,
        "iteration": iteration_count,
        "context": workflow_context,
        "references": referenced_blocks_data,
        "note": "This tool provides context. Agent will make the actual decision."
    }


@tool
async def trigger_escalation(
    reason: str,
    workflow_instance_id: str,
    reviewer_id: Optional[str] = None,
    priority: str = "normal"
) -> Dict[str, Any]:
    """
    Trigger a human escalation/review for a workflow instance.

    Args:
        reason: Explanation of why escalation is needed
        workflow_instance_id: The workflow instance requiring review
        reviewer_id: Optional specific reviewer to assign
        priority: Priority level (low/normal/high/urgent)

    Returns:
        Escalation confirmation with tracking ID
    """
    import uuid

    escalation_id = f"escalation-{uuid.uuid4().hex[:8]}"

    return {
        "success": True,
        "escalation_id": escalation_id,
        "workflow_instance_id": workflow_instance_id,
        "reason": reason,
        "reviewer_id": reviewer_id,
        "priority": priority,
        "created_at": "2025-10-20T12:00:00Z",
        "message": f"Escalation {escalation_id} created for manual review"
    }


@tool
async def get_workflow_execution_context(
    instance_id: str,
    include_history: bool = True
) -> Dict[str, Any]:
    """
    Get the full execution context for a workflow instance.
    Used by agents to understand the current state when making decisions.

    Args:
        instance_id: Workflow instance identifier
        include_history: Whether to include full execution history

    Returns:
        Complete workflow instance context
    """
    # Mock data - replace with database query
    return {
        "success": True,
        "instance_id": instance_id,
        "status": "running",
        "patient_id": "patient-001",
        "triggered_by": {
            "event": "report_available",
            "object_id": "report-001"
        },
        "execution_history": [
            {
                "block_id": "block-trigger-1",
                "type": "trigger-report",
                "status": "completed",
                "output": {"report_id": "report-001", "report_type": "Lab Results"}
            },
            {
                "block_id": "block-condition-1",
                "type": "condition",
                "status": "running",
                "input": {"report_id": "report-001"}
            }
        ] if include_history else [],
        "context_data": {
            "patient_name": "John Smith",
            "report_type": "Lab Results",
            "has_abnormal_results": False
        }
    }


@tool
async def log_agent_decision(
    decision_type: str,
    decision: str,
    reasoning: str,
    instance_id: str,
    block_id: str,
    confidence: Optional[float] = None
) -> Dict[str, Any]:
    """
    Log an agent's decision for audit trail and compliance.
    Important for HIPAA and healthcare regulations.

    Args:
        decision_type: Type of decision (condition/loop/approval)
        decision: The actual decision made
        reasoning: Agent's reasoning for the decision
        instance_id: Workflow instance ID
        block_id: Block ID where decision was made
        confidence: Optional confidence score

    Returns:
        Logging confirmation
    """
    import uuid
    from datetime import datetime

    log_id = f"log-{uuid.uuid4().hex[:8]}"
    timestamp = datetime.now().isoformat()

    return {
        "success": True,
        "log_id": log_id,
        "timestamp": timestamp,
        "decision_type": decision_type,
        "decision": decision,
        "reasoning": reasoning,
        "instance_id": instance_id,
        "block_id": block_id,
        "confidence": confidence,
        "message": "Decision logged for audit trail"
    }


# Create the MCP server for execution tools
execution_mcp_server = create_sdk_mcp_server(
    "execution-tools",
    [
        parse_block_references,
        evaluate_condition,
        decide_loop_action,
        trigger_escalation,
        get_workflow_execution_context,
        log_agent_decision
    ]
)
