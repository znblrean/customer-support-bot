import logging
import sys
<<<<<<< HEAD
from pathlib import Path

def setup_logger():
    """Configure and return a logger instance"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("customer_support")
    logger.setLevel(logging.INFO)
    
=======
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger():
    """تنظیمات logger پیشرفته"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("customer_support_bot")
    logger.setLevel(logging.INFO)
    
    # فرمت log
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
<<<<<<< HEAD
    # File handler
    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()  

cat > logger.py <<EOF
import logging
import sys
from pathlib import Path

def setup_logger(name=__name__):
    """Configure and return a logger instance"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create logs directory if not exists
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    file_handler = logging.FileHandler(logs_dir / "app.log")
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

logger = setup_logger("customer_support")
EOF
=======
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
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)
