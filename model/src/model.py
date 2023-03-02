from __future__ import annotations
from random import Random
from itertools import count
import mesa
import mesa.time
from src.agent import TestAgent, AgentType
from src.schedule import TestScheduler
from src.payment import MOP_TYPE
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
        self._create_agents()
        self._register_listeners()


    def _create_agents(self):
        print("Creating agents")
        self._init_buyers()
        self._init_sellers()

    def _init_buyers(self):
        for i in range(2):
            new_agent = self._init_agent(AgentType.BUYER, {MOP_TYPE.H_CASH:10})
            self.scheduler.add(
                new_agent,
            )

    def _init_sellers(self):
        for i in range(2):
            new_agent = self._init_agent(AgentType.SELLER, {MOP_TYPE.H_CASH:10})
            self.scheduler.add(
                new_agent,
            )

    def _init_agent(self,
                    type: AgentType,
                    mop_holding:dict[MOP_TYPE, float]
                    ):
        agent = self.agent_constructor(
            id = next(self.unique_id_generator),
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
