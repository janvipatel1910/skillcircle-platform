from uuid import UUID

from backend.models.task import Task, TaskStatus
from backend.models.wallet import Wallet


def complete_task(
    task: Task,
    confirmed_by_id: UUID,
    requester_wallet: Wallet,
    helper_wallet: Wallet,
) -> None:
    """Complete a submitted task and transfer its reward exactly once."""

    if task.status is not TaskStatus.SUBMITTED:
        raise ValueError("Only submitted tasks can be completed")

    if confirmed_by_id != task.requester_id:
        raise ValueError("Only the requester can confirm task completion")

    if requester_wallet.user_id != task.requester_id:
        raise ValueError("Requester wallet does not match the task requester")

    if task.helper_id is None or helper_wallet.user_id != task.helper_id:
        raise ValueError("Helper wallet does not match the assigned helper")

    if requester_wallet.reserved_credits < task.reward_credits:
        raise ValueError("Task reward is not fully reserved")

    requester_wallet.spend_reserved(task.reward_credits)
    helper_wallet.credit(task.reward_credits)
    task.status = TaskStatus.COMPLETED










