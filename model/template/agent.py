from __future__ import annotations
from abc import ABC, abstractmethod


import mesa
from src.payment import MOP_TYPE, Payment
from typing import TYPE_CHECKING, Callable, Iterator, Self

if TYPE_CHECKING:
    Number = int | float



class TemplateAgent(mesa.Agent, ABC):

    """
        To match the `Trader` Protocol
    """
    @property
    @abstractmethod
    def MOP(self) -> list[MOP_TYPE]:
        ...
    @abstractmethod
    def set_seen(self, MOPS: set[MOP_TYPE])-> None:
        ... 
    
    @abstractmethod
    def change_in_MOP(self, mop: MOP_TYPE, price: Number) -> None:
        ...
    
    @abstractmethod
    def change_in_goods(self, item , quantity: Number) -> None:
        ...

    """
        To match the schedule
    """
    @abstractmethod
    def decide_consumption(self):
        ...

    @property
    @abstractmethod
    def seller_candidate(self) -> Iterator[Self]:
        ...
    
    @abstractmethod
    def shop(self, seller_candidate : Iterator[Self]):
        
        """
        For each seller in the list(generator)
        1. See if still affordable
        2. Check if still have inventory
        3. Decide means of payment to use 
        4. Announce the payment information 
        5. Finish the procedure

        The buyer stops when it has no more budget or it ran out of candidate
        that can have a successful trade with
        """
        for seller in seller_candidate:
            buyer = self        # for better readability
            
            if not seller.can_sell:
                continue
            
            payment = Payment(seller, buyer)
            payment.set_seen_means_of_payment_to([seller, buyer])
            
            if payment.means_of_payment is None:
                continue

            price : Number      = seller.offered_price
            quantity : Number   = seller.offered_quantity
            payment.pay(price, quantity)
            print(f"Buyer {self.unique_id} is trading with {seller.unique_id}")
    
    @property
    @abstractmethod
    def can_sell(self) -> bool:
        ...

    @property
    @abstractmethod
    def offered_price(self) -> Number:
        ...

    @property
    @abstractmethod
    def offered_quantity(self) -> Number:
        ...