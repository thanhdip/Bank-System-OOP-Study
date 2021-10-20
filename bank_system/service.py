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
        self._service_type = service_type
        self._service_id = service_id
        self._customer_id = customer_id
        self._created_at = created_at


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

    def __init__(
            self, service_type, service_id, customer_id=None,
            interest_rate=None, loan_amount=None, payed=None,
            term=None) -> None:
        super().__init__(service_type, service_id, customer_id=customer_id)
        self.interest_rate = interest_rate
        self.loan_amount = loan_amount
        self.term = term

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

    def __init__(self, service_type, service_id, customer_id=None,
                 interest_rate=None, max_limit=None, annual_fee=None) -> None:
        super().__init__(service_type, service_id, customer_id=customer_id)
        self.interest_rate = interest_rate
        self.max_limit = max_limit
        self.annual_fee = annual_fee
