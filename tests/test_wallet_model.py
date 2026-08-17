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
