import logging


class Service():
    """Represents services of the bank system.

    Attributes:
        service_type: Type of service as string.
        service_id: Distinct id of service as int.
        customer_id: Customer who has the service as int.
        created_at: Time service was created at datetime.date.
    """

    def __init__(self, service_type, service_id, customer_id=None,
                 created_at=None) -> None:
        """Service initialize Service.

        Args:
            service_type: Type of service.
            service_id: Distinct ID from the database.
            customer_id: Distinct ID of user.
        """
        self._service_type = service_type
        self._service_id = service_id
        self._customer_id = customer_id
        self._created_at = created_at
        logging.info("Service initializer...")
        logging.debug("Data: " + str(self.data_dict))


class Loan(Service):
    """Represents loan service of the bank system.

    Attributes:
        service_type: Type of service as string.
        service_id: Distinct id of service as int.
        customer_id: Customer who has the service as int.
        created_at: Time service was created at as datetime.date.
        interest_rate: Interest rate of loan as float.
        loan_amount: Amount loaned as float.
        payed: Amount already payed as float.
        term: Time of loan in years as float.
    """

    def __init__(self, loan_amount=None, interest_rate=None, term=2,  payed=0,
                 service_id=None, customer_id=None,) -> None:
        super().__init__(self.__class__.__name__, service_id,
                         customer_id=customer_id)
        self.interest_rate = interest_rate
        self.loan_amount = loan_amount
        self.term = term
        self.payed = payed
        logging.info("Loan initializer...")
        logging.debug("Data: " + str(self.data_dict))

        @property
        def total_interest(self) -> int:
            return self.loan_amount * self.interest_rate

        @property
        def monthly_payment(self) -> int:
            return self.total_interest / (self.term * 12)


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

    def __init__(self, max_limit=None, interest_rate=None, annual_fee=90,
                 service_id=None, customer_id=None,
                 ) -> None:
        super().__init__(self.__class__.__name__, service_id,
                         customer_id=customer_id)
        self.interest_rate = interest_rate
        self.max_limit = max_limit
        self.annual_fee = annual_fee
        logging.info("Credit card initializer...")
        logging.debug("Data: " + str(self.data_dict))


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
