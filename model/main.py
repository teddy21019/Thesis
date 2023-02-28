from src.model import TestModel
from src.schedule import TestScheduler
"""
Logging configuration
"""
import logging
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('structure')
logger.setLevel(logging.DEBUG)

custom_scheduler = TestScheduler
model = TestModel(N=30, scheduler_constructor=custom_scheduler)

model.step()