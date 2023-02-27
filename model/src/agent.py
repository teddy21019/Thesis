from __future__ import annotations
import mesa
from typing import TYPE_CHECKING, Iterator
from enum import Enum, auto


import logging
logger = logging.getLogger('structure')

if TYPE_CHECKING:
    from src.model import CModel

class AgentType(Enum):
    BUYER = auto()
    SELLER = auto()

class CAgent(mesa.Agent):

    def __init__(self, id:int, model: CModel, type: AgentType):
        self.model: CModel
        super().__init__(id, model)
        self.y = 10 # need change
        self.type : AgentType = type
        
    def decide_consumption(self, *args, **kargs) -> float:
        logger.debug(f"Deciding consumptions for buyer {self.unique_id}")
        budget = self.y * 0.5
        return budget 

    @property
    def seller_candidate(self) -> Iterator[CAgent]:
        """
        Decides the candidate this buyer will want to buy from. 

        Return
        ====
        Iterator with type `CAgent`. Cannot be a list since I do not exclude the
        possibility of sellers exiting the economy, and making it a list might
        cause the agent to not be found
        """

        all_sellers : dict[int, CAgent] = self.__scheduler.sellers
        all_seller_ids = list(
                all_sellers.keys()
        )
        
        random_shuffler = self.model.random.shuffle

        random_shuffler(all_seller_ids)

        print(f"Buyer {self.unique_id} shopping candidate set")

        for seller_id in all_seller_ids:
            if self.__scheduler.seller_exists(seller_id):
                yield all_sellers[seller_id]
    
    def shop(self, seller_candidate : Iterator[CAgent]):
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
        print(f"Buyer {self.unique_id} is shopping") 

        for seller in seller_candidate:
            buyer = self        # for better readability
            
            if seller.can_sell: 
                payment = Payment(seller.MOP, buyer.MOP)
                if payment.means_of_payment is None:
                    payment.set_seen_means_of_payment_to([seller, buyer])
                    continue
                price = seller.offered_price
                payment.pay(buyer, seller, price)
                print(f"Buyer {self.unique_id} is trading with {seller.unique_id}")

    @property
    def can_sell(self):
        return True

    @property
    def MOP(self) :
        return self._MOP

    @MOP.setter
    def MOP(self, value):
        self._MOP = value

    
    @property
    def offered_price(self):
        return self._offered_price 
    
    @offered_price.setter
    def offered_price(self, value):
        self._offered_price = value    

    
    @property
    def __scheduler(self): 
        return self.model.scheduler