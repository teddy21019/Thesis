from __future__ import annotations
from random import Random
from mesa.time import BaseScheduler
from typing import TYPE_CHECKING, Callable, Iterator

from numpy import add

from src.agent import AgentType

from template.agent import TemplateAgent
from template.schedule import TemplateScheduler

import logging

logger = logging.getLogger('structure')

if TYPE_CHECKING:
    from src.agent import TestAgent, AgentType
    from src.model import TestModel

class TestScheduler(TemplateScheduler):
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

    def __init__(self, model: TestModel) -> None:
        super().__init__(model)
        self._sellers: dict[int, TestAgent] = dict()
        self._buyers: dict[int, TestAgent] = dict()

    def add(self, agent:TestAgent):
        atype = agent.type
        if atype == AgentType.BUYER:
            self._add_buyer(agent)
            return
        if atype == AgentType.SELLER:
            self._add_seller(agent)
            return

        raise AgentTypeException(atype, f"No such type as {atype} exist")


    def step(self) -> None:
       super().step()

    def _add_buyer(self, agent: TestAgent) -> None :
        agent_id = agent.unique_id
        if agent_id in self._buyers:
            raise RepeatAgentError(id = agent_id)
        self._buyers[agent_id] = agent


    def _add_seller(self, agent: TestAgent) -> None:
        agent_id = agent.unique_id
        if agent_id in self._sellers:
            raise RepeatAgentError(id = agent_id)
        self._sellers[agent_id] = agent

    @property
    def sellers(self):
        return self._sellers

    @property
    def buyers(self):
        return self._buyers

    def seller_exists(self, seller:TestAgent | int ):
        from src.agent import TestAgent

        if isinstance(seller, TestAgent):
            return seller.unique_id in self._sellers
        elif isinstance(seller, int):
            return seller in self._sellers
        raise ValueError("Agent type error!")

    def buyer_exists(self, buyer:TestAgent | int ):
        if isinstance(buyer, TestAgent):
            return buyer.unique_id in self._buyers
        elif isinstance(buyer, int):
            return buyer in self._buyers
        raise ValueError("Agent type error!")



    def _consumption_decision_step(self) -> None:
        logger.debug("Consumption decision step")
        super()._consumption_decision_step()


    def _consumption_bundling_step(self) -> None:
        logger.debug("Consumption bundling step")
        super()._consumption_bundling_step()

    def _seller_summarize_step(self) -> None:
        logger.debug("Seller summarization step")
        super()._seller_summarize_step()

    def _seller_buyer_toggle_step(self) -> None:
        logger.debug("Seller buyer toggle step")
        super()._seller_buyer_toggle_step()


    def _buyer_activation_order(self) -> Iterator[TestAgent]:
        random_generator: Random = self.model.random #type: ignore
        agent_buyer_keys = list( self._buyers.keys() )
        random_generator.shuffle(agent_buyer_keys)

        for key in agent_buyer_keys:
            if key in self._buyers:
                yield self._buyers[key]

    def _seller_activation_order(self) -> Iterator[TestAgent]:
        random_generator: Random = self.model.random #type: ignore
        agent_seller_keys = list( self._sellers.keys() )
        random_generator.shuffle(agent_seller_keys)

        for key in agent_seller_keys:
            if key in self._sellers:
                yield self._sellers[key]


class AgentTypeException(Exception):
    def __init__(self,type,message):
        super().__init__(message)

class RepeatAgentError(Exception):
    def __init__(self, id):
        super().__init__(f"Agent id {id} is already registered")