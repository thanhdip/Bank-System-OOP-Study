import pytest
from datetime import datetime
from bank_system.account import Account
from bank_system.person import Person
from bank_system.service import Service
from bank_system.database import BankDatabase
from bank_system.person import Employee, Customer
from bank_system.service import Loan, CreditCard
from bank_system.account import Checking, Savings

objs = []
objs.append(Employee("Soren", "Kierke", "Germany", "Teller", 50000))
objs.append(Customer("Gregory", "Nyssa", "Georgia"))
objs.append(Loan(50000, .01, 1))
objs.append(CreditCard(40000, .02, 1))
objs.append(Checking(10000, 500, 1))
objs.append(Savings(20000, 1))

ids = [1, 1, 1, 2, 1, 2]

main_db = BankDatabase("test", mem_mode=True)


def test_save_data():
    for i, obj in enumerate(objs):
        res = main_db.save_data(type(obj).__name__, obj.data_dict)
        obj.id = res[0]
        obj.created_at = res[1]
        assert res[0] == ids[i]
        assert isinstance(obj.created_at, datetime)


def test_find_customer():
    fn = "cus1"
    ln = "lassy"
    ad = "nowhere"
    obj = Customer(fn, ln, ad)
    main_db.save_data(type(obj).__name__, obj.data_dict)
    assert main_db.find_customer(fn, ln, ad)[0]["first_name"] == fn


def test_find_employee():
    fn = "emp1"
    ln = "empy"
    ad = "here"
    title = "yep"
    salary = 10
    obj = Employee(fn, ln, ad, title, salary)
    main_db.save_data(type(obj).__name__, obj.data_dict)
    assert main_db.find_employee(fn, ln, ad)[0]["first_name"] == fn


def test_get_accounts():
    accounts = []
    acc_num = 100
    accounts.append(Checking(10000, 500, acc_num))
    accounts.append(Savings(20000, acc_num))
    for a in accounts:
        main_db.save_data(type(a).__name__, a.data_dict)
    res = main_db.get_accounts(acc_num)
    assert len(res) == 2


def test_get_services():
    services = []
    acc_num = 1000
    services.append(Loan(50000, .01, acc_num))
    services.append(CreditCard(40000, .02, acc_num))
    for a in services:
        main_db.save_data(type(a).__name__, a.data_dict)
    res = main_db.get_services(acc_num)
    assert len(res) == 2


def test_delete_data():
    main_db.delete_data("Employee", 1)
    assert len(main_db.find_employee(id=1)) == 0
