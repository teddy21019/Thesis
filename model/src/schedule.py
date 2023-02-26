from __future__ import annotations
from random import Random
from mesa.time import BaseScheduler
from typing import TYPE_CHECKING, Iterator
from src.agent import AgentType

import logging

logger = logging.getLogger('structure')

if TYPE_CHECKING:
    from mesa import Model, Agent
    from src.agent import CAgent, AgentType
    from src.model import CModel
    from src.schedule import CScheduler
class CScheduler(BaseScheduler):
    """
    The baseline scheduler that defines the basic structure of the model. 


    A scheduler consists of 
    - the tick, or the time index of the model
    - the template for the agent activation 
    
    Extension
    =====
    This class is meant to be extended, but I am not designing this as an
    abstract class, for the sake of demonstration purposes. 
    """

    def __init__(self, model: CModel) -> None:
        super().__init__(model)
        self._sellers: dict[int, CAgent] = dict()
        self._buyers: dict[int, CAgent] = dict()

    def add(self, agent:CAgent, type: AgentType):
        if type == AgentType.BUYER:
            self._add_buyer(agent)
            return 
        if type == AgentType.SELLER:
            self._add_seller(agent)
            return
        
        raise AgentTypeException(type, f"No such type as {type} exist") 
    
    def _add_buyer(self, agent: CAgent) -> None :
        agent_id = agent.unique_id
        if agent_id in self._buyers:
            raise RepeatAgentError(id = agent_id)
        self._buyers[agent_id] = agent


    def _add_seller(self, agent: CAgent) -> None:
        agent_id = agent.unique_id
        if agent_id in self._sellers:
            raise RepeatAgentError(id = agent_id)
        self._sellers[agent_id] = agent



    
    def step(self) -> None:
        """
        The standard step for the model. 

        - Consumption Decision Step : Each buyer decides how much to buy, save,
        given the environment value and recent state variables such as
        endowment/ production
        - Consumption Bundling Step : Each buyer decides an array of consumption
        bundles, and consume until its budget is reached
        - Seller Summarize Step : After all the trading is conducted, the seller
        summarizes their inventory and price, and adjusts their behavior
        accordingly. Means of payment decision is also performed in this step
        - Seller-Buyer Toggle Step : The seller becomes a buyer according to
        some criteria.
        """
        self._consumption_decision_step()
        self._consumption_bundling_step()
        self._seller_summarize_step()
        self._seller_buyer_toggle_step()
        
    def _consumption_decision_step(self) -> None:
        logger.debug("Consumption decision step")
        
        buyer_consumption_decision_order : Iterator[CAgent] = self._buyer_activation_order()
        
        for buyer in buyer_consumption_decision_order:
            buyer.decide_consumption()
        return

    def _consumption_bundling_step(self) -> None:
        logger.debug("Consumption bundling step")
        return

    def _seller_summarize_step(self) -> None:
        logger.debug("Seller summarization step")
        return

    def _seller_buyer_toggle_step(self) -> None:
        logger.debug("Seller buyer toggle step")
        return


    def _buyer_activation_order(self) -> Iterator[CAgent]:
        random_generator: Random = self.model.random #type: ignore
        agent_buyer_keys = list( self._buyers.keys() )
        random_generator.shuffle(agent_buyer_keys)

        for key in agent_buyer_keys:
            if key in self._buyers:
                yield self._buyers[key] 


class AgentTypeException(Exception):
    def __init__(self,type,message):
        super().__init__(message)

class RepeatAgentError(Exception):
    def __init__(self, id):
        super().__init__(f"Agent id {id} is already registered")