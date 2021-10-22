import pytest
from datetime import datetime
from bank_system import account

savings1 = {
    "balance": 1000,
    "account_type": "Savings",
    "account_id": 1001,
    "customer_id": 2001,
    "savings_rate": .02,
    "created_at": datetime(2021, 12, 30, 1, 55, 59, 111110)
}

checking1 = {
    "balance": 1000,
    "account_type": "Checking",
    "account_id": 1001,
    "customer_id": 2001,
    "min_balance": 500,
    "created_at": datetime(2020, 12, 30, 1, 55, 59, 111110)
}


@pytest.fixture
def savings_obj() -> account.Savings:
    return account.Savings(
        savings1["balance"],
        savings1["customer_id"],
        savings1["savings_rate"],
        savings1["account_id"],
        savings1["created_at"]
    )


@pytest.fixture
def checking_obj() -> account.Checking:
    return account.Checking(
        checking1["balance"],
        checking1["min_balance"],
        checking1["customer_id"],
        checking1["account_id"],
        checking1["created_at"],
    )


def test_created_at(savings_obj, checking_obj):
    assert savings_obj.created_at == savings1["created_at"]
    assert checking_obj.created_at == checking1["created_at"]


def test_balance(savings_obj, checking_obj):
    assert savings_obj.balance == savings1["balance"]
    assert checking_obj.balance == checking1["balance"]


def test_account_type(savings_obj, checking_obj):
    assert savings_obj.account_type == savings1["account_type"]
    assert checking_obj.account_type == checking1["account_type"]


def test_account_id(savings_obj, checking_obj):
    assert savings_obj.account_id == savings1["account_id"]
    assert checking_obj.account_id == checking1["account_id"]
    savings_obj.account_id = 1
    checking_obj.account_id = 1
    assert savings_obj.account_id == savings1["account_id"]


def test_customer_id(savings_obj, checking_obj):
    assert savings_obj.customer_id == savings1["customer_id"]
    assert checking_obj.customer_id == checking1["customer_id"]
    savings_obj.customer_id = 1
    checking_obj.customer_id = 1
    assert savings_obj.customer_id == savings1["customer_id"]
    assert checking_obj.customer_id == checking1["customer_id"]


def test_data_dict(savings_obj, checking_obj):
    assert savings_obj.data_dict == savings1
    assert checking_obj.data_dict == checking1


def test_withdraw(savings_obj, checking_obj):
    amt = 5
    savings_obj.withdraw(amt)
    checking_obj.withdraw(amt)
    assert savings_obj.balance == savings1["balance"] - amt
    assert checking_obj.balance == checking1["balance"] - amt


def test_deposit(savings_obj, checking_obj):
    amt = 5
    savings_obj.deposit(amt)
    checking_obj.deposit(amt)
    assert savings_obj.balance == savings1["balance"] + amt
    assert checking_obj.balance == checking1["balance"] + amt


def test_withdraw_except(savings_obj, checking_obj):
    amtS = savings_obj.balance + 5
    amtC = checking_obj.balance + 5
    with pytest.raises(account.OverdraftError):
        savings_obj.withdraw(amtS)
    with pytest.raises(account.OverdraftError):
        checking_obj.withdraw(amtC)
