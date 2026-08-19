from uuid import uuid4

import pytest

from backend.models.wallet import WELCOME_CREDITS, Wallet


def test_new_wallet_receives_welcome_credits():
    wallet = Wallet(user_id=uuid4())

    assert wallet.available_credits == WELCOME_CREDITS
    assert wallet.reserved_credits == 0
    assert wallet.total_credits == WELCOME_CREDITS


def test_reserve_and_release_preserve_total_credits():
    wallet = Wallet(user_id=uuid4())

    wallet.reserve(6000)

    assert wallet.available_credits == 4000
    assert wallet.reserved_credits == 6000
    assert wallet.total_credits == 10000

    wallet.release(6000)

    assert wallet.available_credits == 10000
    assert wallet.reserved_credits == 0
    assert wallet.total_credits == 10000


def test_wallet_rejects_insufficient_available_credits():
    wallet = Wallet(user_id=uuid4())

    with pytest.raises(ValueError, match="Insufficient available credits"):
        wallet.reserve(11000)

    assert wallet.available_credits == 10000
    assert wallet.reserved_credits == 0
def test_reserved_credits_can_be_paid_to_helper():
    requester_wallet = Wallet(user_id=uuid4())
    helper_wallet = Wallet(user_id=uuid4())

    requester_wallet.reserve(4000)
    requester_wallet.spend_reserved(4000)
    helper_wallet.credit(4000)

    assert requester_wallet.available_credits == 6000
    assert requester_wallet.reserved_credits == 0
    assert requester_wallet.total_credits == 6000

    assert helper_wallet.available_credits == 14000
    assert helper_wallet.reserved_credits == 0
    assert helper_wallet.total_credits == 14000


def test_wallet_rejects_payment_above_reserved_credits():
    wallet = Wallet(user_id=uuid4())
    wallet.reserve(3000)

    with pytest.raises(ValueError, match="Insufficient reserved credits"):
        wallet.spend_reserved(4000)

    assert wallet.available_credits == 7000
    assert wallet.reserved_credits == 3000


def test_wallet_rejects_zero_credit():
    wallet = Wallet(user_id=uuid4())

    with pytest.raises(ValueError, match="Credit amount must be greater than zero"):
        wallet.credit(0)

    assert wallet.available_credits == WELCOME_CREDITS
