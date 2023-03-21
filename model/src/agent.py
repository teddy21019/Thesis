from __future__ import annotations
from functools import cached_property
from typing import TYPE_CHECKING, Iterator, Self
from enum import Enum, auto
from src.payment import Payment, MeansOfPaymentType as MOP_TYPE
from template.agent import TemplateAgent
import numpy as np
from scipy.special import softmax

import logging
logger = logging.getLogger('structure')

if TYPE_CHECKING:
    from src.model import TestModel, ThesisModel
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

class ThesisAgent(TemplateAgent):
    """
    Agent that has
    - Country
    - Action Type
    - Means of Payment
    """

    def __init__(self,
                 id:int,
                 model: ThesisModel,
                 type: AgentType,
                 country: str,
                 MOP: dict[ MOP_TYPE, float]):

        self.model: ThesisModel
        super().__init__(id, model)
        self.y = 4 # need change
        self._budget = 0
        self.type : AgentType = type
        self.country = country
        self._offered_price = 1
        self._acceptance_threshold = 0.2
        # holding of assets
        self._MOP : dict[MOP_TYPE, float] = MOP
        self._accepted_mop = MOP
        self._MOP_observe_memory = {mop:1.0 for mop in self._MOP}
        self.init_seller_candidate_list:list[int] = []

        self._money_memory = 1.0

    def decide_consumption(self, *args, **kargs) -> float:
        print(f"Deciding consumptions for buyer {self.unique_id}")
        self._budget += self.y * 0.5
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
        init_seller_candidate:list[int] = self.init_seller_candidate_list.copy()
        random_shuffler = self.model.random.shuffle

        random_shuffler(init_seller_candidate)

        for seller_id in init_seller_candidate:
            if self.__scheduler.seller_exists(seller_id):
                yield self.__scheduler.sellers[seller_id]

    @seller_candidate.setter
    def seller_candidate(self, seller_list: list[int]):
        self.init_seller_candidate_list = seller_list

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
            orig_observation = self._MOP_observe_memory[mop]
            self._MOP_observe_memory[mop] = orig_observation * self._money_memory + 1


    def see(self, mop: MOP_TYPE):
        """ Handles what an agent should do when saw a new means of payments"""
        self._MOP_observe_memory[mop] = 0

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
    def MOP_observe_freq(self):
        """ The relative frequency of each observed means of payment"""
        total_observe_count = sum(v for v in self._MOP_observe_memory.values())
        return {mop: v / total_observe_count
                for mop, v in self._MOP_observe_memory.items()}

    @property
    def accepted_mop(self):
        """A dictionary that returns the accepted means of payment, with frequency as its value"""
        self._accepted_mop = {mop:freq
                for mop,freq in self.MOP_observe_freq.items() if freq > self._acceptance_threshold}
        return self._accepted_mop

    @property
    def MOP_using_prob(self):
        """
        Returns the probability for each agents to use a certain type of means of payment.

        The probability is adjusted using softmax function
        """
        from params.mop_params import INTEREST_RATE_DISUTILITY

        i:dict = self.model.MOP_interest_rate
        accepted_mop_values = np.array(list(self._accepted_mop.values()))
        i_array = np.array([i[mop] for mop in self._accepted_mop])
        utility = accepted_mop_values * 1 + INTEREST_RATE_DISUTILITY * i_array

        probs = softmax(utility)

        return dict(
            zip(self._accepted_mop.keys(),probs)
        )

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
        return self.model.schedule
