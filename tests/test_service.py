import pytest
from datetime import datetime
from bank_system import service

loan1 = {
    "service_type": "Loan",
    "service_id": 100,
    "customer_id": 10001,
    "created_at": datetime(2021, 12, 30, 1, 55, 59, 111110),
    "borrowed_amount": 10000,
    "interest_rate": .01,
    "term": 2,
    "payed": 0
}

credit1 = {
    "borrowed_amount": 500,
    "service_type": "CreditCard",
    "service_id": 100,
    "customer_id": 10001,
    "created_at": datetime(2021, 12, 30, 1, 55, 59, 111110),
    "interest_rate": .02,
    "max_limit": 10000,
    "annual_fee": 80
}


@pytest.fixture
def loan_obj():
    return service.Loan(
        loan1["borrowed_amount"],
        loan1["interest_rate"],
        loan1["term"],
        loan1["payed"],
        loan1["service_id"],
        loan1["customer_id"],
        loan1["created_at"],
    )


@pytest.fixture
def credit_obj():
    return service.CreditCard(
        credit1["borrowed_amount"],
        credit1["interest_rate"],
        credit1["max_limit"],
        credit1["annual_fee"],
        credit1["service_id"],
        credit1["customer_id"],
        credit1["created_at"],
    )


def test_customer_id(loan_obj, credit_obj):
    assert loan_obj.customer_id == loan1["customer_id"]
    assert credit_obj.customer_id == credit1["customer_id"]
    loan_obj.customer_id = 1
    credit_obj.customer_id = 1
    assert loan_obj.customer_id == loan1["customer_id"]
    assert credit_obj.customer_id == credit1["customer_id"]


def test_data_dict(loan_obj, credit_obj):
    assert loan_obj.data_dict == loan1
    assert credit_obj.data_dict == credit1


def test_loan_left(loan_obj):
    assert loan_obj.loan_left == loan1["borrowed_amount"] + (
        loan1["borrowed_amount"] * loan1["interest_rate"]) - loan1["payed"]


def test_loan_pay(loan_obj):
    amt = 10
    amtOver = loan1["borrowed_amount"] * 10
    loan_left = (
        loan1["borrowed_amount"] +
        (loan1["borrowed_amount"] * loan1["interest_rate"]) - loan1["payed"])

    assert loan_obj.pay(amt) == loan_left - amt

    with pytest.raises(service.OverpayedError):
        loan_obj.pay(amtOver)


def test_credit_interest(credit_obj):
    assert credit_obj.interest == (
        credit1["borrowed_amount"] * credit1["interest_rate"])


def test_credit_pay(credit_obj):
    amt = 10
    assert credit_obj.pay(amt) == credit1["borrowed_amount"] - amt


def test_credit_borrow(credit_obj):
    amt = 10
    assert credit_obj.borrow(amt) == credit1["borrowed_amount"] + amt

    with pytest.raises(service.CreditLimitError):
        credit_obj.borrow(credit1["max_limit"] + 10)
