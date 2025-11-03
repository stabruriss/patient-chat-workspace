"""
Custom MCP tools for healthcare context and data
These tools allow the agent to understand healthcare-specific information
"""
from typing import Dict, Any, List, Optional
from claude_agent_sdk import tool, create_sdk_mcp_server
from datetime import datetime


# Mock healthcare data storage (replace with real database in production)
mock_patients: Dict[str, Dict[str, Any]] = {
    "patient-001": {
        "id": "patient-001",
        "name": "John Smith",
        "email": "john.smith@email.com",
        "phone": "(555) 123-4567",
        "status_history": [
            {"status": "created", "timestamp": "2025-01-15T10:00:00Z"},
            {"status": "updated", "timestamp": "2025-01-20T14:30:00Z"}
        ]
    }
}

mock_healthcare_objects: Dict[str, Dict[str, Any]] = {
    "order-001": {
        "object_id": "order-001",
        "object_type": "order",
        "patient_id": "patient-001",
        "current_status": "payment_complete",
        "order_number": "ORD-2025-001",
        "items": ["Complete Blood Count", "Lipid Panel"],
        "status_history": [
            {"status": "order_created", "timestamp": "2025-01-15T10:00:00Z"},
            {"status": "payment_complete", "timestamp": "2025-01-15T10:05:00Z"}
        ]
    },
    "report-001": {
        "object_id": "report-001",
        "object_type": "report",
        "patient_id": "patient-001",
        "current_status": "report_available",
        "report_type": "Lab Results",
        "status_history": [
            {"status": "report_available", "timestamp": "2025-01-18T09:00:00Z"}
        ]
    }
}


@tool
async def get_patient_status(
    patient_id: str,
    object_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get the current status and history for a patient and their associated healthcare objects.

    Args:
        patient_id: The patient identifier
        object_type: Optional filter for specific object type (e.g., "order", "report")

    Returns:
        Patient information and status history
    """
    patient = mock_patients.get(patient_id)
    if not patient:
        return {
            "success": False,
            "error": f"Patient {patient_id} not found"
        }

    # Get all objects for this patient
    patient_objects = [
        obj for obj in mock_healthcare_objects.values()
        if obj.get("patient_id") == patient_id
        and (object_type is None or obj.get("object_type") == object_type)
    ]

    return {
        "success": True,
        "patient": patient,
        "objects": patient_objects,
        "object_count": len(patient_objects)
    }


@tool
async def get_healthcare_object(
    object_id: str
) -> Dict[str, Any]:
    """
    Retrieve a specific healthcare object by ID.

    Args:
        object_id: The healthcare object identifier

    Returns:
        Healthcare object details with status history
    """
    obj = mock_healthcare_objects.get(object_id)
    if not obj:
        return {
            "success": False,
            "error": f"Healthcare object {object_id} not found"
        }

    return {
        "success": True,
        "object": obj
    }


@tool
async def query_workflow_history(
    workflow_id: str,
    patient_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query the execution history of workflows.

    Args:
        workflow_id: The workflow identifier
        patient_id: Optional patient filter for patient-specific workflows

    Returns:
        Workflow execution history and statistics
    """
    # Mock data - replace with database query
    return {
        "success": True,
        "workflow_id": workflow_id,
        "executions": [
            {
                "instance_id": "wf-inst-001",
                "patient_id": patient_id or "patient-001",
                "status": "completed",
                "started_at": "2025-01-18T09:00:00Z",
                "completed_at": "2025-01-18T09:05:00Z",
                "blocks_executed": 5
            }
        ],
        "total_executions": 1,
        "success_rate": 100.0
    }


@tool
async def get_healthcare_objects_by_status(
    object_type: str,
    status: str,
    patient_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Find healthcare objects matching specific type and status criteria.

    Args:
        object_type: Type of healthcare object (e.g., "order", "report", "task")
        status: Status to filter by (e.g., "report_available", "order_created")
        patient_id: Optional patient filter

    Returns:
        List of matching healthcare objects
    """
    matching_objects = [
        obj for obj in mock_healthcare_objects.values()
        if obj.get("object_type") == object_type
        and obj.get("current_status") == status
        and (patient_id is None or obj.get("patient_id") == patient_id)
    ]

    return {
        "success": True,
        "object_type": object_type,
        "status": status,
        "objects": matching_objects,
        "count": len(matching_objects)
    }


@tool
async def get_available_healthcare_statuses(
    object_type: str
) -> Dict[str, Any]:
    """
    Get all possible statuses for a specific healthcare object type.
    Based on obj-status.md definitions.

    Args:
        object_type: Type of healthcare object

    Returns:
        List of valid statuses for that object type
    """
    status_map = {
        "patient_profile": ["created", "updated"],
        "order": [
            "order_created", "order_modified", "order_redrawn",
            "payment_complete", "payment_refund", "payment_failed",
            "lab_shipped", "questionnaire_assigned", "missing_information",
            "test_not_performed", "order_canceled"
        ],
        "report": ["report_available", "report_shared"],
        "encounter_note": ["shared", "updated"],
        "document_form": ["viewed", "submitted"],
        "calendar_event": ["created", "accepted", "rejected", "tentative", "cancelled"],
        "task": ["open", "completed"],
        "internal_note": ["updated"]
    }

    statuses = status_map.get(object_type, [])

    return {
        "success": True,
        "object_type": object_type,
        "statuses": statuses,
        "count": len(statuses)
    }


@tool
async def interpret_healthcare_context(
    context_description: str,
    referenced_objects: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Interpret healthcare context and extract relevant information for decision-making.
    This is used by condition and loop evaluation to understand medical context.

    Args:
        context_description: Natural language description of what to look for
        referenced_objects: List of healthcare objects to analyze

    Returns:
        Interpreted context with insights
    """
    insights = []

    # Analyze referenced objects
    for obj in referenced_objects:
        obj_type = obj.get("object_type")
        status = obj.get("current_status")

        if obj_type == "report" and status == "report_available":
            insights.append(f"New {obj.get('report_type', 'report')} is available for review")
        elif obj_type == "order" and status == "payment_complete":
            insights.append(f"Order {obj.get('order_number')} payment confirmed")
        elif obj_type == "task" and status == "open":
            insights.append(f"Task '{obj.get('title', 'untitled')}' is pending")

    return {
        "success": True,
        "context_description": context_description,
        "insights": insights,
        "object_count": len(referenced_objects),
        "interpretation": " | ".join(insights) if insights else "No specific insights detected"
    }


# Create the MCP server for healthcare tools
healthcare_mcp_server = create_sdk_mcp_server(
    "healthcare-tools",
    [
        get_patient_status,
        get_healthcare_object,
        query_workflow_history,
        get_healthcare_objects_by_status,
        get_available_healthcare_statuses,
        interpret_healthcare_context
    ]
)
