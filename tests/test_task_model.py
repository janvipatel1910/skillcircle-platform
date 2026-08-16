from uuid import uuid4

import pytest
from pydantic import ValidationError

from backend.models.task import Task, TaskStatus


def test_valid_task_starts_open_without_helper():
    task = Task(
        title="Learn basic Excel",
        description="I need an online lesson about Excel formulas.",
        required_skill="Excel",
        reward_credits=5000,
        requester_id=uuid4(),
    )

    assert task.status is TaskStatus.OPEN
    assert task.helper_id is None
    assert task.reward_credits == 5000
    assert task.created_at.tzinfo is not None


def test_zero_reward_credits_are_rejected():
    with pytest.raises(ValidationError, match="greater than 0"):
        Task(
            title="Learn basic Excel",
            description="I need an online lesson about Excel formulas.",
            required_skill="Excel",
            reward_credits=0,
            requester_id=uuid4(),
        )
