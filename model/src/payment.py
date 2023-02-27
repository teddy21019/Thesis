from random import Random
from typing import TYPE_CHECKING, ParamSpec, Protocol, TypeVar
from enum import Enum, auto
from dataclasses import dataclass


class MOP_TYPE(Enum):
    H_CASH = 'H_Cash'
    F_CBDC = 'F_CBDC'
    DEPOSIT = 'Deposit'


class Trader(Protocol):
    
    @property
    def MOP(self) -> list[MOP_TYPE]:
        ...

    def set_seen(self, MOPS: set[MOP_TYPE])-> None:
        ... 
    
    def change_in_MOP(self, mop: MOP_TYPE, price: float | int) -> None:
        ...

    def change_in_goods(self, item , quantity: float | int) -> None:
        ...

class Payment:
    def __init__(self, seller: Trader, buyer: Trader, item = '_', random : Random | None = None) -> None:
        self.__seller = seller
        self.__buyer = buyer
        self.__item = item
        if random is None:
            self.__random = Random()
        else:
            self.__random = random


        self.seller_mops = set(seller.MOP)
        self.buyer_mops = set(buyer.MOP) 

        self.__means_of_payment = self.decide_means_of_payment()
    
    def decide_means_of_payment(self) -> MOP_TYPE | None:

        mop_in_common = list(self.seller_mops & self.buyer_mops)

        if len(mop_in_common) == 0:
            return None

        return self.__random.choice(mop_in_common)
    
    @property
    def means_of_payment(self) -> MOP_TYPE | None:
       return self.__means_of_payment 

    

    def set_seen_means_of_payment_to(self, list_of_traders: list[Trader]) -> None:
        for trader in list_of_traders:
            trader.set_seen(
                self.seller_mops | self.buyer_mops
            )

    
    def pay(self, p, q):
        if self.means_of_payment is None:
            raise InvalidTradingError("Trading fails but forced to trade")

        self.__seller.change_in_MOP(self.means_of_payment, p)
        self.__buyer.change_in_MOP(self.means_of_payment, -p)

        self.__seller.change_in_goods(self.__item, -q)
        self.__buyer.change_in_goods(self.__item, q)


class InvalidTradingError(ValueError):
    def __init__(self, message) -> None:
        super().__init__(message)