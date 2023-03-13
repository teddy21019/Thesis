from __future__ import annotations
from typing import TYPE_CHECKING, Iterator, Self
from enum import Enum, auto
from src.payment import Payment, MeansOfPaymentType as MOP_TYPE
from template.agent import TemplateAgent

import logging
logger = logging.getLogger('structure')

if TYPE_CHECKING:
    from src.model import TestModel
    Number = int | float

class AgentType(Enum):
    BUYER = auto()
    SELLER = auto()




class TestAgent(TemplateAgent):

    def __init__(self, id:int, model: TestModel, type: AgentType, MOP: None | dict[ MOP_TYPE, float]):
        self.model: TestModel
        super().__init__(id, model)
        self.y = 10 # need change
        self._budget = 0
        self.type : AgentType = type
        self._offered_price = 1
        # holding of assets
        if MOP is None:
            self._MOP : dict[MOP_TYPE, float] = {model.init_mop: 10}
        else:
            self._MOP : dict[MOP_TYPE, float] = MOP

    def decide_consumption(self, *args, **kargs) -> float:
        print(f"Deciding consumptions for buyer {self.unique_id}")
        self._budget = self.y * 0.5
        return self._budget

    @property
    def seller_candidate(self) -> Iterator[Self]:
        """
        Decides the candidate this buyer will want to buy from.

        Return
        ====
        Iterator with type `CAgent`. Cannot be a list since I do not exclude the
        possibility of sellers exiting the economy, and making it a list might
        cause the agent to not be found
        """

        all_sellers : dict[int, Self] = self.__scheduler.sellers
        all_seller_ids = list(
                all_sellers.keys()
        )

        random_shuffler = self.model.random.shuffle

        random_shuffler(all_seller_ids)

        print(f"Buyer {self.unique_id} shopping candidate set")

        for seller_id in all_seller_ids:
            if self.__scheduler.seller_exists(seller_id):
                yield all_sellers[seller_id]

    def shop(self, seller_candidate : Iterator[Self]):
        print(f"Buyer {self.unique_id} is shopping")
        super().shop(seller_candidate)

    @property
    def can_buy(self) -> bool:
        return self._budget > 0
    @property
    def can_sell(self):
        return True


    def set_seen(self, MOPS: set[MOP_TYPE])-> None:
        """
        Called by payment system/ network system. Protocol for other classes
        to inform this agent of an unseen means of payment
        """
        for mop in MOPS:
            if mop not in self._MOP:
                self.see(mop)

    def see(self, mop: MOP_TYPE):
        """ Handles what an agent should do when saw a new means of payments"""
        print(f"Agent {self.unique_id} now saw {mop}")

    def change_in_MOP(self, mop: MOP_TYPE, price: float | int) -> None:
        self._MOP[mop]  = self._MOP[mop] + price
        self._budget += self.model.MOP_to_real_value(mop, price)
        print(f"\t Agent {self.unique_id} still can spend {self._budget}")

    def change_in_goods(self, item , quantity: float | int) -> None:
        pass

    def adjust_receive_MOP_as_seller(self):
        print(f"Agent {self.unique_id} adjusting means of payment accepted")

    def adjust_offered_price(self):
        print(f"Agent {self.unique_id} adjusting offered price")


    def adjust_production(self):
        print(f"Agent {self.unique_id} adjusting production")

    @property
    def MOP(self) :
        return list(self._MOP.keys())

    @MOP.setter
    def MOP(self, value):
        self._MOP = value


    @property
    def offered_price(self) :
        return self._offered_price

    @offered_price.setter
    def offered_price(self, value):
        self._offered_price = value

    @property
    def offered_quantity(self):
        return 1

    @property
    def __scheduler(self):
        return self.model.scheduler