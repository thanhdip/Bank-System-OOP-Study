from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer, Float
from sqlalchemy import String, MetaData, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.schema import ForeignKey


class BankDatabase:
    def __init__(self, dbname) -> None:
        self._engine = create_engine(
            f"sqlite:///{dbname}.db")
        self._meta = MetaData()

    def save_data(self, table_name, data_dict) -> None:
        pass

    def _create_tables(self) -> None:
        data_type_map = ((int, Integer), (str, String), (datetime, DateTime))
        accounts = Table('accounts', self._meta, Column(
            "account_id", Integer, primary_key=True, nullable=False),
            Column("account_type", String),
            Column("balance", Float),
            Column("customer_id", Integer),
            Column("created_at", DateTime(timezone=True), default=func.now()),
            Column("savings_rate", Float),
            Column("min_balance", Integer),
        )

        customers = Table('customers', self._meta, Column(
            "customer_id", Integer, primary_key=True, nullable=False),
            Column("first_name", String),
            Column("last_name", String),
            Column("address", String),
            Column("created_at", DateTime(timezone=True), default=func.now()),
        )

        employees = Table('employees', self._meta, Column(
            "employee_id", Integer, primary_key=True, nullable=False),
            Column("first_name", String),
            Column("last_name", String),
            Column("address", String),
            Column("title", String),
            Column("salary", Integer),
            Column("created_at", DateTime(timezone=True), default=func.now()),
        )

        services = Table("services", self._meta, Column(
            "service_id", Integer, primary_key=True, nullable=False),
            Column("service_type", String),
            Column("customer_id", Integer),
            Column("created_at", DateTime(timezone=True), default=func.now()),
            Column("borrowed_amount", Float),
            Column("interest_rate", Float),
            Column("term", Float),
            Column("payed", Float),
            Column("max_limit", Integer),
            Column("annual_fee", Integer),
        )
