import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Configure logging first
if not os.path.exists("logs"):
    os.makedirs("logs")

# Set up rotating file handler
log_file = os.path.join("logs", "platform.log")
max_bytes = 10 * 1024 * 1024  # 10MB
backup_count = 5  # Keep 5 backup files

# Configure root logger with rotating file handler
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

# Clear any existing handlers
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Add rotating file handler
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=max_bytes,
    backupCount=backup_count
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
root_logger.addHandler(file_handler)

# Add console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
root_logger.addHandler(console_handler)

# Import platform configuration
from app.core.platform_config import platform

# Import other modules
from app.workflows import *
from app.agents import *
from app.tools import * 