from sqlalchemy import create_engine


class BankDatabase:
    def __init__(self, dbname) -> None:
        self._engine = create_engine(
            f"sqlite:///{dbname}.db")

    def save_data(self, data_dict) -> None:

        pass
