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
def test_task_can_be_assigned_and_submitted_by_helper():
    requester_id = uuid4()
    helper_id = uuid4()
    task = Task(
        title="Learn basic Excel",
        description="I need an online lesson about Excel formulas.",
        required_skill="Excel",
        reward_credits=5000,
        requester_id=requester_id,
    )

    task.assign(helper_id)

    assert task.helper_id == helper_id
    assert task.status is TaskStatus.ASSIGNED

    task.submit(helper_id)

    assert task.status is TaskStatus.SUBMITTED


def test_requester_cannot_help_their_own_task():
    requester_id = uuid4()
    task = Task(
        title="Learn basic Excel",
        description="I need an online lesson about Excel formulas.",
        required_skill="Excel",
        reward_credits=5000,
        requester_id=requester_id,
    )

    with pytest.raises(ValueError, match="Requester cannot help"):
        task.assign(requester_id)

    assert task.status is TaskStatus.OPEN
    assert task.helper_id is None


def test_unassigned_helper_cannot_submit_task():
    assigned_helper_id = uuid4()
    different_helper_id = uuid4()
    task = Task(
        title="Learn basic Excel",
        description="I need an online lesson about Excel formulas.",
        required_skill="Excel",
        reward_credits=5000,
        requester_id=uuid4(),
    )
    task.assign(assigned_helper_id)

    with pytest.raises(ValueError, match="Only the assigned helper"):
        task.submit(different_helper_id)

    assert task.status is TaskStatus.ASSIGNED
