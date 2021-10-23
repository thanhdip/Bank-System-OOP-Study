from sqlalchemy import create_engine, Table, Column, MetaData
from sqlalchemy import Integer, Float, String, DateTime
from sqlalchemy import insert, update, delete
from sqlalchemy import engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.engine import ResultProxy
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
        if class_name == "Customer":
            return self._save_data(data_dict, self._table_name_customer)
        elif class_name == "Employee":
            new_row_vals = self._employee_class(**data_dict)
            with self._session() as ses:
                ses.add(new_row_vals)
                ses.commit()
                print(repr(new_row_vals))
                res = new_row_vals.id
            return res

    def _save_data(self, data_dict, table_name):
        table = self._meta.tables[table_name]
        stmt = (insert(table).values(data_dict).return_defaults())
        res = self._engine.connect().execute(stmt)
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
