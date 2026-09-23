import os
import logging
from logging.handlers import RotatingFileHandler
from core.config import BASE_DIR

def setup_logger(log_filename: str = "app.log") -> logging.Logger:
    """Aylanuvchi fayl log tizimini sozlash (2MB chegarasi va 3 ta arxiv nusxasi)."""
    log_path = os.path.join(BASE_DIR, log_filename)
    logger = logging.getLogger("PopTumanApp")
    logger.setLevel(logging.INFO)
    
    # Agar avval qo'shilgan handler bo'lsa, qayta qo'shmaymiz
    if not logger.handlers:
        rfh = RotatingFileHandler(log_path, maxBytes=2 * 1024 * 1024, backupCount=3, encoding="utf-8")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        rfh.setFormatter(formatter)
        logger.addHandler(rfh)
        
    return logger

logger = setup_logger()
