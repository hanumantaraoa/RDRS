import os
import sys
from loguru import logger

def setup_logger(log_path: str):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    logger.remove()
    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level:7}</level> | <cyan>{message}</cyan>", level="INFO")
    logger.add(log_path, rotation="10 MB", retention="5 days", level="DEBUG", format="{time:YYYY-MM-DD HH:mm:ss} | {level:7} | {message}")
    return logger
