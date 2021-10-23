import logging


class Service():
    """Represents services of the bank system.

    Attributes:
        borrowed_amount: Amount borrowed as float.
        interest_rate: Interest rate of money borrowed as float.
        service_type: Type of service as string.
        service_id: Distinct id of service as int.
        customer_id: Customer who has the service as int.
        created_at: Time service was created at datetime.date.
    """

    def __init__(self, borrowed_amount, interest_rate, service_type,
                 service_id, customer_id, created_at=None):
        """Service initialize Service.

        Args:
            loan_amount: Amount borrowed as float.
            interest_rate: Interest rate of money borrowed as float.
            service_type: Type of service.
            service_id: Distinct ID from the database.
            customer_id: Distinct ID of user.
        """
        self.service_type = service_type
        self.borrowed_amount = borrowed_amount
        self.interest_rate = interest_rate
        self._service_id = service_id
        self._customer_id = customer_id
        self._created_at = created_at
        logging.info("Service initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def customer_id(self):
        return self._customer_id

    @customer_id.setter
    def customer_id(self, id):
        "Cannot overwrite customer id if already set."
        if self._customer_id is None:
            self._customer_id = id

    @property
    def data_dict(self):
        """Dictionary representation of the service for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        return {
            "service_type": self.service_type,
            "id": self._service_id,
            "customer_id": self._customer_id,
            "created_at": self._created_at,
            "interest_rate": self.interest_rate,
            "borrowed_amount": self.borrowed_amount
        }


class Loan(Service):
    """Represents loan service of the bank system.

    Attributes:
        service_type: Type of service as string.
        service_id: Distinct id of service as int.
        customer_id: Customer who has the service as int.
        created_at: Time service was created at as datetime.date.
        interest_rate: Interest rate of loan as float.
        borrowed_amount: Amount loaned as float.
        payed: Amount already payed as float.
        term: Time of loan in years as float.

    Raises:
        OverpayedError when over paying on loan.
    """

    def __init__(
            self, borrowed_amount, interest_rate, customer_id, term=2, payed=0,
            service_id=None, created_at=None):
        self.term = term
        self.payed = payed
        super().__init__(
            borrowed_amount, interest_rate, self.__class__.__name__,
            service_id, customer_id, created_at)
        logging.info("Loan initializer...")
        logging.debug("Data: " + str(self.data_dict))

        @property
        def total_interest(self):
            return self.loan_amount * self.interest_rate

        @property
        def monthly_payment(self):
            return self.total_interest / (self.term * 12)

    @property
    def data_dict(self):
        """Dictionary representation of the Loan for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["term"] = self.term
        data["payed"] = self.payed
        return data

    @property
    def loan_left(self):
        return self.borrowed_amount + (
            self.borrowed_amount * self.interest_rate) - self.payed

    def pay(self, amount):
        """Pays off loan by an amount.

        Args:
            amount: amount to off loan by.

        Raises:
            OverpayedError when trying to overpay loan.
        """
        if self.loan_left - amount >= 0:
            self.payed += amount
        else:
            raise OverpayedError
        return self.loan_left


class CreditCard(Service):
    """Represents loan service of the bank system.

    Attributes:
        service_type: Type of service as string.
        service_id: Distinct id of service as int.
        customer_id: Customer who has the service as int.
        created_at: Time service was created at as datetime.date.
        interest_rate: Interest rate of loan as float.
        max_limit: Max borrowing limit as int.
        annual_fee: Annual fee if any as int.
    """

    def __init__(self, borrowed_amount, interest_rate, customer_id,
                 max_limit=4000, annual_fee=90, service_id=None,
                 created_at=None) -> None:
        self.max_limit = max_limit
        self.annual_fee = annual_fee
        super().__init__(
            borrowed_amount, interest_rate, self.__class__.__name__,
            service_id, customer_id, created_at)
        logging.info("Credit card initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self):
        """Dictionary representation of the Credit for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["max_limit"] = self.max_limit
        data["annual_fee"] = self.annual_fee
        return data

    @property
    def interest(self):
        "Amount of interest to be payed."
        return self.borrowed_amount * self.interest_rate

    def pay(self, amount):
        """Pay off credit card bill. Can go over to be used later.

        Args:
            amount: Amount to pay off.

        Returns:
            Amount borrowed.
        """
        self.borrowed_amount -= amount
        return self.borrowed_amount

    def borrow(self, amount):
        """Borrow from credit.

        Args:
            amount: Amount to pay off.

        Returns:
            Amount borrowed.
        """
        if self.borrowed_amount + amount > self.max_limit:
            raise CreditLimitError(self.max_limit)
        self.borrowed_amount += amount
        return self.borrowed_amount


class CreditLimitError(Exception):
    """Exception raised when trying to use over credit limit.

    Attributes:
        credit_limit: Max credit limit.
        message: Error msg.
    """

    def __init__(self, credit_limit,
                 message="Credit limit reached. Trying to go over: "):
        super().__init__(message + str(credit_limit))
        logging.error("Credit limit reached!")


class OverpayedError(Exception):
    """Exception raised when overpaying a loan.
    """

    def __init__(self):
        super().__init__("Overpaying loan!")
        logging.error("Loan overpyaing!")
