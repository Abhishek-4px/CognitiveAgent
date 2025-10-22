import structlog
import logging
import sys


logging.basicConfig(
    format="%(message)s",
    stream= sys.stdout,         # where to send logs
    level=logging.INFO          #Debug hidden , info warning error and criticals shown
)

logger = structlog.get_logger()