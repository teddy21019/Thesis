from src.model import CModel
from src.schedule import CScheduler 
"""
Logging configuration
"""
import logging 
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger('structure')
logger.setLevel(logging.DEBUG)

custom_scheduler = CScheduler
model = CModel(N=30, scheduler_constructor=custom_scheduler)

model.step()