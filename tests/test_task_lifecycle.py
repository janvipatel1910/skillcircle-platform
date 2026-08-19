from uuid import uuid4

import pytest

from backend.models.task import Task, TaskStatus
from backend.models.wallet import Wallet
from backend.services.task_lifecycle import complete_task


def build_submitted_task():
    requester_id = uuid4()
    helper_id = uuid4()

    task = Task(
        title="Learn basic Excel",
        description="I need an online lesson about Excel formulas.",
        required_skill="Excel",
        reward_credits=4000,
        requester_id=requester_id,
    )
    requester_wallet = Wallet(user_id=requester_id)
    helper_wallet = Wallet(user_id=helper_id)

    requester_wallet.reserve(task.reward_credits)
    task.assign(helper_id)
    task.submit(helper_id)

    return task, requester_wallet, helper_wallet


def test_requester_can_complete_task_and_reward_helper():
    task, requester_wallet, helper_wallet = build_submitted_task()

    complete_task(
        task,
        task.requester_id,
        requester_wallet,
        helper_wallet,
    )

    assert task.status is TaskStatus.COMPLETED
    assert requester_wallet.available_credits == 6000
    assert requester_wallet.reserved_credits == 0
    assert helper_wallet.available_credits == 14000


def test_completed_task_cannot_reward_helper_twice():
    task, requester_wallet, helper_wallet = build_submitted_task()

    complete_task(
        task,
        task.requester_id,
        requester_wallet,
        helper_wallet,
    )

    with pytest.raises(ValueError, match="Only submitted tasks"):
        complete_task(
            task,
            task.requester_id,
            requester_wallet,
            helper_wallet,
        )

    assert requester_wallet.available_credits == 6000
    assert requester_wallet.reserved_credits == 0
    assert helper_wallet.available_credits == 14000


def test_only_requester_can_confirm_completion():
    task, requester_wallet, helper_wallet = build_submitted_task()

    with pytest.raises(ValueError, match="Only the requester"):
        complete_task(
            task,
            uuid4(),
            requester_wallet,
            helper_wallet,
        )

    assert task.status is TaskStatus.SUBMITTED
    assert requester_wallet.reserved_credits == 4000
    assert helper_wallet.available_credits == 10000
