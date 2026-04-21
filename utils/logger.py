import logging
import sys
from utils.config import config

def setup_logging():
    logger = logging.getLogger("SolidBomber")
    logger.setLevel(config.LOG_LEVEL)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')
    
    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    
    return logger

logger = setup_logging()
