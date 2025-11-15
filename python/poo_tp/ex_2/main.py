import datetime

class Account:
    def __init__(self, amount: float, created_datetime=None):
        if created_datetime is None:
            created_datetime = datetime.datetime.now()
        self.datetime = created_datetime
        if amount < 0:
            raise ValueError("NegativeAmountError")
        self.amount = amount
    
    def deposit(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("NegativeAmountError")
        self.amount += amount
    
    def withdraw(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("NegativeAmountError")
        if self.amount - amount < 0:
            raise ValueError("InsufficientFundsError")
        self.amount -= amount
    
    def transfer(self, other_account: 'Account', amount: float) -> None:
        self.withdraw(amount)
        other_account.deposit(amount)

    def created_at(self):
        return self.datetime


class CheckingAccount(Account):
    def __init__(self, amount, created_datetime=None):
        super().__init__(amount, created_datetime)


class SavingsAccount(Account):
    def __init__(self, amount, created_datetime=None):
        super().__init__(amount, created_datetime)
    
    # We suppose that it has an annual rate of 6%
    def interest_calculation(self):
        days_elapsed = (datetime.datetime.now() - self.datetime).days
        return self.amount * days_elapsed * 0.06 / 365