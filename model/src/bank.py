"""
Home commercial banks, and perhaps foreign commercial banks.

Banks listen to changes during the payment process, and alters their balance sheet.
"""

from abc import ABC, abstractmethod


class Bank(ABC):

    @abstractmethod
    def bank_handle_payment_callback_fn(self, data):
        ...

class TestBank(Bank):

    def bank_handle_payment_callback_fn(self, data):
        print(
            f'\t Agent {data["sender"]} pays agent {data["receiver"]} ${data["amount"]} in the bank'
        )


class ThesisBank(Bank):
    def __init__(self, name: str):
        self.name = name
        self.liability :dict[int, float]= {}
        self.assets = 0
        self._reserve_rate: float = 0.4
        self._leverage = 1
    @property
    def reserve_rate(self):
        return self._reserve_rate

    @reserve_rate.setter
    def reserve_rate(self, value:float):
        if value > 1 or value < 0 :
            raise ValueError("Reserve rate limited within [0,1]")
        self._reserve_rate = value

    def add_account(self, user_id: int, deposit_value:float)->None:
        """Initialize user with its deposit values"""
        self.assets += deposit_value
        self.liability[user_id] = deposit_value

    def change_deposit(self, user_id:int, amount:float):
        self.liability[user_id] += amount

    def bank_handle_payment_callback_fn(self, data):
        sender_id   :int   = data["sender"]
        receiver_id :int   = data["receiver"]
        amount :float = data["amount"]

        self.change_deposit(sender_id, -amount)
        self.change_deposit(receiver_id, amount)


    @property
    def leverage(self):
        return self.assets / sum(self.liability.values())