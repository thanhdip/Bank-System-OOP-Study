import logging


class Person:
    """Represents a person in the banking system.

    Attributes:
        first_name: String for person's first name as string.
        last_name: String for person's last name as string.
        address: String for address as string.
        full_name: First and last together as string.
        created_at: Time created at as datetime.datetime.
    """

    def __init__(self, first_name, last_name, address, created_at):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self._created_at = created_at
        logging.info("Person initializer...")
        logging.debug("Data: " + str(self.data_dict))

    def __str__(self):
        return f"""Name: {self.first_name} {self.last_name}
Address: {self.address}"""

    @property
    def full_name(self):
        """Full name of the person."""
        return f"{self.first_name} {self.last_name}"

    @property
    def data_dict(self):
        """Dictionary representation of the person for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "address": self.address,
                "created_at": self._created_at}


class Employee(Person):
    """Employee in the banking system.

    Attributes:
        first_name: String for person's first name as string.
        last_name: String for person's last name as string.
        address: String for address as string.
        full_name: String, first and last together as string.
        employee_id: Distinct id of employee as int.
        title: Employee's title as string.
        salary: Salary of employee as int.
        created_at: Time created at as datetime.datetime.
    """

    def __init__(
            self, first_name, last_name, address, title, salary,
            employee_id=None, created_at=None):
        self._employee_id = employee_id
        self.title = title
        self.salary = salary
        super().__init__(first_name, last_name, address, created_at)
        logging.info("Employee initializer...")
        logging.debug("Data: " + str(self.data_dict))

    def __str__(self):
        return f"--Employee--\n{self.title}\n{super().__str__()}"

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, id):
        "Cannot overwrite employee id if already set."
        if self._employee_id is None:
            self._employee_id = id

    @property
    def data_dict(self):
        """Dictionary representation of the Employee for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["id"] = self._employee_id
        data["title"] = self.title
        data["salary"] = self.salary
        return data


class Customer(Person):
    """Customer in the banking system.

    Attributes:
        first_name: String for person's first name as string.
        last_name: String for person's last name as string.
        address: String for address as string.
        full_name: First and last together as string.
        customer_id: Customer's distinct id as int.
        accounts: List of customer accounts as list(account).
        services: List of customer services as list(service).
        created_at: Time created at as datetime.datetime.
    """

    def __init__(self, first_name, last_name, address, created_at,
                 customer_id=None, accounts=[], services=[]) -> None:
        self._customer_id = customer_id
        self.accounts = accounts
        self.services = services
        super().__init__(first_name, last_name, address, created_at)
        logging.info("Customer initializer...")
        logging.debug("Data: " + str(self.data_dict))

    def __str__(self) -> str:
        return f"--Customer--\n{super().__str__()}"

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, id) -> None:
        "Cannot overwrite customer id if already set."
        if self._customer_id is None:
            self._customer_id = id

    @property
    def data_dict(self):
        """Dictionary representation of the Customer for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["id"] = self.customer_id
        data["accounts"] = self.accounts
        data["services"] = self.services
        return data
