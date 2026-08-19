from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class TaskStatus(StrEnum):
    """Allowed states for a SkillCircle task."""

    OPEN = "OPEN"
    ASSIGNED = "ASSIGNED"
    SUBMITTED = "SUBMITTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class TaskCreate(BaseModel):
    """Information supplied when a requester creates a task."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=1000)
    required_skill: str = Field(min_length=2, max_length=50)
    reward_credits: int = Field(gt=0)


class Task(TaskCreate):
    """Complete task stored by the SkillCircle system."""

    task_id: UUID = Field(default_factory=uuid4)
    requester_id: UUID
    helper_id: UUID | None = None
    status: TaskStatus = TaskStatus.OPEN
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    def assign(self, helper_id: UUID) -> None:
        """Assign an open task to a helper."""

        if self.status is not TaskStatus.OPEN:
            raise ValueError("Only open tasks can be assigned")

        if helper_id == self.requester_id:
            raise ValueError("Requester cannot help their own task")

        self.helper_id = helper_id
        self.status = TaskStatus.ASSIGNED

    def submit(self, helper_id: UUID) -> None:
        """Mark an assigned task as submitted by its helper."""

        if self.status is not TaskStatus.ASSIGNED:
            raise ValueError("Only assigned tasks can be submitted")

        if helper_id != self.helper_id:
            raise ValueError("Only the assigned helper can submit this task")

        self.status = TaskStatus.SUBMITTED
