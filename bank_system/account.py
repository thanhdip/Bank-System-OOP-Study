import datetime
import logging


class Account:
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.datetime.
    """

    def __init__(self, account_type, balance, customer_id, account_id=None,
                 created_at=None):
        """Initialize account

        Args:
            account_type: Type of account as string.
            balance: Amount of money in account as float.
            account_id: Distinct ID from DB as int.
            created_at: Timestamp of when item was added
            to DB as datetime.datetime.
        """
        self._account_type = account_type
        self._account_id = account_id
        self._customer_id = customer_id
        self._balance = balance
        self._created_at = created_at
        logging.info("Account initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def created_at(self):
        return self._created_at

    @property
    def balance(self):
        return self._balance

    @property
    def account_type(self):
        return self._account_type

    @property
    def account_id(self):
        return self._account_id

    @account_id.setter
    def account_id(self, id):
        "Cannot overwrite account id if already set."
        if self._account_id is None:
            self._account_id = id

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
        """Dictionary representation of the Account for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        return {"account_type": self.account_type,
                "id": self.account_id,
                "customer_id": self.customer_id,
                "balance": self.balance,
                "created_at": self.created_at}

    def withdraw(self, amount):
        """Withdraw amount from account.

        Returns:
            Balance of the account after withdrawal as float.

        Raises:
            OverdraftError when withdrawing over balance.
        """
        if(amount <= self.balance):
            self._balance -= amount
        else:
            raise OverdraftError
        return self._balance

    def deposit(self, amount):
        """Deposit amount to account.

        Returns:
            Balance of the account after deposit as float.
        """
        self._balance += amount
        return self._balance


class Savings(Account):
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.datetime.
        savings_rate: Rate savings increase as float.
    """

    def __init__(
            self, balance, customer_id, savings_rate=.01, account_id=None,
            created_at=None):
        self.savings_rate = savings_rate
        super().__init__(
            self.__class__.__name__, balance, account_id=account_id,
            customer_id=customer_id, created_at=created_at)
        logging.info("Savings initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self):
        """Dictionary representation of the Savings account
        for data passing purposes.

        Returns:
            Dict of variable names and data.
        """
        data = super().data_dict
        data["savings_rate"] = self.savings_rate
        return data


class Checking(Account):
    """Customer accounts in the bank system.

    Attributes:
        account_type: Type of account as string.
        balance: Amount of money in the account as float.
        account_id: Distinct account id as int.
        customer_id: ID of owner of the account as int.
        created_at: Time created at as datetime.datetime.
        min_balance: Minimum allowed balance as int.
    """

    def __init__(self,  balance,  min_balance, customer_id, account_id=None,
                 created_at=None):
        self.min_balance = min_balance
        super().__init__(
            self.__class__.__name__, balance, account_id=account_id,
            customer_id=customer_id, created_at=created_at)
        logging.info("Checking initializer...")
        logging.debug("Data: " + str(self.data_dict))

    @property
    def data_dict(self):
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
