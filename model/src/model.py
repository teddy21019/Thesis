from __future__ import annotations
from random import Random
import mesa
import mesa.time
from src.agent import CAgent, AgentType
from src.schedule import CScheduler

import logging
logger = logging.getLogger('structure')

from typing import (
    TYPE_CHECKING,
    Type
    )

if TYPE_CHECKING:
    SchedulerConstructor =  Type[CScheduler]


class CModel(mesa.Model):
    def __init__(self,
        N                       : int,
        scheduler_constructor   : SchedulerConstructor,
        ):
        self.random: Random
        super().__init__()
        self.scheduler = scheduler_constructor(self)
        self.unique_id_generator = (i for i in range(100_00_00_00) )
        self._create_agents()

    
    def _create_agents(self):
        logger.debug("Creating agents")
        self._init_buyers()
        self._init_sellers()
    
    def _init_buyers(self):
        for i in range(2):
            self.scheduler.add(
                CAgent(
                    id = next(self.unique_id_generator),
                    model=self,
                    type = AgentType.BUYER
                    ), 
                type=AgentType.BUYER
            )

    def _init_sellers(self):
        for i in range(2):
            self.scheduler.add(
                CAgent(
                    id = next(self.unique_id_generator),
                    model=self,
                    type = AgentType.SELLER
                    ), 
                type=AgentType.SELLER
            )



    def step(self):
        self.scheduler.step()
