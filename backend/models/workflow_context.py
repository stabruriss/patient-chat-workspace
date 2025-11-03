"""
Workflow context and state management
Represents the runtime state of a workflow instance
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum


class WorkflowType(str, Enum):
    PATIENT = "patient"
    PRACTICE = "practice"


class BlockType(str, Enum):
    # Triggers
    TRIGGER_PATIENT_PROFILE = "trigger-patient-profile"
    TRIGGER_ORDER = "trigger-order"
    TRIGGER_REPORT = "trigger-report"
    TRIGGER_ENCOUNTER_NOTE = "trigger-encounter-note"
    TRIGGER_DOCUMENT = "trigger-document"
    TRIGGER_CALENDAR_EVENT = "trigger-calendar-event"
    TRIGGER_TASK = "trigger-task"
    TRIGGER_INTERNAL_NOTE = "trigger-internal-note"
    TRIGGER_SCHEDULED = "trigger-scheduled"
    TRIGGER_THRESHOLD = "trigger-threshold"

    # Actions
    ACTION_SEND_MESSAGE = "action-send-message"
    ACTION_SEND_EMAIL = "action-send-email"
    ACTION_CREATE_TASK = "action-create-task"
    ACTION_UPDATE_PATIENT = "action-update-patient"
    ACTION_GENERATE_REPORT = "action-generate-report"

    # Logic
    WAIT = "wait"
    CONDITION = "condition"
    LOOP = "loop"
    APPROVAL = "approval"
    AI_TOUCH = "ai-touch"


class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    WAITING = "waiting"
    ESCALATED = "escalated"


class BlockExecution(BaseModel):
    """Represents the execution of a single block"""
    block_id: str
    block_type: str
    status: ExecutionStatus
    input_data: Optional[Dict[str, Any]] = None
    output_data: Optional[Dict[str, Any]] = None
    ai_reasoning: Optional[str] = None  # For AI-driven decisions
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    execution_order: int = 0


class WorkflowInstance(BaseModel):
    """Represents a running instance of a workflow"""
    instance_id: str
    workflow_id: str
    workflow_type: WorkflowType
    patient_id: Optional[str] = None  # For patient workflows
    status: ExecutionStatus
    triggered_by: Dict[str, Any]  # The event that triggered this workflow
    execution_history: List[BlockExecution] = Field(default_factory=list)
    current_block_id: Optional[str] = None
    context_data: Dict[str, Any] = Field(default_factory=dict)  # Shared data across blocks
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    def add_execution(self, execution: BlockExecution):
        """Add a block execution to history"""
        execution.execution_order = len(self.execution_history)
        self.execution_history.append(execution)
        self.updated_at = datetime.now()

    def get_block_output(self, block_id: str) -> Optional[Dict[str, Any]]:
        """Get the output data from a previously executed block"""
        for execution in reversed(self.execution_history):
            if execution.block_id == block_id:
                return execution.output_data
        return None

    def get_referenced_blocks(self, block_ids: List[str]) -> Dict[str, Any]:
        """Get outputs from multiple referenced blocks (for @@ syntax)"""
        results = {}
        for block_id in block_ids:
            output = self.get_block_output(block_id)
            if output:
                results[block_id] = output
        return results


class WorkflowDefinition(BaseModel):
    """Represents a saved workflow definition"""
    workflow_id: str
    name: str
    description: Optional[str] = None
    workflow_type: WorkflowType
    blocks: List[Dict[str, Any]]  # The workflow blocks from the composer
    created_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True


class ConditionEvaluationRequest(BaseModel):
    """Request to evaluate a condition block"""
    condition_description: str
    workflow_context: Dict[str, Any]
    referenced_block_ids: List[str] = Field(default_factory=list)
    instance_id: str


class ConditionEvaluationResponse(BaseModel):
    """Response from condition evaluation"""
    decision: str  # "true", "false", or "escalate"
    reasoning: str
    confidence: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class LoopEvaluationRequest(BaseModel):
    """Request to evaluate a loop decision"""
    continue_rule: str
    break_rule: str
    escalation_rule: Optional[str] = None
    workflow_context: Dict[str, Any]
    referenced_block_ids: List[str] = Field(default_factory=list)
    iteration_count: int
    instance_id: str


class LoopEvaluationResponse(BaseModel):
    """Response from loop evaluation"""
    action: str  # "continue", "break", or "escalate"
    reasoning: str
    confidence: Optional[float] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class WorkflowGenerationRequest(BaseModel):
    """Request to generate a workflow from natural language"""
    description: str
    workflow_type: WorkflowType
    existing_blocks: Optional[List[Dict[str, Any]]] = None
    conversation_history: List[Dict[str, str]] = Field(default_factory=list)


class WorkflowGenerationResponse(BaseModel):
    """Response containing generated workflow blocks"""
    blocks: List[Dict[str, Any]]
    explanation: str
    suggested_name: Optional[str] = None
    suggested_description: Optional[str] = None
