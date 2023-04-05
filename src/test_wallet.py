import pytest
from wallet import Wallet


@pytest.fixture
def empty_wallet():
    return Wallet(0)


@pytest.fixture
def wallet():
    return Wallet(100)


def test_empty_wallet_copper(empty_wallet):
    assert empty_wallet.copper == 0


def test_empty_wallet_silver(empty_wallet):
    assert empty_wallet.silver == 0


def test_empty_wallet_gold(empty_wallet):
    assert empty_wallet.gold == 0


def test_wallet_copper(wallet):
    assert wallet.copper == 100


def test_wallet_silver(wallet):
    assert wallet.silver == 1


def test_wallet_gold(wallet):
    assert wallet.gold == 0


def test_wallet_add(wallet):
    wallet.add(50)
    assert wallet.balance == 150


def test_wallet_add_negative_raises_exception(wallet):
    with pytest.raises(ValueError):
        wallet.add(-5)


def test_wallet_sub(wallet):
    wallet.sub(50)
    assert wallet.balance == 50


def test_wallet_sub_negative_raises_exception(wallet):
    with pytest.raises(ValueError):
        wallet.sub(-5)


def test_wallet_sub_insufficient_funds_raises_exception(wallet):
    with pytest.raises(ValueError):
        wallet.sub(1500)
