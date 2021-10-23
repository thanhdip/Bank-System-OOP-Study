from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, Float, String, DateTime
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker


class BankDatabase:
    def __init__(self, dbname):
        self._table_name_account = "accounts"
        self._table_name_customer = "customers"
        self._table_name_employee = "employees"
        self._table_name_service = "services"
        self._engine = create_engine(
            f"sqlite:///{dbname}.db")
        self._meta = MetaData(bind=self._engine)
        self._Base = declarative_base(metadata=self._meta)
        self._session = sessionmaker(self._engine)

        # Create tables if needed
        self._employee_class = self._create_tables_employee()
        self._account_class = self._create_tables_account()
        self._customer_class = self._create_tables_customer()
        self._service_class = self._create_tables_service()
        self._meta.create_all()

    def save_data(self, class_name, data_dict):
        obj_data = None
        obj_class = None
        if class_name == "Customer":
            obj_data = self._customer_class(**data_dict)
            obj_class = self._customer_class
        elif class_name == "Employee":
            obj_data = self._employee_class(**data_dict)
            obj_class = self._employee_class
        elif class_name == "Checking" or class_name == "Savings":
            obj_data = self._account_class(**data_dict)
            obj_class = self._account_class
        elif class_name == "Loan" or class_name == "CreditCard":
            obj_data = self._service_class(**data_dict)
            obj_class = self._account_class

        if data_dict["id"] is None:
            return self._add_data(obj_data)
        else:
            return self._update_data(obj_data, obj_class, data_dict)

    def _add_data(self, obj_data):
        with self._session() as ses:
            ses.add(obj_data)
            ses.commit()
            res = (obj_data.id, obj_data.created_at)
        return res

    def _update_data(self, obj_data, obj_class, data_dict):
        with self._session() as ses:
            response = ses.query(obj_class).filter_by(id=obj_data.id)
            response.update(data_dict)
            ses.commit()
            res = (obj_data.id, obj_data.created_at)
        return res

    def _create_tables_account(self):
        accounts = {
            '__tablename__': self._table_name_account,
            "id":            Column(Integer, primary_key=True, nullable=False),
            "account_type":  Column(String),
            "balance":       Column(Float),
            "customer_id":   Column(Integer),
            "created_at":    Column(DateTime(timezone=True),
                                    server_default=func.now()),
            "savings_rate":  Column(Float),
            "min_balance":   Column(Integer)}
        return type(self._table_name_account, (self._Base,), accounts)

    def _create_tables_customer(self):
        customers = {
            '__tablename__': self._table_name_customer,
            "id":            Column(Integer, primary_key=True, nullable=False),
            "first_name":    Column(String),
            "last_name":     Column(String),
            "address":       Column(String),
            "created_at":    Column(DateTime(timezone=True),
                                    server_default=func.now())}
        return type(self._table_name_customer, (self._Base,), customers)

    def _create_tables_employee(self):
        employees = {
            '__tablename__': self._table_name_employee,
            "id":            Column(Integer, primary_key=True, nullable=False),
            "first_name":    Column(String),
            "last_name":     Column(String),
            "address":       Column(String),
            "title":         Column(String),
            "salary":        Column(Integer),
            "created_at":    Column(DateTime(timezone=True),
                                    server_default=func.now())}

        return type(self._table_name_employee, (self._Base,), employees)

    def _create_tables_service(self):
        services = {
            '__tablename__': self._table_name_service,
            "id":            Column(Integer, primary_key=True, nullable=False),
            "service_type":  Column(String),
            "customer_id":   Column(Integer),
            "created_at":    Column(DateTime(timezone=True),
                                    server_default=func.now()),
            "borrowed_amount": Column(Float),
            "interest_rate":  Column(Float),
            "term":           Column(Float),
            "payed":          Column(Float),
            "max_limit":      Column(Integer),
            "annual_fee":     Column(Integer), }

        return type(self._table_name_service, (self._Base,), services)
