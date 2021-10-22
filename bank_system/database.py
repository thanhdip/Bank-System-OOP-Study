from datetime import datetime
from sqlalchemy import create_engine, Table, Column, Integer
from sqlalchemy import String, MetaData, DateTime


class BankDatabase:
    def __init__(self, dbname) -> None:
        self._engine = create_engine(
            f"sqlite:///{dbname}.db")
        self._meta = MetaData()

    def save_data(self, table_name, data_dict) -> None:
        data_type_map = ((int, Integer), (str, String), (datetime, DateTime))
        tb = Table(table_name, self._meta,
                   Column()
                   )

    def create_table(self, table_name, data_dict) -> int:
        pass

    def create_account():
        pass

    def create_employee():
        pass

    def create_customer():
        pass

    def create_service():
        pass
