import logging


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
        """Initialize account

        Args:
            account_type: Type of account as string.
            balance: Amount of money in account as float.
            account_id: Distinct ID from DB as int.
            created_at: Timestamp of when item was added
            to DB as datetime.date.
        """
        self.account_type = account_type
        self.account_id = account_id
        self.customer_id = customer_id
        self.balance = balance
        self.created_at = created_at
        logging.info("Account initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self) -> dict:
        """Dictionary representation of the Account for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        return {"account_type": self.account_type,
                "account_id": self.account_id,
                "customer_id": self.customer_id,
                "balance": self.balance}

    def withdraw(self, amount) -> float:
        """Withdraw amount from account.

        Returns:
            Balance of the account after withdrawal as float.

        Raises:
            OverdraftError when withdrawing over balance.
        """
        if(amount <= self.balance):
            self.balance -= amount
        else:
            raise OverdraftError
        return self.balance

    def deposit(self, amount) -> int:
        """Deposit amount to account.

        Returns:
            Balance of the account after deposit as float.
        """
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

    def __init__(self, balance, savings_rate=.01, account_id=None,
                 customer_id=None, created_at=None) -> None:
        super().__init__(
            self.__class__.__name__, balance, account_id=account_id,
            customer_id=customer_id, created_at=created_at)
        self.saving_rate = savings_rate
        logging.info("Savings initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self) -> dict:
        """Dictionary representation of the Savings account
        for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["savings_rate"] = self.saving_rate
        return data


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
        logging.info("Checking initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self) -> dict:
        """Dictionary representation of the Checking account for data passing
        purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["min_balance"] = self.min_balance
        return data


class OverdraftError(Exception):
    """Exception raised when balance of an account goes past 0.

    Attributes:
        message: Error msg.
    """

    def __init__(self,  message="Trying to withdraw over balance."):
        super().__init__(message)
        logging.error("Overdraft!")
