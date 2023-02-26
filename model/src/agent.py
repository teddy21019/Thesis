from __future__ import annotations
import mesa
from typing import TYPE_CHECKING
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
        super().__init__(id, model)
        self.y = 10 # need change
        self.type : AgentType = type
        
    def decide_consumption(self, *args, **kargs) -> float:
        logger.debug(f"Deciding consumptions for buyer {self.unique_id}")
        budget = self.y * 0.5
        return budget 
    
    