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
