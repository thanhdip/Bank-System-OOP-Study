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
