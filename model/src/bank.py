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
            f'\t Agent {data["sender"]} pays agent {data["receiver"]} some money in the bank'
        )