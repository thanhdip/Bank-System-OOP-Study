import pytest
from datetime import datetime
from bank_system import person

employee1 = {
    "first_name": "Bob",
    "last_name": "Donald",
    "address": "123 Caspy",
    "created_at": datetime(2021, 12, 30, 1, 55, 59, 111110),
    "id": 1000,
    "title": "Teller",
    "salary": 50000
}

customer1 = {
    "first_name": "Alice",
    "last_name": "Drake",
    "address": "456 Take",
    "created_at": datetime(2020, 12, 30, 1, 55, 59, 111110),
    "id": 2000,
    "services": [],
    "accounts": []
}


@pytest.fixture
def employee_obj():
    return person.Employee(
        employee1["first_name"],
        employee1["last_name"],
        employee1["address"],
        employee1["title"],
        employee1["salary"],
        employee1["id"],
        employee1["created_at"],
    )


@pytest.fixture
def customer_obj():
    return person.Customer(
        customer1["first_name"],
        customer1["last_name"],
        customer1["address"],
        customer1["created_at"],
        customer1["id"],
        customer1["accounts"],
        customer1["services"],
    )


def test_full_name(employee_obj, customer_obj):
    e_fn = employee1["first_name"]
    e_ln = employee1["last_name"]
    c_fn = customer1["first_name"]
    c_ln = customer1["last_name"]
    assert employee_obj.full_name == f"{e_fn} {e_ln}"
    assert customer_obj.full_name == f"{c_fn} {c_ln}"


def test_data_dict(employee_obj, customer_obj):
    assert employee_obj.data_dict == employee1
    assert customer_obj.data_dict == customer1


def test_employee_id(employee_obj):
    assert employee_obj.employee_id == employee1["employee_id"]
    employee_obj.employee_id = 1
    assert employee_obj.employee_id == employee1["employee_id"]


def test_customer_id(customer_obj):
    assert customer_obj.customer_id == customer1["customer_id"]
    customer_obj.customer_id = 1
    assert customer_obj.customer_id == customer1["customer_id"]
