import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger():
    """تنظیمات logger پیشرفته"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("customer_support_bot")
    logger.setLevel(logging.INFO)
    
    # فرمت log
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler برای فایل (با چرخش)
    file_handler = RotatingFileHandler(
        logs_dir / "app.log",
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    
    # Handler برای console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # اضافه کردن handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger