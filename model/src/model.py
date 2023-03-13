from __future__ import annotations
from random import Random
from itertools import count
import mesa
import mesa.time
import networkx as nx
from src.agent import TestAgent, AgentType
from src.schedule import TestScheduler
from src.payment import MeansOfPaymentType
from src.broadcast import subscribe
from src.bank import TestBank

import logging
logger = logging.getLogger('structure')

from typing import (
    TYPE_CHECKING,
    Type
    )

if TYPE_CHECKING:
    SchedulerConstructor =  Type[TestScheduler]
    from template import TemplateAgent

class TestModel(mesa.Model):
    def __init__(self,
                N                       : int,
                scheduler_constructor   : SchedulerConstructor,
            ):
        self.random: Random
        super().__init__()
        self.scheduler              = scheduler_constructor(self)
        self.agent_constructor = TestAgent
        self.unique_id_generator    = count()
        self._bank = TestBank()

        self.init_mop = MeansOfPaymentType('H_CBDC')

        self._create_agents()
        self._register_listeners()


    def _create_agents(self):
        print("Creating agents")
        self._init_buyers()
        self._init_sellers()

    def _init_buyers(self):
        for i in range(2):
            new_agent = self._init_agent(AgentType.BUYER, {self.init_mop: 10})
            self.scheduler.add(
                new_agent,
            )

    def _init_sellers(self):
        for i in range(2):
            new_agent = self._init_agent(AgentType.SELLER, {self.init_mop: 10})
            self.scheduler.add(
                new_agent,
            )

    def _init_agent(self,
                    type: AgentType,
                    mop_holding:dict[MeansOfPaymentType, float]
                    ):
        agent = self.agent_constructor(
            id = next(self.unique_id_generator),
            model = self,
            type = type,
            MOP = mop_holding
        )
        return agent

    def _register_listeners(self):
        subscribe(self.init_mop, self._bank.bank_handle_payment_callback_fn)

    def MOP_to_real_value(self, mop:MeansOfPaymentType, value:float):
        return value * mop.exchange_rate_to_real

    def step(self):
        self.scheduler.step()


class ThesisModel(TestModel):
    """ Main model for thesis"""
    def __init__(self,
                N                       : int,
                scheduler_constructor   : SchedulerConstructor,
                cross_border_payment_network: nx.Graph
            ):
        self.random: Random
        super(mesa.Model, self).__init__()
        self.scheduler              = scheduler_constructor(self)
        self.agent_constructor = TestAgent
        self._trading_network = cross_border_payment_network
        self._bank = TestBank()
        self._create_agents()
        self._register_listeners()


    def _create_agents(self):
        """
        Create agents from network.

        ## Agents
        - Initialize agents for both combinations of buyer/seller and country1/country2
        - All information should be encapsulated in the graph it self

        ## Networks
        - After the initialization of all agents
        - Start with buyers, add an array of sellers into the 'buyer contact'
        - When buyers add seller, sellers also add buyer (currently don't
        consider directional graph)
        """
        all_agents = self._trading_network.nodes(data=True)
        self._init_buyers(buyer_dict = {
            node_id:data for node_id, data in all_agents if data['bipartite'] == 'buyer'
            })

        self._init_sellers(seller_dict = {
            node_id:data for node_id, data in all_agents if data['bipartite'] == 'seller'
        })

        self._connect_trading_network_edges()

    def _init_buyers(self, buyer_dict: dict[int, dict]):
        
        for b_id, d_data in buyer_dict.items():
            country :str = d_data['country']
            init_mop = get_init_mop_from_country(country)
            new_agent = self.agent_constructor(
                id          = b_id,
                model       = self,
                type        = AgentType.BUYER,
                MOP         = init_mop
            )

            self.scheduler.add(
                new_agent,
            )

    def _init_sellers(self, seller_dict: dict[int, dict]):
        
        for s_id, d_data in seller_dict.items():
            country :str = d_data['country']
            init_mop = get_init_mop_from_country(country)
            new_agent = self.agent_constructor(
                id          = s_id,
                model       = self,
                type        = AgentType.SELLER,
                MOP         = init_mop
            )

            self.scheduler.add(
                new_agent,
            )
    def _init_sellers(self, seller_dict):
        for i in range(2):
            new_agent = self._init_agent(AgentType.SELLER, {MOP_TYPE.H_CASH:10})
            self.scheduler.add(
                new_agent,
            )

    def _init_agent(self,
                    id: int,
                    country: str,
                    type: AgentType,
                    mop_holding:dict[MOP_TYPE, float]
                    ):
        agent = self.agent_constructor(
            id = id,
            country = country,
            model = self,
            type = type,
            MOP = mop_holding
        )
        return agent


    def _register_listeners(self):
        subscribe(MOP_TYPE.H_CASH.value, self._bank.bank_handle_payment_callback_fn)

    def MOP_to_real_value(self, mop:MOP_TYPE, value:float):
        return value

    def step(self):
        self.scheduler.step()