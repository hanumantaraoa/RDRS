import sys
import os
from loguru import logger

def setup_multichannel_logging():
    os.makedirs("logs", exist_ok=True)
    logger.remove()

    logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | {message}", level="INFO")
    
    logger.add("logs/system.log", rotation="5 MB", filter=lambda r: r["extra"].get("channel") == "system", level="DEBUG")
    logger.add("logs/events.log", rotation="10 MB", filter=lambda r: r["extra"].get("channel") == "events", level="DEBUG")
    logger.add("logs/alerts.log", rotation="5 MB", filter=lambda r: r["extra"].get("channel") == "alerts", level="WARNING")
    logger.add("logs/errors.log", rotation="5 MB", filter=lambda r: r["level"].name in ("ERROR", "CRITICAL"), level="ERROR")
    logger.add("logs/audit.log", rotation="5 MB", filter=lambda r: r["extra"].get("channel") == "audit", level="INFO")