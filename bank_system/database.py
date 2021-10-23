from sqlalchemy import create_engine, Column, MetaData
from sqlalchemy import Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker


class BankDatabase:
    """Represents the database of the banking system. Handles reading
    and writing data in sqlite to a file in the local directory.

    Create new db with db name:
        new_db = BankDatabase("new_db")

    Attributes:
        No public attributes.
    """

    def __init__(self, dbname, mem_mode=False):
        # Table mapping
        self._table_name_account = "accounts"
        self._table_name_customer = "customers"
        self._table_name_employee = "employees"
        self._table_name_service = "services"

        # Start DB
        self._engine = create_engine(
            f"sqlite:///{dbname}.db")
        if mem_mode:
            self._engine = create_engine(
                f"sqlite:///:memory:")
        self._meta = MetaData(bind=self._engine)
        self._Base = declarative_base(metadata=self._meta)
        self._session = sessionmaker(self._engine)

        # Create tables if needed
        self._employee_class = self._create_tables_employee()
        self._account_class = self._create_tables_account()
        self._customer_class = self._create_tables_customer()
        self._service_class = self._create_tables_service()
        self._meta.create_all()

    def _get_table_class(self, class_name):
        obj_class = None
        if class_name == "Customer":
            obj_class = self._customer_class
        elif class_name == "Employee":
            obj_class = self._employee_class
        elif class_name == "Checking" or class_name == "Savings":
            obj_class = self._account_class
        elif class_name == "Loan" or class_name == "CreditCard":
            obj_class = self._service_class

        return obj_class

    def save_data(self, class_name, data_dict):
        """Save data to the database.

        Args:
            class_name: Requires the class name of the object.
            data_dict: Requires the data representation of the object.

        Returns:
            Tuple(id, created_at): Where id is the id primary key in the db.
        """
        obj_class = self._get_table_class(class_name)
        obj_data = obj_class(**data_dict)

        if data_dict["id"] is None:
            return self._add_data(obj_data)
        else:
            return self._update_data(obj_data, obj_class, data_dict)

    def find_employee(self, first_name, last_name, address):
        """Find employee in the database. Given the neccesary info as args.

        Args:
            first_name: Can be None.
            last_name: Can be None.
            address: Can be None.

        Returns:
            Array of the employees as dicts.
        """
        return self._find_person(
            self._employee_class, first_name, last_name, address)

    def find_customer(self, first_name, last_name, address):
        """Find customer in the database. Given the neccesary info as args.

        Args:
            first_name: Can be None.
            last_name: Can be None.
            address: Can be None.

        Returns:
            Array of the customer as dicts.
        """
        return self._find_person(
            self._customer_class, first_name, last_name, address)

    def _find_person(self, search_class, first_name, last_name, address):
        res = []
        with self._session() as ses:
            response = ses.query(search_class).filter_by(
                first_name=first_name)
            if last_name is not None:
                response.filter_by(last_name=last_name)
            if address is not None:
                response.filter_by(address=address)
            for r in response:
                if r is not None:
                    res.append(
                        {key: getattr(r, key)for key in
                         search_class.__table__.columns.keys()})
        return res

    def get_accounts(self, customer_id):
        return self._get_serv_acco(self._account_class, customer_id)

    def get_services(self, customer_id):
        return self._get_serv_acco(self._service_class, customer_id)

    def _get_serv_acco(self, search_class, customer_id):
        res = []
        with self._session() as ses:
            response = ses.query(search_class).filter_by(
                customer_id=customer_id)
            for r in response:
                if r is not None:
                    res.append(
                        {key: getattr(r, key)for key in
                         search_class.__table__.columns.keys()})
        return res

    def delete_data(self, class_name, id):
        with self._session() as ses:
            response = ses.query(
                self._get_table_class(class_name)).filter_by(
                id=id)
            if response is not None:
                response.delete()
            ses.commit()

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
