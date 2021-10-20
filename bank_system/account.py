class Account:
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.date.
    """

    def __init__(self, account_type, balance, account_id=None,
                 customer_id=None, created_at=None) -> None:
        self.account_type = account_type
        self.account_id = account_id
        self.customer_id = customer_id
        self.balance = balance
        self.created_at = created_at

    @property
    def account_type(self) -> str:
        return self._acount_type

    @property
    def balance(self) -> str:
        return self.balance

    @property
    def data_dict(self) -> dict:
        return {"account_type": self.account_type,
                "account_id": self.account_id,
                "customer_id": self.customer_id,
                "balance": self.balance}

    def withdraw(self, amount) -> int:
        self.balance -= amount
        return self.balance

    def deposit(self, amount) -> int:
        self.balance += amount
        return self.balance


class Savings(Account):
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.date.
        savings_rate: Rate savings increase as float.
    """

    def __init__(self, account_type, balance, account_id=None,
                 customer_id=None, created_at=None, savings_rate=None) -> None:
        super().__init__(account_type, balance, account_id=account_id,
                         customer_id=customer_id, created_at=created_at)
        self.saving_rate = savings_rate


class Checking(Account):
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.date.
        min_balance: Minimum allowed balance as int.
    """

    def __init__(self, account_type, balance, account_id=None,
                 customer_id=None, created_at=None, min_balance=None) -> None:
        super().__init__(account_type, balance, account_id=account_id,
                         customer_id=customer_id, created_at=created_at)
        self.min_balance = min_balance
