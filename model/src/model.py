import mesa
import mesa.time
from typing import (
    TYPE_CHECKING,
    Type
    )

if TYPE_CHECKING:
    SchedulerConstructor =  Type[mesa.time.BaseScheduler]


class CModel(mesa.Model):
    def __init__(self,
        N                       : int,
        scheduler_constructor   : SchedulerConstructor,
        ):
        self.scheduler = scheduler_constructor(self)



    def step(self):
        self.scheduler.step()
