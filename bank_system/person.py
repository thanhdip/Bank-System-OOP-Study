class Person:
    """Represents a person in the banking system.

    Attributes:
        first_name: String for person's first name as string.
        last_name: String for person's last name as string.
        address: String for address as string.
        full_name: First and last together as string.
    """

    def __init__(self, first_name, last_name, address) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.address = address

    def __str__(self) -> str:
        return f"""Name: {self.first_name} {self.last_name}
        Address: {self.address}"""

    @property
    def full_name(self) -> str:
        """Full name of the person."""
        return f"{self.first_name} {self.last_name}"

    @property
    def data_dict(self) -> dict:
        """Dictionary representation of the person for data passing purposes.
        """
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "address": self.address}


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
    """

    def __init__(
            self, first_name, last_name,
            address, employee_id, title, salary) -> None:
        super().__init__(self, first_name, last_name, address)
        self.employee_id = employee_id
        self.title = title
        self.salary = salary

    def __str__(self) -> str:
        return f"--Employee--\n{self.title}\n{super().__str__()}"

    @property
    def data_dict(self) -> dict:
        data = super().data_dict
        data["employee_id"] = self.employee_id
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
    """

    def __init__(self, first_name, last_name, address, customer_id,
                 accounts=None, services=None) -> None:
        super().__init__(self, first_name, last_name, address)
        self.customer_id = customer_id
        self.accounts = accounts
        self.services = services

    def __str__(self) -> str:
        return f"--Customer--\n{super().__str__()}"

    @property
    def data_dict(self) -> dict:
        """Dictionary representation of the person for data passing purposes.
        """
        data = super().data_dict
        data["customer_id"] = self.customer_id
        data["accounts"] = self.accounts
        data["services"] = self.services
        return data
