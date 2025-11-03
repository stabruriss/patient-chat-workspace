"""
Healthcare data models based on obj-status.md
Represents the status tracking for healthcare objects
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class PatientProfileStatus(str, Enum):
    CREATED = "created"
    UPDATED = "updated"


class OrderStatus(str, Enum):
    ORDER_CREATED = "order_created"
    ORDER_MODIFIED = "order_modified"
    ORDER_REDRAWN = "order_redrawn"
    PAYMENT_COMPLETE = "payment_complete"
    PAYMENT_REFUND = "payment_refund"
    PAYMENT_FAILED = "payment_failed"
    LAB_SHIPPED = "lab_shipped"
    QUESTIONNAIRE_ASSIGNED = "questionnaire_assigned"
    MISSING_INFORMATION = "missing_information"
    TEST_NOT_PERFORMED = "test_not_performed"
    ORDER_CANCELED = "order_canceled"


class ReportStatus(str, Enum):
    REPORT_AVAILABLE = "report_available"
    REPORT_SHARED = "report_shared"


class EncounterNoteStatus(str, Enum):
    SHARED = "shared"
    UPDATED = "updated"


class DocumentFormStatus(str, Enum):
    VIEWED = "viewed"
    SUBMITTED = "submitted"


class CalendarEventStatus(str, Enum):
    CREATED = "created"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TENTATIVE = "tentative"
    CANCELLED = "cancelled"


class TaskStatus(str, Enum):
    OPEN = "open"
    COMPLETED = "completed"


class InternalNoteStatus(str, Enum):
    UPDATED = "updated"


class StatusEvent(BaseModel):
    """Represents a single status change event"""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[dict] = None


class HealthcareObject(BaseModel):
    """Base class for all healthcare objects"""
    object_id: str
    object_type: str
    patient_id: Optional[str] = None
    status_history: List[StatusEvent] = Field(default_factory=list)
    current_status: Optional[str] = None

    def add_status(self, status: str, metadata: Optional[dict] = None):
        """Add a new status event"""
        event = StatusEvent(status=status, metadata=metadata)
        self.status_history.append(event)
        self.current_status = status

    def get_latest_status(self) -> Optional[StatusEvent]:
        """Get the most recent status event"""
        return self.status_history[-1] if self.status_history else None


class PatientProfile(HealthcareObject):
    object_type: str = "patient_profile"
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class Order(HealthcareObject):
    object_type: str = "order"
    order_number: Optional[str] = None
    items: List[dict] = Field(default_factory=list)
    total_amount: Optional[float] = None


class Report(HealthcareObject):
    object_type: str = "report"
    report_type: Optional[str] = None
    results: Optional[dict] = None
    provider_notes: Optional[str] = None


class EncounterNote(HealthcareObject):
    object_type: str = "encounter_note"
    encounter_date: Optional[datetime] = None
    chief_complaint: Optional[str] = None
    notes: Optional[str] = None


class DocumentForm(HealthcareObject):
    object_type: str = "document_form"
    form_type: Optional[str] = None
    content: Optional[dict] = None


class CalendarEvent(HealthcareObject):
    object_type: str = "calendar_event"
    event_date: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    attendees: List[str] = Field(default_factory=list)


class Task(HealthcareObject):
    object_type: str = "task"
    title: Optional[str] = None
    description: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None


class InternalNote(HealthcareObject):
    object_type: str = "internal_note"
    note_text: Optional[str] = None
    author: Optional[str] = None
